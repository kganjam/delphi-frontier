# S29-D: deepening S29 by attacking its weakest input, the hydromechanical efficiency η_h

**Parent:** S29, `docs/research/fish/S29-organism.md` on branch `claude/s29-launch-energy-2iuixr` (commit `44ed2195`), read in full.

**Status:** derived. This is a recalculation on S29's stated inputs, with one input replaced by values other authors report. **This project measured nothing new.** Every number below comes from `python3 docs/research/fish/S29-deepen_calc.py`. Values from the literature carry their source's read level beside them.

**Result: STRENGTHENS.**

The 0.37 that S29 uses is a *model output* for a *muscle-driven* pike C-start. It is not a measurement of energy flow, and it is not a figure for the mechanism S29 proposes. The only *measured* value for the mechanism S29 actually proposes, a pre-bent elastic fish body released by a latch, is **KE_final / E_stored ≈ 0.10** (Conte et al. 2010). A second similar device gives about 0.11. S29's chain implies 0.323.

With the measured value in place of the implied one:
- the central shortfall rises from **1.86× to 6.0×** (range 3.9–10×);
- the all-skeletal-muscle break-even S29 left open no longer exists: 1.96× short even at the frog maximum;
- "spring volume passes" no longer holds for fish-grade tendon.

On the narrower question, using only *muscle-driven* efficiencies (pike and carp), the verdict **stands**. No reported value reaches the 0.45 at which the gap would close.

---

## 1. Which input the answer is most sensitive to (recomputed)

S29's shortfall is

  shortfall = (½V² + W_drag/m) / (f · w · η_s · η_h) = 10.173 / (0.30 · 53 · 0.93 · 0.37) = **1.859**,

which reproduces S29 and challenges 227 and 231 exactly.

Each input below was multiplied by 2 and divided by 2 with everything else held at the central case (script §1):

| Input (S29 value) | ×2 | ÷2 | Elasticity | Can a ×2 error flip the verdict? |
|---|---|---|---|---|
| η_h (0.37) | 0.93 | 3.72 | −1 | **Yes.** It flips at ×1.86 |
| w, muscle work stored (53 J/kg) | 0.93 | 3.72 | −1 | Yes, at ×1.86 |
| f, muscle fraction (0.30) | 0.93 | 3.72 | −1 | Only up to the physical ceiling f ≤ 0.60, i.e. ×2.00 |
| η_s, spring return (0.93) | — | 3.72 | −1 | **No.** It would need η_s = 1.73 > 1 |
| Cd (0.2) | 1.97 | 1.80 | 0.09 | **No.** Drag is 6.5 % of the need |
| V target (4.37 m/s) | 7.44 | 0.47 | 2 | Yes, at V ÷ 1.36 |

**Why η_h, and not V, w or f** (my judgement, with the reasons stated):
- **V has the largest elasticity, but it is not an input.** It is the *specification* the S29 question asks about ("reach 4.37 m/s"). Its own uncertainty belongs to S28. S29 already flags that the mass-consistent value of 5.53 m/s is *more* negative.
- **η_h, w and f tie on elasticity**, so the choice turns on how well each is established.
  - **f** is physically capped at about ×2.
  - **w** is a measurement of the right *kind* of quantity: energy stored in a series tendon by a single slow contraction (Mendoza & Azizi 2021). Only the taxon is wrong.
  - **η_h** is the only one of the three that is a *different kind of quantity* from the one the budget needs. It is an efficiency of an *actively muscle-driven* start, applied to a *passive spring release*.
  - Challenge 227 had already found that "binding" rests almost entirely on η_h. Break-even falls at η_h = 0.450 for w = 81 and 0.688 for w = 53 (script §2).

## 2. How well is η_h = 0.37 established?

**What S29 says.** S29 gives "Frith & Blake, energetics of fast-starts in *Esox lucius*, ABSTRACT, from a UBC record". It quotes a C-start range of 0.34–0.39 and an S-start value of 0.27.

