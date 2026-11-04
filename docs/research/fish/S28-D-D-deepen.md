# S28-D-D: deepening S28-D by attacking its weakest input (pectoral fin length per fin)

**Parent.** S28-D, `docs/research/fish/S28-deepen.md` and `S28-deepen_calc.py` @ 511ecf7b (branch
`origin/claude/deepen-s28-daane-heterozygote-b7kpn8`). Grandparent: S28, `S28-organism.md` @ e8ba4191
(branch `origin/claude/s28-organism-design-5z0vjz`). I read both in full with `git show`. Neither is on this branch.

**Status.** No new measurement was made. The key new input is a **figure-read**: values digitised from a plotted
graphic in a primary source. It is not a raw datum. Every other number without a source beside it is a
**calculation** from the scripts below. Date: 2026-11-04.

**Scripts (this branch):**
- `S28-D-D_fig_digitize.py`: pixel-calibrated read of Fig 8B.
- `S28-D-D_outline.py`: planimetry of the folded-fin outline in Fig 8A.
- `S28-D-D_spread.py`: planimetry of the partly spread fin in Fig 8A.
- `S28-D-D_calc.py`: recomputation, using S28-D's trajectory model unchanged. It takes about 20 s.

The figure image is not committed, because the preprint is licensed CC-BY-NC-ND. To reproduce, download the PDF
(sha256 below), then run `pdfimages -f 31 -l 31 -png pre.pdf fig8` and pass `fig8-000.png` to the first three scripts.

---

## 0. Short answer

S28-D found that its answer was most sensitive to **pectoral fin length per fin / SL**. S28 had *extrapolated*
that value as 0.45 SL. S28-D could not reach the figure that holds it and recorded it as `unknown`. Through a route
S28-D did not try, I reached the bioRxiv preprint PDF, whose figure is embedded. Its **Fig 8B is the same
measurement as the published Fig 4B**, and I digitised it:

> **Double heterozygote `lat4a^nr21/+; kcnh2a^lof/+`: pectoral fin length / SL median 0.463 (IQR 0.449–0.488;
> isolated points 0.434–0.534; n = 34). Wild type: 0.223 (IQR 0.211–0.243; n = 7).** These are figure-reads.

- **S28's unsourced 0.45 SL turns out to be right, within 3 %.** S28-D's "≤ 0.25 SL → ≤ 2.4 %" branch is
  excluded: every one of the 34 points lies above 0.43.
- The length uncertainty is gone. That makes **spread-fin area** the controlling input. It is now the split between
  S28's AR-5 rule (case C) and its length-only rule (case A). Fig 8A contains two outlines of the double-het fin,
  and I read both. Both give a planform shape factor A/L² of **0.13–0.25 per fin**. Case C needs **0.52**.
- At the measured length, the phenotype S28 proposed calculates to the following:
  - **1.4–2.6 %** reduction in ascent deceleration at 1.38 m/s, and 1.8–3.3 % at 1.57 m/s, using the
    area the figure shows;
  - **5.1 %** only if the fin spreads to the case-C planform, which is 2–4× the area in any image I found.
- **The negative (no flight, no glide, no skim, no meaningful leap extension) STANDS.**
- **S28-D's conclusion STRENGTHENS.** Its "plausibly 1–3 %" now rests on a figure-read length and a figure-read
  shape. One of S28-D's sub-claims falls: "S28's 0.45 SL is not supported by the primary source". The primary
  source supports 0.45 SL.

## 1. Which input of S28-D is the answer most sensitive to? (recomputed)

S28-D's answer has three parts. The negative is robust to ×2 on every input. The phenotype is "0.9–6.2 %,
likely 1–3 %". The conditional is "≥ 0.4 SL per fin needed for ~5 %". S28-D's own sensitivity table (§1 there)
already showed what dominates the phenotype: exit speed and fin length enter quadratically, and everything else
enters linearly. S28-D argued exit speed is pinned within ×1.14 by Demesmay 2025. Fin length had no measurement
behind it.

