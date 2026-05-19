# Eval — prompt-caching

A reproducible 20-task suite that measures whether a coding agent flags **prompt-caching anti-patterns** and recommends the **provider-correct mechanism** when the `prompt-caching` skill is loaded vs not loaded.

> Status: **harness published, baseline run pending.** Run it against your own agent (Claude Code, Gemini CLI, Cursor, Codex). Fill in `results.md` with your numbers. PRs welcome.

## What this measures

The skill makes seven concrete claims about how a well-designed agent should respond when a user asks about prompt caching. Each claim is operationalised as a `check` — a one-line predicate the agent's response either passes or fails.

The seven checks:

| Check | Skill source |
|---|---|
| `flags-dynamic-prefix` | "Dynamic timestamp or request-id in the system prompt. Single character above the boundary = 0% hit rate." |
| `flags-no-measurement` | "If you can't tell me your cache hit rate, you don't have caching — you have wishful thinking." |
| `flags-cache-write-cost` | "Cache writes cost more than reads; cache the *stable* part only." |
| `flags-unstable-ordering` | "Reordering tools per call. Tool list order matters for the hash; keep it deterministic." |
| `flags-cross-user-cache` | "Caching across users where prompts include other users' data. Privacy bug *and* low hit rate." |
| `recommends-explicit-breakpoints` | "Anthropic uses `cache_control: ephemeral` breakpoints; OpenAI auto-caches with hashing. Know which knobs your provider gives you." |
| `flags-ttl-cold-start` | "Anthropic ephemeral cache is 5 minutes; OpenAI's is longer but not infinite." |

A task may exercise more than one check. Scoring is per check, summed per task.

## How to run

```bash
# Pre-req: Python 3.10+; an agent of your choice configured.
python eval/prompt-caching/run_eval.py \
  --agent anthropic \
  --skill-loaded true \
  --output results-anthropic-with.jsonl

python eval/prompt-caching/run_eval.py \
  --agent anthropic \
  --skill-loaded false \
  --output results-anthropic-without.jsonl

python eval/prompt-caching/score.py \
  --with results-anthropic-with.jsonl \
  --without results-anthropic-without.jsonl
```

The harness is provider-agnostic. `run_eval.py` exposes a `--agent` flag that you can extend to call your agent of choice. The reference implementation in this repo issues prompts via Anthropic's SDK; swap the call site for any other.

## What the skill is claiming

Loading the skill should produce **substantively different** responses to the 20 task prompts. Specifically:

- Without the skill, the agent typically *gives generic caching advice* or *recommends the wrong mechanism for the provider*.
- With the skill, the agent *names the anti-pattern, points to the provider-correct mechanism, and asks for the cache-hit-rate metric before tuning*.

The eval quantifies that delta. A skill that doesn't change behaviour is not a skill.

## Reproducibility caveats

- Sampling temperature affects scores. Run with `temperature=0` for the suite. Higher temperatures should be averaged across N≥3 runs.
- Scoring is rubric-based; one check per response, judged by a separate LLM-as-judge call with the rubric in `rubric.md`. Anchor examples are in `rubric_anchors.md`.
- The same model should *not* judge its own output. Use a different model (or a deterministic regex pass first) for scoring.
- Caching-specific numbers (TTLs, percentage premiums, minimum block sizes) occasionally shift as providers tune their products. The rubric tolerates ±10% on numeric claims; refresh anchors when providers publish breaking changes.

## Files

```
eval/prompt-caching/
  README.md              # this file
  tasks.jsonl            # 20 prompts + per-task checks
  rubric.md              # how to judge a response on each check
  rubric_anchors.md      # one anchored example per check (pass / partial / fail)
  run_eval.py            # minimal harness (one provider; extend as needed)
  score.py               # apply rubric, produce delta report
  results.md             # results template — fill in after running
```

## Related skills

- [[agent-evaluation-harness]] — the meta-skill that designed this format.
- [[prompt-caching]] — the skill under test.
- [[agent-cost-modeling]] — caching is the first cost lever; this eval bounds how much it actually moves the needle.
