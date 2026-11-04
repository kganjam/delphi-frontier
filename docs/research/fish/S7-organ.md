# S7 (organ): Can the pectoral girdle bear and transmit lift?

Project: `zebrafish-flight`. Scale: organ. Date: 2026-11-04.

**Short answer.** In this calculation, bone strength is probably not the limit at 0.4 g. The weak point is the joint at the fin root: a fish fin attaches to its girdle through a mobile, muscle-held joint, not a rigid bony connection. The bending moment that gliding puts on it is small in absolute terms but large compared with body weight. None of the zebrafish girdle dimensions needed to close the comparison were found. The overall result is therefore **derived**, resting on measured inputs that are only partly verified.

---

## 1. The question, restated with the numbers that make it hard

A 0.4 g *Danio rerio* weighs W = 0.4×10⁻³ kg × 9.81 m s⁻² = **3.92 mN** (computed). To glide, the pectoral fins, acting as wings, must make lift L ≈ W cos γ ≈ W in a shallow steady glide. In a pull-up, or when leaving the water at high angle of attack, they must make n·W, where n is the load factor.

Each fin therefore carries about W/2 of lift, spread along a semispan that is roughly equal to the body length (see §3). At the fin root, that lift becomes a **bending moment about the fin–girdle articulation**. The girdle (cleithrum plus scapulocoracoid) must either resist that moment or pass it into the body.

Three things make this hard:

- **Magnitude.** In a paddling fish, fin forces are hydrodynamic thrust and braking forces of order a fraction of W, and they act in water. Body weight is mostly carried by buoyancy. In air, buoyancy is gone and the whole of W·n goes through two fin roots.
- **Moment arm.** A gliding-capable fin is long. The design in §3 puts the centre of lift 11–18 mm from the root. Paddling loads act on a fin a few mm long.
- **Geometry.** The pectoral fin of a teleost meets the scapulocoracoid through a row of small proximal radials. That is a hinge-like joint moved by abductor and adductor muscles. It is not a fused cantilever, so bone stiffness alone does not decide whether a moment can be carried there.

## 2. What is measured

Every value below carries its read-level. "Search-summary" means I saw the number only in a search engine's summary of the source, not in the source itself.

