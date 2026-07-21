from __future__ import annotations

from pathlib import Path

from src.data.config import EXPERIMENT_GROUPS, MODULE_TYPES, DatasetConfig
from src.data.prepare_dataset import prepare_dataset


def test_homepage_impressions_are_clearly_synthetic(tmp_path: Path) -> None:
    result = prepare_dataset(
        DatasetConfig(
            source="fixture",
            raw_dir=Path("data/fixtures/retailrocket"),
            output_dir=tmp_path / "processed",
            report_path=tmp_path / "dataset_summary.md",
            seed=42,
        )
    )
    homepage = result["tables"]["homepage_impressions"]

    assert not homepage.empty
    assert homepage["is_synthetic"].all()
    assert set(homepage["experiment_group"]) == set(EXPERIMENT_GROUPS)
    assert set(homepage["module_type"]) == set(MODULE_TYPES)
    assert homepage["source_type"].eq("synthetic_homepage_impression").all()
