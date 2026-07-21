"""Build item/product metadata from Retailrocket item properties."""

from __future__ import annotations

import json

import pandas as pd

from src.data.config import REAL_SOURCE_TYPE
from src.data.schemas import PRODUCTS_COLUMNS


CORE_PROPERTIES = {"categoryid", "available", "price"}


def _latest_property(
    item_properties: pd.DataFrame, property_name: str, output_name: str
) -> pd.DataFrame:
    values = item_properties[item_properties["property_lower"].eq(property_name)].copy()
    if values.empty:
        return pd.DataFrame(columns=["item_id", output_name])
    values = values.sort_values(["item_id", "timestamp"], kind="mergesort")
    latest = values.groupby("item_id", as_index=False).tail(1)
    return latest[["item_id", "value"]].rename(columns={"value": output_name})


def _selected_item_properties(item_properties: pd.DataFrame, max_properties: int = 8) -> pd.DataFrame:
    non_core = item_properties[
        ~item_properties["property_lower"].isin(CORE_PROPERTIES)
    ].copy()
    if non_core.empty:
        return pd.DataFrame(columns=["item_id", "selected_item_properties"])

    non_core = non_core.sort_values(
        ["item_id", "property_lower", "timestamp"], kind="mergesort"
    )
    latest = non_core.groupby(["item_id", "property_lower"], as_index=False).tail(1)

    rows = []
    for item_id, group in latest.groupby("item_id", sort=True):
        selected = (
            group.sort_values("property_lower")
            .head(max_properties)
            .set_index("property_lower")["value"]
            .astype(str)
            .to_dict()
        )
        rows.append(
            {
                "item_id": item_id,
                "selected_item_properties": json.dumps(selected, sort_keys=True),
            }
        )
    return pd.DataFrame(rows)


def build_products(
    events: pd.DataFrame,
    item_properties: pd.DataFrame,
    category_tree: pd.DataFrame,
    source_type: str = REAL_SOURCE_TYPE,
) -> pd.DataFrame:
    """Create products.parquet rows from available item metadata.

    Missing category, availability and price values are preserved as missing
    rather than guessed.
    """
    event_items = events[["item_id"]].drop_duplicates()
    property_items = (
        item_properties[["item_id"]].drop_duplicates()
        if not item_properties.empty
        else pd.DataFrame(columns=["item_id"])
    )
    products = pd.concat([event_items, property_items], ignore_index=True).drop_duplicates()

    if item_properties.empty:
        products["category_id"] = pd.Series(pd.NA, index=products.index, dtype="Int64")
        products["available"] = pd.NA
        products["price"] = pd.NA
        products["selected_item_properties"] = "{}"
    else:
        category = _latest_property(item_properties, "categoryid", "category_id")
        available = _latest_property(item_properties, "available", "available")
        price = _latest_property(item_properties, "price", "price")
        selected = _selected_item_properties(item_properties)

        products = products.merge(category, on="item_id", how="left")
        products = products.merge(available, on="item_id", how="left")
        products = products.merge(price, on="item_id", how="left")
        products = products.merge(selected, on="item_id", how="left")
        products["selected_item_properties"] = products["selected_item_properties"].fillna(
            "{}"
        )

    products["category_id"] = pd.to_numeric(
        products.get("category_id"), errors="coerce"
    ).astype("Int64")
    products["available"] = pd.to_numeric(
        products.get("available"), errors="coerce"
    ).astype("Int64")
    products["price"] = pd.to_numeric(products.get("price"), errors="coerce")

    if category_tree.empty:
        products["parent_category_id"] = pd.Series(pd.NA, index=products.index, dtype="Int64")
    else:
        products = products.merge(category_tree, on="category_id", how="left")

    products["source_type"] = source_type
    products = products.sort_values("item_id", kind="mergesort").reset_index(drop=True)
    return products[PRODUCTS_COLUMNS]
