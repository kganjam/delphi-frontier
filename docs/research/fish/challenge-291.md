# Challenge 291: adversarial review of S30-D ("the realisable LaMSA window falls")

**Claim under review:** S30-D, `docs/research/fish/S30-deepen.md` and `S30-deepen_calc.py`, on branch `claude/deepen-s30-launch-budget-jb7qj4` (commit `efe54c57`). I read the whole `.md` and the top of the script.

**Recorded evidence level:** derived. **Value:** 0.94 mg crossover mass.

**Outcome: WEAKENED.**
- The arithmetic is correct.
- The evidence label "derived" is honest.
- The word **"bounded" / "upper bound" is not honest.** The strain ε that carries the result is a strain fish fibres were *observed to reach* in a C-start. It is not a *capacity ceiling*.
- When that assumption is relaxed, the verdict "no realisable window" survives at the geometric β = 1/3. At S30's measured β = 0.533 it holds only by a margin smaller than the author's own input uncertainty.

Nothing below is a measurement. Every number I computed is labelled as calculated.

---

## 1. Independent arithmetic

I recomputed in a fresh Python one-liner from the stated inputs, without running the author's script.

**S30 baseline, reproduced** (calculated):
- R₀ = 0.30 × 53 × 0.93 × 0.37 / 10.17 = 0.5380.
- m\* = 250 mg × R₀³ = **38.9 mg**.

**Teleost w = ½σ₀ε/ρ with ρ = 1060 kg/m³** (calculated). m\* columns are for β = 1/3, 0.36, 0.40, 0.533:

| σ₀ (kPa) | ε | w (J/kg) | m\* β=1/3 | m\* β=0.36 | m\* β=0.40 | m\* β=0.533 |
|---|---|---|---|---|---|---|
| 250 | 0.13 | 15.33 | **0.942 mg** | 1.42 | 2.39 | 7.62 |
| 250 | 0.125 | 14.74 | 0.837 mg | 1.28 | 2.17 | 7.08 |
| 200 | 0.10 | 9.43 | 0.220 mg | 0.37 | 0.71 | 3.07 |
| 300 | 0.15 | 21.23 | 2.50 mg | 3.52 | 5.39 | **14.0** |
| 300 | 0.24 | 33.96 | 10.2 mg | 13.0 | 17.4 | **33.9** |

**Other checks** (calculated):
- 0.4 g / 0.942 mg = **425×**. This reproduces.
- The validity floor is the mass at which Re_air reaches 700. At m = 37.5 mg: chord 3.29 mm, V 3.19 m/s, ν = 1.5×10⁻⁵ m²/s, giving Re = **699**. This reproduces the 37.5 mg floor.

**One inconsistency in the harvester's reproduction (not the author's):**
- The claim text computes w with ε = 0.125, giving 14.7 J/kg.
- The document and script use ε = 0.13, giving 15.3 J/kg and m\* = 0.94 mg.
- With ε = 0.125, m\* is **0.84 mg**.
- The two are about 11 % apart in m\*. This does not change any conclusion, but the claim's working and its headline number come from different ε values.

**Arithmetic verdict:** all headline figures reproduce, including the crossover formula that the harvester did not re-run.

## 2. Proxy: is C-start fibre strain the quantity that matters?

**No.** The quantity that matters is the largest fibre strain a teleost fast fibre can sustain at high force while loading a compliant series spring. The author's proxy is the fibre strain that trout, rock cod and sculpin fibres were *observed* to reach during C-starts (search-summary).

These two quantities have different causes:
- In a C-start, fibre strain is set **kinematically**, by body curvature and myotomal gearing. The fibres shorten as far as the bend requires, at high velocity and therefore well below P₀.
- In spring loading, strain is set by spring compliance and the fibre's **force–length** curve, in a slow, near-isometric contraction.
- An observed operating strain is therefore not a ceiling. The product ½σ₀ε is an upper bound **only conditional on ε**. Since ε is not itself a bound, w ≈ 15 J/kg is a **conditional central estimate** ("if the fish myotome loads a spring with its C-start strain"), not an upper bound.
- The author states this caveat in §3.2 and §7, calling it the "load-bearing assumption". But the headline, the swarm-result answer and the claim text still say "bounded" and "upper bound". **That headline wording is the defect.**

