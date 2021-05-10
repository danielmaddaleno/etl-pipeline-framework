"""Parquet file loader."""

from __future__ import annotations
from pathlib import Path
import pandas as pd


class ParquetLoader:
    def __init__(self, path: str, **kwargs):
        self.path = Path(path)

    def load(self, df: pd.DataFrame) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(self.path, index=False)
