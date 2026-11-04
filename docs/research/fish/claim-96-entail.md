# Claim 96: what it requires at `tissue` and `organism`

**Source claim (scale `organ`, evidence `derived`):** *The single measured hemitrich-locking factor
(~12x, Alben, Madden & Lauder 2007, clamped 1.98 N/m vs one-base-free) closes a 2.1x gap with 5.7x
margin, so ACTIVE STIFFENING CAN CARRY THE LOAD. This is conditional on isometry holding and on fin
muscles achieving the excised-ray clamping factor in vivo.*

Single reader. **Nothing here was measured by me, and nothing was simulated.** Every number is tagged
*measured* (by the cited authors), *calculated* (by me, in
[`claim-96-entail_calc.py`](claim-96-entail_calc.py), run with `python3 -I`) or *assumption*.

## 0. Where the claim comes from

Claim 96 is the verdict of S26-D (`docs/research/fish/S26-deepen.md` on
`origin/claude/deepen-s26-active-stiffening-48xj8q`, read in full). It rests on the per-ray requirement
from S6-D (`S6-deepen.md` on `origin/claude/deepen-fin-ray-s6-cj2i2x`, read in full):

- The model is a uniform cantilever with `P = n·m·g/(2N)` and failure at δ/L > 0.10.
- The inputs are m = 0.10 kg, N = 14 rays per fin, L = 0.12 m and n = 1. **All four are assumptions.**
- The model puts **all** of the weight on the two pectoral fins.
- The result is EI_req = 6.3e-4 N m^2 per ray (calculated).

Claim 96 then scales a bluegill ray's passive EI (3.8e-6 N m^2) from 40.3 mm to 120 mm as L^4. That gives
3.0e-4 N m^2 (calculated). Multiplying by 12 gives the 5.7x margin.

The claim names its two conditions. The first is **isometry**, which lives at tissue scale (ray
cross-section). The second is **in-vivo muscular clamping**, which also lives at tissue scale (fin-base
muscle), and its duration is set at organism scale. The claim also inherits two organism-scale
assumptions from S6-D: the fish's geometry, and the load path. I entail all of these.

### Sources and read-levels

| Source | Used for | Read-level |
|---|---|---|
| Fish FE (1990) *J Zool Lond* 221:391-403, "Wing design and scaling of flying fish with regard to flight performance" | 199 specimens, 6 genera: allometric regressions, area partition, glide distance and speed | **full-text** (scanned PDF from health-sciences.wcupa.edu, OCR'd with `pdftotext`; I checked the table values against the paper's own prose, see C4) |
| Alben, Madden & Lauder (2007) *J R Soc Interface* 4:243, PMC2359861 | 12x ratio, model ratio vs G, G definition, n = 24 rays, bone ≈ 30% of ray thickness | **full-text via an automated page summarizer** (WebFetch). Not read line by line by me |
| S26-D, S6-D, S26 organ doc (repository branches above) | upstream numbers, including the Puri 2018 relay (1–2 mm bluegill ray diameter) and the Lauder SICB 10–15 mN figure | full-text (as committed). Their own read-levels carry over: Puri 2018 full-text; Lauder SICB abstract search-summary |
| Lou, Curtin & Woledge (2002) *J Exp Biol* 205:1585, dogfish red 142 kN m^-2, white 289 kN m^-2 | muscle stress | **search-summary** |
| Johnston & Salamonski (1986), blue marlin red 57, white 176 kN m^-2 (Ca2+-activated skinned fibres) | muscle stress | **search-summary** |
| Lauder group SICB abstract: 10–15 mN at the distal third for 100 µm hemitrich displacement; "nearly 12 times" | actuation force scale | **search-summary** |
| Cook Islands Biodiversity (Bishop Museum), *Cypselurus poecilopterus* pectoral i,14–15 | ray count | **search-summary** |
| Guinness World Records, 45 s flyingfish flight (NHK, Yakushima, 2008) | glide-duration upper bound | **listing** (search snippet only) |
| Flammang et al. 2013 *J Morphol* full text (sites.harvard.edu) | — | **could-not-access** (DNS blocked in this session) |
| FishBase species pages (fishbase.se) | — | **could-not-access** (DNS blocked in this session) |
| Park & Choi IUTAM 2007 proceedings (monash.edu) | — | **could-not-access** (DNS blocked in this session) |

