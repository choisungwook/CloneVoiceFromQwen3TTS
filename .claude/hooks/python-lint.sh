#!/bin/bash
# Claude Code PostToolUse hook: Python lint check
# Runs black (format check) and ruff (linter) on modified Python files.

set -euo pipefail

VENV_BIN=".venv/bin"

# Read hook input JSON from stdin
INPUT=$(cat)

# Extract file path from tool_input (Edit/Write provide file_path)
FILE=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    fp = data.get('tool_input', {}).get('file_path', '')
    if not fp:
        fp = data.get('tool_response', {}).get('filePath', '')
    print(fp)
except Exception:
    pass
" 2>/dev/null)

# Exit if no file or not a .py file
if [ -z "$FILE" ] || [[ "$FILE" != *.py ]] || [[ ! -f "$FILE" ]]; then
    exit 0
fi

# Check that ruff exists in the venv
if [[ ! -x "$VENV_BIN/ruff" ]]; then
    echo "Warning: ruff not found in .venv. Run 'uv sync' first." >&2
    exit 0
fi

# Auto-fix: ruff format (indent-width = 2)
"$VENV_BIN/ruff" format "$FILE" 2>&1

# Auto-fix: ruff lint
"$VENV_BIN/ruff" check --fix "$FILE" 2>&1
