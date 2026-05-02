# s01 - Harness 心智

## 先说结论

JCode 不是一个“Rust 写的聊天壳”。它是一个 coding-agent harness。

这句话要先理解，不然后面读源码会很痛苦。因为你会看到大量看起来和 LLM 无关的代码：server、socket、TUI、OAuth、provider catalog、session journal、memory、MCP、swarm、reload。这些不是旁枝，它们就是 harness。

本课不读具体实现，只定学习视角。视角错了，后面会把 server、TUI、session 都误读成“额外功能”。

## Agent 和 Harness 的边界

沿用 `learn-claude-code` 的说法：模型才是 agent。模型负责判断下一步该做什么。外部工程负责给模型提供环境。

```text
Agent product = Model + Harness

Harness = Tools
        + Context
        + Runtime
        + UI
        + Storage
        + Permissions
        + Provider integration
        + Memory
```

对 coding agent 来说：

- Tools 是手：读文件、写文件、改文件、跑命令。
- Context 是眼睛：当前消息、文件片段、错误日志、diff、工具结果。
- Runtime 是身体：进程、server、session、后台任务。
- UI 是驾驶舱：流式输出、工具状态、diff、side panel。
- Storage 是恢复能力：历史会话、journal、配置、账号。
- Permissions 是边界：哪些命令能跑，哪些文件能写。
- Provider integration 是发动机适配层：Claude、OpenAI、Gemini、Copilot、OpenRouter、OpenAI-compatible。
- Memory 是长期经验：用户偏好、项目事实、旧会话线索。

## 为什么 JCode 值得学

如果只想理解最小 agent loop，JCode 太大了。你应该先看 pi-mono 或 `Learn-OpenClaw`。

JCode 值得学的是产品化之后的复杂性：

```text
玩具 agent:
LLM + tools + loop

长期可用的 coding-agent harness:
LLM + tools + loop
  + server
  + session
  + provider
  + auth
  + cache
  + compaction
  + memory
  + UI
  + permissions
  + coordination
  + recovery
```

这就是 JCode 的学习价值。

## 和几个参考项目的关系

### Learn-OpenClaw

`Learn-OpenClaw` 更适合快速建立 agent 概念。它把 Node、Workflow、Agent、Tool、MCP、Skill 讲得很直接。

这份 JCode 教程不复刻那个“一天速成”的节奏，而是保留它的实用性：每一课告诉你读哪些文件、看什么问题、最后应该带走什么结论。

### learn-claude-code

`learn-claude-code` 的强项是立场清楚：不要把 prompt plumbing 当 agent，真正要学的是 harness engineering。

这份教程沿用这个立场。JCode 不是让模型“变聪明”的代码，它是让模型能安全、稳定、长期地在代码库里行动的环境。

### pi-mono

pi 的价值是小。它告诉你 `read/write/edit/bash` 就能构成一个有效 coding agent。

JCode 的价值是大。它告诉你当这个 agent 要支持多 provider、多 session、memory、swarm、UI、self-dev 时，工程会长成什么样。

### OpenCode

OpenCode 和 JCode 都是开源 coding agent，都有 client/server 思路。OpenCode 更像开放平台，JCode 更像本地高性能 runtime。

## 这课应该带走的结论

读 JCode 时先用这句话校准视角：

```text
模型是 agent。JCode 是让模型能在代码库里行动的 harness。
```

这句话不是口号。它会影响你怎么看源码：

- `src/tool/` 不是“插件集合”，是模型的手。
- `src/server/` 不是“额外服务”，是长期会话和多 client 的 runtime。
- `src/provider/` 不是“一层 API wrapper”，是不同模型平台的适配层。
- `src/tui/` 不是皮肤，是用户判断 agent 状态的驾驶舱。
- `src/memory*` 不是普通 RAG demo，是长期使用后的召回系统。

也要记住代价：常驻 server 能复用状态，但带来 reload、socket、生命周期管理这些复杂度。JCode 的每个大设计都类似，收益和代价一起出现。
