# s03 - Agent Loop

## Goal

Trace one user input as it becomes:

```text
model output -> tool call -> tool result -> next model input
```

JCode has a lot of surrounding engineering, but the core remains a normal agent loop.

## Minimal Agent Loop

```text
messages
  -> LLM
  -> assistant text or tool_use
  -> execute tool
  -> append tool_result
  -> LLM
  -> ...
```

Do not overcomplicate the loop. The complexity lives around it: cache, compaction, streaming, memory, UI events, and error recovery.

## Read First

```text
src/agent/turn_loops.rs
src/agent/tools.rs
src/agent/messages.rs
src/agent/compaction.rs
src/agent/provider.rs
src/message.rs
src/protocol.rs
```

`src/agent/turn_loops.rs` is the main file.

Do not try to memorize every branch in that file. Follow one normal path first: user input, provider stream, model tool call, tool execution, tool result, next turn.

## What One JCode Turn Does

Inside `run_turn()`, roughly:

1. Repairs missing tool outputs so the provider accepts the history.
2. Builds provider messages and compacts when needed.
3. Builds tool definitions.
4. Takes the memory prompt computed from the previous turn.
5. Builds a split system prompt.
6. Calls provider `complete_split()`.
7. Parses stream events.
8. Collects tool calls.
9. Executes tools.
10. Converts tool output into content blocks.
11. Continues the loop if more tool calls exist.

This is the core path.

## Why Split the System Prompt

JCode splits the prompt into static and dynamic parts because some providers have prompt caching. Stable static content gives better cache hits.

Memory, time, and dynamic state should not be mixed into the static prefix. They would break cache stability.

This is a good example of harness engineering. A demo only cares whether the model answers. A harness cares about long-term latency and cost.

## Why Memory Appears Here

You will see memory injection in the turn loop. JCode memory is not a blocking query before every model call. It is closer to:

```text
turn N context -> background memory query
query result -> injected into turn N+1
```

This keeps the main agent responsive.

This is a tradeoff. Memory is not always maximally fresh in the same turn, but interaction latency stays stable.

## How Tool Result Returns to the Model

Tools return `ToolOutput`. Then `tool_output_to_content_blocks()` turns it into provider-compatible content blocks.

Trace:

```text
StreamEvent::ToolUseStart
  -> ToolCall
  -> Registry::execute()
  -> ToolOutput
  -> tool_output_to_content_blocks()
  -> Message
  -> next provider call
```

## Exercise

Pick a simple tool, such as `ls` or `read`, and trace:

```text
How does the model see this tool definition?
How does the model issue the tool call?
How does JCode parse tool input?
Where does the tool execute?
How does the tool result enter the next messages?
```

Write a note under 500 words.

If the note only says "JCode supports tool calling," you have not traced the path yet. Include at least one function name and one data structure name.
