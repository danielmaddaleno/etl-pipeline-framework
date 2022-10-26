# -*- coding: utf-8 -*-
# Author: Daniel Maddaleno
"""Rename — core implementation."""
"""Rename columns transformer."""

from __future__ import annotations
import pandas as pd


class RenameTransformer:
    def __init__(self, params: dict):
        # params = {"old_col": "new_name", ...}
        self.mapping = params

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns=self.mapping)
