# Examples — agent-architecture-patterns

Three prompts that should trigger this skill, and how the agent's response should change because of it.

---

## Example 1 — Reflex toward multi-agent

**User prompt:**
> "I want three agents — one for retrieval, one for reasoning, one for summarising. They'll pass messages to each other. Help me wire it up in LangGraph."

**Expected behaviour (with skill):** The agent should *pause and challenge the decomposition* before producing code. It should note that retrieval + reasoning + summarising over shared state is a single-agent task with three tools, not three agents. It should ask the user about the **decision shape** (questions from the skill) before recommending an implementation.

**Without skill (failure mode):** The agent produces a LangGraph multi-agent skeleton because that's what was asked, baking in unnecessary cost, latency, and failure modes.

---

## Example 2 — Looping ReAct agent

**User prompt:**
> "My ReAct agent loops forever on ambiguous queries. How do I fix it?"

**Expected behaviour (with skill):** The agent should diagnose the pattern, not the prompt. It should ask whether there's a max-step cap *inside* the loop (not just at the edge), whether the budget check happens per step, and whether the task is actually a Plan-and-Execute shape being mis-implemented as ReAct.

**Without skill:** Generic advice about "improving the prompt" or "lowering temperature."

---

## Example 3 — Framework-first question

**User prompt:**
> "Should I use AutoGen or CrewAI for an agent that triages customer tickets?"

**Expected behaviour (with skill):** The agent should refuse to answer the framework question first. It should reframe: triage is a router or supervisor pattern; pick the pattern, then pick the framework that implements it cleanly. Then walk the decision flow.
