#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


DOMAIN_ORDER = [
    "nextjs-app-router",
    "frontend-design-system",
    "golang-backend",
    "springboot-backend",
    "python-engineering",
]


DOMAIN_CONTENT = {
    "nextjs-app-router": """# Next.js App Router

Use this reference when work touches Next.js application structure, rendering boundaries, route handlers, server actions, caching, or data fetching.

## Focus

- Prefer App Router patterns over legacy Pages Router assumptions.
- Preserve server/client component boundaries deliberately.
- Keep data loading close to the server when possible.
- Treat streaming, suspense boundaries, and cache invalidation as architectural decisions, not afterthoughts.
- When changing routing, middleware, or rendering behavior, verify against current docs instead of relying on memory.

## Triggers

- `app/` directory changes
- `next.config.*`
- route handlers
- server actions
- React Server Components
""",
    "frontend-design-system": """# Frontend Design System

Use this reference when work affects UI consistency, design tokens, component patterns, accessibility, visual hierarchy, or responsive behavior.

## Focus

- Reuse existing visual primitives before creating one-off styles.
- Keep spacing, typography, and state patterns consistent across components.
- Preserve accessibility semantics for interactive controls, forms, and dialogs.
- Treat loading, empty, error, hover, focus, and disabled states as first-class UI requirements.
- Prefer systematic design choices over isolated visual fixes.

## Triggers

- component library changes
- shared CSS or Tailwind tokens
- design system work
- UI consistency issues
- responsive layout changes
""",
    "golang-backend": """# Go Backend

Use this reference when work touches Go services, package boundaries, concurrency, testing, or backend architecture.

## Focus

- Prefer idiomatic package design and explicit interfaces.
- Keep error handling direct and contextual.
- Use `context.Context` consistently across request and service boundaries.
- Treat goroutines, channels, and shutdown flow as correctness concerns, not just implementation details.
- Favor table-driven tests and small package seams for testability.

## Triggers

- `*.go`
- `go.mod`
- handlers, services, repositories
- goroutines or channels
- Go test design
""",
    "springboot-backend": """# Spring Boot Backend

Use this reference when work affects Spring Boot controllers, services, repositories, configuration, transactions, or test structure.

## Focus

- Keep controller, service, and persistence responsibilities separated.
- Prefer explicit transaction boundaries and clear exception handling.
- Treat configuration, profiles, and external clients as architecture concerns.
- Keep REST contracts, validation, and serialization rules consistent.
- Use focused tests for slices, integration paths, and business services.

## Triggers

- `pom.xml`
- `build.gradle` or `build.gradle.kts`
- Spring Boot starters
- controllers, services, repositories
- JPA, configuration, Actuator, validation
""",
    "python-engineering": """# Python Engineering

Use this reference when work touches Python project structure, typing, testing, architecture, packaging, or runtime behavior.

## Focus

- Prefer clear module boundaries and explicit dependency flow.
- Use typing where it improves contracts and maintainability.
- Keep configuration and side effects isolated from domain logic.
- Favor pytest-based testing patterns with fixtures, parametrization, and small seams.
- Treat async usage, observability, and performance choices as architectural decisions.

## Triggers

- `*.py`
- `pyproject.toml`
- `requirements.txt`
- pytest or fixture work
- service layering or package design
""",
}


def has_any(root: Path, names: list[str]) -> bool:
    return any((root / name).exists() for name in names)


def parse_package_json(root: Path) -> dict:
    package_json = root / "package.json"
    if not package_json.exists():
        return {}
    try:
        return json.loads(package_json.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def detect_domains(root: Path) -> list[str]:
    domains: list[str] = []
    package = parse_package_json(root)
    deps = {}
    deps.update(package.get("dependencies") or {})
    deps.update(package.get("devDependencies") or {})

    has_frontend = package != {} or has_any(root, ["app", "src/app", "pages", "src/components"])
    has_next = "next" in deps or has_any(root, ["next.config.js", "next.config.mjs", "next.config.ts", "app", "src/app"])

    if has_next:
        domains.append("nextjs-app-router")
    if has_frontend:
        domains.append("frontend-design-system")
    if (root / "go.mod").exists():
        domains.append("golang-backend")
    if has_any(root, ["pom.xml", "build.gradle", "build.gradle.kts"]):
        content = ""
        for name in ("pom.xml", "build.gradle", "build.gradle.kts"):
            path = root / name
            if path.exists():
                try:
                    content += path.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    pass
        if "spring-boot" in content.lower() or "org.springframework.boot" in content.lower():
            domains.append("springboot-backend")
    if has_any(root, ["pyproject.toml", "requirements.txt", "setup.py", "setup.cfg"]):
        domains.append("python-engineering")

    ordered = [name for name in DOMAIN_ORDER if name in domains]
    return ordered


def render_root_skill(project_name: str, domains: list[str]) -> str:
    bullets = "\n".join(f"- `{name}` -> read `.project-skills/{name}.md` when the task matches that domain" for name in domains)
    stack_line = ", ".join(f"`{name}`" for name in domains) if domains else "`general-project`"
    return f"""---
name: {project_name}-project
description: Use when working in this repository. Start with this project-local skill to route work to the right local framework and engineering references based on the repository stack.
---

# Project Skill Router

This repository uses a project-local skill layer. Start here before relying on generic global assumptions.

## Detected domains

{stack_line}

## Routing

{bullets if bullets else "- No stack-specific references were generated."}

## Rules

- Prefer the local `.project-skills/` references over generic framework assumptions when they apply.
- If a task spans multiple domains, combine the relevant local references.
- Keep implementation aligned with the repository's existing conventions before introducing new patterns.
"""


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate project-local skill files from repository stack signals.")
    parser.add_argument("project_dir", help="Target project directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing generated files")
    parser.add_argument("--dry-run", action="store_true", help="Print detected domains without writing files")
    args = parser.parse_args()

    root = Path(args.project_dir).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"Project directory not found: {root}")

    domains = detect_domains(root)
    if args.dry_run:
        print(json.dumps({"project": str(root), "domains": domains}, ensure_ascii=False, indent=2))
        return 0

    project_name = root.name.replace(" ", "-").lower()
    try:
        write_file(root / "SKILL.md", render_root_skill(project_name, domains), args.force)
        for domain in domains:
            write_file(root / ".project-skills" / f"{domain}.md", DOMAIN_CONTENT[domain], args.force)
    except FileExistsError as exc:
        raise SystemExit(f"Refusing to overwrite existing file without --force: {exc}") from exc

    print(f"Generated project skill router for {root}")
    print("Domains:")
    for domain in domains:
        print(f"- {domain}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
