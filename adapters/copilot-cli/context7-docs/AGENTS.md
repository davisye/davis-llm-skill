# Context7 Docs

Use this repository workflow when GitHub Copilot CLI needs up-to-date, version-specific library or framework documentation.

## Operating rules

- Prefer Context7-backed documentation over model memory for evolving APIs.
- If the user provides a Context7 library ID like `/org/project` or `/org/project/version`, use it directly.
- Otherwise resolve the correct library before querying docs.
- Prefer official or high-reputation matches.
- If version-specific behavior matters, choose a versioned library ID.
- Ask narrow, task-shaped questions such as `Next.js 15 middleware matcher examples` instead of broad prompts like `next.js docs`.
- In the answer, state the selected library ID and separate retrieved facts from inference.

## Good prompt shapes

- `Use Context7 for Next.js 15 middleware matcher examples`
- `Use Context7 with /supabase/supabase for row-level security setup`
- `Resolve the correct TanStack Query library id, then get mutation invalidation examples`

## Avoid

- Broad requests with only a library name
- Claiming docs support for something that was not retrieved
- Skipping library resolution when the target is ambiguous
