# Forward-Deployed AI Systems Workbench

This repository is a local-first build environment and template designed for converting ambiguous operational problems into working software, decision surfaces, evaluation harnesses, and deployable artifacts. It is optimized for an OpenAI build loop where **ChatGPT** turns mission ambiguity into architecture, specs, eval plans, and review checklists, while **Codex** works repo-native to implement changes, run tests, inspect failures, and produce deployable artifacts.

The workbench can still host other model providers or agent runtimes, but the default operating doctrine is:

- **ChatGPT as mission architect**: clarify the operator problem, draft acceptance criteria, generate Mermaid diagrams, prepare eval rubrics, pressure-test assumptions, and convert field notes into implementation briefs.
- **Codex as implementation agent**: edit this repository, add tests, run `pytest`/`ruff`, repair broken code paths, summarize diffs, and keep the artifact reproducible from local files.
- **Human as mission owner**: define constraints, approve operational tradeoffs, validate outputs against real users, and decide when the artifact is ready to hand to an operator or engineering team.

## Getting Started

### 1. Open the Workspace in Codex
Open this repository as the active Codex workspace:
`/Users/charlesdegen/Documents/forward-deployed-ai-workbench`

Use ChatGPT for higher-level shaping prompts such as:

```text
Turn this operator workflow into acceptance criteria, a data contract, a test plan, and a Codex-ready build brief.
```

Use Codex for repo-bound execution prompts such as:

```text
Implement the build brief, add focused tests, run the test suite, and summarize the resulting changes.
```

### 2. Configure Environment
Create a `.env` file in the root of this repository if you want live model-backed assistant features:
```bash
OPENAI_API_KEY="your_api_key_here"
```

The starter app remains useful without a key: local telemetry generation, anomaly scoring, charts, alert queues, and fallback triage checklists all run offline.

### 3. Initialize Python Environment
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run the Starter Triage Application
```bash
streamlit run src/apps/streamlit_app.py
```

## Repository Structure

-   `/specs`: Product specifications, data contracts, and operational workflows.
-   `/skills`: Directory containing filesystem-based agent skills and Codex-readable operating guidance (e.g. `triage-skill`).
-   `/src/core`: Core analytical modules (data ingestion, scoring, transformations).
-   `/src/apps`: Front-end interfaces (Streamlit, NiceGUI, or single-file HTML).
-   `/fixtures`: Sample datasets (telemetry logs, CSV extracts) for testing.
-   `/tests`: pytest testing suites.

## ChatGPT / Codex Workflow

1.  **Frame with ChatGPT**: Convert messy field context into a product brief, threat model, acceptance criteria, eval rubric, and demo script.
2.  **Build with Codex**: Ask Codex to implement from the brief, preserve existing repo patterns, add tests near the changed behavior, and run verification commands.
3.  **Review with ChatGPT**: Paste or upload the resulting diff, screenshots, and test output for architecture review, operator-readiness critique, and missing-risk analysis.
4.  **Repair with Codex**: Feed the review back into Codex as a targeted repair brief: specific defects, files, expected behavior, and verification commands.
5.  **Package the artifact**: Produce a local app, single-file HTML export, screenshot set, README, demo script, and evaluation scorecard.

## Codex-Ready Build Brief Template

```text
Goal:
Build or repair [artifact] for [operator workflow].

Constraints:
- Local-first; no external database required.
- Separate computation from UI.
- Keep changes scoped to the existing repo structure.
- Add tests for scoring, parsing, or export behavior.
- Preserve offline fallback behavior when no API key is present.

Inputs:
- Product brief: specs/product_brief.md
- Skill guidance: skills/triage-skill/SKILL.md
- Starter app: src/apps/streamlit_app.py
- Core logic: src/core/ingestion.py

Acceptance:
- App runs with `streamlit run src/apps/streamlit_app.py`.
- Tests pass with `pytest`.
- README explains how ChatGPT and Codex are used in the build loop.
```
