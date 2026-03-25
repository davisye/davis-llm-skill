#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 || $# -gt 3 ]]; then
  cat <<'EOF' >&2
Usage:
  install_vscode_copilot_adapter.sh <skill-name> <target-project-dir> [--force]
EOF
  exit 1
fi

SKILL_NAME="$1"
TARGET_DIR="$2"
FORCE="${3:-}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_DIR="$REPO_ROOT/adapters/vscode-copilot/$SKILL_NAME"

if [[ ! -d "$SRC_DIR" ]]; then
  echo "Missing VS Code Copilot adapter for skill: $SKILL_NAME" >&2
  exit 1
fi

mkdir -p "$TARGET_DIR"

if [[ -e "$TARGET_DIR/.github" && "$FORCE" != "--force" ]]; then
  echo "Target already has .github content: $TARGET_DIR/.github" >&2
  echo "Review and rerun with --force if the adapter should overwrite matching files." >&2
  exit 2
fi

mkdir -p "$TARGET_DIR/.github"
cp -a "$SRC_DIR/.github/." "$TARGET_DIR/.github/"
if [[ -d "$SRC_DIR/prompts" ]]; then
  mkdir -p "$TARGET_DIR/.github/prompts"
  cp -a "$SRC_DIR/prompts/." "$TARGET_DIR/.github/prompts/"
fi

cat <<EOF
Installed VS Code Copilot adapter:
  Skill: $SKILL_NAME
  Target: $TARGET_DIR

Files copied from:
  $SRC_DIR
EOF
