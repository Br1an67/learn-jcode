# learn-jcode 中文课程

这部分是中文分课文档。README 只做入口，真正学习时按这里的顺序读。

课程安排：

| 课次 | 主题 | 目标 |
| --- | --- | --- |
| [00](./00-map.md) | 全局地图 | 先看 JCode runtime 的整体形状 |
| [glossary](./glossary.md) | 术语表 | 固定反复出现的 runtime 术语 |
| [s01](./s01-harness-mindset.md) | Harness 心智 | 先把模型和 harness 的边界讲清楚 |
| [s02](./s02-startup-server.md) | 启动链路和常驻 server | 读懂 `jcode` 命令启动后发生什么 |
| [s03](./s03-agent-loop.md) | Agent Loop | 追踪一次模型输出、工具调用、工具结果 |
| [s04](./s04-tool-system.md) | 工具系统 | 看懂 JCode 怎样把工具交给模型 |
| [s05](./s05-provider-session.md) | Provider、Auth、Session | 理解多模型平台和长期会话怎么接起来 |
| [s06](./s06-tui-observability.md) | TUI 和可观察性 | 理解 UI 为什么是 harness 的一部分 |
| [s07](./s07-memory.md) | Memory | 理解非阻塞 memory sidecar |
| [s08](./s08-swarm.md) | Swarm | 理解 server-level 多 agent 协作 runtime |
| [s09](./s09-ambient-selfdev.md) | Ambient 和 Self-Dev | 理解后台循环和自我修改边界 |
| [s10](./s10-comparison.md) | 边界课 | 对齐 JCode 和几个 coding-agent runtime 的取舍 |

建议一天读一课或两课。JCode 不适合硬压成一天速成。遇到看不懂的模块，先写下问题，不要为了“读完”把目录硬扫过去。
