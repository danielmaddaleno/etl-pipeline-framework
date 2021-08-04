"""Tests for transform steps."""

import pandas as pd
import pytest

from etl.transformers.rename import RenameTransformer
from etl.transformers.cast_types import CastTypesTransformer
from etl.transformers.filter_rows import FilterRowsTransformer
from etl.transformers.dedup import DedupTransformer


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "Name": ["Alice", "Bob", "Alice"],
        "amount": ["100", "200", "100"],
        "score": [0.5, -0.1, 0.5],
    })


class TestRename:
    def test_renames_columns(self, sample_df):
        t = RenameTransformer({"Name": "name"})
        result = t.transform(sample_df)
        assert "name" in result.columns
        assert "Name" not in result.columns


class TestCastTypes:
    def test_casts_to_float(self, sample_df):
        t = CastTypesTransformer({"amount": "float"})
        result = t.transform(sample_df)
        assert result["amount"].dtype == "float64"


class TestFilter:
    def test_filters_rows(self, sample_df):
        t = FilterRowsTransformer("score > 0")
        result = t.transform(sample_df)
        assert len(result) == 2
        assert (result["score"] > 0).all()


class TestDedup:
    def test_deduplicates(self, sample_df):
        t = DedupTransformer({"subset": ["Name"], "keep": "first"})
        result = t.transform(sample_df)
        assert len(result) == 2
