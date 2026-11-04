# S3-D — deepening S3 by attacking its most sensitive input: the lift coefficient CL_max

**Parent.** S3 (organism), `docs/research/fish/S3-organism.md` and `S3_budget.py` on branch
`claude/s3-organism-mass-budget-000ync` (commit `d0fd062f`). I read both in full. The task prompt
quoted S3's recorded answer as blank, so I took the answer from the S3 file, not from the prompt.
`S3_budget.py` is copied into this branch unchanged, so the parent model can be re-run here.

**Status: derived.** This is a recalculation of S3 with one input examined and replaced by a
bracket. **Nothing in this document is a measurement, by this project or by me.** Every computed
number is printed by `python3 -I docs/research/fish/S3-deepen_calc.py`. That script re-implements
S3 §3.5's launch-power model and asserts that it reproduces S3's 409 W kg⁻¹ and 2,878 W kg⁻¹.
Literature values carry their read-level in the sentence where they are used.

## 0. Result

**Verdict: STANDS** for S3's headline, that the power budget does not close. **The verdict is weakened
(not overturned) for S3's sub-claim** that central-thickness fin tissue "cannot even carry itself" at
1.38 m/s.

- **The input S3 is most sensitive to is CL_max** (1.07). In S3's launch model the
  required/available power ratio scales as **CL_max^−1.5**. I measured that elasticity numerically
  in the script at −1.50; it follows from P ∝ V_to³ and V_to ∝ CL^−½. Every other input enters with
  elasticity −1 or weaker:
  - η_h, f_m, run-up s and muscle power each move linearly;
  - wing areal density σ and body mass enter through M, and only partly.
- **It is the only input whose factor-of-2 error changes S3's conclusion** (computed, §1):
  - CL × 2 takes the most generous case from 2.87× short to **1.01× short**, which is parity.
  - Every other input × 2 leaves it 1.43–2.0× short.
  - CL also sets the self-carry sub-claim, which has only a **9 % margin**: it flips at CL = 1.16.
- **How S3's 1.07 was established.** It is a proxy. It is the steady CL_max of **isolated
  dragonfly (*Sympetrum sanguineum*) wings** in a wind tunnel at Re 700–2,400 (Wakeling &
  Ellington 1997, **abstract**, read in this session). It is Re-matched to the designed wings,
  which I computed at Re ≈ 2,400–3,000 (§3). It is **taxon-mismatched**: a corrugated insect wing,
  not fin membrane.
- **The improvement.** The real quantity is the CL_max of a fin-derived wing. The only
  measurements of that are on flying fish:
  - The Park & Choi 2010 abstract (read in this session) states only that CL peaks at 30–35°. It
    gives no value.
  - Their 2007 IUTAM proceedings, as quoted by a search engine, give **"about 1.0 ~ 1.1"**
    (**search-summary**).
  - A 2019 CFD study on a *C. hiraii*-like model gives **1.03** (**abstract**, read in this session).
  - **The best-supported value for a fin wing is therefore CL_max ≈ 1.0–1.1.** It brackets S3's 1.07.
- **Recomputed with that value** (calculated, not observed):
  - The most generous case is **2.75–3.17× short** (S3: 2.87×).
  - The S28 headline wing is **19–22× short** (S3: 20×).
  - Closure needs CL_max ≥ **2.16**. That is about 2× every steady value found for insect or fin
    wings (0.93–1.15).
- **The self-carry sub-claim does not survive as stated.** Across the sources the margin is
  1.01–1.25. At *C. splendens*' 1.15 it is exactly at parity (1.01). The honest restatement is
  "**at or near parity**, within input uncertainty", not "cannot".

---

## 1. Which input S3 is most sensitive to (recomputed)

**S3's model** (§3.5 of S3), recoded and checked against S3:
- V_to = √(2Mg / (ρ_air S CL)), with M = m_body + σS.
- The run-up time is t = 2s / V_to.
- The required power per kg of muscle is P = (V_to²/2) / t / η_h × M / (f_m m_body).
- This is compared with 142.7 W kg⁻¹. That value is Wakeling & Johnston 1998, which S3 read at
  abstract level.

