# Challenge 235 — adversarial review

**Claim under review (verbatim):**

> "m\* = 39 mg (8.5–173 mg) for the LaMSA route. A 0.4 g zebrafish is ~10x (2.3–47x) TOO LARGE for
> single-impulse launch, not too small. The muscle-only route has no realisable crossover at all"

Recorded evidence level: `derived`. Recorded value: 10.3 times too large.
Recorded source: `S30-organism.md`; "ratio verified here".

**Verdict: WEAKENED.** The arithmetic is correct and the *direction* survives, including a
published counter-example test that goes the claim's way for aquatic fishes. What does not survive
is the headline framing: the deficit is a **2.2-fold linear overshoot**, not a 10-fold one, and the
claim's own confidence interval maps to **9.1–25.0 mm standard length** — entirely inside normal
zebrafish ontogeny — so "a zebrafish is too large" is false at the species level and true only of
an adult. The final sentence ("muscle-only has no realisable crossover at all") is the reverse of
the published work-limited structure and is coherent only under an unstated power/time-limited
reading.

---

## 0. Provenance failure: the stated source is not in this repository

Before anything else. `S30-organism.md` **does not exist in this repository**, and neither does any
text mentioning LaMSA.

Negative-search scope (all run at this commit, repository root, `.git` excluded):

| search | result |
|---|---|
| `find . -iname "*S30*"` | 0 hits |
| `grep -rli "lamsa" --include=*.md .` | 0 hits |
| `grep -rli "zebrafish" .` | 2 hits, both in `findings/gemini-*.json`, both unrelated (fin regeneration, Turing stripes) |
| `grep -rio "latch\|single-impulse\|ballistic"` | 0 hits |
| `docs/` directory | did not exist; created by this review |

Consequence: **I could not redo the derivation of m\* independently from the stated inputs, because
the stated inputs are not available to me.** The claim's provenance note says "ratio verified
here". The ratio is a single division; see §1. The load-bearing quantity — m\* = 39 mg and its
8.5–173 mg interval — is *unverified by anyone in this repository*, and the "verified here" note
invites the reader to think otherwise. Per `CONTRIBUTING-VERIFICATION.md` §2 and §3, the m\* value
should be carrying a source hash and a read-level, not a sibling filename that is absent.

This alone does not refute the claim. It does mean the only part I can attack from stated inputs is
the arithmetic, the framing, and the physics the claim must be assuming. I did all three.

## 1. Arithmetic, redone independently

Recomputed from the claim's own stated numbers, without reference to the author's working
(`scratchpad/chk.py`; this is **calculated**, not observed):

| quantity | my value | claim | verdict |
|---|---|---|---|
| 400 mg / 39 mg | 10.2564… | "~10x" / "10.3" | ✅ correct |
| 400 mg / 173 mg | 2.3121… | "2.3x" | ✅ correct |
| 400 mg / 8.5 mg | 47.0588… | "47x" | ✅ correct |

The ratio and its interval are internally consistent and correctly rounded. **No arithmetic
defect.** This is also the least interesting part of the claim: it is a division of two numbers,
one of which (m\*) is the entire scientific content and is not checkable here.

### 1a. The headline ratio is sensitive to which adult zebrafish you mean

Adult *Danio rerio* wet mass, read-level **search-summary** (I did not reach the primary tables;
see §7 on network limits): roughly **0.28–0.45 g** across sexes, strains and ages, with one
toxicology dataset giving 0.28 g (n=44 males) and 0.39 g (n=59 females) at ~3.25 and ~3.45 cm body
length. 0.4 g is therefore a defensible adult value but sits at the **top** of the credible band.

Recomputed headline ratio across that band (calculated):

| adult mass | ratio to m\* | linear overshoot |
|---|---|---|
| 0.28 g | 7.2x | 1.93x |
| 0.34 g | 8.7x | 2.06x |
| 0.40 g (claim) | 10.3x | 2.17x |
| 0.45 g | 11.5x | 2.26x |

So "~10x" is really "7–12x depending on sex and age", and the claim picks the upper half of that
range without saying so. Minor, but it is the direction `CONTRIBUTING-VERIFICATION.md` §9 warns
about: the choice makes the result look more decisive.

## 2. Is a proxy standing in for the quantity that matters? **Yes — two of them.**

### 2a. Mass is the wrong *unit* in which to report the deficit

