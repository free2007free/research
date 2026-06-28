#!/bin/bash
# PostToolUse hook: auto-format the just-edited file with ruff if it's Python.
# Reads the tool payload from stdin, extracts tool_input.file_path, and formats
# only that file. Never blocks the edit (always exits 0).
set -euo pipefail

payload="$(cat)"
file="$(printf '%s' "$payload" | python3 -c \
  'import sys,json; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' \
  2>/dev/null || true)"

case "$file" in
  *.py)
    if [ -f "$file" ]; then
      ruff_bin="${CLAUDE_PROJECT_DIR:-.}/.venv/bin/ruff"
      [ -x "$ruff_bin" ] || ruff_bin="ruff"
      "$ruff_bin" format "$file" >/dev/null 2>&1 || true
    fi
    ;;
esac
exit 0
