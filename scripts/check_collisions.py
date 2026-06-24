#!/usr/bin/env python3
"""Flag skills whose descriptions are too similar — the anti-drift guard.

Overlapping descriptions cause the wrong skill to trigger. This compares every
pair of skill descriptions (in skills/ only — experimental/ is excluded since
WIP skills aren't wired into triggering) and fails if any pair exceeds the
similarity threshold.

Pure stdlib (difflib). Tune THRESHOLD if it's too strict/loose.
"""
import os
import re
import sys
from difflib import SequenceMatcher

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(ROOT, "skills")
THRESHOLD = 0.80  # ratio above this between two descriptions => flagged


def get_description(skill_dir):
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return None
    block = text.split("---", 2)[1]
    for line in block.splitlines():
        if line.strip().startswith("description:"):
            return line.partition(":")[2].strip()
    return None


def normalize(s):
    return re.sub(r"\s+", " ", s.lower()).strip()


def main():
    skills = {}
    if os.path.isdir(SKILLS_DIR):
        for entry in sorted(os.listdir(SKILLS_DIR)):
            d = os.path.join(SKILLS_DIR, entry)
            if os.path.isdir(d):
                desc = get_description(d)
                if desc:
                    skills[entry] = normalize(desc)

    names = list(skills)
    collisions = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            ratio = SequenceMatcher(None, skills[a], skills[b]).ratio()
            if ratio >= THRESHOLD:
                collisions.append((a, b, ratio))

    if collisions:
        print("Description collision check FAILED:\n")
        for a, b, r in collisions:
            print(f"  - '{a}' and '{b}' are {r:.0%} similar (threshold {THRESHOLD:.0%})")
        print("\nMake their descriptions more distinct so the right skill triggers.")
        sys.exit(1)
    print(f"Collision check passed: {len(names)} skill(s), no overlapping descriptions.")


if __name__ == "__main__":
    main()
