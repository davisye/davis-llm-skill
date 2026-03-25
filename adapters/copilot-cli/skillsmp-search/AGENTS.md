# SkillsMP Search

Use this workflow when GitHub Copilot CLI needs to discover community skills from SkillsMP before installation or adaptation.

- Use keyword search for exact terms such as tool names, formats, and platforms.
- Use AI semantic search for goal-oriented requests when the user does not know exact skill names.
- Keep queries short and concrete.
- Rank results by fit, repository quality signals, stars, and recency.
- Treat marketplace results as discovery only and inspect linked repositories before recommending adoption.

## Avoid

- Treating a marketplace listing as proof of safety
- Using vague searches such as `best skills` without narrowing intent
- Recommending installation before reviewing the underlying repository
