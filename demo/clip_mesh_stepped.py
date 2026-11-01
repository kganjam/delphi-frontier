"""Stepped real-interaction clip of the live Home mesh (software WebGL). Each frame is a real 1920x1080 viewport screenshot taken after a real
mouse/keyboard event on the live page; frames are encoded at a fixed fps. Timing is therefore CONSTRUCTED (not wall-clock), the pixels are not.
(A Playwright video recording of this page crashed the driver under the 4 GB cap, so this replaces it.)"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
out = Path(sys.argv[1])
fr = out / "clip-frames"
fr.mkdir(parents=True, exist_ok=True)
n = 0
log = []


def shot(p, note):
    global n
    p.screenshot(path=str(fr / f"f{n:04d}.png"))
    log.append({"frame": n, "event": note})
    n += 1


with sync_playwright() as pw:
    br = pw.chromium.launch()
    c = br.new_context(viewport={"width": 1920, "height": 1080})
    p = c.new_page()
    p.goto(BASE + "#/home", wait_until="load")
    p.wait_for_selector(".mv-stage[data-mode=interactive]", timeout=45000)
    p.evaluate("() => { const e=document.querySelector('.mv'); window.scrollTo(0, e.getBoundingClientRect().top + scrollY - 100); }")
    p.wait_for_timeout(1500)
    b = p.locator(".mv-stage canvas").first.bounding_box()
    cx, cy = b["x"] + b["width"] / 2, b["y"] + b["height"] / 2
    for _ in range(8):
        shot(p, "rest")
    p.mouse.move(cx - 160, cy)
    p.mouse.down()
    for i in range(1, 41):
        p.mouse.move(cx - 160 + i * 9, cy + i * 1.0)
        p.wait_for_timeout(60)
        shot(p, f"drag step {i}")
    p.mouse.up()
    for _ in range(6):
        shot(p, "after drag")
    p.mouse.click(cx + 40, cy - 20)
    p.wait_for_timeout(500)
    for _ in range(14):
        shot(p, "after click-pick")
    p.locator(".mv button", has_text="Reset view").click()
    p.wait_for_timeout(500)
    for _ in range(10):
        shot(p, "after Reset view")
    c.close()
    br.close()
(out / "clip-frames.json").write_text(json.dumps({"frames": n, "events": log}))
print(n)
