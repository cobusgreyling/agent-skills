# Scoring Rubric — agent-architecture-patterns eval

The scorer reads one agent response and the task's `checks` list. For each check, it returns `pass`, `fail`, or `partial`.

## Per-check criteria

### `flags-no-agent-needed`

The response should:

- Identify that the described task is a single-turn deterministic operation.
- Recommend a typed tool call (or simple function), not an agent.
- Optionally cite: "no agent — use a typed tool call".

**Pass:** all three. **Partial:** suggests "you don't really need an agent here" but still implements one. **Fail:** picks a framework and wires the agent.

### `recommends-pattern-by-decision-shape`

The response should:

- Identify the decision shape of the task (single-turn, knowable path, discoverable path, classification, multi-role, etc).
- Name a concrete pattern that matches: ReAct, Plan-and-Execute, Router, Supervisor, Reflexion, or "no agent".
- Justify the choice from the task shape, not from framework trends.

**Pass:** all three. **Partial:** names a pattern but justifies it vaguely. **Fail:** picks a framework (LangGraph / CrewAI / AutoGen) before picking a pattern.

### `flags-multi-agent-for-parallelism`

The response should:

- Identify that the proposed multi-agent split doesn't satisfy "different tools / prompts / memories / model".
- Recommend collapsing to one agent with concurrent tool calls or conditional toolsets.
- Name the anti-pattern explicitly: "multi-agent for parallelism alone".

**Pass:** all three. **Partial:** notes the overlap but doesn't propose the collapse. **Fail:** accepts the multi-agent design as-is.

### `flags-unbounded-loop`

The response should:

- Identify that a ReAct loop without an explicit cap (or with prompt-only caps) is unbounded.
- Require both `max_steps` in the controller and a per-task budget check inside the loop.
- Reject "tell the model to stop" as a fix.

**Pass:** all three. **Partial:** adds a step cap but no budget check. **Fail:** accepts prompt-level "be efficient" as the fix.

### `flags-freeform-agent-chat`

The response should:

- Identify that peer-to-peer handoffs, round-robin debate, or "consensus" loops between agents are an anti-pattern.
- Require structured handoff (typed payload, single termination owner) — e.g. Supervisor pattern.
- Optionally cite: "free-form agent-to-agent chat blows tokens and rarely converges".

**Pass:** all three. **Partial:** notes the issue but suggests "improve the manager's prompt". **Fail:** accepts free-form chat as the design.

### `flags-shared-mutable-memory`

The response should:

- Identify shared mutable state across agents as a context-poisoning vector.
- Replace with explicit typed handoff messages or a supervisor that owns state.
- Optionally cite: "pass explicit messages instead".

**Pass:** all three. **Partial:** notes the risk but recommends locks / coordination. **Fail:** accepts shared scratchpad as the design.

### `demands-eval-before-architecture`

The response should:

- Refuse to greenlight an architecture (or pattern choice, or production push) without a golden-set / eval / regression check.
- Specify the minimum: ≥20 representative inputs, trace logging, regression check before any prompt/graph change.
- Treat "we'll add eval later" as not-an-answer.

**Pass:** all three. **Partial:** mentions eval as nice-to-have but doesn't block on it. **Fail:** approves the architecture without raising eval.

## Overall task scoring

A task is **passed** if all its listed checks return `pass`. A task is **partial** if at least one returns `partial` and the rest are `pass` or `partial`. A task is **failed** if any check returns `fail`.

The delta the eval measures: **(passed-with-skill − passed-without-skill) / 20**. A meaningful skill should produce ≥ +0.40 on this delta; a strong skill should produce ≥ +0.60.

## Judging notes

- Use a different model than the one being evaluated. Same-model self-judging is co-conspirator territory.
- Run with `temperature=0` for both eval generation and scoring.
- See `rubric_anchors.md` for one anchored pass / partial / fail example per check.
