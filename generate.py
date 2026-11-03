#!/usr/bin/env python3
"""GitHub profile treemap dashboard generator.

Usage:
    python generate.py              # fetch live data, write dashboard.svg + preview.html
    python generate.py --offline    # rebuild from cache.json (no API calls)
    python generate.py --serve      # local editor: refresh candidates, groups, ordering
    python generate.py --help

Style: wireframe heatmap — dark canvas, heat-colored outlines, tile area encodes
weight. Type: 得意黑 Smiley Sans (OFL-1.1, atelier-anchor/smiley-sans), subset to
the glyphs the SVG actually uses and embedded as base64 woff2, so the file is
self-contained when GitHub renders it.

Scoring (dynamic weight -> tile area):
    base   = stars*8 + forks*4 + watchers + 3
    fresh  = 0.35 + 0.65 * exp(-days_since_push / 180)
    weight = base * fresh * boost        (boost is hand-set per repo in projects.json)
    area   ≈ weight^0.60, clamped to 4%..17% of the map so no tile is unreadable
"""
import base64
import datetime
import html
import json
import math
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECTS_JSON = os.path.join(HERE, "projects.json")
CACHE_JSON = os.path.join(HERE, "cache.json")
SVG_OUT = os.path.join(HERE, "dashboard.svg")
PREVIEW_OUT = os.path.join(HERE, "preview.html")
# Markdown to paste under the image in the profile README. The treemap itself is
# a single <img> and can only carry one link, so the per-project links live here
# instead — GitHub's markdown list is the reliable place for them.
MD_OUT = os.path.join(HERE, "dashboard.md")
FONT_DIR = os.path.join(HERE, "assets", "font")

# Width matches GitHub's usable README content width exactly (846px, measured
# off a live profile: 896px card - 2*24px padding - 2px border). GitHub applies
# `max-width:100%` to README images, so anything wider gets scaled down; sitting
# at exactly 846 means the artwork renders at 1:1 with no resampling.
# Height is NOT fixed — it grows with the number of tiles, otherwise every tile
# added past 10 would have to share the same box and become unreadable.
README_CONTENT_W = 846
W, HEADER_H = README_CONTENT_W, 58
MAP_H_BASE = 522        # map height for BASE_N tiles (keeps 10 tiles near 16:9)
BASE_N = 10
PAD = 8
FONT_FAMILY = "SmileySans"


def canvas_height(n):
    """Map height for `n` tiles: fixed W width, height scales sub-linearly.

    Linear growth (n/10) would double the height at 20 tiles, which is more
    vertical space than a profile README wants. n**0.6 keeps the average tile
    area from collapsing while growing gently: 10→522, 20→794, 30→1008.
    """
    if n <= BASE_N:
        return MAP_H_BASE
    return int(round(MAP_H_BASE * (n / BASE_N) ** 0.6))

# muted heat ramp, index 0 = rank 1 (warmest), 9 = rank 10
HEAT = [
    "#dfa08a", "#cf9393", "#9fb8cf", "#93bcab", "#aca6d1",
    "#b7ae8f", "#84a3bd", "#9aa5b5", "#c2a284", "#71808f",
]
INK = "#dde5ee"        # primary text
INK_DIM = "#8d99a9"    # secondary text
INK_FAINT = "#5b6675"  # tertiary text

# GitHub octicons, same 16x16 geometry the profile cards use. Real icons beat
# the "★" character: they render identically everywhere and match the visual
# language of the rest of the profile.
OCTICON_STAR = ("M8 .25a.75.75 0 01.673.418l1.882 3.815 4.21.612a.75.75 0 01.416 1.279l-3.046 "
                "2.97.719 4.192a.75.75 0 01-1.088.791L8 12.347l-3.766 1.98a.75.75 0 "
                "01-1.088-.79l.72-4.194L.818 6.374a.75.75 0 01.416-1.28l4.21-.611L7.327.668A.75.75 "
                "0 018 .25zm0 2.445L6.615 5.5a.75.75 0 01-.564.41l-3.097.45 2.24 2.184a.75.75 0 "
                "01.216.664l-.528 3.084 2.769-1.456a.75.75 0 01.698 0l2.77 1.456-.53-3.084a.75.75 "
                "0 01.216-.664l2.24-2.183-3.096-.45a.75.75 0 01-.564-.41L8 2.694v.001z")
OCTICON_FORK = ("M5 3.25a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm0 2.122a2.25 2.25 0 10-1.5 0v.878A2.25 "
                "2.25 0 005.75 8.5h1.5v2.128a2.251 2.251 0 101.5 0V8.5h1.5a2.25 2.25 0 "
                "002.25-2.25v-.878a2.25 2.25 0 10-1.5 0v.878a.75.75 0 01-.75.75h-4.5A.75.75 0 "
                "015 6.25v-.878zm3.75 7.378a.75.75 0 11-1.5 0 .75.75 0 011.5 0zm3-8.75a.75.75 0 "
                "100-1.5.75.75 0 000 1.5z")

# GitHub's language dot colours (what linguist paints next to the language name).
LANG_COLORS = {
    "Python": "#3572A5", "TypeScript": "#3178c6", "JavaScript": "#f1e05a",
    "Go": "#00ADD8", "HTML": "#e34c26", "CSS": "#563d7c", "C++": "#f34b7d",
    "C": "#555555", "C#": "#178600", "Java": "#b07219", "Rust": "#dea584",
    "Shell": "#89e051", "Dockerfile": "#384d54", "Vue": "#41b883",
    "Kotlin": "#A97BFF", "Swift": "#F05138", "Ruby": "#701516",
}

AREA_EXP = 0.60        # compress weight ratios before sizing tiles
SHARE_MIN = 0.04       # floor: every tile stays legible
SHARE_MAX = 0.17       # ceiling: no tile becomes an empty billboard


def fetch_repo(full, token=None):
    url = f"https://api.github.com/repos/{full}"
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def fetch_user_repos(user, token=None, per_page=100):
    """All public repos of a user — the candidate pool, in one request."""
    url = (f"https://api.github.com/users/{user}/repos"
           f"?per_page={per_page}&sort=pushed&direction=desc")
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)


