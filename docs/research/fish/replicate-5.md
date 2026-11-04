# Replication 5 — Reynolds number and maximum lift coefficient (CL_max) for a 0.4 g zebrafish glider

Claim under test, as it was given to me (with the answer removed): *"Reynolds number is pinned
at ~2e3–4e3 by body weight, so CL_max is probably <= 0.6; the value at that Re is unknown."*

**Method and independence.** I derived both halves myself before looking for the recorded
result. The inputs file `zebrafish-glide-physics.md` is not on this branch. It is on
`origin/claude/zebrafish-glide-physics-j176og`. From it I read only the input rows (mass,
gravity, ν, and the definition Re = Vc/ν), using a grep that excluded every line mentioning a
lift coefficient. While doing so I saw that file's Section 1 heading text: "The Re is pinned by
weight, not by speed (inference, derived here)". I stopped there and did not read that
section's working until my own derivation below was finished (Section 3).

Read-levels: full-text | abstract | listing | search-summary | could-not-access.

**Network scope.** This session could reach arxiv.org and the web search tool. It could NOT
reach cob.silverchair.com, which hosts the J. Exp. Biol. PDFs (Kesel 2000; Wakeling &
Ellington 1997), aero-comlab.stanford.edu, or www2.irb.hr. All three failed with DNS
"ENOTFOUND", so they are `could-not-access`.

---

## 1. Reynolds number (calculated, not observed)

Inputs:

| symbol | value | source | read-level |
|---|---|---|---|
| m | 0.4 g = 4.0e-4 kg | `zebrafish-glide-physics.md`, input table ("given in brief") | full-text (input row only) |
| g | 9.81 m/s² | standard | — |
| ρ_air | 1.2 kg/m³ | standard, sea level, ~20 °C | — |
| ν_air | 1.5e-5 m²/s | standard; same value used in the inputs file | — |
| AR | 3–8 (swept) | my assumption; no fin geometry was retrieved | — |
| C_L | 0.4–1.2 (swept) | my assumption | — |

Derivation:
- In a level, shallow glide, lift equals weight: W = ½ρV²·S·C_L.
- The wing area is S = AR·c², where c is the chord.
- Solving for speed: V = √(2W / (ρ·AR·c²·C_L)).
- Substituting into Re = V·c/ν, the chord cancels:

  **Re = (1/ν)·√(2W / (ρ·AR·C_L))**

So once AR and C_L are fixed, Re depends only on weight. Flying faster forces a smaller wing,
which leaves Re unchanged. This is my inference, derived from the algebra above.

Arithmetic, starting from W = 4.0e-4 × 9.81 = 3.924e-3 N:

| AR | C_L 0.4 | 0.6 | 0.8 | 1.0 | 1.2 |
|---|---|---|---|---|---|
| 3 | 4,922 | 4,018 | 3,480 | 3,113 | 2,841 |
| 5 | 3,812 | 3,113 | 2,696 | 2,411 | 2,201 |
| 8 | 3,014 | 2,461 | 2,131 | 1,906 | 1,740 |

Check of one cell (AR 5, C_L 0.6):
- 2W/(ρ·AR·C_L) = 7.848e-3 / 3.6 = 2.180e-3
- √(2.180e-3) = 0.04669
- 0.04669 / 1.5e-5 = 3,113

**My value: Re ≈ 1.7e3–4.9e3 (calculated) over AR 3–8 and C_L 0.4–1.2. For C_L 0.6–1.0 it is
1.9e3–4.0e3.** The "~2e3–4e3" in the claim holds.

One caveat on "pinned". Re scales as W^½·AR^-½·C_L^-½, so it is pinned only once AR and C_L
are chosen. It moves by a factor of about 2.8 across the swept range. A heavier glider, for
example one carrying the membrane's own added mass, raises it as √W.

## 2. CL_max at Re ≈ 2e3–4e3: what the retrieved literature says

All of these are measurements by the cited authors, as reported by the source named. None is
my own observation.

| # | Source | Configuration | Re | CL_max reported | read-level |
|---|---|---|---|---|---|
| L1 | Holden, Socha, Cardwell & Vlachos (2014) *J. Exp. Biol.* 217:382, as described by Krishnan, Socha, Vlachos & Barba, arXiv:1309.2969 | Flying-snake body cross-section (thick, bluff), water tunnel | 3,000–15,000 | "a maximum CL between 1.1 and 1.9, increasing with Reynolds number"; the spike to 1.9 appears at Re ≥ 9,000 | full-text of the citing arXiv paper; Holden itself is search-summary |
| L2 | Wakeling & Ellington (1997) *J. Exp. Biol.* 200:543 | Isolated real dragonfly and damselfly wings, steady flow | 700–2,400 | 0.93 in free glides; 1.07 (and 1.15, per a different summary) in wind-tunnel tests | search-summary; the 1.15 figure was **not confirmed**; PDF could-not-access |
| L3 | Sunada, Sakaguchi & Kawachi (1997) *J. Fluids Eng.* 119:129 | 15 sections: flat plates, NACA 00xx, cambered plates, corrugated | 4,000 | Best is a 5% cambered plate, CL_max = 1.06 at α = 8°, said to be "higher by 100–150% than the flat plate and G625" | search-summary. The summarizer could not confirm the sentence was Sunada's own, nor whether "100–150%" refers to CL_max or L/D |
| L4 | Kunz (2003) thesis; Kunz & Kroo (2001) | 2-D CFD, Re 1,000–6,000 | 1e3–6e3 | Qualitative only: "maximum lift increases with decreasing Reynolds number" | search-summary; no numbers retrieved |
| L5 | Fujita & Iima, arXiv:2503.12039 | Literature review inside a CFD paper | O(10³) | Qualitative only: corrugated wings may perform well at Re ≈ O(10³); several studies find them no better than flat wings | full-text (pdftotext) |

