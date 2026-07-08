---
name: triage-skill
description: "Assists edge operators in diagnosing telemetry anomalies and generating troubleshooting checklists for degraded operational states."
---

# Telemetry Triage Skill

This skill provides instructions for identifying and troubleshooting anomalies in autonomous edge systems (UAVs, ground vehicles, and sensors).

## ChatGPT / Codex Operating Model
- Use ChatGPT to transform raw field context into diagnostic hypotheses, acceptance criteria, eval rubrics, and operator-facing briefing language.
- Use Codex to modify the workbench repository, add or repair tests, update Streamlit/NiceGUI views, and verify behavior locally.
- Treat model output as advisory until an operator or engineer approves the action. Always expose the telemetry values and assumptions behind a recommendation.

## Triage Priority Rules
1.  **Safety & Power**: Check power grids, battery depletion rates, and temperature status first. If temperature is > 85°C, advise immediate shutdown.
2.  **Communications**: Check link quality and signal-to-noise ratio. If degraded, check line-of-sight and antenna configurations.
3.  **Sensor Alignment**: Check IMU drift, GPS lock, and camera feed frames. If drifts are high, recommend sensor recalibration.
4.  **Compute & Software**: Check CPU/GPU utilization, memory leakage, and thread counts.

## Root Cause Analysis (RCA) Protocol
When generating an engineering report:
- Identify the primary failing component.
- Highlight telemetry values exceeding normal operating parameters.
- Provide step-by-step diagnostic actions performed.
- Draft recommendations for the base engineering team.

## Codex Repository Constraints
When using this skill inside the workbench repository:
- Keep telemetry scoring logic in `src/core`.
- Keep operator interface changes in `src/apps`.
- Add focused tests under `tests` for any changed scoring, parsing, or export behavior.
- Preserve offline fallback triage behavior when `OPENAI_API_KEY` is not configured.
- Summarize changed files, verification commands, and remaining deployment risks after edits.
