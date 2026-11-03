#!/usr/bin/env python3
"""Stats gate for the daily refresh workflow.

`generate.py` rewrites `dashboard.svg` every single day even when nothing about
the repos moved: the freshness term decays with the calendar, and the header
carries today's date. So "did any tracked file change?" can never answer "should
we commit today?". This script answers the question that matters — did stars /
forks / watchers / language / pushed date / description actually move?

It reads the freshly refreshed `cache.json` (written by `generate.py
--refresh`), compares it with the committed snapshot in `data/stats.json`,
prints the deltas and, when something changed, rewrites the snapshot. Under
GitHub Actions it also appends `changed` / `message` to `$GITHUB_OUTPUT`.

Usage:
    python scripts/refresh_stats.py             # check, rewrite snapshot on change
    python scripts/refresh_stats.py --dry-run   # print deltas, never write
    python scripts/refresh_stats.py --stamp     # force-rewrite the snapshot
"""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROJECTS_JSON = os.path.join(ROOT, "projects.json")
CACHE_JSON = os.path.join(ROOT, "cache.json")
SNAPSHOT_JSON = os.path.join(ROOT, "data", "stats.json")

# Everything the dashboard renders on a tile. Anything not listed here (repo
# size, open issues, topics, ...) churns without affecting the output and must
# not trigger a commit.
FIELDS = ("stars", "forks", "watchers", "language", "pushed", "description")


def stats_of(entry):
    return {
        "stars": entry.get("stargazers_count") or 0,
        "forks": entry.get("forks_count") or 0,
        "watchers": entry.get("subscribers_count") or 0,
        "language": entry.get("language") or "",
        "pushed": (entry.get("pushed_at") or "")[:10],
        "description": (entry.get("description") or "").strip(),
    }


def load_json(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def build_snapshot():
    """{repo: stats} for every repo projects.json puts on the map."""
    cfg = load_json(PROJECTS_JSON) or {}
    cache = load_json(CACHE_JSON) or {}
    snap, missing = {}, []
    for p in cfg.get("projects", []):
        repo = p["repo"]
        entry = cache.get(repo)
        if not isinstance(entry, dict):
            missing.append(repo)
            continue
        snap[repo] = stats_of(entry)
    return snap, missing


def diff(old, new):
    """{[repo]: [(field, before, after)]} over repos in `new`."""
    out = {}
    for repo, cur in new.items():
        prev = old.get(repo)
        if prev is None:
            out[repo] = [("new", "", "")]
            continue
        changes = [(f, prev.get(f), cur.get(f)) for f in FIELDS
                   if prev.get(f) != cur.get(f)]
        if changes:
            out[repo] = changes
    for repo in old:
        if repo not in new:
            out.setdefault(repo, []).append(("removed", "", ""))
    return out


def fmt_value(v):
    return str(v) if v not in ("", None) else "—"


def report(changes, total):
    star_delta = fork_delta = 0
    for repo, fields in changes.items():
        for name, before, after in fields:
            if name == "stars":
                star_delta += (after or 0) - (before or 0)
            elif name == "forks":
                fork_delta += (after or 0) - (before or 0)
    for repo, fields in sorted(changes.items()):
        bits = []
        for name, before, after in fields:
            if name == "new":
                bits.append("new on the map")
            elif name == "removed":
                bits.append("dropped from the map")
            elif name == "description":
                bits.append("description updated")
            else:
                bits.append(f"{name} {fmt_value(before)}→{fmt_value(after)}")
        print(f"  {repo}: " + ", ".join(bits))
    print(f"{len(changes)}/{total} repo(s) changed "
          f"(★{star_delta:+d}, fork{fork_delta:+d})")
    return star_delta, fork_delta


def build_message(changes, star_delta, fork_delta):
    parts = []
    if star_delta:
        parts.append(f"★{star_delta:+d}")
    if fork_delta:
        parts.append(f"fork{fork_delta:+d}")
    parts.append(f"{len(changes)} repo(s)")
    return "chore(stats): " + ", ".join(parts)


def write_snapshot(snap):
    """Rewrite the snapshot; `updated` is the last day the numbers really moved."""
    payload = {
        "updated": datetime.date.today().isoformat(),
        "repos": {repo: snap[repo] for repo in snap},
    }
    os.makedirs(os.path.dirname(SNAPSHOT_JSON), exist_ok=True)
    with open(SNAPSHOT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def gh_output(**kv):
    path = os.environ.get("GITHUB_OUTPUT")
    if not path:
        return
    with open(path, "a", encoding="utf-8") as f:
        for key, value in kv.items():
            f.write(f"{key}={value}\n")


def main(argv):
    dry_run = "--dry-run" in argv
    force = "--stamp" in argv
    unknown = [a for a in argv if a not in ("--dry-run", "--stamp")]
    if unknown:
        sys.exit(f"unknown argument(s): {' '.join(unknown)}")

    snap, missing = build_snapshot()
    if not snap:
        sys.exit("no stats in cache.json — run `python generate.py --refresh` first")
    for repo in missing:
        print(f"  [warn] {repo} not in cache.json — skipped", file=sys.stderr)

    old_doc = load_json(SNAPSHOT_JSON) or {}
    old = old_doc.get("repos") or {}
    changes = diff(old, snap)
    bootstrap = not old
    changed = bool(changes) or bootstrap or force
    star_delta = fork_delta = 0

    if bootstrap:
        print(f"no snapshot yet — bootstrapping data/stats.json ({len(snap)} repos)")
        message = f"chore(stats): snapshot {len(snap)} repos"
    elif changes:
        print(f"{len(snap)} repos compared against data/stats.json:")
        star_delta, fork_delta = report(changes, len(snap))
        message = build_message(changes, star_delta, fork_delta)
    else:
        print(f"{len(snap)} repos compared against data/stats.json: no change")
        message = ""

    if changed and not dry_run:
        write_snapshot(snap)
        print(f"wrote {os.path.relpath(SNAPSHOT_JSON, ROOT)}")
    elif changed:
        print("(dry run — snapshot not written)")

    gh_output(changed=str(changed).lower(), message=message)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
