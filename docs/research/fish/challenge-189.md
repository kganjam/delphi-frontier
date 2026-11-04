# Challenge 189 — adversarial review of the S28 zebrafish negative verdict

**Claim under review (S28-organism.md, recorded evidence level `derived`, value `n/a`):**

> "S28 VERDICT NEGATIVE: the best design buildable from demonstrated alleles is the EXISTING Daane
> `lat4a^nr21/+;kcnh2a^lof/+` zebrafish, and it cannot fly, glide, skim, or meaningfully extend its
> leap"

**Outcome: SURVIVED** on its operative conclusion, with a margin larger than the claim asserts.
One sub-clause ("the best design buildable from demonstrated alleles") is unsupported as stated and
is flagged below; it does not change the verdict, because the binding constraint is launch power,
not fin size.

---

## 0. Procedural defect: the source document is absent from this repository

I could not read `S28-organism.md`. **Scope of negative search:** `find` over the full working tree
for `*S28*`, `*organism*`; `grep -ril` for `S28`, `zebrafish`, `lat4a`, `kcnh2a`, `Daane` across all
tracked files; `git ls-tree -r` over the 50 most recent commits on all refs; `git log --all
--diff-filter=A` for added paths matching `s28|organism|fish`. The repository has no `docs/`
directory before this commit. The only `zebrafish` hits are unrelated benchmark-triage notes
(`findings/gemini-triage-267-problems.json`, `findings/gemini-third-assessor-calibration.json`,
referring to ZFIN, BMP/Smoc1 and fin regeneration).

**Consequence, stated plainly:** instruction 1 asks me to redo the arithmetic "from the stated
inputs" without copying the author's working. The author's inputs and working were both unavailable,
so I could not compare against them. Everything below is an *independent* reconstruction from
primary literature. Three review questions are therefore only partly answerable:

- I cannot confirm what the author's inputs were, so I cannot certify their arithmetic — only that a
  correct independent derivation reaches the same verdict.
- I cannot verify whether S28 *presented* the derived result as observed (see §4).
- I cannot assert the author "missed" any counter-example (§5, §6); I can only state that the
  counter-example exists and that the claim as worded does not address it.

## 1. Entities verified

| Entity | Status | Source | Read-level |
|---|---|---|---|
| `lat4a^nr21` | **Real.** Dominant gain-of-function, non-synonymous T200K, chr 15. CRISPR frameshift in *cis* reverts to wild-type fins; homozygous LOF is normal and viable. Suppresses medial-fin overgrowth. | Daane et al. 2021, *Curr Biol* 31(22):5052–5061.e8 | full-text (PMC9172250) |
| `kcnh2a^lof` (*longfin*) | **Real.** chr 2 inversion causing *cis*-ectopic `kcnh2a` overexpression in fins. | same | full-text |
| `lat4a^nr21/+;kcnh2a^lof/+` | **Real and published.** Trans-heterozygotes show elongated paired fins and a hypocercal caudal fin, "remarkably similar to that of flying fishes"; authors conclude it is "sufficient to reproduce the flying fish fin bauplan." | same | full-text |

The genotype is correctly named and the morphological premise is **observed**. No gene symbol,
allele or citation in the claim is fabricated. That part is clean.

## 2. Arithmetic, redone independently

Script: `scratchpad/aero.py` (reproducible; not committed — values reproduced in full below).

**Measured inputs** (each cited, none invented):

- adult *D. rerio* mass ≤ 0.5 g — "adult zebrafish rarely exceed 0.5 g" (Flume study, *PLoS ONE*
  2018, 13:e0199712; read-level: search-summary). Used as an **upper** bound, which favours the
  claim's opponent.
- adult standard length SL = 3.4 ± 0.2 cm (*ibid.* and critical-speed protocol; search-summary).
- U_crit wild-type = 56.0 ± 4.8 cm/s; U_crit long-finned = 43.7 ± 6.8 cm/s, 28 °C (Plaut 2000,
  *J Exp Biol* 203(4):813; read-level: **search-summary only** — `pubmed.ncbi.nlm.nih.gov` and
  `www.researchgate.net` do not resolve in this session and would need allowing in the session's
  network settings. I did not read this abstract. Per CONTRIBUTING-VERIFICATION §3 it is marked
  unread and no conclusion below rests on it alone.)
- ρ_air = 1.225 kg/m³, ν_air = 1.5×10⁻⁵ m²/s, g = 9.81 m/s² (standard constants).

**Derived** quantities (calculated, not observed):

- W = 4.91 mN.
- U_max ≈ 1.15 × U_crit ≈ **0.64 m/s** (≈19 BL/s). The 1.15 factor is from a flume study reporting
  U_max exceeds U_crit by ~15% in the same fish (search-summary).
