[中文](./README.md) | [English](./README-en.md)

# Learn JCode 5.5

This is a JCode source-reading course for engineers. The tone is code walkthrough, not product brochure.

The reader is assumed to know roughly what an agent loop is, but not yet how a product-grade coding-agent harness is built. You are not here to read feature praise; you are here to understand why JCode needs a server, tool registry, provider layer, sessions, TUI, memory, and swarm runtime.

Writing rules live in [docs/writing-style.md](./docs/writing-style.md). New lessons should follow that guide.

## Who This Is For

This is for readers who already know roughly what an agent loop is and want to understand:

- Why does a coding agent need a resident server?
- How does a tool result return to model context?
- Why do provider, auth, and session layers get complicated?
- Why is TUI part of the harness instead of decoration?
- What problems do memory, swarm, ambient, and self-dev solve?
- Where does JCode sit among coding-agent runtimes?

If agents are completely new to you, read a minimal agent-loop demo first, then come back to JCode.

## Project Structure

```text
learn-jcode-5.5/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml  # GitHub Pages deployment
├── book.toml                 # mdBook configuration
├── README.md                 # Chinese entry
├── README-en.md              # English entry
├── mermaid.min.js            # local Mermaid runtime for mdBook
├── mermaid-init.js           # mdBook Mermaid rendering
├── mini/                     # reduced mechanism specimens, not a task track
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
│   ├── check_bilingual_structure.py # bilingual structure drift check
│   └── prepare_mdbook_site.py       # generate temporary mdBook source
├── theme/
│   └── custom.css             # lightweight mdBook styling
├── docs/
│   ├── zh/                   # Chinese lesson docs
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
│   ├── analysis-notes.md     # JCode content analysis and tradeoff notes
│   ├── deploy-pages.md       # GitHub Pages deployment notes
│   ├── glossary.md           # Term glossary
│   ├── project-structure.md  # Why the repository is organized this way
│   ├── sources.md            # Source repositories and revisions
│   └── writing-style.md      # Writing tone and banned expressions
└── .gitignore
```

This course is not building a toy agent from scratch; it is reading JCode itself. Things readers need to know are written directly into the lessons, not moved into a separate hands-on area.

`mini/` contains eight reduced specimens for server/client, tool registry, provider stream, memory sidecar, session journal, swarm channel, ambient scheduler, and self-dev reload gate. They are not another task track; they reduce the cognitive load before reading JCode source.

## Lessons

Read in order, one or two lessons per day.

| Lesson | 中文 | English |
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

If a lesson's source path feels too large, read the corresponding specimen in [mini/](./mini/README.md), then return to the lesson.

## Maintenance Check

When editing Chinese and English lessons, run the structure check first:

```bash
python3 scripts/check_bilingual_structure.py
```

This script only catches structure drift; it does not judge translation quality. It checks file sets, heading levels, code fence languages, Mermaid counts, table rows, and `mini/` specimen references.

This project can also be published to GitHub Pages with mdBook:

```bash
python3 scripts/prepare_mdbook_site.py
mdbook build
```

Deployment details are in [docs/deploy-pages.md](./docs/deploy-pages.md).

## Suggested Pace

Do not treat JCode as a one-day cram project.

```text
Day 0: run it and authenticate one provider
Day 1: read startup and server/client
Day 2: read the agent loop
Day 3: read the tool registry
Day 4: read provider/auth/session
Day 5: read TUI and observability
Day 6: read memory
Day 7: read swarm
Day 8: read ambient/self-dev
Day 9: read the boundaries lesson and check JCode tradeoffs among coding-agent runtimes
```

This is not a strict schedule. The point is: do not skip the first four lessons and jump straight into swarm or self-dev. You will collect names without understanding runtime boundaries.

For a real project, pick one small modification:

- Add a read-only tool, such as `repo_summary`.
- Write OpenAI-compatible provider profile setup and smoke-test docs.
- Build a side-panel workflow.
- Write a source-level boundary note for JCode / OpenCode / pi.
- Document a real memory/session-search use case.

## Source Repositories

This tutorial is based on source reading of these repositories. The main JCode revision analyzed here is `e353796c62f8eab5b9a9b3722c06a3b262e24a25`.

- [JCode](https://github.com/1jehuang/jcode)
- [pi-mono](https://github.com/badlogic/pi-mono)
- [OpenCode](https://github.com/anomalyco/opencode)

Full revisions are listed in [docs/sources.md](./docs/sources.md).

For Claude Code, this tutorial only references public behavior in the boundaries lesson. It does not use, distribute, or summarize non-public or leaked source code.
