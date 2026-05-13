#!/usr/bin/env python3
"""
Decide which version segment to bump based on the commits in the pushed range.

Outputs (to GITHUB_OUTPUT):
  bump_type:          one of: none | patch | minor | major
  new_version:        the new version string
  changelog_sections: JSON {section_name: [bullet, ...]}

Rules (see VERSIONING.md):
  - 'Version-Bump: major' trailer + author == RELEASE_OWNER_LOGIN  -> MAJOR
  - any 'feat' commit                                     -> MINOR (resets PATCH=0)
  - otherwise (fix/refactor/test/deploy/docs/chore)       -> PATCH
  - bot's own commits are filtered out
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

# Preferred format: '[<Agent>] <type>(<scope>)?: <subject>'
# Also accepted (plain Conventional Commits, no Agent prefix): '<type>(<scope>)?: <subject>'
COMMIT_PREFIX_RE = re.compile(
    r"^(?:\[(?P<agent>[A-Za-z]+)\]\s+)?"
    r"(?P<type>feat|fix|refactor|test|deploy|docs|chore|perf|style|ci|build)"
    r"(?P<scope>\([^)]+\))?"
    r"!?:\s+(?P<subject>.+)$"
)
TRAILER_RE = re.compile(r"^Version-Bump:\s*(major)\s*$", re.IGNORECASE)
SECURITY_SCOPE_RE = re.compile(r"^\(security\)$", re.IGNORECASE)

TYPE_TO_SECTION = {
    "feat": "Added",
    "fix": "Fixed",
    "refactor": "Changed",
    "test": "Tests",
    "deploy": "Deployed",
    "docs": "Docs",
    "chore": "Chore",
}


def run(cmd: list[str]) -> str:
    return subprocess.check_output(cmd, text=True).strip()


def commits_in_range(before: str, after: str) -> list[dict]:
    """Return list of commits in (before..after], excluding bot commits and merges."""
    if before == "0000000000000000000000000000000000000000":
        # New branch push — fall back to comparing to default branch.
        rev_range = after
    else:
        rev_range = f"{before}..{after}"

    fmt = "%H%x1f%an%x1f%ae%x1f%s%x1f%B%x1e"
    raw = run(["git", "log", "--no-merges", f"--format={fmt}", rev_range])
    commits: list[dict] = []
    for entry in raw.split("\x1e"):
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split("\x1f")
        if len(parts) < 5:
            continue
        sha, name, email, subject, body = parts[0], parts[1], parts[2], parts[3], parts[4]
        if name == "github-actions[bot]" or email.endswith("[bot]@users.noreply.github.com"):
            continue
        if "[skip version-bump]" in body:
            continue
        commits.append(
            {"sha": sha, "name": name, "email": email, "subject": subject, "body": body}
        )
    return commits


def has_major_trailer(commits: list[dict], actor: str, release_owner: str) -> bool:
    if actor != release_owner:
        return False
    for c in commits:
        for line in c["body"].splitlines():
            if TRAILER_RE.match(line.strip()):
                return True
    return False


# Map non-bump-affecting types to bump-affecting equivalents for the version-bump decision.
# perf -> patch, style -> patch, ci -> patch, build -> patch (treated as 'chore').
TYPE_NORMALISE = {
    "perf": "refactor",
    "style": "chore",
    "ci": "chore",
    "build": "chore",
}


def parse_commit(subject: str) -> dict | None:
    m = COMMIT_PREFIX_RE.match(subject.strip())
    if not m:
        return None
    raw_type = m.group("type").lower()
    norm_type = TYPE_NORMALISE.get(raw_type, raw_type)
    return {
        "agent": m.group("agent") or "contributor",
        "type": norm_type,
        "scope": (m.group("scope") or "").strip(),
        "subject": m.group("subject").strip(),
    }


def decide(commits: list[dict], major_requested: bool) -> tuple[str, dict]:
    parsed: list[dict] = []
    unparsed: list[str] = []
    for c in commits:
        p = parse_commit(c["subject"])
        if p is None:
            unparsed.append(c["subject"])
        else:
            parsed.append(p)

    if unparsed:
        # Don't block CI — emit a warning and treat unparseable commits as PATCH (chore).
        # Hard rejection here is too brittle: a single non-conforming commit would
        # permanently break the auto-bump pipeline. A warning preserves traceability
        # while letting the bump proceed.
        print(
            "::warning::Found commits that do not match the preferred format "
            "'[<Agent>] <type>(<scope>)?: <subject>'. Treating as PATCH (chore):\n  - "
            + "\n  - ".join(unparsed),
            file=sys.stderr,
        )
        for subj in unparsed:
            parsed.append(
                {
                    "agent": "contributor",
                    "type": "chore",
                    "scope": "",
                    "subject": subj,
                }
            )

    if not parsed:
        return "none", {}

    if major_requested:
        bump = "major"
    elif any(p["type"] == "feat" for p in parsed):
        bump = "minor"
    else:
        bump = "patch"

    sections: dict[str, list[str]] = defaultdict(list)
    for p in parsed:
        section = TYPE_TO_SECTION.get(p["type"], "Chore")
        if SECURITY_SCOPE_RE.match(p["scope"]):
            section = "Security"
        sections[section].append(f"[{p['agent']}] {p['subject']}")

    return bump, dict(sections)


def read_version() -> tuple[int, int, int]:
    raw = Path("VERSION").read_text().strip()
    parts = raw.split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        print(f"::error::Malformed VERSION file: {raw!r}", file=sys.stderr)
        sys.exit(1)
    return int(parts[0]), int(parts[1]), int(parts[2])


def bump_version(current: tuple[int, int, int], kind: str) -> str:
    M, m, p = current
    if kind == "major":
        return f"{M + 1}.0.0"
    if kind == "minor":
        return f"{M}.{m + 1}.0"
    if kind == "patch":
        return f"{M}.{m}.{p + 1}"
    return f"{M}.{m}.{p}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--actor", required=True)
    ap.add_argument(
        "--release-owner",
        dest="release_owner",
        required=True,
        help="GitHub login of the End-user (release owner) who alone may trigger a MAJOR bump",
    )
    args = ap.parse_args()

    commits = commits_in_range(args.before, args.after)
    if not commits:
        print("bump_type=none")
        print("new_version=")
        print("changelog_sections={}")
        return

    major_req = has_major_trailer(commits, args.actor, args.release_owner)
    bump_type, sections = decide(commits, major_req)
    if bump_type == "none":
        print("bump_type=none")
        print("new_version=")
        print("changelog_sections={}")
        return

    new_version = bump_version(read_version(), bump_type)
    print(f"bump_type={bump_type}")
    print(f"new_version={new_version}")
    # Single-line JSON, safe for $GITHUB_OUTPUT.
    print("changelog_sections=" + json.dumps(sections, separators=(",", ":")))


if __name__ == "__main__":
    main()
