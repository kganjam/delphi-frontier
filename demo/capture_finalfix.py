"""Addendum captures for the final-fix pass: live System > How it was built (provider jobs, controller outcomes, dated record rows for
Evo2 telemetry and Gemini embedding usage) and the header search for 'fish'. Real 1920x1080 live screenshots, nothing composited.
Writes only under the given output dir (a separate addendum manifest; the original capture manifest is not touched)."""
import datetime
import hashlib
import json
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
SECRET = re.compile(r"bearer\s+[a-z0-9._-]{12,}|sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|token=[A-Za-z0-9._-]{12,}|api[_-]?key\s*[:=]\s*\S{12,}", re.I)
rows = []


def h3_top(p, text, dy=110):
    p.evaluate("([t,dy]) => { const h=[...document.querySelectorAll('main h3')].find(e=>e.textContent.trim().startsWith(t)); if(h) window.scrollTo(0, h.getBoundingClientRect().top + scrollY - dy); }", [text, dy])
    p.wait_for_timeout(700)


def row_top(p, text, dy=300):
    p.evaluate("([t,dy]) => { const r=[...document.querySelectorAll('main tr')].find(e=>e.innerText.includes(t)); if(r) window.scrollTo(0, r.getBoundingClientRect().top + scrollY - dy); }", [text, dy])
    p.wait_for_timeout(700)


def search_fish(p):
    p.goto(BASE + "#/home", wait_until="load")
    p.wait_for_timeout(1500)
    p.fill("#gq", "fish")
    p.press("#gq", "Enter")
    p.wait_for_selector("main h1", timeout=20000)
    p.wait_for_timeout(4500)
    p.evaluate("() => { const e=document.querySelector('main h1'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 110); }")
    p.wait_for_timeout(600)


SCENES = [
    ("ff1-built-own-provider-jobs", "#/work?tab=built", lambda p: h3_top(p, "Own provider jobs"), "System > How it was built: 'Own provider jobs' section (dated 2026-10-31 18:31:20 PDT per the page)", None, 'main h3'),
    ("ff2-built-controller-outcomes", "#/work?tab=built", lambda p: h3_top(p, "Controller outcomes"), "System > How it was built: 'Controller outcomes for recent GPU tasks'", None, 'main h3'),
    ("ff3-built-dated-record-evo2-telemetry", "#/work?tab=built", lambda p: row_top(p, "evo2-zebrafish-h100", 330), "System > How it was built: 'Dated record' table at the evo2-zebrafish-h100 GPU telemetry row (493 samples at 1000 ms per the row)", None, 'main h3'),
    ("ff3z-built-evo2-row-zoom", "#/work?tab=built", lambda p: row_top(p, "evo2-zebrafish-h100", 330), "1.25x crop around the evo2-zebrafish-h100 telemetry row", "main tr:has-text('evo2-zebrafish-h100')", 'main h3'),
    ("ff4-built-gemini-embedding-usage-zoom", "#/work?tab=built", lambda p: row_top(p, "gemini-embedding-001", 330), "1.25x crop around the 'model usage google-generative-language gemini-embedding-001' row", "main tr:has-text('gemini-embedding-001')", 'main h3'),
    ("ff5-search-fish-typed", "#/home", search_fish, "Header search typed 'fish' then Enter: ranked results with engine/index line", None, 'main h1'),
]
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for name, route, prep, desc, zoom, ready in SCENES:
        c = br.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=1.25 if zoom else 1)
        p = c.new_page()
        errs = []
        p.on("pageerror", lambda e: errs.append(str(e)[:160]))
        row = {"file": f"{name}.png", "route": route, "viewport": "1920x1080", "description": desc}
        try:
            p.goto(BASE + route, wait_until="load")
            p.wait_for_selector(ready, timeout=25000)
            p.wait_for_timeout(2500)
            prep(p)
            row["secret_pattern_in_page_text"] = bool(SECRET.search(p.evaluate("() => document.body.innerText")))
            f = OUT / row["file"]
            if zoom:
                bb = p.locator(zoom).first.bounding_box()
                y0 = max(105, min(bb["y"] - 160, 1080 - 864))   # below the 99 px sticky header
                p.screenshot(path=str(f), clip={"x": 192, "y": y0, "width": 1536, "height": 864})
                row["zoom"] = "1536x864 CSS px at device scale 1.25 (file is 1920x1080), table full width, sticky header excluded"
            else:
                p.screenshot(path=str(f))
            row["sha256"] = hashlib.sha256(f.read_bytes()).hexdigest()
            row["time_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
            row["page_errors"] = errs
        except Exception as e:
            row["capture_error"] = repr(e)[:200]
        rows.append(row)
        c.close()
        p = None
    snap = br.new_context().request.get(BASE + "data/snapshot.json", timeout=60000).body()
    live = {}
    for r in ["index.html", "js/app.js", "js/views4.js", "js/demo.js"]:
        live[r] = hashlib.sha256(br.new_context().request.get(BASE + ("" if r == "index.html" else r), timeout=30000).body()).hexdigest()
    br.close()
(OUT / "captures-finalfix-manifest.json").write_text(json.dumps({
    "note": "ADDENDUM manifest; the original capture-manifest.json (33 rows) is not modified.",
    "release": "not identified as one commit: the live files equal e246a51c0c467c95d42d384129c5358973b65a83's site/ (js, css, index, snapshot) except js/demo.js, which e246a51 does not have",
    "live_file_sha256": live, "live_snapshot_sha256": hashlib.sha256(snap).hexdigest(), "rows": rows}, indent=1))
print([r["file"] for r in rows if "capture_error" in r])
