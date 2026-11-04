# Claim 77 — entailment to the cell and organ scales

**Source claim (tissue scale, evidence: derived).**
> S10-D VERDICT STRENGTHENS: the measured teleost pectoral-muscle fraction is ~1.4% of body mass for both fins (*Abudefduf saxatilis*, 0.69% per fin, Mansuit & Herrel 2021 Table 1, full text) against a computed threshold of 7.5–20%. Hover demand is 730–1950 W/kg, 5–15× above measured warm zebrafish fast muscle.

**What the claim depends on.** It combines one measured number, one measured number from a different animal, and two calculated numbers:

| Number | Kind | Animal |
|---|---|---|
| 0.69% body mass per pectoral fin | measured (Mansuit & Herrel 2021, Table 1) | *Abudefduf saxatilis* (sergeant major, Pomacentridae) |
| ~1.4% for both fins | **derived** (0.69 × 2, assumes left/right symmetry) | *A. saxatilis* |
| 7.5–20% muscle fraction threshold | **calculated** (S10-D model) | the modelled zebrafish |
| 730–1950 W/kg hover demand | **calculated** (S10-D model) | the modelled zebrafish |
| "warm zebrafish fast muscle" power | measured; identified below as Mead et al. 2020 | *Danio rerio*, **5-day larva, axial (tail) myotome** |

The S10-D derivation itself is not in this repository (I searched `delphi-frontier` for `S10`, `S32`, `exocoet`, `pectoral` and `zebrafish` and got no hits). So I could not re-check the inputs to the 730–1950 W/kg and 7.5–20% figures. Below they are taken as given, labelled *calculated*.

---

## Sources and read-levels

| Ref | Source | Read-level |
|---|---|---|
| [MH21] | Mansuit R. & Herrel A. (2021) *Front. Ecol. Evol.* 9:702576, doi:10.3389/fevo.2021.702576 | **full-text** (PDF text extracted; Table 1 and Results read) |
| [M20] | Mead A.F., Kennedy G.G., Palmer B.M., Ebert A.M., Warshaw D.M. (2020) "Mechanical characteristics of ultrafast zebrafish larval swimming muscles", *Biophys. J.* 119:806–820; bioRxiv 10.1101/2020.04.02.010298 | **full-text** (bioRxiv preprint PDF; Methods, Results and Discussion read) |
| [AME01] | Askew G.N., Marsh R.L. & Ellington C.P. (2001) quail take-off power, *J. Exp. Biol.* 204 | **search-summary** (abstract sentences quoted by the search tool; journal site `cob.silverchair.com` unreachable from this session) |
| [AM02] | Askew G.N. & Marsh R.L. (2002) "Muscle designed for maximum short-term power…", *J. Exp. Biol.* 205:2153 | **search-summary** (same reason) |
| [W95] | Wiest F.C. (1995) "The specialized locomotory apparatus of the freshwater hatchetfish family Gasteropelecidae", *J. Zool.* 236:571–592 | **listing** (known only from a secondary page, seriouslyfish.com, that cites and summarises it; primary not read) |
| [ADW] | Animal Diversity Web, *Gasteropelecus sternicla*; Wikipedia, Gasteropelecidae | **search-summary** (popular sources; no primary measurement found behind the 25% figure) |
| [TH05] | Thorsen D.H. & Hale M.E. (2005) on the development of the zebrafish pectoral fin musculature, *J. Morphol.* | **search-summary** |
| [PD08] | Patterson S.E. & Devoto S.H. (2008) on pectoral fin muscle growth in zebrafish | **search-summary** |

**Checking the claim's source before using it.** [MH21] Table 1 does give *Abudefduf saxatilis* pectoral muscle as abductor superficialis 0.13, abductor profundus 0.23, adductor superficialis 0.15, adductor profundus 0.18, **total 0.69 [M_muscle/M_body (%)]**. The authors' text says that "the summed muscle mass of each fin represents less than 1% of the total body mass" in actinopterygians and *Latimeria*. *Latimeria* has 0.43% pectoral and 0.30% pelvic. So the 0.69% is per fin, and the claim's ×2 doubling reads it correctly. Two caveats:
- [MH21] is a perspective paper, and the *Abudefduf* row is its **only** actinopterygian mass-fraction row; the other fish rows are PCSA. Its methods attribute the actinopterygian data to Thorsen & Westneat (2005), Dickson & Pierce (2019) and Crawford et al. (2020), so the *Abudefduf* row is presumably from Thorsen & Westneat (2005). That attribution is **my inference**; the table does not say which row came from which paper.
- The fish is a pomacentrid, which uses its pectoral fins for labriform swimming. **It is not a zebrafish.**

