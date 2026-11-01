"""Second single-load follow-up: flying-fish studio (3D, downloads), knowledge graph, history page structure. Read-only."""
import hashlib
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
out = {}
with sync_playwright() as pw:
    br = pw.chromium.launch()
    c = br.new_context(viewport={"width": 1440, "height": 900})
    p = c.new_page()
    p.errs = []
    p.on("pageerror", lambda e: p.errs.append(str(e)[:160]))
    p.goto(BASE + "#/studio/flying-fish", wait_until="load")
    p.wait_for_timeout(8000)
    out["flying_fish"] = p.evaluate("() => ({h1: document.querySelector('h1')?.textContent, canvas: document.querySelectorAll('canvas').length, dl: [...new Set([...document.querySelectorAll('a[href]')].map(a=>a.href).filter(h=>/\\.(stl|glb|tar|xz|zip|json|csv|mp4)(\\?|$)/i.test(h)))].slice(0,30), tabs: [...document.querySelectorAll('[role=tab],button[aria-selected]')].map(e=>e.textContent.trim().slice(0,30)).slice(0,12)})")
    out["flying_fish"]["errs"] = p.errs
    p.screenshot(path="critique/d531330/screens/followup-flying-fish.png")
    rows = []
    for h in out["flying_fish"]["dl"][:12]:
        r = c.request.head(h, timeout=20000)
        row = {"url": h.replace(BASE, ""), "status": r.status, "bytes": r.headers.get("content-length"), "type": r.headers.get("content-type")}
        if r.status == 200 and (not row["bytes"] or int(row["bytes"]) <= 6_000_000):
            b = c.request.get(h, timeout=30000).body()
            row.update(got_bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
        rows.append(row)
    out["downloads"] = rows
    p.goto(BASE + "#/knowledge?tab=graph", wait_until="load")
    p.wait_for_timeout(4000)
    out["knowledge_graph"] = p.evaluate("() => { const s=document.querySelector('main svg'); return s ? {children: [...new Set([...s.querySelectorAll('*')].map(e=>e.tagName))], n: s.querySelectorAll('*').length, label: s.getAttribute('aria-label') || s.querySelector('title')?.textContent, clickable: s.querySelectorAll('a,[tabindex],[role=button]').length} : null }")
    p.goto(BASE + "#/history", wait_until="load")
    p.wait_for_timeout(3000)
    out["history"] = p.evaluate("() => ({headings: [...document.querySelectorAll('main h2,main h3')].map(e=>e.textContent.trim().slice(0,50)).slice(0,12), imgs: document.querySelectorAll('main img').length, imgs_noalt: [...document.querySelectorAll('main img')].filter(i=>!i.alt).length, tables: document.querySelectorAll('main table').length, forms: document.querySelectorAll('main form').length, buttons: [...document.querySelectorAll('main button')].map(b=>b.textContent.trim().slice(0,30)).slice(0,8)})")
    c.close()
    br.close()
Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
