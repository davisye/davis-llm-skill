#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML==6.0.3"]
# ///
"""Build isolated skill views from one allowlist without replacing runtime roots."""
import argparse
import os
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


def load_index(path):
    data = yaml.safe_load(path.read_text())
    shared = data.get("shared_catalog_skills", [])
    only = data.get("runtime_only", {})
    retired = data.get("retired_catalog_skills", [])
    all_names = shared + retired + [n for names in only.values() for n in names]
    if any(not isinstance(n, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", n) for n in all_names):
        raise ValueError("invalid skill name in runtime index")
    active = shared + [n for names in only.values() for n in names]
    if len(active) != len(set(active)) or set(active) & set(retired):
        raise ValueError("duplicate or retired active skill in runtime index")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=Path(os.environ.get("RUNTIME_SKILL_INDEX", REPO_ROOT / "runtime/skill-index.yaml")))
    parser.add_argument("--list", action="store_true", help="print deployable catalog names only")
    parser.add_argument("--check", action="store_true", help="read-only verification of installed views")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-home-links", action="store_true")
    args = parser.parse_args()
    data = load_index(args.index)
    shared = data.get("shared_catalog_skills", [])
    only = data.get("runtime_only", {})
    retired = set(data.get("retired_catalog_skills", []))
    active = sorted(set(shared + [n for names in only.values() for n in names]))
    if args.list:
        print("\n".join(active))
        return 0
    catalog = Path(os.environ.get("AGENTS_SKILLS_ROOT", data.get("catalog_root", "~/.agents/skills"))).expanduser().absolute()
    runtime_root = Path(os.environ.get("RUNTIME_SKILL_ROOT", "~/.agents/runtime-skills")).expanduser().absolute()
    plans = []
    for runtime in ("codex", "dsh", "pi"):
        # Pi's private discovery root is never modified here.
        wanted = sorted(set((shared if runtime != "pi" else []) + only.get(runtime, [])))
        rejected = [Path(p).expanduser().resolve() for p in data.get("rejected_runtime_sources", {}).get(runtime, [])]
        view = runtime_root / runtime / "skills"
        for name in wanted:
            source = catalog / name
            if not (source / "SKILL.md").is_file():
                raise ValueError(f"missing catalog skill: {source}")
            resolved = source.resolve()
            if any(resolved == p or p in resolved.parents for p in rejected):
                raise ValueError(f"rejected runtime source: {source}")
            target = view / name
            if target.exists() and not target.is_symlink():
                raise ValueError(f"runtime-local skill needs explicit review before replacement: {target}")
            if not target.is_symlink() or Path(os.readlink(target)) != source:
                plans.append(("link", target, source))
        # Remove only registered retired catalog links, preserving unknown files.
        for name in sorted(retired):
            target = view / name
            if target.is_symlink():
                link = Path(os.path.abspath(target.parent / os.readlink(target)))
                if link != catalog / name:
                    raise ValueError(f"retired name points outside the catalog; refusing removal: {target}")
                plans.append(("unlink", target, None))
            elif target.exists():
                raise ValueError(f"retired runtime entry is not a managed link: {target}")
    if not args.no_home_links:
        home = Path.home()
        for rel in (".codex/skills", ".codex_xinta/.codex/skills", ".codex_xinta/skills", ".codex_xuanzhi/.codex/skills"):
            target = home / rel
            source = runtime_root / "codex/skills"
            if target.is_symlink() and target.resolve() == source.resolve():
                continue
            if target.exists() and not target.is_symlink():
                raise ValueError(f"home discovery root needs explicit review: {target}")
            plans.append(("link", target, source))
    for action, target, source in plans:
        print(f"{action}: {target}" + (f" -> {source}" if source else ""))
    if args.check:
        if plans:
            print(f"{len(plans)} runtime view changes required", file=sys.stderr)
            return 1
        print("Runtime views match the allowlist")
        return 0
    if args.dry_run:
        return 0
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    backup = runtime_root.parent / "runtime-skill-backups" / stamp
    for action, target, source in plans:
        if target.is_symlink():
            # Preserve old links outside every discovery root, including dangling links.
            old = backup / str(target).lstrip("/")
            old.parent.mkdir(parents=True, exist_ok=True)
            target.rename(old)
        if action == "link":
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(source, target_is_directory=True)
    runtime_root.mkdir(parents=True, exist_ok=True)
    installed_index = runtime_root / "skill-index.yaml"
    if not installed_index.exists() or installed_index.read_bytes() != args.index.read_bytes():
        if installed_index.exists():
            backup.mkdir(parents=True, exist_ok=True)
            shutil.copy2(installed_index, backup / "skill-index.yaml")
        temp = installed_index.with_suffix(".yaml.tmp")
        temp.write_bytes(args.index.read_bytes())
        temp.replace(installed_index)
    print(f"Runtime views synchronized; {len(plans)} changes; local and .system directories preserved")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, yaml.YAMLError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
