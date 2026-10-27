# jaycee-h.github.io – notes for Claude

Self-hosted F-Droid repository (GitHub Pages user site, served from the `gh-pages` branch at
https://jaycee-h.github.io/, repo at https://jaycee-h.github.io/repo). No app code lives here.

## Rules

- **Commits:** author and committer are the owner (`pagnchanak <chea.pagnchanak@gmail.com>`). Never add
  `Co-Authored-By: Claude`, session links or other AI attribution. Work on `main`.
- **Stable only:** index only non-pre-release GitHub releases. Never add dev/pre-release builds.
- **Never change** the repo URL, the signing key (secrets `FDROID_KEYSTORE_BASE64` / `FDROID_KEYSTORE_PASS`,
  alias `xeu-repo`, fingerprint `1BDCB444EB7C5E4B1B5BF62809B942F532C6E0E486306ACBDD78B467B8F57227`) or the
  `gh-pages` publishing branch – users would have to re-add the repo.
- Don't use other companies' logos in listings or the landing page. Exception: F-Droid's official
  "Get it on F-Droid" badge (`site/get-it-on-fdroid.png`), which F-Droid provides for exactly this use.

## Layout

- `apps.yml` – package name + GitHub repo per app.
- `metadata/` – F-Droid listing per app (`<package>.yml`, `<package>/en-US/images/icon.png`).
- `site/index.html` – landing page template (placeholders filled by `scripts/build_site.py`); `site/repo-icon.png`.
- `.github/workflows/publish.yml` – builds with fdroidserver from PyPI (Ubuntu's package has an androguard too old
  for current APKs), checks every listed app is indexed, publishes a
  single force-pushed commit to `gh-pages`. Scheduled runs skip publishing when `.source-digest` is unchanged.

## Notes

- fdroidserver isn't installable in the Claude cloud workspace (PyPI blocked); test by pushing and reading the run's
  annotations: `gh api repos/jaycee-h/jaycee-h.github.io/check-runs/<job-id>/annotations` (notices list the indexed
  versions per app).
- After publishing, verify: https://jaycee-h.github.io/repo/index-v1.json lists every app, and
  https://jaycee-h.github.io/repo/entry.jar is signed with the fingerprint above.
