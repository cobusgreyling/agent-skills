---
name: multi-agent-orchestration
description: >-
  Decide when to split work across multiple agents vs one agent with tools,
  and design the handoffs when you do. Use when the user is sketching a
  multi-agent system or debugging one, and mentions handoff, delegation,
  supervisor, swarm, crew, sub-agent, agent-to-agent, A2A, manager-worker,
  team of agents, or asks "should I split this into multiple agents?" /
  "why do my agents talk forever and never finish?".
tags:
  - multi-agent
  - orchestration
  - architecture
  - handoff
---

# Multi-Agent Orchestration

Every handoff is a context loss. Justify it.

The default assumption is that more agents means more capability. The actual outcome is more tokens, more latency, more variance, and harder debugging — unless the handoff buys something a single agent with tools cannot.

## When to use this skill

- The user is proposing a multi-agent system (Crew, Swarm, Supervisor, A2A).
- The user has a multi-agent system and reports loops, drift, runaway cost, or "no one ever decides".
- The user is comparing "subagents" vs "tools" for the same workload.
- The user is using a framework's multi-agent abstraction without a reason that survives "why not a tool?".

## The handoff test

Before splitting work into a second agent, the handoff must clear all three:

1. **Different context.** The second agent needs context the first agent must *not* see (token budget, role boundary, privacy).
2. **Different tools or model.** The second agent uses tools, a model tier, or constraints the first cannot.
3. **Clear termination.** The second agent returns a single typed result; control returns to a known place.

If any of the three fails, you want a tool call, not an agent.

## Decision flow

1. **Can a single agent with the right tools do the job?** → yes? Stop. Add the tool.
2. **Do you need to enforce a role boundary the prompt can't enforce?** (e.g. critic must not see actor's chain-of-thought) → maybe a second agent. Or use structured prompting.
3. **Do sub-tasks need genuinely different models / token budgets / safety policies?** → multi-agent justified.
4. **Are agents collaborating or delegating?** → delegation only. Free-form collaboration loops are an anti-pattern.
5. **Who owns termination?** → exactly one coordinator. Peer-to-peer termination is a footgun.

## Patterns that work

- **Supervisor + workers.** Supervisor owns state, dispatches a worker per turn, workers are stateless. Returns to supervisor with a typed result.
- **Pipeline (planner → executor → verifier).** Strict ordering, explicit handoffs, no back-edges except `reject → re-plan`.
- **Triage → specialist.** First agent classifies; second agent does the work. Specialist never re-classifies.
- **Critic-actor (Reflexion).** Same task, separate roles, hard iteration cap (≤3).

## Patterns to refuse

- **Peer-to-peer chat.** Agents discussing the task to "reach consensus" burn tokens and rarely converge.
- **Round-robin debate.** Same as above with a turn schedule.
- **Hierarchical-of-hierarchies (team-of-teams).** Debuggability collapses. Use as last resort, never as default.
- **Agent-as-tool with implicit shared memory.** Side-channel state ruins replayability.

## Handoff design rules

- **Typed payload.** Handoff message is a typed schema, not free text.
- **One return path.** The receiver returns to a known parent or terminates the run.
- **Termination contract.** Max turns, max wall-clock, max cost — all three, all enforced.
- **No back-channels.** Agents communicate only via the documented handoff API.
- **Trace the handoff.** Every handoff is a span. See [[agent-observability]].

## Anti-patterns to flag immediately

- **Multi-agent for parallelism.** If sub-agents don't need different context/tools/model, you want concurrent tool calls.
- **Agent personas as design.** "Senior engineer reviews junior engineer's code" — these are roles, not architectures. Use a single agent with a critic step.
- **Free-text handoff.** "Manager: do this thing — Worker: ok" with no schema. Loses fidelity at every step.
- **No termination.** Agents that can hand off without bound. Always set step + cost ceilings.
- **Cross-agent shared mutable memory.** Context poisoning at scale.
- **Framework-driven design.** "We're using CrewAI, so we have a crew." Pick the pattern first, the framework second.

## Questions to ask the user

1. What does the **handoff buy** — different context, different tools, different model, different policy?
2. What is the **typed payload** at each handoff?
3. Who owns **termination** and what are the limits?
4. How does the system **fail gracefully** when an agent loops or hangs?
5. What does a **single trace** look like across agents — can you replay it?
6. If you collapsed this to one agent with tools, what would break?

If the last answer is "nothing would break", collapse it.

## The hard line

**Every additional agent must clear the handoff test or be deleted.** Multi-agent is a debt instrument; interest is paid in tokens and latency on every call.

## Why this exists

The multi-agent boom has produced a generation of systems that are slower, dumber, and more expensive than the single-agent versions they replaced. The systems that work treat handoff as a structural decision — typed payload, single termination, hard limits — not a vibes-level "let agents collaborate".

## References

- `references/patterns.md` — supervisor, pipeline, triage, critic-actor — control-flow sketch and failure modes for each.
- `references/handoff-payloads.md` — typed schemas for common handoffs (triage → specialist, planner → executor, actor → critic).
- `references/frameworks.md` — CrewAI, AutoGen, OpenAI Swarm, LangGraph multi-agent — where each helps, where each leaks.

## Related skills

- Multi-agent is one shape of [[agent-architecture-patterns]] — start there.
- Each agent's tools are still [[tool-use-schema-design]].
- Cost scales by agent-call, not by agent-count — [[agent-cost-modeling]].
- Latency budget must include handoff round-trips — [[latency-budgeting]].
- Handoffs must be traced — [[agent-observability]].
- Loops and hangs are guardrail concerns — [[guardrails-and-safety]].
