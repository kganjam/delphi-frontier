# Challenge 233 — adversarial review of [S15], the zebrafish glide edit-stack claim

**Reviewer:** adversarial pass, did not write the claim.
**Claim source:** `harvest:zebrafish-glide-edit-stack-7kna51`. **This harvest record is not present in
this repository** (`grep` for `zebrafish-glide-edit-stack-7kna51`, `kcnh2a`, `lat4a` across all
`*.md|*.json|*.jsonl|*.yaml|*.py` returned nothing; `docs/` did not exist before this file). So I
could not read the author's working, their cited read-levels, or their input values. Everything
below is recomputed from the claim text as quoted in the challenge prompt.

**Verdict: WEAKENED.** The conclusion survives intact and is in fact reinforced by something the
author did not use. The KEY number does not survive: it rests on an undisclosed load-bearing input
that is below the measured value, and its headline framing (a wing-*area* shortfall) is an artifact
of one freely chosen input rather than a physical bound. The right scale-free comparison inverts
which deficit is binding.

---

## 1. Arithmetic, redone independently

I did not copy the author's working. I started from the lift equation for a weight-supporting glide,
`L = ½ ρ v² S C_L`, set `L = mg`, and solved for `S`:

```
S = 2 m g / (ρ v² C_L)
```

The claim states `S`, `v` and `C_L` but **not `m`**. Body mass is load-bearing and undisclosed, so I
back-solved it from the author's own output (ρ = 1.225 kg/m³, g = 9.81 m/s²):

```
m = S ρ v² C_L / (2 g) = (2.0e-3 × 1.225 × 4 × 0.8) / (2 × 9.81) = 3.996e-4 kg = 0.400 g
```

Forward-checking at that mass reproduces all three of the claim's figures exactly:

| quantity | claim | my recomputation |
|---|---|---|
| `S_req` at v=2 m/s, C_L=0.8 | ~2.0e-3 m² (20 cm²) | 2.002e-3 m² (**20.02 cm²**) |
| shortfall vs 1.4 cm² | ~14x | **14.30x** |
| ratio at v=10 m/s | ~0.6x | **0.57x** |

**The arithmetic is correct and internally consistent.** No computational error. The `1/v²` scaling
is applied correctly. This part of the claim survives cleanly, and I want that on the record before
the criticisms, because the criticisms are not about the author's algebra.

*(Computed, not observed. Scripts: `recheck.py`, `wingload.py` in the session scratchpad.)*

### 1a. But the undisclosed mass is below the measured value

An adult-zebrafish swimming-performance paper reports **mean mass = 0.56 ± 0.014 g (s.e.) at mean
standard length 3.28 cm**, and separately notes that adult zebrafish "rarely exceed 0.5 g"
(read-level: **search-summary** — I have the quoted sentences via search snippet, not the full text).
The two statements are in tension with each other; I preserve rather than average that. Either way,
0.400 g sits at or below the bottom of the measured range.

Re-running at measured mass:

| assumed `m` | `S_req` @ 2 m/s | shortfall vs 1.4 cm² |
|---|---|---|
| 0.400 g — author's implied, undisclosed | 20.02 cm² | 14.30x |
| 0.50 g — "rarely exceed" | 25.03 cm² | 17.88x |
| **0.56 g — measured mean** | **28.03 cm²** | **20.02x** |

So the honest figure at measured mass is a **~20x** shortfall, not ~14x. **This correction makes the
claim's own conclusion stronger, not weaker** — but a load-bearing input that is undisclosed *and*
set below the measured central value is a defect regardless of which way it cuts, because a reader
cannot audit it without back-solving. It also moves the v=10 m/s sensitivity: at 0.56 g the ratio is
0.80 cm²·(0.56/0.40)/1.4 = **0.80x**, not 0.57x — still under 1, so that leg of the claim holds.

### 1b. C_L = 0.8 is optimistic at the relevant Reynolds number

