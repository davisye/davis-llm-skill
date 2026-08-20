#!/usr/bin/env python3
"""Deliver a protected notification job from the user runtime directory."""

from __future__ import annotations

import json
import os
import re
import stat
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path


SETTINGS = Path.home() / ".config/send-notifications/settings.conf"
RUNTIME_DIR = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")) / "send-notifications"
SEND_MAIL = Path.home() / ".local/libexec/send-notifications/send-mail"
VALID_CHANNELS = frozenset({"desktop", "email", "telegram"})
JOB_ID = re.compile(r"^[0-9a-f]{32}$")


class DeliveryError(RuntimeError):
    pass


def read_secret(account: str) -> str:
    result = subprocess.run(
        ["secret-tool", "lookup", "service", "send-notifications", "account", account],
        check=False,
        capture_output=True,
        text=True,
    )
    value = result.stdout.rstrip("\n")
    if result.returncode != 0 or not value:
        raise DeliveryError(f"missing Keyring entry for {account}")
    return value


def read_settings() -> dict[str, str]:
    try:
        info = SETTINGS.stat()
    except FileNotFoundError as exc:
        raise DeliveryError("settings file is missing") from exc
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
        raise DeliveryError("settings file must be owned by the current user and mode 0600")
    settings: dict[str, str] = {}
    for raw_line in SETTINGS.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        key, separator, value = line.partition("=")
        if not separator or key not in {"APP_NAME"} or not value:
            raise DeliveryError("settings file contains an invalid entry")
        settings[key] = value
    return settings


def command(args: list[str], channel: str) -> None:
    result = subprocess.run(args, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        raise DeliveryError(f"{channel} delivery command failed")


def deliver_desktop(title: str, body: str, app_name: str) -> None:
    command(["notify-send", "--app-name", app_name, title, body], "desktop")


def deliver_email(title: str, body_path: Path) -> None:
    recipients = [value for value in read_secret("email-recipients").splitlines() if value]
    if not recipients:
        raise DeliveryError("email-recipients Keyring entry is empty")
    command([str(SEND_MAIL), *sum((["--to", recipient] for recipient in recipients), []), "--subject", title, "--body-file", str(body_path)], "email")


def deliver_telegram(title: str, body: str) -> None:
    token = read_secret("telegram-bot-token")
    chat_id = read_secret("telegram-chat-id")
    payload = json.dumps({"chat_id": chat_id, "text": f"{title}\n\n{body}"}).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status != 200:
                raise DeliveryError("telegram returned a non-success status")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        raise DeliveryError("telegram delivery request failed") from exc


def main(job_id: str) -> int:
    if not JOB_ID.fullmatch(job_id):
        raise DeliveryError("invalid job identifier")
    job_path = RUNTIME_DIR / job_id
    body_path = RUNTIME_DIR / f"{job_id}.body"
    try:
        job = json.loads(job_path.read_text(encoding="utf-8"))
        title = job["title"]
        body = job["body"]
        selected = job["channels"]
        if not isinstance(title, str) or not isinstance(body, str) or not isinstance(selected, list):
            raise DeliveryError("invalid job payload")
        if not selected or not set(selected) <= VALID_CHANNELS:
            raise DeliveryError("job contains unsupported channels")
        settings = read_settings()
        body_path.write_text(body, encoding="utf-8")
        os.chmod(body_path, 0o600)
        for channel in selected:
            if channel == "desktop":
                deliver_desktop(title, body, settings.get("APP_NAME", "send-notifications"))
            elif channel == "email":
                deliver_email(title, body_path)
            else:
                deliver_telegram(title, body)
        return 0
    finally:
        job_path.unlink(missing_ok=True)
        body_path.unlink(missing_ok=True)


if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise DeliveryError("expected one job identifier")
        sys.exit(main(sys.argv[1]))
    except DeliveryError as exc:
        print(f"send-notification: {exc}", file=sys.stderr)
        sys.exit(1)
