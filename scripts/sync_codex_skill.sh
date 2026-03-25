#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_ROOT="$REPO_ROOT/skills"
DEST_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
FORCE=0
SYNC_ALL=0

usage() {
  cat <<'EOF'
Usage:
  sync_codex_skill.sh <skill-name> [--force]
  sync_codex_skill.sh --all [--force]

Behavior:
  - Syncs skills from the repository into ~/.codex/skills
  - Refuses to overwrite a changed destination unless --force is used
EOF
}

copy_skill() {
  local name="$1"
  local src="$SRC_ROOT/$name"
  local dest="$DEST_ROOT/$name"

  if [[ ! -d "$src" ]]; then
    echo "Missing source skill: $name" >&2
    return 1
  fi

  if [[ -e "$dest" ]]; then
    if diff -qr "$src" "$dest" >/dev/null 2>&1; then
      echo "Unchanged: $name"
      return 0
    fi
    if [[ "$FORCE" -ne 1 ]]; then
      echo "Conflict: $name differs at $dest" >&2
      echo "Review diff, then rerun with --force if repo should win." >&2
      return 2
    fi
    rm -rf "$dest"
  fi

  cp -a "$src" "$dest"
  echo "Synced: $name"
}

SKILLS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --all)
      SYNC_ALL=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      SKILLS+=("$1")
      shift
      ;;
  esac
done

mkdir -p "$DEST_ROOT"

if [[ "$SYNC_ALL" -eq 1 ]]; then
  while IFS= read -r dir; do
    SKILLS+=("$(basename "$dir")")
  done < <(find "$SRC_ROOT" -mindepth 1 -maxdepth 1 -type d | sort)
fi

if [[ "${#SKILLS[@]}" -eq 0 ]]; then
  usage >&2
  exit 1
fi

status=0
for skill in "${SKILLS[@]}"; do
  if ! copy_skill "$skill"; then
    status=$?
  fi
done

exit "$status"
