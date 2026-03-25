# Project Skill Bootstrap

Use this workflow when a user wants a project-local skill layer that matches the repository's actual stack instead of relying on a large global skill set.

## Workflow

1. Inspect the repository for stable stack signals such as `package.json`, `next.config.*`, `go.mod`, `pom.xml`, `build.gradle*`, `pyproject.toml`, or `requirements.txt`.
2. Infer a small set of project-relevant domains.
3. Generate or update a project root `SKILL.md`.
4. Write focused references under `.project-skills/` for each detected domain.
5. Keep the generated project skill lightweight. It should route Codex to the right local references, not duplicate whole framework manuals.

## Design rules

- Prefer deterministic file checks over guesswork.
- Generate only the domains that the repository actually uses.
- Keep project `SKILL.md` as a router and policy layer.
- Keep stack-specific guidance in `.project-skills/*.md`.
- Do not overwrite existing files unless the user explicitly asks or a `--force` flag is used.

## Current supported domains

- `nextjs-app-router`
- `frontend-design-system`
- `golang-backend`
- `springboot-backend`
- `python-engineering`

## Output contract

Generate:

- `<project>/SKILL.md`
- `<project>/.project-skills/<domain>.md`

The root `SKILL.md` should:

- describe the detected stack
- say when to open each local reference
- set routing priority when multiple domains apply
