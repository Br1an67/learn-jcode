# Project Structure Notes

This repository is organized as a source-reading course for JCode. The structure should keep the reading path obvious without making the project look like a second implementation of JCode.

## Shape

The course has four layers:

```text
README.md / README-en.md
docs/zh and docs/en
docs/glossary-style-source notes
mini/
```

The root README should stay short. It explains who should read the course, what order to follow, and where the source revisions are recorded.

Lessons live in `docs/{zh,en}`. Each lesson should be self-contained: a diagram, short code excerpts, and plain explanation. A reader should not need to jump between IDE tabs just to understand the main mechanism.

The `mini/` directory is not a task track. It contains reduced mechanism specimens for parts of JCode that are large in the real source.

## Current Structure

```text
learn-jcode/
├── README.md
├── README-en.md
├── mini/
│   ├── README.md
│   ├── 01_server_client.py
│   ├── 02_tool_registry.py
│   ├── 03_provider_stream.py
│   ├── 04_memory_sidecar.py
│   ├── 05_session_journal.py
│   ├── 06_swarm_channel.py
│   ├── 07_ambient_scheduler.py
│   ├── 08_selfdev_reload_gate.py
│   └── mini_compat.py
├── docs/
│   ├── zh/
│   │   ├── README.md
│   │   ├── 00-map.md
│   │   ├── glossary.md
│   │   └── s01...s10
│   ├── en/
│   │   ├── README.md
│   │   ├── 00-map.md
│   │   ├── glossary.md
│   │   └── s01...s10
│   ├── analysis-notes.md
│   ├── project-structure.md
│   ├── sources.md
│   └── writing-style.md
└── .gitignore
```

## Mini Specimens

Current specimens:

```text
mini/01_server_client.py
mini/02_tool_registry.py
mini/03_provider_stream.py
mini/04_memory_sidecar.py
mini/05_session_journal.py
mini/06_swarm_channel.py
mini/07_ambient_scheduler.py
mini/08_selfdev_reload_gate.py
```

Each file maps to a lesson and removes real provider calls, sockets, and file writes. The point is to preserve the shape of the mechanism without asking the reader to understand the full runtime first.

## Future Additions

If the tutorial grows, add these in this order:

1. More `docs/zh` and `docs/en` lessons when a topic deserves its own page.
2. `assets/` for diagrams and screenshots, only when Mermaid is not enough.
3. `scripts/` for validation or content generation, not unrelated demos.
4. `web/` only after Markdown content is stable and the course needs a presentation layer.

Do not add structure for its own sake. The structure should make the course easier to read.
