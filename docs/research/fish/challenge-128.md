# Challenge 128 — adversarial review of `[S23-D-D]` (EI_meas / caudal→pectoral ratio R)

Claim under review (source `harvest:s23-sensitive-input-melodp`, the doc is
`docs/research/fish/S23-D-deepen.md` and its calculator `S23-D-D-calc.py` on branch
`claude/s23-sensitive-input-melodp`, read at `full-text`):

> S23-D's weakest input is EI_meas (caudal fin standing in for the pectoral wing via an
> undeclared R = EI_pectoral/EI_caudal, silently set to 1). Flip threshold R* = 1.35
> (lenient, C=29), 2.80 (lenient, C=14), 33.8 (central, C=29), 70.1 (central, C=14).
> R ≤ 1 from the yellow perch ranking, so the margins become lower bounds and the
> conclusion stands, numerically unimproved at 1.353. Evidence: derived. Verdict: stands.

Date: 2026-11-04. **Every number in §1 and §4 is my computation, not an observation.**

**Outcome: WEAKENED.** The arithmetic checks out, and so does the R ≤ 1 bound. The defects
are a second hidden multiplier that the claim never names, which the R bound cannot cover,
and a mislabelled evidence level on the input that sets the lenient corner.

---

## 1. Arithmetic, redone independently

Inputs as stated: W = 0.4 g × 9.81 = 3.924×10⁻³ N. Two wings share it, so each carries W/2.
For a uniform-load cantilever, EI_req = (W/2)L²/(8·tol).

- central (L = 4 cm, tol = 10 %): EI_req = 1.962×10⁻³ × 1.6×10⁻³ / 0.8 = **3.924×10⁻⁶ N·m²**.
  Divided by 4×10⁻⁹ that gives S = 981.
- lenient (L = 2 cm, tol = 50 %): EI_req = 1.962×10⁻³ × 4×10⁻⁴ / 4 = **1.962×10⁻⁷ N·m²**.
  Divided by 5×10⁻⁹ that gives S = 39.24.
- R* = S/C works out to 70.07 and 33.83 at the central corner, and 2.803 and 1.353 at the
  lenient corner. **All four of the claim's values reproduce** (computed).
- Small point: C is rounded in the claim. E_target/E0 is 10/0.35 = 28.57, not 29, and
  5/0.35 = 14.29, not 14. With the unrounded values the lenient R* is 1.373 and 2.747. The
  rounding raises one threshold and lowers the other by about 2 %, which is not material.
- E0 flip at the lenient corner: E0* = E_target·EI_meas/EI_req = 10 GPa × 5×10⁻⁹ / 1.962×10⁻⁷
  = 255 MPa. This matches the parent.

## 2. Proxy check: is R the right correction, and is R ≤ 1 honest?

**Puri et al. 2018, J Exp Biol 221:jeb171777, PMC5868929. Read-level: `full-text`, fetched
for this review.** This is what the paper says, not my inference:
- The EI is a **whole caudal fin** value at positions along the proximal–distal axis. It is not
  per ray and not per unit width. The authors report "overall bending moments of
  1.5×10⁻⁹–4×10⁻⁹ N m²", with peak stiffness about 2–4 mm from fixation. The fins had 16–18
  rays, were 5–8 mm wide, and had ray diameters of 0.1–0.2 mm. The fish were AB wild type,
  6–12 months old.
- The paper does not mention the pectoral fin.
- **The Conclusions' 2–5×10⁻⁹ N·m² is not a measurement.** The authors got it by scaling
  published bluegill ray data and say it is "in reasonable agreement" with their measurements.

My inference: the claim's whole-fin framing of R is correct, because Puri's number is a
whole-fin number. Ray count also points to R < 1: zebrafish pectoral fins have 10–14 rays
(the claim's search-summary) against 16–18 caudal rays (Puri). That adds to Line A
(perch ray-level ranking). I also re-searched the yellow perch result (doi:10.1002/jmor.20831).
The search summary again attributed "dorsal, anal and caudal similar, intermediate between
the paired fins; pectoral least stiff" to Taft and colleagues (read-level `search-summary`; the
full text was not accessible). **The R ≤ 1 bound survives my attack.**

Two weaker points about R that I am recording but do not count as breaks:
- The perch ranking is per ray and may be confounded by ray length or size. The ray-count
  argument above points the same way for the whole fin, so this does not reverse the
  direction.
- The uniform-EI model uses the peak EI over the whole span. Rays taper (Puri: fin thickness
  falls from 200 to 40 µm), so the real effective EI is lower. That makes the gap larger, which
  is conservative for the conclusion.

