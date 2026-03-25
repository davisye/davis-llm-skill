# GH Address Comments

Use this workflow when handling review comments on the open GitHub PR for the current branch.

- Verify `gh` authentication first.
- Resolve the PR from the current branch unless the user specifies one.
- Fetch review threads and comments needing attention.
- Number them and summarize the required change for each.
- Ask the user which numbered items should be addressed.
- Apply fixes only for the selected comments.