**Controls** (script §0):
- The S10 wing at 2 BL, η_h 0.37 and f_m 0.6 reproduces **409 W kg⁻¹, 2.87×**.
- The S28-C wing reproduces **2,878 W kg⁻¹, 20.2×**. Both are asserted in the script.

**The conclusion under test** is S3's "power fails for every planform", where the least-failing
case is 2.87× short. Each input was doubled and halved, with all others held at S3's most generous
case (script §1):

| Input (S3 value) | ×2 → shortfall | ×0.5 → shortfall | Changes the conclusion at ×2 error? |
|---|---|---|---|
| **CL_max (1.07)** | **1.01×** | 8.11× | **Yes, to parity** |
| σ, wing areal density (0.138 kg m⁻²) | 5.21× | 2.00× | No |
| η_h (0.37) | 1.43× | 5.73× | No |
| f_m (0.6) | 1.43× | 5.73× | No |
| run-up s (2 BL) | 1.43× | 5.73× | No |
| muscle power (142.7 W kg⁻¹) | 1.43× | 5.73× | No |
| m_body (0.40 g) | 5.64× | 1.84× | No |

**The self-carry sub-claim** is σ > ½ρV²CL/g at 1.38 m/s. S3's margin is 0.138 / 0.127 =
**1.086**. A CL of **1.162** flips it, as does a σ only 8 % lower. CL × 2 gives 0.54, so the fin
easily carries itself.

**Why CL rather than σ** for this sub-claim: both have elasticity 1 here. CL is the only input
shared by *both* conclusions, and it is the one with the steeper exponent in the power result.
σ was already bracketed honestly in S3 (§2a–2b, with a separate measurement proposed in S3 §6.2).

**Why CL rather than η_h.** S3 itself called η_h "the decisive unmeasured input" (S3 §5). The
recomputation does not support that ranking. η_h has elasticity −1, and doubling it leaves the case
1.43× short. S3's own §6.1 already found that no η_h ≤ 1 closes any planform alone. **The
recomputation contradicts S3's prose ranking, but not its numbers.** (Inference from the table.)

## 2. How well was CL_max = 1.07 established?

**Chain of custody** (read in this session from sibling branches):
- S3 says "project CL_max 1.07 (derived, S2/S28), used unchanged".
- replicate-24 (`claude/fish-replicate-24-4dc5w4`) traces it to Wakeling & Ellington 1997, as
  the "corrected C_L,max" from challenge-23. The band there is 0.9–1.15, or 0.7–1.15 on another
  replicate branch.

**Primary source.** Wakeling & Ellington 1997, "Dragonfly flight. I. Gliding flight and steady-state
aerodynamic forces", *J. Exp. Biol.* 200:543–556, doi:10.1242/jeb.200.3.543. **Read-level:
abstract** (Europe PMC REST, this session). Quoted:
- "Lift and drag forces were additionally measured from isolated wings and bodies of *S. sanguineum*
  and the damselfly *Calopteryx splendens* in a steady air flow at Reynolds numbers of 700-2400 for
  the wings".
- "The maximum lift coefficients (CL,max) were 1.07 for *S. sanguineum* and 1.15 for *C. splendens*,
  which are greater than those recorded for all other insects except the locust."
- From free glides: "The maximum lift coefficient (CL) recorded from these glides was 0.93; however,
  this is not necessarily the maximum possible from the wings."

**Assessment:**

| Question | Answer |
|---|---|
| Measured? | Yes, for **isolated insect wings**. Steady flow, force balance. |
| Measured for the quantity S3 needs? | **No. It is a proxy.** S3 needs the CL_max of a zebrafish pectoral-fin membrane, scaled up and spread as a wing. |
| Re match | **Good.** Designed wings at V_to run at Re ≈ 2,400–3,000 (computed, §3). That sits at the top of W&E's 700–2,400. |
| Structure match | **Poor.** Dragonfly wings are corrugated, vein-stiffened and cuticular. A fin is a ray-supported membrane that S3 §3.4 showed to be 120–3,600× too floppy at the required load, so in practice it would billow and camber. The sign of that effect on CL_max is `unknown`: membrane camber can raise CL, while flutter and twist-out can lower it. |
| Internal disagreement | 1.07 vs 1.15 between species, and 0.93 in free glide. S3 used only 1.07. **Preserved here** (§3). |
| Has it hardened by repetition? | Partly. "Project value" in S3 traces to one abstract sentence about dragonflies. replicate-24 had it at search-summary; I raised it to abstract this session. |

