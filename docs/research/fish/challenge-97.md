# Challenge 97: the conditions on S26-D's "yes, conditionally", and the "no zebrafish ray EI" negative

**Claim under review** (S26-D, `docs/research/fish/S26-deepen.md` on
`origin/claude/deepen-s26-active-stiffening-48xj8q`, read in full):

> "CONDITIONS ON THAT CONCLUSION: it assumes isometric scaling at constant modulus and proportions from a
> bluegill ray to a 120 mm ray, and that the excised-ray clamping factor is achievable and sustainable by fin
> muscles in vivo. Neither is measured. No exocoetid or zebrafish ray EI exists in any source searched"

Recorded evidence level: *assumed*. Value: n/a.

**Outcome: WEAKENED.** The two stated conditions are real and really are unmeasured. But (a) the list leaves
out a third condition the conclusion rests on just as much, and (b) the zebrafish half of the negative is
wrong. A source the author read in full reports a measured, in-vivo zebrafish fin bending stiffness.

Nothing in this document was measured by me. Every number is tagged as measured (by the cited authors),
calculated (by me) or assumption.

---

## 1. Arithmetic, redone independently

Inputs, as S26-D states them: EI_passive = 3.8e-6 N m^2 (bluegill, relayed by Puri et al. 2018);
EI_req = 6.3e-4 N m^2 per ray (S6-D, calculated from assumptions); F_a = 12 (Alben et al. 2007, n = 1 as
reported); L_src = 40.3 mm (assumption); L_target = 120 mm.

All of the following are **calculated** by me (python3 -I, one-line script):

- (120 / 40.3)^4 = **78.6**. Scaled passive EI = **2.99e-4 N m^2**.
- Active factor needed = 6.3e-4 / 2.99e-4 = **2.11x**. Margin of the 12x = **5.69x**.
- Break-even source length, where the 12x exactly closes the gap: L_src = 120 / (6.3e-4 / (12 × 3.8e-6))^(1/4)
  = **62.2 mm**.
- The 5.69x margin in EI equals 5.69^(1/4) = **1.54x** in ray diameter. So a 120 mm ray that is ≥ 65 % of
  the isometric diameter (at constant E) still passes. One that is thinner fails.

The author's arithmetic reproduces. No fault there.

## 2. Hidden assumption: the condition list is incomplete

The claim says the conclusion "assumes" two things. It also assumes, without listing it here:

**C3. The bluegill ray behind 3.8e-6 N m^2 was ≤ 62 mm long, and the 40.3 mm figure is its length.**
The whole 5.7x margin uses L_src = 40.3 mm. S26-D itself tags this as an assumption: 40.3 mm is the group
*maximum* pectoral ray length of Alben's fish, and the 3.8e-6 figure comes from **Flammang et al. 2013**, a
different study whose specimen sizes S26-D records as `unknown`. Under the same isometric rule, the margin
goes as (L_src / 40.3)^4. Within the bluegill range the dependence runs in the conclusion's favour: a shorter
source ray gives a larger margin. The conclusion fails only if Flammang's ray was > 62 mm. I have no number
for Flammang's ray length (`unknown`; I did not access the full text either), so I cannot say this happened.
The point is that it is a carrying condition, at the same level as the two that are listed, and the
"CONDITIONS" sentence omits it. (S26-D's `depends_on` list does include the 40.3 mm assumption. The
conditions sentence under review does not.)

**C4. EI_req itself is assumption-derived** (m = 0.10 kg, N = 14, L = 0.12 m, δ/L ≤ 0.10). The sentence
"Neither is measured" can be read as saying everything else is measured. It is not. S26-D tested this input
across the replication's corner range (1.1e-4 to 3.1e-3 N m^2) and the 12x still passes at the upper corner
(needs 10.4x, which I recompute as 3.1e-3 / 2.99e-4 = 10.4x). So C4 does not flip the result, but it belongs
in the list of unmeasured inputs.

**Relaxing the listed isometry condition.** I did not find any measured exocoetid ray diameter or modulus
(see §4 for scope). So I can test relaxing isometry only parametrically: the conclusion survives up to
a 1.54x shortfall in diameter at constant E, or a 5.7x drop in E at isometric geometry (calculated). Alben
et al. 2007 give the bluegill composite modulus only as a range, 1e8 to 1e9 Pa (S26-D, full-text via
summarizer). That one decade is wider than the 5.7x margin. So "constant modulus" is the most fragile part
of condition 1. That is my inference; S26-D lists the condition but does not quantify how little room it has.

