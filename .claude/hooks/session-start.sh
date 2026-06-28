#!/bin/bash
# SessionStart hook: bootstrap the Python environment so pytest/ruff/mypy work
# in Claude Code on the web sessions. Idempotent and non-interactive.
set -euo pipefail

# Only needed in the remote (Claude Code on the web) container; skip locally.
if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR"

# Create the venv once; the container caches it for later runs.
if [ ! -d .venv ]; then
  python -m venv .venv
fi

# Install the package with dev + analysis tooling (re-runs are cheap).
./.venv/bin/python -m pip install -e ".[dev,analysis]"

# Put the venv on PATH for the rest of the session so tools resolve directly.
ENV_FILE="${CLAUDE_ENV_FILE:-/dev/null}"
echo "export VIRTUAL_ENV=\"$CLAUDE_PROJECT_DIR/.venv\"" >> "$ENV_FILE"
echo "export PATH=\"$CLAUDE_PROJECT_DIR/.venv/bin:\$PATH\"" >> "$ENV_FILE"