- A deliberately over-generous C-start ceiling of **1.5 m/s** (≈44 BL/s) is also carried through, to
  avoid resting the verdict on U_crit.

**Wing area is measured nowhere** (see §3). Two bounds:

- *Over-generous, sourced:* pectoral fin length at the Davenport ceiling 0.79 × SL = 2.69 cm
  (Davenport 1992/1994: pectoral fin length cannot exceed 78–79% of SL without impairing swimming;
  read-level: search-summary), span = 2 × fin length, chord = 0.3 × fin length → **S = 4.33 cm²**.
- *Cross-check:* scaling from a flying fish of SL 25 cm with ~65 cm² total pectoral area → **S =
  1.20 cm²**. **The 65 cm² figure is my own order-of-magnitude construction, not a cited
  measurement.** It is reported only to show the two bounds bracket the answer; the verdict rests on
  the sourced bound above, which is 3.6× larger and therefore more favourable to the opponent.
- C_L = 1.2 assumed for a thin low-aspect-ratio membrane — itself generous (see §5a).

**Result** — airspeed at which lift equals body weight, v = √(2W / ρ S C_L):

| Bound | S | v required | vs U_max 0.64 m/s | vs generous 1.5 m/s |
|---|---|---|---|---|
| cross-check | 1.20 cm² | **7.45 m/s** (219 BL/s) | 11.6× speed, 134× KE | 5.0× speed, 24.7× KE |
| over-generous, sourced | 4.33 cm² | **3.93 m/s** (115 BL/s) | 6.1× speed, 37× KE | 2.6× speed, 6.9× KE |

Under the most opponent-favourable combination available — maximum sourced fin area, generous C_L,
and a burst speed 2.3× the derived maximum — the fish is still **2.6× short in airspeed and 6.9×
short in kinetic energy**. The claim's "cannot fly, glide" survives, and survives the relaxation of
every assumption I could relax.

Method validation (CONTRIBUTING-VERIFICATION §8 — a control whose answer is known in advance): the
same formula applied to a 25 cm flying fish returns ~21 m/s, consistent with the 10–20 m/s flight
speeds reported for Exocoetidae (search-summary). The method is not producing the negative by
construction. Note also that wing loading scales as W/S ∝ L, so a 3.4 cm fish needs a *lower*
airspeed than a 25 cm flyer — the negative verdict is **not** driven by small size making flight
harder. It is driven by absolute attainable speed, which does not scale down favourably.

## 3. The hidden assumption, and the result does not rest on it

**Fin area carries the result, and no published fin area exists.** Daane et al. 2021 (full-text)
report pectoral fin length *normalised to standard length*, with Tukey's HSD levels, **in Figure 4B
only — the values do not appear in the text**, and no fin area is reported anywhere in the paper.
Any aerodynamic treatment of this genotype must therefore construct an area.

Relaxed: moving from the cross-check to a 3.6× larger sourced bound changes the required airspeed by
only √3.6 ≈ 1.9×, because v ∝ S^(−1/2). Closing a 6–12× speed gap by fin area alone would need a
**36–134× area increase**, which the Davenport 79%-of-SL swimming constraint forbids outright. The
assumption is real but **not load-bearing**. S28 should nonetheless state that the area is
constructed, not measured.

## 4. Is a proxy standing in for the quantity that matters? — Yes, for one of the four verbs

The claim bundles four predicates. Steady-state weight support (§2) is the right test for **fly** and
**glide**. It is the **wrong** test for "**meaningfully extend its leap**": a ballistic leap needs no
full weight support, only a lift fraction that reduces effective gravity over the arc. Using the
glide criterion to dismiss leap extension is a proxy substitution, and it is the one place the claim
reasons from the wrong quantity even though it lands on the right answer.

**The right quantity** — lift as a fraction of body weight at attainable launch speed, and its effect
on ballistic range (range ∝ 1/(1−L/W) to first order):

| Bound | at 0.64 m/s | at 1.5 m/s (over-generous) |
|---|---|---|
| cross-check S | 0.7% of weight → range ×1.01 | 4.1% → ×1.04 |
| sourced generous S | 2.7% of weight → range ×1.03 | **14.6% → ×1.17** |

So even computed correctly, the best case is a ~17% range extension under assumptions stacked
against the claim, and ~1–4% under realistic ones. "Cannot meaningfully extend" **survives** — but
the claim reached it via a criterion that would also have excluded a genuinely meaningful 17%, so the
reasoning is luckier than it is sound. Recommend S28 record the lift-fraction calculation, not the
weight-support calculation, against the leap predicate.

