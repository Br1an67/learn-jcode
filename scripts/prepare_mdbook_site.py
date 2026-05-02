#!/usr/bin/env python3
"""Prepare a temporary mdBook source tree from the repo's docs layout."""

from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".mdbook-src"

ZH_LESSONS = [
    ("README.md", "中文入口"),
    ("00-map.md", "00 - 全局地图"),
    ("glossary.md", "术语表"),
    ("s01-harness-mindset.md", "s01 - Harness 心智"),
    ("s02-startup-server.md", "s02 - 启动链路和常驻 Server"),
    ("s03-agent-loop.md", "s03 - Agent Loop"),
    ("s04-tool-system.md", "s04 - 工具系统"),
    ("s05-provider-session.md", "s05 - Provider、Auth、Session"),
    ("s06-tui-observability.md", "s06 - TUI 和可观察性"),
    ("s07-memory.md", "s07 - Memory"),
    ("s08-swarm.md", "s08 - Swarm"),
    ("s09-ambient-selfdev.md", "s09 - Ambient 和 Self-Dev"),
    ("s10-comparison.md", "s10 - 边界课"),
]

EN_LESSONS = [
    ("README.md", "English Entry"),
    ("00-map.md", "00 - Global Map"),
    ("glossary.md", "Glossary"),
    ("s01-harness-mindset.md", "s01 - Harness Mindset"),
    ("s02-startup-server.md", "s02 - Startup and Resident Server"),
    ("s03-agent-loop.md", "s03 - Agent Loop"),
    ("s04-tool-system.md", "s04 - Tool System"),
    ("s05-provider-session.md", "s05 - Provider, Auth, Session"),
    ("s06-tui-observability.md", "s06 - TUI and Observability"),
    ("s07-memory.md", "s07 - Memory"),
    ("s08-swarm.md", "s08 - Swarm"),
    ("s09-ambient-selfdev.md", "s09 - Ambient and Self-Dev"),
    ("s10-comparison.md", "s10 - Boundaries"),
]


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))


def strip_section(text: str, start_heading: str, next_heading: str) -> str:
    start = text.find(start_heading)
    if start == -1:
        return text
    end = text.find(next_heading, start + len(start_heading))
    if end == -1:
        return text[:start].rstrip() + "\n"
    return text[:start].rstrip() + "\n\n" + text[end:].lstrip()


def copy_reader_home(src: Path, dst: Path) -> None:
    text = src.read_text(encoding="utf-8")
    text = strip_section(text, "## 项目结构", "## 课程")
    text = strip_section(text, "## Project Structure", "## Lessons")
    text = strip_section(text, "## 维护检查", "## 推荐学习节奏")
    text = strip_section(text, "## Maintenance Check", "## Suggested Pace")
    dst.write_text(text, encoding="utf-8")


def write_summary() -> None:
    lines = [
        "# Summary",
        "",
        "[首页 / Home](./README.md)",
        "[English Home](./README-en.md)",
        "[机制标本 / Mechanism Specimens](./mini/README.md)",
        "",
        "---",
        "",
        "# 中文课程",
        "",
    ]
    lines.extend(f"- [{title}](./docs/zh/{filename})" for filename, title in ZH_LESSONS)
    lines.extend(
        [
            "",
            "# English Course",
            "",
        ]
    )
    lines.extend(f"- [{title}](./docs/en/{filename})" for filename, title in EN_LESSONS)
    (OUT / "SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    for filename in ["README.md", "README-en.md"]:
        copy_reader_home(ROOT / filename, OUT / filename)
    copy_tree(ROOT / "docs", OUT / "docs")
    copy_tree(ROOT / "mini", OUT / "mini")
    write_summary()

    print(f"Prepared mdBook source at {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
