# davis-llm-skill

This repository is the source of truth for reusable LLM skills shared across Codex, GitHub Copilot CLI, and VS Code assistants.

## Goals

- Keep reusable skills under version control.
- Separate shared workflow content from client-specific adapters.
- Provide a safe sync path into `~/.codex/skills` without blindly overwriting local edits.

## Layout

- `skills/`: canonical skill folders in Codex-compatible format
- `shared/`: reusable references, templates, and future normalized source files
- `scripts/`: sync and maintenance scripts
- `adapters/codex/`: notes or generated files for Codex-specific packaging
- `adapters/copilot-cli/`: future GitHub Copilot CLI instruction adapters
- `adapters/vscode-copilot/`: future VS Code Copilot instruction adapters

## Adapter strategy

- Put shared workflow semantics in `shared/<skill-name>/`.
- Keep `skills/<skill-name>/` as the Codex deployment format.
- Generate or maintain Copilot-focused files under `adapters/copilot-cli/<skill-name>/`.
- Generate or maintain VS Code Copilot files under `adapters/vscode-copilot/<skill-name>/`.
- Do not assume Copilot can consume Codex `SKILL.md` directly.

The first example is `context7-docs`:

- Shared source: `shared/context7-docs/core.md`
- Codex skill: `skills/context7-docs/`
- Copilot CLI adapter: `adapters/copilot-cli/context7-docs/`
- VS Code Copilot adapter: `adapters/vscode-copilot/context7-docs/`

The same pattern now exists for:

- `gh-address-comments`
- `gh-fix-ci`
- `local-system-admin-context`

## Current source policy

- For now, `skills/` is the canonical source for existing Codex skills.
- Local installed skills under `~/.codex/skills` are treated as deployed copies.
- Edits should be made in this repository first, then synced outward.

## Sync policy

- Default sync direction is repo -> `~/.codex/skills`.
- If a target skill already exists and differs, sync refuses to overwrite unless `--force` is passed.
- Before force-overwriting, review the diff and decide which side is authoritative.
- Do not edit the same skill independently in multiple installed locations.

## Common workflows

Sync one skill into Codex:

```bash
./scripts/sync_codex_skill.sh context7-docs
```

Sync all tracked skills into Codex:

```bash
./scripts/sync_codex_skill.sh --all
```

Force overwrite deployed copies after reviewing diffs:

```bash
./scripts/sync_codex_skill.sh --all --force
```

## Next steps

- Add adapter generators for Copilot CLI and VS Code Copilot instruction files.
- Normalize shared content so one workflow can emit multiple client formats.
- Add install/update commands for other machines.
