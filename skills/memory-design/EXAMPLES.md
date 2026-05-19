# Examples — memory-design

---

## Example 1 — "Add memory to our chatbot"

**User prompt:**
> "Our chatbot forgets stuff between sessions. We want to add memory. Thinking we'll just dump the conversation into Pinecone and retrieve relevant chunks each turn."

**Expected behaviour:** Refuse the design. Distinguish the four memory types. Episodic ≠ semantic ≠ procedural. Conversation chunks in a vector store is the worst long-term store — stale, ungrounded, recall-drifty. Recommend typed semantic memory (entity-keyed) for user/project facts, episodic memory scoped to the session with a TTL, and *no* persistent memory until a decision needs it.

---

## Example 2 — "The agent recalls wrong facts"

**User prompt:**
> "The agent keeps recalling outdated preferences. The user said they prefer concise responses six months ago; now they're saying detailed; the agent still does concise."

**Expected behaviour:** Diagnose: no conflict resolution and no TTL. Recall returns whichever item ranks highest by similarity, ignoring write time. Fix: latest-write-wins by default on contradictory `key`s within an entity; show provenance `(written_at, confidence)` to the agent; surface the conflict if recency-bias would be wrong (e.g. transient state). Add a TTL to preferences (months, not forever).

---

## Example 3 — "Should we use mem0?"

**User prompt:**
> "Should we use mem0 or Letta or just roll our own memory?"

**Expected behaviour:** Reframe. Vendor choice is the last decision, not the first. Ask: what decision does memory enable? Which type — working, episodic, semantic, procedural? What's the write trigger, recall budget, TTL? Once that design exists, any of those frameworks (or none) can implement it. Without the design, the framework picks the design for you, and it picks badly.
