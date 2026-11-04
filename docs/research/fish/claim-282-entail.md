# Claim 282 — entailment at the adjacent scale (`dna` → `protein`)

**Source claim (scale `dna`, evidence: derived).**

> THE STACK IS REFUTED BY THE PROJECT'S OWN CRITERION: six required capabilities contain NO
> demonstrated zebrafish edit — membrane stiffness, launch power, aerial stability, vestibular and
> visual function in air, aerial gas exchange, and mass reduction. Two demonstrated alleles out of
> eight required slots is not a buildable stack

**Adjacent scale propagated to:** `protein`.

**Date of all checks:** 2026-11-04. Database reads were made on that date against live NCBI
endpoints. Re-read before relying on them.

---

## 0. What kind of claim this is, and what it can therefore entail

Claim 282 is a **coverage claim about the published record**, not a physical claim about an
organism. Its content is a tally: six of eight capability slots have no demonstrated zebrafish
allele. Its conclusion — "not a buildable stack" — is a physical claim.

This distinction governs every verdict below, so I state it before any checking. A tally over the
literature entails, at protein scale, only that **nobody has reported a protein-level effector
meeting each requirement**. It does not entail that no such effector can exist. So the constraints
below are written as the requirements that would have to be met *for a slot to be fillable at all*,
and their verdicts answer a question the claim does not itself answer: for each slot, is the
absence of a demonstrated edit an **evidential** gap (nobody looked) or a **physical** one (the
requirement is contradicted by measurement)?

That is the useful work available here. If a slot's requirement turned out to be contradicted by a
measured zebrafish number, claim 282's conclusion would be right for a reason the claim does not
give. If instead every slot's requirement is merely unexamined, the claim's conclusion overreaches
in exactly the way the adversarial review on `claude/challenge-282-zebrafish-stack-kldm62` found.
**The checks below came out the second way, with one directional finding that cuts in the claim's
favour.**

### Two carried-over limitations I did not re-litigate

1. **The cited source `S15-dna.md` is absent** from this repository and its full git history
   (established in `challenge-282.md`; I re-confirmed `find . -iname "*S15*"` → 0 hits in the
   working tree). Read-level: **could-not-access**. So "the project's own criterion" for a
   buildable stack, the eight-slot denominator, and the identity of the two demonstrated alleles
   are all **unverifiable here**. I take the six named capabilities from the claim text as quoted
   and check requirements against them; I cannot check the tally itself.
2. Because the criterion is unreadable, **every "required value" below is unknown**. I can measure
   what zebrafish *has*; I cannot measure what the project says it *needs*. Several constraints are
   `open` for this reason alone, and that is a statement about the missing document, not about the
   fish.

### The sixth slot has no protein-scale entailment

Five of the six named capabilities reduce to a protein-scale requirement. **Mass reduction** does
not: it is a whole-body composition quantity, and "less mass" names no protein property that could
be bounded. I record this rather than inventing a constraint to fill the slot. *My inference, not
the author's:* a slot whose requirement cannot be stated at the adjacent scale is weak evidence for
a conclusion about buildability, because there is nothing there to check in either direction.

### Control on my own searches (repo Rule 8)

Both directions, run against the same PubMed endpoint used for every negative below:

| control | expectation | result |
| --- | --- | --- |
| `zzzqqxx+nonexistent+term+9999` | must come back empty | `Count = 0` |
| `zebrafish` | must come back found | `Count = 68082` |

The must-fail term is genuinely impossible rather than merely unfamiliar. The endpoint can return
zero, so the zeros below are measurements and not silent failures.

---

## 1. ENTAIL — what claim 282 requires at `protein`

