# 🔄 etl-pipeline-framework

Lightweight, configurable **ETL pipeline framework** built with Python, Pandas, and Airflow. Define extraction sources, transformation steps, and load targets via YAML — no boilerplate code required.

## Features

- **YAML-driven pipelines** — declarative config, no code changes per pipeline
- **Pluggable extractors** — CSV, PostgreSQL, REST API, Azure Blob Storage
- **Transform chain** — composable transform steps (rename, cast, filter, deduplicate, custom)
- **Pluggable loaders** — CSV, PostgreSQL, Parquet, Azure Blob
- **Airflow DAG generator** — auto-generates DAGs from pipeline configs
- **Schema validation** with Pydantic before load
- **Logging & lineage** — row counts at each stage, data quality checks

## Project structure

```
etl/
├── pipeline.py          # Pipeline orchestrator
├── extractors/
│   ├── base.py          # Extractor protocol
│   ├── csv_extractor.py
│   ├── postgres.py
│   └── rest_api.py
├── transformers/
│   ├── base.py          # Transformer protocol
│   ├── rename.py
│   ├── cast_types.py
│   ├── dedup.py
│   └── filter_rows.py
├── loaders/
│   ├── base.py          # Loader protocol
│   ├── csv_loader.py
│   └── parquet_loader.py
├── validation.py        # Pydantic schema checks
dags/
├── dag_generator.py     # Auto-generate Airflow DAGs
configs/
├── sample_pipeline.yaml
tests/
├── test_pipeline.py
├── test_transforms.py
requirements.txt
```

## Quick start

```bash
pip install -r requirements.txt
python -m etl.pipeline --config configs/sample_pipeline.yaml
```

## Example config

```yaml
pipeline:
  name: daily_sales_etl
  schedule: "0 6 * * *"

extract:
  type: csv
  path: data/raw/sales.csv

transform:
  - rename: {old_col: "Sale Amount", new_col: "sale_amount"}
  - cast: {sale_amount: float, quantity: int}
  - filter: "sale_amount > 0"
  - dedup: {subset: [order_id]}

load:
  type: parquet
  path: data/processed/sales.parquet
```

## License

MIT


## Installation

```bash
git clone https://github.com/danielmaddaleno/etl-pipeline-framework.git
cd etl-pipeline-framework
pip install -r requirements.txt
```

## Usage

See `docs/` for detailed examples.
