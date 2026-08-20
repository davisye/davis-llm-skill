---
name: send-notifications
description: Use when sending or diagnosing local niri desktop, email, Telegram, or multi-channel notifications through this machine's private systemd notification service.
---

# Send Notifications

Use the local `send-notification` entry point for niri desktop, email, and Telegram delivery. It queues one protected job per request through the user systemd manager; it is not a resident service.

## Send

1. For a non-delivery check, run:

   ```bash
   send-notification --dry-run --title 'Check' --body 'No message is sent.' --channels desktop,email,telegram
   ```

2. For an approved notification, select only the required channels:

   ```bash
   send-notification --title 'Task complete' --body 'The requested operation finished.' --channels email,telegram
   ```

The command succeeds only when every selected channel succeeds. Desktop delivery is best effort: a successful request does not prove the popup was seen.

## Private configuration

Use `send-notification-setup` to interactively store default email recipients, Telegram chat ID, and a rotated Telegram Bot Token in GNOME Keyring. Never paste or print those values. The service reads these accounts:

| Account | Purpose |
| --- | --- |
| `email-recipients` | One recipient per line |
| `telegram-chat-id` | Telegram target |
| `telegram-bot-token` | Rotated Bot API credential |

`~/.config/send-notifications/settings.conf` contains only behavior settings and must remain owned by the current user with mode `0600`.

## Mail integration and diagnosis

Email delivery calls `~/.local/libexec/send-notifications/send-mail`, the verified SMTP implementation archived as a service-internal component. Do not duplicate its SMTP logic.

For a failed request, inspect only the unit result:

```bash
systemctl --user show 'send-notification@*.service' --property=Result --value
```

Do not copy job files, full journal payloads, command lines, Keyring values, or message content into tickets or chat.
