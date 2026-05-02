[中文](./README.md) | [English](./README-en.md)

# Learn JCode 5.5

这是一份给工程师看的 JCode 源码课程。写法按“同事带你读代码”来，不写宣传稿，不堆黑话。

读者默认知道一点 agent loop，但还没系统读过产品级 coding-agent harness。你来这里不是为了看“JCode 很强”，而是为了知道它为什么需要 server、tool registry、provider、session、TUI、memory、swarm 这些东西。

写作口径见 [docs/writing-style.md](./docs/writing-style.md)。后续新增章节都按这份规范写。

## 适合谁

适合已经知道 agent loop 大概是什么，并且想继续理解这些问题的人：

- 一个 coding agent 为什么需要常驻 server？
- tool call 怎么进入模型上下文？
- provider/auth/session 为什么会变复杂？
- TUI 为什么不是装饰，而是 harness 的一部分？
- memory、swarm、ambient、self-dev 这些能力到底解决什么问题？
- JCode 和 pi、OpenCode、Claude Code 的差异在哪里？

如果你完全没接触过 agent，建议先看 `Learn-OpenClaw` 或 pi-mono，再回来读 JCode。

## 项目结构

```text
learn-jcode-5.5/
├── README.md                 # 中文入口
├── README-en.md              # English entry
├── docs/
│   ├── zh/                   # 中文分课文档
│   │   ├── README.md
│   │   ├── s01-harness-mindset.md
│   │   ├── s02-startup-server.md
│   │   ├── s03-agent-loop.md
│   │   ├── s04-tool-system.md
│   │   ├── s05-provider-session.md
│   │   ├── s06-tui-observability.md
│   │   ├── s07-memory.md
│   │   ├── s08-swarm.md
│   │   └── s09-ambient-selfdev.md
│   ├── en/                   # English lesson docs
│   │   ├── README.md
│   │   ├── s01-harness-mindset.md
│   │   ├── s02-startup-server.md
│   │   ├── s03-agent-loop.md
│   │   ├── s04-tool-system.md
│   │   ├── s05-provider-session.md
│   │   ├── s06-tui-observability.md
│   │   ├── s07-memory.md
│   │   ├── s08-swarm.md
│   │   └── s09-ambient-selfdev.md
│   ├── analysis-notes.md     # 本教程写作和参考项目分析
│   ├── project-structure.md  # 为什么这样组织项目
│   ├── sources.md            # 本地参考仓库和 revision
│   └── writing-style.md      # 写作口径和禁用表达
└── .gitignore
```

没有照搬 `learn-claude-code` 的 `agents/` 示例目录。原因是这个教程不是从零写一个 toy agent，而是读 JCode 本身。需要读者知道的内容直接写进课程，不单独开动手区。

## 课程

建议按顺序读，每天 1-2 课。

| 课次 | 中文 | English |
| --- | --- | --- |
| s01 | [Harness 心智](./docs/zh/s01-harness-mindset.md) | [Harness Mindset](./docs/en/s01-harness-mindset.md) |
| s02 | [启动链路和常驻 Server](./docs/zh/s02-startup-server.md) | [Startup and Resident Server](./docs/en/s02-startup-server.md) |
| s03 | [Agent Loop](./docs/zh/s03-agent-loop.md) | [Agent Loop](./docs/en/s03-agent-loop.md) |
| s04 | [工具系统](./docs/zh/s04-tool-system.md) | [Tool System](./docs/en/s04-tool-system.md) |
| s05 | [Provider、Auth、Session](./docs/zh/s05-provider-session.md) | [Provider, Auth, Session](./docs/en/s05-provider-session.md) |
| s06 | [TUI 和可观察性](./docs/zh/s06-tui-observability.md) | [TUI and Observability](./docs/en/s06-tui-observability.md) |
| s07 | [Memory](./docs/zh/s07-memory.md) | [Memory](./docs/en/s07-memory.md) |
| s08 | [Swarm](./docs/zh/s08-swarm.md) | [Swarm](./docs/en/s08-swarm.md) |
| s09 | [Ambient 和 Self-Dev](./docs/zh/s09-ambient-selfdev.md) | [Ambient and Self-Dev](./docs/en/s09-ambient-selfdev.md) |

## 推荐学习节奏

不要把 JCode 当一天速成项目。

```text
第 0 天：跑起来，确认 provider 能登录
第 1 天：读启动链路和 server/client
第 2 天：读 agent loop
第 3 天：读 tool registry
第 4 天：读 provider/auth/session
第 5 天：读 TUI 和可观察性
第 6 天：读 memory
第 7 天：读 swarm
第 8 天：读 ambient/self-dev
```

这个节奏不是硬性安排。重点是不要跳过前四课直接冲 swarm 和 self-dev。那样很容易只记住名词，看不懂运行时边界。

真正要做项目时，建议选一个小改造：

- 新增一个只读工具，比如 `repo_summary`。
- 写一套 OpenAI-compatible provider profile 配置和 smoke test 文档。
- 做一个 side panel 工作流。
- 写一份 JCode / OpenCode / pi 的源码级比较。
- 给 memory/session search 写一个实际用例。

## 本地参考来源

本教程基于这些本地仓库阅读：

- JCode: `/Users/shizi/Documents/workspace/jcode`
- learn-claude-code: `/tmp/learn-claude-code`
- Learn-OpenClaw: `/tmp/Learn-OpenClaw`
- pi-mono: `/Users/shizi/Documents/workspace/pi-mono`
- OpenCode: `/Users/shizi/Documents/workspace/opencode`

具体 revision 见 [docs/sources.md](./docs/sources.md)。

关于 Claude Code：本教程只比较公开行为和 harness 设计思想，不使用、不传播、不复述任何非公开或泄露源码。
