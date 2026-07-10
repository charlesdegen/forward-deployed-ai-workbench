#!/usr/bin/env bash
# Prints a stable SHA-256 over every tracked source file that the verify gate covers.
#
# The commit hook compares this against the hash recorded by the last successful
# ./scripts/verify.sh run. A content hash — rather than a timestamp — means editing
# a source file after verifying always invalidates the gate, no matter how fast.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Runtime artifacts (DuckDB files, exports, screenshots) are deliberately excluded:
# they are generated, gitignored, and must not invalidate the gate.
VERIFIED_PATHS=(
  src
  tests
  scripts
  fixtures
  specs
  local-data-fusion-workbench
  financial-crime-ops-console
  llm-red-team-eval-harness
  single-file-command-briefs
  pyproject.toml
  requirements.txt
)

{
  # The file list itself is hashed so that deletions and additions register.
  git ls-files -- "${VERIFIED_PATHS[@]}" | sort
  git ls-files -- "${VERIFIED_PATHS[@]}" | sort | while IFS= read -r file; do
    if [[ -f "$file" ]]; then
      shasum -a 256 "$file"
    else
      echo "DELETED ${file}"
    fi
  done
} | shasum -a 256 | cut -d' ' -f1
