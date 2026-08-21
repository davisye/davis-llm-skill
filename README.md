# davis-llm-skill

A versioned skill pack for **OpenAI Codex** and **DeepSeek Harness (DSH)**.

[中文说明 / README.zh-CN](./README.zh-CN.md)

Skills deploy to the stable catalog at `~/.agents/skills`. The catalog is not a
runtime discovery root: `scripts/build_runtime_skill_views.sh` builds explicit
Codex and DSH views below `~/.agents/runtime-skills/`, and Codex homes link to
the Codex view. This prevents another runtime's skill source from becoming a
Codex skill merely because it is present in the catalog.

## What this repo contains

- Codex-compatible skills under `skills/`
- Shared workflow sources under `shared/`
- Sync / import / install scripts under `scripts/`

## Current skills (30)

`apple-mail`, `attack-tree-construction`, `audio-transcription`,
`browser-act`, `chrome-cdp-browser-control`, `cloudflare`, `commit`,
`context7-docs`, `frontend-design`, `gh-address-comments`, `gh-fix-ci`, `ghidra`,
`github`, `google-workspace`, `librarian`, `local-system-admin-context`,
`native-web-search`, `openscad`, `pi-share`, `ppt-creator`,
`pptx`, `project-skill-bootstrap`, `send-notifications`, `sentry`,
`skill-repo-manager`, `skillsmp-search`, `summarize`, `tmux`,
`update-changelog`, `uv`

## Repository model

1. Put reusable workflow semantics in `shared/<skill-name>/` (core.md + meta.json)
2. Keep the deployment SKILL.md in `skills/<skill-name>/`
3. Sync into the catalog and rebuild runtime views with `scripts/sync_all.sh`

## Directory layout

```text
skills/     Codex skill folders (SKILL.md + supporting files)
shared/     Shared workflow source files
scripts/    Import, install, and sync tools
```

## Sync into the hub

Sync all skills into the catalog at `~/.agents/skills` and rebuild views:

```bash
./scripts/sync_all.sh
```

Sync one skill, or all, into the catalog and rebuild the runtime views:

```bash
./scripts/sync_codex_skill.sh <skill-name>
./scripts/sync_codex_skill.sh --all
```

Force overwrite deployed copies after diff review:

```bash
./scripts/sync_codex_skill.sh --all --force
```

## Import a new skill

Pull a skill that exists in the hub but not in the repo:

```bash
./scripts/import_from_codex.sh
```

Then review `shared/<skill-name>/meta.json`, regenerate nothing (no adapters are
maintained anymore), and commit.

## Install on a new machine

```bash
./scripts/install_codex_skills.sh
```

## Notes

- `local-system-admin-context` is machine-specific; review its
  `references/local-environment.md` baseline before copying to another machine.
- Imported upstream skills must be deployed as catalog-owned directories, never
  as links into another runtime's checkout.
- Runtime ownership and allowlists live in `runtime/skill-index.yaml`. The
  projection script is the enforcement boundary; documentation-only metadata is
  advisory.

## License

This repository includes files copied from `openai/skills` and
`mitsuhiko/agent-stuff` for some skills. Preserve their license files and review
upstream licensing before redistributing modified copies.
