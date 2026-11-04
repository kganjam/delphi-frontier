# S9 — Material properties of fin ray bone (lepidotrichia) and actinotrichia

Project: `zebrafish-flight` · Scale: tissue · Date of search: 2026-11-04

> **Access note, read this first.** During this session every full-text host was blocked by the
> environment's network policy (`ias.ac.in`, `ncbi.nlm.nih.gov`, `journals.biologists.com`,
> `arxiv.org`, `web.njit.edu`, Harvard `wpmucdn.com` all failed DNS resolution). I could not open
> **any** paper. Every value below was read through web-search result summaries, so the best
> read-level anywhere in this file is **search-summary**. No value here has been checked against a
> table or figure in the source. Treat every number as "reported by a search engine's summary of
> the paper", not as "read from the paper". This is the main limit on the result.

---

## 1. The question, restated with the numbers that make it hard

**What are the measured Young's modulus E, strength, and density of (a) lepidotrichia (the
segmented, paired dermal-bone hemitrichs of the fin ray) and (b) actinotrichia (the
collagen/elastoidin fibres at the fin margin), in *Danio rerio* or, failing that, in any teleost?**

Why it is hard:

- **Scale.** A zebrafish fin ray is tens of micrometres thick. Puri et al. (2018) state, per the
  search summary, that ex-situ ray-bending methods used on larger fish "cannot be used directly, as
  zebrafish are much smaller and thus the bending stiffness is expected to be lower by several
  orders of magnitude". So the comparative fin-ray literature (bluegill, wrasse, perch, gar,
  sea-robin) measures rays that are far larger than the target animal's.
- **What gets measured is EI, not E.** Most fin-ray studies measure flexural stiffness EI by
  three-point bending. Getting E means dividing by a second moment of area I estimated from the
  cross-section. For a segmented, bilaminar, hollow, tapering ray, I is uncertain, and that
  uncertainty passes straight into E.
- **The spread is large.** Reported moduli for fish bone and fin rays run from ~0.11 GPa (distal
  bluegill ray) to ~25 GPa (zebrafish vertebra, nanoindentation). That is a ~225× range
  (24.7 / 0.11). Over that range, "use bone's modulus" is not one assumption but several.
- **Actinotrichia have no measured modulus in teleosts, as far as I could find** (see §2b).

## 2. What is measured

Read-level legend: full-text | abstract | listing | search-summary | could-not-access.
"Method" is the method the summary attributes to the paper.

### 2a. Lepidotrichia / fin rays (ray-level)

| # | Quantity | Value | Species / tissue | Method | Source (year) | Read-level |
|---|---|---|---|---|---|---|
| L1 | E, proximal (basal) ray | mean **1.34 GPa**, range **0.24–3.7 GPa** across rays | Bluegill *Lepomis macrochirus*, pectoral fin rays | Three-point bending; E from EI and estimated I | Lauder, Madden, Tangorra, Anderson, Baker (2011) "Bioinspiration from fish for smart material design and function", *Smart Mater. Struct.* 20:094014 | search-summary (abstract text quoted in summary) |
| L2 | E, distal (segmented) ray | **0.11–0.67 GPa** across rays | Same | Same | Same | search-summary |
| L3 | Proximal:distal stiffness ratio | "as much as **30×**" stiffer proximally | Bluegill (Lauder group) | Bending | A Lauder-group meeting abstract (exact citation not resolved) | search-summary |
| L4 | E, whole ray, rough figure | "about **1 GPa**" | Bony fin rays, general | Review statement | Lauder & Madden (2007) *Exp. Fluids* 43:641 | search-summary |
| L5 | Flexural stiffness EI | **0.0001–1.5109 µN·m²** | Labrid pectoral fin rays (*Gomphosus varius*, *Halichoeres bivittatus*, et al.) | Three-point bending | Aiello et al. (2017) *J. Exp. Biol.* 221:jeb163360 | search-summary |
| L6 | E in bending | "similar between species"; **numbers not obtained** | *G. varius* vs *H. bivittatus* | Bending; E = EI/I | Aiello et al. (2018) *J. Morphol.* 279:1031–1044 | search-summary (claim only, no number) |
| L7 | E, walking rays vs pectoral rays, two loading directions | **numbers not obtained**; walking rays stiffer rostro-caudally, more flexible dorso-ventrally | Sea-robins (Triglidae) | Three-point bending, hydrated, 1.27 mm/min | "Walking on chains…" (2020) *J. Exp. Biol.* 223:jeb227140 | search-summary (claim only) |
| L8 | Flexural stiffness | Reported as force/displacement, **not E**; no number obtained. Fresh ≈ frozen; formalin had a small significant effect in rays < 25 mm | Yellow perch *Perca flavescens* | Three-point bending | Taft et al. (2018) *J. Morphol.* (doi 10.1002/jmor.20831) | search-summary |
| L9 | Lepidotrichia less mineralized than cellular skeletal bone but "has a similar Young's modulus" | qualitative | Teleosts | Review citing Cohen et al. 2012 | Review surfaced by search (not resolved to a specific paper) | search-summary |

