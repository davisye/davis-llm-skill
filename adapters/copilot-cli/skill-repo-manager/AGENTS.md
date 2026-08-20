# Skill Repo Manager

Maintain the shared skill repository: sync skills across Codex, Claude Code, and Copilot. Manage adapters and resolve conflicts.

- Treat the repo as canonical source of truth.
- Do not overwrite deployed skills unless differences are reviewed.
- Regenerate adapters after shared source changes.
- Use sync scripts, never manually copy to deployed directories.
- Port local edits back to the repo before syncing outward.

## Avoid

- Overwriting deployed skills without review
- Manually copying files instead of using sync scripts
- Merging conflicts by guesswork
