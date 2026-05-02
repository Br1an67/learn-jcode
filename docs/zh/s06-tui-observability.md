# s06 - TUI 和可观察性

## 本课目标

理解 UI 为什么是 harness 的一部分。

很多 agent 工程只关心“模型能不能完成任务”。但实际使用时，用户还需要知道它在干什么、改了什么、卡在哪里、花了多少上下文和钱。

JCode 在 TUI 上投入很多，这不是装饰。

判断一个 UI 模块是不是 harness 的一部分，看它是否影响用户判断 agent 状态。tool 状态、diff、usage、memory 命中都影响判断，所以它们不是皮肤。

## 先读这些文件

```text
src/tui/
src/side_panel.rs
src/tool/side_panel.rs
crates/jcode-tui-core/
crates/jcode-tui-render/
crates/jcode-tui-markdown/
crates/jcode-tui-mermaid/
```

不要一开始就扎进 `src/tui/ui.rs`。先看小块：

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

## JCode TUI 展示什么

JCode 的 TUI 不只是打印 assistant text。它还处理：

- tool call 摘要。
- streaming 状态。
- reasoning/thinking 展示。
- diff。
- side panel。
- markdown。
- mermaid。
- usage。
- model/account picker。
- git 状态。
- memory 状态。
- todo 状态。
- swarm/background 状态。

这些都是 harness 的可观察性。

## Side Panel 的意义

Side panel 是一个很实用的设计。它可以放：

- 当前文件。
- diff。
- 计划。
- review checklist。
- memory 命中。
- agent 生成的辅助内容。

这让用户不用在主聊天流里翻来翻去。

Side panel 的价值不是“多一个面板”。它把稳定参考信息从聊天流里拿出来。聊天流适合时间线，side panel 适合当前状态。

## Info Widget 的意义

Info widget 解决的是“状态显示不能抢主输出空间”的问题。比如：

- 当前模型。
- usage。
- git branch。
- memory 命中。
- todos。
- swarm 状态。

这些信息很重要，但不应该把主对话挤没。

## 和 OpenCode 的对比

OpenCode 也重视 UI，但路线不同。OpenCode 同时走 Web/Desktop/Open platform。JCode 更偏 terminal native，强调 Ratatui 渲染、终端信息密度和本地 runtime。

两者都说明一件事：coding agent 的 UI 不是 shell stdout 就够了。

## 一个 widget 应该怎么看

读 `info_widget_git` 或 `info_widget_todos` 时，按这条数据链路看：

```text
数据从哪里来？
在哪里进入状态？
通过什么 event 更新？
在哪里 render？
用户为什么需要这个信息？
```

不要从最复杂的 swarm widget 开始。先看 git 或 todo，因为数据来源清楚。判断一个 widget 是否必要，就问一句：删掉它，用户会少知道什么？答不上来，这个 widget 的用途还没读懂。
