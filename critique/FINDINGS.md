# Independent read-only audit of the public Frontier site

Auditor: Claude Sonnet 5.5 (Claude Code, existing Max subscription capacity; no delegated/metered forks). Provider cost: none observed by me;
I did not read a usage endpoint, so actual spend is unknown, not zero. Did not author the site UI. All times Seattle (PDT) unless UTC shown.
Tools: Playwright 1.58.0 (python), Chromium headless shell 145.0.7632.6. Target `https://frontier.morphoswarm.ai/`. GET/HEAD only; the only
"input" was typing into the header search box (a hash navigation). No annotation, credential or contribute write was made.

## What was run, and against which release (read carefully)
| run | when | release | scope |
|---|---|---|---|
| `critique/52cda98/` bulk crawl | ~17:03-17:19 PDT | **started on 52cda98; production moved to d531330 at an unknown time during it** (the server sends no deploy time). Treat as MIXED, labelled 52cda98 as asked. | 70 routes (21 seeds + links followed, cap 70; **150 discovered links left unvisited**) x desktop 1440 / phone 400 = 140 fresh-page loads, viewport screenshots, DOM checks |
| `critique/d531330/` | ~17:20-17:23 PDT | d531330: four served files (`index.html`, `js/app.js`, `js/studio.js`, `js/history.js`) are byte-identical (sha256) to that commit's `site/` copies | `#/studio`, `#/history`, `#/home` x 2 viewports; interaction probes; two single-load follow-ups |
| `critique/postfix/` | 17:23 PDT (UTC 00:23) | production after root's nginx change d3c8890 **(I did not verify it was live; I only know root said it was deployed)** | 3 ordinary sequential loads, 6 s apart |
Not covered: the 150 unvisited links; any logged-in/contributor flow; any write path; Safari/Firefox (Chromium only); screen readers; colour contrast
(not measured); math (see below); media playback in a full (non-headless-shell) browser; full-page screenshots (viewport only).

## Findings (pre-fix values preserved; each says what was observed)
1. **Rate limiting broke page start-up (observed, root confirmed cause).** In the bulk crawl `/api/session` returned 429 on 51 of 140 loads (25 phone, 26 desktop;
   my crawl was fast and concurrent with other users, so my own load contributed). Three entity routes rendered a blank `main` (21 chars, no `h1`); one threw
   `Cannot destructure property 'html' of 'DF' as it is undefined` (a script did not load). Root's later measurement: 85 HTTP 429 in 1,500 recent requests, mostly JS.
   The app shows **no error or retry message** when its scripts are starved: the visitor sees an empty page. That is a defect independent of the nginx fix.
2. **After the fix (17:23 PDT, 3 loads): pages draw (`h1`=1, no page errors), but `/api/session` still returned 429 on all three** (observed, not explained).
   Either the fix was not yet live, or `/api/session` is covered by the API allowance and an ordinary page load can exceed it. Not resolved here.
3. **Those three routes are not a clean test of entity pages.** The blank routes were `#/frontier?live=morpholib-...-problem-remediation`; loaded singly they render
   the same 8,187-character page for all three, so I could not confirm that `live=` selects a distinct record on this static site. UNVERIFIED either way.
4. **`#/graph` with no parameters is a dead end:** text is "The graph could not be built: "" is not a record kind this site knows ... Nothing is drawn", and it emits
   an unnamed link `<a href="#/entity//"> </a>` (empty accessible name). I reached `#/graph` by guessing the URL, not from a link; whether anything links to it bare is unchecked.
5. **No skip link, and phone focus indicators:** first Tab on `#/home` lands on a candidate chooser control; no "skip to content" (desktop and phone).
   On phone, 4 of the first 30 tab stops had `outline: none` and no box-shadow (my computed-style test; not a visual check). Desktop: 0 of 30.
