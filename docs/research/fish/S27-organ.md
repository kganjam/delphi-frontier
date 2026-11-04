# S27 (organ): Is the fin-ray stiffness screen a one-axis screen hiding a trade-off?

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.
Status: answered, evidence level **derived**. It rests on literature read mostly at abstract level, plus arithmetic in
[`S27_calc.py`](S27_calc.py). Run `python3 docs/research/fish/S27_calc.py` to reproduce every number in §3.

**Short answer.**
- **EI alone is the wrong *representation* of a fin ray.** The evidence for a second property is good, at abstract
  level. The property that matters for S6 is not a *competing* one. It is the factor by which the ray's passive
  stiffness can be raised when engaged, by locking the hemitrich bases or by curving the fin.
- **I found one genuine trade-off.** At a fixed amount of bone, passive flat-ray EI and the stiffness ceiling that
  curvature can reach move in opposite directions. This follows from Nguyen et al.'s formulas; the algebra is mine.
  The stiffness-versus-gust-load link in Flammang et al. is a simulation result, and the stiffness-versus-
  manoeuvrability link in labrids is the authors' framing from background literature, not something they measured.
- **The trade-off cannot reverse S6 the way it reversed the HEA ranking.** S6 is a feasibility screen against a
  floor, not a ranking. A trade-off on any axis other than the engagement multiplier can only add constraints.
- **On the two-axis map (passive EI × engagement multiplier), no measured ray reaches the requirement.** The S6
  verdict **STANDS**.

---

## 0. What S27 inherits, and a provenance correction

The brief quotes three things as "S6": required EI ≈ 6.3e-4 N m², reported ray stiffness ≤ 3.8e-6 N m², and labrid
rays at 1e-10 to 1.51e-6 N m². Those numbers are **not** from `S6-organ.md`
(branch `claude/s6-fin-ray-load-kqweu7`). That document analysed a 0.4 g zebrafish caudal-fin wing and found a
9–196× shortfall in rigidity per unit width.

The quoted numbers come from **S6-D**, `docs/research/fish/S6-deepen.md` on branch `claude/deepen-fin-ray-s6-cj2i2x`.
That is a 100 g flying-fish scenario: m = 0.10 kg, N = 14 rays per fin, L = 0.12 m, n = 1, failure at δ/L > 0.10.
Every one of those values is an assumption. Its swarm-result verdict is `falls`. I read S6, S6-D, both S6-D-D
versions, S25, S26 and challenge-74 in full from their branches.

The S6-D verdict is already contested:

- **S6-D-D, version 1** (branch `claude/deepen-s6-d-sensitive-input-t6ch0y`) concluded "stands". The shortfall
  is about 4.3× (range 0.8–8×) once ray size is normalised.
- **S6-D-D, version 2** (branch `claude/deepen-s6-d-sensitive-input-fc1hm8`) concluded "falls" to **unresolved**.
  Its reason: under isometric scaling, Alben's clamped-base bound passes.
- **Challenge-74** weakened the labrid comparison on size grounds.

**S27 does not re-litigate size scaling.** It asks a different question: whether a *second axis* changes the
picture. Where the size question matters, I show the outcome under both S6-D's absolute comparison and S6-D-D's
normalised one.

## 1. The question, restated

Wang & Buehler's HEA case is **their** claim, taken from the brief; I did not read arXiv:2606.01444. In it, a
one-axis threshold ranking hid a trade-off. The alloys with a higher ΔK_th also had steeper Paris slopes, and a
two-axis damage-tolerance map reversed the ranking.

For fin rays the question has three parts:

- Does the EI screen collapse designs that a second property would separate?
- Do stiffer rays pay for that stiffness somewhere else?
- If so, does that change S6-D's FALLS?

## 2. What is measured, modelled or claimed

Read-levels: **full-text** means I read the text myself. **abstract** means read through the Europe PMC REST API.
**relay** means the value was read at full text by an earlier subproblem in this repository and I am citing that
subproblem.

