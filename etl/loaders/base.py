# -*- coding: utf-8 -*-
"""Base loader protocol."""

from __future__ import annotations
from typing import Protocol
import pandas as pd


class Loader(Protocol):
    def load(self, df: pd.DataFrame) -> None: ...
