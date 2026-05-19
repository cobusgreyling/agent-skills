# Transcript — model-routing

> Side-by-side **behavioural exemplar**: how a realistic prompt is handled by a typical coding agent **without** this skill loaded, vs **with** it loaded. Composite responses representative of patterns observed in production triage, not a single literal model run.

---

## Prompt

> "Our document-processing agent uses Claude Opus end-to-end. Each document goes through: extract metadata → classify type → summarise → answer follow-up questions. Spending $25k/month. Want to cut cost. Should I just switch to Haiku?"

---

## Without skill (typical baseline)

> Switching to Haiku will definitely cut cost — usually 10–20× cheaper than Opus. The risk is that Haiku is weaker on complex reasoning, so test on a representative sample first. If Haiku is good enough on your workload, the savings are huge. If not, try Sonnet as a middle ground.

Treats model choice as a single decision across the whole pipeline. Misses the per-call lever.

---

## With skill (behavioural expectation)

> Wrong framing. You don't have *a* model decision; you have four, and they aren't the same call.
>
> Decompose:
>
> | Call | What it does | Right tier (default) |
> |---|---|---|
> | Extract metadata | Structured output from a known shape | Cheap (Haiku / mini / Flash) |
> | Classify type | Closed-set classification | Cheap |
> | Summarise | Abstractive, mid-complexity | Mid (Sonnet) |
> | Answer follow-ups | Open-ended reasoning over the doc | Mid → Strong (Sonnet, escalate to Opus on confidence drop) |
>
> Two of four calls are almost certainly fine on the cheapest tier. The summariser is a Sonnet job. Only the follow-up answerer plausibly needs Opus, and only sometimes.
>
> Concretely:
>
> 1. **Extraction:** Haiku, `temperature=0`, structured output schema. Validate the schema; on validation failure, escalate to Sonnet (rare). Saves ~95% on this call.
> 2. **Classification:** Haiku with an enum-typed output. Same escalate-on-fail pattern. Saves ~95%.
> 3. **Summarisation:** Sonnet. Evaluate with a held-out summary eval before switching — Haiku often regresses subtly here.
> 4. **Follow-up Q&A:** Sonnet by default. Confidence-based escalation to Opus: if Sonnet returns "I don't know" or a confidence signal below threshold, retry on Opus. Calibrate the threshold against your eval.
>
> Routing rules:
>
> - **The router itself is cheap.** A regex or a single Haiku call to classify the incoming task. Not an Opus call.
> - **Cheap-first + verify.** Run the cheap model; check the output (schema validation, classifier, second-model judge); escalate on fail.
> - **Per-tier eval.** Before routing, you need numbers — does Haiku pass extraction at ≥98%? Does Sonnet pass summarisation? Don't guess.
> - **No hard-coded model names.** Wrap behind `route(task) -> model`. Models change quarterly.
> - **Re-tune sampling per tier.** Temperature and top-p that work on Opus may not on Haiku. Tier swap is a behaviour change.
>
> Anti-patterns I'm watching for:
>
> - **Opus everywhere** (your current state).
> - **Haiku everywhere** (the naive fix you proposed).
> - **Cascade without a confidence signal** — "rerun on the bigger model if the answer looks bad" is folklore.
> - **Routing by trend** ("Sonnet is the hot model right now"). Eval picks the tier.
> - **Same prompt, different model.** Different tiers need different prompts; re-test the system prompt per tier.
> - **No measurement.** Routing decisions without an eval regress silently.
>
> Six questions:
>
> 1. What's the **per-call acceptance criterion** for each of the four calls? (Schema validity? Semantic match? Human grade?)
> 2. What's the **failure cost** per call — free, expensive, unrecoverable?
> 3. Do you have an **eval per call type**? Build it before routing.
> 4. What's the **latency budget** per call — does TTFT matter?
> 5. Is the router **fast and cheap**? It should be.
> 6. Can you **trace the route decision** per call so regressions are debuggable?
>
> Likely realistic outcome on your workload: 60–80% cost cut, no quality regression, two days of eval work to get there.
>
> **Hard line:** no routing decision without an eval. No tier choice without a per-call cost target.

---

## The diff

What changed because the skill fired:

- **Refused the single-model framing.** Decomposed the pipeline into four routing decisions.
- **Assigned a tier per call** with explicit reasoning (task type → tier).
- **Imposed cheap-first + verify** as the default cascade.
- **Required per-tier eval before changing anything.**
- **Wrapped the router** as an abstraction, not a hard-coded model name.
- **Surfaced sampling and prompt re-tuning** as part of any tier swap.
- **Quantified the realistic savings range** with the caveat that the eval must agree.

A naive answer swaps the model. A skilled answer rejects the framing, decomposes the pipeline, demands measurement, and proposes a router with explicit escalation.
