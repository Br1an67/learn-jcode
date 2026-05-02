# s07 - Memory, Swarm, Ambient, Self-Dev

## Goal

Read the most distinctive and easiest-to-get-lost parts of JCode.

Do not start by changing code here. Read docs, draw diagrams, and confirm runtime boundaries first.

These modules are easy to turn into a pile of nouns. Read each one with one question: which concrete weakness of a single-agent loop does it address?

## Memory

Read:

```text
docs/MEMORY_ARCHITECTURE.md
docs/MEMORY_BUDGET.md
src/memory.rs
src/memory_agent.rs
src/memory_graph.rs
src/memory_prompt.rs
src/tool/memory.rs
src/tool/session_search.rs
```

JCode memory is not "manually save a note." It is closer to automatic recall:

```text
current context
  -> embedding
  -> similar memories
  -> graph / cascade retrieval
  -> optional sidecar verification
  -> inject memory prompt in next turn
```

The key design is non-blocking:

```text
turn N triggers retrieval
turn N+1 uses the result
```

This keeps the main agent responsive.

The cost is a one-turn delay. That delay is intentional, not a missing synchronous retrieval step.

## Swarm

Read:

```text
docs/SWARM_ARCHITECTURE.md
src/server/swarm.rs
src/server/swarm_channels.rs
src/server/comm_*.rs
src/tool/communicate.rs
src/tool/task.rs
```

JCode swarm is not a normal subagent. It is concerned with multi-agent runtime coordination:

- how a coordinator assigns work
- how workers report back
- how agents DM / broadcast / use channels
- which files were read or modified by whom
- how plans update
- how blocked / failed / crashed agents recover
- when worktrees help and when they do not

This is where JCode differs strongly from pi. pi is restrained; JCode is more aggressive.

Do not read swarm as "open several subagents." The hard parts are plan ownership, communication, file touches, state recovery, and integration boundaries.

## Ambient

Read:

```text
docs/AMBIENT_MODE.md
src/ambient/
src/ambient_runner.rs
src/tool/ambient.rs
```

Ambient is a background agent. Instead of responding only to user prompts, it can do maintenance when resources allow:

- clean up memory
- inspect recent sessions
- check git activity
- perform low-risk proactive tasks
- decide when to wake next

This is experimental, but important because it points toward long-running agent environment maintenance.

When reading ambient, watch resource limits. A background agent without budget and priority rules becomes another source of interference.

## Self-Dev

Read:

```text
src/cli/selfdev.rs
src/tool/selfdev.rs
src/prompt/selfdev_mode.txt
src/prompt/selfdev_hint.txt
docs/UNIFIED_SELFDEV_SERVER_PLAN.md
```

Self-dev lets JCode modify itself.

Be conservative:

- Create a branch.
- Keep the worktree clean.
- Commit each step.
- Start with small changes.
- Run `cargo check`.
- Do not start with provider, server reload, compaction, or swarm.

## Judgments to Keep

These modules cover weaknesses of a single-agent loop:

```text
Memory: one context cannot remember long-term preferences and project facts, so JCode uses non-blocking recall.
Swarm: one agent is slow on large tasks and pollutes context, so JCode adds server-level coordination.
Ambient: users will not explicitly ask for every memory cleanup or recent-work check, so JCode has a background cycle.
Self-dev: JCode itself can be modified, but branch, commit, and cargo check are the guardrails.
```

Keep the risks with the benefits: memory has one-turn delay; swarm adds planning and communication complexity; ambient without resource limits becomes interference; self-dev changing reload or server state can lose running-session state.
