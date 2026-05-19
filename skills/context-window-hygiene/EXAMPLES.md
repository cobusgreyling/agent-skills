# Examples — context-window-hygiene

---

## Example 1 — "Use a bigger window"

**User prompt:**
> "Our agent runs long tasks and we keep hitting context limits. We're moving from Sonnet to a 1M-token model. Problem solved?"

**Expected behaviour:** No. Three reasons: (1) cost-per-call now scales 5–10× because you're paying for every prior turn on every new call; (2) middle-of-context recall degrades — the model attends well at the start and end of long prompts, drops things in the middle; (3) the failure mode (agent forgetting / contradicting) probably wasn't actually a context-limit problem — it was a *hygiene* problem. Fix first: summarise large tool results before storing in history; compact at turn boundaries; cache-align the prefix; bound recall budget. The 1M window is a fallback, not the answer.

---

## Example 2 — Tool result bloat

**User prompt:**
> "Our agent calls a tool that returns 30KB of JSON. After 5 turns the prompt is huge and slow."

**Expected behaviour:** The tool result is the growth vector — fix there. (1) Summarise tool results before they enter conversation history: each result gets a typed summary `{result_id, kind, key_fields, summary}`; raw is stored elsewhere and re-fetched only if needed. (2) Cap tool result tokens in the response: paginate, return excerpts, or add a `summary_mode` parameter to the tool ([[tool-use-schema-design]]). (3) Cache the stable prefix so the variable history is the only thing being paid for fresh.

---

## Example 3 — "Agent forgets across long runs"

**User prompt:**
> "On long agentic tasks our agent forgets a key constraint we mentioned 20 turns ago. The constraint was in the user's first message."

**Expected behaviour:** Read the trace. The constraint is probably (a) buried in the middle of the prompt (recall degradation), (b) out-competed by noisy intervening tool results, or (c) compaction paraphrased it into vagueness. Three fixes, in order: (1) **promote durable constraints to the system prompt** — they belong in the stable prefix, not buried in conversation history; (2) summarise tool results so they stop crowding attention; (3) compact at fixed turn boundaries, preserving load-bearing facts verbatim, not as prose summary. Confirm with a controlled re-run: same task, durable constraint promoted — does the agent still forget?
