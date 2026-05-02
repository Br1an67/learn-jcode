# s07 - Memory、Swarm、Ambient、Self-Dev

## 本课目标

看 JCode 最有差异化、也最容易读晕的部分。

这一课不要急着改代码。先读文档，画图，确认自己理解运行时边界。

这几个模块很容易被讲成名词堆叠。读的时候只问一个问题：它解决了单 agent loop 的哪个具体短板？

## Memory

先读：

```text
docs/MEMORY_ARCHITECTURE.md
docs/MEMORY_BUDGET.md
src/memory.rs
src/memory_agent.rs
src/memory_graph.rs
src/memory_prompt.rs
src/tool/memory.rs
src/tool/session_search.rs
```

JCode 的 memory 不是“用户手动保存一条笔记”。它更像自动召回：

```text
当前上下文
  -> embedding
  -> 相似 memory
  -> graph / cascade retrieval
  -> 可选 sidecar 验证
  -> 下一轮注入 memory prompt
```

关键设计是非阻塞：

```text
第 N 轮触发查询
第 N+1 轮使用结果
```

这样不会让主 agent 每轮都等 memory。

代价是 memory 有一轮延迟。这个延迟是有意设计，不是漏做同步检索。

## Swarm

先读：

```text
docs/SWARM_ARCHITECTURE.md
src/server/swarm.rs
src/server/swarm_channels.rs
src/server/comm_*.rs
src/tool/communicate.rs
src/tool/task.rs
```

JCode 的 swarm 不是普通 subagent。它关心多 agent 协作运行时：

- coordinator 怎么分配任务。
- worker 怎么汇报。
- agent 之间怎么 DM / broadcast / channel。
- 哪些文件被谁读过、改过。
- plan 怎么更新。
- blocked / failed / crashed 怎么恢复。
- worktree 什么时候用，什么时候不用。

这部分最能体现 JCode 和 pi 的差异。pi 更克制，JCode 更激进。

不要把 swarm 理解成“多开几个 subagent”。真正难的是计划、通信、文件触达、状态恢复和集成边界。

## Ambient

先读：

```text
docs/AMBIENT_MODE.md
src/ambient/
src/ambient_runner.rs
src/tool/ambient.rs
```

Ambient 是后台 agent。它不是用户发一句做一句，而是在资源允许时做维护：

- 整理 memory。
- 检查最近 session。
- 看 git 活动。
- 做低风险主动任务。
- 自己决定下次什么时候醒来。

这个方向还很实验，但值得读，因为它指向长期 agent 环境维护。

读 ambient 时重点看资源限制。后台 agent 如果没有预算和优先级控制，会变成另一个干扰源。

## Self-Dev

先读：

```text
src/cli/selfdev.rs
src/tool/selfdev.rs
src/prompt/selfdev_mode.txt
src/prompt/selfdev_hint.txt
docs/UNIFIED_SELFDEV_SERVER_PLAN.md
```

Self-dev 是让 JCode 改自己。

建议非常保守：

- 新建分支。
- 保持工作区干净。
- 每一步 commit。
- 小改动开始。
- 必须跑 `cargo check`。
- 不要一上来改 provider、server reload、compaction、swarm。

## 本课练习

选一个方向写一页设计笔记：

```text
Memory 如何避免阻塞主 agent？
Swarm 为什么不能只靠 subagent summary？
Ambient 为什么需要资源限制？
Self-dev 最危险的模块是什么？
```

要求：

- 必须引用至少 3 个源码文件。
- 必须画一张 mermaid 图。
- 必须写出一个“不要做什么”的风险点。

不要写“未来可以扩展更多能力”这种空话。写一个具体风险，比如 self-dev 改 reload 路径导致正在运行的 session 丢状态。
