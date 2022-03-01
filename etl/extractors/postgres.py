# -*- coding: utf-8 -*-
"""PostgreSQL extractor (requires psycopg2)."""

from __future__ import annotations

import pandas as pd


class PostgresExtractor:
    def __init__(self, connection_string: str, query: str, **kwargs):
        self.connection_string = connection_string
        self.query = query

    def extract(self) -> pd.DataFrame:
        import psycopg2
        conn = psycopg2.connect(self.connection_string)
        try:
            return pd.read_sql(self.query, conn)
        finally:
            conn.close()
