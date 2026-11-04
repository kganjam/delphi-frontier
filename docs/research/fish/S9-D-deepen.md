# S9-D-D: deepening S9-D by attacking its weakest input (hemitrich wall thickness)

Project: `zebrafish-flight` · Scale: tissue · Date: 2026-11-04

Parent chain:
- `S9` (tissue): `docs/research/fish/S9-tissue.md`, branch `origin/claude/s9-fin-ray-materials-t0royp`
- `S9-D`: `docs/research/fish/S9-deepen.md` (+ `S9-deepen_calc.py`), branch `origin/claude/deepen-s9-fin-ray-ixdx5u`

Calculation script: `docs/research/fish/S9-D-deepen_calc.py`. **Every E, I, EI-prediction, ratio and
margin in this file is a calculation** from S9-D's beam models, which I left unchanged. Measured values
are labelled as measured and carry a read-level.

Read-level legend: full-text | abstract | listing | search-summary | could-not-access.

---

## 0. What S9-D concluded

The task prompt's "recorded answer" field was empty. I took S9-D's answer from its own deliverable and
swarm-result block:

1. S9's key number (bluegill fin-ray E = 1.34 GPa) **falls** as an organ-scale input. It is an E = EI/I
   figure whose I was assumed. A bare E is meaningless unless it comes with the I it was derived from.
2. Organ-scale work should instead carry the **measured** zebrafish caudal-fin flexural stiffness,
   EI = 1.5–4×10⁻⁹ N·m² (Puri et al. 2018, full-text). That is ~0.8–2.5×10⁻¹⁰ N·m² per ray (calc).
3. Under the uncoupled-hemitrich model the implied ray E is **~0.6–11 GPa** (calc), and E scales as
   **t⁻³**. S9-D used t = 11–16.5 µm, the wall thickness of wild-type hemirays.
4. Flagged as an inference, not established: even that upper bound sits **below** zebrafish vertebral
   nanoindentation E (~23–25 GPa). So either the joints or fixation add compliance, or tissue E
   cannot be transferred to the rays.

## 1. The input S9-D is most sensitive to, shown by recomputation

Conclusions 1 and 2 are structural. No factor-2 change in any single input moves them: S9-D's
bonded-vs-uncoupled model choice alone spans ~900×. The conclusions that **can** move are 3 and 4.
Those are the numbers a downstream organ model would use if it ever needs E, for example to change
ray dimensions.

I took S9-D's most generous corner: EI/ray = 2.5×10⁻¹⁰ N·m², w = 100 µm, t = 11 µm. There the
flat-plate bound is E_max = 11.3 GPa. That is only **2.04×** below the 23 GPa vertebral floor. I halved
and doubled each input in turn (calc, `S9-D-deepen_calc.py` §1):

| Input | ×0.5 → E_max | Conclusion 4 still holds? | ×2 → E_max | Conclusion 4 still holds? |
|---|---|---|---|---|
| EI (upper, per ray) | 5.6 GPa | yes | 22.5 GPa | yes (barely: 1.02×) |
| ray width w (= D) | 22.5 GPa | yes (barely) | 5.6 GPa | yes |
| **hemitrich wall thickness t** | **90.2 GPa** | **no, flips** | **1.4 GPa** | yes |
| vertebral E reference | 11.3 GPa vs 11.5 GPa floor | yes (barely) | 11.3 GPa | yes |

N (ray count) enters only through EI per ray, so the EI row covers it.

**Result of the recomputation.** t is the only input whose factor-2 error flips a conclusion outright,
because E ∝ t⁻³ turns a 2× error in t into an **8×** error in E. EI and the vertebral-E reference are
both linear, and both sit right at the edge (≈1.0×). They are recorded below as secondary weak points
and listed in `depends_on`. I attack **t**.

## 2. How well was t established in S9-D?

S9-D's t = 11–16.5 µm came from one source: the hox13 triple-mutant paper (*PLoS Genet.* 2026,
doi 10.1371/journal.pgen.1012055, PMC12956070). I re-read it at **full-text** and found three problems
that S9-D did not state:

1. **Resolution.** The methods (full-text) say: "Voxel size was set at 7.1 μm for each scan", on a SkyScan1173.
   A wall of 11–16.5 µm is therefore **1.5–2.3 voxels** thick. *My inference:* a ±1-voxel boundary
   error is ±7 µm, which is ±40–65% of t. Through t⁻³ that becomes roughly a factor of 0.2–4 in E. The
   measurement has the right sign and order of magnitude, but it cannot fix t to within a factor of 2.
   I have not determined the direction of any partial-volume bias.
2. **Contrast.** The samples were "stained in 1% iodine solution in 99% EtOH overnight" (full-text). Iodine
   is a soft-tissue contrast agent, so the bone-to-soft-tissue boundary in these scans is not a pure
   mineral boundary. The authors do not describe a segmentation threshold, as far as I found.
3. **Wrong fin, wrong position, n = 3.** The measurement is in the **dorsal** fin, 500–1000 µm from the
   ray base, in fish of SL 3.2 cm, with n = 3 per group. Puri's EI is from the **caudal** fin at
   1–6.5 mm from the fixation. The authors' own text does confirm that the plotted "hemiray width" is
   bone thickness ("to compare the thickness of the bone", full-text). That point of S9-D stands.

The values themselves are S9-D's readings off a bar chart, not tabulated numbers.

**Evidence level of t as S9-D used it:** measured in zebrafish, but at a resolution comparable to the
quantity, in a different fin, and read off a plot. It is a **proxy with resolution-limited precision**,
not a caudal-fin measurement.

## 3. Improving it: a caudal-fin hemiray bone thickness at finer resolution

**Found.** Azevedo AS, Grotek B, Jacinto A, Weidinger G, Saúde L (2011). "The regenerative capacity of
the zebrafish caudal fin is not affected by repeated amputations." *PLoS One* 6:e22820.
doi 10.1371/journal.pone.0022820, PMC3145768. Read-level: **full-text** for text and methods, and the
**figure image read** for Fig. 4.

Method, as stated by the authors (full-text):
- Transverse **12 µm cryosections** of caudal fins, Zns5-immunostained, imaged by **confocal
  microscopy**. Image analysis in ImageJ.
- "proximal and distal bone thickness of dorsal and ventral hemi-rays of 5–9 bony rays was measured".
- **2 uncut control fins**, AB wild-type fish. Fish entered the protocol at 1 year of age and the study
  ran ~11 months, so I infer the uncut controls were roughly 2 years old.

Values are **my pixel readings** of the uncut bars in Fig. 4L/M, ±~0.5 µm. The axis ticks were
calibrated in the image. These are not tabulated numbers:

| Region (uncut caudal fin) | Hemiray bone thickness t | Error bar (type not stated) |
|---|---|---|
| Proximal ("old bone" region) | **~20.4 µm** | +~4.9 µm |
| Distal ("new bone" region) | **~19.0 µm** | +~2.7 µm |

I also read the uncut geometry from Fig. 4N–Q: intra-ray (between-hemiray) space was ~85 µm proximal and
~63 µm distal. Fin thickness was ~125 µm proximal and ~104 µm distal. **Consistency check (calc):**
2t + intra-ray space = 126 µm and 101 µm. That matches the separately plotted fin thickness to within
3 µm, so the bars are internally consistent. The fin thickness also falls inside Puri's calliper range
of 200→40 µm (full-text). Fig. 4I shows deep crescent ("( )") hemirays, which agrees with S9-D.

The authors also claim (full-text) that repeated amputation thickens old bone significantly
(to ~37 µm proximally in Fig. 4L). Only the **uncut** bars are used here.

**What this improves over S9-D's input:**
- the right fin (caudal, the same fin Puri bent);
- a resolution finer than the quantity: an optical section, not 7.1 µm voxels;
- an independent lab and method;
- dorsal and ventral hemirays measured separately, across 5–9 rays.

**What it does not fix (caveats, kept):**
- **n = 2 fish.** The error-bar type (SD or SEM) is not stated in the legend or the methods as far as I
  found.
- **Section obliquity.** A transverse section cut off-perpendicular inflates the apparent wall by
  1/cos θ, for example +15% at 30°. *Inference:* any such bias makes true t **smaller** and E larger.
