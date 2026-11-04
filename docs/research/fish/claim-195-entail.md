# Claim 195 — entailment to the organ and behaviour scales

**Source claim** (claim 195, scale `organism`, evidence level **derived**; from S28, `docs/research/fish/S28-organism.md`
@ `origin/claude/s28-organism-design-5z0vjz`):

> CHEAPEST DECISIVE MEASUREMENT: pectoral fin AREA in the existing Daane double heterozygote. Daane et al. measured
> fin LENGTH only and never reported area, so the animal exists and the measurement does not. It decides whether
> even the small phenotype is detectable.

The "small phenotype" is S28 §3.6: a reduction in ascent deceleration during a leap, **"if the fish spreads its
pectorals during the leap. Whether it does so has never been observed."** Challenge 194 put its size at ≤ 4.5–4.9 %;
S28-D (`origin/claude/deepen-s28-daane-heterozygote-b7kpn8`) at 0.9–6.2 %, conditional on fin length.

Date 2026-11-04. I made no measurement. Every number in this note is labelled as **measured (by someone, cited)**,
**calculated (by me)**, or **project-derived (calculated by an earlier note, not by me)**.

## What the claim requires below and beside it

For "area decides detectability" to be true, area has to be the factor that is unknown and limiting, and the other
factors in the phenotype have to be in place. The phenotype is a product:

  lift-on-ascent ∝ (projected area in air) × CL × V²_exit × [fins spread in air: 0 or 1]

So the claim entails requirements on the **organ** (how big the fin is, and whether a static photograph of it is the
area that flies) and on the **behaviour** (whether the fin is spread in the air at all, fast enough, and at a speed
where the lift is non-trivial).

| # | Scale | Kind | Requirement (generic) | Bound | Status |
|---|---|---|---|---|---|
| 1 | organ | range | Double-het pectoral fin length per fin must be large enough for the phenotype to reach ≥ 2 % at in-species speeds | L_fin/SL ≥ 0.22–0.26 | **open** (value exists in Daane Fig. 4B; could-not-access) |
| 2 | organ | range | Fin must hold its spread planform under leap loads, so that static spread area ≈ area that flies | whole-fin EI ≥ ~2.8e-8 N m² (my calculation); S28 states 6.3e-5 | **unsatisfied** (no zebrafish measurement) |
| 3 | behaviour | existence | A behaviour must exist in which the pectoral fins are abducted/spread while airborne | — | **unsatisfied** (never observed; larval data lean against) |
| 4 | behaviour | range | Water-exit speed must reach the speed at which the case-C fin gives the rule's 10 % W "proceed" lift | V_exit ≥ 1.40 m/s | **unsatisfied** (exit speed never measured; in-water proxies straddle the bound) |
| 5 | behaviour | timescale | Fin abduction must complete in a small fraction of the ascent time | t_abduct ≤ ~0.05 s (half of a 0.10–0.14 s ascent) | **open** (not checked to a number) |

No constraint is `unsatisfiable`. I looked for a measured number that contradicts each one and found none in the
right species and setting (§2–§5 say what I found instead). One constraint (2) exposes a probable error in the
requirement S28 itself states.

---

## 1. Organ / range — the fin must be long enough for any phenotype to exist

**Requirement.** S28-D (project-derived, not mine; script `S28-deepen_calc.py`) computed that, at S28's body
(SL 3.0 cm, 0.25 g), AR-5 geometry and a 45° launch, a ≥ 2 % ascent-deceleration reduction needs a pectoral fin of
**≥ 0.26 SL** per fin at 1.38 m/s and **≥ 0.22 SL** at 1.57 m/s; ≥ 5 % needs 0.39–0.51 SL. If the double het's fin
is below ~0.22 SL, the area measurement has nothing to decide: the phenotype is below 2 % for every in-species speed.

**Check.** The number that settles this exists — Daane et al. 2021 Fig. 4B plots pectoral fin length normalised by SL
for WT, `lof/+`, `nr21/+` and the double het — but I could not read it.

