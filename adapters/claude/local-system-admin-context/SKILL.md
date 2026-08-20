---
name: local-system-admin-context
description: Local System Admin Context
---

# Local System Admin Context Core

Use this workflow for tasks that change the local machine's stable software or configuration baseline.

## Workflow

1. Read the current local environment baseline before acting.
2. Verify machine state with commands instead of assuming.
3. Apply the requested local system change.
4. If the stable baseline changed, update the baseline record before finishing.

## Operating rules

- Prefer platform-appropriate instructions over generic advice.
- Distinguish stable baseline changes from transient runtime state.
- Keep the baseline concise and operational.
- Do not treat one machine's baseline as portable to another machine without review.
