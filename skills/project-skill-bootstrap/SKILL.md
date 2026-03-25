---
name: project-skill-bootstrap
description: Use when a user wants to generate or refresh a project-local SKILL.md and .project-skills references based on the repository's detected stack, especially for Next.js, frontend design consistency, Go, Spring Boot, or Python projects.
---

# Project Skill Bootstrap

Use this skill when the repository should carry its own local skill routing instead of depending on a large global skill set.

This Codex skill is the deployed format for the shared repository workflow defined in `/home/davisye/project/davis-llm-skill/shared/project-skill-bootstrap/core.md`. Keep the semantics aligned with the shared source and generated adapters.

## Workflow

1. Inspect the target project for stable stack signals.
2. Map the detected stack to one or more supported domains.
3. Generate a project root `SKILL.md` that routes Codex to local references.
4. Generate stack-specific references under `.project-skills/`.
5. Review the generated files with the user when the project has mixed stacks or unusual conventions.

## Commands

Generate project-local skills for the current directory:

```bash
python ./scripts/bootstrap_project_skill.py .
```

Generate for another project directory:

```bash
python ./scripts/bootstrap_project_skill.py ~/project/my-app
```

Replace existing generated files:

```bash
python ./scripts/bootstrap_project_skill.py ~/project/my-app --force
```

Preview detected domains without writing files:

```bash
python ./scripts/bootstrap_project_skill.py ~/project/my-app --dry-run
```

## Current supported domains

- `nextjs-app-router`
- `frontend-design-system`
- `golang-backend`
- `springboot-backend`
- `python-engineering`

## Generation rules

- Detect stack from stable files such as `package.json`, `next.config.*`, `go.mod`, `pom.xml`, `build.gradle*`, `pyproject.toml`, and `requirements.txt`.
- Generate only domains that fit the repository.
- Keep the root `SKILL.md` short and routing-oriented.
- Put stack-specific guidance into `.project-skills/*.md`.
- Do not overwrite existing files unless `--force` is used.

## Output

The generator writes:

- `<project>/SKILL.md`
- `<project>/.project-skills/<domain>.md`

The generated root file tells Codex when to read each local reference. The local references capture framework and engineering guidance for that project.
