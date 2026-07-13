"""Command-line entry point for the baseline recommendation pipeline."""

from __future__ import annotations

from pathlib import Path

from src.config import (
    OUTPUT_TABLES_DIR,
    PROCESSED_SESSIONS_PATH,
    RANDOM_SEED,
    RAW_EVENTS_PATH,
    TEST_SIZE,
)


def split_by_session(
    sessions, test_size: float = TEST_SIZE, random_seed: int = RANDOM_SEED
):
    """Split processed events into train/test sets by unique session_id."""
    from sklearn.model_selection import train_test_split

    unique_sessions = sessions["session_id"].drop_duplicates()
    if len(unique_sessions) < 2:
        raise ValueError("Need at least two sessions to create a train/test split.")

    train_session_ids, test_session_ids = train_test_split(
        unique_sessions,
        test_size=test_size,
        random_state=random_seed,
    )

    train_df = sessions[sessions["session_id"].isin(train_session_ids)].copy()
    test_df = sessions[sessions["session_id"].isin(test_session_ids)].copy()

    return train_df, test_df


def main() -> None:
    """Run preprocessing, baseline training, and offline evaluation."""
    raw_path = Path(RAW_EVENTS_PATH)
    if not raw_path.exists():
        print(
            f"Raw data file not found at {RAW_EVENTS_PATH}.\n"
            "Please place RetailRocket-style events.csv in data/raw/events.csv, "
            "then run: python -m src.run_baselines"
        )
        return

    from src.baselines import LastCategoryBaseline, PopularityBaseline, RandomBaseline
    from src.data_loader import basic_summary, load_events
    from src.evaluation import compare_models
    from src.preprocess import prepare_processed_sessions

    raw_events = load_events(RAW_EVENTS_PATH)
    basic_summary(raw_events)

    sessions = prepare_processed_sessions(RAW_EVENTS_PATH, PROCESSED_SESSIONS_PATH)
    if sessions.empty:
        print(
            "No valid sessions were created. Check the raw data columns and event counts."
        )
        return

    train_df, test_df = split_by_session(sessions)

    popularity_model = PopularityBaseline().fit(train_df)
    random_model = RandomBaseline(random_seed=RANDOM_SEED).fit(train_df)
    last_category_model = LastCategoryBaseline()

    models = {
        "PopularityBaseline": popularity_model,
        "LastCategoryBaseline": last_category_model,
        "RandomBaseline": random_model,
    }

    results = compare_models(test_df, models)

    output_dir = Path(OUTPUT_TABLES_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "baseline_results.csv"
    results.to_csv(output_path, index=False)

    print("\nBaseline results")
    print("----------------")
    print(results.to_string(index=False))
    print(f"\nSaved results to {output_path}")


if __name__ == "__main__":
    main()