**Search scope for a direct zebrafish pectoral EI:** web index, English, 2026-11-04, standard
mode, query `zebrafish pectoral fin ray bending stiffness measurement flexural rigidity`. It
returned labrid, bluegill and other-species work and no zebrafish pectoral measurement, which
agrees with the claim. `zendy.io` and `sites.harvard.edu` (the abstract and the Flammang 2013
PDF) returned `ENOTFOUND` and are `could-not-access`. Line B (Flammang 2013) is therefore still
at `search-summary`; I could not check it either.

## 3. The hidden assumption that carries the result: EI is passive

Both ancestors and the claim take the wing's working EI to be **R × (passive EI of an
anesthetized fish)**. Puri measured anesthetized animals with the peduncle held in foam. The
claim never asks whether a gliding fish holds its fin at that passive stiffness.

**Alben, Madden & Lauder, "The mechanics of active fin-shape control in ray-finned fishes,"
J R Soc Interface 4(13):243–256 (journal date 2006-11-28, often cited as 2007), PMC2359861.
Read-level: `full-text` via fetch-and-summarise, so treat the quoted figures as relayed.**
These are the authors' claims:
- The bilaminar hemitrich mechanism allows "a variation in ray stiffness over more than an
  order of magnitude depending on actuation at the bases of the fin rays."
- **Measured:** a stiffness ratio of about 12 between clamped bases and one hemitrich base
  free. This comes from a single bluegill (*Lepomis macrochirus*) pectoral fin ray, out of 24
  rays tested mechanically.
- **Modelled:** a factor of 4 to 100 across shear modulus values.

My inference: this introduces a second multiplier, A = EI_active/EI_passive ≥ 1. It is
independent of R, and the bound R ≤ 1 says nothing about it. The hemitrich architecture is
shared by lepidotrichia in general, so it applies to both fins. That means R stays as it is,
but the wing's working EI is R·A·EI_caud, and the margin is 1.353/(R·A) at the lenient corner.
The numeric value of A for a zebrafish pectoral fin holding a sustained glide load is
**`unknown`**. Alben's "free base" reference is not physiological, because an anesthetized fish
still has its hemitrichs attached through relaxed muscle and ligament. So 12 is an extreme
upper reference, not an estimate. A could plausibly be anywhere from 1 to about 12.

Relaxed recompute (computed, with R = 1 at its bound):

