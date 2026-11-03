---
name: write-awesome-readme
description: Generate, rewrite, review, audit, or improve professional README.md files for software repositories. Use when the user asks to create a README for a project, rewrite or refresh an existing README, review/audit a README and suggest what can be improved or optimized ("check this README", "what's missing", "how can this README be better"), polish a GitHub/open-source README, add specific sections (install, quickstart, usage, development, license, star history), or turn repository facts into clear project documentation.
---

# Write Awesome README

## Overview

Create README files that are clear, factual, scannable, and useful to the project's real audience. Distill the quality patterns from `matiassingers/awesome-readme` into a conservative workflow: inspect the repository first, write only what is supported by evidence, and mark missing information explicitly.

For a new README, a major rewrite, or an audit against "awesome README" quality, read `references/readme-patterns.md` before drafting. For a narrow README edit, use the workflow below and load the reference only if section choice, visuals, or structure is unclear.

## Workflow

1. Inspect the repository before writing.
   - Read any existing `README*`, `docs/`, examples, package manifests, build files, CI config, license files, contribution docs, screenshots, demos, and entrypoints.
   - Prefer fast local discovery with `rg --files`, `rg`, and targeted reads.
   - Identify real commands from files such as `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `Dockerfile`, `compose.yaml`, `pom.xml`, `build.gradle`, `justfile`, or CI workflows.

2. Classify the project and reader.
   - Pick the closest type: library/package, CLI, web/app, API/service, data/ML, infrastructure/devops, documentation/content, architecture-heavy system, or mixed.
   - Write for the first useful reader: evaluator, user, integrator, contributor, maintainer, or operator.
   - Default to English unless the user requests another language or an existing README clearly establishes a different language.

3. Choose sections by evidence, not by template.
   - Always consider: title, tagline, short description, status/badges, visual/demo, features, installation, quick start, usage, configuration, docs links, examples, development, testing, architecture, contributing, license, acknowledgements.
   - Include only sections that can be filled accurately or are useful with `TODO:` placeholders.
   - Add a table of contents only when the README is long enough that navigation helps.
   - **License**: if no `LICENSE`/`COPYING` file exists and package metadata does not declare one, ask the user which license to use (e.g., MIT, Apache-2.0, GPL-3.0, BSD-3-Clause, MPL-2.0, Unlicense, proprietary/none) before writing the section. Do not leave a TODO for license — it is a small bounded choice that the maintainer would have to come back to anyway.
   - **Star History**: for public GitHub repos, explicitly ask the user whether to include a "Star History" section. If yes, embed it with the hosted `star-history.com` chart (no setup, just an image URL) — do not invent a custom chart or screenshot. Template:
     ```markdown
     ## Star History

     [![Star History Chart](https://api.star-history.com/svg?repos=OWNER/REPO&type=Date)](https://star-history.com/#OWNER/REPO&Date)
     ```
     Replace `OWNER/REPO` with the actual GitHub slug discovered from the repo's `origin` remote or `package.json` repository field. Skip the section entirely for private repos, monorepo subfolders without their own repo, or when the user declines.

4. Draft a strong first viewport.
   - Start with project name, a concise tagline, a factual one-paragraph description, and the most useful links or badges.
   - Use screenshots, GIFs, terminal recordings, diagrams, or demo links only when assets or URLs exist. Otherwise add a targeted `TODO:` such as `TODO: Add a screenshot of the dashboard`.
   - Avoid decorative clutter, excessive badges, and unsupported marketing claims.

5. Make the first run succeed.
   - Installation and quick-start commands must be copy-pasteable and traceable to repository files.
   - If prerequisites are not discoverable, mark them as `TODO:` or ask the user.
   - Separate end-user usage from contributor development when both audiences matter.

6. Review before finalizing.
   - Check every command, link, badge, feature claim, version, license statement, and screenshot path.
   - Remove sections that are generic filler.
   - Keep headings conventional so GitHub readers can scan quickly.

## Factuality Rules

- Do not invent features, performance numbers, compatibility claims, install commands, environment variables, roadmap items, maintainers, funding links, support channels, screenshots, badges, or license terms.
- Treat package descriptions, tests, examples, docs, CI, and source entrypoints as evidence; treat names and directory guesses as weak evidence.
- When a fact is missing, choose between `TODO:` and asking the user by the size of the gap:
  - **Ask** when the answer is a small bounded choice from a known set (license, primary language for the README, package name, support channel, target audience). One question is cheaper than a TODO the maintainer must resolve later.
  - **TODO** when the answer is open-ended or expensive to obtain (screenshots, benchmark numbers, future roadmap, third-party links).
  - Batch all questions into one concise message instead of asking one-at-a-time.
- Preserve accurate existing content when rewriting. Improve structure and clarity without discarding project-specific details.
- For public badges, use only links that are clearly correct for the repository or already present.

## Default README Shape

Use this as a flexible starting point, then add/remove sections based on project type and evidence:

```markdown
# Project Name

One-sentence tagline.

Short paragraph explaining what the project does, who it is for, and the main outcome.

## Features
## Installation
## Quick Start
## Usage
## Configuration
## Documentation
## Development
## Testing
## Architecture
## Contributing
## License
```

Do not output an empty template. If a section cannot be completed, either omit it or include a specific `TODO:` that tells the maintainer exactly what information is needed.

## Project-Type Adjustments

- Library/package: prioritize install, minimal import/use example, API links, compatibility, versioning, and examples.
- CLI: prioritize installation, command synopsis, common commands, examples, config, shell completions, and terminal demo if available.
- Web/app: prioritize screenshots/demo, local setup, environment variables, scripts, deployment, and user-facing features.
- API/service: prioritize run instructions, configuration, API docs, auth, example requests, deployment, and operations notes.
- Data/ML: prioritize dataset expectations, environment setup, training/inference/evaluation commands, artifacts, reproducibility, and citations when present.
- Infrastructure/devops: prioritize prerequisites, deployment flow, configuration, security notes, rollback/destroy commands, and supported environments.
- Architecture-heavy systems: include a source map, lifecycle overview, diagrams if present, invariants, and design-decision links.

## Output Behavior

- If the user asks to edit the repository, update `README.md` directly.
- If the user asks for a draft, provide Markdown in the response.
- If replacing an existing README, preserve useful links and verified project-specific material.
- End with a short note listing any assumptions, TODOs, or commands that could not be verified.

## Reference

- `references/readme-patterns.md`: distilled patterns from `matiassingers/awesome-readme`, including visual, section, architecture, and review guidance.