**Identifying "warm zebrafish fast muscle".** [M20] Methods: work loops were run with the preparation "maintained at … 28° C (isometric force, force:velocity, work loops)". Results: "maximum net power … was produced at 80 Hz (134.4±19.9 W/kg) and remained high (122.9±11.1 W/kg) at 100 Hz". Dividing, 730/134 = 5.4 and 1950/134 = 14.6, which matches the claim's "5–15×". So I take [M20] to be the comparator. That is **my inference from the arithmetic**; the claim does not name its source.

---

## Constraints and checks

### C1 — cell — `range` — cycle-averaged power of zebrafish fast fibres
**Requirement.** For "5–15× above" to hold, the cycle-averaged net mechanical power of zebrafish fast skeletal muscle must be at most 730/5 ≈ **146 W/kg muscle** (no lower bound required).

**Check.** [M20], full-text: **134.4 ± 19.9 W/kg at 80 Hz, 28 °C**, net power in sinusoidal work loops (measured). The mean is within the bound. Mean + 1 SD is 154 W/kg, which gives a ratio of 4.7× against 730 W/kg. So the "5×" end of the claim sits on the measurement's error bar but does not change the conclusion.

**Same animal?** Zebrafish on both sides. However, the measurement is on a **5 dpf larva's axial tail myotome**, not adult pectoral muscle (see C2).

**Status: satisfied** for larval axial fast muscle, measured.

**Flag (not a refutation).** [M20] also reports **peak instantaneous power during shortening of 498.9 ± 127.0 W/kg (80 Hz) and 640.2 ± 151.5 W/kg (100 Hz)**. That peak is within 1.14× of the 730 W/kg lower hover bound, and its upper error bar (792 W/kg) overlaps it. The 5–15× margin therefore holds only if S10-D's 730–1950 W/kg is a **cycle-averaged** demand compared against cycle-averaged supply. I could not confirm this because the S10-D derivation is not in this repo. If the demand were compared against instantaneous capacity, the margin would shrink to roughly 1.1–3×.

### C2 — cell — `range` — power of the fibres that actually drive the fin
**Requirement.** The muscle that would power a hover is the **pectoral fin** abductor/adductor in an **adult**, not larval tail muscle. The claim needs that muscle's cycle-averaged power to also be at most ~146 W/kg.

**Check.** I ran three web searches: adult zebrafish pectoral fin muscle contractile properties, power output, and fibre twitch. I found **no** mechanical measurement on zebrafish pectoral fin muscle at any stage. The nearest items were:
- Adult zebrafish isolated fast fibres from **dorsal trunk** muscle, with "superfast" excitation–contraction coupling (*J. Gen. Physiol.* 2022, 154:e202213158; search-summary). That paper reports Ca²⁺ kinetics, not power.
- [TH05] and [PD08], which give anatomy and development only. [TH05] reports that adult pectoral fin function shifts from axial-locomotion support to "swim initiation and maneuvering".

**Status: unsatisfied — in the sense of "nobody has looked, as far as this search reached".** The scope was three general web searches, not a database search (PubMed or Web of Science were not queried directly). This is a different finding from "measured and found low". The claim currently assumes pectoral fibres behave like the larval tail myotome.

### C3 — cell — `range` — no vertebrate fibre type could rescue the claim
**Requirement.** The "strengthens" verdict also requires that **no known vertebrate skeletal muscle** delivers cycle-averaged power at or above the hover demand, i.e. ≤ 730 W/kg. Otherwise the shortfall would be a zebrafish-specific limit, not a limit of vertebrate muscle.

**Check.** [AME01]/[AM02], search-summary:
- Blue-breasted quail (*Coturnix chinensis*) pectoralis during take-off: mean **390 W/kg**, calculated from kinematics and aerodynamics.
- One individual: **530 W/kg**, calculated.
- In-vitro fibre bundles: **433 W/kg**, measured.
- As quoted from a later review: "the highest instantaneous and cycle average power outputs of skeletal muscle measured to date are approximately 1200 W kg⁻¹ and 400 W kg⁻¹, respectively".

The cycle-average record (~400, at most 530 W/kg) is below 730 W/kg. The instantaneous record (~1200 W/kg) is above it. This is the same instantaneous-versus-averaged issue as in C1.

**Same animal?** No. These are bird numbers, used only as a ceiling on what vertebrate muscle is known to do, not as a zebrafish measurement.

**Status: satisfied** (as a ceiling), on search-summary read-level only. The primary papers were not readable from this session, so the 390, 433 and 530 figures should be re-read in full text before anyone relies on them.

