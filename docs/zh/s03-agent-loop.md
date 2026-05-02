# s03 - Agent Loop

## 本课目标

追踪一次用户输入如何变成：

```text
模型输出 -> 工具调用 -> 工具结果 -> 下一轮模型输入
```

JCode 外围工程很多，但核心仍然是普通 agent loop。

## 最小 Agent Loop

最小 loop 长这样：

```text
messages
  -> LLM
  -> assistant text or tool_use
  -> execute tool
  -> append tool_result
  -> LLM
  -> ...
```

不要把 agent loop 想复杂。复杂的是 loop 旁边的缓存、压缩、stream、memory、UI event 和错误恢复。

## 先读这些文件

```text
src/agent/turn_loops.rs
src/agent/tools.rs
src/agent/messages.rs
src/agent/compaction.rs
src/agent/provider.rs
src/message.rs
src/protocol.rs
```

其中 `src/agent/turn_loops.rs` 是重点。

读这个文件时不要试图一次性记住所有分支。先只追一条正常路径：用户输入、provider stream、模型发 tool call、工具执行、tool result 回到下一轮。

## `turn_loops.rs` 怎么读

先打开 `src/agent/turn_loops.rs`，只看 `impl Agent` 里的 `run_turn()`。这个函数很长，第一遍不要从头到尾精读。把它切成三段看。

第一段是 provider 调用前的准备。读 `repair_missing_tool_outputs()`、`messages_for_provider()`、`tool_definitions().await`、`build_memory_prompt_nonblocking_shared()`、`build_system_prompt_split()`。这几行告诉你 JCode 发请求前要同时处理消息修复、compaction、工具定义、memory pending result 和 split prompt。

第二段是 provider stream。找到 `provider.complete_split(...)`，再往下看 `while let Some(event) = stream.next().await`。这里不要先看所有 event，先只看四个：`TextDelta`、`ToolUseStart`、`ToolInputDelta`、`ToolUseEnd`。它们对应模型一边输出文本，一边拼出一个 JSON tool input。

第三段是工具执行。搜索 `registry.execute`，你会看到两处：一处处理 `StreamEvent::NativeToolCall`，另一处处理普通 `tool_calls`。先读普通路径：构造 `ToolContext`，发布 `ToolStatus::Running`，执行 `self.registry.execute(&tc.name, tc.input.clone(), ctx).await`，再用 `tool_output_to_content_blocks()` 把结果变成下一轮 `Role::User` message。

然后跳到 `src/agent/tools.rs` 看 `tool_output_to_content_blocks()`。这个函数小，但位置很关键：它把 Rust 工具输出翻译成 provider 能继续消费的 `ContentBlock::ToolResult`。读完它，再回到 `run_turn()` 末尾看 `self.session.save()`，你就能连上“工具结果进入会话历史”这一步。

`src/agent/messages.rs` 和 `src/message.rs` 放在这条线后面读。先看 `Message`、`Role`、`ContentBlock` 的形状，再回头理解 `messages_for_provider()` 为什么要整理历史。`src/protocol.rs` 最后读，它解释这些事件怎样给 TUI 或远程 client 看。

## 核心代码节选

`run_turn()` 的第一段不是模型调用，而是整理请求材料：

```rust
// src/agent/turn_loops.rs，精简版
loop {
    let repaired = self.repair_missing_tool_outputs();
    let (messages, compaction_event) = self.messages_for_provider();
    let tools = self.tool_definitions().await;

    let memory_pending =
        self.build_memory_prompt_nonblocking_shared(messages.clone(), None);

    let split_prompt = self.build_system_prompt_split(None);

    let mut stream = self.provider.complete_split(
        &messages_with_memory,
        &tools,
        &split_prompt.static_part,
        &split_prompt.dynamic_part,
        self.provider_session_id.as_deref(),
    ).await?;
}
```

这段代码说明 JCode 的 agent loop 不是直接把聊天记录丢给模型。它先修 history、可能 compact、生成 tools、取上一轮 memory 结果，再用 split prompt 调 provider。

stream 事件里，先只看 tool call 相关的四个分支：

```rust
// src/agent/turn_loops.rs，精简版
match event {
    StreamEvent::TextDelta(text) => {
        text_content.push_str(&text);
    }
    StreamEvent::ToolUseStart { id, name } => {
        current_tool = Some(ToolCall { id, name, input: Value::Null, intent: None });
        current_tool_input.clear();
    }
    StreamEvent::ToolInputDelta(delta) => {
        current_tool_input.push_str(&delta);
    }
    StreamEvent::ToolUseEnd => {
        let tool_input = serde_json::from_str(&current_tool_input)
            .unwrap_or(Value::Null);
        tool.input = tool_input;
        tool_calls.push(tool);
    }
    _ => {}
}
```

