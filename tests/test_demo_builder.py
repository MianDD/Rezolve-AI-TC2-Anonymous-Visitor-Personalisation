from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.demo.build_demo_data import build_demo_payload, write_demo_data


def test_demo_payload_uses_processed_outputs(tmp_path: Path) -> None:
    data_dir = tmp_path / "processed"
    baseline_dir = tmp_path / "tables"
    data_dir.mkdir()
    baseline_dir.mkdir()

    events = pd.DataFrame(
        {
            "session_id": ["s1", "s1", "s1", "s1"],
            "event_index": [0, 1, 2, 3],
            "timestamp": pd.date_range("2024-01-01", periods=4, freq="min"),
            "seconds_from_session_start": [0.0, 60.0, 120.0, 180.0],
            "event_type": ["view", "view", "add_to_cart", "transaction"],
            "item_id": [10, 10, 11, 11],
            "category_id": [1, 1, 1, 1],
        }
    )
    labels = pd.DataFrame(
        {
            "session_id": ["s1"],
            "decision_event_index": [3],
            "next_item_id": [11],
            "next_category_id": [1],
            "will_add_to_cart_after_decision": [False],
            "will_purchase_after_decision": [True],
            "final_conversion_stage": ["purchase"],
            "intent_proxy": ["purchase_intent"],
        }
    )
    features = pd.DataFrame(
        {
            "session_id": ["s1"],
            "decision_event_index": [3],
            "decision_timestamp": [pd.Timestamp("2024-01-01 00:03:00")],
            "prefix_event_count": [3],
            "prefix_view_count": [2],
            "prefix_add_to_cart_count": [1],
            "prefix_unique_items": [2],
            "prefix_unique_categories": [1],
            "first_item_id": [10],
            "first_category_id": [1],
            "last_item_id": [11],
            "last_category_id": [1],
            "most_frequent_category_id": [1],
            "seconds_from_session_start": [180.0],
            "source_type": ["fixture_retailrocket"],
        }
    )
    homepage = pd.DataFrame(
        {
            "session_id": ["s1", "s1"],
            "experiment_group": ["control", "rule_based"],
            "strategy": ["training_global_popularity", "early_session_category_rule"],
            "module_type": ["hero_banner", "hero_banner"],
            "content_item_id": [10, 11],
            "content_category_id": [1, 1],
            "rank": [1, 1],
            "simulated_click": [False, True],
            "is_synthetic": [True, True],
        }
    )
    splits = pd.DataFrame({"session_id": ["s1"], "split": ["test"]})

    events.to_parquet(data_dir / "events.parquet", index=False)
    labels.to_parquet(data_dir / "labels.parquet", index=False)
    features.to_parquet(data_dir / "decision_features.parquet", index=False)
    homepage.to_parquet(data_dir / "homepage_impressions.parquet", index=False)
    splits.to_parquet(data_dir / "splits.parquet", index=False)

    payload = build_demo_payload(data_dir=data_dir, baseline_dir=baseline_dir, max_sessions=1)

    assert payload["session_count"] == 1
    assert payload["sessions"][0]["session_id"] == "s1"
    assert payload["sessions"][0]["prefix"][0]["item_id"] == 10
    assert payload["sessions"][0]["next_event"]["event_type"] == "transaction"
    assert payload["sessions"][0]["impressions"][1]["is_synthetic"] is True

    output = write_demo_data(payload, tmp_path / "demo_data.js")
    assert output.read_text(encoding="utf-8").startswith("window.TC2_DEMO_DATA = ")
