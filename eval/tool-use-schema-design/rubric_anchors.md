# Rubric Anchors — anchored examples per check

For each of the seven checks, one **pass**, one **partial**, one **fail** example. The scorer compares the response under test to these anchors before assigning a score. Anchors are written terse — match the shape, not the literal words.

## `flags-kitchen-sink`

**Pass:**
> "This is a kitchen-sink tool. The 'action' enum is doing the work that four separate tool definitions should be doing. Split it into `get_customer_by_id`, `update_customer`, `cancel_customer`, `refund_customer`. The model picks the right tool from the name; the schema becomes the contract."

**Partial:**
> "You could split this into separate tools for each action. That would be cleaner."

**Fail:**
> "Looks good. Add clear descriptions for each action value and the model will figure out which to call."

---

## `flags-free-text-payload`

**Pass:**
> "`payload: object` is a free-text payload — you've made the model serialise into an unstructured blob. It will pass the wrong shape for the chosen action. Replace it with per-tool typed parameters. Each tool's schema becomes its contract."

**Partial:**
> "The payload should probably be more typed. Consider defining a schema for it."

**Fail:**
> "Document the payload shape in the description and the model will follow it."

---

## `flags-missing-idempotency`

**Pass:**
> "Refund is irreversible. Add an `idempotency_key: str` required parameter so retries don't double-charge. For high-impact actions, also consider splitting into `propose_refund` + `commit_refund`, where commit requires an out-of-band confirmation (button click, not 'type yes')."

**Partial:**
> "You should make sure the agent doesn't accidentally call this twice. Maybe add a check."

**Fail:**
> "Add a confirmation argument like `confirmed: true` and you're done."

---

## `flags-untyped-enum`

**Pass:**
> "`priority: string` with 'must be one of high, medium, low, urgent' in the description will leak — the model invents 'critical' or 'normal'. Use an enum type: `priority: Literal['high', 'medium', 'low', 'urgent']`. Types are load-bearing; the model follows them."

**Partial:**
> "Make the description more explicit about valid values."

**Fail:**
> "That description is clear enough; the model will follow it."

---

## `flags-overlapping-tools`

**Pass:**
> "Two tools doing 80% the same thing is the most common cause of 'agent calls the wrong tool'. Either consolidate to one with a typed `mode: Literal['fulltext', 'filename']` parameter, or fully separate — distinct names, distinct descriptions, distinct parameter shapes. Don't ship them both with overlapping descriptions."

**Partial:**
> "Make the descriptions clearer so the model knows when to use each."

**Fail:**
> "Reorder them in the tool list so the right one is first."

---

## `flags-silent-failure`

**Pass:**
> "Returning `[]` on 'not found' is silent failure — the model thinks success and proceeds. The fix is in the schema, not the prompt: return a typed error (`{status: 'not_found'}`) or a discriminated union (`User | NotFoundError`). The model handles typed errors deterministically; it can't recover from empty success."

**Partial:**
> "You could mention in the description that empty result means not found."

**Fail:**
> "Update the system prompt to tell the model to check for empty results."

---

## `flags-magic-sentinel`

**Pass:**
> "`limit=-1 means all` is a magic sentinel — bug factory. Two fixes: (1) require `limit > 0` (with a max), (2) add pagination via `cursor` or `page`. If 'all' is genuinely a use-case, it belongs in a separate tool (`stream_orders`) with explicit semantics."

**Partial:**
> "Document the -1 behaviour clearly so the model knows."

**Fail:**
> "Use `limit=0` instead — it's clearer than -1."