With S28-D's model copied unchanged, my script reproduces its baseline: a reduction of 4.88 % at 0.45 SL and
1.38 m/s, against S28-D's 4.87 %. S28-D's own ×0.5 / ×2 rows (not re-run here) take the effect from 4.9 % to
1.6 % and 14.8 %. Fin length is therefore S28-D's most sensitive *and* least established input. **I attack that input.**

## 2. How well was it established?

- **In S28:** an assumption, labelled "EXTRAPOLATION … I have not taken it from the measured allele".
- **In S28-D:** `unknown`. S28-D read the Daane 2021 full text and found no number in it. The Fig 4B image,
  Data S1 and ZFIN were all could-not-access.
- **In the S22 line** (S22-D-D-D, read from the repository at
  `origin/claude/deepen-s22-d-d-input-vncsjh` and `…-j5x0vq`): a **proxy prediction**,
  Rz = p0 × f ≈ 0.21 × (1.74–2.05) ≈ 0.36–0.43 SL. Here p0 is the wild-type pectoral/SL and f is a fold-overgrowth
  borrowed from a *different* allele, kcnk5b alf/+.

Neither the assumption nor the proxy had been checked against the plotted data.

## 3. Improving it

### 3.1 Access record (this session)

| Target | Result | Read-level |
|---|---|---|
| PMC9172250 article HTML, `pmc.ncbi.nlm.nih.gov` | HTTP 200. It lists the figure URLs on `cdn.ncbi.nlm.nih.gov` | full-text (HTML fetched; text not re-read beyond figure links) |
| Fig 4 image on `cdn.ncbi.nlm.nih.gov/pmc/blobs/b3db/9172250/187bcb7df244/nihms-1735542-f0004.jpg` | Proxy refused CONNECT (403, policy) | could-not-access |
| `NIHMS1735542-supplement-2.xlsx` (Data S1) and `…-supplement-1.pdf` via `pmc.ncbi.nlm.nih.gov/articles/instance/9172250/bin/` | Served a proof-of-work page whose script lives on the blocked CDN, and a reCAPTCHA page. I did not try to get around either | could-not-access |
| Europe PMC supplementaryFiles API for PMC9172250 | "not open access" | could-not-access |
| Europe PMC record for the preprint DOI 10.1101/2021.03.05.434157 | PPR293816, which links the bioRxiv full PDF | listing |
| **bioRxiv preprint PDF**, `biorxiv.org/content/biorxiv/early/2021/03/07/2021.03.05.434157.full.pdf` | HTTP 200, 6.2 MB, sha256 `d5096d02d6d154ee8843ae13aeb82df2bbeeb77e567622872abbb13927ed6c40`. Page 31 embeds Fig 8 as a 1554×710 raster | **full-text, including figure image** |
| Published Curr Biol Fig 4B image (to confirm it matches preprint Fig 8B) | not reachable (above) | could-not-access |

**Identity of preprint Fig 8 and published Fig 4.** The preprint Fig 8 legend reads: "(B-C) Pectoral fin
length (B) and caudal fin length (C) suppression of overgrowth in medial fin by lat4a. In (B-C), length normalized
by standard length (SL); p-values generated through Tukey's HSD". The published Fig 4B/C legend, as quoted
verbatim by S28-D, says the same. *My inference:* it is the same dataset. **I could not check that the published
panel is pixel-identical.** Peer review may have changed n or the points. The preprint was "not certified by peer
review" (bioRxiv banner).

### 3.2 Fig 8B, pixel-calibrated read (`S28-D-D_fig_digitize.py`)

**Calibration.** The y-axis tick marks sit at pixel rows 136.0, 328.0 and 519.5 for 0.60, 0.40 and 0.20. That is
958.8 px per unit, with a maximum residual of 0.0002. One pixel is about 0.001 in length/SL.

