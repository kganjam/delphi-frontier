# Claim 190: what it requires at the organ and behaviour scales, and whether the requirements are met

**Source claim (organism scale, evidence: derived).** "Granting an unmeasured 1-BL span and AR-5 fin (S=192 mm2), the wing
produces 10% of body weight at launch and ~5% at the apex."

**Origin.** S28, `docs/research/fish/S28-organism.md` §3.2, branch `origin/claude/s28-organism-design-5z0vjz`
(read-level: **full-text**, repository).

- **Subject animal:** the Daane et al. 2021 *lat4a^nr21/+; kcnh2a^lof/+* double-heterozygote **zebrafish** (*Danio rerio*).
- **Formula:** lift fraction L/W = ½ρV²·S·CL_max / (m g).
- **Inputs:**
  - m = 0.25 g (assumed, back-solved);
  - CL_max = 1.07 (project-derived);
  - V = 1.38 m/s, an in-water burst speed taken as the exit speed;
  - launch angle 45° (assumed).
- **The apex value** applies the same formula at the horizontal component, V cos 45°.

**Every number in this note that has no source beside it is a calculation.** The script is
`docs/research/fish/claim-190-entail_calc.py` (`python3 -I`). Nothing here is a new measurement.

**Disclosure.** An earlier entailment of this claim exists on `origin/claude/claim-190-entail-aqs5y9` (commit a016ea45).
- I read it before starting. So this note is **not independent** of it, and several of its bounds reappear here
  (C1, C3, C4, C5), because the arithmetic is the same.
- **Differences from that note:**
  - I re-checked the sources myself.
  - I picked up a later project figure-read of Daane's fin length (S28-D-D, commit 03d63560), which changes the
    length constraint from `open` to `satisfied`.
  - I identified and opened Miln et al. 2021.
  - I added the fin-tucked fast-swimming gait to the timescale constraint.

## Verdict

| # | Scale | Kind | Requirement | Status |
|---|---|---|---|---|
| C1 | organ | range | Spread lifting planform S ∈ [177, 216] mm² | **unsatisfied**. Nothing measured meets it. The only images of this animal's fin give 50–96 mm², and those images are lower bounds (see C1) |
| C2 | organ | spatial | Per-fin length ∈ [0.36, 0.55] SL (span ≈ 1 SL within ×1.2) | **satisfied**. Double-het median 0.463 SL, figure-read, n = 34 |
| C3 | organ | range | Whole-fin flexural stiffness EI ≥ 2.7×10⁻⁸ N m² | **unsatisfied**. No pectoral value exists. The same-species *caudal* fin measures 7–18× below |
| C4 | behaviour | range | Water-exit speed ∈ [1.32, 1.46] m/s | **unsatisfied**. Exit speed has never been measured. In-water escape peaks lie in or near the band |
| C5 | behaviour | timescale | Pectorals abducted ≤ 20 ms after exit and held ≥ 100 ms | **unsatisfied**. Never observed. The preceding fast gait is the fin-*tucked* gait |

**Nothing is `unsatisfiable`.** The two constraints under most pressure are C1 and C3. In both, the nearest measured
number is about this zebrafish, or this species, but it is **not the quantity the constraint bounds**:
- for C1, a photographed, not-fully-spread fin;
- for C3, a different fin.

A number for a related quantity cannot refute the constraint. The argument for each is under its section.

## 1. The entailments

The claim is a statement about lift. For it to describe a real animal and not only a granted geometry, five things must
hold. I take "10 %" to mean 9–11 %.

**C1 — organ, range.**
- **Requirement:** the paired fins, as spread in air, must present a combined lifting planform large enough to carry
  9–11 % of body weight at the launch speed.
- **Bound:** S = f·W / (½ρV²CL) at V = 1.38 m/s gives **S ∈ [177, 216] mm²**.
- The claim's own 192 mm² gives **9.8 %**. The "10 %" comes from S28 rounding V_to to 4.37 m/s; 192 mm² gives
  4.41 m/s. This was already recorded by replicate-190 and is immaterial.

**C2 — organ, spatial.**
- **Requirement:** each pectoral fin must be long enough that span = 2ℓ + body width (4 mm) is about one SL, within a
  factor 1.2.
