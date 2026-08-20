# Chrome CDP Browser Control

Control a local GUI Chrome instance through the Chrome DevTools Protocol and Playwright.

- Use the existing project at /home/davisye/workspace/chrome-cdp-control.
- Prefer the separate controllable Chrome over the user's existing browser.
- Keep automation isolated in ~/.cache/chrome-cdp-control.
- Verify control with concrete checks like listing tabs or printing page URLs.
- Do not claim control of pre-existing Chrome windows without CDP enabled.

## Avoid

- Creating duplicate browser-control projects
- Attaching to user's normal Chrome without CDP enabled
- Making broad system changes when CDP connection fails
