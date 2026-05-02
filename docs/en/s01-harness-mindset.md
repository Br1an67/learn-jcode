# s01 - Harness Mindset

## The Point

JCode is not a "chat wrapper written in Rust." It is a coding-agent harness.

This has to be clear before you read the source. Otherwise, a lot of the repository will look unrelated to LLMs: server, socket, TUI, OAuth, provider catalog, session journal, memory, MCP, swarm, reload. These are not side quests. They are the harness.

## Agent vs Harness

This follows the core stance from `learn-claude-code`: the model is the agent. The model decides what to do next. The surrounding code provides the environment.

```text
Agent product = Model + Harness

Harness = Tools
        + Context
        + Runtime
        + UI
        + Storage
        + Permissions
        + Provider integration
        + Memory
```

For a coding agent:

- Tools are the hands: read files, write files, edit files, run commands.
- Context is the eyes: messages, file snippets, logs, diffs, tool results.
- Runtime is the body: processes, server, sessions, background tasks.
- UI is the cockpit: streaming output, tool status, diffs, side panels.
- Storage is recovery: session history, journals, config, accounts.
- Permissions are boundaries: which commands can run and which files can be written.
- Provider integration is the engine adapter: Claude, OpenAI, Gemini, Copilot, OpenRouter, OpenAI-compatible endpoints.
- Memory is long-term experience: preferences, project facts, old session clues.

## Why JCode Is Worth Studying

If you only want the minimal agent loop, JCode is too large. Start with pi-mono or `Learn-OpenClaw`.

JCode is worth studying because it shows product-grade complexity:

```text
Toy agent:
LLM + tools + loop

Long-running coding-agent harness:
LLM + tools + loop
  + server
  + session
  + provider
  + auth
  + cache
  + compaction
  + memory
  + UI
  + permissions
  + coordination
  + recovery
```

That is the learning value.

## Relationship to Reference Projects

### Learn-OpenClaw

`Learn-OpenClaw` is better for quickly building agent intuition. It explains Node, Workflow, Agent, Tool, MCP, and Skill very directly.

This JCode course does not copy the one-day pacing, but it keeps the practical style: each lesson tells you which files to read, which questions to ask, and which exercise to do.

### learn-claude-code

`learn-claude-code` is valuable because its stance is clear: do not confuse prompt plumbing with agents; learn harness engineering.

This course keeps that stance. JCode is not code that makes a model intelligent. It is an environment that lets an already capable model act safely and persistently in a codebase.

### pi-mono

pi is valuable because it is small. It shows that `read/write/edit/bash` is enough to build a useful coding agent.

JCode is valuable because it is large. It shows what happens when the harness needs multi-provider support, sessions, memory, swarm, UI, and self-dev.

### OpenCode

OpenCode and JCode are both open-source coding agents with client/server thinking. OpenCode feels more like an open platform. JCode feels more like a high-performance local runtime.

## Exercise

Write 200-300 words answering:

```text
Why is JCode a harness, not the agent itself?
```

Requirements:

- Mention the boundary between model and harness.
- Mention at least 4 JCode harness components.
- Do not write marketing copy. Write your own understanding.
