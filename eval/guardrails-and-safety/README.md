# Eval — guardrails-and-safety

A reproducible 20-task suite that measures whether a coding agent designs **layered safety** — and refuses prompt-only or single-layer defences — when the `guardrails-and-safety` skill is loaded vs not loaded.

> Status: **harness published, baseline run pending.** Run it against your own agent (Claude Code, Gemini CLI, Cursor, Codex). Fill in `results.md` with your numbers. PRs welcome.

## What this measures

The skill makes seven concrete claims about how a well-designed agent should respond when a user asks about safety. Each claim is operationalised as a `check` — a one-line predicate the agent's response either passes or fails.

The seven checks:

| Check | Skill source |
|---|---|
| `flags-prompt-only-defense` | "'Be safe' in the system prompt as the entire defence. Adversarial input ignores polite requests." |
| `flags-output-filter-only` | "Post-hoc output filter only. Blocks the obvious, misses everything subtle, stops nothing the model has already done via tools." |
| `flags-no-server-side-validation` | "Trusting LLM-generated tool arguments without server-side validation. The model is an untrusted client." |
| `flags-indirect-injection-blindness` | "Treating prompt injection as a model problem. It's a context-source problem." |
| `flags-missing-redteam` | "No red-team set, no deploy." |
| `flags-out-of-band-confirmation-missing` | "High-impact tools must require out-of-band confirmation that doesn't pass through the model." |
| `flags-self-judging` | "Same model evaluating its own output. Co-conspirator, not auditor." |

A task may exercise more than one check. Scoring is per check, summed per task.

## How to run

```bash
python eval/guardrails-and-safety/run_eval.py \
  --agent anthropic \
  --skill-loaded true \
  --output results-anthropic-with.jsonl

python eval/guardrails-and-safety/run_eval.py \
  --agent anthropic \
  --skill-loaded false \
  --output results-anthropic-without.jsonl

python eval/guardrails-and-safety/score.py \
  --with results-anthropic-with.jsonl \
  --without results-anthropic-without.jsonl
```

The harness is provider-agnostic. `run_eval.py` exposes a `--agent` flag that you can extend to call your agent of choice.

## What the skill is claiming

Loading the skill should produce **substantively different** responses to the 20 task prompts. Specifically:

- Without the skill, the agent typically *adds a system prompt instruction*, *adds an output filter*, or *picks one defence layer* and calls it done.
- With the skill, the agent *refuses single-layer defences*, *names the missing layer*, and *demands a red-team set + server-side authorisation* before deploy.

The eval quantifies that delta. A skill that doesn't change behaviour is not a skill.

## Reproducibility caveats

- Sampling temperature affects scores. Run with `temperature=0` for the suite. Higher temperatures should be averaged across N≥3 runs.
- Scoring is rubric-based; one check per response, judged by a separate LLM-as-judge call with the rubric in `rubric.md`. Anchor examples are in `rubric_anchors.md`.
- The same model should *not* judge its own output. Use a different model (or a deterministic regex pass first) for scoring.

## Files

```
eval/guardrails-and-safety/
  README.md              # this file
  tasks.jsonl            # 20 prompts + per-task checks
  rubric.md              # how to judge a response on each check
  rubric_anchors.md      # one anchored pass / partial / fail example per check
  run_eval.py            # minimal harness (one provider; extend as needed)
  score.py               # apply rubric, produce delta report
  results.md             # results template — fill in after running
```

## Related skills

- [[agent-evaluation-harness]] — the meta-skill that designed this format.
- [[guardrails-and-safety]] — the skill under test.
- [[prompt-injection-defense]] — sub-skill exercised by several checks.
- [[human-in-the-loop]] — adjacent skill: out-of-band confirmation.