**The right quantity:** the width of the zebrafish (or teleost) fast-fibre force–length curve at high force. The author lists this as `unknown`. My search (one standard web search; read level search-summary) found only partial data:
- **Sculpin fast fibres:** force "strongly dependent on sarcomere length between 2.1 and 3.6 µm", with optima of 2.33–2.45 µm (PhD thesis, via search summary; core.ac.uk).
- **Zebrafish larval fast muscle:** optimum about 2.15 µm (bioRxiv 2020.04.02.010298 and PMC2346565, search summary).

Neither source gives the strain range over which force stays near P₀. So I cannot replace ε with a measured capacity value either. **My inference:** the sculpin data show fish fast fibres produce force over a sarcomere range well beyond ±13 %, so 0.13 is not obviously a ceiling. I did not quantify this.

## 3. Hidden assumption relaxed

**Question:** what w, and what ε, would restore a window at the 37.5 mg validity floor? (Calculated, with S30's η chain and f = 0.30.)

| β | w needed | ε needed at 250 kPa | ε needed at 300 kPa |
|---|---|---|---|
| 1/3 | 52.3 J/kg | 0.44 | 0.37 |
| **0.533** (S30's measured upper β) | **35.8 J/kg** | **0.30** | **0.25** |

**Reading:**
- **At β = 1/3** the window needs about 37–44 % fibre shortening at full stress. This is far above any fish value the author cites. "Falls" is robust here.
- **At β = 0.533** it needs only about 25–30 %. The author's own carp curvature ceiling (ε = 0.24 at 300 kPa) gives **33.9 mg**, which is within 10 % of the 37.5 mg floor. A σ₀ of about 330 kPa would close that gap, as would a strain of about 0.25.
- The author says "every one-side teleost value lies below that floor". That is true, but at this corner it is a knife-edge, not a margin.
- The frog itself implies ε ≈ 0.37 (derived by the author). So a vertebrate spring-loading muscle *does* reach this regime. Whether fish fast fibres could do so, if built into a spring architecture, is exactly what is unknown.

**Second assumption: treating "below the CL_max data floor" as "no window".**
- Below 37.5 mg the result is *unvalidated*, not *negative*. Calling it "no realisable window" is S30's own rule, applied consistently by the author.
- Strictly, the result reads: "no window within the mass range where the aerodynamic inputs are valid".
- **My inference, not tested:** CL_max tends to fall and drag rises as Re drops, so extrapolating would probably make takeoff harder, not easier. The direction of the conclusion is likely right, but its logical status is weaker than "falls" implies.

## 4. Is the evidence level honest?

- **"derived" for 0.94 mg: yes.** The document labels every m\* as calculated and gives the σ₀ and ε inputs at search-summary level.
- **"bounded" / "upper bound": no.** As shown in §2, this presents a conditional estimate as a bound. It is a framing defect, not a numerical one.
- The teleost σ₀ (200–300 kPa) and the C-start strains are search-summary level, as the claim says. I did not raise that read level.

## 5. Missed regime, taxon or counter-example

- **No teleost spring-loading measurement exists in my scope either.** Scope: two standard web searches (fish fast-muscle force–length/sarcomere range; Mendoza & Azizi fascicle strain), both at search-summary level. Not searched: full texts, theses, Web of Science or Scopus, non-English sources.
- **Mendoza & Azizi 2021** (search summary, ouci.dntb.gov.ua listing) attribute the Cuban tree frog's high storage to **higher pennation and stiffer tendons**. That is an *architectural* tuning, not a muscle-tissue property unique to frogs.
  - To first order, work per volume (σ × ε) does not depend on pennation. So this neither supports nor refutes transferring the frog value.
  - It does support the reading that w depends on how muscle and spring are paired, which a designed LaMSA fish would by definition change. The author's §2 inference already points this way.
- I found no published fish counter-example that stores ≥ 35 J/kg in a spring. I also found no evidence that fish fibres cannot.

## 6. Verdict

**WEAKENED.**
- The arithmetic, the 425× ratio and the 37.5 mg floor all reproduce (calculated).
- The sign and "the zebrafish is too large" survive.
- **But 0.94 mg is a conditional central estimate, not an upper bound.** It assumes a spring-loaded myotome shortens no more than in a C-start, a kinematic operating strain used as a proxy for force–length capacity.
- With that assumption relaxed:
  - At β = 1/3, "no window" survives unless ε reaches ≥ 0.37.
  - At S30's measured β = 0.533, the window returns at ε ≈ 0.25–0.30. That lies at the author's own carp ceiling, which already reaches 33.9 mg against a 37.5 mg floor.
- **Corrected statement:** the realisable single-impulse window is *very probably absent at β ≈ 1/3*, and *marginal and unresolved at β ≈ 0.5*, pending a teleost fast-fibre force–length width measurement (the author's §5 experiment).

## Sources

| Source | Read level | Used for |
|---|---|---|
| S30-deepen.md and S30-deepen_calc.py (`claude/deepen-s30-launch-budget-jb7qj4`, efe54c57) | full-text (md); script read to line ~80 | All claim inputs |
| [Mendoza & Azizi 2021, OUCI listing](https://ouci.dntb.gov.ua/works/4VbbDJb4) | search-summary | Pennation and tendon-stiffness attribution |
| [Sculpin fast-fibre length–tension (thesis, core.ac.uk)](https://core.ac.uk/download/30318937.pdf) | search-summary | Force depends on SL from 2.1 to 3.6 µm; optima 2.33–2.45 µm |
| [Zebrafish larval muscle mechanics (bioRxiv)](https://www.biorxiv.org/content/10.1101/2020.04.02.010298.full.pdf) and [PMC2346565](https://pmc.ncbi.nlm.nih.gov/articles/PMC2346565) | search-summary | Optimum about 2.15 µm; no force–length width extracted |

```swarm-challenge
{"claim_id": 291, "outcome": "weakened", "reason": "Arithmetic reproduces (m* 0.942 mg, 425x, 37.5 mg floor), but w~15 J/kg rests on in-vivo C-start fibre strain (a kinematic operating strain, search-summary) labelled as an upper bound when it is not a capacity ceiling; relaxing it, the window stays shut at beta=1/3 (needs eps>=0.37) but at S30's measured beta=0.533 reopens at eps~0.25-0.30, which the author's own carp ceiling (33.9 vs 37.5 mg) nearly reaches.", "corrected_value": "m* ~0.94 mg (calculated) as a conditional central estimate assuming C-start strain, not an upper bound; capacity-limited range 0.22 mg to ~37.5 mg+ at beta=0.533 if eps>=0.25-0.30 (calculated)", "depends_on": ["S30 crossover m* = m0*R0^(1/(beta-alpha)), alpha=0, m0=0.25 g (S30, via S30-D)", "S30 R0 inputs f=0.30, eta_s=0.93, eta_h=0.37, need=10.17 J/kg (S29, via S30-D)", "S30 beta range 1/3 to 0.533 (Fish1990, PROJECT-TRANSCRIBED, via S30-D)", "teleost fast-fibre P0 200-300 kPa (search-summary, via S30-D)", "C-start fibre strain 0.10-0.15 and carp 0.24 ceiling (search-summary, via S30-D)", "muscle density 1060 kg/m3 (assumed)", "37.5 mg validity floor from Re_air>=700 CL_max data (S2, recomputed: Re 699 at 37.5 mg)", "sculpin fast-fibre force-length range 2.1-3.6 um (thesis, search-summary)", "ASSUMPTION (mine): C-start operating strain is not a force-length capacity ceiling"]}
```
