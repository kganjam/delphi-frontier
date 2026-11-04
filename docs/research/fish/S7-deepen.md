# S7-D: Deepening S7 (organ). Can the pectoral girdle bear and transmit lift?

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.
Parent: `docs/research/fish/S7-organ.md` on branch `claude/s7-organ-pectoral-girdle-xlxpkt` (commit `a61c9688`).
Script: `docs/research/fish/S7-deepen.py`. **Every number produced by that script is a calculation, not an observation.**

## 0. What S7 concluded

S7 found that the bone of the girdle is probably not the limit. It gave two reasons:

- The computed root bending moment per fin is 2×10⁻⁵ to 1.1×10⁻⁴ N·m.
- Carrying that moment needs only a solid-equivalent bone section of about 0.12–0.35 mm.

S7 put the binding constraint at the mobile fin–girdle joint. It also said that no zebrafish girdle dimension was used.

## 1. Which input is the conclusion most sensitive to? (recomputed)

I varied every modelled input of S7 by ×0.5 and ×2 around the worst case (V = 3 m/s, n = 3, σ_y = 25 MPa, r = 0.5 mm). The results below are **calculated** (script part 1).

| Input varied ×0.5 / ×2 | Effect on moment M | Effect on required section d | Required d (mm) | Joint reaction (×W) |
|---|---|---|---|---|
| Speed V (assumed) | ×2.06 / ×0.47 | ×1.27 / ×0.78 | 0.449 / 0.275 | 113 / 26 |
| Load factor n (assumed) | ×2.0 / ×0.5 | ×1.26 / ×0.79 | 0.445 / 0.280 | 110 / 28 |
| C_L (search-summary) | ×1.44 / ×0.69 | ×1.13 / ×0.88 | 0.399 / 0.312 | 79 / 38 |
| Aspect ratio (search-summary) | ×0.69 / ×1.44 | ×0.88 / ×1.13 | 0.312 / 0.399 | 38 / 79 |
| Bone yield stress σ_y (assumed construction) | none | ×1.26 / ×0.79 | 0.445 / 0.280 | none |
| Muscle moment arm r, muscle stress | none | none | 0.353 | 110 / 28 |
| Body half-width | ≤6% | ≤2% | about 0.35 | 52–57 |

The required section changes by at most 27% for any factor-of-two error in any modelled input, because d ∝ M^(1/3). **None of these inputs flips the conclusion.** All the "required" numbers sit in a narrow band of about 0.2–0.45 mm.

The conclusion turns instead on the number S7 did *not* have: the **actual bending section of the girdle element that receives the fin's moment**. S7 compared its required section with a guess that the zebrafish cleithrum is "a few tenths of a mm" thick. Stress in a section scales as 1/(linear size)³. So if that guessed size is wrong by a factor of two, the bone stress changes by a factor of **8** (calculated). Take a 0.4 mm guess and halve it to 0.2 mm: the stress then exceeds the worst-case requirement of 0.35 mm by a factor of (0.353/0.2)³ ≈ 5.5, and the answer flips to "bone fails". **This is the weakest input:** the actual section modulus of the girdle at the fin articulation.

The joint conclusion is linear in the two assumed muscle inputs, moment arm r and muscle stress. A factor of two there moves the required adductor area from 1.1 to 2.2 mm². That is still about 0.5% of body mass, and S7's judgement that this is "not obviously prohibitive" survives it. That judgement is weak for a different reason: the available adductor area is also unmeasured.

## 2. How well established is the weakest input?

**Evidence level: assumption. It is not measured, and not even a proxy.** S7 itself wrote that the section is "plausible but unverified". But S7's headline sentence ("bone strength … probably not the binding constraint") reads as more settled than that. This is a case of an assumption being repeated until it reads like a finding.

There is also a second problem, in the anatomy. S7 modelled "the girdle" as a beam and named the cleithrum. In teleosts, though, the fin rays articulate with **proximal radials**, and those articulate with the **scapula** (and coracoid). The cleithrum is reached only after that.

- Keer et al. 2019 (full-text, PMC6800157, read through an automated summarising fetch): "There are four proximal radials (rad I–IV) on each side that articulate with the scapulae." The scapula, mesocoracoid and coracoid are "endochondral mesoderm-derived bones". The cleithrum is dermal bone.
- In thyroid-hormone-deficient fish, the proximal radials "rarely ossify" and the coracoid and scapula "fail to fully ossify or fuse" (Keer 2019, full-text). This shows that ossification of these root elements depends on hormonal state. The paper describes the wild type only qualitatively.

