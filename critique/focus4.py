"""Fourth pass: mesh reset only, canvas blurred before every capture (focus3 left the canvas focused, so a focus ring may have differed between initial and after-reset). A NEW browser context per mesh variant (focus2 reused one page and
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
    cv.evaluate("e => e.blur()")
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

    section("mesh_reset_blurred", lambda: [mesh(v) for v in ["drag", "keys", "keys-key0", "zoom-keys", "pick"]])

    br.close()
(out / "focus4-50352fd.json").write_text(json.dumps(res, indent=1))
print("written")
