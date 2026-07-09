# Financial Crime Operations Console — Product Brief

**Portfolio artifact #3** — regulated workflow triage signal (Palantir / banking FDE edge).

## Problem

Compliance analysts triage high-volume transaction alerts without a local, auditable case surface that separates rule-based risk scoring from advisory narrative drafts.

## Operator workflow

1. Load synthetic transaction fixtures (or upload CSV).
2. Score cases with transparent thresholds (amount, jurisdiction, channel, prior SAR).
3. Work the case queue ordered by risk band.
4. Append audit-trail actions (escalate, request info, close).
5. Export evidence packet + SAR narrative **draft** (training only).

## Constraints

- Local-first: DuckDB file under `artifacts/`; no bank APIs.
- All data synthetic — no real PII.
- Scoring in `fin_crime/core/`; UI in `fin_crime/apps/`.
- SAR text is explicitly a draft template, not a filing.

## Acceptance

- Fixture loads and scores ≥1 CRITICAL case (TX-1007).
- Audit log persists across session actions.
- Evidence JSON/MD exports include governance + assumptions.
- pytest covers scoring bands, schema validation, export shape.
