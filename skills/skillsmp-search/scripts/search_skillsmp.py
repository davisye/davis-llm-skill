#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request


API_BASE = "https://skillsmp.com/api/v1/skills"


def read_token() -> str:
    env_token = os.environ.get("SKILLSMP_API_TOKEN")
    if env_token:
        return env_token.strip()

    try:
        result = subprocess.run(
            ["secret-tool", "lookup", "service", "skillsmp", "key", "api-token"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise SystemExit("secret-tool is not available and SKILLSMP_API_TOKEN is unset") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        if stderr:
            raise SystemExit(f"failed to read token from keyring: {stderr}") from exc
        raise SystemExit("SKILLSMP_API_TOKEN is unset and no keyring token was found") from exc

    token = result.stdout.strip()
    if not token:
        raise SystemExit("SKILLSMP_API_TOKEN is unset and keyring lookup returned an empty token")
    return token


def endpoint_for_mode(mode: str) -> str:
    if mode == "keyword":
        return f"{API_BASE}/search"
    if mode == "ai":
        return f"{API_BASE}/ai-search"
    raise ValueError(f"unsupported mode: {mode}")


def fetch(query: str, mode: str, limit: int, page: int, sort_by: str | None) -> tuple[dict, dict]:
    params = {"q": query}
    if mode == "keyword":
        params["limit"] = str(limit)
        params["page"] = str(page)
        if sort_by:
            params["sortBy"] = sort_by

    url = endpoint_for_mode(mode) + "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {read_token()}",
            "Accept": "application/json",
            "User-Agent": "davis-llm-skill/skillsmp-search",
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
            headers = dict(response.headers.items())
            return payload, headers
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(body)
        except json.JSONDecodeError:
            detail = body
        raise SystemExit(f"SkillsMP API error {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"request failed: {exc.reason}") from exc


def extract_items(payload: dict) -> list[dict]:
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, dict):
            skills = data.get("skills")
            if isinstance(skills, list):
                return skills
            nested = data.get("data")
            if isinstance(nested, list):
                items: list[dict] = []
                for entry in nested:
                    if isinstance(entry, dict) and isinstance(entry.get("skill"), dict):
                        items.append(entry["skill"])
                    elif isinstance(entry, dict):
                        items.append(entry)
                return items
        for key in ("skills", "data", "results", "items"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    if isinstance(payload, list):
        return payload
    return []


def get_field(item: dict, *names: str) -> str:
    for name in names:
        value = item.get(name)
        if value is not None and value != "":
            return str(value)
    return ""


def normalize(item: dict) -> dict:
    repo = item.get("repository")
    repo_name = ""
    repo_url = ""
    if isinstance(repo, dict):
        repo_name = get_field(repo, "fullName", "name")
        repo_url = get_field(repo, "url", "html_url")

    author = item.get("author")
    if isinstance(author, dict):
        author_name = get_field(author, "name", "login")
    else:
        author_name = get_field(item, "authorName", "author")

    return {
        "name": get_field(item, "name", "title"),
        "description": get_field(item, "description", "summary"),
        "author": author_name,
        "repository": repo_name or get_field(item, "repo", "repositoryName"),
        "repository_url": repo_url or get_field(item, "repositoryUrl", "repoUrl", "githubUrl"),
        "url": get_field(item, "url", "htmlUrl", "skillUrl"),
        "stars": get_field(item, "stars", "stargazersCount"),
        "updated": get_field(item, "updatedAt", "updated", "lastUpdated"),
    }


def print_text(items: list[dict], headers: dict) -> None:
    remaining = headers.get("X-RateLimit-Daily-Remaining")
    limit = headers.get("X-RateLimit-Daily-Limit")
    if remaining and limit:
        print(f"quota: {remaining}/{limit} remaining")
        print()

    if not items:
        print("No skills found.")
        return

    for index, item in enumerate(items, start=1):
        print(f"{index}. {item['name'] or '(unnamed)'}")
        if item["description"]:
            print(f"   description: {item['description']}")
        if item["author"]:
            print(f"   author: {item['author']}")
        if item["repository"]:
            print(f"   repository: {item['repository']}")
        if item["stars"]:
            print(f"   stars: {item['stars']}")
        if item["updated"]:
            print(f"   updated: {item['updated']}")
        if item["url"]:
            print(f"   url: {item['url']}")
        elif item["repository_url"]:
            print(f"   repository_url: {item['repository_url']}")
        print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Search SkillsMP skills.")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--mode", choices=("keyword", "ai"), default="keyword")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--sort-by", choices=("stars", "recent"), default="stars")
    parser.add_argument("--json", action="store_true", help="Print normalized JSON")
    args = parser.parse_args()

    payload, headers = fetch(args.query, args.mode, args.limit, args.page, args.sort_by)
    items = [normalize(item) for item in extract_items(payload)]

    if args.json:
        json.dump(
            {
                "mode": args.mode,
                "query": args.query,
                "quota": {
                    "daily_limit": headers.get("X-RateLimit-Daily-Limit"),
                    "daily_remaining": headers.get("X-RateLimit-Daily-Remaining"),
                },
                "items": items,
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        print()
        return 0

    print_text(items, headers)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
