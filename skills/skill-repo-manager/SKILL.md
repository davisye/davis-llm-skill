---
name: skill-repo-manager
description: Maintain the davis-llm-skill canonical repository, deployed skill catalog, source locks, and isolated Codex/DSH discovery views. Use for skill updates, imports, synchronization, or drift review.
---

# Skill Repo Manager

`~/project/davis-llm-skill/skills/` is the canonical deployable source.
`shared/<name>/core.md` and `meta.json` mirror its workflow and discovery metadata.
`~/.agents/skills/` is a deployed catalog, not a shared runtime discovery root.
Codex and DSH use separate views under `~/.agents/runtime-skills/`; never link a
skill into another runtime's private configuration.

## Update and synchronize

1. Inspect repository and catalog drift. Preserve unrelated dirty changes,
   machine-specific baseline updates, and any meaningful local adaptations.
2. For external skills, consult `runtime/skill-sources.json`. Update from an
   official tagged release where available, or record the exact upstream commit.
   Keep supporting resources and licenses together with the entrypoint.
3. Update canonical `skills/` first, then mirror its body and parsed YAML metadata
   into `shared/`. Do not regenerate obsolete client adapters.
4. Register active names and runtime ownership in `runtime/skill-index.yaml`.
   User-retired names stay in `retired_catalog_skills`; never restore them merely
   because their historical source directories remain in the repository.
5. Run `scripts/sync_all.sh`. A conflicting destination must fail visibly before
   any skill is copied. After reviewing the diff, `--force` preserves replaced
   skill directories in a backup outside discovery roots.
6. Run `uv run scripts/check_skill_catalog.py` and
   `scripts/build_runtime_skill_views.sh --check`. Add `--upstream` to the former
   for a read-only source check. It reports changes; it never installs them.
7. Tell the user what changed and what was verified. Open a new Codex conversation
   or restart the client if its skill list is cached; recheck other runtimes' lists
   rather than assuming they refreshed.

## Imports and local ownership

`scripts/import_from_codex.sh --dry-run` inventories catalog and Codex-only installs.
Review the source before importing; the helper skips existing canonical skills.
Register newly imported skills explicitly before building runtime views.

The builder reads the YAML allowlist instead of a second hardcoded list. It
updates managed links incrementally, preserves `.system` and unrelated runtime-local
directories, and removes only explicitly retired catalog links. An active name
occupied by a real local directory requires review before converting it to a link.

Do not edit runtime-owned `.system` skills as part of ordinary catalog updates.
Do not access or migrate credentials while checking skill versions.