def fetch_org_repos(org, token=None, per_page=100, max_pages=3):
    """Public repos of an organisation, tagged with their owner.

    Orgs are whitelisted in projects.json so repos maintained there (often the
    higher-star ones) show up as candidates alongside your own.
    """
    out = []
    for page in range(1, max_pages + 1):
        url = (f"https://api.github.com/orgs/{org}/repos"
               f"?per_page={per_page}&page={page}&sort=pushed&direction=desc")
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=25) as r:
            batch = json.load(r)
        if not isinstance(batch, list):
            break
        out.extend(batch)
        if len(batch) < per_page:
            break
    return out



def score_repo(data, boost):
    stars = data.get("stargazers_count") or 0
    forks = data.get("forks_count") or 0
    watchers = data.get("subscribers_count") or 0
    pushed_at = data.get("pushed_at") or ""
    pushed = pushed_at[:10] or "—"
    try:
        dt = datetime.datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
        days = max(0, (datetime.datetime.now(datetime.timezone.utc) - dt).days)
    except Exception:
        days = 365
    base = stars * 8 + forks * 4 + watchers + 3
    fresh = 0.35 + 0.65 * math.exp(-days / 180)
    weight = round(base * fresh * boost, 2)
    return (weight, stars, forks, data.get("language") or "—", pushed, days, fresh,
            (data.get("description") or "").strip())


# ---- squarified treemap ----
def squarify(weights, x, y, w, h):
    """Return [(index, rx, ry, rw, rh)]. weights: list of (idx, value)."""
    vals = [(i, v) for i, v in weights if v > 0]
    total = sum(v for _, v in vals)
    if total <= 0:
        return []
    scale = (w * h) / total
    vals = [(i, v * scale) for i, v in vals]  # now areas in px^2
    return list(_squarify(vals, x, y, w, h))


def _squarify(items, x, y, w, h):
    if not items:
        return
    if len(items) == 1:
        i, a = items[0]
        yield (i, x, y, w, h)
        return
    row, rest = [], list(items)
    best = None
    while rest:
        row.append(rest.pop(0))
        s = sum(a for _, a in row)
        worst = _worst(row, s, min(w, h))
        if best is None or worst <= best:
            best = worst
        else:
            rest.insert(0, row.pop())
            break
    s = sum(a for _, a in row)
    if w >= h:
        rw = s / h
        yy = y
        for i, a in row:
            rh = a / rw
            yield (i, x, yy, rw, rh)
            yy += rh
        yield from _squarify(rest, x + rw, y, w - rw, h)
    else:
        rh = s / w
        xx = x
        for i, a in row:
            cw = a / rh
            yield (i, xx, y, cw, rh)
            xx += cw
        yield from _squarify(rest, x, y + rh, w, h - rh)


def _worst(row, s, side):
    mx = max(a for _, a in row)
    mn = min(a for _, a in row)
    return max(side * side * mx / (s * s), (s * s) / (side * side * mn))


def area_shares(weights):
    """Weight -> fraction of the map, compressed and clamped so every tile reads."""
    raw = [max(w, 1e-6) ** AREA_EXP for w in weights]
    total = sum(raw)
    base = [r / total for r in raw]
    return _clamp_shares(base, SHARE_MIN, SHARE_MAX)


def _clamp_shares(shares, lo, hi):
    """Rescale shares into [lo, hi] while keeping the total at 1.

    Done by finding the single scale factor k with sum(clamp(k*share, lo, hi)) == 1
    (the sum is monotonic in k, so it's a bisection). Scaling instead of clamping
    each value independently keeps the ordering intact and the total exact.

    The bounds are widened first when the tile count makes them infeasible: one
    tile must own the whole map, and 40 tiles cannot each hold 4% of it.
    """
    n = len(shares)
    if n == 0:
        return []
    # Bounds must stay feasible: n*lo <= 1 <= n*hi. Raise the ceiling to 1.6/n
    # rather than 1/n so a small set of tiles can still show a spread instead of
    # being forced into an even split.
    lo = min(lo, 1.0 / n)
    hi = max(hi, 1.6 / n)

    def total(k):
        return sum(min(hi, max(lo, k * s)) for s in shares)

    k_lo, k_hi = 0.0, 1.0
    while total(k_hi) < 1.0 and k_hi < 1e12:
        k_hi *= 2.0
    for _ in range(80):
        mid = (k_lo + k_hi) / 2
        if total(mid) < 1.0:
            k_lo = mid
        else:
            k_hi = mid

    out = [min(hi, max(lo, k_hi * s)) for s in shares]
    total_out = sum(out)
    return [s / total_out for s in out] if total_out > 0 else [1 / n] * n


# ---- text metrics: real glyph advances, so CJK/Latin mix measures correctly ----
class Metrics:
    def __init__(self, path=None):
        self.upem = 1000
        self.cmap = {}
        self.hmtx = {}
        self.missing = set()
        self.loaded = False
        if path:
            try:
                from fontTools.ttLib import TTFont
                f = TTFont(path, lazy=True)
                self.upem = f["head"].unitsPerEm
                self.cmap = f.getBestCmap()
                self.hmtx = f["hmtx"]
                self.loaded = True
            except Exception as e:
                print(f"  [font] metrics unavailable ({e}) — falling back to estimates",
                      file=sys.stderr)

    def adv(self, ch):
        o = ord(ch)
        if o in (0xFE0E, 0xFE0F, 0x200B):  # variation selectors / zero-width space
            return 0
        g = self.cmap.get(o)
        if g is not None:
            return self.hmtx[g][0]
        self.missing.add(ch)
        return self.upem * (1.0 if o > 0x2E7F else 0.55)

    def width(self, t, fs):
        return sum(self.adv(c) for c in t) * fs / self.upem


METRICS = Metrics()


def text_w(t, fs):
    return METRICS.width(t, fs)


def line_h(fs):
    return round(fs * 1.45, 1)


def esc(t):
    return html.escape(str(t), quote=True)


def _fit(t, max_px, fs):
    if text_w(t, fs) <= max_px:
        return t
    ell = "…"
    while t and text_w(t + ell, fs) > max_px:
        t = t[:-1]
    return (t + ell) if t else (ell if text_w(ell, fs) <= max_px else "")


def _wrap(t, max_px, fs):
    """Greedy wrap into lines that fit max_px (metrics-aware, breaks between chars)."""
    lines, cur = [], ""
    for ch in t:
        if text_w(cur + ch, fs) <= max_px:
            cur += ch
        else:
            if cur:
                lines.append(cur)
            cur = ch if text_w(ch, fs) <= max_px else ""
    if cur:
        lines.append(cur)
    return lines or [""]


