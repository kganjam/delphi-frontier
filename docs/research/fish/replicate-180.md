# Replication 180 — S7-D: required girdle section with measured teleost bone yield

Date: 2026-11-04. Independent re-derivation of the S7-D claim.

**My value (calculated, not observed): the worst-case required solid-equivalent circular section is d = 0.260 mm at σ_y = 62.6 MPa, or 0.255 mm at 66.8 MPa.** Using the lower 1-SD yield stresses gives 0.282 mm (49.4 MPa) and 0.294 mm (43.4 MPa). The uncertainty I can defend is therefore **0.25–0.29 mm**, conditional on the load model. Every load input is an assumption, not a measurement.

## What I read, and in what order

1. **The problem definition and load-model assumptions**, from `docs/research/fish/S7-organ.md` §1–3d, branch `claude/s7-organ-pectoral-girdle-xlxpkt`. Read-level: full-text. This is the upstream S7 work, not the claim I am checking.
2. **The input script** of the claim, `docs/research/fish/S7-deepen.py`, branch `claude/deepen-s7-pectoral-girdle-b6j2hx`. The brief pointed me there for inputs. **Disclosure:** that script contains the formula, so I saw the method before I derived anything. It prints no results, and I did not run it. I then wrote my own script (`replicate-180.py`) and read the yield stress from the primary paper myself. This is therefore an independent recomputation of the **arithmetic and the material input**. It is **not** an independent choice of load model.
3. **The primary paper for bone yield.** I read Fiedler et al. 2019 myself (step 2 of the derivation below).
4. **The recorded value.** I opened `S7-deepen.md` only after my numbers were final (comparison section).

## Inputs

| Input | Value | Source | Read-level | Status |
|---|---|---|---|---|
| Body mass m | 0.4 g | Project brief, as given in S7-organ §1 | full-text (repo) | assumed design point |
| g | 9.81 m s⁻² | standard | — | constant |
| Air density ρ | 1.2 kg m⁻³ | standard sea-level value | — | constant |
| C_L | 0.78 | Park & Choi 2010, *J. Exp. Biol.* 213:3269, as cited in S7-organ | search-summary (per S7-organ; I did not re-read it) | measured on flying fish, borrowed |
| Speed V | 3 m s⁻¹ (worst case) | S7-organ assumption A3 | full-text (repo) | assumed |
| Aspect ratio AR | 9 | S7-organ A4; source unidentified | search-summary per S7-organ | assumed |
| Body half-width | 2.5 mm | S7-organ A5 | full-text (repo) | assumed |
| Lift centroid | 4/(3π) of fin length (elliptic loading) | standard idealisation | — | assumed |
| Load factor n | 3 (worst case) | S7-organ A7 | full-text (repo) | assumed |
| **Bone yield stress σ_y** | **66.8 ± 23.4 MPa** (small fish, n=20); **62.6 ± 13.2 MPa** (large fish, n=23); maximum stress 110.5 ± 23.4 and 107.5 ± 22.6 MPa; E 3.5 ± 1.4 and 2.6 ± 0.5 GPa | Fiedler et al. 2019, *J. Biomech.*, doi 10.1016/j.jbiomech.2019.07.009, PMC6995032, Table 1. Atlantic herring intermuscular bones, uniaxial micro-tensile test. | full-text (PMC, read via a fetch tool that summarised the page; I asked it for the Table 1 values verbatim) | **measured** |

## Arithmetic (all calculated)

- W = 0.4×10⁻³ × 9.81 = 3.924×10⁻³ N
- S = 2W/(ρV²C_L) = 7.848×10⁻³ / (1.2 × 9 × 0.78) = 7.848×10⁻³ / 8.424 = 9.316×10⁻⁴ m²
- b = √(AR·S) = √(8.385×10⁻³) = 0.09157 m
- Fin length s = b/2 − 0.0025 = 0.04579 − 0.0025 = 0.04328 m
- Lift centroid ȳ = 0.42441 × 0.04328 = 0.01837 m
- Root moment per fin M = n(W/2)ȳ = 3 × 1.962×10⁻³ × 0.01837 = **1.081×10⁻⁴ N·m**
- Required solid rod diameter d = (32M/(πσ_y))^(1/3). Here 32M = 3.460×10⁻³.
  - σ_y = 62.6 MPa: 3.460×10⁻³ / 1.9666×10⁸ = 1.760×10⁻¹¹ m³, so d = **0.260 mm**
  - σ_y = 66.8 MPa: d = 0.2545 mm
  - σ_y = 49.4 MPa (62.6 − 13.2): d = 0.2815 mm
  - σ_y = 43.4 MPa (66.8 − 23.4): d = 0.2939 mm
  - For reference, the old 25–114 MPa bracket gives 0.353–0.213 mm. Using maximum stress (107.5 MPa) instead of yield gives 0.217 mm.

