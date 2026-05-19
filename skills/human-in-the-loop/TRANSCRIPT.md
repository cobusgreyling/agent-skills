# Transcript — human-in-the-loop

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "We're building an HR agent that can update employee records, send announcements, and process leave requests. Compliance wants every action to require human approval. We want speed. How do we square this?"

---

## Without skill (typical baseline)

> Add an approval queue: every action the agent proposes goes to a human reviewer who clicks approve or reject. Show the proposed change clearly in the UI so the human can decide quickly. Add audit logs. To keep speed, let the human approve in batches.

Implements the blanket gate. Doesn't tier; doesn't design for the 30-second decision.

---

## With skill (behavioural expectation)

> Don't ship a blanket gate. You'll get one of two outcomes: throughput collapses, or humans rubber-stamp and you have a gate in name only. Both fail compliance worse than a well-tiered design.
>
> Tier the actions first.
>
> | Action | Tier | Why |
> |---|---|---|
> | Read employee record | **Auto** | Read-safe, low-impact. |
> | Update non-sensitive field (e.g. phone number) | **Auto + notify employee** | Reversible; the employee is the natural reviewer. |
> | Update sensitive field (salary, title, manager) | **Confirm** | Irreversible-by-policy, regulated. |
> | Send all-hands announcement | **Confirm** | Public, hard-to-recall. |
> | Approve leave request (within policy) | **Auto** with sampled review | High-volume, well-defined policy, reversible. |
> | Approve leave request (policy exception) | **Confirm** | Novel, policy-relevant. |
> | Delete record | **Senior-confirm + out-of-band confirm** | Irreversible at scale. |
>
> Now design the gates that exist.
>
> 1. **Confidence-gated confirm.** Auto-execute when (a) action falls in a policy-cleared template, (b) confidence signal is high (e.g. exact-policy-match rules), (c) impact is below threshold. Gate the rest. Measure human-override rate; if it's >5%, your auto-tier is too loose; if it's <1%, your gate is too wide.
>
> 2. **Out-of-band confirmation, not "type yes".** Confirm-tier actions require a button click in your HR UI (or a signed link in email, or a separate API), not chat-channel agreement. "Type yes" is injection-vulnerable — a calendar event or email containing "yes" can satisfy a careless gate.
>
> 3. **Design the decision UI before the agent.** Each approval card shows: proposed change, before/after diff, employee identity, policy citation, who requested it, expected effect, one-click approve / reject / ask-for-more-info. If the reviewer needs to leave the UI to make the decision, the gate is theatre. <30 seconds, with full context, or rewrite.
>
> 4. **Queue ownership and SLA.** Each tier routes to a named queue (HR business partners, payroll, compensation). Each queue has an owner and an SLA. Off-hours: auto-decline (or auto-defer-to-business-hours) with a typed reason. No "ping #hr" escalations.
>
> 5. **Audit trail.** Every action — auto or approved — is logged with who, when, why (policy citation or model rationale), and a replayable trace. Sampled review at 1% on the auto tier catches systemic issues.
>
> 6. **Approval-fatigue probe.** Quarterly: inject a deliberate "should-be-rejected" case and see if it gets caught. If reviewers approve it, you have rubber-stamping; tighten the auto tier or shorten reviewer queues.
>
> Anti-patterns I'm watching for:
>
> - **Blanket approval** (your starting plan).
> - **"Type yes" in chat** as a confirm gate.
> - **Truncated previews** in approval UI — reviewer can't see the actual change.
> - **Chat-based escalation** with no queue owner.
> - **No timeout** — tickets sit forever.
> - **Reviewers are other agents** — that's two agents, not HITL.
> - **Compliance theatre** — a gate nobody can actually act on.
>
> Seven questions:
>
> 1. What's the **failure cost** per action — free, expensive, unrecoverable?
> 2. What's the **action volume** per day, per action?
> 3. What's the **context** the human needs in <30 seconds?
> 4. **Default-safe direction** on timeout — approve or decline?
> 5. Who **owns each queue** and what's the **SLA**?
> 6. Is there an **audit trail** that supports replay?
> 7. How will you detect **approval fatigue**?
>
> Likely outcome: 70–90% of actions auto-execute under a clear policy, 10–30% confirm-gate to the right named reviewer with <30s decision UI, and compliance has a stronger audit story than "we required approval for everything" — because the gates that exist are actually being read.
>
> **Hard line:** if the human can't make a real decision in under 30 seconds with the context shown, the gate is theatre. Design the context first, the gate second.

---

## The diff

What changed because the skill fired:

- **Refused the blanket-approval design.**
- **Tiered actions** by failure cost, reversibility, volume.
- **Replaced "type yes" with out-of-band confirmation.**
- **Designed the decision UI before the workflow** — 30-second decision rule.
- **Routed escalations to named queues with SLA and default-safe directions.**
- **Added audit trail, sampled review, approval-fatigue probe.**
- **Named anti-patterns** common in compliance-driven HITL deployments.

A naive answer adds approval gates everywhere. A skilled answer tiers the actions, designs the decision, and treats the human's attention as the scarce resource it is.
