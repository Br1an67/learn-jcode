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

## 这组文件怎么读

先打开 `src/tool/mod.rs`，从 `Tool` trait 开始读。不要先看 `read` 或 `bash` 的实现。`Tool` trait 定了工具在 JCode 里的合同：工具名、描述、JSON schema、执行函数。模型看到的是 definition，runtime 调的是 `execute()`，这两个动作都从这里开始。

接着读 `Tool::to_definition()`。它把 trait 方法转成 `ToolDefinition`。这一步连接了工具系统和 provider 层：没有 definition，模型不知道工具存在；没有 execute，工具只是 prompt 里的说明。

然后读 `Registry` 结构体。先看字段：`tools`、`skills`、`compaction`。这说明 registry 不是简单 map。它还要知道 skill registry，并且给 `conversation_search` 这类工具保存 compaction 相关状态。

下一步读 `Registry::base_tools()`。这里能看到哪些工具是无状态、可复用、通过 `OnceLock` 缓存的。重点不是背工具名，而是看 JCode 把 `read/write/edit/bash/grep/ls` 这类基础工具，和 `memory/goal/schedule/selfdev/swarm` 这类 harness 工具放进同一个 registry。

再看 `Registry::new(provider)`。它先拿 base tools，再插入 `subagent`、`batch`、`conversation_search` 这些 session-specific tools。原因很直接：这些工具需要当前 provider、registry 或 compaction manager，不能像 `read` 一样全局复用。

然后读 `Registry::definitions()`。注意它会过滤 allowed tools，并按 name 排序。排序不是洁癖，它减少 prompt cache 抖动。这个点和 `s03` 的 split prompt 是一条线：harness 要控制每次请求的稳定性。

最后读 `Registry::execute()`。先看 `resolve_tool_name()`，它把 `shell_exec`、`file_read`、`task` 这些 alias 转成 JCode 内部名字；再看执行后调用 `guard_context_overflow()`。这说明工具输出不是直接塞回上下文，registry 会管别名、telemetry、错误和截断。

读具体工具时按难度走：先看 `src/tool/read.rs` 或 `src/tool/ls.rs`，再看 `src/tool/edit.rs`、`src/tool/bash.rs`，最后看 `src/tool/task.rs`、`src/tool/communicate.rs`、`src/tool/mcp.rs`。不要第一天读 `swarm` 工具，它会把你拉到 server coordination。

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

## 一个小改造应该长什么样

如果要给 JCode 加一个入门级工具，`repo_summary` 是合适例子。它是只读工具，输出：

```text
branch:
latest commit:
top-level dirs:
tracked file count:
```

这个例子说明工具设计的边界：

- 不写文件。
- 不访问网络。
- 输出简短。
- 注册到 tool registry。
- 先能被模型调用，再考虑要不要接入 TUI。

它比天气 API 工具更适合 JCode 教程，因为它走的是 coding harness 的真实路径：schema、registry、execute、tool result、上下文截断。顺序反了，比如先做 widget，会把一个工具入门任务变成 UI 任务。
