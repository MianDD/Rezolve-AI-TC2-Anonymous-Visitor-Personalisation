from __future__ import annotations

import pandas as pd

from src.baseline_evaluation import (
    add_binary_predictions,
    evaluate_binary_predictions,
    evaluate_nominal_predictions,
    fit_mode_mapping,
)


def test_nominal_evaluation_tracks_coverage_and_accuracy() -> None:
    examples = pd.DataFrame(
        {
            "split": ["validation", "validation", "validation"],
            "target": [1, 2, pd.NA],
            "prediction": [1, pd.NA, 3],
        }
    )

    result = evaluate_nominal_predictions(
        examples,
        target_col="target",
        prediction_col="prediction",
        task="toy",
        model="ToyModel",
    )

    row = result.iloc[0]
    assert row["evaluated_rows"] == 2
    assert row["covered_rows"] == 1
    assert row["correct"] == 1
    assert row["coverage"] == 0.5
    assert row["accuracy"] == 0.5
    assert row["accuracy_on_covered"] == 1.0


def test_binary_evaluation_computes_precision_recall_f1() -> None:
    examples = pd.DataFrame(
        {
            "split": ["test", "test", "test", "test"],
            "target": [True, True, False, False],
            "prediction": [True, False, True, False],
        }
    )

    result = evaluate_binary_predictions(
        examples,
        target_col="target",
        prediction_col="prediction",
        task="toy_binary",
        model="ToyRule",
    )

    row = result.iloc[0]
    assert row["true_positive"] == 1
    assert row["false_positive"] == 1
    assert row["false_negative"] == 1
    assert row["true_negative"] == 1
    assert row["accuracy"] == 0.5
    assert row["precision"] == 0.5
    assert row["recall"] == 0.5
    assert row["f1"] == 0.5


def test_mode_mapping_uses_modal_train_target() -> None:
    train = pd.DataFrame(
        {
            "prefix_category": [10, 10, 10, 20, 20],
            "next_category": [99, 99, 100, 30, 31],
        }
    )

    mapping = fit_mode_mapping(train, "prefix_category", "next_category")

    assert mapping[10] == 99
    assert mapping[20] == 30


def test_binary_rules_use_only_prefix_columns() -> None:
    examples = pd.DataFrame(
        {
            "prefix_add_to_cart_count": [0, 1],
            "prefix_unique_items": [3, 2],
            "prefix_unique_categories": [3, 1],
            "prefix_event_count": [3, 3],
        }
    )

    output = add_binary_predictions(examples)

    assert output["pred_add_to_cart_always_negative"].tolist() == [False, False]
    assert output["pred_add_to_cart_early_cart"].tolist() == [False, True]
    assert output["pred_add_to_cart_product_focus"].tolist() == [False, True]
