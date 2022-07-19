# -*- coding: utf-8 -*-
# Author: Daniel Maddaleno
"""Dag Generator — core implementation."""
"""Auto-generate Airflow DAGs from pipeline YAML configs."""

from __future__ import annotations

import logging
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)

DAG_TEMPLATE = '''"""Auto-generated Airflow DAG for pipeline: {name}."""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from etl.pipeline import Pipeline


def run_pipeline():
    pipe = Pipeline.from_yaml("{config_path}")
    pipe.run()


with DAG(
    dag_id="{name}",
    schedule_interval="{schedule}",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["etl", "auto-generated"],
) as dag:
    task = PythonOperator(
        task_id="run_{name}",
        python_callable=run_pipeline,
    )
'''


def generate_dag(config_path: str | Path, output_dir: str | Path = "dags") -> Path:
    """Read a pipeline YAML and write a corresponding Airflow DAG file."""
    with open(config_path) as f:
        config = yaml.safe_load(f)

    name = config["pipeline"]["name"]
    schedule = config["pipeline"].get("schedule", "@daily")

    dag_code = DAG_TEMPLATE.format(
        name=name,
        config_path=str(config_path),
        schedule=schedule,
    )

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    dag_file = out / f"dag_{name}.py"
    dag_file.write_text(dag_code)
    logger.info("Generated DAG: %s", dag_file)
    return dag_file


if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", default="dags")
    args = parser.parse_args()
    generate_dag(args.config, args.output)
