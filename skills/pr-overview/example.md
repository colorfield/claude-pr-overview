# Example: framework upgrade

A fictional upgrade of a content site from framework 4 to 5, with a runtime
bump. Shows the level of detail and the section order the skill asks for.

---

[SHOP-412](https://acme.example.com/browse/SHOP-412)

## Summary

Framework 4.8 → **5.2**, runtime 3.11 → **3.13**, ORM 2 → 3. The admin UI moves
from the contrib dashboard to the built-in one. Deploys now run a single
`deploy` command. The dependency audit is clean afterwards: the update also
brings two pending security releases.

The full log, with decisions and verification, is in
[`docs/upgrade-framework-5.md`](https://github.com/acme/shop/blob/upgrade-5/docs/upgrade-framework-5.md).

## Not worth reviewing line by line

- Lock files, generated scaffold (`public/index.*`, `config/defaults/`), the
  rebuilt database snapshot used by local setup
- Deprecation fixes in application code (renamed imports, return types,
  removed helpers)
- Settings rewritten by the framework's own migrations (cache keys, logging)
- Re-rolled vendor patches that apply unchanged

## Worth a look in review

| Change | Why |
| --- | --- |
| `deploy.yml`: one `deploy` step instead of five | The old cache clear before migrations **fails on the first 5.x deploy** (reproduced on a copy of the production database). |
| `package.json` keeps `dashboard-legacy` | The new dashboard migration needs the old package installed to read its settings. Removed in the next release. |
| `assets/vendor/carousel.min.js` | The new templating runtime dropped a helper the carousel used; every slider stayed blank. Two calls patched. |
| `jobs/cleanup.py`: query fix, `CLEANUP_ENABLED=false` | The cleanup job has crashed since 2023. Fixed, it would delete about 4,000 audit rows on first run, so it stays off until its owner confirms. |
| `payments-sdk` pinned to a commit | The last release blocks the runtime upgrade; the pinned commit is upstream's fix. |

## Manual testing on staging

- **Admin:** log in as editor and as admin. Check the new dashboard, creating
  and editing a product, and the media picker.
- **Storefront:** carousels, product videos, language switch (en/fr).
- **Checkout:** place a test order; check it appears in the payment provider's
  dashboard and the confirmation email arrives.
- **Feeds:** product RSS feed with image enclosures, sitemap.

## Production deploy: attention points

- **First deploy:** `deploy` runs migrations, then settings import. Rehearsed
  on a production database copy and on the local snapshot; both passed.
- Container images switch to runtime 3.13.
- **After deploy, check:**
  - the settings diff command: drift in translated settings is expected and
    re-exported in a follow-up;
  - the status page: the "experimental dashboard" warning is expected;
  - logs of the first scheduled-job run.

## Follow-up release

Remove `dashboard-legacy` once every environment has run the migration.
