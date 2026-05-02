# Learn JCode 5.5 English Course

This directory contains the English lesson docs. The root README is only the entry point; read the course in this order.

The writing follows [../writing-style.md](../writing-style.md): source walkthrough, not marketing copy. Each lesson should answer three questions: which files to read first, what design tradeoff to notice, and what conclusion to keep.

Course map:

| Lesson | Topic | Goal |
| --- | --- | --- |
| [s01](./s01-harness-mindset.md) | Harness mindset | Understand the boundary between model and harness |
| [s02](./s02-startup-server.md) | Startup and resident server | Trace what happens after the `jcode` command starts |
| [s03](./s03-agent-loop.md) | Agent loop | Follow model output, tool calls, and tool results |
| [s04](./s04-tool-system.md) | Tool system | Understand how JCode gives tools to the model |
| [s05](./s05-provider-session.md) | Provider, auth, session | Understand how model platforms and long-running sessions connect |
| [s06](./s06-tui-observability.md) | TUI and observability | Understand why UI is part of the harness |
| [s07](./s07-memory.md) | Memory | Understand non-blocking memory sidecar design |
| [s08](./s08-swarm.md) | Swarm | Understand server-level multi-agent coordination |
| [s09](./s09-ambient-selfdev.md) | Ambient and self-dev | Understand background cycles and self-modification boundaries |

Read one or two lessons per day. JCode is not a good one-day cram project. If a module does not make sense yet, write down the question and move on; do not scan directories just to feel done.
