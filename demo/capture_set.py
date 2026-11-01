"""Real 1920x1080 Playwright captures of the live Frontier site for the narrated demo. Every frame is a viewport screenshot of the
live UI after real navigation/interaction; nothing is composited or animated. Manifest rows carry route, release, time, viewport, sha256,
description, interaction and WebGL renderer. Read-only (header search is a hash navigation)."""
from __future__ import annotations

import datetime
import hashlib
import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
OUT = Path(sys.argv[1])
RELEASE = sys.argv[2]
ONLY = set(sys.argv[3].split(",")) if len(sys.argv) > 3 else None
SECRET = re.compile(r"bearer\s+[a-z0-9._-]{12,}|sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|token=[A-Za-z0-9._-]{12,}|api[_-]?key\s*[:=]\s*\S{12,}", re.I)


def top(p, sel, dy=108):
    p.evaluate("([s,dy]) => { const e=document.querySelector(s); if(e){ window.scrollTo(0, e.getBoundingClientRect().top + scrollY - dy); } }", [sel, dy])
    p.wait_for_timeout(700)


def s_home(p):
    p.wait_for_selector(".mv-stage[data-mode=interactive]", timeout=45000)
    p.wait_for_timeout(2500)
    top(p, ".mv", 100)


def s_mesh_pick(p):
    p.wait_for_selector(".mv-stage[data-mode=interactive]", timeout=45000)
    p.wait_for_timeout(2000)
    top(p, ".mv-stage", 110)
    cv = p.locator(".mv-stage canvas").first
    b = cv.bounding_box()
    cv.focus()
    for _ in range(4):
        p.keyboard.press("ArrowRight")
    p.wait_for_timeout(400)
    for fx, fy in [(0.5, 0.5), (0.3, 0.6), (0.62, 0.55)]:
        p.mouse.click(b["x"] + b["width"] * fx, b["y"] + b["height"] * fy)
        p.wait_for_timeout(350)
        if "Click a part" not in p.evaluate("() => document.querySelector('.mv-detail, .mv [class*=detail]')?.innerText || ''"):
            break
    cv.evaluate("e => e.blur()")
    p.wait_for_timeout(400)


def s_search(p):
    p.goto(BASE + "#/home", wait_until="load")
    p.wait_for_timeout(1500)
    p.fill("#gq", "fin mechanics")
    p.press("#gq", "Enter")
    p.wait_for_timeout(3500)
    top(p, "main h1", 110)


def s_graph_node(p):
    p.locator("main svg g.g-node").nth(3).click()
    p.wait_for_timeout(1200)


def h2_top(text, dy=110):
    return lambda p: p.evaluate("([t,dy]) => { const h=[...document.querySelectorAll('main h2')].find(e=>e.textContent.trim().startsWith(t)); if(h) window.scrollTo(0, h.getBoundingClientRect().top + scrollY - dy); }", [text, dy])


def s_scale_cell(p):
    p.locator("main a:text-is('Cell')").first.click()
    p.wait_for_timeout(1500)
    h2_top("Scales", 110)(p)
    p.wait_for_timeout(500)


