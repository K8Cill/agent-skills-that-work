#!/usr/bin/env python3
"""Validate every SKILL.md against the Agent Skills spec + repo rules.

Checks per skill:
  - SKILL.md exists
  - YAML frontmatter present with `name` and `description`
  - name: lowercase letters/digits/hyphens, <=64 chars, no leading/trailing hyphen
  - name matches its parent folder exactly
  - description: <=1024 chars, no angle brackets
  - no angle brackets anywhere in frontmatter

Scans skills/ and experimental/. Exits non-zero on any error.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN_DIRS = ["skills", "experimental"]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(text):
    if not text.startswith("---"):
        return None, "missing opening '---' frontmatter delimiter"
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, "missing closing '---' frontmatter delimiter"
    block = parts[1]
    fm = {}
    for line in block.splitlines():
        line = line.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        fm[key.strip()] = val.strip()
    return fm, block


def check_skill(skill_dir):
    errors = []
    folder = os.path.basename(skill_dir)
    path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(path):
        return [f"{folder}: no SKILL.md found"]

    with open(path, encoding="utf-8") as f:
        text = f.read()

    fm, block = parse_frontmatter(text)
    if fm is None:
        return [f"{folder}: {block}"]

    if "<" in block or ">" in block:
        errors.append(f"{folder}: angle brackets (< or >) in frontmatter are not allowed")

    name = fm.get("name")
    desc = fm.get("description")

    if not name:
        errors.append(f"{folder}: missing required `name` field")
    else:
        if len(name) > 64:
            errors.append(f"{folder}: name exceeds 64 chars")
        if not NAME_RE.match(name):
            errors.append(f"{folder}: name must be lowercase letters/digits/hyphens, no leading/trailing hyphen")
        if name != folder:
            errors.append(f"{folder}: name '{name}' must match folder name '{folder}'")

    if not desc:
        errors.append(f"{folder}: missing required `description` field")
    elif len(desc) > 1024:
        errors.append(f"{folder}: description exceeds 1024 chars ({len(desc)})")

    return errors


def main():
    all_errors = []
    found = 0
    for d in SCAN_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for entry in sorted(os.listdir(base)):
            skill_dir = os.path.join(base, entry)
            if not os.path.isdir(skill_dir):
                continue
            found += 1
            all_errors.extend(check_skill(skill_dir))

    if all_errors:
        print("Skill lint FAILED:\n")
        for e in all_errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"Skill lint passed: {found} skill(s) checked, no issues.")


if __name__ == "__main__":
    main()
