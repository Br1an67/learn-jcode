# s04 - Tool System

## Goal

Understand how JCode gives tools to the model.

The tool system is the core of a coding-agent harness. Without tools, the model can only chat. With tools, it can read code, edit code, run tests, search history, and coordinate with other agents.

## Read First

```text
src/tool/mod.rs
src/tool/read.rs
src/tool/write.rs
src/tool/edit.rs
src/tool/bash.rs
src/tool/grep.rs
src/tool/task.rs
src/tool/communicate.rs
src/tool/mcp.rs
src/tool/memory.rs
src/tool/side_panel.rs
```

Start with `src/tool/mod.rs`.

## Tool Trait

JCode tools implement a shared `Tool` trait:

```text
name()
description()
parameters_schema()
execute(input, ctx)
```

This interface solves four problems:

- The model can see tool names and descriptions.
- The provider can see JSON schemas.
- The runtime can execute tools.
- UI and telemetry can observe calls.

## Tool Groups

### Basic Coding Tools

```text
read
write
edit
multiedit
patch
apply_patch
glob
grep
ls
bash
open
```

These are the basic actions a coding agent needs.

### Enhanced Tools

```text
agentgrep
browser
webfetch
websearch
codesearch
lsp
side_panel
session_search
conversation_search
```

These are not mandatory for a minimal agent, but they reduce context-hunting and make the runtime easier to observe.

Do not judge this section by tool count. More tools can pollute prompts, overflow context, or make the model choose the wrong action. JCode's real topic here is tool governance.

### Harness-Level Tools

```text
subagent
batch
swarm
memory
goal
todo
mcp
skill_manage
schedule
selfdev
```

These are no longer simple function calls. They operate on JCode runtime capabilities.

## What the Registry Does

`Registry::base_tools()` registers base tools. Notice:

- `OnceLock` caches base tools to reduce per-session initialization cost.
- `skill_manage` needs the skills registry, so it is inserted separately.
- `subagent`, `batch`, and `conversation_search` are session-specific because they need provider or registry references.
- Tool definitions are sorted by name to reduce prompt-cache churn.
- Tool outputs go through a context guard to avoid context overflow.
- MCP tools can be dynamically registered after background connection.

This is where JCode differs from toy demos. With many tools, the problem is no longer "how do I call a function?" The problem becomes "how do I govern a tool ecosystem?"

## Difference From pi-mono

pi is more restrained by default: `read/write/edit/bash` can already do a lot.

JCode is more expansive: it keeps strong base tools, but also exposes memory, MCP, subagent, swarm, and side-panel capabilities as tools.

This is a target difference:

```text
pi: minimal effective coding harness
JCode: long-running multi-session local agent runtime
```

You should be able to name the cost: pi is small and easy to modify; JCode is larger and has to handle caching, truncation, dynamic registration, permissions, and UI state.

## Exercise: Design `repo_summary`

Add a read-only `repo_summary` tool that returns:

```text
branch:
latest commit:
top-level dirs:
tracked file count:
```

Rules:

- Do not write files.
- Do not access the network.
- Keep output short.
- Register it in the tool registry.
- Run at least one manual validation.

This exercise walks the real tool path and is more useful than a weather API tool.

Do not start with TUI integration. First make the tool callable by the model; then decide whether it deserves a widget. Reversing that order makes the task harder than it needs to be.
