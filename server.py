#!/usr/bin/env python3
"""Local editing server for the profile dashboard.

    python generate.py --serve [--port 8765] [--no-open]

Routes:
    GET  /                  editor UI
    GET  /api/state         config + candidate pool + rendered svg
    POST /api/refresh       pull the repo list from GitHub (candidates + scores)
    POST /api/config        save config (order, groups, boost, key_points)
    POST /api/svg           render only, returns svg for live preview
    POST /api/export        write dashboard.svg + preview.html to disk
    GET  /assets/...        font files for the UI

Everything runs on the loopback interface only.
"""
import json
import os
import sys
import threading
import traceback
import urllib.error
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import generate as g
from ui import UI_HTML

HOST = "127.0.0.1"
LOCK = threading.Lock()
TOKEN = os.environ.get("GITHUB_TOKEN")


# ---- state helpers --------------------------------------------------------

def candidate_pool(cfg, cache, repos):
    """Normalise a GitHub repo list into the shape the UI wants."""
    picked = {p["repo"] for p in cfg["projects"]}
    out = []
    for d in repos:
        full = d.get("full_name") or f"{d.get('owner', {}).get('login')}/{d.get('name')}"
        if not full or "/" not in full:
            continue
        w, st, fk, lang, pushed, days, fresh, desc = g.score_repo(d, 1.0)
        out.append({
            "repo": full,
            "owner": full.split("/", 1)[0],
            "stars": st, "forks": fk, "lang": lang, "pushed": pushed,
            "days": days, "fresh": fresh, "weight": w,
            "desc": g.clean_text(desc),
            "selected": full in picked,
        })
    out.sort(key=lambda r: r["weight"], reverse=True)
    return out


def org_repo_names(cfg, cache):
    """Which cached repos came from a whitelisted org (for UI badging)."""
    orgs = {o.lower() for o in (cfg.get("orgs") or [])}
    return {r for r in cache if r.split("/", 1)[0].lower() in orgs}


class RateLimited(Exception):
    pass


def _fetch_with_retry(fn, note_label, notes, attempts=2):
    """Fetch, recording a short status into `notes`.

    Unauthenticated GitHub allows 60 requests/hour; an org whitelist burns
    through that fast. A 403 here is an expected, recoverable condition —it gets
    reported in the note and the refresh carries on with whatever is cached —    rather than aborting the whole request.
    """
    for attempt in range(attempts):
        try:
            return fn()
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                raise RateLimited()
            if attempt == attempts - 1:
                notes.append(f"{note_label} 失败 HTTP {e.code}")
                return None
        except Exception as e:
            if attempt == attempts - 1:
                notes.append(f"{note_label} 失败 {type(e).__name__}")
                return None
    return None


def build_state(refresh=False, use_cache_only=False, owners=None):
    """Load config, refresh the pool if asked, render, and return the payload.

    `owners` limits a refresh to specific sources — `['user']` refreshes the
    personal account, an org name refreshes just that org. None (or empty)
    means refresh everything, which is the original behaviour and the fast way
    to burn through GitHub's unauthenticated 60 req/hour when the whitelist is
    long.
    """
    cfg = g.load_config()
    cache = g.load_cache()
    note = ""

    if refresh:
        if use_cache_only:
            note = "离线模式：未请求 GitHub，候选池来自 cache.json"
        else:
            notes = []
            limited = False
            user = cfg.get("user", "Weidows")
            orgs = cfg.get("orgs") or []

            # normalise the requested owners to what actually exists in config
            wanted = set(owners or [])
            do_user = (not wanted) or "user" in wanted or f"@{user}" in wanted
            do_orgs = [o for o in orgs if (not wanted) or o in wanted
                       or f"@{o}" in wanted]
            # an owner was asked for by name but matches nothing: say so
            known = {"user", f"@{user}"} | set(orgs) | {f"@{o}" for o in orgs}
            unknown = [w for w in wanted if w not in known]

            if do_user:
                try:
                    repos = _fetch_with_retry(lambda: g.fetch_user_repos(user, TOKEN),
                                              f"@{user}", notes)
                    if repos:
                        for d in repos:
                            if d.get("full_name"):
                                cache[d["full_name"]] = d
                        notes.append(f"@{user} {len(repos)} 个")
                except RateLimited:
                    limited = True
                    notes.append(f"@{user} 限流")

            if not limited:
                for org in do_orgs:
                    try:
                        repos = _fetch_with_retry(
                            lambda o=org: g.fetch_org_repos(o, TOKEN), org, notes)
                        if repos:
                            for d in repos:
                                if d.get("full_name"):
                                    cache[d["full_name"]] = d
                            notes.append(f"{org} {len(repos)} 个")
                    except RateLimited:
                        limited = True
                        notes.append(f"{org} 限流")
                        break        # rest will be limited too; stop burning quota

            g.save_cache(cache)
            if unknown:
                notes.append("未知来源: " + ", ".join(unknown))
            note = ("已刷新 " + " · ".join(notes)) if notes else "没有指定要刷新的来源"
            if limited:
                note += "｜GitHub 未登录只有 60 次/小时，设 GITHUB_TOKEN 可解"

    items, weights = g.resolve_items(cfg, cache, offline=False, token=TOKEN, refresh=False)
    svg, rects, regions, canvas = g.render_layout(items, weights, cfg.get("groups"))
    shares = g.area_shares(weights)

    pool = candidate_pool(cfg, cache, list(cache.values()))
    from_org = org_repo_names(cfg, cache)
    for c in pool:
        c["from_org"] = c["repo"] in from_org

    # ensure every selected repo appears in the pool even if it isn't public
    have = {c["repo"] for c in pool}
    for it in items:
        if it["repo"] not in have:
            pool.insert(0, {
                "repo": it["repo"], "owner": it["repo"].split("/", 1)[0],
                "stars": it["stars"], "forks": it["forks"],
                "lang": it["lang"], "pushed": it["pushed"], "days": it["days"],
                "fresh": it["fresh"], "weight": it["weight"],
                "desc": g.clean_text(it["desc"]), "selected": True,
                "from_org": it["repo"] in from_org,
            })

    return {
        "config": cfg,
        "pool": pool,
        "svg": svg,
        "markdown": g.build_markdown(items, weights, shares, cfg.get("groups"),
                                     user=cfg.get("user", "Weidows")),
        "layout": {"tiles": rects, "regions": regions,
                       "w": canvas["w"], "h": canvas["h"],
                       "map_h": canvas["map_h"], "date": canvas["date"]},
        "meta": {
            "note": note,
            "items": [
                {"repo": it["repo"], "weight": it["weight"], "share": s,
                 "stars": it["stars"], "forks": it["forks"], "lang": it["lang"],
                 "pushed": it["pushed"], "days": it["days"], "fresh": it["fresh"],
                 "desc": it["desc"], "group": it.get("group", ""),
                 "boost": it.get("boost", 1.0), "key_points": it["key_points"]}
                for it, s in zip(items, shares)
            ],
            "w": canvas["w"], "h": canvas["h"],
        },
    }


