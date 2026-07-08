# Product Brief: Mission Autonomy Field Support Console

## Overview
A field-deployable dashboard that enables operators to monitor telemetry, evaluate system diagnostics, detect anomaly drifts, and triage incidents on edge autonomous assets (e.g. UAVs, ground robots) in disconnected or degraded network conditions.

## Target User
-   **Field Operations Engineers (FDEs)**: Needs rapid triage capability to determine if a malfunction is hardware, software, or network-bound.
-   **Edge Operators**: Needs simple, light/dark-mode toggleable interfaces with clear diagnostic instructions.

## Operational Constraints
-   **Local Execution**: The application must run locally on standard operator laptops with no external cloud database requirements.
-   **Sovereign & Degraded Ops**: Network connectivity is expected to be brittle. Telemetry data will be ingested from local CSV or log streams, and diagnostic scoring must run entirely on-device.
-   **Human-Owned Decisions**: AI assistance may draft checklists, briefs, and code changes, but operators and engineers retain final authority over field actions and deployment decisions.

## Core Features
1.  **Telemetry Aggregation**: Synthetic telemetry generation, local CSV ingestion, and required-column schema validation. DuckDB/Polars adapters are reserved for larger local datasets.
2.  **Stateful Diagnostics**: Anomaly ranking based on compute loads, battery state, and sensor drift.
3.  **Operator Action log**: Simple, persistent local CSV logging of triage actions for RCA packets and engineering handoff.
4.  **AI-Assisted Troubleshooting**: Prompt export mode for ChatGPT-ready troubleshooting prompts and Codex-readable `triage-skill` guidance. Live API-backed troubleshooting is a later integration point, not a starter requirement.

## ChatGPT Role
-   Convert field notes and operator interviews into acceptance criteria, telemetry contracts, and scenario-based test plans.
-   Draft diagnostic playbooks from the `triage-skill` and turn alert patterns into operator-facing recovery checklists.
-   Review screenshots, exported RCA packets, and test output for clarity, missing assumptions, and operator readiness.
-   Generate briefing artifacts: Mermaid architectures, demo scripts, threat-model prompts, eval rubrics, and executive summaries.

## Codex Role
-   Modify the repository directly: Streamlit/NiceGUI surfaces, scoring functions, data contracts, fixtures, tests, and export utilities.
-   Run local verification commands such as `pytest`, `ruff`, and app smoke tests after implementation.
-   Repair defects from test failures, operator feedback, or ChatGPT review notes while preserving local-first behavior.
-   Produce implementation summaries with changed files, verification results, and follow-up risks for engineering handoff.

## OpenAI-Specific Acceptance Criteria
-   The README explains how ChatGPT and Codex cooperate across framing, implementation, review, repair, and packaging.
-   The app presents OpenAI prompt export setup using `OPENAI_API_KEY` as optional future configuration while keeping offline fallback triage available without credentials.
-   The `triage-skill` is useful as Codex context: it should specify triage priorities, RCA expectations, and repo-editing constraints.
-   Any model-backed troubleshooting output must expose assumptions, cite the telemetry values that triggered the recommendation, and separate advisory text from operator-approved actions.
