#!/usr/bin/env bash
# Installs the pre-commit hook into .git/hooks/ for this repo clone.
# Run once after cloning the repo. Re-run if the hook source updates.
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOK_SRC="$REPO_ROOT/scripts/hooks/pre-commit"
HOOK_DST="$REPO_ROOT/.git/hooks/pre-commit"

if [ ! -f "$HOOK_SRC" ]; then
  echo "✗ source hook missing at $HOOK_SRC"
  exit 1
fi

cp "$HOOK_SRC" "$HOOK_DST"
chmod +x "$HOOK_DST"
echo "✓ pre-commit hook installed at $HOOK_DST"
echo "  source: $HOOK_SRC"
echo "  test it by trying a commit that bumps app.html without bumping sw.js — should ABORT."
