"""9d5a3d08: expand the collapsed System audit panels (contributor audit, model-use ledger) and measure/screenshot them at 1440 and 390 wide. Read-only."""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
OUT = Path(sys.argv[1])
res = {}
M = r"""(sel) => { const d = document.querySelector(sel); if (!d) return null; const t = d.querySelector('table'); const out = {open: d.open, text_len: d.innerText.length, lists: [...d.querySelectorAll('ul')].map(u => u.children.length), h4: [...d.querySelectorAll('h4')].map(h => h.textContent.trim().slice(0,50)), rows: t ? t.rows.length : 0};
  if (t) { const wrap = t.closest('.tablewrap') || t.parentElement; const wr = wrap.getBoundingClientRect(); const tr = t.getBoundingClientRect();
    const lc = (n) => { const r = document.createRange(); r.selectNodeContents(n); return new Set([...r.getClientRects()].map(x => Math.round(x.top))).size; };
    const pills = [...t.querySelectorAll('.pill,[class*=pill]')].filter(p => lc(p) > 1).map(p => p.textContent.trim().slice(0, 24));
    out.table = {cols: t.rows[0].cells.length, wrap_w: Math.round(wr.width), table_w: Math.round(tr.width), overflows: wrap.scrollWidth > wrap.clientWidth + 1, wrapped_pills: pills.slice(0, 5), stacked_labels: !!t.querySelector('td[data-label]'),
      display: getComputedStyle(t.rows[1] ? t.rows[1].cells[1] || t.rows[1].cells[0] : t).display}; }
  return out; }"""
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for w, h, mob in [(1440, 900, False), (390, 800, True)]:
        c = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob)
        p = c.new_page()
        errs = []
        p.on("pageerror", lambda e: errs.append(str(e)[:150]))
        p.goto(BASE + "#/work?tab=built", wait_until="load")
        p.wait_for_timeout(4500)
        for sel in ["details.contributor-audit", "details.model-usage-audit"]:
            loc = p.locator(sel)
            r = {"present": loc.count()}
            if loc.count():
                loc.locator("summary").first.click()
                p.wait_for_timeout(700)
                r["facts"] = p.evaluate(M, sel)
                try:
                    loc.first.scroll_into_view_if_needed(timeout=6000)
                    loc.first.screenshot(path=str(OUT / "screens" / f"{sel.split('.')[1]}-{w}.png"), timeout=15000)
                except Exception as e:
                    r["shot_error"] = repr(e)[:80]
            res[f"{sel}|{w}"] = r
        res[f"errs|{w}"] = errs
        c.close()
    br.close()
(OUT / "details.json").write_text(json.dumps(res, indent=1))
print("ok")
