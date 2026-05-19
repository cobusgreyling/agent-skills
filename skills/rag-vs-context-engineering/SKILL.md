---
name: rag-vs-context-engineering
description: >-
  Decide between RAG, long-context, structured tool retrieval, and prompt-only
  approaches for grounding an LLM in private or fresh data. Use when the user
  is designing a knowledge-grounded agent or chatbot and mentions RAG, vector
  search, embeddings, retrieval, chunking, long context, context window, tool
  retrieval, hybrid search, rerank, or asks "do I need RAG?" / "should I just
  use a big context window?".
tags:
  - rag
  - retrieval
  - context-engineering
  - architecture
---

# RAG vs. Context Engineering

Retrieval is one tool in context engineering, not the whole job.

Most "RAG problems" are actually context-engineering problems: wrong granularity, wrong source, wrong ordering, wrong refresh policy. Picking RAG before you've decided what context the model actually needs is putting the engine before the chassis.

## When to use this skill

- The user is sketching a knowledge-grounded agent and reaches for embeddings reflexively.
- The user is debugging "the model gives wrong answers" and has not measured retrieval quality independently.
- The user is choosing between RAG, long-context-stuffing, structured tool calls, or fine-tuning.
- The user is mid-build and asking why their RAG isn't working.

## Decision flow

1. **Does the answer live in a known, small, stable document?** → no retrieval. Put it in the system prompt. Cache the prefix.
2. **Does the answer live in a structured store (DB, API, spreadsheet)?** → not RAG. Give the model a **typed tool** to query it. Schemas beat embeddings for structured data.
3. **Does the answer live in a corpus that fits the context window after filtering on a cheap signal (date, tag, user-id)?** → load the filtered subset directly. Retrieval is overkill.
4. **Is the corpus large, unstructured, and the query semantic?** → **RAG**. But measure retrieval quality before measuring answer quality.
5. **Is freshness critical (minutes, not days)?** → tool-call retrieval at query time, not a pre-indexed embedding store.
6. **Is the relevant context interactive (chat history, scratchpad, ongoing task)?** → working memory, not retrieval. Manage it explicitly.

## The patterns in one line each

- **Prompt-only** — put the knowledge in the system prompt. Fastest, cheapest, easiest to debug.
- **Structured tool retrieval** — model issues a typed query against a real backend. The right answer for structured data.
- **Filtered context load** — pull the candidate set by metadata, hand the model the whole filtered slice.
- **Embedding RAG** — semantic chunk search. Right answer for unstructured semantic queries over large corpora.
- **Hybrid retrieval** — embeddings + lexical (BM25) + rerank. Default to this when embedding RAG underperforms.
- **Long-context-stuffing** — dump the corpus into the prompt. Works for ≤200k-token corpora; fails on cost and latency at scale.
- **Fine-tuning** — only when the task is a *style* or *format* the base model can't produce; never as a substitute for retrieval.

## Anti-patterns to flag immediately

- **Chunk-and-pray.** Fixed-size chunks with no structural awareness; the answer always straddles two chunks.
- **Embeddings without rerank.** Top-k by cosine alone is a baseline, not a system.
- **RAG over a structured database.** Embedding rows is almost never better than letting the model write a query.
- **Dumping the whole DB into the context.** Cheap until it isn't — and silently degrades the model's attention to what matters.
- **Single-stage retrieval for multi-hop questions.** If the query needs evidence A *and* B, one retrieval pass will miss one of them.
- **No retrieval eval, only answer eval.** You can't fix what you can't isolate.
- **Refreshing the whole index nightly when only 1% changes.** Incremental indexing exists.

## Questions to ask the user

1. What is the **corpus shape** — structured (rows, columns), semi-structured (markdown, JSON), or unstructured (PDFs, transcripts)?
2. What is the **corpus size** in tokens, not documents?
3. How fresh does the answer need to be?
4. What is the **query shape** — factoid, multi-hop, summarisation, action?
5. Is the relevant context **per-user** (tenant-scoped) or global?
6. What does a **wrong answer** cost — annoyance, money, legal exposure?

If you can't answer (1) and (2), you cannot pick a retrieval strategy. Stop and measure.

## The hard line

**Show me your retrieval evals before you show me your embeddings.** Recall@k on a labelled set is the only honest signal. Without it, you're tuning vibes.

## Why this exists

Most "RAG isn't working" complaints in the wild are misdiagnosed retrieval problems hidden under prompt tweaking. Naming the layers — corpus, retrieval, context assembly, generation — lets you debug them independently and pick the right pattern instead of the trendy one. See [link to article on context engineering].

## References

- `references/retrieval-patterns.md` — when each pattern wins, with worked examples.
- `references/retrieval-evals.md` — recall@k, MRR, and how to build a labelled set without months of work.
- `references/chunking.md` — structural chunking, overlap, and metadata.
