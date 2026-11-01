"""Second focused pass: clean mesh reset experiment, neighbourhood graph with a pinned namespace, math on claim pages. Read-only."""
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


try:
  with sync_playwright() as pw:
      br = pw.chromium.launch()
      c = br.new_context(viewport={"width": 1440, "height": 900})
      p = c.new_page()
      errs = []
      p.on("pageerror", lambda e: errs.append(str(e)[:200]))
      runs = []
      for variant in ["drag-then-button", "keys-then-button", "keys-then-key0", "pick-then-button"]:
          p.goto(BASE + "#/home", wait_until="load")
          p.wait_for_selector(".mv-stage[data-mode=interactive]", timeout=45000)
          cv = p.locator(".mv-stage canvas").first
          cv.scroll_into_view_if_needed()
          p.wait_for_timeout(1500)
          h0 = px(cv)
          p.wait_for_timeout(1500)
          h0b = px(cv)
          box = cv.bounding_box()
          cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
          if variant.startswith("drag"):
              p.mouse.move(cx, cy)
              p.mouse.down()
              p.mouse.move(cx + 140, cy + 30, steps=8)
              p.mouse.up()
          elif variant.startswith("keys"):
              cv.focus()
              for _ in range(6):
                  p.keyboard.press("ArrowLeft")
          else:
              p.mouse.click(cx, cy)
          p.wait_for_timeout(500)
          h1 = px(cv)
          if variant.endswith("key0"):
              cv.focus()
              p.keyboard.press("0")
          else:
              p.locator(".mv button", has_text="Reset view").click()
          p.wait_for_timeout(800)
          h2 = px(cv)
          runs.append({"variant": variant, "initial": h0, "initial_1.5s_later": h0b, "scene_static_without_input": h0 == h0b,
                       "after_input": h1, "input_changed_pixels": h1 != h0, "after_reset": h2, "reset_equals_initial": h2 == h0})
      res["mesh_reset_experiment"] = runs

      p.goto(BASE + "#/graph/Claim/fisher-ftns", wait_until="load")
      p.wait_for_timeout(3500)
      links = p.evaluate("() => [...document.querySelectorAll('main a[href^=\"#/graph\"], main a[href*=\"ns=\"]')].map(a=>a.getAttribute('href')).slice(0,4)")
      nb = {"choice_links": links}
      if links:
          p.goto(BASE + links[0], wait_until="load")
          p.wait_for_timeout(4500)
          nb["after_choice"] = p.evaluate("() => ({svg: !!document.querySelector('main svg.gsvg'), nodes: document.querySelectorAll('main g.g-node').length, text: document.querySelector('main').innerText.slice(0,300), zoomctl: document.querySelectorAll('main [data-z]').length})")
          if nb["after_choice"]["nodes"]:
              t = lambda: p.evaluate("() => document.querySelector('main svg.gsvg g[transform]')?.getAttribute('transform')")  # noqa: E731
              a = t()
              p.locator("main [data-z=in]").click()
              b = t()
              p.locator("main g.g-node").nth(1).click()
              nb["zoom_in_transform"] = [a, b]
              nb["node_click_detail"] = p.evaluate("() => document.querySelector('#gdetail')?.innerText.slice(0,80)")
      res["neighbourhood_graph"] = nb

      m = {}
      for route in ["#/knowledge/fisher-ftns", "#/knowledge/fisher-infinitesimal", "#/entity/Claim/fisher-ftns"]:
          p.goto(BASE + route, wait_until="load")
          try:
              p.wait_for_selector(".katex, .katex-error", timeout=12000)
          except Exception:
              pass
          m[route] = p.evaluate("() => ({rendered: document.querySelectorAll('.katex').length, errors: document.querySelectorAll('.katex-error').length, raw_frac_in_text: /\\\\frac|\\\\Delta/.test(document.querySelector('main').innerText), sample_aria: [...document.querySelectorAll('.katex')].slice(0,2).map(e=>(e.closest('[aria-label]')||e).getAttribute('aria-label')?.slice(0,70))})")
          if m[route]["rendered"]:
              p.screenshot(path=str(out / "screens" / ("50352fd-math-" + route.strip("#/").replace("/", "-") + ".png")))
      res["math_on_claim_pages"] = m
      res["page_errors"] = errs
      br.close()
finally:
    res["incomplete_if_missing_keys"] = True
    (out / "focus2-50352fd.json").write_text(json.dumps(res, indent=1))
