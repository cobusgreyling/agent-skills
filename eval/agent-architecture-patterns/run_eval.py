#!/usr/bin/env python3
"""Run the agent-architecture-patterns eval against an agent.

Reads tasks.jsonl, dispatches each prompt to the configured agent, writes
agent responses to <output>.jsonl with one record per task.

This is a minimal reference harness. Extend `call_agent` to wire up the
agent of your choice. Provided here for Anthropic SDK; swap in OpenAI,
Gemini, Bedrock, etc. as needed.

Run with `--skill-loaded true` after installing the skill in your agent's
loading mechanism; run again with `--skill-loaded false` after removing it.
The output filename should encode that distinction.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

EVAL_DIR = Path(__file__).resolve().parent
TASKS = EVAL_DIR / "tasks.jsonl"
SKILL_NAME = "agent-architecture-patterns"


def call_agent(prompt: str, agent: str, skill_loaded: bool) -> str:
    """Dispatch one prompt to the chosen agent. Returns the response string."""
    if agent == "anthropic":
        try:
            from anthropic import Anthropic
        except ImportError as e:
            raise SystemExit("Install the anthropic SDK: `pip install anthropic`") from e
        client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        system = ""
        if skill_loaded:
            system = (EVAL_DIR.parent.parent / "skills" / SKILL_NAME / "SKILL.md").read_text(encoding="utf-8")
        resp = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=2048,
            temperature=0,
            system=system,
            messages=[{"role": "user", "content": prompt}],
        )
        return "".join(block.text for block in resp.content if block.type == "text")

    raise SystemExit(
        f"Agent '{agent}' not wired in this reference harness. "
        f"Extend run_eval.py with the integration of your choice."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", default="anthropic")
    parser.add_argument("--skill-loaded", choices=["true", "false"], required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    skill_loaded = args.skill_loaded == "true"
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with TASKS.open("r", encoding="utf-8") as f, out_path.open("w", encoding="utf-8") as out:
        for line in f:
            line = line.strip()
            if not line:
                continue
            task = json.loads(line)
            print(f"running {task['id']}...", file=sys.stderr)
            response = call_agent(task["prompt"], args.agent, skill_loaded)
            json.dump({
                "task_id": task["id"],
                "prompt": task["prompt"],
                "checks": task["checks"],
                "response": response,
            }, out, ensure_ascii=False)
            out.write("\n")

    print(f"wrote {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