EMOJI_RE = re.compile(
    "[\U0001F000-\U0001FAFF\u2600-\u27BF\u2B00-\u2BFF\uFE0F\u200D]+")


def clean_text(t):
    """Drop glyphs Smiley Sans has no outline for (emoji, variation selectors).
    Leaving them in would silently fall back to the system emoji font and break
    the typeface inside a tile."""
    t = t or ""
    if not METRICS.loaded:
        return re.sub(r"\s+", " ", EMOJI_RE.sub("", t)).strip()
    kept = "".join(c for c in t
                   if c.isspace() or ord(c) in METRICS.cmap)
    return re.sub(r"\s+", " ", kept).strip()


LATIN_RE = re.compile(r"[\x20-\x7E]")
TOKEN_RE = re.compile(r"[A-Za-z0-9_+\-#./:&@]+|\s|.", re.S)


def _is_latin(t):
    return len(LATIN_RE.findall(t)) >= 0.7 * len(t.replace(" ", "")) if t else False


def _wrap_smart(t, max_px, fs):
    """Wrap on word boundaries for ASCII runs and between characters for CJK.

    Pure char-wrapping splits things like 'ScriptCat' in half inside a mixed
    Chinese/English line, which reads as broken rather than wrapped.
    """
    lines, cur = [], ""
    for tok in TOKEN_RE.findall(t):
        if tok.isspace() and not cur:
            continue
        cand = cur + tok
        if text_w(cand, fs) <= max_px:
            cur = cand
            continue
        if cur:
            lines.append(cur.rstrip())
        # a single token wider than the tile has to be split somewhere
        while tok and text_w(tok, fs) > max_px:
            head = tok
            while head and text_w(head, fs) > max_px:
                head = head[:-1]
            if not head:
                head, tok = tok[0], tok[1:]
            lines.append(head)
            tok = tok[len(head):]
        cur = tok.lstrip()
    if cur.strip():
        lines.append(cur.rstrip())
    return lines or [""]


# ---- font: Smiley Sans subset embedding ----
def find_font_source():
    if not os.path.isdir(FONT_DIR):
        return None
    for f in sorted(os.listdir(FONT_DIR)):
        if f.lower().endswith((".ttf", ".otf")):
            return os.path.join(FONT_DIR, f)
    return None


