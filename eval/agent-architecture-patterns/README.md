# Eval — agent-architecture-patterns

A reproducible 20-task suite that measures whether a coding agent picks the **right architectural pattern** — and refuses the wrong ones — when the `agent-architecture-patterns` skill is loaded vs not loaded.

> Status: **harness published, baseline run pending.** Run it against your own agent (Claude Code, Gemini CLI, Cursor, Codex). Fill in `results.md` with your numbers. PRs welcome.

## What this measures

The skill makes seven concrete claims about how a well-designed agent should respond when a user proposes or debugs an agent architecture. Each claim is operationalised as a `check` — a one-line predicate the agent's response either passes or fails.

The seven checks:

| Check | Skill source |
|---|---|
| `flags-no-agent-needed` | "Is the task a single turn with deterministic tools? → no agent. Use a typed tool call." |
| `recommends-pattern-by-decision-shape` | "Pick the pattern that matches the task's decision shape." |
| `flags-multi-agent-for-parallelism` | "If sub-agents don't need *different* tools, prompts, or memories, you want concurrent tool calls, not agents." |
| `flags-unbounded-loop` | "Every ReAct agent needs a max-step cap *and* a budget check inside the loop." |
| `flags-freeform-agent-chat` | "Round-robin debates blow tokens and rarely converge. Force structured handoffs with explicit termination." |
| `flags-shared-mutable-memory` | "Shared mutable memory across agents. Causes context poisoning. Pass explicit messages instead." |
| `demands-eval-before-architecture` | "No eval harness, no architecture decision. Block the conversation on it." |

A task may exercise more than one check. Scoring is per check, summed per task.

## How to run

```bash
# Pre-req: Python 3.10+; an agent of your choice configured.
python eval/agent-architecture-patterns/run_eval.py \
  --agent anthropic \
  --skill-loaded true \
  --output results-anthropic-with.jsonl

python eval/agent-architecture-patterns/run_eval.py \
  --agent anthropic \
  --skill-loaded false \
  --output results-anthropic-without.jsonl

python eval/agent-architecture-patterns/score.py \
  --with results-anthropic-with.jsonl \
  --without results-anthropic-without.jsonl
```

The harness is provider-agnostic. `run_eval.py` exposes a `--agent` flag that you can extend to call your agent of choice. The reference implementation in this repo issues prompts via Anthropic's SDK; swap the call site for any other.

## What the skill is claiming

Loading the skill should produce **substantively different** responses to the 20 task prompts. Specifically:

- Without the skill, the agent typically *agrees with the proposed architecture* and offers framework recommendations.
- With the skill, the agent *refuses the architecture, names the failure mode, and proposes a simpler pattern with explicit limits*.

The eval quantifies that delta. A skill that doesn't change behaviour is not a skill.

## Reproducibility caveats

- Sampling temperature affects scores. Run with `temperature=0` for the suite. Higher temperatures should be averaged across N≥3 runs.
- Scoring is rubric-based; one check per response, judged by a separate LLM-as-judge call with the rubric in `rubric.md`. Anchor examples are in `rubric_anchors.md`.
- The same model should *not* judge its own output. Use a different model (or a deterministic regex pass first) for scoring.

## Files

```
eval/agent-architecture-patterns/
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
- [[agent-architecture-patterns]] — the skill under test.
- [[multi-agent-orchestration]] — sub-skill exercised by several checks here.
