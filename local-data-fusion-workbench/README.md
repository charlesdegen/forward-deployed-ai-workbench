# Local Data Fusion Workbench

Portfolio artifact #2 for the Forward-Deployed AI Systems Workbench.

**Polars + DuckDB + NiceGUI** — upload, profile, join, detect anomalies, export clean datasets with Mermaid lineage.

## Run

```bash
source ../.venv/bin/activate   # or repo-root .venv
python fusion/apps/nicegui_app.py
```

Open http://127.0.0.1:8081 — fixture bundle loads on startup.

## Workflow

1. **Profile** — column dtypes, null %, uniqueness per dataset
2. **Join** — select left/right datasets and keys (defaults to `customer_id`)
3. **Anomalies** — orphan keys (`C999`, `C888` in demo), duplicate detection
4. **Export** — fused CSV + Parquet + lineage markdown under `artifacts/exports/`

## Verify

```bash
pytest tests -q
```

From repo root:

```bash
pytest local-data-fusion-workbench/tests -q
./scripts/verify.sh
```

## Layout

```
local-data-fusion-workbench/
  fixtures/           # customers, transactions, events
  specs/product_brief.md
  fusion/core/        # ingestion, profiling, matching, fusion, anomalies, lineage, duckdb, exports
  fusion/apps/nicegui_app.py
  tests/
  artifacts/          # data_fusion.duckdb, exports/ (runtime)
```