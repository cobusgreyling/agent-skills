# Failure Pattern Index

Each skill in this collection exists because a specific production failure pattern showed up at least three times. This index maps the failure → the skill that catches it. Browse here to find the brief that matches what just bit you.

> Failures are grouped by category. Within each category, failures are ordered by how often they show up in real triage.

## Architecture and orchestration

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **Multi-agent for parallelism** | 3+ "agents" that share prompt, tools, model — separated only because the framework had a "crew" abstraction. | [[agent-architecture-patterns]], [[multi-agent-orchestration]] |
| **Unbounded ReAct loop** | One stuck task burns 200k tokens; no in-loop budget check; "max_steps = 50" is the only cap. | [[agent-architecture-patterns]] |
| **Free-form agent-to-agent chat** | Round-robin "consensus" debate between roles; tokens burn; nothing converges. | [[multi-agent-orchestration]] |
| **Shared mutable memory across agents** | Two agents read/write the same scratchpad; race conditions in prod; context poisoning. | [[multi-agent-orchestration]], [[memory-design]] |
| **Mega-prompt doing routing + execution + reflection** | 8k-token system prompt with everything in it; impossible to debug, regresses silently. | [[agent-architecture-patterns]] |
| **Hierarchical-of-hierarchies as default** | Team-of-teams design where 1-3 agents would do; debuggability collapses. | [[multi-agent-orchestration]] |

## Cost and economics

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **Opus / GPT-5 / Pro everywhere** | Most-expensive tier on every call; bill 5×-10× what a routed deployment would pay. | [[agent-cost-modeling]], [[model-routing]] |
| **No cost ceiling** | Architecture decisions made without a per-task dollar target; debates loop forever. | [[agent-cost-modeling]] |
| **Cache-key poisoning** | `Today is {timestamp}` in system prompt; hit rate stuck at 0%; cost climbs. | [[prompt-caching]], [[context-window-hygiene]] |
| **Mutating tool list per call** | Tools reordered or filtered per call; cache hash changes every time. | [[prompt-caching]], [[tool-use-schema-design]] |
| **Cost-per-call as cost-per-task** | 30% failure rate not in denominator; reported cost is 30% understated. | [[agent-cost-modeling]] |
| **Tool-result bloat** | 30KB JSON in conversation history; cost grows quadratic-ish across a long run. | [[context-window-hygiene]], [[tool-use-schema-design]] |
| **Counting only model cost** | Embeddings, retrieval, tool calls, observability not on the dashboard; "the bill" surprises. | [[agent-cost-modeling]] |

## Latency

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **No per-stage budget** | Total latency target exists; per-stage doesn't; can't tell where the slow is. | [[latency-budgeting]] |
| **No streaming on TTFT-sensitive paths** | User waits 4s for the first token; could stream at 200ms with same total. | [[latency-budgeting]] |
| **Slow tool blocks the whole run** | One flaky API hangs 30s; no timeout; whole agent looks dead. | [[tool-failure-handling]], [[latency-budgeting]] |
| **Approval gate adds 30 minutes** | HITL queue in critical path; no off-hours fallback. | [[human-in-the-loop]], [[latency-budgeting]] |

## Tools and structured output

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **Kitchen-sink tool** | `do_thing(action, payload)`; model picks `action`, serialises `payload`, fails. | [[tool-use-schema-design]] |
| **Free-text payload parameter** | `payload: object`; model invents fields; downstream breaks. | [[tool-use-schema-design]] |
| **JSON repair function** | 300 lines of regex fixing model output; native schema mode unused. | [[structured-output-reliability]] |
| **Blind retry on timeout** | Non-idempotent write retried; customer charged twice. | [[tool-failure-handling]] |
| **No idempotency key on writes** | Tool call retried; duplicate side effect; oncall paged. | [[tool-failure-handling]] |
| **Stringified errors to the agent** | `"AttributeError: ..."` returned as tool result; model can't recover. | [[tool-failure-handling]] |
| **No timeout per call** | One slow tool hangs the whole agent. | [[tool-failure-handling]] |
| **Untyped enum in description** | `priority: string` with "must be one of X, Y, Z" in description; model invents new values. | [[tool-use-schema-design]], [[structured-output-reliability]] |