**What the primary paper says.** Frith & Blake 1995, *J. Exp. Biol.* 198:1863–1873, doi:10.1242/jeb.198.9.1863. **Read level: abstract** (Europe PMC record).
- The efficiencies "are **calculated from hydrodynamic theory**". "The Weihs model is employed and modified", and is applied to filmed kinematics.
- "Hydrodynamic efficiencies for fast-starts **range from 0.16 to 0.39**". The values are lower for S-starts during the first two tail beats.
- Useful power is defined as "the power used to accelerate the virtual mass of the fish, i.e. fish body mass + longitudinal added mass, in the direction of motion".

**Assessment.**

| Question | Answer |
|---|---|
| Measured? | **No.** It is a model estimate by the authors: Weihs's theory applied to measured kinematics. The kinematics are measured; the energy flows are calculated. Over many citations it has come to read as a measured efficiency. S29's ledger lists it under "Measured (by others)", which is a mislabel. |
| Range | **The sources disagree.** S29 (via the thesis record) gives 0.34–0.39 for C-starts and 0.27 for S-starts. The 1995 paper's abstract gives 0.16–0.39 across fast-starts and does not give a C-start-only range. I could not reach the thesis (open.library.ubc.ca is outside this session's network allowlist), so the two ranges are not reconciled here. Both are reported. |
| Proxy for what? | For "the fraction of the actuator's work that ends up as forward kinetic energy of the fish". In pike, that actuator is *muscle that shapes the body wave throughout the stroke*. In S29 it is a *spring released through a latch*, which unbends along its own dynamics. These are different processes. |
| Definition fit | Frith & Blake's useful power includes the longitudinal added mass. S29 applies η_h to body KE plus drag work. That roughly offsets: drag is 6.5 % of KE, and the added mass is unknown from the abstract. The effect is small next to the issues above. |
| Read level | abstract (paper); could-not-access (thesis). |

**Evidence level of the input as S29 used it: transferred model estimate, abstract read level, wrong mechanism.**

## 3. Improving it

### 3a. Is there a direct value for small fish, or for cyprinids? (yes, for muscle-driven starts)

**Wakeling, Kemp & Johnston 1999**, *J. Exp. Biol.* 202:3057, doi:10.1242/jeb.202.22.3057. **Abstract.**
- Common carp, a cyprinid like zebrafish, reared at 20 °C from 7 mm to 80 mm total length.
- The abstract defines hydrodynamic efficiency as relating "the mechanical power produced by the muscles to the inertial power requirements in the direction of travel". It reports that the efficiency "showed **no significant change during ontogeny**".
- The abstract gives no numerical value.

**Wakeling, Cole, Kemp & Johnston 2000**, *Am. J. Physiol.* 279:R657, doi:10.1152/ajpregu.2000.279.2.r657. **Abstract.**
- Carp 9.5–69 mm.
- Hydrodynamic efficiency rises "**0.19 to 0.38**" as acute temperature rises from 10 to 20 °C.
- Like the pike value, this is model-derived: muscle power is predicted from fibre strain, and hydrodynamic power from kinematics.

**What this improves** (my inference from the two abstracts). The objection that pike is "a much larger fish at higher Re" (S29 §6, and challenge 227 §3) is weakened. In a cyprinid spanning the 30 mm zebrafish size, a muscle-driven fast-start efficiency of about 0.38 at 20 °C does not change detectably with size. Zebrafish are normally kept warmer than 20 °C. The abstracts do not say whether efficiency keeps rising above 20 °C: `unknown`.