| # | Property (axis candidate) | What the source says | Kind | Source | Read-level |
|---|---|---|---|---|---|
| E1 | Fin stiffness ≠ ray EI | "Measurement of fin stiffness has therefore been considered synonymous with the measurement of bending rigidity of the rays themselves [35], and no other parameters are considered." Fin stiffness ranges between R0 = 3Bn/L³ (weak membrane) and R∞ = R0(1+γ), where γ = Bt/Bn ~ W²/T². For mackerel the authors estimate "a factor of 1 + W²/T² ranging from 300–700% relative to the normal stiffness of its rays." | model + µCT geometry (authors' derivation) | Nguyen, Yu, Bandi, Venkadesan & Mandre, "Curvature-induced stiffening of a fish fin", *J R Soc Interface* 2017; arXiv:1608.05891v3 | **full-text** (arXiv PDF, text extracted) |
| E2 | Torsional stiffness | The authors say "the anisotropic bending moduli and the torsional stiffness of the rays are important to experimentally quantify". They describe ray torsion as an effect that current models omit. | authors' statement that it is unmeasured | Nguyen et al. 2017 | full-text |
| E3 | Post-threshold / large-deflection stability | Hemitrich "flexural stiffness … is 5-6 times lower than their axial stiffness". The collagenous core is "3-4 orders of magnitude more compliant than the hemitrichs" and "provides negligible resistance to shearing from the initial position, but it prevents buckling and collapse of the structure at large deformations". Rainbow trout rays. | measured (micromechanical tests) + fitted nonlinear model | Das, Hannard & Barthelat, *Acta Biomater* 167:171–181 (2023), doi:10.1016/j.actbio.2023.06.029 | **abstract** (colorado.edu PDF: host not resolvable from this session) |
| E4 | Graceful vs catastrophic failure | Under a vortex jet of about 1 m s⁻¹ (67 ± 2.3 mN at impact) the bluegill ray reached a maximum curvature of 9.38 mm⁻¹. "Buckling of the fin ray was constrained to the area of impact and did not disrupt the motion of the pectoral fin during swimming." | observed (in vivo) | Flammang, Alben, Madden & Lauder, *J Morphol* 274:1044 (2013), doi:10.1002/jmor.20161 | **abstract** |
| E5 | **Stiffness vs perturbation load (trade-off)** | "very flexible fin rays … Due to their small bending rigidity … impacting vortices transferred little force to the fin ray. Conversely, stiffer fin rays experienced rapid small-amplitude oscillations from vortex impacts, with large impact forces all along the length of the fin ray." Also: "This flexibility may offer intrinsic damping of environmental fluid perturbations". | **CFD simulation**; the damping sentence is a hypothesis ("may") | Flammang et al. 2013 | **abstract** |
| E6 | Active modulation range | "a variation in ray stiffness over more than an order of magnitude depending on actuation at the bases of the fin rays". The clamped/one-base-free ratio is about 12× on one bluegill ray (n = 1); the linear model's asymptote is about 100× for G > 1e5. | measured (n = 1) + model | Alben, Madden & Lauder, *J R Soc Interface* 4:243 (2007), doi:10.1098/rsif.2006.0181 | abstract (this session); 12× and 100× via **relay** from S26 |
| E7 | Stiffness vs morphing amplitude | Segmentation provides "combinations of high flexural stiffness and high morphing amplitude … that … would not be possible with rays made of a continuous material". | model + tests on 3D-printed rays (not biological rays) | Hannard, Mirkhalaf, Ameri & Barthelat, *Sci Robot* 6:eabf9710 (2021) | **abstract** |
| E8 | Thrust and lift vs stiffness | Robotic rays at 150–2000× biological stiffness. "More compliant fin rays produced lower peak magnitude forces"; "thrust was maximized by the 500× stiffness fin rays and lift was maximized by the 1000× stiffness fin rays." | robot experiment | Esposito, Tangorra, Flammang & Lauder, *J Exp Biol* 215:56 (2012), doi:10.1242/jeb.062711 | **abstract** |
| E9 | Stiffness vs behaviour (labrids) | Ray EI 0.0001–1.5109 µN m². Flapper (*G. varius*) proximal rays are "nearly an order of magnitude stiffer" than the rower's (*H. bivittatus*). Background statement: "Rowers are more maneuverable than flappers, but flappers generate greater thrust at high speeds and achieve greater mechanical efficiency at all speeds." | EI measured (three-point bending); the manoeuvrability claim is the authors' background framing, **not measured in this paper** | Aiello, Hardy, Cherian, Olsen, Ahn, Hale & Westneat, *J Exp Biol* 221:jeb163360 (2018) | **abstract** |
| E10 | Stiffness vs sensory sensitivity | At 50 % ray length, EI is 190 ± 30 to 210 ± 50 × 10⁻⁹ N m² in high-aspect-ratio (AR) species and 20 ± 10 to 40 ± 10 × 10⁻⁹ N m² in low-AR species. Afferent response threshold is 5.91–8.20 % of ray length in high-AR species and 17.84–30.67 % in low-AR species. The authors found "no significant correlation between response threshold and fin ray flexural stiffness" (P = 0.2447). Specimens were 7.3–13.2 cm SL. | measured | Aiello, Westneat & Hale, *PNAS* 114:4459 (2017), PMC5410822 | full-text, **through an automated page summariser** (numbers quoted by it, not read line by line) |
| E11 | Membrane contribution, zebrafish | Cutting the interray tissue made no significant difference to whole-fin EI (1.5–4 × 10⁻⁹ N m²). The authors conclude that the rays set the stiffness. | measured | Puri et al., *J Exp Biol* 221:jeb171777 (2018) | **relay** (S6 read it at full text) |
| E12 | Damping / viscoelasticity | Stress relaxation in crucian carp caudal fin rays fits a fractional Zener model. The same group concludes internal viscoelastic dissipation during cruising is small. | measured relaxation + model | Chen, Jia & Yin, *Chin J Theor Appl Mech* 2011 (doi:10.6052/0459-1879-2011-1-lxxb2010-145); *Chin Phys Lett* 28:088703 (2011) | **search-summary** only |

**Searched for and not found.** Searches covered web search plus Europe PMC; publisher and lab hosts
(colorado.edu, dash.harvard.edu, sites.harvard.edu, silverchair) were unreachable from this session. Measured
values I could not find:

- torsional stiffness (GJ) of any fin ray, in any species. Nguyen et al. 2017 say explicitly that it still needs
  measuring;
- fin-ray strength, fracture toughness, strain to failure, or fatigue life. One web search returned stiffness
  papers only;
- a measured damping ratio or loss tangent for a fin ray under dynamic loading;
- any of the above for Exocoetidae, the S6-D target taxon.

I report these as **absent within that scope**, not as absent from the literature.

**A correction to a search summary.** One web-search summary described Nguyen et al.'s γ as a
"bending-to-torsion ratio". It is not. In the paper (eq. 18) γ = Bt/Bn is the ratio of **tangential to normal
bending** rigidity. Torsion appears only as an unmodelled complication (E2).

## 3. What I computed (computation, not observation)

**C1. The one-axis screen, recomputed** (§1 of the script). Shortfall EI_req/EI against 6.3e-4 N m²:

| Ray | Shortfall |
|---|---|
| S6-D passive 3.8e-6 | 166× |
| labrid proximal maximum 1.51e-6 | 417× |
| labrid high-AR mid-ray 2.1e-7 (Aiello 2017) | 3,000× |
| bluegill passive 1.9e-6 (S6-D-D's back-calculation) | 332× |
| bluegill clamped-base bound 4.3e-5 (S6-D-D) | 15× |
| Flammang 565e-6 | 1.1× |

**C2. The second axis that can actually move a floor verdict** (§2 of the script).

Define the engagement multiplier M = EI_engaged / EI_0, where EI_0 is the passive, flat, unlocked value. The
design is feasible when EI_0 · M ≥ EI_req.

Starting from EI_0 = 3.8e-6:

- Measured base locking (M = 12) leaves the ray **13.8× short**.
- Locking × curvature, assuming the two mechanisms **compound multiplicatively** (unverified), gives 12 × 7 = 84.
  That leaves it **2.0× short** (4.0× short at EI_0 = 1.9e-6; 5.0× short at the labrid maximum).
- Only Alben's *model* ceiling (100) × Nguyen's curvature factor (7) = 700 clears the floor, by 0.24–0.60×. That
  ceiling requires G > 1e5, which effectively means fused hemitrichs (S26 C3).

Under S6-D-D's size-normalised shortfall of 4.3× (0.8–8×), measured locking alone (12×) closes the gap
(0.07–0.67×). That result inherits S6-D-D's untested assumption of isometric transfer.

**C3. The one genuine trade-off I can derive** (§3 of the script; my algebra on Nguyen et al.'s eq. 7 and eq. 18).

Hold the ray's cross-section area A = W·T fixed, which fixes bone mass per unit length. Then:

- Bn = E·A²/(12√γ), and
- Bt = E·A²·√γ/12.

Making the ray flatter (larger γ) therefore **lowers** the passive flat-fin stiffness as γ^-1/2. At γ = 10, passive
Bn is 0.32× its round-section value. The same change **raises** the curvature-engaged ceiling R∞ ∝ Bn(1+γ) to
3.5×, and to 10× at γ = 100.

So at fixed mass, *passive EI and engageable stiffness are anti-correlated*. A screen on passive EI would rank the
flatter ray worse, while on engaged stiffness it is better. That is exactly the HEA shape. Caveats:

- R∞ is reached only if the membrane is stiff enough, by Nguyen's criterion L/l ≳ γ^1/3.
- For the zebrafish caudal fin, cutting the membrane changed nothing measurable (E11). My inference is that this
  fin sits in the weak-membrane R0 regime at those loads, where the trade-off is not exercised.

**C4. Stiffness versus mass does not bind the floor** (§4 of the script). A solid rod meeting EI_req at
E = 1 GPa (assumed, S6-D's basis) is 1.89 mm across. EI ∝ d⁴ while mass ∝ d², so doubling d buys 16× EI for 4×
mass. Mass is a cost, but not one that reverses the screen.

**C5. Bilaminar coupling cap** (§5 of the script; S26 C4 re-run). Full hemitrich coupling gives R = 1 + 3(d/t)².
R = 166 needs d/t = 7.4, and R = 12 needs 1.9. No d/t is measured for Exocoetidae.

## 4. The answers

**Q1. What does EI alone miss?** In order of how much it matters for S6-D:

1. **The engageable range.** A ray is an interval [EI_0, EI_0·M], not a point. M comes from base locking (E6,
   12× measured on n = 1) and from fin curvature through membrane coupling (E1, 3–7× derived for mackerel). Two
   rays with equal passive EI can have different M. EI alone collapses them. Of all the candidates, this is the
   only one that can raise the stiffness S6-D compares against its floor.
2. **Post-threshold stability.** This is the closest analogue of the Paris slope. Das et al. (E3) report that the
   core, which contributes almost nothing to small-deflection EI, is what prevents collapse at large deflection.
   Flammang et al. (E4) observed buckling that stayed local and did not disrupt the fin beat. So the component that
   decides graceful versus catastrophic failure is *invisible* to an EI screen. That is their claim at abstract
   level. Calling it "the second axis" is my framing.
3. **Anisotropy** (E1, E3). Bt ≠ Bn, and axial stiffness is 5–6× flexural stiffness in hemitrichs. EI is one
   component of a stiffness tensor.
4. **Torsion and damping.** These are real candidates for flutter, but **no measured value exists** within my
   search (E2, E12). I cannot place any ray on either axis.

**Q2. Is there a real trade-off?**

- **Yes, but not a measured anti-correlation across real rays.** The trade-offs I can support are:
  - **(a)** passive EI versus curvature-engaged ceiling at fixed bone mass. This is derived (C3), from Nguyen's
    model formulas.
  - **(b)** stiffness versus perturbation load transmission. This is a CFD result (E5): stiffer rays take larger
    vortex impact forces. Its damping corollary is a hypothesis.
  - **(c)** stiffness versus manoeuvrability in labrids. The authors frame it this way (E9), but manoeuvrability
    was not measured with stiffness.
- **Two candidate trade-offs turned out not to be trade-offs.**
  - Thrust is non-monotonic in stiffness (E8), so it has an optimum rather than an anti-correlation.
  - Stiffness and afferent sensitivity *co-vary* in labrids rather than trade (E10). Stiffer species have lower
    thresholds, but within species there is no correlation.
  - Hannard et al. (E7) show that the stiffness-versus-morphing trade-off of continuous materials is *escaped* by
    segmentation, so it is not forced on a segmented ray.
- **My inference.** The trade-offs in E5, E7 and E9 offer a reason why measured rays sit 2–6 orders of magnitude
  below a gliding requirement. Their stiffness appears tuned toward perturbation compliance and morphing for
  aquatic use, so the low EI is plausibly a design choice, not an accident of material. The cited authors do not
  make this argument about gliding.

**Q3. The two-axis map.**

- **x-axis:** passive flexural rigidity EI_0 (N m²), meaning flat, unactuated, small deflection, at the ray's own
  length (state L).
- **y-axis:** engagement multiplier M = EI_max/EI_0 (dimensionless), from base locking × curvature coupling.
- **Feasible region:** above the line M = EI_req/EI_0, a line of slope −1 on log-log axes through
  (6.3e-4 N m², 1). On a size-normalised map (S6-D-D's convention), replace EI with EI/L⁴ (Pa); the requirement
  becomes 3.0 Pa.

Where real rays sit (EI_0 is measured or derived; M is measured only for bluegill):

| Ray | EI_0 (N m²) | M | EI_0·M (N m²) | Position |
|---|---|---|---|---|
| bluegill (Alben 2007; S6-D-D back-calculation) | ~1.9e-6 | 12 (measured, n = 1) | 2.3e-5 | **27.6× below** the line (absolute) |
| bluegill, Alben model ceiling | ~1.9e-6 | ≤100 (model) | 1.9e-4 | 3.3× below |
| mackerel (Nguyen 2017) | unknown | 3–7 (curvature, derived) | — | cannot place |
| labrids (Aiello 2018; 2017) | 1e-10 – 1.51e-6 | unknown | — | x only; 417× short at M = 1 |
| zebrafish caudal fin (Puri 2018) | 1.5–4e-9 (whole fin) | membrane term measured ≈ 0 (E11); locking unknown | — | x only |
| Flammang 2013 bluegill | 5.65e-4 ("calculated") | unknown whether passive or engaged (S25, S26 D1) | — | at the line if passive; S6-D-D argues it cannot be a passive excised value |
| **design requirement (S6-D)** | — | — | **≥ 6.3e-4** | the line |

**Where the design must sit.** Either:

- EI_0 ≥ 6.3e-4 N m² with M = 1, meaning a solid-equivalent rod of about 1.9 mm at E ≈ 1 GPa; or
- a passive ray of 3.8e-6 N m² with **M ≥ 166**. That exceeds the measured locking factor (12), and exceeds
  locking × curvature (84) even if the two compound.

A third axis is post-threshold stability (E3, E4). It is real, but no ray can be placed on it numerically, so I do
not plot it. The map records it as a named, unpopulated axis rather than an invented one.

**Q4. Does it change the S6 verdict? STANDS.**

- **Why the reframing cannot flip FALLS by itself.** HEA used ΔK_th to *rank* candidates, and a hidden trade-off
  reverses a ranking. S6-D uses EI as a *feasibility floor*. A trade-off on a competing axis (gust load,
  manoeuvrability, mass, damping) can only add constraints. It can tighten the window from above but cannot lift a
  ray over the floor. The only second axis able to flip FALLS is one that multiplies EI, and that is M.
- **What the numbers say with M on the map.** On S6-D's absolute comparison, the best *measured* point (bluegill,
  EI_0·M = 2.3e-5) is 27.6× below the line. Granting locking × curvature compounding still leaves 2–5× short.
  Only a modelled, near-fused ceiling clears it. So the barrier is a property of the problem, not of the
  one-axis representation, as long as the comparison is absolute.
- **The one route by which the map could flip the verdict** is if S6-D-D's size normalisation is accepted. Then
  measured locking closes the gap (C2). That is a dispute about size scaling between S6-D-D and its
  counter-version, not something a second axis decides.
- I say STANDS, not STRENGTHENS. The trade-off evidence that would tighten the window (E5, stiffer rays taking
  larger gust loads) is CFD at abstract level, and I could not quantify it for an air-loaded wing.

## 5. What this does NOT establish

- **It does not measure anything.** Every trade-off here is a model result (C3, E1), a simulation (E5), a
  robot (E8), 3D-printed analogues (E7), or the authors' framing (E9). I found no anti-correlation measured on
  biological rays.
- **The compounding of locking and curvature (12 × 7) is assumed.** The two mechanisms may interact
  sub-multiplicatively. Locking stiffens Bn, and Nguyen's gain scales with Bt/Bn, so locking might *reduce* γ. I
  did not model this.
- **The 3–7× curvature factor is for mackerel**, from µCT geometry, with membrane-sufficiency criteria the authors
  checked only at 20–30 % fin length. It is not measured as a fin stiffness change.
- **It does not compute flutter.** Torsional stiffness, damping and elastic-axis position remain unmeasured for any
  fin ray (§2 scope). A torsion-limited flutter boundary could add a separate failure mode that EI does not see.
  That would make the verdict harsher, not softer.
- **Strength and fatigue remain unknown.** S6-D's 3.2 MPa root stress suggests strength is not binding, but no
  fin-ray failure stress was found to confirm it.
- **Most sources are abstract-level.** Das 2023, Hannard 2021, Esposito 2012 and both Aiello 2018 papers were read
  only through Europe PMC abstracts, because the lab and publisher PDF hosts are blocked in this session.
- **It does not settle the S6-D-D size-scaling dispute,** on which the map's verdict is conditional (Q4).
- **I did not read Wang & Buehler (arXiv:2606.01444).** The HEA comparison is taken from the brief.

## 6. What would change the answer

1. **A measured M for a flying-fish or any glide-relevant ray** (locked vs free bases, flat vs curved fin) of
   **≥ 166** at EI_0 ≈ 3.8e-6, or ≥ 15 if S6-D-D's normalised shortfall is accepted, flips FALLS. This is the
   decisive experiment. It is the same bending rig as S6-D step B, run in four states.
2. **A measured biological anti-correlation**, for example across a clade where higher proximal EI comes with lower
   M or lower post-buckling stability. That would turn C3 from model algebra into a result and make the one-axis
   screen provably inadequate for *ranking* rays. It would still not rescue the floor.
3. **Measured torsional stiffness and damping** would populate the axes I left empty. A low GJ could add a flutter
   failure mode; that strengthens FALLS, it does not weaken it.
4. **Allowing colorado.edu and dash.harvard.edu in the session network policy** would lift Das 2023, Hannard 2021
   and Esposito 2012 to full text, and give the numeric large-deflection stability data needed to place rays on the
   third axis.

---

Sources (read-levels as in §2):
- Nguyen K, Yu N, Bandi MM, Venkadesan M, Mandre S (2017) [arXiv:1608.05891](https://arxiv.org/abs/1608.05891). Full text.
- Das S, Hannard F, Barthelat F (2023) Acta Biomater 167:171, doi:10.1016/j.actbio.2023.06.029. Abstract (Europe PMC).
- Flammang BE, Alben S, Madden PGA, Lauder GV (2013) J Morphol 274:1044, doi:10.1002/jmor.20161. Abstract.
- Alben S, Madden PG, Lauder GV (2007) J R Soc Interface 4:243, doi:10.1098/rsif.2006.0181. Abstract; values via S26 relay.
- Hannard F, Mirkhalaf M, Ameri A, Barthelat F (2021) Sci Robot 6:eabf9710, doi:10.1126/scirobotics.abf9710. Abstract.
- Esposito CJ, Tangorra JL, Flammang BE, Lauder GV (2012) J Exp Biol 215:56, doi:10.1242/jeb.062711. Abstract.
- Aiello BR et al. (2018) J Exp Biol 221:jeb163360, doi:10.1242/jeb.163360. Abstract.
- Aiello BR, Westneat MW, Hale ME (2017) PNAS 114:4459, [PMC5410822](https://pmc.ncbi.nlm.nih.gov/articles/PMC5410822). Full text through a summariser.
- Puri S et al. (2018) J Exp Biol 221:jeb171777, PMC5868929. Via S6 relay (full text there).
- Chen, Jia & Yin (2011), [doi:10.6052/0459-1879-2011-1-lxxb2010-145](https://dx.doi.org/10.6052/0459-1879-2011-1-lxxb2010-145); [Chin Phys Lett 28:088703](https://cpl.iphy.ac.cn/Y2011/V28/I8/88703). Search summary.
- Repository inputs: S6-organ.md, S6-deepen.md (S6-D), S6-D-deepen.md (both versions), S25-organ.md, S26-organ.md, challenge-74.md, each read on its own branch.

```swarm-result
{"subproblem": "S27",
 "evidence": "derived: literature mostly at abstract level (Das 2023, Flammang 2013, Hannard 2021, Esposito 2012, Aiello 2018 via Europe PMC), Nguyen 2017 at full text, Aiello 2017 at full text via summariser, Alben 2007 and Puri 2018 via repository relays; trade-off arithmetic is mine (S27_calc.py); no biological anti-correlation measured; no torsion, damping, strength or fatigue value found for any fin ray",
 "answer": "EI alone is the wrong representation of a fin ray. A ray is an interval [EI_0, M*EI_0], where M comes from hemitrich base locking (12x measured, n=1) and from fin curvature through membrane coupling (3-7x derived, mackerel). Large-deflection stability is set by a collagen core that is invisible to EI (Das 2023, abstract). One genuine trade-off follows from Nguyen 2017's formulas (my algebra): at fixed bone area, passive Bn falls as gamma^-1/2 while the curvature-engaged ceiling rises as Bn*(1+gamma). Stiffness-vs-gust-load (Flammang 2013 CFD) and stiffness-vs-manoeuvrability (Aiello 2018, authors' framing) are not measured anti-correlations. Because S6-D is a feasibility floor, not a ranking, only the multiplier axis M can flip it. On the proposed map (x = passive EI_0 in N m^2, y = M dimensionless, feasible where EI_0*M >= 6.3e-4 N m^2), the best measured point (bluegill, 1.9e-6 x 12 = 2.3e-5) is 27.6x below the line. Locking x curvature (84x, compounding assumed) is still 2-5x short. Only the modelled near-fused ceiling (700x) clears it.",
 "key_number": "M >= 166 needed at EI_0 = 3.8e-6 N m^2 vs 12 measured (base locking, n=1) and <= 84 if locking and curvature (3-7x) compound; best measured EI_0*M = 2.3e-5 N m^2, 27.6x below 6.3e-4",
 "verdict": "stands",
 "depends_on": [
   "S6-D (docs/research/fish/S6-deepen.md, branch claude/deepen-fin-ray-s6-cj2i2x): EI_req = 6.3e-4 N m^2 from assumptions m=0.10 kg, N=14, L=0.12 m, n=1, delta/L<=0.10; verdict falls",
   "S6-D-D both versions: passive bluegill EI ~1.9e-6 back-calculated from Alben 2007 k=1.98 N/m / 12; size-normalised shortfall 4.3x (0.8-8x) vs unresolved under isometric scaling (dispute not settled here)",
   "S26: Alben 2007 clamped/free ratio ~12x (n=1) and model asymptote ~100x at G>1e5; bilaminar cap R = 1+3(d/t)^2",
   "S25: 3.8e-6 N m^2 untraced to Flammang 2013; 565e-6 is the abstract value",
   "Nguyen et al. 2017 arXiv:1608.05891 full text: R_inf = R0(1+gamma), gamma = Bt/Bn ~ W^2/T^2, mackerel 300-700%; torsional stiffness unmeasured",
   "Das, Hannard & Barthelat 2023 Acta Biomater abstract: core negligible in shear at small deflection, prevents buckling and collapse at large",
   "Flammang et al. 2013 J Morphol abstract: local buckling did not disrupt fin motion; CFD shows stiffer rays take larger vortex impact forces",
   "Hannard et al. 2021 Sci Robot abstract: segmentation escapes the stiffness-vs-morphing trade-off (3D-printed models)",
   "Esposito et al. 2012 J Exp Biol abstract: thrust max at 500x, lift max at 1000x biological stiffness (robot)",
   "Aiello et al. 2018 J Exp Biol abstract: labrid EI 1e-10 to 1.51e-6 N m^2; rower-manoeuvrability vs flapper-thrust is authors' framing",
   "Aiello, Westneat & Hale 2017 PNAS (summariser): stiffness and afferent sensitivity co-vary by group, no within-species correlation",
   "Puri et al. 2018 via S6 relay: cutting zebrafish interray tissue did not change fin EI",
   "assumption: locking and curvature multipliers compound multiplicatively (unverified)",
   "assumption: E = 1 GPa solid-rod equivalence (S6-D basis)"
 ]}
```
