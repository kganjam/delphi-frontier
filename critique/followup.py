"""Single-load follow-ups for items the bulk crawl flagged. Read-only; one page at a time with pauses."""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
out = {}
with sync_playwright() as pw:
    br = pw.chromium.launch()

    def load(route, wait=3500):
        c = br.new_context(viewport={"width": 1440, "height": 900})
        p = c.new_page()
        p.errs, p.bad = [], []
        p.on("pageerror", lambda e: p.errs.append(str(e)[:160]))
        p.on("response", lambda r: p.bad.append(f"{r.status} {r.url[-70:]}") if r.status >= 400 else None)
        p.on("requestfailed", lambda r: p.bad.append(f"FAILED {r.url[-70:]} {r.failure}"))
        p.goto(BASE + route, wait_until="load")
        p.wait_for_timeout(wait)
        return c, p

    c, p = load("#/work")
    out["work_null_context"] = p.evaluate("() => { const t=document.querySelector('main').innerText; const i=t.search(/\\bnull\\b/); return i<0?null:t.slice(Math.max(0,i-80),i+60); }")
    c.close()
    c, p = load("#/graph")
    out["graph_unnamed"] = p.evaluate("() => [...document.querySelectorAll('button,a[href],[role=button]')].filter(e=>!(e.getAttribute('aria-label')||e.textContent||e.title||'').trim()).map(e=>e.outerHTML.slice(0,200))")
    out["graph_text"] = p.evaluate("() => document.querySelector('main').innerText.slice(0,300)")
    c.close()
    c, p = load("#/search?q=zzqxjv&tab=catalog")
    out["search_nonsense_text"] = p.evaluate("() => document.querySelector('main').innerText.slice(0,700)")
    c.close()
    c, p = load("#/evidence")
    out["evidence_notfound_context"] = p.evaluate("() => { const t=document.querySelector('main').innerText; const i=t.search(/not found/i); return i<0?null:t.slice(Math.max(0,i-80),i+80); }")
    c.close()
    for slug in ["morpholib-pezzulo-bioelectric-target-morphol", "morpholib-streichan-global-morphogenetic-flo"]:
        c, p = load("#/frontier?live=" + slug, 5000)
        out["entity_" + slug[-12:]] = p.evaluate("() => ({h1: document.querySelectorAll('h1').length, main: document.querySelector('main').innerText.length})") | {"errs": p.errs, "bad": p.bad[:4]}
        c.close()
    c, p = load("#/home", 6000)
    vids = p.evaluate("() => [...document.querySelectorAll('video')].map(v=>({src:(v.currentSrc||v.src||v.querySelector('source')?.src||'').slice(-60), ready:v.readyState, err:v.error&&v.error.code, paused:v.paused, autoplay:v.autoplay, muted:v.muted, controls:v.controls, label:v.getAttribute('aria-label')}))")
    out["home_videos"] = vids
    out["home_bad"] = p.bad
    out["turntable_head"] = c.request.head(BASE + "artifacts/simulations/fish3d-render/turntable.mp4").status
    c.close()
    c, p = load("#/studio", 9000)
    out["studio_viewer"] = p.evaluate("() => ({canvas: document.querySelectorAll('canvas').length, viewer: [...document.querySelectorAll('[class*=viewer],[id*=viewer],model-viewer')].map(e=>e.tagName+'.'+e.className).slice(0,5), dl: [...new Set([...document.querySelectorAll('a[href],a[download]')].map(a=>a.getAttribute('href')).filter(h=>/artifacts|download|\\.stl|\\.glb|\\.tar/i.test(h||'')))].slice(0,20)})")
    c.close()
    br.close()
Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
