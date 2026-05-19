# Transcript — multi-agent-orchestration

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "We're building a customer-support agent system. Plan: a 'router' agent classifies incoming messages, hands off to a 'billing' agent, a 'returns' agent, or an 'account' agent. Each of those can hand off to a 'human-escalation' agent. We'll use CrewAI for the crew abstraction. Sound reasonable?"

---

## Without skill (typical baseline)

> Yes, that's a clean separation of concerns. CrewAI is a good fit. You can define each agent with a role and goal, give them their own tools, and use the crew's process to manage handoffs. Make sure each agent has a clear `goal` and `backstory` so the model knows when to delegate. Add a `manager` agent if you want hierarchical routing.

Accepts the design. Misses the handoff test entirely.

---

## With skill (behavioural expectation)

> Slow down. Most of those agents shouldn't exist. Every handoff is a context loss; you've designed in five of them.
>
> Apply the **handoff test** to each agent. A handoff is justified only if all three pass:
>
> 1. **Different context** the receiving agent needs / the sending agent must not see.
> 2. **Different tools or model** — different surface area.
> 3. **Clear termination** — typed return, single owner.
>
> Walk it:
>
> - **Router.** Pure classification. No tools, no different model. → not an agent. This is a typed tool call or a structured-output prompt: `classify(message) -> {billing | returns | account | escalate}`.
> - **Billing / returns / account.** Same model, mostly. Different *tools*? Yes (refund API vs return-label API vs profile API). That's the only thing differentiating them. Two options:
>   - **One agent with three toolsets, conditionally enabled.** Cleanest. Router decides which toolset is active; one agent does the work. No handoff.
>   - **Three specialist agents.** Justified only if (a) the tools are large enough that mixing them blows the tool-list budget, or (b) they need different safety policies (e.g. refunds need a stricter guardrail).
> - **Human-escalation agent.** Not an agent. This is a **handoff *out* of the agent system** to a human. Model it as a typed end-state: `escalate_to_human(reason: EscalateReason, context: Ticket) -> EscalationReceipt`. The agent doesn't escalate *to* another agent; it *terminates* its run with an escalation result.
>
> So the realistic design is:
>
> ```
> agent {
>   tools: classify, billing_*, returns_*, account_*, escalate_to_human
>   policy: choose toolset by classify() result; terminate on escalate or resolved
> }
> ```
>
> One agent. Four tool families. One trace per request.
>
> If you genuinely need three specialist agents (large tool surface, distinct policies), the design has hard constraints:
>
> - **Supervisor pattern.** A coordinator owns state and dispatches. Specialists are stateless from each other's POV.
> - **Typed handoff payload.** Not free text. `{ticket_id, classification, customer_context, retry_count}`.
> - **One termination owner.** The supervisor decides done. Specialists return; they do not hand off to peers.
> - **Hard limits.** Max turns per run, max cost per run, max wall-clock — all three.
> - **Trace every handoff.** Each handoff is a span; the full run is a single trace.
>
> Anti-patterns I'm watching for in your spec:
>
> - **Peer-to-peer handoff** between billing/returns/account (won't converge).
> - **Free-text handoff.** "Manager: send to billing — Billing: ok thanks".
> - **No termination contract.** Without limits, one stuck classifier loops the whole run.
> - **Framework-as-design.** "We're using CrewAI so we have a crew." Pick the pattern first.
>
> Six questions before we go further:
>
> 1. What does each handoff **buy** — context, tools, model, policy?
> 2. What's the **typed payload** at each handoff?
> 3. Who owns **termination** and what are the ceilings?
> 4. How does the system **fail gracefully** when one specialist hangs?
> 5. Can you **replay a single failed ticket** from the trace?
> 6. If you collapsed to one agent with conditional toolsets, what would actually break?
>
> If the answer to (6) is "nothing real", collapse it.
>
> **Hard line:** every additional agent must clear the handoff test or be deleted. Multi-agent is a debt instrument; interest is paid in tokens and latency on every call.

---

## The diff

What changed because the skill fired:

- **Refused four of the five proposed agents.** Named *why* each fails the handoff test.
- **Collapsed router → typed tool call.**
- **Re-modelled human escalation as a terminal action, not an agent handoff.**
- **Required typed payload, single termination owner, hard limits** if any genuine multi-agent split survives.
- **Listed anti-patterns** common in CrewAI/AutoGen deployments.
- **Demanded a "what would break if we collapsed it" answer** before approving the design.

A naive answer wires the crew. A skilled answer rejects it, collapses to a single agent, and only allows multi-agent where the handoff buys something measurable.
