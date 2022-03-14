# -*- coding: utf-8 -*-
"""Cast column types transformer."""

from __future__ import annotations
import pandas as pd

_TYPE_MAP = {"int": "int64", "float": "float64", "str": "object", "bool": "bool"}


class CastTypesTransformer:
    def __init__(self, params: dict):
        # params = {"col_name": "float", ...}
        self.type_map = params

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        for col, dtype in self.type_map.items():
            target = _TYPE_MAP.get(dtype, dtype)
            df[col] = df[col].astype(target)
        return df
