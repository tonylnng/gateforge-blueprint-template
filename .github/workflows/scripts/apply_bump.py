#!/usr/bin/env python3
"""
Apply a version bump:
  1. Update VERSION
  2. Move accumulated [Unreleased] entries into a new dated section
  3. Append the new section's bullets from the current push
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path

UNRELEASED_RE = re.compile(r"(^## \[Unreleased\][^\n]*\n)(.*?)(?=^## \[)", re.DOTALL | re.MULTILINE)


def read_version() -> tuple[int, int, int]:
    raw = Path("VERSION").read_text().strip()
    M, m, p = raw.split(".")
    return int(M), int(m), int(p)


def bump_version(current: tuple[int, int, int], kind: str) -> str:
    M, m, p = current
    if kind == "major":
        return f"{M + 1}.0.0"
    if kind == "minor":
        return f"{M}.{m + 1}.0"
    if kind == "patch":
        return f"{M}.{m}.{p + 1}"
    raise SystemExit(f"::error::Unknown bump kind: {kind}")


def render_section(version: str, date: str, sections: dict[str, list[str]]) -> str:
    """Render a CHANGELOG section. Empty sections are omitted."""
    order = ["Added", "Changed", "Deprecated", "Removed", "Fixed", "Security",
             "Deployed", "Tests", "Docs", "Chore"]
    lines = [f"## [{version}] - {date}", ""]
    emitted = False
    for name in order:
        bullets = sections.get(name, [])
        if not bullets:
            continue
        emitted = True
        lines.append(f"### {name}")
        for b in bullets:
            lines.append(f"- {b}")
        lines.append("")
    if not emitted:
        lines.append("### Chore")
        lines.append("- Version bump (no user-facing changes)")
        lines.append("")
    return "\n".join(lines)


def update_changelog(new_version: str, sections: dict[str, list[str]]) -> None:
    path = Path("CHANGELOG.md")
    if not path.exists():
        print("::error::CHANGELOG.md is missing", file=sys.stderr)
        sys.exit(1)
    text = path.read_text()
    today = _dt.date.today().isoformat()
    new_section = render_section(new_version, today, sections)

    # Find the line that introduces the next existing version (or end-of-file)
    # and insert the new section directly after the [Unreleased] block.
    marker = "## [Unreleased]"
    if marker not in text:
        # Fallback: prepend the new section just under the H1.
        lines = text.splitlines(keepends=True)
        out = []
        inserted = False
        for line in lines:
            out.append(line)
            if not inserted and line.startswith("# "):
                out.append("\n" + new_section + "\n")
                inserted = True
        path.write_text("".join(out))
        return

    # Replace [Unreleased] block: keep [Unreleased] header but reset bullets,
    # and insert the new dated section directly after.
    pattern = re.compile(
        r"(## \[Unreleased\][^\n]*\n)(.*?)(?=^## \[|\Z)",
        re.DOTALL | re.MULTILINE,
    )
    def repl(m: re.Match) -> str:
        header = m.group(1)
        # Reset Unreleased to placeholder template
        reset = (
            "\n"
            "### Added\n- [PLACEHOLDER — New features added since last release]\n\n"
            "### Changed\n- [PLACEHOLDER — Changes to existing functionality]\n\n"
            "### Fixed\n- [PLACEHOLDER — Bug fixes]\n\n"
            "### Security\n- [PLACEHOLDER — Security-related changes]\n\n"
            "---\n\n"
        )
        return header + reset + new_section + "\n\n---\n\n"

    new_text, n = pattern.subn(repl, text, count=1)
    if n != 1:
        print("::error::Could not locate [Unreleased] section", file=sys.stderr)
        sys.exit(1)
    path.write_text(new_text)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bump", required=True, choices=["major", "minor", "patch"])
    ap.add_argument("--sections-json", required=True)
    args = ap.parse_args()

    sections = json.loads(args.sections_json)
    new_version = bump_version(read_version(), args.bump)
    Path("VERSION").write_text(new_version + "\n")
    update_changelog(new_version, sections)
    print(f"Bumped to {new_version}")


if __name__ == "__main__":
    main()
