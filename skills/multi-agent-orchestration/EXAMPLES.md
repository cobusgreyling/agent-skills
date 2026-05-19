# Examples — multi-agent-orchestration

---

## Example 1 — "Researcher → writer → reviewer"

**User prompt:**
> "I'm building a content pipeline: researcher agent gathers sources, writer agent drafts, reviewer agent edits. CrewAI seems perfect."

**Expected behaviour:** Apply the handoff test. Three roles, but do they need different *context*, *tools*, or *model*? If researcher and writer share the same context and tools and model, this is one agent with two prompts, not two agents. Reviewer only justifies splitting if (a) it must not see the writer's chain-of-thought (role-boundary), or (b) it uses a different model tier for quality scoring. Otherwise: single agent with a `critique → revise` loop, hard iteration cap.

---

## Example 2 — "Agents talk forever"

**User prompt:**
> "My CrewAI crew loops — manager keeps asking workers for clarification, workers ask back, nothing ships."

**Expected behaviour:** Diagnose three failures: (1) no typed handoff payload (free-text "do this thing"), (2) no termination contract (max turns / cost / wall-clock), (3) peer-to-peer back-and-forth instead of strict delegation. Fix: supervisor owns termination, workers return a typed result or `INSUFFICIENT_INFO` with a structured ask; supervisor decides whether to retry or escalate. Cap turns hard.

---

## Example 3 — "Should this subagent be a tool?"

**User prompt:**
> "I have a sub-agent that does SQL. It takes a question, writes SQL, runs it, returns rows. Should it be an agent or a tool?"

**Expected behaviour:** Apply handoff test. Does the SQL sub-agent need (a) context the parent should not have, (b) a different model or tools, (c) a clear typed return? If only (c) is true, this is a **tool**, not an agent — `query_database(question: str) -> Rows` with the SQL synthesis inside the tool implementation. Collapsing it removes a handoff, a trace span, a failure mode, and a non-trivial cost.
