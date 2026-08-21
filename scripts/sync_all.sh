#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FORCE=0

usage() {
  cat <<'EOF'
Usage:
  sync_all.sh [--force]

Sync: deploys the repository's skills into the stable catalog at
~/.agents/skills, rebuilds runtime-specific Codex and DSH views, then reports
any catalog skills missing from the repo. Run after any change to skills/ or
shared/.

Steps:
  1. scripts/sync_codex_skill.sh --all [--force]
  2. Reports any skills that exist in the hub but not in the repo

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

echo "=== Step 1/2: Sync to Codex (hub) ==="
"$REPO_ROOT/scripts/sync_codex_skill.sh" --all $FORCE_FLAG
echo ""

echo "=== Step 2/2: Check for hub-only skills ==="
"$REPO_ROOT/scripts/import_from_codex.sh" --dry-run 2>/dev/null || true
echo ""

echo "Sync complete. Catalog skills:"
echo "  Catalog (~/.agents/skills): $(ls -d "$HOME/.agents/skills/"*/ 2>/dev/null | wc -l) skills"
echo "  Repo: $(find "$REPO_ROOT/skills" -mindepth 1 -maxdepth 1 -type d | wc -l) skills"
