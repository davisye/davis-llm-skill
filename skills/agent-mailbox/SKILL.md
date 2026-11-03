---
name: agent-mailbox
description: "Use when reading, checking, or sending email through the dedicated agent@davisye.cn mailbox."
---

# Agent Mailbox

Use this skill for the dedicated `agent@davisye.cn` enterprise mailbox. It is separate from the machine notification sender: use it when an agent needs to read or send ordinary email.

Run `scripts/agent_mail.py` from this skill directory. It reads its password only from the user's GNOME Keyring and never accepts one on the command line, in an environment variable, or from a file.

## Safety

- Listing and reading mail are read-only. The script uses IMAP `readonly` mode and `BODY.PEEK`, so it does not mark messages read.
- Treat mail content, recipients, and attachments as potentially sensitive. Summarize only what the user asked for; do not paste raw messages or credential-related output into chat or tickets.
- Sending email is an external action. Before running `send`, confirm the recipients, subject, and body with the user unless all three were explicitly provided in the current request. Prefer `--body-file` for substantial content.
- Never run mailbox delete, move, flag, or mark-read operations. This skill intentionally does not implement them.

## Commands

```bash
MAILBOX_SKILL="$HOME/.codex/skills/agent-mailbox"

# Authenticate to IMAP and SMTP without sending a message.
python3 "$MAILBOX_SKILL/scripts/agent_mail.py" check

# List recent headers; default mailbox is INBOX.
python3 "$MAILBOX_SKILL/scripts/agent_mail.py" list --limit 20 --unread

# Read one message by its displayed UID without marking it read.
python3 "$MAILBOX_SKILL/scripts/agent_mail.py" read --uid 1234

# Send after the required confirmation.
python3 "$MAILBOX_SKILL/scripts/agent_mail.py" send --to recipient@example.com \\
  --subject 'Subject' --body-file /path/to/body.txt
```

The initial password enrollment is a one-time local-admin operation. It must put the password in GNOME Keyring under the attributes documented in `scripts/agent_mail.py`, then securely remove the source password file. Do not store credentials in the skill directory.
