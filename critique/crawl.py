"""Read-only Playwright crawl of the public Frontier site. GET-only; no form submissions except the header search box
(a hash navigation). A fresh page per route and viewport. Records what was observed; nothing is inferred as a pass."""
from __future__ import annotations

import argparse
import json
import re
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
SEED = ["#/home", "#/studio", "#/frontier", "#/knowledge", "#/knowledge?tab=browse", "#/evidence", "#/evidence?tab=artifacts",
        "#/work", "#/system", "#/engineering", "#/simulations", "#/belief", "#/formalize", "#/graph", "#/search?q=fish",
        "#/about", "#/about/team", "#/about/docs", "#/about/inspirations", "#/generative", "#/no-such-view"]
VIEWPORTS = {"desktop": (1440, 900), "phone": (400, 800)}

PAGE_JS = r"""() => {
  const q = (s) => [...document.querySelectorAll(s)];
  const name = (e) => (e.getAttribute('aria-label') || e.getAttribute('aria-labelledby') || e.textContent || e.getAttribute('title') || '').trim();
  const ids = {}; q('[id]').forEach(e => ids[e.id] = (ids[e.id] || 0) + 1);
  const text = document.body.innerText;
  const main = document.querySelector('main');
  const wide = q('body *').filter(e => { const r = e.getBoundingClientRect(); return r.right > innerWidth + 1 && r.width > 0 && getComputedStyle(e).position !== 'fixed'; }).slice(0, 5).map(e => e.tagName + '.' + (e.className || '').toString().slice(0, 40));
  return {
    title: document.title, lang: document.documentElement.lang, h1: q('h1').length, h1_text: q('h1').map(e => e.textContent.trim().slice(0, 80)),
    heading_levels: q('h1,h2,h3,h4').map(e => +e.tagName[1]).slice(0, 80),
    overflow_x: document.documentElement.scrollWidth > innerWidth + 1, scrollWidth: document.documentElement.scrollWidth, innerWidth,
    overflowing: wide, has_main: !!main, main_len: main ? main.innerText.length : 0,
    img_no_alt: q('img').filter(e => !e.hasAttribute('alt')).length, imgs: q('img').length,
    unnamed_controls: q('button,a[href],[role=button]').filter(e => !name(e)).length,
    controls: q('button,a[href],[role=button]').length,
    inputs_unlabelled: q('input:not([type=hidden]),select,textarea').filter(e => !(e.labels && e.labels.length) && !e.getAttribute('aria-label') && !e.getAttribute('aria-labelledby')).map(e => e.id || e.name || e.type).slice(0, 8),
    dup_ids: Object.entries(ids).filter(([, n]) => n > 1).map(([k]) => k).slice(0, 8),
    bad_text: ['undefined', 'NaN', '[object Object]', 'null'].filter(w => new RegExp('\\b' + w.replace(/[[\]]/g, '\\$&') + '\\b').test(text)),
    raw_math: /\\\(|\\\[|\$\$|\\frac|\\sum/.test(text), math_rendered: q('.katex,mjx-container,math').length,
    links_hash: [...new Set(q('a[href^="#/"]').map(e => e.getAttribute('href')))].slice(0, 400),
    links_ext: [...new Set(q('a[href]:not([href^="#"])').map(e => e.href))].slice(0, 200),
    tabindex_pos: q('[tabindex]').filter(e => +e.getAttribute('tabindex') > 0).length,
    focusable: q('a[href],button,input,select,textarea,summary,[tabindex]').length,
  };
}"""


def visit(ctx_factory, route: str, vp: str, shots: Path) -> dict:
    ctx = ctx_factory(vp)
    page = ctx.new_page()
    errs, bad_req, cons = [], [], []
    page.on("pageerror", lambda e: errs.append(str(e)[:200]))
    page.on("console", lambda m: cons.append(m.text[:200]) if m.type in ("error", "warning") else None)
    page.on("response", lambda r: bad_req.append(f"{r.status} {r.url[-90:]}") if r.status >= 400 else None)
    page.on("requestfailed", lambda r: bad_req.append(f"FAILED {r.url[-90:]}"))
    t0 = time.time()
    rec = {"route": route, "viewport": vp}
    try:
        page.goto(BASE + route, wait_until="load", timeout=30000)
        page.wait_for_timeout(2500)
        rec.update(page.evaluate(PAGE_JS))
        slug = re.sub(r"[^a-z0-9]+", "-", route.lower()).strip("-") or "root"
        f = shots / f"{vp}-{slug[:60]}.png"
        page.screenshot(path=str(f), full_page=False)
        rec["screenshot"] = f.name
    except Exception as e:  # recorded, not hidden
        rec["crawl_error"] = repr(e)[:200]
    rec.update(page_errors=errs, console=cons[:6], bad_requests=bad_req[:8], load_s=round(time.time() - t0, 1))
    ctx.close()
    return rec


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-routes", type=int, default=70)
    ap.add_argument("--seed", action="append", help="route(s) to crawl instead of the default list")
    ap.add_argument("--no-follow", action="store_true", help="do not queue links found on pages")
    a = ap.parse_args()
    out = Path(a.out)
    shots = out / "screens"
    shots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch()
        ver = br.version

        def mk(vp):
            w, h = VIEWPORTS[vp]
            return br.new_context(viewport={"width": w, "height": h}, is_mobile=(vp == "phone"), has_touch=(vp == "phone"))

        seen, queue, results = set(), list(a.seed or SEED), []
        while queue and len(seen) < a.max_routes:
            r = queue.pop(0)
            if r in seen:
                continue
            seen.add(r)
            for vp in VIEWPORTS:
                rec = visit(mk, r, vp, shots)
                results.append(rec)
                if vp == "desktop" and not a.no_follow:
                    for h in rec.get("links_hash", []):
                        if h not in seen and h not in queue and "src=" not in h and len(queue) < 400:
                            queue.append(h)
        br.close()
    (out / "routes.json").write_text(json.dumps({"base": BASE, "chromium": ver, "routes_visited": len(seen),
                                                 "queue_left_unvisited": queue[:200], "results": results}, indent=1))
    print("routes", len(seen), "unvisited", len(queue), "chromium", ver)


if __name__ == "__main__":
    main()
