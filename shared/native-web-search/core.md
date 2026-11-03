# Native Web Search

Use the current runtime's available web search and page-reading tools. Prefer
primary sources, open the pages needed to establish the answer, and cite their
direct URLs. State uncertainty when a claim could not be verified.

Use focused queries and batch independent searches where supported. Match the
depth to the user's request rather than launching a separate model by default.

The retained `search.mjs` is an upstream Pi integration, not a Codex or DSH
entrypoint. Do not execute it from these runtimes or load Pi's settings, modules,
or OAuth credentials. If native search is unavailable, disclose that limitation
and use an available authorized connector instead of another runtime's account.
