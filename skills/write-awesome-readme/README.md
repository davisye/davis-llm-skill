# Write Awesome README

A Codex skill for creating clear, factual, and useful project README files.

Write Awesome README gives Codex a repeatable workflow for inspecting a repository, choosing the right README sections, and drafting documentation that is grounded in real project evidence instead of generic template filler. It is intended for maintainers and coding agents that need to generate, rewrite, review, or polish README files for software projects.

## Features

- Inspects repository structure before writing documentation.
- Classifies the project type and expected reader before choosing sections.
- Prioritizes copy-pasteable install, quick start, usage, development, and testing instructions when those commands are discoverable.
- Uses explicit `TODO:` notes for missing open-ended facts instead of inventing details.
- Includes guidance for common project types such as libraries, CLIs, apps, APIs, data projects, infrastructure repositories, and architecture-heavy systems.
- Provides a companion reference with README quality patterns distilled from `matiassingers/awesome-readme`.

## Repository Layout

```text
.
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
`-- references/
    `-- readme-patterns.md
```

- `SKILL.md`: the main skill definition, trigger description, workflow, factuality rules, and output behavior.
- `agents/openai.yaml`: OpenAI/Codex-facing display metadata and default prompt.
- `references/readme-patterns.md`: supporting guidance for README structure, visual choices, section recipes, and final review checks.

## Usage

Use the skill when you want Codex to create or improve a repository README:

```text
Use $write-awesome-readme to create a professional README for this repository.
```

Typical requests include:

- Create a README for a new project.
- Rewrite or refresh an existing README.
- Audit a README and identify missing sections or unsupported claims.
- Add sections such as installation, quick start, usage, development, testing, or architecture.
- Turn repository facts into polished project documentation.

## Workflow

The skill guides Codex through a conservative documentation process:

1. Inspect existing repository files, manifests, docs, examples, build files, CI config, license files, and entrypoints.
2. Classify the project and primary reader.
3. Select only sections that can be filled accurately or usefully.
4. Draft a strong first viewport with the project name, tagline, description, and useful proof when available.
5. Verify that install and quick-start commands are traceable to repository files.
6. Review claims, links, commands, badges, license wording, and missing facts before finalizing.

## Development

This repository is documentation-only. There is no package manifest, build system, or automated test suite in the current tree.

When editing the skill:

- Keep `SKILL.md` concise and action-oriented.
- Put detailed reusable guidance in `references/readme-patterns.md`.
- Avoid adding rules that require Codex to invent facts that are not present in the target repository.
- Update `agents/openai.yaml` if the display name, summary, or default prompt changes.

## Verification

There are no automated tests configured for this repository. For changes to the skill, review the files manually and try the default prompt against a small sample repository.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=0xCryptoZen/write-awesome-readme&type=Date)](https://star-history.com/#0xCryptoZen/write-awesome-readme&Date)

## License

MIT License.
