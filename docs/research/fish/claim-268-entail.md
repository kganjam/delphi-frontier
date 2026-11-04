# Claim 268 — entailment to organ and behaviour scales

**Source claim (organism scale, evidence: derived):**
> THRUST PASSES: leaving the water cuts body drag by 816x -- exactly the water/air density
> ratio, 1000/1.225 -- from 4.6 mN to 8 uN, and burst-calibrated lobe thrust (1.1-3.4 mN)
> exceeds total drag 3-40x. Speed genuinely rises, doubling in ~10 strokes at 52 Hz

The claim is about the flying-fish (Exocoetidae) **taxi**: the trunk is airborne while
the lower caudal lobe stays in the water and beats.

**Bottom line.** One constraint is **unsatisfiable**: the momentum budget (C4). The claim's
own thrust ceiling (≤ 3.4 mN net) cannot double the speed of any measured flying fish at a
measured taxi speed within ~10 strokes. The shortfall is a factor of ~8 for the smallest
specimen Fish (1990) measured, using the *slowest* reported taxi acceleration. The
claim's numbers only hold together for a body with m·U₀ ≤ 6.5×10⁻⁴ kg·m/s (for example
≤ 65 mg at 10 m/s). The structural requirement (C1) and the timescale (C3) are satisfied.
The beat-frequency range (C2) and the power budget (C5) are **open**.

## Sources and read-levels

| # | Source | Read-level | Used for |
|---|---|---|---|
| S1 | Fish, F. E. (1990). Wing design and scaling of flying fish with regard to flight performance. *J. Zool., Lond.* 221, 391–403. PDF from health-sciences.wcupa.edu | **full-text** (text layer of a scanned PDF) | specimen masses; hypocaudal lobe share; taxi speeds and distance (compiled from older literature) |
| S2 | Davenport, J. (1994). How and why do flying fish fly? *Rev. Fish Biol. Fish.* 4, 184–214 | **search-summary** (abstract text quoted by a search engine; data.zhenzhi.com unreachable) | "tail beats … at up to 50 beats s⁻¹" |
| S3 | bioRxiv 10.1101/765560, "Why does a flying fish taxi on sea surface before take-off? A hydrodynamic interpretation" (unreviewed preprint) | **search-summary**; full text **could-not-access** (HTTP 429 on 4 attempts) | 50–70 strokes s⁻¹ (as summarised); simulated 350 W → 16.5 m/s |
| S4 | APS March Meeting 2024 abstract, "Flying fish taxiing on the water's surface" | **search-summary**; page **could-not-access** (host not resolvable from this session) | 13.5 Hz tail slapping |
| S5 | Edgerton & Breder (1941), *Zoologica* 26, 311–314 | **listing** (archive.org / biostor not reachable) | not used for numbers |
| S6 | Park & Choi (2010), *J. Exp. Biol.* 213, 3269–3279 | **listing** | not used; specimen masses not obtained |

Hosts this session could not reach: archive.org, en.wikipedia.org, typeset.io,
meetings-archive.aps.org, bamlab.princeton.edu, data.zhenzhi.com. biorxiv.org returned HTTP 429.

### Key measured or literature numbers (S1, verbatim)

- "Specimens examined in this study range in mass (M) from 0.003 to 0.53 kg" (199
  specimens across six genera). This is **measured** by the author.
- "The mean percentage of the caudal fin composed of the hypocaudal lobe from the pooled
  data for all genera of flying fish is 63.1 ± 0.5." This is **measured**.
- "During the taxi, the elongated hypocaudal lobe of the caudal fin continues to remain in
  the water and generate thrust increasing speed for take-off from 10 to 16-20 m/s
  (Shoulejkin, 1929; Mills, 1936a; Edgerton & Breder, 1941; Franzisket, 1965; Aleyev,
  1977). The average taxi is 9 m (Hubbs, 1933)." These are **literature** values: Fish
  compiled them from older observations, and I have not read those primary sources.
  Fish's sentence does not say whether 10 m/s is the speed at the start of the taxi or
  at emergence. I read it as the speed at the start of the taxi. That reading is my
  inference.

## Derived quantities (my calculations, not observations)

- The claim's doubling time is 10 strokes ÷ 52 Hz = **0.19 s**.
- Taxi duration from S1: 9 m at a mean speed of 13–15 m/s gives **0.60–0.69 s**, which
  is 31–36 strokes at 52 Hz. This assumes roughly uniform acceleration.
- Mean taxi acceleration from S1: (6–10 m/s) ÷ (0.60–0.69 s) gives **8.7–16.7 m/s²**.
- The claim's own impulse ceiling: F_net ≤ 3.4 mN acting for 0.19 s gives
  Δ(mU) ≤ **6.5×10⁻⁴ kg·m/s**.

