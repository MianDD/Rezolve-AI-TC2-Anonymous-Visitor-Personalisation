"""Legacy pure-random synthetic session generator."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_pure_random_sessions(
    n_sessions: int = 100,
    events_per_session: int = 5,
    n_items: int = 50,
    n_categories: int = 10,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate random sessions with no behavioural realism claims."""
    rng = np.random.default_rng(seed)
    rows = []
    for session_number in range(n_sessions):
        session_id = f"synthetic_random_{session_number:06d}"
        start = pd.Timestamp("2024-01-01") + pd.Timedelta(minutes=session_number)
        for event_index in range(events_per_session):
            item_id = int(rng.integers(1, n_items + 1))
            rows.append(
                {
                    "session_id": session_id,
                    "event_index": event_index,
                    "timestamp": start + pd.Timedelta(seconds=event_index * 30),
                    "item_id": item_id,
                    "category_id": int(rng.integers(1, n_categories + 1)),
                    "event_type": rng.choice(["view", "add_to_cart", "transaction"], p=[0.9, 0.08, 0.02]),
                    "source_type": "synthetic_legacy_pure_random",
                    "is_synthetic": True,
                }
            )
    return pd.DataFrame(rows)