- Daane JM et al. 2021, *Curr Biol* 31:5052, doi:10.1016/j.cub.2021.08.054, PMC9172250. **Read-level: full-text**
  (NCBI eutils efetch PMC XML, 202,692 bytes, fetched this session). I grepped it for *area*, *ImageJ*, *Fiji*,
  *normaliz*, *standard length*, *pectoral*. Author statements: Fig. 4B/C legend "Pectoral fin length (B) and caudal
  fin length (C) suppression of overgrowth in medial fin by *lat4a* mutation … In (B) and (C), length normalized by
  SL." **No numeric pectoral length/SL and no fin area appear in the text.** This independently confirms the claim's
  literature half ("measured LENGTH only, never area") at full-text level.
- Supplementary Data S1 (`NIHMS1735542-supplement-2.xlsx`): **could-not-access**. pmc.ncbi.nlm.nih.gov and
  www.ncbi.nlm.nih.gov returned a proof-of-work challenge page instead of the file; Europe PMC returned 403, and its
  REST API says the article "is not open access". The text cites Data S1A–S1K for the beloniform allometry and
  genomics, not for Fig. 4, so I do not know whether the zebrafish lengths are in it at all.
- ZFIN figure record ZDB-FIG-221222-34: **could-not-access** (HTTP 503 this session). bioRxiv preprint
  10.1101/2021.03.05.434157: **could-not-access** (HTTP 429).
- S28-D (repository, full-text) also could not reach Fig. 4B and found no adult WT pectoral length/SL anywhere.

**Status: open.** This is not "unsatisfied": the measurement has been made and published as a plot; it is
inaccessible to me, not absent. S28's 0.45 SL is an extrapolation (S28 §2.2, its own word) and does not count as
meeting the bound. Note the consequence for claim 195: reading Fig. 4B costs minutes and can close the line
(fin ≤ 0.22 SL) **before** any fish is anaesthetised, so for one of its outcomes it is cheaper than the claim's
measurement (challenge 195 made the same point).

## 2. Organ / range — the photographed area must be the area that flies

**Requirement.** The claim measures the area of an anaesthetised, manually spread fin. That equals the lift-relevant
area only if the fin holds its planform under leap loads. Generic form: the fin's flexural stiffness must keep tip
deflection small (I use δ/L ≤ 0.1) under the lift it carries at water exit.

**My calculation of the bound** (calculated, not measured): lift at exit 0.10 W = 2.45e-4 N (W = 0.25 g × g),
1.23e-4 N per fin, treated as a uniformly loaded cantilever of L = 13.5 mm (S28's extrapolated fin):
δ_tip = F L³ / (8 EI), so δ/L ≤ 0.1 ⇒ **EI ≥ F L² / 0.8 = 2.8e-8 N m² for the whole fin**.

**Disagreement with the source, preserved.** S28 §4 item 3 states the leap requirement as "0.1 × 6.3e-4 =
**6.3e-5 N m²**". That is **~2,200× my bound**. I could not find where 6.3e-4 comes from (S28 attributes it to S25,
and I did not trace it further), so I do not know whether it is per-ray, per-fin, or computed for a larger body or a
different load. I record both and do not average them. On my bound the constraint is much easier to meet; on S28's
it is much harder.

**Check.**
- **Zebrafish pectoral ray EI: no measurement found.** Scope: one web search ("zebrafish pectoral fin ray flexural
  stiffness EI measured", search-summary) and the project's S25 / S25-D-D notes (repository, full-text). The search
  summary explicitly found none for zebrafish. This is "I looked and found nothing", within that scope.
- The project's two disputed values, **3.8e-6** and **565e-6 N m²**, are **bluegill** rays (Alben 2007; Flammang et
  al. 2013, *J Morphol* 274:1044 — S25-D-D has the latter at abstract level only), not zebrafish. S25-D-D argues
  565e-6 is 13–105× too high for a single 40 mm ray (calculated there). The dispute stays unresolved.
- Nearest measured small-fish values: Aiello et al. 2018, *J Exp Biol* 221:jeb163360, three-point bending of labrid
  pectoral rays, **1e-10 to 1.51e-6 N m²** per ray region. **Read-level: search-summary** (and via S25-D-D).
