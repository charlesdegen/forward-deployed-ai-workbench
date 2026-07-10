# GrokBuild Workbench — Gap Analysis & Backlog

**Date:** 2026-07-09  
**Scope:** Repo fidelity vs. README, doctrines, and product briefs.

## Status Summary

| Area | Maturity | Notes |
|---|---|---|
| Vision & doctrine | Strong | README + doctrines + docs/ |
| Portfolio (5 artifacts) | **5 / 5 shipped** | Screenshots for all surfaces |
| Agent wiring | Good | AGENTS.md, CLAUDE.md, prompts, skills, hooks |
| CI / verify gate | Done | pytest + ruff (all artifacts) + py_compile + smoke + screenshots |
| Test integrity | Done | Every scoring branch fixture-reachable and golden-pinned |
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

## Closed (prior session)

- [x] Screenshots for fusion / fin-crime / redteam / single-file
- [x] Playwright smoke script + pytest marker (`scripts/smoke_ui.py`, `tests/test_smoke_ui.py`)
- [x] Smoke wired into `scripts/verify.sh` (default on; `VERIFY_SMOKE=0` to skip)
- [x] `.claude/hooks/require-verify.sh` + settings + `.grok/hooks` for commit/push gate
- [x] Air-gap vendored assets for single-file brief (no CDN)
- [x] README / docs / GAP updated

## Closed (FDE mandate audit)

Audit found the gate passing while several branches could not fail. Fixed:

- [x] **Red-team evaluator bypass** — `expected_result` overrode the heuristic for all 8
      fixture cases, so the evaluator under test never ran. It is now ground truth the
      heuristic is scored against; disagreements surface in the summary and the UI.
- [x] **`comms_anomaly` was dead** — no fixture, mock, or test tripped it. Fixture now
      injects comms degradation (40–42), a full cascade at 45 (`risk_score` 100), and a
      temperature warning band at 47. Golden pins every flag count.
- [x] **Published ranges were unenforced** — `parse_telemetry_csv` now reads bounds from
      `src/schemas/input_schema.json` and rejects violations; schemas have negative tests.
- [x] **Logic in UI** — `system_state` / `alert_count` / alert filter moved behind
      `summarize_alert_state()` + `alert_mask()`; fin-crime queue cutoff is now
      `CASE_QUEUE_MIN_SCORE`, imported rather than hardcoded in the app.
- [x] **Gate lint scope** — ruff now covers all four artifacts (3 latent errors fixed).
- [x] **Time-based commit gate** — `scripts/source_hash.sh` replaces the 30-minute stamp
      with a content hash, so a post-verify edit always re-runs the gate.
- [x] **Fin-crime had no golden** — per-transaction scores/bands/flags pinned; a weight
      regression (e.g. `AMOUNT_HIGH` 25→5) now fails instead of passing.
- [x] **Governance gaps** — test status added to fin-crime and red-team panels; fusion
      panel now shows data source, last refresh, and source row count.

Suite grew 36 → 68 tests. Verified by mutation: comms operator flip, comms threshold
change, fin-crime weight change, and re-introducing the red-team override each now fail.

- [x] **Unpinned dependencies** — all 22 deps now pinned in `requirements.txt` and
      `pyproject.toml`. The unused `openai` SDK moved to an opt-in `llm` extra (no
      surface calls a live model) and unused `streamlit-extras` was dropped. Validated
      by building a clean venv from the pinned file: 69 tests pass and the Streamlit
      starter serves with `OPENAI_API_KEY` unset and the SDK absent.

- [x] **Full smoke covered 3 of 5 surfaces** — `SMOKE_FULL=1` now launches all five
      (starter, mission console, fusion, fin-crime, red-team) plus the static brief.
      The starter smoke strips `OPENAI_API_KEY` so the offline-fallback constraint is
      enforced by the gate, not just claimed.

## Closed (polish sweep, 2026-07-09)

- [x] **Acceptance criteria ratified** — all 36 boxes mapped to a pinned test,
      verify gate, or verified code path; ratification note in the spec header.
- [x] **Hash-verified installs** — `requirements-lock.txt` locks the full transitive
      closure (2,497 SHA-256 hashes, `uv pip compile --generate-hashes`). Validated:
      clean venv via `pip install --require-hashes`, then 81 tests pass from it.
- [x] **Fusion/red-team test gaps** — `normalize_key`, `add_normalized_key`, JSON/
      Parquet/Excel/file-like loaders, and `inner/outer/cross` joins now tested.
      Testing found two real `fuse_datasets` defects: `outer` relied on a deprecated
      polars alias (now maps to `full`) and `cross` crashed by passing join keys.
      Red-team fixture gained `low` (TB-003) and `info` (HL-003) cases so every
      `SEVERITY_ORDER` tier is fixture-reachable; weights pinned (info = 0 weight
      but still blocks SHIP; low < high).
- [x] **Full smoke by default** — `verify.sh` now runs the complete surface smoke
      unless `SMOKE_FULL=0` (brief-only) or `VERIFY_SMOKE=0` (skip).

## Remaining (human-owned / conditional)

- [ ] Demo video / Loom (human-owned)
- [ ] Split monorepo into five remotes (only if packaging requires)

---

## Verify recipes

```bash
./scripts/verify.sh
VERIFY_SECURITY=1 ./scripts/verify.sh
SMOKE_FULL=1 ./scripts/verify.sh
python scripts/capture_screenshots.py
```