## 3. Improving it: a CL_max for a fin-derived wing

**Sources found** (scope of searches at the end of this section):

| # | Source | Quantity | Value | Re | Read-level |
|---|---|---|---|---|---|
| C1 | Park & Choi 2010, *J. Exp. Biol.* 213:3269, doi:10.1242/jeb.046052 | Whole dried *Cypselurus hiraii* model, wind tunnel | "The lift coefficient is largest at attack angles around 30∼35 deg" | **No value in the abstract** | abstract (Europe PMC, this session). Full text: could-not-access (journals.biologists.com returned a captcha page) |
| C2 | Park & Choi, IUTAM 2007 proceedings ("S1_Park.pdf") | same group, flying-fish models | **"the maximum lift coefficients are about 1.0 ~ 1.1"** | `unknown` from this source | **search-summary**: the sentence was quoted by a search engine. The PDF host (flair.monash.edu, and its mirror) did not resolve from this session |
| C3 | 2019 *Bioinspir. Biomim.*, doi:10.1088/1748-3190/ab23e6, "Numerical prediction of aerodynamic performance for a flying fish during gliding flight" | CFD on a *C. hiraii*-like pectoral-fin model | "maximum lift force coefficient of 1.03" (angle not rendered in the abstract text) | `unknown` | abstract (Europe PMC, this session). **This is a simulation, not a measurement** |
| C4 | Park & Choi 2010, as relayed by S2-D-D (`claude/deepen-s2-d-imobtp`) | test Re | ~1.9–2.2 × 10⁴ | — | S2-D-D says full-text |
| C5 | "C_L = 0.78, Park & Choi 2010", as used by S7 and descendants | — | 0.78 | — | search-summary, via S7. **replicate-201 read the abstract and found no 0.78 in it.** I also did not find it (C1 abstract). **Unconfirmed; carried only as a low sensitivity bound** |

**Disagreement preserved:**
- **Insect wings:** 0.93 (glide), 1.07 and 1.15 (isolated).
- **Fin wing:** 1.0–1.1 (C2, measured, search-summary) and 1.03 (C3, CFD).
- **Unconfirmed relay:** 0.78 (C5).

These are not averaged. The fin-wing sources cluster at **1.0–1.1**. My inference is that the
agreement is real but not independent, because C3 was built to mimic C1's model.

**Limits of the improvement, all kept visible:**
- **Re mismatch, in the opposite direction.** The flying-fish data are at Re ~2 × 10⁴ (C4). That is
  ~8× above the designed zebrafish wings, while the insect proxy is Re-matched. So I have traded a
  taxon proxy for a Re proxy. The direction of the Re effect on CL_max between 2.4 × 10³ and
  2 × 10⁴ for a thin membrane is `unknown` to me. My one search on ultralow-Re plate CL_max found
  no value at Re ≈ 2–4 × 10³.
- **Whole animal vs wing.** C1/C2 measured the whole fish, with pelvic fins spread and the body
  included. The **reference area used to normalise CL is `unknown`** to me, because the full text
  was unread. If it was pectoral area only, the wing-alone CL is lower. The C1 abstract says the
  pelvic fins *increase* lift, and a search-engine summary of the paper says that without them CL is
  ">20 %" lower (**search-summary**).
- **A flying-fish fin is not a zebrafish fin.** It has AR 9–10.7 (S2-D-D, full-text), long stiff
  rays and a 20 cm body. The designed wings are AR 4–6. Lower AR generally lowers CL_max at a given
  α in attached flow but delays stall. The net effect is `unknown`.
- **Transient (unsteady) lift was not attacked.** An impulsively started wing can briefly exceed its
  steady CL_max through a leading-edge vortex. Revolving-wing studies report "high" coefficients
  (Usherwood & Ellington 2002, **search-summary**). I did not obtain a numeric value, so none is used.
  It would last only a few chord-lengths of travel, roughly milliseconds at these chords and speeds
  (my inference). Whether that carries a fish through launch is not computed.

