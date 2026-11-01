"""Follow-ups on live c3fd6026 for the inconclusive items: ecology scrub (regex on the saved-state line), autocomplete with a whole word,
history detail panel text, phone mesh readiness (up to 25 s), first Tab stop. Read-only."""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
out = {}
with sync_playwright() as pw:
    br = pw.chromium.launch()

    def page(w=1440, h=900, mob=False):
        c = br.new_context(viewport={"width": w, "height": h}, is_mobile=mob, has_touch=mob)
        return c, c.new_page()

    c, p = page()
    p.goto(BASE + "#/ecology", wait_until="load")
    p.wait_for_selector("#eco-host canvas", timeout=30000)
    p.wait_for_timeout(2500)
    grab = lambda: p.evaluate("() => (document.querySelector('#eco-host').innerText.match(/t = [0-9.]+ s \\(saved state [0-9]+ of [0-9]+/)||[null])[0]")  # noqa: E731
    out["eco_t_initial"] = grab()
    rng = p.locator("#eco-host input[type=range]").first
    rng.evaluate("e => { e.value = Math.round(e.max*0.5); e.dispatchEvent(new Event('input', {bubbles:true})); e.dispatchEvent(new Event('change', {bubbles:true})); }")
    p.wait_for_timeout(900)
    out["eco_t_after_scrub_half"] = grab()
    p.get_by_role("button", name="Play").first.click()
    p.wait_for_timeout(2500)
    out["eco_t_while_playing"] = grab()
    c.close()

    c, p = page()
    p.goto(BASE + "#/home", wait_until="load")
    p.wait_for_timeout(3000)
    p.click("#gq")
    p.keyboard.type("fish", delay=150)
    p.wait_for_timeout(3000)
    out["autocomplete_fish"] = p.evaluate("() => ({expanded: document.querySelector('#gq')?.getAttribute('aria-expanded'), options: [...document.querySelectorAll('#ac-list [role=option], #ac-list li')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,80)).slice(0,5), status: (document.querySelector('#ac-status')||{}).innerText})")
    p.keyboard.press("Tab")
    c.close()

    c, p = page()
    p.goto(BASE + "#/history", wait_until="load")
    p.wait_for_timeout(4000)
    sel = p.evaluate("() => document.querySelector('main').innerText.match(/Select a node[^\\n]*/)?.[0]")
    nodes = p.locator("main svg [role=button], main svg g.g-node")
    out["history_nodes"] = nodes.count()
    if nodes.count() > 1:
        nodes.nth(1).click(timeout=6000)
        p.wait_for_timeout(800)
        out["history_before"] = sel
        out["history_after"] = p.evaluate("() => (document.querySelector('main').innerText.match(/Select a node[^\\n]*/)||['(prompt gone)'])[0]")
        out["history_detail_excerpt"] = p.evaluate("() => [...document.querySelectorAll('main h2,main h3')].map(e=>e.textContent.trim().slice(0,50)).slice(0,10)")
    c.close()

    c, p = page(400, 800, True)
    p.goto(BASE + "#/home", wait_until="load")
    try:
        p.wait_for_selector(".mv-stage[data-mode=interactive], .mv-stage[data-mode=fallback]", timeout=25000)
    except Exception:
        pass
    out["phone_mesh_mode_after_wait"] = p.evaluate("() => document.querySelector('.mv-stage')?.dataset.mode")
    out["phone_mesh_status"] = p.evaluate("() => document.querySelector('.mv [data-state]')?.textContent?.slice(0,160)")
    c.close()

    c, p = page()
    p.goto(BASE + "#/home", wait_until="load")
    p.wait_for_timeout(2500)
    p.keyboard.press("Tab")
    out["first_tab_stop"] = p.evaluate("() => { const e=document.activeElement; return {tag:e.tagName, text:(e.textContent||'').trim().slice(0,40), href:e.getAttribute('href')}; }")
    c.close()
    br.close()
Path(sys.argv[1]).write_text(json.dumps(out, indent=1))
print("ok")
