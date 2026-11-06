# Anchoring review comments

Turns the Worth a look table into inline comments on the lines the reviewer
should read, posted as **one** review so the author gets one notification.

1. Only for an open PR, and only after the user confirms the draft comments.
2. Check what is already there, so a rerun does not duplicate:
   `gh api repos/OWNER/REPO/pulls/N/comments --paginate`.
3. For each table row, pick the line in the PR diff that carries the change
   (new side). Lines must be part of the diff: take them from
   `gh api repos/OWNER/REPO/pulls/N/files --paginate` (`patch` hunks). A row
   with no single line (a deleted file, a binary) stays in the table only.
4. Comment body: the Why from the table plus what to check, in one or two
   sentences.
5. Post all comments in one review, with event `COMMENT` (never approve or
   request changes on behalf of the user):

```json
{
  "event": "COMMENT",
  "body": "Review guide: the rows of the Worth a look table, anchored to their lines.",
  "comments": [
    { "path": "deploy.yml", "line": 12, "side": "RIGHT", "body": "..." }
  ]
}
```

```bash
gh api repos/OWNER/REPO/pulls/N/reviews --method POST --input review.json
```

A `422` usually means a line is outside the diff; fix that comment's line or
drop it, then post again.
