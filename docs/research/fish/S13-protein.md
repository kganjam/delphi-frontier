# S13 — Can a stiffer structural protein variant be designed for the fin ray?

**Project:** `zebrafish-flight` · **Scale:** protein · **Subproblem:** S13
**Date of work:** 2026-11-04 · **Author:** Claude Code (automated research agent)

> Read-level key, used on every source below:
> `full-text` | `abstract` | `listing` | `search-summary` | `could-not-access`
>
> Every number in §3 is **computed by me**, not observed. Every number in §2 is
> quoted from a source. The AlphaFold numbers in §2.5 are the output of a
> **structure prediction**, not a measurement, and are labelled as such in every
> sentence that uses them.

---

## 1. The question, restated precisely

S6 (geometric route to fin-ray stiffness) is the sibling subproblem. **I could not
read S6's result**: at the time of writing there is no `docs/research/fish/`
directory in this repository and no S6 artefact anywhere in it (`git ls-files`
listed no fish/fin research file, and a repo-wide `grep -rI '\bS6\b'` at commit
`3272d3e` matched only this file). So I cannot condition
on "S6 fails on stiffness". I instead derive the stiffness target independently,
in §3, and state the answer as a function of it.

Restated with the numbers that make it hard:

- *Danio rerio* adult: body length ~4 cm, mass ~0.4 g → weight **3.92 mN**
  (computed, §3.1).
- The measured flexural rigidity of a whole adult zebrafish caudal fin is
  **1.5–4 × 10⁻⁹ N·m²** (Puri et al. 2018, measured in vivo; §2.1).
- A cantilever spar that holds a 0.4 g body in a 4.5 m/s glide to a 10% tip
  deflection needs **EI ≈ 1.0 × 10⁻⁶ N·m²** (computed, §3.2).
- That is a **245×–654×** shortfall in flexural rigidity (computed, §3.3).

The protein question is therefore sharp, and it is *not* "can a collagen be made
stiffer at all". It is: **can a redesigned structural protein supply a factor of
~250–650 in the material term `E` of `EI`?** Because `EI = E · I`, a pure-materials
route must find all of that factor in `E`. The relevant ceiling is whatever the
stiffest protein-based solid actually measures at (§2.4).

A second, separate question hides inside the first, and the honesty floor requires
me to split them: **protein design tools predict thermodynamic/thermal stability
(ΔΔG, Tm), not Young's modulus.** A successful stability design is not a
successful stiffness design. §4 answers both.

---

## 2. What is measured

### 2.1 Zebrafish fin mechanics — the only in-vivo numbers at the right scale

Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018). "In vivo
quantification of mechanical properties of caudal fins in adult zebrafish."
*J Exp Biol* 221(4): jeb171777. doi:10.1242/jeb.171777.
**Read-level: full-text** (PMC5868929, fetched 2026-11-04).