### C4 — organ — `range` — the zebrafish's own pectoral muscle fraction
**Requirement.** The claim is about the zebrafish. It therefore requires **zebrafish** pectoral muscle (both fins) to be below the 7.5% lower bound of the calculated threshold. Quantity: M_pectoral/M_body, hi = 7.5%.

**Check.**
- **Zebrafish:** no measured value found. Two web searches for adult zebrafish pectoral abductor/adductor mass relative to body mass returned only anatomy: [TH05], [PD08], and a reference to the Siomava & Diogo adult myology description, which I did not retrieve and which, as described, is anatomical, not gravimetric. Status for zebrafish: **unknown**.
- **Cross-species, *Abudefduf saxatilis*:** 0.69% per fin, 1.38% for both [MH21, full-text, measured]. This is 5.4× below the 7.5% bound.
- **Cross-species, *Latimeria*:** 0.43% per fin [MH21].

**Same animal?** No. The only measured teleost number is a pomacentrid. My inference: damselfish use the pectoral fins as their main cruising propulsors, so a body–caudal swimmer like the zebrafish would plausibly carry the same or less pectoral muscle. That is an argument, not a measurement, and it cannot turn this constraint into `satisfied`.

**Status: open.** The constraint is checkable cheaply: dissect and weigh the pectoral abductor and adductor in a few adult zebrafish. As far as these searches reached, nobody has published it.

### C5 — organ — `existence` — a high-muscle teleost should be the one that powers aerial pectoral flapping
**Requirement.** If the 7.5–20% threshold is right, then any teleost that **does** power aerial flapping with its pectorals must have a pectoral muscle fraction in or above that range. Conversely, teleosts well below it (≈1–2%) must not flap-fly. This is a test of the calculated threshold against an independent animal.

**Check.**
- Freshwater hatchetfishes (Gasteropelecidae, Characiformes; the same superorder, Ostariophysi, as zebrafish) are repeatedly reported to have pectoral muscles of **"up to 25%"** of body mass [ADW, search-summary]. I found **no primary measurement** behind that figure; it may be a repeated popular estimate.
- Wiest (1995) [W95, listing only] reportedly used high-speed video to show the pectoral fins are used **to leave the water but not beaten while airborne**. Other popular sources still describe fin-beating flight. **The sources disagree, and that disagreement is preserved here.**
- If the 25% figure is real, then a teleost does exist with a pectoral fraction above the calculated 20% ceiling, and even it reportedly does not sustain flapping flight. On its face that is **consistent** with the claim that muscle fraction is the limit, since this animal sits above threshold and only launches. But it also shows that ~1.4% is not a hard anatomical ceiling for teleosts.
- Exocoetids (flying fish) glide on pectoral "wings" powered by caudal taxiing, not pectoral flapping. I did **not** re-check this in the present session, so it is stated here only as background and not used.

**Same animal?** No. Hatchetfish and flying-fish data are cross-species and cannot confirm or refute a zebrafish claim.

**Status: open.** The 25% figure is unverified (no primary source found) and [W95] was not read.

---

## Verdict on claim 77 from below

- **No constraint is `unsatisfiable`.** No measured number on the same animal contradicts the claim.
- **C1** (larval zebrafish fast-muscle power at most ~146 W/kg) is **satisfied** by a same-species measurement: 134 W/kg at 28 °C, full-text.
- **C3** (no vertebrate muscle at or above 730 W/kg cycle-averaged) is **satisfied** as a ceiling, but only at search-summary read-level.
- **The claim's weak points are the zebrafish-specific organ and cell inputs**, both of which are unmeasured:
  - the zebrafish pectoral muscle fraction (C4, `open`; only *Abudefduf* has been measured);
  - the power of the pectoral fin fibres themselves (C2, `unsatisfied`, apparently not looked for).
- **The margin depends on how demand is averaged.** It holds only if the S10-D demand is cycle-averaged. Measured peak instantaneous power in larval zebrafish muscle (640 ± 151 W/kg) reaches the 730 W/kg lower bound within error.

