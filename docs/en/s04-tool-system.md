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

## How to Read These Files

Open `src/tool/mod.rs` and start with the `Tool` trait. Do not begin with `read` or `bash`. The trait defines the contract for every tool in JCode: name, description, JSON schema, and execution. The model sees definitions; the runtime calls `execute()`. Both start here.

Next read `Tool::to_definition()`. It turns trait methods into `ToolDefinition`. This is the bridge between the tool system and the provider layer: without the definition, the model does not know the tool exists; without `execute()`, the definition is only text.

Then read the `Registry` struct. Look at `tools`, `skills`, and `compaction`. The registry is not just a map. It also knows about the skill registry and keeps compaction-related state for tools such as `conversation_search`.

Now read `Registry::base_tools()`. This shows which tools are stateless enough to share and cache through `OnceLock`. Do not memorize the list. Notice that JCode puts basic tools like `read/write/edit/bash/grep/ls` and harness tools like `memory/goal/schedule/selfdev/swarm` into the same registry.

After that, read `Registry::new(provider)`. It starts from base tools, then inserts `subagent`, `batch`, and `conversation_search` as session-specific tools. Those tools need the current provider, registry, or compaction manager, so they cannot be global in the same way as `read`.

Then read `Registry::definitions()`. It filters allowed tools and sorts by name. Sorting is not cosmetic. It reduces prompt-cache churn. This is the same theme as split prompts in `s03`: a harness tries to keep request prefixes stable.

Finally read `Registry::execute()`. Start with `resolve_tool_name()`, which maps aliases such as `shell_exec`, `file_read`, and `task` to internal JCode names. Then read the call to `guard_context_overflow()`. Tool output is not blindly appended to context; the registry handles aliases, telemetry, errors, and truncation.

When you move to concrete tools, go in this order: `src/tool/read.rs` or `src/tool/ls.rs`, then `src/tool/edit.rs` and `src/tool/bash.rs`, then `src/tool/task.rs`, `src/tool/communicate.rs`, and `src/tool/mcp.rs`. Do not start with the swarm tool on day one. It pulls you into server coordination.

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

## What a Small Modification Looks Like

If you add a beginner-friendly JCode tool, `repo_summary` is a good example. It is read-only and returns:

```text
branch:
latest commit:
top-level dirs:
tracked file count:
```

This example shows the boundaries of tool design:

- Do not write files.
- Do not access the network.
- Keep output short.
- Register it in the tool registry.
- Make it callable by the model before touching TUI.

It fits this tutorial better than a weather API tool because it walks the real coding-harness path: schema, registry, execute, tool result, context truncation. Starting with a widget turns a tool task into a UI task too early.
