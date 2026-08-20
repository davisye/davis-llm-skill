#!/usr/bin/env python3
"""Queue one private notification job for the systemd user manager."""

from __future__ import annotations

import argparse
import json
import os
import secrets
import subprocess
import sys
import tempfile
from pathlib import Path


RUNTIME_DIR = Path(os.environ.get("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")) / "send-notifications"
VALID_CHANNELS = frozenset({"desktop", "email", "telegram"})


def channels(value: str) -> list[str]:
    selected = [item.strip() for item in value.split(",") if item.strip()]
    if not selected:
        raise argparse.ArgumentTypeError("at least one channel is required")
    unknown = set(selected) - VALID_CHANNELS
    if unknown:
        raise argparse.ArgumentTypeError(f"unsupported channel: {sorted(unknown)[0]}")
    return list(dict.fromkeys(selected))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a private local notification.")
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", required=True)
    parser.add_argument("--channels", type=channels, default=list(VALID_CHANNELS))
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.dry_run:
        print("dry run: " + ",".join(args.channels))
        return 0

    old_umask = os.umask(0o077)
    try:
        RUNTIME_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
        job_id = secrets.token_hex(16)
        job_path = RUNTIME_DIR / job_id
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=RUNTIME_DIR, prefix=".job-", delete=False
        ) as job_file:
            json.dump({"title": args.title, "body": args.body, "channels": args.channels}, job_file)
            job_file.flush()
            os.fsync(job_file.fileno())
            temporary_path = Path(job_file.name)
        os.replace(temporary_path, job_path)
    finally:
        os.umask(old_umask)

    result = subprocess.run(
        ["systemctl", "--user", "start", "--wait", f"send-notification@{job_id}.service"],
        check=False,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
