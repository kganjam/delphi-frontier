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


def eco_play(p):
    p.wait_for_selector("#eco-host canvas", timeout=30000)
    p.wait_for_timeout(2500)
    top(p, "#eco-host", 108)
    p.get_by_role("button", name="Play").first.click()
    p.wait_for_timeout(3500)
    p.get_by_role("button", name="Play").first.click() if p.get_by_role("button", name="Pause").count() == 0 else p.get_by_role("button", name="Pause").first.click()
    p.wait_for_timeout(600)


def gen_side_by_side(p):
    p.evaluate("() => { const i=[...document.querySelectorAll('main img')].find(x=>/solver-versus-generated-u/.test(x.src)); if(i) window.scrollTo(0, i.getBoundingClientRect().top + scrollY - 190); }")
    p.wait_for_timeout(1200)


def fz_lower(p):
    p.evaluate("() => { const e=[...document.querySelectorAll('main h2')].find(x=>/^Check this proposal/.test(x.textContent.trim())); if(e) window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 130); }")
    p.wait_for_timeout(800)


SCENES = [
    ("21-experimentation-plan-table", "#/experimentation", lambda p: top(p, "#ex-plan", 110), "Experimentation: candidate designs ranked 1 and 2 with target variance prior to expected posterior (0.36 to 0.0189474 vs 0.232941), assumed units; prospective only", "#ex-plan", None),
    ("21z-experimentation-plan-zoom", "#/experimentation", lambda p: top(p, "#ex-plan", 110), "Zoomed 960x540 at 2x: the plan table rows (order, design, likelihood rank, cost, target variance, reduction per cost)", "#ex-plan", "#ex-plan table"),
    ("22-ecology-saved-state-viewer", "#/ecology", lambda p: (p.wait_for_selector("#eco-host canvas", timeout=30000), p.wait_for_timeout(2500), top(p, "#eco-host", 108)), "Ecology: saved-state viewer (WebGL) at t=0; page labels states as saved run output, run ended early, flags quoted", "#eco-host", None),
    ("23-ecology-viewer-after-play", "#/ecology", eco_play, "Ecology viewer after a real Play click and ~3.5 s of playback, then paused (time advanced from 0.000 s)", "#eco-host", None),
    ("24-ecology-rendered-movies", "#/ecology", h2_top("Rendered movies", 110), "Ecology: the 'Rendered movies' section; the mp4s (glide.mp4, school.mp4) are site artifacts; headless Chromium may not decode them, check the frame", "main h1", None),
    ("25-generative-diffusion-recorded", "#/generative", lambda p: top(p, "#diffusion-recorded", 110), "Generative: recorded reverse diffusion figure (state 04/20) with its labels: abstract reaction-diffusion fields, not fish", "#diffusion-recorded", None),
    ("26-generative-solver-vs-generated", "#/generative", gen_side_by_side, "Generative: recorded solver versus generated u-channel and v-channel images side by side", "#diffusion-recorded", None),
    ("27-system-overview", "#/work", lambda p: top(p, "main h1", 100), "System overview at this release", "main h1", None),
    ("28-system-how-built", "#/work?tab=built", lambda p: top(p, "main h1", 100), "System > How it was built at this release (dated counters, provider outcomes)", "main h1", None),
    ("29-formalize-proposal-checker", "#/formalize", lambda p: top(p, "main h1", 100), "Proposal checker: source passage and proposed constraints; page says it checks written constraints, no Lean is run", "main h1", None),
    ("30-formalize-check-section", "#/formalize", fz_lower, "Proposal checker: 'Check this proposal' section (not clicked; no check was run for this capture)", "main h1", None),
    ("31-frontier-whiteboard", "#/frontier", lambda p: top(p, "#wbgraph", 120), "Frontier: open-questions whiteboard graph", "#wbgraph", None),
    ("32-blueprints-overview-recheck", "#/blueprints", lambda p: top(p, "main h1", 100), "Blueprints top at this release (set 1 had literal HTML and [object Object] on dc57df0): check before use", "main h1", None),
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
            row["mode"] = "live site, real interaction" if name in ("23-ecology-viewer-after-play",) else "live site, real navigation"
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