Side note at the organism scale, not one of the constraints: the 816x ratio equals
ρ_w/ρ_a only if the drag coefficient is the same in both media at the same speed.
Kinematic viscosity is about 15x higher in air than in water (standard property values),
so Re drops about 15x, and a friction-dominated C_D will rise. "Exactly the density ratio"
is therefore a modelling assumption, not a result.

## Constraints

### C1 — organ · existence — **satisfied**
*A propulsor must exist that stays immersed and makes thrust while the trunk is airborne.*
S1 measured an elongated hypocaudal (lower) lobe that makes up 63.1 ± 0.5 % of caudal-fin
area, with no significant difference among the six genera. S1 also states, citing older
observers, that this lobe "continues to remain in the water and generate thrust" during
the taxi. The anatomy is measured. The thrust role is the author's claim, based on
literature.

### C2 — organ · range — **open**
*The immersed propulsor must be able to sustain a beat frequency of about 52 Hz.*
The sources disagree, and I could reach each of them only through a search summary:
- S2: "up to 50 beats s⁻¹". On this figure, 52 Hz is slightly *above* the reported
  maximum.
- S3: 50–70 strokes s⁻¹. This range contains 52 Hz.
- S4: 13.5 Hz, which is about 4x lower.

These figures may describe different species, sizes or temperatures. S3 is summarised as
mentioning a ~25 °C Caribbean context. I have not averaged them. No source was read at
full text, so I am not marking this satisfied. Nothing I read contradicts 52 Hz
outright: S2's "up to 50" is a reported ceiling within ~4 % of the value. To close this,
read S2 and S3 in full, along with the primary high-speed film records they cite.

### C3 — behaviour · timescale — **satisfied** (derived from literature)
*The speed-doubling time must be no longer than the duration of the taxi.*
The claim needs 0.19 s. The taxi duration derived from S1's 9 m mean distance is
0.60–0.69 s, so the requirement is met. There is a tension, which I have kept: S1 reports
a speed gain over the *whole* taxi of only 1.6–2.0x (10 → 16–20 m/s). The claim's rate,
a doubling in 0.19 s, implies an acceleration about 3–6x the derived mean (≈52 m/s² if
U₀ = 10 m/s). Sustained over a real taxi, it would overshoot the reported take-off speeds.
This is not a contradiction, because acceleration need not be uniform. But the claim's
rate sits above what the behavioural record implies.

### C4 — behaviour · conservation — **unsatisfiable**
*Momentum must balance. The impulse of (lobe thrust − total drag) over the taxi must equal
the body's change in momentum, m·ΔU, at measured masses and taxi speeds.*
- Required net force at measured scales (derived): F = m·a. The low end uses S1's smallest
  specimen (0.003 kg) and the lowest derived acceleration (8.7 m/s²), giving **26 mN**.
  The high end uses 0.53 kg × 16.7 m/s², giving 8.8 N.
- What the claim provides: net force ≤ 3.4 mN (thrust minus drag ≤ thrust).
- Even at the most favourable end (smallest measured fish, slowest reported acceleration),
  the requirement is **~8x** more than the claim's ceiling. The claim's own statement
  (doubling in 0.19 s at ≤ 3.4 mN) needs m·U₀ ≤ 6.5×10⁻⁴ kg·m/s. At the reported taxi
  speed of 10 m/s, that is m ≤ 65 mg, about **46x** below the lightest specimen in S1.

The measured numbers behind this are S1's masses (0.003–0.53 kg, the author's own
measurement) and taxi speeds of ≥ 10 m/s (S1 quoting Shoulejkin 1929, Edgerton & Breder
1941 and others). The contradiction does not depend on the drag model: it holds even with
drag set to zero.

Caveats, stated rather than softened:
1. The speed values are secondary. I read Fish's compilation, not the primary films.
2. The 3 g specimen may be below flight-capable size. S1 says >98 % of specimens over
   0.05 m could fly. Using any larger fish makes the shortfall worse.
3. My inference is that claim 268's model fish runs at a far lower speed or mass than real
   taxiing fish. This is consistent with a water-phase drag of only 4.6 mN, which I
   estimate is orders of magnitude below the drag on a centimetre-scale body at 10 m/s.
   That estimate is an order-of-magnitude calculation, not a measurement.

As stated, the claim ("thrust passes, speed doubles in ~10 strokes") is refuted from below
for flying fish at measured sizes and speeds. A rescaled version may still be internally
consistent, but it would then describe a body that is not a taxiing flying fish.

