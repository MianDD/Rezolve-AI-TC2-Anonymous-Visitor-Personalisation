"""Load and normalise Retailrocket-style raw files."""

from __future__ import annotations

from pathlib import Path
from typing import NamedTuple

import pandas as pd

from src.data.config import EVENT_TYPE_MAP, EXPECTED_RETAILROCKET_FILES


class RetailrocketRawData(NamedTuple):
    events: pd.DataFrame
    item_properties: pd.DataFrame
    category_tree: pd.DataFrame
    missing_metadata_files: list[str]


def _read_csv_if_exists(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def _normalise_timestamp(series: pd.Series) -> pd.Series:
    if pd.api.types.is_numeric_dtype(series):
        return pd.to_datetime(series, unit="ms", errors="coerce")
    return pd.to_datetime(series, errors="coerce")


def load_raw_retailrocket(raw_dir: str | Path) -> RetailrocketRawData:
    """Load Retailrocket CSV files from a directory.

    `events.csv` is required. Item property and category files are optional so
    local development can still run with a minimal fixture, but missing metadata
    is returned and surfaced in the report.
    """
    directory = Path(raw_dir)
    events_path = directory / "events.csv"
    if not events_path.exists():
        expected = ", ".join(EXPECTED_RETAILROCKET_FILES)
        raise FileNotFoundError(
            f"Missing Retailrocket events file: {events_path}. "
            f"Expected files in {directory}: {expected}. "
            "Download from Kaggle or use --source fixture for local tests."
        )

    events = pd.read_csv(events_path)
    part1_path = directory / "item_properties_part1.csv"
    part2_path = directory / "item_properties_part2.csv"
    part1 = _read_csv_if_exists(part1_path)
    part2 = _read_csv_if_exists(part2_path)
    item_properties = pd.concat([part1, part2], ignore_index=True)
    category_tree = _read_csv_if_exists(directory / "category_tree.csv")

    missing_metadata = [
        filename
        for filename in EXPECTED_RETAILROCKET_FILES[1:]
        if not (directory / filename).exists()
    ]

    return RetailrocketRawData(events, item_properties, category_tree, missing_metadata)


def normalise_event_types(events: pd.DataFrame) -> pd.Series:
    normalised = events["event"].astype(str).str.strip().str.lower().map(EVENT_TYPE_MAP)
    return normalised


def normalise_events(raw_events: pd.DataFrame, source_type: str) -> pd.DataFrame:
    """Normalise Retailrocket event rows while retaining visitorid internally."""
    required = {"timestamp", "visitorid", "event", "itemid"}
    missing = sorted(required.difference(raw_events.columns))
    if missing:
        raise ValueError(f"Retailrocket events.csv is missing required columns: {missing}")

    events = raw_events.copy()
    events["_raw_row_number"] = range(len(events))
    events["timestamp"] = _normalise_timestamp(events["timestamp"])
    events["event_type"] = normalise_event_types(events)
    events = events.dropna(subset=["timestamp", "visitorid", "event_type", "itemid"])

    if "transactionid" not in events.columns:
        events["transactionid"] = pd.NA

    events = events.rename(
        columns={
            "itemid": "item_id",
            "transactionid": "transaction_id",
        }
    )
    events["item_id"] = pd.to_numeric(events["item_id"], errors="coerce").astype("Int64")
    events = events.dropna(subset=["item_id"])
    events["event_id"] = (
        "rr_evt_" + events["_raw_row_number"].astype(int).astype(str).str.zfill(10)
    )
    events["source_type"] = source_type

    columns = [
        "visitorid",
        "timestamp",
        "event_id",
        "item_id",
        "event_type",
        "transaction_id",
        "source_type",
    ]
    return events[columns].sort_values(["visitorid", "timestamp"], kind="mergesort")


def normalise_item_properties(raw_properties: pd.DataFrame) -> pd.DataFrame:
    """Normalise Retailrocket item property rows."""
    if raw_properties.empty:
        return pd.DataFrame(
            columns=["timestamp", "item_id", "property", "value", "property_lower"]
        )

    required = {"timestamp", "itemid", "property", "value"}
    missing = sorted(required.difference(raw_properties.columns))
    if missing:
        raise ValueError(
            f"Retailrocket item_properties files are missing columns: {missing}"
        )

    properties = raw_properties.copy()
    properties["timestamp"] = _normalise_timestamp(properties["timestamp"])
    properties = properties.rename(columns={"itemid": "item_id"})
    properties["item_id"] = pd.to_numeric(properties["item_id"], errors="coerce").astype(
        "Int64"
    )
    properties = properties.dropna(subset=["timestamp", "item_id", "property"])
    properties["property_lower"] = properties["property"].astype(str).str.lower()
    return properties[["timestamp", "item_id", "property", "value", "property_lower"]]


def normalise_category_tree(raw_category_tree: pd.DataFrame) -> pd.DataFrame:
    """Normalise Retailrocket category tree columns."""
    if raw_category_tree.empty:
        return pd.DataFrame(columns=["category_id", "parent_category_id"])

    category_tree = raw_category_tree.copy()
    rename_map = {}
    if "categoryid" in category_tree.columns:
        rename_map["categoryid"] = "category_id"
    if "parentid" in category_tree.columns:
        rename_map["parentid"] = "parent_category_id"
    category_tree = category_tree.rename(columns=rename_map)

    if "category_id" not in category_tree.columns:
        raise ValueError("category_tree.csv must contain categoryid or category_id.")
    if "parent_category_id" not in category_tree.columns:
        category_tree["parent_category_id"] = pd.NA

    category_tree["category_id"] = pd.to_numeric(
        category_tree["category_id"], errors="coerce"
    ).astype("Int64")
    category_tree["parent_category_id"] = pd.to_numeric(
        category_tree["parent_category_id"], errors="coerce"
    ).astype("Int64")
    return category_tree[["category_id", "parent_category_id"]].drop_duplicates()


def attach_event_categories(
    events: pd.DataFrame, item_properties: pd.DataFrame
) -> pd.DataFrame:
    """Attach category_id known at or before each event timestamp.

    This avoids using future item-category changes for historical events.
    """
    output = events.copy()
    category_history = item_properties[
        item_properties["property_lower"].eq("categoryid")
    ].copy()

    if category_history.empty:
        output["category_id"] = pd.Series(pd.NA, index=output.index, dtype="Int64")
        return output

    category_history["category_id"] = pd.to_numeric(
        category_history["value"], errors="coerce"
    ).astype("Int64")
    category_history = category_history.dropna(subset=["category_id"])
    category_history = category_history.sort_values(
        ["item_id", "timestamp"], kind="mergesort"
    )

    left = output.sort_values(["item_id", "timestamp"], kind="mergesort")
    right = category_history[["item_id", "timestamp", "category_id"]]

    try:
        merged = pd.merge_asof(
            left,
            right,
            by="item_id",
            on="timestamp",
            direction="backward",
        )
    except ValueError:
        pieces = []
        for item_id, item_events in left.groupby("item_id", sort=False):
            item_history = right[right["item_id"].eq(item_id)]
            if item_history.empty:
                item_copy = item_events.copy()
                item_copy["category_id"] = pd.NA
            else:
                item_copy = pd.merge_asof(
                    item_events.sort_values("timestamp"),
                    item_history.sort_values("timestamp"),
                    on="timestamp",
                    direction="backward",
                )
                item_copy["item_id"] = item_id
            pieces.append(item_copy)
        merged = pd.concat(pieces, ignore_index=True)

    merged["category_id"] = pd.to_numeric(
        merged["category_id"], errors="coerce"
    ).astype("Int64")
    return merged.sort_values(["visitorid", "timestamp"], kind="mergesort")


def load_and_prepare_raw(raw_dir: str | Path, source_type: str) -> RetailrocketRawData:
    """Load raw files and normalise all available Retailrocket tables."""
    raw = load_raw_retailrocket(raw_dir)
    events = normalise_events(raw.events, source_type=source_type)
    item_properties = normalise_item_properties(raw.item_properties)
    category_tree = normalise_category_tree(raw.category_tree)
    events = attach_event_categories(events, item_properties)
    return RetailrocketRawData(
        events=events,
        item_properties=item_properties,
        category_tree=category_tree,
        missing_metadata_files=raw.missing_metadata_files,
    )
