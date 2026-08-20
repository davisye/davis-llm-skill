---
name: context7-docs
description: Use when a task needs current, version-specific library or framework documentation, API examples, migration guidance, or prompt patterns backed by Context7. Trigger for requests such as "look up the latest docs", "verify this API still exists", "show the official syntax", "find the right library ID", or "use Context7 for React/Next.js/Supabase/etc".
---

# Context7 Docs

Use this skill when the answer depends on up-to-date library docs instead of model memory. Favor Context7 over guesswork for framework APIs, versioned behavior, migrations, and example code.

## Workflow

1. Identify the target library and whether the user already provided a Context7 library ID such as `/vercel/next.js` or `/facebook/react/v19.2.0`.
2. If no exact library ID is provided, call `resolve-library-id` first.
3. Choose the best match by name, source reputation, snippet coverage, and fit to the user's task.
4. If the user mentions a version, prefer a versioned library ID when available.
5. Call `query-docs` with a narrow, task-shaped query. Ask for the exact feature, API, migration, or pattern the user needs.
6. Answer from the returned docs, citing the chosen library ID and noting when an inference goes beyond the retrieved text.

## Prompt Patterns

Use narrow prompts. Good prompts name the feature, API, version, or outcome.

Good:

- `use context7 for Next.js 15 middleware matcher examples`
- `use context7 with /supabase/supabase for row-level security setup`
- `resolve the right TanStack Query library id, then get invalidation examples for mutations`
- `use /facebook/react/v19.2.0 and show useEffect cleanup examples`

Bad:

- `use context7 for react`
- `get next.js docs`
- `show me supabase`

## Query Rules

- Resolve first when the library is ambiguous.
- Skip resolution when the user already gave an exact Context7 library ID.
- Prefer official or high-reputation sources when multiple matches exist.
- Include a concrete version when version-specific behavior matters.
- Ask one focused docs question at a time instead of one broad "tell me everything" query.
- Query for the user's task, not just a keyword. Example: `app router middleware matcher examples` is better than `middleware`.
- If the first query is too broad, refine it instead of repeating the same call.
- Do not claim Context7 said something unless it was in the retrieved results.

## Answer Style

- State which library ID was chosen.
- If multiple candidates existed, say why one was selected.
- Summarize the relevant docs instead of dumping large excerpts.
- Include short code examples only when they materially help.
- Call out uncertainty when the retrieved docs do not fully answer the user's case.

## When Not To Use

- Do not use this skill for stable general programming knowledge that does not need fresh docs.
- Do not use it when the user only wants brainstorming, rewriting, translation, or opinionated design ideas.
- Do not guess library IDs from memory when a quick resolution call would remove ambiguity.

## Resources

- For concise reminders and reusable phrasing, read [best-practices.md](./references/best-practices.md) when shaping prompts or responses.
