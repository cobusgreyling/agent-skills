# Eval — agent-cost-modeling

A reproducible 20-task suite that measures whether a coding agent reasons in **cost per task** (six-term equation, all levers) when the `agent-cost-modeling` skill is loaded vs not loaded.

> Status: **harness published, baseline run pending.** Run it against your own agent (Claude Code, Gemini CLI, Cursor, Codex). Fill in `results.md` with your numbers. PRs welcome.

## What this measures

The skill makes seven concrete claims about how a well-designed agent should respond when a user asks about cost. Each claim is operationalised as a `check` — a one-line predicate the agent's response either passes or fails.

The seven checks:

| Check | Skill source |
|---|---|
| `flags-missing-cost-ceiling` | "What is the cost ceiling per task? Without it, you cannot pick a pattern or a model." |
| `flags-call-graph-missing` | "Sketch the call graph before pricing." |
| `flags-cache-savings-ignored` | "Caching is the first lever, not the last." |
| `flags-wrong-tier` | "The smallest model that passes the eval wins." |
| `flags-unbounded-loop-cost` | "Cap loops at the controller, not the prompt." |
| `flags-non-model-costs` | "Counting only model cost. Retrieval, embedding, tool, observability all show up on the bill." |
| `flags-cost-per-failed-task` | "Cost is per successful task. Include retries, failed runs, and abandoned sessions in the denominator." |

A task may exercise more than one check. Scoring is per check, summed per task.

## How to run

```bash
python eval/agent-cost-modeling/run_eval.py \
  --agent anthropic \
  --skill-loaded true \
  --output results-anthropic-with.jsonl

python eval/agent-cost-modeling/run_eval.py \
  --agent anthropic \
  --skill-loaded false \
  --output results-anthropic-without.jsonl

python eval/agent-cost-modeling/score.py \
  --with results-anthropic-with.jsonl \
  --without results-anthropic-without.jsonl
```

The harness is provider-agnostic. `run_eval.py` exposes a `--agent` flag that you can extend to call your agent of choice.

## What the skill is claiming

Loading the skill should produce **substantively different** responses to the 20 task prompts. Specifically:

- Without the skill, the agent typically *quotes list prices*, *suggests a model swap*, or *gives generic cost advice* — without demanding the call graph, cost ceiling, or cache hit rate.
- With the skill, the agent *refuses to price without the equation's six terms*, asks for the missing levers, and reaches for caching, model routing, and loop caps before list-price tuning.

The eval quantifies that delta. A skill that doesn't change behaviour is not a skill.

## Reproducibility caveats

- Sampling temperature affects scores. Run with `temperature=0` for the suite. Higher temperatures should be averaged across N≥3 runs.
- Scoring is rubric-based; one check per response, judged by a separate LLM-as-judge call with the rubric in `rubric.md`. Anchor examples are in `rubric_anchors.md`.
- The same model should *not* judge its own output. Use a different model (or a deterministic regex pass first) for scoring.
- Per-1M-token prices shift; the rubric does not require the agent to quote prices, only the levers.

## Files

```
eval/agent-cost-modeling/
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
- [[agent-cost-modeling]] — the skill under test.
- [[prompt-caching]] — caching is the first lever this skill demands.
- [[model-routing]] — wrong-tier is one of the failure modes.