```swarm-entail
{"source_claim": 77, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "cell", "kind": "range",
      "statement": "Cycle-averaged net mechanical power of the animal's fast skeletal muscle fibres must be at most hover demand / 5",
      "quantity": "cycle-averaged net power, zebrafish fast muscle", "lo": null, "hi": 146, "units": "W/kg muscle",
      "status": "satisfied",
      "satisfied_by": "Measured 134.4 +/- 19.9 W/kg at 80 Hz (122.9 +/- 11.1 at 100 Hz), 28 C sinusoidal work loops, 5 dpf larval zebrafish axial myotome. Peak instantaneous power 640 +/- 151 W/kg at 100 Hz reaches the 730 W/kg lower demand bound, so the margin holds only if S10-D demand is cycle-averaged (not verifiable: S10-D derivation not in repo).",
      "satisfied_evidence": "measured",
      "note": "Mead et al. 2020 Biophys J 119:806-820 (bioRxiv 10.1101/2020.04.02.010298), full-text. Same species (zebrafish) but larval tail muscle, not adult pectoral."},
    {"target_scale": "cell", "kind": "range",
      "statement": "Cycle-averaged power of the fibres that actually drive the pectoral fin (adult abductor/adductor) must also be at most hover demand / 5",
      "quantity": "cycle-averaged net power, adult zebrafish pectoral fin muscle", "lo": null, "hi": 146, "units": "W/kg muscle",
      "status": "unsatisfied",
      "satisfied_by": "No mechanical measurement of zebrafish pectoral fin muscle at any stage found. Nearest: adult zebrafish dorsal-trunk fast fibres (Ca2+ kinetics only, J Gen Physiol 2022 154:e202213158); pectoral anatomy/development only (Thorsen & Hale 2005; Patterson & Devoto 2008).",
      "satisfied_evidence": "unknown",
      "note": "Scope: three general web searches (adult zebrafish pectoral fin muscle contractile properties / power output / fibre twitch); PubMed and Web of Science not queried directly. Finding is 'nobody has looked, as far as searched', not 'measured and found low'. Read-level: search-summary."},
    {"target_scale": "cell", "kind": "range",
      "statement": "No known vertebrate skeletal muscle may deliver cycle-averaged power at or above the hover demand, or the shortfall is species-specific rather than a muscle limit",
      "quantity": "highest measured cycle-averaged vertebrate muscle power", "lo": null, "hi": 730, "units": "W/kg muscle",
      "status": "satisfied",
      "satisfied_by": "Blue-breasted quail (Coturnix chinensis) pectoralis take-off: mean 390 W/kg (calculated), 530 W/kg one individual (calculated), 433 W/kg in-vitro bundles (measured); review: cycle-average record ~400 W/kg, instantaneous ~1200 W/kg (instantaneous exceeds 730).",
      "satisfied_evidence": "literature",
      "note": "Askew, Marsh & Ellington 2001 J Exp Biol 204; Askew & Marsh 2002 J Exp Biol 205:2153. Read-level: search-summary only (journal host unreachable from session). Bird, not zebrafish: used only as a vertebrate ceiling."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The modelled animal's total pectoral muscle mass (both fins) must lie below the lower bound of the computed threshold",
      "quantity": "M_pectoral(both fins)/M_body, zebrafish", "lo": null, "hi": 7.5, "units": "% body mass",
      "status": "open",
      "satisfied_by": "Zebrafish value unknown: no gravimetric measurement found. Cross-species only: Abudefduf saxatilis 0.69% per fin (1.38% both, doubling is derived); Latimeria 0.43% per fin.",
      "satisfied_evidence": "unknown",
      "note": "Mansuit & Herrel 2021 Front Ecol Evol 9:702576 Table 1, full-text (Abudefduf is the only actinopterygian mass-fraction row; likely from Thorsen & Westneat 2005, which is my inference). Zebrafish search scope: two web searches for adult pectoral abductor/adductor mass; returned anatomy only (Thorsen & Hale 2005, Patterson & Devoto 2008, Siomava & Diogo not retrieved). Pomacentrid is not zebrafish, so it cannot satisfy this constraint."},
    {"target_scale": "organ", "kind": "existence",
      "statement": "Any teleost that powers aerial pectoral flapping must carry pectoral muscle at or above the computed threshold, and teleosts near 1-2% must not",
      "quantity": "M_pectoral/M_body in aerial teleosts", "lo": 7.5, "hi": null, "units": "% body mass",
      "status": "open",
      "satisfied_by": "Gasteropelecidae (hatchetfish, Ostariophysi) reported 'up to 25%' pectoral muscle (popular sources; no primary measurement found). Wiest 1995 reportedly shows fins used to leave water but not beaten airborne; popular sources disagree. Consistent with the threshold if true, but cross-species and unverified.",
      "satisfied_evidence": "literature",
      "note": "Animal Diversity Web / Wikipedia Gasteropelecidae (search-summary); Wiest 1995 J Zool 236:571-592 (listing only, via seriouslyfish.com). Hatchetfish, not zebrafish: cannot confirm or refute. Exocoetid gliding not re-checked this session and not used."}
  ]}
```