def normalise_config(body):
    """Validate an incoming config before it touches disk."""
    if not isinstance(body, dict):
        raise ValueError("config must be an object")
    projects = body.get("projects")
    if not isinstance(projects, list) or not projects:
        raise ValueError("projects must be a non-empty list")

    seen, clean = set(), []
    for p in projects:
        if not isinstance(p, dict):
            raise ValueError("each project must be an object")
        repo = str(p.get("repo", "")).strip()
        if "/" not in repo:
            raise ValueError(f"invalid repo name: {repo!r} (expected owner/name)")
        if repo in seen:
            raise ValueError(f"duplicate repo: {repo}")
        seen.add(repo)
        try:
            boost = float(p.get("boost", 1.0))
        except (TypeError, ValueError):
            raise ValueError(f"invalid boost for {repo}")
        if not (0 < boost <= 100):
            raise ValueError(f"boost for {repo} must be in (0, 100]")
        kps = p.get("key_points") or []
        if not isinstance(kps, list):
            raise ValueError(f"key_points for {repo} must be a list")
        clean.append({
            "repo": repo,
            "boost": boost,
            "group": str(p.get("group", "")).strip(),
            "key_points": [str(k).strip() for k in kps if str(k).strip()][:3],
        })

    groups = body.get("groups") or []
    if not isinstance(groups, list):
        raise ValueError("groups must be a list")
    gclean, gseen = [], set()
    for gr in groups:
        name = str(gr.get("name", "").strip() if isinstance(gr, dict) else gr).strip()
        if not name or name in gseen:
            continue
        gseen.add(name)
        gclean.append({"name": name})

    # Org whitelist: repo owners whose candidates get pulled in on refresh.
    orgs = body.get("orgs") or []
    if not isinstance(orgs, list):
        raise ValueError("orgs must be a list")
    org_clean, org_seen = [], set()
    for o in orgs:
        name = str(o if not isinstance(o, dict) else o.get("name", "")).strip()
        name = name.lstrip("@").strip()
        if not name:
            continue
        if "/" in name or " " in name:
            raise ValueError(f"invalid org name: {name!r}")
        key = name.lower()
        if key in org_seen:
            continue
        org_seen.add(key)
        org_clean.append(name)

    return {
        "user": str(body.get("user") or "Weidows").strip(),
        "count": len(clean),
        "orgs": org_clean,
        "groups": gclean,
        "projects": clean,
    }


