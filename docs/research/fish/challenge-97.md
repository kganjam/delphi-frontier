# Challenge 97: the conditions attached to S26-D's "yes, conditionally"

**Claim under review** (from `docs/research/fish/S26-deepen.md`, branch
`origin/claude/deepen-s26-active-stiffening-48xj8q`, read in full along with its `S26_deepen_calc.py`):

> "CONDITIONS ON THAT CONCLUSION: it assumes isometric scaling at constant modulus and proportions from a
> bluegill ray to a 120 mm ray, and that the excised-ray clamping factor is achievable and sustainable by fin
> muscles in vivo. Neither is measured. No exocoetid or zebrafish ray EI exists in any source searched."

Recorded evidence level: *assumed*. Value: n/a.

**Verdict: WEAKENED.** The two conditions it names are real and are unmeasured. But the list leaves out two
other unmeasured assumptions, and relaxing one of them, using the author's own primary-derived number, cuts
the margin from 5.7x to 1.6x. The negative-search sentence is also too broad: a measured zebrafish fin EI sits
in a paper the author read in full.

Nothing in this document was measured by me. Each number is tagged *measured* (by the cited authors),
*calculated* (by me, in [`challenge-97_calc.py`](challenge-97_calc.py), run with `python3 -I`) or *assumption*.

## 1. Arithmetic, redone independently

These inputs come from S26-D: EI_req = 6.3e-4 N m^2 per ray, EI_passive = 3.8e-6 N m^2, F_a = 12, L = 120 mm,
L_src = 40.3 mm. I recomputed from them (calculated):

- (120/40.3)^4 = **78.61**. Scaled passive EI = **2.99e-4 N m^2**. Factor needed = **2.11x**. Margin of 12x =
  **5.69x**. These match S26-D.
- Break-even source-ray length = **62.2 mm**. This matches.

The arithmetic is correct. The question is what it rests on.

## 2. Hidden assumptions, tested by relaxing them

### 2a. Isometry (named in the claim), relaxed

Let ray diameter scale as d ∝ L^α at constant E and section shape, so EI ∝ L^(4α). The 12x closes the gap
only if **α ≥ 0.60** (calculated). At α = 0.5 the margin is 0.64, a fail. At α = 0 (no thickening, just a
longer ray) it is 0.07, a fail. So the result does not need strict isometry. It does need diameter to grow at
least ~0.6 power of length. That is a narrower and more testable condition than "isometry". Whether exocoetid
rays meet it is `unknown`.

The "constant modulus" part does have one weak external check (§3). The "proportions" part has none.

### 2b. Not named in the claim: the 12x stacks on top of 3.8e-6 (the strongest fault)

The headline route computes the locked EI as 3.8e-6 × 12 = 4.56e-5 N m^2 for a ≤40 mm bluegill ray. That
treats 3.8e-6 as the **unlocked (one-hemitrich-free) baseline**. The base condition of 3.8e-6 is not stated in
its only readable source, Puri 2018's one-sentence relay. S26-D's own back-calculation from Alben 2007's measured
1.98 N/m gives a **fully clamped** EI of 1.28e-5 N m^2 at L = 40.3 mm (calculated by S26-D, and reproduced by
me under the same assumptions: uniform cantilever, load at 2/3 L).

- The stacked value 4.56e-5 is **3.6x above** that clamped ceiling at 40.3 mm, and 8.6x or 29x above it if the
  tested ray was 30 or 20 mm (calculated). Within the author's own numbers, multiplying 12x onto 3.8e-6
  produces a ray stiffer than fully clamped. That is internally inconsistent unless 3.8e-6 belongs to a
  longer or thicker ray than Alben's.
- If I instead take the clamped EI itself as the ceiling and size-correct it to 120 mm (isometry still
  assumed), the margin over EI_req is **1.60x** (calculated, tested L = 40.3 mm). It rises to 2.2x at 30 mm and
  3.2x at 20 mm. Against the tip-heavy load (×1.47) the margin is **1.09x**. Against the replication's upper
  corner, EI_req = 3.1e-3, the margin is **0.32x, a fail**. S26-D reported a pass there, needing 10.4x.

So S26-D's "yes" survives this relaxation only narrowly at nominal load, and it flips at the upper corner that
S26-D said passes. S26-D did not size-correct its own clamped-ceiling route. It reported that route only
uncorrected, as "49x short".

### 2c. Not named in the claim: the length of the ray behind 3.8e-6

S26-D sets L_src = 40.3 mm, which is the maximum pectoral ray length of *Alben's* fish. But 3.8e-6 is relayed
from *Flammang* 2013, whose specimen sizes S26-D itself records as `unknown`. The conclusion flips if that ray
was longer than 62 mm (calculated). This is a third unmeasured condition. The claim's wording ("from a bluegill
ray") hides it.

## 3. The negative search: counter-example inside a source the author read

"No … zebrafish ray EI exists in any source searched" is **too broad**. Puri et al. 2018, *J Exp Biol*
221:jeb171777, PMC5868929 (**full-text**: Europe PMC fullTextXML, read by me, and also read in full by the
author) **measured** the bending stiffness of live adult zebrafish caudal fins:

- The values are 1.5e-9 to 4e-9 N m^2 along the proximal–distal axis, from 5 fish at 6 positions, under
  anaesthesia.
