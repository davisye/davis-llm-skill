#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC_ROOT="$REPO_ROOT/skills"
# The catalog is deliberately not a Codex runtime root.  Runtime-specific views
# are built from this stable source after the copy completes.
DEST_ROOT="${AGENTS_SKILLS_ROOT:-$HOME/.agents/skills}"
FORCE=0
SYNC_ALL=0
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

usage() {
  cat <<'EOF'
Usage:
  sync_codex_skill.sh <skill-name> [--force]
  sync_codex_skill.sh --all [--force]

Behavior:
  - Syncs skills from the repository into ~/.agents/skills (the catalog)
  - Rebuilds the isolated Codex and DSH runtime views afterwards
  - Refuses to overwrite a changed destination unless --force is used
EOF
}

copy_skill() {
  local name="$1"
  local src="$SRC_ROOT/$name"
  local dest="$DEST_ROOT/$name"
  local backup_root
  if ! printf '%s\n' "${MANAGED[@]}" | grep -Fxq -- "$name"; then
    echo "Skill is retired or not registered: $name" >&2
    return 1
  fi

  if [[ ! -d "$src" ]]; then
    echo "Missing source skill: $name" >&2
    return 1
  fi

  if [[ -e "$dest" ]]; then
    # A matching tree reached through a link into another runtime is still
    # cross-runtime coupling. Preserve that link for rollback, then materialize
    # the repository-owned copy when --force has been explicitly approved.
    if [[ -L "$dest" ]] && [[ "$(readlink -f "$dest")" != "$(readlink -f "$src")" ]]; then
      if [[ "$FORCE" -ne 1 ]]; then
        echo "Conflict: $name is linked outside the catalog at $dest" >&2
        echo "Review the link, then rerun with --force to preserve it as a backup and materialize the repo copy." >&2
        return 2
      fi
      mv "$dest" "$dest.pre-runtime-skill-isolation-$STAMP"
      cp -a "$src" "$dest"
      echo "Materialized: $name"
      return 0
    fi
    if diff -qr --exclude=__pycache__ --exclude="*.pyc" --exclude="*.bak-*" "$src" "$dest" >/dev/null 2>&1; then
      echo "Unchanged: $name"
      return 0
    fi
    if [[ "$FORCE" -ne 1 ]]; then
      echo "Conflict: $name differs at $dest" >&2
      echo "Review diff, then rerun with --force if repo should win." >&2
      return 2
    fi
    backup_root="${SKILL_SYNC_BACKUP_ROOT:-$HOME/.agents/runtime-skill-backups/catalog-$STAMP}"
    mkdir -p "$backup_root"
    mv "$dest" "$backup_root/$name"
  fi

  cp -a "$src" "$dest"
  echo "Synced: $name"
}

SKILLS=()
mapfile -t MANAGED < <(uv run --script "$REPO_ROOT/scripts/build_runtime_skill_views.py" --list)
if [[ "${#MANAGED[@]}" -eq 0 ]]; then
  echo "No registered skills; refusing synchronization" >&2
  exit 1
fi

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
  SKILLS=("${MANAGED[@]}")
fi

if [[ "${#SKILLS[@]}" -eq 0 ]]; then
  usage >&2
  exit 1
fi

for skill in "${SKILLS[@]}"; do
  if ! printf '%s\n' "${MANAGED[@]}" | grep -Fxq -- "$skill"; then
    echo "Skill is retired or not registered: $skill" >&2
    exit 1
  fi
  src="$SRC_ROOT/$skill"
  dest="$DEST_ROOT/$skill"
  if [[ ! -f "$src/SKILL.md" ]]; then
    echo "Missing source skill: $skill" >&2
    exit 1
  fi
  if [[ "$FORCE" -ne 1 && ( -e "$dest" || -L "$dest" ) ]]; then
    if [[ -L "$dest" ]] || ! diff -qr --exclude=__pycache__ --exclude="*.pyc" --exclude="*.bak-*" "$src" "$dest" >/dev/null 2>&1; then
      echo "Conflict: $skill differs at $dest; review before --force" >&2
      exit 2
    fi
  fi
done

status=0
for skill in "${SKILLS[@]}"; do
  if copy_skill "$skill"; then
    :
  else
    status=$?
  fi
done

if [[ "$status" -eq 0 && -x "$REPO_ROOT/scripts/build_runtime_skill_views.sh" ]]; then
  "$REPO_ROOT/scripts/build_runtime_skill_views.sh"
fi

exit "$status"
