"""Synthetic homepage-impression layer for public clickstream data."""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.data.config import MODULE_TYPES, SYNTHETIC_HOMEPAGE_SOURCE_TYPE
from src.data.schemas import HOMEPAGE_IMPRESSIONS_COLUMNS


def _not_missing(value: Any) -> bool:
    return not pd.isna(value)


def _matches(next_item: Any, next_category: Any, item_id: Any, category_id: Any) -> bool:
    if _not_missing(item_id) and _not_missing(next_item) and item_id == next_item:
        return True
    if _not_missing(category_id) and _not_missing(next_category) and category_id == next_category:
        return True
    return False


def _popularity_tables(
    events: pd.DataFrame, splits: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame]:
    train_sessions = splits[splits["split"].eq("train")]["session_id"]
    train_events = events[events["session_id"].isin(train_sessions)].copy()
    if train_events.empty:
        raise ValueError("Cannot simulate homepage impressions without train events.")

    item_popularity = (
        train_events.groupby(["item_id", "category_id"], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values(["count", "item_id"], ascending=[False, True], kind="mergesort")
        .reset_index(drop=True)
    )
    category_popularity = (
        train_events.dropna(subset=["category_id"])
        .groupby("category_id")
        .size()
        .reset_index(name="count")
        .sort_values(["count", "category_id"], ascending=[False, True], kind="mergesort")
        .reset_index(drop=True)
    )
    return item_popularity, category_popularity


def _nth_popular_item(
    item_popularity: pd.DataFrame, rank_index: int, category_id: Any | None = None
) -> tuple[Any, Any]:
    candidates = item_popularity
    if category_id is not None and _not_missing(category_id):
        category_candidates = item_popularity[item_popularity["category_id"].eq(category_id)]
        if not category_candidates.empty:
            candidates = category_candidates

    if candidates.empty:
        return pd.NA, category_id if category_id is not None else pd.NA

    row = candidates.iloc[rank_index % len(candidates)]
    return row["item_id"], row["category_id"]


def _popular_category(category_popularity: pd.DataFrame) -> Any:
    if category_popularity.empty:
        return pd.NA
    return category_popularity.iloc[0]["category_id"]


def _infer_rule_based_category(prefix: pd.DataFrame, category_popularity: pd.DataFrame) -> Any:
    cart_events = prefix[prefix["event_type"].eq("add_to_cart")].dropna(
        subset=["category_id"]
    )
    if not cart_events.empty:
        return cart_events.iloc[-1]["category_id"]

    categories = prefix["category_id"].dropna()
    if not categories.empty:
        counts = categories.value_counts()
        return counts.index[0]

    return _popular_category(category_popularity)


def _impression_timestamp(session: pd.DataFrame, decision_event_index: int) -> Any:
    decision_rows = session[session["event_index"].eq(decision_event_index)]
    if not decision_rows.empty:
        return decision_rows.iloc[0]["timestamp"]
    return session.iloc[-1]["timestamp"]


def simulate_homepage_impressions(
    events: pd.DataFrame,
    labels: pd.DataFrame,
    splits: pd.DataFrame,
    seed: int = 42,
) -> pd.DataFrame:
    """Create labelled synthetic homepage module impressions.

    Module selection uses only training popularity plus current-session prefix
    events before the decision point. The simulated click label may compare the
    displayed content with the next observed event, but it is always marked as
    synthetic and must not be interpreted as observed CTR.
    """
    del seed  # Deterministic ranking rules are used; seed is kept for the CLI contract.

    if labels.empty:
        return pd.DataFrame(columns=HOMEPAGE_IMPRESSIONS_COLUMNS + ["source_type"])

    item_popularity, category_popularity = _popularity_tables(events, splits)
    label_lookup = labels.set_index("session_id")
    rows: list[dict[str, Any]] = []

    for session_id, session in events.groupby("session_id", sort=False):
        if session_id not in label_lookup.index:
            continue

        label = label_lookup.loc[session_id]
        decision_index = int(label["decision_event_index"])
        prefix = session[session["event_index"] < decision_index]
        impression_time = _impression_timestamp(session, decision_index)
        next_item = label["next_item_id"]
        next_category = label["next_category_id"]

        for rank, module_type in enumerate(MODULE_TYPES, start=1):
            item_id, category_id = _nth_popular_item(item_popularity, rank - 1)
            rows.append(
                {
                    "session_id": session_id,
                    "decision_event_index": decision_index,
                    "impression_timestamp": impression_time,
                    "experiment_group": "control",
                    "strategy": "training_global_popularity",
                    "module_id": f"{session_id}_control_{rank}",
                    "module_type": module_type,
                    "content_item_id": item_id,
                    "content_category_id": category_id,
                    "rank": rank,
                    "simulated_click": _matches(
                        next_item, next_category, item_id, category_id
                    ),
                    "is_synthetic": True,
                    "source_type": SYNTHETIC_HOMEPAGE_SOURCE_TYPE,
                }
            )

        inferred_category = _infer_rule_based_category(prefix, category_popularity)
        for rank, module_type in enumerate(MODULE_TYPES, start=1):
            item_id, category_id = _nth_popular_item(
                item_popularity, rank - 1, category_id=inferred_category
            )
            if pd.isna(category_id):
                category_id = inferred_category
            rows.append(
                {
                    "session_id": session_id,
                    "decision_event_index": decision_index,
                    "impression_timestamp": impression_time,
                    "experiment_group": "rule_based",
                    "strategy": "early_session_category_rule",
                    "module_id": f"{session_id}_rule_based_{rank}",
                    "module_type": module_type,
                    "content_item_id": item_id,
                    "content_category_id": category_id,
                    "rank": rank,
                    "simulated_click": _matches(
                        next_item, next_category, item_id, category_id
                    ),
                    "is_synthetic": True,
                    "source_type": SYNTHETIC_HOMEPAGE_SOURCE_TYPE,
                }
            )

    output = pd.DataFrame(rows)
    return output[HOMEPAGE_IMPRESSIONS_COLUMNS + ["source_type"]].sort_values(
        ["session_id", "experiment_group", "rank"], kind="mergesort"
    )
