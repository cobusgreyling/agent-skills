# Frameworks — mapping patterns to libraries

Pick the pattern first. Then pick the framework. Not the other way around.

## LangGraph

Graph runtime: nodes are functions, edges are control flow, state is a typed dict.

- **ReAct** — `create_react_agent` or a two-node loop (`agent`, `tools`) with a conditional edge.
- **Plan-and-Execute** — three nodes: `planner`, `executor`, `replanner`. State carries `plan: list[str]` and `past_steps: list[tuple]`.
- **Reflexion** — `actor` and `critic` nodes with a conditional edge to either revise or finish. Cap with a counter in state.
- **Supervisor** — supervisor node returns the next worker's name; conditional edges fan to worker nodes; workers return to supervisor.
- **Hierarchical** — sub-graphs compiled as nodes inside a parent graph. Verify you actually need this.

State management is the biggest footgun: a state field that grows unboundedly across loop iterations will silently double cost every turn.

## AutoGen (Microsoft)

Conversation-centric. Agents exchange messages; an orchestrator decides who speaks next.

- **ReAct** — single `AssistantAgent` + `UserProxyAgent` with tool execution.
- **Supervisor** — `GroupChatManager` with role-typed agents. Pin the speaker-selection prompt or you get round-robin chatter.
- **Reflexion** — two-agent loop: writer + reviewer with an explicit termination message.

Watch for: free-form group chats are AutoGen's default and almost never what you want.

## CrewAI

Role-and-task abstraction over LangChain.

- **Plan-and-Execute** — `Crew` with `Process.sequential`. Each `Task` is a step.
- **Supervisor** — `Process.hierarchical` with a manager LLM.

CrewAI hides the control loop. Fine for prototypes, painful to debug at scale. If you need step-level traces, instrument before you grow past 3 tasks.

## OpenAI Swarm (experimental) / Agents SDK

Handoff-based. Each agent has tools, some of which return another `Agent`.

- **Swarm / Handoff** — native idiom.
- **Router** — single agent whose only tools are handoffs.
- **Supervisor** — possible but awkward; agents don't share state by default.

The new OpenAI Agents SDK is the supported successor; Swarm is reference code.

## Plain SDK (Anthropic / OpenAI)

Often the right answer. ReAct, Plan-and-Execute, Reflexion, and Router all fit in <300 lines of Python with no framework. You trade boilerplate for full control of state, logging, and retries.

Rule of thumb: if you can't sketch the control flow on a whiteboard, the framework is hiding bugs from you.
