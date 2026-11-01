"""Second table pass: element screenshots of the worst tables and a stricter check (pure-letter words >=5 chars split across lines = true mid-word
break; breaks at hyphens, slashes, underscores and periods are NOT counted). Read-only; one load per route."""
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
OUT = Path(sys.argv[1])
(OUT / "screens").mkdir(parents=True, exist_ok=True)
# (route, table index, [viewport widths], slug)
TARGETS = [("#/work?tab=built", 0, [1440, 390], "built-counters"), ("#/work?tab=work", 0, [1440, 390], "work-board"),
           ("#/engineering", 0, [1440, 390], "eng-constraints"), ("#/engineering", 4, [1440, 390], "eng-9col"),
           ("#/frontier", 0, [1440, 768], "frontier-questions"), ("#/frontier", 1, [1440, 1024], "frontier-board"),
           ("#/evidence", 0, [1440, 390], "evidence-sources"), ("#/formalize", 0, [1024, 390], "formalize-symbols"),
           ("#/blueprints", 1, [1440, 768], "blueprints-ledger"), ("#/studio/flying-fish", 0, [1440, 390], "studio-matrix"),
           ("#/work?tab=resources", 4, [1440, 390], "resources-board"), ("#/simulations", 0, [1440, 390], "sim-couplings"),
           ("#/experimentation", 0, [1440, 390], "exp-plan"), ("#/ecology", 0, [1440, 1024], "eco-receipts")]
JS = r"""(i) => {
  const t = [...document.querySelectorAll('main table')][i]; if (!t) return null;
  const w = document.createTreeWalker(t, NodeFilter.SHOW_TEXT); const bad = []; let n = 0;
  while (w.nextNode()) { const node = w.currentNode; const re = /(?<![\w\-\/_.])[A-Za-z]{5,}(?![\w\-\/_.])/g; let m;
    while ((m = re.exec(node.textContent))) { n++; const r = document.createRange(); r.setStart(node, m.index); r.setEnd(node, m.index + m[0].length);
      const tops = new Set([...r.getClientRects()].map(x => Math.round(x.top))); if (tops.size > 1) bad.push(m[0]); } }
  const wrap = t.closest('.tablewrap') || t.parentElement; const cs = getComputedStyle(wrap);
  const hdrs = [...t.querySelectorAll('thead th')].map(h => ({t: h.textContent.trim().slice(0, 18), w: Math.round(h.getBoundingClientRect().width)}));
  const pillWrap = [...t.querySelectorAll('.pill,[class*=pill]')].filter(p => { const r = document.createRange(); r.selectNodeContents(p); return new Set([...r.getClientRects()].map(x => Math.round(x.top))).size > 1; }).map(p => p.textContent.trim().slice(0, 22));
  const lastRight = Math.max(...[...t.rows[0].cells].map(c => c.getBoundingClientRect().right)); const wr = wrap.getBoundingClientRect();
  return {alpha_words: n, midword_breaks: bad.length, midword_examples: [...new Set(bad)].slice(0, 6), pill_wrap_n: pillWrap.length, pill_wrap: [...new Set(pillWrap)].slice(0, 4),
          overflows: wrap.scrollWidth > wrap.clientWidth + 1, overflow_x: cs.overflowX, hidden_px: Math.max(0, Math.round(lastRight - wr.right)), header_widths: hdrs.slice(0, 9)};
}"""
rows = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    last = None
    c = None
    for route, idx, vws, slug in TARGETS:
        if route != last:
            if c is not None:
                c.close()
                time.sleep(3)
            c = br.new_context(viewport={"width": 1440, "height": 900})
            p = c.new_page()
            p.goto(BASE + route, wait_until="load", timeout=30000)
            p.wait_for_timeout(3500)
            last = route
        for w in vws:
            p.set_viewport_size({"width": w, "height": 900})
            p.wait_for_timeout(700)
            r = p.evaluate(JS, idx)
            if r is None:
                rows.append({"slug": slug, "route": route, "vp": w, "error": "no such table"})
                continue
            f = OUT / "screens" / f"{slug}-{w}.png"
            try:
                el = p.locator("main table").nth(idx)
                wrap = el.evaluate_handle("t => t.closest('.tablewrap') || t.parentElement").as_element()
                wrap.scroll_into_view_if_needed(timeout=6000)
                wrap.screenshot(path=str(f), timeout=10000)
                rows.append({"slug": slug, "route": route, "table": idx, "vp": w, "file": f.name, **r})
            except Exception as e:
                rows.append({"slug": slug, "route": route, "table": idx, "vp": w, "screenshot_error": repr(e)[:90], **r})
    br.close()
(OUT / "tables_shots.json").write_text(json.dumps(rows, indent=1))
print(len(rows))
