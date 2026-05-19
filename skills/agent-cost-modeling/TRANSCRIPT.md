# Transcript — agent-cost-modeling

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "We're choosing between Sonnet and Opus for our support-ticket triage agent. Opus is 5× more expensive per token. Is it worth it?"

---

## Without skill (typical baseline)

> Opus is more capable but more expensive. Sonnet is usually 80–90% as good on reasoning tasks at a fraction of the cost. For triage, Sonnet is probably the right starting point unless you need the absolute best quality. I'd recommend running a benchmark on a sample of tickets to compare.
>
> Some factors to consider:
> - How complex are the tickets?
> - What's your accuracy bar?
> - How latency-sensitive is the use case?
>
> Most teams find Sonnet sufficient for triage. You can always upgrade specific cases to Opus via a routing step.

Generic price-list reasoning. No equation, no per-task number, no architecture question.

---

## With skill (behavioural expectation)

> Token-per-token price is the wrong unit. The unit is **cost per task**, and it has six terms — not two.
>
> Before I can answer "is Opus worth it", I need:
>
> 1. **Cost ceiling per task** (in dollars). Without this, every answer is a guess.
> 2. **Call graph per ticket.** How many model calls and tool calls per triage? If it's 1, model choice matters most. If it's 5+, architecture matters more than model.
> 3. **Token count per call** at p50 and p95. Triage prompts vary wildly — one with full ticket history is 8× one without.
> 4. **Cache hit rate.** If your system prompt is static and you serve 100 tickets/hour, you should be seeing 60%+ cache hits. Sonnet with caching beats Opus without.
> 5. **Retry rate.** Cost per *successful* task includes retries. If Sonnet retries 20% of the time and Opus retries 2%, the gap closes.
> 6. **Traffic shape.** 100/day or 100k/hour? At low volume, the question is irrelevant; at high volume, a 5× cost gap is a $50k/month decision.
>
> If I had to predict before the numbers: triage is a **routing/classification task**. Default to the smallest model that passes the eval. Reserve Opus for the 5% of tickets that fail the small-model eval. Two-tier routing usually beats one-tier-premium at half the cost and same quality.
>
> Architecture to consider:
>
> ```
> ticket → router (Haiku) → simple? → Sonnet (cached)
>                        → complex? → Opus (cached, rare)
> ```
>
> **Hard line:** no cost-per-task number, no production approval. A cost ceiling without measurement is a wish.

---

## The diff

What changed because the skill fired:

- **Refused price-list reasoning.** Reframed around cost per task, not per token.
- **Asked the six diagnostic questions** before recommending a model.
- **Surfaced caching** as a likely-bigger lever than model choice.
- **Proposed a routing architecture** instead of a model swap.
- **Named the cost-per-*successful*-task** subtlety (retries count).
- **Invoked the hard line** on measurement before approval.

A naive answer picks a model. A skilled answer reframes the question and finds the real lever.
