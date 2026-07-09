# Claude / Grok verify hook

`require-verify.sh` runs on **Bash** PreToolUse when the command looks like `git commit` or `git push`.

- Runs `./scripts/verify.sh` unless `artifacts/.last_verify_ok` is newer than 30 minutes.
- Block exit code: **2**
- Escape hatch: `VERIFY_SKIP_HOOK=1` (emergency only)

Trust project hooks once with `/hooks-trust` (Grok) so project-local hooks are allowed.
