# davis-llm-skill

A versioned skill pack for OpenAI Codex, GitHub Copilot CLI, and VS Code Copilot.

[中文说明 / README.zh-CN](./README.zh-CN.md)

This repository keeps reusable skill workflows in one place, then maps them into the formats each client understands.

## What this repo contains

- Codex-compatible skills under `skills/`
- Shared workflow sources under `shared/`
- Generated or maintained adapter files for Copilot CLI and VS Code Copilot under `adapters/`
- Utility scripts for generation, sync, and installation under `scripts/`

## Current skills

- `context7-docs`
- `gh-address-comments`
- `gh-fix-ci`
- `local-system-admin-context`
- `project-skill-bootstrap`
- `skillsmp-search`
- `skill-repo-manager`

## Repository model

The repository uses a shared-first workflow:

1. Put reusable workflow semantics in `shared/<skill-name>/`
2. Keep Codex deployment files in `skills/<skill-name>/`
3. Generate or maintain Copilot CLI files in `adapters/copilot-cli/<skill-name>/`
4. Generate or maintain VS Code Copilot files in `adapters/vscode-copilot/<skill-name>/`
5. Sync Codex skills into `~/.codex/skills/` only after reviewing changes

This avoids treating one client's file format as the canonical source for every other client.

## Directory layout

```text
skills/                    Codex skill folders
shared/                    Shared workflow source files
adapters/copilot-cli/      AGENTS.md and Copilot CLI instructions
adapters/vscode-copilot/   VS Code Copilot instructions and prompt files
scripts/                   Generator, installer, and sync tools
```

## Generate adapters

Regenerate adapter files from the shared skill sources:

```bash
python scripts/generate_adapters.py --all
```

Generate only one skill:

```bash
python scripts/generate_adapters.py context7-docs
```

The generator reads machine-readable metadata from `shared/<skill-name>/meta.json`.

## Sync into Codex

Sync one skill into `~/.codex/skills`:

```bash
./scripts/sync_codex_skill.sh context7-docs
```

Sync all tracked skills:

```bash
./scripts/sync_codex_skill.sh --all
```

Force overwrite deployed copies after diff review:

```bash
./scripts/sync_codex_skill.sh --all --force
```

## Install on a new machine

Clone or update the repository, then sync all Codex skills:

```bash
./scripts/install_codex_skills.sh
```

You can also pass a custom repo URL or install directory:

```bash
./scripts/install_codex_skills.sh https://github.com/DavisYe/davis-llm-skill.git ~/project/davis-llm-skill
```

## Install VS Code Copilot files into a project

Copy one skill's VS Code Copilot adapter into a target project:

```bash
./scripts/install_vscode_copilot_adapter.sh context7-docs ~/project/my-app
```

If the target already contains `.github` instruction files and you want this repository copy to win:

```bash
./scripts/install_vscode_copilot_adapter.sh context7-docs ~/project/my-app --force
```

## Cross-platform notes

- Codex consumes `skills/<name>/`
- Copilot CLI consumes instruction-oriented files such as `AGENTS.md`
- VS Code Copilot consumes `.github/copilot-instructions.md`, scoped instruction files, and prompt files
- `local-system-admin-context` is machine-specific and should not be copied to another machine without reviewing its baseline data

## Contribution workflow

1. Update the shared source when the skill has reusable semantics
2. Update `shared/<skill-name>/meta.json` when adapter wording changes
2. Regenerate adapters with `python scripts/generate_adapters.py --all`
3. Update Codex-specific files if needed
4. Sync to local Codex with `./scripts/sync_codex_skill.sh --all`
5. Commit and push

## CI

GitHub Actions validates that generated adapter files are up to date by rerunning the generator and checking for diffs.

## License

This repository includes files copied from `openai/skills` for some skills. Preserve their license files and review upstream licensing before redistributing modified copies.