def subset_font_b64(chars):
    """Subset Smiley Sans to the used chars, return base64 woff2 ('' on failure)."""
    src = find_font_source()
    if not src:
        print("  [font] no ttf/otf in assets/font — SVG falls back to system fonts",
              file=sys.stderr)
        return ""
    out = os.path.join(FONT_DIR, "subset.woff2")
    txt = os.path.join(FONT_DIR, ".subset-chars.txt")
    open(txt, "w", encoding="utf-8").write(chars)
    try:
        r = subprocess.run(
            [sys.executable, "-m", "fontTools.subset", src,
             f"--text-file={txt}", "--flavor=woff2",
             f"--output-file={out}", "--no-hinting"],
            capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            tail = (r.stderr or r.stdout or "").strip().splitlines()
            print(f"  [font] subset failed: {tail[-1] if tail else 'unknown error'}",
                  file=sys.stderr)
            return ""
        raw = open(out, "rb").read()
        print(f"  [font] {os.path.basename(src)} -> subset {len(raw) // 1024}KB woff2, "
              f"{len(chars)} chars")
        return base64.b64encode(raw).decode()
    finally:
        if os.path.exists(txt):
            os.remove(txt)


def font_face_css(b64):
    if not b64:
        return ""
    return ("@font-face{font-family:'%s';src:url(data:font/woff2;base64,%s) format('woff2');"
            "font-weight:400;font-display:swap;}" % (FONT_FAMILY, b64))


def preview_font_face():
    """preview.html references the full local font (its table has more text)."""
    if not os.path.isdir(FONT_DIR):
        return ""
    for f in sorted(os.listdir(FONT_DIR)):
        if f.startswith("subset"):
            continue
        if f.lower().endswith((".woff2", ".ttf", ".otf")):
            ext = f.rsplit(".", 1)[1].lower()
            fmt = {"woff2": "woff2", "ttf": "truetype", "otf": "opentype"}[ext]
            return ("@font-face{font-family:'%s';src:url('assets/font/%s') format('%s');}" %
                    (FONT_FAMILY, f, fmt))
    return ""


# ---- tiles ----
def _octicon(path_d, x, y, size, fill):
    """A 16x16 octicon drawn at `size`, its centre at (y) on the text baseline."""
    s = size / 16.0
    top = y - size * 0.78
    return (f'<g transform="translate({x:.2f},{top:.2f}) scale({s:.4f})">'
            f'<path fill="{fill}" d="{path_d}"/></g>')


def stats_row_svg(x, baseline, fs, parts, gap=0.55):
    """Star count, fork count, language dot and push date on one baseline.

    Mirrors the GitHub profile cards referenced in the project: a golden
    octicon glyph slightly larger than the text, then the number, then a
    coloured dot for the primary language. Everything scales with `fs` so it
    stays proportional inside any tile size.
    """
    icon = fs * 1.25          # icons read better a touch larger than the digits
    ICON_FILL = "#c9a34e"     # muted gold — bright enough to read, quiet enough not to shout
    out = []
    cx = x
    for i, (kind, val) in enumerate(parts):
        if kind == "star":
            out.append(_octicon(OCTICON_STAR, cx, baseline, icon, ICON_FILL))
            cx += icon + fs * 0.22
            out.append(f'<text x="{cx:.1f}" y="{baseline:.1f}" font-size="{fs}" '
                       f'fill="{INK_DIM}">{esc(val)}</text>')
            cx += text_w(str(val), fs)
        elif kind == "fork":
            out.append(_octicon(OCTICON_FORK, cx, baseline, icon, ICON_FILL))
            cx += icon + fs * 0.22
            out.append(f'<text x="{cx:.1f}" y="{baseline:.1f}" font-size="{fs}" '
                       f'fill="{INK_DIM}">{esc(val)}</text>')
            cx += text_w(str(val), fs)
        elif kind == "dot":
            colour = LANG_COLORS.get(val, INK_FAINT)
            r = fs * 0.28
            cy = baseline - fs * 0.30
            cx += r
            out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{colour}"/>')
            cx += r + fs * 0.28
            out.append(f'<text x="{cx:.1f}" y="{baseline:.1f}" font-size="{fs}" '
                       f'fill="{INK_DIM}">{esc(val)}</text>')
            cx += text_w(val, fs)
        elif kind == "text":
            out.append(f'<text x="{cx:.1f}" y="{baseline:.1f}" font-size="{fs}" '
                       f'fill="{INK_FAINT}">{esc(val)}</text>')
            cx += text_w(val, fs)
        if i < len(parts) - 1:
            cx += fs * gap
    return "".join(out)


def tile_svg(px, py, pw, ph, item, rank, share, heat, heat_idx):
    gap = 6
    x, y, w, h = px + gap / 2, py + gap / 2, pw - gap, ph - gap
    area = pw * ph
    big = area > 30000
    pad = 16 if w >= 150 else 10
    tx = x + pad
    maxw = max(18, w - 2 * pad)
    name = item["repo"].split("/", 1)[1]
    desc = clean_text(item["desc"])
    lang = item["lang"] if item["lang"] != "—" else ""
    micro = w < 86 or h < 56
    bar = h >= 108 and maxw >= 96

    tip = esc(f"{item['repo']}\n★{item['stars']} · fork {item['forks']}"
              f"{' · ' + lang if lang else ''}"
              f" · pushed {item['pushed']} ({item['days']}d ago) · {share * 100:.1f}% of map\n"
              + (desc + "\n" if desc else "")
              + " · ".join(clean_text(k) for k in item["key_points"]))
    parts = [f"<title>{tip}</title>"]

    # surface: heat wash on large tiles, flat wash on small ones
    if big:
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" '
                     f'fill="url(#hg{heat_idx})"/>')
    else:
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" '
                     f'fill="#ffffff" opacity="0.03"/>')
    sw = 2.0 if rank < 3 else 1.3
    op = 0.9 if rank < 3 else 0.62
    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="12" '
                 f'fill="none" stroke="{heat}" stroke-width="{sw}" opacity="{op}"/>')
    parts.append(f'<rect x="{tx:.1f}" y="{y + 1.5:.1f}" width="26" height="2.5" rx="1.25" '
                 f'fill="{heat}" opacity="0.9"/>')
    if not micro:
        parts.append(f'<text x="{x + w - pad:.1f}" y="{y + 20:.1f}" text-anchor="end" '
                     f'font-size="11" fill="{heat}" opacity="0.7">#{rank + 1}</text>')

    if micro:
        f = 12 if w >= 72 else 10.5
        parts.append(f'<text x="{x + w / 2:.1f}" y="{y + h / 2 + f * 0.36:.1f}" '
                     f'text-anchor="middle" font-size="{f}" fill="{INK}">'
                     f'{esc(_fit(name, w - 12, f))}</text>')
        return f"<g>{''.join(parts)}</g>"

    # rank watermark on oversized tiles only, kept well clear of the text column
    if area > 46000 and h > 200:
        wf = min(96, h * 0.42)
        parts.append(f'<text x="{x + w - pad:.1f}" y="{y + h - 40:.1f}" text-anchor="end" '
                     f'font-size="{wf:.0f}" fill="{heat}" opacity="0.05">'
                     f'{rank + 1:02d}</text>')

    # --- type scale follows the tile, not fixed thresholds ---
    fs_name = max(13.0, min(32.0, 0.085 * min(w, h * 1.6) + 6))
    while fs_name > 10 and text_w(name, fs_name) > maxw:
        fs_name -= 0.5

    # --- stats row: octicon + number, GitHub-card style ---
    # Three densities, chosen by what actually fits. The icons are drawn at the
    # text size so they sit on the same baseline as the numbers.
    meta_variants = [
        ("full",  [("star", item["stars"]), ("fork", item["forks"]),
                   ("dot", lang), ("text", item["pushed"])]),
        ("mid",   [("star", item["stars"]), ("fork", item["forks"]), ("dot", lang)]),
        ("mini",  [("star", item["stars"]), ("fork", item["forks"])]),
    ]

    bottom = y + h - (26 if bar else 12)
    top = y + 20
    avail = bottom - top - line_h(fs_name)

    def meta_width(parts, fs):
        """Approximate width of a stats row, icons included."""
        icon = fs * 1.25           # must match stats_row_svg's icon size
        pad = fs * 0.55            # gap between items
        total = 0.0
        for i, (kind, val) in enumerate(parts):
            if kind in ("star", "fork"):
                total += icon + fs * 0.22 + text_w(str(val) if val else "0", fs)
            elif kind == "dot":
                if val:
                    total += fs * 0.56 + text_w(val, fs)
            elif kind == "text":
                if val:
                    total += text_w(val, fs)
            if i < len(parts) - 1:
                total += pad
        return total

    def layout(fs_meta, fs_body, kp_cap=None):
        """Wrap the body at a given type size. Returns (rows, height)."""
        stats = []
        for _, parts in meta_variants:
            # drop trailing empty pieces (no language / no push date)
            trimmed = [p for p in parts if not (p[0] == "dot" and not p[1])
                       and not (p[0] == "text" and not p[1])]
            if trimmed and meta_width(trimmed, fs_meta) <= maxw:
                stats = trimmed
                break
        rows = []
        if stats:
            rows.append(("meta", stats, fs_meta, 0))
        kp_lines = []
        for kp in item["key_points"]:
            for i, ln in enumerate(_wrap_smart(clean_text(kp), maxw - 12, fs_body)):
                kp_lines.append(("kp" if i == 0 else "kpcont", ln, fs_body, 0))
        if kp_cap is not None:
            kp_lines = kp_lines[:kp_cap]
        if kp_lines:
            rows.append(("gap", "", 0, 7))
            rows.extend(kp_lines)
        hgt = sum((r[3] + line_h(r[2])) if r[0] != "gap" else r[3] for r in rows)
        return rows, hgt

    # Grow the body type until it fills the tile. The GitHub description is
    # deliberately not rendered: it usually restates the key-points, so showing
    # both duplicates the copy (it stays available in the hover title).
    fs_meta = max(10.5, min(13.0, fs_name * 0.52))
    fs_body = max(11.0, min(13.5, fs_name * 0.56))
    limit = max(15.0, fs_name * 0.78)
    rows, hgt = layout(fs_meta, fs_body)
    while fs_body < limit:
        next_body, next_meta = fs_body + 0.5, min(fs_meta + 0.25, 16.0)
        r2, h2 = layout(next_meta, next_body)
        if h2 > avail * 0.94:
            break
        fs_body, fs_meta, rows, hgt = next_body, next_meta, r2, h2

    # still too tall: drop trailing key-point lines, then the meta line
    cap = None
    while hgt > avail and rows:
        if cap is None:
            cap = sum(1 for r in rows if r[0] in ("kp", "kpcont")) - 1
        else:
            cap -= 1
        if cap < 0:
            rows, hgt = [], 0
            break
        rows, hgt = layout(fs_meta, fs_body, cap)
        if cap == 0:
            break

    # Name sits at a fixed offset from the top on every tile, so titles line up
    # across the grid. The body block below is vertically centered in the space
    # that's left, with a small fixed inter-line bonus so two-line tiles don't
    # look cramped. Spreading slack across line gaps instead reads as broken.
    cur = top
    base = cur + fs_name * 0.78
    parts.append(f'<text x="{tx:.1f}" y="{base:.1f}" font-size="{fs_name}" fill="{INK}">'
                 f'{esc(_fit(name, maxw, fs_name))}</text>')
    body_top = cur + line_h(fs_name) + (8 if rows else 0)

    slack = bottom - body_top - hgt
    cur = body_top + min(max(slack, 0) * 0.45, 28)
    extra = 1.5 if rows else 0

    for kind, txt, fs, lead in rows:
        cur += lead
        if kind == "gap":
            continue
        if cur + line_h(fs) > bottom:
            break
        if kind == "meta":
            parts.append(stats_row_svg(tx, cur + fs * 0.78, fs, txt))
        elif kind == "kp":
            parts.append(f'<text x="{tx:.1f}" y="{cur + fs * 0.78:.1f}" font-size="{fs}" '
                         f'fill="{INK}"><tspan fill="{heat}">›</tspan> {esc(txt)}</text>')
        else:
            parts.append(f'<text x="{tx + 12:.1f}" y="{cur + fs * 0.78:.1f}" font-size="{fs}" '
                         f'fill="{INK}">{esc(txt)}</text>')
        cur += line_h(fs) + extra

    if bar:
        by = y + h - 15
        bw = max(24, maxw - 66)
        parts.append(f'<rect x="{tx:.1f}" y="{by:.1f}" width="{bw:.1f}" height="3" rx="1.5" '
                     f'fill="#ffffff" opacity="0.08"/>')
        parts.append(f'<rect x="{tx:.1f}" y="{by:.1f}" width="{max(4, bw * item["fresh"]):.1f}" '
                     f'height="3" rx="1.5" fill="{heat}"/>')
        parts.append(f'<text x="{x + w - pad:.1f}" y="{by + 4.6:.1f}" text-anchor="end" '
                     f'font-size="9.5" fill="{INK_FAINT}">fresh {item["fresh"]:.2f}</text>')

    return f"<g>{''.join(parts)}</g>"


