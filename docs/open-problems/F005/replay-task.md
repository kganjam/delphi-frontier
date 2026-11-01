# Offered task: independent replay of reaction-diffusion sweep cells 240 and 1306

Status: **offered in draft, not taken.** No second participant has seen or accepted it. Not proposed to the live store yet (needs a
provisioned credential and the lead's approval).

## Why these two cells
* Cell 240 (Schnakenberg, ρ = 3, ε = 0.01): the frozen sweep's final dominant mode is 7, the fastest linear mode is 6 — an R3 mismatch in F003.
* Cell 1306 (Brusselator, ρ = 0.97, linearly stable, ε = 0.3): a finite-amplitude pattern (mode 5) from a linearly stable state — an R1 event.
Both were reproduced by the project's own rerun to 4e-15 (`engineering/simulation/rd/receipt.json`); that rerun is **not independent**.

## How to reach it (no credential needed)
1. MCP `https://frontier.morphoswarm.ai/mcp` (Streamable HTTP): `frontier_search {"query": "Schnakenberg cell 240"}` returns Claim
   `node-a/Claim/viz-rd-claim-cell-240` version `4a649305d04a8a9599fbbd19b874091924f34644bff06337bd54613a7b362407`; `frontier_get` on it and on
   Problem `delphi-frontier/F003` version `72c7b472…a52cc` resolve (receipt: `mcp-reachability-receipt.json`).
2. Inputs: `https://raw.githubusercontent.com/kganjam/delphi-frontier/42cbd81857b3f8c0962382cda701709326711b5a/engineering/simulation/rd/cells.json`,
   sha256 `f74184cb56ba36e4face9978c96c2c00ae728a471183294c3f9d866eb066d6b6` (checked 2026-11-01 by fetching the raw URL).

## What to do
Integrate each cell with your own solver to T = 800 τ (zero-flux ends, Du = 1, the cell's Dv, L, kinetics; initial condition = steady
state + the K-mode cosine series defined by the cell's `seed`, `K`, `eps`). Report the final dominant cosine mode (largest |DCT-II| of u − mean,
mode 0 excluded) and std(u), then repeat once with dt halved or the grid doubled. Fill the submission format in `check_replay.py`'s docstring
and run `python3 -I check_replay.py submission.json`.

## Acceptance (mechanical, then human)
Mode equal and std(u) within 2% on both cells, your own refinement consistent, receipt exit 0 → mechanically accepted; then a reviewer who
is neither you nor the project author reads it. **A disagreement is a useful result**: it moves the cell to unresolved in F003.
Checker self-test (project's own non-independent rerun as input): exit 0; a mutant with cell 240's mode changed to 6: exit 1; fetching
cells.json from the raw URL instead of a local copy: exit 0.
