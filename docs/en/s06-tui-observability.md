# s06 - TUI and Observability

## Goal

Understand why UI is part of the harness.

Many agent projects only care whether the model can finish a task. In real use, the user also needs to know what the agent is doing, what changed, where it is stuck, and how much context or money it is spending.

JCode invests heavily in TUI for this reason.

A UI module belongs to the harness if it changes how the user judges agent state. Tool status, diffs, usage, and memory hits all affect that judgment.

## Read First

```text
src/tui/
src/side_panel.rs
src/tool/side_panel.rs
crates/jcode-tui-core/
crates/jcode-tui-render/
crates/jcode-tui-markdown/
crates/jcode-tui-mermaid/
```

Do not start by reading all of `src/tui/ui.rs`. Start smaller:

```text
src/tui/info_widget.rs
src/tui/info_widget_git.rs
src/tui/info_widget_memory_render.rs
src/tui/info_widget_todos.rs
src/tui/info_widget_swarm_background.rs
src/tui/ui_tools.rs
src/tui/ui_diff.rs
src/tui/stream_buffer.rs
```

## What the JCode TUI Shows

JCode does not only print assistant text. It also handles:

- tool call summaries
- streaming state
- reasoning/thinking display
- diffs
- side panels
- markdown
- mermaid
- usage
- model/account pickers
- git status
- memory status
- todo status
- swarm/background status

This is harness observability.

## Why Side Panel Matters

The side panel can hold:

- current file
- diff
- plan
- review checklist
- memory hits
- agent-generated auxiliary content

This keeps the user from digging through the main chat stream.

The point is not "one more panel." Chat is good for timeline. Side panels are good for stable current state.

## Why Info Widgets Matter

Info widgets solve the problem of showing state without stealing the main response area. Examples:

- current model
- usage
- git branch
- memory hits
- todos
- swarm status

These details matter, but should not crowd out the main conversation.

## Comparison With OpenCode

OpenCode also cares about UI, but its direction is different. OpenCode also targets Web/Desktop/open-platform surfaces. JCode is more terminal-native, with Ratatui rendering, high terminal information density, and local runtime emphasis.

Both projects show the same lesson: stdout is not enough for a serious coding agent.

## How to Read a Widget

When reading `info_widget_git` or `info_widget_todos`, follow this data path:

```text
Where does the data come from?
Where does it enter state?
Which event updates it?
Where is it rendered?
Why does the user need this information?
```

Do not start with the more complex swarm widget. Git and todo widgets have clearer data sources. To judge whether a widget matters, ask: if this were removed, what would the user stop knowing? If you cannot answer, you have not understood the widget.
