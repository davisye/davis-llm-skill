
# Skill Repo Manager

Use this skill when the task is about maintaining the shared skill repository, not about executing one domain skill.

## Source Of Truth

- Treat `~/project/davis-llm-skill/skills/` and `shared/` as the canonical sources.
- Treat `~/.agents/skills/` as the global skill hub (deployed location): DSH reads it
  directly; the Codex environments (`~/.codex/skills`, `~/.codex_xinta/.codex/skills`,
  `~/.codex_xuanzhi/.codex/skills`) reach it through symlinks.
- Prefer editing the repository copy first, then sync outward into the hub.

## Workflow

1. Identify whether the task is repo authoring, repo -> hub sync, or conflict resolution.
2. Before syncing, inspect whether the deployed target already differs from the repo copy.
3. If there is drift, do not overwrite silently. Review the diff and decide which side wins.
4. Use `scripts/sync_all.sh` to deploy repo skills into the hub, or `scripts/sync_codex_skill.sh` for one skill.
5. Only use `--force` after reviewing differences and deciding the repo is authoritative.
6. After sync, tell the user whether Codex needs a restart to pick up new or changed skills
   (DSH refreshes its skill catalog live via its watcher; no restart needed there).
7. If the hub copy was updated in place (e.g. `local-system-admin-context/references/local-environment.md`
   after a system change), port it back into the repo before committing.

## Conflict Rules

- If the repo copy changed and the deployed copy also changed, stop and compare them.
- Do not merge by guesswork when both sides have meaningful edits.
- If the user wants local edits preserved, port them back into the repo before syncing.
- If the repo should overwrite local copies, use `--force` explicitly and say that the deployed copy was replaced.

## Hub Direction

- Keep reusable workflow logic in `shared/<skill>/` (core.md + meta.json) as the canonical source.
- The deployment SKILL.md lives in `skills/<name>/SKILL.md` and is synced verbatim into the hub.
- No client adapters (Claude / Copilot / VS Code) are maintained anymore; do not regenerate them.
- For shared-first skills, update `shared/<skill-name>/` first, then port the change to `skills/<skill-name>/`.

## Repository Checklist

When adding or updating a skill:

1. Update the shared source under `shared/<skill-name>/` (core.md + meta.json).
2. Update the deployment skill under `skills/<skill-name>/` (SKILL.md + supporting files).
3. Sync to the hub with `scripts/sync_all.sh` (or `scripts/sync_codex_skill.sh <name>`).
4. If the skill is one of the 16 symlinked from upstream `mitsuhiko/agent-stuff`,
   refresh the imported snapshot in the repo after upstream changes.

## New Skill Import

When a skill exists in the hub but not in the repo:

1. Run `scripts/import_from_codex.sh` to pull it into the repo (it reads the hub through
   the `~/.codex/skills` symlink and skips skills already present).
2. Review the generated `shared/<name>/meta.json` and fix CRLF/quotes if the source was CRLF.
3. Commit the import; the hub copy already matches the repo copy byte-for-byte.

## Paths

- Repo root: `/home/davisye/project/davis-llm-skill`
- Global hub: `/home/davisye/.agents/skills` (git-tracked; README documents provenance)
- Codex deploy target: `/home/davisye/.codex/skills` -> symlink to the hub
- Sync all: `scripts/sync_all.sh`
- Codex sync: `scripts/sync_codex_skill.sh`
- Import from hub: `scripts/import_from_codex.sh`
- New-machine installer: `scripts/install_codex_skills.sh`
