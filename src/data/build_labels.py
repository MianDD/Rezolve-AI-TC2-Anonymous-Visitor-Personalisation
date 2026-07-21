"""Build leakage-safe labels and decision-time features."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.data.config import INTENT_PROXIES
from src.data.schemas import DECISION_FEATURES_COLUMNS, LABELS_COLUMNS


def _first_non_null(values: pd.Series) -> Any:
    non_null = values.dropna()
    return non_null.iloc[0] if not non_null.empty else pd.NA


def _last_non_null(values: pd.Series) -> Any:
    non_null = values.dropna()
    return non_null.iloc[-1] if not non_null.empty else pd.NA


def _mode_or_missing(values: pd.Series) -> Any:
    non_null = values.dropna()
    if non_null.empty:
        return pd.NA
    counts = non_null.value_counts()
    return counts.index[0]


def derive_intent_proxy(prefix: pd.DataFrame, future: pd.DataFrame) -> str:
    """Derive a weak behavioural intent proxy for evaluation only.

    The label is stored only in labels.parquet:
    - purchase_intent: a transaction occurs after the decision point;
    - cart_intent: an add-to-cart occurs after the decision point;
    - product_focused: no future cart/purchase, but early behaviour revisits
      the same item or category;
    - browsing: none of the above.
    """
    future_events = set(future["event_type"])
    if "transaction" in future_events:
        return "purchase_intent"
    if "add_to_cart" in future_events:
        return "cart_intent"

    repeated_item = prefix["item_id"].duplicated().any()
    categories = prefix["category_id"].dropna()
    repeated_category = categories.duplicated().any()
    if repeated_item or repeated_category:
        return "product_focused"
    return "browsing"


def final_conversion_stage(future: pd.DataFrame) -> str:
    future_events = set(future["event_type"])
    if "transaction" in future_events:
        return "purchase"
    if "add_to_cart" in future_events:
        return "add_to_cart"
    return "browse"


def build_labels_and_decision_features(
    events: pd.DataFrame, decision_event_index: int = 3
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create labels and decision-time input features.

    Features use only events with event_index < decision_event_index. Labels use
    the next/future events and must not be merged into model input tables.
    """
    label_rows: list[dict[str, Any]] = []
    feature_rows: list[dict[str, Any]] = []

    for session_id, session in events.groupby("session_id", sort=False):
        session = session.sort_values("event_index", kind="mergesort").reset_index(drop=True)
        if len(session) <= decision_event_index:
            continue

        prefix = session[session["event_index"] < decision_event_index]
        future = session[session["event_index"] >= decision_event_index]
        next_event = session.loc[session["event_index"].eq(decision_event_index)].iloc[0]

        will_add_to_cart = bool((future["event_type"] == "add_to_cart").any())
        will_purchase = bool((future["event_type"] == "transaction").any())
        intent_proxy = derive_intent_proxy(prefix, future)
        if intent_proxy not in INTENT_PROXIES:
            raise ValueError(f"Unexpected intent proxy: {intent_proxy}")

        label_rows.append(
            {
                "session_id": session_id,
                "decision_event_index": decision_event_index,
                "next_item_id": next_event["item_id"],
                "next_category_id": next_event["category_id"],
                "will_add_to_cart_after_decision": will_add_to_cart,
                "will_purchase_after_decision": will_purchase,
                "final_conversion_stage": final_conversion_stage(future),
                "intent_proxy": intent_proxy,
            }
        )

        feature_rows.append(
            {
                "session_id": session_id,
                "decision_event_index": decision_event_index,
                "decision_timestamp": next_event["timestamp"],
                "prefix_event_count": len(prefix),
                "prefix_view_count": int((prefix["event_type"] == "view").sum()),
                "prefix_add_to_cart_count": int(
                    (prefix["event_type"] == "add_to_cart").sum()
                ),
                "prefix_unique_items": int(prefix["item_id"].nunique()),
                "prefix_unique_categories": int(prefix["category_id"].nunique()),
                "first_item_id": _first_non_null(prefix["item_id"]),
                "first_category_id": _first_non_null(prefix["category_id"]),
                "last_item_id": _last_non_null(prefix["item_id"]),
                "last_category_id": _last_non_null(prefix["category_id"]),
                "most_frequent_category_id": _mode_or_missing(prefix["category_id"]),
                "seconds_from_session_start": next_event["seconds_from_session_start"],
                "source_type": next_event["source_type"],
            }
        )

    labels = pd.DataFrame(label_rows, columns=LABELS_COLUMNS)
    decision_features = pd.DataFrame(feature_rows, columns=DECISION_FEATURES_COLUMNS)
    return labels, decision_features
