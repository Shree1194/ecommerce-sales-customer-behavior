"""Load and validate raw Olist CSV tables."""

from __future__ import annotations

import logging
from pathlib import Path

import pandas as pd

from src.config import EXPECTED_FILES

logger = logging.getLogger(__name__)


def validate_raw_files(raw_dir: Path) -> None:
    """Raise a clear error when expected Kaggle files are missing."""
    missing = [
        filename
        for filename in EXPECTED_FILES.values()
        if not (raw_dir / filename).exists()
    ]
    if missing:
        missing_list = "\n".join(f"- {name}" for name in missing)
        raise FileNotFoundError(
            "Missing Olist CSV files in data/raw. Download the Brazilian "
            "E-Commerce Public Dataset by Olist from Kaggle and place these "
            f"files there:\n{missing_list}"
        )


def load_raw_tables(raw_dir: Path) -> dict[str, pd.DataFrame]:
    """Load all expected Olist CSV files into a table dictionary."""
    validate_raw_files(raw_dir)
    tables: dict[str, pd.DataFrame] = {}

    for table_name, filename in EXPECTED_FILES.items():
        path = raw_dir / filename
        logger.info("Loading %s from %s", table_name, path)
        tables[table_name] = pd.read_csv(path)

    return tables