**Zebrafish-specific, ray-level:**

| # | Quantity | Value | Method | Source (year) | Read-level |
|---|---|---|---|---|---|
| Z1 | Whole caudal fin bending stiffness ("overall bending moments") along proximal–distal axis | **1.5×10⁻⁹ – 4×10⁻⁹ N·m²**, non-monotonic, with a peak not explained by geometry | In vivo, micro-Newton line-force deflection in water, accuracy ≥10% at 100 µN | Puri, Aegerter-Wilmsen, Jaźwińska, Aegerter (2018) *J. Exp. Biol.* 221:jeb171777 | search-summary |
| Z2 | Effective Young's modulus of the fin (EI / I_eff) | **Peaked; value not obtained from the paper.** Secondary sources cite the zebrafish fin's effective modulus as **~8 MPa** (rays + interray together) | Derived by authors from Z1 | Puri et al. 2018 (primary, value not seen); unnamed citing papers (secondary) | search-summary; the 8 MPa is a **secondary citation**, not checked |
| Z3 | Interray tissue modulus | **4 ± 2 kPa**, stated as an upper bound | In vivo | Puri et al. 2018 | search-summary |
| Z4 | Cutting the interray tissue | no significant change to bending stiffness. Authors: flexibility is dominated by the bony rays | In vivo | Puri et al. 2018 | search-summary |

Caution on Z2. A later paper from the same circle reports **~0.8 MPa**, but that figure is for
**PDMS hydrofoils** characterized with Puri's method, not for fin tissue. I have kept it out of
the tissue data on purpose.

### 2b. Actinotrichia / elastoidin

| # | Quantity | Value | Species / tissue | Method | Source (year) | Read-level |
|---|---|---|---|---|---|---|
| A1 | Tensile modulus and strength of elastoidin vs rat-tail tendon | **No number obtained.** Author claim: elastoidin modulus is **higher than tendon both dry and hydrated**; dry strength higher than tendon; strength "comparatively low when hydrated"; failure by lamellar fissuring | **Shark** fin elastoidin (ceratotrichia), not teleost actinotrichia | Tensile test of fibres | Rajaram, Sanjeevi, Ramanathan (1981) *J. Biosci.* 3:303–309, doi 10.1007/BF02702941 | search-summary (full text at ias.ac.in: could-not-access, host blocked) |
| A2 | Elastoidin "intermediate between collagen and elastin" | qualitative expectation, not a measurement | — | Review statement | Review surfaced by search | search-summary |
| A3 | Composition of zebrafish actinotrichia | type I and type II collagen are the main components (attributed to Durán and colleagues). Other components unknown | *D. rerio* | Biochemistry / histology | Durán et al. (2011) as cited in a 2024 *PNAS Nexus* paper on actinotrichia probes | search-summary |
| A4 | Actinotrichia dimensions, orientation, number along larval finfold | **measured, values not obtained.** Camber from actinotrichial orientation raises finfold stiffness (model + morphometry) | Larval *D. rerio* and *Cyprinus carpio* | Morphometry + mechanical model using collagen strain limits | "Structure and function of the median finfold in larval teleosts" (2012) *J. Exp. Biol.* 215:2359 | search-summary |
| A5 | Mechanical role of actinotrichia | *col9a1c* knockout: actinotrichia lost over growth → fin tip shortens dorso-ventrally, rays fuse. **No stiffness measured**, per summary | *D. rerio* | Genetics + morphology | Nakagawa et al. (2021) *Dev. Biol.* 481:52 | search-summary |

**Negative finding (actinotrichia modulus).** I found **no measured Young's modulus, strength or
density of teleost actinotrichia.** Search scope: six web searches (standard and extended) on
combinations of "actinotrichia", "elastoidin", "Young's modulus", "stiffness", "AFM",
"nanoindentation", "tensile", "zebrafish", "collagen fibre". All bodies were read at search-summary
level; no database (Web of Science, Scopus, PubMed advanced) was queried directly. The nearest
measurement is on **shark** elastoidin (A1), and I could not read its numbers.