| Quantity | Value | Source, year | Read-level | Notes |
|---|---|---|---|---|
| Zebrafish vertebral elastic modulus (nanoindentation, control group) | 22.74 ± 1.60 GPa | Bohns, Akhtar, Chuang & Chen, 2024 (glucocorticoid-osteoporosis model) | search-summary | Measured on **vertebrae**, not girdle bone. Nanoindentation measures tissue-level modulus, which is generally higher than whole-bone modulus. Treated as an upper bound. |
| Zebrafish mutant bone modulus | *liliput*: about 32% lower E than wild type. *stöpsel*: higher E, more brittle. | Wang et al. 2002; Zhang et al. 2002 | search-summary | No absolute values obtained. Shows that zebrafish bone modulus is genetically variable. |
| Teleost bone modulus relative to amniotes | Young's moduli of cellular (carp, *Cyprinus carpio*) and acellular (tilapia) bone are "in the same range, and lower than Young's moduli of the bones of mammals and birds" | Cohen, Dean, Shipov, Atkins, Monsonego-Ornan & Shahar, 2012, *J. Exp. Biol.* 215:1983 | abstract (Europe PMC) | Carp is a cyprinid, like zebrafish. Full text returned HTTP 403, so the absolute numbers are **unknown** to me. Fish bone is reported as less mineralised than amniote bone. |
| Teleost bone **strength** (ultimate or yield stress) | **unknown** | I tried Horton & Summers 2009 (sculpin ribs), the Dean & Shahar 2012 review and Cohen et al. 2012 | abstract / search-summary only | No strength value was retrieved. The sculpin abstract reports stiffness falling along the rib, but no strength value. |
| Flying-fish (*Cypselurus hiraii*) maximum lift coefficient | ≈0.78 at α ≈ 30–35° (wind tunnel, stuffed specimens) | Park & Choi, 2010, *J. Exp. Biol.* 213:3269 | Abstract (via Europe PMC) for the 30–35° angle. **Search-summary** for the 0.78 value. | **Disagreement:** a later CFD study of the same morphology is reported to give C_L,max = 1.03 and L/D_max = 4.7, against the wind-tunnel 0.78 and 4.37. I keep both values; §3 uses 0.78, which is the more conservative because it needs a larger wing and so a larger moment. |
| Flying-fish model weight | ≈0.6 N (≈61 g) | Park & Choi 2010 | search-summary | Used only for the scaling comparison. |
| Flying-fish aspect ratio | 9.0–10.7 | Unnamed paper returned with Park & Choi search results | search-summary | Source not identified. Treat as indicative. |
| Flying-fish pectoral girdle | "considerably enlarged by comparison with most teleosts, the coracoid and scapula being particularly hypertrophied" | Davenport, 1994, *Rev. Fish Biol. Fish.* 4:184 (as quoted in a search summary) | search-summary | No dimensions. The full text is paywalled (Springer). |
| Flying-fish wing loading | Positive allometry with standard length. Largest individuals are comparable to cormorants and pelicans. Flight begins at about 50 mm standard length. | Davenport 1994 | search-summary (abstract-level) | No numerical values obtained. |
| Hatchetfish (Gasteropelecidae, Characiformes) girdle | "enlarged, heavily-muscled pectoral girdle". Expanded coracoids are fused to a corrugated median keel. Powered flapping flight is reported as disproven by Wiest 1995; they leap and glide. | FishBase family summary, citing Wiest 1995 and Weitzman & Palmer 1996 | listing / search-summary | This is an **ostariophysan** relative of zebrafish with a load-bearing girdle. Wiest 1995 itself was not read. |
| Mudskipper (*Periophthalmus barbarus*) pectoral-fin ground reaction force | Isolated fins bear peak net ground reaction force, as a fraction of body weight, similar to salamander forelimbs (SICB abstract). The journal abstract says vertical ground reaction force is *lower* than in salamanders and more medially directed. The authors suggest medial forces would give high bone stresses. | Kawano & Blob, 2013, *Integr. Comp. Biol.* 53:283 | abstract / search-summary | **Disagreement between the two abstracts** is kept as found. No numbers were obtained. |
| Zebrafish cleithrum or scapulocoracoid cross-section, fin-base width, adductor/abductor mass | **unknown** | Searched "adult zebrafish pectoral fin length area cleithrum size morphometrics mm" | search-summary (no hits) | **Scope of negative search:** one web search plus the literature above. ZFIN, μCT atlases (for example the Hur et al. / Weinstein-lab microCT data) and the Gioia et al. 2017 supplementary tables were **not** checked. Absence here does not mean the data do not exist. |

Access limits for this session: journals.biologists.com returned 403. typeset.io, semanticscholar.org and flair.monash.edu (the Park & Choi IUTAM 2007 PDF) are outside the session's network allow-list. Europe PMC abstracts were reachable.

## 3. What I computed

**Everything in this section is computation, not observation.** Script: `S7.py`, kept in the session scratchpad; all of its arithmetic is reproduced below.

### 3a. Assumptions

| # | Assumption | Basis |
|---|---|---|
| A1 | m = 0.4 g, W = 3.92 mN | Project brief |
| A2 | C_L = 0.78 at the design point | Park & Choi wind-tunnel value (search-summary). The CFD value of 1.03 would shrink the wing and the moment by about 1/√1.32 in span. |
| A3 | Glide or launch speed V = 3 or 5 m s⁻¹ | **Bracket I chose myself; not measured for zebrafish.** Zebrafish burst speed out of water is outside S7's scope and belongs to another subproblem. |
| A4 | Aspect ratio 9 (span over both fins plus body) | Low end of the flying-fish range (search-summary) |
| A5 | Body half-width 2.5 mm | Estimate; not measured |
| A6 | Elliptic spanwise lift, so the centroid of each half-wing's lift sits at 4/(3π) ≈ 0.424 of the fin length | Standard aerodynamic idealisation |
| A7 | Load factor n = 1 (steady glide) and n = 3 (launch or pull-up) | Engineering bracket; not measured |
| A8 | Bone yield stress σ_y = E × 0.5% yield strain, with E = 5–22.7 GPa, giving **σ_y = 25–114 MPa** | The 0.5% yield strain is a generic bone value I am **assuming; I did not retrieve it for fish**. The 22.7 GPa is the zebrafish vertebral nanoindentation value. The 5 GPa lower bound is my own choice, reflecting "lower than mammals" (Cohen 2012) and the fact that whole bone is less stiff than nanoindentation shows. |
| A9 | Fish skeletal muscle isometric stress 200 kPa | Generic vertebrate-muscle order of magnitude; **assumed, not retrieved** |
| A10 | Moment arm of the fin adductor about the articulation r = 0.5–1.0 mm | Estimate from a guess that the fin base is 1–2 mm wide; **not measured** |

