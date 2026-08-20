---
name: gh-address-comments
description: GH Address Comments
---

# GH Address Comments Core

Use this workflow when working on review comments or issue comments for the open GitHub PR of the current branch.

## Workflow

1. Verify `gh` authentication before making GitHub API calls.
2. Resolve the open PR for the current branch, or use the PR specified by the user.
3. Fetch review threads and comments that need attention.
4. Number each thread or comment and summarize what change would be required.
5. Ask the user which numbered items should be addressed.
6. Apply fixes only for the selected items.

## Operating rules

- Run `gh` with sufficient auth scopes for repo and workflow access.
- If authentication fails, ask the user to run `gh auth login` and retry.
- Do not change code for unselected comments.
- Summaries should be concise and actionable.