Context, not actinotrichia data: generic single collagen fibrils by AFM give **2–7 GPa** in one
study and **0.2–0.8 GPa** (in aqueous media) in another (search-summary; studies not individually
resolved). These are kept as a bracket for a different structure and must not be used as an
actinotrichia value.

### 2c. Fish bone tissue (not fin ray), for bracketing

| # | Quantity | Value | Species / tissue | Method | Source (year) | Read-level |
|---|---|---|---|---|---|---|
| B1 | E | **3.67–8.40 GPa, mean 6.48 GPa** | Great sculpin *Myoxocephalus polyacanthocephalus*, **acellular rib** | Bending of ribs | Horton & Summers (2009) *J. Exp. Biol.* 212:1413, doi 10.1242/jeb.020636 | search-summary |
| B2 | E, cellular vs acellular | "same range", lower than mammal/bird bone; **numbers not obtained**. Acellular bone more mineralized than cellular | Carp (cellular) vs tilapia (acellular), ribs/opercula | Mechanical tests + mineral analysis | Cohen, Dean, Shipov, Atkins, Monsonego-Ornan, Shahar (2012) *J. Exp. Biol.* 215:1983, doi 10.1242/jeb.064790 | search-summary |
| B3 | E (nanoindentation), wild type | **24.7 ± 1.8 GPa** (mutant 21.2 ± 0.8) | ***D. rerio* vertebra** | Nanoindentation | Fiedler et al. (2018) *J. Bone Miner. Res.* (Chihuahua *col1a1a* OI model) | search-summary |
| B4 | E and hardness, control adults (7 mo) | **E 22.74 ± 1.60 GPa; H 1.18 ± 0.13 GPa** | ***D. rerio* vertebra** | Nanoindentation | Glucocorticoid study (title/authors not resolved by search) | search-summary |
| B5 | Relative change, *lil/lil* mutant | −32% E, −36% hardness vs wild type; **absolute values not obtained** | *D. rerio* skeletal bone | Nanoindentation | Wang et al. (2002) *Biomaterials* 23:4557, PMID 12322976 | search-summary |
| B6 | E, *stöpsel* mutant | "significantly greater" E, similar hardness vs wild type; **no number obtained** | *D. rerio* skeletal bone | AFM nanoindentation | (2002) *Bone*, PMID 11934643 | search-summary |
| B7 | Hydrated bone tissue density | **1.557 g/cm³** (albacore), 1.856 g/cm³ (whale); organ densities 1.161–1.423 g/cm³ | Albacore *Thunnus alalunga* bone, not fin ray | Densitometry | Tont, Pearcy & Arnold (1977) *Marine Biology* | search-summary |

**Negative findings (lepidotrichia strength and density).**
- **Strength:** I found **no measured failure stress, yield stress or ultimate strength of
  lepidotrichia** in any species. Scope: three searches on "fin ray bending strength / failure
  stress / fracture / ultimate stress / lepidotrichia MPa", read at search-summary level.
  Horton & Summers (2009) may report a rib yield strength, but I could not read it.
- **Density / mineral density:** I found **no fin-ray tissue density (g/cm³) or calibrated tissue
  mineral density (mg HA/cm³)**, for zebrafish or any teleost. Zebrafish fin micro-CT studies
  surfaced (Silvent et al. 2017; Cardeira et al. 2016, *Sci. Rep.* 6:39191) use qualitative
  imaging or alizarin-red intensity proxies, per the summaries. Scope: two searches.
- **Zebrafish lepidotrichia E at material level:** I found **no nanoindentation or ex-vivo bending
  E measured on zebrafish fin rays.** All zebrafish material-level E values (B3–B6) are vertebral
  or general skeletal bone. Scope: four searches.

### 2d. Disagreements, preserved

1. **Ray-level E vs bone-tissue E differ by ~1–2 orders of magnitude.** Bluegill ray bending gives
   0.11–3.7 GPa (L1, L2). Fish rib bending gives 3.67–8.40 GPa (B1). Zebrafish vertebra
   nanoindentation gives ~23–25 GPa (B3, B4). These are **not** necessarily in conflict.
   Bending of a segmented, jointed, collagen-rich composite ray measures a structural *effective*
   modulus. Nanoindentation measures local mineralized matrix, and it typically reads higher than
   bulk tests. They are still different quantities, and an organ-scale model must say which one it
   uses.
