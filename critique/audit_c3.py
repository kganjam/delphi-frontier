"""Read-only route sweep of the live Frontier site at c3fd6026, desktop 1440x900 and phone 400x800. GET-only, fresh context per load,
3.5 s apart (the anonymous session mint limiter 429s a fast crawl). No form submissions, no credentials. Records observations only."""
import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
OUT = Path(sys.argv[1])
SC = ["molecular", "macromolecular", "subcellular", "cellular", "tissue", "organ", "neural", "organism", "developmental", "collective", "ecological"]
ROUTES = (["#/home", "#/studio", "#/studio/flying-fish", "#/engineering", "#/simulations", "#/belief", "#/formalize", "#/experimentation",
           "#/ecology", "#/regulatory", "#/blueprints", "#/reuse", "#/history", "#/frontier", "#/knowledge?tab=browse", "#/knowledge?tab=graph",
           "#/knowledge/fisher-ftns", "#/evidence", "#/evidence?tab=artifacts", "#/search?q=fish&tab=catalog", "#/search?q=zzqxjv&tab=catalog",
           "#/graph/Claim/fisher-ftns", "#/entity/Claim/fisher-ftns", "#/about", "#/about/team", "#/about/docs", "#/about/inspirations",
           "#/generative", "#/demo", "#/no-such-view"]
          + [f"#/work?tab={t}" for t in ["overview", "built", "specs", "work", "resources", "receipts", "runtime", "connect"]]
          + [f"#/engineering?scale={s}" for s in SC[:4]])
JS = r"""() => {
  const q = (s) => [...document.querySelectorAll(s)];
  const main = document.querySelector('main'); const text = main ? main.innerText : '';
  const name = (e) => (e.getAttribute('aria-label') || e.textContent || e.getAttribute('title') || '').trim();
  const pills = q('main .pill, main [class*=pill]');
  const wrapped = pills.filter(p => p.getBoundingClientRect().height > parseFloat(getComputedStyle(p).lineHeight || 20) * 1.6 && p.textContent.trim().length < 14).map(p => p.textContent.trim());
  return {title: document.title, h1: q('h1').length, h1_text: (q('h1')[0] || {textContent: ''}).textContent.trim().slice(0, 70),
    overflow_x: document.documentElement.scrollWidth > innerWidth + 1, main_len: text.length,
    object_object: /\[object Object\]/.test(text), literal_html: /<span|<\/\w+>|&lt;|&gt;/.test(text), undefined_text: /\bundefined\b|\bNaN\b/.test(text),
    unnamed: q('button,a[href],[role=button]').filter(e => !name(e)).map(e => e.outerHTML.slice(0, 90)).slice(0, 3),
    unlabelled_inputs: q('input:not([type=hidden]),select,textarea').filter(e => !(e.labels && e.labels.length) && !e.getAttribute('aria-label')).length,
    img_no_alt: q('img').filter(e => !e.hasAttribute('alt')).length, video: q('video').length, canvas: q('canvas').length, svg: q('main svg').length,
    wrapped_pills: wrapped.slice(0, 6), katex: q('.katex').length, katex_err: q('.katex-error').length,
    stale_receipts_footer: /no receipt exists in this tree/.test(text), skip_link: !!document.querySelector('a[href="#main"], a.skip, a[href*=skip]'),
    not_found_text: /Not found|no view called/i.test(text)};
}"""
rows = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    ver = br.version
    for r in ROUTES:
        for vp, (w, h, mob) in {"desktop": (1440, 900, False), "phone": (400, 800, True)}.items():
            c = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob)
            p = c.new_page()
            errs, bad = [], []
            p.on("pageerror", lambda e: errs.append(str(e)[:160]))
            p.on("response", lambda x: bad.append(f"{x.status} {x.url.replace(BASE, '')[-60:]}") if x.status >= 400 else None)
            p.on("requestfailed", lambda x: bad.append(f"FAILED {x.url.replace(BASE, '')[-60:]}") if "turntable" not in x.url and ".mp4" not in x.url else None)
            row = {"route": r, "vp": vp}
            t0 = time.time()
            try:
                p.goto(BASE + r, wait_until="load", timeout=30000)
                p.wait_for_timeout(3500)
                row.update(p.evaluate(JS))
                if vp == "desktop" and r in ("#/home", "#/studio/flying-fish", "#/ecology", "#/blueprints", "#/history", "#/experimentation", "#/formalize", "#/frontier", "#/demo", "#/engineering", "#/work?tab=built", "#/generative", "#/reuse", "#/regulatory"):
                    n = re.sub(r"[^a-z0-9]+", "-", r.lower()).strip("-")
                    p.screenshot(path=str(OUT / "screens" / f"{n}.png"))
            except Exception as e:
                row["error"] = repr(e)[:160]
            row.update(page_errors=errs, bad=bad[:6], load_s=round(time.time() - t0, 1))
            rows.append(row)
            c.close()
            time.sleep(3.5)
    br.close()
(OUT / "routes.json").write_text(json.dumps({"base": BASE, "chromium": ver, "rows": rows}, indent=1))
print(len(rows))
