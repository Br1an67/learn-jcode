# Glossary - 术语表

这页只做一件事：把教程里反复出现的词固定下来。后面课程遇到这些词，不再每次重新解释。

## 核心术语

| 术语 | 本教程里的意思 | 容易误读成 |
| --- | --- | --- |
| model | 做判断的模型，例如 Claude、OpenAI、Gemini 等 provider 后面的 LLM | JCode 自己的规则系统 |
| harness | 模型外面的运行环境：工具、上下文、权限、状态、UI、存储 | 一组 prompt 或工作流 |
| agent loop | 一轮又一轮把 messages 发给模型、处理 tool call、追加 tool result 的循环 | 一个复杂的 planner |
| runtime | 支撑 agent loop 长期运行的进程、状态和后台任务集合 | 单个函数调用 |
| resident server | JCode 的常驻本地 server，负责 session、provider、MCP、swarm、event 等长期状态 | 普通后台转发进程 |
| TUI client | 终端 UI 客户端，连接 server，展示消息、工具状态、diff、widgets | 所有状态的拥有者 |
| session | JCode 的长期会话状态，包含 messages、journal、replay、compaction、render 信息 | 聊天文本数组 |
| journal | session 的追加式事件记录，用于恢复和重放 | 普通日志 |
| replay | 把保存下来的 session/event 重新变成可继续消费的状态 | 播放聊天记录 |
| provider | 模型平台适配层，把 JCode 的 messages/tools/system prompt 转成平台请求，再把 stream 转回 `StreamEvent` | 一行 API 调用 |
| `StreamEvent` | JCode 内部统一的 provider 流事件，例如 text delta、tool use、usage、error | 某个 provider 的原始 SSE |
| registry | 工具注册和执行中心，负责 tool definition、allowed tools、alias、telemetry、截断 | `HashMap<String, Tool>` |
| tool definition | 给模型看的工具名、描述和 JSON schema | 工具实现本身 |
| tool result | 工具执行后的结果，会作为下一轮模型输入的一部分 | 只给用户看的输出 |
| sidecar | 主 agent loop 旁边的后台组件，不阻塞主 turn，比如 memory agent | 独立产品或插件 |
| memory | JCode 的长期召回系统，用 sidecar 非阻塞检索并在下一轮注入 | 手动笔记或普通 RAG demo |
| pending memory | memory sidecar 已经算好、等待主 agent 下一轮取走的 prompt | 当前轮立即生效的上下文 |
| swarm | server 维护的多 agent 协作状态，包含 plan、worker、channel、heartbeat、report | 多开几个 subagent |
| coordinator | swarm 里的协调会话，负责计划和整合 | 更聪明的模型 |
| worker | swarm 里的工作会话，接收任务、汇报进度和结果 | 普通函数调用 |
| channel | swarm 内的通信订阅关系，由 server 维护 channel/session 索引 | prompt 里的 `#name` 约定 |
| heartbeat | worker 向 server plan 回写的活跃信号 | UI 动画 |
| checkpoint | worker 对当前进度的中间摘要 | 最终报告 |
| ambient | 后台维护循环，用预算和 scheduler 做低风险环境维护 | 无限后台 agent |
| scheduler | ambient 的唤醒和排序机制，决定什么时候跑、先跑什么 | cron 的别名 |
| self-dev | 让 JCode 在受控 session 里 build/test/reload 自己 | 普通热重载 |
| canary | self-dev reload 前待测试的新版本标记 | 发布版本 |
| reload handoff | 新 binary 接管旧 server，并尽量恢复 session 的过程 | 直接 kill 再重启 |
| MCP pool | server 维护的 MCP 连接池，让工具能力可以来自外部服务 | 一次性 MCP 调用 |
| side panel | 模型可操作的持久页面，能写入、追加、聚焦、删除 | TUI 里的临时显示块 |
| compaction | 把长历史压缩成可继续使用的状态，减少上下文压力 | 简单总结 |

## 几组边界

### client 和 server

client 负责交互和展示，server 负责长期状态。client 退出不等于 session 消失。这个边界解释了为什么 JCode 需要 socket、reload、multi-client 和 server runtime。

### provider 和 agent loop

agent loop 只处理 JCode 内部消息和 `StreamEvent`。provider 层负责处理不同平台的请求体、鉴权、stream 格式和缓存行为。这个边界让 JCode 不需要在 turn loop 里写一堆 provider-specific 分支。

### tool definition 和 tool execution

definition 给模型看，execution 给 runtime 调。一个工具要同时有 schema 和 handler。只写 prompt 说明不算工具，只写 handler 也不能让模型知道怎么调用。

### memory 和当前 turn

memory sidecar 不阻塞当前 turn。它把结果写到 pending memory，主 agent 下一轮再注入。这个一轮延迟是设计选择，不是漏掉同步检索。

### subagent 和 swarm

subagent 偏一次性委派，swarm 偏长期协作现场。swarm 需要 plan、channel、heartbeat、checkpoint、report 和恢复逻辑。

### ambient 和 self-dev

ambient 维护环境，self-dev 修改 JCode 自己。前者要受 budget 和 scheduler 约束，后者要受 self-dev session、build/test、canary、reload recovery 约束。
