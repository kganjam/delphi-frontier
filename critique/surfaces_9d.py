"""Read-only checks of the surfaces new at 9d5a3d08: FAQ, print-law viewer, assemblies, System built tab (counts / model-use ledger), simulations cards
(aeroelastic-coupling, nca-pattern, nca-seed-placement). Desktop 1440x900 and phone 400x800, one fresh context per load, 4 s apart. No writes."""
import json
import re
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
OUT = Path(sys.argv[1])
res = {}
FACT = r"""() => {
  const q = (s) => [...document.querySelectorAll(s)]; const m = document.querySelector('main'); const t = m ? m.innerText : '';
  return {h1: q('h1').map(e => e.textContent.trim().slice(0, 70)), main_len: t.length, overflow_x: document.documentElement.scrollWidth > innerWidth + 1,
    h2: q('main h2').map(e => e.textContent.trim().slice(0, 50)).slice(0, 16), tables: q('main table').length, details: q('main details').length,
    katex: q('.katex').length, katex_err: q('.katex-error').length, object_object: /\[object Object\]/.test(t), literal_html: /<span|<\/\w+>/.test(t),
    unnamed: q('button,a[href]').filter(e => !(e.getAttribute('aria-label') || e.textContent || e.title || '').trim()).length,
    verified_words: (t.match(/[^.\n]{0,60}\b(verified|validated|cleared|kernel-checked|proved)\b[^.\n]{0,40}/gi) || []).slice(0, 10)};
}"""
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for route in ["#/faq", "#/print-laws", "#/assemblies", "#/work?tab=built", "#/simulations"]:
        for vp, (w, h, mob) in {"desktop": (1440, 900, False), "phone": (400, 800, True)}.items():
            c = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob)
            p = c.new_page()
            errs, bad = [], []
            p.on("pageerror", lambda e: errs.append(str(e)[:150]))
            p.on("response", lambda x: bad.append(f"{x.status} {x.url.replace(BASE, '')[-60:]}") if x.status >= 400 else None)
            row = {}
            try:
                p.goto(BASE + route, wait_until="load", timeout=30000)
                p.wait_for_timeout(4000)
                row = p.evaluate(FACT)
                n = re.sub(r"[^a-z0-9]+", "-", route.lower()).strip("-")
                p.screenshot(path=str(OUT / "screens" / f"{n}-{vp}.png"))
                if route == "#/faq":
                    row["links"] = p.evaluate("() => [...document.querySelectorAll('main a[href]')].map(a => a.href)")
                    row["numbers_in_text"] = p.evaluate("() => (document.querySelector('main').innerText.match(/[^.\\n]{0,50}\\b[0-9][0-9,]{1,}\\b[^.\\n]{0,40}/g) || []).slice(0, 12)")
                    row["questions"] = p.evaluate("() => [...document.querySelectorAll('main h2, main h3, main summary')].map(e => e.textContent.trim().slice(0, 80)).slice(0, 14)")
                if route == "#/print-laws":
                    row["picker_options"] = p.evaluate("() => document.querySelectorAll('#print-file option').length")
                    row["metrics"] = p.evaluate("() => [...document.querySelectorAll('.print-metrics b')].map(e => e.textContent.trim())")
                    row["grid_cols"] = p.evaluate("() => getComputedStyle(document.querySelector('.print-law-grid')||document.body).gridTemplateColumns.split(' ').length")
                    row["pills"] = p.evaluate("() => [...document.querySelectorAll('main .pill')].map(e => e.textContent.trim()).slice(0, 14)")
                    row["note_warn"] = p.evaluate("() => (document.querySelector('main .note.warn')||{}).innerText")
                    if vp == "desktop":
                        sel = p.locator("#print-file")
                        opts = sel.evaluate("e => [...e.options].map(o => o.value)")
                        before = p.evaluate("() => document.querySelector('main h1').textContent + '|' + (document.querySelector('.print-file-hash code')||{}).textContent")
                        pick = next((o for o in opts if "withdrawn" in o or "pectoral_R" in o), opts[min(3, len(opts) - 1)])
                        sel.select_option(pick)
                        p.wait_for_timeout(2500)
                        row["picker_changed"] = [before[:80], p.evaluate("() => document.querySelector('main h1').textContent + '|' + (document.querySelector('.print-file-hash code')||{}).textContent")[:80], pick]
                        row["after_pick_pills"] = p.evaluate("() => [...document.querySelectorAll('main .pill')].map(e => e.textContent.trim()).slice(0, 10)")
                        p.screenshot(path=str(OUT / "screens" / "print-laws-after-pick-desktop.png"))
                if route == "#/assemblies":
                    row["asinspect"] = p.evaluate("() => document.querySelectorAll('.asinspect').length")
                    sm = p.locator(".asinspect summary")
                    if sm.count():
                        sm.first.click()
                        p.wait_for_timeout(500)
                        row["astree_open"] = p.evaluate("() => ({dl: document.querySelectorAll('dl.astree').length, cols: getComputedStyle(document.querySelector('dl.astree')||document.body).gridTemplateColumns.split(' ').length, txt: (document.querySelector('dl.astree')||{}).innerText?.slice(0,160)})")
                if route == "#/simulations":
                    row["cards"] = p.evaluate("() => ['aeroelastic-coupling','nca-pattern','nca-seed-placement'].map(id => { const el = document.getElementById(id) || document.querySelector('[id*=\"'+id+'\"]'); return {id, found: !!el, text: el ? el.innerText.slice(0, 230).replace(/\\s+/g,' ') : null, video: el ? el.querySelectorAll('video').length : 0, poster: el ? [...el.querySelectorAll('video')].map(v => v.getAttribute('poster')) : []}; })")
                    row["videos_total"] = p.evaluate("() => document.querySelectorAll('video').length")
                    row["cards_total_text"] = p.evaluate("() => (document.querySelector('main').innerText.match(/Showing \\d+ of \\d+[^\\n]*/)||[null])[0]")
            except Exception as e:
                row["error"] = repr(e)[:150]
            row.update(page_errors=errs, bad=bad[:5])
            res[f"{route}|{vp}"] = row
            c.close()
            time.sleep(4)
    br.close()
(OUT / "surfaces.json").write_text(json.dumps(res, indent=1))
print(len(res))
