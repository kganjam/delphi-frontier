# Claim 225: entailment to the organ and behaviour scales

**Source claim (S29's, not mine).** Scale: organism. Evidence: derived.

> SPRING VOLUME PASSES: 1–4 % of body volume as mammal-grade tendon, 13–24 % at measured fish-tendon strains.

**Where it comes from.** `docs/research/fish/S29-organism.md` §2.4 and §6, on branch `claude/s29-launch-energy-2iuixr`. I read the whole file (read level: full-text).

**Prior reviews I read in full** (read level: full-text):
- Challenge 225 (`claude/challenge-spring-volume-passes-0y7v5t`). Verdict: WEAKENED. Its corrected range is 1.8–4.1 % at working stress and 13–30 % with fish return.
- Challenge 224 (`claude/c-start-spring-energy-chv9eu`). It finds that the stored energy of 11.83 mJ is a lower bound, with a range of 10.9–19.0 mJ.

**What the claim is.** It says that a launch spring storing 11.83 mJ fits inside a 0.40 g teleost (body volume 381 mm³).
- The 1–4 % figure is collagen loaded to 100 or 50 MPa at E = 1.65 GPa (sheep tendon).
- The 13–24 % figure is tuna caudal tendon (E 1.2 or 0.65 GPa) at the 2 % strain measured at burst.

**Calculations.** Every number marked *calculated* below is printed by `docs/research/fish/claim_225_entail.py`. None of them is an observation.

## 1. Entailed constraints

If the claim is true, five things must hold at the adjacent scales.

| # | Scale | Kind | Requirement (generic) | Bound |
|---|---|---|---|---|
| C1 | organ | range | The axial collagenous element of a teleost must store elastic energy at its in-use load, at a density that keeps the spring within the claimed volume. | u ∈ [0.130, 3.04] MJ m⁻³ |
| C2 | organ | range | That element must survive the stress the mammal-grade branch assumes. | failure stress ≥ 50 MPa (≥ 100 MPa for the 1 % end) |
| C3 | organ | spatial | The loading muscle must be able to shorten far enough, at force, to put the stored energy into the spring in one loading stroke. The muscle's excursion must match the spring's required stretch. | fibre strain 0.28–1.11 |
| C4 | behaviour | timescale | A loading-and-hold phase must exist that is slow compared with the 5–14 ms release, so that the muscle escapes its force–velocity penalty. A held latch phase must come before the launch. | loading ≥ ~50 ms, i.e. ≥ ~10× release |
| C5 | behaviour | range | During the launch behaviour itself, the element must actually be strained to the level the volume figure assumes. | ≥ 2 % (fish branch); 3.0–6.1 % (mammal branch) |

**How the bounds were derived** (all calculated):
- **C1:** u = W / V. The bound 0.130 corresponds to 23.9 % of the body; the bound 3.04 corresponds to 1.02 %.
- **C3:** fibre strain ε = W / (σ_iso · V_muscle). The low end, 0.28, is all skeletal muscle (60 % of body) under ideal constant-force loading. The high end, 1.11, is one side of the body (30 %) loading a linear spring.
- **C5:** the mammal-branch strain is σ/E = 50/1.65 to 100/1.65.

I did not add separate `energetic` or `conservation` constraints. The energy that must flow into the spring is S29's own binding term (energy per stroke), and C3 restates it as a length-scale match. Challenge 225 §3 already notes that the volume "pass" and the energy "fail" are the same constraint seen twice.

## 2. Checks

### C1 — organ, range: in-use energy density of the axial collagen ≥ 0.130 MJ m⁻³

**Status: satisfied, for tuna-grade tendon only. Zebrafish-grade tendon falls outside the band.**

**What satisfies it: tuna caudal tendon.** Shadwick (SICB abstract, "Structure and Function of Axial Tendons in Tunas") gives E = 0.65–1.2 GPa and 7–25 % dissipation in excised skipjack and yellowfin tendon. Read level: search-summary of the abstract. The 1.5–2 % burst strain is taken from S29's report of the same abstract; my search did not return the strain number.
- At 2 % strain this gives u = 0.130–0.240 MJ m⁻³ (calculated), which meets the lower bound.
- This is circular. The 13–24 % row of the claim is built from exactly these inputs, so the check confirms the arithmetic, not new biology.

**The source disagrees with the claim's use of it.** The same abstract concludes that *"the caudal tendons in tunas do not function as energy saving locomotor springs, even at maximal swimming effort"*, and that the strain energy stored is *"insignificant compared to the work done by the muscle"* (search-summary). That is a statement about how tuna use the tendon, not about what the material can do. A 2013 ISB poster hypothesises the opposite: that caudal tendons store energy slowly and release it quickly. That is untested (search-summary). I am preserving this disagreement, not resolving it.

**Zebrafish tendon misses the band.** Shah et al. 2015 (J. Orthop. Res. 33:867) measured zebrafish *craniofacial* tendon at a linear modulus of **515 ± 152 MPa**. Read level: search-summary of the abstract. The full ZFIN record returned HTTP 503.
- At 2 % strain this gives u = 0.103 MJ m⁻³ (calculated). The spring would then be **30.1 % of body volume**, which is outside the claim's 13–24 %.
- *My inference:* these are craniofacial tendons, not axial or myoseptal tendons. No modulus for zebrafish axial tendon was found, so the transfer is uncertain in either direction.

### C2 — organ, range: failure stress of teleost axial tendon ≥ 50 MPa

**Status: unsatisfied. No measured value was found within my search scope.**

**Searches** (three standard web searches):
- "fish tendon tensile strength ultimate stress MPa teleost myoseptal tendon"
- "tuna tendon tensile strength breaking stress MPa fish collagen"
- "Summers Koob 2002 evolution of tendon … failure stress"

**What turned up, and why none of it settles the question:**
- A rainbow-trout epicentral tendon–vertebra attachment tensile study (uOttawa repository). The snippet gave no strength number, and I did not read it.
- Summers & Koob 2002 (Comp. Biochem. Physiol. A 133:1159), which may hold comparative data. Listing only; I could not access it.
- Shadwick's tuna work gives modulus and dissipation, not strength.
- Mammal and bird tendon strengths are known. For example, turkey tendons measure 67–112 MPa (PMC3459684, search-summary). These are not teleost values.

**Scope of the negative.** This finding means I found no number. It does not mean people looked and found nothing. I cannot distinguish "never measured" from "measured but not reached by my search", because two candidate sources were inaccessible and the session network policy blocks `sicb.org`.

**Effect on the claim.** Until a teleost tendon is shown to tolerate 50–100 MPa, the "1–4 % as mammal-grade tendon" branch is a statement about mammalian material only. Challenge 225 adds that 100 MPa is roughly the fracture stress of mammalian tendon (Ker, Alexander & Bennett 1988, search-summary).

### C3 — organ, spatial: loading-muscle fibre strain of 0.28–1.11 in one stroke

**Status: unsatisfied. Not unsatisfiable, for the reason given at the end of this section.**

**What is required** (calculated). The inputs are:
- W = 11.83 mJ
- σ_iso = 186 kPa for cod fast skinned fibres (Altringham & Johnston 1982, as used by challenge 225; read level: search-summary via that note; I did not re-read it)

| Loading muscle | Muscle volume | Fibre strain needed (constant force) | Fibre strain needed (linear spring) |
|---|---|---|---|
| One side (30 % of body) | 114 mm³ | 56 % | 111 % |
| All skeletal muscle (60 %) | 229 mm³ | 28 % | 56 % |

**What has been measured.** Spierts & van Leeuwen 1999 (J. Exp. Biol. 202:393, carp C- and S-starts) report white-muscle sarcomere strains up to about **16 %** in C-starts, and about 27 % in red fibres. Read level: search-summary of the abstract and text extracts.
- The same extracts also give anterior white strains of 24 % against posterior 10 %. From the abstract, this split appears to belong to the S-starts.
- The extracts contradict each other on whether anterior and posterior strains are similar. I report both figures as given.
- Wakeling & Johnston 1999 (carp white muscle strain, sonomicrometry, 70 fast-starts) was found, but its strain values were not in the summary. Read level: listing.

**Comparison** (calculated). At σ_iso with 16–24 % strain, the most work one loading stroke can put in is 28–43 J kg⁻¹ of muscle under constant force. That is below the 98.5 J kg⁻¹ S29 requires for one side, and below 49 J kg⁻¹ for all skeletal muscle.

**This calculation conflicts with a direct measurement.** Mendoza & Azizi 2021 measured frog muscle loading its own tendon at 53 J kg⁻¹ on average (range 32–81). That figure comes via S29, which read the full text. It exceeds my σε cap, so either frog muscle runs at higher stress or strain, or skinned-fibre σ_iso underestimates intact muscle. I am recording the conflict, not resolving it.

**Why this is not unsatisfiable.** The 16 % is the strain a carp *uses* in a reflex C-start. It is not a measured strain *capacity* under slow loading. No measured value contradicts a fish myotome shortening 28 % at force. If a measured working-range limit of ≤ 24 % turns up for teleost fast fibres, then C3 becomes unsatisfiable for every muscle fraction, and the claim fails from below.

### C4 — behaviour, timescale: a loading-and-hold phase ≥ ~50 ms before a 5–14 ms release

**Status: satisfied in teleost feeding behaviour. Not found in any teleost locomotor behaviour.**

**Satisfied by: syngnathiform pre-strike loading.** Van Wassenbergh, Strother, Flammang, Ferry-Graham & Aerts 2008 (J. R. Soc. Interface 5:285) studied the bay pipefish.
- Epaxial muscle activity often began **> 300 ms** before the first visible capture motion. Head and hyoid rotation are held back during that period, which the authors read as energy storage in the epaxial tendons. Read level: search-summary of the abstract.
- A 2014 seahorse paper by the same lead author states the figure as "≥ 200 ms before head rotation" (search-summary). The two use different reference points, so I do not read this as a conflict.
- The ratio is ≥ 300 / 5 ≈ 60× the release time (calculated), so the constraint is met.

**Not met in locomotion.** Zebrafish escape C-starts are Mauthner-initiated. Their latency from stimulus to response is **about 5–10 ms**, and the cut-off between short- and long-latency responses is 13–18 ms across 23–27 °C. These figures are from larval zebrafish (review and ZFIN figure summaries, read level: search-summary). There is no preparatory loading phase.

**My inference, not a sourced claim.** A spring-loaded launch therefore cannot be the existing startle escape with a spring attached. It needs a new, voluntary, pre-loaded behaviour lasting ≥ 50 ms. In pipefish that pattern exists, but only in feeding.

**Scope.** I ran two standard searches on pipefish pre-strike timing and zebrafish C-start latency. I did not survey locomotor behaviour in other teleosts for a held pre-launch posture, so "not found in locomotion" is limited to those searches.

### C5 — behaviour, range: in-use strain at launch ≥ 2 % (fish branch) or 3.0–6.1 % (mammal branch)

**Status: unsatisfied for the mammal branch. The fish branch is met only at its boundary.**

**Measured in behaviour.** Tuna caudal tendon reaches strain below 1 % in steady swimming and 1.5–2 % at maximal burst (Shadwick abstract, as reported by S29; my search did not return the strain number). The fish branch uses exactly 2 %, the measured maximum. It is satisfied only at the edge of the measured range, with no margin.

**Mammal branch** (calculated). At E = 1.65 GPa it needs 3.0–6.1 % strain. At the zebrafish modulus (515 MPa), the same energy density needs **5.4–10.8 % strain at 28–56 MPa**.
- No teleost tendon has been observed at these strains in any behaviour I found.
- *My inference:* the upper end of 10.8 % approaches the 10–15 % failure strain that a general tendon review gives for (non-fish) tendon (search-summary).

**Scope.** I found measurements in tuna only. I found no in-vivo tendon or myoseptum strain for any cyprinid.

## 3. What this does to claim 225

No constraint is **unsatisfiable**. I found no measured number that contradicts any of them, so the claim is **not refuted from below**.

| Constraint | Result |
|---|---|
| C1 | Satisfied only by the claim's own tuna inputs. The one measured zebrafish tendon modulus puts the spring at 30 % of the body, outside the stated band. |
| C2 | Unsatisfied. No teleost tendon strength was found. The "mammal-grade" branch is a mammalian number. |
| C3 | Unsatisfied. At measured carp C-start strains (≤ 16–24 %), fish muscle cannot fill the spring in one stroke. Fish strain capacity under slow loading is unmeasured. This is the constraint closest to unsatisfiable. |
| C4 | Satisfied in feeding (pipefish). Absent in locomotion, where the zebrafish escape is a 5–10 ms reflex. |
| C5 | Fish branch met only at its measured edge. Mammal branch unsatisfied. |

**Narrower statement the evidence supports** (my wording): the spring fits *by volume* only for a tuna-grade axial tendon strained to its maximum observed in-use strain. Nothing measured at the organ or behaviour scale yet supports a teleost tendon working at mammalian stress. Nothing measured shows a fish muscle that can load such a spring in one stroke.

**Most decisive measurements, in order:**
1. **Maximum fast-fibre strain at force in a teleost myotome under slow loading.** If it is ≤ 24 %, C3 is unsatisfiable.
2. **Failure stress of teleost axial or myoseptal tendon.** This settles C2.
3. **Modulus of zebrafish axial tendon.** This settles whether C1 lands at 13–24 % or at about 30 %.

## Sources

| Source | Used for | Read level |
|---|---|---|
| S29-organism.md (`claude/s29-launch-energy-2iuixr`) | the claim and its inputs | full-text |
| challenge-225.md and challenge-224.md | prior reviews; the cod σ_iso | full-text |
| [Shadwick, Structure and Function of Axial Tendons in Tunas (SICB abstract)](https://sicb.org/?p=36037) | E, dissipation, conclusion | search-summary (fetch blocked: `sicb.org` is outside the network allowlist) |
| [ISB 2013 poster ps2-21a](https://media.isbweb.org/images/conferences/isb-congresses/2013/poster/ps2-21a.pdf) | the opposing hypothesis | search-summary |
| [Shah et al. 2015, J. Orthop. Res. 33:867](https://www.zfin.org/ZDB-PUB-150211-17) | zebrafish tendon 515 ± 152 MPa | search-summary (ZFIN returned HTTP 503) |
| [Spierts & van Leeuwen 1999, J. Exp. Biol. 202:393](https://cob.silverchair.com/jeb/article-pdf/202/4/393/2597183/jexbio_202_4_393.pdf) | carp C-start sarcomere strain | search-summary |
| [Wakeling & Johnston 1999, carp white muscle strain](https://research-portal.st-andrews.ac.uk/en/publications/white-muscle-strain-in-the-common-carp-and-red-to-white-muscle-ge/) | existence of sonomicrometry data; no number used | listing |
| [Van Wassenbergh et al. 2008, J. R. Soc. Interface 5:285](https://researchwith.njit.edu/en/publications/extremely-fast-prey-capture-in-pipefish-is-powered-by-elastic-rec/) | > 300 ms pre-strike loading | search-summary |
| [Zebrafish startle latency (ConductScience protocol)](https://conductscience.com/conductvision/zebrafish-startle) and [ZFIN ZDB-PUB-150512-4 figures](https://zfin.org/action/publication/ZDB-PUB-150512-4/all-figures) | 5–10 ms latency; 13 ms cut-off | search-summary |
| [Turkey tendon strength, PMC3459684](https://pmc.ncbi.nlm.nih.gov/articles/PMC3459684) | non-teleost comparison only | search-summary |
| Summers & Koob 2002, Comp. Biochem. Physiol. A 133:1159 | possible teleost tendon data | listing (could not access) |

```swarm-entail
{"source_claim": 225, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The teleost axial collagenous element must store elastic energy at its in-use load at a density that keeps an 11.83 mJ spring within 1-24% of body volume",
      "quantity": "elastic energy density at in-use load", "lo": 0.130, "hi": 3.04, "units": "MJ m^-3",
      "status": "satisfied",
      "satisfied_by": "Tuna caudal tendon, E 0.65-1.2 GPa at measured 2% burst strain -> 0.130-0.240 MJ m^-3 (calculated from measured inputs; these are the claim's own inputs, so the check is circular)",
      "satisfied_evidence": "derived",
      "note": "Shadwick SICB abstract (search-summary). Shadwick concludes that tuna caudal tendons are NOT energy-saving springs even at maximal effort; a 2013 ISB poster hypothesises the opposite (untested). Disagreement preserved. Zebrafish craniofacial tendon E 515+/-152 MPa (Shah et al. 2015 J Orthop Res 33:867, search-summary) at 2% strain gives 0.103 MJ m^-3 -> 30.1% of body, outside the band; no zebrafish axial-tendon modulus found."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The teleost axial tendon must tolerate the working stress assumed by the mammal-grade branch without failure",
      "quantity": "tensile failure stress", "lo": 50, "hi": 100, "units": "MPa",
      "status": "unsatisfied",
      "satisfied_by": "No measured failure stress for any teleost axial or myoseptal tendon was found",
      "satisfied_evidence": "unknown",
      "note": "Scope: 3 standard web searches (teleost/myoseptal tendon strength; tuna tendon breaking stress; Summers & Koob 2002). Summers & Koob 2002 CBP-A 133:1159 (listing, could not access) and a trout epicentral tendon attachment study (no number in snippet) are candidate sources not read; sicb.org is blocked. This is 'not found by me', not 'looked for and absent'. Mammal tendon fracture is ~100 MPa (Ker, Alexander & Bennett 1988, via challenge-225, search-summary)."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "The loading muscle's excursion at force must match the stretch needed to put the stored energy into the spring in a single loading stroke",
      "quantity": "required fibre strain of loading muscle (60% body/constant force .. 30% body/linear spring)", "lo": 0.28, "hi": 1.11, "units": "dimensionless strain",
      "status": "unsatisfied",
      "satisfied_by": "Measured carp C-start white sarcomere strain max ~16% (anterior 24% vs posterior 10%, apparently in S-starts; extracts disagree); at cod sigma_iso 186 kPa this caps single-stroke work at 28-43 J/kg muscle (calculated) vs 49-98.5 J/kg required",
      "satisfied_evidence": "literature",
      "note": "Spierts & van Leeuwen 1999 J Exp Biol 202:393 (search-summary); Altringham & Johnston 1982 sigma_iso via challenge-225 (search-summary). Not unsatisfiable: 16% is the strain used in a reflex C-start, not a measured strain capacity under slow loading; frog in-situ spring loading of 53 (32-81) J/kg (Mendoza & Azizi 2021, via S29) exceeds my sigma*epsilon cap, so the cap may be low. A measured teleost working-range limit of <=24% would make this unsatisfiable."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "A slow loading-and-hold phase must precede the release and be long compared with the 5-14 ms release",
      "quantity": "duration of pre-release loading phase", "lo": 50, "hi": null, "units": "ms",
      "status": "satisfied",
      "satisfied_by": "Bay pipefish pre-strike epaxial activity >300 ms before visible capture motion, with head/hyoid rotation held (feeding, Syngnathiformes); NOT found in any teleost locomotor behaviour: zebrafish Mauthner C-start latency is ~5-10 ms with no preparatory phase",
      "satisfied_evidence": "measured",
      "note": "Van Wassenbergh et al. 2008 J R Soc Interface 5:285 (search-summary); larval zebrafish startle latency 5-10 ms, SLC/LLC cutoff 13-18 ms (search-summary). Satisfied in feeding only; a locomotor launch would need a new voluntary pre-loaded behaviour (my inference). Scope: 2 standard searches; no survey of held pre-launch postures across teleost locomotion."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "During the launch behaviour the elastic element must actually reach the strain the volume figure assumes",
      "quantity": "in-use tendon strain at launch (fish branch lo; mammal branch at E 1.65 GPa hi)", "lo": 2.0, "hi": 6.1, "units": "%",
      "status": "unsatisfied",
      "satisfied_by": "Tuna caudal tendon reaches 1.5-2% at maximal burst, so the fish branch is met only at the measured edge; no teleost tendon observed at 3.0-6.1% (or 5.4-10.8% at the zebrafish modulus) in any behaviour",
      "satisfied_evidence": "literature",
      "note": "Shadwick SICB abstract, strain value as reported by S29 (abstract); my own search returned the modulus and dissipation but not the strain. Scope: tuna only; no in-vivo tendon/myoseptum strain found for any cyprinid. Observed in-use strain is not a capacity limit, so this is unsatisfied, not unsatisfiable."}
  ]}
```
