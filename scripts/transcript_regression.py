#!/usr/bin/env python3
"""Replay each skill's TRANSCRIPT.md prompt against the current model.

Each skills/<name>/TRANSCRIPT.md ships with one prompt and two annotated
responses (without skill, with skill). Over time, models change; the
"without skill" baseline drifts toward the "with skill" expectation and the
'proof, not just briefs' claim weakens.

This script extracts the prompt from each TRANSCRIPT.md and re-runs it
against the configured model in two conditions:

  1. Without the SKILL.md loaded as system prompt.
  2. With the SKILL.md loaded as system prompt.

It writes a report flagging skills where the without-skill response now
looks substantively like the with-skill expectation — a drift signal worth
investigating (skill obsolete, baseline shifted, or the skill needs updating).

This is a diagnostic, not a scorer. Read the report; decide per-skill.

Usage:

    python scripts/transcript_regression.py --model claude-opus-4-7
    python scripts/transcript_regression.py --skill memory-design --model claude-opus-4-7

Environment:

    ANTHROPIC_API_KEY    required for the default provider.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
REPORT_DIR = ROOT / "out" / "transcript-regression"

PROMPT_HEADER = "## Prompt"
BLOCKQUOTE_RE = re.compile(r"^>\s?(.*)$")


def extract_prompt(transcript_md: Path) -> str:
    """Extract the user prompt from a TRANSCRIPT.md.

    The prompt section is delimited by '## Prompt' and the next '##' heading.
    Lines inside the section are typically blockquoted with '> '.
    """
    text = transcript_md.read_text(encoding="utf-8")
    start = text.find(PROMPT_HEADER)
    if start == -1:
        return ""
    rest = text[start + len(PROMPT_HEADER):]
    next_heading = rest.find("\n## ")
    body = rest[:next_heading] if next_heading != -1 else rest

    lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "---":
            continue
        match = BLOCKQUOTE_RE.match(stripped)
        if match:
            lines.append(match.group(1))
        else:
            lines.append(stripped)
    return "\n".join(lines).strip()


def call_model(prompt: str, system: str, model: str) -> str:
    try:
        from anthropic import Anthropic
    except ImportError as e:
        raise SystemExit("pip install anthropic") from e
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    resp = client.messages.create(
        model=model,
        max_tokens=2048,
        temperature=0,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def drift_signal(without: str, with_skill: str) -> str:
    """Cheap heuristic for whether the without-skill response looks like the with-skill one.

    Real signal needs a judge model; this is a fast pre-filter.

    The skill's behavioural fingerprint is usually: refusing the user's design,
    naming an anti-pattern explicitly, invoking the hard line. Look for those
    phrases in the without-skill response.
    """
    refuse_markers = ["stop.", "refuse", "anti-pattern", "do not", "wrong",
                      "instead", "hard line", "this is the wrong"]
    score = sum(1 for m in refuse_markers if m in without.lower())
    if score >= 4:
        return "POSSIBLE_DRIFT (baseline now refuses without skill — re-check the transcript)"
    if score >= 2:
        return "MINOR_DRIFT (baseline shows some skill-aligned framing)"
    return "OK (baseline still gives generic answer)"


def process_skill(skill_dir: Path, model: str) -> dict:
    transcript_md = skill_dir / "TRANSCRIPT.md"
    skill_md = skill_dir / "SKILL.md"
    if not transcript_md.exists() or not skill_md.exists():
        return {"skill": skill_dir.name, "status": "missing_files"}

    prompt = extract_prompt(transcript_md)
    if not prompt:
        return {"skill": skill_dir.name, "status": "no_prompt_extracted"}

    print(f"  prompt extracted ({len(prompt)} chars)", file=sys.stderr)
    without = call_model(prompt, system="", model=model)
    print(f"  without-skill response: {len(without)} chars", file=sys.stderr)
    with_skill = call_model(prompt, system=skill_md.read_text(encoding="utf-8"), model=model)
    print(f"  with-skill response: {len(with_skill)} chars", file=sys.stderr)

    return {
        "skill": skill_dir.name,
        "status": "ok",
        "model": model,
        "prompt": prompt,
        "without_skill_response": without,
        "with_skill_response": with_skill,
        "drift_signal": drift_signal(without, with_skill),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="claude-opus-4-7")
    parser.add_argument(
        "--skill",
        help="Run a single skill by name. If omitted, runs all.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write JSON report. Default: out/transcript-regression/<model>.json",
    )
    args = parser.parse_args()

    if not SKILLS_DIR.is_dir():
        print(f"FAIL: {SKILLS_DIR} does not exist", file=sys.stderr)
        return 1

    if args.skill:
        skill_dirs = [SKILLS_DIR / args.skill]
        if not skill_dirs[0].is_dir():
            print(f"FAIL: skill `{args.skill}` not found", file=sys.stderr)
            return 1
    else:
        skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = Path(args.output) if args.output else REPORT_DIR / f"{args.model}.json"

    results = []
    for d in skill_dirs:
        print(f"running {d.name}...", file=sys.stderr)
        results.append(process_skill(d, args.model))

    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out_path}", file=sys.stderr)

    print()
    print("Drift summary:")
    for r in results:
        if r.get("status") == "ok":
            print(f"  {r['skill']:<35} {r['drift_signal']}")
        else:
            print(f"  {r['skill']:<35} status={r['status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
