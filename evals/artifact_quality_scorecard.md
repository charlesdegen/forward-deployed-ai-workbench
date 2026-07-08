# Artifact Quality Scorecard

**Artifact:** Mission Autonomy Field Support Console (starter)  
**Evaluator:** _______________  
**Date:** _______________  
**Version / commit:** _______________

## Scoring (0 = fail, 1 = partial, 2 = pass)

| Criterion | 0 | 1 | 2 | Score | Notes |
|---|---|---|---|---|---|
| Solves a real operator workflow end-to-end | | | | | |
| Runs locally without cloud dependency | | | | | |
| Core logic separated from UI (`src/core` vs `src/apps`) | | | | | |
| `./scripts/verify.sh` passes on evaluator machine | | | | | |
| Fixtures included and documented | | | | | |
| README run instructions accurate | | | | | |
| Known limitations documented (not hidden) | | | | | |
| Reusable leverage left behind (skill, spec, test, template) | | | | | |

**Total / 16:** _______

## Thresholds

- **Ship:** ≥ 14
- **Repair loop:** 10–13
- **Reject:** < 10

## Evidence checklist

- [ ] Screenshot of governance sidebar with live metadata
- [ ] Screenshot of alerts queue with scored anomalies
- [ ] `./scripts/verify.sh` output attached
- [ ] `git diff` or change summary attached
- [ ] RCA export sample in `artifacts/exports/`