# S9-D-D: Deepening S9-D by attacking its weakest input, the clamp behind the zebrafish fin EI

Project: `zebrafish-flight` · Scale: tissue · Date: 2026-11-04

**Parents.** Neither parent is on this branch.

- S9: `docs/research/fish/S9-tissue.md`, on `origin/claude/s9-fin-ray-materials-t0royp`.
- S9-D: `docs/research/fish/S9-deepen.md` and `S9-deepen_calc.py`, on `origin/claude/deepen-s9-fin-ray-ixdx5u`.

**Calculation script:** `docs/research/fish/S9-D-deepen_calc.py`. Every number it prints is a
**calculation**, not an observation.

**Read-levels:** full-text | abstract | listing | search-summary | could-not-access.

---

## 0. What S9-D concluded

This task's prompt left the "recorded answer" field empty, so I took S9-D's answer from its own
swarm-result block. S9-D made four claims:

1. S9's key number (bluegill fin-ray E = 1.34 GPa) **falls**. Every fin-ray "modulus" is
   E = EI / I with an assumed I. With the same measured EI, the implied E ranges from ~3 MPa to
   ~11 GPa, depending on how the two hemitrichs are coupled.
2. So a bare E should not be used at the organ scale. Organ-scale work should **carry the measured
   flexural stiffness instead**: the whole zebrafish caudal fin **EI = 1.5–4 × 10⁻⁹ N·m²** (Puri et
   al. 2018, in vivo), or about 0.8–2.5 × 10⁻¹⁰ N·m² per ray.
3. Under the uncoupled thin-plate model, with hemitrich wall thickness t = 11–16.5 µm, the implied
   ray-bone E is ≤ 0.6–11 GPa. That is below the ~23–25 GPa from zebrafish vertebral
   nanoindentation. S9-D proposed three explanations: joint compliance, flatter crescents, or
   foam-pad compliance at the root. It flagged the last one as its own hypothesis and left it untested.
4. Nothing is known about strength, density or actinotrichia.

## 1. The input S9-D's answer is most sensitive to

**It is the boundary condition behind Puri et al.'s EI: the assumption that the fin is rigidly
clamped at the fixation point p0.**

Puri et al. did not measure EI directly. They measured a force–deflection slope F/y at a span L, and
converted it using the clamped-free cantilever formula (their Eqn 3; full-text):

> EI_app = (F/y) · L³ / 3, with L measured "from the fixation point to the loading point".

The fish's peduncle is held by "two opposing foam pads" (Fig. 1E; supplementary Fig. S2: "soft
synthetic foam pads"). That is full-text, and it is the authors' description. The fixation point p0
sits at the base of the fin (supplementary Fig. S4, full-text).

Why this input, and not S9-D's other candidates (sensitivities computed by the script; calculation,
not observation):

- **EI_app ∝ L³ about an assumed clamp origin.** If the effective clamp sits δ proximal of p0, the
  true EI is larger by (1 + δ/L)³:
  - an offset of **0.34 mm doubles EI at the shortest span (L = 1.3 mm)**;
  - an offset of 0.78 mm doubles it at L = 3 mm.
  - Any root compliance in series, whether translational, rotational or shear, acts in the same
    direction.
  - Every number in S9-D's key_number inherits this sensitivity, including the per-ray EI.
- **What a factor of two would change.** S9-D's claim 3 ("uncoupled-plate E sits below bone
  E") would weaken or reverse:
  - With EI doubled, the t = 11 µm, D = 100 µm envelope rises from ≤ 11 to ≤ 22 GPa. That reaches
    vertebral bone E.
  - With EI ×4, the t = 11 µm bound reaches 31 GPa (section 6 of the script). That exceeds bone, so
    the fully uncoupled model would be ruled out.
  - So the absolute EI is what decides between S9-D's coupling models. Only a factor of ~100 in EI
    would rescue the bonded-tube model.
- **Runner-up: hemitrich thickness t** (E ∝ t⁻³). It controls the *derived* E, but S9-D's
  recommended number is EI, which does not depend on t at all. S9-D's own recommendation therefore
  insulates its answer from t. It does not insulate it from the clamp.

