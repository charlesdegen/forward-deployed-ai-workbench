# Deployment

## Local operator laptop (default)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./scripts/verify.sh
```

| Surface | Command | Port |
|---|---|---|
| Mission Console | `python src/apps/nicegui_app.py` | 8080 |
| Streamlit starter | `streamlit run src/apps/streamlit_app.py` | 8501 |
| Data Fusion | `python local-data-fusion-workbench/fusion/apps/nicegui_app.py` | 8081 |
| Fin Crime | `streamlit run financial-crime-ops-console/fin_crime/apps/streamlit_app.py` | 8501+ |
| Red-Team | `streamlit run llm-red-team-eval-harness/redteam/apps/streamlit_app.py` | 8501+ |
| Command brief | open `single-file-command-briefs/index.html` | n/a |

## Constrained / air-gapped notes

- Core scoring and DuckDB paths need only the venv wheels already installed.
- Single-file brief embeds narrative JSON; CDN CSS/JS may be blocked — content still readable if you strip script tags or vendor assets offline later.
- Never copy `.env` or `artifacts/*` operator logs into shared drives without review.

## Packaging options

1. **Zip export** — repo subset + `.venv` instructions (no secrets).
2. **Single-file HTML** — executive snapshot for email/USB.
3. **GitHub** — `origin` → `charlesdegen/forward-deployed-ai-workbench`.

## Optional security lane

```bash
source .venv/bin/activate
bandit -r src financial-crime-ops-console/fin_crime llm-red-team-eval-harness/redteam local-data-fusion-workbench/fusion -ll
pip-audit
```

Wired as non-blocking optional step in `scripts/verify.sh` when `VERIFY_SECURITY=1`.

## Playwright smoke

```bash
pip install playwright && playwright install chromium
python scripts/smoke_ui.py              # single-file brief (fast)
SMOKE_FULL=1 python scripts/smoke_ui.py # mission + fin-crime apps
```

`./scripts/verify.sh` runs the fast smoke by default (`VERIFY_SMOKE=0` to skip).

## Agent hooks (commit/push gate)

Project hooks in `.claude/settings.json` and `.grok/hooks/require-verify.json` block `git commit` / `git push` Bash tool calls unless `./scripts/verify.sh` has passed recently (or runs it). Escape hatch: `VERIFY_SKIP_HOOK=1`. Grok: trust the folder with `/hooks-trust` once.
