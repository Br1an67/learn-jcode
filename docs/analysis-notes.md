# Analysis Notes

## Course Style

This course should read like an engineer walking through source with another engineer.

- Start with a mental model, not installation.
- Use one runtime mechanism as the anchor for each lesson.
- Put core code excerpts directly in the lesson instead of sending readers to a file list.
- Use Mermaid for state flow and ownership boundaries.
- End each lesson with what the reader should be able to explain, not a separate task area.

## JCode Subject Model

JCode should be taught as a coding-agent harness, not as a generic chatbot framework.

Core identity:

- Rust-based performance-first harness.
- Single server, multiple clients, persistent sessions.
- Rich terminal UI with side panels, diagrams, info widgets, and custom rendering.
- Broad provider support, including OAuth/subscription-backed flows and OpenAI-compatible endpoints.
- Large built-in tool registry: file tools, shell, browser/web, MCP, memory, session search, subagent, batch, swarm, ambient, side panel, self-dev.
- Non-blocking semantic memory and graph-oriented memory design.
- Swarm coordination for multi-session/multi-agent collaboration.
- Self-dev mode for improving JCode from inside JCode.

## Differentiation Angle

JCode is not the smallest harness and not only a clone of Claude Code. Its differentiator is the combination of performance, server residency, memory, and native multi-session coordination.

Comparison framing:

- pi-mono: minimalist TypeScript harness. Four core tools, extensibility through packages/skills/extensions, simple to understand and modify.
- OpenCode: open-source provider-agnostic coding agent with client/server architecture, strong TUI and LSP direction, configurable agents and permissions.
- Claude Code: polished proprietary reference for harness design. The tutorial can compare public behavior and concepts, but should avoid using or reproducing leaked/proprietary source code.
- JCode: Rust implementation optimized for low latency, low memory growth per extra session, persistent server lifecycle, semantic memory, ambient work, and built-in swarm coordination.

## Tutorial Shape

The first README draft was too close to an architecture guide and too synthetic in tone. The revised tutorial should be direct, source-grounded, and paced over several days.

- Start from harness engineering: the model acts; JCode provides tools, context, permissions, runtime, and observability.
- Do not force a one-day promise. JCode is a long-running runtime, not a tiny demo.
- Avoid generic "AI documentation" tone. Write like engineering course notes: direct, opinionated, grounded in source snippets, and occasionally blunt.
- Keep comparisons tied to actual runtime decisions: pi for minimal path, OpenCode for open-platform direction, Claude Code only for public behavior boundaries.
- Keep bilingual README files complete enough to stand alone.

The repository should stay small and readable:

- `README.md`: Chinese main tutorial.
- `README-en.md`: English main tutorial.
- `docs/zh` and `docs/en`: complete lesson tracks.
- `mini/`: reduced mechanism specimens connected from the relevant lessons.
- `docs/analysis-notes.md`: source analysis and editorial decisions.
