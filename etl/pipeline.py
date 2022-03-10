# -*- coding: utf-8 -*-
"""ETL Pipeline orchestrator — reads YAML config and runs E → T → L."""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from etl.extractors.csv_extractor import CSVExtractor
from etl.transformers.rename import RenameTransformer
from etl.transformers.cast_types import CastTypesTransformer
from etl.transformers.filter_rows import FilterRowsTransformer
from etl.transformers.dedup import DedupTransformer
from etl.loaders.csv_loader import CSVLoader
from etl.loaders.parquet_loader import ParquetLoader

logger = logging.getLogger(__name__)

# ── Registry ────────────────────────────────────────────────────────
EXTRACTORS = {"csv": CSVExtractor}
LOADERS = {"csv": CSVLoader, "parquet": ParquetLoader}
TRANSFORMERS = {
    "rename": RenameTransformer,
    "cast": CastTypesTransformer,
    "filter": FilterRowsTransformer,
    "dedup": DedupTransformer,
}


class Pipeline:
    """YAML-driven ETL pipeline."""

    def __init__(self, config: dict[str, Any]):
        self.name: str = config["pipeline"]["name"]
        self.config = config

    @classmethod
    def from_yaml(cls, path: str | Path) -> "Pipeline":
        with open(path) as f:
            config = yaml.safe_load(f)
        return cls(config)

    def run(self) -> pd.DataFrame:
        start = time.perf_counter()
        logger.info("▶ Starting pipeline '%s'", self.name)

        # Extract
        df = self._extract()
        logger.info("  Extracted %d rows", len(df))

        # Transform
        df = self._transform(df)
        logger.info("  Transformed → %d rows", len(df))

        # Load
        self._load(df)
        elapsed = time.perf_counter() - start
        logger.info("✔ Pipeline '%s' completed in %.2fs", self.name, elapsed)
        return df

    def _extract(self) -> pd.DataFrame:
        ext_cfg = self.config["extract"]
        ext_type = ext_cfg.pop("type")
        extractor_cls = EXTRACTORS[ext_type]
        return extractor_cls(**ext_cfg).extract()

    def _transform(self, df: pd.DataFrame) -> pd.DataFrame:
        for step in self.config.get("transform", []):
            for step_type, params in step.items():
                transformer_cls = TRANSFORMERS[step_type]
                df = transformer_cls(params).transform(df)
                logger.info("    [%s] → %d rows", step_type, len(df))
        return df

    def _load(self, df: pd.DataFrame) -> None:
        load_cfg = self.config["load"]
        load_type = load_cfg.pop("type")
        loader_cls = LOADERS[load_type]
        loader_cls(**load_cfg).load(df)
        logger.info("  Loaded %d rows to %s", len(df), load_type)


if __name__ == "__main__":
    import argparse
    import sys

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    args = parser.parse_args()
    Pipeline.from_yaml(args.config).run()
