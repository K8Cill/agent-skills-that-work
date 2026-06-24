---
name: skill-authoring
description: Create, edit, and validate agent skills for the agent-skills-that-work library following this repo's conventions. Use this whenever the user wants to add a new skill, scaffold a SKILL.md, improve an existing skill's description or trigger reliability, or check a skill against the repo standard — even if they don't explicitly say "skill". Always use this before adding anything to skills/ or experimental/.
---

# Skill Authoring (agent-skills-that-work)

The house style for building skills in this repository. Read `CLAUDE.md` at the repo root first — it holds the binding rules. This skill is the workflow on top of them.

## When to use

- "Add a skill for X" / "make a skill that does Y"
- "Scaffold a new skill" / "turn this into a skill"
- "Improve this skill's description" / "why isn't this skill triggering"
- Auditing or cleaning up an existing `SKILL.md`

## Workflow

1. **Capture intent.** What should the skill do? When should it trigger (exact user phrases/contexts)? What's the output? Pull answers from the conversation before asking.

2. **Scaffold.** Copy `template/` to `experimental/<skill-name>/`. New skills start in `experimental/`, never directly in `skills/`.

3. **Write the description first.** This is the product — it's the only part loaded at discovery, and it alone decides whether the skill triggers. Use the Trigger Triad:
   - **Capability** — verb + object ("Generates X", "Audits Y").
   - **When to use** — the contexts and phrases that should fire it.
   - **Pushiness** — agents under-trigger; add "use this whenever… even if they don't explicitly say…".
   Rewrite it 3–4 times before touching the body. Keep it distinct from every existing skill's description (overlap = wrong skill fires).

4. **Write the body.** Keep under ~5,000 tokens. Push detail into `references/`. Scripts for deterministic steps go in `scripts/`.

5. **Validate.** Run the repo validators (see `scripts/`) before promoting:
   - frontmatter present, `name` matches folder, ≤64 chars, lowercase-hyphen
   - description ≤1024 chars, no angle brackets
   - no trigger collision with existing skills

6. **Test triggering (recommended).** Use the `skill-creator` skill's eval loop to measure trigger rate against realistic prompts. Substantive, multi-step prompts test triggering meaningfully; trivial one-liners don't.

7. **Promote.** Once the trigger and behavior are validated, move the folder from `experimental/` to `skills/`. Commit.

## Guidelines

- One skill = one concern. If it does two things, split it.
- Don't edit a sibling skill's description as a side effect — re-check collisions if you do.
- Behavior-shaping wording is load-bearing. Don't reword a working skill without a reason.
- Zero unnecessary runtime dependencies.

## References

- Repo conventions: `../../CLAUDE.md`
- Seed: `../../template/SKILL.md`
- Validators: `../../scripts/`
