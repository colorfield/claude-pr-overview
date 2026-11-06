---
name: pr-overview
description: Use when writing or updating a pull request description that should guide reviewers, especially for large or mixed changes (framework or dependency upgrade, release, migration, broad refactor), or when asked for a PR overview, a review guide, manual testing steps, deploy notes or follow-up tickets for a PR.
---

# PR overview

## Overview

A PR description triages; it is not a changelog. Code reviewers learn in two
minutes what to read and what to skip. People without access to the code
(product, QA, whoever deploys) get testing steps, deploy notes and follow-ups
where they already work: the ticket. Full detail stays in the commits or a
linked report.

## Where each part goes

| Part | Audience | Goes to |
| --- | --- | --- |
| Summary, Worth a look, Not worth reviewing | code reviewers | PR description |
| Manual testing, Deploy attention points, Follow-ups | everyone | ticket comment, when the ticket split applies; otherwise the PR |

**Ticket split** applies when `acli` is installed and authenticated and a
ticket key is known (branch name, PR title or body, or the user). Read
`jira.md` for the commands. Without it, everything goes in the PR.

## The PR description, in this order

1. **Ticket link** on the first line, as a Markdown link, when there is a
   ticket.
2. **`## Summary`**: 2-4 sentences. The headline moves only (main framework,
   runtime or component; the one behaviour change users or operators will
   notice), then one line on side benefits. Link the detailed report, if the
   branch has one, with an absolute URL. It answers "am I the right person to
   review this?".
3. **`## Worth a look in review`**: table `Change | Why`, at most 10 rows. One
   row per file or area where reviewer judgment adds value: deploy or process
   changes, temporary workarounds, pins to unreleased code, deliberate
   removals, behaviour-changing fixes, anything touching data, and every
   judgment call you were unsure about. The Why is the concrete consequence
   ("fails on the first deploy", "would delete 4,000 rows"). For a small PR
   with nothing risky, write `Nothing needs a closer look.` instead of the
   table.
4. **Not worth reviewing**, collapsed:

   ```markdown
   <details>
   <summary>Not worth reviewing line by line</summary>

   - one line per category of mechanical change, with a few example paths
   </details>
   ```

   Categories: lock files, generated or scaffold files, binary artifacts,
   deprecation fixes, config written by tools or update scripts, re-rolled
   patches, renames. Omit the block when there is nothing mechanical.
5. With the ticket split: one line, `Testing steps, deploy notes and
   follow-ups: [<KEY> comment](<comment URL>)`. Without it, the three ticket
   sections below follow here, with Manual testing inside `<details>`.

When the repo has a PR template (`.github/pull_request_template.md`,
`.github/PULL_REQUEST_TEMPLATE/`, `docs/` or root), fill in its headings in
their order instead of adding new ones for the same purpose: the ticket link
under the heading that asks for related issues (and not on the first line),
Summary under the heading that asks what or why, testing under the heading
that asks how it was tested. Then append Worth a look and the collapsed Not
worth reviewing. Remove the template's HTML comments.

## Ask first

Before drafting the ticket part, ask the user two questions in one message:

1. **Visibility**: public comment, or restricted to a group (list the
   available groups; `jira.md`)?
2. **Where each open point goes**: list every follow-up and finding, one line
   each, with a proposed destination: *task in this ticket*, *deploy
   instruction*, *note*, *check with the PM*, or *new ticket*. Default to
   *check with the PM* for findings unrelated to the PR; propose *new ticket*
   only when the user's process clearly wants one.

## The ticket sections, in this order

The comment starts with a link to the PR.

1. **Manual testing on <pre-production environment>**: bullets grouped by
   user-facing area, each starting with a bold area name, then the steps and
   the expected result. Admin paths where they help.
2. **<Production> deploy: attention points**: deploy order and how it was
   rehearsed; infrastructure changes; post-deploy checks with the warnings or
   drift that are *expected*; anything irreversible.
3. The open points, placed where the user classified them: *deploy
   instructions* and *tasks in this ticket* as bullets in section 2 (a task
   says when it is due, e.g. "next release"), then a **Note** section per
   note, then **To check with the PM: possible follow-ups**, then **Follow-up
   tickets** with the keys of the tickets created (`jira.md`). Omit empty
   sections. Keep all of them out of this PR's scope.

## Size

Each bullet and each table cell is one or two sentences. Lists are flat; the
only nested list is the post-deploy checks. Evidence (test counts, rehearsal
details) gets one clause where it supports a point, not its own paragraph.

## Before publishing

- Check every factual claim against evidence from this session: paths,
  warnings that "will appear", counts. Fix or drop anything inferred.
- For a large PR (dozens of commits or files), have a fresh subagent review
  the draft against `git log` and `git diff --stat` of the branch: it lists
  every claim the commits or the diff do not support, and anything a reviewer
  would need that is missing. Fix those before publishing.
- If the PR already has a description, read it and keep what the author wrote
  that this structure has no slot for.
- Show each outward action as a draft and post it only after the user
  confirms: PR description (`gh pr edit --body-file`), ticket comment, new
  tickets, review comments.

## Review comments (opt-in)

When the PR exists and the user wants it, anchor each Worth a look row to its
lines with a single review of inline comments. Read `review-comments.md`.

See `example.md` for a complete PR description and ticket comment.
