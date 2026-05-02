[中文](./README.md) | [English](./README-en.md)

# Learn JCode 5.5

This is a JCode source-reading course for engineers. The tone is code walkthrough, not product brochure.

The reader is assumed to know roughly what an agent loop is, but not yet how a product-grade coding-agent harness is built. You are not here to read feature praise; you are here to understand why JCode needs a server, tool registry, provider layer, sessions, TUI, memory, and swarm runtime.

Writing rules live in [docs/writing-style.md](./docs/writing-style.md). New lessons should follow that guide.

## Who This Is For

This is for readers who already know roughly what an agent loop is and want to understand:

- Why does a coding agent need a resident server?
- How does a tool result return to model context?
- Why do provider, auth, and session layers get complicated?
- Why is TUI part of the harness instead of decoration?
- What problems do memory, swarm, ambient, and self-dev solve?
- How is JCode different from pi, OpenCode, and Claude Code?

If agents are completely new to you, read `Learn-OpenClaw` or pi-mono first, then come back to JCode.

## Project Structure

```text
learn-jcode-5.5/
├── README.md                 # Chinese entry
├── README-en.md              # English entry
├── docs/
│   ├── zh/                   # Chinese lesson docs
│   │   ├── README.md
│   │   ├── s01-harness-mindset.md
│   │   ├── s02-startup-server.md
│   │   ├── s03-agent-loop.md
│   │   ├── s04-tool-system.md
│   │   ├── s05-provider-session.md
│   │   ├── s06-tui-observability.md
│   │   └── s07-memory-swarm-selfdev.md
│   ├── en/                   # English lesson docs
│   │   ├── README.md
│   │   ├── s01-harness-mindset.md
│   │   ├── s02-startup-server.md
│   │   ├── s03-agent-loop.md
│   │   ├── s04-tool-system.md
│   │   ├── s05-provider-session.md
│   │   ├── s06-tui-observability.md
│   │   └── s07-memory-swarm-selfdev.md
│   ├── analysis-notes.md     # Writing notes and reference-project analysis
│   ├── project-structure.md  # Why the repository is organized this way
│   ├── sources.md            # Local source repositories and revisions
│   └── writing-style.md      # Writing tone and banned expressions
└── .gitignore
```

This repository does not currently copy `learn-claude-code`'s `agents/` example directory. That is intentional: this course is not building a toy agent from scratch; it is reading JCode itself. If we add practice code later, it should probably live under `labs/`, not in an unrelated miniature agent implementation.

## Lessons

Read in order, one or two lessons per day.

| Lesson | 中文 | English |
| --- | --- | --- |
| s01 | [Harness 心智](./docs/zh/s01-harness-mindset.md) | [Harness Mindset](./docs/en/s01-harness-mindset.md) |
| s02 | [启动链路和常驻 Server](./docs/zh/s02-startup-server.md) | [Startup and Resident Server](./docs/en/s02-startup-server.md) |
| s03 | [Agent Loop](./docs/zh/s03-agent-loop.md) | [Agent Loop](./docs/en/s03-agent-loop.md) |
| s04 | [工具系统](./docs/zh/s04-tool-system.md) | [Tool System](./docs/en/s04-tool-system.md) |
| s05 | [Provider、Auth、Session](./docs/zh/s05-provider-session.md) | [Provider, Auth, Session](./docs/en/s05-provider-session.md) |
| s06 | [TUI 和可观察性](./docs/zh/s06-tui-observability.md) | [TUI and Observability](./docs/en/s06-tui-observability.md) |
| s07 | [Memory、Swarm、Ambient、Self-Dev](./docs/zh/s07-memory-swarm-selfdev.md) | [Memory, Swarm, Ambient, Self-Dev](./docs/en/s07-memory-swarm-selfdev.md) |

## Suggested Pace

Do not treat JCode as a one-day cram project.

```text
Day 0: run it and authenticate one provider
Day 1: read startup and server/client
Day 2: read the agent loop
Day 3: read the tool registry
Day 4: read provider/auth/session
Day 5: read TUI and observability
Day 6: read memory/swarm/ambient/self-dev
```

This is not a strict schedule. The point is: do not skip the first four lessons and jump straight into swarm or self-dev. You will collect names without understanding runtime boundaries.

For a real project, pick one small modification:

- Add a read-only tool, such as `repo_summary`.
- Write OpenAI-compatible provider profile setup and smoke-test docs.
- Build a side-panel workflow.
- Write a source-level comparison of JCode / OpenCode / pi.
- Document a real memory/session-search use case.

## Local Sources

This tutorial is based on local reading of:

- JCode: `/Users/shizi/Documents/workspace/jcode`
- learn-claude-code: `/tmp/learn-claude-code`
- Learn-OpenClaw: `/tmp/Learn-OpenClaw`
- pi-mono: `/Users/shizi/Documents/workspace/pi-mono`
- OpenCode: `/Users/shizi/Documents/workspace/opencode`

Exact revisions are listed in [docs/sources.md](./docs/sources.md).

For Claude Code, this tutorial compares public behavior and harness design ideas only. It does not use, distribute, or summarize non-public or leaked source code.
