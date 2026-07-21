"""Chronological train/validation/test splitting by session start time."""

from __future__ import annotations

import pandas as pd


def assign_time_splits(
    sessions: pd.DataFrame,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
) -> pd.DataFrame:
    """Assign one chronological split per session."""
    if sessions.empty:
        raise ValueError("Cannot split an empty sessions table.")

    ordered = sessions.sort_values(["session_start", "session_id"], kind="mergesort")
    n_sessions = len(ordered)
    if n_sessions < 3:
        raise ValueError("Need at least three sessions for non-empty train/validation/test splits.")

    train_end = int(n_sessions * train_fraction)
    validation_end = int(n_sessions * (train_fraction + validation_fraction))

    train_end = min(max(1, train_end), n_sessions - 2)
    validation_end = min(max(train_end + 1, validation_end), n_sessions - 1)

    splits = ["train"] * train_end
    splits.extend(["validation"] * (validation_end - train_end))
    splits.extend(["test"] * (n_sessions - validation_end))

    output = ordered[["session_id"]].copy()
    output["split"] = splits
    return output.reset_index(drop=True)


def filter_to_labelled_sessions(table: pd.DataFrame, labels: pd.DataFrame) -> pd.DataFrame:
    labelled_sessions = set(labels["session_id"])
    return table[table["session_id"].isin(labelled_sessions)].copy()
