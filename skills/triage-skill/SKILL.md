---
name: triage-skill
description: "Assists edge operators in diagnosing telemetry anomalies and generating troubleshooting checklists for degraded operational states. Use for field telemetry triage, RCA packets, and repo repairs in the Mission Autonomy console."
---

# Telemetry Triage Skill

Instructions for identifying and troubleshooting anomalies in autonomous edge systems (UAVs, ground vehicles, and sensors).

**Specs:** `specs/operator_workflow.md`, `specs/data_contract.md`  
**Starter app:** `src/apps/streamlit_app.py`  
**Core logic:** `src/core/ingestion.py`

## Triage Priority Rules

1. **Safety & Power**: Check power grids, battery depletion rates, and temperature first. Treat temperature > 80°C as warning and > 85°C as critical — may require immediate shutdown.
2. **Communications**: Check link quality (`comms_link` < 80 %). If degraded, check line-of-sight and antenna configuration.
3. **Sensor Alignment**: Check IMU drift (`sensor_drift` > 0.3), GPS lock, and camera frames. Recommend recalibration when drift is high.
4. **Compute & Software**: Check CPU utilization (> 85 %), memory leakage, and thread counts.

## Root Cause Analysis (RCA) Protocol

When generating an engineering report:

- Identify the primary failing component.
- Highlight telemetry values exceeding thresholds in `specs/data_contract.md`.
- List diagnostic actions performed (cross-reference operator action log).
- Draft recommendations for the base engineering team.
- Include data source, time range, and assumptions.

## Agent Operating Models

### ChatGPT (mission architect)

- Transform field context into diagnostic hypotheses, acceptance criteria, and operator-facing checklists.
- Review screenshots, action logs, and test output for operator readiness.
- Generate Mermaid diagrams, demo scripts, and threat-model prompts.

### Codex (repo-native implementation)

- Modify scoring in `src/core/`, UI in `src/apps/`, tests in `tests/`.
- Run `./scripts/verify.sh` after changes.
- Preserve offline fallback when `OPENAI_API_KEY` is unset.
- Summarize changed files, verification output, and deployment risks.

### Grok Build (terminal agent)

- Attach context: `@specs/ @src/core/ @skills/triage-skill/SKILL.md`
- Use `prompts/grok_build_brief.md` as the task template.
- Gate with `/check-work` and `/review --local` before handoff.
- Follow `AGENTS.md` and `GROKBUILD_DOCTRINE.md`.

### Claude Code (repo-native agent)

- Load `CLAUDE.md` and `prompts/claude_build_brief.md` every session.
- Run `./scripts/verify.sh` before claiming completion.
- Follow `CLAUDEBUILD_DOCTRINE.md` for multi-surface workflows.

## Repository Constraints (all agents)

- Keep telemetry scoring and schema validation in `src/core/ingestion.py`.
- Keep operator interface changes in `src/apps/`.
- Add focused tests for changed scoring, parsing, logging, or export behavior.
- Treat all model output as **advisory** until an operator or engineer approves the action.
- Expose telemetry values and assumptions behind every recommendation.