# jaycee-h apps – F-Droid repository

A self-hosted [F-Droid](https://f-droid.org) repository for my Android apps, served at
**https://jaycee-h.github.io/**.

## Add it

[<img src="site/get-it-on-fdroid.png" alt="Get it on F-Droid" height="60">](https://jaycee-h.github.io/)

Open https://jaycee-h.github.io/ on your phone and tap **Add to F-Droid**, or in F-Droid (Droid-ify, Neo Store)
go to Settings → Repositories → + and enter:

```
https://jaycee-h.github.io/repo
```

Fingerprint: `1BDCB444EB7C5E4B1B5BF62809B942F532C6E0E486306ACBDD78B467B8F57227`

## Apps

| App | Source |
| --- | --- |
| XEU Forums – unofficial app for the Xiaomi.EU community forum | [XEU-Forums/xeu-forums-app](https://github.com/XEU-Forums/xeu-forums-app) |

## How it works

- `apps.yml` lists each app's package name and the GitHub repo whose releases carry its APK.
- `metadata/<package>.yml` (+ `metadata/<package>/en-US/images/icon.png`) is the store listing.
- `.github/workflows/publish.yml` downloads the latest 3 **stable** (non-pre-release) APKs of every app, builds and
  signs the F-Droid index, renders the landing page (`site/index.html` via `scripts/build_site.py`) and force-pushes
  everything as a single commit to the `gh-pages` branch. It runs on push to `main`, every 3 hours, and on demand.
- APKs keep their developers' signing keys, so GitHub and F-Droid installs update each other.

### Add another app

1. Add an entry to `apps.yml`.
2. Add `metadata/<package>.yml` and an icon at `metadata/<package>/en-US/images/icon.png` (512×512 PNG).
3. Make sure the app's GitHub repo has at least one non-pre-release release with an `.apk` attached.
4. Push to `main`.

### Secrets

`FDROID_KEYSTORE_BASE64` and `FDROID_KEYSTORE_PASS` hold the repo signing key (PKCS12, alias `xeu-repo`).
Without them the workflow does a dry run and publishes nothing. Never commit the keystore; losing it means everyone
has to re-add the repository.
