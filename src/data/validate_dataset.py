"""Validate processed TC2 dataset outputs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.data.config import INTENT_PROXIES
from src.data.schemas import (
    NON_NULL_COLUMNS_BY_TABLE,
    REQUIRED_COLUMNS_BY_TABLE,
    target_columns_in_feature_table,
    valid_event_types,
    valid_experiment_groups,
    valid_module_types,
)


TABLE_FILES = {
    "events": "events.parquet",
    "products": "products.parquet",
    "sessions": "sessions.parquet",
    "labels": "labels.parquet",
    "homepage_impressions": "homepage_impressions.parquet",
    "splits": "splits.parquet",
    "decision_features": "decision_features.parquet",
}


def _check(results: list[dict[str, Any]], name: str, condition: bool, message: str) -> None:
    results.append(
        {
            "check": name,
            "passed": bool(condition),
            "message": "ok" if condition else message,
        }
    )


def _load_tables(data_dir: Path, results: list[dict[str, Any]]) -> dict[str, pd.DataFrame]:
    tables: dict[str, pd.DataFrame] = {}
    for table_name, filename in TABLE_FILES.items():
        path = data_dir / filename
        exists = path.exists()
        _check(results, f"{table_name}_file_exists", exists, f"Missing {path}")
        if exists:
            tables[table_name] = pd.read_parquet(path)
        else:
            tables[table_name] = pd.DataFrame()
    return tables


def validate_processed_dataset(data_dir: str | Path, raise_on_error: bool = True) -> dict[str, Any]:
    """Run automated validation checks over processed Parquet outputs."""
    directory = Path(data_dir)
    results: list[dict[str, Any]] = []
    tables = _load_tables(directory, results)

    for table_name, required_columns in REQUIRED_COLUMNS_BY_TABLE.items():
        table = tables[table_name]
        missing = [column for column in required_columns if column not in table.columns]
        _check(
            results,
            f"{table_name}_required_columns",
            not missing,
            f"{table_name} is missing columns: {missing}",
        )

        if not table.empty:
            non_null_columns = NON_NULL_COLUMNS_BY_TABLE.get(table_name, [])
            existing = [column for column in non_null_columns if column in table.columns]
            missing_counts = table[existing].isna().sum()
            bad_missing = missing_counts[missing_counts > 0].to_dict()
            _check(
                results,
                f"{table_name}_required_non_nulls",
                not bad_missing,
                f"{table_name} has missing required values: {bad_missing}",
            )

    events = tables["events"]
    if not events.empty:
        invalid_events = sorted(set(events["event_type"]).difference(valid_event_types()))
        _check(
            results,
            "valid_event_types",
            not invalid_events,
            f"Invalid event types: {invalid_events}",
        )
        _check(
            results,
            "unique_event_ids",
            events["event_id"].is_unique,
            "events.event_id must be unique.",
        )
        monotonic = (
            events.sort_values(["session_id", "event_index"], kind="mergesort")
            .groupby("session_id")["timestamp"]
            .apply(lambda values: values.is_monotonic_increasing)
            .all()
        )
        _check(
            results,
            "monotonic_timestamps_within_sessions",
            bool(monotonic),
            "Timestamps must be monotonically increasing within every session.",
        )
        valid_indexes = (
            events.sort_values(["session_id", "event_index"], kind="mergesort")
            .groupby("session_id")["event_index"]
            .apply(lambda values: list(values) == list(range(len(values))))
            .all()
        )
        _check(
            results,
            "valid_event_indexes",
            bool(valid_indexes),
            "event_index must start at 0 and increase by 1 within each session.",
        )

    splits = tables["splits"]
    if not splits.empty:
        split_counts = splits["split"].value_counts().to_dict()
        _check(
            results,
            "non_empty_train_validation_test",
            all(split_counts.get(split, 0) > 0 for split in ["train", "validation", "test"]),
            f"Expected non-empty train/validation/test splits, got {split_counts}.",
        )
        _check(
            results,
            "one_split_per_session",
            splits["session_id"].is_unique,
            "A session appears in more than one split assignment.",
        )
        known_splits = {"train", "validation", "test"}
        unknown_splits = sorted(set(splits["split"]).difference(known_splits))
        _check(
            results,
            "valid_split_names",
            not unknown_splits,
            f"Unknown split names: {unknown_splits}",
        )

    labels = tables["labels"]
    if not labels.empty:
        unknown_intents = sorted(set(labels["intent_proxy"]).difference(INTENT_PROXIES))
        _check(
            results,
            "valid_intent_proxy_values",
            not unknown_intents,
            f"Unknown intent_proxy values: {unknown_intents}",
        )

    decision_features = tables["decision_features"]
    if not decision_features.empty and not events.empty:
        merged = decision_features[["session_id", "decision_event_index", "prefix_event_count"]]
        prefix_counts = []
        for row in merged.itertuples(index=False):
            actual_count = len(
                events[
                    events["session_id"].eq(row.session_id)
                    & (events["event_index"] < row.decision_event_index)
                ]
            )
            prefix_counts.append(actual_count == row.prefix_event_count)
        _check(
            results,
            "decision_features_use_prefix_only",
            all(prefix_counts),
            "Decision features must be derived only from events before the decision index.",
        )

    for feature_table in ["events", "products", "decision_features"]:
        leaked_targets = target_columns_in_feature_table(tables[feature_table].columns)
        _check(
            results,
            f"{feature_table}_has_no_label_targets",
            not leaked_targets,
            f"{feature_table} contains target/leakage columns: {leaked_targets}",
        )

    homepage = tables["homepage_impressions"]
    if not homepage.empty:
        _check(
            results,
            "homepage_impressions_all_synthetic",
            bool(homepage["is_synthetic"].all()),
            "Every homepage impression must have is_synthetic=True.",
        )
        invalid_groups = sorted(
            set(homepage["experiment_group"]).difference(valid_experiment_groups())
        )
        _check(
            results,
            "valid_homepage_experiment_groups",
            not invalid_groups,
            f"Invalid experiment_group values: {invalid_groups}",
        )
        invalid_modules = sorted(set(homepage["module_type"]).difference(valid_module_types()))
        _check(
            results,
            "valid_homepage_module_types",
            not invalid_modules,
            f"Invalid module_type values: {invalid_modules}",
        )

    model_ready_tables = [
        "events",
        "products",
        "sessions",
        "labels",
        "homepage_impressions",
        "splits",
        "decision_features",
    ]
    visitor_leaks = [
        table_name
        for table_name in model_ready_tables
        if "visitorid" in tables[table_name].columns or "visitor_id" in tables[table_name].columns
    ]
    _check(
        results,
        "no_raw_visitor_id_in_model_ready_files",
        not visitor_leaks,
        f"Raw visitor IDs appear in model-ready tables: {visitor_leaks}",
    )

    manifest_path = directory / "dataset_manifest.json"
    if manifest_path.exists():
        with manifest_path.open("r", encoding="utf-8") as handle:
            manifest = json.load(handle)
        _check(
            results,
            "manifest_contains_seed",
            "seed" in manifest.get("config", {}),
            "dataset_manifest.json must include the deterministic seed.",
        )
    else:
        _check(
            results,
            "manifest_contains_seed",
            False,
            f"Missing {manifest_path}",
        )

    passed = all(result["passed"] for result in results)
    output = {
        "passed": passed,
        "results": results,
        "data_dir": str(directory),
    }
    if raise_on_error and not passed:
        failed = [result for result in results if not result["passed"]]
        failure_text = "\n".join(
            f"- {result['check']}: {result['message']}" for result in failed
        )
        raise ValueError(f"Dataset validation failed:\n{failure_text}")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate processed TC2 dataset outputs.")
    parser.add_argument("--data-dir", default="data/processed")
    args = parser.parse_args()

    result = validate_processed_dataset(args.data_dir, raise_on_error=False)
    print(json.dumps(result, indent=2, default=str))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
