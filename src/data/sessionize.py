"""Anonymous session construction for Retailrocket visitor streams."""

from __future__ import annotations

import pandas as pd


def validate_monotonic_sessions(events: pd.DataFrame) -> bool:
    """Return True when timestamps are monotonically increasing per session."""
    if events.empty:
        return True
    ordered = events.sort_values(["session_id", "event_index"], kind="mergesort")
    return bool(
        ordered.groupby("session_id")["timestamp"]
        .apply(lambda values: values.is_monotonic_increasing)
        .all()
    )


def sessionize_events(
    events: pd.DataFrame,
    gap_minutes: int = 30,
    min_session_events: int = 2,
) -> pd.DataFrame:
    """Create anonymous sessions using an inactivity-gap rule.

    The raw `visitorid` is used only to construct sessions and is removed from
    the returned model-ready event table.
    """
    required = {"visitorid", "timestamp", "event_id", "item_id", "event_type"}
    missing = sorted(required.difference(events.columns))
    if missing:
        raise ValueError(f"Cannot sessionize events; missing columns: {missing}")

    if events.empty:
        return pd.DataFrame()

    working = events.copy().sort_values(["visitorid", "timestamp"], kind="mergesort")
    time_gap = working.groupby("visitorid")["timestamp"].diff()
    new_session = time_gap.isna() | (time_gap > pd.Timedelta(minutes=gap_minutes))
    working["_visitor_session_number"] = new_session.groupby(working["visitorid"]).cumsum()
    working["_internal_session_key"] = (
        working["visitorid"].astype(str)
        + "::"
        + working["_visitor_session_number"].astype(int).astype(str)
    )

    session_sizes = working.groupby("_internal_session_key")["_internal_session_key"].transform(
        "size"
    )
    working = working[session_sizes >= min_session_events].copy()
    if working.empty:
        return pd.DataFrame()

    session_order = (
        working.groupby("_internal_session_key")
        .agg(session_start=("timestamp", "min"))
        .reset_index()
        .sort_values(["session_start", "_internal_session_key"], kind="mergesort")
    )
    session_order["session_id"] = [
        f"s_{index:08d}" for index in range(len(session_order))
    ]
    working = working.merge(session_order, on="_internal_session_key", how="left")
    working = working.sort_values(["session_id", "timestamp"], kind="mergesort")
    working["event_index"] = working.groupby("session_id").cumcount()
    working["seconds_from_session_start"] = (
        working["timestamp"] - working["session_start"]
    ).dt.total_seconds()

    if "transaction_id" not in working.columns:
        working["transaction_id"] = pd.NA
    if "category_id" not in working.columns:
        working["category_id"] = pd.Series(pd.NA, index=working.index, dtype="Int64")

    output_columns = [
        "session_id",
        "event_id",
        "event_index",
        "timestamp",
        "seconds_from_session_start",
        "item_id",
        "category_id",
        "event_type",
        "transaction_id",
        "source_type",
    ]
    output = working[output_columns].reset_index(drop=True)
    if not validate_monotonic_sessions(output):
        raise ValueError("Timestamps are not monotonically increasing within sessions.")

    return output


def sample_complete_sessions(
    events: pd.DataFrame,
    max_sessions: int | None = None,
    max_events: int | None = None,
    strategy: str = "evenly_spaced",
) -> pd.DataFrame:
    """Deterministically sample whole sessions without cutting a session midway."""
    if events.empty or (max_sessions is None and max_events is None):
        return events.copy()

    session_order = (
        events.groupby("session_id")
        .agg(session_start=("timestamp", "min"), number_of_events=("event_id", "count"))
        .reset_index()
        .sort_values(["session_start", "session_id"], kind="mergesort")
    )

    if strategy not in {"first", "evenly_spaced"}:
        raise ValueError("strategy must be one of: first, evenly_spaced")

    if strategy == "evenly_spaced" and max_sessions is not None:
        n_sessions = len(session_order)
        if max_sessions >= n_sessions:
            candidate_order = session_order
        elif max_sessions <= 1:
            candidate_order = session_order.head(max_sessions)
        else:
            raw_positions = [
                round(index * (n_sessions - 1) / (max_sessions - 1))
                for index in range(max_sessions)
            ]
            positions: list[int] = []
            used = set()
            for position in raw_positions:
                position = int(position)
                while position in used and position + 1 < n_sessions:
                    position += 1
                if position not in used:
                    positions.append(position)
                    used.add(position)
            candidate_order = session_order.iloc[positions].sort_values(
                ["session_start", "session_id"], kind="mergesort"
            )
    else:
        candidate_order = session_order

    selected: list[str] = []
    total_events = 0
    for row in candidate_order.itertuples(index=False):
        if max_sessions is not None and len(selected) >= max_sessions:
            break
        if max_events is not None and selected and total_events + row.number_of_events > max_events:
            break
        if max_events is not None and not selected and row.number_of_events > max_events:
            selected.append(row.session_id)
            break
        selected.append(row.session_id)
        total_events += row.number_of_events

    sampled = events[events["session_id"].isin(selected)].copy()
    return sampled.sort_values(["session_id", "event_index"], kind="mergesort").reset_index(
        drop=True
    )
