"""Prepare reproducible TC2 anonymous homepage personalisation datasets."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from src.data.build_labels import build_labels_and_decision_features
from src.data.build_products import build_products
from src.data.build_sessions import build_sessions
from src.data.config import DatasetConfig, VALID_SAMPLE_STRATEGIES, VALID_SOURCES
from src.data.load_retailrocket import (
    attach_event_categories,
    load_category_tree,
    load_item_properties_for_items,
    load_raw_events,
    normalise_category_tree,
    normalise_events,
    normalise_item_properties,
)
from src.data.schemas import REQUIRED_COLUMNS_BY_TABLE
from src.data.sessionize import sample_complete_sessions, sessionize_events
from src.data.simulate_homepage import simulate_homepage_impressions
from src.data.split_dataset import assign_time_splits
from src.data.validate_dataset import validate_processed_dataset


OUTPUT_TABLES = {
    "events": "events.parquet",
    "products": "products.parquet",
    "sessions": "sessions.parquet",
    "labels": "labels.parquet",
    "decision_features": "decision_features.parquet",
    "homepage_impressions": "homepage_impressions.parquet",
    "splits": "splits.parquet",
}


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_parquet(table: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_parquet(path, index=False)


def _load_and_sessionize_events(config: DatasetConfig) -> tuple[pd.DataFrame, int]:
    """Load events, create sessions, and apply deterministic complete-session sampling."""
    raw_events = load_raw_events(config.raw_dir)
    raw_event_count = len(raw_events)
    events = normalise_events(raw_events, source_type=config.source_type)
    sessionized = sessionize_events(
        events,
        gap_minutes=config.session_gap_minutes,
        min_session_events=config.min_session_events,
    )
    sampled = sample_complete_sessions(
        sessionized,
        max_sessions=config.max_sessions,
        max_events=config.max_events,
        strategy=config.sample_strategy,
    )
    return sampled, raw_event_count


def _load_metadata_for_events(
    config: DatasetConfig, events: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    """Load item metadata for the event items retained in the dataset."""
    item_ids = events["item_id"].dropna().unique()
    raw_properties, missing_properties = load_item_properties_for_items(
        config.raw_dir,
        item_ids=item_ids,
    )
    category_tree_path = config.raw_dir / "category_tree.csv"
    missing_metadata = list(missing_properties)
    if not category_tree_path.exists():
        missing_metadata.append("category_tree.csv")

    item_properties = normalise_item_properties(raw_properties)
    category_tree = normalise_category_tree(load_category_tree(config.raw_dir))
    return item_properties, category_tree, missing_metadata


def _session_length_distribution(sessions: pd.DataFrame) -> dict[str, float]:
    if sessions.empty:
        return {}
    lengths = sessions["number_of_events"]
    return {
        "min": float(lengths.min()),
        "p25": float(lengths.quantile(0.25)),
        "median": float(lengths.median()),
        "p75": float(lengths.quantile(0.75)),
        "max": float(lengths.max()),
    }


def _missing_summary(tables: dict[str, pd.DataFrame]) -> dict[str, dict[str, int]]:
    return {
        table_name: {
            column: int(count)
            for column, count in table.isna().sum().items()
            if int(count) > 0
        }
        for table_name, table in tables.items()
    }


def _format_dict(values: dict[str, Any]) -> str:
    if not values:
        return "- none\n"
    return "".join(f"- {key}: {value}\n" for key, value in values.items())


def generate_dataset_report(
    report_path: str | Path,
    config: DatasetConfig,
    raw_event_count: int,
    missing_metadata_files: list[str],
    tables: dict[str, pd.DataFrame],
    validation: dict[str, Any],
) -> None:
    """Write reports/dataset_summary.md."""
    report = Path(report_path)
    report.parent.mkdir(parents=True, exist_ok=True)

    events = tables["events"]
    sessions = tables["sessions"]
    splits = tables["splits"]
    homepage = tables["homepage_impressions"]

    event_counts = events["event_type"].value_counts().to_dict() if not events.empty else {}
    split_counts = splits["split"].value_counts().to_dict() if not splits.empty else {}
    conversion_rate = (
        float(sessions["converted"].mean()) if not sessions.empty else 0.0
    )
    cart_rate = (
        float((sessions["number_of_add_to_cart_events"] > 0).mean())
        if not sessions.empty
        else 0.0
    )
    validation_lines = "\n".join(
        f"- [{'x' if row['passed'] else ' '}] {row['check']}: {row['message']}"
        for row in validation["results"]
    )

    content = f"""# Dataset Summary

