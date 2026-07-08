# GrokBuild Workbench — Gap Analysis

**Date:** 2026-07-08  
**Scope:** Repo fidelity vs. README, GROKBUILD_DOCTRINE.md, CLAUDEBUILD_DOCTRINE.md, and product brief.

## Status Summary

| Area | Maturity | Notes |
|---|---|---|
| Vision & doctrine | Strong | Portfolio-grade narrative in README + two doctrine docs |
| Starter artifact | Partial | Telemetry scoring + Streamlit console + operator log |
| Repo scaffold | ~20% | Many documented paths not yet created |
| Agent wiring | Weak | No `CLAUDE.md`; `AGENTS.md` added in P0 |
| Portfolio (5 artifacts) | Not started | Documented only |
| CI / verify gate | Missing | No `scripts/verify.sh` |

---

## 1. Structure Gaps (documented vs. on disk)

### Missing entirely

- `CLAUDE.md` and `.claude/` (skills, agents, hooks)
- `.grok/sandbox.toml`, `.grok/rules/`
- `pyproject.toml`
- `src/schemas/input_schema.json`, `output_schema.json`
- `src/core/transforms.py`, `scoring.py`, `exports.py` (logic consolidated in `ingestion.py`)
- `src/apps/nicegui_app.py`
- `single_file_html/` no-build template
- `scripts/verify.sh`
- `/evals/` scorecards (artifact, security, field readiness)
- `/docs/` (architecture, deployment, demo_script)
- Five portfolio sub-repos under umbrella

### Partial

| Path | Have | Missing |
|---|---|---|
| `/specs` | `product_brief.md` | `operator_workflow.md`, `data_contract.md`, `acceptance_criteria.md`, `threat_model.md` |
| `/prompts` | ChatGPT architect, Codex repair | Grok/Claude build briefs, eval, design system prompts |
| `/fixtures` | `sample_telemetry.csv` (P0) | xlsx, json, logs samples |
| `/tests` | `test_ingestion.py` | App smoke tests, golden outputs, schema contract tests |
| `/artifacts` | Runtime operator log | html, mermaid, exports dirs; committed structure |

---

## 2. Starter App vs. Product Brief

| Brief promise | Current state | Gap |
|---|---|---|
| CSV ingestion | `load_telemetry_csv()` in core; UI wired in P0 | Was mock-only in UI |
| DuckDB/Polars adapters | In `requirements.txt`, unused | No implementation |
| Live governance metadata | Static sidebar strings | P0 adds dynamic source + refresh |
| RCA packet export | Referenced in skill | Not implemented |
| AI triage (live API) | Prompt export mode only | Intentional for starter |
| NiceGUI + DuckDB console | Streamlit only | Portfolio artifact #1 mismatch |
| JSON data contracts | Not present | No `src/schemas/` |

---

## 3. Cross-Document Consistency

| Issue | Resolution path |
|---|---|
| README defaults to ChatGPT/Codex; doctrines are Grok/Claude-native | `AGENTS.md` routes adapters to shared FDE loop (P0) |
| Skills describe Codex only | Extend `triage-skill` in P1 |
| AI tab exports ChatGPT/Codex only | Add Grok/Claude brief export in P1 |
| Doctrines reference rules files that didn't exist | `AGENTS.md` added; `CLAUDE.md` still needed for Claude Code |
| README claims paths not in git | Commit working tree in P0 |

---

## 4. Testing & Quality

| Item | Status |
|---|---|
| pytest (ingestion/scoring) | 5 tests passing |
| ruff | E712 in tests — fix in P0 commit |
| App smoke tests | Missing |
| Golden output files | Missing |
| `bandit` / `pip-audit` | Installed, never run |
| Headless verify script | Missing |

---

## 5. Git & Portfolio

| Item | Status |
|---|---|
| Local git | Initialized on `main` |
| Remote origin | Not configured |
| Uncommitted work | P0 commit closes this |
| Operator log in git | Should stay gitignored (`artifacts/operator_action_log.csv`) |

---

## 6. Priority Roadmap

### P0 — Close honesty gap (this session)

- [x] Commit pending working tree
- [x] Add `AGENTS.md`
- [x] Add `fixtures/sample_telemetry.csv`
- [x] Wire Streamlit CSV upload + fixture default
- [x] Dynamic governance metadata in sidebar
- [x] Document gaps in this file

### P1 — Make doctrines executable

- [x] `specs/data_contract.md`, `acceptance_criteria.md`, `operator_workflow.md`
- [x] `/prompts/grok_build_brief.md`, `claude_build_brief.md`
- [x] Extend `triage-skill` for all three adapters
- [x] `scripts/verify.sh` (`pytest` + `ruff` + `py_compile`)
- [x] `CLAUDE.md` for Claude Code auto-loading

### P2 — Governance & eval layer

- [x] `/evals/` scorecard templates
- [x] RCA packet export to `artifacts/exports/`
- [x] JSON schemas in `src/schemas/`
- [x] Golden output tests

### P3 — Portfolio path

- [ ] Build artifact #1 (Mission Console) or #3 (Data Fusion)
- [ ] GitHub remote + README screenshots
- [ ] Split into umbrella sub-repos when artifact count ≥ 2

---

## 7. What's in Good Shape

- Core telemetry loop: generate → validate schema → score → alert queue
- Operator action log with local CSV persistence
- Prompt export mode for ChatGPT/Codex (offline-safe)
- Python venv + full `requirements.txt` install
- Git history with doctrine docs and README adapters
- Anomaly injection at index 30 validated by tests

---

## 8. Single Highest-Leverage Remaining Gap

**P3 portfolio path** — build artifact #1 (Mission Console) or #3 (Data Fusion), add GitHub remote, screenshots, and demo video. The starter now proves triage + governance handoff; portfolio sub-repos prove domain signal strength.