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

### `agents/`

`learn-claude-code` has runnable miniature agents because it teaches harness mechanisms by implementing them from scratch.

This project studies JCode itself, so the main course stays source-first. If we add miniature code, it should be a small mechanism specimen that clarifies JCode concepts, not a detached exercise track.

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
├── docs/
│   ├── zh/
│   │   ├── README.md
│   │   └── s01...s09
│   ├── en/
│   │   ├── README.md
│   │   └── s01...s09
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
