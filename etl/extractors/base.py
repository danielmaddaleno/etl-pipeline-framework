# -*- coding: utf-8 -*-
"""Base — core implementation."""
"""Base extractor protocol."""

from __future__ import annotations
from typing import Protocol
import pandas as pd


class Extractor(Protocol):
    def extract(self) -> pd.DataFrame: ...
