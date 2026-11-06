# Ticket split with `acli` (Jira)

## Detect

- `command -v acli` succeeds and `acli jira auth status` prints
  `Authenticated`. The `Site:` line gives the base URL.
- A ticket key is known: from the branch name, the PR title or body, or the
  user. Without a key, ask; without `acli`, keep everything in the PR.
- Read the ticket first (`acli jira workitem view KEY`,
  `acli jira workitem comment list --key KEY --json`). Reuse an earlier
  comment of this kind instead of adding a second one, and do not repeat what
  the ticket already says.

## Format

Jira comments take Atlassian Document Format (ADF), not Markdown. Write the
ticket sections in Markdown, then convert:

```bash
python3 <this skill's folder>/scripts/md-to-adf.py ticket.md > ticket.json
```

`<details>` becomes an expand block; tables, lists, bold, code and links
convert.

## Post or update the comment

```bash
acli jira workitem comment create --key KEY --body-file ticket.json --json
acli jira workitem comment update --key KEY --id COMMENT_ID --body-adf ticket.json
```

Use `update` when an earlier comment exists, so a rerun after the PR changes
does not add a new one. Link the comment from the PR as
`https://<site>/browse/KEY?focusedCommentId=COMMENT_ID`.

## Follow-up tickets

For each follow-up, search for an existing ticket first:

```bash
acli jira workitem search --jql 'project = PROJ AND statusCategory != Done AND text ~ "keyword"' --limit 5
```

Show the user one line per candidate (summary, why it can wait, possible
duplicates) and create only the ones they pick:

```bash
acli jira workitem create --project PROJ --type Task --summary "..." --description-file followup.json
```

Mention the source ticket and PR in the description. Then list the created
keys in the ticket comment's Follow-ups section.
