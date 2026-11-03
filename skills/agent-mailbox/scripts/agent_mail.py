#!/usr/bin/env python3
"""Read and send mail through the dedicated agent mailbox.

Passwords are read solely from GNOME Keyring. This tool deliberately supports
no state-changing IMAP operations.
"""

from __future__ import annotations

import argparse
import imaplib
import smtplib
import subprocess
import sys
from email import policy
from email.header import decode_header, make_header
from email.message import EmailMessage
from email.parser import BytesParser
from pathlib import Path


ADDRESS = "agent@davisye.cn"
IMAP_HOST = "imap.qiye.aliyun.com"
IMAP_PORT = 993
SMTP_HOST = "smtp.qiye.aliyun.com"
SMTP_PORT = 465
KEYRING_ATTRIBUTES = (
    "service",
    "agent-mailbox",
    "credential",
    "imap-smtp-password",
    "account",
    ADDRESS,
)


def password() -> str:
    """Return the password from Secret Service without exposing it."""
    result = subprocess.run(
        ["secret-tool", "lookup", *KEYRING_ATTRIBUTES],
        check=True,
        capture_output=True,
        text=True,
    )
    value = result.stdout.rstrip("\r\n")
    if not value:
        raise RuntimeError("Agent mailbox password is missing from GNOME Keyring.")
    return value


def imap_client() -> imaplib.IMAP4_SSL:
    client = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT, timeout=30)
    client.login(ADDRESS, password())
    return client


def decode(value: str | None) -> str:
    if not value:
        return ""
    return str(make_header(decode_header(value)))


def fetch_headers(client: imaplib.IMAP4_SSL, uids: list[bytes]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for uid in uids:
        status, data = client.uid(
            "fetch",
            uid,
            "(FLAGS INTERNALDATE BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE MESSAGE-ID)])",
        )
        if status != "OK" or not data or not isinstance(data[0], tuple):
            continue
        metadata, raw_headers = data[0]
        message = BytesParser(policy=policy.default).parsebytes(raw_headers)
        flags = "UNSEEN" if b"\\Seen" not in metadata else "SEEN"
        rows.append(
            {
                "uid": uid.decode(),
                "date": decode(message.get("Date")),
                "from": decode(message.get("From")),
                "subject": decode(message.get("Subject")),
                "status": flags,
            }
        )
    return rows


def select_readonly(client: imaplib.IMAP4_SSL, mailbox: str) -> None:
    status, _ = client.select(mailbox, readonly=True)
    if status != "OK":
        raise RuntimeError(f"Cannot open mailbox read-only: {mailbox}")


def command_check(_: argparse.Namespace) -> None:
    with imap_client() as client:
        select_readonly(client, "INBOX")
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as client:
        client.login(ADDRESS, password())
    print("IMAP and SMTP authentication succeeded.")


def command_list(args: argparse.Namespace) -> None:
    with imap_client() as client:
        select_readonly(client, args.mailbox)
        criteria = "UNSEEN" if args.unread else "ALL"
        status, data = client.uid("search", None, criteria)
        if status != "OK":
            raise RuntimeError("Mailbox search failed.")
        uids = data[0].split()[-args.limit :]
        rows = fetch_headers(client, list(reversed(uids)))
    if not rows:
        print("No messages matched.")
        return
    for row in rows:
        print("\t".join((row["uid"], row["status"], row["date"], row["from"], row["subject"])))


def command_read(args: argparse.Namespace) -> None:
    with imap_client() as client:
        select_readonly(client, args.mailbox)
        status, data = client.uid("fetch", str(args.uid), "(BODY.PEEK[])")
        if status != "OK" or not data or not isinstance(data[0], tuple):
            raise RuntimeError(f"Message UID {args.uid} was not found in {args.mailbox}.")
        sys.stdout.buffer.write(data[0][1])


def command_send(args: argparse.Namespace) -> None:
    body = args.body_file.read_text(encoding="utf-8") if args.body_file else args.body
    message = EmailMessage()
    message["From"] = ADDRESS
    message["To"] = ", ".join(args.to)
    message["Subject"] = args.subject
    message.set_content(body)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=30) as client:
        client.login(ADDRESS, password())
        client.send_message(message)
    print(f"Sent email to: {message['To']}")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("check", help="Authenticate to IMAP and SMTP without sending.").set_defaults(func=command_check)

    list_parser = commands.add_parser("list", help="List message headers without marking messages read.")
    list_parser.add_argument("--mailbox", default="INBOX")
    list_parser.add_argument("--limit", type=int, default=20)
    list_parser.add_argument("--unread", action="store_true")
    list_parser.set_defaults(func=command_list)

    read_parser = commands.add_parser("read", help="Output a raw RFC 822 message without marking it read.")
    read_parser.add_argument("--mailbox", default="INBOX")
    read_parser.add_argument("--uid", type=int, required=True)
    read_parser.set_defaults(func=command_read)

    send_parser = commands.add_parser("send", help="Send a plain-text email.")
    send_parser.add_argument("--to", action="append", required=True)
    send_parser.add_argument("--subject", required=True)
    content = send_parser.add_mutually_exclusive_group(required=True)
    content.add_argument("--body")
    content.add_argument("--body-file", type=Path)
    send_parser.set_defaults(func=command_send)
    return root


def main() -> None:
    args = parser().parse_args()
    if getattr(args, "limit", 1) < 1:
        raise SystemExit("--limit must be at least 1")
    try:
        args.func(args)
    except (OSError, imaplib.IMAP4.error, smtplib.SMTPException, subprocess.CalledProcessError, RuntimeError) as error:
        raise SystemExit(f"agent-mailbox: {error}") from error


if __name__ == "__main__":
    main()
