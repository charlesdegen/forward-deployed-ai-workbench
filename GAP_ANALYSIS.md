# GrokBuild Workbench — Gap Analysis & Backlog

**Date:** 2026-07-09  
**Scope:** Repo fidelity vs. README, doctrines, and product briefs.

## Status Summary

| Area | Maturity | Notes |
|---|---|---|
| Vision & doctrine | Strong | README + doctrines + docs/ |
| Portfolio (5 artifacts) | **5 / 5 shipped** | Screenshots for all surfaces |
| Agent wiring | Good | AGENTS.md, CLAUDE.md, prompts, skills, hooks |
| CI / verify gate | Done | pytest + ruff + py_compile + smoke + screenshot presence |
| Packaging | Strong | Air-gap single-file `vendor/` assets |

---

## Portfolio scoreboard

| # | Artifact | Status | Screenshot |
|---|---|---|---|
| 1 | Mission Console | **Shipped** | `mission_console_*.png` |
| 2 | Local Data Fusion | **Shipped** | `data_fusion_overview.png` |
| 3 | Financial Crime Ops | **Shipped** | `fin_crime_overview.png` |
| 4 | LLM Red-Team Eval | **Shipped** | `redteam_overview.png` |
| 5 | Single-File Command Brief | **Shipped** (air-gap) | `single_file_command_brief.png` |

---

## Closed (this session)

- [x] Screenshots for fusion / fin-crime / redteam / single-file
- [x] Playwright smoke script + pytest marker (`scripts/smoke_ui.py`, `tests/test_smoke_ui.py`)
- [x] Smoke wired into `scripts/verify.sh` (default on; `VERIFY_SMOKE=0` to skip)
- [x] `.claude/hooks/require-verify.sh` + settings + `.grok/hooks` for commit/push gate
- [x] Air-gap vendored assets for single-file brief (no CDN)
- [x] README / docs / GAP updated

## Remaining optional polish

- [ ] Demo video / Loom (human-owned)
- [ ] Split monorepo into five remotes (only if packaging requires)
- [ ] Expand smoke full suite in default CI if machine budget allows (`SMOKE_FULL=1`)

---

## Verify recipes

```bash
./scripts/verify.sh
VERIFY_SECURITY=1 ./scripts/verify.sh
SMOKE_FULL=1 ./scripts/verify.sh
python scripts/capture_screenshots.py
```
