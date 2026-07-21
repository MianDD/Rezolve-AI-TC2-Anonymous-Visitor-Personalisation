"""Baseline evaluation over prepared TC2 Parquet datasets."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class BaselineEvaluationConfig:
    data_dir: Path = Path("data/processed")
    output_dir: Path = Path("outputs/tables")
    report_path: Path = Path("reports/baseline_evaluation.md")


def _safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return 0.0
    return float(numerator / denominator)


def _mode_or_none(values: pd.Series) -> Any | None:
    values = values.dropna()
    if values.empty:
        return None
    return values.value_counts().index[0]


def _constant_series(index: pd.Index, value: Any | None) -> pd.Series:
    return pd.Series([value] * len(index), index=index)


def load_processed_tables(data_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Load processed Parquet tables required for baseline evaluation."""
    directory = Path(data_dir)
    required_files = {
        "events": "events.parquet",
        "labels": "labels.parquet",
        "decision_features": "decision_features.parquet",
        "splits": "splits.parquet",
    }
    missing = [
        filename for filename in required_files.values() if not (directory / filename).exists()
    ]
    if missing:
        raise FileNotFoundError(
            f"Missing processed files in {directory}: {missing}. "
            "Run python -m src.data.prepare_dataset first."
        )

    tables = {
        name: pd.read_parquet(directory / filename)
        for name, filename in required_files.items()
    }

    homepage_path = directory / "homepage_impressions.parquet"
    if homepage_path.exists():
        tables["homepage_impressions"] = pd.read_parquet(homepage_path)
    else:
        tables["homepage_impressions"] = pd.DataFrame()
    return tables


