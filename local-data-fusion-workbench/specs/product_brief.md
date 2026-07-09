# Product Brief: Local Data Fusion Workbench

## Overview

Portfolio artifact for FDE data integration: upload local datasets, profile columns, match entity keys, join with Polars, persist inspectable state in DuckDB, detect orphan keys and outliers, and export a clean fused dataset with Mermaid lineage.

## Target user

- **Field data engineers** fusing CSV/XLSX/JSON extracts from disconnected systems
- **Analysts** who need fast local joins without standing up a warehouse

## Core workflow

1. Load fixture bundle or upload datasets
2. Review per-column profiles (null %, dtype, uniqueness)
3. Select join keys and run left/inner/outer fusion
4. Review orphan keys and duplicate-key anomalies
5. Export fused CSV/Parquet + lineage markdown to `artifacts/exports/`

## Stack

- **Polars** — profiling, joins, exports
- **DuckDB** — local persistence (`artifacts/data_fusion.duckdb`)
- **NiceGUI** — operator surface on port `8081`

## Demo datasets

- `fixtures/customers.csv` — 4 customer records
- `fixtures/transactions.csv` — 8 transactions including orphan `C999` / `C888` keys
- `fixtures/events.json` — supplemental entity events

## Acceptance

- `pytest local-data-fusion-workbench/tests` passes
- `python local-data-fusion-workbench/fusion/apps/nicegui_app.py` launches on `8081`
- Fusion of fixtures yields 8 rows with orphan-key anomalies surfaced