# Example: framework upgrade

A fictional upgrade of a content site from framework 4 to 5, with a runtime
bump and the ticket split applied. Shows the level of detail and the order the
skill asks for.

## PR description

[SHOP-412](https://acme.example.com/browse/SHOP-412)

## Summary

Framework 4.8 → **5.2**, runtime 3.11 → **3.13**. The admin UI moves from the
contrib dashboard to the built-in one, and deploys now run a single `deploy`
command. The dependency audit is clean afterwards: the update also brings two
pending security releases.

The full log, with decisions and verification, is in
[`docs/upgrade-framework-5.md`](https://github.com/acme/shop/blob/upgrade-5/docs/upgrade-framework-5.md).

## Worth a look in review

| Change | Why |
| --- | --- |
| `deploy.yml`: one `deploy` step instead of five | The old cache clear before migrations **fails on the first 5.x deploy** (reproduced on a copy of the production database). |
| `package.json` keeps `dashboard-legacy` | The new dashboard migration reads the old package's settings. Removed in the next release. |
| `assets/vendor/carousel.min.js` | The new templating runtime dropped a helper the carousel used; every slider stayed blank. Two calls patched. |
| `jobs/cleanup.py`: query fix, `CLEANUP_ENABLED=false` | The cleanup job has crashed since 2023. Fixed, it would delete about 4,000 audit rows on its first run, so it stays off until its owner confirms. |
| `payments-sdk` pinned to a commit | The last release blocks the runtime upgrade; the pinned commit is upstream's fix. Unsure whether to wait for a release instead. |

<details>
<summary>Not worth reviewing line by line</summary>

- Lock files, generated scaffold (`public/index.*`, `config/defaults/`), the rebuilt database snapshot used by local setup
- Deprecation fixes in application code (renamed imports, return types, removed helpers)
- Settings rewritten by the framework's own migrations (cache keys, logging)
- Re-rolled vendor patches that apply unchanged
</details>

Testing steps, deploy notes and follow-ups: [SHOP-412 comment](https://acme.example.com/browse/SHOP-412?focusedCommentId=10234)

## Ticket comment (SHOP-412)

### Manual testing on staging

- **Admin:** log in as editor and as admin. Check the new dashboard, creating and editing a product, and the media picker.
- **Storefront:** carousels and product videos render; switching between en and fr keeps the current page.
- **Checkout:** place a test order. It appears in the payment provider's dashboard and the confirmation email arrives.
- **Feeds:** the product RSS feed has image enclosures; the sitemap lists products.

### Production deploy: attention points

- **First deploy:** `deploy` runs migrations, then the settings import. Rehearsed on a production database copy; it passed.
- Container images switch to runtime 3.13.
- **After deploy, check:**
  - the settings diff: drift in translated settings is expected and re-exported in a follow-up;
  - the status page: the "experimental dashboard" warning is expected;
  - logs of the first scheduled-job run.
- **Irreversible:** the dashboard migration drops the old settings tables; rolling back needs a database restore.

### Follow-ups

- SHOP-431: remove `dashboard-legacy` once every environment has run the migration.
- SHOP-432: decide with the job owner whether to enable the cleanup.
