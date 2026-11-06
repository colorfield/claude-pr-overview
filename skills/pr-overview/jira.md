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

## Visibility

List the groups with `acli jira workitem comment visibility --group` and let
the user pick. `comment create` cannot restrict visibility, so a restricted
comment is posted in two steps, back to back:

1. Check who would be notified: `acli jira workitem view KEY --json --fields
   watches,reporter,assignee`. If people outside the group watch the ticket,
   say so before posting.
2. `comment create` (below), then immediately `comment update --key KEY --id
   COMMENT_ID --body-adf ticket.json --visibility-group GROUP_ID`. It takes
   the group **ID**, not its name.
3. Verify with `acli jira workitem view KEY --json --fields comment`: the
   comment's `visibility.value` is the group. The text preview of
   `comment list` drops lists, so check the stored body there too.

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

`create` does not return the comment ID: read it from `acli jira workitem
comment list --key KEY --json` (the last comment). Use `update` when an
earlier comment exists, so a rerun after the PR changes does not add a new
one; pass `--visibility-group` again on every update of a restricted comment. Link the comment from the PR as
`https://<site>/browse/KEY?focusedCommentId=COMMENT_ID`.

## Follow-up tickets

Only for the points the user classified as *new ticket*. Search for an
existing ticket first:

```bash
acli jira workitem search --jql 'project = PROJ AND statusCategory != Done AND text ~ "keyword"' --limit 5
```

Show the user one line per ticket (summary, why it can wait, possible
duplicates) and create them after confirmation:

```bash
acli jira workitem create --project PROJ --type Task --summary "..." --description-file followup.json
```

Mention the source ticket and PR in the description. Then list the created
keys in the ticket comment's Follow-ups section.
