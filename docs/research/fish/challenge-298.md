# Challenge 298: adversarial review of S5-D-D (AR convention factor k)

**Date:** 2026-11-04. **Status:** desk review. No experiment was run. Every number I give below is
**calculated** by me in [`challenge-298_calc.py`](challenge-298_calc.py) (`python3 -I challenge-298_calc.py`)
from carried-over inputs, unless the sentence says otherwise.

**Claim under review** (S5-D-D, `claude/s5-d-sensitive-input-ol0bzg`, `docs/research/fish/S5-D-deepen.md`,
which I read in full): S5-D's conclusion stands, but its bars were in Fish 1990's AR convention, which is
2.0–2.6× the single-fin semispan²/area that S5-D's protocol measures. So the bars fall from A0 ≥ 3.0 / 9.0 to
about A0 ≥ 1.1–1.5 (Fish envelope) and ≥ 4.3–5.7 (mean *Cypselurus*/*Exocoetus* single fin). k = 2.03–2.64.

**Verdict: SURVIVED.** I found no fault that changes the conclusion or the numbers beyond their stated
rounding. There are three caveats. They should travel with the numbers, but none of them breaks the claim.

---

## 1. Independent arithmetic

I did not reuse the author's script. I took the raw inputs from `origin/main`
`artifacts/print/design/{C-four-wing-glider,B-two-wing-glider}.json` (`biological_design_SI`, read in full).
Those inputs are:
- Table I span b and wing area S;
- Table IV pectoral share;
- the Table III fit at 0.1 kg;
- the design body width w at the pectorals.

I then recomputed one fin's area myself as A = share·S/2. I did not take the stored `pectoral_area_per_fin_m2`.

| | *Cypselurus* (C) | *Exocoetus* (B) | claim |
|---|---|---|---|
| A = share·S/2 (m²) | 0.0033790 | 0.0038345 | matches stored value |
| L = (b−w)/2 (m) | 0.12051 | 0.14737 | — |
| single L²/A | 4.298 | 5.664 | 4.30 / 5.66 ✔ |
| pair b²/(2A) | 11.152 | 13.575 | 11.15 / 13.58 ✔ |
| whole b²/S | 8.474 | 12.466 | 8.47 / 12.47 ✔ |
| k = Table III fit / single | 2.033 | 2.638 | 2.03 / 2.64 ✔ |
| Fish low-end bar 3.0/k | 1.476 | 1.137 | 1.14–1.48 ✔ |
| Park & Choi bar 9.0/k | 4.43 | 3.41 | 3.4–4.4 ✔ |
| fan spread for the mean fin, θ = 2/AR | 26.7° | 20.2° | 27° / 20° ✔ |
| fan spread for the Fish bar | 77.7° | 100.8° | 78–101° ✔ |

The α = 1 variants also check: 1.14/1.74 = 0.65, 1.48/1.74 = 0.85, 4.30/1.74 = 2.47 and 5.66/1.74 = 3.25.
All of them reproduce.

## 2. Proxy check

- **Threshold side.** The quantity that matters is the AR of an individual flying-fish fin in the same
  convention as S5-D's measured A0. S5-D §3a, which I read on `claude/deepen-s5-pectoral-fin-ajxurw`, defines
  that span as *"base to farthest tip, perpendicular to the base"*, i.e. a perpendicular semispan. The claim's
  proxy is the design's (b−w)/2 with one fin's area, and it is the **same** quantity. I had suspected the
  protocol measured a leading-ray length, which would have made k ≈ 1 the right comparison. It does not, so
  that line of attack fails.
- **Fish's side remains a proxy.** k is inferred from two separate regressions (Table III and Table I) taken
  at one mass. It is not read from Fish's Methods. The author says so (caveat 1). I tried to read Fish 1990
  and could not: `digitalcommons.wcupa.edu` was refused by the proxy (HTTP CONNECT 403). For me the source is
  **could-not-access**, and every Fish value above is carried over.
- **Scope of "flying-fish status".** This is my inference, not the author's claim. S5-D explicitly reduces
  "planform" to AR (scale-free). The same design JSONs record mean flying-fish pectoral length/SL of 0.59
  (C) and 0.71 (B). These are derived values. S5-D's reachable span is 0.36 SL. So the reachable fin would
  be short relative to body length whatever A0 is. That is a span/body-scale question, which S5-D
  deliberately left out of "planform", so it does not falsify the claim as scoped. But "status depends
  entirely on A0" holds only under that scoping, and only under α ≈ 2. The author does state the α = 1 bars.

## 3. Hidden assumption, relaxed: body width w at the pectorals

The single-fin AR, and therefore k and every improved bar, depends on w. w is a `design_assumption`
derived from an assumed density of 1025 kg/m³ and an aesthetic body profile; it was not measured. The
author lists it in `depends_on` but does not propagate it. I relaxed it:

| w scaled by | k (Cyp) | k (Exo) | Fish bar 3.0/k | mean single-fin bar |
|---|---|---|---|---|
| 0 (unphysical floor) | 1.57 | 2.20 | 1.36–1.91 | 5.58 / 6.79 |
| 0.5 | 1.78 | 2.41 | 1.25–1.69 | 4.92 / 6.21 |
| 1.0 (claim) | 2.03 | 2.64 | 1.14–1.48 | 4.30 / 5.66 |
| 1.5 | 2.35 | 2.91 | 1.03–1.28 | 3.72 / 5.14 |

The elasticity of single-fin AR with respect to w is −0.28 (*Cypselurus*) and −0.19 (*Exocoetus*). So a
10% error in w moves the bars by only about 2–3%. Even with w = 0, k stays ≥ 1.57, so **k = 1 (S5-D's
implicit value) is excluded for every w ≥ 0**. The direction and rough size of the correction (about ×2)
are robust. The three-figure bars (4.30, 5.66) carry an unstated uncertainty of roughly ±10–15% for a ±50%
error in w. The ±50% is my sensitivity choice, not an estimate of the true w error; the true error is
`unknown`. This is a precision caveat, not a break.

## 4. Evidence level

The claim records evidence level **derived**, value n/a. That is honest:
- k is a ratio of carried-over fitted means;
- A0 is stated as `unknown`, not estimated;
- the Fish 1990 read-level (could-not-access to the author, carried over as full-text from the project's
  earlier pdftotext read) is disclosed.

The phrase "Fish 1990's convention, which is 2.0–2.6×" reads more like a fact than an inference. The body
of the note calls it a calculated inference, though, so I do not count it as a defect.

## 5. Counter-examples and other regimes

- **Pure doubling convention.** Wainwright et al. 2002 reportedly multiply single-fin AR by two
  (search-summary, carried over; not re-read by me). Under that convention k = 2 exactly, and the Fish bar is
  3.0/2 = **1.50**. That is 0.02 above the claim's 1.48 upper end, but it sits inside the headline's "about
  1.1–1.5". So it is not a counter-example.
- **Mass dependence of k.** The Fish 3.0 minimum is a *Cypselurus* individual of unknown mass, and k was
  evaluated at 0.1 kg. The project's source card records that Fish's Fig. 3 shows no significant AR–mass
  correlation (carried over). If the convention is definitional (doubling), k does not depend on mass. If k
  is instead an artefact of the regressions, it could vary with mass, which I cannot test without the
  Table I exponents. I did not find them in the design JSONs (`biological_design_SI`, read in full) or in
  the source-card fields I grepped. They are `unknown` to me.
- **Genus disagreement.** k differs between the genera (2.03 vs 2.64), and no single convention fits both
  genera. The claim keeps this as a range rather than averaging it, which is correct.
- **Literature search.** I found no published single-fin zebrafish pectoral AR that would let A0 be tested
  against the bars. My search was limited to the repo branches named above plus one attempted fetch of Fish
  1990, which was refused. I ran no new literature search for A0 because the author's 7 Europe PMC queries
  and 2 web searches already cover that, and I had nothing new to add.

## Sources and read-levels

- S5-D-D note and calc, `claude/s5-d-sensitive-input-ol0bzg`: **full-text** (repo).
- S5-D note, `claude/deepen-s5-pectoral-fin-ajxurw`, `docs/research/fish/S5-deepen.md`: **full-text** for §§0–3a (repo).
- `origin/main` `artifacts/print/design/C-four-wing-glider.json` and `B-two-wing-glider.json`: **full-text**
  for `biological_design_SI` (repo).
- `origin/main` `data/research/flying-fish-source-cards.json` and `docs/printing.md`: **listing** (grep of
  AR passages only).
- Fish FE 1990, *J Zool Lond* 221:391–403: **could-not-access** (WCUPA host refused by the proxy). All values
  are carried over.
- Wainwright et al. 2002: **search-summary**, carried over from the author; I did not access it.

```swarm-challenge
{"claim_id": 298, "outcome": "survived", "reason": "Independent recomputation from the design JSON inputs reproduces k = 2.03-2.64 and every improved bar, S5-D's protocol measures the same perpendicular-semispan quantity the claim assumes, and relaxing the unmeasured body width (elasticity -0.19 to -0.28, k >= 1.57 even at w = 0) moves the bars only ~10-15% without restoring k = 1.", "corrected_value": null, "depends_on": ["Fish 1990 Table I span and wing-area fits at 0.1 kg (carried over via origin/main artifacts/print/design B and C JSONs; Fish 1990 could-not-access)", "Fish 1990 Table IV pectoral share 0.7599 / 0.9183 (carried over)", "Fish 1990 Table III AR fit at 0.1 kg 8.74 / 14.94 and low end 3.0 (carried over)", "design assumption: body width at pectorals 0.0335 / 0.0279 m (unmeasured; sensitivity tested, elasticity -0.28 / -0.19)", "S5-D section 3a protocol: span measured base to farthest tip perpendicular to the base", "assumption: Fish's individual-fin AR convention is constant across fish mass (Fig 3 no AR-mass correlation, carried over)", "S5-D premise alpha ~ 2 and its fan model sector AR = 2/theta", "unknown: wild-type adult zebrafish pectoral AR A0"]}
```