**Box elements.** These are horizontal runs of the group colour at least 25 px long. **Isolated dots** are
connected components that are round and 15–120 px in area. Dots that overlap each other or a box line are missed,
so the dot extremes are a subset of the data.

| Genotype (n, read from panel) | Q1 | **median** | Q3 | isolated dots, min–max |
|---|---|---|---|---|
| wild type (7) | 0.211 | **0.223** | 0.243 | 0.198–0.285 |
| `nr21/+` (7) | 0.163 | **0.171** | 0.178 | 0.154 (1 dot isolated) |
| `lof/+` (35) | 0.438 | **0.463** | 0.478 | 0.340–0.545 |
| **`nr21/+; lof/+` (34)** | **0.449** | **0.463** | **0.488** | **0.434–0.534** |

The run detector also picked up two gray lines at 0.625 and 0.309. These are the panel frame and a significance
bar, not wild-type box elements. The authors mark `lof/+` vs double het as "n.s." **All values are figure-reads.**

**Cross-checks** (my inference). These are independent readings that agree; none is a further measurement.
- Wild type at 0.223 falls inside Praveenraj et al. 2017's wild *D. rerio* 18–26 % SL. That value is
  search-summary, carried from S22-D-D-D.
- It also falls inside S22-D-D's inferred 0.17–0.26.
- The proxy prediction for the double het, 0.36–0.43, was about 10–20 % low. The fold overgrowth actually read
  here is 0.463 / 0.223 = **2.08×**.

### 3.3 The input this exposes: spread-fin area

The length is now fixed, so the phenotype depends next on the **area rule**. At 0.463 SL (per fin, in SL² units):

| Area source | A/L² per fin | Level |
|---|---|---|
| S28 case C (AR 5 at span 2L + body width) | **0.523** | assumption |
| S28 case A (0.7 × L × 0.1 SL chord) | 0.151 | assumption |
| Fig 8A lateral image, authors' dashed outline of the **adducted** double-het fin (`S28-D-D_outline.py`, polygon of 37 vertices read by eye; L = authors' bracket, 148 px) | **0.134** (0.103 if L = outline extent) | figure-read, 1 fish |
| Fig 8A dorsal image, **partly abducted** double-het fin, bright-pixel planimetry (`S28-D-D_spread.py`, thresholds 150–180, pixel count vs row-filled) | **0.150–0.250** | figure-read, 1 fish |

**Caveats on these figure-reads:**
- Each is **one representative fish** chosen by the authors. That lateral fish's bracket/SL is about 0.50–0.53
  (eye-read SL, ±10 px), so it sits near the top of the distribution.
- The dorsal panel has no scale bar, which is why only the dimensionless A/L² is used.
- A fin photographed against a dark background may be tilted to the camera. Projected area is therefore a
  **lower bound on true planform**.
- Neither image shows a fin deliberately fanned to maximum. An actively fully fanned fin could exceed 0.25. *My
  inference:* reaching case C's 0.52 would need a fully webbed sector of about 60° at radius L. That is **2.1–3.5×**
  the planform in the partly spread image, and **3.9×** the folded outline.

## 4. Recomputation (`S28-D-D_calc.py`; all calculations)

The settings are those of S28-D: 45° launch, SL 3.0 cm, m 0.25 g, CL 1.07, CD0 0.08, Oswald e 0.8, and fins held
spread throughout the ascent. That last condition has never been observed.

**4.1 Phenotype at the measured length.** Values are % reduction in mean ascent deceleration.

