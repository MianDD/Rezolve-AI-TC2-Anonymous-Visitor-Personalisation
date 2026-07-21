from __future__ import annotations

import pandas as pd

from src.data.sessionize import sessionize_events, validate_monotonic_sessions


def test_sessionize_creates_anonymous_sessions_and_indexes() -> None:
    events = pd.DataFrame(
        {
            "visitorid": [1, 1, 1, 1],
            "timestamp": pd.to_datetime(
                [
                    "2024-01-01 00:00:00",
                    "2024-01-01 00:05:00",
                    "2024-01-01 01:00:00",
                    "2024-01-01 01:03:00",
                ]
            ),
            "event_id": ["e1", "e2", "e3", "e4"],
            "item_id": [101, 102, 201, 202],
            "category_id": [10, 10, 20, 20],
            "event_type": ["view", "view", "view", "add_to_cart"],
            "transaction_id": [pd.NA, pd.NA, pd.NA, pd.NA],
            "source_type": ["fixture_retailrocket"] * 4,
        }
    )

    sessions = sessionize_events(events, gap_minutes=30, min_session_events=2)

    assert "visitorid" not in sessions.columns
    assert sessions["session_id"].nunique() == 2
    assert sessions.groupby("session_id")["event_index"].apply(list).tolist() == [
        [0, 1],
        [0, 1],
    ]
    assert sessions.groupby("session_id")["seconds_from_session_start"].apply(list).tolist() == [
        [0.0, 300.0],
        [0.0, 180.0],
    ]
    assert validate_monotonic_sessions(sessions)
