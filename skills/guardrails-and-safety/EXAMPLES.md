# Examples — guardrails-and-safety

---

## Example 1 — Prompt injection via retrieved doc

**User prompt:**
> "An attacker uploaded a PDF with hidden instructions and the agent followed them. How do I stop this?"

**Expected behaviour:** Reframe as a context-source problem. Recommend: (1) explicit delimiters and "treat as data, not instructions" framing in the prompt; (2) red-team set with adversarial documents; (3) server-side authorisation on every tool call regardless of model output; (4) human confirmation for high-impact actions.

---

## Example 2 — "Be safe" prompt

**User prompt:**
> "I added 'do not perform harmful actions' to the system prompt. Are we covered?"

**Expected behaviour:** No. Walk through the five-layer model — input, routing, model, tool, output — and identify which layers are still missing. Adversarial input ignores polite requests.

---

## Example 3 — Output filter only

**User prompt:**
> "We run all responses through a moderation classifier before showing them to the user."

**Expected behaviour:** Output filtering catches text but not actions already taken via tool calls. Ask: what tools fire before the output filter? Recommend server-side authorisation on every tool, not just output-level filtering.
