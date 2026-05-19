---
name: agent-architecture-patterns
description: >-
  Choose the right architecture for an LLM agent or multi-agent system. Use
  when the user is designing, comparing, or debugging agentic workflows and
  mentions ReAct, Reflexion, Plan-and-Execute, Router, Supervisor, Hierarchical,
  multi-agent, tool-use loop, agent graph, LangGraph, AutoGen, CrewAI, or asks
  "which agent pattern should I use" / "how should this agent be structured".
---

# Agent Architecture Patterns

Most agent failures are architectural, not prompt-level.

Pick the pattern that matches the task's **decision shape**, not the framework
that's trending. The wrong pattern multiplies cost, latency, and failure modes.

## When to use this skill

- The user is sketching a new agent or rewriting an existing one.
- The user describes symptoms — looping, drifting, exceeding budget, losing context — that point at the architecture, not the prompt.
- The user names a framework (LangGraph, AutoGen, CrewAI, Swarm) and wants to know which pattern to instantiate.
- The user is comparing single-agent vs. multi-agent for a given workload.

## Decision flow

Walk this top-down before recommending anything.

1. **Is the task a single turn with deterministic tools?** → no agent. Use a typed tool call.
2. **Is the path knowable up front?** → **Plan-and-Execute**. Plan once, execute steps, no re-planning unless a step fails.
3. **Is the path discoverable only by trying?** → **ReAct**. Tight think→act→observe loop, one step at a time.
4. **Does the task need self-correction on quality (not just errors)?** → wrap the executor in **Reflexion** / critic-actor.
5. **Are there ≥3 disjoint skills (e.g. SQL, code, search) with no shared state?** → **Router** dispatches a single sub-agent per turn.
6. **Do sub-agents need to collaborate, hand off, or argue?** → **Supervisor** owns the conversation and delegates; sub-agents do not talk to each other directly.
7. **Are there ≥2 tiers of decomposition (team-of-teams)?** → **Hierarchical**. Use sparingly — debuggability collapses fast.

Default to the simplest pattern that fits. Escalate only on evidence.

## The patterns in one line each

- **ReAct** — interleaved reasoning + action in a single loop. Cheap, observable, brittle on long tasks.
- **Plan-and-Execute** — produce a plan, then execute it. Cuts token cost vs. ReAct on long tasks; brittle if the world changes mid-plan.
- **Reflexion** — actor proposes, critic scores, actor revises. Buys quality at 2–4× cost. Cap iterations hard.
- **Router** — one classifier picks one downstream skill per turn. Not multi-agent — it's `switch` with an LLM.
- **Supervisor** — a coordinator agent owns state and dispatches workers. Workers are stateless from each other's POV.
- **Hierarchical** — supervisors of supervisors. Last resort.
- **Swarm / handoff** — peer agents pass control via explicit handoff tools. Useful for role-shaped tasks (triage → specialist), dangerous for open-ended ones.

See `references/patterns.md` for the full per-pattern brief — when each works, when each fails, and the minimal control-flow sketch.

## Anti-patterns to flag immediately

- **Multi-agent for parallelism alone.** If sub-agents don't need *different* tools, prompts, or memories, you want concurrent tool calls, not agents.
- **Free-form agent-to-agent chat.** Round-robin debates blow tokens and rarely converge. Force structured handoffs with explicit termination.
- **Unbounded ReAct loops.** Every ReAct agent needs a max-step cap *and* a budget check inside the loop, not only at the edge.
- **Shared mutable memory across agents.** Causes context poisoning. Pass explicit messages instead.
- **One mega-prompt doing routing + execution + reflection.** Separate the roles into separate calls; you can't debug what you can't isolate.

## Picking the pattern: questions to ask the user

Before recommending anything, get answers to:

1. What's the **input shape** (single message, document, stream, ticket)?
2. What's the **output contract** (free text, JSON, side-effect on a system)?
3. What **tools** exist and how reliable are they?
4. What's the **budget** per task — latency and cost ceiling?
5. Is there a **human in the loop**, and at which step?
6. What does **failure** look like, and who notices?

If you can't answer these, you're not ready to pick a pattern — say so.

## Evaluation, not vibes

Whatever pattern is chosen, demand:

- A **golden set** of ≥20 representative inputs before the first commit.
- **Trace logging** of every step (input, tool call, output) — see `references/observability.md`.
- A **regression check** before any prompt or graph change ships.

No eval harness, no architecture decision. Block the conversation on it.

## References

- `references/patterns.md` — full per-pattern brief (when to use, failure modes, control-flow sketch).
- `references/frameworks.md` — mapping patterns to LangGraph, AutoGen, CrewAI, OpenAI Swarm.
- `references/observability.md` — what to log, span shape, eval scaffolding.
