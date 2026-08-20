#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FORCE=0

usage() {
  cat <<'EOF'
Usage:
  sync_all.sh [--force]

Three-way sync: regenerates all adapters and syncs skills to Codex, Claude Code,
and Copilot adapters. Run after any change to shared/ or skills/.

Steps:
  1. python scripts/generate_adapters.py --all
  2. scripts/sync_codex_skill.sh --all [--force]
  3. scripts/sync_claude_skill.sh --all [--force]
  4. Reports any skills that exist in Codex or Claude but not in repo

EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --force)
      FORCE=1
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

FORCE_FLAG=""
if [[ "$FORCE" -eq 1 ]]; then
  FORCE_FLAG="--force"
fi

echo "=== Step 1/4: Generate adapters ==="
python "$REPO_ROOT/scripts/generate_adapters.py" --all
echo ""

echo "=== Step 2/4: Sync to Codex ==="
"$REPO_ROOT/scripts/sync_codex_skill.sh" --all $FORCE_FLAG
echo ""

echo "=== Step 3/4: Sync to Claude Code ==="
"$REPO_ROOT/scripts/sync_claude_skill.sh" --all $FORCE_FLAG
echo ""

echo "=== Step 4/4: Check for external-only skills ==="
echo ""
echo "Codex-only skills:"
"$REPO_ROOT/scripts/import_from_codex.sh" --dry-run 2>/dev/null || true
echo ""
echo "Claude-only skills:"
"$REPO_ROOT/scripts/import_from_claude.sh" --dry-run 2>/dev/null || true
echo ""

echo "Sync complete. Active skills:"
echo "  Codex:  $(ls "$HOME/.codex/skills/" 2>/dev/null | grep -v '^\.' | wc -l) skills"
echo "  Claude: $(ls "$HOME/.claude/skills/" 2>/dev/null | grep -v '^\.' | wc -l) skills"
echo "  Repo:   $(find "$REPO_ROOT/skills" -mindepth 1 -maxdepth 1 -type d | wc -l) skills"
