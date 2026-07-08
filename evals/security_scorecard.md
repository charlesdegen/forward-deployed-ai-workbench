# Security & Governance Scorecard

**Artifact:** Mission Autonomy Field Support Console (starter)  
**Evaluator:** _______________  
**Date:** _______________  
**Version / commit:** _______________

## Scoring (0 = fail, 1 = partial, 2 = pass)

| Criterion | 0 | 1 | 2 | Score | Notes |
|---|---|---|---|---|---|
| No hardcoded secrets in repository | | | | | |
| `.env` / operator logs gitignored | | | | | |
| Input schema validation on ingest | | | | | |
| Model usage disclosed in governance / RCA | | | | | |
| Advisory AI output separated from operator actions | | | | | |
| `bandit` / `pip-audit` run documented or clean | | | | | |
| Threat assumptions documented in specs | | | | | |
| Export artifacts exclude credential fields | | | | | |

**Total / 16:** _______

## Thresholds

- **Ship to constrained environment:** ≥ 14
- **Repair loop:** 10–13
- **Reject:** < 10

## Quick checks

```bash
source .venv/bin/activate
bandit -r src -ll
pip-audit
rg -n "api[_-]?key|password|secret" --glob '!*.md' .
```

## Findings log

| ID | Severity | Finding | Mitigation | Status |
|---|---|---|---|---|
| SEC-001 | | | | |