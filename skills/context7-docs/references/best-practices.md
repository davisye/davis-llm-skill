# Context7 Best Practices

## Fast selection

- If the user gives `/org/project` or `/org/project/version`, use it directly.
- Otherwise resolve the library ID before querying docs.
- Prefer exact name match plus high source reputation.

## Good query shapes

- Feature plus goal: `server actions form submission example`
- API plus behavior: `useEffect cleanup function example`
- Migration plus version: `migrate from pages router to app router in Next.js 15`
- Integration plus constraint: `Supabase auth middleware for SSR`

## Versioning

- Use a versioned ID when the user names a version or when the API changed across releases.
- If the user says "latest" but no version is required, use the unversioned official library ID unless docs resolution strongly suggests a versioned variant.

## Response template

1. Chosen library ID
2. Why this match
3. Relevant doc findings
4. Minimal example
5. Gaps or assumptions