| Quantity (authors' measurement) | Value |
|---|---|
| Bending stiffness `EI`, caudal fin, 6 positions along proximal–distal axis | **1.5 × 10⁻⁹ – 4 × 10⁻⁹ N·m²** |
| Same, authors' extrapolated estimate in Conclusions | 2 × 10⁻⁹ – 5 × 10⁻⁹ N·m² |
| Effective area moment of inertia `I_eff` | **7 × 10⁻¹⁶ → 3 × 10⁻¹⁶ m⁴** (decreasing distally) |
| Fin thickness along axis | 200 → 40 µm |
| Fin width | ~5 → 8 mm |
| Individual ray diameter | **0.1–0.2 mm** |
| Rays per caudal fin | 16–18 |
| Interray tissue effective tensional modulus | **4 ± 2 kPa** (authors call this an upper bound) |
| Interray spring constant, intact / cut | 0.4 ± 0.1 / 0.08 ± 0.04 N·m⁻¹ |
| Animals | 5 adult wild-type AB, 6–12 months |
| Stated accuracy | "at least 10%" |

**Authors' claim:** removing interray tissue did not measurably change bending
stiffness, so "fin flexibility depends mainly on the rays' mechanical
properties." **My inference, separately:** this makes the rays the only legitimate
target for a materials intervention, and makes the interray 4 kPa modulus
irrelevant to the stiffness budget.

**The authors do not report a Young's modulus for the ray material.** They
compute an effective modulus as `EI / I_eff` but publish it only as a figure in
the supplement (Fig. S5C), which I could not read. **Read-level for the ray
modulus itself: could-not-access.**

### 2.2 Larger-fish fin-ray stiffness — sources disagree, and I preserve it

Flammang BE, Alben S, Madden PGA, Lauder GV (2013). "Functional morphology of
the fin rays of teleost fishes." *J Morphol* 274: 1044–1059.
**Read-level: search-summary of the abstract.** The PDF host (`sites.harvard.edu`)
is not reachable from this session's network allow-list; `journals.biologists.com`
returned HTTP 403. I did not read the paper.

- Flammang et al. 2013 abstract, as summarised: bluegill pectoral fin ray
  flexural stiffness **565 × 10⁻⁶ N·m²**.
- Puri et al. 2018 (full-text), citing Flammang et al. 2013 for bluegill:
  **3.8 × 10⁻⁶ N·m²**.

**These two differ by ~150×.** I cannot resolve which quantity each refers to
(single ray vs. whole fin; proximal vs. distal; possible unit or transcription
difference) without the Flammang full text. **I do not average them and I do not
use either as a load-bearing input.** The zebrafish in-vivo value (§2.1) is the
only measurement I build on. Flagged as an open discrepancy for whoever holds S6.

Additional, lower-confidence context, **read-level: search-summary** only:
reported teleost whole-ray moduli cluster near **~1 GPa** (one source: mean
1.34 GPa proximal, range 0.24–3.7 GPa; distal 0.11–0.67 GPa), while fin-mechanics
*models* assume bone at 4–20 GPa and membrane collagen at 3–12 GPa. The
198–209 GPa figures that surface in searches on this topic are **not fin tissue**:
in Puri et al. they are the steel calibration cantilever (200 ± 10 GPa). I note
this because it is an easy citation trap.

### 2.3 What the fin ray is actually made of

- Zhang J, Wagh P, Guay D, et al. (2010). "Loss of fish actinotrichia proteins
  and the fin-to-limb transition." *Nature* 466: 234–237.
  **Read-level: search-summary.** Identifies **Actinodin 1 and Actinodin 2**
  (And1/And2) as non-collagenous structural components of elastoidin, the
  material of actinotrichia; present in teleosts and elephant shark, absent in
  tetrapods; double knockdown removes actinotrichia and impairs fin folds.
- Duran I, Marí-Beffa M, Santamaría JA, et al. (2011), reported as: actinotrichia
  are formed by **Collagen I plus a fish-specific Collagen II encoded by
  `col2a1b`**, the only type II collagen expressed in fins; lysyl hydroxylase 1
  co-expressed. **Read-level: search-summary.** I did not verify the author list
  or volume/pages from a primary record, so I give the gene symbol (`col2a1b`,
  which I did verify independently in UniProt, §2.5) and not a page citation.
- Mineralised **lepidotrichia** (the segmented bony rays) are the load-bearing
  element in the adult; **actinotrichia** are the unmineralised distal
  collagenous rods. **Read-level: search-summary.**

**My inference, stated separately:** a "structural protein variant for the fin
ray" has three possible targets — Col1a1a, the fin-specific Col2a1b, or
Actinodin — and only the first two are triple-helical collagens for which any
sequence→stability predictor exists. Actinodin has no structural homologue with
a stability model.

### 2.4 The stiffness ceiling of protein-based solids

All **read-level: search-summary**. These are the numbers that decide §4, so their
read-level matters: none of them is full-text here.

| Material | Reported Young's modulus | Note |
|---|---|---|
| Single collagen triple helix | **0.35–12.2 GPa** (optical trapping, radius-dependent); 2.9 GPa (XRD); ~14.5 GPa (optical tweezers); 12–25 GPa (AFM) | order-of-magnitude disagreement, preserved |
| Collagen fibril, **hydrated** | **0.2–0.8 GPa** | AFM, aqueous |
| Collagen fibril, dry/ambient | 2–7 GPa; 5–11.5 GPa (nanoindentation, air) | hydration dominates |
| Isolated fresh thin collagen fibre | 100–360 MPa | authors argue modulus is a distribution, not a number |
| Amyloid fibril | **10–30 GPa** (18–30 GPa for Aβ(1-40), modelling); 3.3 ± 0.4 GPa (insulin fibril, AFM) | described as "among the stiffest protein materials known", and brittle |
| Silk | ~1–10 GPa | literature range, not one measurement |
| Silica-coated amyloid nanofibril | "up to and beyond ~20 GPa" | **hybrid, not a pure protein** |
| Steel (for scale) | 200 ± 10 GPa | measured in Puri et al. as a calibration |

**Disagreement preserved:** the single-molecule collagen modulus spans 0.35 to
25 GPa across methods, and simulation values rise above 15 GPa only at
non-physiological pulling rates (>100 m/s). The one thing the sources agree on is
**ordering**: hydrated fibril < dry fibril ≲ single molecule, i.e. the assembled
material is *softer* than the molecule it is made of.

### 2.5 Sequences and a real structure-prediction run

Sequences retrieved from UniProt REST, 2026-11-04. **Read-level: full-text**
(direct machine-readable record). Real accessions, not invented:

| Protein | Accession | Length |
|---|---|---|
| *D. rerio* Col1a1a (`col1a1a`, allele `chi`/*chihuahua*) | **Q6U1J5** | 1447 aa |
| *D. rerio* Collagen type II α-1b (`col2a1b`) | **L0S5L0** | 1493 aa |
| *D. rerio* Actinodin1 (`and1`) | **E7F5V5** | 570 aa |
| *H. sapiens* COL1A1 (comparator) | **P02452** | 1464 aa |

AlphaFold Protein Structure Database, queried via
`https://alphafold.ebi.ac.uk/api/prediction/{accession}`, 2026-11-04.
**Read-level: full-text** (API response). Pipeline reported by the API as
**"AlphaFold Monomer v2.0 pipeline"**, model created 2025-08-01, DB entry
version 6. **These are predictions produced by EBI/DeepMind, not by me, and not
measurements:**

| Accession | Predicted global pLDDT | pLDDT very-low | low | confident | very-high |
|---|---|---|---|---|---|
| Q6U1J5 (Dr Col1a1a) | **53.44** | 0.658 | 0.137 | 0.062 | 0.144 |
| L0S5L0 (Dr Col2a1b) | **52.38** | 0.694 | 0.114 | 0.061 | 0.131 |
| P02452 (Hs COL1A1) | **52.72** | 0.673 | 0.131 | 0.045 | 0.150 |
| E7F5V5 (Dr Actinodin1) | **57.06** | 0.416 | 0.309 | 0.223 | 0.053 |

`A0A8M1PCU7` (a second TrEMBL entry for `col1a1a`, identical length) returned
HTTP 404 from the AlphaFold API — no model. Noted, not worked around.

**My inference, stated separately:** for all three fin-ray structural proteins,
the majority of residues fall in the *very-low* confidence band, and the
prediction is of a **monomer**. Collagen's load-bearing unit is a
**triple helix of three chains**, which the v2.0 monomer pipeline does not model.
The structure-prediction output for exactly the proteins this subproblem is about
therefore does not resolve the structure whose stiffness is in question.

### 2.6 What I could not access

- **Collagen Stability Calculator** (Persikov AV, Ramshaw JAM, Brodsky B 2005,
  "Prediction of collagen stability from amino acid sequence", *J Biol Chem*
  280(19): 19343–19349; calculator at `collagen.princeton.edu`).
  **Read-level: search-summary** for the paper; **could-not-access** for the tool
  and for its propensity table. All three Princeton hosts
  (`collagen.princeton.edu`, `www.princeton.edu`, `compbio.cs.princeton.edu`)
  were refused by this session's egress proxy (`connect_rejected`). I therefore
  have **no propensity numbers**, and I have not reconstructed any from memory.
- **A structure/stability prediction run of my own.** This container has
  4 CPUs, 15 GB RAM, **no GPU** (`nvidia-smi` absent), no `torch`, and
  `huggingface.co`, `cdn-lfs.huggingface.co`, `dl.fbaipublicfiles.com` and
  `api.esmatlas.com` are all unreachable from here. ESMFold/AlphaFold/Rosetta/
  ThermoMPNN weights cannot be obtained and could not be run on this hardware for
  a 1447-residue chain in any case. **I did not simulate a prediction, and I am
  not reporting one.**
- Flammang et al. 2013 full text (§2.2); Puri et al. supplementary Fig. S5C (§2.1).

---

## 3. What I computed

**Everything in this section is computation, not observation.** Arithmetic is
shown so it can be checked and so the assumptions can be attacked. Script
committed alongside this file: `docs/research/fish/s13_arith.py`
(`python3 -I docs/research/fish/s13_arith.py` reproduces §3.1–§3.5).

### 3.1 Weight

`W = m·g = 0.4 × 10⁻³ kg × 9.81 m·s⁻² = 3.924 × 10⁻³ N = 3.92 mN`

### 3.2 Required spar rigidity for a glide

Assumptions, each of which is a soft spot:

| Assumption | Value | Why / risk |
|---|---|---|
| Wing planform area `S` | 4 × 10⁻⁴ m² (4 cm²) | two "wings" of 2 cm² on a 4 cm fish; generous, implies a fin far larger than the real pectoral |
| Lift coefficient `C_L` | 0.8 | optimistic at this Reynolds number |
| Air density `ρ` | 1.225 kg·m⁻³ | sea level |
| Semi-span `b/2` | 0.02 m (2 cm) | = half body length |
| Spar load model | cantilever, uniformly distributed load | ignores spanwise lift taper (conservative in the *un*helpful direction: real loading is more inboard, so this over-estimates the requirement somewhat) |
| Allowable tip deflection | 10% of semi-span = 2 mm | a chosen engineering criterion, **not** a measured biological limit |

`V = √(2W / (ρ·S·C_L)) = √(2 × 3.924×10⁻³ / (1.225 × 4×10⁻⁴ × 0.8)) = √20.0 = 4.47 m·s⁻¹`

Chord Reynolds number, `c = 0.01 m`, `ν = 1.5 × 10⁻⁵ m²·s⁻¹`:
`Re = 4.47 × 0.01 / 1.5×10⁻⁵ ≈ 2.98 × 10³` — **low-Re regime, where `C_L` = 0.8 is
already generous.**

Uniformly distributed load per half-wing:
`w = (W/2)/(b/2) = 1.962×10⁻³ / 0.02 = 0.0981 N·m⁻¹`

Cantilever tip deflection `δ = w·(b/2)⁴ / (8·EI)`, set `δ = 2×10⁻³ m`:

`EI_req = w·(b/2)⁴ / (8·δ) = 0.0981 × 1.600×10⁻⁷ / (8 × 2×10⁻³) = **9.81 × 10⁻⁷ N·m²**`

### 3.3 The shortfall

Against Puri et al.'s measured whole-caudal-fin `EI`:

| Measured `EI` (N·m²) | `EI_req / EI_meas` |
|---|---|
| 1.5 × 10⁻⁹ (low) | **654×** |
| 2.75 × 10⁻⁹ (mid) | **357×** |
| 4.0 × 10⁻⁹ (high) | **245×** |

### 3.4 Homogenised fin modulus, from the measured numbers

`E_eff = EI / I_eff`, using the measured ranges:

- `1.5×10⁻⁹ / 7×10⁻¹⁶ = 2.1 MPa`
- `1.5×10⁻⁹ / 3×10⁻¹⁶ = 5.0 MPa`
- `4.0×10⁻⁹ / 7×10⁻¹⁶ = 5.7 MPa`
- `4.0×10⁻⁹ / 3×10⁻¹⁶ = 13.3 MPa`

→ **homogenised whole-fin plate modulus ≈ 2–13 MPa (computed).** This is a
*plate* modulus: the cross-section it refers to is 5–8 mm of mostly membrane with
16–18 rays of 0.1–0.2 mm embedded in it. It is **not** the ray material's modulus,
and I do not use it as one.

### 3.5 Where a 357× factor can come from

`EI = E·I`. For a rod, `I ∝ d⁴`, so:

| Route | Requirement for 245× / 357× / 654× |
|---|---|
| Geometry only (`I`) | ray diameter × **3.96 / 4.34 / 5.06** → 0.15 mm ray becomes 0.59 / 0.65 / 0.76 mm |
| Material only (`E`) | `E` × **245 / 357 / 654** |

Taking 357× and applying it to each candidate baseline (computed):

| Baseline `E` | Required `E` after 357× |
|---|---|
| homogenised fin plate, 5 MPa (§3.4) | **1.8 GPa** |
| hydrated collagen fibril, 0.3 GPa (§2.4) | **107 GPa** |
| teleost whole-ray, ~1.0 GPa (§2.2, search-summary) | **356 GPa** |

Compare the measured ceiling for protein solids, §2.4: amyloid fibril
**10–30 GPa**, the stiffest protein material reported; silk 1–10 GPa; and the
single collagen triple helix at **0.35–25 GPa** depending on method.

### 3.6 Sequence composition — a real computation on real sequences

Computed from the UniProt sequences in §2.5. I located the longest contiguous
Gly-X-Y run in each chain (every third residue Gly) and counted proline
occupancy of the X and Y positions. **Caveat stated up front:** UniProt gives the
translated sequence, so Y-position prolines are a *proxy* for
4-hydroxyproline (Hyp), which is installed post-translationally; the real Hyp
fraction is not in the sequence and I did not measure it.

| Chain | Longest Gly-X-Y run | Triplets | Pro in X | Pro in Y | Pro per triplet |
|---|---|---|---|---|---|
| Dr Col1a1a (Q6U1J5) | 1017 aa (res 163–1179) | 339 | 101 (29.8%) | 102 (30.1%) | **59.9%** |
| Hs COL1A1 (P02452) | 1014 aa (res 179–1192) | 338 | 119 (35.2%) | 117 (34.6%) | **69.8%** |
| Dr Col2a1b (L0S5L0) | 1017 aa (res 207–1223) | 339 | 106 (31.3%) | 103 (30.4%) | **61.7%** |
| Dr Actinodin1 (E7F5V5) | **6 aa** | 2 | 0 | 0 | 0% |

**Computed finding:** the zebrafish fin collagens carry ~10 percentage points
*less* imino-acid occupancy per Gly-X-Y triplet than human COL1A1
(59.9% / 61.7% vs 69.8%). **My inference, separately from any author's claim:**
there is real, quantifiable *headroom* on the thermal-stability axis — a
designed variant that raises X/Y proline occupancy toward the mammalian value is
a plausible, non-exotic design target, consistent with a poikilotherm at ~28 °C
not needing a 37 °C-competent helix. Actinodin1, with no Gly-X-Y periodicity
at all, is not a triple-helical protein and offers no such axis.

**What I did not do:** I did not convert this into a ΔTm, because the measured
propensity table that would license that conversion (Persikov et al. 2005) was
unreachable (§2.6), and I will not reconstruct it from memory.

---

## 4. The answer

**Evidence level: `derived`** — a mechanical argument computed from measured
inputs, with the decisive design run `refused` by the environment.

**Answer, in one sentence:** No — a stiffer structural protein variant cannot
supply the stiffness a 0.4 g glider needs, because the required factor is
~245–654× in `EI` and, measured against any ray-material baseline above
~0.1 GPa, that demands a modulus of 10¹–10² GPa, above the ~10–30 GPa ceiling
measured for the stiffest protein solids known; and the sequence→stability design
run that would otherwise settle the designability half of the question could not
be executed in this environment, so that half is `unknown`.

Unpacked into the three claims it rests on, each with its own level:

1. **The stiffness gap is ~245–654× in `EI`.** Level: `derived` (§3.2–3.3) from
   `measured` inputs (Puri et al. 2018, full-text).
2. **A protein-only route cannot cover it.** Level: `derived` from
   `search-summary` material data. The argument has two legs, and the second is
   the stronger one:
   - *Ceiling:* the stiffest measured protein solid is an amyloid fibril at
     10–30 GPa; 107–356 GPa (§3.5) is outside it, and above nacre and tooth
     enamel too. Only mineral (hydroxyapatite, ~10² GPa) reaches there — which
     is a *composition/architecture* change, not a protein-sequence change.
   - *Direction of the loss:* every source in §2.4 agrees that the hydrated
     fibril (0.2–0.8 GPa) is **softer** than the single triple helix
     (≥~2–3 GPa even on the low estimates). The tissue is
     **architecture-limited, not molecule-limited.** A stiffer molecule is
     therefore pushing on the term that is already not the bottleneck; the best
     a sequence redesign can do is recover the molecule→fibril→tissue loss, not
     exceed the molecule. That caps the sequence route at roughly one order of
     magnitude, against a requirement of two to three.
3. **A stiffer-*and*-more-stable collagen variant is nonetheless designable in
   principle, and there is measurable headroom to design into.** Level:
   `derived` from my own sequence computation (§3.6) on `full-text` UniProt
   records — zebrafish fin collagens sit ~10 points below human COL1A1 in
   X/Y imino-acid occupancy. **But the axis with headroom is Tm, not `E`.**
   Protein-design and stability predictors output ΔΔG and Tm; Young's modulus is
   not among their outputs. A ΔTm win is not a stiffness win, and I will not
   present one as the other.

**On the stated refutation condition** ("predicted stability changes
indistinguishable from wild type"): I **cannot report on it**. I ran no stability
predictor, because the weights, the APIs and the Princeton calculator were all
unreachable and the container has no GPU (§2.6). The refutation condition is
therefore neither met nor avoided — it is untested. **Level: `refused`
(environment), not `measured` and not `simulated`.** The real AlphaFold DB
predictions I *could* retrieve (§2.5) are monomer predictions at global pLDDT
52–57 with 42–69% of residues very-low confidence, i.e. they do not resolve the
triple helix whose stiffness is at issue, so they cannot stand in for the missing
run either.

**The single number that decides it:** **EI_req ≈ 9.8 × 10⁻⁷ N·m² against a
measured 1.5–4 × 10⁻⁹ N·m²** — a 245–654× gap, of which a protein-sequence
change can address at most ~10×.

---

## 5. What this does NOT establish

This section is meant to be read as carefully as §4. Being generous here:

1. **It does not establish that no stiffer collagen variant exists.** I showed
   that one would be *insufficient*, not that one is *impossible*. §3.6 in fact
   points the opposite way: there is 10 percentage points of imino-acid headroom
   to exploit. The negative is about **sufficiency for flight loads**, nothing else.
2. **It does not report any designed sequence.** The deliverable asked for
   candidate sequences with predicted structure and stability from a real
   prediction run. **I produced none, and I invented none.** Anything that looked
   like a candidate here would be fabrication. §2.6 states exactly what was
   unreachable.
3. **It does not establish the ray material's Young's modulus.** The one
   number that would anchor §3.5 — `E` of zebrafish lepidotrichia — is
   `could-not-access` (Puri et al. Fig. S5C) and the larger-fish proxies are
   `search-summary` only, with the two Flammang-derived values disagreeing by
   ~150× (§2.2). My conclusion is robust across the plausible range (any baseline
   ≥0.1 GPa fails), but the baseline itself is not established here.
4. **It does not establish `EI_req`.** §3.2 is one load case with six chosen
   assumptions. Change `C_L`, allowable deflection, planform, or the load
   distribution and the requirement moves by a factor of a few — though not by
   the two orders of magnitude that would change the answer. **The 10% tip
   deflection criterion is mine, not biology's**; a flapping or
   passively-cambering wing may tolerate far more, and if it tolerates ~20× more
   deflection the gap closes to ~10–30×, which is where this answer would start
   to wobble. That is the single most load-bearing arbitrary choice in the
   document.
5. **It does not account for mass.** The geometric route (§3.5: ray diameter
   ×4–5) carries a mass penalty on a 0.4 g animal that I did not compute at all.
   "Geometry wins over materials" here means only "geometry can reach the
   number"; whether it can reach it *and* still fly is S6's problem, not answered
   here.
6. **It does not test any protein-design model's accuracy.** "This is where
   protein design models earn their place" — on this subproblem, they could not
   be run, so they neither earned nor lost it. The AlphaFold pLDDT values I
   retrieved are evidence about *monomer* prediction confidence on collagen, not
   a verdict on protein design as a field; AlphaFold-Multimer, AF3, Boltz or a
   collagen-specific method would very likely do better on the triple helix and
   none of them was available to me.
7. **It does not touch Tm, hydration, cross-linking, or mineral nucleation,**
   each of which a sequence change could plausibly move and any of which could
   matter to fin-ray performance for reasons other than stiffness (fatigue life,
   regeneration, thermal range). The question asked was stiffness; I answered
   stiffness.
8. **It does not resolve which protein to target.** Col1a1a, Col2a1b and
   Actinodin all sit in actinotrichia/lepidotrichia; the division of mechanical
   labour between them is not quantified in any source I read.
9. **I did not read the primary papers for most of §2.3 and all of §2.4.** Those
   are `search-summary`. If any one of them is misquoted upstream, the
   corresponding row is wrong. The 10–30 GPa amyloid ceiling in particular is
   partly computational in origin, and I am using it as a ceiling.
10. **Negative-search scope.** My searches for a measured Young's modulus of
    *actinotrichia or elastoidin specifically* returned nothing usable: scope was
    English-language web search (one query, "standard" mode) plus attempted
    full-text access to PMC/NCBI; `sites.harvard.edu`, `journals.biologists.com`
    (403), Princeton and Hugging Face were unreachable. The closest hit was a
    1987 *J Mater Sci* study of elastoidin at varying strain rates
    (Arumugam & Sanjeevi, per a Springer listing — **read-level: listing**) whose
    full text I could not open and whose moduli I therefore do not quote.
    **Absence here means "not found within that scope", not "does not exist".**

---

## 6. What would change the answer

Ordered by how much each would move it:

1. **A measured `E` for zebrafish lepidotrichia.** If the ray material's modulus
   turns out to be ~10 MPa rather than ~1 GPa — i.e. if the rays are much softer
   than the whole-ray teleost proxies and the fin is soft because its *material*
   is soft rather than because its *geometry* is slender — then 357× lands at
   ~3.6 GPa, which is inside the measured range for dry collagen fibrils and
   silk. **A materials route would then be live.** This is the single
   measurement that could flip the answer. Nanoindentation or microbeam bending
   on isolated adult zebrafish rays, hydrated, would settle it; Puri et al.'s
   own Fig. S5C may already contain it.
2. **A defended deflection criterion.** Replace my 10%-of-semi-span with a
   measured or aerodynamically-derived limit (see item 4 in §5). A tolerance of
   ~40% semi-span, as a passively-cambering membrane wing might allow, cuts the
   requirement ~4× and brings the protein route within an order of magnitude of
   mattering.
3. **A real design run, unblocked.** With GPU access and reachable weights:
   (a) AlphaFold-Multimer or AF3 on an explicit Col1a1a/Col1a2 heterotrimer to
   get a triple-helix model with per-residue confidence; (b) the Collagen
   Stability Calculator (Persikov 2005) or the 2020 *Nat Chem* heterotrimer
   algorithm on the §3.6 candidate class (raise X/Y imino occupancy from 59.9%
   toward 69.8%) for a predicted ΔTm; (c) explicitly **note that none of these
   outputs is a modulus**, and pair them with a coarse-grained or MD estimate of
   axial modulus if a stiffness claim is wanted. This would answer the
   *designability* half that is currently `unknown`.
4. **Resolution of the Flammang 2013 discrepancy** (565 × 10⁻⁶ vs
   3.8 × 10⁻⁶ N·m², §2.2). Not decisive for S13, but it is a 150× error sitting
   in the literature chain this project depends on, and S6 may be standing on it.
5. **Any measured modulus for a protein-only solid above ~50 GPa.** That would
   break the ceiling leg of §4.2 and reopen the materials route on its own terms.
   I know of none and found none.
6. **Reframing the target from `E` to mineral fraction.** If S6 fails on
   geometry *and* S13 fails on protein `E`, the remaining route in this part of
   the design space is **mineralisation** — more/denser hydroxyapatite in the
   lepidotrichia, reached by changing collagen's mineral-nucleating sequence
   motifs or the osteoblast program rather than the collagen backbone's own
   stiffness. That is a protein-level intervention with a composite-level
   mechanism, and it is a different subproblem from the one I was asked. I flag
   it as the natural successor rather than claiming it works.

---

## Provenance

- Network environment: egress proxy with a host allow-list. Reachable:
  `rest.uniprot.org`, `alphafold.ebi.ac.uk`, `pmc.ncbi.nlm.nih.gov`,
  `www.ncbi.nlm.nih.gov`, `arxiv.org`. Refused/unreachable:
  `collagen.princeton.edu`, `www.princeton.edu`, `compbio.cs.princeton.edu`,
  `huggingface.co`, `cdn-lfs.huggingface.co`, `dl.fbaipublicfiles.com`,
  `api.esmatlas.com`, `sites.harvard.edu`; `journals.biologists.com` → HTTP 403.
- Compute: 4 CPU, 15 GB RAM, no GPU, no `torch`.
- All arithmetic in §3 is reproducible from the expressions shown.
- No number, citation, gene symbol, allele or accession in this file was invented.
  Where a value was unavailable it is marked `could-not-access`, `unknown`, or
  omitted.

```swarm-result
{"subproblem": "S13", "evidence": "derived",
  "answer": "No: closing the ~245-654x flexural-rigidity gap to a 0.4 g glider would need a ray modulus of 10^1-10^2 GPa against a measured ~10-30 GPa ceiling for the stiffest protein solids, and since hydrated collagen fibrils are already softer than the triple helix the tissue is architecture-limited rather than molecule-limited, so a stiffer protein variant is insufficient even though ~10 points of imino-acid headroom exists on the separate thermal-stability axis; the design run that would settle designability could not be executed here.",
  "key_number": "EI_req 9.8e-7 N m^2 vs measured 1.5-4e-9 N m^2 (245-654x gap)",
  "blocked_on": "No structure/stability prediction run was possible: no GPU and huggingface.co, dl.fbaipublicfiles.com, api.esmatlas.com and collagen.princeton.edu (Collagen Stability Calculator, Persikov 2005) all unreachable; also could not access Puri et al. 2018 Fig. S5C (ray effective Young's modulus) or Flammang et al. 2013 full text, leaving a 150x unresolved discrepancy in the bluegill fin-ray stiffness literature."}
```
