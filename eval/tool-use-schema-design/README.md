# Eval — tool-use-schema-design

A reproducible 20-task suite that measures whether a coding agent flags **schema-design anti-patterns** when the `tool-use-schema-design` skill is loaded vs not loaded.

> Status: **harness published, baseline run pending.** Run it against your own agent (Claude Code, Gemini CLI, Cursor, Codex). Fill in `results.md` with your numbers. PRs welcome.

## What this measures

The skill makes seven concrete claims about how a well-designed agent should respond when a user proposes a tool schema. Each claim is operationalised as a `check` — a one-line predicate the agent's response either passes or fails.

The seven checks:

| Check | Skill source |
|---|---|
| `flags-kitchen-sink` | "If the description needs the word 'or', split the tool." |
| `flags-free-text-payload` | "Free-text payload parameters: the model has to serialise into a string. It will fail." |
| `flags-missing-idempotency` | "Errors are first-class. Idempotency keys on destructive tools." |
| `flags-untyped-enum` | "Types are load-bearing. Use enums for closed sets." |
| `flags-overlapping-tools` | "Two tools that overlap by 80% — the model alternates and confuses itself." |
| `flags-silent-failure` | "Silent failure: the model thinks success and proceeds." |
| `flags-magic-sentinel` | "No magic sentinel values. `-1` for 'all' is a bug factory." |

A task may exercise more than one check. Scoring is per check, summed per task.

## How to run

```bash
# Pre-req: Python 3.10+; an agent of your choice configured.
python eval/tool-use-schema-design/run_eval.py \
  --agent claude-code \
  --skill-loaded true \
  --output results-claude-code-with.jsonl

python eval/tool-use-schema-design/run_eval.py \
  --agent claude-code \
  --skill-loaded false \
  --output results-claude-code-without.jsonl

python eval/tool-use-schema-design/score.py \
  --with results-claude-code-with.jsonl \
  --without results-claude-code-without.jsonl
```

The harness is provider-agnostic. `run_eval.py` exposes a `--agent` flag that you can extend to call your agent of choice. The reference implementation in this repo issues prompts via Anthropic's SDK; swap the call site for any other.

## What the skill is claiming

Loading the skill should produce **substantively different** responses to the 20 task prompts. Specifically:

- Without the skill, the agent typically *implements what was asked*.
- With the skill, the agent *refuses the design, names the anti-pattern, and proposes a refactor*.

The eval quantifies that delta. A skill that doesn't change behaviour is not a skill.

## Reproducibility caveats

- Sampling temperature affects scores. Run with `temperature=0` for the suite. Higher temperatures should be averaged across N≥3 runs.
- Scoring is rubric-based; one check per response, judged by a separate LLM-as-judge call with the rubric in `rubric.md`. Anchor examples are in `rubric_anchors.md`.
- The same model should *not* judge its own output. Use a different model (or a deterministic regex pass first) for scoring.

## Files

```
eval/tool-use-schema-design/
  README.md              # this file
  tasks.jsonl            # 20 prompts + per-task checks
  rubric.md              # how to judge a response on each check
  rubric_anchors.md      # 2-3 anchored examples per check (pass + fail)
  run_eval.py            # minimal harness (one provider; extend as needed)
  score.py               # apply rubric, produce delta report
  results.md             # results template — fill in after running
```

## Related skills

- [[agent-evaluation-harness]] — the meta-skill that designed this format.
- [[tool-use-schema-design]] — the skill under test.