## 2. How well is that input established?

**Evidence level of S9-D's key number:** measured force and deflection (calibrated). These are
converted to EI under a **boundary condition that is assumed, not measured**.

- **Calibration exists, but it does not test the fish boundary.** Puri et al. benchmarked steel and
  polyimide cantilevers and recovered 200 ± 10 GPa and 2.0 ± 0.3 GPa (full-text). They do not say
  how those strips were clamped. Nothing in the text or the supplement (both full-text) tests the
  foam-pad peduncle mount, measures root rotation, or measures root translation.
- **The authors' own data show the signature of root compliance.** Supplementary Fig. S5C
  (full-text; values read off the plot by me) plots E_eff = EI_app / I_rays(L). I_rays already
  removes the ray taper (their Fig. S5B decreases monotonically). Even so, E_eff **rises with span
  in all five fish, roughly 1.2–3.7×, and then levels off or falls**. In a rigidly clamped,
  uniform-material beam, E_eff would be flat.
  - **Authors' claim:** the stiffness peak "cannot be readily explained from geometry" and
    "coincides with the position of the first bifurcation" of the rays.
  - **My inference, not theirs:** a compliant root in series also produces a rise that saturates,
    with no change in material at all.
- **The abstract's range understates the plotted data.** This is a reading of the plots, not a
  re-measurement.
  - Abstract (full-text): "1.5×10⁻⁹–4×10⁻⁹ N m²".
  - Fig. 2C, intact fins, my reading: ~0.95 × 10⁻⁹ (fish 11, L ≈ 1.7 mm) up to ~4.35 × 10⁻⁹
    (fish 12, L ≈ 3 mm).
  - Fig. 2F, interray-disrupted fins (a partly different set of fish; only fish 5 appears in both), my reading: up to ~7 × 10⁻⁹ (fish 17,
    L ≈ 3.2 mm).
  - The authors report no significant intact-vs-disrupted difference. I preserve both ranges and do
    not average them.
- **No independent replication was found.** Scope of the search:
  - Europe PMC "cited-by" list for Puri 2018 (PMID 29246971): 16 records, titles screened. The one
    same-lab follow-up, Dagenais et al. 2021, *J. Exp. Biol.* (PMID 34338301), was read at
    abstract level. It reports hydrofoil flow, not fin stiffness.
  - Two Europe PMC keyword searches: zebrafish + caudal fin + bending/flexural stiffness (15 hits);
    zebrafish + fin ray + three-point bending/nanoindentation/flexural rigidity (32 hits). Titles
    screened.
  - Result: **no second measurement of zebrafish fin EI and no characterization of the mount
    compliance.**
  - Not searched: Scopus, Web of Science, theses.

**Verdict on the input.** A measurement wrapped in an untested assumption, and the authors' own
supplementary data argue against that assumption. It has been cited as "measured EI", including by
S9-D, without that caveat.

## 3. Improving it: refit Puri's own data with a compliant root

There is no primary source that measures the mount compliance (negative result, scope as in §2). So I
improved the input from the primary data itself. I digitized Fig. S5C (5 intact fish, 6 spans each)
and Fig. S5B at 300 dpi from the full-text supplement. The readings are mine, ±0.1 mm and
±0.15 MPa. I then fitted each fish's **rising limb**, the points up to its maximum, with:

    y/F = L³/(3 E I) + [L²/k_rot] + [1/k_trans] + [L/(κGA)]
    ⇒ E_app(L) = E_∞ / (1 + a/L + b/L³ + c/L²)

All results below are **calculations**:

| fish (n pts) | constant E (rigid clamp) rmse, MPa | translational root: E_∞, rmse | shear term: E_∞, rmse | rotational only |
|---|---|---|---|---|
| 13 (5) | 1.82 | 11.9 MPa, 0.79 | 15.7 MPa, 0.69 | runs to grid edge (a unconstrained) |
| 12 (4) | 2.34 | 11.4 MPa, 0.30 | 15.0 MPa, 0.44 | runs to grid edge |
| 5 (5) | 2.92 | 12.1 MPa, 0.18 | 15.3 MPa, 0.30 | runs to grid edge |
| 4 (2) | 0.54 | 8.7 MPa, 0.01 | 9.7 MPa, 0.00 | 2 points only; not informative |
| 11 (4) | 1.11 | 6.1 MPa, 0.06 | 9.1 MPa, 0.04 | runs to grid edge |

