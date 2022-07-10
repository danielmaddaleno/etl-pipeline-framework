# -*- coding: utf-8 -*-
"""Filter Rows — core implementation."""
"""Filter rows transformer using DataFrame.query()."""

from __future__ import annotations
import pandas as pd


class FilterRowsTransformer:
    def __init__(self, params: str):
        # params is a query expression string, e.g. "amount > 0"
        self.expression = params

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.query(self.expression).reset_index(drop=True)
