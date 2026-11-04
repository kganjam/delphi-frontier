OPTIONAL PUBLIC-SOURCE CAPTURE

Rebuilding the archived films uses the retained media and does not need a browser or live-site access. These optional scripts support future source review. They read the public Delphi/MorphoSwarm pages in a new isolated browser context without a user profile, login or service credential.

Dependencies: Node.js, playwright-core, an installed Chromium/Chrome executable, and an operating-system memory/task limiter. No browser binary is bundled. Set CHROMIUM_BIN to the browser executable and optionally CHROMIUM_MEMORY_MIB (default 1536). The provided launcher caps the actual browser. The capture scripts request a single browser process and one page. Do not start concurrent captures on a shared machine.

Install dependencies in an isolated directory or use your existing toolchain. Do not check node_modules or browser profiles into the repository. The capture launcher must be executable.

Examples, from this scripts directory:
  node capture-sites.mjs public-capture-targets.json NEW_SITE_CAPTURE_DIRECTORY
  node capture-deck.mjs NEW_DECK_CAPTURE_DIRECTORY
  node capture-deck.mjs NEW_DECK_CAPTURE_DIRECTORY --animate

Both scripts require a new output directory so archived source bytes are not overwritten. Targets are restricted to delphibio.org, studio.morphoswarm.ai and morphoswarm.ai. The deck script uses the published slide button labels and may need revision if the live deck changes.

The animation option captures 180 actual page frames at a target 15fps. It records wall-clock capture times and leaves the JPEG frames for encoding. A historical 12-second encode used:
  ffmpeg -framerate 15 -i sphere-frames/frame-%04d.jpg -vf fps=30 -c:v libx264 -pix_fmt yuv420p original-slide-1-animated-12s.mp4
The separately retained sphere-only clip is a crop of the recorded original composition. Its source hash and capture bounds are recorded in sources/provenance/deck/capture-provenance.json. The archive's existing clips are the canonical rebuild inputs; this optional command does not promise a byte-identical re-creation of a live animation.

The target catalog reconstructs public route URLs from the original saved page records. Detailed component screenshots and interactive states were captured during production; the catalog does not reproduce every prior selection automatically. Inspect any fresh capture before substituting it into a film.

These scripts were made path-portable and syntax-checked for the public archive. They were not rerun during archival preparation; capture provenance describes the original production captures. The Linux launcher is provided as a bounded configuration and was not exercised on the production Mac.

INVENTORY REBUILD

inventory/simulation-inventory.json is the portable curated 49-record source. From that directory, run build_inventory.mjs with @oai/artifact-tool available to regenerate the CSV, readable text and static HTML. The builder checks exact spreadsheet value round-trip and all 49 distinct IDs. It uses no credentials and runs no scientific models. check_public_links.py optionally checks distinct public URLs with four concurrent HEAD requests and a 15-second timeout per request.

The original media review's raw working copies and machine paths are not needed. Used source media is bundled by the film archive; the complete inventory streams from public links, which can change after the dated checks.