### 3b. Wing size needed

Wing area: S = 2W / (ρ V² C_L), with ρ = 1.2 kg m⁻³. Span: b = √(AR·S). Fin length: s = b/2 − 2.5 mm.

| V (m/s) | S (cm²) | b (cm) | fin length s (cm) | lift centroid ȳ (mm) |
|---|---|---|---|---|
| 3 | 9.32 | 9.16 | 4.33 | 18.4 |
| 5 | 3.35 | 5.49 | 2.50 | 10.6 |

At these speeds each fin must be **about 0.6–1.1 times the body length** (40 mm). Wild-type zebrafish pectoral fins are much shorter; their actual length is unknown here.

### 3c. Root bending moment per fin

Root bending moment: M = n · (W/2) · ȳ

| V | n = 1 | n = 3 |
|---|---|---|
| 3 m/s | 3.60×10⁻⁵ N·m | **1.08×10⁻⁴ N·m** |
| 5 m/s | 2.08×10⁻⁵ N·m | 6.24×10⁻⁵ N·m |

### 3d. Path 1: the girdle bone carries M as a beam

To check whether bone alone could carry the moment, I treated the girdle as a solid circular bone section. The required section modulus is Z = M/σ_y. The equivalent solid-rod diameter is d = (32Z/π)^(1/3).

| Case | σ_y = 25 MPa | σ_y = 114 MPa |
|---|---|---|
| V=3, n=1 | d = 0.245 mm | 0.148 mm |
| V=3, n=3 | **d = 0.353 mm** | 0.213 mm |
| V=5, n=1 | 0.204 mm | 0.123 mm |
| V=5, n=3 | 0.294 mm | 0.177 mm |

On this calculation, a girdle element with a solid-equivalent bending section of **about 0.12–0.35 mm** would carry the design moment at yield. Adding a safety factor of 1.5 multiplies d by 1.5^(1/3) = 1.14, giving at most about 0.40 mm.

Whether the adult zebrafish cleithrum or scapulocoracoid has a section like this is **unknown**: I could not obtain the dimensions. The cleithrum of an adult 4 cm zebrafish is a bone plate a few mm long. A section of a few tenths of a mm is plausible but **unverified**. This is the comparison the question asks for, and it cannot be closed without a µCT measurement.

### 3e. Path 2: the fin–girdle articulation carries M through muscle (the actual load path)

The fin rays and radials articulate with the scapulocoracoid rather than fusing to it. So the root moment must be held by the adductor muscles (which pull the fin down against upward lift), by ligaments, or by a bony stop that locks the joint. Holding it with muscle alone takes a force F = M/r and a muscle cross-section (PCSA) of F/200 kPa.

| Case | r = 0.5 mm | r = 1.0 mm |
|---|---|---|
| V=3, n=1 | 72 mN (18 W), PCSA 0.36 mm² | 36 mN (9 W), 0.18 mm² |
| V=3, n=3 | **216 mN (55 W), PCSA 1.08 mm²** | 108 mN (28 W), 0.54 mm² |
| V=5, n=3 | 125 mN (32 W), 0.62 mm² | 62 mN (16 W), 0.31 mm² |

The joint must therefore carry a **reaction of 9–55 times body weight**. The same force, reacted at the scapulocoracoid, is what actually loads the girdle bone, mostly as concentrated shear and bearing at the articular facets. The PCSA needed is about 0.1–1.1 mm². With fibres about 1 mm long, that is about 1 mm³ ≈ 1 mg of muscle per side, roughly 0.25% of body mass. That is **not obviously prohibitive**, but whether it exists in zebrafish is **unknown**: I found no zebrafish pectoral adductor PCSA.

### 3f. Scaling check against a flying fish (derived; assumes isometry)

Bending moment scales as M ∝ m·L ∝ m^(4/3). Section modulus scales as Z ∝ L³ ∝ m. So bone stress scales as σ ∝ m^(1/3).

Going from a 61 g *Cypselurus* (model weight from search-summary) to 0.4 g: the moment falls by a factor of 0.00122, the section modulus by 0.0065, and so **the bone stress is about 0.19 times** that in a geometrically similar flying fish.