The three hosts marked could-not-access have to be allowed in the session's network settings before
they can be read.

## 1. Constraints and checks

### C1 — `tissue`, spatial: the ray's cross-section must keep up with its length

**Requirement (calculated).** For a 12x lock to carry the load, the passive EI of a 120 mm ray must be
at least EI_req/12 = **5.3e-5 N m^2**.

- **From the 3.8e-6 bluegill baseline:** EI must rise ×13.8 over a ×2.98 length increase. So EI ∝ L^b
  needs **b ≥ 2.41**; isometry gives 4. At constant modulus (EI ∝ d^4), the ray diameter must grow
  **≥ ×1.93**. With Puri's 1–2 mm bluegill diameter, a 120 mm ray needs a base diameter **≥ 1.9–3.9 mm**.
- **From S26-D's own back-calculation of Alben's measurement:** the one-base-free value is 1.07e-6. On
  that baseline the requirement tightens to **b ≥ 3.57** and **d ≥ 2.6–5.3 mm**.

I preserve both baselines. They differ by 3.6x. The Flammang 2013 abstract value, 565e-6, would pass
with no lock at all. That disagreement (D1 in S26/S26-D) is still unresolved.

**Check.** I found no measured pectoral-ray diameter, second moment of area or EI for any exocoetid. I
also found no measured scaling exponent of ray EI or diameter against ray length in any teleost.

- Scope of the search:
  - my two web searches: "fin ray bending stiffness scaling with size allometry lepidotrichia
    cross-section diameter" and "flying fish Exocoetidae pectoral fin ray stiffness OR diameter OR
    micro-CT";
  - the upstream searches in S6-D (Europe PMC, 35 hits) and S26-D (two web searches).
- What the searches did return: within-fin variation (yellow perch, gar, sturgeon, coho salmon SICB
  abstracts, all search-summary), and a coho abstract noting that rays are "stiffer … than we would
  predict based on size". None of these is an exocoetid, and none gives an exponent.
- Fish 1990 (full-text) shows that Cypselurus wing **span** scales with **positive** allometry. The
  exponent is b = 0.375 (95% CI 0.364–0.387) against 0.33 predicted. That is a fin-planform measurement,
  not a cross-section. **My inference:** it says nothing about whether d keeps pace with L.

**What this finding is.** This is a case of *nobody has looked*: no one has measured it. It is not a
case of *people looked and found it small*. No measured number contradicts the requirement.
**Status: unsatisfied.**

### C2 — `tissue`, range: fin-base muscle must hold the hemitrich couple

When the bases are locked, the bending moment at the base is carried largely as an axial tension and
compression couple between the two hemitrichs. On the tension side, something must hold the hemitrich
base against the girdle. The claim says that thing is muscle.

**Requirement (calculated).**

- The base moment is M = P·L/2 = 2.1e-3 N m.
- Under isometry, the ray diameter at 120 mm is 3.0–6.0 mm. Taking the hemitrich centroid separation as
  0.7–1.0 of the diameter (bone is ~30% of the thickness, Alben 2007), the couple force is
  **F ≈ 0.35–1.0 N per ray**.
- This is an upper-end estimate. With a lock ratio of 12 rather than the model ceiling of ~100, the
  hemitrichs also carry part of M in their own bending.
- Measured fish muscle stress ranges from 57 kN m^-2 (marlin red, search-summary) to 289 kN m^-2
  (dogfish white, search-summary). At those stresses each ray needs **≥ 1.2 mm^2** of muscle
  cross-section in the best case and up to ~18 mm^2 in the worst case.
- Across 28 rays, that is **34–495 mm^2** of muscle, holding a **total tension of 10–28 N**. Body
  weight is 0.98 N, so this is **10–29 times body weight**.
- For scale, a different quantity: the bluegill actuation figure (10–15 mN per 100 µm, search-summary),
  scaled by L^2, gives only 89–133 mN.

**Check.**

- I found no measured cross-section, mass or force of exocoetid pectoral or fin-ray muscles.
- I found no EMG of any exocoetid fin muscle during a glide.
- Scope: my web searches for flying-fish pectoral myology and EMG, and for the 100 µm/10–15 mN source.
- What the searches did return: EMG in bluegill, perch, killifish and *Polypterus*. Hatchetfish
  (Gasteropelecidae) "flight" muscles (lecture notes, different family). None of these are exocoetids.

