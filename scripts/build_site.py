#!/usr/bin/env python3
"""Builds the landing page (site/index.html template) from an F-Droid repo's index-v1.json.

usage: build_site.py <repo_dir> <template> <out_html> <repo_url> <fingerprint> <qr_svg_file>
"""
import html
import json
import os
import sys
from datetime import datetime, timezone

repo_dir, template, out_html, repo_url, fingerprint, qr_file = sys.argv[1:7]
index = json.load(open(os.path.join(repo_dir, "index-v1.json")))


def localized(app, key):
    loc = app.get("localized", {})
    for lang in ("en-US", "en"):
        if loc.get(lang, {}).get(key):
            return loc[lang][key], lang
    for lang, vals in loc.items():
        if vals.get(key):
            return vals[key], lang
    return app.get(key), None


def icon_url(app):
    pkg = app["packageName"]
    icon, lang = localized(app, "icon")
    if icon and lang and os.path.exists(os.path.join(repo_dir, pkg, lang, icon)):
        return f"repo/{pkg}/{lang}/{icon}"
    if app.get("icon"):
        for d in ("icons-640", "icons-480", "icons-320", "icons"):
            if os.path.exists(os.path.join(repo_dir, d, app["icon"])):
                return f"repo/{d}/{app['icon']}"
    return "repo/icons/icon.png"


cards = []
for app in sorted(index.get("apps", []), key=lambda a: (localized(a, "name")[0] or a["packageName"]).lower()):
    pkg = app["packageName"]
    name = localized(app, "name")[0] or pkg
    summary = localized(app, "summary")[0] or ""
    versions = index.get("packages", {}).get(pkg, [])
    latest = max(versions, key=lambda v: v.get("versionCode", 0)) if versions else {}
    ver = latest.get("versionName", "")
    cards.append(
        f'      <div class="app"><img src="{html.escape(icon_url(app))}" alt="">'
        f'<div><b>{html.escape(name)}</b><span>{html.escape(summary)}</span>'
        f'<small>{html.escape(ver)}</small></div></div>'
    )

host_path = repo_url.split("://", 1)[1]
page = (
    open(template).read()
    .replace("@APPS@", "\n".join(cards) or '      <p class="muted">No apps yet.</p>')
    .replace("@REPO_HOST_PATH@", host_path)
    .replace("@REPO_URL@", repo_url)
    .replace("@FINGERPRINT@", fingerprint)
    .replace("@QR_SVG@", open(qr_file).read())
    .replace("@UPDATED@", datetime.now(timezone.utc).strftime("%d %b %Y"))
)
open(out_html, "w").write(page)
print(f"landing page: {len(cards)} app(s)")