With chord ~5 mm and ν_air ≈ 1.5e-5 m²/s, `Re = vc/ν` ≈ **670** at v=2 m/s (≈1,330 at 10 mm chord);
at v=10 m/s, Re ≈ 3,300–6,700. C_L = 0.8 is a thin-plate figure that is hard to defend at Re ≈ 10²–10³,
where lift-curve slope degrades and L/D collapses. Relaxed to C_L = 0.5, `S_req` at 2 m/s rises to
32.0 cm² (22.9x at 0.40 g; 32.0x at 0.56 g). **This assumption also cuts in the claim's favour** —
relaxing it widens the gap. I flag it as undeclared optimism, not as an error.

---

## 2. The proxy — and it is the load-bearing defect

**Two proxies are in play, and the second one is the serious one.**

### 2a. Minor: body silhouette is the wrong denominator

The claim compares a required *wing* area against "~1.4 cm² whole-body dorsal silhouette." In
Exocoetidae the wing is overwhelmingly *fin*, not body: a comparative study across six exocoetid
genera reports that fin area and span scale with body mass while the pectoral share of total wing
area stays roughly constant, with pelvic fins contributing a further ~20–35% of lateral fin area
(read-level: **search-summary**). Body silhouette is therefore neither what carries a flying fish nor
what the `lof;nr21` genotype actually modifies — that genotype's aerodynamic surface would be its
*elongated paired fins*.

My independent sanity check of the 1.4 cm² figure: at measured SL 3.28 cm (TL ≈ 4.1 cm) and max body
width ~4–5 mm, a fusiform dorsal projection ≈ 0.6 × 4.1 × 0.45 ≈ 1.1 cm². So **1.4 cm² is a sound
order-of-magnitude estimate for the body alone** — but it is an *estimate* of unstated provenance in
the claim, presented as a given.

The correctly-posed denominator — achievable paired-fin planform area in `kcnh2a^lof/+; lat4a^nr21/+`
— is **unknown**. The source paper measures fin *length* normalised to standard length, plus
lepidotrichia segmentation and qRT-PCR; I found no fin-*area* measurement (read-level: **full-text**,
first 100k characters of PMC9172250; the final ~49k characters were not read, so I cannot call this
exhaustive). Using silhouette as a ceiling understates achievable area, which cuts *against* the
claim — but not by anything close to 14x, since elongated-but-narrow rays add ones of cm², not tens.

### 2b. Major: area is a proxy for the wrong quantity entirely

The quantity that matters is **wing loading**, `W/S`, because it is the scale-free statement of
whether an aerofoil can hold a body up; and the independent constraint is **airspeed**, because `S`
and `v` trade as `S ∝ 1/v²`.

Computing the wing loading a glide can support, `W/S = ½ ρ v² C_L`, against the zebrafish's loading
on its bare body silhouette:

```
zebrafish on 1.4 cm2:   m=0.40 g -> W/S = 28.0 N/m2
                        m=0.56 g -> W/S = 39.2 N/m2   (measured mass)

supportable W/S:   v=10 m/s, C_L=0.5 ->  30.6 N/m2
                   v=15 m/s, C_L=0.5 ->  68.9 N/m2
                   v= 2 m/s, C_L=0.8 ->   1.96 N/m2
```

**A zebrafish, on its bare body silhouette and at its measured mass, already has a wing loading
(28–39 N/m²) inside the range that a 10–15 m/s glide supports (31–69 N/m²)** — and reported flying-fish
takeoff speeds sit at or above that band (~14–19 m/s from a popular explainer; 20 m/s in a published
*simulation*; read-level: **search-summary**, and I note one of those is simulated, not observed).

That is the break. **There is no scale-free ~14x area deficit.** The 14x exists only because `v` was
pinned at 2 m/s; it is a restatement of the velocity shortfall in area units, not an independent
finding. Quoting an area deficit *and* a speed sensitivity presents one deficit as two, and puts the
derived one in the headline.

Stated the right way round, with `S` held at the body silhouette and `v` solved for:

| | speed needed on 1.4 cm² | vs measured U_crit 0.548 m/s | power at `v³` |
|---|---|---|---|
| m=0.40 g, C_L=0.8 | 7.6 m/s (231 SL/s) | 13.8x | ~2.6e3x |
| m=0.56 g, C_L=0.5 | 11.3 m/s (345 SL/s) | 20.7x | ~8.8e3x |

