#!/usr/bin/env python3
"""Score paired with/without runs and produce a delta report.

Reads two .jsonl outputs from run_eval.py and applies the rubric in
rubric.md via an LLM judge. Writes a results table.

The judge model MUST differ from the model being evaluated.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
RUBRIC = EVAL_DIR / "rubric.md"
ANCHORS = EVAL_DIR / "rubric_anchors.md"

JUDGE_PROMPT = """\
You are scoring an agent response against one check from a rubric.

Check name: {check}

Rubric for this check:
{rubric_section}

Anchored examples (pass / partial / fail):
{anchors_section}

The task the agent was responding to:
{prompt}

The agent's response:
{response}

Score this response on the check above. Respond with exactly one of:
PASS
PARTIAL
FAIL

Followed by one short sentence justifying the score.
"""


def load_records(path: Path) -> list[dict]:
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def extract_section(text: str, heading: str) -> str:
    marker = f"### `{heading}`"
    start = text.find(marker)
    if start == -1:
        return ""
    rest = text[start + len(marker):]
    next_heading = rest.find("\n### ")
    if next_heading == -1:
        return rest.strip()
    return rest[:next_heading].strip()


def judge_call(prompt: str, judge_model: str) -> str:
    try:
        from anthropic import Anthropic
    except ImportError as e:
        raise SystemExit("pip install anthropic") from e
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    resp = client.messages.create(
        model=judge_model,
        max_tokens=256,
        temperature=0,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in resp.content if b.type == "text")


def parse_score(judge_response: str) -> str:
    head = judge_response.strip().splitlines()[0].upper()
    for level in ("PASS", "PARTIAL", "FAIL"):
        if head.startswith(level):
            return level
    return "FAIL"


def score_record(record: dict, rubric_text: str, anchors_text: str, judge_model: str) -> dict:
    results = {}
    for check in record["checks"]:
        rubric_section = extract_section(rubric_text, check)
        anchors_section = extract_section(anchors_text, check)
        if not rubric_section:
            results[check] = "FAIL"
            continue
        prompt = JUDGE_PROMPT.format(
            check=check,
            rubric_section=rubric_section,
            anchors_section=anchors_section,
            prompt=record["prompt"],
            response=record["response"],
        )
        raw = judge_call(prompt, judge_model)
        results[check] = parse_score(raw)
    return results


def task_passed(check_scores: dict[str, str]) -> bool:
    return all(v == "PASS" for v in check_scores.values())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--with", dest="with_path", required=True)
    parser.add_argument("--without", dest="without_path", required=True)
    parser.add_argument("--judge-model", default="claude-sonnet-4-6")
    args = parser.parse_args()

    rubric_text = RUBRIC.read_text(encoding="utf-8")
    anchors_text = ANCHORS.read_text(encoding="utf-8")

    with_records = {r["task_id"]: r for r in load_records(Path(args.with_path))}
    without_records = {r["task_id"]: r for r in load_records(Path(args.without_path))}

    print(f"{'task_id':<12} {'with_skill':<12} {'without_skill':<14}")
    with_passes = 0
    without_passes = 0
    for tid in sorted(with_records):
        w = score_record(with_records[tid], rubric_text, anchors_text, args.judge_model)
        wo = score_record(without_records[tid], rubric_text, anchors_text, args.judge_model)
        w_pass = task_passed(w)
        wo_pass = task_passed(wo)
        with_passes += int(w_pass)
        without_passes += int(wo_pass)
        print(f"{tid:<12} {'PASS' if w_pass else 'FAIL':<12} {'PASS' if wo_pass else 'FAIL':<14}")

    n = len(with_records)
    print()
    print(f"with skill:    {with_passes}/{n} ({with_passes / n:.0%})")
    print(f"without skill: {without_passes}/{n} ({without_passes / n:.0%})")
    print(f"delta:         {(with_passes - without_passes) / n:+.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