**Recomputed with every muscle-driven value found** (script §3, all else at S29's central case):

| η_h source | η_h | Shortfall at w = 32 / 53 / 81 | All muscle, w = 81 |
|---|---|---|---|
| Pike, low end (F&B 1995) | 0.16 | 7.12 / 4.30 / 2.81 | 1.41 |
| Carp, 10 °C (Wakeling 2000) | 0.19 | 6.00 / 3.62 / 2.37 | 1.18 |
| **S29 (pike)** | **0.37** | **3.08 / 1.86 / 1.22** | 0.61 |
| Carp, 20 °C (Wakeling 2000) | 0.38 | 3.00 / 1.81 / 1.18 | 0.59 |
| Pike, high end (F&B 1995) | 0.39 | 2.92 / 1.76 / 1.15 | 0.58 |

**No reported muscle-driven value reaches the 0.45 flip point.** The highest found is 0.39. Scope of that negative: Europe PMC searches for fast-start, C-start and hydromechanical efficiency, five web searches, and full-text keyword searches of Tytell & Lauder 2008 and Ravel et al. 2025 (§5).

### 3b. The real quantity: energy out of a released spring, measured (the improvement that matters)

S29's mechanism needs **KE at exit ÷ energy stored in the spring**. S29 builds this as η_s × η_h × KE/(KE + drag) = 0.93 × 0.37 / 1.065 = **0.323** (script §4).

Exactly this quantity has been measured, on an engineered analogue rather than an animal.

**Conte, Modarres-Sadeghi, Watts, Hover & Triantafyllou 2010**, "A fast-starting mechanical fish that accelerates at 40 m s⁻²", *Bioinspir. Biomim.* 5:035004, doi:10.1088/1748-3182/5/3/035004. **Read level: abstract** (Europe PMC); full text could-not-access (iopscience.iop.org is outside this session's network allowlist).

| Feature | What the authors report |
|---|---|
| Body | A thin metal beam covered in urethane rubber, pike-shaped, with a tail |
| Loading and latch | "held in curvature … by two restraining lines, which were simultaneously released by a pneumatic cutting mechanism". This is a stored-elastic-energy body released through a latch, which is S29's architecture |
| Efficiency definition | "the ratio of the final kinetic energy of the fish and the initially stored potential energy in the body beam" |
| Result | "The hydrodynamic efficiency of the fish was found to be **around 10%**." |
| Performance | Peak acceleration ~40 m s⁻²; final velocity ~1.2 m s⁻¹ |
| Wake | Acceleration peaks coincide with "the shedding of two vortex rings in **near-lateral** directions" |
| Size and mass | **Not in the abstract.** Reynolds number therefore `unknown` |

**Watts (MIT thesis, chain pickerel mechanical fish): 11 %.** Read level: **search-summary only.** The thesis title and year are unknown to me; dspace.mit.edu is outside the allowlist. I use it only as a second point beside Conte. It is not the basis of anything.

**Comparison.** S29's implied chain of 0.323 is **3.2× higher** than the measured 0.10 (script §4). Holding η_s = 0.93 and S29's drag term, the measured 0.10 corresponds to η_h ≈ 0.115.

**Why the passive device is the better analogue** (my inference; the authors do not draw it):
- The muscle-driven values in §3a describe an animal that controls its body wave throughout the stroke.
- Once the latch opens, a latch-released spring cannot do that. The body unbends along its own mode shapes.
- Conte et al. report that the wake goes near-lateral. That is energy leaving sideways, which fits a low forward efficiency.
- Tytell & Lauder 2008 (full text, §5) found that even in a live bluegill, the caudal-fin jet in stage 1 "opposes the escape trajectory". An uncontrolled release has less means of avoiding such losses.

**Why it may not transfer. These caveats are stated in full, not averaged away:**
1. **Material loss is lumped in.** Conte's 10 % includes damping in the urethane and the beam, which S29 books separately as η_s. For S29's 0.323 to be right, the robot would have had to lose 71 % of its stored energy internally (0.10 / 0.347 = 0.288 retained; calculated). I cannot rule this out: the energy accounting is in the full text, which I could not reach.
2. **Scale.** The device's length and Re are unknown. A zebrafish at exit has Re ≈ 1.3 × 10⁵ (script §7).
3. **Definition of "final".** If "final KE" is taken after coasting, the 0.10 contains post-stroke drag. S29 also pays that drag (it coasts about 1 cm to the surface), but S29 does not book it in the shortfall.
4. **Spring shape.** An engineered axial spring could in principle be shaped to unbend more like a muscle-driven wave. Nothing I found measures such a device: `unknown`.

## 4. Recomputation and verdict

**With the measured spring-release chain** (script §5, w = mean 53 J/kg and one-side f = 0.30 unless stated):

| Chain KE/E_stored | Stored (J/kg body) | Shortfall w = 32 / 53 / 81 | All muscle at 53 / 81 | At 5.53 m/s, w = 53 |
|---|---|---|---|---|
| 0.323 (S29 implied) | 29.6 | 3.08 / **1.86** / 1.22 | 0.93 / 0.61 | 2.97 |
| 0.11 (Watts, search-summary) | 86.8 | 9.04 / 5.46 / 3.57 | 2.73 / 1.79 | 8.74 |
| **0.10 (Conte, measured)** | **95.5** | 9.95 / **6.01** / 3.93 | 3.00 / **1.96** | 9.61 |

The muscle fraction needed with the Conte chain is **118 %** of body mass at w = 81, and 180 % at w = 53. That is impossible.

**Knock-on effects on S29's other "passes"** (script §6, calculated):
- **Spring volume** for 38.2 mJ stored:
  - Mammal tendon: 3.3 % of body at 100 MPa, 5.9 % at 75 MPa, 13.2 % at 50 MPa.
  - Tuna tendon at 2 % strain: **42–77 %** of body. S29's "either way it fits" fails for fish-grade tendon. This extends challenge 225's finding.
- **Multi-contraction loading** (challenge 231's escape route): 4 contractions at w = 81, **7 at w = 53** (6.01, rounded up), 10 at w = 32. Under S29's chain it was 2 at w = 53.

**Verdict: STRENGTHENS.**

| Question | Outcome |
|---|---|
| Does η_h = 0.37 hold for a muscle-driven start in a fish this size? | **Stands.** Cyprinid evidence: no size effect from 7–80 mm, about 0.38 at 20 °C (abstracts). No value reaches the 0.45 flip point |
| Is it the right input for a latch-released spring? | **No.** The only measured analogue gives a chain about 3.2× lower |
| S29's conclusion with the improved input | NEGATIVE on energy per stroke, but by **~6× (3.9–10×)**, not ~1.86×. The all-muscle break-even S29 left open is gone |
| Is the "narrow" in "NEGATIVE (narrow)" still justified? | **No**, on the measured analogue. The gap is no longer much smaller than the wing routes' ≥10×. S29's "2× vs ≥10×" contrast, which is what made it "the project's deepest result", is weakened. At 5.53 m/s the spring route is short by 9.6×, comparable to the wing routes |

What strengthens is the **negative**. What weakens is S29's framing that the spring route came *close*.

## 5. What measurement would settle it, and what it would cost

**The decisive quantity is KE_exit / E_stored for a ~30 mm, ~0.4 g latch-released elastic fish body in water.** The thresholds from the script:
- ≥ 0.39 closes the energy term for one-side muscle at w = 81 J/kg;
- ≥ 0.60 closes it at w = 53 J/kg;
- S29 assumed 0.323; Conte measured 0.10 at an unknown, probably larger size.

**Proposed bench test** (my design; the cost figures are estimates, not quotes):
1. Make spring-steel or PET shim beams with a cast silicone body, zebrafish outline, 30 mm long, 0.4 g.
2. Measure stored energy E_stored by force–deflection on a load cell, integrated to the latched curvature.
3. Release with a line-cut or thermal (nichrome) latch, as Conte did, in still water.
4. Film at ≥ 5,000 fps from above to get the centre-of-mass KE time series.
5. **Controls (rule 8):**
   - *Material-loss control:* release the same beam in air, or run a cyclic tensile test, to separate material loss from hydrodynamic loss. This answers caveat 1 directly.
   - *Positive control:* a rigid projectile fired from a calibrated spring, whose KE/E_stored in air must come back close to the spring's measured return.
   - *Must-fail control:* the beam released from a straight, unloaded state, which must give KE ≈ 0.
6. **Estimated cost:** materials under about US$500, plus access to a high-speed camera, often borrowable from a biomechanics lab. A few days to two weeks of work. The output would be *measured*.

**A cheaper but weaker alternative:** CFD of a passive beam release at Re 10⁴–10⁵. The output would be *simulated* and must be labelled so.

A third measurement, in situ spring-loading work for zebrafish myotomal muscle (S29's test 1), remains necessary. It does not substitute for the test above: the two enter as a product.

## 6. Sources

| # | Source | Read level | Used for |
|---|---|---|---|
| 1 | S29-organism.md and S29_launch_energy.py (branch `claude/s29-launch-energy-2iuixr`, commit 44ed2195) | full-text | all baseline inputs |
| 2 | challenge-225, -227, -229 and -231 (branches `claude/challenge-*`) | full-text | prior challenges; flip thresholds; multi-contraction route |
| 3 | Frith & Blake 1995, *J. Exp. Biol.* 198:1863, doi:10.1242/jeb.198.9.1863 | abstract | η_h model-derived; range 0.16–0.39; useful-power definition |
| 4 | Frith 1990, UBC thesis, "Energetics of fast-starts in northern pike" | search-summary (site could-not-access) | S29's 0.37 provenance; disagreement over range |
| 5 | Wakeling, Kemp & Johnston 1999, *J. Exp. Biol.* 202:3057 | abstract | no size effect on η_h in carp, 7–80 mm |
| 6 | Wakeling, Cole, Kemp & Johnston 2000, *Am. J. Physiol.* 279:R657 | abstract | carp η_h 0.19–0.38 (10–20 °C) |
| 7 | Conte et al. 2010, *Bioinspir. Biomim.* 5:035004 | abstract (full text could-not-access) | **measured KE/E_stored ≈ 0.10** for a latch-released elastic fish |
| 8 | Watts, MIT thesis (chain pickerel mechanical fish) | search-summary (could-not-access; title unknown) | second point, 11 %; not load-bearing |
| 9 | Tytell & Lauder 2008, *J. Exp. Biol.* 211:3359, PMC2669901 | full-text (PMC HTML, keyword-searched, not read end to end) | stage-1 caudal jet opposes escape; reports momentum, not efficiency |
| 10 | Borazjani et al. 2012, *J. Exp. Biol.* 215:671; Borazjani 2013, 216:1658 | abstract | bluegill C-start CFD; no efficiency in abstracts |
| 11 | Ravel et al. 2025, *iScience* 28:112056, PMC11930232 | full-text (keyword-searched) | larval zebrafish escape CFD; notes that useful work is hard to isolate for escapes; no η_h value found by my search |
| 12 | Currier, Lheron & Modarres-Sadeghi 2020, *Bioinspir. Biomim.* 15:055006 | abstract | snap-through spine robot, >20 g; **no efficiency in abstract** |
| 13 | Thandiackal et al. 2021, *Proc. R. Soc. B* 288:20202726 | abstract (full text could-not-access) | tuna robot accelerations; no efficiency in abstract |
| 14 | Gazzola, van Rees & Koumoutsakos 2012, *J. Fluid Mech.* | search-summary | C-start kinematics optimise distance, not energy; context only |

**Scope of negative searches.**
- About ten Europe PMC queries (fast-start / C-start × efficiency / energetics / robot / spring / bistable / zebrafish).
- Five standard web searches.
- Full-text keyword searches of #9 and #11.
- Blocked hosts: open.library.ubc.ca, arch.neicon.ru, iopscience.iop.org, dspace.mit.edu, api.openalex.org, absimage.aps.org. PMC returned a captcha for #13.

**Not found:** any measured KE/E_stored for a fish-scale (< 5 cm) spring release, and any measured (as opposed to model-derived) η_h for an adult zebrafish C-start. Both are `unknown`.

**Not used:** a 2012 *J. Exp. Biol.* 215:4015 larval-fish CFD study (authors not confirmed, search-summary only), whose propulsive efficiency of 0.22–0.32 is for cyclic swimming, not a single impulse.

## 7. Honesty ledger

- **Measured by others:**
  - Conte 2010: ~0.10 (abstract).
  - Watts: 0.11 (search-summary).
  - Kinematics underlying #3, #5 and #6.
- **Calculated by others (model output, not measurement):**
  - Pike η_h 0.16–0.39.
  - Carp η_h 0.19–0.38.
- **Calculated here:** every shortfall, threshold, volume and contraction count.
- **Assumed here:** that a pike-shaped, latch-released robot of unknown size is a better analogue for a latch-released zebrafish spring than a muscle-driven pike C-start. This is the load-bearing judgement of S29-D. If caveat 1 (material loss) explains most of the gap, the verdict reverts to **stands**.

```swarm-result
{"subproblem": "S29-D", "evidence": "derived (recalculation on S29 inputs) using literature values at abstract read-level: Frith & Blake 1995 eta_h 0.16-0.39 is a Weihs-model output for muscle-driven pike starts, not a measurement; carp (cyprinid, 7-80 mm) model eta_h 0.19-0.38 with no size effect; the only measured spring-release value is Conte et al. 2010 KE_final/E_stored ~0.10 (abstract; full text could-not-access), with an 11% second point at search-summary level", "answer": "S29's binding input eta_h=0.37 is a model-derived efficiency of a muscle-driven pike C-start (no muscle-driven value found reaches the 0.45 flip point, and carp data indicate no size effect, so for muscle drive the verdict stands), but the only measured value for S29's actual mechanism - a latch-released elastic fish body - is KE/E_stored ~0.10 versus S29's implied 0.323, which raises the energy shortfall from 1.86x to ~6.0x (3.9-10x), removes the all-muscle break-even (1.96x short at 81 J/kg), and makes fish-grade tendon springs 42-77% of body volume, so the negative strengthens and is no longer 'narrow'.", "key_number": "spring-release chain efficiency KE_exit/E_stored ~0.10 (Conte et al. 2010, measured, abstract) vs 0.323 implied by S29 (0.93 x 0.37 / 1.065); equivalent eta_h ~0.115", "verdict": "strengthens", "depends_on": ["S29 (S29-organism.md, commit 44ed2195): shortfall formula and central inputs", "S28 V_exit 4.37 m/s target (and S29's mass-consistent 5.53 m/s)", "S28 frontal area 24 mm^2", "body mass 0.40 g (S29 brief)", "body density 1050 kg/m^3 (assumed, S29)", "Cd 0.2 and stroke 1.09 cm (assumed, S29)", "Mendoza-Azizi2021 frog spring-loading work 32/53/81 J/kg muscle (via S29, full-text per challenge 227)", "F_ONE_SIDE 0.30 (assumed, S29)", "F_ALL 0.60 zebrafish skeletal muscle fraction (secondary, S29)", "Ker1981 tendon return 0.93 and E 1.65 GPa (via S29, abstract)", "tendon working stress 50-100 MPa (S29) / 75 MPa (challenge 225, search-summary)", "Shadwick tuna tendon E 0.65-1.2 GPa at 2% burst strain (via S29, abstract)", "Frith-Blake1995 eta_h 0.16-0.39, Weihs-model-derived (abstract)", "Frith1990 UBC thesis eta_h 0.37, C-start 0.34-0.39 (S29's source; could-not-access here)", "Wakeling-Kemp-Johnston1999 no ontogenetic change in carp fast-start eta_h 7-80 mm (abstract)", "Wakeling2000 carp eta_h 0.19-0.38 at 10-20 C (abstract)", "Conte2010 latch-released mechanical fish KE_final/E_stored ~0.10 (abstract)", "Watts MIT thesis chain pickerel mechanical fish 11% (search-summary)", "ASSUMPTION: passive latch-released robot is a better analogue for a zebrafish axial spring than a muscle-driven C-start, and Conte's 10% is not dominated by urethane/beam material loss", "challenge-227 break-even eta_h 0.45 (w81) / 0.69 (w53)", "challenge-231 multi-contraction loading route", "challenge-225 spring-volume critique"]}
```
