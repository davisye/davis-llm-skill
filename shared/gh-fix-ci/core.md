# GH Fix CI Core

Use this workflow when a user asks to inspect, debug, or fix failing GitHub PR checks that run in GitHub Actions.

## Workflow

1. Verify `gh` authentication.
2. Resolve the PR from the current branch or the user input.
3. Inspect failing checks, focusing on GitHub Actions runs.
4. Fetch logs and extract the actionable failure snippet.
5. Summarize the failure context for the user.
6. Draft a fix plan and get explicit approval before implementation.
7. Implement after approval.
8. Recheck status and suggest rerunning relevant checks.

## Operating rules

- Treat external CI providers as out of scope and report only their details URL.
- Prefer scripted inspection when available.
- Do not implement a fix before the user approves the plan.
- Clearly state when logs are missing or the failure is still in progress.