GROUP_HEADER_H = 20
GROUP_GAP = 8           # clear space between group regions
GROUP_PAD = 3           # breathing room between the border and the tiles inside


def group_tiles(items, weights, groups, map_h=None):
    """Split the map into one region per group, then lay tiles out inside each.

    Groups are laid out with the same squarified algorithm at the top level, so a
    group's region area is the sum of its tiles — the grouping shows up in the
    layout, not just as a label. Each region reserves a header strip for its name
    and is inset by half of GROUP_GAP, so neighbouring groups have visible air
    between them instead of sharing a hairline.

    Items whose `group` is empty or names a group that no longer exists are
    collected into an implicit "ungrouped" region. Without that they'd be laid
    out nowhere and silently vanish from the map.

    Returns (tile_rects, group_rects). Tile order follows the input order, which
    is the user's manual arrangement.
    """
    map_h = map_h or canvas_height(len(items))
    shares = area_shares(weights)
    declared = [g["name"] for g in (groups or [])]
    if not declared and not any(it.get("group") for it in items):
        return (squarify(list(enumerate(weights)), PAD, HEADER_H + PAD,
                         W - 2 * PAD, map_h - 2 * PAD), [])

    # bucket every item, in config order, so groups read top-to-bottom in the
    # order the user arranged
    buckets = {name: [] for name in declared}
    orphans = []
    for i, it in enumerate(items):
        name = it.get("group") or ""
        (buckets[name] if name in buckets else orphans).append(i)

    # a group keeps its declared position; the ungrouped bucket goes last.
    # Empty groups are kept too, with a small fixed share: they need a visible
    # (if tiny) region on the map, otherwise a freshly-created group has no drop
    # target and the only way to fill it is the editor's old group dropdown.
    layout_groups = [(name, buckets[name]) for name in declared]
    if orphans:
        layout_groups.append(("", orphans))

    # An empty group still needs a visible, hit-testable region — otherwise a
    # freshly created group has no drop target and can only be filled through
    # the editor. They share one small fixed budget so a pile of empty groups
    # can never crowd out the projects that actually exist.
    EMPTY_BUDGET = 0.14
    n_empty = sum(1 for _, members in layout_groups if not members)
    empty_share = (EMPTY_BUDGET / n_empty) if n_empty else 0.0

    # Squarify places items in the order it receives them, and a small group
    # arriving late gets whatever sliver is left over — a single-project group
    # came back as 35x495, too narrow to show a card. Placing the small groups
    # first lets them claim a full-height column while the map is still open,
    # and the big ones absorb the remainder (they tolerate any shape). The
    # user's declared order is restored afterwards for rendering.
    area_total = (W - 2 * PAD) * (map_h - 2 * PAD)
    def group_floor(n_members):
        """Minimum share a group needs to stay legible.

        A lone project in its own group used to fall back to whatever sliver
        squarify had left (30x492). A tile needs roughly 150px on its short
        side, so the group needs enough area to give a squarish slot at that
        size — ~150x150 for one card, scaling with the member count.
        """
        px = max(1, n_members) * (150 * 150)
        # A group is also bounded in one dimension by the map, so a short-but-wide
        # map still has to give it a workable column width.
        return min(px / area_total, 0.30)

    gweights, gmembers = [], []
    for name, members in layout_groups:
        key = len(gmembers)
        base = sum(shares[i] for i in members) or empty_share
        gweights.append((key, max(base, group_floor(len(members)))))
        gmembers.append(({"name": name}, members))

    raw_total = sum(w for _, w in gweights)
    if raw_total > 1.0:                              # floors overshot: rescale
        gweights = [(k, w / raw_total) for k, w in gweights]

    # Lay out small groups first (they need a squarish slot more than big ones
    # do), then map the results back to declaration order for rendering.
    by_size = sorted(gweights, key=lambda kv: kv[1])   # smallest first
    grects_sorted = squarify(by_size, PAD, HEADER_H + PAD, W - 2 * PAD, map_h - 2 * PAD)
    slot_of = {idx: rect for idx, *rect in grects_sorted}
    grects = [(i,) + tuple(slot_of[k]) for i, (k, _) in enumerate(gweights)]

    out, groups_out = [], []
    half = GROUP_GAP / 2
    for (gi, gx, gy, gw, gh), (g, members) in zip(grects, gmembers):
        # inset the whole region: neighbouring groups then read as separate blocks
        gx, gy, gw, gh = gx + half, gy + half, gw - GROUP_GAP, gh - GROUP_GAP
        if gw <= 0 or gh <= 0:
            continue
        groups_out.append((g, gx, gy, gw, gh))
        # Tiles are laid out inside the padded area; the border is still drawn on
        # the unpadded rect, so the dashes sit clear of the artwork. A sliver
        # region (squarify can return ~35px wide) keeps its full width — shaving
        # 4px off a 35px strip would cost more than the inset is worth.
        pad = GROUP_PAD if min(gw, gh) >= 120 else 0
        inner_x = gx + pad
        inner_w = gw - 2 * pad
        inner_y, inner_h = gy + pad, gh - 2 * pad
        # only a named region gets a header strip; "ungrouped" stays unlabelled
        if g["name"]:
            inner_y += GROUP_HEADER_H
            inner_h -= GROUP_HEADER_H
            if inner_h < 12:                  # region too short to label
                inner_y = gy + pad
                inner_h = gh - 2 * pad
        if inner_w <= 0 or inner_h <= 0:
            continue
        inner = squarify([(i, shares[i]) for i in members],
                         inner_x, inner_y, inner_w, inner_h)
        out.extend(inner)
    return out, groups_out


