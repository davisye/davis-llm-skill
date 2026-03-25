---
name: skill-repo-manager
description: "Use when working with the davis-llm-skill repository itself: adding skills, syncing them into ~/.codex/skills, preparing multi-client adapters, reviewing drift, or resolving conflicts between the repo copy and deployed copies."
---

# Skill Repo Manager

Use this skill when the task is about maintaining the shared skill repository, not about executing one domain skill.

## Source Of Truth

- Treat `~/project/davis-llm-skill/skills/` as the canonical source for tracked skills.
- Treat `~/.codex/skills/` as a deployed location for Codex.
- Prefer editing the repository copy first, then sync outward.

## Workflow

1. Identify whether the task is repo authoring, repo -> Codex sync, or conflict resolution.
2. Before syncing, inspect whether the deployed target already differs from the repo copy.
3. If there is drift, do not overwrite silently. Review the diff and decide which side wins.
4. Use `scripts/sync_codex_skill.sh <skill-name>` for one skill or `scripts/sync_codex_skill.sh --all` for a full sync.
5. Only use `--force` after reviewing differences and deciding the repo is authoritative.
6. After sync, tell the user whether Codex needs a restart to pick up new or changed skills.
7. When shared skill text changes, regenerate Copilot adapters with `scripts/generate_adapters.py --all` before committing.

## Conflict Rules

- If the repo copy changed and the deployed copy also changed, stop and compare them.
- Do not merge by guesswork when both sides have meaningful edits.
- If the user wants local edits preserved, port them back into the repo before syncing.
- If the repo should overwrite local copies, use `--force` explicitly and say that the deployed copy was replaced.

## Multi-Client Direction

- Keep reusable workflow logic in repository files, not hidden in one installed client.
- Codex consumes `skills/<name>/`.
- Copilot CLI and VS Code Copilot should get generated adapters instead of reusing Codex files verbatim.
- When adding a new adapter, preserve the same workflow semantics and note any client-specific limits.
- For shared-first skills such as `context7-docs`, update `shared/<skill-name>/` first, then port the change to `skills/<skill-name>/` and the client adapters.

## Repository Checklist

When adding or updating a cross-platform skill:

1. Update the shared source under `shared/<skill-name>/`.
2. Update the Codex skill under `skills/<skill-name>/`.
3. Update Copilot CLI files under `adapters/copilot-cli/<skill-name>/`.
4. Update VS Code Copilot files under `adapters/vscode-copilot/<skill-name>/`.
5. Sync the Codex copy into `~/.codex/skills` if the installed version should change.
6. Regenerate adapters if the shared source is authoritative.

## Paths

- Repo root: `/home/davisye/project/davis-llm-skill`
- Codex deploy target: `/home/davisye/.codex/skills`
- Sync script: `/home/davisye/project/davis-llm-skill/scripts/sync_codex_skill.sh`
- Adapter generator: `/home/davisye/project/davis-llm-skill/scripts/generate_adapters.py`
- New-machine installer: `/home/davisye/project/davis-llm-skill/scripts/install_codex_skills.sh`