**Counter-pressure I could not resolve, preserved rather than averaged away:** the enlarged fins also
*cost* launch speed, and range ∝ v², so the net leap could be shorter than wild-type. If Plaut's 22%
U_crit deficit transferred, range would fall to ×0.71 — the engineered fish would leap ~29% *less*
far, strengthening the claim beyond its own wording. **I do not assert this**, for two reasons that
pull against it: (a) Plaut's long-finned strain overgrows the **median** fins, whereas `lat4a^nr21`
specifically *suppresses* medial overgrowth so the double mutant has wild-type median fins and
enlarged **paired** fins — the deficit does not transfer cleanly; (b) U_crit is sustained aerobic
performance and is itself a proxy for burst launch speed, and zebrafish adduct the pectorals during
fast starts, which would reduce both the drag penalty and the lift benefit. Direction of the net
effect: **unknown**. It requires a measurement nobody has made.

## 5. Is the evidence level honest? — Yes, `derived` is correct, with one required caveat

Daane et al. 2021 (full-text) **performed no locomotor assay of any kind** on this genotype. Their
claims are explicitly morphological: the fin *bauplan* is phenocopied. They do not examine pectoral
girdle, musculature, skeletal elements, semicircular canals, corneas or jaw morphology in the double
mutant, and do not report its allometric curve against the flying fish.

So `derived` is the honest label for the locomotor verdict, and `value: n/a` is defensible given that
the claim is a verdict rather than a measurement. **The defect to watch:** "it cannot fly" is an
unmeasured prediction, and the sentence must say so. I could not check whether S28's prose does
(§0). If S28 states the incapacity without marking it derived, that is a CONTRIBUTING-VERIFICATION §6
violation even though the number is right.

One under-claim in the other direction: the double mutant's caudal fin is "generally wild type in
size" though hypocercal. Flying fish taxi using an enlarged **lower caudal lobe** as a thrust organ
while the body is airborne. The genotype lacks that organ — an independent reason the leap cannot be
extended, available from the same paper, and not reflected in the claim.

## 6. Regime and taxon counter-examples — three found; all strengthen the claim

**(a) Reynolds-number regime — the author's generous C_L is unattainable.** At the sourced fin chord
(0.3 × 2.69 cm = 0.81 cm) and U_max 0.64 m/s, chord Re ≈ **346**. Thin plates below Re ≈ 10³ do not
reach C_L 1.2; lift is poor and L/D falls to single digits. My own C_L = 1.2 is therefore too
generous, and the true deficits in §2 and §4 are **worse** than tabulated. This regime point is
absent from the claim and makes it more robust, not less.

**(b) Pitch stability, a failure mode independent of fin size.** Davenport reports that the
"non-flying" flying fish fails *not* primarily on wing loading but because the centre of gravity
sits so far behind the pectoral fins that "stalling on take-off would be inevitable"
(read-level: search-summary). A zebrafish with enlarged pectorals and an unmodified body plan has no
reason to be balanced about its new lifting surfaces. No allele in the design touches CG position.
This is a second, independent sufficient reason for the negative — again strengthening.

**(c) Gasteropelecidae — the strongest available counter-example, and it fails too.** Freshwater
hatchetfish are the obvious taxon to raise against a "small fish cannot leave the water" verdict:
*Carnegiella myersi* ~2.2 cm, *C. schereri* ~2.6 cm, *C. marthae* ~2.8 cm — **smaller** than an adult
zebrafish — with an enormously enlarged sternal keel and pectoral musculature reaching **~25% of
total body mass**. If any small fish could fly, it is this one. Yet high-speed video (Wiest 1995,
cited via Seriously Fish; read-level: **search-summary, primary paper not accessed**) found the
pectoral fins are used **to leave the water, not while airborne** — powered flight does not occur —
and the fish manage only one or two jumps before needing rest.

This is decisive for the review, and in the claim's favour: the nearest small-bodied analogue, with
vastly more enabling anatomy than any potassium-channel or amino-acid-transporter allele can build,
**still does not fly**. The limiting factor is power and skeletal support, not fin area — exactly the
axis on which the demonstrated alleles do nothing. I found **no** published counter-example of a
fish of zebrafish body size achieving flight, glide, or lift-extended leaping. **Scope of that
negative search:** web search for flying-fish takeoff/wing-loading biomechanics, Gasteropelecidae
flight, and zebrafish burst-swimming performance; primary full-text read for Daane et al. 2021 only;
`pubmed.ncbi.nlm.nih.gov` and `www.researchgate.net` unreachable in this session.

## 7. The sub-clause that does not survive: "the best design buildable from demonstrated alleles"