### Sensitivity check (calculated)

Ratio of d to its baseline (σ_y = 62.6 MPa, worst case) for a factor-of-2 change in one input:

| Input | ×0.5 | ×2 |
|---|---|---|
| V | 1.272 | 0.778 |
| n | 0.794 | 1.260 |
| σ_y | 1.260 | 0.794 |
| C_L | 1.129 | 0.884 |
| AR | 0.884 | 1.129 |
| half-width | 1.010 | 0.980 |
| **body mass m** | **0.701** | **1.422** |

The claim's "≤27%" holds for every input in the claim's sweep. **Mass is not in that sweep.** In this model d ∝ m^0.5, since M ∝ W·b ∝ W^1.5. So a factor-of-2 change in mass moves d by 42%. This is my inference from the model. Mass is a fixed design point in the project brief, not an estimated input, so it does not contradict the claim as worded. It is still the one load input that exceeds the 27% bound. Doubling mass would give d ≈ 0.37 mm.

The "×8" statement is geometry. Bending stress is M/Z, and Z ∝ d³ for a solid section, so halving the actual section multiplies stress by 2³ = 8. Taking the worst case of 2.6× (62.6 MPa / 25 MPa) as a rough guide, factor-of-2 errors in the loads cannot flip the conclusion, but a factor-of-2 error in the actual section can. I did not try to measure the actual girdle section. MorphoSource 000415918: could-not-access (not attempted; the claim reports it as inaccessible from this environment).

### Caveats (my inference, not the authors')

- The yield value comes from **tension** on **herring intermuscular bone**, not zebrafish girdle bone in bending. Bending strength of bone is usually higher than tensile yield, so using tensile yield is probably conservative. That is my inference, and I did not verify it for fish bone.
- Herring IB is a different species and skeletal element from zebrafish girdle bone. Whether the two have comparable bone tissue is unknown to me.
- The small-fish SD (±23.4 MPa) is large. The 1-SD band, not the mean, is the honest uncertainty.

## Comparison with the recorded value

I opened `S7-deepen.md` only after my numbers were final. It records the worst case (V = 3, n = 3) as "0.255–0.260 mm" at 62.6–66.8 MPa, 0.294 mm at the lower 1-SD value, and M ≈ 1.1×10⁻⁴ N·m per fin. Its 1-SD figure uses 43.4 MPa. It also records the ≤27% sensitivity bound.

**AGREE.** I get 0.2545–0.2601 mm, 0.294 mm, and 1.081×10⁻⁴ N·m, which match to the digits shown. The Table 1 yield values (62.6 and 66.8 MPa) match what I read in the paper. Two caveats limit how much this agreement is worth:

- I saw the claim's input script before deriving, so the load model is shared, not independently chosen.
- The ≤27% bound does not cover a factor-of-2 error in body mass (42%), which their sweep omits.

Sources: [Fiedler et al. 2019, PMC6995032](https://pmc.ncbi.nlm.nih.gov/articles/PMC6995032) (full-text); [UKE FIS listing](https://fis.uke.de/portal/de/publications/microstructure-mineral-and-mechanical-properties-of-teleost-intermuscular-bones(20383074-52ca-4868-ab15-1c3062f8f7df).html) (listing).

```swarm-replication
{"claim_id": 180, "my_value": "0.260 mm (0.255–0.260 mm at 62.6–66.8 MPa; 0.28–0.29 mm at lower 1-SD yield) for M = 1.08e-4 N·m per fin", "agrees": true,
  "note": "Arithmetic and measured herring IB yield (Fiedler 2019 Table 1, full-text) reproduce the 0.26 mm worst case, but the load model was seen in the claim's script and the ≤27% sensitivity omits body mass (factor 2 → ×1.42)."}
```