What the fits show:

- **The rigid-clamp model does not fit the rising limb.** Its rmse is 1.1–2.9 MPa, against a reading
  error of ~0.15 MPa.
- **A series compliance does fit.** Either a translational term (b/L³) or a shear term (c/L²) fits to
  within reading error in 3 of the 4 informative fish. The exception is fish 13, which has a
  non-monotonic dip at 2.3 mm.
- **A pure hinge (rotational spring) cannot produce the observed rise** in fish 12, 5 and 11. Under a
  pure hinge the ratio E_app(L₂)/E_app(L₁) can never exceed L₂/L₁. The observed ratios are 2.51, 3.65
  and 2.58, against ceilings of 2.31, 3.14 and 2.06.
- **The implied translational root stiffness is k ≈ 0.8–4.4 N/m.** That is comparable to the measured
  F/y at the shortest spans, ~0.6–2.5 N/m (read off Fig. 2B). So at L ≈ 1.3–1.7 mm, roughly half or
  more of the deflection Puri measured would be root deflection, not fin bending. This is an
  inference from the fit.

**What the fit cannot separate (preserved, not resolved).** Three readings remain, and the shape of
the rising limb does not tell them apart:

- **(i) Foam/peduncle root compliance.** This is a measurement artefact. EI_app is a lower bound.
- **(ii) Shear compliance of the soft collagenous core between the hemitrichs.** This is real
  biology. It is length-dependent partial coupling. In that case EI_app at short span is real
  *structural* stiffness, but it is not a beam EI.
- **(iii) A genuine proximal-to-distal rise in ray E up to the first bifurcation.** This is the
  authors' interpretation.

(i) and (ii) predict the same functional form. (iii) can fit anything, by construction. The
**descending** limb beyond ~3.5–4.5 mm is not explained by (i) or (ii). It needs either a distal
drop in E or an I(L) that falls faster than Fig. S5B shows.

**What would settle it, and what it would cost (my estimates, not quoted prices):**

1. **Track the fin base at p0 during loading.** Use Puri's existing side camera (camera 1 in Fig. 1C)
   or a second marker. Translation or rotation at p0 measures k_root directly. If the raw videos
   exist, this is a reanalysis, at roughly zero marginal cost. Otherwise it is a few rig-days on an
   existing setup.
2. **Repeat the spans with a rigid mount.** Use a cyanoacrylate-bonded or 3D-printed clamp at the
   hypural plate, on euthanized or excised fins. Compare against the foam mount on the same fins. If
   E_eff becomes flat in L, reading (iii) falls. If it stays rising, reading (ii) remains. Cost: about
   a week of rig time plus ~10 fish.
3. **Do a two-point deflection on one load.** Measuring y at two spans under one load separates the
   L², L³ and constant terms. No new hardware is needed beyond a second displacement readout.

## 4. Recompute S9-D's conclusion with the improved input

Corrected whole-fin EI = E_∞ × I_rays(L) over the measured spans. This is a **calculation**:

| | Fin EI over spans (N·m²) | Upper end vs S9-D's 4 × 10⁻⁹ |
|---|---|---|
| Puri, as reported (abstract) | 1.5–4 × 10⁻⁹ | — |
| Puri, my plot reading, intact | 0.94–4.35 × 10⁻⁹ | ×1.09 |
| Corrected, translational root | **2.1–6.0 × 10⁻⁹** | ×1.51 |
| Corrected, shear term | **3.2–7.8 × 10⁻⁹** | ×1.96 |
| Corrected, rotational + translational | up to 1.7 × 10⁻⁸ | ×4.2, **driven by fish 13's unconstrained fit; not reliable** |

Effect on each S9-D claim:

