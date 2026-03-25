---
name: skillsmp-search
description: Use when the user wants to search SkillsMP for community skills, compare candidates, or find a skill by tool, workflow, or intent before deciding whether to install it. Trigger for requests such as "search SkillsMP", "find a Codex skill for X", "look up a community skill", or "find a skill that helps with Y".
---

# SkillsMP Search

Use this skill to search SkillsMP from Codex without opening the website manually.

This Codex skill is the deployed format for the shared repository workflow defined in `/home/davisye/project/davis-llm-skill/shared/skillsmp-search/core.md`. Keep the semantics aligned with the shared source and generated adapters.

## Workflow

1. Map the user's request to one concrete search query.
2. Choose search mode:
   - `keyword` for exact tool names, formats, or platform terms
   - `ai` for intent-heavy requests where the user describes a goal rather than known keywords
3. Run `python ./scripts/search_skillsmp.py "<query>"` with optional flags.
4. Review the top candidates before recommending anything.
5. If the user wants to install or adapt a result, inspect the linked repository or skill files first.

## Commands

Keyword search:

```bash
python ./scripts/search_skillsmp.py "codex github review" --mode keyword --limit 5 --sort-by stars
```

AI semantic search:

```bash
python ./scripts/search_skillsmp.py "find a skill that helps review pull request comments" --mode ai
```

JSON output for further processing:

```bash
python ./scripts/search_skillsmp.py "context7" --json
```

## Token handling

The script looks for the API token in this order:

1. `SKILLSMP_API_TOKEN` environment variable
2. `secret-tool lookup service skillsmp key api-token`

Do not hardcode the token into the repository or skill files.

## Query rules

- Prefer keyword search when the user already knows the domain or tool.
- Prefer AI search when the prompt is goal-based rather than name-based.
- Keep the query narrow. One use case is better than five mixed ones.
- Use `--sort-by stars` for mature results and `--sort-by recent` for fast-moving topics.
- Treat SkillsMP as a discovery index, not a trust boundary.

## Answer style

- State which mode you used and why.
- Give a short ranked list with name, URL or repository, and fit.
- Call out obvious risks such as low stars, stale updates, or unclear ownership.
- If a result looks promising, say that the underlying repo should still be reviewed before installation.
