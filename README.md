# pr-overview

Claude Code skill that writes the description of a large pull request as a review guide, not a changelog.

Upgrades, releases and broad refactors produce PRs nobody can read line by line. Left alone, an agent describes them commit by commit. This skill asks for a triage instead, in this order:

1. **Summary**: what moves, in 2-4 sentences, with a link to the detailed report if there is one.
2. **Not worth reviewing line by line**: the categories of mechanical change (lock files, scaffold, deprecation fixes, tool-written config).
3. **Worth a look in review**: a short `Change | Why` table, where the why is the concrete consequence.
4. **Manual testing** on the pre-production environment, grouped by user-facing area.
5. **Production deploy: attention points**: order, infrastructure changes, the noise that is expected after the deploy, anything irreversible.
6. **Follow-up release**, when the PR schedules one.

See [`skills/pr-overview/example.md`](skills/pr-overview/example.md) for a complete description.

## Install

In Claude Code:

```
/plugin install pr-overview --marketplace colorfield/claude-pr-overview
```

## Use

Ask for a high-level overview of a PR, or type `/pr-overview`. Claude also reaches for it when it writes the description of a PR that is too large to review line by line.

The skill writes the body; it does not open the PR. Point it at an existing PR to rewrite its description.

## With other PR skills

Other skills may also trigger on "write a PR description" (for example one that asks for Summary, Evidence and Merge Danger). This one is scoped to large PRs. If both load, say which one you want, or settle it in your project's agent instructions.