### C5 — organ · energetic — **open**
*The propulsive musculature must deliver mechanical power ≥ m·a·U during the taxi.*
Derived requirement from S1's numbers: a·U ≈ 8.7 × 10 = **87 W/kg** at the low end and
16.7 × 20 = **334 W/kg** of body mass at the high end. Per kilogram of muscle it is higher.
I have not compared this with a measured power output for fish axial or white muscle; I
did not search for one. S3 reports a **simulated** 350 W to reach 16.5 m/s. That figure
comes from a model, not an observation, and I read it only as a search summary. Under
the claim's own numbers (3.4 mN × U) the power would be trivially small. That small
number is exactly the momentum shortfall from C4 showing up as power.

## Machine-readable block

```swarm-entail
{"source_claim": 268, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "existence",
      "statement": "A propulsive surface must exist that remains immersed and generates thrust while the trunk is airborne",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "satisfied",
      "satisfied_by": "Elongated hypocaudal caudal lobe, 63.1 +/- 0.5% of caudal fin area pooled over six exocoetid genera; described as remaining in water and generating thrust during the taxi",
      "satisfied_evidence": "measured",
      "note": "Fish 1990 J Zool Lond 221:391-403 (full-text). Lobe area share measured by author; thrust role is author's statement citing Breder 1929, Hubbs 1933, 1936, Hertel 1966 (not read)."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The immersed propulsor must sustain a beat frequency of about 52 Hz",
      "quantity": "taxiing tail-beat frequency", "lo": 52, "hi": null, "units": "Hz",
      "status": "open",
      "satisfied_by": "Conflicting reports reached only via search summaries: Davenport 1994 'up to 50 beats/s' (52 Hz marginally above stated max); bioRxiv 10.1101/765560 '50-70 strokes/s' (contains 52); APS March 2024 abstract '13.5 Hz' (~4x lower)",
      "satisfied_evidence": "literature",
      "note": "All three at search-summary read level; bioRxiv full text could-not-access (HTTP 429), APS page could-not-access (host blocked). Sources disagree and were not averaged. Not marked satisfied because no full text was read."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "The speed-doubling time must not exceed the duration of the surface taxi",
      "quantity": "taxi duration", "lo": 0.19, "hi": null, "units": "s",
      "status": "satisfied",
      "satisfied_by": "Derived taxi duration 0.60-0.69 s (mean taxi 9 m at mean 13-15 m/s) exceeds required 0.19 s (10 strokes / 52 Hz)",
      "satisfied_evidence": "derived",
      "note": "Inputs from Fish 1990 (full-text) quoting Hubbs 1933 (9 m) and Shoulejkin 1929, Edgerton & Breder 1941 et al. (10 -> 16-20 m/s). Tension: whole-taxi gain is only 1.6-2.0x, so the claim's implied acceleration is ~3-6x the derived mean."},
    {"target_scale": "behaviour", "kind": "conservation",
      "statement": "Impulse of net propulsive force over the taxi must equal the body's momentum gain at measured body masses and taxi speeds",
      "quantity": "net force required to produce measured taxi acceleration", "lo": 0.026, "hi": 8.8, "units": "N",
      "status": "unsatisfiable",
      "satisfied_by": "Claim supplies net force <= 3.4 mN. Measured masses 0.003-0.53 kg (Fish 1990) times derived taxi acceleration 8.7-16.7 m/s2 require >= 26 mN even for the smallest specimen, ~8x the ceiling. The claim's own doubling in 0.19 s needs m*U0 <= 6.5e-4 kg m/s, i.e. m <= 65 mg at 10 m/s, ~46x below the lightest measured specimen",
      "satisfied_evidence": "measured",
      "note": "Masses: Fish 1990 own measurement (full-text). Taxi speeds >= 10 m/s: Fish 1990 compiling Shoulejkin 1929, Mills 1936a, Edgerton & Breder 1941, Franzisket 1965, Aleyev 1977 (primary sources not read). Holds even with drag = 0. Acceleration is derived from those values assuming uniform acceleration."},
    {"target_scale": "organ", "kind": "energetic",
      "statement": "Propulsive musculature must deliver mechanical power at least m*a*U during the taxi",
      "quantity": "mass-specific mechanical power", "lo": 87, "hi": 334, "units": "W/kg body mass",
      "status": "open",
      "satisfied_by": "Requirement derived from Fish 1990 speeds and taxi distance; not compared against any measured fish muscle power output (not searched)",
      "satisfied_evidence": "unknown",
      "note": "bioRxiv 10.1101/765560 reports a SIMULATED 350 W to reach 16.5 m/s (search-summary only). No search for measured axial or white muscle power was performed, so this is 'not looked', not 'looked and found nothing'."}
  ]}
```
