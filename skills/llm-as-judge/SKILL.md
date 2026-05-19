---
name: llm-as-judge
description: >-
  Design and validate LLM-as-judge scoring — pairwise vs pointwise, bias
  correction, anchor calibration, and the cases where a judge is the wrong
  tool. Use when the user is building an eval, scoring open-ended outputs,
  or comparing model versions and mentions LLM-as-judge, model grader,
  pairwise comparison, position bias, length bias, judge calibration,
  meta-eval, or asks "how do I score open-ended responses?" / "is my
  LLM-judge biased?".
tags:
  - evaluation
  - scoring
  - quality
  - production
---

# LLM-as-Judge

A judge is a model, and models are biased. Calibrate it like any other classifier.

LLM-as-judge is the only scalable way to score open-ended outputs — and the easiest way to ship a "passing" agent that's actually worse. Position bias, length bias, self-preference, and verbosity reward are routine. Treat the judge as a system that needs its own eval before it's allowed to score anything.

## When to use this skill

- The user is scoring open-ended agent output (summaries, drafts, plans, refactors).
- The user is using one LLM to compare two LLMs.
- The user is reporting eval results without confidence intervals or judge-agreement numbers.
- The user is using the same model as both candidate and judge.

## The four bias modes

Every LLM-judge has at least the first three. Name them; correct for them.

- **Position bias.** A or B presented first wins more often, regardless of quality.
- **Length bias / verbosity reward.** Longer answers score higher even when they're worse.
- **Self-preference.** Models prefer their own outputs (and same-family outputs) at meaningful rates.
- **Format / style bias.** Markdown, headers, hedging language inflate scores independently of content.

## Decision flow

1. **Can the output be scored deterministically?** → yes → use a rule, regex, or exact match. Don't reach for a judge.
2. **Is the output a discrete classification?** → yes → use a small classifier model, not a free-form judge.
3. **Is the output open-ended?** → judge appropriate, with calibration.
4. **Are you comparing two candidates?** → **pairwise** beats pointwise for open-ended outputs. Most signal, most agreement, least calibration drift.
5. **Are you scoring against a fixed rubric?** → **pointwise** is OK, with anchored examples per score level.
6. **Are you ranking >2 candidates?** → tournament of pairwise, not a single pointwise sweep.

## Pairwise rules

- **Randomise order per call.** Position bias is otherwise baked in. Measure how often A and B win when their position is swapped — high disagreement signals the judge isn't tracking quality.
- **Both presented in the same call.** Cross-call comparisons drift on temperature and context.
- **Tie option allowed.** Without ties, the judge fabricates differences.
- **Score-then-explain or explain-then-score, consistently.** Mixing orders within a study introduces noise.

## Pointwise rules

- **Anchored examples per score level.** "5 = like this, 4 = like this..." The model anchors; descriptions alone don't.
- **Small ordinal scale (1–5 or 1–7).** Continuous scales (0.0–1.0) are noise; the model rounds anyway.
- **Score one dimension per call.** Conflated dimensions (helpful AND safe AND well-formatted) produce muddy averages.
- **No "rate this overall".** Decompose into named dimensions.

## Meta-eval — validate the judge before trusting it

The judge needs its own eval. A judge that scores 0.5 inter-rater agreement with humans is producing roughly random numbers.

- **Human-judge agreement** on ≥50 examples. Cohen's kappa or % agreement. <0.6 means the judge isn't ready.
- **Judge-judge agreement** between two model versions. Useful for tracking judge drift across model upgrades.
- **Bias probes.** Re-score the same eval with positions swapped, with length normalised, with output reformatted. Score drift signals bias.

## Anti-patterns to flag immediately

- **Same model as candidate and judge.** Self-preference is real. Use a different model (different family is better).
- **No randomised position.** Pairwise without order swap is reporting position bias as quality.
- **Unanchored rubric.** "Rate 1–10 on helpfulness" with no examples ≈ random.
- **No meta-eval.** Reporting judge scores without judge-human agreement is reporting unvalidated numbers.
- **One judge call per task.** N=1 on a noisy classifier. Average N≥3 for meaningful differences.
- **Aggregating dimensions silently.** "Overall score" hides which axis moved.
- **Trusting the judge's free-text explanation as scoring signal.** The explanation is post-hoc; the score is the score.
- **Judge sees the candidate's prompt or system instructions.** Leaks evaluation criteria into the judge's reasoning.

## Questions to ask the user

1. Could this be **deterministic** (rule, regex, exact match) instead of a judge?
2. Is the judge a **different model** from the candidate? Different family?
3. **Pairwise or pointwise?** Why?
4. Is position **randomised**? Are ties **allowed**?
5. Does the rubric have **anchored examples** per score level?
6. What's the **judge-human agreement** on your task?
7. What's the **bias probe result** — same eval re-run with swapped positions / normalised length / reformatted style?
8. Are you reporting **confidence intervals**, or single-point scores?

## The hard line

**A judge that hasn't been meta-evaluated isn't a scorer; it's a vibes amplifier.** Validate against humans on ≥50 examples before any production decision rests on its scores.

## Why this exists

LLM-as-judge is everywhere in the eval discourse and almost never validated. Teams ship "the new model scored 4.7 vs 4.3" and don't notice the judge would rate two random outputs at 4.5/4.5. The discipline — pairwise, randomised, anchored, meta-evaluated — converts the judge from a vibes machine into a measurement instrument. The cost is one weekend of human labelling; the alternative is months of shipping regressions confident.

## References

- `references/pairwise-vs-pointwise.md` — when each is appropriate, with measurement guarantees and failure modes.
- `references/bias-probes.md` — concrete bias-probe protocols for position, length, self-preference, format.
- `references/meta-eval.md` — how to validate a judge with ~50 human labels; agreement metrics; thresholds.

## Related skills

- This is a sub-skill of [[agent-evaluation-harness]] — read that first.
- Judge calls are model calls — [[model-routing]] (use a cheap, capable judge; not the same tier as the candidate).
- Judge calls have cost — [[agent-cost-modeling]].
- Judge calls are traced events — [[agent-observability]].
- Judge instructions are a prompt, vulnerable to injection from the candidate output — [[prompt-injection-defense]].
