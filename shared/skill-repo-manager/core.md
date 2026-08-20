# Skill Repo Manager

Use this skill when the task is about maintaining the shared skill repository, not about executing one domain skill.

## Source Of Truth

- Treat `~/project/davis-llm-skill/skills/` as the canonical source for tracked skills.
- Treat `~/.codex/skills/` as a deployed location for Codex.
- Treat `~/.claude/skills/` as a deployed location for Claude Code.
- Prefer editing the repository copy first, then sync outward.

## Workflow

1. Identify whether the task is repo authoring, repo → platform sync, or conflict resolution.
2. Before syncing, inspect whether the deployed target already differs from the repo copy.
3. If there is drift, do not overwrite silently. Review the diff and decide which side wins.
4. Use `scripts/sync_all.sh` for a full three-way sync, or target specific platforms.
5. Only use `--force` after reviewing differences and deciding the repo is authoritative.
6. After sync, tell the user whether Codex needs a restart to pick up new or changed skills.
7. When shared skill text changes, regenerate adapters with `scripts/generate_adapters.py --all` before committing.

## Conflict Rules

- If the repo copy changed and the deployed copy also changed, stop and compare them.
- Do not merge by guesswork when both sides have meaningful edits.
- If the user wants local edits preserved, port them back into the repo before syncing.
- If the repo should overwrite local copies, use `--force` explicitly and say that the deployed copy was replaced.

## Three-Platform Direction

- Keep reusable workflow logic in `shared/<skill>/` as the canonical source.
- Codex consumes `skills/<name>/SKILL.md`.
- Claude Code consumes `adapters/claude/<name>/SKILL.md`.
- Copilot CLI and VS Code Copilot consume adapters under `adapters/copilot-cli/` and `adapters/vscode-copilot/`.
- When adding a new platform adapter, preserve the same workflow semantics and note any platform-specific limits.
- For shared-first skills, update `shared/<skill-name>/` first, then port changes to skill and adapter files.

## Repository Checklist

When adding or updating a cross-platform skill:

1. Update the shared source under `shared/<skill-name>/`.
2. Update the Codex skill under `skills/<skill-name>/`.
3. Update Claude Code files under `adapters/claude/<skill-name>/`.
4. Update Copilot CLI files under `adapters/copilot-cli/<skill-name>/`.
5. Update VS Code Copilot files under `adapters/vscode-copilot/<skill-name>/`.
6. Sync to all platforms with `scripts/sync_all.sh` or individually.
7. Regenerate adapters with `scripts/generate_adapters.py --all`.

## New Skill Import

When a skill is created directly in Codex or Claude Code:

1. Run `scripts/import_from_codex.sh` or `scripts/import_from_claude.sh` to pull it into the repo.
2. Fill in the generated `shared/<name>/meta.json` with proper metadata.
3. Run `scripts/generate_adapters.py --all` to create adapters for all platforms.
4. Run `scripts/sync_all.sh` to deploy to all platforms.

## Paths

- Repo root: `~/project/davis-llm-skill`
- Codex deploy target: `~/.codex/skills`
- Claude Code deploy target: `~/.claude/skills`
- Sync all: `scripts/sync_all.sh`
- Codex sync: `scripts/sync_codex_skill.sh`
- Claude sync: `scripts/sync_claude_skill.sh`
- Import from Codex: `scripts/import_from_codex.sh`
- Import from Claude: `scripts/import_from_claude.sh`
- Adapter generator: `scripts/generate_adapters.py`