2. **Lauder group "~1 GPa, similar to tendon" (L1, L4) vs "fin rays have a similar Young's modulus
   to cellular bone" (L9, via Cohen et al. 2012).** If cellular fish bone sits in the
   3.7–8.4 GPa band (B1/B2), then L9 and L1 disagree by a factor of ~3–6. I cannot resolve this
   without full texts.
3. **Effective whole-fin modulus ~8 MPa (Z2, secondary).** This is ~170× below the lowest bluegill
   ray value (1.34 GPa / 8 MPa ≈ 168). That is expected if I_eff is the I of the whole fin plate,
   including soft tissue, rather than of the bone alone. It is still a separate number from a
   separate definition, and must not be swapped for a bone modulus.
4. **Within-study scatter is large.** Proximal bluegill rays span 15× (3.7 / 0.24). Distal rays
   span 6× (0.67 / 0.11). Sculpin ribs span 2.3× (8.40 / 3.67).

## 3. What I computed (computation, not observation)

All arithmetic below is **computed by me** from the search-summary values above. None of it is a
measurement.

**C1. Range of reported moduli.** 24.7 GPa / 0.11 GPa = **~225×** from the softest distal ray
to the zebrafish vertebra.

**C2. What zebrafish fin geometry would be implied by each candidate E.** This is an illustrative
inversion, not a prediction. Take Puri et al.'s whole-fin bending stiffness EI = 1.5–4 ×10⁻⁹ N·m²
(Z1). Assume all of it is carried by **one solid circular rod** of modulus E (a deliberately crude
assumption). Then I = EI/E and r = (4I/π)^¼:

| Assumed E | Source of E | I (m⁴), EI = 1.5e-9 → 4e-9 | Equivalent solid-rod radius (µm) |
|---|---|---|---|
| 8 MPa | Z2 (secondary, whole-fin effective) | 1.9e-16 → 5.0e-16 | 124 → 159 |
| 0.11 GPa | L2 distal bluegill, low end | 1.4e-17 → 3.6e-17 | 65 → 83 |
| 1.34 GPa | L1 proximal bluegill, mean | 1.1e-18 → 3.0e-18 | 35 → 44 |
| 6.48 GPa | B1 sculpin rib, mean | 2.3e-19 → 6.2e-19 | 23 → 30 |
| 24.7 GPa | B3 zebrafish vertebra | 6.1e-20 → 1.6e-19 | 17 → 21 |

Assumptions: linear elastic; Euler–Bernoulli beam; one solid round section. In reality there are
~18 rays, each a pair of hollow, segmented hemitrichs. I do not know whether Puri's EI is per fin,
per ray or per unit width; the summary does not say. The point of this table is only this: the
choice of E moves the inferred cross-section by ~7× in radius (159 / 21), equivalent to ~3,000×
in I. Choosing E is therefore not a minor input.

**C3. Specific stiffness E/ρ.** Use the only fish bone-tissue density found (albacore,
1.557 g/cm³, B7), which is **not a fin-ray density**:
- 0.11 GPa → 7.1×10⁴ m²/s²
- 1.34 GPa → 8.6×10⁵ m²/s²
- 6.48 GPa → 4.2×10⁶ m²/s²
- 24.7 GPa → 1.6×10⁷ m²/s²

That is the same ~225× spread as C1. The density is borrowed, so these figures are bracketing
only.

## 4. The answer

**Evidence level: `literature` for the lepidotrichia modulus in non-zebrafish teleosts (read at
search-summary only). `unknown` for zebrafish lepidotrichia material E, for lepidotrichia
strength and density in any species, and for any property of teleost actinotrichia.**

- **Lepidotrichia, E.** The best ray-level measurement surfaced is bluegill pectoral rays by
  three-point bending (Lauder et al. 2011, search-summary): proximal **mean 1.34 GPa (0.24–3.7)**,
  distal **0.11–0.67 GPa**. Bracketing fish bone values run from 3.67–8.40 GPa (sculpin rib,
  bending) to ~23–25 GPa (zebrafish vertebra, nanoindentation). **No material-level E for
  zebrafish fin rays was found.** The only zebrafish ray-level datum is an in-vivo whole-fin EI of
  1.5–4×10⁻⁹ N·m² (Puri et al. 2018).
- **Lepidotrichia, strength.** **unknown.** No measured failure stress was found.
- **Lepidotrichia, density.** **unknown.** No fin-ray density was found. The nearest is albacore
  bone tissue at 1.557 g/cm³.
