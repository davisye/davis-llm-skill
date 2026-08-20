#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_ADAPTERS="$REPO_ROOT/adapters/claude"
SKILLS_DIR="$REPO_ROOT/skills"
SHARED_DIR="$REPO_ROOT/shared"
CLAUDE_SKILLS="${CLAUDE_HOME:-$HOME/.claude}/skills"
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  import_from_claude.sh [--dry-run]

Detects skills in ~/.claude/skills that are not yet in the repo, and imports them.
After importing, regenerate adapters with: python scripts/generate_adapters.py --all
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

if [[ ! -d "$CLAUDE_SKILLS" ]]; then
  echo "No Claude skills directory found at $CLAUDE_SKILLS" >&2
  exit 1
fi

imported=0
while IFS= read -r claude_dir; do
  name="$(basename "$claude_dir")"

  # Skip hidden dirs
  [[ "$name" == .* ]] && continue

  repo_adapter="$CLAUDE_ADAPTERS/$name"
  if [[ -d "$repo_adapter" ]]; then
    continue  # Already in repo
  fi

  echo "Importing: $name"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    imported=1
    continue
  fi

  # Copy Claude adapter to repo
  mkdir -p "$repo_adapter"
  cp -a "$claude_dir"/* "$repo_adapter/" 2>/dev/null || true

  # Create shared/ if it doesn't exist
  shared_skill_dir="$SHARED_DIR/$name"
  if [[ ! -d "$shared_skill_dir" ]]; then
    mkdir -p "$shared_skill_dir"

    # Extract body (skip frontmatter)
    if [[ -f "$repo_adapter/SKILL.md" ]]; then
      awk '
        BEGIN { found=0 }
        /^---$/ { found++; next }
        found >= 2 { print }
      ' "$repo_adapter/SKILL.md" > "$shared_skill_dir/core.md"

      desc=$(awk '/^description:/ { sub(/^description: */, ""); gsub(/"/, "\\\""); print; exit }' "$repo_adapter/SKILL.md")
      title=$(awk '/^name:/ { sub(/^name: */, ""); print; exit }' "$repo_adapter/SKILL.md")
      [[ -z "$desc" ]] && desc="$title"

      cat > "$shared_skill_dir/meta.json" <<METAEOF
{
  "title": "$title",
  "description": "$desc",
  "claude_description": "$desc",
  "copilot_cli_intro": "$desc",
  "copilot_rules": [],
  "vscode_intro": "$desc",
  "vscode_rules": [],
  "instruction_rules": [],
  "prompt_title": "$title Prompt",
  "prompt_intro": "$desc",
  "prompt_checklist": []
}
METAEOF
    fi
  fi

  # Create Codex-format SKILL.md in skills/ if not present
  repo_skill_dir="$SKILLS_DIR/$name"
  if [[ ! -d "$repo_skill_dir" ]] && [[ -f "$repo_adapter/SKILL.md" ]]; then
    mkdir -p "$repo_skill_dir"
    # Generate Codex-format SKILL.md from Claude format (same content, different frontmatter)
    awk '
      BEGIN { found=0 }
      /^---$/ { found++; next }
      found == 1 && /^(name|description|allowed-tools|version|license):/ { next }
      found >= 1 { print }
    ' "$repo_adapter/SKILL.md" > "$repo_skill_dir/SKILL.md"

    # Add codex frontmatter
    sed -i "1i---\nname: $name\ndescription: $desc\n---\n" "$repo_skill_dir/SKILL.md"
  fi

  echo "  -> Imported to $repo_adapter"
  imported=1
done < <(find "$CLAUDE_SKILLS" -mindepth 1 -maxdepth 1 -type d | sort)

if [[ "$imported" -eq 0 ]]; then
  echo "No new skills found in Claude Code."
elif [[ "$DRY_RUN" -eq 1 ]]; then
  echo "Dry run complete. Run without --dry-run to import."
else
  echo ""
  echo "Import complete. Next steps:"
  echo "  python $REPO_ROOT/scripts/generate_adapters.py --all"
  echo "  $REPO_ROOT/scripts/sync_codex_skill.sh --all --force"
  echo "  $REPO_ROOT/scripts/sync_claude_skill.sh --all --force"
fi
