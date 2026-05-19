#!/usr/bin/env python3
"""Convert each SKILL.md into the per-agent format variants.

The repository's SKILL.md is Claude Code-native. Other agents need format
conversion, manually documented in the README. This script automates those
conversions so the per-agent files don't drift from the canonical SKILL.md.

Outputs:

    out/cursor/.cursor/rules/<skill>.mdc      # Cursor Rule format
    out/codex/AGENTS.md                       # Codex single-file aggregate
    out/gemini-cli/GEMINI.md                  # Gemini CLI @-ref aggregate

Each conversion preserves the SKILL.md body verbatim; only the frontmatter
(or surrounding structure) is reshaped.

Usage:

    python scripts/convert.py --target cursor
    python scripts/convert.py --target codex
    python scripts/convert.py --target gemini-cli
    python scripts/convert.py --target all     # default
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
OUT_DIR = ROOT / "out"


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    raw = text[4:end]
    try:
        front = yaml.safe_load(raw) or {}
    except yaml.YAMLError:
        front = {}
    body = text[end + 5 :]
    return front, body


def to_cursor(skill_dir: Path, out_root: Path) -> None:
    """Write Cursor MDC Rule file for one skill."""
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    front, body = parse_frontmatter(text)
    description = " ".join(str(front.get("description", "")).split())
    description = description.replace('"', '\\"')

    mdc_text = (
        "---\n"
        f'description: "{description}"\n'
        'globs: ["**/*"]\n'
        "alwaysApply: false\n"
        "---\n\n"
    )
    mdc_text += body.lstrip()

    out_dir = out_root / "cursor" / ".cursor" / "rules"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{skill_dir.name}.mdc"
    out_path.write_text(mdc_text, encoding="utf-8")


def demote_headings(body: str) -> str:
    """Demote each Markdown heading level by one (# → ##, ## → ###, ...).

    Used when nesting a SKILL.md body under a parent heading; preserves
    relative structure while preventing duplicate top-level titles.
    """
    out_lines = []
    for line in body.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("#"):
            n_hash = len(stripped) - len(stripped.lstrip("#"))
            if 0 < n_hash < 6 and (len(stripped) == n_hash or stripped[n_hash] == " "):
                line = "#" + line
        out_lines.append(line)
    return "\n".join(out_lines)


def to_codex(skill_dirs: list[Path], out_root: Path) -> None:
    """Write a single AGENTS.md aggregating all skill bodies."""
    parts = ["# Agent rules", "", "Generated from skills/. Do not edit by hand.", ""]
    for d in skill_dirs:
        text = (d / "SKILL.md").read_text(encoding="utf-8")
        _, body = parse_frontmatter(text)
        parts.append("")
        parts.append(demote_headings(body.strip()))
    out_dir = out_root / "codex"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "AGENTS.md").write_text("\n".join(parts) + "\n", encoding="utf-8")


def to_gemini(skill_dirs: list[Path], out_root: Path) -> None:
    """Write a GEMINI.md that @-references each skill."""
    lines = [
        "# Project context",
        "",
        "Generated from skills/. Do not edit by hand.",
        "",
    ]
    for d in skill_dirs:
        rel = d.relative_to(ROOT)
        lines.append(f"@./{rel}/SKILL.md")
    out_dir = out_root / "gemini-cli"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "GEMINI.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--target",
        choices=["cursor", "codex", "gemini-cli", "all"],
        default="all",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove the out/ directory before regenerating.",
    )
    args = parser.parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"FAIL: {SKILLS_DIR} does not exist", file=sys.stderr)
        return 1

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print(f"FAIL: no skills found under {SKILLS_DIR}", file=sys.stderr)
        return 1

    if args.clean and OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)

    targets = ["cursor", "codex", "gemini-cli"] if args.target == "all" else [args.target]

    if "cursor" in targets:
        for d in skill_dirs:
            to_cursor(d, OUT_DIR)
        print(f"WROTE: out/cursor/.cursor/rules/*.mdc ({len(skill_dirs)} files)")
    if "codex" in targets:
        to_codex(skill_dirs, OUT_DIR)
        print("WROTE: out/codex/AGENTS.md")
    if "gemini-cli" in targets:
        to_gemini(skill_dirs, OUT_DIR)
        print("WROTE: out/gemini-cli/GEMINI.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
