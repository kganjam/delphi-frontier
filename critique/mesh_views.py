"""Save the three mesh canvas states for visual comparison: first paint, after keys+Reset, after drag+Reset. Read-only."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
out = Path(sys.argv[1])
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for name in ["first-paint", "keys-reset", "drag-reset"]:
        c = br.new_context(viewport={"width": 1440, "height": 900})
        p = c.new_page()
        p.goto(BASE + "#/home", wait_until="load")
        p.wait_for_selector(".mv-stage[data-mode=interactive]", timeout=45000)
        cv = p.locator(".mv-stage canvas").first
        cv.scroll_into_view_if_needed()
        p.wait_for_timeout(2500)
        box = cv.bounding_box()
        if name == "keys-reset":
            cv.focus()
            [p.keyboard.press("ArrowLeft") for _ in range(6)]
            p.locator(".mv button", has_text="Reset view").click()
        if name == "drag-reset":
            p.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            p.mouse.down()
            p.mouse.move(box["x"] + box["width"] / 2 + 140, box["y"] + box["height"] / 2 + 30, steps=8)
            p.mouse.up()
            p.locator(".mv button", has_text="Reset view").click()
        p.wait_for_timeout(1500)
        cv.evaluate("e => e.blur()")
        cv.screenshot(path=str(out / f"50352fd-mesh-{name}.png"))
        c.close()
    br.close()