- **Bound:** ℓ/SL ∈ **[0.36, 0.55]**.
- Span matters to the lift fraction only through AR, and so through the CL_max that S28 assumes for AR 5. It is
  still part of the granted premise, so it must hold.

**C3 — organ, range.**
- **Requirement:** the fin must stay near-planar under the lift it is claimed to produce. I take that to mean tip
  deflection ≤ 10 % of fin length.
- **Model:**
  - load per fin is 1.20×10⁻⁴ N (wing loading 1.25 Pa);
  - uniform-load cantilever, L = 13.5 mm, with δ = FL³/(8EI).
- **Bound:** **EI ≥ 2.7×10⁻⁸ N m²**.
- The 10 % criterion is my choice. Allowing 20 % halves the bound.

**C4 — behaviour, range.**
- **Requirement:** the fish must leave the water at the speed the 10 % was computed for.
- **Bound:** at S = 192 mm², **V_exit ∈ [1.32, 1.46] m/s**.

**C5 — behaviour, timescale.**
- **Requirement:** some behaviour must move the pectorals into a lifting posture essentially at exit. The claim says
  "at launch", so I set the abduction within ≤ 10 % of the airtime, **≤ 20 ms**.
- The fins must then stay spread at least to the apex, **≥ 99 ms**, because the claim states "~5 % at the apex".
- **Timing:** vacuum airtime at 1.38 m/s and 45° is 199 ms.

**Entailed but not listed as a sixth constraint (behaviour, range): launch angle.** The "~5 % at the apex" needs
θ ∈ [38°, 50°], which spans 6 % to 4 % (from 0.098·cos²θ). At 60° the apex value is 2.4 %, and at 90° it is 0.

The only zebrafish take-off angle I found is a Gibb-lab SICB abstract on jumps made by **stranded fish on land**. It
reports that zebrafish take-off angles "approach 90 degrees", against about 45° for *Gambusia*.
- Read-level: **search-summary**. The host `sicb.org` was unreachable, so I did not read the abstract itself.
- **Same species, different behaviour** (a tail-flip from a substrate, not a leap from water). It does not refute
  the 38–50° requirement. It shows only that a steep take-off is in this species' repertoire.
- The status of the launch-angle requirement is **open**.

**An organism-scale caveat, outside the adjacent scales.** Every fraction scales as 1/m, and m = 0.25 g is assumed.
I make no constraint of it here.

## 2. Checks

### C1 — spread planform S ∈ [177, 216] mm². **unsatisfied**

- **No measurement of spread-fin area exists for this genotype or for wild-type adult zebrafish.**
  - I confirmed that Daane et al. 2021 (*Curr. Biol.* 31:5052, PMC9172250) report fin **length** normalised to SL
    and say nothing about area. Read-level: full-text via summarizer, both passes (0–100 k and 100 k–149 k
    characters).
  - The project's own protocol for measuring it (S43, commit 18632212) exists, but it is a protocol, not a result.
- **Nearest number: same animal, related quantity.**
  - S28-D-D (branch `origin/claude/deepen-s28-sensitive-input-4x2i7x`, commit 03d63560; read-level full-text,
    repository) digitised the two double-het fin images in Daane's preprint Fig 8A.
  - It reports a planform shape factor **A/L² = 0.134** for the *adducted* fin and **0.150–0.250** for a *partly
    abducted* fin, from one fish each.
  - The author calls these **figure-reads**. I did not redo the digitisation, so for me they are relayed.
  - **My calculation:** at the measured length (0.463 SL), they give **S = 50–96 mm²**. That is **1.8–3.5× below**
    the 177 mm² floor, and L/W = 2.6–4.9 % at 1.38 m/s.
- **Why this is not `unsatisfiable`.** The quantity C1 bounds is the planform *as spread in air*. The images are:
  - of a fin the authors did not deliberately fan, photographed in anaesthesia or in water;
  - projected areas that S28-D-D itself calls a **lower bound** on true planform;
  - one fish per image.

  A lower bound below the band does not contradict the band. A fully fanned fin could still reach it.
  - S28-D-D's inference is that reaching 192 mm² needs a fully webbed sector of about 60° at radius L, which is
    2–4× the area any image shows. That is pressure, not a measured contradiction.
