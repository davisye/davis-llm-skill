#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$REPO_ROOT/skills"
SHARED_DIR="$REPO_ROOT/shared"
CODEX_SKILLS="${CODEX_HOME:-$HOME/.codex}/skills"
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  import_from_codex.sh [--dry-run]

Detects skills in ~/.codex/skills that are not yet in the repo, and imports them.
After importing, review metadata and register names in runtime/skill-index.yaml.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ ! -d "$CODEX_SKILLS" ]]; then
  echo "No Codex skills directory found at $CODEX_SKILLS" >&2
  exit 1
fi

imported=0
while IFS= read -r codex_dir; do
  name="$(basename "$codex_dir")"

  # Skip .system and hidden dirs
  [[ "$name" == .* ]] && continue

  repo_skill_dir="$SKILLS_DIR/$name"
  if [[ -d "$repo_skill_dir" ]] && [[ -f "$repo_skill_dir/SKILL.md" ]]; then
    continue  # Already in repo
  fi

  echo "Importing: $name"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    imported=1
    continue
  fi

  # Copy entire skill to repo
  mkdir -p "$repo_skill_dir"
  cp -a "$codex_dir"/* "$repo_skill_dir/" 2>/dev/null || true

  # Create shared/core.md from SKILL.md (strip YAML frontmatter)
  if [[ -f "$repo_skill_dir/SKILL.md" ]]; then
    shared_skill_dir="$SHARED_DIR/$name"
    mkdir -p "$shared_skill_dir"

    # Extract body (skip frontmatter between --- markers); normalize CRLF
    awk '
      BEGIN { skip=0; found=0 }
      /^---\r?$/ { found++; next }
      found >= 2 { sub(/\r$/, ""); print }
      found == 1 { skip=1 }
    ' "$repo_skill_dir/SKILL.md" > "$shared_skill_dir/core.md"

    # Extract description from frontmatter for meta.json (strip CRLF and
    # surrounding quotes so the value embeds cleanly in JSON)
    desc=$(awk '/^description:/ { sub(/^description: */, ""); sub(/\r$/, ""); sub(/^"/, ""); sub(/"$/, ""); gsub(/"/, "\\\""); print; exit }' "$repo_skill_dir/SKILL.md")
    title=$(awk '/^name:/ { sub(/^name: */, ""); sub(/\r$/, ""); print; exit }' "$repo_skill_dir/SKILL.md")
    [[ -z "$desc" ]] && desc="$title"

    cat > "$shared_skill_dir/meta.json" <<METAEOF
{
  "title": "$title",
  "description": "$desc"
}
METAEOF
  fi

  echo "  -> Imported to $repo_skill_dir"
  imported=1
done < <(find -L "$CODEX_SKILLS" -mindepth 1 -maxdepth 1 -type d | sort)

if [[ "$imported" -eq 0 ]]; then
  echo "No new skills found in Codex."
elif [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Dry run complete. Run without --dry-run to import."
else
  echo ""
  echo "Import complete. Next steps:"
  echo "  Review shared metadata and register names in runtime/skill-index.yaml"
  echo "  $REPO_ROOT/scripts/sync_all.sh"
  echo "  Review any reported conflicts before synchronizing."
fi
