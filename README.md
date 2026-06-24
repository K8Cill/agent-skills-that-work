<p align="center">
  <img src="https://shieldcn.dev/header/gradient.svg?title=agent-skills-that-work&subtitle=A%20personal%20agent%20skills%20library%20for%20Claude%2C%20Codex%20%26%20Copilot&theme=violet&font=geist" alt="agent-skills-that-work" />
</p>

<p align="center">
  <a href="https://github.com/k8cill/agent-skills-that-work/blob/main/LICENSE"><img src="https://shieldcn.dev/github/license/k8cill/agent-skills-that-work.svg?variant=secondary" alt="License" /></a>
  <a href="https://github.com/k8cill/agent-skills-that-work/stargazers"><img src="https://shieldcn.dev/github/stars/k8cill/agent-skills-that-work.svg?logo=github" alt="Stars" /></a>
  <a href="https://github.com/k8cill/agent-skills-that-work/commits/main"><img src="https://shieldcn.dev/github/last-commit/k8cill/agent-skills-that-work.svg?variant=secondary" alt="Last commit" /></a>
  <a href="https://github.com/k8cill/agent-skills-that-work/actions"><img src="https://shieldcn.dev/github/ci/k8cill/agent-skills-that-work.svg?statusDot=true" alt="CI" /></a>
</p>

<p align="center">
  <img src="https://shieldcn.dev/badge/Claude-ready-D97757.svg?logo=anthropic&logoColor=fff&split=true" alt="Claude" />
  <img src="https://shieldcn.dev/badge/Codex-ready-000000.svg?logo=openai&logoColor=fff&split=true" alt="Codex" />
  <img src="https://shieldcn.dev/badge/Copilot-ready-000000.svg?logo=githubcopilot&logoColor=fff&split=true" alt="GitHub Copilot" />
  <img src="https://shieldcn.dev/badge/Agent%20Skills-spec-violet.svg?variant=branded" alt="Agent Skills spec" />
</p>

> A curated, version-controlled library of personal agent skills for Claude, Codex, and Copilot — built and maintained by Sasa Vasic ([niceguysash](https://linktr.ee/niceguysash)).

[Agent Skills](https://agentskills.io) are folders of instructions an AI agent loads on demand. Each skill is a `SKILL.md` file plus optional scripts and references. This repo is the source of truth for my personal collection.

## Quick start

### Claude Code

Register this repo as a plugin marketplace, then install:

```bash
/plugin marketplace add k8cill/agent-skills-that-work
/plugin install agent-skills-that-work@agent-skills-that-work
```

### npx skills (Codex, Cursor, OpenCode & 40+ agents)

The [Vercel `skills` CLI](https://github.com/vercel-labs/skills) installs straight from this repo — no registry needed:

```bash
# List every skill in the repo
npx skills add k8cill/agent-skills-that-work --list

# Install one skill, targeting specific agents
npx skills add k8cill/agent-skills-that-work --skill skill-authoring -a codex -a claude-code -y

# Install all skills
npx skills add k8cill/agent-skills-that-work -y
```

### Manual / other agents

```bash
git clone https://github.com/k8cill/agent-skills-that-work.git
```

Then point your agent at the `skills/` folder.

## Repository layout

```text
agent-skills-that-work/
├── .claude-plugin/     # plugin + marketplace metadata (Claude Code + skills CLI)
├── skills/             # stable skills — one folder per skill
├── experimental/       # work-in-progress skills (hidden from discovery)
├── evals/              # trigger-rate tests
├── template/           # starting point for a new skill
├── scripts/            # validators used by CI
├── .github/workflows/  # CI: lint, collision check, manifest validation
└── CLAUDE.md           # conventions for agents working in this repo
```

## Adding a skill

1. Copy `template/` to `skills/<your-skill-name>/`.
2. Fill in the `SKILL.md` frontmatter (`name` must match the folder) and instructions.
3. Add the skill path to the `skills` array in `.claude-plugin/marketplace.json`.
4. Follow the conventions in [`CLAUDE.md`](./CLAUDE.md).
5. Push — CI validates structure, frontmatter, and trigger collisions automatically.

Work-in-progress skills go in `experimental/` (or carry `metadata.internal: true` to stay hidden from discovery) until they earn promotion to `skills/`.

## License

[MIT](./LICENSE) © Sasa Vasic

---

<p align="center">
  <a href="https://linktr.ee/niceguysash"><img src="https://shieldcn.dev/badge/Linktree-niceguysash-39E09B.svg?variant=secondary&logo=linktree" alt="Linktree" /></a>
  <a href="https://x.com/niceguysash"><img src="https://shieldcn.dev/badge/-niceguysash-000000.svg?logo=x" alt="X" /></a>
  <a href="mailto:hi@x00.ai"><img src="https://shieldcn.dev/badge/Email-hi@x00.ai-violet.svg?variant=secondary" alt="Email" /></a>
</p>