- **Actinotrichia, E / strength / density.** **unknown.** No teleost measurement was found. The
  nearest is a 1981 tensile study of **shark** elastoidin, which says, per the summary, that its
  modulus exceeds tendon's, wet and dry. I could not read its numbers.

The key number for organ-scale work is the **proximal fin-ray modulus, 1.34 GPa (range
0.24–3.7 GPa, bluegill, search-summary)**. It must be carried with its 15× within-study scatter
and the ~225× cross-method spread. It must not be treated as a zebrafish value.

## 5. What this does NOT establish

- **It does not establish any zebrafish fin-ray material property.** Every ray-level E is from
  bluegill. The zebrafish values are either whole-fin structural EI (Puri) or vertebral
  nanoindentation (B3–B6). Neither is lepidotrichia material E.
- **It does not establish that any number here matches its source.** All reads are
  search-summary. Search summaries can misattribute, garble or merge figures. For example, one
  summary first attached the 1.34 GPa figure to a 2014 IROS actuator paper; a later search placed
  it in Lauder et al. 2011. Every value needs a full-text check before it is load-bearing.
- **It does not establish what Puri et al.'s EI is normalized to** (whole fin, per ray, per unit
  width). So C2 is illustrative only.
- **It does not establish that bending-derived E and nanoindentation E are comparable.** They
  measure different things at different scales. The ~10–20× gap between them is partly a method
  artefact, and I have not separated the artefact from biology.
- **It does not establish that Lauder et al.'s E accounts for ray segmentation, joints or hollow
  sections.** How I was estimated is not known from the summary.
- **It does not give strength.** That means no fracture, yield, fatigue or toughness value for
  rays. Any claim at the organ scale about a ray surviving a load, such as a glide-landing impact
  or aerodynamic loading in air, has no measured basis from this subproblem.
- **It does not give density for fin-ray bone.** Albacore bone-tissue density is from a different
  bone, a different species and a different ossification type.
- **It does not give anything for actinotrichia.** Their stiffness, strength, density and
  hydration dependence are all unmeasured as far as this search reached. Shark elastoidin is a
  homologous-ish material in a different clade at different dimensions. Generic collagen-fibril
  moduli (0.2–7 GPa) are not actinotrichia data.
- **It does not establish properties in air or when dried.** Every ray value here is from
  hydrated or in-water tests. Rajaram et al. (1981) suggest elastoidin properties shift strongly
  with hydration, and a flying or gliding fin would be partly exposed to air.
- **It does not establish ontogenetic or regional variation in zebrafish.** Bluegill shows a
  30× proximal-to-distal stiffness change. Whether zebrafish rays show the same pattern is not
  known. Puri's non-monotonic EI peak hints that they differ.
- **The negative searches are narrow.** Roughly 25 web searches in total, no direct database
  queries, no full texts. Absence here is weak evidence of absence in the literature.

## 6. What would change the answer

1. **Opening the full texts.** This is the cheapest change, and it needs network access to
   `journals.biologists.com`, `ncbi.nlm.nih.gov`, `ias.ac.in` and `arxiv.org`. It would upgrade
   every read-level, and it would likely add numbers for: Puri et al. 2018 effective E peak;
   Aiello et al. 2018 E; sea-robin 2020 E by direction; Cohen et al. 2012 E, mineral content and
   microhardness; Horton & Summers 2009 yield strength; Rajaram et al. 1981 elastoidin modulus
   and strength; Wang et al. 2002 absolute zebrafish GPa values; larval actinotrichia diameters
   (*J. Exp. Biol.* 215:2359).
2. **A direct measurement on adult zebrafish lepidotrichia**, which would replace the bluegill
   proxy. This means nanoindentation of hemitrich cross-sections, plus micro-bending of isolated
   rays with micro-CT-derived I, plus a calibrated micro-CT TMD (mg HA/cm³) with phantoms.
3. **A tensile or AFM measurement on isolated zebrafish actinotrichia**, wet and dry. This would
   move actinotrichia from `unknown` to `measured`.
4. **A failure test (three-point or cantilever to fracture) on fin rays.** Without it, no
   load-survival claim at the organ scale can be calibrated.
5. **Design-side.** If the organ-scale design relies only on EI, not E, and EI is measured
   directly on the zebrafish fin as Puri et al. did, then the missing material E matters less. In
   that case the gap moves to strength and to how EI scales if ray dimensions are changed.

