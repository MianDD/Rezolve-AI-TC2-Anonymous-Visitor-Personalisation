"""Build session-level summary table."""

from __future__ import annotations

import pandas as pd

from src.data.schemas import SESSIONS_COLUMNS


def build_sessions(events: pd.DataFrame) -> pd.DataFrame:
    """Aggregate processed event rows into sessions.parquet."""
    if events.empty:
        return pd.DataFrame(columns=SESSIONS_COLUMNS)

    ordered = events.sort_values(["session_id", "event_index"], kind="mergesort")
    grouped = ordered.groupby("session_id", sort=False)

    sessions = grouped.agg(
        session_start=("timestamp", "min"),
        session_end=("timestamp", "max"),
        number_of_events=("event_id", "count"),
        number_of_views=("event_type", lambda values: int((values == "view").sum())),
        number_of_add_to_cart_events=(
            "event_type",
            lambda values: int((values == "add_to_cart").sum()),
        ),
        number_of_transactions=(
            "event_type",
            lambda values: int((values == "transaction").sum()),
        ),
        number_of_unique_items=("item_id", "nunique"),
        number_of_unique_categories=("category_id", "nunique"),
        first_item_id=("item_id", lambda values: values.iloc[0]),
        first_category_id=("category_id", lambda values: values.iloc[0]),
        last_item_id=("item_id", lambda values: values.iloc[-1]),
        last_category_id=("category_id", lambda values: values.iloc[-1]),
        source_type=("source_type", "first"),
    ).reset_index()

    sessions["session_duration_seconds"] = (
        sessions["session_end"] - sessions["session_start"]
    ).dt.total_seconds()
    sessions["converted"] = sessions["number_of_transactions"] > 0

    sessions = sessions.sort_values(["session_start", "session_id"], kind="mergesort")
    return sessions[SESSIONS_COLUMNS].reset_index(drop=True)