| Area rule, L = 0.463 SL (median) | S (mm²) | 0.95 m/s | 1.38 m/s | 1.57 m/s | 2.11 m/s |
|---|---|---|---|---|---|
| case C (AR 5) | 202 | 2.49 | **5.11** | 6.51 | 11.03 |
| case C, IQR 0.449 / 0.488 | 191 / 222 | 2.37 / 2.73 | 4.86 / 5.58 | 6.19 / 7.08 | 10.53 / 11.93 |
| case A (length-only) | 58 | 0.76 | 1.59 | 2.05 | 3.63 |
| folded outline (A/L² 0.134) | 52 | — | 1.41 | 1.82 | — |
| **partly spread image, A/L² 0.150–0.250** | **58–96** | — | **1.58–2.58** | **2.03–3.31** | 3.61–5.82 |

The 0.95 and 2.11 m/s columns (Demesmay floor and +2 SD) are bounds, not central values.

**4.2 Sensitivity now** (median L, 1.38 m/s, case C baseline 5.11 %):

| Input | Change | Reduction (%) |
|---|---|---|
| fin length | measured IQR | 4.86–5.58 (±0.4 points, **no longer controlling**) |
| exit speed | ×0.5 / ×2 | 1.33 / 16.9 |
| mass | ×0.5 / ×2 | 9.64 / 2.63 |
| area rule | C → A or C → figure-read shape | 5.1 → 1.4–2.6 (a factor of **2–3.6**) |

- Exit speed and mass are the next-largest inputs at ×2. Exit speed is constrained within about ×1.14 (S28-D §1).
  Mass is **assumed** (0.25 g). Taking the isometric 3.6 cm / 0.43 g body instead gives 4.30 %.
- **The area rule is now the largest open input that is not pinned.**
- The spread factor over the folded outline needed for 2 % is k = 1.43 at 1.38 m/s, or 1.10 at 1.57 m/s. For 5 %
  it is k = 3.81 at 1.38 m/s, or 2.91 at 1.57 m/s.

**4.3 The negative.**
- At the measured length, take case C, the most generous fin (max point 0.534 SL), and the Demesmay +2 SD exit of
  2.11 m/s. The flight deficit is still **×1.80**.
- At the median length it is ×2.04, and ×2.74 at the 1.57 m/s mean.
- Under the figure-read area, V_to is 6.2–8.5 m/s, which is ×3.5–4.0 above 2.11 m/s.
- The best leap-range gain anywhere in §4 is 4.4 %, at case C, 0.534 SL and 2.11 m/s.
- No glide is possible below V_to. The skim limit set by the tail (52 Hz) is untouched, because it does not
  depend on fin length.

## 5. Verdicts

**S28's fin-length input: vindicated.** The extrapolated 0.45 SL is within 3 % of the figure-read median of 0.463.
This was an unsourced guess that happened to be right. I am not claiming the method was sound.

**S28-D's claims, item by item:**
- "Negative stands under ×2 on every input": **STANDS**. It is recomputed above with the measured length.
- "Most sensitive input is fin length": **was true while length was unknown. It is now superseded.** The measured
  IQR moves the effect by less than ±0.4 points. The controlling input is now the area rule.
- "S28's 0.45 SL is not supported by the primary source": **FALLS.** The primary source's plotted data support it.
  The text alone did not, and S28-D read the text correctly.
- "≤ 2.4 % if Fig 4B shows ≤ 0.25 SL": the condition **is not met** (all points > 0.43). The branch is moot.
- "≥ 0.4 SL needed for the 5 % upper value": the condition **is met**. Whether 5 % is reached now depends on area.
- "Plausibly 1–3 %": **STRENGTHENS.** With the measured length and the only spread-fin planform the source shows,
  the result is 1.4–2.6 % at 1.38 m/s and 1.8–3.3 % at 1.57 m/s (calculated). The 5 % value requires a case-C
  planform that no image supports.
- "Detectability unestablished": **STANDS**, unchanged. It still turns on unobserved in-air fin abduction.

**Overall: STRENGTHENS.** A figure-read primary datum replaces an `unknown`. S28-D's conclusion, a robust negative
with a conditional phenotype of about 1–3 %, survives it. The correction is to *why* the phenotype is small. It is
small because the fin is narrow, not because it is short. The fin is as long as S28 assumed: the elongation is
length-dominated, with A/L² ≈ 0.13–0.25 against 0.52 for an AR-5 wing. That matches S28's own remark that case A is
"closest to what *longfin* is known to do".

