# Rubric Anchors — anchored examples per check

For each check, one **pass**, one **partial**, one **fail** example. The scorer compares the response under test to these anchors before assigning a score. Anchors are written terse — match the shape, not the literal words.

## `flags-no-agent-needed`

**Pass:**
> "You don't need an agent for this. `get_orders(customer_id) -> List[Order]` is a typed tool call. Wrap it as a function and call it directly. Reach for an agent only when the path isn't knowable up front."

**Partial:**
> "An agent might be overkill here. You could probably get away with a single function call, but if you want to use LangGraph it'll still work."

**Fail:**
> "LangGraph is a good choice for this. You'll define a node that fetches orders and returns them. Here's the basic graph structure..."

---

## `recommends-pattern-by-decision-shape`

**Pass:**
> "Pick the pattern from the decision shape. Your task has a knowable path (parse → fetch policy → draft → verify). That's Plan-and-Execute, not ReAct, and not multi-agent. ReAct would burn tokens re-deciding what's already deterministic; multi-agent would split a single decision into four. Framework comes after the pattern; LangGraph and Swarm can both implement Plan-and-Execute."

**Partial:**
> "Plan-and-Execute might fit. ReAct could also work depending on the task. Either should be doable in LangGraph."

**Fail:**
> "AutoGen and CrewAI are both good — try CrewAI for its multi-agent abstractions."

---

## `flags-multi-agent-for-parallelism`

**Pass:**
> "These aren't agents — they're parallel tool calls. Three 'agents' that fetch from different APIs with the same prompt, same context, same model = concurrent tool calls inside one agent. Multi-agent here adds handoff overhead with no upside. Collapse to one agent with three tools called in parallel."

**Partial:**
> "You might be able to consolidate these into fewer agents. Multi-agent overhead is a thing."

**Fail:**
> "CrewAI's parallel-agent execution is well-suited for this. Define each agent with its own role and tool, and the crew handles concurrency."

---

## `flags-unbounded-loop`

**Pass:**
> "'Be efficient' in the system prompt isn't a cap. ReAct loops need two enforcement points: `max_steps` in the controller (hard cap, code, not prompt) and a per-task budget check *inside* the loop (cost, tokens, wall-clock). Without both, one runaway task drains the budget for the day. Prompt-level instructions are advisory; controllers enforce."

**Partial:**
> "Add a max-steps cap to your agent loop. Something like 10 should be fine."

**Fail:**
> "The new prompt instruction should help. Also consider increasing the model size — bigger models tend to converge faster."

---

## `flags-freeform-agent-chat`

**Pass:**
> "Researcher → analyst → critic loops to 'consensus' are token bonfires that rarely converge. Replace with **Reflexion**: actor (analyst) emits a thesis, critic emits structured critique, actor revises once or twice — hard iteration cap (≤3). Or **Supervisor**: coordinator owns state, dispatches researcher, analyst, critic as workers; workers return typed results and do not talk to each other."

**Partial:**
> "The agents might be talking too much. Try improving their prompts so they reach consensus faster."

**Fail:**
> "CrewAI's process model handles this well — define their roles and goals, and the crew will coordinate the back-and-forth."

---

## `flags-shared-mutable-memory`

**Pass:**
> "Shared scratchpad between concurrent agents is context-poisoning by design. Replace with explicit typed handoff: each agent emits a structured message; a supervisor owns the canonical state and dispatches updates. Agents are stateless from each other's POV. Don't add locks; remove the shared state."

**Partial:**
> "You'll need to coordinate writes to the scratchpad. Maybe add locks or a queue."

**Fail:**
> "Use file locking on the scratchpad and have the agents read-then-write atomically."

---

## `demands-eval-before-architecture`

**Pass:**
> "Stop. No eval = no architecture decision. Before any pattern, framework, or model choice: ≥20 representative inputs in a golden set, trace logging on every step, regression check on every prompt or graph change. Otherwise you're picking architecture by vibes and won't notice regressions. 'We'll add eval next sprint' is how regressions ship."

**Partial:**
> "An eval would be helpful before deciding. Consider building one in parallel."

**Fail:**
> "Architecture looks clean. LangGraph is a good choice; ship it and iterate."
