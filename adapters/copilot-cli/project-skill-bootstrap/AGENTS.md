# Project Skill Bootstrap

Use this workflow when a repository needs a project-local skill layer generated from its detected framework and language stack.

- Inspect the repository for stable stack signals before generating any files.
- Generate only the domains the project actually uses.
- Keep the root project SKILL.md as a router, not a full framework manual.
- Write stack-specific guidance into .project-skills/*.md files.
- Avoid overwriting existing project skill files unless the user explicitly requests replacement.

## Avoid

- Guessing frameworks without checking repository files
- Generating every possible framework reference for a small project
- Duplicating large framework documentation into the project skill