- **Scope of the negative.** This is "nobody has measured the spread area", not "measured and found short". Searched:
  - the Daane full text;
  - one web search on adult zebrafish pectoral morphometrics, which returned other species' tables and ZFIN caudal-fin
    records only (search-summary);
  - the project branches whose commit messages mention fin area.

### C2 — per-fin length ℓ/SL ∈ [0.36, 0.55]. **satisfied**

- **Measurement.** Daane et al. 2021, bioRxiv 10.1101/2021.03.05.434157 Fig 8B, which is the same measurement as
  published Fig 4B. S28-D-D digitised it:

  > double heterozygote pectoral length/SL median **0.463** (IQR 0.449–0.488; isolated points 0.434–0.534; n = 34);
  > wild type 0.223 (n = 7)

  Read-level for me: **relayed figure-read**. I read S28-D-D's account in full. I did not re-download the PDF or redo
  the pixel calibration.
- **My calculation:** span = 2ℓ + 4 mm is 1.03–1.11 SL across the IQR. Every point listed (0.434–0.534) lies inside
  [0.36, 0.55].
- **Same animal on both sides:** the double-het zebrafish the claim is about.
- **Caveats that remain.**
  1. The values were digitised from a plotted figure. They are not raw per-fish data.
  2. The published Fig 4B was not reachable (CDN 403, recorded by S28-D-D), so preprint ≡ published is an
     assumption based on identical legends.
  3. The length is of a fin at rest. Span in air also needs the fins held out at roughly 90° to the body. That
     requirement belongs to C5, not here.
- **Inference (mine).** C2 being satisfied does not help C1. The fin is as long as S28 assumed but, on the only
  images, about 2–4× narrower than AR 5 requires.

### C3 — whole-fin EI ≥ 2.7×10⁻⁸ N m². **unsatisfied**

- **No pectoral-fin bending stiffness has been measured in zebrafish,** for any genotype. Scope:
  - one web search on zebrafish fin-ray bending stiffness, carried by the earlier note (search-summary);
  - Puri et al. 2018, which concerns only the caudal fin;
  - project challenges 267 and 175, which concern bluegill rays.
- **Nearest measurement: same species, different fin.**
  - Source: Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM, "In vivo quantification of mechanical properties of
    caudal fins in adult zebrafish", *J. Exp. Biol.* 221:jeb171777 (2018), PMC5868929. Read-level: **full-text via
    summarizer** (this session).
  - Author's claim: "We detected overall bending moments of 1.5×10⁻⁹–4×10⁻⁹ N m² along the proximal–distal axis".
  - Method: the load was a line force from a 0.4 mm pin ("lined force attack"), on fin regions "∼5 to 8 mm" wide.
  - The authors' cross-check, scaled from bluegill, gives "between 2×10⁻⁹ and 5×10⁻⁹ N m²". The paper does not
    mention pectoral fins.
- **Comparison (my calculation).**
  - The requirement is **7–18× above** the caudal values.
  - Taken at face value, the caudal EI would bend a fin of this length to δ/L ≈ 0.7–1.8 under the claimed lift. That
    is outside the small-deflection model, and it means the fin folds rather than holding CL 1.07.
  - The case-C fin's mean chord, 7.1 mm, is close to Puri's 5–8 mm measured width. So the gap is not an artefact of
    comparing a narrow strip with a wide fin. That is my inference from the stated widths.
- **Why this is not `unsatisfiable`.** The measured number is about:
  1. the **caudal** fin, not the pectoral;
  2. **wild-type** fish, not the double het;
  3. a fin loaded in water by a pin.

  The species matches, but the organ does not. No measured pectoral value contradicts C3.
- **Disagreement inside the project, preserved and not resolved.** S28 §4 item 3 gives the leap-load requirement as
  "0.1 × 6.3e-4 = 6.3e-5 N m²", with no derivation shown. That is **~2300×** my cantilever bound.
  - On S28's number, the Puri value fails by about 10⁴×, and the bluegill-derived candidates (3.8×10⁻⁶ and
    5.65×10⁻⁴) split.
  - On mine, only the zebrafish caudal value fails.
  - I have not traced the 6.3e-4. Both requirements cannot be right.

