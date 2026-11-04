# S26 (organ): Can active stiffening carry the load a passive ray cannot?

Project: `zebrafish-flight`. Scale: organ (the pectoral fin as a load-bearing lifting surface).
Status: answered on the evidence available. The answer is **no** for the measured active mechanism, and **not shown** for the modelled maximum. Evidence level: **derived** (published measurements and models, plus arithmetic done here).

---

## 0. Inputs carried in from upstream, and a provenance warning

The brief gives two numbers from S6:

- required flexural rigidity of the load-bearing ray: **EI_req = 6.3e-4 N m^2**
- the passive gap: **165x**

**I could not find S6 in this repository.** I ran `git grep` for "zebrafish", "fin ray", "hemitrich", "6.3e-4" and "165" across every tracked file on this branch, and checked `git log --all` for fish- or S6-related commits. Nothing came back except two unrelated `findings/gemini-*` JSON files. So:

- I take 6.3e-4 N m^2 and 165x **as given in the brief**. I have not re-derived them.
- From them I infer (this is my inference, not an S6 statement) that the passive zebrafish ray S6 used has
  EI_passive = 6.3e-4 / 165 = **3.8e-6 N m^2**.
- **Unknown, and it matters a lot:** whether EI_req is (a) per ray, or (b) for the whole fin, with the load shared across rays. It is also unknown whether S6's passive value came from an intact excised ray, in which the hemitrich bases are partly constrained by tissue, or from a ray whose bases slide freely. Both questions change the answer. See sections 3 and 5.

## 1. The question, restated precisely

A teleost fin ray (lepidotrichium) is bilaminar. Two hemitrichs are bound by collagen and elastic fibres, and muscles insert on each hemitrich base. If a base is pulled or held, the hemitrichs are pushed to slide relative to each other. The ray then curves (shape control) and resists bending through interlaminar shear (stiffness control).

The question is whether this active mechanism can multiply the passive ray's rigidity by **at least 165x**, from 3.8e-6 to 6.3e-4 N m^2, in a zebrafish-sized ray. It covers base locking, hemitrich offset (actuation), and any coupling between rays through the fin membrane.

Why it is hard: 165x is more than two orders of magnitude, and there is only one published locked-vs-sliding measurement of the bilaminar factor, on one ray of one species (section 2). A beam's EI also scales roughly as L^4 under isometry, so shrinking from a bluegill-sized ray to a zebrafish-sized one costs rigidity much faster than it saves load.

## 2. What is measured (and what is modelled), with sources