- My inference, not an observation: isometrically scaling the bluegill 3.8e-6 from a 40 mm ray to a 13.5 mm ray
  (EI ∝ L⁴) gives ~5e-8 N m² per ray, which would meet my whole-fin bound with ~10 rays and miss S28's by ~10⁴.
  The answer therefore hinges on which requirement is right, not on the stiffness data.

**Status: unsatisfied** — no measured zebrafish value meets either bound, because none exists within the scope above.
Not `unsatisfiable`: no measured zebrafish number contradicts it. Not `satisfied`: the scaled cross-species estimate
is a calculation.

## 3. Behaviour / existence — the fish must spread its pectorals in the air

**Requirement.** A behaviour must exist in which the pectoral fins are abducted (spread) during the airborne phase of
a leap. If it does not, lift on ascent is ≈ 0 for every fin area and the area measurement decides nothing.

**Check.**
- S28 §3.6 (repository, full-text), author's statement: "Whether it does so has never been observed."
- **Adult zebrafish, airborne fin posture: nothing found.** Scope: web searches "adult zebrafish pectoral fin adducted
  during fast start escape C-start pectoral fin posture", "adult zebrafish pectoral fins folded against body at high
  swimming speeds …", "zebrafish jumping out of water leap behaviour" (all search-summary). This is **"nobody has
  looked"**, not "looked and found absent": I found no study that filmed fin posture in an adult zebrafish leap.
- The only zebrafish airborne-locomotion study surfaced is **terrestrial** jumping from a surface: Gibb, Ashley-Ross,
  Pace & Long 2011, *J Exp Zool A* 315A:649, doi:10.1002/jez.711 (**read-level: abstract via search-summary and
  press coverage**). Zebrafish produce tail-flip jumps; press summaries say they launch near 90° and tumble more than
  *Gambusia*. Nothing on pectoral posture reached me. It is not a water exit.
- **Larval evidence, which leans against abduction at high speed** (in water, larvae — a different stage and setting,
  so my inference that it bears on adult leaps is weak):
  - Green, Ho & Hale 2011, *J Exp Biol* 214:3111 (**search-summary**): pectoral fin beat amplitude falls as speed rises
    over 1.47–4.56 BL/s; fins not required for forward rhythmic swimming.
  - A larval kinematics paper (**search-summary**; I did not identify it beyond the summary) reports a critical speed
    above which larvae stop moving the pectorals and swim by body undulation alone.
  - A 2012 *PLoS ONE* larval escape study (**search-summary**): pectoral fins play no role in short-latency C-bends.

**Status: unsatisfied.** The scope of the negative is adult airborne fin posture, never filmed as far as I found.
The larval data are not a measured contradiction of an adult airborne behaviour, so not `unsatisfiable`. This is the
constraint that most directly weakens "decisive": area is one factor and this is a factor that may be zero.

## 4. Behaviour / range — exit speed must reach the "proceed" threshold

**Requirement.** S28's decision rule says "proceed to film leaps" at S ≥ ~190 mm², because there lift is 10 % W at
exit. That threshold presumes an exit speed. Solving for it (calculated, S28 inputs: m 0.25 g, ρ 1.225 kg m⁻³,
CL 1.07 assumed, S = 192.2 mm²): V_to = 4.41 m/s, so 10 % W needs **V_exit ≥ 4.41 × √0.1 = 1.40 m/s**.