### C4 — water-exit speed ∈ [1.32, 1.46] m/s. **unsatisfied**

- **No zebrafish water-exit speed has ever been measured,** in any genotype. Searched:
  - three web searches on adult zebrafish leaping or jumping out of water and its kinematics (search-summary). These
    found land-stranding jump studies and aquarium anecdote, and no exit kinematics;
  - one search on adult zebrafish C-start peak velocity, which found larval and goldfish work only.
- **What *was* measured is in-water escape speed. I keep the two sources separate.**

| Source | Value | Subject | Read-level (this session) |
|---|---|---|---|
| Demesmay L et al. 2025, *PLoS Biol.* 23:e3003484 | "157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants". 240 fps, manual tracking in Fiji. Fish 2.6 ± 0.2 cm (4 mo) and 3.6 ± 0.2 cm (12 mo). The stimulus was a 1 g object dropped from 30 cm | zebrafish, in water; no jumping or water exit mentioned | **full-text via summarizer** (first 100 k of 110 k characters) |
| Miln C, Ward AJW, Seebacher F 2021, *R. Soc. Open Sci.* 8:210146, PMC8025299, "Social rank and not physiological capacity determines competitive success in zebrafish" | Fast-start escape and accelerated sprint, n = 50, 120 fps. **No absolute speeds appear in the text.** They are only in Fig 1, which I did not read. The value 1.38 m/s, and the 0.45 m/s that S28 cites from this paper, do not appear in the text (the only "0.45" is a tank dimension) | zebrafish, in water | **full-text via summarizer** (text only; figure not read) |

- **Inference (mine).**
  - The band [1.32, 1.46] lies inside Demesmay's mean ± 1 SD (1.30–1.84 m/s). So it is compatible with what this
    species reaches *under water*.
  - The claim's input, 1.38 m/s, is attributed to Miln 2021, but I could **not verify** it from Miln's text. It may
    be a figure-read made elsewhere in the project (relayed via challenges 75 and 192). It is unverified by me.
  - If exit speed equalled Demesmay's mean, L/W would be 12.6 % (calculated), so the claim's "10 %" is not
    conservative with respect to speed.
  - None of this is an exit speed. Surface breaking may cost speed. The earlier note relays a guppy measurement of
    exit 1.02 m/s, which I have not read and do not use.

### C5 — abduction ≤ 20 ms after exit, held ≥ 99 ms. **unsatisfied**

- **The behaviour has never been observed.** No account was found of adult zebrafish spreading their pectorals in air.
  S28 itself says "Whether it does so has never been observed." Scope: the three leap searches under C4.
- **A relevant fact about the preceding gait.** The leap is launched from fast axial swimming, and in zebrafish that
  gait is **fin-tucked**.
  - Thorsen, Cassidy & Hale 2004, *J. Exp. Biol.* 207:4175 (PMID 15531638): larval zebrafish keep the pectoral fins
    against the body during fast swimming. The search summary of the abstract adds that adult fish tuck the fins when undulating (a paraphrase, not a verbatim quote).
    Read-level: **search-summary** (ZFIN returned 503; `cob.silverchair.com` was not attempted again after the earlier
    note recorded it as unreachable).
  - Green & Hale 2012, fictive larval preparation: at high swim frequencies the fin abductor motoneurons stopped firing (a paraphrase from the summary),
    which the authors read as active control of the fin-tucked gait. Read-level: **search-summary** (via a
    peeref listing).
- **Inference (mine), not a measurement.** For C5 to hold, the fish must switch from a gait that actively holds the
  abductors silent to full abduction within about 20 ms of exit.
  - That is a gait transition no study has looked for. It is not shown to be impossible.
  - Both sources are larval, and the adult statement is a general remark in an abstract, not a measured adult
    zebrafish value.
  - The double-het's elongated fin is also a larger, heavier fin to abduct against air drag and its own weight.
- **Rate.** I found no adult zebrafish pectoral abduction duration. The earlier note relays a larval fin-beat of
  about 28 Hz (Green et al. 2011, search-summary; half-cycle ≈ 18 ms). A larva is a different size and Reynolds
  regime, so I do not use it as evidence that C5 is met.
- **Why this is not `unsatisfiable`.** No in-air measurement exists. "The burst gait is fin-tucked" constrains where
  the fins start, not whether they can be spread after exit.