def build_svg(items, weights, date, groups=None, title="Featured Projects"):
    """Render the treemap. `groups` (list of {name}) draws group headers and
    confines each group's tiles to its own region; items must already be in the
    user's chosen order."""
    svg, _, _, _ = build_svg_layout(items, weights, date, groups, title)
    return svg


def build_svg_layout(items, weights, date, groups=None, title="Featured Projects"):
    """Like build_svg, but also returns tile geometry and group regions so the
    editor can lay an HTML interaction layer over the exact same boxes.

    Width is always W; height comes from canvas_height(len(items)) so adding
    tiles past the baseline grows the map instead of shrinking every tile.
    """
    map_h = canvas_height(len(items))
    total_h = HEADER_H + map_h
    rects, groups_out = group_tiles(items, weights, groups, map_h)
    rank_of = {idx: r for r, idx in enumerate(
        sorted(range(len(items)), key=lambda i: weights[i], reverse=True))}
    shares = area_shares(weights)

    # Which groups ended up with tiles? Empty ones get a dashed placeholder so a
    # freshly-created group is visible on the map and clearly a drop target.
    filled = {(it.get("group") or "") for it in items}

    group_bands = ""
    for g, gx, gy, gw, gh in groups_out:
        name = g["name"]
        empty = bool(name) and name not in filled
        if empty:
            # Dotted rather than dashed, and dimmer: an empty group still needs
            # to be visible as a drop target without competing with real ones.
            group_bands += (
                f'<rect x="{gx:.1f}" y="{gy:.1f}" width="{gw:.1f}" height="{gh:.1f}" rx="12" '
                f'fill="#ffffff" opacity="0.018"/>'
                f'<rect x="{gx + 0.75:.1f}" y="{gy + 0.75:.1f}" width="{gw - 1.5:.1f}" '
                f'height="{gh - 1.5:.1f}" rx="12" fill="none" stroke="#3b4759" '
                f'stroke-width="1.5" stroke-dasharray="2 4" stroke-linecap="round"/>'
                f'<text class="glabel" x="{gx + 11:.1f}" y="{gy + 15:.1f}" font-size="10.5" '
                f'fill="{INK_DIM}" opacity="0.85">{esc(name)}</text>')
            # "empty" hint, only when the region is tall enough to hold it
            if gh > 52:
                group_bands += (
                    f'<text x="{gx + gw / 2:.1f}" y="{gy + gh / 2 + 4:.1f}" '
                    f'text-anchor="middle" font-size="11" fill="{INK_FAINT}" '
                    f'opacity="0.75">拖入项目</text>')
            continue
        group_bands += (
            f'<rect x="{gx:.1f}" y="{gy:.1f}" width="{gw:.1f}" height="{gh:.1f}" rx="12" '
            f'fill="#ffffff" opacity="0.032"/>'
            f'<rect x="{gx + 0.75:.1f}" y="{gy + 0.75:.1f}" width="{gw - 1.5:.1f}" '
            f'height="{gh - 1.5:.1f}" rx="12" fill="none" stroke="#4d5c78" '
            f'stroke-width="1.5" stroke-dasharray="6 5"/>'
            f'<text class="glabel" x="{gx + 11:.1f}" y="{gy + 15:.1f}" font-size="10.5" '
            f'fill="{INK_DIM}" opacity="0.9">{esc(name)}</text>')

    tiles = []
    rects_out = {}
    for idx, rx, ry, rw, rh in rects:
        heat_idx = rank_of[idx] % len(HEAT)
        rects_out[items[idx]["repo"]] = {
            "x": round(rx, 1), "y": round(ry, 1),
            "w": round(rw, 1), "h": round(rh, 1),
            "rank": rank_of[idx], "share": round(shares[idx], 5),
        }
        tiles.append(tile_svg(rx, ry, rw, rh, items[idx], rank_of[idx],
                              shares[idx], HEAT[heat_idx], heat_idx))

    defs = "<defs>" + "".join(
        f'<linearGradient id="hg{i}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{c}" stop-opacity="0.13"/>'
        f'<stop offset="1" stop-color="{c}" stop-opacity="0.02"/>'
        f'</linearGradient>' for i, c in enumerate(HEAT)) + "</defs>"

    head = (
        f'<text x="20" y="33" font-size="24" fill="{INK}">{esc(title)}</text>'
        f'<text x="20" y="51" font-size="11.5" fill="{INK_FAINT}">'
        f'面积按 ★·fork·新鲜度加权 · 色深对应排名 · hover 看详情</text>'
        f'<text x="{W - 20}" y="33" text-anchor="end" font-size="11.5" fill="{INK_FAINT}">'
        f'Weidows · top {len(items)}</text>'
        f'<text x="{W - 20}" y="51" text-anchor="end" font-size="11" fill="{INK_FAINT}" '
        f'opacity="0.75">updated {esc(date)}</text>'
        f'<line x1="20" y1="{HEADER_H}" x2="{W - 20}" y2="{HEADER_H}" '
        f'stroke="#1a2130" stroke-width="1"/>')

    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{total_h}" '
           f'viewBox="0 0 {W} {total_h}" role="img" aria-labelledby="svgtitle svgdesc">'
           f'<title id="svgtitle">Featured projects treemap</title>'
           f'<desc id="svgdesc">Top {len(items)} repositories sized by stars, forks and '
           f'recency, colored by rank.</desc>'
           f'<style>__FONTFACE__text{{font-family:"{FONT_FAMILY}","Segoe UI",system-ui,sans-serif;}}'
           f'</style>'
           f'<rect width="{W}" height="{total_h}" rx="16" fill="#0b0e13"/>'
           f'<rect x="0.5" y="0.5" width="{W - 1}" height="{total_h - 1}" rx="15.5" fill="none" '
           f'stroke="#1c2330" stroke-width="1"/>'
           f'{defs}{head}{group_bands}{"".join(tiles)}</svg>')

    regions = [{"group": g["name"], "x": round(gx, 1), "y": round(gy, 1),
                "w": round(gw, 1), "h": round(gh, 1)}
               for g, gx, gy, gw, gh in groups_out]
    return svg, rects_out, regions, {"date": date, "w": W, "h": total_h,
                                     "map_h": map_h}


