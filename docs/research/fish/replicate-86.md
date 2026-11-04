# Replication 86 — Reynolds number of a 0.4 g gliding zebrafish, and CL_max at that Re

**Claim under test, as I reconstructed it.** The task text gave only "Replication" and pointed at
`replicate-5.md` on branch `claude/zebrafish-glide-replication-ptg7f5`. I read that file's first
~40 lines to find the question. That excerpt contained:
- the claim, "Reynolds number is pinned at ~2e3–4e3 by body weight, so CL_max is probably ≤ 0.6";
- its input table (m = 0.4 g, ν = 1.5e-5 m²/s, AR 3–8, C_L 0.4–1.2);
- the start of its method (lift = weight, S = AR·c²).

I stopped reading at the line "the chord cancels", before its result. **Independence caveat:**
I had already seen the inputs and the shape of the method, so my Re arithmetic is not
independent in method. It is only an independent check of the algebra and the arithmetic.

Read-levels: full-text | abstract | listing | search-summary | could-not-access.

## 1. Reynolds number (calculated, not observed)

| symbol | value | source | read-level |
|---|---|---|---|
| m | 0.4 g = 4.0e-4 kg | `replicate-5.md` input table (which cites `zebrafish-glide-physics.md`, "given in brief") | full-text (input rows) |
| g | 9.81 m/s² | standard | — |
| ρ | 1.2 kg/m³ | standard sea-level air | — |
| ν | 1.5e-5 m²/s | standard air, ~20 °C | — |
| AR | 3, 5, 8 | assumption; no fin geometry measured | — |
| C_L | 0.4, 0.6, 0.8, 1.2 | assumption | — |

Derivation:
- Steady glide, lift equals weight: mg = ½ρV²·S·C_L, with S = AR·c².
- So V·c = √(2mg / (ρ·AR·C_L)). The chord cancels.
- Therefore Re = √(2mg / (ρ·AR·C_L)) / ν.

Arithmetic:
- mg = 4.0e-4 × 9.81 = 3.924e-3 N.
- 2mg/ρ = 6.54e-3 m⁴/s².

Two worked cases:
- AR = 3, C_L = 1.2: 6.54e-3 / 3.6 = 1.817e-3. The square root is 0.04262 m²/s, and dividing by ν gives Re = **2,841**.
- AR = 8, C_L = 1.2: 6.54e-3 / 9.6 = 6.81e-4. The square root is 0.02610, and dividing by ν gives Re = **1,740**.

Full sweep, all values calculated in Python:

| AR \ C_L | 0.4 | 0.6 | 0.8 | 1.2 |
|---|---|---|---|---|
| 3 | 4,922 | 4,018 | 3,480 | 2,841 |
| 5 | 3,812 | 3,113 | 2,696 | 2,201 |
| 8 | 3,014 | 2,461 | 2,131 | 1,740 |

**My value: Re ≈ 1.7e3–4.9e3 (calculated), central value ~3e3.** Re scales as m^½ and as (AR·C_L)^-½,
so the assumed geometry changes it by a factor of only about 2.8 across the sweep. That is the
sense in which weight "pins" Re. This is my inference from the formula.

## 2. CL_max at Re ≈ 3e3

- Web search, "maximum lift coefficient flat plate airfoil Reynolds number 4000 measured" (read-level: search-summary). It returned no numerical flat-plate CL_max at Re 2e3–5e3. It mentioned a NACA 0012 result of CL_max 0.455→0.59 with reduced turbulence, but at higher Re. That result is not applicable.
- Web search, "Sunada 1997 … Re 4000" (read-level: search-summary). It found the bibliographic record: Sunada et al. 1997, *J. Fluids Eng.* 119(1):129–135. The abstract excerpt says leading-edge vortices dominate at this Re and that planform matters little. **It gave no CL_max number.** Full text: could-not-access (not attempted beyond search; ASME is paywalled).
- Scope of the negative: two standard web searches only. I fetched no primary PDF.

**My value for CL_max: unknown.** I found no number from a primary source. I will not assert that it is ≤ 0.6, or anything else.

## 3. Comparison with the recorded value (read only after Sections 1–2)

I then read the rest of `replicate-5.md`. Its recorded values:
- Re ≈ 1.7e3–4.9e3 over AR 3–8 and C_L 0.4–1.2, and 1.9e3–4.0e3 for C_L 0.6–1.0.
- CL_max ≈ 1.0 (0.9–1.1) for a cambered or corrugated thin wing, which it cites to snake and dragonfly measurements.
- CL_max ≈ 0.4–0.55 for a flat plate, which it bases on a Sunada search summary it calls ambiguous.
- The CL_max ≤ 0.6 half of the claim was rejected (DISAGREE).

- **Re: AGREE.** My table reproduces 1,740–4,922 exactly. My C_L 0.6 / AR 3 cell (4,018) matches its upper bound. Caveat: the inputs were identical and the method was seen in advance, so this agreement is weak evidence. It confirms the arithmetic, not the modelling.
- **CL_max: CANNOT TELL.** I could not retrieve the primary measurements it relies on. My Sunada summary contains no CL_max figure, so I can neither confirm nor refute its 1.0 or its 0.4–0.55.

```swarm-replication
{"claim_id": 86, "my_value": "Re 1.7e3-4.9e3 (calculated; AR 3-8, C_L 0.4-1.2, m 0.4 g, nu 1.5e-5 m^2/s); CL_max at that Re unknown", "agrees": true, "note": "Re arithmetic reproduces the recorded 1.7e3-4.9e3 exactly from identical inputs (weak independence); the CL_max half could not be checked because no primary low-Re lift data were retrieved."}
```
