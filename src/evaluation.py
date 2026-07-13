"""Offline evaluation for anonymous next-category recommendation."""

from __future__ import annotations

from typing import Any

import pandas as pd


PURCHASE_EVENTS = {"transaction", "order", "purchase"}
CART_EVENTS = {"addtocart", "cart", "add_to_cart"}
ENGAGEMENT_EVENTS = {"view", "click", "clicks"}


def event_reward(event_type: str) -> int:
    """Map an event type to a simple business-weighted reward."""
    event_name = str(event_type).lower()
    if event_name in PURCHASE_EVENTS:
        return 5
    if event_name in CART_EVENTS:
        return 3
    if event_name in ENGAGEMENT_EVENTS:
        return 1
    return 0


def evaluate_next_category(
    df: pd.DataFrame,
    model: Any,
    category_col: str = "category_id",
    event_col: str = "event",
) -> dict[str, Any]:
    """Evaluate a model by predicting the next category within each session."""
    total_steps = 0
    correct_steps = 0
    total_reward = 0
    session_results: list[dict[str, Any]] = []

    if df.empty:
        return {
            "total_steps": 0,
            "correct_steps": 0,
            "accuracy": 0.0,
            "total_reward": 0,
            "average_reward": 0.0,
            "per_session_results": pd.DataFrame(),
        }

    for session_id, session in df.groupby("session_id", sort=False):
        session = session.sort_values("timestamp").reset_index(drop=True)
        session_steps = 0
        session_correct = 0
        session_reward = 0

        for step in range(1, len(session)):
            history = session.iloc[:step]
            next_event = session.iloc[step]
            prediction = model.predict(history)
            true_category = next_event[category_col]
            is_correct = prediction == true_category

            reward = event_reward(next_event[event_col]) if is_correct else 0
            total_steps += 1
            correct_steps += int(is_correct)
            total_reward += reward
            session_steps += 1
            session_correct += int(is_correct)
            session_reward += reward

        session_results.append(
            {
                "session_id": session_id,
                "steps": session_steps,
                "correct_steps": session_correct,
                "accuracy": session_correct / session_steps if session_steps else 0.0,
                "reward": session_reward,
                "average_reward": session_reward / session_steps if session_steps else 0.0,
            }
        )

    accuracy = correct_steps / total_steps if total_steps else 0.0
    average_reward = total_reward / total_steps if total_steps else 0.0

    return {
        "total_steps": total_steps,
        "correct_steps": correct_steps,
        "accuracy": accuracy,
        "total_reward": total_reward,
        "average_reward": average_reward,
        "per_session_results": pd.DataFrame(session_results),
    }


def compare_models(test_df: pd.DataFrame, models_dict: dict[str, Any]) -> pd.DataFrame:
    """Evaluate multiple models and return a compact comparison table."""
    rows: list[dict[str, Any]] = []

    for model_name, model in models_dict.items():
        result = evaluate_next_category(test_df, model)
        rows.append(
            {
                "model": model_name,
                "total_steps": result["total_steps"],
                "accuracy": result["accuracy"],
                "average_reward": result["average_reward"],
                "total_reward": result["total_reward"],
            }
        )

    return pd.DataFrame(rows)