*My inference, not the authors' claim:* the section that first meets the root moment is the row of four proximal radials and the scapula. These are smaller than the cleithrum plate. So S7's guess was not only unmeasured; it was taken at the **wrong element**, and probably on the generous side.

## 3. Going to improve it

### 3a. The real quantity: girdle section from µCT

**Search scope.** Three web searches: adult zebrafish cleithrum thickness by µCT; cleithrum size in mm; cleithrum thickness in µm from histology. Full-text reads of:

- Keer et al. 2019 (PMC6800157), first 100k of 115k characters;
- Nguyen et al. 2022 (PMC9204358);
- *Nat. Commun.* 2024 "Multiple embryonic sources converge to form the pectoral girdle skeleton in zebrafish" (PMC11282072), first 100k of 130k characters.

**Result.** None of these reports a numeric thickness, area, second moment of area or volume for an adult zebrafish cleithrum, scapula, coracoid or proximal radial. Keer 2019 is qualitative and uses clearing-and-staining and histology, not µCT. Nguyen 2022 segments the supracleithrum but reports no girdle measurement. The *Nat. Commun.* 2024 paper covers 72–96 hpf larvae only. The value stays **unknown**.

**Primary data that would settle it does exist.** Nguyen, Lanni, Xu, Michaelson & McMenamin 2022, *Front. Physiol.* 13:875866 (full-text, read through a summarising fetch) deposited raw whole-body µCT scans of juvenile and adult zebrafish (12–25 mm SL) at a 10.5 µm scanning resolution. They are in MorphoSource project **000415918**; Table 1 lists the scan IDs, for example 000415877 for the 12 mm SL fish.

At 10.5 µm, a 0.2–0.4 mm section is about 20–40 voxels across, which is enough to resolve it. **I could not access these scans.** www.morphosource.org is refused by this session's network policy (proxy CONNECT 403; DNS refusal from the fetch tool). MorphoSource downloads may also need an account. Accessing the scans would require MorphoSource to be allowed in the session's network settings, plus a MorphoSource login.

**Measurement that would settle it, and its cost.**

1. Download 2–3 adult scans (≥20 mm SL) from project 000415918.
2. In 3D Slicer, using the segmentation workflow of Bearce et al. 2023 (*STAR Protocols*, listing), segment the proximal radials, scapula and cleithrum.
3. At the radial–scapula articulation and at the cleithrum just anterior to the fin base, take cross-sections perpendicular to the fin's spanwise axis.
4. Compute area, I and Z = I/c (BoneJ "Slice Geometry").

Cost: no wet-lab work and no new scanning. About one to two analyst-days with free software (calculated estimate). Note that 20–25 mm SL is smaller than the 0.4 g, ~40 mm design fish, so isometric scaling to 40 mm (Z ∝ L³) would itself add an assumption.

Commissioning new scans would cost about one day of a lab µCT instrument per batch of fish. The price is not known to me; I did not look it up.

**Threshold the measurement must beat (calculated).** I modelled the receiving element as a plate of depth h (in the bending plane) and thickness t, with Z = t·h²/6. This uses the worst case (V = 3 m/s, n = 3), measured σ_y = 62.6 MPa (§3b) and a safety factor of 1.5.

| Depth h | Required thickness t (σ_y = 62.6 MPa) | Required t (σ_y = 43.4 MPa, lower 1-SD) |
|---|---|---|
| 0.25 mm | 249 µm | 359 µm |
| 0.5 mm | 62 µm | 90 µm |
| 1.0 mm | 16 µm | 22 µm |
| 2.0 mm | 4 µm | 6 µm |

**Decision rule** (all calculated):
- A broad plate (cleithrum-like, h ≥ 1 mm) is almost certainly adequate as a material, because any ossified plate is thicker than about 20 µm.
- A narrow rod (radial-like, h ≈ 0.25 mm) needs to be nearly solid and about 0.25–0.36 mm across. That is roughly the same scale as the element itself, so the outcome there is genuinely open.

### 3b. A secondary input that I *could* improve: bone yield stress

S7 built σ_y = E × 0.5% yield strain, with E = 5–22.7 GPa, giving 25–114 MPa. **That was an assumed construction, not a measurement.**

