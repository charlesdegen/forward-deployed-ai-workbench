# Forward-Deployed AI Systems Workbench — Claude Code Rules

Claude Code loads this file every session. These rules mirror `AGENTS.md` with Claude-specific execution patterns.

## Mission

Convert ambiguous operational requirements into **local-first, high-trust, testable** artifacts — not demos or prompt theater.

## Non-Negotiable Constraints

- **Local-first**: no required cloud database or external service for core workflows.
- **Logic vs. UI**: scoring, ingestion, validation, and exports in `src/core/`; operator surfaces in `src/apps/`.
- **No secrets in repo**: use environment variables only (`OPENAI_API_KEY`, etc.).
- **Preserve tests**: never remove existing tests; add focused tests for changed behavior.
- **Offline fallback**: starter triage app works without API credentials.
- **Governance visibility**: expose data source, last refresh, assumptions, and test status in operator UIs.

## Key Specs (read before editing)

| File | Purpose |
|---|---|
| `specs/product_brief.md` | Mission Autonomy console overview |
| `specs/data_contract.md` | Telemetry schema and scoring thresholds |
| `specs/acceptance_criteria.md` | Ship gates for the starter artifact |
| `specs/operator_workflow.md` | Field operator triage steps |
| `GAP_ANALYSIS.md` | Repo gaps and priority roadmap |

## Repository Map

| Path | Purpose |
|---|---|
| `prompts/` | Build briefs per adapter — use `claude_build_brief.md` as template |
| `skills/triage-skill/` | Triage priorities and RCA protocol |
| `fixtures/sample_telemetry.csv` | Canonical test/demo dataset |
| `artifacts/` | Runtime operator logs and exports (do not commit `operator_action_log.csv`) |
| `CLAUDEBUILD_DOCTRINE.md` | Full Claude surface map and portfolio doctrine |

## Verification Gate

Run before handoff:

```bash
./scripts/verify.sh
```

Or manually:

```bash
source .venv/bin/activate
python -m pytest
python -m ruff check src tests scripts \
  local-data-fusion-workbench financial-crime-ops-console llm-red-team-eval-harness
python -m py_compile src/apps/streamlit_app.py src/core/ingestion.py
```

The commit hook (`.claude/hooks/require-verify.sh`) compares a SHA-256 of every
verified source file against the hash recorded by the last passing `verify.sh`.
Editing any source after verifying re-runs the gate; there is no time window.

Report: changed files, verify output, `git diff` summary, known gaps.

## Implementation Discipline

1. Read relevant `specs/` files before changing ingestion or UI behavior.
2. Keep threshold constants in `src/core/ingestion.py` — update `specs/data_contract.md` if thresholds change.
3. Wire new data paths through `fixtures/` and `tests/`.
4. Use `skills/triage-skill/SKILL.md` when changing triage or alert behavior.
5. Update README only when run instructions or workflow change.
6. Every scoring branch must be reachable from a fixture and pinned by a golden test.
   A threshold change that no test notices is a defect, not a passing build.
7. Fixtures declare ground truth; they never substitute for the logic under test.

## Claude Code Patterns

- **Explore first**: read `src/core/ingestion.py` and `tests/test_ingestion.py` before scoring changes.
- **Subagents**: delegate parallel test writing or docs updates when scope is large.
- **Hooks** (optional): add `.claude/hooks/` to block commits without passing `scripts/verify.sh`.
- **Headless**: `claude -p "..."` for scripted verify or batch doc generation.

## Adapter Equivalence

This repo also supports Codex (default in README) and Grok Build. All adapters follow the same FDE loop documented in `AGENTS.md` — only the runtime differs.