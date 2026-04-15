#!/usr/bin/env python3
"""
Terminology lint — flag mis-use of 'raise' for opens or first postflop bets.

Rules:
- "preflop: X raise" or "preflop X raises" → should be "X opens"
- The first action on flop/turn/river that uses 'raise' (with no prior bet on that street) → should be "bets"

Run before publishing any review/comms doc or solver HTML.
"""
import sys, re, glob

PROBLEMS = []

PREFLOP_OPEN_PATTERNS = [
    re.compile(r"preflop:\s*(UTG|HJ|CO|BTN|SB|BB)\s+raises?\b", re.I),
    re.compile(r"preflop\s+(UTG|HJ|CO|BTN|SB|BB)\s+raises?\b", re.I),
]

# Heuristic: street: <seat> raise / raises with no prior bet keyword on the same line
STREET_OPEN_RAISE = re.compile(
    r"(flop|turn|river):\s*(UTG|HJ|CO|BTN|SB|BB)\s+raises?\b(?![^\n]*\bbet\b)",
    re.I
)

def lint_file(path):
    with open(path) as f:
        text = f.read()
    for line_no, line in enumerate(text.split('\n'), 1):
        for p in PREFLOP_OPEN_PATTERNS:
            if p.search(line):
                PROBLEMS.append((path, line_no, "preflop 'raise' should be 'opens'", line.strip()[:120]))
        m = STREET_OPEN_RAISE.search(line)
        if m:
            PROBLEMS.append((path, line_no, f"{m.group(1)}: '{m.group(2)} raise' likely should be '{m.group(2)} bets'", line.strip()[:120]))

if __name__ == "__main__":
    paths = sys.argv[1:] or glob.glob("review/comms/*.md") + glob.glob("review/comms/*.html")
    for p in paths:
        lint_file(p)
    if PROBLEMS:
        print(f"❌ {len(PROBLEMS)} terminology issue(s) found:")
        for p, n, msg, snip in PROBLEMS:
            print(f"  {p}:{n}  {msg}\n    > {snip}")
        sys.exit(1)
    print(f"✓ No terminology issues found across {len(paths)} files.")