Under isometry, a girdle shaped like a flying fish's would be about **5 times less stressed** at zebrafish size. This is the usual "small animals are relatively strong" result, but it depends entirely on the zebrafish girdle being as robust in proportion as the hypertrophied flying-fish girdle, which it is not reported to be.

## 4. The answer

**Evidence level: derived.** The inputs are partly measured, but the measured values were mostly read at search-summary or abstract level.

> At 0.4 g, the computed root bending moment per fin at design lift is 2×10⁻⁵ to 1.1×10⁻⁴ N·m. Bone of 25–114 MPa yield strength could carry it in a solid-equivalent section of only about 0.12–0.35 mm. So **bone strength of the girdle is probably not the binding constraint at this size** (computed). The binding requirement is at the **articulation**: the mobile fin–scapulocoracoid joint must be locked or held by adductor muscle and ligament against a reaction of about 9–55 times body weight. In the current wild-type girdle, neither the joint geometry nor the muscle cross-section has been measured.

The girdle can plausibly *bear* the load as a material. Whether it can *transmit* the load, through a joint built for paddling, is **unknown** and depends on measurements I could not obtain.

On the stated refutation test, **the answer to "is there a teleost girdle bearing comparable loads?" is yes, at literature level.** Exocoetids glide carrying full body weight on their pectoral fins (Park & Choi 2010, abstract). Hatchetfishes leap and glide on a keeled, fused girdle (FishBase, listing). Both lineages have hypertrophied or fused girdles (Davenport 1994; FishBase; search-summary). That evidence supports the view that a *modified* teleost girdle can do this. It does not show that an *unmodified* zebrafish girdle can.

## 5. What this does NOT establish

- **No zebrafish girdle dimension was used.** The comparison of "required section" against "actual section" is open on one side. The computation gives the required value only.
- **No fish bone strength was measured or retrieved.** σ_y comes from modulus times an assumed 0.5% yield strain. The modulus comes from **vertebral** nanoindentation (search-summary), which overstates whole-bone stiffness. Girdle bone may differ in mineralisation, and in whether it is cellular or acellular (zebrafish bone is cellular); I did not check its material.
- **The beam model idealises the cleithrum and scapulocoracoid as a solid rod.** The real cleithrum is a curved, flanged plate, and the scapulocoracoid is partly cartilaginous in many teleosts. In a thin plate, buckling, stress concentration at the radial facets, and failure of the cartilage–bone interface could all fail before beam yield. None of these were analysed.
- **Fatigue and impact were not analysed.** Water-exit impact loads and repeated launches are not included. Bone's fatigue limit is well below its yield strength.
- **Torsion was ignored.** Lift acting off the fin's articular axis (fin pitch) produces a twisting moment about the fin root. That was not computed.
- **The speeds (3–5 m/s) and load factors (1–3) were my own brackets**, not measurements. Whether a zebrafish can reach either speed is outside S7.
- **The fin itself was not checked.** S7 asks about the girdle. Whether the lepidotrichia (fin rays) can carry a 1–4 cm cantilever lift without collapsing is a separate question, and it may well bind before the girdle does.
- **The muscle numbers (§3e) rest on two assumptions.** The 200 kPa muscle stress and the 0.5–1 mm moment arm are both assumed. A 0.25 mm moment arm would double the force and the PCSA.
- **How the load passes on from the girdle to the body was not traced.** That path runs from the cleithrum through the supracleithrum and posttemporal to the skull, and through hypaxial muscle to the body. In a symmetric glide the left and right moments partly balance across the ventral cleithral symphysis, which the girdle carries as a closed loop. The loop's strength and the skull suspension were not assessed.
- **The flying-fish and hatchetfish evidence shows that a modified girdle works.** It says nothing about the developmental route to such a girdle in *Danio*.
- **The CFD-versus-wind-tunnel disagreement over C_L (1.03 vs 0.78) was not resolved.** I used 0.78, which is conservative.

## 6. What would change the answer

1. **µCT of the adult zebrafish pectoral girdle** would close the comparison in §3d and move the evidence level toward *measured* input. It should give the cleithrum and scapulocoracoid cross-sectional area and second moment of area at the fin articulation, and the width of the radial row.
   - If the solid-equivalent section is ≥0.4 mm, bone is clearly adequate.
   - If it is ≤0.15 mm, girdle bone fails at n = 3 even at the high-strength bound, and **the answer flips to "no"**.