**The sources disagree, and I am keeping that disagreement visible.**
- L1 and L2 are measured steady-flow values at or near this Re. They sit at about **0.9–1.1**.
- L3 is the only flat-plate datum. Taken literally, "100–150% higher" gives CL_max,flat =
  1.06/2.5 to 1.06/2.0 ≈ **0.42–0.53**. This is my arithmetic on a search summary whose
  attribution is uncertain. If the percentage refers to L/D rather than CL_max, the figure is
  void.

**My value (inference from the table above, not a measurement of any fish fin):**
- **CL_max ≈ 1.0 (plausible range 0.9–1.1)** for a thin wing with some camber or corrugation at
  Re ≈ 2e3–4e3. This rests on two independent measured lines, L1 and L2.
- **CL_max ≈ 0.4–0.55, weakly supported,** for an ideal flat plate. This rests on L3 alone, and
  L3 is ambiguous.
- **Overall: CL_max ≈ 0.5–1.1, best estimate ~1.0 for a cambered membrane.**

A ray-supported fin membrane under load would probably camber, which places it nearer the upper
row. That is my inference; no fin data was retrieved. For a pectoral fin itself, no
measurement at this Re was found: **unknown**.

Further caveats:
- L2 comes from 3-D wings but at lower Re (700–2,400).
- L1 is a thick bluff section, not a membrane.
- None of these is a low-aspect-ratio fish fin. Low aspect ratio would usually reduce the
  usable 3-D C_L below the section CL_max.

**Scope of the negative searches.** Six standard and extended web searches targeted Sunada
1997, Okamoto 1996, Kesel 2000, Kunz & Kroo, Wakeling & Ellington, and generic "flat plate
CL_max Re 1e3–1e4" queries. None of them returned a numerical flat-plate CL_max at Re 2e3–4e3
that I could read at full text. arXiv:2605.19468 is full-text but reports only CL/CD optima,
not CL_max.

## 3. Comparison with the recorded value (read only after Sections 1–2 were written)

The recorded document (`zebrafish-glide-physics.md` on `origin/claude/zebrafish-glide-physics-j176og`)
contains these points:
- **Re:** "Re = V·c/ν = √(2W / (ρ·C_L·AR)) / ν, with V cancelling out". It gives Re of 1,906–4,018
  for C_L 0.6–1.0 (calc). This is the same formula and the same numbers as mine (Section 1, AR 3–8).
  Agreement on arithmetic is expected, since the inputs are identical. **AGREE.**
- **CL_max:** the document says the value at Re ≈ 3e3 for a fish-fin-like membrane is
  **unknown**. It uses C_L = 0.6 as the working value and C_L = 1.0 as "an optimistic
  sensitivity case (cambered or corrugated membrane, unproven)".

My verdict on each part:
- **"The value at that Re is unknown" (for a fin):** AGREE. I also found no fin measurement.
- **"CL_max is probably ≤ 0.6":** DISAGREE as a statement of probability.
  - The two measured steady-flow sources I could retrieve near this Re (L1, L2) give about
    0.9–1.1.
  - Only an ambiguous search summary (L3) supports ≈0.5, and only for a flat plate.
  - 0.6 is defensible as a deliberately *conservative* design value. It is not the likely
    value for a cambered membrane, and the recorded "optimistic" case of 1.0 matches my
    central estimate.

The disagreement affects the conclusion. At C_L ≈ 1.0, the required wing area falls by a factor
of 1/0.6 ≈ 1.67 relative to the C_L 0.6 tables (calculated).

```swarm-replication
{"claim_id": 5, "my_value": "Re 1.9e3-4.0e3 (calc, C_L 0.6-1.0, AR 3-8); CL_max ~1.0 (0.9-1.1) for a cambered/corrugated thin wing, ~0.4-0.55 for a flat plate (weak, one ambiguous source); fin value unknown", "agrees": false, "note": "Re pinning reproduces exactly, but measured steady CL_max near Re 3e3 (snake section 1.1, dragonfly wings 0.93-1.07) argues CL_max is more likely ~1.0 than <=0.6, which holds only for a flat plate on weak evidence."}
```
