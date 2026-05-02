# Analysis Notes

## Tutorial Style To Reuse

`learn-claude-code` uses a strong thesis first: agent capability comes from the model, while product quality comes from the harness. It then teaches one harness mechanism per lesson. The useful pattern is:

- Start with a mental model, not installation.
- Use one simple loop or formula as the anchor.
- Add progressive lessons with a motto for each mechanism.
- Keep the conclusion project-oriented: what can the reader build after learning this?

`Learn-OpenClaw` uses a practical beginner path. It compresses agent concepts into a one-day roadmap, explains terms bluntly, and tells readers what to read or build for job/interview readiness. The useful pattern is:

- Give time estimates.
- Prefer small examples over exhaustive theory.
- Explain Tool, MCP, Skill, Memory, Multi-Agent in plain terms.
- Tie learning to a concrete project path.

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

The repository should stay small and readable:

- `README.md`: Chinese main tutorial.
- `README-en.md`: English main tutorial.
- `docs/analysis-notes.md`: source analysis and editorial decisions.
- Optional future docs can split lessons, but for this request the two main READMEs should be complete enough to stand alone.
