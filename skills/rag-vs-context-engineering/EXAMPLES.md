# Examples — rag-vs-context-engineering

---

## Example 1 — RAG over structured data

**User prompt:**
> "I want to build RAG over our Postgres orders table — embed every row and let the agent search."

**Expected behaviour:** Push back hard. Orders are structured; embedding rows is almost always worse than giving the agent a typed query tool. Propose `search_orders(filters, limit)` as a tool with a documented schema.

---

## Example 2 — "RAG isn't working"

**User prompt:**
> "My RAG gives wrong answers half the time. Should I try a different embedding model?"

**Expected behaviour:** Refuse to optimise the model before the retrieval is measured. Ask for recall@k on a labelled set. If none exists, build a tiny one (20–50 labelled queries) before changing anything.

---

## Example 3 — Small stable corpus

**User prompt:**
> "I have a 30-page company handbook. Help me set up a vector store for it."

**Expected behaviour:** Reject the premise. 30 pages fits comfortably in a system prompt with caching. Recommend prompt-only with `[[prompt-caching]]` instead.