- **Claim 1 (S9's 1.34 GPa falls): STANDS.**
  - The model-choice span (~900×) is far larger than this ≤2× correction.
  - The bonded-tube model still over-predicts fin EI. Before correction it was 80–220× too stiff.
    After correction it is still ~55–160× too stiff (calc: 3.3 × 10⁻⁷ against 2.1–6.0 × 10⁻⁹).
- **Claim 2 (carry EI, not E): STANDS, with a revised number and a revised status.**
  - The number to carry is **~2–8 × 10⁻⁹ N·m² for the whole fin** (calc, root-compliance
    corrected). S9-D's 1.5–4 × 10⁻⁹ is a **rigid-clamp lower bound**, not a value.
  - At the shortest spans the correction is ×1.3–5. At the peak it is ×1.1–1.9.
  - The fish-to-fish spread narrows from ~4.6× (0.94–4.35) to ~2.5–2.9×.
  - For organ-scale use, one point matters. If the design question is "how does the fin deflect when
    attached to a body", the root compliance may be *biologically real* (peduncle, hypural joint).
    In that case the uncorrected F/y(L) curve is the right input, and EI should not be used at all.
    Which of the two applies is a design decision, and it should be stated wherever the number is
    used.
- **Claim 3 (uncoupled-plate E sits below bone E): WEAKENED, not refuted.**
  - With the corrected EI, the t = 11–16.5 µm, D = 150 µm, uncoupled flat-plate upper bound becomes
    **≤ 3.4–11 GPa** (translational) or **≤ 4.4–15 GPa** (shear). S9-D had 2.2–7.5 GPa.
  - The gap to the 23–25 GPa vertebral nanoindentation narrows from ~3–11× to ~1.6–7×.
  - Root compliance therefore explains **part** of S9-D's puzzle, but not all of it. The remainder
    needs joint compliance, a curved crescent I, or a genuinely lower fin-ray bone E.
  - The vertebral E is still search-summary only (S9 B3/B4). So this comparison is no firmer than
    that read.
- **Claim 4 (strength, density, actinotrichia unknown): STANDS.** These were not re-searched, and
  S9's search scope still applies.
- **New, against the primary source.**
  - The authors' claim that a stiffness *peak* coincides with the first bifurcation is **not
    established** by their data. The proximal rise is explained to within reading error by a series
    compliance with constant E. This is a calculation, on 2–5 points per fish.
  - The distal decline is not explained by that compliance and remains open.
  - This is my inference. It challenges the authors' interpretation; it does not refute it.

**Overall verdict for S9-D: STANDS.** Its qualitative answer survives: S9 falls, and organ-scale
work should carry the measured EI and not E. Its key number moves up by ~1.5–2× and must be relabelled
as a rigid-clamp lower bound.

## 5. What this does NOT establish

- **It does not show that the foam mount is compliant.** The fit shows that a series compliance is
  *sufficient* to explain the rise. It does not show that it is the cause. Core shear (biology) fits
  equally well.
- **It does not rest on author-tabulated data.** Every Fig. S5B/S5C value is my reading of a raster
  plot. The fits have 2–5 points and 2 free parameters per fish, so they have 0–3 degrees of freedom.
- **Constant I across each fitted range is my simplification.** Fig. S5B varies by ≤10% over
  1–3 mm, so this matters less than the reading error.
- **It does not re-read S9-D's other inputs.** The hox13 hemiray thickness (PMC12956070), the Das
  et al. 2023 coupling claim (abstract) and the S9 vertebral E (search-summary) are taken at S9-D's
  stated read-levels. I did not re-open them in this session.
- **It says nothing about the descending limb, about hydrated vs dry properties, or about
  dynamic (frequency-dependent) stiffness.** Puri's test was quasi-static.

## Sources

- **Puri S, Aegerter-Wilmsen T, Jaźwińska A, Aegerter CM (2018).** In vivo quantification of
  mechanical properties of caudal fins in adult zebrafish. *J. Exp. Biol.* 221:jeb171777.
  PMID 29246971, PMC5868929.
  - **Full-text:** article XML and Fig. 2 image, plus the supplementary PDF (Figs. S1–S6), via the
    Europe PMC REST `fullTextXML` and `supplementaryFiles` endpoints.
  - Quantitative values from Figs. 2B, 2C, 2F, S5B and S5C are **my plot readings**.
- **Dagenais P et al. (2021).** Hydrodynamic stress and phenotypic plasticity of the zebrafish
  regenerating fin. *J. Exp. Biol.* PMID 34338301. **abstract** (no stiffness measurement).
- **Jimenez YE, Lucas KN, Long JH, Tytell ED (2023).** Flexibility is a hidden axis of
  biomechanical diversity in fishes. *J. Exp. Biol.* PMID 37086034. **abstract** (review; no
  zebrafish fin EI).
- **Inherited from S9-D, not re-read here:**
  - hox13 triple mutant, *PLoS Genet.* 2026, PMC12956070 (S9-D: full-text, plot reading);
  - Das, Hannard & Barthelat 2023, *Acta Biomater.*, PMID 37364788 (S9-D: abstract);
  - Lauder et al. 2011 (S9: search-summary);
  - zebrafish vertebral nanoindentation, Fiedler et al. 2018 and one unresolved study (S9:
    search-summary).

```swarm-result
{"subproblem": "S9-D-D", "evidence": "literature (Puri 2018 full-text incl. supplement; values are my plot readings) + calculation (series-compliance refit); no independent replication found",
  "answer": "S9-D's answer (S9's 1.34 GPa falls; carry measured fin EI rather than E) stands, but its key number rests on an untested rigid-clamp assumption at a foam-pad mount: Puri's own supplementary E_eff rises 1.2-3.7x with span in all five fish, a rigid-clamp/constant-E model misfits (rmse 1.1-2.9 MPa vs ~0.15 MPa reading error) while a series root or core-shear compliance fits within reading error, so the reported 1.5-4e-9 N m^2 is a lower bound and the corrected whole-fin EI is ~2-8e-9 N m^2 (calculated), which narrows but does not close S9-D's gap between uncoupled-hemitrich E and vertebral bone E.",
  "key_number": "zebrafish whole caudal fin EI ~2.1-7.8e-9 N m^2 (calculated, series-compliance-corrected from Puri 2018 Fig. S5B/S5C plot readings); reported rigid-clamp value 1.5-4e-9 N m^2 is a lower bound; per ray ~1.2-4.9e-10 N m^2 (calc, /16-18 rays)",
  "verdict": "stands",
  "depends_on": [
    "Puri et al. 2018 J Exp Biol 221:jeb171777 force-deflection data (Fig. 2A-C) and EI = (F/y) L^3/3 conversion, full-text",
    "Puri et al. 2018 Fig. S5B ray-only I_eff(L) 0.28-0.50e-15 m^4, my plot reading",
    "Puri et al. 2018 Fig. S5C E_eff(L) for 5 intact fish, my plot reading (+-0.1 mm, +-0.15 MPa)",
    "Puri et al. 2018 Fig. 2F disrupted-fin EI up to ~7e-9 N m^2, my plot reading",
    "Fixation by foam pads on the peduncle with L measured from p0 (Puri 2018 Fig. 1E, S2, S4), full-text",
    "Euler-Bernoulli cantilever with series compliance model y/F = L^3/(3EI) + L^2/k_rot + 1/k_trans + L/(kGA)",
    "Constant I within each fish's rising-limb fit range (my simplification)",
    "16-18 rays per caudal fin (Puri 2018)",
    "S9-D: model-choice span of implied ray E ~3 MPa to ~11 GPa and bonded-tube forward check (S9-deepen_calc.py)",
    "S9-D: hemitrich wall thickness t = 11-16.5 um, zebrafish dorsal fin micro-CT, PMC12956070 Fig. 7E (not re-read here)",
    "S9-D: uncoupled-hemitrich coupling claim, Das, Hannard & Barthelat 2023 Acta Biomater PMID 37364788 (abstract; not re-read here)",
    "S9 B3/B4: zebrafish vertebral nanoindentation E ~23-25 GPa (search-summary only)",
    "S9 L1: bluegill proximal fin-ray E 1.34 GPa, Lauder et al. 2011 (search-summary only)",
    "Negative search: no independent zebrafish fin EI replication or mount-compliance characterisation (Europe PMC cited-by of PMID 29246971, 16 records; two keyword searches, 47 hits; titles screened)"
  ]}
```
