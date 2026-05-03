[中文](./README.md) | [English](./README-en.md)

# learn-jcode

这是一份给工程师看的 JCode 源码课程。写法按“同事带你读代码”来，不写宣传稿，不堆黑话。

读者默认知道一点 agent loop，但还没系统读过产品级 coding-agent harness。你来这里不是为了看“JCode 很强”，而是为了知道它为什么需要 server、tool registry、provider、session、TUI、memory、swarm 这些东西。

## 适合谁

适合已经知道 agent loop 大概是什么，并且想继续理解这些问题的人：

- 一个 coding agent 为什么需要常驻 server？
- tool call 怎么进入模型上下文？
- provider/auth/session 为什么会变复杂？
- TUI 为什么不是装饰，而是 harness 的一部分？
- memory、swarm、ambient、self-dev 这些能力到底解决什么问题？
- JCode 和几个 coding-agent runtime 的边界在哪里？

如果你完全没接触过 agent，建议先看一个最小 agent loop demo，再回来读 JCode。

## 项目结构

```text
learn-jcode/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml  # GitHub Pages 部署
├── book.toml                 # mdBook 配置
├── README.md                 # 中文入口
├── README-en.md              # English entry
├── mermaid.min.js            # mdBook 本地 Mermaid runtime
├── mermaid-init.js           # mdBook Mermaid 渲染
├── mini/                     # 核心机制的最小复现，不是任务区
│   ├── README.md
│   ├── 01_server_client.py
│   ├── 02_tool_registry.py
│   ├── 03_provider_stream.py
│   ├── 04_memory_sidecar.py
│   ├── 05_session_journal.py
│   ├── 06_swarm_channel.py
│   ├── 07_ambient_scheduler.py
│   └── 08_selfdev_reload_gate.py
├── scripts/
│   ├── check_bilingual_structure.py # 中英文结构漂移检查
│   └── prepare_mdbook_site.py       # 生成临时 mdBook source
├── theme/
│   └── custom.css             # mdBook 轻量样式
├── docs/
│   ├── zh/                   # 中文分课文档
│   │   ├── README.md
│   │   ├── 00-map.md
│   │   ├── s01-harness-mindset.md
│   │   ├── s02-startup-server.md
│   │   ├── s03-agent-loop.md
│   │   ├── s04-tool-system.md
│   │   ├── s05-provider-session.md
│   │   ├── s06-tui-observability.md
│   │   ├── s07-memory.md
│   │   ├── s08-swarm.md
│   │   ├── s09-ambient-selfdev.md
│   │   └── s10-comparison.md
│   ├── en/                   # English lesson docs
│   │   ├── README.md
│   │   ├── 00-map.md
│   │   ├── s01-harness-mindset.md
│   │   ├── s02-startup-server.md
│   │   ├── s03-agent-loop.md
│   │   ├── s04-tool-system.md
│   │   ├── s05-provider-session.md
│   │   ├── s06-tui-observability.md
│   │   ├── s07-memory.md
│   │   ├── s08-swarm.md
│   │   ├── s09-ambient-selfdev.md
│   │   └── s10-comparison.md
│   ├── analysis-notes.md     # JCode 内容分析和取舍记录
│   ├── deploy-pages.md       # GitHub Pages 部署说明
│   ├── glossary.md           # 术语表
│   ├── project-structure.md  # 为什么这样组织项目
│   └── sources.md            # 源码仓库和 revision
└── .gitignore
```

这个教程不是从零写一个 toy agent，而是读 JCode 本身。需要读者知道的内容直接写进课程，不单独开动手区。

`mini/` 里是 8 个核心机制的最小复现，对应 server/client、tool registry、provider stream、memory sidecar、session journal、swarm channel、ambient scheduler、self-dev reload gate。它们不是另一条任务线，只用于降低读 JCode 源码前的认知负担。

## 课程

建议按顺序读，每天 1-2 课。

| 课次 | 中文 | English |
| --- | --- | --- |
| 00 | [全局地图](./docs/zh/00-map.md) | [Global Map](./docs/en/00-map.md) |
| glossary | [术语表](./docs/zh/glossary.md) | [Glossary](./docs/en/glossary.md) |
| s01 | [Harness 心智](./docs/zh/s01-harness-mindset.md) | [Harness Mindset](./docs/en/s01-harness-mindset.md) |
| s02 | [启动链路和常驻 Server](./docs/zh/s02-startup-server.md) | [Startup and Resident Server](./docs/en/s02-startup-server.md) |
| s03 | [Agent Loop](./docs/zh/s03-agent-loop.md) | [Agent Loop](./docs/en/s03-agent-loop.md) |
| s04 | [工具系统](./docs/zh/s04-tool-system.md) | [Tool System](./docs/en/s04-tool-system.md) |
| s05 | [Provider、Auth、Session](./docs/zh/s05-provider-session.md) | [Provider, Auth, Session](./docs/en/s05-provider-session.md) |
| s06 | [TUI 和可观察性](./docs/zh/s06-tui-observability.md) | [TUI and Observability](./docs/en/s06-tui-observability.md) |
| s07 | [Memory](./docs/zh/s07-memory.md) | [Memory](./docs/en/s07-memory.md) |
| s08 | [Swarm](./docs/zh/s08-swarm.md) | [Swarm](./docs/en/s08-swarm.md) |
| s09 | [Ambient 和 Self-Dev](./docs/zh/s09-ambient-selfdev.md) | [Ambient and Self-Dev](./docs/en/s09-ambient-selfdev.md) |
| s10 | [边界课](./docs/zh/s10-comparison.md) | [Boundaries](./docs/en/s10-comparison.md) |

如果某课的源码太大，可以先看 [mini/](./mini/) 里的对应最小复现，再回到课程正文。

## 维护检查

改中文和英文课程时，先跑一次结构检查：

```bash
python3 scripts/check_bilingual_structure.py
```

这个脚本只防结构漂移，不替你判断翻译质量。它会检查中英文文件集合、标题层级、代码块语言、Mermaid 数量、表格行数和 `mini/` 最小复现引用是否一致。

本项目也可以用 mdBook 发布到 GitHub Pages：

```bash
python3 scripts/prepare_mdbook_site.py
mdbook build
```

部署细节见 [docs/deploy-pages.md](./docs/deploy-pages.md)。

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
第 9 天：读边界课，确认 JCode 和几个 coding-agent runtime 的取舍
```

这个节奏不是硬性安排。重点是不要跳过前四课直接冲 swarm 和 self-dev。那样很容易只记住名词，看不懂运行时边界。

后面想动手改代码时，建议选一个小改造：

- 新增一个只读工具，比如 `repo_summary`。
- 写一套 OpenAI-compatible provider profile 配置和 smoke test 文档。
- 做一个 side panel 工作流。
- 写一份 JCode / OpenCode / pi 的源码级边界说明。
- 给 memory/session search 写一个实际用例。

## 源码来源

本教程基于这些仓库的源码阅读。主要分析对象是 JCode `e353796c62f8eab5b9a9b3722c06a3b262e24a25`。

- [JCode](https://github.com/1jehuang/jcode)
- [pi-mono](https://github.com/badlogic/pi-mono)
- [OpenCode](https://github.com/anomalyco/opencode)

完整 revision 见 [docs/sources.md](./docs/sources.md)。

关于 Claude Code：本教程只在边界课里参考公开行为，不使用、不传播、不复述任何非公开或泄露源码。
