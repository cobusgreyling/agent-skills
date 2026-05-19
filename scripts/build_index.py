#!/usr/bin/env python3
"""Rewrite the 'Available Skills' section of README.md from skills/*/SKILL.md.

The section is delimited by these HTML comment markers in README.md:

    <!-- BEGIN: auto-generated skill index -->
    ...generated content...
    <!-- END: auto-generated skill index -->

Anything between the markers is replaced. Anything outside is preserved.
Run before committing; CI fails if the section is stale.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
README = ROOT / "README.md"

BEGIN = "<!-- BEGIN: auto-generated skill index -->"
END = "<!-- END: auto-generated skill index -->"


def load_frontmatter(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[4:end]) or {}
    except yaml.YAMLError:
        return {}


def load_description(skill_md: Path) -> str:
    front = load_frontmatter(skill_md)
    return " ".join(str(front.get("description", "")).split())


def load_tags(skill_md: Path) -> list[str]:
    front = load_frontmatter(skill_md)
    tags = front.get("tags") or []
    return [t for t in tags if isinstance(t, str)]


def build_section() -> str:
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        return "_No skills yet._"
    lines = []
    for d in skill_dirs:
        desc = load_description(d / "SKILL.md") or "_(missing description)_"
        tags = load_tags(d / "SKILL.md")
        tag_suffix = ""
        if tags:
            tag_suffix = "  \n  _tags:_ " + ", ".join(f"`{t}`" for t in tags)
        lines.append(f"- [**{d.name}**](./skills/{d.name}) — {desc}{tag_suffix}")
    return "\n".join(lines)


BEGIN_MATRIX = "<!-- BEGIN: auto-generated tag matrix -->"
END_MATRIX = "<!-- END: auto-generated tag matrix -->"


def build_tag_matrix() -> str:
    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    tag_to_skills: dict[str, list[str]] = {}
    for d in skill_dirs:
        for tag in load_tags(d / "SKILL.md"):
            tag_to_skills.setdefault(tag, []).append(d.name)
    if not tag_to_skills:
        return "_No tagged skills yet._"
    lines = ["| Tag | Skills |", "| --- | --- |"]
    for tag in sorted(tag_to_skills):
        skills = ", ".join(
            f"[{s}](./skills/{s})" for s in sorted(tag_to_skills[tag])
        )
        lines.append(f"| `{tag}` | {skills} |")
    return "\n".join(lines)


def main() -> int:
    if not README.exists():
        print(f"FAIL: {README} not found", file=sys.stderr)
        return 1

    text = README.read_text(encoding="utf-8")
    if BEGIN not in text or END not in text:
        print(
            f"FAIL: README.md is missing the auto-index markers:\n  {BEGIN}\n  {END}",
            file=sys.stderr,
        )
        return 1

    section = build_section()
    new_text = re.sub(
        rf"{re.escape(BEGIN)}.*?{re.escape(END)}",
        f"{BEGIN}\n{section}\n{END}",
        text,
        count=1,
        flags=re.DOTALL,
    )

    if BEGIN_MATRIX in new_text and END_MATRIX in new_text:
        matrix = build_tag_matrix()
        new_text = re.sub(
            rf"{re.escape(BEGIN_MATRIX)}.*?{re.escape(END_MATRIX)}",
            f"{BEGIN_MATRIX}\n{matrix}\n{END_MATRIX}",
            new_text,
            count=1,
            flags=re.DOTALL,
        )

    if new_text == text:
        print("OK: README.md skill index already current")
        return 0

    README.write_text(new_text, encoding="utf-8")
    print("UPDATED: README.md skill index regenerated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
