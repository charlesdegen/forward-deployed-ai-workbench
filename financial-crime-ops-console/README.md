# Financial Crime Operations Console

Portfolio artifact #3 for the Forward-Deployed AI Systems Workbench.

**Streamlit + DuckDB** — synthetic AML case queue, rule-based risk scoring, audit trail, evidence / SAR-draft export.

## Run

```bash
source ../.venv/bin/activate
streamlit run fin_crime/apps/streamlit_app.py
```

## Workflow

1. **Load** — fixture `sample_transactions.csv` (or upload)
2. **Score** — amount, jurisdiction, channel, prior SAR rules
3. **Triage** — case queue sorted by risk band
4. **Audit** — append operator actions to local DuckDB
5. **Export** — evidence packet JSON + markdown (training draft only)

## Verify

```bash
pytest tests -q
```

From repo root: `pytest financial-crime-ops-console/tests -q`

## Layout

```
financial-crime-ops-console/
  fixtures/sample_transactions.csv
  specs/product_brief.md
  fin_crime/core/     # ingestion, scoring, duckdb, exports
  fin_crime/apps/streamlit_app.py
  tests/
  artifacts/          # fin_crime.duckdb, exports/
```

## Guardrails

- All counterparties are synthetic.
- SAR narrative is **not** a regulatory filing.
- Domain skill: `../skills/fin-crime-skill/SKILL.md`