Measured adult U_crit is **0.548 ± 0.007 m/s = 18.0 SL/s** (read-level: **search-summary**). I could
not find an adult-zebrafish *fast-start peak* speed in m/s paired with body mass — the escape-kinematics
papers I reached covered larvae or 18–30 mm juveniles (scope of negative search: targeted web search
on adult *Danio rerio* fast-start/burst speed with mass, ~8 results reviewed; **not** a literature
review, and I did not search Web of Science or read the escape-kinematics full texts). So I cannot
state the burst ceiling. I note only that the claim's chosen 2 m/s is **61 SL/s**, roughly 3.7x
measured U_crit, i.e. the author picked a launch speed that is already generous — and 10 m/s is
**305 SL/s**, which the claim correctly treats as the unreachable leg.

**So the binding deficit is launch power, which is one of the six slots the claim already identifies
as empty.** The claim names the right constraint in its slot list and then measures a different one
in its KEY.

---

## 3. Hidden assumptions, relaxed

**(a) Equilibrium weight-supporting glide (`L = W`).** This is the assumption that carries the
result, and the claim never declares it. "Gliding" in the weaker sense of extending an airborne
trajectory needs only `L < W`:

| criterion | `S_req` @ 2 m/s, 0.40 g | shortfall |
|---|---|---|
| L = 1.0 W (claim's implicit test) | 20.0 cm² | 14.3x |
| L = 0.5 W | 10.0 cm² | 7.1x |
| L = 0.3 W | 6.0 cm² | 4.3x |
| L = 0.1 W | 2.0 cm² | **1.4x** |

At `L = 0.1 W` the requirement is within ~1.4x of the silhouette. Whether partial lift counts as
"gliding" is a definitional question the claim resolves silently in the strict direction. That is a
legitimate choice, but it is a choice, and it moves the headline number by an order of magnitude.

**(b) Steady state at all.** A launch is ballistic and ~0.1 s long. Quasi-steady lift at Re ≈ 10³
over that interval is an assumption, not a given; unsteady and added-mass effects at this scale are
not captured by `½ρv²SC_L` in either direction.

**(c) Small size is the problem.** It is not. Weight scales as `L³` and area as `L²`, so wing
loading `∝ L` — *smaller is aerodynamically favourable* for loading, and the exocoetid morphometrics
agree: wing loading "rises in positive allometric fashion with standard length" (read-level:
**search-summary**), i.e. the small flying fish are the lightly-loaded ones. The zebrafish is not too
small to be held up; it is too slow to reach the speed at which it would be held up.

---

## 4. Is the evidence level honest? No.

Recorded as **evidence level: literature, value: n/a**. Both fields are wrong, and by this
repository's own `CONTRIBUTING-VERIFICATION.md` rule 6 ("Separate columns, always — **proved** /
**simulated** / **observed**"):

1. **`value: n/a` is false.** The KEY carries numeric values (2.0e-3 m², 14x, 0.6x) that are the
   claim's entire quantitative content.
2. **The decisive numbers are calculated, not literature.** 20 cm², 14x and 0.6x are outputs of the
   lift equation applied to *assumed* inputs (C_L = 0.8 "assumed" — the claim does say so; v = 2 m/s
   declared but unsourced) plus one input (m ≈ 0.400 g) that is **not in the claim at all**. Filing
   this under "literature" puts a computation in the observation column. The genetics half of the
   claim *is* literature; the KEY half is arithmetic. One label covers both.
3. **The 1.4 cm² silhouette has no stated provenance** — measured, estimated, or assumed is not said.

This is a real defect independent of whether the numbers are right, which is exactly the failure
mode rule 6 exists to catch. The author's arithmetic is right and its label is wrong.

---

## 5. Regime, taxon and counter-examples

### 5a. Genetics: I attacked it and it held

I expected to break the allele string and could not. For the record, what I checked and found
**correct**:

- **`kcnh2a^lof(dt2)`** — correct. The paper uses `lof^dt2`: "The dominant longfin mutant (lof dt2)
  was first isolated in an aquarium population." (read-level: **full-text**, PMC9172250)
- **`lat4a^nr21/dmh26`** — correct, though the notation is a trap. I suspected `nr21/dmh26` was being
  passed off as a *lat4a* trans-heterozygote, and that `dmh26` was one of the CRISPR cis-frameshift
  revertants (which revert to wild-type fins — the opposite phenotype). It is not. Methods: "Lat4a
  alleles identified and used in this work are lat4a nr21 (dmh26), and lat4a del (mh152)." **`dmh26`
  is the ZFIN designation *of* `nr21`,** not a second allele; the revertant is `L106Rfs39` and carries
  no dmh number. ZFIN lists it as `slc43a2a^dmh26` (same gene, alternative symbol). The claim's "/"
  is a name/designation separator. **Not an error, but it reads as a genotype in a sentence that then
  says "whose viable transheterozygote," and should be written `lat4a^nr21 (dmh26)`.**
- **"dominant T200K"** — correct, and correctly called gain-of-function: "identified a nonsynonymous
  mutation (T200K) in a conserved domain of the L-type amino acid transporter, lat4a"; "the mutation
  in lat4a nr21 results from a gain-of-function effect"; *lat4a* loss-of-function has no fin phenotype.
- **"fin-size suppressor"** — correct and, importantly, *medial-fin-specific*. I initially thought
  pairing an overgrowth allele with a size suppressor must net toward *less* wing area, defeating the
  stack's own purpose. Wrong: the suppressor acts on the medial fins while the **paired** fins stay
  elongated, which is precisely the flying-fish allometry.
- **The transheterozygote** is `kcnh2a^lof/+; lat4a^nr21/+` — a double heterozygote across two loci,
  as the claim says. "Surprisingly, the caudal fin of kcnh2a lof/+;lat4a nr21/+, while generally wild
  type in size, is hypocercal, with an elongated ventral lobe."
- **"published as a flying-fish-like fin-allometry phenocopy"** — fairly scoped. The paper's own
  sentence: "The overall fin phenotype of the kcnh2a lof;lat4a nr21 fish is thus remarkably similar
  to that of flying fishes." The claim's qualifier "**fin-allometry** phenocopy" correctly does *not*
  overstate this as a gliding phenocopy. Source: Daane et al. 2021, *Current Biology*, "Modulation of
  bioelectric cues in the evolution of flying fishes" (PMID 34534441; read-level: **full-text** for
  chars 0–100,000 of PMC9172250).