2. **Three-point bending or microbeam tests of zebrafish or carp girdle bone (ultimate and yield stress)** would replace the assumed 25–114 MPa bracket.
3. **Measurements of pectoral adductor PCSA and moment arm in adult zebrafish** (dissection or µCT with contrast staining) would test path 2.
   - If the available PCSA is ≪0.3 mm², the joint cannot hold glide lift, and a locking mechanism or girdle hypertrophy becomes a hard design requirement.
4. **A design change: a passive joint lock.** A bony stop, as hypothesised (not established here) for exocoetid fin spreading, or fusion of the radials would remove the muscle requirement in §3e. It would turn the root into a true cantilever, which §3d shows is light work for the bone.
5. **A higher C_L (1.03, the CFD value) or a higher launch speed** shrinks the wing and so the moment. At V = 5 m/s and C_L = 1.03 the moment falls by roughly a further 13% (computed via the span).
6. **Getting Davenport 1994, Wiest 1995 and Park & Choi 2010 in full text** would replace the search-summary values with full-text values. Exocoetid girdle cross-sections, if given, would give a real "teleost girdle under glide load" measurement to scale from.

## Sources

- Bohns F.R., Akhtar R., Chuang Y.-J., Chen P.-Y. (2024). Zebrafish vertebral nanoindentation, glucocorticoid-induced osteoporosis. [Liverpool repository](https://livrepository.liverpool.ac.uk/id/eprint/3180374). *search-summary*.
- Wang X. et al. (2002), *liliput*; Zhang Y. et al. (2002), *stöpsel*. Zebrafish bone nanomechanics. [ZFIN ZDB-PUB-020410-2](https://zfin.org/ZDB-PUB-020410-2). *search-summary*.
- Cohen L., Dean M., Shipov A., Atkins A., Monsonego-Ornan E., Shahar R. (2012). Comparison of structural, architectural and mechanical aspects of cellular and acellular bone in two teleost fish. *J. Exp. Biol.* 215:1983–1993. doi:10.1242/jeb.064790. *abstract* (Europe PMC, PMID 22573778); full text returned 403.
- Horton J.M., Summers A.P. Acellular bone of great sculpin ribs. [SICB abstract](https://sicb.org/?p=31605). *search-summary*.
- Dean M.N., Shahar R. (2012). The structure–mechanics relationship and the response to load of the acellular bone of neoteleost fish: a review. *J. Appl. Ichthyol.* 28:320–329. *listing*.
- Park H., Choi H. (2010). Aerodynamic characteristics of flying fish in gliding flight. *J. Exp. Biol.* 213:3269–3279. doi:10.1242/jeb.046052. *abstract* (Europe PMC, PMID 20833919). The C_L 0.78 and 0.6 N values are *search-summary*. Full text returned 403.
- CFD follow-up of *C. hiraii* (C_L,max 1.03, L/D 4.7): [Bioinspir. Biomim. ab23e6, PubMed 31117061](https://pubmed.ncbi.nlm.nih.gov/31117061/). *search-summary*.
- Davenport J. (1994). How and why do flying fish fly? *Rev. Fish Biol. Fish.* 4:184–214. doi:10.1007/BF00044128. *search-summary*.
- FishBase, Family Gasteropelecidae (citing Wiest 1995; Weitzman & Palmer 1996). [fishbase.se](https://www.fishbase.se/summary/FamilySummary.php?ID=109). *listing*.
- Kawano S.M., Blob R.W. (2013). *Integr. Comp. Biol.* 53:283–294. doi:10.1093/icb/ict051. [OUP](https://academic.oup.com/icb/article/53/2/283/806410) and [SICB abstract](https://sicb.org/?p=24372). *abstract / search-summary*.

```swarm-result
{"subproblem": "S7", "evidence": "derived", "answer": "The computed root bending moment at design lift (2e-5 to 1.1e-4 N·m per fin for a 0.4 g fish) needs only a ~0.12–0.35 mm solid-equivalent bone section, so girdle bone strength is probably not limiting; the unresolved constraint is the mobile fin–scapulocoracoid joint, which must hold a 9–55× body-weight reaction via muscle or a lock, and the zebrafish girdle section and adductor PCSA that would close the comparison are unknown.", "key_number": "1.1e-4 N·m root bending moment per fin (V=3 m/s, n=3, C_L=0.78)", "blocked_on": "adult zebrafish cleithrum/scapulocoracoid cross-section and pectoral adductor PCSA (no µCT/morphometric data found); teleost bone ultimate strength (full texts of Cohen 2012, Horton & Summers 2009 inaccessible)"}
```