## Safety and injection

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **Indirect injection via document** | RAG corpus contains adversarial content; agent follows embedded instructions. | [[prompt-injection-defense]], [[guardrails-and-safety]] |
| **"Type yes to confirm"** | In-chat confirmation gate; a document containing "yes" satisfies it. | [[human-in-the-loop]], [[prompt-injection-defense]] |
| **No server-side authorisation on tool calls** | Agent decides; service executes without policy check; one prompt = one wrong action. | [[guardrails-and-safety]], [[prompt-injection-defense]], [[tool-use-schema-design]] |
| **System prompt as the entire defence** | "Be safe and refuse bad requests"; adversarial input ignores polite framing. | [[guardrails-and-safety]] |
| **No red-team set** | "We haven't seen abuse"; functional eval only; first incident wasn't novel. | [[guardrails-and-safety]] |
| **One model reads and acts on untrusted text** | No isolation between reader and decider; injection reaches actor as instructions. | [[prompt-injection-defense]] |
| **High-impact tool on every turn** | `delete_user` / `transfer_money` available in every context; no capability gating per source. | [[prompt-injection-defense]], [[human-in-the-loop]] |

## Memory and context

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **One vector store as "the memory"** | Conversation dumps into Pinecone; recalls stale chunks; agent acts confidently wrong. | [[memory-design]] |
| **Memory writes every turn** | Signal-to-noise collapses; old facts buried under restatements. | [[memory-design]] |
| **No memory TTL** | Preferences from 2 years ago still influence today; recall returns nostalgia. | [[memory-design]] |
| **Cross-user retrieval leakage** | User A's notes retrieved when agent is acting for User B. | [[memory-design]], [[prompt-injection-defense]] |
| **1M-context as a forgetting fix** | "Just use the bigger window"; cost balloons; middle-of-context recall still degrades. | [[context-window-hygiene]] |
| **Compaction at the cliff** | Hits 95% context, panics, summarises lossily — at the worst moment. | [[context-window-hygiene]] |
| **Tool results in history verbatim** | Raw HTML/JSON in conversation; every subsequent turn pays for it. | [[context-window-hygiene]] |
| **Free-text summary memory** | Summaries paraphrase facts into vagueness; precision drops over time. | [[memory-design]], [[context-window-hygiene]] |

## Evaluation

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **No eval, ship anyway** | "We'll add eval next sprint"; regression ships; nobody notices for a month. | [[agent-evaluation-harness]] |
| **Same-model self-judging** | GPT-4 grades GPT-4; 0.4 delta is self-preference, not quality. | [[llm-as-judge]] |
| **No position randomisation in pairwise** | A wins more than B because A is always first. | [[llm-as-judge]] |
| **Unanchored rubric** | "Rate 1-10 on helpfulness" with no examples; judge noise dominates signal. | [[llm-as-judge]] |
| **No judge-human agreement** | Reporting judge scores without validating the judge against humans. | [[llm-as-judge]] |
| **Eval drift on model upgrade** | Provider ships a new version; old eval baseline becomes meaningless overnight. | [[agent-evaluation-harness]], [[llm-as-judge]] |

## Observability

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **One span per agent run** | Whole loop collapses into one opaque event; can't replay failure. | [[agent-observability]] |
| **No input capture** | "Model said X" without "given what input" — story, not trace. | [[agent-observability]] |
| **Print-debugging only** | Works in dev; in prod with concurrency, useless. | [[agent-observability]] |
| **Sampling errors out** | "Only 10% of traces" — but errors are in the 90% you discarded. | [[agent-observability]] |
| **No cost-per-request attribution** | Monthly total only; per-feature cost is unknown; can't debug regressions. | [[agent-observability]], [[agent-cost-modeling]] |

## Human oversight

| Failure pattern | What it looks like | Skill |
|---|---|---|
| **Blanket "approve every action" gates** | After one incident, every action needs approval; throughput collapses; rubber-stamping starts. | [[human-in-the-loop]] |
| **Approval UI with no context** | Truncated preview, approve button; humans approve regardless. | [[human-in-the-loop]] |
| **Bottleneck queue** | All escalations to one person; queue grows; SLAs miss. | [[human-in-the-loop]] |
| **Chat-based escalation** | "I'll ping #ops"; pings get missed. | [[human-in-the-loop]] |
| **Compliance theatre HITL** | Gate exists, but nobody can actually act on it; checkbox, not control. | [[human-in-the-loop]] |

## How to read this index

- **Browsing by symptom**: scan the "what it looks like" column; click through to the brief.
- **Browsing by area**: skip to the category header relevant to what you're debugging.
- **Browsing by name**: every skill in the collection appears at least once; if a skill is here, it has a triage record.

If you've hit a failure pattern that isn't in this index, that's a candidate for a new skill — see [AUTHORING.md](./AUTHORING.md) and [CONTRIBUTING.md](./CONTRIBUTING.md).
