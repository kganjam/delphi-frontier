# Claim 282 — entailment to the protein scale

**Source claim** 282, at the `dna` scale, evidence level `derived`:

> THE STACK IS REFUTED BY THE PROJECT'S OWN CRITERION: six required capabilities
> contain NO demonstrated zebrafish edit — membrane stiffness, launch power, aerial
> stability, vestibular and visual function in air, aerial gas exchange, and mass
> reduction. Two demonstrated alleles out of eight required slots is not a buildable
> stack.

**Adjacent scale propagated to:** `protein`.

---

## 0. Provenance warning — read before using this document

Claim 282 is **not in this repository**. Neither is the "project's own criterion", the
list of eight required slots, or the identity of the two alleles called demonstrated.

Scope of that negative: `git grep -il` on both branches present in the clone
(`work/frontier-foundation`, `claude/claim-282-entail-cyot51`) for `zebrafish`,
`flying fish`, `membrane stiffness`, `launch power`, `claim-282`, and `swarm-entail`;
plus a listing of `findings/`, `frontier/`, `ledger/`, `preregistrations/`, `seeds/`,
`specs/`, `results/`. There is no `docs/` directory before this commit. The only
`zebrafish` hits are in `findings/gemini-third-assessor-calibration.json` and
`findings/gemini-triage-267-problems.json`, and both concern blastomere surface-tension
mechanics in an unrelated claim, not a flight stack.

Consequence: **the claim's premises are taken as given from the task prompt and were not
verified.** I did not check that six slots are empty, that two alleles are demonstrated,
or that eight slots are required. What follows entails *from* the claim and then checks
the entailments against the literature. If the premises are wrong, section 1 still
stands as a requirement list; section 2's findings stand independently of the premises.

One check below (C1) happens to bear on a premise, and it goes against the claim. It is
reported as found.

---

## 1. ENTAIL — what claim 282 requires at the protein scale

Claim 282 is an accounting claim at the DNA scale: it says the allele ledger is too
sparse to constitute a buildable stack. For that accounting to be the *right* accounting,
each of the six capabilities it lists must genuinely be a thing that a protein-level
change can be the lever on, and the protein-level requirement must genuinely be unmet. So
the entailments at the protein scale are the requirements those capabilities impose on
proteins — and checking them can refute the claim from below (if the protein requirements
turn out to be met) or sharpen it (if they turn out to be unmet, or mis-scaled).

### C1 — `existence`

For each of the six capabilities, there must exist at least one protein whose altered
abundance, kinetics or sequence is **individually sufficient** to move the
organism-level parameter into the required range. The claim counts *alleles*, so it
presupposes single-locus sufficiency. If a capability has no single-protein lever, the
capability is not addressable by one edit and the "empty slot" framing mis-describes it —
the slot is not empty, it is the wrong shape.

### C2 — `energetic`

The contractile protein assembly of the launch musculature must deliver peak
mass-specific mechanical power at or above the level needed to reach minimum gliding
speed within one power stroke.
Bounded quantity: peak mass-specific mechanical power, W/kg wet muscle.

### C3 — `spatial`

The eye's back focal distance must match its axial length, in air, to within the eye's
depth of focus — and, for the claim's accounting to be right, that re-match must be
reachable by a change in **lens protein composition** (refractive-index gradient) alone,
without a change in lens or corneal geometry. Length scale that must match: back focal
distance against axial eye length.

### C4 — `timescale`

Oxygen supply to flight muscle — from body stores, from aerial uptake, or substituted by
anaerobic capacity — must outlast the aerial phase. Process A: onset of
performance-limiting hypoxia in flight muscle. Process B: glide duration.

### C5 — `range`

The fin's load-bearing protein matrix must have a Young's modulus high enough that an
aerodynamic surface of achievable thickness resists dynamic pressure at flight speed
without collapsing. Bounded quantity: Young's modulus of fin structural matrix, GPa.

Mass reduction is not given its own constraint; it enters C2 as the denominator of the
power requirement, and section 2's C1 finding is where it bites.

---

## 2. CHECK — each constraint against the literature

Sources and read-levels are listed in section 3. Numbers I calculated are marked
**calculated** in the sentence; everything else is quoted from a source.