| id | kind | slot | requirement |
|----|------|------|-------------|
| C1 | spatial | vestibular & **visual** function in air | In air, the eye's optical focal length must match the lens-to-retina distance within a few percent, or no image forms on the retina. A protein-scale effector must be able to retune the refractive gradient or corneal curvature by that amount. |
| C2 | range | membrane stiffness | The flexural stiffness of the fin, set by its structural proteins, must reach the value that holds an aerial lifting surface against aerodynamic load. |
| C3 | timescale | **vestibular** function in air | Sensory mechanotransduction must be fast relative to the body-rotation timescale of an unsupported aerial trajectory, or attitude feedback arrives too late to use. |
| C4 | energetic | launch power | Contractile protein power density must reach the mass-specific power the launch requires. |
| C5 | conservation | aerial gas exchange | Oxygen flux across an air-exposed surface must balance aerobic demand, with no water-ventilated gill available. |

C1, C2 and C3 are checkable against measured numbers with no simulation. C4 and C5 each need a
required value that the inaccessible criterion would have supplied.

---

## 2. CHECK — each constraint

### C1 — spatial: aerial focal length must match retinal radius — **unsatisfied**, and the one known allele moves the wrong way

This is the most informative result in the document, and it **supports claim 282's accounting for
this slot** while resting on a zebrafish measurement rather than a flying-fish one.

**Measured baseline, zebrafish, read-level abstract** (Collery RF, Veth KN, Dubis AM, Carroll J,
Link BA, *PLoS One* 2014;9(10):e110699, doi:10.1371/journal.pone.0110699; erratum *PLoS One*
2015;10(3):e0119779; SD-OCT on live zebrafish):

- "Ray-traced focal lengths of wild-type zebrafish lenses were **equal to their retinal radii**."
  The wild-type zebrafish eye is optically matched — *in water*.
- `lrp2` mutants "had longer retinal radii than focal lengths," with relative refractive error
  **−0.327** versus wild type.
- Dark-reared wild types: relative refractive error **−0.132** versus light-reared siblings.

Note the authors' quantity is *relative refractive error* (their stated definition: difference
between observed retinal radial length and controls), not dioptres. I do not convert it; the
conversion needs the full-text geometry I could not read.