**Measured replacement.** Fiedler, Zeveleva, Duarte, Zhao, Depalle, Cardoso, Jin & Berteau 2019, "Microstructure, mineral and mechanical properties of teleost intermuscular bones", *J. Biomech.* 94:59–66 (full-text, PMC6995032, read through a summarising fetch). They ran uniaxial micro-tensile tests on hydrated Atlantic herring intermuscular bones.

| Group | E (GPa) | Yield stress (MPa) | Ultimate stress (MPa) | Yield strain |
|---|---|---|---|---|
| Small fish (n = 20) | 3.5 ± 1.4 | 66.8 ± 23.4 | 110.5 ± 23.4 | 0.030 ± 0.009 |
| Large fish (n = 23) | 2.6 ± 0.5 | 62.6 ± 13.2 | 107.5 ± 22.6 | 0.036 ± 0.008 |

The authors claim these bones have "similar strength as mammalian cortical bone".

**What this shows about S7's construction** (my inference from the table): the measured yield strain is about **3%, not 0.5%**. Fish bone here is compliant but not weak. Applying S7's E × 0.5% rule to herring's own E would predict 13–18 MPa, which is about 4× below the measured yield. The rule is biased low for compliant fish bone. S7's bracket happened to contain the measured value, but for the wrong reason.

**Disagreement between sources on modulus** (kept, not averaged):

| Source | E | Method and specimen | Read-level |
|---|---|---|---|
| Fiedler 2019 | 2.6–3.5 GPa | Tensile, herring intermuscular bone | full-text |
| Atkins et al. 2014, *PNAS* 111:16047 (PMC4234560) | "5–8 GPa" for fish bone | Citing others; carp and tilapia opercula tested in 3-point bending, but no numbers in the text; fish curves "continued to strain without failure until the displacement limit of the testing machine" | full-text |
| Jiao et al. 2020, *Materials* 13:5099 (PMC7696420) | ~12 GPa | 3-point bending, first rib of *Carassius langsdorfii*, a cyprinid like zebrafish | full-text |
| Bohns et al. 2024 (carried over from S7) | 22.74 GPa | Nanoindentation, zebrafish vertebra | search-summary |

The spread is about 8×. It reflects differences in method (tissue nanoindentation, whole-bone bending, tensile) and in bone type. The result does not depend on E, because the relevant quantity is yield *stress*.

**Caveats on transferring the herring numbers:**
- Herring (Clupeiformes) and zebrafish (Cypriniformes) are both otocephalans, but the bone types differ: intermuscular bones are tendon ossifications, while the girdle has dermal and endochondral bone. Whether girdle bone yields at the same stress is **unknown**.
- These are tensile values. Bending yield is usually higher than tensile yield for bone, which would make the test conservative; I did not retrieve a fish-specific comparison.
- No zebrafish girdle bone strength test was found. The search scope is the one in §3a plus one search for fish-bone yield strength in MPa.

## 4. Recomputation

With σ_y = 62.6–66.8 MPa (measured means, herring) in place of the 25–114 MPa construction, the required solid-equivalent section is as follows (calculated):

| Case | S7 (σ_y = 25–114 MPa) | S7-D (σ_y = 62.6–66.8 MPa) | S7-D, lower 1-SD (43.4 MPa) |
|---|---|---|---|
| V = 3, n = 1 | 0.148–0.245 mm | 0.176–0.180 mm | 0.204 mm |
| V = 3, n = 3 (worst) | 0.213–0.353 mm | **0.255–0.260 mm** | 0.294 mm |
| V = 5, n = 1 | 0.123–0.204 mm | 0.147–0.150 mm | 0.170 mm |
| V = 5, n = 3 | 0.177–0.294 mm | 0.212–0.217 mm | 0.245 mm |

**What improved.** The material side is now anchored to a measured teleost yield stress, read in full text, instead of an assumed strain applied to a vertebral modulus. The worst-case requirement falls from 0.353 mm to 0.26 mm, or 0.29 mm at the lower 1-SD value.

**What did not improve.** The input the answer is most sensitive to is the actual section of the receiving element. It is still unmeasured: data exist (MorphoSource 000415918) but were not accessible from this session. Section 2 adds that the receiving element is the proximal radials and scapula, which are probably narrower than the cleithrum S7 implicitly used.

**Verdict: STANDS.**
- S7's claim that bone strength is "probably not the binding constraint" survives. On the material side it is a little better supported: a narrower and measured σ_y, and a required section about 26% smaller in the worst case.
- It does not strengthen to a closed comparison, because the actual section is still unknown.
- The anatomical correction in §2 *adds* risk. For a cleithrum-like plate, bone is adequate by a wide margin. For radial-like rods about 0.25 mm deep, the outcome is open (§3a table).
- S7's joint conclusion (a reaction of 9–55× W, held by muscle or a lock) is unchanged; its inputs were not improved here.