### C1 — `existence` → **unsatisfied** (five of six), with one exception that cuts against the claim

**The exception, stated first because it goes against the claim we are propagating.**
Zebrafish *mstnb* loss-of-function **is** demonstrated, twice over and by two methods:
TALEN-generated *mstnb*-deficient lines showing "enhanced muscle growth with muscle fibre
hyperplasia", and a CRISPR/Cas9 *mstnb*⁻/⁻ mutant showing "a typical double-muscle
phenotype with increased muscle mass" from 5 months post-hatch (search-summary; see
section 3). That is a demonstrated zebrafish edit with an organism-level effect on
muscle, which is the "launch power" slot's subject matter.

**But — and this is my inference, not the authors' claim — it is a lever on muscle
*mass*, not on muscle *mass-specific power*.** The cited mechanism is hyperplasia (more
fibres), and one source reports "more lipids accumulated in skeletal muscle in the
*mstnb*-deficient zebrafish than in the wild-type". Nothing I read measured specific
power or power-to-weight in these mutants. So:

- For C2's numerator (total power available), *mstnb* is a real lever.
- For C2's denominator and for the separate "mass reduction" capability, *mstnb* moves
  the **wrong way**: a grass-carp *mstnb* knockout is reported at "17.5 % greater body
  weight" (different species; search-summary). Added mass raises the launch-energy and
  wing-loading requirements.

So the one demonstrated edit in this region of the stack creates a conflict *between* two
of the claim's eight slots. That is a sharper objection than "the slot is empty", and it
is an objection the claim as written does not make.

For the remaining five capabilities — membrane stiffness, aerial stability, vestibular
and visual function in air, aerial gas exchange — I found **no** report of a single
protein whose alteration is individually sufficient at the organism level.

Scope of that negative: five extended web searches (muscle power output; flying-fish
take-off and aerodynamics; amphibious fish aerial vision; fin-ray material mechanics;
air-breathing fish aerial oxygen uptake), plus the repository search in section 0. I did
**not** search ZFIN, the Zebrafish Information Network allele tables, MGI, or any
mutant-phenotype database, and I did not read full texts behind the abstracts surfaced.
This is "I looked in the general literature and did not find" — it is **not** "people
looked for a single-locus lever and established there is none". Those are different
findings and I am not merging them.

### C2 — `energetic` → **unsatisfied** (and explicitly *not* unsatisfiable)

**Measured ceiling.** Peak instantaneous power during in vivo escape responses in
*Myoxocephalus scorpius* reached **307 W/kg** wet muscle mass for the C-bend and
**222 W/kg** for the contralateral contraction, and was independent of body size. Work-loop
means across fish species run far lower, from 18.1 W/kg at 0 °C in *Notothenia coriiceps*
to 75.7 W/kg at 15 °C in *M. scorpius*; isolated dogfish white fibres reached 91 ± 14 W/kg.
The highest vertebrate figure I found is in zebrafish itself, but in larvae:
**134 ± 20 W/kg** mean work-loop power at 80 Hz, with peak shortening-phase power
**640.2 ± 151.5 W/kg** at 100 Hz. All search-summary; see section 3 for the caveat the
search itself flagged about mixing mean-cycle and peak-instantaneous protocols.

**Required value — calculated by me, not observed.** Inputs: adult zebrafish mass 5.0×10⁻⁴ kg
(from the measured statement that "adult zebrafish rarely exceed 0.5 g"); ρ_air = 1.2 kg/m³;
C_L = 0.8 **assumed** for Re ≈ 10⁴ (the wind-tunnel L/D curve for flying fish is in a
figure I could not read); axial muscle 50 % of body mass **assumed**; power-stroke
duration 25 ms **assumed** (I did not find a measured adult zebrafish C-start duration);
lift = weight at minimum glide speed.

| Case | Fin area S | v_min (calculated) | Launch KE | Required power (calculated) |
|---|---|---|---|---|
| A — generous: S ≈ body-length², far beyond any fish's pectoral area | 1.0×10⁻³ m² | 3.2 m/s | 2.6×10⁻³ J | **4.1×10² W/kg** |
| B — realistic fin area | 2.0×10⁻⁴ m² | 7.1 m/s | 1.3×10⁻² J | **2.0×10³ W/kg** |
| B′ — B with launch efficiency 0.3 (work against water during exit; assumed) | 2.0×10⁻⁴ m² | 7.1 m/s | — | **≈6.8×10³ W/kg** |

