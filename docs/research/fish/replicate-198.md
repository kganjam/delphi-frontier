# Replicate 198: independent re-derivation of the S23 actinotrichia-stiffness claim

**Claim under test (S23):** no published gain-of-function raises actinotrichia. The computed
material-only ceiling for stiffening an unmineralised collagenous fibril falls one to two orders
of magnitude short of the fin flexural-stiffness increase a 0.4 g glider would need. Adult
actinotrichia-null fish still form rays (with thicker hemirays, per the claim). So actinotrichial
stiffness is probably not what limits S6.

## What I did and did not see

- The harvest the task names (`harvest:s23-actinotrichia-stiffness-protein-wwp5m2`) is **not in
  this repository**. I searched the whole working tree and all git refs for `actinotrich`. The
  only hit was `findings/gemini-triage-267-problems.json`, a triage text about actinodin/Hox13
  mutants. It holds no stiffness numbers and no S23 working, and I read only the matching
  sentence. **I did not see the original derivation.**
- The question text itself still contains the figures "~20-25x" and "~10^2-10^3x", so I could
  not be blind to the recorded values. I derived my own numbers from primary sources before
  comparing them, and I report where mine differ.

## Inputs (source, read-level)

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| I1 | Hydrated single collagen fibril, tensile E (in PBS) | 470 ± 410 MPa (range 110–1470, n = 11) | Shen et al. 2010, *Biophys J* 99:1986, PMC2941005 (sea-cucumber dermis, MEMS tension) | full-text (via fetch summary) |
| I2 | Same fibrils, in air | 860 MPa (authors' earlier study) | Shen et al. 2010, Discussion | full-text (via fetch summary) |
| I3 | Literature range, hydrated fibrils | 0.2–0.86 GPa | Svensson et al. 2010, *Biophys J* 99:4020, PMC3000511, Introduction | full-text (via fetch summary) |
| I4 | Hydrated human tendon fibril, tensile E (in PBS) | 2.89 ± 0.23 GPa | Svensson et al. 2010, Table 1 | full-text (via fetch summary) |
| I5 | Within-study dry→hydrated drop | ~2–3x (pilot, Svensson); ~10x, ~5 → ~0.5 GPa (van der Rijt, as cited by Svensson); bending 1–3.9 GPa dry vs 0.07–0.17 GPa hydrated (Yang, as cited by Svensson) | Svensson et al. 2010, Discussion | full-text (cited values are secondary) |
| I6 | Dry fibril E, upper end | 5–11.5 GPa (Wenger, Oliver–Pharr indentation); 0.9–11.5 GPa overall review range | search-result summary of a review (encyclopedia.pub/PMC) | search-summary |
| I7 | Hydrated fibril, indentation (radial) | ~1.2 MPa | cited in Shen et al. 2010, which attributes the low value to anisotropy | full-text (secondary citation) |
| I8 | Whole adult zebrafish caudal fin flexural stiffness EI, in vivo | 1.5×10⁻⁹ – 4×10⁻⁹ N m², measured along the proximal–distal axis; 16–18 rays; ray diameter 0.1–0.2 mm; fin width ~5–8 mm; fish aged 6–12 months | Puri et al. 2018, *J Exp Biol* 221: jeb171777, PMC5868929 | full-text (via fetch summary) |
| I9 | Interray tissue does not measurably change fin EI; E_tissue = 4 ± 2 kPa | — | Puri et al. 2018 | full-text (via fetch summary) |
| I10 | and1/and2 double-mutant adults: fins lack actinotrichia; all fin-fold-derived skeleton disrupted but rays present; no bifurcations; blunt ray tips; fewer, shorter, wavy lepidotrichia | — | Hanzelova et al. 2026, *Development* 153: dev204990 (ZFIN ZDB-PUB-260327-1) and a uOttawa thesis | search-summary (zfin.org returned 503; franklin.zfin.org, ruor.uottawa.ca and www.uottawa.ca did not resolve from this session) |
| I11 | Glider body mass | 0.4 g (from the claim; matches adult zebrafish mass) | claim text | — |
| I12 | Glider fin geometry: semi-span L = 1–2 cm (central 1.5 cm), uniform load, two fins, allowed tip deflection δ/L = 0.05–0.2 (central 0.1) | — | **my assumption**, not sourced | — |

## Part A: is there a gain-of-function that raises actinotrichia?

- **Searches run (web, standard mode):**
  - "actinodin overexpression gain-of-function actinotrichia increased zebrafish transgenic"
  - "actinotrichia overexpression collagen9 col9a1 …"
- **What turned up:**
  - Loss-of-function work: Zhang et al. 2010 *Nature*; Hanzelova et al. 2026; Nakagawa et al. 2022 on col9a1c.
  - and1 enhancer and reporter work: 2019 *PLoS One*, PMC6497306.
  - A col9a1 overexpression **rescue** of the *prp* mutant (Huang et al. 2009). A rescue restores normal actinotrichia. It is not a gain above wild type.
- **Finding:** no gain-of-function that raises actinotrichia above wild type turned up.
- **Scope of this negative:** two web searches, read at search-summary level. I did not search PubMed or ZFIN directly (ZFIN returned 503). I also did not check heat-shock or mRNA overexpression of and1/and2 specifically. **This is a weak negative.**

## Part B: material-only stiffness ceiling for an unmineralised collagen fibril (calculated)

"Material-only" means the fibril's Young's modulus E rises while its cross-section stays fixed,
and without mineral. The highest unmineralised value on record is the dry fibril. A real tissue
stays hydrated, so this ceiling is generous: it is not a route that is actually reachable.

| Ratio | Arithmetic | Result |
|---|---|---|
| Cross-study: dry upper end ÷ hydrated tensile mean | 11.5 GPa / 0.47 GPa (I6/I1) | **24.5x** |
| Cross-study: dry lower Wenger end ÷ hydrated tensile mean | 5 / 0.47 | 10.6x |
| Within-study (van der Rijt) | ~5 / ~0.5 | ~10x |
| Within-study (Svensson pilot) | — | ~2–3x |
| Within-study bending (Yang) | 1/0.17 = 5.9x to 3.9/0.07 = 55.7x | **6–56x** |
| Against the stiff hydrated human fibril | 11.5 / 2.89 (I6/I4) | 4.0x |
| Extreme cross-study | 11.5 / 0.07 | 164x |

**Sources disagree, and I am not averaging them.**
- The hydrated baseline spans more than an order of magnitude even within tension: 0.11–2.9 GPa (I1 vs I4).
- Indentation gives a hydrated value about 400x lower still (I7), which Shen et al. attribute to anisotropy.

**My value (calculated): about 10x**, plausible range **~3–25x**. Within-study figures above 25x
exist (up to ~56x from bending tests, and 164x only by pairing extremes from different studies).
The claim's "~20–25x" sits at the top of my plausible range and matches my 24.5x cross-study
pairing exactly. My central estimate, built on within-study ratios, is lower.

## Part C: flexural-stiffness increase a 0.4 g glider fin needs (calculated)

Model (calculated, Euler–Bernoulli beam):
- Each pectoral fin is a cantilever of semi-span L.
- The weight is shared equally between the two fins and spread evenly along each one.
- Tip deflection: δ = F·L³/(8·EI), so the stiffness needed is EI_req = F·L²/(8·(δ/L)).

Load:
- W = 0.4×10⁻³ kg × 9.81 m s⁻² = 3.924×10⁻³ N
- Load per fin: F = 1.962×10⁻³ N
- A cross-check, not needed for EI: with total fin area 3×10⁻⁴ m², wing loading = 13.1 N m⁻². With C_L = 0.8 and ρ_air = 1.2, glide speed ≈ 5.2 m s⁻¹.

Central case (L = 0.015 m, δ/L = 0.1):
- EI_req = 1.962×10⁻³ × 2.25×10⁻⁴ / 0.8 = **5.5×10⁻⁷ N m²**

Baseline: the whole caudal fin of an adult zebrafish measures EI = 1.5–4×10⁻⁹ N m² (I8, an
observation). Using the caudal fin is generous, because the pectoral fin is smaller.

Ratio needed (calculated):

| L (m) | δ/L | EI_req (N m²) | Ratio to I8 |
|---|---|---|---|
| 0.010 | 0.20 | 1.2×10⁻⁷ | 31–82x |
| 0.010 | 0.10 | 2.5×10⁻⁷ | 61–164x |
| 0.015 | 0.10 | 5.5×10⁻⁷ | **138–368x** |
| 0.015 | 0.05 | 1.1×10⁻⁶ | 276–736x |
| 0.020 | 0.05 | 2.0×10⁻⁶ | 490–1308x |

**My value (calculated): ~1.4–3.7×10² x** in the central case, with a range of **~30x to ~1.3×10³ x**
across my assumed geometry. The geometry (I12) is my own assumption and is the main source of
uncertainty.

## Part D: the gap, and what it means (inference)

- Need ÷ material ceiling (calculated):
  - Central: ~140–370 / ~10 ≈ 14–37, about 1–1.5 orders of magnitude.
  - Most favourable to material: 31 / 25 ≈ 1.2, almost no gap.
  - Least favourable: 1308 / 3 ≈ 400, about 2.6 orders of magnitude.
- **My inference:** in most of the parameter space, material stiffening alone does not get there.
  Geometry is the obvious lever, because EI grows as thickness to the fourth power for a solid rod (∝ r⁴):
  - A 140–370x increase needs the ray radius to grow by 140^(1/4) to 370^(1/4) = 3.4–4.4x.
  - Or, with an effective section where EI ∝ t³, the thickness must grow 5.2–7.2x.
- **A second inference, from I8, I9 and I10:** in adult fins the bending load is carried by the
  rays (mineralised lepidotrichia), not by the interray tissue (I9). Actinotrichia sit only at the
  distal fin margin. Rays still form without actinotrichia (I10). Both point the same way as the
  claim: actinotrichia are not the main stiffness element in an adult fin.
- **"Thicker hemirays": I could not verify this.** The sources I could reach (search-summary
  level) describe adult and1/and2 double-mutant rays as fewer, shorter and wavy, with no
  bifurcations and blunt tips. None of them mention hemiray thickness. The full text of
  Hanzelova et al. 2026 was not reachable from this session (the network blocked it). This part
  of the claim stays **unverified, not refuted**.

## Comparison with the recorded value

The recorded figures appear in the question as "~20–25x" (ceiling) and "~10²–10³x" (need).

| Item | Recorded | Mine | Verdict |
|---|---|---|---|
| Material ceiling | ~20–25x | ~10x central, ~3–25x | **Agree in order of magnitude.** The recorded figure sits at my upper bound and matches my cross-study 24.5x. Mine is lower centrally, which makes the claim's gap *larger*. |
| Glider need | ~10²–10³x | ~1.4–3.7×10² central, 30–1300x | **Agree.** |
| Gap of 1–2 orders | 1–2 orders | ~1–1.5 central, 0.1–2.6 range | **Agree**, with a lower edge where the gap nearly closes. |
| No gain-of-function | none published | none found (weak, scoped negative) | Agree, weakly |
| Null adults have thicker hemirays | yes | not verifiable | **CANNOT TELL** |

**Overall: I AGREE with the quantitative core** (ceiling about 10¹ against a need of about 10²–10³,
so material stiffening is insufficient). I **CANNOT TELL** on "thicker hemirays".

Caveats:
- I could see the recorded numbers in the question text, so this replication is not fully blind.
- My glider geometry is assumed, not sourced.

```swarm-replication
{"claim_id": 198, "my_value": "material-only ceiling ~10x (range ~3-25x, calculated); required fin EI increase ~140-370x central (range ~30-1300x, calculated) vs adult zebrafish caudal fin EI 1.5-4e-9 N m^2 (observed)", "agrees": true,
  "note": "Independent ratios reproduce a ~1-2 order-of-magnitude shortfall of material-only stiffening (my central ceiling is lower than the recorded 20-25x, which strengthens the claim), but the 'thicker hemirays' detail could not be verified because the Hanzelova 2026 full text was unreachable."}
```
