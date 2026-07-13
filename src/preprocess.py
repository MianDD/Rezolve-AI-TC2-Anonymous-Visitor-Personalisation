"""Preprocessing utilities for anonymous session construction."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data_loader import load_events


REQUIRED_COLUMNS = ["timestamp", "visitorid", "event", "itemid"]


def prepare_events(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw events and sort them by visitor and time."""
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    cleaned = df.copy()
    cleaned = cleaned.dropna(subset=REQUIRED_COLUMNS)
    cleaned["timestamp"] = pd.to_datetime(
        cleaned["timestamp"], unit="ms", errors="coerce"
    )
    cleaned = cleaned.dropna(subset=["timestamp"])
    cleaned = cleaned.sort_values(["visitorid", "timestamp"], kind="mergesort")
    cleaned = cleaned.reset_index(drop=True)

    return cleaned


def create_sessions(df: pd.DataFrame, gap_minutes: int = 30) -> pd.DataFrame:
    """Create anonymous sessions using a visitor-level inactivity gap rule."""
    if df.empty:
        return df.copy()

    sessions = df.copy()
    sessions = sessions.sort_values(["visitorid", "timestamp"], kind="mergesort")
    time_gap = sessions.groupby("visitorid")["timestamp"].diff()
    new_session = time_gap.isna() | (time_gap > pd.Timedelta(minutes=gap_minutes))
    sessions["session_number"] = new_session.groupby(sessions["visitorid"]).cumsum()
    sessions["session_id"] = (
        sessions["visitorid"].astype(str)
        + "_"
        + sessions["session_number"].astype(int).astype(str)
    )

    useful_columns = [
        "session_id",
        "visitorid",
        "timestamp",
        "event",
        "itemid",
    ]
    if "transactionid" in sessions.columns:
        useful_columns.append("transactionid")
    if "category_id" in sessions.columns:
        useful_columns.append("category_id")

    return sessions[useful_columns].reset_index(drop=True)


def filter_sessions(
    df: pd.DataFrame, min_events: int = 2, max_events: int = 100
) -> pd.DataFrame:
    """Keep sessions with a reasonable number of events."""
    if df.empty:
        return df.copy()

    session_lengths = df.groupby("session_id")["session_id"].transform("size")
    filtered = df[
        (session_lengths >= min_events) & (session_lengths <= max_events)
    ].copy()

    return filtered.reset_index(drop=True)


def add_category_placeholder(df: pd.DataFrame) -> pd.DataFrame:
    """Add a temporary category column when no real item-category mapping exists."""
    sessions = df.copy()
    if "category_id" not in sessions.columns:
        # Temporary placeholder: itemid stands in for category_id until an
        # item-to-category mapping is added to the project.
        sessions["category_id"] = sessions["itemid"]

    return sessions


def prepare_processed_sessions(raw_path: str, output_path: str) -> pd.DataFrame:
    """Run the full preprocessing pipeline and save processed sessions."""
    raw_events = load_events(raw_path)
    cleaned_events = prepare_events(raw_events)
    sessions = create_sessions(cleaned_events)
    sessions = filter_sessions(sessions)
    sessions = add_category_placeholder(sessions)

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    sessions.to_csv(output_file, index=False)

    return sessions
