#!/usr/bin/env bash
# PreToolUse guard: block git commit / push when the portfolio verify gate is dirty.
# Exit 0 = allow, exit 2 = block (Claude Code / Grok PreToolUse convention).
set -euo pipefail

ROOT="${CLAUDE_PROJECT_DIR:-${GROK_PROJECT_DIR:-}}"
if [[ -z "${ROOT}" ]]; then
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi
cd "$ROOT"

# stdin may contain JSON tool payload — collect command text if present
INPUT="$(cat || true)"
CMD=""
if command -v python3 >/dev/null 2>&1; then
  CMD="$(printf '%s' "$INPUT" | python3 -c '
import json,sys
raw=sys.stdin.read().strip()
if not raw:
    raise SystemExit(0)
try:
    data=json.loads(raw)
except Exception:
    print(raw)
    raise SystemExit(0)
# Claude / Grok shapes
tool = data.get("tool_name") or data.get("tool") or ""
inp = data.get("tool_input") or data.get("input") or data
if isinstance(inp, dict):
    print(inp.get("command") or inp.get("cmd") or "")
else:
    print(str(inp))
' 2>/dev/null || true)"
else
  CMD="$INPUT"
fi

# Only gate commit / push style commands
if ! printf '%s' "$CMD" | grep -Eiq '(^|[[:space:];|&])git[[:space:]]+(commit|push)'; then
  exit 0
fi

if [[ "${VERIFY_SKIP_HOOK:-0}" == "1" ]]; then
  echo "require-verify: VERIFY_SKIP_HOOK=1 — allowing git without re-verify" >&2
  exit 0
fi

STAMP="artifacts/.last_verify_ok"
NEED_RUN=1
if [[ -f "$STAMP" ]]; then
  # Accept stamp younger than 30 minutes
  if command -v python3 >/dev/null 2>&1; then
    AGE="$(python3 -c "import time,pathlib; p=pathlib.Path('$STAMP'); print(int(time.time()-p.stat().st_mtime))")"
    if [[ "$AGE" -lt 1800 ]]; then
      NEED_RUN=0
    fi
  fi
fi

if [[ "$NEED_RUN" == "1" ]]; then
  echo "require-verify: running ./scripts/verify.sh before git commit/push..." >&2
  if ! ./scripts/verify.sh; then
    echo "require-verify: verify failed — commit/push blocked" >&2
    exit 2
  fi
else
  echo "require-verify: recent verify stamp present ($STAMP)" >&2
fi

exit 0