- Surgical removal of the interray tissue gave no significant change in stiffness. The authors conclude that
  stiffness is ray-dominated.

This is a whole-fin value, not an isolated single ray, so a strict "single-ray EI" reading would survive.
Even so, it is a measured, ray-dominated zebrafish EI, and the sentence as written denies it exists.

The paper also partly tests the "constant modulus" assumption, which is my inference, not the authors' claim.
Dividing by Puri's 16–18 rays (parallel-sum *assumption*) gives zebrafish per-ray EI ≈ 8.3e-11 to 2.5e-10 N m^2
(calculated). The bluegill/zebrafish ratio is then 1.5e4 to 4.6e4. At Puri's nominal 10x diameter ratio that
implies EI ∝ d^4.2–4.7 (calculated), which is consistent with d^4 at roughly constant E. With their stated
diameter ranges (1–2 vs 0.1–0.2 mm) the exponent could be anywhere from 3.2 to 6.7, so the check is weak. It
also scales *down* in size and tests diameter only, not the d ∝ L proportion that matters for a 120 mm ray. So
"neither is measured" is roughly right for proportions, but not quite right for modulus.

**Exocoetid:** I found no exocoetid ray EI. Scope: one standard web search ("flying fish pectoral fin ray
bending stiffness flexural rigidity measurement Exocoetidae"). Its hits were labrid, bluegill and mackerel work
and a robotic flying-fish model, with no ray EI. I did not search Google Scholar, Web of Science or CNKI.
**Zebrafish isolated-ray:** one standard web search ("zebrafish fin ray lepidotrichia bending stiffness flexural
rigidity three-point bending") found only Puri 2018 and its supplement, plus perch, gar and sturgeon three-point
bending abstracts. That part of the claim survives at this search depth.

## 4. Is the evidence level honest?

"Assumed" fits a sentence that lists assumptions. The defect is not mislabelling. It is **incompleteness**: a
reader handed only this sentence would think two conditions carry the result. At least four do: isometry
(α ≥ 0.6), in-vivo clamping, 12x stacking on an unlocked baseline, and Flammang's ray length ≤ 62 mm. The
third alone moves the margin from 5.7x to 1.6x.

## 5. What survives

- The two named conditions are genuine and unmeasured. In-vivo clamping has no measurement in any source I
  saw. Puri's anaesthetised in-vivo values speak only to the passive state.
- No exocoetid ray EI was found at my search depth.
- The arithmetic is correct.

## Sources

- S26-deepen.md and S26_deepen_calc.py, branch `origin/claude/deepen-s26-active-stiffening-48xj8q`. Read-level:
  full-text.
- Puri, Aegerter-Wilmsen, Jaźwińska & Aegerter 2018, *J Exp Biol* 221:jeb171777, PMC5868929. Read-level:
  full-text (Europe PMC XML).
- Alben, Madden & Lauder 2007, and Flammang et al. 2013: only as reported in S26-D. Read-level for me:
  could-not-access (not re-fetched); their values are used as S26-D gives them.
- [Curvature-induced stiffening of a fish fin (arXiv 1608.05891)](https://arxiv.org/pdf/1608.05891), [Puri et al.
  supplement (UZH)](https://ikarus.physik.uzh.ch/dam/jcr:591c8376-341d-4385-8d73-64b5b4106f6b/finbending.pdf),
  [labrid fin-ray stiffness (J Morphol, zendy listing)](https://zendy.io/title/10.1002/jmor.20830), [yellow perch
  lepidotrichia (SICB)](https://sicb.org/?p=17834). Read-level: search-summary.

```swarm-challenge
{"claim_id": 97, "outcome": "weakened", "reason": "The two named conditions are real and unmeasured, but the list omits that 12x is stacked on a 3.8e-6 baseline of unknown base condition and length (author's own clamped back-calc 1.28e-5, size-corrected, gives only 1.6x margin and fails at the 3.1e-3 upper corner) and the 'no zebrafish ray EI' sentence ignores Puri 2018's measured in-vivo ray-dominated zebrafish fin EI of 1.5-4e-9 N m^2, which the author read in full.", "corrected_value": null, "depends_on": ["S26-deepen.md inputs: EI_req 6.3e-4 N m^2, EI_passive 3.8e-6 N m^2, F_a 12, L 120 mm, L_src 40.3 mm", "S26-deepen.md back-calculation: Alben 2007 1.98 N/m clamped -> EI_clamped 1.28e-5 N m^2 at assumed tested length 40.3 mm, uniform cantilever with load at 2/3 L", "replicate-72 EI_req upper corner 3.1e-3 N m^2 and challenge-72 tip-heavy factor x1.47 (as reported in S26-deepen.md)", "Puri et al. 2018 J Exp Biol jeb171777 (full-text): in-vivo zebrafish caudal fin EI 1.5e-9 to 4e-9 N m^2, n=5 fish, interray removal no significant effect, 16-18 rays, ray diameter 0.1-0.2 mm vs bluegill 1-2 mm", "assumption: per-ray EI = fin EI / ray count (parallel sum)", "assumption: d ~ L^alpha at constant E and section shape for the isometry relaxation", "negative search scope: two standard web searches (exocoetid ray EI; zebrafish isolated-ray EI), no Scholar/WoS/CNKI"]}
```
