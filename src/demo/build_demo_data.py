"""Build a compact static dataset for the homepage personalisation demo."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


def _value(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    if hasattr(value, "item"):
        return value.item()
    return value


def _records(df: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {column: _value(value) for column, value in row.items()}
        for row in df.to_dict(orient="records")
    ]


def _load_required_parquet(data_dir: Path, name: str) -> pd.DataFrame:
    path = data_dir / f"{name}.parquet"
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Run src.data.prepare_dataset first.")
    return pd.read_parquet(path)


def _load_optional_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def choose_demo_sessions(
    labels: pd.DataFrame,
    decision_features: pd.DataFrame,
    splits: pd.DataFrame,
    max_sessions: int,
) -> list[str]:
    examples = labels.merge(
        decision_features,
        on=["session_id", "decision_event_index"],
        how="inner",
        validate="one_to_one",
    ).merge(splits, on="session_id", how="inner", validate="many_to_one")

    examples["has_category"] = examples["next_category_id"].notna() & examples[
        "last_category_id"
    ].notna()
    examples["priority"] = (
        examples["has_category"].astype(int) * 10
        + examples["will_purchase_after_decision"].astype(int) * 4
        + examples["will_add_to_cart_after_decision"].astype(int) * 2
        + examples["prefix_add_to_cart_count"].gt(0).astype(int)
    )

    split_order = {"test": 0, "validation": 1, "train": 2}
    examples["split_order"] = examples["split"].map(split_order).fillna(3)
    examples = examples.sort_values(
        ["split_order", "priority", "session_id"],
        ascending=[True, False, True],
        kind="mergesort",
    )

    selected: list[str] = []
    for intent in ["purchase_intent", "cart_intent", "product_focused", "browsing"]:
        subset = examples[examples["intent_proxy"].eq(intent)]
        for session_id in subset["session_id"]:
            if session_id not in selected:
                selected.append(session_id)
            if len(selected) >= max_sessions:
                return selected

    for session_id in examples["session_id"]:
        if session_id not in selected:
            selected.append(session_id)
        if len(selected) >= max_sessions:
            break
    return selected


def build_demo_payload(
    data_dir: str | Path = "data/processed",
    baseline_dir: str | Path = "outputs/tables",
    max_sessions: int = 12,
) -> dict[str, Any]:
    data_path = Path(data_dir)
    baseline_path = Path(baseline_dir)
    events = _load_required_parquet(data_path, "events")
    labels = _load_required_parquet(data_path, "labels")
    features = _load_required_parquet(data_path, "decision_features")
    homepage = _load_required_parquet(data_path, "homepage_impressions")
    splits = _load_required_parquet(data_path, "splits")

    selected_sessions = choose_demo_sessions(labels, features, splits, max_sessions)
    examples = labels.merge(
        features,
        on=["session_id", "decision_event_index"],
        how="inner",
        validate="one_to_one",
    ).merge(splits, on="session_id", how="inner", validate="many_to_one")
    examples = examples[examples["session_id"].isin(selected_sessions)]

    sessions_payload = []
    for session_id in selected_sessions:
        example = examples[examples["session_id"].eq(session_id)].iloc[0]
        decision_index = int(example["decision_event_index"])
        session_events = events[events["session_id"].eq(session_id)].sort_values(
            "event_index", kind="mergesort"
        )
        prefix_events = session_events[session_events["event_index"] < decision_index]
        next_event = session_events[session_events["event_index"].eq(decision_index)]
        future_events = session_events[session_events["event_index"] >= decision_index]
        impressions = homepage[homepage["session_id"].eq(session_id)].sort_values(
            ["experiment_group", "rank"], kind="mergesort"
        )

        sessions_payload.append(
            {
                "session_id": session_id,
                "split": example["split"],
                "decision_event_index": decision_index,
                "decision_timestamp": _value(example["decision_timestamp"]),
                "intent_proxy": example["intent_proxy"],
                "final_conversion_stage": example["final_conversion_stage"],
                "will_add_to_cart_after_decision": _value(
                    example["will_add_to_cart_after_decision"]
                ),
                "will_purchase_after_decision": _value(
                    example["will_purchase_after_decision"]
                ),
                "prefix": _records(
                    prefix_events[
                        [
                            "event_index",
                            "timestamp",
                            "seconds_from_session_start",
                            "event_type",
                            "item_id",
                            "category_id",
                        ]
                    ]
                ),
                "next_event": _records(
                    next_event[
                        [
                            "event_index",
                            "timestamp",
                            "seconds_from_session_start",
                            "event_type",
                            "item_id",
                            "category_id",
                        ]
                    ]
                )[0],
                "future_summary": {
                    "events_after_decision": int(len(future_events)),
                    "add_to_cart_events_after_decision": int(
                        future_events["event_type"].eq("add_to_cart").sum()
                    ),
                    "transactions_after_decision": int(
                        future_events["event_type"].eq("transaction").sum()
                    ),
                },
                "impressions": _records(
                    impressions[
                        [
                            "experiment_group",
                            "strategy",
                            "module_type",
                            "content_item_id",
                            "content_category_id",
                            "rank",
                            "simulated_click",
                            "is_synthetic",
                        ]
                    ]
                ),
            }
        )

    nominal = _load_optional_csv(baseline_path / "baseline_nominal_results.csv")
    binary = _load_optional_csv(baseline_path / "baseline_binary_results.csv")
    homepage_results = _load_optional_csv(
        baseline_path / "homepage_synthetic_match_results.csv"
    )

    metrics = {
        "next_category_recent_rule_test_accuracy": _metric(
            nominal,
            task="next_category_prediction",
            model="RecentCategoryRule",
            split="test",
            column="accuracy",
        ),
        "next_item_recent_rule_test_accuracy": _metric(
            nominal,
            task="next_item_prediction",
            model="RecentItemRule",
            split="test",
            column="accuracy",
        ),
        "add_to_cart_early_cart_test_f1": _metric(
            binary,
            task="add_to_cart_prediction",
            model="EarlyCartRule",
            split="test",
            column="f1",
        ),
        "purchase_early_cart_test_f1": _metric(
            binary,
            task="purchase_prediction",
            model="EarlyCartRule",
            split="test",
            column="f1",
        ),
        "homepage_control_test_match_rate": _metric(
            homepage_results,
            task="homepage_synthetic_match",
            model="control",
            split="test",
            column="simulated_match_rate",
        ),
        "homepage_rule_based_test_match_rate": _metric(
            homepage_results,
            task="homepage_synthetic_match",
            model="rule_based",
            split="test",
            column="simulated_match_rate",
        ),
    }

    return {
        "generated_from": str(data_path),
        "session_count": len(sessions_payload),
        "metrics": metrics,
        "sessions": sessions_payload,
        "limitations": [
            "Homepage impressions are simulated.",
            "Simulated clicks are not observed CTR.",
            "Synthetic match rates do not establish causal uplift.",
            "Intent labels are behavioural proxies, not human-labelled intent.",
        ],
    }


def _metric(
    df: pd.DataFrame,
    task: str,
    model: str,
    split: str,
    column: str,
) -> float | None:
    if df.empty:
        return None
    rows = df[
        df["task"].eq(task) & df["model"].eq(model) & df["split"].eq(split)
    ]
    if rows.empty or column not in rows.columns:
        return None
    return float(rows.iloc[0][column])


def write_demo_data(payload: dict[str, Any], output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    content = (
        "window.TC2_DEMO_DATA = "
        + json.dumps(payload, indent=2, ensure_ascii=False)
        + ";\n"
    )
    path.write_text(content, encoding="utf-8")
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build static demo data.")
    parser.add_argument("--data-dir", default="data/processed")
    parser.add_argument("--baseline-dir", default="outputs/tables")
    parser.add_argument("--output", default="demo/demo_data.js")
    parser.add_argument("--max-sessions", type=int, default=12)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_demo_payload(
        data_dir=args.data_dir,
        baseline_dir=args.baseline_dir,
        max_sessions=args.max_sessions,
    )
    path = write_demo_data(payload, args.output)
    print(f"Wrote demo data for {payload['session_count']} sessions to {path}")


if __name__ == "__main__":
    main()
