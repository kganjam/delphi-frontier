# S13-D-D — Deepening S13-D: the ray-modulus baseline under the feasibility negative

**Project:** `zebrafish-flight` · **Scale:** protein · **Subproblem:** S13-D-D (deepening of S13-D)
**Date of work:** 2026-11-04 · **Author:** Claude Code (automated research agent)

**Parents, read in full:**
- `docs/research/fish/S13-protein.md` and `s13_arith.py`, branch `claude/s13-protein-fin-ray-e8y8d8`.
- `docs/research/fish/S13-deepen.md` and `s13d_sensitivity.py`, branch
  `claude/deepen-s13-fin-ray-xfsos0` @ `4024bdc8`. This is the S13-D record.

**Siblings used, read in the parts cited:**
- `challenge-175.md`, branch `claude/challenge-175-fin-ray-modulus-jgup79`.
- `challenge-97.md`, branch `claude/challenge-97-fish-ray-ei-uded9g`.
- `challenge-181.md`, branch `claude/challenge-181-actinotrichia-modulus-4opo02`.

**Script:** `docs/research/fish/S13-D-D-deepen_calc.py`. Running
`python3 -I docs/research/fish/S13-D-D-deepen_calc.py` from the repo root reproduces every number
in §1 and §4.

> Read-level key: `full-text` | `abstract` | `listing` | `search-summary` | `could-not-access`.
>
> Nothing here is an observation I made. Each number has one of four origins, and the sentence
> that uses it says which:
> - (a) **measured by cited authors**
> - (b) **calculated by me**
> - (c) **calculated by a sibling agent**
> - (d) **assumed**

---

## 0. What S13-D concluded, and which part is attacked here

S13-D reached two verdicts:

1. **The recorded justification for the regime transition was false.** The recorded line said
   0.0% of residues are above pLDDT 70. The AlphaFold DB v6 record gives 27.6% (And1, E7F5V5) and
   26.8% (And2, A9JRX1). The transition `R-protein-fold → R-material-assembly` was still correct,
   for a different reason: pLDDT is not a modulus, and the load-bearing object is an assembly.
   I do not re-attack this. It rests on a database read that S13-D reproduced from two hosts, and
   no number in it is near a threshold.
2. **The feasibility negative STANDS.** A stiffer protein cannot close the 245–654× flexural-rigidity
   gap. S13-D tested this against one input only, the tip-deflection tolerance.

Verdict 2 is the one with an unattacked weak input. That input is **the ray-material baseline
modulus `E_base`**. S13 multiplies the EI gap by `E_base` to get the modulus a protein-only route
would need, and then compares that number with a 10–30 GPa ceiling for protein solids. S13 took
`E_base` ≈ 1 GPa, which it called a "teleost whole-ray" modulus with read-level `search-summary`.
S13 named this input itself as the one that "could flip the answer" (§6.1 of S13), and so did
S13-D (§5.4, §6.3). Neither of them improved it.

---

## 1. Sensitivity, recomputed rather than asserted

The feasibility margin is `M = (EI_req/EI_meas) · E_base / E_ceiling`. A margin `M > 1` means the
required modulus is above the protein ceiling, so the negative holds. The values below were
calculated by me with the script, §1–2. I used S13's own model:

- a cantilever under a uniformly distributed load
- m = 0.4 g
- semi-span 2 cm
- tip-deflection tolerance 10%

| Input | Factor-of-two move | Margin (least favourable EI_meas = 4×10⁻⁹) |
|---|---|---|
| none (as recorded) | — | **8.2** (21.8 at EI_meas = 1.5×10⁻⁹) |
| `E_base` | ×0.5 | 4.1 |
| `E_ceiling` | ×2 | 4.1 |
| `EI_meas` | ×2 | 4.1 |
| tolerance | ×2 (20%) | 4.1 |
| semi-span | ×0.5 | 2.0 (EI_req ∝ L²) |
| mass | ×0.5 | 4.1 |

**No single input flips the conclusion at ×2.** All six moved together in the unfavourable direction
give M = 0.064, which is a flip. So the instruction's test ("a factor-of-two error changes the
conclusion") is not met by any one input. I report that plainly rather than force a candidate.

The input that matters is the one whose *actual uncertainty* is wider than the margin. Each input
except `E_base` carries roughly a factor of 2–3 of uncertainty. `E_base` carries more than three
orders of magnitude, because it depends on which cross-section model is used to turn the same
measured EI into a modulus:

- **Puri's EI divided by Puri's own effective I:** 2.1–13.3 MPa (calculated by me, §3). Puri's
  inputs are I_eff = 3–7×10⁻¹⁶ m⁴ and EI = 1.5–4×10⁻⁹ N·m², both full-text via S13.
- **Challenge-175 cross-section models:**
  - solid rod: 3.35–10.1 MPa
  - uncoupled flat hemitrich plates: 0.56–11.3 GPa
  - envelope over all models: ~11 MPa to ~11 GPa
  - (calculated by a sibling agent; not re-run here)
- **S13's own value:** ~1 GPa, `search-summary`. Challenge-175 shows that its I definition is
  `unknown`.

The flip threshold is `E_base* = 46–122 MPa` (calculated by me). **That threshold lies inside the
plausible range of `E_base`.** If `E_base` is at the solid-rod value (~5 MPa), the required modulus
falls to ~1–3 GPa, which is well inside the protein range, and S13's ceiling argument fails. This is
exactly the scenario S13 §6.1 flagged. **`E_base` is the most sensitive input in the sense that
counts: it is the only one whose credible range crosses the flip line.**

## 2. How well `E_base` is established

**Evidence level: `proxy`. Read-level: `search-summary`.**

- The 1 GPa (more precisely 1.34 GPa, with a 0.24–3.7 GPa range) comes from a whole-ray bending
  test on a larger teleost. The source is Lauder et al. 2011, reached only through search summaries
  (S13 §2.2; and the search I ran today returned the same snippet).
- It is a *structural* modulus, EI/I, with an I that is `unknown` (challenge-175 §4).
- It is not zebrafish, and it is not a tissue measurement.

The S13 chain uses it as though it were the *material* modulus of the ray, and that is a category
error. My inference, stated separately: a materials route changes the modulus of the material.
The quantity that has to be multiplied is therefore the **tissue** modulus, not any
geometry-contaminated EI/I. The MPa values in §1 are effective moduli of a jointed, two-part
structure. They carry the same category error in the other direction. Taking them as the material
baseline would "flip" the answer for the wrong reason.

## 3. Improving the input: the primary measurement

**Bohns FR, Shih Y-R, Chuang Y-J, Akhtar R, Chen P-Y (2020/21).** "Influence of Prednisolone and
Alendronate on the de novo Mineralization of Zebrafish Caudal Fin." *JBMR Plus*,
doi:10.1002/jbm4.10435, PMC7872341, PMID 33615104. **Read-level: `full-text`.** I retrieved the
Europe PMC `fullTextXML` (HTTP 200) on 2026-11-04 and read the Methods and Results on mechanics.

