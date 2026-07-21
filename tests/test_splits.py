from __future__ import annotations

import pandas as pd

from src.data.split_dataset import assign_time_splits


def test_assign_time_splits_is_chronological_and_non_overlapping() -> None:
    sessions = pd.DataFrame(
        {
            "session_id": [f"s_{index:02d}" for index in range(10)],
            "session_start": pd.date_range("2024-01-01", periods=10, freq="h"),
        }
    )

    splits = assign_time_splits(sessions)

    assert splits["session_id"].is_unique
    assert splits["split"].value_counts().to_dict() == {
        "train": 7,
        "validation": 1,
        "test": 2,
    }
    assert splits.iloc[:7]["split"].eq("train").all()
    assert splits.iloc[7:8]["split"].eq("validation").all()
    assert splits.iloc[8:]["split"].eq("test").all()
