# Conventions for agents working in this repo

This file is read by Claude / Codex / Copilot when working inside `agent-skills-that-work`. It defines the rules every skill must follow. Skills are not prose — they are instructions that shape agent behavior, so treat changes with care.

## Maintainer

Solo-maintained by Sasa Vasic (GitHub: `k8cill`). Only the maintainer and his coding agents commit. `main` is branch-protected; all changes land via the maintainer.

## Skill structure

Every skill is a folder under `skills/`:

```text
skills/<skill-name>/
├── SKILL.md        # required
├── references/     # optional — docs loaded on demand
├── scripts/        # optional — executable code
└── assets/         # optional — templates, fonts, icons
```

## SKILL.md rules (enforced by CI)

- **Frontmatter** must contain `name` and `description`, nothing required beyond that.
- **`name`** — lowercase letters, numbers, hyphens only. Must match the folder name exactly. Max 64 chars. No leading/trailing hyphen.
- **`description`** — max 1024 chars. State both *what the skill does* and *when to use it*. No angle brackets (`<` `>`) anywhere in frontmatter.
- **Body** — keep under ~5,000 tokens (roughly 500 lines). Push detail into `references/`.

## The description is the product

At startup the agent only reads each skill's `name` + `description`. The body never loads if the description doesn't match the request. So:

- Write the description to trigger reliably — capability + when-to-use + concrete phrases.
- Be slightly "pushy" about when to use it; agents tend to under-trigger skills.
- Rewrite the description several times before touching the body.
- Keep descriptions distinct from each other. Overlapping descriptions cause the wrong skill to fire. CI flags collisions.

## Progressive disclosure

Three loading levels: metadata (always) → SKILL.md body (on trigger) → bundled resources (as needed). Don't dump everything in the body. Reference files clearly with guidance on when to read them.

## Workflow

- New skills start in `experimental/`. Promote to `skills/` only once the trigger and behavior are validated.
- To keep a skill discoverable-but-hidden from the `skills` CLI, add `metadata.internal: true` to its frontmatter. It then only installs with `INSTALL_INTERNAL_SKILLS=1`. Remove the flag to make it public.
- When promoting a skill to `skills/`, add its path to the `skills` array in `.claude-plugin/marketplace.json`.
- Use the `skill-creator` skill (or its eval loop) to test trigger rate before promoting.
- Run `scripts/` validators locally before pushing if possible — CI runs them anyway.

## Hard rules

- One skill per folder. One concern per skill.
- Don't edit another skill's description without checking it doesn't steal a sibling's triggers.
- Don't add third-party runtime dependencies to a skill unless essential.