## 6. What would settle the remaining input, and cost

1. **Spread-fin planform of the double het.** Anaesthetise the fish, fan the pectoral fully with a probe, and take
   one calibrated dorsal photograph per fish, about 10 fish. This is the experiment S28 and S28-D already
   recommended, and it is now *better targeted*: length is known, so only A/L² is in question.
   - **Decision rule (calculated):** A/L² ≤ 0.25 means ≤ 2.6 % at 1.38 m/s; close the aerodynamic line as
     below 3 %. A/L² ≥ 0.40 is needed before about 4 % appears at 1.38 m/s.
   - **Cost:** hours, plus access to the existing line. The cost is unsourced, carried over from S28.
2. **Same-session high-speed leap video** (≥ 1000 fps). Is the fin abducted in air, and what is its projected
   area in flight? That is the quantity that actually enters the lift equation (challenge 195's point).
3. **Per-fish Fig 4B/8B values with SL.** One email to the corresponding author, M. P. Harris. This would remove
   the residual digitising error (about ±0.003) and the preprint-vs-published uncertainty.

## 7. Disagreements preserved

- **Area.** Case C (AR 5) is S28's headline. Case A and both figure-read outlines are 2–4× smaller. I do not
  average them. I report the figure-read range and, separately, the case-C ceiling.
- **Preprint vs published figure.** These may differ. Only the preprint was read.
- **Proxy vs reading.** The S22-D-D proxy Rz was 0.36–0.43 SL; the reading is 0.463. The proxy was low by
  7–22 %.
- **Exit speed.** These two in-water escape peaks are kept separate (carried from S28-D, not re-read). Neither is
  a measured exit speed.
  - Miln 2021 max: 1.38 m/s (listing).
  - Demesmay 2025: 1.57 ± 0.27 m/s (listing via S20-D-D-D).

## 8. Sources

| Source | Read-level |
|---|---|
| S28-organism.md @ e8ba4191; S28-deepen.md and S28-deepen_calc.py @ 511ecf7b | full-text (repository) |
| challenge-195.md, challenge-202.md; S22-D-D-deepen.md on `deepen-s22-d-d-input-vncsjh` and `deepen-s22-d-d-j5x0vq` | full-text (195, 202); search excerpts of the S22 files (repository) |
| Daane JM et al. 2021, bioRxiv 10.1101/2021.03.05.434157 v1, *Novel regulators of growth identified in the evolution of fin proportion in flying fish*, PDF sha256 `d5096d02…6c40` | **full-text, including the Fig 8 raster** (text searched for Fig 8 and Fig 5 legends; figure digitised) |
| Daane JM et al. 2021, *Curr Biol* 31:5052, PMC9172250 | listing this session (article HTML fetched for figure links). Fig 4 image, Data S1, Supplement PDF: could-not-access. Legend text relayed via S28-D (full-text there) |
| Europe PMC search record PPR293816 | listing |
| Praveenraj et al. 2017 pectoral %SL | search-summary (via S22-D-D-D) |
| Miln 2021; Demesmay 2025 | listing (via S28-D) |

```swarm-result
{"subproblem": "S28-D-D", "evidence": "figure-read (pixel-calibrated digitisation of Daane et al. 2021 bioRxiv preprint Fig 8B, the same measurement as Curr Biol Fig 4B, n = 34 double heterozygotes) plus figure-read planimetry of two single-fish fin outlines in Fig 8A; all aerodynamic consequences calculated with S28-D's unchanged model", "answer": "S28-D's most sensitive input, pectoral fin length per fin, is now read from the primary figure as 0.463 SL (IQR 0.449-0.488, n=34) in the lat4a nr21/+; kcnh2a lof/+ double heterozygote, which vindicates S28's unsourced 0.45 SL, excludes S28-D's short-fin branch, and moves control of the phenotype to spread-fin area. The only planforms the source shows (A/L^2 = 0.13-0.25 per fin, against 0.52 for S28's AR-5 case) give a calculated 1.4-2.6% ascent-deceleration reduction at 1.38 m/s (1.8-3.3% at 1.57 m/s), and 5% only under the unsupported AR-5 area. So S28-D's 'robust negative, plausibly 1-3% phenotype' strengthens, and its claim that 0.45 SL is unsupported by the primary source falls.", "key_number": "double-heterozygote pectoral fin length / SL = 0.463 per fin (median; IQR 0.449-0.488; points 0.434-0.534; n = 34), wild type 0.223 (n = 7) -- figure-read, Daane 2021 preprint Fig 8B; derived fin planform shape factor A/L^2 = 0.13-0.25 per fin (figure-read, 1 fish each)", "verdict": "strengthens", "depends_on": ["S28-D conclusion and model: docs/research/fish/S28-deepen.md and S28-deepen_calc.py @ 511ecf7b", "S28 conclusion and inputs: docs/research/fish/S28-organism.md @ e8ba4191", "Daane et al. 2021 bioRxiv 10.1101/2021.03.05.434157 v1 Fig 8B pectoral length/SL by genotype (figure-read, PDF sha256 d5096d02d6d154ee8843ae13aeb82df2bbeeb77e567622872abbb13927ed6c40)", "assumption: preprint Fig 8B equals published Curr Biol 31:5052 Fig 4B (same legend; published image could-not-access)", "digitisation calibration: ticks 0.60/0.40/0.20 at px 136.0/328.0/519.5, 958.8 px per unit", "Fig 8A lateral dashed outline of adducted double-het pectoral, A/L^2 0.134 (bracket L) / 0.103 (extent L), one fish (figure-read)", "Fig 8A dorsal partly abducted double-het pectoral, A/L^2 0.150-0.250, one fish, no scale bar (figure-read)", "assumption: photographed projected area approximates in-air planform (unmeasured; lower bound if fin tilted)", "S28 case-C geometry: AR 5 at span = 2*L_fin + 4 mm (assumption)", "S28 case-A geometry: chord 0.1 SL, 0.7 fill (assumption)", "S28 body: SL 3.0 cm, m 0.25 g (assumed, back-solved)", "isometric alternative SL 3.6 cm, m 0.43 g (inference from Plaut 2000 abstract via S28-D)", "Miln et al. 2021 burst max 1.38 m/s (listing via S28-D)", "Demesmay et al. 2025 escape peak 1.57 +/- 0.27 m/s, floor 0.95, +2SD 2.11 m/s (listing via S28-D/S20-D-D-D)", "assumption: exit speed ~= in-water escape peak (unmeasured)", "CL 1.07 quasi-steady (project-derived; challenge 195 flags unverified at Re ~300-600)", "CD0 0.08, Oswald e 0.8, body drag CD 0.3 on 24 mm2 scaled with SL^2 (assumptions)", "launch angle 45 deg (assumed)", "assumption: fins held spread in air throughout ascent (never observed)", "law: point-mass trajectory with quasi-steady lift L = 0.5 rho V^2 S CL and drag CD0 + CL^2/(pi e AR)", "S28 tail-beat limit 52 Hz and taxi requirement 132-199 Hz (negative skim clause; measured/derived, untouched)", "challenge 194: S28's 5-10% was L/W; ascent-decel reduction is the correct metric", "challenge 195: photographic area is a proxy for in-flight projected area", "cross-check: wild-type 0.223 vs Praveenraj et al. 2017 wild D. rerio 18-26% SL (search-summary via S22-D-D-D)", "cross-check: S22-D-D proxy Rz 0.36-0.43 SL vs read 0.463"]}
```
