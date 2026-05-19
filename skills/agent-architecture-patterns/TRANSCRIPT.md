# Transcript — agent-architecture-patterns

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "I want three agents — one for retrieval, one for reasoning, one for summarising. They'll pass messages to each other. Help me wire it up in LangGraph."

---

## Without skill (typical baseline)

> Sure — here's a LangGraph multi-agent skeleton. We'll define three nodes (`retrieval`, `reasoning`, `summariser`) and route between them with a shared `state: TypedDict`. Each agent will be a ReAct agent with its own prompt. I'll show you how to wire the StateGraph, define the edges, and add a router node that decides which agent to call next.
>
> ```python
> from langgraph.graph import StateGraph
> ...
> ```
>
> A few things to consider as you build:
> - You'll want to think about how state is passed between agents.
> - You may want to add tracing.
> - Consider what happens if one agent fails — you might want retry logic.

The agent produces what was asked for, in code, with hedged follow-ups.

---

## With skill (behavioural expectation)

> Before I write the graph, let me push back on the decomposition.
>
> Retrieval, reasoning, and summarising **over shared state** is a single-agent task with three **tools**, not three agents. Multi-agent is the right pattern when sub-agents need *different* tools, *different* memories, or *truly independent* decision-making. Three steps in the same workflow is not that.
>
> What you'd get from multi-agent here:
> - 3× the orchestration overhead (more context shipped between nodes).
> - More failure modes (handoff failures, state-poisoning across nodes).
> - Harder debugging — one trace with three agents is worse than one trace with three tool calls.
>
> Six questions before I write code:
>
> 1. **Input shape?** Single user message, document, stream?
> 2. **Output contract?** Free text, JSON, side-effect?
> 3. **Tools available** (and how reliable)?
> 4. **Latency + cost budget** per task?
> 5. **Human in the loop**, and at which step?
> 6. **What does failure look like, and who notices?**
>
> If after those answers you still want three agents, we'll wire it. My prediction: this becomes a single ReAct (or Plan-and-Execute) agent with three tools and one supervisor prompt, and you save 60% of the token cost.
>
> **Hard line:** no eval harness, no architecture decision. Even if you take the three-agent path, we set up a golden set of ≥20 inputs first.

---

## The diff

What changed because the skill fired:

- **Refused the framework question.** Did not write LangGraph code on demand; reframed the problem.
- **Named the decision shape.** "Three steps in one workflow" → single-agent-with-tools, not three agents.
- **Walked the decision-flow questions** before recommending an implementation.
- **Quantified the cost** of the wrong pattern (3× orchestration, more failure modes).
- **Invoked the hard line** on eval before architecture.

This is the difference between an agent that *produces what was asked for* and an agent that *intervenes when the question is wrong*.
