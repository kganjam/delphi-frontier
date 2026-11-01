"""Read-only table audit of live Frontier (c3fd6026). One page load per route; the viewport is resized through 1440, 1024, 768 and 390 wide.
Per table: columns, scroll container, overflow/clipping, badge (pill) text wrapped across lines, words broken mid-word. No writes."""
import json
import os
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
OUT = Path(sys.argv[1])
VPS = [(1440, 900), (1024, 800), (768, 900), (390, 800)]
ROUTES = (["#/work?tab=" + t for t in ["overview", "built", "specs", "work", "resources", "receipts", "runtime", "connect"]]
          + ["#/engineering", "#/simulations", "#/knowledge?tab=browse", "#/evidence", "#/evidence?tab=artifacts", "#/blueprints", "#/regulatory",
             "#/reuse", "#/experimentation", "#/formalize", "#/studio/flying-fish", "#/history", "#/frontier", "#/knowledge/fisher-ftns", "#/about/docs",
             "#/ecology", "#/generative", "#/belief", "#/search?q=fish&tab=catalog"])
JS = r"""() => {
  const tables = [...document.querySelectorAll('main table')];
  const lineCount = (node) => { const r = document.createRange(); r.selectNodeContents(node); const tops = new Set([...r.getClientRects()].map(x => Math.round(x.top))); return tops.size; };
  const brokenWords = (root) => {
    let n = 0; const ex = []; const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (w.nextNode() && ex.length < 6) {
      const t = w.currentNode; const s = t.textContent; const re = /\S{4,}/g; let m; let k = 0;
      while ((m = re.exec(s)) && k++ < 40) { const r = document.createRange(); r.setStart(t, m.index); r.setEnd(t, m.index + m[0].length); const tops = new Set([...r.getClientRects()].map(x => Math.round(x.top))); if (tops.size > 1) { n++; if (ex.length < 6) ex.push(m[0].slice(0, 24)); } }
    }
    return {n, ex};
  };
  return tables.map((t, i) => {
    const wrap = t.closest('.tablewrap') || t.parentElement; const cs = getComputedStyle(wrap);
    const ths = [...t.querySelectorAll('thead th')];
    const pills = [...t.querySelectorAll('.pill, [class*=pill], [class*=badge], .lvl-a, .lvl-m')];
    const wrappedPills = pills.filter(p => p.textContent.trim().length > 0 && lineCount(p) > 1).map(p => p.textContent.trim().slice(0, 24));
    const wr = wrap.getBoundingClientRect(); const tr = t.getBoundingClientRect();
    const clippedCells = [...t.querySelectorAll('td,th')].filter(c => { const r = c.getBoundingClientRect(); return r.width > 0 && r.right > wr.right + 1 && cs.overflowX !== 'visible'; }).length;
    const bw = brokenWords(t);
    return {i, caption: ((t.querySelector('caption') || {}).textContent || '').trim().slice(0, 50), cols: ths.length || (t.rows[0] ? t.rows[0].cells.length : 0), rows: t.rows.length,
      headers: ths.map(h => h.textContent.trim().slice(0, 22)).slice(0, 8), has_data_label: !!t.querySelector('td[data-label]'),
      table_w: Math.round(tr.width), wrap_w: Math.round(wr.width), wrap_overflow_x: cs.overflowX, scroll_w: wrap.scrollWidth, client_w: wrap.clientWidth,
      overflows: wrap.scrollWidth > wrap.clientWidth + 1, scrolls: wrap.scrollWidth > wrap.clientWidth + 1 && /auto|scroll/.test(cs.overflowX),
      clipped_cells: clippedCells, page_overflow: document.documentElement.scrollWidth > innerWidth + 1,
      pills: pills.length, wrapped_pills: wrappedPills.slice(0, 6), wrapped_pill_n: wrappedPills.length, broken_words_n: bw.n, broken_words: bw.ex,
      narrow_th: ths.filter(h => h.getBoundingClientRect().width < 70).map(h => h.textContent.trim().slice(0, 14)).slice(0, 5)};
  });
}"""
if os.environ.get("TABLE_ROUTES"):
    ROUTES = os.environ["TABLE_ROUTES"].split(",")
res = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for r in ROUTES:
        c = br.new_context(viewport={"width": 1440, "height": 900})
        p = c.new_page()
        try:
            p.goto(BASE + r, wait_until="load", timeout=30000)
            p.wait_for_timeout(3500)
            for (w, h) in VPS:
                p.set_viewport_size({"width": w, "height": h})
                p.wait_for_timeout(700)
                res.append({"route": r, "vp": w, "tables": p.evaluate(JS)})
        except Exception as e:
            res.append({"route": r, "error": repr(e)[:120]})
        c.close()
        time.sleep(3)
    br.close()
(OUT / "tables.json").write_text(json.dumps(res, indent=1))
print(len(res))
