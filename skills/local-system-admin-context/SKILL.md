---
name: local-system-admin-context
description: Use when tasks involve software installation, package management, system configuration, desktop environment setup, shell/tool configuration, or service changes on the user's local machine. Before making changes, read references/local-environment.md. After finishing the task, update that file if the machine's stable software or configuration baseline changed.
---

# Local System Admin Context

Use this skill for tasks that change the local machine's software or stable configuration, including:

This Codex skill is the deployed format for the shared repository workflow defined in `/home/davisye/project/davis-llm-skill/shared/local-system-admin-context/core.md`. Keep the semantics aligned with the shared source, but treat the baseline reference as machine-specific.

- Installing, removing, or upgrading software packages
- Configuring desktop, display, shell, terminal, input method, fonts, or themes
- Changing system services, startup behavior, users, groups, permissions, or paths
- Editing config files for locally installed tools

## Required workflow

1. Before acting, open `references/local-environment.md` and treat it as the current machine baseline.
2. When the task depends on actual machine state, verify with commands instead of assuming.
3. If the task changes the stable baseline, update `references/local-environment.md` before ending the task.
4. Do not add transient state such as current memory usage, disk usage, uptime, temporary IPs, or process snapshots unless the user explicitly asks for them.

## What counts as a baseline update

Update the reference file when any of these change:

- OS, kernel policy, boot mode, filesystem notes
- Desktop/session stack such as Wayland/X11, compositor, WM, DE
- Primary shell, terminal, editor, package helper, service manager usage
- Installed tools that materially affect future guidance
- Important local conventions or constraints discovered during the task

Do not update it for:

- One-off command output
- Temporary failures
- Runtime resource usage
- Logs or ephemeral service state

## Update style

- Keep the file concise and in Chinese.
- Prefer stable facts and operational conventions.
- Preserve existing useful content; revise instead of appending noisy history.
