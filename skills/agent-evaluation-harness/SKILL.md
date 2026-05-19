---
name: agent-evaluation-harness
description: >-
  Design an evaluation harness for an LLM agent before shipping it. Use when
  the user is building or rewriting an agent, deciding ship/no-ship, debugging
  regressions, or mentions golden sets, eval suites, regression tests,
  trace-level evals, LLM-as-judge, scoring rubrics, or asks "how do I test this
  agent?" / "how do I know if my agent got better?".
tags:
  - evaluation
  - production
  - regression
  - quality
---

# Agent Evaluation Harness

An agent without an eval harness is a demo, not a system.

You cannot ship, refactor, or compare agents responsibly without one. Every prompt tweak that "feels better" is a coin flip until you have a number to back it.

## When to use this skill

- The user is about to merge a prompt or graph change.
- The user is choosing between two models, two patterns, or two providers.
- The user is debugging a regression and has no way to reproduce it.
- The user is asking "is this good enough to ship?"
- The user mentions LLM-as-judge, golden set, eval suite, or regression test.

## What an eval harness actually is

Three pieces. If any is missing, you don't have one.

1. **A frozen input set.** ≥20 representative tasks, labelled with the expected outcome shape (not necessarily exact text). Curated, not sampled — covers the long tail, not the average.
2. **A scoring function.** Deterministic where possible (exact match, schema validation, tool-call correctness). LLM-as-judge only for free-form outputs, and *only* with a rubric and anchors.
3. **A regression gate.** The score is compared against the last known-good run. A drop fails CI or blocks merge.

## Decision flow

1. **Does the task have a checkable answer?** → deterministic scorer (regex, JSON-schema, tool-call match). Cheapest and most reliable.
2. **Is the output a structured artefact (code, SQL, JSON)?** → run the artefact. Did it execute? Did it produce the expected effect?
3. **Is the output free-form (summary, reply, plan)?** → rubric-based LLM-as-judge with explicit criteria *and* 3–5 anchored examples per score level. Never freeform "rate 1–10".
4. **Is the task multi-step (agent loop)?** → score the trace, not just the final answer. Did it call the right tools, in the right order, within budget?

## Anti-patterns to flag immediately

- **Vibe checks.** "It looks better." This is not signal.
- **LLM-as-judge without anchors.** A judge that has never seen what a "5" looks like is a random number generator.
- **Single-example tweaking.** Iterating against one failing input always overfits. Add it to the set, run the whole set.
- **Eval set that grows with every change.** That's a training set, not a held-out one. Freeze one, grow another.
- **Scoring only the final answer for agent loops.** A right answer via the wrong trace is a future regression.
- **Re-rolling the judge until it agrees.** If you sample N times and pick the best, you're not evaluating, you're cherry-picking.

## What to log per eval run

- Inputs (verbatim) and ground-truth labels.
- Full trace: every model call, every tool call, every retry.
- Scores per criterion, not just the aggregate.
- Wall-clock latency and total token cost — quality is not the only axis.
- Model version, prompt version, graph version. Pin everything.

## Questions to ask the user

1. What does **success** look like for one task — concretely, in one sentence?
2. What does the **failure** distribution look like — wrong answer, no answer, unsafe answer, slow answer?
3. How many representative inputs can the user **provide today** (not aspirationally)?
4. Who decides what "correct" means when humans disagree?
5. Where will the eval **run** — locally, in CI, on a schedule?
6. What's the **budget** per eval run? Token cost decides cadence.

If the answer to any of these is "I don't know," that's the first task — not the harness.

## The hard line

**No golden set, no merge.** No exceptions for "small" prompt changes — small changes are exactly where regressions hide.

## Why this exists

Most agent failures in production trace back to a prompt change that nobody could quantify at the time. Teams ship on intuition, regress silently, and discover it when a user complains. The harness flips the loop: change something, see a number, decide. See [link to article on agent evaluation].

## References

- `references/scoring.md` — deterministic vs rubric vs LLM-as-judge, with examples.
- `references/golden-sets.md` — how to curate and grow an input set without overfitting.
- `references/ci.md` — wiring the harness into CI and PR gates.
