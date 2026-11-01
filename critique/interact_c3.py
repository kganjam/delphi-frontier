"""Read-only interaction checks on live c3fd6026: mesh orbit/reset, Studio region/assurance, parameter control, ecology viewer, history,
graphs, demo page, phone nav. Nothing is submitted (no Check button, no contribute, no annotation). One fresh context per section."""
import hashlib
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
OUT = Path(sys.argv[1])
res = {}


def px(cv):
    cv.evaluate("e => e.blur()")
    return hashlib.sha256(cv.screenshot()).hexdigest()[:12]


def settle(p, cv):
    last = None
    for _ in range(10):
        h = px(cv)
        if h == last:
            return h
        last = h
        p.wait_for_timeout(400)
    return last


def section(name, fn):
    try:
        res[name] = fn()
    except Exception as e:
        res[name] = {"section_error": repr(e)[:260]}


with sync_playwright() as pw:
    br = pw.chromium.launch()

    def ctx(w=1440, h=900, mobile=False):
        c = br.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile)
        p = c.new_page()
        p.errs = []
        p.on("pageerror", lambda e: p.errs.append(str(e)[:160]))
        return c, p

    def mesh():
        out = []
        for v in ["keys", "drag"]:
            c, p = ctx()
            p.goto(BASE + "#/home", wait_until="load")
            p.wait_for_selector(".mv-stage[data-mode=interactive], .mv-stage[data-mode=fallback]", timeout=45000)
            mode = p.get_attribute(".mv-stage", "data-mode")
            if mode != "interactive":
                out.append({"variant": v, "mode": mode})
                c.close()
                continue
            cv = p.locator(".mv-stage canvas").first
            cv.scroll_into_view_if_needed()
            h0 = settle(p, cv)
            b = cv.bounding_box()
            if v == "keys":
                cv.focus()
                [p.keyboard.press("ArrowLeft") for _ in range(6)]
            else:
                p.mouse.move(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
                p.mouse.down()
                p.mouse.move(b["x"] + b["width"] / 2 + 140, b["y"] + b["height"] / 2 + 30, steps=8)
                p.mouse.up()
            h1 = settle(p, cv)
            p.locator(".mv button", has_text="Reset view").click()
            h2 = settle(p, cv)
            out.append({"variant": v, "mode": mode, "orbit_changed": h1 != h0, "reset_equals_initial_hash": h2 == h0, "errs": p.errs})
            c.close()
        return out

    def studio_region():
        c, p = ctx()
        p.goto(BASE + "#/studio/flying-fish", wait_until="load")
        p.wait_for_timeout(5000)
        r = p.evaluate("() => ({assurance: !!document.querySelector('#assurance'), ctrls: [...document.querySelectorAll('main select, main input[type=range], main input[type=number]')].map(e=>e.tagName+':'+(e.id||e.name||e.getAttribute('aria-label')||'')).slice(0,14), nodes: document.querySelectorAll('#assurance [role=button], #assurance button, #assurance [data-node]').length, h2: [...document.querySelectorAll('main h2')].map(e=>e.textContent.trim().slice(0,40)).slice(0,14)})")
        c.close()
        return r

    def engineering_params():
        c, p = ctx()
        p.goto(BASE + "#/engineering", wait_until="load")
        p.wait_for_timeout(5000)
        ctr = p.evaluate("() => [...document.querySelectorAll('main select, main input')].map(e=>e.tagName+':'+e.type+':'+(e.id||e.name||'')+':'+(e.labels&&e.labels[0]?e.labels[0].textContent.trim().slice(0,30):'')).slice(0,20)")
        r = {"controls": ctr}
        sel = p.locator("main select").first
        if sel.count():
            before = p.evaluate("() => document.querySelector('main').innerText.length")
            opts = sel.evaluate("e => [...e.options].map(o=>o.value)")
            if len(opts) > 1:
                sel.select_option(opts[1])
                p.wait_for_timeout(1500)
                r["select_changed_text_len"] = [before, p.evaluate("() => document.querySelector('main').innerText.length")]
                r["stale_or_recompute_words"] = p.evaluate("() => (document.querySelector('main').innerText.match(/stale|recomput|preview|needs re-?run|not re-?run/gi)||[]).slice(0,6)")
        r["errs"] = p.errs
        c.close()
        return r

    def ecology():
        c, p = ctx()
        p.goto(BASE + "#/ecology", wait_until="load")
        p.wait_for_selector("#eco-host canvas", timeout=30000)
        p.wait_for_timeout(2500)
        t0 = p.evaluate("() => document.querySelector('#eco-host')?.innerText.match(/t = [0-9.]+ s/)?.[0]")
        rng = p.locator("#eco-host input[type=range]").first
        r = {"t0": t0, "range": rng.count()}
        if rng.count():
            rng.evaluate("e => { e.value = Math.round(e.max*0.5); e.dispatchEvent(new Event('input', {bubbles:true})); e.dispatchEvent(new Event('change', {bubbles:true})); }")
            p.wait_for_timeout(800)
            r["t_after_scrub"] = p.evaluate("() => document.querySelector('#eco-host')?.innerText.match(/t = [0-9.]+ s/)?.[0]")
        cases = p.locator("#eco-host button", has_text="Escape, with neighbours")
        if cases.count():
            cases.first.click()
            p.wait_for_timeout(2500)
            r["after_case_click"] = p.evaluate("() => document.querySelector('#eco-host')?.innerText.slice(0,200)")
            fish = p.locator("#eco-host [data-fish], #eco-host button:has-text('fish-')")
            r["fish_buttons"] = fish.count()
            if fish.count() > 2:
                fish.nth(2).click()
                p.wait_for_timeout(600)
                r["fish_detail"] = p.evaluate("() => document.querySelector('#eco-host')?.innerText.match(/fish-0[0-9][^\\n]*/g)?.slice(0,3)")
        r["banner"] = p.evaluate("() => [...document.querySelectorAll('#eco-host *')].map(e=>e.innerText||'').find(t=>/Run ended at/.test(t))?.slice(0,160)")
        r["errs"] = p.errs
        c.close()
        return r

    def history():
        c, p = ctx()
        p.goto(BASE + "#/history", wait_until="load")
        p.wait_for_timeout(4000)
        r = p.evaluate("() => ({nodes: document.querySelectorAll('main svg g.g-node, main svg [role=button], main button.node, main [data-node]').length, tables: document.querySelectorAll('main table').length, sel_text: document.querySelector('main')?.innerText.match(/Select a node[^\\n]*/)?.[0]})")
        n = p.locator("main svg [role=button], main svg g.g-node, main [data-node]")
        if n.count() > 1:
            before = p.evaluate("() => document.querySelector('main').innerText.length")
            n.nth(1).click(timeout=6000)
            p.wait_for_timeout(700)
            r["detail_changed"] = before != p.evaluate("() => document.querySelector('main').innerText.length")
        r["errs"] = p.errs
        c.close()
        return r

    def graphs():
        out = {}
        c, p = ctx()
        p.goto(BASE + "#/knowledge?tab=graph", wait_until="load")
        p.wait_for_timeout(4000)
        out["claim_graph_nodes"] = p.locator("main svg g.g-node").count()
        out["claim_graph_zoom_controls"] = p.locator("main [data-z]").count()
        c.close()
        c, p = ctx()
        p.goto(BASE + "#/graph/Claim/fisher-ftns", wait_until="load")
        p.wait_for_timeout(3500)
        links = p.evaluate("() => [...document.querySelectorAll('main a')].map(a=>a.getAttribute('href')).filter(h=>/ns=/.test(h||''))")
        out["ambiguous_choices"] = len(links)
        if links:
            p.goto(BASE + links[0], wait_until="load")
            p.wait_for_timeout(5000)
            out["pinned"] = p.evaluate("() => ({nodes: document.querySelectorAll('main g.g-node').length, edges: document.querySelectorAll('main svg line').length, zoom: document.querySelectorAll('main [data-z]').length, trunc_text: /truncat/i.test(document.querySelector('main').innerText), legend: !!document.querySelector('main .legend')})")
            z = p.locator("main [data-z=in]")
            if z.count():
                tf = lambda: p.evaluate("() => document.querySelector('main svg.gsvg g[transform]')?.getAttribute('transform')")  # noqa: E731
                a = tf()
                z.first.click()
                out["zoom_in"] = [a, tf()]
                p.locator("main [data-z=out]").first.click()
                out["zoom_out"] = tf()
                rs = p.locator("main [data-z=reset]")
                if rs.count():
                    rs.first.click()
                    out["zoom_reset"] = tf()
        c.close()
        return out

    def demo():
        c, p = ctx()
        p.goto(BASE + "#/demo", wait_until="load")
        p.wait_for_timeout(4000)
        r = p.evaluate("() => ({videos: [...document.querySelectorAll('video')].map(v=>({src:(v.currentSrc||v.getAttribute('src')||'').replace(location.origin,''), poster:(v.getAttribute('poster')||'').replace(location.origin,''), tracks:[...v.querySelectorAll('track')].map(t=>t.getAttribute('src')), controls:v.controls})), links:[...document.querySelectorAll('main a[href]')].map(a=>a.getAttribute('href')).filter(h=>/mp4|vtt|srt|poster|jpg|manifest|txt/.test(h||'')).slice(0,20)})")
        heads = []
        for u in {x for v in r["videos"] for x in [v["src"], v["poster"]] + v["tracks"] if x} | set(r["links"]):
            q = c.request.head(BASE + u.lstrip("/"), timeout=20000)
            heads.append([u, q.status, q.headers.get("content-length"), q.headers.get("content-type")])
        r["heads"] = heads
        r["errs"] = p.errs
        c.close()
        return r

    def autocomplete():
        c, p = ctx()
        p.goto(BASE + "#/home", wait_until="load")
        p.wait_for_timeout(3000)
        p.click("#gq")
        p.keyboard.type("fin mech", delay=120)
        p.wait_for_timeout(2500)
        r = p.evaluate("() => ({expanded: document.querySelector('#gq')?.getAttribute('aria-expanded'), role: document.querySelector('#gq')?.getAttribute('role'), options: [...document.querySelectorAll('#ac-list [role=option], #ac-list li')].map(e=>e.innerText.replace(/\\s+/g,' ').slice(0,70)).slice(0,5), status: document.querySelector('#ac-status, [aria-live]')?.innerText?.slice(0,80)})")
        p.keyboard.press("ArrowDown")
        p.wait_for_timeout(300)
        r["active_descendant"] = p.evaluate("() => document.querySelector('#gq')?.getAttribute('aria-activedescendant')")
        p.keyboard.press("Escape")
        p.wait_for_timeout(300)
        r["after_escape_expanded"] = p.evaluate("() => document.querySelector('#gq')?.getAttribute('aria-expanded')")
        r["errs"] = p.errs
        c.close()
        return r

    def phone():
        c, p = ctx(400, 800, True)
        p.goto(BASE + "#/home", wait_until="load")
        p.wait_for_timeout(4000)
        r = {"overflow": p.evaluate("() => document.documentElement.scrollWidth > innerWidth + 1")}
        about = p.locator(".aboutmenu summary")
        if about.count():
            about.first.tap()
            p.wait_for_timeout(500)
            r["about_menu_links"] = p.locator(".aboutmenu a").count()
            r["about_menu_visible"] = p.locator(".aboutmenu ul").first.is_visible()
        r["mesh_mode"] = p.evaluate("() => document.querySelector('.mv-stage')?.dataset.mode")
        r["errs"] = p.errs
        c.close()
        return r

    for name, fn in [("mesh", mesh), ("studio_region", studio_region), ("engineering_params", engineering_params), ("ecology", ecology),
                     ("autocomplete", autocomplete), ("history", history), ("graphs", graphs), ("demo", demo), ("phone", phone)]:
        section(name, fn)
    br.close()
(OUT / "interactions.json").write_text(json.dumps(res, indent=1))
print("written")
