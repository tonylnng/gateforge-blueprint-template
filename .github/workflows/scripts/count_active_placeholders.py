#!/usr/bin/env python3
"""Count "active" PLACEHOLDER occurrences in a markdown file.

"Active" means PLACEHOLDER occurrences that are NOT inside:
  - HTML comments  (<!-- ... -->)
  - Fenced code blocks (``` ... ``` or ~~~ ... ~~~)

This avoids false positives from instructional text and example fences,
which legitimately mention the word PLACEHOLDER for documentation purposes.

Usage:
    python3 count_active_placeholders.py <path> [head_lines]

If head_lines is 0 or omitted, counts the entire file.
Prints the count to stdout. If the file does not exist, prints 0.
"""
import re
import sys


def count_active_placeholders(path: str, head_lines: int = 0) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except FileNotFoundError:
        return 0

    # Strip HTML comments (multi-line)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    # Strip fenced code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", "", text, flags=re.DOTALL)

    lines = text.splitlines()
    if head_lines > 0:
        lines = lines[:head_lines]
    return sum(line.count("PLACEHOLDER") for line in lines)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: count_active_placeholders.py <path> [head_lines]", file=sys.stderr)
        return 2
    path = sys.argv[1]
    head_lines = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    print(count_active_placeholders(path, head_lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
