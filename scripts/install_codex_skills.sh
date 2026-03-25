#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${1:-https://github.com/DavisYe/davis-llm-skill.git}"
DEST_DIR="${2:-$HOME/project/davis-llm-skill}"

if [[ -d "$DEST_DIR/.git" ]]; then
  git -C "$DEST_DIR" pull --ff-only
else
  mkdir -p "$(dirname "$DEST_DIR")"
  git clone "$REPO_URL" "$DEST_DIR"
fi

"$DEST_DIR/scripts/sync_codex_skill.sh" --all

cat <<EOF
Installed or updated skills from:
  $DEST_DIR

Codex deployed copies synced to:
  ${CODEX_HOME:-$HOME/.codex}/skills

Restart Codex if you added new skills or want the latest copies loaded into a new session.
EOF
