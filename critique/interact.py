"""Read-only interaction probes against the public Frontier site. Header search is a hash navigation; nothing is submitted
to a server or persisted. Each probe records observed values."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"


def probe(fn):
    def w(*a, **k):
        try:
            return fn(*a, **k)
        except Exception as e:
            return {"probe_error": repr(e)[:300]}
    w.__name__ = fn.__name__
    return w


def new(br, vp=(1440, 900), mobile=False):
    c = br.new_context(viewport={"width": vp[0], "height": vp[1]}, is_mobile=mobile, has_touch=mobile)
    p = c.new_page()
    p.errs = []
    p.on("pageerror", lambda e: p.errs.append(str(e)[:200]))
    return c, p


@probe
def knowledge_scroll(br, shots):
    c, p = new(br)
    p.goto(BASE + "#/knowledge?tab=browse", wait_until="load")
    p.wait_for_timeout(2500)
    cnt = lambda: p.evaluate("() => document.querySelectorAll('main li, main tr, main article, main .card, main .row').length")  # noqa: E731
    seq = [cnt()]
    for _ in range(8):
        p.mouse.wheel(0, 6000)
        p.wait_for_timeout(1200)
        seq.append(cnt())
    more = p.evaluate("() => [...document.querySelectorAll('button,a')].filter(e=>/more|load|next/i.test(e.textContent)).map(e=>e.textContent.trim().slice(0,40)).slice(0,5)")
    shot = p.evaluate("() => ({sh: document.documentElement.scrollHeight, y: scrollY})")
    p.screenshot(path=str(shots / "interact-knowledge-scrolled.png"))
    out = {"item_count_after_each_scroll": seq, "more_controls": more, "page": shot, "page_errors": p.errs}
    c.close()
    return out


@probe
def search(br, shots):
    out = {}
    for label, q in [("normal", "fish"), ("nonsense", "zzqxjv"), ("empty", ""), ("html", "<img src=x onerror=alert(1)>"), ("quote", 'a"b\'c')]:
        c, p = new(br)
        dialogs = []
        p.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))
        p.goto(BASE + "#/home", wait_until="load")
        p.wait_for_timeout(1500)
        p.fill("#gq", q)
        p.press("#gq", "Enter")
        p.wait_for_timeout(1800)
        r = p.evaluate("() => ({hash: location.hash, h1: document.querySelector('h1')?.textContent?.trim(), n: document.querySelectorAll('main li, main tr, main article').length, injected_img: !!document.querySelector('main img[src=x]'), text: document.querySelector('main')?.innerText.slice(0,160)})")
        r.update(dialogs=dialogs, page_errors=p.errs)
        out[label] = r
        if label == "normal":
            p.screenshot(path=str(shots / "interact-search-fish.png"))
        c.close()
    return out


@probe
def graph(br, shots):
    out = {}
    for route in ["#/graph", "#/knowledge?tab=graph", "#/frontier"]:
        c, p = new(br)
        p.goto(BASE + route, wait_until="load")
        p.wait_for_timeout(3000)
        r = p.evaluate("() => ({svg: document.querySelectorAll('main svg').length, canvas: document.querySelectorAll('main canvas').length, nodes: document.querySelectorAll('main svg circle, main svg [data-node], main svg g.node').length, edges: document.querySelectorAll('main svg line, main svg path.edge, main svg .edge').length, svg_with_title: [...document.querySelectorAll('main svg')].filter(s=>s.querySelector('title')||s.getAttribute('aria-label')).length})")
        before = p.evaluate("() => location.hash")
        el = p.query_selector("main svg circle, main svg [data-node], main svg g.node")
        if el:
            try:
                el.click(timeout=3000)
                p.wait_for_timeout(800)
                r["after_node_click_hash"] = p.evaluate("() => location.hash")
                r["hash_before"] = before
            except Exception as e:
                r["node_click_error"] = repr(e)[:120]
        r["page_errors"] = p.errs
        p.screenshot(path=str(shots / f"interact-graph-{re.sub(r'[^a-z]+', '-', route)}.png"))
        out[route] = r
        c.close()
    return out


@probe
def downloads_and_3d(br, shots, snap_text):
    c, p = new(br)
    p.goto(BASE + "#/studio", wait_until="load")
    p.wait_for_timeout(3500)
    gl = p.evaluate("() => { const c=document.createElement('canvas'); return !!(c.getContext('webgl2')||c.getContext('webgl')); }")
    viewer = p.evaluate("() => ({canvas: document.querySelectorAll('canvas').length, model_viewer: document.querySelectorAll('model-viewer,[data-model-viewer],.model-viewer').length})")
    links = p.evaluate("() => [...new Set([...document.querySelectorAll('a[href]')].map(a=>a.href).filter(h=>/\\.(stl|glb|gltf|tar|xz|gz|zip|json|csv|npz|mp4|png)(\\?|$)/i.test(h)))]")
    p.screenshot(path=str(shots / "interact-studio-3d.png"))
    res = []
    for h in links[:40]:
        r = c.request.head(h, timeout=20000)
        row = {"url": h.replace(BASE, ""), "status": r.status, "bytes": r.headers.get("content-length"), "type": r.headers.get("content-type")}
        if r.status == 200 and row["bytes"] and int(row["bytes"]) <= 6_000_000:
            body = c.request.get(h, timeout=30000).body()
            sha = hashlib.sha256(body).hexdigest()
            row.update(sha256=sha, sha_published_in_snapshot=sha in snap_text, got_bytes=len(body))
        res.append(row)
    out = {"webgl": gl, "viewer_elements": viewer, "page_errors": p.errs, "download_links_found": len(links), "checked": res}
    c.close()
    return out


@probe
def studio_links(br):
    c, p = new(br)
    p.goto(BASE + "#/studio", wait_until="load")
    p.wait_for_timeout(3000)
    hrefs = p.evaluate("() => [...new Set([...document.querySelectorAll('a[href^=\"#/\"]')].map(a=>a.getAttribute('href')))]")
    res = []
    for h in hrefs[:60]:
        p.goto(BASE + h, wait_until="load")
        p.wait_for_timeout(900)
        r = p.evaluate("() => ({h1: document.querySelector('h1')?.textContent?.trim().slice(0,60), notfound: /Not found/i.test(document.querySelector('main')?.innerText||'')})")
        res.append({"href": h, **r})
    c.close()
    return {"links": len(hrefs), "checked": len(res), "not_found": [r["href"] for r in res if r["notfound"] or not r["h1"]], "rows": res}


@probe
def keyboard(br, shots):
    out = {}
    for vp, (w, h), mob in [("desktop", (1440, 900), False), ("phone", (400, 800), True)]:
        c, p = new(br, (w, h), mob)
        p.goto(BASE + "#/home", wait_until="load")
        p.wait_for_timeout(2000)
        seq = []
        for _ in range(30):
            p.keyboard.press("Tab")
            seq.append(p.evaluate("() => { const e=document.activeElement; const s=getComputedStyle(e); const r=e.getBoundingClientRect(); return {tag:e.tagName, text:(e.getAttribute('aria-label')||e.textContent||'').trim().slice(0,30), outline:s.outlineStyle+' '+s.outlineWidth, shadow: s.boxShadow!=='none', visible: r.width>0&&r.height>0&&r.bottom>0&&r.top<innerHeight}; }"))
        out[vp] = {"first_five": [s["text"] or s["tag"] for s in seq[:5]], "no_visible_focus_indicator": sum(1 for s in seq if s["outline"].startswith("none") and not s["shadow"]),
                   "focus_offscreen": sum(1 for s in seq if not s["visible"]), "tabs": len(seq), "skip_link_first": bool(re.search("skip", (seq[0]["text"] or ""), re.I))}
        c.close()
    return out


@probe
def back_forward(br):
    c, p = new(br)
    p.goto(BASE + "#/home", wait_until="load")
    p.wait_for_timeout(1500)
    trail = []
    for r in ["#/studio", "#/knowledge", "#/evidence"]:
        p.evaluate("(h) => { location.hash = h }", r)
        p.wait_for_timeout(1200)
        trail.append(p.evaluate("() => location.hash"))
    p.go_back()
    p.wait_for_timeout(1000)
    after_back = p.evaluate("() => ({hash: location.hash, h1: document.querySelector('h1')?.textContent?.trim()})")
    p.reload()
    p.wait_for_timeout(2000)
    after_reload = p.evaluate("() => ({hash: location.hash, h1: document.querySelector('h1')?.textContent?.trim()})")
    c.close()
    return {"trail": trail, "after_back": after_back, "after_reload": after_reload}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    shots = out / "screens"
    shots.mkdir(parents=True, exist_ok=True)
    c0 = None
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        c0 = br.new_context()
        snap_text = c0.request.get(BASE + "data/snapshot.json", timeout=30000).text()
        c0.close()
        res = {"chromium": br.version, "base": BASE,
               "knowledge_scroll": knowledge_scroll(br, shots), "search": search(br, shots), "graph": graph(br, shots),
               "downloads_and_3d": downloads_and_3d(br, shots, snap_text), "studio_links": studio_links(br),
               "keyboard": keyboard(br, shots), "back_forward": back_forward(br)}
        br.close()
    (out / "interactions.json").write_text(json.dumps(res, indent=1))
    print("done")


if __name__ == "__main__":
    main()