### 5b. The fact the author did not use, which strengthens the claim

**The source paper reports no aerial, gliding, flight, or locomotor performance data at all** — only
fin length normalised to SL, lepidotrichia segmentation, and qRT-PCR; "gliding" appears only in its
phylogenomic/GO analyses and citations (read-level: **full-text**, chars 0–100,000; the unread final
~49k characters are Methods/supplementary, so I state this as "not found in the first 100k," not as
proven absent). This is direct support for the claim's conclusion: the two filled slots are
**morphological only**, with zero demonstrated aerodynamic function. The claim is right, and had a
stronger argument available than the one it led with.

### 5c. The counter-example the author missed — and it points the same way

**Gasteropelecidae (freshwater hatchetfish)** — 3–7 cm, and **Otophysi, the same superorder as
zebrafish**. They leave the water and travel aerially at cm body scale. Their pectoral musculature is
reported at **up to ~25% of body mass** (read-level: **search-summary** only; Britannica, a hobbyist
magazine, an aquarium site, and a study-guide site — **no primary paper located**).

The sources **disagree sharply and I do not average them**: Britannica and a magazine article report
in-air pectoral flapping adding thrust; a study-guide page asserts high-speed video "definitively
disproved" powered flight and that the fins are held rigid as wings. I could not identify that
high-speed-video study, its authors, or its date, and the site reads as generated content, so that
assertion should not be treated as settled either. Scope of negative search: targeted web search on
Gasteropelecidae/*Carnegiella* aerial locomotion, ~9 results; I did **not** search JEB, Zoology, or
Web of Science directly, and found no DOI-bearing primary source.

Even at that weak read-level it bears on the claim, because the *direction* is unambiguous and is
what the disagreement is about: hatchetfish get airborne via **launch power** — hypertrophied pectoral
musculature — not via a 20 cm² membrane. A cm-scale ostariophysan getting airborne is an existence
proof that the body scale is not prohibitive, which is what the "14x area shortfall" framing implies;
and the mechanism it uses is the claim's own empty **launch power** slot. **The counter-example
refutes the KEY's framing and confirms the claim's conclusion**, in agreement with the wing-loading
computation in §2b. The claim should have cited it, and should also address the smallest size at which
exocoetids themselves begin gliding — which I could not establish (`www.wcupa.edu` does not resolve in
this session's network policy and would need allowing; read-level: **could-not-access**).

---

## 6. What survives, what does not

**Survives:**
- The arithmetic, exactly, including the `1/v²` sensitivity.
- Every allele identifier, the mechanism assignments, and the transheterozygote genotype.
- The characterisation of the published result, correctly scoped to *fin allometry*.
- **The conclusion.** Six slots (membrane stiffness, launch power, aerial stability, vestibular/visual
  function in air, aerial gas exchange, mass reduction) with no demonstrated zebrafish edit means no
  minimal edit stack for gliding can be written. Nothing I found fills any of them, and the source
  paper's complete absence of locomotor data reinforces this. **Negative result, intact.**

**Does not survive:**
- **The KEY as a headline metric.** Area is not the binding deficit; launch power/airspeed is. The
  "~14x" is the velocity shortfall re-expressed in area units at a freely chosen v=2 m/s, and it
  dissolves under the scale-free comparison — the zebrafish's body-silhouette wing loading (28–39 N/m²)
  is *already within* the 31–69 N/m² a 10–15 m/s glide supports.
- **The specific number.** At measured adult mass (0.56 g) it is ~20x, not ~14x; the v=10 m/s leg
  becomes 0.80x, not 0.57x (both still under 1, so that conclusion holds).
- **The evidence label.** A calculation on an undisclosed input is filed as "literature / n/a".

**Net:** the claim reaches a correct conclusion, with correct genetics and correct arithmetic, via a
headline statistic that measures the wrong quantity and a label that misstates what kind of number it
is. The right KEY is a power/velocity deficit of ~14–21x in speed and ~10³–10⁴x in required power
against measured U_crit — larger and more decisive than the area figure it replaces.

**One thing the claim gets exactly right that I want to flag positively:** it refutes itself by its
own criterion rather than manufacturing feasibility. Under rule 7 ("report the null"), that is the
deliverable, and it is correct.

---

## Sources and read-levels

| source | read-level |
|---|---|
| Daane et al. 2021, *Curr Biol*, "Modulation of bioelectric cues in the evolution of flying fishes" — [PMC9172250](https://pmc.ncbi.nlm.nih.gov/articles/PMC9172250/), [PubMed 34534441](https://pubmed.ncbi.nlm.nih.gov/34534441/) | **full-text**, chars 0–100,000 of 149,104; final ~49k unread |
| Stewart et al., longfin / *kcnh2a* cis-ectopic expression — [bioRxiv 790329](https://www.biorxiv.org/content/10.1101/790329v3), [ZFIN ZDB-PUB-210602-7](https://zfin.org/ZDB-PUB-210602-7) | **search-summary** |
| Daane et al. 2021 preprint — [bioRxiv 2021.03.05.434157](https://www.biorxiv.org/content/10.1101/2021.03.05.434157v1.full) | **search-summary** |
| [ZFIN Daane 2021 Fig. 4](https://www.zfin.org/ZDB-FIG-221222-35) (`slc43a2a^dmh26`) | **search-summary** |
| Adult zebrafish mass 0.56±0.014 g, SL 3.28 cm; U_crit 0.548±0.007 m/s = 18.0 SL/s; "rarely exceed 0.5 g" — [PLoS ONE flume paper](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0199712), [PMC6019105](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6019105/), [PMC3013094](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3013094/) | **search-summary** |
| Exocoetid wing-loading allometry and fin-area partition — [Davenport, wing-loading/morphometrics](https://www.researchgate.net/publication/231928949_Wing-loading_stability_and_morphometric_relationships_in_flying_fish_Exocoetidae_from_the_North-eastern_Atlantic), [Fish, wing design & scaling](https://www.researchgate.net/publication/227706330_Wing_design_and_scaling_of_flying_fish_with_regard_to_flight_performance) | **search-summary** |
| Flying-fish takeoff speed (~14–19 m/s popular; 20 m/s *simulated*) — [Earth Lab explainer](https://lab.bluehub.jp/en/flying-fish-glide/), [arXiv 2304.04302](https://arxiv.org/pdf/2304.04302) | **search-summary** |
| Gasteropelecidae aerial locomotion — [Wikipedia](https://en.wikipedia.org/wiki/Gasteropelecidae), [Britannica](https://www.britannica.com/animal/hatchetfish), [TFH magazine](https://www.tfhmagazine.com/articles/freshwater/the-perfect-surface-dweller-hatchetfish-full-article) | **search-summary**, no primary source; sources conflict |
| Fish 1991, "On a Fin and a Prayer" | **could-not-access** (`www.wcupa.edu` not resolvable under this session's network policy) |

Constants used: ρ_air = 1.225 kg/m³, g = 9.81 m/s², ν_air = 1.5e-5 m²/s. All quantities in §1–§3 are
**calculated**, not observed. No experiment was run.

```swarm-challenge
{"claim_id": 233, "outcome": "weakened", "reason": "Arithmetic, allele identifiers and the six-empty-slots conclusion all verify, but the KEY's ~14x wing-area shortfall rests on an undisclosed 0.400 g body mass (measured mean is 0.56 g, giving ~20x) and is a regime artifact of pinning launch speed at 2 m/s: on the scale-free wing-loading comparison the zebrafish silhouette already sits at 28-39 N/m2, inside the 31-69 N/m2 a 10-15 m/s glide supports, so the binding deficit is launch power, not area, and the evidence level 'literature / n/a' mislabels a calculation as a literature value.",
  "corrected_value": "Launch-power/velocity deficit ~14-21x in speed and ~2.6e3-8.8e3x in required power vs measured U_crit 0.548 m/s; area shortfall restated at measured mass 0.56 g = ~20x (28.0 cm2 required vs 1.4 cm2), with the v=10 m/s leg 0.80x not 0.57x",
  "depends_on": ["harvest:zebrafish-glide-edit-stack-7kna51 (claim text as quoted; harvest record absent from this repo)", "lift equation L=0.5*rho*v^2*S*C_L with L=mg for equilibrium glide", "rho_air=1.225 kg/m3", "g=9.81 m/s2", "nu_air=1.5e-5 m2/s", "claim's assumed C_L=0.8", "claim's assumed launch speed 2 m/s", "claim's stated S_req=2.0e-3 m2 (used to back-solve the undisclosed m=0.400 g)", "claim's stated 1.4 cm2 whole-body dorsal silhouette", "adult zebrafish mean mass 0.56+/-0.014 g at SL 3.28 cm (search-summary)", "adult zebrafish 'rarely exceed 0.5 g' (search-summary, in tension with the 0.56 g mean)", "adult zebrafish U_crit 0.548+/-0.007 m/s = 18.0 SL/s (search-summary)", "flying-fish takeoff speed ~14-20 m/s (search-summary; one value simulated, not observed)", "exocoetid wing loading rises with positive allometry vs standard length (search-summary)", "exocoetid wing area is predominantly pectoral+pelvic fin, pelvics 20-35% of lateral fin area (search-summary)", "Daane et al. 2021 Curr Biol PMC9172250: lof^dt2, lat4a^nr21(dmh26) T200K gain-of-function, transhet kcnh2a^lof/+;lat4a^nr21/+ 'remarkably similar to that of flying fishes' (full-text chars 0-100000)", "absence of locomotor/aerial performance data in PMC9172250 (full-text chars 0-100000; final ~49k unread)", "Gasteropelecidae cm-scale aerial locomotion with pectoral muscle ~25% body mass (search-summary; no primary source; sources conflict on in-air flapping)", "CONTRIBUTING-VERIFICATION.md rule 6 (separate proved/simulated/observed columns) and rule 3 (mark read-levels)"]}
```
