"""Tests for the ETL pipeline."""

import tempfile
from pathlib import Path

import pandas as pd
import pytest
import yaml

from etl.pipeline import Pipeline


@pytest.fixture
def sample_csv(tmp_path):
    df = pd.DataFrame({
        "order_id": [1, 2, 2, 3],
        "sale_amount": [100.0, 200.0, 200.0, -50.0],
        "quantity": [1, 3, 3, 2],
    })
    path = tmp_path / "input.csv"
    df.to_csv(path, index=False)
    return path


@pytest.fixture
def pipeline_config(sample_csv, tmp_path):
    output_path = tmp_path / "output.csv"
    config = {
        "pipeline": {"name": "test_pipeline"},
        "extract": {"type": "csv", "path": str(sample_csv)},
        "transform": [
            {"filter": "sale_amount > 0"},
            {"dedup": {"subset": ["order_id"]}},
        ],
        "load": {"type": "csv", "path": str(output_path)},
    }
    config_path = tmp_path / "config.yaml"
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    return config_path, output_path


class TestPipeline:
    def test_end_to_end(self, pipeline_config):
        config_path, output_path = pipeline_config
        pipe = Pipeline.from_yaml(config_path)
        result = pipe.run()

        # Should filter out negative sale and deduplicate order_id=2
        assert len(result) == 2
        assert output_path.exists()

    def test_pipeline_name(self, pipeline_config):
        config_path, _ = pipeline_config
        pipe = Pipeline.from_yaml(config_path)
        assert pipe.name == "test_pipeline"
