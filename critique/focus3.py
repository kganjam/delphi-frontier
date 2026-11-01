"""Third focused pass (replaces focus2's confounded mesh experiment). A NEW browser context per mesh variant (focus2 reused one page and
a same-hash goto does not reload, so each 'initial' was the previous run's end state), and pixels are read only after they settle
(two consecutive identical captures). Each section is isolated so one failure does not lose the others. Read-only."""
import hashlib
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
out = Path(sys.argv[1])
res = {}


def px(cv):
    return hashlib.sha256(cv.screenshot()).hexdigest()[:16]


def settled(p, cv, tries=12):
    last, seq = None, []
    for _ in range(tries):
        h = px(cv)
        seq.append(h)
        if h == last:
            return h, len(seq) * 0.4
        last = h
        p.wait_for_timeout(400)
    return seq[-1], None


def section(name, fn):
    try:
        res[name] = fn()
    except Exception as e:
        res[name] = {"section_error": repr(e)[:300]}


with sync_playwright() as pw:
    br = pw.chromium.launch()

    def mesh(variant):
        c = br.new_context(viewport={"width": 1440, "height": 900})
        p = c.new_page()
        p.goto(BASE + "#/home", wait_until="load")
        p.wait_for_selector(".mv-stage[data-mode=interactive]", timeout=45000)
        cv = p.locator(".mv-stage canvas").first
        cv.scroll_into_view_if_needed()
        h0, t0 = settled(p, cv)
        box = cv.bounding_box()
        cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
        if variant == "drag":
            p.mouse.move(cx, cy)
            p.mouse.down()
            p.mouse.move(cx + 140, cy + 30, steps=8)
            p.mouse.up()
        elif variant.startswith("keys"):
            cv.focus()
            for _ in range(6):
                p.keyboard.press("ArrowLeft")
        elif variant == "zoom-keys":
            cv.focus()
            for _ in range(4):
                p.keyboard.press("+")
        else:
            p.mouse.click(cx, cy)
        h1, _ = settled(p, cv)
        if variant == "keys-key0":
            cv.focus()
            p.keyboard.press("0")
        else:
            p.locator(".mv button", has_text="Reset view").click()
        h2, t2 = settled(p, cv)
        r = {"variant": variant, "initial": h0, "after_input": h1, "input_changed": h1 != h0, "after_reset": h2,
             "reset_equals_initial": h2 == h0, "settle_s_after_reset": t2}
        c.close()
        return r

    section("mesh_reset", lambda: [mesh(v) for v in ["drag", "keys", "keys-key0", "zoom-keys", "pick"]])

    def nb():
        c = br.new_context(viewport={"width": 1440, "height": 900})
        p = c.new_page()
        p.goto(BASE + "#/graph/Claim/fisher-ftns", wait_until="load")
        p.wait_for_timeout(3500)
        links = p.evaluate("() => [...document.querySelectorAll('main a')].map(a=>[a.getAttribute('href'),a.textContent.trim().slice(0,50)]).filter(x=>/graph|ns=/.test(x[0]||'')).slice(0,4)")
        r = {"choice_links": links}
        if links:
            p.goto(BASE + links[0][0], wait_until="load")
            p.wait_for_timeout(5000)
            r["after_choice"] = p.evaluate("() => ({svg: !!document.querySelector('main svg.gsvg'), nodes: document.querySelectorAll('main g.g-node').length, edges: document.querySelectorAll('main svg line').length, zoomctl: document.querySelectorAll('main [data-z]').length, text: document.querySelector('main').innerText.slice(0,260)})")
            if r["after_choice"]["zoomctl"]:
                tf = lambda: p.evaluate("() => document.querySelector('main svg.gsvg g[transform]')?.getAttribute('transform')")  # noqa: E731
                a = tf()
                p.locator("main [data-z=in]").first.click()
                r["zoom_in_transform"] = [a, tf()]
            if r["after_choice"]["nodes"]:
                p.locator("main g.g-node").last.click(timeout=8000)
                r["node_click_detail"] = p.evaluate("() => document.querySelector('#gdetail')?.innerText.slice(0,100)")
        c.close()
        return r

    section("neighbourhood_graph", nb)

    def math():
        c = br.new_context(viewport={"width": 1440, "height": 900})
        p = c.new_page()
        m = {}
        for route in ["#/knowledge/fisher-ftns", "#/knowledge/fisher-infinitesimal", "#/entity/Claim/fisher-ftns"]:
            p.goto(BASE + route, wait_until="load")
            try:
                p.wait_for_selector(".katex, .katex-error", timeout=12000)
            except Exception:
                pass
            m[route] = p.evaluate("() => ({rendered: document.querySelectorAll('.katex').length, errors: document.querySelectorAll('.katex-error').length, raw_tex_in_text: /\\\\frac|\\\\Delta/.test(document.querySelector('main').innerText), sample_aria: [...document.querySelectorAll('.katex')].slice(0,2).map(e=>(e.closest('[aria-label]')||e).getAttribute('aria-label')?.slice(0,70)), h1: document.querySelector('h1')?.textContent.slice(0,50)})")
            if m[route]["rendered"]:
                p.screenshot(path=str(out / "screens" / ("50352fd-math-" + route.strip("#/").replace("/", "-") + ".png")))
        c.close()
        return m

    section("math_on_claim_pages", math)
    br.close()
(out / "focus3-50352fd.json").write_text(json.dumps(res, indent=1))
print("written")