def svg_chars(svg):
    """Every visible glyph in the SVG — the subset is derived from this, not a
    hand-maintained list that drifts out of sync."""
    body = re.sub(r"<style>.*?</style>", "", svg, flags=re.S)
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    chars = set()
    for t in re.findall(r">([^<>]*)<", body):
        chars.update(html.unescape(t))
    return "".join(sorted(c for c in chars if c == " " or not c.isspace()))


def build_markdown(items, weights, shares, groups=None, image="dashboard.svg",
                   user="Weidows"):
    """The profile README block: the treemap image, then a linked list.

    A single <img> on GitHub can only carry one link (an SVG loaded through
    <img> is sealed — inner <a> elements are inert and <map>/<area> are stripped
    by the sanitiser). So the image goes on top unlinked, and each project gets
    a real markdown link in a list underneath. That keeps the treemap's area
    proportions while still giving every card its own clickable destination.

    The list mirrors the map's grouping and order, so scanning down it matches
    scanning across the image.
    """
    declared = [g["name"] for g in (groups or [])]
    buckets = {name: [] for name in declared}
    orphans = []
    for idx, it in enumerate(items):
        name = it.get("group") or ""
        (buckets[name] if name in buckets else orphans).append(idx)

    def entry(idx):
        it = items[idx]
        repo = it["repo"]
        url = f"https://github.com/{repo}"
        slug = repo.split("/", 1)[1]
        share = shares[idx]
        stats = []
        if it["stars"]:
            stats.append(f"★ {it['stars']}")
        if it["forks"]:
            stats.append(f"fork {it['forks']}")
        lang = it["lang"] if it["lang"] != "—" else ""
        if lang:
            stats.append(lang)
        stats.append(f"{share * 100:.1f}%")

        line = f"- [**{slug}**]({url})"
        if stats:
            line += " — " + " · ".join(stats)
        if it["key_points"]:
            line += "： " + " / ".join(clean_text(k) for k in it["key_points"])
        return line

    lines = [f'<img src="{image}" alt="Featured projects" width="{W}">', ""]
    for name in declared:
        members = buckets[name]
        if not members:
            continue
        lines.append(f"**{name}**")
        lines.append("")
        lines.append("\n".join(entry(i) for i in members))
        lines.append("")
    if orphans:
        lines.append("\n".join(entry(i) for i in orphans))
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_preview(svg, items, weights, shares, groups=None):
    group_of = {it["repo"]: it.get("group", "") for it in items}
    rows = []
    for it, w, s in zip(items, weights, shares):
        rows.append(
            f"<tr><td><b>{esc(it['repo'])}</b><br><small>{esc(it['desc'][:90])}</small></td>"
            f"<td>{esc(group_of.get(it['repo'], ''))}</td>"
            f"<td class=num>{it['stars']} / {it['forks']}</td><td>{esc(it['lang'])}</td>"
            f"<td class=num>{esc(it['pushed'])}</td><td class=num>{it['days']}d</td>"
            f"<td class=num>{w:.2f}</td><td class=num>{s * 100:.1f}%</td>"
            f"<td class=num>{it['fresh']:.2f}</td><td class=num>{it['boost']}</td>"
            f"<td>{esc(' / '.join(it['key_points']))}</td></tr>")
    return f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>profile dashboard 预览</title>