For context, the flying fish the stack is modelled on is a much larger animal: standard
length ≈ 200 mm on the wind-tunnel models, pectoral-fin aspect ratio 9.0–10.7, and a
maximum flight speed of roughly **10–20 m/s** (that speed is cited by the wind-tunnel
authors to Hertel 1966 / Fish 1990 / Davenport 1994, not measured by them).

**Verdict and why it is not `unsatisfiable`.** Case B′ exceeds the highest measured
vertebrate muscle power by roughly an order of magnitude, and case B by 3–15× depending
on which measured ceiling you compare against. But case A — the most generous assumption
set — gives 4.1×10² W/kg, which sits **above** the 307 W/kg adult in vivo figure yet
**below** the 640 W/kg larval zebrafish peak. A measured number therefore does not
contradict the constraint at its generous end.

Two further reasons I am not calling this unsatisfiable, both of which I want on the
record rather than buried:

1. The required value is **mine, calculated**, and it swings by a factor of ~16 on
   assumptions (fin area, launch efficiency, stroke duration) that I could not source.
   An unsatisfiable verdict resting on an unsourced C_L and an assumed 25 ms is not an
   unsatisfiable verdict.
2. **Elastic power amplification** is a real escape route and it lies outside this
   constraint as written. A latch-and-spring arrangement can multiply muscle power output
   by a large factor, and its spring is made of protein. I did not search for measured
   amplification factors in fish launch mechanics. A constraint on *contractile* protein
   power does not bound the amplified system.

So: `unsatisfied`, with the realistic end of the requirement exceeding every measured
value I found, and the generous end not contradicted. I looked for an `unsatisfiable`
here and did not earn one.

### C3 — `spatial` → **unsatisfied** (the known solutions are at the wrong scale)

**Measured.** The fish lens is a gradient-index sphere: central refractive index about
**1.52**, falling to **1.33–1.36** at the surface. A homogeneous lens would need an index
of **1.66** to reach the same f/r ≈ 2.5 — no protein medium reaches 1.66. Matthiessen's
ratio (focal length / lens radius) is "constant at 2.55 in most fishes", with a reported
species span from as high as 3.6 down to 2.3. One 1988 Vision Research paper prefers a
central index of **1.555** against Matthiessen's 1.50–1.54, and a surface index of 1.36
against his 1.38–1.386 — I am recording that disagreement rather than averaging it, and I
flag that the search returned that passage garbled and I could not confirm which value is
whose. All search-summary.

**Required value: unknown.** Computing the aerial requirement needs a measured zebrafish
corneal radius of curvature and a measured aerial refractive state. I did not find either
and did not calculate from guessed radii.

**The finding that matters.** The two amphibious-vision solutions I could check are
**geometric, not compositional**. In *Anableps anableps* each eye has two corneas and two
pupils feeding **one lens that is oval rather than spherical**: "light from the air passes
through a relatively flat part of the lens, like a land animal's, while water light passes
through a more curved part", and the aerial cornea's extra refraction is offset by that
shape difference. The retina is split to match, with different opsin sets dorsally and
ventrally (search-summary). The sources I read describe fixed lens and cornea *geometry*;
the search explicitly could not confirm any accommodation mechanism, so I am not claiming
one either way.

So nothing known satisfies C3 *as stated* — aerial re-match by lens protein composition
alone. The capability is real, but the demonstrated route to it is organ geometry, which
is not a protein-scale object and is poorly served by an allele count.

Scope of the negative: one extended search on amphibious fish aerial vision and one on
lens refractive index. I did not search mudskipper corneal flattening specifically (the
vision search returned nothing on mudskippers), did not search tetrapod lens
accommodation proteins, and read no full texts.

### C4 — `timescale` → **open**

Glide duration is bounded: the wind-tunnel paper cites glide distances "up to about 400 m
in 30 s" (cited by those authors to Hertel 1966 / Fish 1990 / Davenport 1994, not their
own measurement), so the aerial phase is of order seconds to tens of seconds.