## 5. What this does not establish

- **No zebrafish girdle dimension was measured** here either. The comparison is still open on one side.
- **Herring intermuscular bone is not zebrafish girdle bone.** It differs in species, bone type and loading mode (tensile, not bending).
- **The plate model ignores real geometry.** It ignores curvature, flanges, stress concentrations at the radial facets, cartilage–bone interfaces and buckling, as S7's rod model did.
- **The load-path correction (radials and scapula before cleithrum) is an inference.** It comes from the articulation described by Keer 2019; the moment share each element carries was not computed.
- **Scaling the 20–25 mm SL scan fish to a 40 mm design fish** would add an isometry assumption.

## Sources

- Keer S. et al. (2019). Anatomical assessment of the adult skeleton of zebrafish reared under different thyroid hormone profiles. *Anat. Rec.* doi:10.1002/ar.24139. [PMC6800157](https://pmc.ncbi.nlm.nih.gov/articles/PMC6800157/). *full-text* (summarising fetch; first 100k of 115k characters).
- Nguyen S.V., Lanni D., Xu Y., Michaelson J.S., McMenamin S.K. (2022). Dynamics of the zebrafish skeleton in three dimensions during juvenile and adult development. *Front. Physiol.* 13:875866. [PMC9204358](https://pmc.ncbi.nlm.nih.gov/articles/PMC9204358/). *full-text* (summarising fetch). MorphoSource project 000415918: *could-not-access* (network policy).
- Multiple embryonic sources converge to form the pectoral girdle skeleton in zebrafish (2024). *Nat. Commun.* [PMC11282072](https://pmc.ncbi.nlm.nih.gov/articles/PMC11282072/). *full-text* (summarising fetch; first 100k of 130k characters). Author names were not extracted, so they are not given here.
- Fiedler I.A.K., Zeveleva S., Duarte A., Zhao X., Depalle B., Cardoso L., Jin S., Berteau J.P. (2019). Microstructure, mineral and mechanical properties of teleost intermuscular bones. *J. Biomech.* 94:59–66. [PMC6995032](https://pmc.ncbi.nlm.nih.gov/articles/PMC6995032/). *full-text* (summarising fetch).
- Atkins A., Dean M.N., Habegger M.L., Motta P.J., Ofer L., Repp F., Shipov A., Weiner S., Currey J.D., Shahar R. (2014). Remodeling in bone without osteocytes: billfish challenge bone structure–function paradigms. *PNAS* 111:16047–16052. doi:10.1073/pnas.1412372111. [PMC4234560](https://pmc.ncbi.nlm.nih.gov/articles/PMC4234560/). *full-text* (summarising fetch; Supporting Information not read).
- Jiao Y.Y., Okada M., Hara E.S., Xie S.C., Nagaoka N., Nakano T., Matsumoto T. (2020). Micro-architectural investigation of teleost fish rib inducing pliant mechanical property. *Materials* 13:5099. [PMC7696420](https://pmc.ncbi.nlm.nih.gov/articles/PMC7696420/). *full-text* (summarising fetch). The MDPI copy returned 403.
- Bearce et al. (2023). *STAR Protocols*, adult zebrafish µCT segmentation protocol. *listing*.
- Cohen L. et al. (2012). *J. Exp. Biol.* 215:1983. Absolute values are still *could-not-access*; a search for its MPa values returned only abstract-level text.
- Bohns et al. (2024). Carried over from S7: *search-summary*.

```swarm-result
{"subproblem": "S7-D", "evidence": "derived", "answer": "The conclusion is insensitive (≤27%) to factor-2 errors in every modelled input but flips with a factor-2 error in the unmeasured actual girdle section (stress ∝ size⁻³, ×8); replacing the assumed 25–114 MPa bone yield with measured teleost yield (62.6–66.8 MPa, herring intermuscular bone, tensile) narrows the worst-case required solid-equivalent section to ~0.26 mm, so 'bone probably not limiting' stands but stays open until the proximal-radial/scapula section is measured from existing µCT (MorphoSource 000415918, not accessible from this session).", "key_number": "bone yield stress 62.6–66.8 MPa (measured, herring IB tensile) → required section 0.26 mm at 1.1e-4 N·m per fin; actual girdle section: unknown", "verdict": "stands"}
```