# ---- HTTP -----------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = "dashboard/1.0"

    def log_message(self, fmt, *args):
        if os.environ.get("DASHBOARD_VERBOSE"):
            sys.stderr.write(f"  {self.address_string()} {fmt % args}\n")

    # -- helpers
    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if isinstance(body, (dict, list)):
            body = json.dumps(body, ensure_ascii=False)
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _json_body(self):
        n = int(self.headers.get("Content-Length") or 0)
        if n <= 0:
            return {}
        if n > 4 * 1024 * 1024:
            raise ValueError("body too large")
        return json.loads(self.rfile.read(n).decode("utf-8"))

    def _guard(self, fn):
        try:
            with LOCK:
                fn()
        except ValueError as e:
            self._send(400, {"error": str(e)})
        except Exception as e:
            traceback.print_exc()
            self._send(500, {"error": f"{type(e).__name__}: {e}"})

    # -- routes
    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, UI_HTML, "text/html; charset=utf-8")
        elif path == "/api/state":
            self._guard(lambda: self._send(200, build_state()))
        elif path.startswith("/assets/"):
            self._serve_asset(path)
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == "/api/refresh":
            self._guard(self._refresh)
        elif path == "/api/config":
            self._guard(self._save_config)
        elif path == "/api/svg":
            self._guard(self._render_only)
        elif path == "/api/export":
            self._guard(self._export)
        else:
            self._send(404, {"error": "not found"})

    def _refresh(self):
        body = self._json_body()
        owners = body.get("owners")
        if owners is not None and not isinstance(owners, list):
            raise ValueError("owners must be a list of source names")
        state = build_state(refresh=True, use_cache_only=bool(body.get("offline")),
                            owners=owners)
        self._send(200, state)

    def _save_config(self):
        cfg = normalise_config(self._json_body())
        g.save_config(cfg)
        state = build_state()
        state["meta"]["note"] = "配置已保存"
        self._send(200, state)

    def _render_only(self):
        body = self._json_body()
        cfg = normalise_config(body)
        cache = g.load_cache()
        items, weights = g.resolve_items(cfg, cache, offline=False)
        svg, rects, regions, canvas = g.render_layout(items, weights, cfg.get("groups"))
        shares = g.area_shares(weights)
        md = g.build_markdown(items, weights, shares, cfg.get("groups"),
                              user=cfg.get("user", "Weidows"))
        self._send(200, {
            "svg": svg,
            "markdown": md,
            "layout": {"tiles": rects, "regions": regions,
                       "w": canvas["w"], "h": canvas["h"],
                       "map_h": canvas["map_h"], "date": canvas["date"]},
            "meta": {"items": [
                {"repo": it["repo"], "weight": it["weight"], "share": s,
                 "stars": it["stars"], "forks": it["forks"], "lang": it["lang"],
                 "pushed": it["pushed"], "days": it["days"], "fresh": it["fresh"],
                 "desc": it["desc"], "group": it.get("group", ""),
                 "boost": it.get("boost", 1.0), "key_points": it["key_points"]}
                for it, s in zip(items, shares)],
                "note": "预览已更新（未保存）"},
        })

    def _export(self):
        body = self._json_body()
        cfg = normalise_config(body)
        g.save_config(cfg)
        cache = g.load_cache()
        items, weights = g.resolve_items(cfg, cache, offline=False)
        svg, rects, regions, canvas = g.render_layout(items, weights, cfg.get("groups"))
        shares = g.area_shares(weights)
        md = g.build_markdown(items, weights, shares, cfg.get("groups"),
                              user=cfg.get("user", "Weidows"))
        with open(g.SVG_OUT, "w", encoding="utf-8") as f:
            f.write(svg)
        with open(g.PREVIEW_OUT, "w", encoding="utf-8") as f:
            f.write(g.build_preview(svg, items, weights, shares, cfg.get("groups")))
        with open(g.MD_OUT, "w", encoding="utf-8") as f:
            f.write(md)
        self._send(200, {
            "svg": svg,
            "markdown": md,
            "layout": {"tiles": rects, "regions": regions,
                       "w": canvas["w"], "h": canvas["h"],
                       "map_h": canvas["map_h"], "date": canvas["date"]},
            "files": [g.SVG_OUT, g.PREVIEW_OUT, g.MD_OUT],
            "meta": {"note": "已写入 dashboard.svg / preview.html / dashboard.md"},
        })

    def _serve_asset(self, path):
        rel = path[len("/assets/"):]
        base = os.path.join(g.HERE, "assets")
        full = os.path.normpath(os.path.join(base, rel))
        if not full.startswith(os.path.normpath(base)) or not os.path.isfile(full):
            return self._send(404, {"error": "not found"})
        ext = full.rsplit(".", 1)[-1].lower()
        ctype = {"woff2": "font/woff2", "ttf": "font/ttf", "otf": "font/otf",
                 "txt": "text/plain; charset=utf-8"}.get(ext, "application/octet-stream")
        with open(full, "rb") as f:
            self._send(200, f.read(), ctype)


def run(port=8765, open_browser=True):
    g.METRICS = g.Metrics(g.find_font_source())
    try:
        httpd = ThreadingHTTPServer((HOST, port), Handler)
    except OSError as e:
        sys.exit(f"cannot bind {HOST}:{port} —{e}\n"
                 f"try: python generate.py --serve --port {port + 1}")
    url = f"http://{HOST}:{port}/"
    print(f"dashboard editor → {url}\n  Ctrl+C to stop")
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
