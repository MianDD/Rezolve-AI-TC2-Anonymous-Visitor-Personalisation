"""Legacy synthetic generator with simple repeated-category behaviour."""

from __future__ import annotations

import numpy as np
import pandas as pd


def generate_reasonable_random_sessions(
    n_sessions: int = 100,
    events_per_session: int = 6,
    n_items_per_category: int = 20,
    n_categories: int = 10,
    seed: int = 42,
) -> pd.DataFrame:
    """Generate synthetic sessions with category persistence.

    This is still simulated data and must not be presented as observed
    Retailrocket behaviour.
    """
    rng = np.random.default_rng(seed)
    rows = []
    for session_number in range(n_sessions):
        session_id = f"synthetic_reasonable_{session_number:06d}"
        start = pd.Timestamp("2024-01-01") + pd.Timedelta(minutes=session_number)
        preferred_category = int(rng.integers(1, n_categories + 1))
        for event_index in range(events_per_session):
            category_id = (
                preferred_category
                if rng.random() < 0.75
                else int(rng.integers(1, n_categories + 1))
            )
            item_offset = int(rng.integers(1, n_items_per_category + 1))
            item_id = category_id * 1000 + item_offset
            event_type = "view"
            if event_index >= 2 and rng.random() < 0.12:
                event_type = "add_to_cart"
            if event_index >= 4 and rng.random() < 0.04:
                event_type = "transaction"
            rows.append(
                {
                    "session_id": session_id,
                    "event_index": event_index,
                    "timestamp": start + pd.Timedelta(seconds=event_index * 45),
                    "item_id": item_id,
                    "category_id": category_id,
                    "event_type": event_type,
                    "source_type": "synthetic_legacy_reasonable_random",
                    "is_synthetic": True,
                }
            )
    return pd.DataFrame(rows)
