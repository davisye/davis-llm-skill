#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML==6.0.3"]
# ///
"""Read-only skill metadata, deployment drift, and optional upstream checks."""
import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


def files(root):
    result = {}
    for p in root.rglob("*"):
        if not p.is_file() or any(x in {".git", "node_modules", "__pycache__"} for x in p.relative_to(root).parts) or ".bak-" in p.name or p.suffix == ".pyc":
            continue
        result[str(p.relative_to(root))] = hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "davis-skill-readonly-check"}), timeout=20) as response:
        return json.load(response)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-only", action="store_true", help="validate canonical sources without an installed catalog")
    parser.add_argument("--upstream", action="store_true", help="GET official metadata; never update files")
    args = parser.parse_args()
    index = yaml.safe_load((ROOT / "runtime/skill-index.yaml").read_text())
    lock = json.loads((ROOT / "runtime/skill-sources.json").read_text())
    names = sorted(set(index["shared_catalog_skills"] + [n for ns in index["runtime_only"].values() for n in ns]))
    hub = Path(os.environ.get("AGENTS_SKILLS_ROOT", index["catalog_root"])).expanduser()
    failed = False
    largest = (0, "")
    for name in names:
        source, deployed = ROOT / "skills" / name, hub / name
        try:
            text = (source / "SKILL.md").read_text()
            if not text.startswith("---\n"):
                raise ValueError("missing frontmatter fence")
            data = yaml.safe_load(text.split("---", 2)[1])
            desc = data.get("description")
            if data.get("name") != name or not isinstance(desc, str) or not desc.strip():
                raise ValueError("invalid name or description")
            size = len(desc.encode("utf-8"))
            if size > 1024:
                raise ValueError(f"description exceeds 1024 UTF-8 bytes: {size}")
            largest = max(largest, (size, name))
            if name not in lock["skills"]:
                raise ValueError("missing provenance")
            if not args.source_only and files(source) != files(deployed):
                raise ValueError("catalog differs from canonical source")
        except (OSError, ValueError, yaml.YAMLError) as exc:
            print(f"FAIL {name}: {exc}")
            failed = True
    if not failed:
        print(f"PASS {len(names)} skills: metadata, <=1024 UTF-8 bytes, provenance" + ("" if args.source_only else ", and deployed file hashes") + f"; largest={largest[1]}:{largest[0]}")
    if args.upstream:
        cache = {}
        for name in names:
            upstream = lock["skills"][name].get("upstream")
            if not upstream:
                continue
            repo = upstream["repo"]
            ref = upstream.get("ref", "main")
            try:
                key = (repo, ref)
                if key not in cache:
                    info = get_json(f"https://api.github.com/repos/{repo}")
                    tree = get_json(f"https://api.github.com/repos/{repo}/git/trees/{ref}?recursive=1")
                    if tree.get("truncated"):
                        raise ValueError("upstream tree response is truncated")
                    cache[key] = (info, {x["path"]: x for x in tree["tree"]})
                info, tree = cache[key]
                entry_path = (upstream["path"].rstrip("/") + "/" if upstream["path"] else "") + "SKILL.md"
                entry = tree.get(entry_path)
                pinned_blob = upstream.get("entry_blob")
                state = "ARCHIVED" if info.get("archived") else "REMOVED" if not entry else "CHANGED" if pinned_blob and entry["sha"] != pinned_blob else "UNCHANGED" if pinned_blob else "UNPINNED"
                print(f"UPSTREAM {name}: {state} ({repo}@{ref}); local overlays={bool(lock['skills'][name].get('local_overlays'))}")
            except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
                print(f"UPSTREAM {name}: UNKNOWN ({exc})")
                failed = True
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