- **Age.** The controls were ~2 yr old; Puri's fish were 6–12 months (full-text). The authors of a
  review (Marí-Beffa & Murciano 2010, *Dev. Dyn.*, PMC3036817, full-text) state that "lepidotrichia
  thickness also grows gradually" during development and regeneration. *Inference:* Puri's younger fish
  may have thinner walls, which also pushes E up. I found no number for the size of this effect.
- **Position.** "Proximal" and "distal" here mean the regions on either side of an amputation plane ~6
  segments from the fin base, **not** the fin tip. Puri's fin thickness tapers to 40 µm distally, so t
  near the tip is probably smaller than 19 µm. That is my inference, and it is **unmeasured**.

**Disagreement preserved, not averaged.** For a wild-type zebrafish hemiray wall:
- dorsal fin, micro-CT at 7.1 µm voxels, 3.2 cm SL: 11–16.5 µm (S9-D's reading of hox13 Fig. 7E);
- caudal fin, confocal on cryosections, ~2-yr-old AB: 19–20.4 µm (my reading of Azevedo Fig. 4L/M).

The caudal values are 1.2–1.9× thicker. I cannot separate fin identity, age, method and resolution as
causes.

**Negative search, scope stated.**
- *Europe PMC:* ~6 queries on zebrafish + (hemiray | hemitrich | lepidotrichia) + (thickness | width |
  cross section). ~150 titles screened. Full text grepped for thickness-with-µm statements in 18
  open-access papers: PMC9946992, PMC9259016, PMC7782361, PMC6971026, PMC3036817, PMC7432380,
  PMC11264301, PMC11642618, PMC13120675, PMC5722281, PMC7872341, PMC9110718, PMC13643786, PMC5805328,
  PMC5171864, PMC13018208, PMC12956070 and PMC3145768. PMC8918783 returned no XML.
- *Web searches:* 2, extended mode.
- *Result:* PMC3145768 is the only source found that gives a **numerical** caudal-fin hemiray bone
  thickness. Cardeira et al. 2016 (PMC5171864) scanned caudal fins by micro-CT at a **3 µm voxel**
  (full-text), but they report BMD and volume, not wall thickness. Marí-Beffa & Murciano 2010
  (PMC3036817) define "lepidotrichia thickness" in a figure but give no number in the text. Becerra
  et al. 1983 and Montes et al. 1982 (histology, *Cell Tissue Res.* and *Histochemistry*) were read at
  **abstract** only, and neither abstract gives a thickness.
- *Not searched:* Scopus, Web of Science, paywalled full texts, Murciano et al. 2007/2018 full texts,
  and thesis repositories.
- **No hemitrich thickness measured on the same fish that were bending-tested exists, as far as this
  search reached.**

**What would settle t, and the cost.** These are my estimates, not quoted prices, and they repeat
S9-D's item 1 with a sharper specification. Scan the bending-tested caudal fins at **≤2 µm voxel**, for
example on a SkyScan 1272-class instrument, which Cardeira et al. ran at 3 µm. Use an
unstained/ethanol-fixed or phosphotungstic-acid protocol and report the bone threshold. That would give
t to within ~10% at each of Puri's deflection positions, so E to within ~±30% given t⁻³. Cost: of order
USD 2–5k and 1–2 instrument days for 5–10 fins, plus the Puri-type rig time. Cryosection histology on
the same fins after testing is cheaper (<USD 1k, estimate) but destructive, and it carries the
obliquity bias above.

## 4. Recompute S9-D's conclusions with the improved input

Same models, same EI, same D = 100–200 µm. Only t changes (calc, `S9-D-deepen_calc.py` §2):

| t used | Uncoupled flat-plate E envelope | At D = 150 µm | Margin below 23 GPa |
|---|---|---|---|
| S9-D: 11–16.5 µm (dorsal, micro-CT) | 0.56 – 11.3 GPa | 0.74 – 7.5 GPa | ≥ 2.0× |
| **Caudal means: 19.0–20.4 µm (Azevedo)** | **0.29 – 2.2 GPa** | **0.39 – 1.46 GPa** | **≥ 10.5×** |
| Caudal mean ± bar: 16.3–25.3 µm | 0.15 – 3.5 GPa | 0.21 – 2.3 GPa | ≥ 6.6× |

- The E ratio between the inputs (calc) is (t_caudal / t_dorsal)³ = 1.9–5.2×. The upper end of S9-D's
  E range was **too high by ~5×**.
- The flat-plate model would need tissue-level E (≥23 GPa) only if t < **8.7 µm** (calc). That is
  about half of every caudal reading.
- **Forward check (calc).** Take tissue E = 23 GPa and caudal t = 16.3–25.3 µm, with uncoupled flat
  plates and 17 rays. That predicts a whole-fin EI of 2.8×10⁻⁸ – 2.1×10⁻⁷ N·m². This is **7–141× stiffer
  than Puri measured**, and it is the most compliant beam geometry in S9-D's set. Curved crescents
  would raise I and widen the gap further.
- A coincidence I note and do not use: at D = 150 µm the recomputed flat-plate E (0.39–1.46 GPa)
  brackets the bluegill 1.34 GPa. This does **not** rescue S9's key number. The coincidence holds only
  under one assumed I, which is exactly the objection S9-D raised.

What happens to each S9-D conclusion:

1. **"S9's 1.34 GPa falls; a bare E is not a usable input." This stands.** It is structural and
   unaffected by t.
2. **"Carry the measured EI = 1.5–4×10⁻⁹ N·m²." This stands, and is strengthened.** With the measured
   caudal t, no beam model in S9-D's set reproduces the in-vivo EI from tissue-level E. The miss is
   ≥7×, where the margin with S9-D's own t was 2×. A modeller who builds the ray from bone E and
   geometry would now overpredict fin stiffness by about an order of magnitude. Carrying the measured
   EI directly is therefore the only route consistent with the data.
3. **"Implied E ~0.6–11 GPa, ∝ t⁻³." The t⁻³ scaling stands. The range is revised to ~0.15–3.5 GPa**
   (caudal t ± bar), or 0.29–2.2 GPa (caudal means). The upper bound drops ~3–5×.
4. **"Tissue E cannot be transferred; extra compliance exists (joints, fixation, coupling)." This
   strengthens,** from a 2× margin that a factor-2 error in t could erase to a ≥6.6–10.5× margin that
   only a t < 8.7 µm could erase. This remains **an inference from calculation, not an observation**:
   - I have not separated which compliance source is responsible.
   - The 23–25 GPa reference is still vertebral, not fin-ray, and still search-summary.
   - If lepidotrichia E were far below vertebral E (S9's L9 hints at lower mineralization), part of the
     gap would be material, not structural. That too would mean vertebral E cannot be used for rays,
     so the practical conclusion is unchanged.

**Verdict on S9-D: STRENGTHENS.** The headline conclusion holds under the improved input and becomes
harder to overturn. The secondary E range is corrected downward, and that correction is part of this
deliverable.

**Unchanged and not re-searched.** No fin-ray strength, no fin-ray density, and no actinotrichia
property. S9's negative-search scope still applies to all three.

## 5. Remaining weak points (each is a `depends_on` edge)

- **Puri EI** is a single study, in vivo, n = 5 fish, with foam-pad fixation. A factor-2 error in EI
  alone no longer flips conclusion 4: the margin is now ≥6.6×.
- **Vertebral E 23–25 GPa** is search-summary only and from a different bone. A factor-2 error alone
  no longer flips conclusion 4.
- **Uncoupled-hemitrich model** rests on Das, Hannard & Barthelat 2023 (rainbow trout, *Acta
  Biomater.*, PMID 37364788, **abstract**). If the hemitrichs were bonded, E would fall a further
  ~170–300× (S9-D). That makes conclusion 4 stronger, not weaker.
- **t transfer across age and position**: §3 caveats. If t were ≤8.7 µm at Puri's positions,
  conclusion 4 would fall.

## Sources

- Azevedo AS, Grotek B, Jacinto A, Weidinger G, Saúde L (2011). The regenerative capacity of the
  zebrafish caudal fin is not affected by repeated amputations. *PLoS One* 6:e22820. PMC3145768.
  **full-text** (text and methods), **figure image read** (Fig. 4L–Q, my pixel readings).
- hox13 triple-mutant paper (2026). *PLoS Genet.* doi 10.1371/journal.pgen.1012055, PMC12956070.
  **full-text** (methods: 7.1 µm voxel, iodine stain, n = 3; results: "thickness of the bone").
- Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018). *J. Exp. Biol.* 221:jeb171777.
  PMC5868929. **full-text** (age 6–12 months, AB; fin thickness 200→40 µm; EI 1.5–4×10⁻⁹ N·m²).
- Marí-Beffa M, Murciano C (2010). Dermoskeleton morphogenesis in zebrafish fins. *Dev. Dyn.*
  PMC3036817. **full-text** (qualitative statement only).
- Cardeira J et al. (2016). *Sci. Rep.* 6:39191. PMC5171864. **full-text** (3 µm-voxel micro-CT
  method; no wall thickness).
- Becerra J, Montes GS, Bexiga SR, Junqueira LC (1983). *Cell Tissue Res.* 230:127. **abstract.**
- Montes GS et al. (1982). *Histochemistry* 75:363. **abstract.**
- Das S, Hannard F, Barthelat F (2023). *Acta Biomater.* PMID 37364788. **abstract** (via S9-D; not
  re-read).
- Fiedler et al. (2018) and the glucocorticoid study, zebrafish vertebral nanoindentation.
  **search-summary** (via S9; not re-read).

```swarm-result
{"subproblem": "S9-D-D", "evidence": "literature (caudal-fin hemiray thickness: Azevedo 2011 full-text + figure read by me; Puri 2018 full-text; hox13 2026 full-text; vertebral E still search-summary; trout coupling claim abstract)",
  "answer": "S9-D's most sensitive input is hemitrich wall thickness t (E ~ t^-3; a factor-2 error flips its 'tissue E cannot reproduce in-vivo EI' conclusion), and replacing its 7.1-um-voxel dorsal-fin value (11-16.5 um) with a confocal caudal-fin measurement (~19-20.4 um, n=2 fish) lowers the implied uncoupled-plate ray modulus to ~0.15-3.5 GPa, leaving tissue-level E (>=23 GPa) 7-141x too stiff to reproduce Puri's measured fin EI, so S9-D's conclusion to carry measured EI rather than any E stands and becomes harder to overturn.",
  "key_number": "zebrafish caudal-fin hemiray bone thickness t ~ 20.4 um proximal, ~19.0 um distal (uncut adults, confocal on 12-um cryosections, Azevedo et al. 2011 Fig 4L/M, read off plot +-0.5 um; error bars +4.9/+2.7 um, type unstated)",
  "verdict": "strengthens",
  "depends_on": [
    "S9-D conclusion: S9 key number 1.34 GPa falls; carry measured EI instead",
    "S9-D models: uncoupled flat-plate / crescent / bonded-tube / solid-rod I formulas (S9-deepen_calc.py)",
    "measured: zebrafish caudal fin EI = 1.5-4e-9 N m^2 in vivo (Puri et al. 2018, PMC5868929, full-text)",
    "measured: 16-18 caudal fin rays (Puri et al. 2018, full-text)",
    "measured: ray diameter 0.1-0.2 mm and fin thickness 200->40 um (Puri et al. 2018, full-text)",
    "assumption: line load shared equally across rays (supported by Puri interray-cut result, full-text)",
    "measured: caudal hemiray bone thickness ~20.4 um proximal / ~19.0 um distal, n=2 fish (Azevedo et al. 2011, PMC3145768, figure read)",
    "measured: dorsal hemiray thickness 11-16.5 um at 7.1 um voxel, n=3 (hox13 PLoS Genet 2026, PMC12956070, full-text; plot read by S9-D)",
    "assumption: caudal t from ~2-yr-old fish at mid-fin transfers to Puri's 6-12-month fish at 1-6.5 mm",
    "claim: hemitrichs bend uncoupled, core 3-4 orders more compliant (Das, Hannard & Barthelat 2023, PMID 37364788, abstract; rainbow trout)",
    "search-summary: zebrafish vertebral nanoindentation E ~23-25 GPa (Fiedler 2018 and one other, via S9 B3/B4)",
    "law: Euler-Bernoulli linear-elastic beam bending, EI = E*I",
    "negative search: no hemitrich thickness measured on bending-tested fins (Europe PMC ~6 queries, 18 full texts grepped, 2 web searches)"
  ]}
```