| A | central C=14 | central C=29 | lenient C=14 | lenient C=29 |
|---|---|---|---|---|
| 1 (claim's implicit value) | 70.1 | 33.8 | 2.80 | 1.353 |
| 1.35 | 51.9 | 25.1 | 2.08 | **1.002** (edge) |
| 2.8 | 25.0 | 12.1 | **1.001** (edge) | **0.48 FLIPS** |
| 12 (bluegill clamped/free, extreme) | 5.84 | 2.82 | **0.23 FLIPS** | **0.11 FLIPS** |

The central corner holds for every A up to 12. **The lenient corner flips once A > 1.35
(C=29) or A > 2.8 (C=14).** The claim says its conclusion is "intact" at every design corner.
That rests on A = 1, an assumption that is undeclared in the same way R was, and that has a
published measurement suggesting it could exceed the flip threshold. The difference is that
the measurement is from another species and another reference state.

This does not refute the claim. No zebrafish value for A exists, and R ≤ 1 pulls the other way:
if R is well below 1, it offsets part of A. The sign of R·A − 1.35 is therefore unknown. But
the claim's verdict at the lenient corner should be **indeterminate, not stands**. Its own
§5.3 already allows this reading for a reader who weights Line C differently.

## 4. Evidence-level check

- The claim's evidence tag `derived` is honest for R* and for the margins.
- **Defect, inherited from the ancestors but repeated here:** the lenient corner uses
  EI_meas = 5×10⁻⁹ N·m², which the calculator labels "measured, CAUDAL fin" and the
  `depends_on` list records as "measured in vivo". Puri's full text shows this upper value
  comes from scaling bluegill ray data. It is derived, not measured. The highest *measured*
  value is 4×10⁻⁹. With that value the lenient margin is **1.69 (C=29) and 3.50 (C=14)**
  (computed). So the mislabel made the claim *more* conservative and does not hurt its verdict.
  It is still a derived number presented as measured, and the floor rule counts that as a
  defect.
- **Overstatement:** the claim says R's 35 % tolerance is "far tighter than any other input in
  the chain". At the lenient corner every multiplicative input has the same 1.35× tolerance by
  construction, because the corner is the edge of every range. E0's headroom, for example, is
  0.35/0.255 = 1.37× (computed). R stands out because of its provenance (undeclared), not
  because its tolerance is numerically tighter. Ranking it "weakest" is a defensible judgment
  about evidence, but the numerical argument given for it does not support it.

## 5. Verdict

**WEAKENED.**

- **What survives:**
  - all four R* values (recomputed independently);
  - the whole-fin framing of R (Puri's EI is a whole-fin value);
  - the R ≤ 1 bound (perch ranking plus a ray count of 10–14 pectoral against 16–18 caudal);
  - the central-corner conclusion, which holds even with a 12× active-stiffening factor.
- **What breaks:**
  - "conclusion intact … at every design corner" depends on a second undeclared multiplier,
    active hemitrich stiffening A, being set to 1. A measured bluegill pectoral-ray contrast of
    about 12× (single specimen, against an unphysiological free-base reference) shows A could
    exceed the lenient flip thresholds of 1.35 and 2.8. The lenient corner is therefore
    **indeterminate**.
  - The claim's lenient input, 5×10⁻⁹, is mislabelled as measured.
- **What would settle it:** measure the same rig (Puri) on a zebrafish pectoral fin both
  anesthetized and with fin-base muscles actively recruited, or electrically stimulated. That
  gives R and A together.

## Sources

- `docs/research/fish/S23-D-deepen.md`, `S23-D-D-calc.py` @ `claude/s23-sensitive-input-melodp` — `full-text`.
- `docs/research/fish/S23-deepen.md` @ `claude/deepen-s23-actinotrichia-bhvko5` — `full-text` (searched for the inputs it uses).
- [Puri et al. 2018, J Exp Biol 221:jeb171777, PMC5868929](https://pmc.ncbi.nlm.nih.gov/articles/PMC5868929/) — `full-text` (fetch-and-summarise).
- [Alben, Madden & Lauder, J R Soc Interface 4:243–256, PMC2359861](https://pmc.ncbi.nlm.nih.gov/articles/PMC2359861/) — `full-text` (fetch-and-summarise).
- Yellow perch fin-ray stiffness, J Morphol doi:10.1002/jmor.20831; [SICB abstract](https://sicb.org/?p=17834); [UWM poster](https://dc.uwm.edu/uwsurca/2015/Poster2/90) — `search-summary`; zendy.io `could-not-access` (ENOTFOUND).
- Flammang et al. 2013 J Morphol — `could-not-access` (sites.harvard.edu ENOTFOUND); not evaluated.

```swarm-challenge
{"claim_id": 128, "outcome": "weakened", "reason": "The R* arithmetic and the R<=1 bound reproduce, but the claim's 'intact at every corner' depends on a second undeclared multiplier, active hemitrich stiffening A (measured ~12x clamped-vs-free in one bluegill pectoral ray, zebrafish value unknown), which flips the lenient corner for A>1.35 (C=29) or A>2.8 (C=14), so that corner is indeterminate; the lenient input 5e-9 N*m^2 is also a scaling estimate in Puri 2018, not a measurement.",
  "corrected_value": "lenient-corner margin = 1.353/(R*A) with R<=1 and A>=1 unknown (indeterminate); 1.69 if the top measured EI 4e-9 N*m^2 is used with R=A=1; central corner >= 2.8 for A<=12 (holds)",
  "depends_on": [
    "S23-D-D calculator inputs: m = 0.4 g, L = 2-4 cm, tol = 10-50 percent, C = 14 and 29, uniform-load cantilever EI_req = (W/2)L^2/(8 tol)",
    "Puri et al. 2018 J Exp Biol 221:jeb171777 (full-text): whole caudal fin EI 1.5e-9 to 4e-9 N*m^2 measured in anesthetized fish; 2e-9 to 5e-9 in the Conclusions estimated by scaling bluegill ray data; 16-18 caudal rays",
    "Alben, Madden & Lauder J R Soc Interface 4:243-256 (full-text via summary): measured ~12x ray stiffness ratio, clamped vs one hemitrich base free, single bluegill pectoral fin ray",
    "Assumption that the hemitrich active-stiffening mechanism is present in zebrafish pectoral lepidotrichia (inferred, not measured)",
    "Yellow perch ranking pectoral least stiff, caudal intermediate (doi:10.1002/jmor.20831, search-summary)",
    "Zebrafish pectoral ray count 10-14 (search-summary, inherited from S23-D-D)",
    "E0 >= 0.35 GPa and E_target 5/10 GPa, inherited from S23-D"
  ]}
```
