"""Count log levels and print the most frequent lines."""

import re
import sys
from collections import Counter
from pathlib import Path

LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
LEVEL_RE = re.compile(r"\b(" + "|".join(LEVELS) + r")\b")
STACK_RE = re.compile(r"^\s+at |^\s+\S+\(")


def analyze(path):
    level_counts = Counter()
    line_counts = Counter()
    stack_lines = 0
    for line in path.open(errors="replace"):
        line = line.rstrip("\n")
        if STACK_RE.match(line):
            # guard: skip stack-trace frames so they do not dominate
            stack_lines += 1
            continue
        match = LEVEL_RE.search(line)
        if match:
            level_counts[match.group(1)] += 1
        line_counts[line] += 1
    return level_counts, line_counts, stack_lines


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "app.log"
    path = Path(target)
    if not path.exists():
        print(f"no such file: {target}")
        return 1

    levels, lines, stack_lines = analyze(path)
    print("level counts:")
    for level in LEVELS:
        if levels[level]:
            print(f"  {level:<8} {levels[level]}")
    if stack_lines:
        print(f"  (skipped {stack_lines} stack-trace lines)")

    print("\nmost frequent lines:")
    for line, count in lines.most_common(10):
        print(f"  {count:>5}  {line[:100]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