Mass is the steepest-looking unit available. Launch feasibility in every work- or power-limited
model runs on **specific energy (J kg⁻¹)**, **takeoff speed**, and **acceleration distance**, all of
which scale on a length, not a mass. Under isometry m ∝ L³, so:

- 10.26x in mass = **2.17x in standard length** (calculated: 10.256^(1/3) = 2.173).
- If the binding shortfall is specific energy ∝ m^(−1/3) (the only sublinear scaling that produces
  an m\* at all; see §3), a 10.26x mass overshoot is a **2.17x specific-energy shortfall**, i.e.
  1.47x in takeoff speed and 2.17x in ballistic height.

"10x too large" and "needs 1.5x more takeoff speed" describe the same gap. The first is the one in
the claim. Reporting a cube-law quantity in the cubed unit inflates the apparent impossibility by
a factor of ~4.7 relative to the quantity a biologist would act on.

### 2b. Body mass is the wrong *variable*, and the fish literature says so explicitly

Published result, read-level **search-summary** (Minicozzi et al., "Big Fish Cannot Jump? Allometry
of Terrestrial Jumping in Cyprinodontiform Fishes", plus SICB abstracts on *Kryptolebias
marmoratus*): **aquatic killifishes decrease total jump distance as mass increases, while
amphibious killifishes increase total jump distance as mass increases.** In *K. marmoratus*
specifically, preparatory-phase acceleration scales as ~m^(+0.38) with contact time roughly
mass-invariant, so larger individuals reach *higher* takeoff velocities. The authors attribute the
split to **anterior–posterior body-mass distribution** — fusiform (anterior-heavy) aquatic fishes
versus more uniformly distributed amphibious ones.

Two taxa at overlapping gram-scale masses scale in **opposite directions**. Body mass therefore
cannot be the governing variable; the governing variables are the mass distribution and the
takeoff-impulse geometry (contact time × ground-reaction impulse), with mass entering only as a
covariate. A single scalar m\* applied to "the organism" discards exactly the variable that
decides the sign.

This cuts both ways, honestly: see §5, where the same literature *supports* the claim's direction
for zebrafish specifically.

## 3. The hidden assumption, and what happens when it is relaxed