I did **not** find the other side of the comparison. One extended search on air-breathing
fish returned aerial-uptake and oxygen-debt partitioning — in *Arapaima gigas* air
breathing accounted for about 80 % of oxygen-debt repayment after exercise; striped
catfish in poorly oxygenated water took in "more than 100 %" of their oxygen from air —
but **no time-to-hypoxia in seconds** for a small teleost at burst metabolic rate, and no
breath-hold duration I could compare against a 2–30 s glide. The search itself reported
that those timing figures were absent and that species-specific work (snakeheads,
climbing perch, post-burst lactate kinetics) would be needed.

Status is therefore `open`, not `unsatisfied`: I did not run the search that would give a
negative a scope.

**Unchecked inference, flagged as such.** If a breath-hold or anaerobic capacity covers
tens of seconds — which is the direction the oxygen-debt literature points, since burst
work in fish is routinely anaerobic with the debt repaid later — then "aerial gas
exchange" may require **no protein novelty at all** for a glide of this duration, and the
claim's six-empty-slots count would be one too high. I have not checked this and it must
not be read as a finding.

### C5 — `range` → **open**, with the measurement recorded and a scale objection

**Measured.** Young's modulus of lepidotrichia (fin rays) in Hawaiian stream fishes ranged
**3.67–8.40 GPa**, mean 6.48 GPa, with pelvic rays stiffest and pectoral rays least stiff.
Pectoral-ray flexural stiffness spans roughly **1×10⁻¹⁰ to 1.5×10⁻⁶ N·m²**, decreasing
exponentially along the proximo-distal span. A separate report gives distal-region moduli
of 0.11–0.67 GPa, but the search could not establish whether those were biological rays or
an engineered actuator, so I am not using them. All search-summary. No measurement of
**fin membrane** (inter-ray) tissue stiffness was returned — that is the tissue the claim
names, and it is the one with no number.

**Required value: unknown.** I did not compute the required EI and found no measured
flying-fish fin EI to compare against.

**Scale objection — my inference from the measured spans, not any author's claim.**
Flexural stiffness is E·I. Across the measured lepidotrichia data, the protein-composition
lever on E spans about **2.3×** (3.67 → 8.40 GPa), while the geometric lever on I spans
about **four orders of magnitude** in the measured EI data. If the aerodynamic requirement
is more than ~2.3× away from what a zebrafish fin already achieves, no protein edit closes
it and only geometry can. On that reading "membrane stiffness" is mis-assigned to the DNA
and protein scales, and its empty allele slot is uninformative rather than damning.

Scope of the negative on fin membrane: one extended search on fin-ray and fin-membrane
mechanics, which returned ray data only and explicitly reported no membrane measurements.
I did not search soft-tissue mechanobiology literature or collagen-network mechanics.

---

## 3. Sources and read-levels