# (name, route, prep, description, ready selector, zoom selector or None). zoom = a 960x540 CSS-pixel region rendered at 2x so the file is
# a crisp 1920x1080 frame of the same live layout (not an upscale).
SCENES = [
    ("01-hero-3d-mesh", "#/home", s_home, "Home: real 3D fish mesh viewer (actual GLB), interactive WebGL", ".mv-stage[data-mode=interactive]", None),
    ("02-mesh-part-provenance", "#/home", s_mesh_pick, "After keyboard orbit and a click on the mesh: part detail with GLB node provenance", ".mv-stage[data-mode=interactive]", None),
    ("03-engineering-recorded-runs", "#/engineering", lambda p: top(p, "main h1", 100), "Engineering: recorded geometry and simulation outputs, each with its hash (a gallery; use as a cutaway, not a read)", "main h1", None),
    ("04-studio-scale-navigation", "#/engineering", s_scale_cell, "Engineering: scale navigation (Molecular ... Evolution / ecology), 'Cell' scale selected by a real click", "main h1", None),
    ("05-studio-project-design-review", "#/studio/flying-fish", lambda p: top(p, "main h1", 100), "Studio project: Flying fish, design review with exact-version challenges", "main h1", None),
    ("06-search-results", "#/home", s_search, "Header search 'fin mechanics': results are labelled by the page as engine 'hybrid' (lexical plus vector, model gemini-embedding-001), each score shown with its kind", "main h1", None),
    ("07-claim-equations", "#/knowledge/fisher-ftns", lambda p: p.wait_for_selector(".katex", timeout=15000), "A claim with rendered equations (KaTeX), source and assumptions", ".katex", None),
    ("07z-claim-equations-zoom", "#/knowledge/fisher-ftns", lambda p: (p.wait_for_selector(".katex", timeout=15000), top(p, ".katex", 200)), "Zoomed 960x540 region at 2x: the claim's equation, context and assumptions", ".katex", ".katex"),
    ("08-knowledge-graph", "#/knowledge?tab=graph", lambda p: top(p, "main svg", 110), "Claim graph: nodes are claims, edges typed", "main svg", None),
    ("09-graph-node-detail", "#/knowledge?tab=graph", lambda p: (s_graph_node(p), top(p, "main svg", 110)), "Claim graph after clicking a node: detail panel", "main svg", None),
    ("10-blueprints-actors", "#/blueprints", lambda p: top(p, "#bp-act", 110), "Blueprints: regulatory actors table (roles, evidence class, what the sources do and do not show)", "#bp-act", None),
    ("11-blueprints-sources", "#/blueprints", lambda p: top(p, "#bp-src", 110), "Blueprints: source citations with read level of each source", "#bp-src", None),
    ("12-claim-reuse-dispute", "#/reuse", lambda p: top(p, "main h1", 100), "Claim reuse and an independent dispute", "main h1", None),
    ("13-system-provider-outcomes", "#/work?tab=built", lambda p: top(p, "main h1", 100), "System > How it was built: recorded counters incl. GPU jobs 31 (22 completed, 6 failed, 3 cancelled) with limits and source files", "main h1", None),
    ("14-system-receipts", "#/work?tab=receipts", lambda p: top(p, "main h1", 100), "System > Receipts: three measured receipts with hashes and what each covers", "main h1", None),
    ("15-simulations-index", "#/simulations", lambda p: top(p, "main h1", 100), "Simulations index with recorded players (video playback not captured: see manifest note)", "main h1", None),
]

OUT.mkdir(parents=True, exist_ok=True)
rows = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for name, route, prep, desc, ready, zoom in SCENES:
        if ONLY and name not in ONLY:
            continue
        c = br.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=2 if zoom else 1)
        p = c.new_page()
        errs = []
        p.on("pageerror", lambda e: errs.append(str(e)[:160]))
        p.goto(BASE + route, wait_until="load")
        row = {"file": f"{name}.png", "route": route, "releaseSHA": RELEASE, "viewport": "1920x1080", "description": desc}
        try:
            p.wait_for_selector(ready, timeout=20000)
            p.wait_for_timeout(1500)
            prep(p)
            row["secret_pattern_in_page_text"] = bool(SECRET.search(p.evaluate("() => document.body.innerText")))
            gl = p.evaluate("() => { const c=document.createElement('canvas'); const g=c.getContext('webgl2')||c.getContext('webgl'); if(!g) return null; const x=g.getExtension('WEBGL_debug_renderer_info'); return x? g.getParameter(x.UNMASKED_RENDERER_WEBGL): 'webgl (renderer hidden)'; }")
            row["webgl_renderer"] = gl
            f = OUT / row["file"]
            if zoom:
                bb = p.locator(zoom).first.bounding_box()
                x0 = max(0, min(bb["x"] - 40, 1920 - 960))
                y0 = max(0, min(bb["y"] - 30, 1080 - 540))
                p.screenshot(path=str(f), clip={"x": x0, "y": y0, "width": 960, "height": 540})
                row["zoom"] = "960x540 CSS px at device scale 2 (file is 1920x1080)"
            else:
                p.screenshot(path=str(f))
            row["sha256"] = hashlib.sha256(f.read_bytes()).hexdigest()
            row["time_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
            row["mode"] = "live site, real interaction" if name in ("02-mesh-part-provenance", "04-studio-scale-navigation", "06-search-results", "09-graph-node-detail") else "live site, real navigation"
            row["page_errors"] = errs
        except Exception as e:
            row["capture_error"] = repr(e)[:200]
        rows.append(row)
        c.close()
        time.sleep(3)
    br.close()
mf = OUT / "capture-manifest.json"
old = json.loads(mf.read_text()) if mf.exists() and ONLY else []
by = {r["file"]: r for r in old}
by.update({r["file"]: r for r in rows})
mf.write_text(json.dumps(list(by.values()), indent=1))
print(len(rows), [r["file"] for r in rows if "capture_error" in r])
