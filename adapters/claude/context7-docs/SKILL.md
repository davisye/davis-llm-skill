---
name: context7-docs
description: Context7 Docs
---

# Context7 Docs Core

Use Context7 when a task needs current, version-specific library or framework documentation instead of model memory.

## Trigger conditions

Use this workflow for requests such as:

- look up the latest docs
- verify whether an API still exists
- show the official syntax
- find the correct library ID
- retrieve framework examples for a named library

## Workflow

1. Identify the target library and whether the user already provided a Context7 library ID such as `/vercel/next.js` or `/facebook/react/v19.2.0`.
2. If no exact library ID is provided, resolve the library ID first.
3. Choose the best match by name, source reputation, snippet coverage, and fit to the task.
4. If the user mentions a version, prefer a versioned library ID when available.
5. Query docs with a narrow, task-shaped request for the exact feature, API, migration, or pattern.
6. Answer from the retrieved docs, state the chosen library ID, and mark any inference that goes beyond the returned material.

## Prompt patterns

Good prompts:

- `use context7 for Next.js 15 middleware matcher examples`
- `use context7 with /supabase/supabase for row-level security setup`
- `resolve the right TanStack Query library id, then get invalidation examples for mutations`
- `use /facebook/react/v19.2.0 and show useEffect cleanup examples`

Bad prompts:

- `use context7 for react`
- `get next.js docs`
- `show me supabase`

## Query rules

- Resolve first when the library is ambiguous.
- Skip resolution when the user already gave an exact Context7 library ID.
- Prefer official or high-reputation sources when multiple matches exist.
- Include a concrete version when version-specific behavior matters.
- Ask one focused docs question at a time.
- Query for the task, not just a keyword.
- If the first query is too broad, refine it.
- Do not claim Context7 said something unless it appeared in the retrieved docs.

## Answer shape

1. Chosen library ID
2. Why this match
3. Relevant findings
4. Minimal example if useful
5. Gaps or assumptions

## When not to use

- Stable general programming knowledge that does not need fresh docs
- Brainstorming, translation, rewriting, or opinion-only requests
- Cases where guessing a library ID would be riskier than resolving it