## Source Dataset

- Source: {config.source}
- Source type in event tables: {config.source_type}
- Retailrocket files expected in: `{config.raw_dir}`
- Missing metadata files during this run: {missing_metadata_files or "none"}
- Processing date: {datetime.now(timezone.utc).isoformat()}

Retailrocket is a public e-commerce behavioural dataset distributed through Kaggle. Follow Kaggle's dataset page for attribution and licence requirements before using the full dataset in shared or commercial work.

## Configuration

```json
{json.dumps(config.to_dict(), indent=2)}
```

## Volumes

- Raw event rows loaded: {raw_event_count}
- Retained event rows: {len(events)}
- Retained sessions: {len(sessions)}
- Unique items: {int(events["item_id"].nunique()) if not events.empty else 0}
- Unique categories: {int(events["category_id"].nunique()) if not events.empty else 0}
- Synthetic homepage impressions: {len(homepage)}

## Event-Type Counts

{_format_dict(event_counts)}
## Session Length Distribution

{_format_dict(_session_length_distribution(sessions))}
## Conversion Rates

- Session conversion rate: {conversion_rate:.4f}
- Session add-to-cart rate: {cart_rate:.4f}

## Train/Validation/Test Sizes

{_format_dict(split_counts)}
## Missing-Value Summary

```json
{json.dumps(_missing_summary(tables), indent=2, default=str)}
```

## Output Schemas

{json.dumps(REQUIRED_COLUMNS_BY_TABLE, indent=2)}

## Validation Results

{validation_lines}

## Intent Proxy Derivation

- `purchase_intent`: a transaction occurs after the decision point.
- `cart_intent`: no future transaction, but an add-to-cart occurs after the decision point.
- `product_focused`: no future cart or purchase, but early-session behaviour revisits the same item or category.
- `browsing`: none of the above.

These proxy labels are stored only in `labels.parquet` and are intended for evaluation or weak supervision, not as input features.

## Limitations