**An energy argument alone produces no critical mass whatsoever.** Independent derivation
(calculated, from first principles, not from the author's working):

Work-limited launch, muscle mass fraction f, muscle work density e_m, transmission efficiency η:

  E/m = η f e_m  →  v = √(2 η f e_m)  →  h = v²/2g = η f e_m / g

Every term is mass-independent. This is Borelli's principle: under isometry, work-limited jump
height does not depend on body size. **m\* = 39 mg cannot come from an energy budget under
isometric scaling.** It can only come from one of:

1. **available launch energy scaling sublinearly with mass** — e.g. the spring/tendon being an
   area-like structure with volume ∝ m^(2/3), giving E_avail/E_req ∝ m^(−1/3);
2. **the target growing super-linearly with mass**; or
3. **a power/time limit**, not an energy limit.

Relax (1) to isometry (spring volume ∝ m, the default for a scaled organism) and **the crossover
disappears entirely** — there is no m\*, and the "10x too large" verdict evaporates with it. The
claim's number is therefore an artifact of a sublinear-scaling exponent that the claim as quoted
never states. That exponent, not the 39 mg, is the thing that needed the error bar.

Note also that option (3) is self-undermining as a source of "too large": for a power-limited
muscle launch over acceleration distance d ∝ L, setting delivered power P ∝ m against
E/t ≈ m v³/4d gives **v ∝ m^(1/9)** — larger is *better*, not worse. So a power limit cannot
generate a "too large" verdict either.

Relaxed-assumption summary: of the three mechanisms that could produce m\*, one (isometric energy)
gives no m\*, one (power limit) gives the opposite sign, and only sublinear spring-volume scaling
gives the claim's sign. The claim is one unstated exponent away from having no content.

## 4. Is the evidence level honest? **Mostly yes; the sentence is not.**

`derived` is the right label for the ratio, and the claim does not pretend to be an observation —
good. Two defects remain:

- The *sentence* reads "A 0.4 g zebrafish **is** ~10x too large", which is the grammar of a fact
  about an animal, not of a model output. Per `CONTRIBUTING-VERIFICATION.md` §6 the word
  "modelled" or "derived" belongs inside that sentence, as the honesty floor here requires.
- The interval "8.5–173 mg" is a **20-fold** range. An interval that wide is not a precision
  statement about m\*; it is a statement that m\* is known to within about one order of magnitude.
  Reporting the central value to two significant figures (39 mg, 10.3x) alongside a 20-fold
  interval overstates resolution. And the upper bound matters: at m\* = 173 mg the zebrafish is
  only 2.3x over, which is the kind of margin that model assumptions move.

## 5. Regimes, taxa and published counter-examples

### 5a. The "not too small" half of the claim SURVIVES, and I can show why

I tested the obvious attack — that a small body is drag-penalised, so the error might run the other
way. Aerial drag-to-weight at takeoff for a 0.4 g, ~33 mm fish at 2 m s⁻¹ (calculated;
ρ=1.2 kg m⁻³, C_d=0.2, A=1.5×10⁻⁵ m²): **1.8 × 10⁻³**. Negligible. There is no small-size penalty
at this scale in air, so the claim's "not too small" is correct and robustly so.

**Scope condition the claim omits:** that calculation assumes an *aerial* ballistic phase. For a
launch that stays submerged, added mass and drag dominate completely, a gram-scale fish decelerates
within roughly a body length, and there is no ballistic phase for an m\* to be defined against.
The claim is silent on whether "single-impulse launch" means water-exit; it only has meaning in the
aerial case.

### 5b. The direction is corroborated for zebrafish's own taxon

Zebrafish is a fully aquatic cyprinid. The Minicozzi result (read-level **search-summary**) is that
**aquatic** killifishes jump *less* far as mass increases. That is the claim's sign, in fishes, at
roughly the right scale. I went looking for a counter-example and found support instead; I am
recording that rather than burying it.

### 5c. The counter-example that does land: the claim's own interval contains zebrafish

This is the sharpest finding, and it comes from the claim's own numbers.

Mapping m\* to standard length under isometry, anchored on 0.40 g at 33 mm SL (calculated):

| m\* | implied standard length |
|---|---|
| 8.5 mg (lower bound) | **9.1 mm** |
| 39 mg (central) | **15.2 mm** |
| 173 mg (upper bound) | **25.0 mm** |

**The entire stated confidence interval for m\* lies inside normal zebrafish ontogeny.** 9 mm is a
late-larval/early-juvenile fish; 15 mm is a juvenile; 25 mm is a small adult. So the claim's own
interval cannot exclude a 25 mm zebrafish, and its central value says a **~15 mm juvenile zebrafish
sits essentially at the crossover**.

The defensible statement is therefore not "a zebrafish is ~10x too large" but: *an adult zebrafish
is ~10x over the modelled crossover mass; the crossover falls within zebrafish ontogeny at roughly
15 mm standard length (interval 9–25 mm).* Those two sentences license completely different next
actions — the first says change organism, the second says change life stage. The claim as written
is a species-level negative that its own numbers do not support.

(Stated honestly: this says nothing about whether a 15 mm zebrafish would be *useful* for whatever
S30 wanted. It says the "too large" verdict is a stage statement, not a species statement.)

### 5d. "The muscle-only route has no realisable crossover at all" is backwards

Published numbers, read-level **full-text** (Sutton, Mendoza, Azizi, Longo, Olberding, Ilton &
Patek, *Integrative and Comparative Biology* 59(6):1609–1618, 2019, "Why do Large Animals Never
Actuate Their Jumps with Latch-Mediated Springs? Because They can Jump Higher Without Them",
doi:10.1093/icb/icz145, read via PMC6907395):

- muscle work density **15.0 J/kg**;
- a spring "can maximally store only **28%** of the available input energy (**4.2 J/kg**)" — the
  paper's own Introduction says "~30%" and its Abstract "about one-third", and the paper does not
  reconcile these figures. I preserve that disagreement rather than averaging it;
- modelled crossover at **~2.5 g**: below it spring-actuated jumps higher, above it
  muscle-actuated jumps higher; empirically the crossover sits in the **~1 g to just under 1 kg**
  band occupied by anurans, and jumpers >1 kg are treated as muscle-actuated;
- muscle-actuated maximum height asymptotes to **~3x** the spring-actuated maximum.

Positive control on those numbers (calculated by me, answer known in advance per
`CONTRIBUTING-VERIFICATION.md` §8): h = e/g gives 15.0 J/kg → **1.53 m** and 4.2 J/kg → **0.43 m**.
The paper's largest *observed* jumps are 1.54 m (muscle-actuated, *C. familiaris*) and 0.49 m
(spring-actuated). Both land. The retrieved numbers are self-consistent and I am using them
correctly.

Now the problem for the claim. **In the work-limited regime LaMSA cannot exceed muscle work — it
is muscle work, minus spring losses** (4.2 vs 15.0 J/kg above). So a world in which the LaMSA route
has a feasible window (m ≤ 39 mg) while the muscle-only route "has no realisable crossover at all"
requires LaMSA to deliver *more* specific energy than direct muscle actuation. In an energy-limited
framing that is impossible, and the published numbers say the gap runs 3.6x the other way.

The conjunction is rescuable only under a strictly **power/time-limited** reading, where the latch's
contribution is rate, not energy, and the muscle route fails on stroke duration rather than on work.
The claim as quoted never says which regime it is in — and as shown in §3, the power-limited regime
gives v ∝ m^(1/9), which *favours larger* animals and so cannot be the source of the "too large"
verdict either. The claim needs one regime for its m\* and the other for its final sentence.

Separately: m\* = 39 mg is **64x below** Sutton et al.'s modelled 2.5 g crossover and three orders
below the empirical 1 g–1 kg band. These are **not the same quantity** — Sutton's crossover is
"mass above which muscle beats spring", the claim's m\* is "mass above which LaMSA misses an
unstated target" — so this is not a contradiction and I will not present it as one. It does mean
the only published crossover mass for this mechanism class offers the claim no corroboration, and
that at 0.4 g the published framework puts the fish in the band where muscle-only is *becoming the
better route*, not where it is unrealisable.

## 6. What I could not break

- The arithmetic (§1). Correct to the digit.
- The sign of the effect for aquatic fishes (§5a, §5b): "too large, not too small" is right, drag
  gives no small-size penalty at 0.4 g in air, and the aquatic-killifish allometry independently
  agrees.
- The `derived` evidence label itself is honest, even where the sentence around it is not.

## 7. Limits of this review

- `S30-organism.md` is absent (§0), so m\* and its interval were never independently re-derived.
  A review that cannot see the derivation cannot refute it; "weakened" is the strongest honest
  verdict available, and a reviewer with the source could reach a different one.
- Network: `experts.nau.edu` and `pubmed.ncbi.nlm.nih.gov` both failed DNS in this session and
  would need allowing in the session's network settings. The Minicozzi allometry paper and the
  *K. marmoratus* kinematics are therefore **search-summary** read-level only — conference
  abstracts and a publication listing as relayed by search, with one SICB abstract on geographic
  variation reporting that jump distance *decreased* with body length while another reports it
  increasing with mass in amphibious forms. That disagreement is unresolved and I have not
  averaged it. `pmc.ncbi.nlm.nih.gov` did resolve, which is how Sutton et al. 2019 is **full-text**.
- Zebrafish adult mass is **search-summary** (§1a); I did not reach the primary morphometric tables.
- No experiment was run. Every number I introduce is calculated or retrieved, and labelled as such
  in the sentence where it appears.
- The isometric m ∝ L³ mapping in §5c is my own assumption, stated here: zebrafish are not
  perfectly isometric across 9–33 mm SL, so the implied lengths carry at least a few mm of slop.
  The conclusion — that the whole interval falls inside ontogeny — survives that slop comfortably,
  since even strongly allometric growth keeps 173 mg below adult size.

---

## Corrected framing

> Modelled crossover m\* = 39 mg (8.5–173 mg) for the LaMSA route, under an unstated sublinear
> spring-energy scaling without which no crossover exists. An **adult** 0.4 g zebrafish is ~10x
> over m\* in mass, which is a **2.2x overshoot in standard length** (7–12x in mass across the
> 0.28–0.45 g adult band). The direction is correct: too large, not too small — aerial drag is
> negligible at this scale (drag/weight ≈ 2×10⁻³) and aquatic killifish allometry independently
> gives the same sign. But m\*'s full interval maps to **9–25 mm standard length**, inside normal
> zebrafish ontogeny, so this is a **life-stage** statement, not a species-level exclusion. The
> claim that the muscle-only route "has no realisable crossover at all" is unsupported as stated:
> in the work-limited regime LaMSA stores only ~28% (4.2 J/kg) of muscle's 15.0 J/kg
> [Sutton et al. 2019, full text], so muscle-only cannot be the strictly worse route, and the
> conjunction holds only under a power/time-limited reading that the claim does not declare — and
> which predicts v ∝ m^(1/9), favouring larger animals.

## Sources

- Sutton GP, Mendoza E, Azizi E, Longo SJ, Olberding JP, Ilton M, Patek SN (2019). *Why do Large
  Animals Never Actuate Their Jumps with Latch-Mediated Springs? Because They can Jump Higher
  Without Them.* Integr Comp Biol 59(6):1609–1618. doi:10.1093/icb/icz145 —
  [PMC6907395](https://pmc.ncbi.nlm.nih.gov/articles/PMC6907395) — read-level **full-text**.
- Ilton M et al. (2018). *The principles of cascading power limits in small, fast biological and
  engineered systems.* Science 360(6387):eaao1082. doi:10.1126/science.aao1082 — read-level
  **search-summary** (I did not reach the paper or its SI; cited only for the existence of
  critical-mass transitions in LaMSA models, not for any number).
- Minicozzi M et al. *Big Fish Cannot Jump? Allometry of Terrestrial Jumping in Cyprinodontiform
  Fishes.* — [NAU publication listing](https://experts.nau.edu/en/publications/big-fish-cannot-jump-allometry-of-terrestrial-jumping-in-cyprinod-2/)
  (DNS failed in this session) — read-level **search-summary**. Journal, year and DOI: `unknown`;
  I tried the NAU listing and PubMed and both hosts failed to resolve.
- *Kryptolebias marmoratus* tail-flip jump kinematics and population variation — SICB abstracts
  ([1](https://sicb.org/?p=24086), [2](https://sicb.org/?p=12864), [3](https://sicb.org/?p=6597),
  [4](https://sicb.org/?p=23410)) — read-level **search-summary**, conference abstracts only.
- Adult *Danio rerio* body mass — read-level **search-summary** from
  [PMC7108797 table](https://pmc.ncbi.nlm.nih.gov/articles/PMC7108797/table/tbl2) and
  [PMC6071982 table](https://pmc.ncbi.nlm.nih.gov/articles/PMC6071982/table/pone.0201278.t001)
  as relayed by search; primary tables not reached.
- `S30-organism.md` — read-level **could-not-access**: absent from this repository (search scope
  in §0).

```swarm-challenge
{"claim_id": 235, "outcome": "weakened", "reason": "Arithmetic and the too-large direction survive, but the deficit is a 2.2x linear overshoot reported in cubed units, m*'s full 8.5-173 mg interval maps to 9-25 mm standard length and so lies inside zebrafish ontogeny (a life-stage, not a species, exclusion), the crossover exists only under an unstated sublinear spring-energy scaling, and the 'muscle-only has no realisable crossover' clause contradicts LaMSA storing only ~28% of muscle work in the work-limited regime.",
  "corrected_value": "2.17x overshoot in standard length (equivalently 10.3x in mass, 7-12x across the 0.28-0.45 g adult band); m* = 39 mg (8.5-173 mg) maps to 15.2 mm SL (9.1-25.0 mm)",
  "depends_on": ["m* = 39 mg central value (LaMSA route, from S30-organism.md - NOT verifiable, file absent from repo)", "m* interval 8.5-173 mg (same source, same unverified status)", "adult zebrafish body mass 0.4 g (search-summary; credible band 0.28-0.45 g)", "adult zebrafish standard length ~33 mm, used to anchor the mass-to-length mapping (search-summary; 3.25-3.45 cm)", "isometric scaling m proportional to L^3 across 9-33 mm zebrafish SL (my own assumption)", "unstated sublinear spring-energy scaling exponent (<1) in the author's derivation, without which no m* exists", "Sutton et al. 2019 muscle work density 15.0 J/kg and LaMSA storage limit 28% / 4.2 J/kg (full text)", "Sutton et al. 2019 modelled ~2.5 g muscle-vs-spring crossover and empirical 1 g-1 kg band (full text)", "Minicozzi et al. aquatic-vs-amphibious killifish jump-distance allometry sign (search-summary, abstract-level only)", "aerial launch (a ballistic phase exists); drag/weight ~2e-3 at 0.4 g computed for air, not water"]
}
```
