# -*- coding: utf-8 -*-
"""Rest Api — core implementation."""
"""REST API extractor — GET endpoint → DataFrame."""

from __future__ import annotations

import pandas as pd
import requests


class RESTAPIExtractor:
    def __init__(self, url: str, headers: dict | None = None, params: dict | None = None, **kwargs):
        self.url = url
        self.headers = headers or {}
        self.params = params or {}

    def extract(self) -> pd.DataFrame:
        response = requests.get(self.url, headers=self.headers, params=self.params)
        response.raise_for_status()
        data = response.json()
        # Support both list-of-dicts and {"results": [...]} patterns
        if isinstance(data, list):
            return pd.DataFrame(data)
        if isinstance(data, dict) and "results" in data:
            return pd.DataFrame(data["results"])
        return pd.DataFrame([data])