- Homepage impressions are simulated because the public Retailrocket data does not contain homepage module impressions.
- Simulated clicks do not establish causal CTR uplift.
- Intent labels are behavioural proxies rather than human-labelled intent.
- Offline evaluation cannot fully reproduce a deployed A/B test.
- Category and product metadata can be missing or time-varying; event categories are assigned using item metadata known at or before the event timestamp.
"""
    report.write_text(content, encoding="utf-8")


def prepare_dataset(config: DatasetConfig) -> dict[str, Any]:
    """Run the full reproducible dataset preparation pipeline."""
    if config.source not in VALID_SOURCES:
        raise ValueError(f"Unsupported source {config.source!r}. Choose from {VALID_SOURCES}.")

    events, raw_event_count = _load_and_sessionize_events(config)
    if events.empty:
        raise ValueError(
            "No sessions were retained. Try lowering --min-session-events or checking raw data."
        )

    item_properties, category_tree, missing_metadata_files = _load_metadata_for_events(
        config, events
    )
    events = attach_event_categories(events, item_properties)
    sessions = build_sessions(events)
    splits = assign_time_splits(sessions)
    products = build_products(
        events,
        item_properties,
        category_tree,
        source_type=config.source_type,
    )
    labels, decision_features = build_labels_and_decision_features(
        events,
        decision_event_index=config.decision_event_index,
    )
    homepage = simulate_homepage_impressions(
        events,
        labels,
        splits,
        seed=config.seed,
    )

    tables = {
        "events": events,
        "products": products,
        "sessions": sessions,
        "labels": labels,
        "decision_features": decision_features,
        "homepage_impressions": homepage,
        "splits": splits,
    }

    config.output_dir.mkdir(parents=True, exist_ok=True)
    for table_name, filename in OUTPUT_TABLES.items():
        _write_parquet(tables[table_name], config.output_dir / filename)

    output_hashes = {
        filename: _sha256_file(config.output_dir / filename)
        for filename in OUTPUT_TABLES.values()
    }
    manifest = {
        "config": config.to_dict(),
        "raw_event_count": raw_event_count,
        "missing_metadata_files": missing_metadata_files,
        "output_hashes": output_hashes,
    }
    manifest_path = config.output_dir / "dataset_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")

    validation = validate_processed_dataset(config.output_dir, raise_on_error=False)
    generate_dataset_report(
        config.report_path,
        config,
        raw_event_count,
        missing_metadata_files,
        tables,
        validation,
    )
    if not validation["passed"]:
        failed = [row for row in validation["results"] if not row["passed"]]
        failure_text = "\n".join(f"- {row['check']}: {row['message']}" for row in failed)
        raise ValueError(f"Prepared dataset failed validation:\n{failure_text}")

    return {
        "config": config,
        "tables": tables,
        "validation": validation,
        "manifest_path": manifest_path,
        "report_path": Path(config.report_path),
    }


def parse_args() -> DatasetConfig:
    parser = argparse.ArgumentParser(description="Prepare TC2 reproducible datasets.")
    parser.add_argument("--source", default="retailrocket", choices=sorted(VALID_SOURCES))
    parser.add_argument(
        "--sample-strategy",
        default="evenly_spaced",
        choices=sorted(VALID_SAMPLE_STRATEGIES),
        help="How to choose complete sessions when --max-sessions is set.",
    )
    parser.add_argument("--raw-dir", default=None)
    parser.add_argument("--output-dir", default="data/processed")
    parser.add_argument("--report-path", default="reports/dataset_summary.md")
    parser.add_argument("--session-gap-minutes", type=int, default=30)
    parser.add_argument("--min-session-events", type=int, default=2)
    parser.add_argument("--decision-event-index", type=int, default=3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--max-events", type=int, default=None)
    parser.add_argument("--max-sessions", type=int, default=None)
    args = parser.parse_args()

    if args.raw_dir is None:
        raw_dir = (
            Path("data/fixtures/retailrocket")
            if args.source == "fixture"
            else Path("data/raw/retailrocket")
        )
    else:
        raw_dir = Path(args.raw_dir)

    return DatasetConfig(
        source=args.source,
        raw_dir=raw_dir,
        output_dir=Path(args.output_dir),
        report_path=Path(args.report_path),
        session_gap_minutes=args.session_gap_minutes,
        min_session_events=args.min_session_events,
        decision_event_index=args.decision_event_index,
        seed=args.seed,
        max_events=args.max_events,
        max_sessions=args.max_sessions,
        sample_strategy=args.sample_strategy,
    )


def main() -> None:
    config = parse_args()
    try:
        result = prepare_dataset(config)
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(f"Dataset preparation failed: {exc}")
        raise SystemExit(1) from exc

    tables = result["tables"]
    print("Dataset preparation complete.")
    print(f"Events: {len(tables['events'])}")
    print(f"Sessions: {len(tables['sessions'])}")
    print(f"Labels: {len(tables['labels'])}")
    print(f"Homepage impressions: {len(tables['homepage_impressions'])}")
    print(f"Output directory: {config.output_dir}")
    print(f"Report: {result['report_path']}")


if __name__ == "__main__":
    main()
