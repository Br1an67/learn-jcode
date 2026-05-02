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

## 练习

选一个简单工具，比如 `ls` 或 `read`，追踪完整路径：

```text
模型如何看到这个工具定义？
模型如何发起 tool call？
JCode 如何解析 tool input？
工具在哪里 execute？
工具结果如何进入下一轮 messages？
```

写成一段笔记，不要超过 500 字。

如果笔记里只写“JCode 支持工具调用”，说明你还没追到关键路径。至少要写出一个函数名和一个数据结构名。
