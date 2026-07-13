"""Data loading helpers for RetailRocket-style event data."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


def load_events(path: str) -> pd.DataFrame:
    """Load raw clickstream events from a CSV file."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Could not find raw events at {csv_path}. "
            "Place RetailRocket-style events.csv in data/raw/ and try again."
        )

    return pd.read_csv(csv_path)


def basic_summary(df: pd.DataFrame) -> dict[str, Any]:
    """Return and print a compact summary of the raw event data."""
    summary: dict[str, Any] = {
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "columns": list(df.columns),
        "event_type_counts": (
            df["event"].value_counts(dropna=False).to_dict()
            if "event" in df.columns
            else {}
        ),
        "unique_visitors": (
            int(df["visitorid"].nunique()) if "visitorid" in df.columns else None
        ),
        "unique_items": int(df["itemid"].nunique()) if "itemid" in df.columns else None,
        "missing_values": df.isna().sum().to_dict(),
    }

    print("Data summary")
    print("------------")
    print(f"Rows: {summary['num_rows']}")
    print(f"Columns: {summary['num_columns']}")
    print(f"Column names: {summary['columns']}")
    print(f"Event type counts: {summary['event_type_counts']}")
    print(f"Unique visitors: {summary['unique_visitors']}")
    print(f"Unique items: {summary['unique_items']}")
    print(f"Missing values: {summary['missing_values']}")

    return summary