这里能看到 provider stream 和 tool call 的关系：模型不是一次性给出完整 JSON，JCode 会把 input delta 拼起来，等 `ToolUseEnd` 再解析成 `ToolCall`。

工具执行和结果回填是下一段：

```rust
// src/agent/turn_loops.rs，节选
let result = self.registry.execute(&tc.name, tc.input.clone(), ctx).await;

match result {
    Ok(output) => {
        let blocks = tool_output_to_content_blocks(tc.id, output);
        self.add_message_with_duration(Role::User, blocks, Some(duration_ms));
    }
    Err(e) => {
        self.add_message_with_duration(
            Role::User,
            vec![ContentBlock::ToolResult {
                tool_use_id: tc.id,
                content: format!("Error: {}", e),
                is_error: Some(true),
            }],
            Some(duration_ms),
        );
    }
}
```

这段代码把 agent loop 接回下一轮：模型发 tool call，registry 执行工具，工具结果被写回成下一轮 `Role::User` message。没有这一步，模型不会看到工具结果。

再看转换函数：

```rust
// src/agent/tools.rs，节选
pub(super) fn tool_output_to_content_blocks(
    tool_use_id: String,
    output: ToolOutput,
) -> Vec<ContentBlock> {
    let mut blocks = vec![ContentBlock::ToolResult {
        tool_use_id,
        content: output.output,
        is_error: None,
    }];

    for img in output.images {
        blocks.push(ContentBlock::Image {
            media_type: img.media_type,
            data: img.data,
        });
    }

    blocks
}
```

这说明 JCode 的工具结果不只是文本。工具可以返回图片，最终都被转成 provider 能继续消费的 content blocks。

## JCode 一轮 turn 做什么

在 `run_turn()` 里，大致会发生：

1. 修复缺失 tool output，避免 provider 拒绝消息。
2. 生成 provider messages，必要时 compact。
3. 构建 tool definitions。
4. 获取上一轮算好的 memory prompt。
5. 构建 split system prompt。
6. 调 provider 的 `complete_split()`。
7. 解析 stream event。
8. 收集 tool calls。
9. 执行工具。
10. 把 tool output 转成 content blocks。
11. 如果还有工具调用，继续 loop。

这是 JCode 最核心的路径。

## 为什么要 split system prompt

JCode 会把 prompt 分成 static 和 dynamic 部分。原因很直接：有些 provider 有 prompt cache，静态部分稳定，缓存命中更好。

Memory、时间、动态状态这类内容如果混进静态 prefix，会破坏 cache。

这类细节很能体现 harness 工程和 demo 工程的区别。demo 只关心能不能答，harness 要关心长期成本和延迟。

## Memory 为什么在这里出现

在 turn loop 里你会看到 memory 注入。JCode 的 memory 不是同步阻塞查询，而是：

```text
第 N 轮上下文 -> 后台 memory 查询
查询结果 -> 第 N+1 轮注入
```

这样主 agent 不会因为 memory search 变慢。

这是一种取舍：memory 不是每次都立刻最完整，但交互不会被检索拖住。教程里讲 memory 时都按这个取舍理解。

## Tool Result 怎么回到模型

工具执行后会返回 `ToolOutput`。然后 `tool_output_to_content_blocks()` 把它转成 provider 能理解的 content block。

你要追的路径是：

```text
StreamEvent::ToolUseStart
  -> ToolCall
  -> Registry::execute()
  -> ToolOutput
  -> tool_output_to_content_blocks()
  -> Message
  -> 下一轮 provider call
```

## 一条工具调用路径

读 `ls` 或 `read` 时，把路径按下面这条线看：

```text
模型如何看到这个工具定义？
模型如何发起 tool call？
JCode 如何解析 tool input？
工具在哪里 execute？
工具结果如何进入下一轮 messages？
```

对应到源码，大致是：

```text
Registry::definitions()
  -> provider complete_split()
  -> StreamEvent::ToolUseStart / ToolInputDelta / ToolUseEnd
  -> Registry::execute()
  -> Tool::execute()
  -> ToolOutput
  -> tool_output_to_content_blocks()
  -> next provider messages
```

只记“JCode 支持工具调用”没有意义。你要记住函数和数据结构怎么接起来。
