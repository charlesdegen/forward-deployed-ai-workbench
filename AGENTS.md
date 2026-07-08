# Forward-Deployed AI Systems Workbench — Agent Rules

These rules apply to every agent session in this repository (Codex, Grok Build, Claude Code, and compatible CLIs that load `AGENTS.md`).

## Mission

Convert ambiguous operational requirements into **local-first, high-trust, testable** artifacts — not demos or prompt theater.

## Non-Negotiable Constraints

- **Local-first**: no required cloud database or external service for core workflows.
- **Logic vs. UI**: keep scoring, ingestion, validation, and exports in `src/core/`; keep operator surfaces in `src/apps/`.
- **No secrets in repo**: never hardcode API keys; use environment variables only.
- **Preserve tests**: do not remove existing tests; add focused tests for changed behavior.
- **Offline fallback**: the starter triage app must work without API credentials.
- **Governance visibility**: surfaces must expose data source, last refresh, assumptions, and test status where applicable.

## Repository Map

| Path | Purpose |
|---|---|
| `specs/` | Product briefs, data contracts, acceptance criteria |
| `prompts/` | Reusable architect and repair briefs per agent adapter |
| `skills/` | Domain skills (`SKILL.md`) for triage, RCA, evals |
| `src/core/` | Ingestion, scoring, exports (`exports.py` RCA packets) |
| `src/schemas/` | JSON Schema contracts for input, output, RCA |
| `evals/` | Artifact, security, field-readiness scorecards |
| `src/apps/` | Streamlit, NiceGUI, and other operator UIs |
| `fixtures/` | Sample datasets for tests and demos |
| `tests/` | pytest suites and golden outputs |
| `artifacts/` | Runtime exports and operator logs (generated locally) |
| `CLAUDE.md` | Claude Code session rules (mirrors this file) |
| `scripts/verify.sh` | pytest + ruff + py_compile gate |
| `GROKBUILD_DOCTRINE.md` | Grok Build operating doctrine |
| `CLAUDEBUILD_DOCTRINE.md` | Claude Build operating doctrine |

## Verification Before Handoff

Run before claiming an artifact is ready:

```bash
./scripts/verify.sh
```

Summarize: changed files, commands run, test results, `git diff` highlights, known gaps.

## Build Brief Checklist

When implementing or repairing:

1. Read `specs/product_brief.md` and relevant `skills/*/SKILL.md`.
2. Keep telemetry schema validation in `src/core/ingestion.py`.
3. Wire new data paths through fixtures and tests.
4. Update README only when behavior or run instructions change.
5. Document known limitations in code comments or specs — not hidden assumptions.

## Agent Adapter Routing

| Task | Default | Optional adapters |
|---|---|---|
| Decompose ambiguity → spec | ChatGPT | Grok (`/design`, `/plan`), Claude Desktop |
| Repo-native implementation | Codex | Grok Build, Claude Code |
| Verify before demo | `pytest` + human | Grok `/check-work`, Claude Code hooks |
| Pre-handoff review | ChatGPT + `git diff` | Grok `/review --local` |

All adapters execute the **same FDE loop**; only the runtime differs.