#!/usr/bin/env python3
"""Validate every skills/<name>/SKILL.md against the repo's contract.

Exit code 0 if all skills pass, 1 otherwise. Intended for CI.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"

KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TAG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DESCRIPTION_MAX = 1024
DESCRIPTION_MIN = 20
BODY_SOFT_MAX_BYTES = 10_000
TAGS_MAX = 8


def parse_frontmatter(text: str) -> tuple[dict, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    raw = text[4:end]
    try:
        data = yaml.safe_load(raw) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"frontmatter YAML failed to parse: {e}") from e
    if not isinstance(data, dict):
        raise ValueError("frontmatter must be a YAML mapping")
    return data, text[end + 5 :]


def lint_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    try:
        parsed = parse_frontmatter(text)
    except ValueError as e:
        return [f"{skill_dir.name}: {e}"]
    if parsed is None:
        return [f"{skill_dir.name}: SKILL.md must start with YAML frontmatter delimited by ---"]

    front, body = parsed

    name = front.get("name")
    if not name:
        errors.append(f"{skill_dir.name}: frontmatter missing required field `name`")
    elif not isinstance(name, str):
        errors.append(f"{skill_dir.name}: `name` must be a string")
    else:
        if not KEBAB_RE.match(name):
            errors.append(f"{skill_dir.name}: `name` must be kebab-case (got `{name}`)")
        if name != skill_dir.name:
            errors.append(
                f"{skill_dir.name}: `name` field (`{name}`) must match folder name"
            )

    description = front.get("description")
    if not description:
        errors.append(f"{skill_dir.name}: frontmatter missing required field `description`")
    elif not isinstance(description, str):
        errors.append(f"{skill_dir.name}: `description` must be a string")
    else:
        flat = " ".join(description.split())
        if len(flat) < DESCRIPTION_MIN:
            errors.append(
                f"{skill_dir.name}: `description` is too short ({len(flat)} chars, min {DESCRIPTION_MIN}) — "
                "agents won't fire on vague triggers"
            )
        if len(flat) > DESCRIPTION_MAX:
            errors.append(
                f"{skill_dir.name}: `description` is {len(flat)} chars, max {DESCRIPTION_MAX}"
            )

    tags = front.get("tags", [])
    if tags is not None:
        if not isinstance(tags, list):
            errors.append(f"{skill_dir.name}: `tags` must be a list of kebab-case strings")
        else:
            if len(tags) > TAGS_MAX:
                errors.append(f"{skill_dir.name}: too many tags ({len(tags)}, max {TAGS_MAX})")
            for tag in tags:
                if not isinstance(tag, str) or not TAG_RE.match(tag):
                    errors.append(f"{skill_dir.name}: tag `{tag}` must be kebab-case string")

    if len(body.encode("utf-8")) > BODY_SOFT_MAX_BYTES:
        errors.append(
            f"{skill_dir.name}: SKILL.md body exceeds {BODY_SOFT_MAX_BYTES} bytes — "
            "split long material into references/ and load on demand"
        )

    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"FAIL: {SKILLS_DIR} does not exist", file=sys.stderr)
        return 1

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print(f"FAIL: no skills found under {SKILLS_DIR}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for skill_dir in skill_dirs:
        all_errors.extend(lint_skill(skill_dir))

    if all_errors:
        print(f"FAIL: {len(all_errors)} problem(s) found:", file=sys.stderr)
        for err in all_errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"OK: {len(skill_dirs)} skill(s) validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