## 3. Is a proxy standing in for the quantity that matters?

Yes, and S26-D says so. The quantity that matters is the passive EI, and the achievable in-vivo locking
factor, of a ~120 mm exocoetid pectoral ray. The proxies are an excised ≤ 41 mm bluegill ray (EI) and one
excised bluegill ray (locking factor). The claim names both proxy steps correctly as unmeasured. No defect
here beyond C3.

## 4. The negative search, tested: a zebrafish fin EI does exist, in a paper the author read in full

The claim says "No exocoetid or zebrafish ray EI exists in any source searched". S26-D's §2 lists
**Puri et al. 2018**, *J Exp Biol* 221:jeb171777, PMC5868929 as read **full-text** (Europe PMC XML).

I re-fetched the same Europe PMC full-text XML (read-level: **full-text**). The title is "In vivo
quantification of mechanical properties of caudal fins in adult zebrafish". Its primary result is a
**measured** zebrafish bending stiffness:

- Abstract: "We detected overall bending moments of 1.5×10^-9 – 4×10^-9 N m^2 along the proximal–distal axis".
  (The authors write "bending moments", but the units and the Methods show it is bending stiffness EI.)
- Five adult wild-type AB zebrafish, six positions per fin, anaesthetised and alive. The fin was loaded as a
  cantilever with a line force.
- Surgical removal of interray tissue "revealed no significant changes to the overall bending stiffness".
  The authors conclude stiffness "predominantly relies on the mechanical properties of the rays".
- Ray/fin thickness at the loading positions is 200 to 40 µm. Effective I is 7e-16 to 3e-16 m^4. An
  effective Young's modulus is reported in Fig. S5C. I did not read the supplementary figures, so I have no
  number for it (`unknown`).

So a measured, in-vivo, ray-dominated **zebrafish caudal-fin EI exists** in a source on S26-D's own reading
list. It is whole-fin, not single-ray. The authors give no per-ray value. The claim's zebrafish negative
is false as worded: it is a search miss, not an absence in the literature. The exocoetid half of the
negative still stands at its stated scope. I ran no new exocoetid search, so I cannot extend that negative.

**Per-ray value (calculated by me, not reported by Puri):** I divide by Puri's 16–18 rays and assume the rays
act in parallel and share the load equally. That gives 1.5e-9 / 18 to 4e-9 / 16 = **8.3e-11 to 2.5e-10 N m^2
per ray**.

**Does it change the conclusion? Not decisively. It does show how fragile the proportions condition is.**

- Puri used the 3.8e-6 relay plus d^4 scaling (1–2 mm bluegill vs 0.1–0.2 mm zebrafish) to predict
  2–5e-9 N m^2 per fin. They called this "in reasonable agreement" with their measurement. Redoing their
  step with a diameter ratio of exactly 10 and 16–18 rays, I get 6.1–6.8e-9 (calculated), which is 1.5–4.5x
  above their measured range. The stated diameter ranges allow ratios from 5 to 20, i.e. 625x to 160,000x
  in EI. So this "agreement" is consistent within a ~2.5-decade uncertainty. It is weak support for
  constant-modulus d^4 scaling across taxa, not a test of it.
- Going the other way, I scale the measured zebrafish per-ray EI up to a bluegill ray using d^4, from
  d = 0.2 mm (the thick proximal end) to d = 1–2 mm. That gives **5.2e-8 to 2.5e-6 N m^2** (calculated).
  This is 1.5x to 73x *below* the 3.8e-6 relay. With d_zf = 0.1 mm, the values are 16x higher and bracket
  the relay. **The two sources disagree, or agree, depending entirely on which ray diameter goes into
  d^4.** I am not averaging them. I preserve both: if you build the baseline from zebrafish rather than from
  the bluegill relay, the required active factor runs from about 3x to about 150x. The 12x covers only the
  lower part of that span.