## Sources (all read at search-summary level; full text could-not-access)

- Lauder GV, Madden PGA, Tangorra JL, Anderson E, Baker TV (2011). Bioinspiration from fish for smart material design and function. *Smart Mater. Struct.* 20:094014.
- Lauder GV, Madden PGA (2007). Fish locomotion: kinematics and hydrodynamics of flexible foil-like fins. *Exp. Fluids* 43:641–653.
- Alben S, Madden PG, Lauder GV (2007). The mechanics of active fin-shape control in ray-finned fishes. *J. R. Soc. Interface* 4:243–256. *(listing only; no modulus obtained)*
- Flammang BE, Alben S, Madden PGA, Lauder GV (2013). Functional morphology of the fin rays of teleost fishes. *J. Morphol.* *(listing only; no modulus obtained)*
- Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018). In vivo quantification of mechanical properties of caudal fins in adult zebrafish. *J. Exp. Biol.* 221:jeb171777.
- Aiello BR et al. (2017). The relationship between pectoral fin ray stiffness and swimming behavior in Labridae. *J. Exp. Biol.* 221:jeb163360.
- Aiello BR, Hardy AR, Cherian C, Olsen AM, Orsbon CP, Hale ME, Westneat MW (2018). A comparison of pectoral fin ray morphology and its impact on fin ray flexural stiffness in labriform swimmers. *J. Morphol.* 279:1031–1044.
- Taft NK et al. (2018). Variation in flexural stiffness of the lepidotrichia within and among the soft fins of yellow perch under different preservation techniques. *J. Morphol.* doi 10.1002/jmor.20831.
- (2020). Walking on chains: the morphology and mechanics behind the fin ray derived limbs of sea-robins. *J. Exp. Biol.* 223:jeb227140.
- Nguyen K, Yu N, Bandi MM, Venkadesan M, Mandre S (2017). Curvature-induced stiffening of a fish fin. *J. R. Soc. Interface*. *(listing only; parameter values not obtained)*
- Horton JM, Summers AP (2009). The material properties of acellular bone in a teleost fish. *J. Exp. Biol.* 212:1413–1420.
- Cohen L, Dean M, Shipov A, Atkins A, Monsonego-Ornan E, Shahar R (2012). Comparison of structural, architectural and mechanical aspects of cellular and acellular bone in two teleost fish. *J. Exp. Biol.* 215:1983–1993.
- Fiedler IAK et al. (2018). Severely impaired bone material quality in Chihuahua zebrafish resembles classical dominant human osteogenesis imperfecta. *J. Bone Miner. Res.*
- Wang XM et al. (2002). Variation of nanomechanical properties of bone by gene mutation in the zebrafish. *Biomaterials* 23:4557–4563.
- (2002). Mechanical properties of skeletal bone in gene-mutated stöpsel^dtl28d and wild-type zebrafish measured by AFM-based nanoindentation. *Bone*, PMID 11934643.
- Tont SA, Pearcy WG, Arnold JS (1977). Bone structure of some marine vertebrates. *Marine Biology*.
- Rajaram A, Sanjeevi R, Ramanathan N (1981). The tensile properties and mode of fracture of elastoidin. *J. Biosci.* 3:303–309.
- Nakagawa H et al. (2021). Mechanical role of actinotrichia in shaping the caudal fin of zebrafish. *Dev. Biol.* 481:52.
- (2012). Structure and function of the median finfold in larval teleosts. *J. Exp. Biol.* 215:2359.

```swarm-result
{"subproblem": "S9", "evidence": "literature",
  "answer": "Teleost fin-ray (lepidotrichia) modulus is reported only from non-zebrafish bending tests (bluegill proximal mean 1.34 GPa, range 0.24-3.7; distal 0.11-0.67 GPa; read at search-summary level), bracketed by fish-bone values of 3.7-8.4 GPa (rib bending) to ~23-25 GPa (zebrafish vertebra nanoindentation); zebrafish fin-ray material modulus, fin-ray strength and density, and every actinotrichia property are unknown.",
  "key_number": "1.34 GPa (bluegill proximal fin-ray Young's modulus, range 0.24-3.7 GPa; not zebrafish)",
  "blocked_on": "Full texts unreachable (network policy blocked journals.biologists.com, ncbi.nlm.nih.gov, ias.ac.in, arxiv.org); no measured zebrafish lepidotrichia E, no fin-ray strength or density, no actinotrichia modulus/strength/density in any teleost found."}
```
