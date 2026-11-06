# pr-overview

Claude Code skill that writes a pull request description as a review guide, not a changelog, and puts the non-code parts where non-developers read them.

Upgrades, releases and broad refactors produce PRs nobody can read line by line. Left alone, an agent describes them commit by commit. This skill asks for a triage instead.

**In the PR**, for code reviewers:

1. **Summary**: what moves, in 2-4 sentences ("am I the right person to review this?").
2. **Worth a look in review**: a short `Change | Why` table, including the judgment calls the agent was unsure about. Ideally short, sometimes empty.
3. **Not worth reviewing line by line**, collapsed: lock files, scaffold, deprecation fixes, tool-written config.

**In the ticket**, for everyone (product, QA, whoever deploys):

4. **Manual testing** on the pre-production environment: steps and expected results.
5. **Production deploy: attention points**: order, infrastructure changes, the noise that is expected after the deploy, anything irreversible.
6. **Follow-ups**, proposed as new tickets so the PR stays focused.

The ticket part needs an authenticated [`acli`](https://developer.atlassian.com/cloud/acli/) (Atlassian CLI) and a ticket key. Without them, everything goes in the PR. A repo's PR template is filled in, not replaced. Every post (PR description, ticket comment, new tickets) is shown as a draft first.

Optionally, the rows of the Worth a look table become inline review comments on the lines they refer to, in one review.

See [`skills/pr-overview/example.md`](skills/pr-overview/example.md) for a complete example.

## Install

In Claude Code:

```
/plugin install pr-overview --marketplace colorfield/claude-pr-overview
```

## Use

Ask for a PR overview or a review guide, or type `/pr-overview`. Point it at an existing PR to rewrite its description.

## With other PR skills

Other skills may also trigger on "write a PR description" (for example one that asks for Summary, Evidence and Merge Danger). If both load, say which one you want, or settle it in your project's agent instructions.
