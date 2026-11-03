#!/usr/bin/env bash
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec uv run --script "$REPO_ROOT/scripts/build_runtime_skill_views.py" "$@"
