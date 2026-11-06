---
name: pr-overview
description: Use when writing or updating the description of a large pull request that reviewers cannot read line by line (framework or dependency upgrade, release, migration, broad refactor), or when asked for a high-level PR overview, a review guide, what to test manually, or what to watch when deploying.
---

# PR overview

## Overview

A large PR needs a description that triages, not a changelog. The reviewer
should know in two minutes what to skip, what to read, what to click through on
a test environment and what to watch in production. The full detail lives in
the commits or a linked report; the description points to it.

## The description, in this order

1. **Ticket link** on the first line, as a Markdown link, when there is a
   ticket.
2. **`## Summary`**: 2-4 sentences. The headline moves only (the main
   framework, runtime or component, and the one behaviour change users or
   operators will notice), then one line on side benefits (security fixes,
   audit clean). The list of every bumped package belongs in the report or the
   commits. If the branch has a detailed report or log, link it here with an
   absolute URL.
3. **`## Not worth reviewing line by line`**: 3-6 bullets naming *categories*
   of mechanical change, with a few example paths each: lock files, generated
   or scaffold files, binary artifacts, deprecation fixes, config written by
   tools or update scripts, re-rolled patches, renames.
4. **`## Worth a look in review`**: a two-column table, `Change | Why`, at most
   10 rows. One row per file or area where reviewer judgment adds value:
   deploy or process changes, temporary workarounds, pins to unreleased code,
   deliberate removals, bug fixes that change behaviour, anything touching
   data. The Why column states the concrete consequence or finding ("fails on
   the first deploy", "would delete 4,000 rows"), not a restatement of the
   change.
5. **`## Manual testing on <pre-production environment>`**: bullets grouped by
   user-facing area, each starting with a bold area name, then concrete
   actions and the expected result, with admin paths where they help.
6. **`## <Production> deploy: attention points`**: deploy order and how it was
   rehearsed; infrastructure changes (images, runtimes); post-deploy checks
   with the warnings or drift that are *expected*, so nobody chases them;
   anything irreversible.
7. **`## Follow-up release`** (only when this PR schedules work for the next
   one, such as removing packages it deprecated): one or two lines.

Then the attribution footer, if the environment requires one.

## Size

Each bullet and each table cell is one or two sentences. Lists are flat; the
only nested list is the post-deploy checks. Evidence (test counts, rehearsal
details) gets one clause where it supports a point, not its own paragraph.

## Before publishing

- Check every factual claim against evidence from this session (a path, a
  warning that "will appear", a count). Overviews are read as verified; fix or
  drop anything you inferred.
- If the PR already has a description, read it first and keep what the author
  wrote that this structure has no slot for.
- Write the body to a file and pass it with `--body-file`, not inline.

## Quick reference

| Section | Size | Content |
| --- | --- | --- |
| Summary | 2-4 sentences | what moves, link to report |
| Not worth reviewing | 3-6 bullets | categories of mechanical change |
| Worth a look | ≤10 rows | change, concrete why |
| Manual testing | 4-8 bullets | area, actions, expected result |
| Deploy attention | 3-6 bullets | order, infra, expected noise, irreversible |
| Follow-up release | 1-2 lines | only if scheduled |

See `example.md` for a complete description.