| Source | Read-level | Used for |
|---|---|---|
| Park & Choi, *Aerodynamic characteristics of flying fish in gliding flight*, JEB 213(19):3269 — journals.biologists.com/jeb/article/213/19/3269/9762 | **full-text**, chars 0–100,000 of 157,328; Table 1 and Fig. 7 are images and were **not** read | SL ≈ 200 mm, aspect ratio 9.0–10.7, Re 1.9–2.2×10⁴ at 12 m/s, wind-tunnel speeds; 10–20 m/s and 400 m / 30 s are *cited within it* to Hertel 1966, Fish 1990, Davenport 1994 |
| Fish muscle work-loop and escape-response literature (JEB 201(10):1505; JEB 201(7):913; JEB 140(1):187; JEB 157(1):409; bioRxiv 2020.04.02.010298) | **search-summary** — surfaced and quoted via web search; no full text opened | 307 / 222 W/kg in vivo peak; 18.1–75.7 W/kg work-loop means; 91 ± 14 W/kg dogfish; 134 ± 20 W/kg and 640.2 ± 151.5 W/kg larval zebrafish |
| Adult zebrafish swimming-performance papers (PLoS ONE flume and exercise studies; PubMed 33659376) | **search-summary** | "adult zebrafish rarely exceed 0.5 g"; Ucrit 0.548 m/s = 18.0 BL/s |
| Zebrafish *mstnb* TALEN and CRISPR/Cas9 reports; grass-carp and blunt-snout-bream *mstn* knockouts | **search-summary** | demonstrated zebrafish *mstnb* edits; hyperplasia; muscle lipid accumulation; 17.5 % body-weight gain (grass carp) |
| *Anableps anableps* vision literature (PLoS ONE 10.1371/journal.pone.0005970; PubMed 21775314; PMC9556854) | **search-summary** | two corneas / two pupils / one oval lens; split retina and opsin sets; no accommodation mechanism confirmed |
| Fish lens refractive-index sources (Matthiessen's ratio summary; Vision Research 1988, deepblue.lib.umich.edu/.../0000499.pdf; Land 2012) | **search-summary**; the 1988 passage came back garbled and is flagged in C3 | 1.52 central / 1.33–1.36 surface; 1.66 homogeneous equivalent; f/r 2.55, span 2.3–3.6; the 1.555 / 1.36 disagreement |
| Fin-ray mechanics (Flammang et al. 2013 JMorph; JEB 223:jeb227140; JEB 221:jeb163360) | **search-summary** | E = 3.67–8.40 GPa, mean 6.48; EI ≈ 1×10⁻¹⁰–1.5×10⁻⁶ N·m²; **no** fin-membrane measurement returned |
| Air-breathing fish literature (J Fish Biol 2014 reviews; J Comp Physiol B 2026 *Arapaima*; JEB 226:JEB245038) | **search-summary** | aerial uptake rises with exertion; ~80 % of oxygen debt repaid aerially in *Arapaima*; **no** time-to-hypoxia or breath-hold duration |
| researchgate.net (Cypselurus take-off acceleration-logger paper, and several others) | **could-not-access** | DNS does not resolve in this session; researchgate.net would need allowing in the session's network settings. The measured flying-fish take-off velocity therefore remains **unknown** to me; I used the wind-tunnel paper's cited 10–20 m/s flight speed instead and labelled it as cited |

No ZFIN, MGI or allele database was queried. No full text behind a paywall was opened.

## 4. Net effect on claim 282

Nothing here refutes claim 282 from below — no constraint came back `unsatisfiable`, and I
say so plainly rather than dressing up C2 as one.

What the checks do is relocate the claim's force. Three of its six capabilities
(membrane stiffness, visual function in air, and — on an unchecked inference — aerial gas
exchange) look **mis-scaled**: the demonstrated solutions are organ geometry, or no
protein novelty is needed at all, so an empty allele slot is weak evidence about them. One
(launch power) has a **demonstrated zebrafish allele** the claim's count appears to miss,
and that allele moves body mass the wrong way, which is a real internal conflict in the
stack and a stronger objection than the one the claim makes. C2's power requirement
exceeds every measured vertebrate muscle value at realistic fin areas, which is the
single most load-bearing quantitative result in this document, and it is **calculated,
not measured**.

```swarm-entail
{"source_claim": 282, "source_scale": "dna",
  "constraints": [
    {"target_scale": "protein", "kind": "existence",
      "statement": "For each required capability there must exist at least one protein whose altered abundance, kinetics or sequence is individually sufficient to move the organism-level parameter into the required range, since the criterion counts single alleles.",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Found for one capability and not the other five. Zebrafish mstnb loss-of-function IS demonstrated (TALEN lines with muscle fibre hyperplasia; CRISPR/Cas9 mstnb-/- with a double-muscle phenotype from 5 months post-hatch), which is a single-locus lever on muscle relevant to the launch-power slot. MY INFERENCE, not the authors' claim: it is a lever on muscle mass, not mass-specific power (mechanism is hyperplasia; no specific-power measurement found), and it raises body mass (grass-carp mstnb KO reported at 17.5% greater body weight), which works against the mass-reduction slot. For membrane stiffness, aerial stability, vestibular and visual function in air, and aerial gas exchange: no single sufficient protein found.",
      "satisfied_evidence": "literature",
      "note": "mstnb: zebrafish TALEN and CRISPR/Cas9 reports, read-level search-summary. NEGATIVE SCOPE: five extended web searches (muscle power, flying-fish take-off/aerodynamics, amphibious aerial vision, fin-ray mechanics, air-breathing fish) plus a git grep of both branches of kganjam/delphi-frontier. ZFIN, MGI and other allele/phenotype databases were NOT queried and no full texts were opened. This is 'not found in the general literature', NOT 'people looked and established there is none'."},

    {"target_scale": "protein", "kind": "energetic",
      "statement": "The contractile protein assembly of the launch musculature must deliver peak mass-specific mechanical power at or above the level needed to reach minimum gliding speed within one power stroke.",
      "quantity": "peak mass-specific mechanical power of launch musculature",
      "lo": 410, "hi": 6800, "units": "W/kg wet muscle",
      "status": "unsatisfied",
      "satisfied_by": "Measured ceiling is below the realistic end of the requirement but not below its most generous end. Measured: 307 and 222 W/kg peak instantaneous in vivo during escape responses in Myoxocephalus scorpius, size-independent; work-loop means 18.1 W/kg (Notothenia coriiceps, 0 C) to 75.7 W/kg (M. scorpius, 15 C); 91 +/- 14 W/kg isolated dogfish white fibres; larval zebrafish 134 +/- 20 W/kg at 80 Hz with peak shortening-phase 640.2 +/- 151.5 W/kg at 100 Hz. Required range is CALCULATED BY ME, not observed: lift=weight at minimum glide speed for a 5.0e-4 kg body, giving 4.1e2 W/kg under a generous fin area of 1.0e-3 m2 and 100% launch efficiency, and ~6.8e3 W/kg at a realistic 2.0e-4 m2 with efficiency 0.3.",
      "satisfied_evidence": "measured",
      "note": "Muscle values: JEB 201(7):913, JEB 201(10):1505, JEB 140(1):187, JEB 157(1):409, bioRxiv 2020.04.02.010298 - all read-level search-summary, no full text; the search itself flagged that mean-cycle and peak-instantaneous protocols differ and should not be pooled. Body mass from 'adult zebrafish rarely exceed 0.5 g' (PLoS ONE flume study, search-summary). DELIBERATELY NOT MARKED unsatisfiable: (1) the generous case, 4.1e2 W/kg, exceeds the 307 W/kg adult figure but is BELOW the 640 W/kg larval zebrafish peak, so no measured number contradicts the constraint at that end; (2) my required value swings ~16x on C_L=0.8, 50% muscle fraction and a 25 ms stroke, all ASSUMED and unsourced - the flying-fish wind-tunnel L/D curve is in a figure I could not read, and the measured Cypselurus take-off velocity is unknown to me because researchgate.net does not resolve in this session; (3) elastic power amplification (a protein spring plus latch) lies outside a constraint on contractile power and was not searched."},

    {"target_scale": "protein", "kind": "spatial",
      "statement": "The eye's back focal distance must match its axial length in air to within the eye's depth of focus, and for an allele-count accounting to be apt that re-match must be reachable by a change in lens protein composition (refractive-index gradient) alone, without altered lens or corneal geometry.",
      "quantity": "back focal distance matched against axial eye length in air (required value unknown)",
      "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Nothing known satisfies it as stated: both amphibious-vision solutions I could check are GEOMETRIC, not compositional. Anableps anableps has two corneas and two pupils feeding one OVAL lens, aerial light passing through a flatter region and aquatic light through a more curved one, with a split retina and different dorsal/ventral opsin sets. Compositional bounds are measured and narrow: fish lens central refractive index ~1.52 falling to 1.33-1.36 at the surface, where a homogeneous lens would need 1.66 for the same f/r ~2.5; Matthiessen's ratio ~2.55 in most fishes, species span 2.3-3.6. The required aerial value is unknown: it needs a measured zebrafish corneal radius of curvature and aerial refractive state, neither of which I found, and I did not calculate from guessed radii.",
      "satisfied_evidence": "literature",
      "note": "Anableps: PLoS ONE 10.1371/journal.pone.0005970, PubMed 21775314, PMC9556854 - read-level search-summary. Lens index: Matthiessen's-ratio summary and Land 2012, search-summary. DISAGREEMENT PRESERVED, not averaged: a 1988 Vision Research paper prefers central index 1.555 against Matthiessen's 1.50-1.54 and surface 1.36 against his 1.38-1.386; the search returned that passage garbled and I could not confirm which value belongs to whom. The sources describe fixed geometry and the search could not confirm any accommodation mechanism, so I claim none either way. NEGATIVE SCOPE: one extended search on amphibious aerial vision (returned nothing on mudskippers) and one on lens refractive index; mudskipper corneal flattening was not searched specifically, no full texts read."},

    {"target_scale": "protein", "kind": "timescale",
      "statement": "Oxygen supply to flight muscle - from body stores, aerial uptake, or substituted anaerobic capacity - must outlast the aerial phase: onset of performance-limiting hypoxia must be slow relative to glide duration.",
      "quantity": "time to performance-limiting hypoxia in flight muscle, against glide duration",
      "lo": null, "hi": null, "units": "s",
      "status": "open",
      "satisfied_by": "Not checked to a conclusion. One side is bounded: glides of up to about 400 m in 30 s, so the aerial phase is seconds to tens of seconds (cited by the wind-tunnel authors to Hertel 1966 / Fish 1990 / Davenport 1994, not their own measurement). The other side was not found: one extended search returned aerial-uptake and oxygen-debt partitioning (~80% of post-exercise oxygen debt repaid aerially in Arapaima gigas; striped catfish taking 'more than 100%' of oxygen from air in poorly oxygenated water) but NO time-to-hypoxia in seconds for a small teleost at burst metabolic rate and no comparable breath-hold duration.",
      "satisfied_evidence": "unknown",
      "note": "J Fish Biol 2014 reviews, J Comp Physiol B 2026 (Arapaima), JEB 226:JEB245038 - read-level search-summary. Marked open rather than unsatisfied because one shallow search does not give a negative a defensible scope; the search itself reported that species-specific work (snakeheads, climbing perch, post-burst lactate kinetics) would be needed. UNCHECKED INFERENCE, flagged and not a finding: if breath-hold or anaerobic capacity covers tens of seconds, which is the direction the oxygen-debt literature points since fish burst work is routinely anaerobic, then aerial gas exchange may need no protein novelty at all over a 2-30 s glide and the claim's count of six empty slots would be one too high."},

    {"target_scale": "protein", "kind": "range",
      "statement": "The fin's load-bearing protein matrix must have a Young's modulus high enough that an aerodynamic surface of achievable thickness resists dynamic pressure at flight speed without collapsing.",
      "quantity": "Young's modulus of fin load-bearing protein matrix",
      "lo": null, "hi": null, "units": "GPa",
      "status": "open",
      "satisfied_by": "Measurement recorded, requirement not computed, and the tissue the claim names has no number. Measured: lepidotrichia Young's modulus 3.67-8.40 GPa, mean 6.48, in Hawaiian stream fishes, pelvic rays stiffest and pectoral least stiff; pectoral-ray flexural stiffness ~1e-10 to 1.5e-6 N.m2, decreasing exponentially proximo-distally. NO fin-membrane (inter-ray) stiffness measurement was returned, and that is the tissue 'membrane stiffness' names. Required EI unknown: not computed, and no measured flying-fish fin EI found.",
      "satisfied_evidence": "measured",
      "note": "Flammang et al. 2013 JMorph, JEB 223:jeb227140, JEB 221:jeb163360 - read-level search-summary. Distal moduli of 0.11-0.67 GPa from a flapping-actuator paper were DISCARDED because the search could not establish whether they were biological or engineered. SCALE OBJECTION, my inference from the measured spans and not any author's claim: flexural stiffness is E.I, the composition lever on E spans only ~2.3x across the measured data (3.67 to 8.40 GPa) while the geometric lever on I spans ~4 orders of magnitude in the measured EI data, so if the aerodynamic requirement is more than ~2.3x from what a zebrafish fin already achieves, no protein edit closes it and 'membrane stiffness' is mis-assigned to the DNA and protein scales. NEGATIVE SCOPE for the membrane: one extended search on fin-ray and fin-membrane mechanics, which returned ray data only and reported no membrane measurements; soft-tissue mechanobiology and collagen-network literature not searched."}
  ]}
```
