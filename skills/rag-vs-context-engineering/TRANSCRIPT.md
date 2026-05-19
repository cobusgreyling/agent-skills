# Transcript — rag-vs-context-engineering

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "I'm building a chatbot that answers questions about our internal HR policies. I'm going to embed all the policies into a vector DB and use RAG. Anything I should watch for?"

---

## Without skill (typical baseline)

> Sounds reasonable. A few things to watch for:
>
> - Choose a good chunking strategy (semantic chunking often beats fixed-size).
> - Use a strong embedding model.
> - Consider a reranker for the top-k results.
> - Add prompt-injection mitigations for retrieved content.
> - Test with real user questions.
>
> You might also want to add hybrid retrieval (BM25 + embeddings) for better recall on keyword-heavy queries.

Sensible RAG checklist. Never questions whether RAG is the right pattern.

---

## With skill (behavioural expectation)

> Before we talk chunking and embeddings — let me question the pattern.
>
> RAG is one tool in context engineering, not the whole job. Walking the decision flow for your case:
>
> 1. **Does the answer live in a known, small, stable document?** HR policies are usually <500k tokens total, change rarely, and are version-controlled. If you fit in **prompt-only** (load the policy doc into a cached system prompt), you skip the entire retrieval stack. Latency drops, cost drops with caching, debugging trivialises. **Try this first.**
>
> 2. **Does the answer live in a structured store?** Some HR data is in HRIS systems (leave balances, salary, manager). For those, **tool-call retrieval** with a typed query beats embedding tabular data. Two patterns coexisting in one agent.
>
> 3. **Is the corpus large/unstructured AND queries semantic?** Policies tend to be the latter only in big orgs (thousands of pages, edge-case clauses). Then RAG. But the eval is on **retrieval first** (recall@k on a labelled set), not answer quality.
>
> So the answer to "anything I should watch for" is mostly: **don't reach for RAG yet**. Try prompt-only with a cached policy doc. If it underperforms on a small eval set, escalate.
>
> If you do end up needing retrieval, anti-patterns I'd flag:
>
> - **Chunk-and-pray** — fixed-size chunks straddle the answer half the time. Use structural chunking (heading-aware) or RAPTOR.
> - **Embeddings without rerank** — top-k by cosine alone is a baseline, not a system. Hybrid (BM25 + embed) + rerank is the production default.
> - **RAG over a structured DB** — never embed rows; let the model write a query.
> - **Single-stage retrieval for multi-hop** — "what is policy X under condition Y" needs two passes.
> - **No retrieval eval** — recall@k on a labelled set of 30+ Q→relevant-doc pairs. Without it, you're tuning vibes.
> - **Refresh-everything-nightly** when 1% changes. Incremental indexing exists.
>
> Six questions:
>
> 1. **Corpus shape** — structured, semi-structured, unstructured?
> 2. **Corpus size in tokens**, not documents?
> 3. **How fresh does the answer need to be?** Policies usually: days. HRIS data: minutes.
> 4. **Query shape** — factoid, multi-hop, summarisation, action?
> 5. **Per-user (tenant-scoped) or global?**
> 6. **What does a wrong answer cost** — annoyance, money, legal exposure?
>
> **Hard line:** show me your retrieval evals before you show me your embeddings. Recall@k on a labelled set is the only honest signal.

---

## The diff

What changed because the skill fired:

- **Refused to default to RAG** without walking the decision flow.
- **Surfaced prompt-only as the likely-right answer** for HR policies.
- **Named two patterns coexisting** (prompt-only + tool-call to HRIS).
- **Listed retrieval anti-patterns** specifically, with the production default (hybrid + rerank).
- **Asked corpus-shape and query-shape questions** before any code.
- **Invoked the hard line** on retrieval evals before embedding work.

A naive answer optimises RAG. A skilled answer questions whether RAG is the right pattern at all.