What the authors measured (author's claims):

| Item | Value (as stated) |
|---|---|
| Animals | adult wild-type AB, 3 months old, length 30.73 ± 4.32 mm |
| Method | Berkovich nanoindentation, Bruker TI 980, 100 nm depth, 5/5/5 s load/hold/unload |
| Site | "the central point of the hemi rays of the third dorsal lepidotrichia", ~26 indents proximal and ~20 distal |
| Prep | OCT cryosections cut at −21 °C; excess OCT washed off with PBS. **The hydration state during indentation is not stated.** |
| Quantity | **reduced modulus E_r**, not Young's modulus |
| E_r, proximal, lowest group (CTRL_REGEN, regenerated untreated) | **4.57 ± 2.62 GPa** |
| E_r, proximal, highest group (ALN_REGEN), which the authors say matches the "pre-amputation condition" | **8.68 ± 8.74 GPa** |
| E_r, prednisolone-treated | 5.60 ± 5.04 GPa |
| E_r, untreated pre-amputation (CTRL) | **in Fig. 5B only. No number in the text, so `unknown` as a number.** |
| Sample size behind each E_r | n = 2 fins were sectioned per group, and one of them was used for mechanics. **That is one fin per group.** |
| Authors' caveat | high SDs "may be related to the impossibility to perform finishing procedures on sectioned samples" |
| Distal E_r | lower than proximal, per the authors. Values are in the figure only (`unknown` as numbers) |

**My conversion (calculated, with an assumed ν = 0.3):** E = (1 − ν²)·E_r gives **4.2–7.9 GPa**.
I neglected the diamond-tip compliance term. That correction moves E by a few percent at most at
these moduli.

**Agreement and disagreement with other sources:**
- The value sits inside the 4–20 GPa "bone" range that fin-mechanics models assume. That range
  appears in arXiv:1608.05891 (search-summary) and is cited in S13 §2.2.
- It is 3–8× above S13's 1 GPa proxy and ~400–4000× above the solid-rod effective modulus.
- The sources do not disagree about the material. They disagree because they measure different
  things: tissue versus structure.

**How good the improved input is, honestly:**
- It is a **measured** tissue modulus of the right tissue in the right species. That is better
  than anything in the S13 chain.
- Its limits:
  - one fin per group
  - SDs of 57–100% of the mean
  - unpolished sections
  - unstated hydration state
  - the untreated adult value is readable only from a figure
- Dry testing typically raises indentation modulus relative to wet testing. That is my inference,
  not something this paper measured. If the sections were tested dry, the wet modulus is lower.
  §4 shows the conclusion survives even a 10× lower value.

## 4. Recomputing the conclusion with the improved input

All calculated by me (script §4–6).

**4.1 Ceiling leg (pure-material route).** Use E_base = 4.2–7.9 GPa:

- required modulus = **1.0–5.2 TPa**
- margin over the 30 GPa protein ceiling = **34–172×** (it was 8–22× with the 1 GPa proxy)
- the requirement is above diamond-class stiffness

Even S13-D's most lenient corner (80% tip deflection) still needs **127 GPa**, a margin of 4.2×,
where S13-D had found it touching 31 GPa. The flip threshold is 46–122 MPa, so the measured tissue
modulus would have to be overestimated **~35–170×** before this leg fails.

**4.2 What the tissue modulus reveals.** Dividing the measured fin EI by the measured tissue E
gives the structural I that each ray actually delivers: **1.1–6.0×10⁻²⁰ m⁴ per ray** (calculated
by me, 16–18 rays). Compare challenge-175's geometric integrals at D = 150 µm and t = 15 µm
(calculated by a sibling):

- **Uncoupled flat hemitrich plates, 8.4×10⁻²⁰.** The real fin is at or *below* the
  fully-uncoupled bound, by 1.4–8×.
- **Bonded tube, 1.47×10⁻¹⁷.** Full coupling would give **245–1393×** headroom.
- **Solid rod, 2.49×10⁻¹⁷.** **414–2360×** headroom.

My inference, stated separately: the zebrafish fin is soft because its two hemitrichs bend almost
independently, and probably also because of segment-joint compliance. Its bone is not soft. This
**strengthens** S13's second leg ("architecture-limited, not molecule-limited") with a measured
tissue number. Before, that leg rested only on search-summary collagen-fibril data.

**4.3 A route the S13 chain did not price, and its measured lever.** The coupling between hemitrichs
is made of protein: collagen fibres that let the hemitrichs slide past each other. So "stiffen the
protein that couples the hemitrichs" is a protein-level route, and S13's "at most ~10×" cap does
not obviously apply to it. That cap was derived from the molecule→fibril ratio.

- **Geometric ceiling of this route (calculated by me, §4.2):** 245–2360×. On paper it is enough.
- **Measured lever:** preventing hemitrich sliding in excised sunfish rays raised stiffness
  "nearly 12 times". Read-level: `search-summary`, from the PMC11285607 / Barthelat-group
  morphing-beam literature. This is the same 12× that challenge-97 carries as a clamping factor.
  It was obtained by mechanically **clamping** the hemitrichs, which is an upper bound for any
  biological coupling, not by changing a protein.
- **Residual gap after a full 12× (calculated by me):** **20–54×**. That is still well short.

**My inference about why** the measured 12× is far below the 245×+ geometric ceiling: segmented
joints and finite core shear stiffness cap realised coupling. This is unmeasured in zebrafish.

## 5. Verdict: STRENGTHENS

- **Ceiling leg:** the margin rises from 8–22× to **34–172×** once the search-summary 1 GPa proxy is
  replaced by a full-text, measured zebrafish hemiray tissue modulus (E_r 4.57–8.68 GPa).
- **Architecture leg:** this leg is now quantified from measured inputs. The rays deliver 1.1–6×10⁻²⁰
  m⁴ per ray, at or below an uncoupled-plate bound, against 245–2360× more available from full
  coupling.
- **New qualification.** A protein route via hemitrich coupling exists, and S13 did not price it.
  Its only measured lever (~12×, clamping, sunfish, search-summary) leaves a 20–54× gap. It
  therefore **does not rescue** the protein route. It does replace S13's derived "~10× cap" with a
  mechanism-specific, measured ~12× ceiling.

## 6. What this does NOT establish

1. **Untreated adult tissue modulus as a number.** It is in Bohns Fig. 5B only. I used the range
   spanned by the regenerated-control and alendronate groups, which the authors say brackets
   pre-amputation values.
2. **Wet tissue modulus.** The hydration state is unstated. This does not threaten the conclusion
   unless the error is ≳35×.
3. **Coupling stiffness of zebrafish hemitrichs.** The 12× is sunfish, excised, clamped, and at
   search-summary level. A zebrafish value is `unknown`.
4. **Model inputs are inherited unchanged from S13:** mass, semi-span, tolerance and load model.
   Challenge-181 uses a 4 cm span for the same problem, which would raise EI_req 4× and strengthen
   this result further. I preserve that disagreement rather than choose between the two.
5. **No protein design, structure prediction or stability calculation was run.** Every protein
   number is inherited.
6. **Negative-search scope.** I searched for a measured *Young's* modulus of unperturbed adult
   zebrafish lepidotrichia with two standard-mode web searches (2026-11-04) and found only Bohns
   et al. (reduced modulus). I also saw a National Tsing Hua University thesis listing (read-level
   `listing`; values not read), which reports a proximal→distal decline in E_r. I did not search
   Web of Science or Scholar, or CNKI and other non-English databases. A third search, for the
   composition of segment-joint ligaments, found descriptions of a "fibrous joint" (search-summary)
   and no modulus.

## 7. What would settle what remains, and the cost

- **Hydrated, polished nanoindentation of untreated adult zebrafish hemirays (≥5 fish).** Cost:
  a few instrument days. Do it in the same fish as a Puri-type in-vivo EI and a micro-CT of the
  cross-section. That would give E_tissue × I_geometric versus EI_measured directly, and so the
  coupling efficiency.
- **Hemitrich clamping test on zebrafish rays** (the zebrafish analogue of the sunfish 12×). Cost:
  a microbeam rig. This is the number that bounds any coupling-protein route.

---

## Provenance

- Reachable today: `www.ebi.ac.uk/europepmc` (HTTP 200, Bohns full text) and web search.
- Every number is reproducible from `S13-D-D-deepen_calc.py` or quoted with its source.
- No number, citation, gene symbol, allele or accession was invented. Values I could not read are
  marked `unknown`.

```swarm-result
{"subproblem": "S13-D-D", "evidence": "derived",
  "answer": "The feasibility negative strengthens: replacing S13's search-summary ~1 GPa whole-ray proxy with the measured zebrafish hemiray tissue modulus (Bohns et al. 2020 nanoindentation, E_r 4.57-8.68 GPa, ~4.2-7.9 GPa Young's with nu=0.3 assumed) raises the modulus a pure-protein route would need to 1.0-5.2 TPa (34-172x above the 30 GPa protein ceiling, previously 8-22x) and shows the fin is soft because its hemitrichs are nearly uncoupled, not because its bone is soft; the one protein-level route this exposes, stiffening hemitrich coupling, has a measured lever of only ~12x (sunfish clamping, search-summary), leaving a 20-54x gap.",
  "key_number": "zebrafish caudal-fin hemiray tissue reduced modulus E_r = 4.57-8.68 GPa (Bohns et al. 2020 JBMR Plus PMC7872341, Berkovich nanoindentation, one fin per group, SD 57-100%) replacing the ~1 GPa whole-ray proxy",
  "verdict": "strengthens",
  "depends_on": [
    "S13 feasibility model: cantilever UDL, m=0.4 g, semi-span 2 cm, tip deflection 10% (assumed, S13-protein.md s3.2)",
    "Puri et al. 2018 JEB 221:jeb171777 whole caudal fin EI 1.5-4e-9 N m^2, I_eff 3-7e-16 m^4, 16-18 rays (full-text via S13 and challenge-175)",
    "Bohns et al. 2020 JBMR Plus doi:10.1002/jbm4.10435 hemiray reduced modulus 4.57-8.68 GPa, n=1 fin per group, hydration unstated (full-text)",
    "Poisson ratio 0.3 for E_r to E conversion (assumed)",
    "protein-solid modulus ceiling 10-30 GPa, amyloid fibril (search-summary via S13)",
    "S13 whole-ray proxy ~1 GPa / Lauder et al. 2011 1.34 GPa (search-summary), replaced here",
    "challenge-175 cross-section I integrals at D=150 um t=15 um: flat plates 8.44e-20, bonded tube 1.47e-17, solid rod 2.49e-17 m^4 (calc by sibling)",
    "sunfish hemitrich clamping raises ray stiffness ~12x (search-summary, PMC11285607 / Barthelat-group literature)",
    "S13-D deflection-tolerance sensitivity table 5-80% (calc, S13-deepen.md s4.2)",
    "S13-D pLDDT correction 26.8-27.6% above pLDDT 70 (AlphaFold DB v6; not re-attacked here)"
  ]}
```