| # | Quantity | Value | Kind | Source | Read-level |
|---|---|---|---|---|---|
| M1 | Point-load stiffness of one bluegill (*Lepomis macrochirus*) pectoral ray (ray 4 of 13), both hemitrich bases clamped | 1.98 N m^-1 | **measured** | Alben, Madden & Lauder, *J R Soc Interface* 4(13):243-256, online 2006, issue 2007, doi:10.1098/rsif.2006.0181 | full-text (PMC2359861, read through an automated page summarizer, not line by line) |
| M2 | Ratio of clamped-base stiffness to one-base-free stiffness, same ray | **~12x** | **measured** (n = 1 ray) | same | full-text (as above) |
| M3 | Composite Young's modulus (three-point bending) | 1e8 - 1e9 Pa | measured | same | full-text (as above) |
| M4 | Bluegill ray bending rigidity B = EI | **1e-6 - 1e-5 N m^2** | measured or estimated (the paper's order-of-magnitude value) | same | full-text (as above) |
| M5 | Bluegill maximum pectoral ray length | 40.3 +/- 0.8 mm (6 fish) | measured | same | full-text (as above) |
| S1 | Modelled clamped/free stiffness ratio as a function of the nondimensional interlaminar-shear parameter G | ~3-4 at G ~ 3; ~12 at G ~ 1e2 (matches M2); **asymptote ~100 for G > 1e5** | **model** (linear, planar, small-deflection) | same | full-text (as above) |
| S2 | Authors' summary claim | the fish can "actively vary fin-ray stiffness over more than an order of magnitude" | author claim | same | full-text (as above) |
| M6 | Preventing relative hemitrich displacement raised ray stiffness | "nearly 12 times" | measured | Lauder, Madden & McHenry, SICB meeting abstract (sunfish) | search-summary (sicb.org could not be reached from this session) |
| M7 | Force at the distal third of middle rays for a 100 µm hemitrich displacement | 10-15 mN | measured | same abstract | search-summary |
| M8 | Proximal vs distal ray stiffness | proximal up to **30x** stiffer than distal; stiffness varies ~2 orders of magnitude across the fin | measured | Lauder group, sunfish (Lauder et al. 2011 *Smart Mater. Struct.* and/or SICB abstract; the search summary did not say which) | search-summary |
| M9 | Mean proximal modulus, bluegill rays | 1.34 GPa (range 0.24-3.7 GPa) | measured | Lauder group companion study (source attribution from search summary) | search-summary |
| M10 | Bluegill pectoral ray flexural stiffness, **calculated from an in-vivo vortex-jet perturbation** (~1 m/s jet) | **565e-6 N m^2** | calculated from in-vivo kinematics (not a bending test) | Flammang, Alben, Madden & Lauder, *J Morphol* 2013, "Functional morphology of the fin rays of teleost fishes" | search-summary (sites.harvard.edu PDF could not be reached) |
| M11 | Maximum ray curvature under that perturbation | reported as 9.38 mm^-1 | measured | same | search-summary. This value is suspicious: it is a radius of about 0.1 mm. It may be a summarizer unit error. I have not verified it. |
| M12 | Labrid (wrasse) pectoral ray EI, two species | 0.0001 - 1.51 µN m^2 = **1e-10 - 1.5e-6 N m^2**; the flapping species' proximal rays are ~10x stiffer | measured | Aiello et al., *J Exp Biol* 221: jeb163360 (2018) | search-summary |
| S3 | Simulated sunfish ray with antagonistic actuation, modelled as a root offset between hemitrichs | effective stiffness and curvature are **modulated together**, not independently | **simulated** | *J Fluid Mech* 2023 (Lauder/Alben-lineage fin-ray FSI model; full author list not confirmed) | search-summary |
| S4 | Dynamic hemitrich offsets in FSI simulations | no quantitative stiffness result | simulated | Bodaghi & Xue, APS DFD 2021 abstract Q13.4 | search-summary |

### Disagreements, preserved

- **D1, bluegill ray EI: M4 vs M10.** Alben et al. (M4) give about 1e-6 to 1e-5 N m^2. Flammang et al. (M10) calculate 5.65e-4 N m^2 for the same species and fin. That is a 56x to 565x difference. The two numbers come from different methods: an excised-ray bending test with an order-of-magnitude estimate, versus inversion of in-vivo deformation under a jet. My inference, not the authors' claim: the gap could reflect active stiffening in the living fish, a different ray region (proximal vs distal, M8), or a different definition of "stiffness" in the inversion. I could not read the Flammang full text to tell which. **I do not average these.**
- **D2, independence of the "12x".** M2 (one ray, J R Soc Interface) and M6 (SICB abstract, "nearly 12 times") come from the same lab and period and are probably the same or overlapping experiments. I treat them as **one measurement**, not two.
- **D3, shape vs stiffness.** In the linear model of Alben et al., a base offset sets the ray's shape, and the clamped-versus-free condition sets its stiffness. The 2023 simulation (S3) reports that stiffness and curvature are coupled under actuation. These are not strictly contradictory, because the second is a nonlinear FSI setting. But the 2023 result means stiffness cannot be maximised without also imposing curvature.

### Searches run, and their scope

Three standard web searches, then one targeted search, on: the Alben et al. hemitrich mechanics; fin-ray EI by three-point bending in bluegill and zebrafish; active stiffening by hemitrich displacement; and the "565" bluegill value. Full text was read only for Alben et al. 2007 (PMC). `sites.harvard.edu` and `sicb.org` failed to resolve in this sandbox, so those items are search-summary only.

**Negative result, with scope:** these searches returned **no measured flexural rigidity for a zebrafish (*Danio rerio*) fin ray, passive or active, and no locked-vs-sliding measurement in any cyprinid.** That covers only the four web searches above. Zebrafish-specific databases, ZFIN, and the fin-regeneration mechanics literature were not searched.

## 3. What I computed (all of this is computation, not observation)

**C1. Required active factor.**
F_req = EI_req / EI_passive = 165, by construction from the brief.

**C2. Measured active factor applied to the S6 passive ray.**
EI_active = 3.8e-6 x 12 = **4.6e-5 N m^2**.
Shortfall: 6.3e-4 / 4.6e-5 = **13.8x short**.
Assumption A1 (generous): S6's passive value is the *one-base-free* state, so the full 12x applies. If S6 measured or assumed an intact ray whose bases are partly constrained, the available gain is below 12x and the shortfall is worse than 13.8x.

**C3. Modelled ceiling applied to the S6 passive ray.**
EI_ceiling = 3.8e-6 x 100 = **3.8e-4 N m^2**.
Shortfall: 6.3e-4 / 3.8e-4 = **1.65x short**.
This needs G > 1e5. The one measured ray sits at G ~ 1e2 (S1). So reaching the ceiling means raising the interlaminar shear coupling about 1000-fold, toward a fully bonded hemitrich pair. A fully bonded pair is no longer an actively *controlled* ray but a fused one. Even the model ceiling does not close the gap.

**C4. Geometric upper bound, sanity check (my own textbook beam algebra, not from any source).**
Treat the two hemitrichs as rectangular strips of thickness t, width b, with centroids separated by d.
- Uncoupled: EI_0 = 2 E b t^3 / 12.
- Fully coupled, by the parallel-axis theorem: EI_full = 2 E (b t^3/12 + b t d^2/4).
- Ratio R = EI_full / EI_0 = **1 + 3 (d/t)^2**.

R = 100 (the model ceiling) needs d/t ~ 5.7. R = 165 needs **d/t ~ 7.4**: the hemitrichs would have to be spaced more than seven of their own thicknesses apart. I have no measured d/t for zebrafish, so whether real rays can reach R = 165 even in principle is **unknown**. The point of C4 is structural: any bilaminar gain is capped by cross-section geometry, whatever the muscles do.

**C5. Taking the in-vivo bluegill value (M10) at face value, scaled to zebrafish.**
Under isometric scaling, EI ∝ s^4, where s = L_zebrafish-ray / L_bluegill-ray and L_bluegill-ray = 40.3 mm.
- EI_zf = 5.65e-4 x s^4.
- Meeting 6.3e-4 needs s^4 >= 1.115, so s >= **1.03**. The zebrafish ray would have to be **at least as long as a bluegill's (~41 mm)**, on a fish only 40 mm long overall.
- Illustrative only, because zebrafish pectoral ray length is **unknown** to me (I did not find it): s = 0.25 gives EI_zf = 2.2e-6 N m^2, which is 285x short. s = 0.5 gives 3.5e-5 N m^2, 18x short.

Assumption A2: material, segmentation and active gain are size-independent. I have not verified this.

**C6. Load sharing across rays (multi-ray coupling).**
If EI_req is a *whole-fin* requirement and N rays share the load in parallel through the membrane, each ray needs only EI_req / N.
- With the measured 12x active factor, closure needs N >= 13.8.
- With the 100x model ceiling, it needs N >= 1.65.

Zebrafish pectoral ray count is **unknown** here (not retrieved). If it is in the low teens, the measured mechanism plus perfect load sharing would sit right at the margin. Perfect sharing is an optimistic assumption: the rays are not rigidly coupled, and M8 shows ~2 orders of magnitude variation in stiffness between rays.

## 4. The answer

**On the measured evidence, active stiffening does not close the gap.**

The single measured bilaminar locking factor is about **12x** (bluegill, one ray, *measured*, full-text). That leaves a zebrafish-scale ray **about 14x short** of 6.3e-4 N m^2 (C2, *derived*). The modelled asymptote of ~100x, from the linear model with near-fused hemitrichs, still leaves it **1.65x short** (C3, *derived from a model*).

The answer can flip in only two ways:
- (a) EI_req is a whole-fin figure and at least 14 rays share the load near-perfectly (C6), or
- (b) the in-vivo bluegill value (M10) reflects a real active state, and a zebrafish ray could be as long as a bluegill's (C5). That is geometrically implausible for a 4 cm fish, but I have not measured it.

**Evidence level: derived.**
**Key number: 12x** (measured active locking factor) against **165x** required.

## 5. What this does NOT establish

- **It does not establish that S6's 6.3e-4 N m^2 or 165x are right.** I could not find S6 and did not re-derive them. If EI_req is per fin rather than per ray, C6 is the operative calculation and the answer may become "marginal" rather than "no".
- **It does not use any zebrafish measurement.** Every number above is bluegill, sunfish or labrid. Zebrafish ray EI, ray length, ray count, hemitrich thickness and spacing (d/t), and interlaminar shear modulus are all **unknown** here.
- **The 12x is a single ray (n = 1) in a single species**, measured as the clamped-versus-one-base-free stiffness ratio at a point load at 2/3 of the ray length. It is not a measured ratio of *active-muscle-driven* stiffness to intact passive stiffness, and not a whole-fin value. It may over- or under-state what a living fish achieves.
- **It does not resolve D1.** If Flammang et al.'s 5.65e-4 N m^2 (in-vivo, calculated) is the right baseline for "an actively controlled bluegill ray", then live rays may be stiffer, by roughly 50-500x over excised values, than the bilaminar 12x alone explains. That would be strong evidence *for* large active (or in-vivo) stiffening. I could not read that paper's full text, and M11's curvature value looks like a unit error, so I hold M10 at search-summary level.
- **It does not address dynamic loads.** All numbers are quasi-static, small-deflection, linear. Flapping and gust loads, buckling under compression (not discussed by Alben et al.), fatigue, and nonlinear collagen stiffening (the authors saw force rising faster than linearly) are all out of scope.
- **It does not address cost.** Holding the bases locked takes sustained muscle force: 10-15 mN for 100 µm displacement in sunfish (M7, search-summary). The energetic and fatigue cost of holding that through a glide is not estimated.
- **It does not test non-bilaminar routes to stiffness:** thicker or more mineralised hemitrichs, fewer segment joints (segmentation is a flexibility feature per Flammang et al. 2013), fused distal tips (which raise resistance in the low-G limit per Alben et al.), or added rays. These are design changes, not active control, and are out of S26's scope.
- **The negative search is narrow:** four web searches plus one full-text read. Absence of a zebrafish ray EI in these results is not absence in the literature.

## 6. What would change the answer

1. **Measure a zebrafish pectoral ray**: EI in three-point and cantilever bending, with bases (i) free, (ii) one free, (iii) both clamped. This directly gives EI_passive and the zebrafish active factor. A zebrafish factor >= 165x, or a clamped EI >= 6.3e-4 N m^2, flips the answer to yes.
2. **Measure hemitrich thickness t and spacing d in zebrafish** (histology or µCT). If d/t < 7.4, then a 165x bilaminar gain is impossible even with perfect locking (C4), and the "no" becomes a geometric certainty rather than an evidence-limited one.
3. **Fix the upstream requirement**: state whether 6.3e-4 N m^2 is per ray or per fin, and give the zebrafish ray count N. With N >= 14 and good membrane load sharing, the measured 12x may suffice (C6).
4. **Resolve D1**: read Flammang et al. 2013 in full and establish whether 5.65e-4 N m^2 is an active in-vivo ray EI comparable to Alben et al.'s 1e-6 to 1e-5. If it is, then in-vivo active stiffening is much larger than 12x, and the answer must be re-done with that factor.
5. **Design change at the organ level**: a fused or partly fused hemitrich pair (pushing G toward 1e5) plus a thicker cross-section (larger d/t). This gives up active camber control for passive rigidity, which hands the problem back to S6's passive framing with a better beam.

---

Sources (read-levels as in section 2):
- [Alben, Madden & Lauder, J R Soc Interface (PMC2359861)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2359861) (full-text, via summarizer)
- [Flammang et al. 2013 J Morphol, Harvard-hosted PDF](https://sites.harvard.edu/glauder/files/2022/03/Flammang.etal_.2013.JMorph_finrays.pdf) (could-not-access; seen as search-summary)
- [Flammang et al. 2013, NJIT listing](https://researchwith.njit.edu/en/publications/functional-morphology-of-the-fin-rays-of-teleost-fishes/) (listing)
- [SICB abstract, fin rays of ray-finned fishes](https://sicb.org/?p=32702) (could-not-access; search-summary)
- [Lauder et al. 2011 Smart Mater. Struct.](https://bpb-us-e1.wpmucdn.com/sites.harvard.edu/dist/6/58/files/2022/03/Lauder-etal-SMS-2011.pdf) (search-summary)
- [Aiello et al. 2018 J Exp Biol jeb163360](https://cob.silverchair.com/jeb/article/221/1/jeb163360/19550/The-relationship-between-pectoral-fin-ray) (search-summary)
- [Bodaghi & Xue, APS DFD 2021 Q13.4](https://archive.aps.org/dfd/2021/q13/4) (search-summary)
- J Fluid Mech 2023 actuated sunfish fin-ray simulation (search-summary; [core reader link](https://core-prod.cambridgecore.org/core/product/1452FBF93D258A71675AAEA45606D401/core-reader); authors not confirmed)

```swarm-result
{"subproblem": "S26", "evidence": "derived",
  "answer": "No on current evidence: the only measured active (hemitrich base-locking) stiffening factor is ~12x (one bluegill ray), leaving a zebrafish-scale ray ~14x short of 6.3e-4 N m^2, and even the modelled ~100x ceiling is 1.65x short; it could close only if the requirement is per-fin and shared across >=14 rays, or if an unverified in-vivo bluegill EI of 5.65e-4 N m^2 reflects a much larger active effect.",
  "key_number": "12x measured active stiffening factor vs 165x required",
  "blocked_on": "No zebrafish fin-ray EI, ray length, ray count or hemitrich d/t found; S6 not present in repo (per-ray vs per-fin requirement unknown); Flammang et al. 2013 full text unreachable (sites.harvard.edu, sicb.org blocked by network policy)"}
```
