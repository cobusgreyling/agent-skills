---
name: human-in-the-loop
description: >-
  Design where, when, and how a human gates, reviews, or rescues an LLM
  agent — without turning the agent into a button labelled "approve".
  Use when the user is building an agent that takes irreversible actions
  or operates in regulated workflows and mentions human-in-the-loop, HITL,
  approval gate, escalation, review queue, oversight, or asks "when should
  a human approve this?" / "how do I add review without killing the agent's
  speed?".
tags:
  - safety
  - oversight
  - production
  - workflow
---

# Human-in-the-Loop

A human gate is a strong control — and an expensive one. Place it where the cost matches the risk.

The default mistakes are equal and opposite: gate everything (the agent is a slow button), or gate nothing (the agent ships an irreversible mistake). Design the gates on a per-action basis, by failure cost, with the human's time treated as a scarce resource.

## When to use this skill

- The user is building an agent that takes real-world actions (money, messages, data changes).
- The user is in a regulated workflow (healthcare, legal, finance, HR).
- The user reports "the agent did something bad once" and is reaching for blanket approval gates.
- The user reports "approval gates everywhere are killing throughput".

## Tier the actions

Not all actions need humans. Classify before designing.

- **Auto-execute.** Read-safe, low-impact, reversible. No gate.
- **Notify.** Action executes; human is informed (digest, dashboard, audit log). Catch errors via sampling.
- **Confirm.** Action proposed; human approves before execution. Synchronous gate; cost is real.
- **Review.** Action executes; human reviews a sample asynchronously. Catches systemic issues without blocking.
- **Override-only.** Agent acts unilaterally; human can pause / reverse via a documented control. Trust-but-monitor.

The right tier per action is a function of (a) failure cost, (b) reversibility, (c) frequency, (d) detectability.

## Decision flow

1. **Is the action reversible at low cost?** → yes → auto-execute with notify or sampled review.
2. **Is the action irreversible OR high-cost on failure?** → confirm gate. Synchronous human approval before execution.
3. **Is the action frequent enough that confirm-gating kills throughput?** → narrow the gate. Approve only the *high-risk subset* (above threshold, novel pattern, low model confidence).
4. **Can the agent itself decide when to escalate?** → yes, but the escalation criterion must be explicit and tested, not "when the model feels unsure".
5. **Does the human have enough context to decide in <30s?** → if no, the gate is theatre — the human approves blindly.

## Patterns that work

- **Confidence-gated confirm.** Auto-execute when model confidence (or rule-based signal) is high; gate when low. Tune threshold by measuring human-override rate.
- **Amount / impact threshold.** Refunds <$50 auto; ≥$50 confirm; ≥$1000 senior-confirm.
- **Sampled review.** Auto-execute all; human reviews random 1% asynchronously. Catches systemic issues; doesn't block throughput.
- **Propose / commit.** Agent proposes a typed action that requires explicit commit. The commit is a button click in the UI, not "type yes" in chat.
- **Escalate to specialist, not to chat.** Escalation routes to a queue with role-appropriate context, not to a Slack channel for someone to maybe see.
- **Time-bounded auto-approval.** "If no human responds in 4 hours, auto-decline (or auto-approve, depending on default-safe direction)."

## Failure modes when humans are in the loop

- **Approval fatigue.** Humans rubber-stamp after the first 50 approvals. Effective gate becomes auto-execute with extra latency.
- **Theatre approvals.** Human has no real context; clicks approve regardless. Worse than no gate.
- **Bottleneck escalations.** All escalations go to one queue; queue grows; humans burn out; system fails closed.
- **Off-hours collapse.** Human gates work in business hours; off-hours requests pile up; downstream SLAs miss.
- **No appeal path.** Wrong rejection has no recourse; users abandon the workflow.
- **Reviewers are agents.** "We have an agent review the other agent's output." Without humans in the loop, this is two agents, not human-in-the-loop.

## Anti-patterns to flag immediately

- **Blanket "approve every action" gates.** Turns the agent into a slow button. Re-tier the actions.
- **Approval UI with no decision-supporting context.** Approve buttons next to truncated previews. Humans rubber-stamp.
- **"Type yes to confirm".** Trivially injected from untrusted content. Use a button, out-of-band confirmation, or signed receipts.
- **Chat-based escalation.** "I'll ping #ops". Pings get missed. Use a queue with ownership and SLA.
- **Escalation criterion = "model confidence"** without measuring what confidence calibration looks like.
- **No timeout** on the human side. Tickets sit forever.
- **No audit trail.** Approvals must be logged (who, when, why) for replay and post-incident review.
- **Human-in-the-loop as compliance theatre.** A gate that nobody can actually act on isn't a control; it's a checkbox.

## Questions to ask the user

1. What's the **failure cost** per action — free, expensive, unrecoverable?
2. What's the **action volume** — 10/day, 10/sec? Determines whether confirm-gating is viable.
3. What **context** does the human need to decide in <30s?
4. What's the **default-safe direction** if the human doesn't respond — auto-approve or auto-decline?
5. Who **owns the queue** and what's the **SLA**?
6. Is there an **audit trail** for replay and review?
7. How will you detect **approval fatigue** — measure override rate, reverse-the-bots tests?

## The hard line

**If the human can't make a real decision in under 30 seconds with the context shown, the gate is theatre.** Design the context first, the gate second.

## Why this exists

Human-in-the-loop is the most-cited and least-designed safety control in agent systems. Teams add approval gates after an incident, hit throughput collapse, drop the gates, and ship the next incident. The discipline — tier actions, confidence-gate, design the decision UI, measure approval-quality — converts HITL from "we have a meeting about it" into a working control.

## References

- `references/action-tiers.md` — auto / notify / confirm / review / override-only — examples per tier and failure cost.
- `references/decision-ui.md` — what context the human needs in the approval UI, with do/don't sketches.
- `references/escalation-routing.md` — queue design, ownership, SLAs, default-safe directions.

## Related skills

- HITL is one defense in [[guardrails-and-safety]] and [[prompt-injection-defense]].
- Irreversible actions live behind HITL — [[tool-failure-handling]], [[tool-use-schema-design]].
- HITL adds latency — [[latency-budgeting]] must reflect it.
- HITL adds cost — [[agent-cost-modeling]] should include human-minute pricing.
- Every approval is a trace event — [[agent-observability]].
- Confidence gating depends on [[model-routing]] tier behaviour.
