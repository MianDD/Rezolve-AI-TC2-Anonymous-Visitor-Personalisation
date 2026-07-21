from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data.config import DatasetConfig, TARGET_COLUMNS
from src.data.prepare_dataset import prepare_dataset


def test_fixture_pipeline_has_no_decision_feature_leakage(tmp_path: Path) -> None:
    result = prepare_dataset(
        DatasetConfig(
            source="fixture",
            raw_dir=Path("data/fixtures/retailrocket"),
            output_dir=tmp_path / "processed",
            report_path=tmp_path / "dataset_summary.md",
            seed=42,
        )
    )
    tables = result["tables"]

    for table_name in [
        "events",
        "products",
        "sessions",
        "labels",
        "homepage_impressions",
        "splits",
        "decision_features",
    ]:
        assert "visitorid" not in tables[table_name].columns
        assert "visitor_id" not in tables[table_name].columns

    feature_columns = set(tables["decision_features"].columns)
    assert feature_columns.isdisjoint(TARGET_COLUMNS)
    assert "intent_proxy" not in tables["events"].columns
    assert "intent_proxy" not in tables["products"].columns

    events = tables["events"]
    decision_features = tables["decision_features"]
    for row in decision_features.itertuples(index=False):
        prefix = events[
            events["session_id"].eq(row.session_id)
            & (events["event_index"] < row.decision_event_index)
        ]
        assert len(prefix) == row.prefix_event_count
        assert row.last_item_id == prefix.iloc[-1]["item_id"]


def test_outputs_are_deterministic_for_same_seed(tmp_path: Path) -> None:
    first = prepare_dataset(
        DatasetConfig(
            source="fixture",
            raw_dir=Path("data/fixtures/retailrocket"),
            output_dir=tmp_path / "first",
            report_path=tmp_path / "first_report.md",
            seed=42,
        )
    )
    second = prepare_dataset(
        DatasetConfig(
            source="fixture",
            raw_dir=Path("data/fixtures/retailrocket"),
            output_dir=tmp_path / "second",
            report_path=tmp_path / "second_report.md",
            seed=42,
        )
    )

    for table_name in [
        "events",
        "products",
        "sessions",
        "labels",
        "decision_features",
        "homepage_impressions",
        "splits",
    ]:
        pd.testing.assert_frame_equal(
            first["tables"][table_name].reset_index(drop=True),
            second["tables"][table_name].reset_index(drop=True),
        )
