# -*- coding: utf-8 -*-
"""Csv Extractor — core implementation."""
"""CSV file extractor."""

from __future__ import annotations

import pandas as pd


class CSVExtractor:
    def __init__(self, path: str, encoding: str = "utf-8", sep: str = ",", **kwargs):
        self.path = path
        self.encoding = encoding
        self.sep = sep

    def extract(self) -> pd.DataFrame:
        return pd.read_csv(self.path, encoding=self.encoding, sep=self.sep)
