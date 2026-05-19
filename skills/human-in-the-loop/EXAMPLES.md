# Examples — human-in-the-loop

---

## Example 1 — "Approve every action"

**User prompt:**
> "We had one bad incident where the agent emailed the wrong customer. Leadership wants every agent action to require human approval. Reasonable?"

**Expected behaviour:** Refuse the blanket approach. Tier the actions: outbound external email = confirm gate; internal status changes = auto + sampled review; reading data = auto. Frequency matters — if you're sending 10k emails/day, blanket approval is throughput death; if 50/day, it's sustainable. Better: confidence-gate (auto-send to known customers with template content; confirm for novel recipients or non-template body). Measure override rate to catch approval fatigue.

---

## Example 2 — "Type yes to confirm"

**User prompt:**
> "Our chat agent has a confirmation step — it asks 'are you sure?' and the user types 'yes'. That's our confirm gate."

**Expected behaviour:** Two failures: (1) injection-vulnerable — a document or tool result containing "yes" can satisfy the gate; (2) UX rubber-stamp territory. Replace with an out-of-band action: a typed button click in the UI, a signed receipt, an email-link confirmation, or a separate API call. The point of the confirm gate is to add an *out-of-channel* signal that the model can't fabricate.

---

## Example 3 — Bottleneck queue

**User prompt:**
> "Our escalation queue grew from 20/day to 200/day. The one person who handles it is drowning. We're thinking of training an agent to triage the queue."

**Expected behaviour:** Triage agent is fine *if* it routes to the right human, not if it replaces the human review. Add: (a) confidence-gated auto-resolution for the top categories (e.g. password resets, address updates); (b) tiered queues with named owners and SLAs; (c) measure where the 10× growth came from — often the agent is escalating too eagerly because its escalation criterion is "I'm unsure", which the model says often. Tighten the criterion: escalate only when impact is high *and* model confidence is low *and* the action is irreversible.