**Search scope for the negative results:**
- Europe PMC REST: 3 DOI queries, all returned abstracts.
- Web searches:
  - 1 standard and 1 extended search for the Park & Choi CL_max value;
  - 1 standard search for ultralow-Re plate CL_max;
  - 1 standard search for the Usherwood & Ellington revolving-wing value.
- Fetch attempts failed on journals.biologists.com (captcha), and on flair.monash.edu,
  eng-web77-v02.ocio.monash.edu, typeset.io and semanticscholar.org. These hosts did not resolve
  from this session's network policy. **Reading Park & Choi Table 2 or Figure 5 would raise C2
  from search-summary to full-text and settle the reference-area question.**

**The measurement that would settle it.** Mount an excised pectoral fin from a long-fin zebrafish
mutant (or a fin-tissue-thickness membrane replica of the designed planform) on a sub-mN force
balance in a low-speed wind tunnel at V = 2–6 m/s, and record the lift polar to stall.
- Expected lift is ~0.5 mN for 1 cm² at 3 m/s and CL 1 (computed: ½ × 1.225 × 9 × 1 × 10⁻⁴ N).
  So a micro-balance of the kind used for insect wings is needed.
- **Cost (my estimate, not a quote):** days of tunnel time where an insect-flight lab already has
  the rig. Fresh tissue is needed, because a dried fin's camber and stiffness differ.
- This would give CL_max at the right Re *and* the right material at the same time.

## 4. Recompute S3 with the improved input

Calculated by script §2. "Generous" is S10, 2 BL, η_h 0.37, f_m 0.6. S28-C is the same model on the
192 mm² headline wing.

| CL_max (source) | Generous case: W kg⁻¹ muscle (× short) | S28-C (× short) | Self-carry margin at 1.38 m/s |
|---|---|---|---|
| 1.07 (S3 baseline, W&E dragonfly) | 409 (2.87×) | 20.2× | 1.09 |
| 1.15 (W&E damselfly) | 367 (2.57×) | 18.1× | **1.01** |
| 0.93 (W&E free glide) | 505 (3.54×) | 24.9× | 1.25 |
| **1.0 (C2 low)** | **453 (3.17×)** | **22.3×** | **1.16** |
| **1.1 (C2 high)** | **392 (2.75×)** | **19.4×** | **1.06** |
| 1.03 (C3 CFD) | 433 (3.04×) | 21.4× | 1.13 |
| 0.78 (C5, unconfirmed) | 657 (4.61×) | 32.4× | 1.49 |
| *2.16, a scenario and not a source: what closure needs* | *143 (1.00×)* | *7.0×* | *0.54* |

The CL needed to close the other planforms was also computed (generous assumptions otherwise):
- **2.39** for S2-mid;
- **7.93** for S28-C.

**Conclusion (my inference from the computation):**
- **Power budget: STANDS.**
  - Closure of even the most generous case needs CL_max ≥ 2.16.
  - That is 1.9–2.2× every steady CL_max found for any insect or fin wing (0.93–1.15).
  - It is 2.0–2.2× the fin-wing values (1.0–1.1).
  - On the improved input the shortfall is **2.75–3.17×**, the same as S3's 2.87× within the bracket.
  - The S28 headline wing would need CL 7.9, so that wing is excluded by any lift coefficient.
- **Self-carry sub-claim: weakened.** Every source gives a margin ≥ 1.0, so the sign never flips,
  but the margin is 1.01–1.25 (excluding unconfirmed C5). Given σ's own bracket (0.042–0.44 kg m⁻²),
  the statement "at central thickness, fin tissue cannot lift itself at 1.38 m/s" is better read as
  "fin tissue at central thickness is **at roughly break-even** at today's burst speed". The
  conclusion S3 drew from it is unaffected: at 1.38 m/s a wing can carry essentially nothing beyond
  itself.
- **S3's ranking of η_h as "the decisive unmeasured input" is not supported** by the recomputed
  sensitivities. CL_max has the larger exponent, and η_h alone cannot close any case.

