from __future__ import annotations

from pathlib import Path

import pytest

from src.data.config import DatasetConfig
from src.data.load_retailrocket import load_raw_retailrocket
from src.data.prepare_dataset import prepare_dataset
from src.data.validate_dataset import validate_processed_dataset


def test_validate_fixture_outputs_pass(tmp_path: Path) -> None:
    output_dir = tmp_path / "processed"
    prepare_dataset(
        DatasetConfig(
            source="fixture",
            raw_dir=Path("data/fixtures/retailrocket"),
            output_dir=output_dir,
            report_path=tmp_path / "dataset_summary.md",
            seed=42,
        )
    )

    result = validate_processed_dataset(output_dir, raise_on_error=True)
    assert result["passed"]


def test_missing_raw_events_has_readable_error(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError, match="Missing Retailrocket events file"):
        load_raw_retailrocket(tmp_path / "empty")
