---
name: chrome-cdp-browser-control
description: Use when the user wants Codex to start, attach to, or operate a locally visible Chrome browser through Chrome DevTools Protocol (CDP) and Playwright. Trigger for requests such as "use my browser", "open this page in the controllable Chrome", "attach to Chrome over CDP", or "operate the GUI Chrome you can see". For headless automation, web scraping, or fetching rendered pages, use browser-act instead.
---

# Chrome CDP Browser Control

Use this skill when the task is to control a local GUI Chrome instance through CDP instead of only reading web pages.

This machine already has a minimal local setup at `/home/davisye/workspace/chrome-cdp-control`:

- Launcher: `/home/davisye/workspace/chrome-cdp-control/scripts/launch-chrome-cdp.sh`
- Connector: `/home/davisye/workspace/chrome-cdp-control/scripts/connect.js`
- Package root: `/home/davisye/workspace/chrome-cdp-control`

## What This Skill Is For

- Start a separate Chrome instance with `--remote-debugging-port=9222`
- Connect to that browser with `playwright-core`
- List tabs, bring a page to front, open a page, or drive the browser further
- Explain the difference between this controllable Chrome and the user's ordinary Chrome session

## Constraints

- CDP is built into Chrome. There is nothing separate to install for the protocol itself.
- Codex cannot attach to an already running normal Chrome unless that Chrome was started with `--remote-debugging-port`.
- On this machine, the supported path is the separate controllable Chrome launched by the local script above.
- GUI launch and host-level inspection usually require escalated command execution.

## Workflow

1. Confirm whether the user wants the separate controllable Chrome or their existing Chrome session.
2. Prefer the separate controllable Chrome unless the user explicitly wants to relaunch their existing browser.
3. Start Chrome with:

```bash
/home/davisye/workspace/chrome-cdp-control/scripts/launch-chrome-cdp.sh
```

4. Verify control by connecting over CDP:

```bash
cd /home/davisye/workspace/chrome-cdp-control
npm run tabs
```

5. Use the existing helper commands when they fit:

```bash
cd /home/davisye/workspace/chrome-cdp-control
npm run connect
npm run tabs
npm run open
```

6. If the user wants page-specific actions beyond the helper commands, edit `scripts/connect.js` or add another script in the same project instead of inventing a new ad hoc setup elsewhere.

## Operational Rules

- Use the existing project at `/home/davisye/workspace/chrome-cdp-control`; do not create duplicate browser-control projects unless the user asks.
- Keep automation isolated in the dedicated profile directory `~/.cache/chrome-cdp-control`.
- Do not claim control of the user's pre-existing Chrome windows unless CDP was explicitly enabled on them and you verified the endpoint.
- When verifying a live browser, prefer concrete checks such as listing tabs or printing the connected page URL.
- If CDP connection fails, check whether Chrome is still running and whether `127.0.0.1:9222` is listening before making broader changes.

## Answer Style

- Be explicit about whether you are controlling the separate CDP Chrome or the user's existing browser.
- When giving commands, prefer the exact local paths already configured on this machine.
- If a step requires user approval because it launches GUI software or inspects host processes, say so briefly and then request the command execution approval.
