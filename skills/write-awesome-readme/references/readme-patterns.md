# README Patterns

This reference distills recurring patterns from `matiassingers/awesome-readme` into reusable README decisions. Use it to choose the right sections and polish level for a specific repository.

## Core Qualities

- Clear first impression: project name, concise tagline, useful badges, and a plain explanation of what the project does.
- Fast proof: screenshot, GIF, terminal demo, diagram, live demo, generated output, or short code sample near the top when available.
- Reliable first run: installation, prerequisites, quick start, and usage examples that match real repository commands.
- Scannable structure: conventional headings, short paragraphs, tables for dense options, and a table of contents for long READMEs.
- Trust signals: license, CI/test status, package/version badges, docs links, contribution guide, security policy, support/community links, and release/download links when real.
- Depth on demand: keep the README focused and link to docs, API references, architecture docs, examples, or wiki pages for long-form material.

## First Viewport Recipe

Use this order when the project has enough evidence:

1. Project logo or name.
2. One-sentence tagline.
3. Relevant badges only.
4. One short paragraph answering: what it is, who it helps, and why it exists.
5. Primary proof: screenshot, GIF, terminal recording, diagram, or minimal code sample.
6. Quick links: documentation, demo, examples, releases, contributing, license.

Skip visuals when no asset exists; add a precise TODO only if a visual would materially improve comprehension.

## Section Recipes by Project Type

### Library or Package

- Install from the real package manager.
- Show the smallest useful import/use example.
- Link to API docs or examples if present.
- Include compatibility/runtime requirements only when verified.
- Include advanced examples, migration notes, or alternatives only when supported by docs or source.

### CLI

- Show install methods and the command name.
- Include a command synopsis and common workflows.
- Use terminal examples with expected output when examples or tests verify behavior.
- Mention config files, environment variables, completions, and exit behavior only when discoverable.
- A GIF or terminal recording is valuable for CLIs with interactive output.

### Web App or Desktop/Mobile App

- Lead with a screenshot, GIF, live demo, or release/download link when present.
- Separate user-facing features from developer setup.
- Include local development commands, environment setup, build, test, and deploy instructions.
- Use tables for platform downloads or feature comparisons when relevant.

### API or Service

- Explain the service boundary and primary use cases.
- Include local run instructions, configuration, and dependency setup.
- Link to OpenAPI/Swagger, generated docs, route files, or examples when present.
- Provide one minimal request/response example only if the route and shape are verified.
- Include deployment and operations notes when Docker, compose, IaC, or CI evidence exists.

### Data, ML, or Research

- State the task, data expectations, and outputs.
- Include reproducible setup and commands for training, inference, evaluation, or notebooks.
- Link datasets, model artifacts, papers, or citations only when present.
- Clarify hardware/runtime requirements only when documented or inferable from config.

### Infrastructure or DevOps

- Put prerequisites and safety notes before apply/deploy commands.
- Include setup, plan/dry-run, deploy, verify, rollback, and destroy flows when supported.
- Document required variables, secrets, providers, and environments from real config.
- Avoid suggesting destructive commands unless the repo already documents them.

### Architecture-Heavy Repositories

- Add a source map: major directories and why they exist.
- Include lifecycle, request flow, data flow, or build pipeline diagrams if present.
- Call out invariants, design decisions, extension points, and constraints.
- Link to `ARCHITECTURE.md`, ADRs, docs, or wiki pages instead of duplicating everything.

## Visual Guidance

- Screenshots work best for UI apps, dashboards, generated documents, games, and design-heavy projects.
- GIFs or terminal recordings work best for CLIs, editors, workflows, animations, and before/after transformations.
- Diagrams work best for services, protocols, infrastructure, compilers, engines, and multi-component systems.
- Tables work best for install choices, command options, feature comparisons, environment variables, compatibility, and downloads.
- Badges should be useful, current, and few: CI, coverage, package version, downloads, docs, license, security, or platform support.
- Star history (optional, public GitHub repos only): if the user opts in, embed the hosted `star-history.com` SVG (`https://api.star-history.com/svg?repos=OWNER/REPO&type=Date`) rather than committing a static screenshot — the hosted chart stays current with no maintenance.

## Writing Rules

- Prefer concrete nouns and verbs over generic claims like "powerful", "simple", or "next-generation".
- Explain the outcome before implementation details.
- Keep code examples minimal but runnable.
- Put long configuration, API surfaces, and exhaustive option lists in docs when possible.
- For missing facts, prefer asking the user when the answer is a small bounded choice (license, primary language, package name); use `TODO:` only for open-ended gaps (screenshots, benchmark numbers, roadmap).
- Keep tone professional and direct; match a friendly open-source tone only when the project already uses it.

## Final Checklist

- The first screen tells a new reader what the project is.
- Every install, run, build, and test command is traceable to repo files.
- Features are supported by code, docs, examples, or tests.
- Links and relative asset paths are valid.
- Badges point to the correct repository/package.
- License wording matches the actual license file or package metadata.
- Missing facts are explicit TODOs or questions.
- The README has enough detail for first use without becoming a full manual.
