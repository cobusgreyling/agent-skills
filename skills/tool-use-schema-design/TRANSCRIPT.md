# Transcript — tool-use-schema-design

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "I'm exposing our internal API to Claude. The API has one endpoint, `/customer`, that takes an action parameter (`get`, `update`, `cancel`, `refund`) and a JSON payload. I'll just wrap it as one tool."

---

## Without skill (typical baseline)

> Sure, you can wrap it as one tool. Define the schema with an `action` enum and a `payload` object. Add good descriptions so the model knows when to use each action. Something like:
>
> ```json
> {
>   "name": "customer",
>   "description": "Manage customer records. Pass an action and a payload.",
>   "parameters": {
>     "action": {"enum": ["get", "update", "cancel", "refund"]},
>     "payload": {"type": "object"}
>   }
> }
> ```
>
> Make sure the descriptions explain when to call each action.

Goes along with the user's plan. Misses the central design failure.

---

## With skill (behavioural expectation)

> Stop. What you've described is a **kitchen-sink tool**, and it's the #1 reason models call tools wrong.
>
> The rule is: **one tool, one job**. If the description needs the word "or", split the tool. Yours needs "or" three times.
>
> Worse: `payload: object` is a **free-text payload parameter**. You've made the model serialise into an unstructured blob. It will fail — sometimes silently, sometimes by inventing fields, almost always by passing the wrong shape for the chosen `action`.
>
> Refactor to four tools:
>
> ```
> get_customer_by_id(customer_id: str) -> Customer
> update_customer(customer_id: str, fields: UpdateFields) -> Customer
> cancel_customer(customer_id: str, reason: CancelReason) -> CancellationReceipt
> refund_customer(customer_id: str, amount_cents: int, reason: RefundReason, idempotency_key: str) -> RefundReceipt
> ```
>
> Five things changed:
>
> 1. **Names carry the action.** `verb_noun` for actions, `get_noun_by_key` for lookups. The model now knows *which* tool to call from the name alone.
> 2. **Typed parameters per tool.** No generic `payload`. Each tool's schema is the contract. Required vs optional is explicit.
> 3. **Enums for closed sets** (`CancelReason`, `RefundReason`). Models follow enums; they leak when "must be one of X, Y, Z" lives in a string description.
> 4. **Idempotency key on the destructive tool.** Refund is irreversible. The tool requires an explicit key so retries don't double-charge.
> 5. **Typed return shapes.** `CancellationReceipt` not `dict`. The model reasons about returns when planning next calls.
>
> One more concern: **refund is high-impact and reversible only by an engineer**. Either require an explicit `confirmed: true` argument, or split into `propose_refund` + `commit_refund` with the second requiring an out-of-band confirmation (button click, not "type yes").
>
> Anti-patterns I'm watching for in your other tools:
>
> - **Kitchen-sink tools** like the one you proposed.
> - **Free-text payloads** (`payload: string`).
> - **Two tools that overlap by 80%** — the model alternates between them.
> - **HTML/markup return values** instead of structured data.
> - **Silent failure** (returning empty results on error) — the model assumes success.
> - **No examples in descriptions** — one concrete example doubles reliability.
>
> Six questions:
>
> 1. What does each tool **do in one verb**? If you need two, split.
> 2. What's the **smallest set of parameters** that fully specify the action?
> 3. What does the tool return on **success, partial success, and failure**?
> 4. Is the action **idempotent**? If not, who owns retry safety?
> 5. What's the **rate / call-budget** the agent must respect?
> 6. How will you **observe every call**?
>
> **Hard line:** if the schema needs a paragraph to explain when to call the tool, split the tool. The schema is the contract; if humans can't read it, the model can't either.

---

## The diff

What changed because the skill fired:

- **Refused the kitchen-sink design.** Named the failure mode explicitly.
- **Refactored one tool into four**, with verbs, typed enums, typed returns.
- **Added idempotency key** to the destructive tool unprompted.
- **Surfaced the propose-then-commit pattern** for irreversible actions.
- **Listed six anti-patterns** to scan their existing tools for.
- **Invoked the hard line** on the schema-as-contract rule.

A naive answer wraps the API. A skilled answer refuses, refactors, and hardens the destructive path before any code ships.