- My inference: this is the same weakness as C3 and the modulus point. The isometric extrapolation turns a
  modest uncertainty in source geometry into an error larger than the 5.7x margin, because EI goes as the
  fourth power of size. The zebrafish datum does not refute S26-D's number. It shows the conclusion is held
  up by geometric assumptions that no available measurement pins down to better than ~2x in diameter,
  which is ~16x in EI.

Scope of my searches: one Europe PMC full-text fetch of PMC5868929, keyword-scanned for stiffness, modulus,
diameter and length. I ran no new exocoetid, cyprinid or general web search. I did not access the Flammang
2013 full text or the Puri supplementary figures.

## 5. Evidence level

The claim is recorded as *assumed*. The first two sentences are a list of assumptions, so *assumed* fits
them. The third sentence is a **negative search result**. It is not an assumption, and it should carry its
search scope. Its zebrafish half is contradicted by full-text evidence (§4). That is a labelling defect as
well as a factual one.

## 6. Counter-examples or regimes missed

- **Puri et al. 2018 zebrafish in-vivo fin EI** (§4). Missed, although the author read the paper.
- In-vivo vs excised: Puri's fish were anaesthetised and intact. That gives a third boundary state, neither
  excised-free nor clamped. It is closer to the "passive in vivo" baseline that the active factor should
  multiply than Alben's excised rays are. S26-D does not use it.

## Verdict

**WEAKENED.** The two listed conditions are genuine and genuinely unmeasured. The arithmetic behind the
conclusion reproduces: 2.11x needed, 5.69x margin, break-even at L_src = 62.2 mm. But:

1. The conditions list omits the source-ray length (C3, carrying, unknown) and the assumption-derived
   EI_req (C4, non-carrying within the tested range).
2. "No … zebrafish ray EI exists in any source searched" is false. Puri et al. 2018, read full-text by the
   author, reports a measured in-vivo zebrafish caudal-fin EI of 1.5e-9 to 4e-9 N m^2 (n = 5 fish). The rays
   dominate it, and it gives ~0.8–2.5e-10 N m^2 per ray (my calculation, equal sharing assumed).
3. The "constant modulus and proportions" condition has much less room than the sentence suggests. The
   margin tolerates only a 1.54x diameter or 5.7x modulus deviation. Alben's own modulus range is 10x, and
   the zebrafish-derived baseline moves the required factor across ~3x to ~150x depending on diameter.

```swarm-challenge
{"claim_id": 97, "outcome": "weakened", "reason": "The two stated conditions are real and unmeasured and the arithmetic reproduces, but the list omits the carrying source-ray-length assumption (break-even L_src = 62 mm, Flammang ray length unknown), the margin tolerates only a 1.54x diameter or 5.7x modulus deviation, and the zebrafish half of the negative is false: Puri et al. 2018, which the author read in full, reports a measured in-vivo zebrafish caudal-fin EI of 1.5e-9 to 4e-9 N m^2.", "corrected_value": "zebrafish caudal-fin EI 1.5e-9 to 4e-9 N m^2 measured in vivo (Puri et al. 2018, n=5); ~8.3e-11 to 2.5e-10 N m^2 per ray calculated assuming equal sharing over 16-18 rays; no exocoetid ray EI found (scope unchanged)", "depends_on": ["Puri et al. 2018 J Exp Biol 221:jeb171777 PMC5868929, full-text: in-vivo zebrafish caudal-fin EI 1.5e-9 to 4e-9 N m^2, n=5 fish, interray removal no significant effect, 16-18 rays, thickness 200-40 um, bluegill ray diameter 1-2 mm vs zebrafish 0.1-0.2 mm", "Puri et al. 2018 relay of bluegill ray EI 3.8e-6 N m^2 citing Flammang et al. 2013", "S6-D EI_req 6.3e-4 N m^2 per ray (assumption-derived) and replicate-72 corner range 1.1e-4 to 3.1e-3 N m^2, as stated in S26-deepen.md", "Alben et al. 2007 locking factor ~12x (n=1 as reported) and composite modulus range 1e8-1e9 Pa, as relayed in S26-deepen.md (full-text via summarizer)", "Alben et al. 2007 bluegill max pectoral ray length 40.3 mm, used by S26-D as assumed source length", "assumption: rays in a zebrafish fin share bending load equally and act in parallel (per-ray division)", "assumption: EI scales as d^4 or L^4 at constant modulus (used only to quantify sensitivity, not endorsed)"]}
```
