# Glossary

This page fixes the vocabulary used across the course. Later lessons use these terms without redefining them every time.

## Core Terms

| Term | Meaning In This Course | Common Misread |
| --- | --- | --- |
| model | The LLM that makes decisions, behind providers such as Claude, OpenAI, or Gemini | JCode's own rule system |
| harness | The runtime around the model: tools, context, permissions, state, UI, storage | A prompt chain or workflow |
| agent loop | The repeated loop that sends messages to the model, handles tool calls, and appends tool results | A complex planner |
| runtime | Processes, state, and background tasks that let the agent loop run over time | One function call |
| resident server | JCode's local long-running server that owns sessions, providers, MCP, swarm, and events | A simple background proxy |
| TUI client | Terminal UI client that connects to the server and displays messages, tool state, diff, and widgets | The owner of all state |
| session | Long-running JCode conversation state: messages, journal, replay, compaction, render data | A text transcript array |
| journal | Append-only session event record used for recovery and replay | Normal logs |
| replay | Turning saved session/events back into state the agent can continue | Playing chat history |
| provider | Model-platform adapter that maps JCode messages/tools/system prompt to platform requests and streams back to `StreamEvent` | One API call |
| `StreamEvent` | JCode's normalized provider stream event: text delta, tool use, usage, error | Raw provider SSE |
| registry | Tool registration and execution center for definitions, allowed tools, aliases, telemetry, truncation | `HashMap<String, Tool>` |
| tool definition | Tool name, description, and JSON schema shown to the model | The tool implementation |
| tool result | Output from tool execution, fed into the next model turn | User-only display text |
| sidecar | Background component beside the main agent loop, such as the memory agent | A separate product or plugin |
| memory | Long-term recall system that retrieves in a sidecar and injects on the next turn | Manual notes or a basic RAG demo |
| pending memory | Memory prompt prepared by the sidecar and waiting for the main agent to pick up | Context active in the current turn |
| swarm | Server-level multi-agent coordination runtime: plan, worker, channel, heartbeat, report | Several subagents opened at once |
| coordinator | Swarm session that owns planning and integration | A smarter model |
| worker | Swarm session assigned to work, checkpoint, and report | A function call |
| channel | Server-maintained swarm communication subscription | A `#name` convention in prompt text |
| heartbeat | Worker activity signal written back to the server plan | UI animation |
| checkpoint | Intermediate progress summary from a worker | Final report |
| ambient | Background maintenance loop with budget and scheduler constraints | Infinite background agent |
| scheduler | Ambient wake-up and ordering logic | Another name for cron |
| self-dev | Controlled build/test/reload path where JCode modifies itself | Normal hot reload |
| canary | New self-dev version marked for testing before activation | Release version |
| reload handoff | New binary takes over the old server while preserving session continuity | Kill and restart |
| MCP pool | Server-owned pool of MCP connections that exposes external tools | One-off MCP call |
| side panel | Model-operable persistent page that can be written, appended, focused, deleted | Temporary TUI display |
| compaction | Compressing long history into state that can still be used | Plain summary |

## Boundaries To Keep

### Client And Server

The client handles interaction and display. The server owns long-lived state. Client exit does not mean session loss. This boundary explains sockets, reload, multi-client support, and server runtime.

### Provider And Agent Loop

The agent loop handles JCode messages and `StreamEvent`. The provider layer absorbs platform-specific request bodies, auth, streaming formats, and cache behavior. This prevents provider-specific branches from leaking into the turn loop.

### Tool Definition And Tool Execution

Definitions are for the model. Execution is for runtime. A real tool needs both schema and handler. Prompt text alone is not a tool; a handler alone is invisible to the model.

### Memory And Current Turn

The memory sidecar does not block the current turn. It writes pending memory, and the main agent injects it on the next turn. One-turn delay is a design choice, not a missing synchronous retrieval path.

### Subagent And Swarm

Subagent is closer to one-off delegation. Swarm is a long-running coordination scene. Swarm needs plan, channel, heartbeat, checkpoint, report, and recovery logic.

### Ambient And Self-Dev

Ambient maintains the environment. Self-dev modifies JCode itself. Ambient needs budget and scheduler constraints; self-dev needs self-dev session gates, build/test, canary, and reload recovery.
