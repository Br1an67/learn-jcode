# s04 - 工具系统

## 本课目标

看懂 JCode 怎样把工具交给模型。

工具系统是 coding-agent harness 的核心。没有工具，模型只能聊天。有了工具，模型才能读代码、改代码、跑测试、查历史、和其他 agent 协作。

## 先读这些文件

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

重点先看 `src/tool/mod.rs`。

## Tool trait

JCode 的工具统一实现 `Tool` trait：

```text
name()
description()
parameters_schema()
execute(input, ctx)
```

这套接口解决四个问题：

- 模型能看到工具名和说明。
- provider 能看到 JSON schema。
- runtime 能执行工具。
- UI/telemetry 能观察工具调用。

## 工具分类

### 基础 coding 工具

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

这些对应 coding agent 最基础的行动能力。

### 增强工具

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

这些不是最小 agent 必需，但能显著改善效率和可观察性。

这里不要只数工具数量。工具越多，越容易污染 prompt、撑爆上下文、让模型误选工具。JCode 的重点是工具治理，不是“工具越多越好”。

### Harness 级工具

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

这些工具已经不是普通函数调用，而是在操作 JCode 的运行时能力。

## Registry 做了什么

`Registry::base_tools()` 负责注册基础工具。注意几个实现细节：

- 用 `OnceLock` 缓存 base tools，减少每个 session 的初始化成本。
- `skill_manage` 需要 skills registry，所以单独插入。
- `subagent`、`batch`、`conversation_search` 是 session-specific，因为需要 provider 或 registry。
- tool definitions 会按名字排序，减少 prompt cache 抖动。
- tool output 会被 context guard 截断，防止撑爆上下文。
- MCP 工具可以在后台连接后动态注册。

这就是 JCode 和玩具 demo 的差距。工具多了以后，问题不再是“怎么 call function”，而是“怎么治理工具生态”。

## 和 pi-mono 的差异

pi 的默认哲学更克制：`read/write/edit/bash` 就够强。

JCode 的哲学更像：基础工具要强，同时把 memory、MCP、subagent、swarm、side panel 这类 harness 能力也变成工具。

这不是谁对谁错。差异在目标：

```text
pi: 最小有效 coding harness
JCode: 长期多会话本地 agent runtime
```

读到这里要能说出代价：pi 小，所以容易改；JCode 大，所以必须处理缓存、截断、动态注册、权限和 UI 状态。

## 练习：设计 repo_summary 工具

新增一个只读工具 `repo_summary`，输出：

```text
branch:
latest commit:
top-level dirs:
tracked file count:
```

要求：

- 不写文件。
- 不访问网络。
- 输出简短。
- 注册到 tool registry。
- 至少做一次手动验证。

这个练习能走通完整工具路径，比写一个天气 API 工具更接近 coding harness。

做这个练习时先不要接入 TUI。先让工具能被模型调用，再考虑要不要显示成 widget。顺序反了会把问题搞复杂。