def build_prediction_examples(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Merge labels with decision-time features and chronological split assignments."""
    labels = tables["labels"]
    features = tables["decision_features"]
    splits = tables["splits"]
    examples = labels.merge(
        features,
        on=["session_id", "decision_event_index"],
        how="inner",
        validate="one_to_one",
    )
    examples = examples.merge(splits, on="session_id", how="inner", validate="many_to_one")
    return examples.sort_values(["split", "session_id"], kind="mergesort").reset_index(
        drop=True
    )


def fit_mode_mapping(
    train_examples: pd.DataFrame,
    key_col: str,
    target_col: str,
) -> dict[Any, Any]:
    """Fit a train-only mapping from a prefix feature to the modal target."""
    filtered = train_examples[[key_col, target_col]].dropna()
    if filtered.empty:
        return {}

    counts = (
        filtered.groupby([key_col, target_col], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values([key_col, "count", target_col], ascending=[True, False, True])
    )
    best = counts.groupby(key_col, as_index=False).head(1)
    return dict(zip(best[key_col], best[target_col], strict=False))


def fit_popular_item_by_category(train_events: pd.DataFrame) -> dict[Any, Any]:
    """Fit train-only category -> popular item mapping."""
    filtered = train_events[["category_id", "item_id"]].dropna()
    if filtered.empty:
        return {}

    counts = (
        filtered.groupby(["category_id", "item_id"], dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values(["category_id", "count", "item_id"], ascending=[True, False, True])
    )
    best = counts.groupby("category_id", as_index=False).head(1)
    return dict(zip(best["category_id"], best["item_id"], strict=False))


def evaluate_nominal_predictions(
    examples: pd.DataFrame,
    target_col: str,
    prediction_col: str,
    task: str,
    model: str,
) -> pd.DataFrame:
    """Evaluate next-item or next-category top-1 predictions by split."""
    rows: list[dict[str, Any]] = []
    for split, split_examples in examples.groupby("split", sort=False):
        target = split_examples[target_col]
        prediction = split_examples[prediction_col]
        target_available = target.notna()
        prediction_available = prediction.notna() & target_available

        evaluated_rows = int(target_available.sum())
        covered_rows = int(prediction_available.sum())
        correct = int((prediction[prediction_available] == target[prediction_available]).sum())

        rows.append(
            {
                "task": task,
                "model": model,
                "split": split,
                "evaluated_rows": evaluated_rows,
                "covered_rows": covered_rows,
                "coverage": _safe_divide(covered_rows, evaluated_rows),
                "accuracy": _safe_divide(correct, evaluated_rows),
                "accuracy_on_covered": _safe_divide(correct, covered_rows),
                "correct": correct,
            }
        )
    return pd.DataFrame(rows)


def evaluate_binary_predictions(
    examples: pd.DataFrame,
    target_col: str,
    prediction_col: str,
    task: str,
    model: str,
) -> pd.DataFrame:
    """Evaluate binary add-to-cart or purchase predictions by split."""
    rows: list[dict[str, Any]] = []
    for split, split_examples in examples.groupby("split", sort=False):
        target = split_examples[target_col].astype(bool)
        prediction = split_examples[prediction_col].astype(bool)
        tp = int((target & prediction).sum())
        tn = int((~target & ~prediction).sum())
        fp = int((~target & prediction).sum())
        fn = int((target & ~prediction).sum())
        n_rows = int(len(split_examples))

        precision = _safe_divide(tp, tp + fp)
        recall = _safe_divide(tp, tp + fn)
        rows.append(
            {
                "task": task,
                "model": model,
                "split": split,
                "evaluated_rows": n_rows,
                "actual_positive_rate": float(target.mean()) if n_rows else 0.0,
                "predicted_positive_rate": float(prediction.mean()) if n_rows else 0.0,
                "accuracy": _safe_divide(tp + tn, n_rows),
                "precision": precision,
                "recall": recall,
                "f1": _safe_divide(2 * precision * recall, precision + recall),
                "true_positive": tp,
                "false_positive": fp,
                "true_negative": tn,
                "false_negative": fn,
            }
        )
    return pd.DataFrame(rows)


def add_nominal_predictions(
    examples: pd.DataFrame,
    train_events: pd.DataFrame,
    train_examples: pd.DataFrame,
) -> pd.DataFrame:
    """Add next-item and next-category baseline prediction columns."""
    output = examples.copy()
    global_item = _mode_or_none(train_events["item_id"])
    global_category = _mode_or_none(train_events["category_id"])

    category_to_next_category = fit_mode_mapping(
        train_examples,
        key_col="most_frequent_category_id",
        target_col="next_category_id",
    )
    category_to_item = fit_popular_item_by_category(train_events)

    output["pred_next_item_global_popularity"] = _constant_series(output.index, global_item)
    output["pred_next_item_recent_item"] = output["last_item_id"]
    output["pred_next_item_category_popularity"] = output["last_category_id"].map(
        category_to_item
    )
    output["pred_next_item_category_popularity"] = output[
        "pred_next_item_category_popularity"
    ].fillna(global_item)

    output["pred_next_category_global_popularity"] = _constant_series(
        output.index, global_category
    )
    output["pred_next_category_recent_category"] = output["last_category_id"]
    output["pred_next_category_early_category_popularity"] = output[
        "most_frequent_category_id"
    ].map(category_to_next_category)
    output["pred_next_category_early_category_popularity"] = output[
        "pred_next_category_early_category_popularity"
    ].fillna(global_category)
    return output


def add_binary_predictions(examples: pd.DataFrame) -> pd.DataFrame:
    """Add simple decision-time binary rule predictions."""
    output = examples.copy()
    product_focus = output["prefix_unique_items"] < output["prefix_event_count"]
    category_focus = output["prefix_unique_categories"] < output["prefix_event_count"]
    early_cart = output["prefix_add_to_cart_count"] > 0

    output["pred_add_to_cart_always_negative"] = False
    output["pred_add_to_cart_early_cart"] = early_cart
    output["pred_add_to_cart_product_focus"] = product_focus | category_focus
    output["pred_add_to_cart_cart_or_focus"] = early_cart | product_focus | category_focus

    output["pred_purchase_always_negative"] = False
    output["pred_purchase_early_cart"] = early_cart
    output["pred_purchase_product_focus"] = product_focus | category_focus
    output["pred_purchase_cart_or_focus"] = early_cart | product_focus | category_focus
    return output


def evaluate_homepage_synthetic_match(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Summarise synthetic homepage match rate by split and experiment group."""
    homepage = tables.get("homepage_impressions", pd.DataFrame())
    if homepage.empty:
        return pd.DataFrame(
            columns=[
                "task",
                "model",
                "split",
                "evaluated_rows",
                "simulated_match_rate",
                "note",
            ]
        )

    homepage = homepage.merge(
        tables["splits"], on="session_id", how="left", validate="many_to_one"
    )
    rows = []
    for (split, group), group_df in homepage.groupby(["split", "experiment_group"]):
        rows.append(
            {
                "task": "homepage_synthetic_match",
                "model": group,
                "split": split,
                "evaluated_rows": len(group_df),
                "simulated_match_rate": float(group_df["simulated_click"].mean()),
                "note": "Synthetic match signal only; not observed CTR or causal uplift.",
            }
        )
    return pd.DataFrame(rows)


def run_baseline_evaluation(config: BaselineEvaluationConfig) -> dict[str, pd.DataFrame]:
    """Run train-fitted baselines and save result tables."""
    tables = load_processed_tables(config.data_dir)
    examples = build_prediction_examples(tables)
    event_splits = tables["events"].merge(
        tables["splits"], on="session_id", how="inner", validate="many_to_one"
    )
    train_events = event_splits[event_splits["split"].eq("train")]
    train_examples = examples[examples["split"].eq("train")]

    examples = add_nominal_predictions(examples, train_events, train_examples)
    examples = add_binary_predictions(examples)

    nominal_specs = [
        (
            "next_item_prediction",
            "next_item_id",
            "GlobalItemPopularity",
            "pred_next_item_global_popularity",
        ),
        (
            "next_item_prediction",
            "next_item_id",
            "RecentItemRule",
            "pred_next_item_recent_item",
        ),
        (
            "next_item_prediction",
            "next_item_id",
            "CategoryItemPopularity",
            "pred_next_item_category_popularity",
        ),
        (
            "next_category_prediction",
            "next_category_id",
            "GlobalCategoryPopularity",
            "pred_next_category_global_popularity",
        ),
        (
            "next_category_prediction",
            "next_category_id",
            "RecentCategoryRule",
            "pred_next_category_recent_category",
        ),
        (
            "next_category_prediction",
            "next_category_id",
            "EarlyCategoryPopularity",
            "pred_next_category_early_category_popularity",
        ),
    ]
    nominal_results = pd.concat(
        [
            evaluate_nominal_predictions(examples, target, pred, task, model)
            for task, target, model, pred in nominal_specs
        ],
        ignore_index=True,
    )

    binary_specs = [
        (
            "add_to_cart_prediction",
            "will_add_to_cart_after_decision",
            "AlwaysNegative",
            "pred_add_to_cart_always_negative",
        ),
        (
            "add_to_cart_prediction",
            "will_add_to_cart_after_decision",
            "EarlyCartRule",
            "pred_add_to_cart_early_cart",
        ),
        (
            "add_to_cart_prediction",
            "will_add_to_cart_after_decision",
            "ProductFocusRule",
            "pred_add_to_cart_product_focus",
        ),
        (
            "add_to_cart_prediction",
            "will_add_to_cart_after_decision",
            "CartOrFocusRule",
            "pred_add_to_cart_cart_or_focus",
        ),
        (
            "purchase_prediction",
            "will_purchase_after_decision",
            "AlwaysNegative",
            "pred_purchase_always_negative",
        ),
        (
            "purchase_prediction",
            "will_purchase_after_decision",
            "EarlyCartRule",
            "pred_purchase_early_cart",
        ),
        (
            "purchase_prediction",
            "will_purchase_after_decision",
            "ProductFocusRule",
            "pred_purchase_product_focus",
        ),
        (
            "purchase_prediction",
            "will_purchase_after_decision",
            "CartOrFocusRule",
            "pred_purchase_cart_or_focus",
        ),
    ]
    binary_results = pd.concat(
        [
            evaluate_binary_predictions(examples, target, pred, task, model)
            for task, target, model, pred in binary_specs
        ],
        ignore_index=True,
    )
    homepage_results = evaluate_homepage_synthetic_match(tables)

    config.output_dir.mkdir(parents=True, exist_ok=True)
    nominal_results.to_csv(config.output_dir / "baseline_nominal_results.csv", index=False)
    binary_results.to_csv(config.output_dir / "baseline_binary_results.csv", index=False)
    homepage_results.to_csv(
        config.output_dir / "homepage_synthetic_match_results.csv", index=False
    )

    write_baseline_report(config, nominal_results, binary_results, homepage_results)
    return {
        "nominal": nominal_results,
        "binary": binary_results,
        "homepage": homepage_results,
    }


def _markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "_No rows._"
    display = df.copy()
    for column in display.columns:
        if pd.api.types.is_float_dtype(display[column]):
            display[column] = display[column].map(lambda value: f"{value:.4f}")
    headers = [str(column) for column in display.columns]
    rows = [
        ["" if pd.isna(value) else str(value) for value in row]
        for row in display.itertuples(index=False, name=None)
    ]
    header_line = "| " + " | ".join(headers) + " |"
    separator_line = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join([header_line, separator_line, *row_lines])


def write_baseline_report(
    config: BaselineEvaluationConfig,
    nominal_results: pd.DataFrame,
    binary_results: pd.DataFrame,
    homepage_results: pd.DataFrame,
) -> None:
    """Write a compact Markdown baseline report."""
    config.report_path.parent.mkdir(parents=True, exist_ok=True)

    validation_nominal = nominal_results[nominal_results["split"].eq("validation")]
    test_nominal = nominal_results[nominal_results["split"].eq("test")]
    validation_binary = binary_results[binary_results["split"].eq("validation")]
    test_binary = binary_results[binary_results["split"].eq("test")]

    content = f"""# Baseline Evaluation

Generated: {datetime.now(timezone.utc).isoformat()}

Data directory: `{config.data_dir}`

Baselines are fitted using the chronological training split only. Validation and test sessions are used only for evaluation.

## Next-Item And Next-Category Baselines

Validation:

{_markdown_table(validation_nominal)}

Test:

{_markdown_table(test_nominal)}

## Add-To-Cart And Purchase Baselines

Validation:

{_markdown_table(validation_binary)}

Test:

{_markdown_table(test_binary)}

## Homepage Synthetic Match

{_markdown_table(homepage_results)}

This homepage table reports synthetic match rates only. It is not observed CTR and must not be interpreted as causal personalisation uplift.

## Notes

- `GlobalItemPopularity` and `GlobalCategoryPopularity` use train-period event popularity only.
- `RecentItemRule` and `RecentCategoryRule` use only decision-time prefix features.
- `EarlyCategoryPopularity` maps early-session category context to the modal train next-category, with a train global fallback.
- Binary baselines are deliberately simple prefix rules and are not calibrated machine-learning models.
"""
    config.report_path.write_text(content, encoding="utf-8")


def parse_args() -> BaselineEvaluationConfig:
    parser = argparse.ArgumentParser(description="Evaluate simple TC2 baseline models.")
    parser.add_argument("--data-dir", default="data/processed")
    parser.add_argument("--output-dir", default="outputs/tables")
    parser.add_argument("--report-path", default="reports/baseline_evaluation.md")
    args = parser.parse_args()
    return BaselineEvaluationConfig(
        data_dir=Path(args.data_dir),
        output_dir=Path(args.output_dir),
        report_path=Path(args.report_path),
    )


def main() -> None:
    config = parse_args()
    try:
        results = run_baseline_evaluation(config)
    except (FileNotFoundError, ValueError, ImportError) as exc:
        print(f"Baseline evaluation failed: {exc}")
        raise SystemExit(1) from exc

    print("Baseline evaluation complete.")
    print(f"Nominal rows: {len(results['nominal'])}")
    print(f"Binary rows: {len(results['binary'])}")
    print(f"Homepage rows: {len(results['homepage'])}")
    print(f"Output directory: {config.output_dir}")
    print(f"Report: {config.report_path}")


if __name__ == "__main__":
    main()