<style>{preview_font_face()}
:root{{color-scheme:dark}}
body{{background:#05070b;color:#dde5ee;margin:32px 24px;
font-family:"{FONT_FAMILY}","Segoe UI",system-ui,sans-serif}}
.wrap{{max-width:920px;margin:auto}}
h1{{font-size:19px;font-weight:400;margin:0 0 4px}}
.sub{{color:#5b6675;font-size:12px;margin:0 0 20px}}
svg{{width:100%;height:auto;border-radius:16px;display:block}}
table{{border-collapse:collapse;width:100%;font-size:12.5px;margin-top:26px}}
th{{text-align:left;color:#8d99a9;font-weight:400;border-bottom:1px solid #1c2330;
padding:8px 10px;white-space:nowrap}}
td{{border-bottom:1px solid #121821;padding:8px 10px;vertical-align:top}}
tbody tr:nth-child(even){{background:#080b11}}
.num{{font-variant-numeric:tabular-nums;color:#9fb8cf;white-space:nowrap}}
small{{color:#5b6675;font-size:11.5px}}
.note{{color:#5b6675;font-size:12px;line-height:1.7;margin-top:22px}}
code{{color:#93bcab}}</style></head><body><div class="wrap">
<h1>GitHub Profile Dashboard · 本地预览</h1>
<p class="sub">宽 880 固定 · 高度随项目数增长 · README 正文宽 896px，留边距不被缩放</p>
{svg}
<table><thead><tr><th>repo</th><th>分组</th><th>★ / fork</th><th>语言</th><th>push</th><th>距今</th>
<th>weight</th><th>面积</th><th>fresh</th><th>boost</th><th>key-points</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
<p class="note">改 <code>projects.json</code>（增删项目、key-points、boost）后重跑
<code>python generate.py</code>；只调样式/文案用 <code>--offline</code> 免 API 配额。
想在网页里刷新候选项目 / 分组 / 排序，跑 <code>python generate.py --serve</code>。
得意黑 Smiley Sans（OFL-1.1）按实际用字子集化后内嵌进 SVG，GitHub 上直接渲染。</p>
</div></body></html>"""


def load_config():
    with open(PROJECTS_JSON, encoding="utf-8") as f:
        return json.load(f)


def save_config(cfg):
    tmp = PROJECTS_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    os.replace(tmp, PROJECTS_JSON)


def load_cache():
    if os.path.exists(CACHE_JSON):
        with open(CACHE_JSON, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(cache):
    tmp = CACHE_JSON + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=1)
    os.replace(tmp, CACHE_JSON)


def resolve_items(cfg, cache, offline=False, token=None, refresh=False):
    """Turn config + cache into scored items in the user's chosen order.

    Items are emitted in config order (the manual arrangement), NOT sorted by
    weight — the treemap ranks tiles by weight for colour and area, but the
    layout order belongs to the user.
    """
    items, weights = [], []
    for p in cfg["projects"]:
        repo = p["repo"]
        data = cache.get(repo)
        if not offline and (refresh or data is None):
            try:
                data = fetch_repo(repo, token)
                cache[repo] = data
            except Exception as e:
                if data is None:
                    raise
                print(f"fetch {repo} failed: {e} (used cache)", file=sys.stderr)
        if data is None:
            raise RuntimeError(f"no cached data for {repo} — fetch it first")
        w, st, fk, lang, pushed, days, fresh, desc = score_repo(data, p.get("boost", 1.0))
        items.append({**p, "weight": w, "stars": st, "forks": fk, "lang": lang,
                      "pushed": pushed, "days": days, "fresh": fresh, "desc": desc})
        weights.append(w)
    return items, weights


_FONT_CACHE = {}


def _subset_cached(chars):
    """Subsetting shells out to fontTools (~1s). Live editing re-renders on every
    drag, and the glyph set barely changes, so memoise on the char set."""
    key = hash(chars)
    if key not in _FONT_CACHE:
        if len(_FONT_CACHE) > 8:          # keep the map small
            _FONT_CACHE.clear()
        _FONT_CACHE[key] = font_face_css(subset_font_b64(chars))
    return _FONT_CACHE[key]


def render(items, weights, groups=None, date=None, title="Featured Projects"):
    """Build the final SVG string with the font subset embedded."""
    return render_layout(items, weights, groups, date, title)[0]

def render_layout(items, weights, groups=None, date=None, title="Featured Projects"):
    """Render and also return tile geometry + group regions + canvas size."""
    date = date or datetime.date.today().isoformat()
    svg, rects, regions, meta = build_svg_layout(items, weights, date, groups, title)
    if METRICS.missing:
        print(f"  [font] {len(METRICS.missing)} glyph(s) not in Smiley Sans "
              f"({''.join(sorted(METRICS.missing))!r}) — browser falls back for those",
              file=sys.stderr)
    css = _subset_cached(svg_chars(svg))
    return svg.replace("__FONTFACE__", css), rects, regions, meta


def main():
    argv = sys.argv[1:]
    if any(a in ("--help", "-h") for a in argv):
        print(__doc__)
        return

    flags = {"--offline", "--serve", "--no-open"}
    port = 8765
    unknown = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in flags:
            pass
        elif a == "--port":
            if i + 1 >= len(argv):
                sys.exit("--port needs a value")
            try:
                port = int(argv[i + 1])
            except ValueError:
                sys.exit(f"invalid port: {argv[i + 1]!r}")
            i += 1
        elif a.startswith("--port="):
            try:
                port = int(a.split("=", 1)[1])
            except ValueError:
                sys.exit(f"invalid port: {a!r}")
        else:
            unknown.append(a)
        i += 1
    if unknown:
        sys.exit(f"unknown argument(s): {' '.join(unknown)} (try --help)")

    if "--serve" in argv:
        import server
        return server.run(port=port, open_browser="--no-open" not in argv)

    offline = "--offline" in argv
    cfg = load_config()
    cache = load_cache()

    global METRICS
    METRICS = Metrics(find_font_source())

    items, weights = resolve_items(cfg, cache, offline, os.environ.get("GITHUB_TOKEN"))
    if not offline:
        save_cache(cache)

    svg, _, _, canvas = render_layout(items, weights, cfg.get("groups"))
    shares = area_shares(weights)
    md = build_markdown(items, weights, shares, cfg.get("groups"),
                        user=cfg.get("user", "Weidows"))
    open(SVG_OUT, "w", encoding="utf-8").write(svg)
    open(PREVIEW_OUT, "w", encoding="utf-8").write(
        build_preview(svg, items, weights, shares, cfg.get("groups")))
    open(MD_OUT, "w", encoding="utf-8").write(md)
    print(f"wrote {SVG_OUT} ({canvas['w']}x{canvas['h']}, {len(svg) // 1024}KB)")
    print(f"wrote {PREVIEW_OUT} and {MD_OUT} ({len(md)} chars)")
    for it, s in zip(items, shares):
        print(f"  {it['weight']:7.2f} {s * 100:5.1f}%  ★{it['stars']:<3} f{it['forks']:<2} "
              f"{it['pushed']}  {it['repo']}")


if __name__ == "__main__":
    main()