**What this finding is.** Again, *nobody has looked*. The number to compare against does not exist.
**Status: unsatisfied.** It is not unsatisfiable, because no measured muscle capacity falls below the
requirement.

**My inference, flagged as such:** a sustained per-ray tension of up to ~1 N, summing to tens of body
weights, is the strongest demand this claim makes. It is the first thing a dissection would test.

### C3 — `organism`, timescale: the lock must be held for a whole glide

**Requirement.** Muscular clamping must be sustainable at least as long as one glide.

- Fish 1990 (full-text) relays typical Cypselurus flights of **15–92 m** (Hubbs 1918; Aleyev 1977) and
  speeds of **10 to 16–20 m/s** (several sources).
- From those, a single glide lasts **~0.75–9 s** (calculated).
- Fish 1990 also says flight is extended by up to 12 successive glides, with a taxi between glides.
- Guinness (listing level) records a 45 s airborne flight.
- So the lock must be held for **≥ ~1–9 s**. In the extreme case it is **≤ 45 s**, unless the fish can
  relax the lock during the taxiing phases.

**Check.**

- I found no fibre-type, fatigue or endurance data for any exocoetid fin muscle.
- Other taxa: in notothenioids, slow fibres are the major component of the pectoral adductor profundis
  (search-summary). Goldfish pectoral adductors gain 23% more oxidative fibres when cold-acclimated
  (search-summary). Weakfish pectoral muscle is mainly white (search-summary).
- **My inference:** fibre-type composition varies by taxon, so it cannot be transferred to exocoetids.
- Scope: one web search on pectoral-fin muscle fibre types and isometric endurance, plus the flying-fish
  myology search in C2.

**What this finding is.** *Nobody has looked* in exocoetids. **Status: unsatisfied.**

### C4 — `organism`, spatial: the fish must have the geometry the requirement assumes

**Requirement.** A ~0.1 kg fish with ~14 load-bearing rays per pectoral fin, each about 0.12 m long.
Under isometry the margin scales as L^2, so the 12x lock still suffices for any L ≥ 0.12/√5.7 = 0.050 m,
and a longer ray helps (calculated): at L = 100, 120, 137 and 161 mm the margin is 3.9, 5.7, 7.4 and 10.2.

**Check (measured regressions, applied by me).**

- **Mass.** Fish 1990 measured flying fish from 0.003 to 0.53 kg (n = 199), so 0.1 kg is within the
  measured range.
- **Unit check.** The regressions give Danichthyes span = 0.622·M^0.310. At M = 0.53 kg this is 0.511 m,
  which matches the paper's prose ("0.51 m"). So the units are m and kg.
- **Lengths at 0.1 kg (calculated from the regressions):**
  - Cypselurus: SL = 203 mm, span = 275 mm, semispan = 137 mm.
  - Exocoetus: SL = 208 mm, span = 323 mm, semispan = 161 mm.
  - The semispan includes half the body width, which was not measured here. So the fin length is a
    little shorter. On that **assumption**, it comes out at ~0.12–0.15 m.
- **Davenport's ceiling.** Davenport (1992), relayed by S6-D at abstract level, says pectoral fin length
  is at most 78–79% of SL. That allows up to ~160 mm, which is consistent.
- **Ray count.** *C. poecilopterus* has pectoral i,14–15 (search-summary). That is consistent with N = 14
  for a single species. I did not establish the range across the genus.
- **Caveat.** Fin length is not the length of the longest ray. Ray length was not measured directly here.

**Status: satisfied**, with evidence *derived* (measured regressions applied at 0.1 kg).

### C5 — `organism`, conservation: per-ray load must not exceed what the margin covers

**Requirement.** Momentum balance in a steady glide requires total lift = n·m·g with n = 1. EI_req is
linear in the per-ray load. So the 5.7x margin holds as long as (pectoral share of weight) × n ≤ 5.7.

**Check.**

- S6-D gives the pectoral fins 100% of the weight. Fish 1990 (full-text) measured the pectoral fins at
  **76.0 ± 0.6%** of total wing area in Cypselurus and **91.8 ± 0.4%** in Exocoetus. The rest is pelvic
  fin.
- If lift is proportional to area (an **assumption**), the S6-D load is conservative by up to 1/0.76.
  The tolerable n then rises to 6.2–7.5 (calculated).
- Fish 1990 describes the glide path as "relatively flat", so a steady glide has n ≈ 1.
- **Not checked:** I found no measured load factor for take-off pull-up, turning or landing.

