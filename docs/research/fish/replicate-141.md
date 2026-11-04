# Replication of claim 141 — [S1-D-D] adult zebrafish escape speed (Danos & Lauder 2012)

Independent re-derivation, written without seeing the recorded derivation.

## What I looked at and what I did not

- I searched this repository (all branches present locally: `claude/s1-d-escape-speed-replication-1ngcms`,
  `work/frontier-foundation`) for `S1-D`, `escape`, `Danos` and `fish`, in file contents and commit messages.
  **None found.** There is no `docs/research/fish/` directory and no branch named
  `deepen-s1-d-sensitive-input-3mdmls`. So I did not come across the earlier working.
- **Caveat on independence:** the question text itself contains the claimed values
  (0.84 m/s, 0.95 m/s, 1.03 SL, ≤31 %). I could not avoid reading them. So my arithmetic below is a check
  of the stated numbers, not a blind derivation of them.

## Primary source: what I could read

| Source | Read-level | What it gives |
|---|---|---|
| Danos N. & Lauder G.V. (2012) *Challenging zebrafish escape responses by increasing water viscosity.* J. Exp. Biol. 215:1854–1862, doi:10.1242/jeb.068957 (PMID 22573764) | **abstract** (via Europe PMC REST) | Adult *Danio rerio*, 1000 fps video, three viscosities (1, 10, 20 mPa s). Viscosity "decreased maximum velocity of the center of mass … during stage 1". **The abstract gives no velocity value and no body length.** |
| Same paper, full text | **could-not-access** | Tried: journals.biologists.com article page and PDF (Cloudflare challenge, 403); sites.harvard.edu/glauder PDF (blocked by the proxy); dash.harvard.edu (blocked); unpaywall and semanticscholar APIs (blocked by the proxy). |
| Crossref record for the DOI | listing | Confirms the bibliographic data only. |
| Mohammadi et al. (2025, iScience; PMC11930232), cites Danos & Lauder as ref. 13 | full-text (read through WebFetch) | Cites the paper but gives **no** adult escape velocity or adult body length. The only length it reports is 3.829 mm SL for 5 dpf larvae, which does not apply here. |
| Web search (standard and extended) for the paper's velocity values in m s⁻¹ or BL s⁻¹ | search-summary | No numeric value found. Scope: two web searches, with result snippets only. |

## Result

**Adult escape speed from Danos & Lauder 2012: `unknown`.** I could not get the paper's Table 1 or Results text,
so I cannot confirm the input "0.84 m/s" from the primary source, and I cannot tell whether it was quoted
directly or derived (for example, as BL s⁻¹ × body length). This is the deliverable: a precisely scoped
negative result.

The adult standard length (SL) that Danos & Lauder used is also `unknown` (full text not accessed).

## Conditional arithmetic (calculated, not observed)

This is a drag-free ballistic apex height, h = v²/(2g), with g = 9.80665 m s⁻². It assumes the full escape
speed is directed vertically at the water surface. Both v values are taken **from the question text, not
from a source I read**.

- v = 0.84 m/s → h = 0.7056 / 19.6133 = **0.03598 m (3.60 cm)**
- v = 0.95 m/s → h = 0.9025 / 19.6133 = **0.04601 m (4.60 cm)**
- Ratio of heights: (0.84/0.95)² = 0.884² = 0.782, so the height is 21.8 % lower. The speed itself is 11.6 % lower.
- "A 13 % drop": 0.95 × 0.87 = 0.8265 m/s → h = 3.48 cm. So 0.84 m/s is a smaller drop (11.6 %) than the stated 13 % flip threshold.

To express h in body lengths I need an adult SL that I could not source. Below, the SL values are
**assumptions spanning a typical adult zebrafish range, not citations**:

| SL (assumed) | h/SL at 0.84 m/s | h/SL at 0.95 m/s |
|---|---|---|
| 3.0 cm | 1.20 | 1.53 |
| 3.5 cm | 1.03 | 1.31 |
| 4.0 cm | 0.90 | 1.15 |

Inference (mine): the stated "1.03 SL drag-free upper bound" matches v = 0.84 m/s only if SL ≈ 3.49 cm
(0.03598 / 1.03). The arithmetic is internally consistent with that SL. But the result in body lengths
depends on an SL I could not check, and moves between 0.90 and 1.20 SL across a plausible SL range.

**Lift ≤ 31 % of weight:** `unknown`. I lack the lift coefficient, the planform area and the mass, and the
question does not give how they were obtained. I did not re-derive this figure.

## Comparison with the recorded value

The recorded inputs are visible only in the question text: 0.84 m/s from Danos & Lauder, and 1.03 SL.

- The arithmetic from 0.84 m/s to 3.60 cm is reproduced, and gives 1.03 SL if SL ≈ 3.5 cm: **consistent**.
- The primary-source input (0.84 m/s) could not be checked: **CANNOT TELL**.

Because the claim's key point is that a *second independent source* gives 0.84 m/s, and I could not read
that source, I cannot confirm or refute the claim.

To unblock this, allow `journals.biologists.com` (it currently gets a Cloudflare challenge) or `sites.harvard.edu`
in the session's network settings, then read Table 1 for the 1 mPa s maximum centre-of-mass velocity and
the fish SL.

```swarm-replication
{"claim_id": 141, "my_value": "unknown (Danos & Lauder 2012 full text not accessible; conditional on v=0.84 m/s from the question, h=v^2/2g=3.60 cm = 0.90-1.20 SL for assumed SL 3-4 cm)", "agrees": null,
  "note": "Only the abstract was readable and it gives no velocity or body length, so the 0.84 m/s input cannot be checked; the downstream arithmetic is consistent with 1.03 SL only if SL is about 3.5 cm."}
```