6. **Home `turntable.mp4` did not load in headless Chromium:** the request ends `net::ERR_ABORTED`; the first `<video>` ended with empty `currentSrc`, readyState 0, while a
   second video on the page reached readyState 4. `HEAD` on the file returned 200. I did not test a full browser, so this may be a headless artifact or a preload abort. UNVERIFIED as a site defect.
7. **Studio `flying-fish` downloads:** 6 STLs linked; the ones I fetched returned 200 with `model/stl` and content-length equal to bytes received (hash list in `critique/d531330/followup2.json`).
   I did NOT compare these hashes with published ones (the first probe's lookup in `snapshot.json` only covered the two JSON files it found). `#/studio` itself shows 0 canvases
   after 9 s and `#/studio/flying-fish` also 0 canvases after 8 s: **I did not find or exercise an interactive 3D viewer** (home's keyboard order mentions "Interactive 3D fish mesh"). WebGL is available in this Chromium. 3D interaction: NOT verified.
8. **Knowledge infinite scroll works as observed:** 8 wheel scrolls grew the item count 50 -> 300 (steps of 50), page height 41,626 px, no page errors. Back/forward: hash and heading
   restored after Back and after reload.
9. **Search:** "fish" navigates to `#/search?q=fish&tab=catalog`; nonsense query shows "No ranked result"; `<img onerror>` and quote strings produced no injected `img` and no dialog.
   My result-count column is a poor metric (counts generic list items; 20 on the empty-result page), so I make no claim about result counts.
10. **Graphs:** `#/knowledge?tab=graph` has one labelled SVG ("Claim graph"), 118 elements (path/g/rect/text), 26 focusable/clickable. I did **not** click a node, pan or zoom: interaction NOT verified.
    `#/graph` drew nothing (see 4).
11. **`#/history` (new in d531330):** `h1` "Fish design history"; sections How to read it / Lineage / Select a node / Sibling groups / Every node, as a table; 2 tables, 0 images, 0 forms,
    no horizontal overflow on desktop or phone, no page errors. The lineage interaction ("Select a node") was not exercised.
12. **Layout and structure, 52cda98-labelled crawl:** no horizontal overflow on any of 70 routes at either viewport; `h1`=1 on all except the 3 blank ones; no duplicate ids, no
    unlabelled inputs, no images without alt, no positive tabindex found by my checks.
13. **Math:** my check looked for raw TeX in page text (`\(`, `$$`, `\frac`) and found none on the 70 routes; I did not count rendered math elements per route, so "math renders correctly" is NOT established.
14. **Scientific labelling:** I did not audit labelling claim by claim. What I saw: the search page states ranks are "not truth, quality or acceptance" and shows a score only with its kind; `#/history` and the Home pages
    were screenshotted but not read for claim wording. NOT assessed.

## Probe false positives (recorded so nobody re-files them)
- `bad_text` "null" on `#/work`/`#/system`: real prose ("retain null results"). `#/evidence` flagged "Not found" by Studio-link probe: a table cell value "not found". Neither is a defect.

## Reproduce / files
`critique/crawl.py` (bulk), `interact.py`, `followup.py`, `followup2.py`, `recheck_blank.py`; outputs `critique/<tag>/routes.json`, `interactions.json`, `followup*.json`, `screens/`.
Under `systemd-run --user --scope -p TasksMax=256 -p MemoryMax=4G -p MemorySwapMax=0 -p CPUQuota=100%`. `TasksMax=256` was needed for Chromium.

---
# Addendum: focused Home mesh / graph / math check on 50352fd (completes items 7, 10, 13 of the first audit)

**Release check, 17:45 PDT.** Live `index.html` + all 27 `js/`/`css/` files (28 files) are byte-identical (sha256) to commit `50352fd` and live
`data/snapshot.json` sha256 prefix is `035388ce988766c8`, the value in `50352fd` (it was `1ffb82fa…`, `d531330`'s, at 17:38). So the focus runs below
ran against 50352fd content. Readiness was awaited by app state (`.mv-stage[data-mode=interactive]`, then pixel settling, then `.katex` presence), never networkidle.
Files: `critique/focus/focus-50352fd-run1.json` (first run; its label says it was first misnamed "rehearsal-d531330" before I checked the hash),
`focus3-50352fd.json`, `focus4-50352fd.json`, screenshots in `critique/focus/screens/`. **Superseded:** `focus2.py` crashed without output on its first attempt; its
second attempt (`focus2-50352fd.json`, partial) is **confounded** (one page reused, a same-hash `goto` does not reload, so each "initial" was the previous run's end state;
mid-reset captures). Do not cite it. `focus3` left the canvas focused (a focus ring enters a canvas screenshot), so `focus4` blurs before every capture.

**Home 3D mesh (actual `fish-adult-fao.glb`, 4.78 MB, status line says sha256 matches `appearance-adult-fao.json`: that is the page's statement, I did not recompute it).**
- Interactive in 3.9 s (single timing); WebGL available in this Chromium; 13 components listed.
- **Orbit:** 6 ArrowLeft presses and a mouse drag each changed the canvas pixels. The scene is static without input (identical captures 1.5 s apart). Observed in 5 fresh contexts: first-paint hash identical every time (`0fb5c877…`).
- **Pick:** of 4 clicks, 2 selected a part and filled the detail panel (SCALES, PECTORAL_L, with GLB node/provenance text), 2 hit no part and left the default prompt. Which list item is highlighted: NOT verified (my selector guess matched nothing).
- **Reset view:** after keyboard orbit or zoom, `Reset view` and key `0` give the same final image, and it matches the first-paint image to within noise (0 pixels differ by >30 of 435,936; mean abs diff 0.07; the hashes still differ). **After one mouse drag, Reset leaves a visibly different framing:** 38,247 pixels (8.8%) differ by >30, mean abs 7.15 (`50352fd-mesh-drag-reset.png` vs `-first-paint.png`, viewed side by side: the fish sits slightly larger and shifted). One drag, one run; cause not investigated.
- **Reset does not clear a pick:** after a click-pick, `Reset view` left the pixels unchanged (selection highlight remained). Whether that is intended is not established.
- Not tested: touch orbit/pinch, scroll-wheel zoom, "Show all components", component checkboxes, the fallback (static render) path.

**Graphs.**
- Claim graph `#/knowledge?tab=graph` (21 nodes): clicking a node opened its detail and changed the hash to `#/knowledge/fisher-infinitesimal?tab=graph`. **I found no zoom or pan control there and the wheel changed no transform** (no `g[transform]` exists), so zoom is absent or undetected on this graph.
- Neighbourhood graph: unpinned `#/graph/Claim/fisher-ftns` asks the visitor to choose a namespace (`delphi-frontier` or `node-a`; "nothing is picked for you"). Pinned (`ns=delphi-frontier&v=…`): the page says it is from the runtime's `/api/graph`, draws **1 node and 0 edges**, the `Zoom in` control changed `scale(1)` to `scale(1.25)`, and clicking the node opened its claim detail. Zoom out, reset, wheel and drag-pan were not exercised. A one-node graph is a weak test of node-to-node interaction.

**Math.** `#/knowledge/fisher-ftns`: 3 `.katex` elements, 0 `katex-error`, no raw `\frac`/`\Delta` in the text; `#/knowledge/fisher-infinitesimal`: 5 `.katex`, 0 errors, same. Each carries its TeX source in `aria-label` (e.g. `\Delta_{NS}\bar{w} = V_A(w)/\bar{w}`).
Only these 2 of the snapshot's 21 claims were checked (the snapshot holds 27 `\frac` occurrences overall); `#/entity/Claim/fisher-ftns` is the ambiguous-namespace page and shows no math. Visual correctness of the typesetting beyond these two screenshots was not judged.

Scope reminders unchanged: Chromium headless shell 145 only; no Safari/Firefox; no touch; the first audit's pre-fix findings, labels and false-positive notes stand.