**Status: satisfied** for the steady glide. The evidence is *derived*: momentum balance plus a measured
area partition. Manoeuvring load factors are **open**: *nobody has looked*.

## 2. What the entailments say about the claim

**No constraint is unsatisfiable.** I found no measured number that contradicts any requirement, so the
claim is **not** refuted from below.

- **Satisfied (C4, C5).** Both are organism-scale bookkeeping. The assumed fish exists at the assumed
  size. The steady-glide load is, if anything, overstated.
- **Unsatisfied (C1, C2, C3).** Every one of these is a tissue-scale or physiology quantity that
  **nobody has measured in exocoetids**. They are the claim's two named conditions, made quantitative:
  - isometry requires a base ray diameter of ≥ ~1.9–5.3 mm;
  - in-vivo clamping requires ~0.35–1.0 N of sustained tension per ray, which is 10–29 body weights
    summed over both fins, held for ~1–9 s or more.

**The claim's own `evidence: derived` is therefore accurate.** "Active stiffening can carry the load" is
a statement of feasibility in arithmetic. It has no biological confirmation at either adjacent scale.

**Not entailed separately:** whether the lock factor itself is ≥ 2.1 in a 120 mm ray. My reasoning is as
follows; none of this is the authors' claim.

- Alben's nondimensional G = (shear modulus × intraray area)·L²/B. Under isometry that combination is
  invariant, so the 12x carries over by construction.
- Per the summarizer read of Alben 2007, the model ratio rises from ~3 to ~100 as G increases through 1,
  so it is never below ~3.
- Checking this constraint would only restate the claim's premise. It would not test it.

**The cheapest decisive test** (my estimate, not sourced): dissect one exocoetid pectoral fin and measure
the base diameter of the longest rays and the cross-section of the fin-base muscles. That resolves C1 and
the order of magnitude of C2 in a day.