## 3. What would move these

1. **High-speed video of double-het leaps from water**, at ≥ 1000 fps, two views. One session measures C4 (exit
   speed), C5 (whether and when the fins abduct, and how long they stay spread) and the launch angle. It is the only
   experiment that touches all the behaviour-scale requirements.
2. **Planimetry of a fully fanned fin** (C1), using the S43 protocol. If A/L² stays ≤ 0.25, C1 fails by a measured
   1.8× or more and becomes `unsatisfiable` for this genotype. The area would then be measured on the same animal.
3. **One pectoral-fin EI** in the Puri rig, for wild type and double het (C3). This converts C3 either way.

## Sources and read-levels

| Source | Read-level |
|---|---|
| S28-organism.md (`origin/claude/s28-organism-design-5z0vjz`) | full-text (repository) |
| S28-D-D-deepen.md (`origin/claude/deepen-s28-sensitive-input-4x2i7x`, 03d63560); S28-deepen.md (511ecf7b, excerpts) | full-text / excerpt (repository); its figure-reads are relayed |
| Earlier claim-190 entailment (a016ea45); replicate-190 (21ab3fb0) | full-text (repository) |
| Daane et al. 2021 *Curr. Biol.* 31:5052, PMC9172250 | full-text via summarizer, both passes; no figures |
| Daane et al. 2021 bioRxiv preprint Fig 8 | not read by me; relayed via S28-D-D |
| Puri et al. 2018 *J. Exp. Biol.* 221:jeb171777, PMC5868929 | full-text via summarizer |
| Demesmay et al. 2025 *PLoS Biol.* 23:e3003484 | full-text via summarizer (first 100 k characters) |
| Miln, Ward & Seebacher 2021 *R. Soc. Open Sci.* 8:210146, PMC8025299 | full-text via summarizer (text only; Fig 1 not read); Europe PMC record: listing |
| Widrick et al. 2018 *PLoS One* 13:e0199712 (adult U_max flume; not used for a bound) | full-text via summarizer |
| Thorsen, Cassidy & Hale 2004; Green & Hale 2012 | search-summary |
| Gibb-lab SICB abstract, zebrafish land-jump take-off angle | search-summary (`sicb.org` and `experts.nau.edu` unreachable) |
| Danos & Lauder 2012 | could-not-access (`sites.harvard.edu` unreachable) |
| Royal Society publisher page for Miln 2021 | could-not-access (403) |