**Corroborating optical geometry, zebrafish, read-level search-summary** (an OCT-based GRIN lens
model with ray tracing; I read a search engine's summary, not the paper): lens focal length
1.22 mm for a 0.96 mm diameter lens at 800 nm, giving Matthiessen's ratio **2.54**, inside the
2.19–2.82 range reported across fish lenses. The host carrying this paper
(`cob.silverchair.com`) **does not resolve from this session** — read-level
**could-not-access** for the primary text. These numbers are *modelled from measured geometry*,
not directly measured focal lengths, and the summary says so.

**The direction of the air shift — and here the animal changes.** That a water-adapted eye becomes
myopic in air follows from refractive-index matching: the cornea (n ≈ 1.37) has almost no power in
water (n ≈ 1.33) and gains strong positive power in air, so the focus moves in front of the retina.
The quantitative statement I could find for this in fish — lens power change of **20–30 dioptres** —
is from **Baylor 1967, *Nature* 214:307** (read-level: abstract/search-summary), and that paper is
about **flying fish (Exocoetidae)**, not zebrafish.

**Verdict, with both animals named.** The requirement is **unsatisfied**, not unsatisfiable:

- The measurement establishing that the zebrafish eye is matched in water is about **zebrafish**
  (Collery 2014). The measurement giving the magnitude of the air-induced defocus is about
  **flying fish** (Baylor 1967). Those are different animals, so I do **not** declare the
  constraint unsatisfiable — I have no zebrafish measurement of aerial refractive state at all
  (`zebrafish+refractive+state+emmetropia+air` → `Count = 0`).
- What I can say from zebrafish numbers alone: the field is active — `zebrafish+myopia` returns
  **45** records — and across it, the alleles and manipulations reported to shift zebrafish
  refractive state (`lrp2`, dark-rearing) shift it **more myopic**, i.e. **the opposite of the
  direction air requires**. *This is my inference from Collery's signs, not a claim Collery makes;*
  Collery's paper is about myopia modelling and says nothing about air.
- Scope of the negative: PubMed, 2026-11-04, `zebrafish+transgenic+cornea+curvature+allele` →
  `Count = 0`; `zebrafish+lrp2+myopia` → 3 records, all myopia-direction. These are AND-joined
  conjunctions, so a zero means *this conjunction* is empty, not that the whole topic is
  unstudied. Given 45 zebrafish myopia records exist, this is closer to **"people worked nearby
  and nobody looked at the aerial case"** than to **"people looked at the aerial case and found
  nothing."** The two are different findings and I am not merging them.

### C2 — range: fin flexural stiffness must reach the aerial-load value — **open**

**Measured, zebrafish, read-level abstract** (Puri S, Aegerter-Wilmsen T, Jaźwińska A,
Aegerter CM, "In vivo quantification of mechanical properties of caudal fins in adult zebrafish,"
*J Exp Biol* 2018;221(Pt 4):jeb171777, doi:10.1242/jeb.171777, PMID 29246971, PMC5868929):

- Overall bending stiffness **1.5×10⁻⁹ – 4×10⁻⁹ N m²** along the proximal–distal axis, measured
  *in vivo* by applying micro-Newton forces, "showing a non-monotonous pattern that was not due to
  the geometry of the fin itself."
- "Surgical disruption of the interray tissues … revealed no significant changes to the overall
  bending stiffness," so "the flexibility of the fin … predominantly relies on the mechanical
  properties of the **rays**."

The authors' own words are quoted above; the following is **my inference**: because the rays and
not the interray membrane set the stiffness, the protein-scale effector for this slot is the
mineralised ray matrix, and an edit aimed at "membrane stiffness" as the claim names it would be
aimed at the component Puri et al. measured to be mechanically irrelevant. If the project's slot is
genuinely about the *membrane*, the slot may be misspecified — but I cannot check that, because the
criterion document is missing (§0).

**Why this is `open` and not satisfied or refuted:** I have the zebrafish value and no required
value. The aerodynamic load an aerial lifting surface imposes at zebrafish scale is not something I
measured or am willing to assert — deriving it here would be a calculation presented where an
observation is needed, and the claim's own criterion for the slot is unreadable. A comparator from
a gliding species would be the obvious next step and I could not get one: a targeted search for
flying-fish pectoral fin ray rigidity or membrane stiffness returned **no measurements** (results
were popular-science overviews and the Park & Choi 2010 aerodynamics paper, which the summaries do
not report as containing stiffness values; read-level search-summary). A rainbow-trout hemitrich
flexural modulus of order **1 GPa** exists (Barthelat lab, read-level search-summary) but is
**trout, not zebrafish**, and is a material modulus rather than a structural EI.

### C3 — timescale: transduction must be fast relative to aerial body rotation — **open** (cross-species, and probably not the binding constraint)

**No zebrafish measurement exists that I could find.** Scope: PubMed
`zebrafish+hair+cell+mechanotransduction+kinetics+activation` → `Count = 0`, and a web search for
zebrafish MET channel activation time constants returned no zebrafish kinetic measurement — the one
zebrafish hit (a 2014 channelrhodopsin study) **bypasses** the MET channel by design and so cannot
measure it. Meanwhile `zebrafish+vestibular` returns **271** records, so the field is active and
this is again "nobody looked at this particular quantity," not "looked and found nothing."

**Nearest measurements, and every one is a different animal** (read-level search-summary
throughout):

| value | animal | note |
| --- | --- | --- |
| ~40 µs response latency at 22 °C | **bullfrog** saccular hair cells | corrected for epithelial electrical time constant |
| ~50 µs limiting activation time constant | **turtle** hair cells | decreased ~10-fold with stimulus amplitude |
| 50 ± 10 µs | **rat** outer hair cells | authors state it was *limited by stimulation and recording speed*, not by the channel |
| "a few microseconds" | **mouse** outer hair cells | 2021 modelling of single-channel and noise data; authors note the kinetics are too fast to measure conventionally |

Note the disagreement, which I am preserving rather than averaging: the rat figure is explicitly an
instrument-limited upper bound and the mouse figure is a model inference, so these are not four
estimates of one number.

**Verdict `open`, both sides named.** The claim is about **zebrafish**; every available number is
from **bullfrog, turtle, rat or mouse**. *Derived, not observed, and flagged as such:* taking
vertebrate hair-cell transduction at tens of microseconds against a body-rotation timescale of
order 10–100 ms for an unsupported trajectory at this body size gives a margin of roughly 10³.
**My inference:** protein-scale transduction speed is very unlikely to be what blocks this slot, so
the absence of a demonstrated edit here most plausibly reflects that no one has attempted it. That
inference does not license `satisfied` — the zebrafish number does not exist, and a three-orders-of-
magnitude margin computed from another class of animal is an argument, not a measurement.

### C4 — energetic: contractile power density must meet the launch requirement — **open**

**Zebrafish:** work-loop power output of isolated zebrafish muscle **has been measured** — Seebacher
F, Tallis J, McShea K, James RS, *Int J Obes (Lond)* 2017;41(8):1271–1278, doi:10.1038/ijo.2017.81,
PMID 28337027 (read-level **abstract**) reports "isolated muscle isometric stress, work-loop power
output and relaxation rates" in lean, obese and weight-reduced *Danio rerio*. **The abstract gives
no absolute W/kg**, only directions of change (obesity decreased work-loop power, P<0.001, not
reversed by weight loss). I could not reach the full text. Scope: PubMed
`zebrafish+muscle+power+output+work+loop` → `Count = 1`, that paper.

**Other teleosts, and they are other teleosts** (read-level search-summary): short-horn **sculpin**
peak instantaneous power **307 W kg⁻¹** (C-bend) and **222 W kg⁻¹** (contralateral contraction), wet
muscle mass, reported independent of body size; Antarctic **rock cod** fast fibres "up to
**290 W kg⁻¹**"; a **Cottidae** thesis reporting **20 W kg⁻¹** (5 °C-acclimated) and **58 W kg⁻¹**
(15 °C-acclimated) for the contralateral contraction, with work-loop values of 33 and 66 W kg⁻¹ in
the same study. The last of these disagrees with the first two by roughly a factor of five, across
method and temperature, and I am not reconciling them.

**Verdict `open`.** No zebrafish absolute power density in hand, no required value (criterion
missing), and the available absolute numbers are **sculpin, Antarctic rock cod and sculpin-family**
fish, not **zebrafish**. This is precisely the configuration the task warns about: it would be easy
to put a required launch power next to 307 W kg⁻¹ and call something refuted, and the result would
be a cross-species comparison wearing a refutation's clothes.

### C5 — conservation: aerial O₂ flux must balance demand — **unsatisfied**

**Scope of the negative, stated in full.** PubMed, 2026-11-04:
`zebrafish+aerial+respiration+air+breathing` → `Count = 0`;
`zebrafish+air+exposure+oxygen+uptake` → `Count = 0`;
`Danio+rerio+emersion+terrestrial` → `Count = 0`. Against that,
`zebrafish+hypoxia+tolerance` → **95** records. So aquatic hypoxia physiology in zebrafish is well
populated while the air-exposed case returns nothing on these three conjunctions. **Nobody appears
to have looked**, as distinct from having looked and found nothing. These are AND-joined queries and
a zero bounds the conjunction, not the topic.

**What zebrafish numbers do exist, and what they are not.** Larval zebrafish rely on **cutaneous**
O₂ transfer before gill maturation (Hughes & Perry 2021; and Parker, Zimmer & Perry 2020 measured
cutaneous O₂ flux over the yolk-sac epithelium by scanning micro-optrode — read-level
search-summary for both). I could **not** find any study partitioning whole-body zebrafish O₂
uptake into a cutaneous fraction; the one percentage my search surfaced (~41% at rest) is from
**octopus** and I am discarding it rather than repurposing it. I also could not obtain a baseline
zebrafish haemoglobin **P50** in mmHg: the likely source (Cadiz et al. 2019, *Comp Biochem Physiol
B* 234:18–25) reports that acute hypoxia *decreases* P50 but I did not reach a baseline figure —
read-level **search-summary**, and I have not checked its reported values.

**Cross-species comparator, named as such.** Mudskippers (*Periophthalmus*, *Periophthalmodon*)
accomplish aerial gas exchange cutaneously and bucco-opercularly, with *P. schlosseri* reported to
take up oxygen more effectively in air than in water (read-level search-summary, via the prior
challenge document). That is a **mudskipper**, not a **zebrafish**. It establishes that aerial gas
exchange is within the teleost repertoire — defeating any claim that the capability is impossible
for a bony fish — and establishes nothing about *Danio rerio*. Surface-to-volume ratio favours a
smaller animal for cutaneous exchange, which is the one scaling argument in this document pointing
*toward* feasibility at zebrafish size; it is an argument, not a measurement.

---

## 3. Net effect on claim 282

**No constraint came back `unsatisfiable`, and I am not reaching for one.** Nothing I measured
contradicts any of the five requirements. Claim 282 is therefore **not refuted from below**, and it
is also **not confirmed** — what the checks establish is the *character* of its six negatives:

| slot | protein-scale requirement | verdict | nature of the gap |
| --- | --- | --- | --- |
| visual function in air | C1 spatial | unsatisfied | nobody looked at the aerial case; the one allele that shifts refractive state shifts it **adversely** |
| membrane stiffness | C2 range | open | zebrafish baseline measured; required value unreadable; slot may name the mechanically irrelevant component |
| vestibular function in air | C3 timescale | open | cross-species only; margin ~10³ suggests this is **not** the blocker |
| launch power | C4 energetic | open | zebrafish power measured but no absolute value accessible; comparators are other species |
| aerial gas exchange | C5 conservation | unsatisfied | nobody looked; capability exists in another teleost |
| mass reduction | — | — | no protein-scale requirement statable |

Four of the five checked slots are **evidential** gaps with stated scope. This is what the prior
adversarial review concluded on internal grounds, now checked against the literature: the claim
establishes *undemonstrated*, not *unbuildable*.

**The one finding that strengthens the claim**, and it is worth separating out because it is the
only place a zebrafish measurement bears on a slot directionally: for the visual slot, the zebrafish
eye is optically matched in water (Collery 2014, ray-traced focal length = retinal radius), and
every zebrafish perturbation reported to move refractive state moves it *more myopic* — away from
what air demands. That is a real asymmetry, it comes from the right animal, and it means this
particular slot's emptiness is not merely an absence of effort. It still is not a refutation of
anything: no measured zebrafish number says the retuning is impossible, and the magnitude of the
required shift is known to me only from **flying fish** (Baylor 1967, 20–30 D).

**The species trap, scored.** Of the measurements I located, the ones bearing on four of five
slots are from **flying fish, mudskipper, sculpin, Antarctic rock cod, trout, bullfrog, turtle, rat
and mouse**. Exactly one slot (visual) had a usable **zebrafish** measurement. Had I treated any of
the others as refuting, I would have filed a cross-species comparison as a refutation — the error
the task describes, in the direction the task predicts.

**What would close these.** C2 and C4 need the criterion document `S15-dna.md`, which does not
exist in this repository — without a required value they cannot leave `open` no matter how much
literature is read. C1's magnitude needs a zebrafish measurement of aerial refractive state, which
appears not to exist. C3 needs zebrafish MET-channel kinetics. C5 needs a zebrafish air-exposure
respirometry study. Three session-level access limits also bound this document:
`cob.silverchair.com` and `ikarus.physik.uzh.ch` do not resolve from here (both carry primary texts
I wanted), so several numbers above sit at **search-summary** rather than full-text read-level;
those hosts would have to be allowed in the session's network settings.

```swarm-entail
{"source_claim": 282, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "spatial",
      "statement": "In air, the eye's optical focal length must match the lens-to-retina distance within a few percent for an image to form on the retina, so a protein-scale effector must be able to retune the refractive gradient or corneal curvature by the amount air imposes.",
      "quantity": "ratio of optical focal length to retinal radius in air", "lo": 0.97,
      "hi": 1.03, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish allele or mechanism found that retunes aerial refractive state, and the known perturbations move it the wrong way. ZEBRAFISH measurement (Collery 2014): ray-traced focal lengths of wild-type lenses were equal to their retinal radii -- the eye is matched IN WATER; lrp2 mutants had longer retinal radii than focal lengths (relative refractive error -0.327) and dark-reared wild types -0.132, i.e. both shifts are MORE myopic, the opposite of the direction air requires. Separately, a zebrafish GRIN-lens ray-tracing model gives focal length 1.22 mm for a 0.96 mm lens at 800 nm, Matthiessen's ratio 2.54 (within the 2.19-2.82 fish range).",
      "satisfied_evidence": "measured",
      "note": "Collery RF, Veth KN, Dubis AM, Carroll J, Link BA, PLoS One 2014;9(10):e110699, doi:10.1371/journal.pone.0110699 (erratum PLoS One 2015;10(3):e0119779), SD-OCT in live zebrafish, read-level ABSTRACT via NCBI efetch 2026-11-04. The authors' quantity is 'relative refractive error' (their definition: difference between observed retinal radial length and controls), NOT dioptres; I did not convert it. MY INFERENCE, not Collery's: the sign of lrp2 and dark-rearing effects is adverse for air -- Collery's paper concerns myopia modelling and says nothing about air. ANIMALS ON BOTH SIDES: the water-matched measurement is ZEBRAFISH; the only quantitative air-shift figure I found for a fish (lens power change 20-30 dioptres) is Baylor 1967, Nature 214:307, about FLYING FISH (Exocoetidae), read-level abstract/search-summary. Because the magnitude comes from the wrong animal this is 'unsatisfied', NOT 'unsatisfiable' -- no measured zebrafish number says the retuning is impossible. Matthiessen 2.54 figure is read-level SEARCH-SUMMARY and is MODELLED from measured geometry, not a measured focal length; its host cob.silverchair.com does not resolve from this session (read-level could-not-access for the primary text) and would need allowing in the session's network settings. NEGATIVE SCOPE, PubMed 2026-11-04: 'zebrafish+refractive+state+emmetropia+air' Count=0, 'zebrafish+transgenic+cornea+curvature+allele' Count=0, while 'zebrafish+myopia' Count=45 and 'zebrafish+lrp2+myopia' Count=3 (all myopia-direction) -- so the field is active and this is NOBODY LOOKED AT THE AERIAL CASE, not people looked and found nothing. Queries are AND-joined conjunctions, so each zero bounds the conjunction, not the topic. Search controls passed both ways: gibberish term Count=0, 'zebrafish' Count=68082."},

    {"target_scale": "protein", "kind": "range",
      "statement": "The flexural stiffness of the fin, set by its structural proteins, must reach the value needed to hold an aerial lifting surface against aerodynamic load.",
      "quantity": "caudal fin flexural stiffness EI", "lo": 1.5e-9,
      "hi": 4.0e-9, "units": "N m^2",
      "status": "open",
      "satisfied_by": "Zebrafish baseline is measured but the required value is unknown, so the comparison cannot be made. MEASURED, ZEBRAFISH: overall bending stiffness 1.5e-9 to 4e-9 N m^2 along the proximal-distal axis of the adult caudal fin, in vivo under micro-Newton forces, 'showing a non-monotonous pattern that was not due to the geometry of the fin itself'; surgical disruption of interray tissue produced no significant change, so stiffness 'predominantly relies on the mechanical properties of the rays'. The aerodynamic-load requirement is not available: the project criterion document is missing.",
      "satisfied_evidence": "measured",
      "note": "Puri S, Aegerter-Wilmsen T, Jazwinska A, Aegerter CM, J Exp Biol 2018;221(Pt 4):jeb171777, doi:10.1242/jeb.171777, PMID 29246971, PMC5868929, read-level ABSTRACT via NCBI efetch 2026-11-04 (full text at ikarus.physik.uzh.ch does not resolve from this session -- read-level could-not-access; host would need allowing in the session's network settings). The lo/hi given are the MEASURED zebrafish interval, not a requirement window -- the requirement side is unknown because S15-dna.md is absent from this repository and its entire git history (re-confirmed: find . -iname '*S15*' returns 0 hits), so this constraint cannot leave 'open' on literature alone. MY INFERENCE, not the authors': since rays and not the interray membrane set the stiffness, an edit aimed at 'membrane stiffness' as claim 282 names the slot would target the component Puri et al. measured to be mechanically irrelevant, so the slot may be misspecified -- unverifiable while the criterion is unreadable. NEGATIVE SCOPE: targeted search for flying-fish pectoral fin ray rigidity or membrane stiffness returned NO measurements (hits were popular-science overviews plus Park & Choi 2010 aerodynamics, which the summaries do not report as carrying stiffness values; read-level search-summary). Nearest material value is a rainbow TROUT hemitrich flexural modulus of order 1 GPa (Barthelat lab, read-level search-summary) -- wrong animal AND a material modulus rather than a structural EI, so not comparable. PubMed 'zebrafish+mutant+bone+mineral+density+fin+ray+stiffness' Count=0, against 'zebrafish+fin+ray+mutant' Count=27."},

    {"target_scale": "protein", "kind": "timescale",
      "statement": "Sensory mechanotransduction must be fast relative to the body-rotation timescale of an unsupported aerial trajectory, or attitude feedback arrives too late to be used for stabilisation.",
      "quantity": "ratio of mechanotransduction activation time to body-rotation timescale", "lo": null,
      "hi": 0.1, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No zebrafish measurement exists that I could find; every available number is from another animal. NEAREST MEASUREMENTS, all read-level search-summary: BULLFROG saccular hair cells ~40 us response latency at 22 C (corrected for epithelial electrical time constant); TURTLE hair cells ~50 us limiting activation time constant, decreasing ~10-fold with stimulus amplitude; RAT outer hair cells 50 +/- 10 us, which the authors state was limited by stimulation and recording speed rather than by the channel; MOUSE outer hair cells 'a few microseconds' from 2021 modelling of single-channel and noise data, the authors noting the kinetics are too fast to measure conventionally.",
      "satisfied_evidence": "literature",
      "note": "ANIMALS ON BOTH SIDES: claim 282 is about ZEBRAFISH; the four available numbers are BULLFROG, TURTLE, RAT and MOUSE. Verdict is therefore 'open' and not 'satisfied'. DISAGREEMENT PRESERVED, not averaged: the rat figure is explicitly an instrument-limited upper bound and the mouse figure is a model inference, so these are not four estimates of one quantity. DERIVED, NOT OBSERVED, and flagged as such in the document: vertebrate transduction at tens of microseconds against a body-rotation timescale of order 10-100 ms at this body size gives a margin of roughly 1e3. MY INFERENCE: protein-scale transduction speed is very unlikely to be what blocks this slot, so its empty record most plausibly reflects that nobody attempted it -- but a 1e3 margin computed from another class of animal is an argument, not a measurement, and does not license 'satisfied'. NEGATIVE SCOPE, PubMed 2026-11-04: 'zebrafish+hair+cell+mechanotransduction+kinetics+activation' Count=0 and 'zebrafish+otolith+gravity+vestibular+air' Count=0, against 'zebrafish+vestibular' Count=271 -- field active, this quantity unexamined. A web search for zebrafish MET activation time constants returned no zebrafish kinetic measurement; its single zebrafish hit (a 2014 channelrhodopsin-2 line) BYPASSES the MET channel by design and so cannot measure it. Nobody looked, as distinct from looked and found nothing."},

    {"target_scale": "protein", "kind": "energetic",
      "statement": "Contractile protein power density must reach the mass-specific mechanical power that the launch requires.",
      "quantity": "mass-specific muscle power output", "lo": null,
      "hi": null, "units": "W kg^-1 wet muscle mass",
      "status": "open",
      "satisfied_by": "Neither side of the comparison is available. ZEBRAFISH: work-loop power output of isolated Danio rerio muscle HAS been measured (Seebacher, Tallis, McShea, James) but the accessible abstract reports only directions of change -- obesity decreased work-loop power, P<0.001, not reversed by weight loss -- and NO absolute W/kg; full text not reached. OTHER TELEOSTS, read-level search-summary: short-horn SCULPIN peak instantaneous power 307 W/kg (C-bend) and 222 W/kg (contralateral contraction) of wet muscle mass, reported independent of body size; Antarctic ROCK COD fast fibres up to 290 W/kg; a COTTIDAE thesis reporting 20 W/kg (5 C-acclimated) and 58 W/kg (15 C-acclimated) for the contralateral contraction with work-loop values of 33 and 66 W/kg. Required launch power unknown: criterion document missing.",
      "satisfied_evidence": "unknown",
      "note": "Seebacher F, Tallis J, McShea K, James RS, Int J Obes (Lond) 2017;41(8):1271-1278, doi:10.1038/ijo.2017.81, PMID 28337027, read-level ABSTRACT via NCBI efetch 2026-11-04. NEGATIVE SCOPE: PubMed 'zebrafish+muscle+power+output+work+loop' Count=1, that paper alone. DISAGREEMENT PRESERVED: the Cottidae values (20-66 W/kg) differ from the sculpin and rock cod values (222-307 W/kg) by roughly a factor of five across method and temperature; I am not reconciling them. ANIMALS ON BOTH SIDES: claim 282 is about ZEBRAFISH; every absolute power density available is SCULPIN, ANTARCTIC ROCK COD or another cottid. Placing a required launch power beside 307 W/kg and declaring a refutation would file a cross-species comparison as a refutation -- the specific error this task warns against -- so the verdict is 'open'. lo/hi left null deliberately: no required window can be stated while S15-dna.md is inaccessible."},

    {"target_scale": "protein", "kind": "conservation",
      "statement": "Oxygen flux across an air-exposed respiratory surface must balance whole-body aerobic demand, with no water-ventilated gill available.",
      "quantity": "ratio of aerial O2 uptake to aerobic demand", "lo": 1.0,
      "hi": null, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "Nothing known meets it for zebrafish, and the air-exposed case appears unstudied. NEGATIVE SCOPE, PubMed 2026-11-04: 'zebrafish+aerial+respiration+air+breathing' Count=0; 'zebrafish+air+exposure+oxygen+uptake' Count=0; 'Danio+rerio+emersion+terrestrial' Count=0 -- against 'zebrafish+hypoxia+tolerance' Count=95, so aquatic hypoxia physiology is well populated while air exposure returns nothing on these three conjunctions. NOBODY APPEARS TO HAVE LOOKED, as distinct from having looked and found nothing. Queries are AND-joined, so each zero bounds the conjunction, not the topic.",
      "satisfied_evidence": "literature",
      "note": "Zebrafish numbers that do exist and what they are not: larval zebrafish rely on CUTANEOUS O2 transfer before gill maturation (Hughes & Perry 2021; Parker, Zimmer & Perry 2020 measured cutaneous O2 flux over the yolk-sac epithelium by scanning micro-optrode) -- read-level SEARCH-SUMMARY for both, and neither partitions whole-body uptake into a cutaneous fraction, which I could not find for zebrafish at all. The one such percentage my search surfaced (~41% at rest) is from OCTOPUS and I discarded it rather than repurposing it. I could NOT obtain a baseline zebrafish haemoglobin P50 in mmHg: the likely source (Cadiz et al. 2019, Comp Biochem Physiol B 234:18-25) is reported to show acute hypoxia DECREASING P50, but I did not reach a baseline figure -- read-level search-summary, values unchecked. CROSS-SPECIES COMPARATOR, NAMED AS SUCH: mudskippers (Periophthalmus, Periophthalmodon) achieve aerial gas exchange cutaneously and bucco-opercularly, with P. schlosseri reported to take up oxygen more effectively in air than in water (read-level search-summary, via challenge-282.md). That is a MUDSKIPPER, not a ZEBRAFISH: it defeats any claim that aerial gas exchange is impossible for a teleost and establishes nothing about Danio rerio, so it does not convert this verdict in either direction. Surface-to-volume ratio favours a smaller animal for cutaneous exchange -- the one scaling argument here pointing toward feasibility at zebrafish size, and it is an argument, not a measurement."}
  ]}
```
