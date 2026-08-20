#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import textwrap


REPO_ROOT = Path(__file__).resolve().parent.parent
SHARED_ROOT = REPO_ROOT / "shared"
ADAPTERS_ROOT = REPO_ROOT / "adapters"
CLAUDE_ROOT = ADAPTERS_ROOT / "claude"


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered_list(items: list[str]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, start=1))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def load_meta(skill: str) -> dict:
    meta_path = SHARED_ROOT / skill / "meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"Missing metadata: {meta_path}")
    return json.loads(meta_path.read_text(encoding="utf-8"))


def available_skills() -> list[str]:
    return sorted(
        path.name for path in SHARED_ROOT.iterdir()
        if path.is_dir() and (path / "meta.json").exists()
    )


def generate_claude(skill: str, meta: dict, core_content: str) -> None:
    claude_dir = CLAUDE_ROOT / skill
    description = meta.get("claude_description") or meta.get("description") or meta.get("title") or skill
    allowed_tools = meta.get("claude_allowed_tools")
    tools_line = f"\nallowed-tools: [{', '.join(allowed_tools)}]" if allowed_tools else ""

    frontmatter = f"""---
name: {skill}
description: {description}{tools_line}
---

"""

    write(claude_dir / "SKILL.md", frontmatter + core_content)


def generate(skill: str) -> None:
    meta = load_meta(skill)
    core_path = SHARED_ROOT / skill / "core.md"
    core_content = core_path.read_text(encoding="utf-8") if core_path.exists() else ""

    generate_claude(skill, meta, core_content)

    copilot_dir = ADAPTERS_ROOT / "copilot-cli" / skill
    vscode_dir = ADAPTERS_ROOT / "vscode-copilot" / skill

    agents_md = f"""# {meta['title']}

{meta['copilot_cli_intro']}

{bullet_list(meta['copilot_rules'])}
"""
    if meta.get("copilot_avoid"):
        agents_md += "\n## Avoid\n\n" + bullet_list(meta["copilot_avoid"]) + "\n"

    copilot_instructions = f"""# {meta['title']} Instructions

{meta['copilot_cli_intro']}

{bullet_list(meta['copilot_rules'])}
"""

    vscode_instructions = f"""# Repository Instructions: {meta['title']}

{meta['vscode_intro']}

{bullet_list(meta['vscode_rules'])}
"""

    instruction_rules = meta.get("instruction_rules") or []
    scoped_instructions = textwrap.dedent(
        f"""\
        ---
        applyTo: "**"
        ---

        {instruction_rules[0] if instruction_rules else ""}

        {bullet_list(instruction_rules[1:])}
        """
    )

    prompt_md = f"""# {meta['prompt_title']}

{meta['prompt_intro']}

Checklist:

{numbered_list(meta['prompt_checklist'])}
"""

    write(copilot_dir / "AGENTS.md", agents_md)
    write(copilot_dir / "copilot-instructions.md", copilot_instructions)
    write(vscode_dir / ".github" / "copilot-instructions.md", vscode_instructions)
    write(vscode_dir / ".github" / "instructions" / f"{skill}.instructions.md", scoped_instructions)
    write(vscode_dir / "prompts" / f"{skill}.prompt.md", prompt_md)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Copilot adapter files from shared skill metadata.")
    parser.add_argument("skills", nargs="*", help="Specific skill names to generate")
    parser.add_argument("--all", action="store_true", help="Generate adapters for all configured skills")
    args = parser.parse_args()

    skills = available_skills() if args.all else args.skills
    if not skills:
        parser.error("provide skill names or use --all")

    known = set(available_skills())
    for skill in skills:
        if skill not in known:
            raise SystemExit(f"Unsupported skill for generator: {skill}")
        generate(skill)
        print(f"Generated adapters for {skill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
