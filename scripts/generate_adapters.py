#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import textwrap


REPO_ROOT = Path(__file__).resolve().parent.parent
SHARED_ROOT = REPO_ROOT / "shared"
ADAPTERS_ROOT = REPO_ROOT / "adapters"


SKILLS = {
    "context7-docs": {
        "title": "Context7 Docs",
        "copilot_cli_intro": "Use this repository workflow when GitHub Copilot CLI needs up-to-date, version-specific library or framework documentation.",
        "copilot_rules": [
            "Prefer Context7-backed documentation over model memory for evolving APIs.",
            "If the user provides a Context7 library ID like `/org/project` or `/org/project/version`, use it directly.",
            "Otherwise resolve the correct library before querying docs.",
            "Prefer official or high-reputation matches.",
            "If version-specific behavior matters, choose a versioned library ID.",
            "Ask narrow, task-shaped questions such as `Next.js 15 middleware matcher examples` instead of broad prompts like `next.js docs`.",
            "In the answer, state the selected library ID and separate retrieved facts from inference.",
        ],
        "copilot_avoid": [
            "Broad requests with only a library name",
            "Claiming docs support for something that was not retrieved",
            "Skipping library resolution when the target is ambiguous",
        ],
        "vscode_intro": "Use Context7 when the answer depends on current, version-specific library or framework documentation.",
        "vscode_rules": [
            "Resolve the library ID unless the prompt already includes `/org/project` or `/org/project/version`.",
            "Prefer official or high-reputation matches.",
            "Query narrowly for the requested feature, API, migration, or example.",
            "If version-specific behavior matters, use a versioned library ID.",
            "In the response, name the selected library ID and separate retrieved facts from inference.",
        ],
        "instruction_rules": [
            "Use the Context7 workflow for requests about current library or framework documentation.",
            "Resolve the correct library ID first unless the user already provided one.",
            "Prefer exact and high-reputation matches.",
            "Ask narrow questions such as `useEffect cleanup example` or `Next.js 15 middleware matcher examples`.",
            "Prefer versioned IDs when the request is version-sensitive.",
            "State the chosen library ID in the final answer.",
        ],
        "prompt_title": "Context7 Docs Prompt",
        "prompt_intro": "Use Context7 to answer with current, version-specific library documentation and examples.",
        "prompt_checklist": [
            "Resolve the library ID unless the prompt already includes one.",
            "Prefer official or high-reputation matches.",
            "Query for the exact feature, migration, API, or integration pattern.",
            "Use a versioned ID when the request is version-sensitive.",
            "State the chosen library ID and any assumptions in the answer.",
        ],
    },
    "gh-address-comments": {
        "title": "GH Address Comments",
        "copilot_cli_intro": "Use this workflow when handling review comments on the open GitHub PR for the current branch.",
        "copilot_rules": [
            "Verify `gh` authentication first.",
            "Resolve the PR from the current branch unless the user specifies one.",
            "Fetch review threads and comments needing attention.",
            "Number them and summarize the required change for each.",
            "Ask the user which numbered items should be addressed.",
            "Apply fixes only for the selected comments.",
        ],
        "vscode_intro": "Use the GitHub comment-handling workflow for review comments on the current PR.",
        "vscode_rules": [
            "Verify `gh` auth first.",
            "Resolve the current PR.",
            "Fetch comments and review threads.",
            "Number them and summarize the required change.",
            "Ask which numbered items should be addressed.",
        ],
        "instruction_rules": [
            "For GitHub PR comment work:",
            "Verify `gh` auth.",
            "Enumerate actionable comments.",
            "Summarize the required fix for each item.",
            "Ask the user which items to address before changing code.",
        ],
        "prompt_title": "GH Address Comments Prompt",
        "prompt_intro": "Handle PR review comments safely.",
        "prompt_checklist": [
            "Verify `gh` authentication.",
            "Resolve the PR.",
            "Fetch and number actionable comments.",
            "Summarize each required change.",
            "Ask which items to address before implementing.",
        ],
    },
    "gh-fix-ci": {
        "title": "GH Fix CI",
        "copilot_cli_intro": "Use this workflow when GitHub Actions checks on a PR are failing.",
        "copilot_rules": [
            "Verify `gh` authentication.",
            "Resolve the target PR.",
            "Inspect failing GitHub Actions checks and fetch logs.",
            "Summarize the failure context with a short actionable snippet.",
            "Propose a fix plan.",
            "Wait for explicit approval before implementation.",
        ],
        "vscode_intro": "Use the GitHub Actions triage workflow for failing PR checks.",
        "vscode_rules": [
            "Verify `gh` auth.",
            "Resolve the PR.",
            "Inspect failing checks and logs.",
            "Summarize the failure snippet.",
            "Propose a fix plan and wait for approval before implementing.",
        ],
        "instruction_rules": [
            "For failing GitHub Actions PR checks:",
            "Verify `gh` authentication.",
            "Inspect failing checks and logs.",
            "Summarize the actionable failure.",
            "Draft a plan.",
            "Wait for explicit user approval before implementation.",
        ],
        "prompt_title": "GH Fix CI Prompt",
        "prompt_intro": "Debug failing GitHub Actions PR checks carefully.",
        "prompt_checklist": [
            "Verify `gh` authentication.",
            "Resolve the PR.",
            "Fetch failing checks and logs.",
            "Summarize the actionable failure.",
            "Propose a fix plan.",
            "Implement only after approval.",
        ],
    },
    "local-system-admin-context": {
        "title": "Local System Admin Context",
        "copilot_cli_intro": "Use this workflow for changes to the current machine's stable software or configuration baseline.",
        "copilot_rules": [
            "Read the machine baseline first.",
            "Verify actual system state with commands.",
            "Apply the requested local change.",
            "Update the stable baseline record if the machine baseline changed.",
            "This workflow is machine-specific and should be reviewed before reuse on another host.",
        ],
        "vscode_intro": "Use the local system admin workflow only for the current machine.",
        "vscode_rules": [
            "Read the baseline first.",
            "Verify machine state with commands.",
            "Update the baseline record after stable changes.",
            "Treat the baseline as host-specific, not universally portable.",
        ],
        "instruction_rules": [
            "For local system configuration work:",
            "Read the current machine baseline before acting.",
            "Verify system state with commands.",
            "Record stable baseline changes.",
            "Avoid reusing host-specific baseline data blindly on other machines.",
        ],
        "prompt_title": "Local System Admin Context Prompt",
        "prompt_intro": "Handle local machine configuration carefully.",
        "prompt_checklist": [
            "Read the baseline.",
            "Verify actual machine state.",
            "Make the requested local change.",
            "Update the baseline if the stable configuration changed.",
            "Treat the baseline as host-specific.",
        ],
    },
}


def bullet_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered_list(items: list[str]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, start=1))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def generate(skill: str) -> None:
    meta = SKILLS[skill]
    shared = SHARED_ROOT / skill / "core.md"
    if not shared.exists():
      raise FileNotFoundError(f"Missing shared source: {shared}")

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

    scoped_instructions = textwrap.dedent(
        f"""\
        ---
        applyTo: "**"
        ---

        {meta['instruction_rules'][0]}

        {bullet_list(meta['instruction_rules'][1:])}
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
    parser = argparse.ArgumentParser(description="Generate Copilot adapter files from shared skill sources.")
    parser.add_argument("skills", nargs="*", help="Specific skill names to generate")
    parser.add_argument("--all", action="store_true", help="Generate adapters for all configured skills")
    args = parser.parse_args()

    skills = []
    if args.all:
        skills = sorted(SKILLS.keys())
    else:
        skills = args.skills

    if not skills:
        parser.error("provide skill names or use --all")

    for skill in skills:
        if skill not in SKILLS:
            raise SystemExit(f"Unsupported skill for generator: {skill}")
        generate(skill)
        print(f"Generated adapters for {skill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