```swarm-entail
{"source_claim": 190, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The paired fins, as spread in air, must present a combined lifting planform large enough to carry 9-11% of body weight at the launch speed",
      "quantity": "combined spread pectoral planform area S", "lo": 177, "hi": 216, "units": "mm2",
      "status": "unsatisfied",
      "satisfied_by": "No measurement of spread-fin area exists for the double het or for wild-type adult zebrafish. The nearest values are relayed figure-reads of Daane preprint Fig 8A for the same double-het zebrafish (S28-D-D): A/L^2 0.134 adducted, 0.150-0.250 partly abducted, one fish each, giving S = 50-96 mm2 (calculated), 1.8-3.5x below the floor",
      "satisfied_evidence": "unknown",
      "note": "Not unsatisfiable: the images are photographed projected areas of a fin not deliberately fanned, which S28-D-D calls a lower bound on true planform, so they cannot contradict a requirement on the in-air spread planform. Scope: Daane 2021 Curr Biol full text (PMC9172250, summarizer; length only, no area), one web search on adult zebrafish pectoral morphometrics (search-summary), project branches mentioning fin area (S43 is a protocol, not a result). Nobody has measured it. Bound calculated at V 1.38 m/s, CL 1.07, m 0.25 g."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "Each paired fin must be long enough that the spread span is about one standard length, within a factor 1.2",
      "quantity": "pectoral fin length per fin / standard length", "lo": 0.36, "hi": 0.55, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Daane et al. 2021 bioRxiv 10.1101/2021.03.05.434157 Fig 8B (same measurement as Curr Biol Fig 4B), double-het lat4a nr21/+; kcnh2a lof/+ zebrafish: median 0.463 SL, IQR 0.449-0.488, points 0.434-0.534, n=34, as digitised by S28-D-D; span 1.03-1.11 SL (calculated)",
      "satisfied_evidence": "measured",
      "note": "Measured by Daane et al.; the value is a pixel-calibrated figure-read by S28-D-D (commit 03d63560, branch origin/claude/deepen-s28-sensitive-input-4x2i7x), relayed here, not re-digitised. Preprint-equals-published is assumed from identical legends (published image could-not-access). Same animal as the claim. Satisfying length does not satisfy area (C1)."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The lifting fin must be stiff enough to stay near-planar (tip deflection <= 10% of length) under the claimed lift load",
      "quantity": "whole-fin flexural stiffness EI", "lo": 2.7e-8, "hi": null, "units": "N m2",
      "status": "unsatisfied",
      "satisfied_by": "No pectoral-fin EI has been measured in zebrafish. The nearest measurement is the adult wild-type zebrafish CAUDAL fin in vivo, 1.5e-9 to 4e-9 N m2, 7-18x below the requirement (calculated delta/L 0.7-1.8 if it applied)",
      "satisfied_evidence": "measured",
      "note": "Puri et al. 2018 J Exp Biol 221:jeb171777, PMC5868929 (full-text via summarizer): 'overall bending moments of 1.5x10^-9-4x10^-9 N m2', line-force pin load, fin width ~5-8 mm. Same species but a different organ and genotype, so not unsatisfiable. Requirement calculated (uniform-load cantilever, 1.2e-4 N per fin, L 13.5 mm; the 10% criterion is my choice). Unresolved ~2300x disagreement with S28's stated 6.3e-5 N m2 (derivation not shown). Scope: one web search plus project challenges 267/175; no pectoral measurement exists."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The animal must leave the water at the speed for which the launch lift fraction is computed",
      "quantity": "water-exit speed", "lo": 1.32, "hi": 1.46, "units": "m/s",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish water-exit speed has been measured. In-water escape peaks exist: Demesmay et al. 2025 157 +/- 27 cm/s (controls), which brackets the band; Miln et al. 2021 values are only in Fig 1, and S28's 1.38 m/s attributed to it could not be verified from the text",
      "satisfied_evidence": "unknown",
      "note": "Demesmay L et al. 2025 PLoS Biol 23:e3003484 (full-text via summarizer; 240 fps, manual tracking, dropped-object stimulus, no water exit). Miln, Ward & Seebacher 2021 R Soc Open Sci 8:210146, PMC8025299 (full-text via summarizer, text only; n=50, 120 fps, no absolute speeds in text). Scope of the negative: three web searches on adult zebrafish leaping out of water (search-summary; found only land-stranding jumps and anecdote) and one on adult C-start peak velocity. Nobody has looked. Bound calculated at S 192 mm2."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "A behaviour must bring the paired fins from the swimming posture into a spread lifting posture within ~10% of the airtime after water exit and hold them spread at least to the apex",
      "quantity": "time from water exit to full pectoral abduction (with hold >= 0.099 s)", "lo": null, "hi": 0.020, "units": "s",
      "status": "unsatisfied",
      "satisfied_by": "In-air pectoral abduction in a zebrafish leap has never been observed; no adult abduction duration found. The fast axial gait that precedes a leap is fin-tucked (larval data, abductor motoneurons silent at high frequency), so a tucked-to-spread transition at exit would be required and has not been looked for",
      "satisfied_evidence": "unknown",
      "note": "Thorsen, Cassidy & Hale 2004 J Exp Biol 207:4175 (search-summary): larvae keep pectorals against the body in fast swimming; the abstract, as summarised, says adults tuck the fins when undulating (a paraphrase; a general statement, not a measured adult zebrafish value). Green & Hale 2012 (search-summary). Larval data, so not evidence about the adult double het either way. Scope: three web searches on zebrafish leap kinematics and pectoral use (search-summary). Airtime 199 ms and apex 99 ms at 1.38 m/s and 45 deg are calculated. Related, unlisted requirement: launch angle 38-50 deg for the ~5% apex value is open; the only zebrafish take-off angle found (~90 deg) is from jumps by fish stranded on land (Gibb-lab SICB abstract, search-summary), a different behaviour, not a refutation."}
  ]}
```
