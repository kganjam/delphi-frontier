"""One ordinary fresh load per previously blank route (sequential, 6 s apart). Read-only; no synthetic load."""
import datetime
import json
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

BASE = "https://frontier.morphoswarm.ai/"
ROUTES = ["#/frontier?live=morpholib-pezzulo-bioelectric-target-morphology-memory-problem-remediation", "#/frontier?live=morpholib-streichan-global-morphogenetic-flow-problem-remediation", "#/frontier?live=morpholib-thomas-coral-calice-septa-insertion-problem-remediation"]
out = []
with sync_playwright() as pw:
    br = pw.chromium.launch()
    for r in ROUTES:
        c = br.new_context(viewport={"width": 1440, "height": 900})
        p = c.new_page()
        errs, bad = [], []
        p.on("pageerror", lambda e: errs.append(str(e)[:160]))
        p.on("response", lambda x: bad.append(f"{x.status} {x.url[-60:]}") if x.status >= 400 else None)
        p.on("requestfailed", lambda x: bad.append(f"FAILED {x.url[-60:]} {x.failure}"))
        t = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
        p.goto(BASE + r, wait_until="load")
        p.wait_for_timeout(5000)
        s = p.evaluate("() => ({h1: document.querySelectorAll('h1').length, main: document.querySelector('main')?.innerText.length})")
        out.append({"route": r, "utc": t, **s, "page_errors": errs, "bad": bad})
        c.close()
        time.sleep(6)
    ver = br.version
    br.close()
Path(sys.argv[1]).write_text(json.dumps({"chromium": ver, "rows": out}, indent=1))