**Check.**
- **Adult zebrafish water-exit speed: never measured** within my scope (the leap search in §3 found only terrestrial
  jumps; S28-D §6 states "Neither study measured a surface exit. No adult zebrafish exit speed is known in the
  record"). This is "nobody has measured", not "measured and too slow".
- The in-water proxies **disagree across the bound, and I keep them separate**:
  - Miln et al. 2021, *R Soc Open Sci* 8:210146: per-fish maximum burst **1.38 m/s** — just **below** 1.40.
    Read-level: **listing** (via project challenges 75/192).
  - Demesmay et al. 2025, *PLoS Biol* 23:e3003484: adult escape peak **1.57 ± 0.27 m/s** — mean **above** 1.40.
    Read-level: **listing** (via S20-D-D-D's full-text read).
  - Exit speed ≤ in-water peak is my assumption (surface break and the pre-exit trajectory can only cost speed).

**Status: unsatisfied** — no measured exit speed exists to meet it. Not `unsatisfiable`: neither proxy is an exit
speed, and one proxy's mean clears the bound. Because lift ∝ V², this constraint is as strong as area itself (S28-D
§1), which is a second reason area alone is not decisive.

## 5. Behaviour / timescale — the fin must open before the ascent is over

**Requirement.** Lift matters most at exit (it falls as V²), so the fins must be spread within a small fraction of
the ascent. Ascent time t_up = V sinθ / g (calculated): **0.099 s** at 1.38 m/s and 45°; **0.141 s** at 1.38 m/s
vertical; 0.113–0.160 s at 1.57 m/s. Requirement: abduction complete in **≤ ~0.05 s** (half the shortest ascent).

**Check.** I did not find an adult zebrafish pectoral abduction time or beat frequency to a number. The larval
studies in §3 report pectoral beating in larvae but I did not read a frequency at a usable read-level, and larval
fins are not adult fins. **Status: open.** I am not marking it satisfied on the plausibility that a fin can move in
50 ms.

---

## What this means for claim 195 (my inference)

- The literature half of the claim — Daane measured length only and reported no area — **holds at full-text level**.
- The organ scale contains a cheaper prior gate (constraint 1): Fig. 4B's length/SL, already measured, can close the
  line by itself if it is ≤ ~0.22 SL.
- The behaviour scale contains two factors that are each as strong as area and are unmeasured (constraints 3, 4).
  For area to "decide" detectability, both must already be in place; neither is established. Area measures one
  factor of the product; it cannot decide the product.
- The requirement S28 states for fin stiffness under leap load (6.3e-5 N m²) disagrees with my own cantilever bound
  by ~2,200×; whoever next uses that number should trace it.

## Sources

| Source | Read-level |
|---|---|
| Daane JM et al. 2021, *Curr Biol* 31:5052, PMC9172250 (text and legends) | full-text |
| Daane 2021 Supplementary Data S1 (xlsx); ZFIN ZDB-FIG-221222-34; bioRxiv 10.1101/2021.03.05.434157 | could-not-access |
| S28-organism.md; S28-D `S28-deepen.md`; challenge-195.md (`origin/claude/challenge-195-fin-area-mb1jwk`); S25-D-D `S25-D-deepen.md` | full-text (repository) |
| Gibb AC, Ashley-Ross MA, Pace CM, Long JH 2011, *J Exp Zool A* 315A:649 | abstract (via search-summary / press) |
| Green MH, Ho RK, Hale ME 2011, *J Exp Biol* 214:3111 | search-summary |
| 2012 *PLoS ONE* larval escape study (pectoral fins in C-bends) | search-summary |
| Aiello BR et al. 2018, *J Exp Biol* 221:jeb163360 | search-summary |
| Alben S et al. 2007; Flammang BE et al. 2013, *J Morphol* 274:1044 | via S25-D-D (abstract there) |
| Miln C et al. 2021, *R Soc Open Sci* 8:210146 | listing (via project notes) |
| Demesmay L et al. 2025, *PLoS Biol* 23:e3003484 | listing (via project notes) |

```swarm-entail
{"source_claim": 195, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The double heterozygote's pectoral fin must be long enough, relative to body length, for the leap phenotype to reach at least 2% at in-species exit speeds; otherwise there is nothing for an area measurement to decide",
      "quantity": "pectoral fin length per fin / standard length", "lo": 0.22, "hi": null, "units": "fraction of SL",
      "status": "open",
      "satisfied_by": "Not determined. The deciding value is plotted in Daane et al. 2021 Fig. 4B (pectoral length normalised by SL) but could not be accessed; the paper's text has no numeric length or area. S28's 0.45 SL is an unsourced extrapolation and does not count.",
      "satisfied_evidence": "unknown",
      "note": "Bound is project-derived (S28-D: 0.22 SL at 1.57 m/s, 0.26 SL at 1.38 m/s for >=2%). Daane 2021 Curr Biol 31:5052 PMC9172250 full-text grepped: no numeric fin length/SL, no area. Supplementary Data S1 (PMC proof-of-work page; Europe PMC 403/not OA), ZFIN ZDB-FIG-221222-34 (503), bioRxiv preprint (429): could-not-access. The value exists but is inaccessible; this is not a negative."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The fin must be stiff enough to hold its spread planform under the lift it carries at water exit, so that a static spread-fin area equals the area that produces lift (tip deflection <= 0.1 of fin length)",
      "quantity": "whole-fin flexural stiffness EI", "lo": 2.8e-08, "hi": null, "units": "N m^2",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish pectoral ray or fin EI measurement found. Project values 3.8e-6 and 565e-6 N m^2 are bluegill and disputed; labrid rays 1e-10 to 1.51e-6 N m^2 per ray region (Aiello 2018) are another family.",
      "satisfied_evidence": "unknown",
      "note": "lo is my calculation (uniform-load cantilever, 0.1 W at exit split over two fins, L = 13.5 mm). S28 states the requirement as 6.3e-5 N m^2, ~2200x higher; its origin (attributed to S25) was not traced; disagreement preserved. Negative scope: one web search for zebrafish pectoral ray EI (search-summary) plus project S25/S25-D-D notes. Isometric scaling of bluegill 3.8e-6 to a 13.5 mm ray gives ~5e-8 per ray (calculation, not observation)."},
    {"target_scale": "behaviour", "kind": "existence",
      "statement": "A behaviour must exist in which the pectoral fins are abducted (spread) while the fish is airborne after leaving the water",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Never observed in adult zebrafish. Nearest data are larval and in-water: pectoral beat amplitude falls with speed and fins stop moving above a critical speed (Green, Ho & Hale 2011); pectorals play no role in short-latency C-bends (2012 PLoS ONE). Only airborne zebrafish study found is terrestrial jumping (Gibb et al. 2011), with no fin posture reported in what I could read.",
      "satisfied_evidence": "unknown",
      "note": "S28 sec 3.6: 'Whether it does so has never been observed.' Scope: three web searches (adult fast-start fin posture; adult high-speed pectoral folding; zebrafish leaping out of water), all search-summary. Finding is 'nobody has looked', not 'looked and found absent'. Larval data lean against but are a different stage and setting, so not a contradiction. Gibb et al. 2011 J Exp Zool A 315A:649 doi:10.1002/jez.711 (abstract); Green et al. 2011 J Exp Biol 214:3111 (search-summary)."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "Water-exit speed must be high enough that the most generous fin gives the decision rule's 10% of body weight lift at exit",
      "quantity": "water-exit speed", "lo": 1.40, "hi": null, "units": "m/s",
      "status": "unsatisfied",
      "satisfied_by": "No adult zebrafish water-exit speed has been measured. In-water escape proxies straddle the bound: Miln 2021 per-fish maximum 1.38 m/s (below); Demesmay 2025 mean 1.57 +/- 0.27 m/s (above).",
      "satisfied_evidence": "unknown",
      "note": "lo is my calculation from S28 inputs (m 0.25 g, S 192.2 mm2, CL 1.07 assumed): V_to 4.41 m/s x sqrt(0.1). Miln et al. 2021 R Soc Open Sci 8:210146 (listing); Demesmay et al. 2025 PLoS Biol 23:e3003484 (listing). Proxies kept separate, not averaged. Assumes exit speed <= in-water peak. Negative scope: web search for zebrafish leaping out of water plus S28-D's record; 'nobody has measured'."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "Pectoral fin abduction must complete within a small fraction of the airborne ascent, since lift is largest at exit and falls as V^2",
      "quantity": "time to full pectoral abduction", "lo": null, "hi": 0.05, "units": "s",
      "status": "open",
      "satisfied_by": "Not checked to a number: no adult zebrafish pectoral abduction time or beat frequency read at a usable read-level.",
      "satisfied_evidence": "unknown",
      "note": "hi is half the shortest ascent time, my calculation: t_up = V sin(theta)/g = 0.099 s at 1.38 m/s and 45 deg; 0.141 s vertical; 0.113-0.160 s at 1.57 m/s. Larval pectoral kinematics exist (Green et al. 2011) but larval fins are not adult fins. Left open, not marked satisfied on plausibility."}
  ]}
```