## 5. What this does NOT establish

- It does not measure CL_max. The improved bracket rests on one search-summary sentence (C2) and one
  CFD abstract (C3), both at Re ~8× too high and normalisation `unknown`.
- It does not address unsteady or transient lift during water exit, or a multi-stroke taxi launch.
  Both lie outside S3's model.
- It inherits, unchanged, every other S3 input and caveat:
  - η_h from pike;
  - f_m, which was assumed;
  - muscle power from *Scorpaena* (abstract);
  - σ from caudal-fin thickness with proxy densities;
  - the constant-acceleration run-up.

```swarm-result
{"subproblem": "S3-D", "evidence": "derived (recalculation of S3's model; CL_max improved from an insect-wing proxy to fin-wing values at search-summary and CFD-abstract level; no new measurement)", "answer": "S3's launch-power shortfall scales as CL_max^-1.5 and CL_max is the only input whose factor-2 error reaches parity; replacing the Re-matched dragonfly-wing proxy (1.07) with the flying-fish fin-wing bracket 1.0-1.1 gives a calculated 2.75-3.17x shortfall in the most generous case (closure needs CL_max >= 2.16, about 2x any steady insect or fin-wing value found), so the power verdict stands, while the 'fin tissue cannot carry itself at 1.38 m/s' sub-claim weakens to near break-even (margin 1.01-1.25).", "key_number": "CL_max of a fin-derived wing = 1.0-1.1 (flying fish, Park & Choi IUTAM 2007, search-summary; 1.03 CFD, abstract) vs S3's 1.07 dragonfly proxy; closure threshold CL_max = 2.16 (calculated)", "verdict": "stands", "depends_on": ["S3 conclusion and launch model: docs/research/fish/S3-organism.md and S3_budget.py @ d0fd062f (constant-acceleration run-up, P = (V^2/2)/t/eta_h * M/(f_m m_body))", "law: quasi-steady lift L = 0.5 rho V^2 S CL, take-off at V_to = stall speed", "Wakeling & Ellington 1997 J Exp Biol 200:543 abstract: isolated wing CL,max 1.07 (S. sanguineum), 1.15 (C. splendens), Re 700-2400; free-glide CL 0.93", "Park & Choi 2010 J Exp Biol 213:3269 abstract: whole-fish CL largest at 30-35 deg, no value stated", "Park & Choi IUTAM 2007 proceedings: maximum lift coefficients about 1.0-1.1 (search-summary; reference area unknown)", "Bioinspir Biomim 2019 doi:10.1088/1748-3190/ab23e6 abstract: CFD CL max 1.03 on C. hiraii-like model (simulation)", "Park & Choi 2010 test Re ~1.9-2.2e4 (via S2-D-D, full-text)", "assumption: steady CL_max of a flying-fish fin wing at Re ~2e4 transfers to a zebrafish-fin wing at Re ~2.4-3e3 and AR 4-6", "assumption: transient leading-edge-vortex lift does not govern take-off (not computed)", "C5 CL 0.78 relayed by S7 (unconfirmed; used only as sensitivity bound)", "S3 input: hydromechanical efficiency eta_h 0.37 (pike, Frith & Blake via S29, abstract)", "S3 input: fast-muscle power 142.7 W/kg (Wakeling & Johnston 1998, abstract)", "S3 input: muscle fraction f_m 0.3/0.6 (assumption / secondary review via S29)", "S3 input: run-up 0.5-2 body lengths of 4 cm (assumption)", "S3 input: central fin areal density 0.138 kg/m^2 (Puri 2018 caudal thickness 200->40 um, Robertson 2008 body density, Tont 1977 bone density via S9, assumed 20% ray fraction)", "S3 input: body mass 0.40 g (project brief)", "S3 input: measured zebrafish burst 1.38 m/s (Miln et al. 2021 via S28)", "S3 inputs: planform areas S10 1070 mm2, S2-mid 900 mm2, S28-C 192 mm2 (sibling designs) and spans used for Re", "air density 1.225 kg/m3, kinematic viscosity 1.5e-5 m2/s, g 9.81"]}
```
