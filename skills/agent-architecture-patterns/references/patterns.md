# Patterns — full briefs

Each entry: shape, when to pick it, when it fails, minimal sketch.

---

## ReAct

**Shape.** One agent, one loop: `thought → action → observation → thought → ...` until the agent emits a final answer.

**Pick when.** The path is not knowable up front. The task fits in a small step budget (typically <10). Tools are cheap and idempotent.

**Fails when.**
- The task is long (>20 steps). The agent forgets earlier context and starts looping.
- A tool is expensive or has side effects. Cost compounds.
- The model is small. ReAct is parser-fragile on weaker models.

**Sketch.**
```
loop:
  thought, action = model(prompt + history)
  if action == FINISH: return thought
  observation = run(action)
  history.append(thought, action, observation)
  if step > MAX_STEPS or budget_exceeded: abort
```

**Knobs that matter.** `MAX_STEPS`, per-step timeout, observation truncation, tool whitelist per step.

---

## Plan-and-Execute

**Shape.** Planner produces a typed plan once. Executor runs steps. Optional re-planner triggers on step failure.

**Pick when.** The task decomposes cleanly and the world is stable across the plan's lifetime. Long horizons (>10 steps). You need to show the plan to a human before execution.

**Fails when.**
- The world changes between planning and step N (e.g. market data, file state). Plan goes stale.
- Steps have data dependencies the planner couldn't see. Cascading replans.
- The planner is over-confident. Plans that look good but skip a required step.

**Sketch.**
```
plan = planner(task)              # list of typed steps
for step in plan:
  result = executor(step, state)
  state.update(result)
  if result.failed and replans < CAP:
    plan = replanner(task, state, failure=result)
    replans += 1
return state.final
```

**Knobs that matter.** Plan schema (free text plans are useless), replan cap, per-step retry, plan-vs-state divergence check.

---

## Reflexion (Critic-Actor)

**Shape.** Actor produces an attempt. Critic scores it against a rubric. Actor revises using critic feedback. Loop until pass or cap.

**Pick when.** Quality matters more than latency. The task has a checkable rubric (code that compiles, JSON that validates, an answer with citations). You can afford 2–4× the tokens.

**Fails when.**
- The rubric is vague — critic confabulates issues, actor "fixes" non-problems.
- No cap — infinite politeness loops.
- Critic and actor are the same model with the same prompt. They will agree.

**Sketch.**
```
attempt = actor(task)
for i in range(MAX_REVISIONS):
  verdict = critic(task, attempt)
  if verdict.passes: return attempt
  attempt = actor(task, prior=attempt, feedback=verdict)
return attempt  # best effort
```

**Knobs that matter.** Concrete rubric, revision cap, asymmetric models (a stronger critic catches more), explicit failure mode if cap hit.

---

## Router

**Shape.** A classifier picks one downstream skill per turn. No state shared between turns by the router itself.

**Pick when.** You have ≥3 disjoint skills (SQL, code-gen, search, summarization) and each turn cleanly belongs to one.

**Fails when.**
- The router is also doing execution. Separate them.
- Skills overlap — input matches two. Add a fall-through skill or merge.
- The classifier is unconfident. Log routing decisions and audit weekly.

**Sketch.**
```
skill = classifier(message, skills_catalog)
return skill.handle(message)
```

This is not a multi-agent system. It's a typed dispatcher with an LLM as the switch.

---

## Supervisor

**Shape.** Coordinator owns the conversation and state. Workers are stateless, single-purpose, called by the supervisor with explicit inputs and return values.

**Pick when.** Multiple workers must contribute to one task, with shared state the supervisor is responsible for. Workers have different tools / prompts / models.

**Fails when.**
- Workers talk to each other directly. You've reinvented chaos.
- Supervisor's prompt is doing too much. Split into planner + dispatcher.
- State grows unbounded. Compact between worker calls.

**Sketch.**
```
state = init(task)
while not done(state):
  next_worker, inputs = supervisor(state)
  result = workers[next_worker](inputs)
  state = update(state, result)
return state.output
```

**Knobs that matter.** Worker contract (typed inputs/outputs), state schema, termination predicate, supervisor-step cap.

---

## Hierarchical

**Shape.** Supervisors of supervisors. Top-level supervisor dispatches to sub-supervisors, each owning a worker pool.

**Pick when.** You genuinely have team-of-teams structure (e.g. research team + writing team + review team) and you've already tried flat Supervisor and hit prompt-size or specialization limits.

**Fails when.** Almost always. Debuggability collapses, costs balloon, errors cross tiers and become untraceable.

If you reach for this, write down what the flat Supervisor failed at first. Most "hierarchical" designs are flat designs with worse logging.

---

## Swarm / Handoff

**Shape.** Peer agents. Each agent has a set of handoff tools that transfer control (and conversation state) to another agent.

**Pick when.** Role-shaped tasks: triage → specialist → escalation. The control path is bounded and the handoff graph is acyclic.

**Fails when.**
- Cycles in the handoff graph. Two agents bounce a task forever.
- Implicit termination — no agent owns "we're done".
- Context bloat — every handoff passes the full history.

**Sketch.** OpenAI Swarm's model: `Agent` objects with `functions = [transfer_to_other_agent]`. Runtime swaps the active agent on tool return.

**Knobs that matter.** Explicit terminal agent, max-handoff cap, context-summarization on handoff.
