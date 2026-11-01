"""Focused read-only check: Home mesh orbit/pick/reset, graph node click/zoom, math rendering. Waits on app readiness
(viewer data-mode, rendered DOM), never networkidle. One page at a time. Output records what happened; no pass is inferred."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
EXPECT_SNAPSHOT_PREFIX = sys.argv[3] if len(sys.argv) > 3 else ""   # snapshot.json sha256 prefix of the target commit
out_dir = Path(sys.argv[1])
(out_dir / "screens").mkdir(parents=True, exist_ok=True)
label = sys.argv[2]
res: dict = {"label": label}


def px(canvas) -> str:
    return hashlib.sha256(canvas.screenshot()).hexdigest()[:16]


with sync_playwright() as pw:
    br = pw.chromium.launch()
    res["chromium"] = br.version
    c = br.new_context(viewport={"width": 1440, "height": 900})
    snap = c.request.get(BASE + "data/snapshot.json", timeout=60000).body()
    res["live_snapshot_sha256_16"] = hashlib.sha256(snap).hexdigest()[:16]
    res["matches_target_snapshot"] = bool(EXPECT_SNAPSHOT_PREFIX) and res["live_snapshot_sha256_16"].startswith(EXPECT_SNAPSHOT_PREFIX)
    p = c.new_page()
    errs: list = []
    p.on("pageerror", lambda e: errs.append(str(e)[:200]))
    t0 = time.time()
    p.goto(BASE + "#/home", wait_until="load")
    # readiness = the viewer reports a mode, not a quiet network
    try:
        p.wait_for_selector(".mv-stage[data-mode=interactive], .mv-stage[data-mode=fallback]", timeout=45000)
        mode = p.get_attribute(".mv-stage", "data-mode")
    except Exception as e:
        mode = "never-ready: " + repr(e)[:80]
    mv = {"mode": mode, "ready_s": round(time.time() - t0, 1),
          "status": p.evaluate("() => document.querySelector('.mv [data-state]')?.textContent?.slice(0,260)"),
          "reset_disabled": p.evaluate("() => [...document.querySelectorAll('.mv button')].filter(b=>/Reset view/.test(b.textContent)).map(b=>b.disabled)")}
    if mode == "interactive":
        cv = p.locator(".mv-stage canvas").first
        cv.scroll_into_view_if_needed()
        p.wait_for_timeout(1200)
        mv["canvas_box"] = cv.bounding_box()
        h0 = px(cv)
        cv.focus()
        for _ in range(6):
            p.keyboard.press("ArrowLeft")
        p.wait_for_timeout(500)
        h_orbit_key = px(cv)
        box = cv.bounding_box()
        cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        p.mouse.move(cx, cy)
        p.mouse.down()
        p.mouse.move(cx + 120, cy + 30, steps=8)
        p.mouse.up()
        p.wait_for_timeout(500)
        h_orbit_drag = px(cv)
        detail_before = p.evaluate("() => document.querySelector('.mv-detail, .mv [class*=detail]')?.innerText?.slice(0,120) || null")
        picks = []
        for fx, fy in [(0.5, 0.5), (0.4, 0.5), (0.6, 0.45), (0.3, 0.6)]:
            p.mouse.click(box["x"] + box["width"] * fx, box["y"] + box["height"] * fy)
            p.wait_for_timeout(300)
            picks.append({"at": [fx, fy], "detail": p.evaluate("() => document.querySelector('.mv-detail, .mv [class*=detail]')?.innerText?.slice(0,100) || null"),
                          "selected_li": p.evaluate("() => [...document.querySelectorAll('.mv-list li')].filter(l=>l.classList.contains('sel')||l.getAttribute('aria-selected')==='true'||l.classList.contains('on')).map(l=>l.dataset.comp)")})
        p.screenshot(path=str(out_dir / "screens" / f"{label}-mesh-picked.png"))
        p.keyboard.press("Escape")
        p.locator(".mv button", has_text="Reset view").click()
        p.wait_for_timeout(700)
        h_reset = px(cv)
        mv.update(pixels={"initial": h0, "after_6_arrow_left": h_orbit_key, "after_drag": h_orbit_drag, "after_reset": h_reset},
                  orbit_by_keys_changed_pixels=h_orbit_key != h0, orbit_by_drag_changed_pixels=h_orbit_drag != h_orbit_key,
                  reset_restored_initial_pixels=h_reset == h0, detail_before_pick=detail_before, picks=picks,
                  components=p.evaluate("() => document.querySelectorAll('.mv-list li').length"))
    res["home_mesh"] = mv | {"page_errors": list(errs)}

    g = {}
    for route in ["#/knowledge?tab=graph", "#/graph/Claim/fisher-ftns"]:
        p.goto(BASE + route, wait_until="load")
        p.wait_for_timeout(4500)
        row = p.evaluate("() => { const s=document.querySelector('main svg'); return {svg: !!s, nodes: document.querySelectorAll('main svg g.g-node').length, text: document.querySelector('main').innerText.slice(0,200)} }")
        if row["nodes"]:
            node = p.locator("main svg g.g-node").nth(1)
            before = p.evaluate("() => (document.querySelector('main #gdetail, main .detail-col, main [id*=detail]')||document.querySelector('main')).innerText.slice(0,80)")
            try:
                node.click(timeout=8000)
            except Exception as e:
                row["node_click_error"] = repr(e)[:160]
            p.wait_for_timeout(500)
            row["detail_before"] = before
            row["detail_after_click"] = p.evaluate("() => (document.querySelector('main #gdetail, main .detail-col, main [id*=detail]')||document.querySelector('main')).innerText.slice(0,80)")
            row["hash_after_click"] = p.evaluate("() => location.hash")
            tr = lambda: p.evaluate("() => document.querySelector('main svg g[transform]')?.getAttribute('transform')")  # noqa: E731
            t_a = tr()
            zin = p.locator("main [data-z=in]")
            if zin.count():
                zin.first.click()
                p.wait_for_timeout(300)
            else:
                box = p.locator("main svg").first.bounding_box()
                p.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                p.mouse.wheel(0, -400)
                p.wait_for_timeout(300)
            row["transform_before_zoom"], row["transform_after_zoom"] = t_a, tr()
            row["zoom_changed_transform"] = t_a != row["transform_after_zoom"]
        p.screenshot(path=str(out_dir / "screens" / f"{label}-graph-{len(g)}.png"))
        g[route] = row
    res["graph"] = g | {"page_errors": list(errs)}

    m = {}
    for route in ["#/knowledge", "#/frontier", "#/knowledge/claims", "#/evidence", "#/about/docs"]:
        p.goto(BASE + route, wait_until="load")
        p.wait_for_timeout(3500)
        m[route] = p.evaluate("() => ({katex_global: !!window.katex, rendered: document.querySelectorAll('.katex').length, katex_err: document.querySelectorAll('.katex-error').length, raw_tex: /\\\\(frac|sum|cdot|partial|alpha|beta)|\\$[^$ ]{1,40}\\$/.test(document.querySelector('main').innerText), sample: [...document.querySelectorAll('.katex')].slice(0,2).map(e=>e.getAttribute('aria-label')||e.parentElement.getAttribute('aria-label')).filter(Boolean)})")
    res["math"] = m
    br.close()
(out_dir / f"focus-{label}.json").write_text(json.dumps(res, indent=1))
print(json.dumps({k: (v if k in ("label", "matches_target_snapshot", "live_snapshot_sha256_16") else "…") for k, v in res.items()}))
