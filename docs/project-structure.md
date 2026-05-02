# Project Structure Notes

This repository borrows the course layout from `/tmp/learn-claude-code`, but adapts it to JCode.

## What We Reuse

`learn-claude-code` uses:

```text
README.md
README-zh.md
docs/en/s01-...
docs/zh/s01-...
agents/s01_...
skills/...
tests/...
web/...
```

For `learn-jcode-5.5`, the useful parts are:

```text
README.md
README-en.md
docs/zh/s01-...
docs/en/s01-...
```

The root README should stay short. Lessons should live in `docs/{zh,en}`.

## What We Do Not Copy Yet

### `mini/`

`learn-claude-code` has runnable miniature agents because it teaches harness mechanisms by implementing them from scratch.

This project studies JCode itself, so the main course stays source-first. The `mini/` directory is intentionally smaller than `learn-claude-code`'s `agents/`: it contains mechanism specimens, not a second course.

Current specimens:

```text
mini/01_server_client.py
mini/02_tool_registry.py
mini/03_provider_stream.py
mini/04_memory_sidecar.py
```

Each file maps to a JCode lesson and removes real provider calls, sockets, and file writes. The goal is to make the mechanism visible before readers return to the JCode source.

### `skills/`

`learn-claude-code` includes skills because part of its course is about skill loading.

This repository can add `skills/` later only if we create actual reusable Codex/JCode learning skills. Do not add placeholder skills just to imitate the shape.

### `web/`

`learn-claude-code` has a web presentation layer. This project should stay Markdown-first until the content stabilizes.

## Current Structure

```text
learn-jcode-5.5/
├── README.md
├── README-en.md
├── mini/
│   ├── README.md
│   ├── 01_server_client.py
│   ├── 02_tool_registry.py
│   ├── 03_provider_stream.py
│   ├── 04_memory_sidecar.py
│   └── mini_compat.py
├── docs/
│   ├── zh/
│   │   ├── README.md
│   │   └── s01...s10
│   ├── en/
│   │   ├── README.md
│   │   └── s01...s10
│   ├── analysis-notes.md
│   ├── project-structure.md
│   ├── sources.md
│   └── writing-style.md
└── .gitignore
```

## Future Additions

If the tutorial grows, add these in this order:

1. More `docs/zh` and `docs/en` lessons when a topic deserves its own page.
2. `assets/` for diagrams and screenshots.
3. `scripts/` only for validation or content generation, not for unrelated demos.
4. `web/` only after Markdown content is stable.

Do not add structure for its own sake. The structure should make the course easier to read.
