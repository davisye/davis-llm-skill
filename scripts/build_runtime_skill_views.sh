#!/usr/bin/env bash
set -euo pipefail

# Build runtime-specific discovery roots from the immutable-ish catalog.  This
# script never deletes a prior view or an existing Codex skill link: replacement
# links and views are moved to timestamped rollback paths first.

CATALOG_ROOT="${AGENTS_SKILLS_ROOT:-$HOME/.agents/skills}"
RUNTIME_ROOT="${RUNTIME_SKILL_ROOT:-$HOME/.agents/runtime-skills}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INDEX_SOURCE="$REPO_ROOT/runtime/skill-index.yaml"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"

catalog_skills=(
  apple-mail attack-tree-construction audio-transcription browser-act
  chrome-cdp-browser-control cloudflare commit context7-docs frontend-design
  gh-address-comments gh-fix-ci ghidra github google-workspace librarian
  local-system-admin-context native-web-search openscad pi-share ppt-creator
  pptx project-skill-bootstrap runtime-skill-guard send-notifications sentry
  skill-repo-manager skillsmp-search summarize tmux update-changelog uv
)
codex_only_skills=(academic-research-suite)

for skill in "${catalog_skills[@]}"; do
  if [[ ! -f "$CATALOG_ROOT/$skill/SKILL.md" ]]; then
    echo "Missing catalog skill: $CATALOG_ROOT/$skill/SKILL.md" >&2
    exit 1
  fi
done

for skill in "${codex_only_skills[@]}"; do
  if [[ ! -f "$CATALOG_ROOT/$skill/SKILL.md" ]]; then
    echo "Missing Codex-only skill: $CATALOG_ROOT/$skill/SKILL.md" >&2
    exit 1
  fi
done

parent_dir="$(dirname "$RUNTIME_ROOT")"
mkdir -p "$parent_dir"
staging="$(mktemp -d "$parent_dir/.runtime-skills-staging.XXXXXX")"
trap 'rm -rf "$staging"' EXIT

mkdir -p "$staging/codex/skills" "$staging/dsh/skills" "$staging/pi/skills"
cp "$INDEX_SOURCE" "$staging/skill-index.yaml"
for skill in "${catalog_skills[@]}"; do
  ln -s "$CATALOG_ROOT/$skill" "$staging/codex/skills/$skill"
  ln -s "$CATALOG_ROOT/$skill" "$staging/dsh/skills/$skill"
done
for skill in "${codex_only_skills[@]}"; do
  ln -s "$CATALOG_ROOT/$skill" "$staging/codex/skills/$skill"
done

if [[ -e "$RUNTIME_ROOT" || -L "$RUNTIME_ROOT" ]]; then
  mv "$RUNTIME_ROOT" "$RUNTIME_ROOT.rollback-$STAMP"
fi
mv "$staging" "$RUNTIME_ROOT"
trap - EXIT

codex_roots=(
  "$HOME/.codex/skills"
  "$HOME/.codex_xinta/.codex/skills"
  "$HOME/.codex_xinta/skills"
  "$HOME/.codex_xuanzhi/.codex/skills"
)
for root in "${codex_roots[@]}"; do
  target="$RUNTIME_ROOT/codex/skills"
  if [[ -L "$root" && "$(readlink -f "$root")" == "$target" ]]; then
    continue
  fi
  if [[ -e "$root" || -L "$root" ]]; then
    mv "$root" "$root.pre-runtime-skill-isolation-$STAMP"
  fi
  ln -s "$target" "$root"
done

echo "Runtime skill views built at: $RUNTIME_ROOT"
echo "Codex view: $RUNTIME_ROOT/codex/skills"
echo "DSH view:   $RUNTIME_ROOT/dsh/skills"
