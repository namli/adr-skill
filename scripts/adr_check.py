#!/usr/bin/env python3
"""Check a project's decision records.

Usage: python3 -I adr_check.py [PROJECT_ROOT] [--budget BYTES]

Fails (exit 1) when:
- a citation ``ADR-NNNN`` names no record in docs/decisions/;
- docs/DECISIONS.md and docs/decisions/ disagree;
- a record's file number differs from its heading number;
- CLAUDE.md or AGENTS.md exceeds the byte budget.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

SUFFIXES = {
    ".md", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".php", ".py", ".json", ".yaml", ".yml", ".toml", ".sql", ".twig", ".vue",
}
SKIPPED_DIRS = {"node_modules", "vendor", "dist", "build", ".git", ".next", "coverage", "__pycache__", "var", ".cache"}
INSTRUCTIONS = ["AGENTS.md", "CLAUDE.md"]

CITATION = re.compile(r"ADR-\d{4}")
HEADING = re.compile(r"^# (ADR-(\d{4}))\b", re.MULTILINE)
ROW = re.compile(r"\[(ADR-\d{4})\]\(decisions/([^)]+)\)")
FILE_NUMBER = re.compile(r"^(\d{4})-")
IGNORE = "adr-check: ignore"


def records(records_dir: Path) -> tuple[dict[str, str], list[str]]:
    """Map ADR number -> file name. Also return problems found in the records."""
    found: dict[str, str] = {}
    problems: list[str] = []
    for path in sorted(records_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        headings = HEADING.findall(text)
        if not headings:
            problems.append(f"{path.name}: no '# ADR-NNNN — ...' heading")
            continue
        if len(headings) > 1:
            problems.append(f"{path.name}: more than one ADR heading")
        number, digits = headings[0]
        m = FILE_NUMBER.match(path.name)
        if not m or m.group(1) != digits:
            problems.append(f"{path.name}: file number does not match heading {number}")
        if number in found:
            problems.append(f"{path.name}: {number} already defined in {found[number]}")
        found[number] = path.name
    return found, problems


def citations(root: Path) -> list[tuple[str, str]]:
    """Return (site, number) for every ADR citation under root."""
    sites: list[tuple[str, str]] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix not in SUFFIXES:
            continue
        relative = path.relative_to(root)
        if SKIPPED_DIRS & set(relative.parts[:-1]):
            continue
        lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        for lineno, line in enumerate(lines, start=1):
            if IGNORE in line:
                continue
            for number in CITATION.findall(line):
                sites.append((f"{relative}:{lineno}", number))
    return sites


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", nargs="?", default=".", help="project root (default: current directory)")
    parser.add_argument("--budget", type=int, default=40_000, help="byte budget for CLAUDE.md / AGENTS.md (default 40000)")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    records_dir = root / "docs" / "decisions"
    index = root / "docs" / "DECISIONS.md"
    errors: list[str] = []

    if not records_dir.is_dir():
        errors.append(f"missing directory: {records_dir.relative_to(root)}")
    if not index.is_file():
        errors.append(f"missing index: {index.relative_to(root)}")
    if errors:
        print("\n".join(errors))
        return 1

    known, problems = records(records_dir)
    errors += problems

    dangling = [f"{site} cites {number}, which has no record" for site, number in citations(root) if number not in known]
    errors += dangling

    indexed = dict(ROW.findall(index.read_text(encoding="utf-8")))
    for number, file_name in sorted(known.items()):
        if number not in indexed:
            errors.append(f"{number} ({file_name}) is not in docs/DECISIONS.md")
        elif indexed[number] != file_name:
            errors.append(f"{number}: index points at {indexed[number]}, record file is {file_name}")
    for number in sorted(set(indexed) - set(known)):
        errors.append(f"docs/DECISIONS.md lists {number}, but docs/decisions/ has no such record")

    for name in INSTRUCTIONS:
        path = root / name
        if path.is_file():
            size = path.stat().st_size
            if size > args.budget:
                errors.append(f"{name} is {size} bytes, budget is {args.budget}; move decisions into records")

    if errors:
        print("\n".join(errors))
        return 1
    print(f"OK: {len(known)} record(s), index and citations agree")
    return 0


if __name__ == "__main__":
    sys.exit(main())
