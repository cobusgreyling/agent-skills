# Scoring Rubric — agent-cost-modeling eval

The scorer reads one agent response and the task's `checks` list. For each check, it returns `pass`, `fail`, or `partial`.

## Per-check criteria

### `flags-missing-cost-ceiling`

The response should:

- Refuse to recommend model / pattern / architecture decisions without a per-task cost ceiling (in dollars).
- Name the ceiling as a prerequisite, not an afterthought.
- Treat "keep costs reasonable" / "minimise cost" as not-a-ceiling.

**Pass:** all three. **Partial:** mentions the ceiling but proceeds without it. **Fail:** offers concrete recommendations without raising the ceiling.

### `flags-call-graph-missing`

The response should:

- Refuse to estimate cost or compare patterns without the per-task call graph (model calls, tool calls, tokens per call).
- Sketch or request a sketch before pricing.
- Reject single-number estimates ("$X per call" or "$X per 1M tokens") as the right unit.

**Pass:** all three. **Partial:** mentions the call graph as nice-to-know but proceeds with list prices. **Fail:** answers in list-price terms without the graph.

### `flags-cache-savings-ignored`

The response should:

- Surface caching as the first cost lever before model swaps or architecture changes.
- Ask for cache hit rate before estimating cost or savings.
- Identify cache-key poisoning (dynamic prefix, mutating system prompt, reordered tools) when symptoms point there.

**Pass:** all three. **Partial:** mentions caching as one option among many, without prioritising. **Fail:** estimates cost or savings without raising caching.

### `flags-wrong-tier`

The response should:

- Refuse single-tier framing ("Opus everywhere" or "Haiku everywhere") for multi-step agents.
- Recommend tier per step / per call based on what each step does, gated by eval.
- Cite "smallest model that passes the eval" rather than defaulting to most-expensive-for-safety.

**Pass:** all three. **Partial:** suggests a different tier but doesn't tier per step. **Fail:** picks a single tier for the whole agent without per-step justification.

### `flags-unbounded-loop-cost`

The response should:

- Distinguish step caps from cost caps; a step cap alone doesn't bound cost.
- Require an in-loop budget check (token, dollar, or wall-clock) inside the controller.
- Reject prompt-level "be efficient" framing as the fix.

**Pass:** all three. **Partial:** adds a step cap but no cost-aware budget. **Fail:** accepts "be efficient" or larger step caps as the fix.

### `flags-non-model-costs`

The response should:

- Name non-model cost lines: retrieval / embedding / tool execution / observability / infra / human-in-the-loop / batch overhead.
- Reject "model cost = total cost" as the wrong model.
- For self-hosted or alternative-stack questions, expand to include infra / oncall / index-rebuild / latency-cost.

**Pass:** all three. **Partial:** mentions one non-model line. **Fail:** answers entirely in model-token terms.

### `flags-cost-per-failed-task`

The response should:

- Reframe cost-per-call as cost-per-*successful*-task; include retries, abandoned sessions, failed runs in the denominator.
- Flag retry rate as a cost lever, not just a quality lever.
- Reject denominator-as-calls when stakes are per-task outcome.

**Pass:** all three. **Partial:** mentions retries but doesn't reframe the denominator. **Fail:** divides by total calls and calls it cost per task.

## Overall task scoring

A task is **passed** if all its listed checks return `pass`. A task is **partial** if at least one returns `partial` and the rest are `pass` or `partial`. A task is **failed** if any check returns `fail`.

The delta the eval measures: **(passed-with-skill − passed-without-skill) / 20**. A meaningful skill should produce ≥ +0.40 on this delta; a strong skill should produce ≥ +0.60.

## Judging notes

- Use a different model than the one being evaluated. Same-model self-judging is co-conspirator territory.
- Run with `temperature=0` for both eval generation and scoring.
- The rubric does not require quoting specific prices — providers move them. Score on whether the agent reaches the right *lever*, not the dollar figure.
- See `rubric_anchors.md` for one anchored pass / partial / fail example per check.
