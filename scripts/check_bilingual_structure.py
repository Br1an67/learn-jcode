#!/usr/bin/env python3
"""Check that Chinese and English docs keep the same structural shape."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ZH_DIR = ROOT / "docs" / "zh"
EN_DIR = ROOT / "docs" / "en"

MINI_REF_RE = re.compile(r"mini/[A-Za-z0-9_.\-/]+")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\|.*\|$", re.MULTILINE)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lesson_files(directory: Path) -> dict[str, Path]:
    return {path.name: path for path in sorted(directory.glob("*.md"))}


def heading_levels(text: str) -> list[int]:
    return [len(match.group(1)) for match in HEADING_RE.finditer(text)]


def code_fence_languages(text: str) -> list[str]:
    languages: list[str] = []
    in_fence = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("```"):
            continue
        if not in_fence:
            language = line[3:].strip().split(maxsplit=1)[0] if line[3:].strip() else ""
            languages.append(language)
            in_fence = True
        else:
            in_fence = False
    return languages


def mini_refs(text: str) -> list[str]:
    return sorted(set(MINI_REF_RE.findall(text)))


def table_row_count(text: str) -> int:
    return len(TABLE_ROW_RE.findall(text))


def compare_pair(label: str, zh_text: str, en_text: str) -> list[str]:
    errors: list[str] = []

    zh_headings = heading_levels(zh_text)
    en_headings = heading_levels(en_text)
    if zh_headings != en_headings:
        errors.append(
            f"{label}: heading level sequence differs: zh={zh_headings} en={en_headings}"
        )

    zh_fences = code_fence_languages(zh_text)
    en_fences = code_fence_languages(en_text)
    if zh_fences != en_fences:
        errors.append(f"{label}: code fence languages differ: zh={zh_fences} en={en_fences}")

    zh_mini = mini_refs(zh_text)
    en_mini = mini_refs(en_text)
    if zh_mini != en_mini:
        errors.append(f"{label}: mini references differ: zh={zh_mini} en={en_mini}")

    zh_tables = table_row_count(zh_text)
    en_tables = table_row_count(en_text)
    if zh_tables != en_tables:
        errors.append(f"{label}: table row count differs: zh={zh_tables} en={en_tables}")

    return errors


def main() -> int:
    errors: list[str] = []

    zh_files = lesson_files(ZH_DIR)
    en_files = lesson_files(EN_DIR)
    if set(zh_files) != set(en_files):
        errors.append(
            "docs file set differs: "
            f"zh_only={sorted(set(zh_files) - set(en_files))} "
            f"en_only={sorted(set(en_files) - set(zh_files))}"
        )

    for name in sorted(set(zh_files) & set(en_files)):
        errors.extend(compare_pair(f"docs/{name}", read(zh_files[name]), read(en_files[name])))

    root_pairs = [(ROOT / "README.md", ROOT / "README-en.md")]
    for zh_path, en_path in root_pairs:
        errors.extend(compare_pair(zh_path.name, read(zh_path), read(en_path)))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    checked = len(set(zh_files) & set(en_files)) + len(root_pairs)
    print(f"OK: bilingual structure matches for {checked} document pairs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