This is asserted, not shown, and at least one demonstrated alternative is unaddressed. `kcnk5b`
carries two independent dominant fin-overgrowth alleles — `alf^dty86d` and `alf^d30mh` (Perathoner
et al. 2014, *PLoS Genet* 10:e1004080; read-level: search-summary) — acting locally in fin mesenchyme
via increased K⁺ conductance and hyperpolarisation, with follow-on calcineurin work (Daane et al.
2018, *Sci Rep* 8:10391; search-summary). `lat4a^nr21/+;kcnk5b^alf/+` is a candidate the claim's
"best" does not consider. I state only that it exists and is unaddressed by the claim's wording; I
**cannot** say the author missed it, because `S28-organism.md` is unavailable (§0).

Why this does not change the outcome: §2 and §6c show the binding constraint is launch power and
skeletal support, not fin size. Every fin-size allele — `kcnh2a`, `kcnk5b`, `lat4a`, or any
combination — fails against the same 6–12× speed deficit. The "best design" clause is therefore
**unsupported but immaterial**. Correct repair: drop the superlative and state the constraint, e.g.
"no combination of demonstrated fin-size alleles can close a 6–12× launch-speed deficit, so the
design space is empty regardless of which is chosen." That is a stronger claim than the original and
is what the evidence actually supports.

## 8. Verdict

The claim is a correctly-signed negative, and it is more robust than its author appears to have
established. It survives independent re-derivation, relaxation of its load-bearing assumption,
correction of a proxy substitution on the "leap" predicate, and the best taxonomic counter-example
available. Its defects are presentational and specificity-related, not directional: an unsupported
superlative (§7), a proxy used for the leap predicate (§4), a constructed fin area that should be
labelled as such (§3), and a required marking of the locomotor incapacity as derived rather than
observed (§5). No fault I found reverses the verdict, and I decline to manufacture one.

A negative stated precisely is the deliverable here. **Nothing in this review manufactures
feasibility, and nothing supports any claim that this genotype gains aerial capability.**

```swarm-challenge
{"claim_id": 189, "outcome": "survived", "reason": "Independent re-derivation from measured zebrafish mass, standard length and swimming speed gives a 2.6-11.6x launch-speed deficit (6.9-134x kinetic energy) against the airspeed needed for weight support even under maximally opponent-favourable fin area and lift coefficient, and the best small-bodied counter-example (hatchetfish, ~25% body mass as pectoral muscle) still lacks powered flight; only the unsupported 'best design' superlative and a proxy substitution on the leap predicate are defective, neither reversing the verdict.",
  "corrected_value": "weight-support airspeed 3.93-7.45 m/s vs <=0.64 m/s attainable (6.1-11.6x speed deficit); lift <=14.6% of body weight at any attainable launch speed, giving <=1.17x ballistic range; net leap change vs wild-type unknown (unmeasured)",
  "depends_on": ["S28-organism.md (ABSENT from repository; author's inputs and working unavailable, so author's arithmetic uncertified)", "Daane et al. 2021 Curr Biol 31(22):5052-5061.e8 (full-text): lat4a^nr21 and kcnh2a^lof alleles, trans-heterozygote fin phenotype, pectoral fin length reported in Fig 4B only, NO fin area reported, NO locomotor assay performed", "adult D. rerio mass <=0.5 g (search-summary)", "adult D. rerio standard length 3.4 +/- 0.2 cm (search-summary)", "Plaut 2000 J Exp Biol 203(4):813 U_crit wild-type 56.0 cm/s vs long-finned 43.7 cm/s (search-summary, UNREAD abstract; pubmed/researchgate unreachable this session)", "U_max ~= 1.15 x U_crit (search-summary, derived factor)", "Davenport pectoral fin length ceiling 78-79% of standard length (search-summary)", "Davenport centre-of-gravity/stall mechanism in non-flying flying fish (search-summary)", "Wiest 1995 hatchetfish high-speed video: pectoral fins used to exit water, not airborne (search-summary via Seriously Fish; primary NOT accessed)", "Gasteropelecidae body length 2.2-2.8 cm and ~25% body mass pectoral musculature (search-summary, secondary sources)", "Perathoner et al. 2014 PLoS Genet 10:e1004080 kcnk5b alf^dty86d and alf^d30mh (search-summary)", "assumed C_L = 1.2 for thin low-aspect-ratio membrane (ASSUMPTION, shown too generous at chord Re ~346)", "constructed pectoral wing area 1.20-4.33 cm^2 (DERIVED, no published measurement exists; 65 cm^2 flying-fish reference area is my own construction, not a cited value)", "standard constants rho_air 1.225 kg/m^3, nu_air 1.5e-5 m^2/s, g 9.81 m/s^2"]}
```
