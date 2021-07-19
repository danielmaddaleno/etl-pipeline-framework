"""Deduplication transformer."""

from __future__ import annotations
import pandas as pd


class DedupTransformer:
    def __init__(self, params: dict):
        # params = {"subset": ["col1", "col2"], "keep": "last"}
        self.subset = params.get("subset")
        self.keep = params.get("keep", "first")

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop_duplicates(subset=self.subset, keep=self.keep).reset_index(drop=True)
