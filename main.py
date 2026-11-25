#!/usr/bin/env python3
"""Fridge Roast: One Line, Biggest Laugh.

Writes a single roast line about a smart fridge to /output/entry.txt.

Pure Python standard library only; deterministic: the same bytes are
written on every run.
"""

import os

# Candidate roast lines, strongest first by construction. The picker below
# scores each one and takes the best, so the choice is deterministic and
# auditable instead of a bare constant.
CANDIDATES = [
    # Fresh angle: a fridge stuffed with tech that still cannot do the one
    # job a fridge exists for -- make ice. Dodges the obvious milk-expiry
    # and "update to open the door" cracks.
    "My smart fridge has Wi-Fi, a touchscreen, and a camera inside \u2014 "
    "and after six years of firmware updates it still can't make one "
    "cube of ice.",
    # Runner-up: the fridge scolds you while its own hardware is broken.
    "My smart fridge's ice maker died two years ago and its camera fogs "
    "up, yet it still beeps at me like I'm the one that's broken.",
]

# Judge-brief weights: specificity to smart fridges matters most after the
# punchline, so fridge-specific words earn the most.
SPECIFIC_WORDS = ("wi-fi", "touchscreen", "camera", "firmware", "ice")


def score_line(line):
    """Deterministic score: fridge-specific words, then tightness."""
    words = line.lower()
    hits = sum(1 for w in SPECIFIC_WORDS if w in words)
    # Prefer lines that land their turn late (punchline at the end) and
    # stay well inside the 200-character cap.
    return (hits, -abs(len(line) - 140), -len(line))


def pick_line(candidates):
    """Pick the highest-scoring candidate; ties break by list order."""
    best = None
    best_score = None
    for line in candidates:
        s = score_line(line)
        if best_score is None or s > best_score:
            best, best_score = line, s
    return best


ENTRY = pick_line(CANDIDATES)

OUTPUT_PATH = "/output/entry.txt"


def validate(line):
    """Gate check, mirroring the competition gate: 1-200 chars, not blank."""
    if not isinstance(line, str):
        raise TypeError("entry must be a string")
    if not (1 <= len(line) <= 200):
        raise ValueError("entry must be 1-200 characters, got %d" % len(line))
    if not line.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    line.encode("utf-8")  # must be valid UTF-8
    return line


def write_entry(path=OUTPUT_PATH):
    line = validate(ENTRY)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    return line


def main():
    line = write_entry()
    print("Wrote %d characters to %s" % (len(line), OUTPUT_PATH))


if __name__ == "__main__":
    main()
