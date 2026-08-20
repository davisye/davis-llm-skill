---
name: skillsmp-search
description: SkillsMP Search
---

# SkillsMP Search

Use SkillsMP when the task is to discover community skills by keyword or semantic intent before deciding whether to install, copy, or adapt them.

## Workflow

1. Translate the user's need into one tight search query.
2. Use keyword search for exact terms such as tool names, file formats, or platforms.
3. Use AI semantic search for intent-heavy requests such as "find a skill that helps review PRs".
4. Review the returned candidates before recommending any install.
5. Treat SkillsMP as a discovery layer, not a trust signal. Inspect the linked repository or skill files before adopting anything.

## Query rules

- Prefer keyword search first when the user already knows the target domain or tool.
- Use AI search when the request is goal-oriented and not tied to exact words.
- Keep the query short and concrete.
- Avoid wildcard-style searches and vague prompts such as "best skills".
- When multiple results are similar, compare stars, update recency, repository, and fit to the user's actual workflow.

## Answer style

- State which search mode was used.
- Return a short ranked list with name, author or repo, fit, and any obvious risk.
- Separate "discoveries from SkillsMP" from your own recommendation.
- Do not claim a skill is safe just because it appears in the marketplace.
