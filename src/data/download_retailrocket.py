"""Optional Retailrocket download helper using the Kaggle CLI."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

from src.data.config import EXPECTED_RETAILROCKET_FILES


DEFAULT_KAGGLE_DATASET = "retailrocket/ecommerce-dataset"


def expected_files_exist(raw_dir: str | Path) -> bool:
    directory = Path(raw_dir)
    return all((directory / filename).exists() for filename in EXPECTED_RETAILROCKET_FILES)


def missing_expected_files(raw_dir: str | Path) -> list[str]:
    directory = Path(raw_dir)
    return [
        filename
        for filename in EXPECTED_RETAILROCKET_FILES
        if not (directory / filename).exists()
    ]


def download_retailrocket(
    raw_dir: str | Path = "data/raw/retailrocket",
    kaggle_dataset: str = DEFAULT_KAGGLE_DATASET,
    force: bool = False,
) -> bool:
    """Download Retailrocket data if Kaggle CLI credentials are available."""
    destination = Path(raw_dir)
    destination.mkdir(parents=True, exist_ok=True)

    if expected_files_exist(destination) and not force:
        print(f"Retailrocket files already exist in {destination}.")
        return True

    if shutil.which("kaggle") is None:
        print(
            "Kaggle CLI is not installed or not on PATH. "
            "Install/configure Kaggle or manually download the Retailrocket files "
            f"into {destination}."
        )
        return False

    command = [
        "kaggle",
        "datasets",
        "download",
        "-d",
        kaggle_dataset,
        "-p",
        str(destination),
        "--unzip",
    ]
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        print(
            "Kaggle download did not complete. Check your Kaggle credentials and "
            "dataset access, or download the files manually."
        )
        return False

    missing = missing_expected_files(destination)
    if missing:
        print(f"Download finished, but these expected files are missing: {missing}")
        return False

    print(f"Retailrocket files are available in {destination}.")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Optional Retailrocket Kaggle download.")
    parser.add_argument("--raw-dir", default="data/raw/retailrocket")
    parser.add_argument("--kaggle-dataset", default=DEFAULT_KAGGLE_DATASET)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    ok = download_retailrocket(args.raw_dir, args.kaggle_dataset, args.force)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