```swarm-entail
{"source_claim": 96, "source_scale": "organ",
  "constraints": [
    {"target_scale": "tissue", "kind": "spatial",
      "statement": "The load-bearing ray's cross-section must grow with ray length fast enough that a 120 mm ray's passive EI is at least EI_req/12; at constant modulus its base diameter must be >=1.93x (relay baseline) to >=2.65x (Alben one-free baseline) that of a 40 mm bluegill ray",
      "quantity": "base diameter of a 120 mm load-bearing pectoral ray (equivalently passive EI >= 5.3e-5 N m^2; EI~L^b with b >= 2.41-3.57)", "lo": 1.9, "hi": null, "units": "mm",
      "status": "unsatisfied",
      "satisfied_by": "No exocoetid ray diameter, second moment or EI found, and no measured EI-vs-length or diameter-vs-length exponent for any teleost ray; only within-fin variation (perch, gar, sturgeon, coho) and Cypselurus wing-span positive allometry (b=0.375, Fish 1990), which is planform, not cross-section",
      "satisfied_evidence": "unknown",
      "note": "Requirement calculated (claim-96-entail_calc.py) from S6-D EI_req 6.3e-4 (assumption-driven), Puri 2018 1-2 mm bluegill diameter (full-text, relayed by S26-D), baselines 3.8e-6 (relay) and 1.07e-6 (S26-D back-calc of Alben 2007) preserved separately; lo uses the less demanding baseline and 1 mm bluegill diameter, worst case 5.3 mm. Negative scope: two web searches by me + S6-D Europe PMC (35 hits) + S26-D two web searches; Google Scholar, Web of Science, ZFIN not searched. Nobody has looked (not measured), not looked-and-found-small. Flammang 2013 565e-6 (abstract) would pass without any lock; D1 unresolved."},
    {"target_scale": "tissue", "kind": "range",
      "statement": "A contractile (or other tension-bearing) element at each ray base must sustain the hemitrich axial couple that a locked base implies, ~M/d per ray",
      "quantity": "sustained tension per ray at the hemitrich base (implying >= 1.2 mm^2 muscle CSA per ray at 289 kPa, up to ~18 mm^2 at 57 kPa; 10-28 N summed over 28 rays = 10-29 body weights)", "lo": 0.35, "hi": 1.0, "units": "N",
      "status": "unsatisfied",
      "satisfied_by": "No exocoetid fin-base muscle CSA, mass, force or glide EMG found. Only non-exocoetid fin EMG (bluegill, perch, killifish, Polypterus) and the bluegill actuation figure 10-15 mN per 100 um (scales to ~0.09-0.13 N under L^2, a different quantity)",
      "satisfied_evidence": "unknown",
      "note": "Requirement calculated: M = P L/2 = 2.1e-3 N m, d = 0.7-1.0 x isometric 3-6 mm diameter (bone ~30% of thickness, Alben 2007, full-text via summarizer); upper-end because a 12x lock leaves part of M in hemitrich bending. Muscle stress: Lou, Curtin & Woledge 2002 dogfish red 142 / white 289 kN m^-2; Johnston & Salamonski 1986 marlin red 57 / white 176 kN m^-2 (both search-summary). Lauder SICB abstract (search-summary). Negative scope: my web searches on flying-fish pectoral myology/EMG and on the 10-15 mN source. Nobody has looked."},
    {"target_scale": "organism", "kind": "timescale",
      "statement": "Active clamping must be sustainable for at least one glide, i.e. lock endurance >= glide duration (unless the lock can be released during inter-glide taxiing)",
      "quantity": "duration the lock must be held", "lo": 0.75, "hi": 45, "units": "s",
      "status": "unsatisfied",
      "satisfied_by": "No fibre-type, fatigue or endurance data found for any exocoetid fin muscle; other taxa disagree (notothenioid pectoral adductor profundis mainly slow; weakfish pectoral mainly white; goldfish +23% oxidative when cold-acclimated), so nothing transfers",
      "satisfied_evidence": "unknown",
      "note": "0.75-9.2 s calculated from Fish 1990 (full-text) relaying typical Cypselurus flights 15-92 m (Hubbs 1918; Aleyev 1977) and speeds 10 to 16-20 m/s; up to 12 successive glides; 45 s airborne record from Guinness (listing). Fibre-type sources search-summary. Negative scope: one web search on pectoral-fin fibre types/isometric endurance + the myology search. Nobody has looked in exocoetids."},
    {"target_scale": "organism", "kind": "spatial",
      "statement": "A gliding fish of ~0.1 kg must exist with ~14 load-bearing rays per pectoral fin of span near the assumed 0.12 m; under isometry the margin scales as L^2, so the 12x lock still suffices for L >= 0.12/sqrt(5.7) = 0.050 m and longer is safer",
      "quantity": "pectoral fin span (semispan) of a 0.1 kg flying fish", "lo": 0.050, "hi": null, "units": "m",
      "status": "satisfied",
      "satisfied_by": "Fish 1990 r.m.a. regressions at 0.1 kg: Cypselurus semispan 137 mm, SL 203 mm; Exocoetus semispan 161 mm, SL 208 mm (calculated from measured regressions; semispan includes half body width, so fin ~0.12-0.15 m, assumption); mass range measured 0.003-0.53 kg (n=199); Cypselurus poecilopterus pectoral i,14-15",
      "satisfied_evidence": "derived",
      "note": "Fish FE 1990 J Zool Lond 221:391-403 (full-text, OCR; regression units verified against the paper's own 0.51 m Danichthyes span). Ray count: Cook Islands Biodiversity (search-summary); genus-wide range not established; FishBase could-not-access. Fin span is not longest-ray length; ray length not directly measured. Margin at L = 100/120/137/161 mm: 3.9/5.7/7.4/10.2 (calculated, isometric)."},
    {"target_scale": "organism", "kind": "conservation",
      "statement": "Momentum balance: the lift carried by the pectoral rays must not exceed (5.7 / pectoral share) times weight, i.e. pectoral share x load factor <= 5.7",
      "quantity": "load factor n on the pectoral rays (with pectoral share 0.76-1.0)", "lo": null, "hi": 5.7, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Steady flat glide (Fish 1990) gives n ~ 1 by momentum balance; pectoral fins are 76.0 +/- 0.6% (Cypselurus) and 91.8 +/- 0.4% (Exocoetus) of wing area, so S6-D's 100%-on-pectorals load is conservative if lift ~ area (assumption); tolerable n 5.7-7.5 (calculated)",
      "satisfied_evidence": "derived",
      "note": "Fish 1990 (full-text). Satisfied for steady glide only: no measured load factor for take-off pull-up, turns or landing was found (nobody has looked in the searched scope), so manoeuvring loads remain open."}
  ]}
```
