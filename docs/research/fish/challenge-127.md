# Challenge 127: adversarial review of S9-D-D (hemitrich wall thickness; "verdict strengthens")

Claim under review. Author: S9-D-D, commit `cd18bca3`, `docs/research/fish/S9-D-deepen.md`.

> "S9-D's most sensitive input is hemitrich wall thickness t (E ~ t^-3; a factor-2 error flips its
> 'tissue E cannot reproduce in-vivo EI' conclusion), and replacing its 7.1-um-voxel dorsal-fin value
> (11-16.5 um) with a confocal caudal-fin measurement (~19-20.4 um, n=2 fish) lowers the implied
> uncoupled-plate ray modulus to ~0.15-3.5 GPa, leaving tissue-level E (>=23 GPa) 7-141x too stiff to
> reproduce Puri's measured fin EI, so S9-D's conclusion to carry measured EI rather than any E stands
> and becomes harder to overturn." Recorded evidence level: literature.

Date: 2026-11-04. Read-level legend: full-text | abstract | listing | search-summary | could-not-access.
Labels used in this file:
- **calc**: I computed it.
- **author**: S9-D-D or a cited paper states it.
- **inference**: my own reasoning.
- **my pixel reading**: a measurement I took off a published figure image.

**Verdict: WEAKENED.**
- **What stands.** The headline recommendation, "carry measured EI, not a bare E", survives every
  attack below. It also held under S9-D's original t.
- **What does not survive.** The upgrade is not supported: "becomes harder to overturn" and
  "tissue E is 7–141× too stiff".
  - The replacement t is not clearly better than the old one. The source paper's own representative
    image, scaled with its own geometry bars, gives a wall of ~12–14 µm. That is about S9-D's old value.
  - The ≥23 GPa reference is a dry or embedded nanoindentation figure from a different bone.
  - Under either correction alone, the margin at the flat-plate corner falls back to ≈1.4–4.5×.

---

## 1. Independent arithmetic (calc)

I did not reuse the author's script. I wrote my own expressions:
- per-ray EI = EI_fin / N;
- uncoupled flat hemitrich pair, I = 2·w·t³/12;
- E = EI_ray / I.

| Quantity | Inputs | My value (calc) | Claim |
|---|---|---|---|
| EI per ray, low / high | 1.5e-9/18, 4e-9/16 | 8.33e-11 / 2.50e-10 N m² | ✔ |
| Most-generous corner, S9-D t | EI_hi, w = 100 µm, t = 11 µm | 11.3 GPa | ✔ |
| Same corner, t × 0.5 | t = 5.5 µm | 90 GPa (> 23: flips) | ✔ |
| Envelope, t = 16.3–25.3 µm, w = 100–200 µm | | 0.154–3.46 GPa | "0.15–3.5" ✔ |
| Envelope, t = 19.0–20.4 µm | | 0.29–2.19 GPa | ✔ |
| Forward check, E = 23 GPa, 17 rays, t = 16.3 µm, w = 100 µm, vs 4e-9 | | 7.1× | "7×" ✔ |
| Forward check, t = 25.3 µm, w = 200 µm, vs 1.5e-9 | | 141× | ✔ |
| t below which E ≥ 23 GPa is needed (EI_hi, w = 100 µm) | | 8.67 µm | "8.7" ✔ |

**No arithmetic error found.** Every number in the claim follows from its stated inputs.

## 2. Proxy check: is "Azevedo bone thickness" the wall thickness that matters?

I read Azevedo et al. 2011 (*PLoS One* 6:e22820, PMC3145768) at **full-text**, from the Europe PMC
XML, and the Fig. 4 image, fetched from journals.plos.org at 2306×1425 px.

### 2a. The author's "internal consistency check" is a definition, not a check

- **Author (S9-D-D §3):** "2t + intra-ray space = 126 µm and 101 µm. That matches the separately
  plotted fin thickness to within 3 µm, so the bars are internally consistent."
- **Author (Azevedo, full-text):** "the overall fin thickness, **which is the sum of the bone thickness
  and the intra-ray space**".

So Fig. 4P/Q is not measured separately. Their agreement to within 3 µm is arithmetic plus plot-reading
error. It is not evidence that t is right.

The same quote gives a second problem. Azevedo's "fin thickness" excludes the epidermis. Fig. 4I
shows a multi-cell DAPI+ epidermis outside both hemirays. Puri's calliper thickness (200→40 µm)
includes it. *Inference:* the author's statement that the fin thickness "falls inside Puri's calliper
range" compares two different quantities.

### 2b. The paper's own representative image does not reproduce the plotted t

The figure has no scale bar. I therefore scaled Fig. 4I (uncut, proximal) with the paper's own
plotted geometry.

**My pixel reading,** at 3× upscale of panel I, measured on vertical lines where the crescent wall
runs roughly horizontal:

| Feature | Pixels |
|---|---|
| Wall, between the green Zns5 lines | ~46–50 px (unlabelled dark band) |
| Inner-to-inner distance between hemirays, at mid-ray | ~353 px |
| Outer-to-outer distance | ~452 px |

Wall-to-intra ratio:
- image: 50/353 = **0.14**;
- plotted bars: 20.4/85 = **0.24**.

Implied wall thickness (calc):
- scaled to the plotted intra-ray space of 85 µm: **~12 µm**;
- scaled to the plotted "fin thickness" of 125 µm: **~14 µm**.

Caveats on this reading:
- It is one section of one ray, and it may not be a measured one.
- Edge blur is about ±5 px, roughly ±1.3 µm.
- The intra-ray space of a curled crescent is ambiguous.
- If Azevedo measured the bone from the outer edge of one Zns5 osteoblast layer to the outer edge of
  the other, the wall gains ~6 px, which is still only ~13–15 µm.
- The methods do **not** state the boundary used for bone thickness (full-text checked).

*Inference:* the paper's illustration is consistent with **S9-D's original 11–16.5 µm**, not with
19–20.4 µm. The 1.2–1.9× "disagreement" that S9-D-D preserved may partly be a gap between the bars
and the image within Azevedo itself. This does not show the bars are wrong. It shows that "confocal,
therefore better than micro-CT" is not established by this source.

The osteoblast-inclusion worry, checked and **not** sustained: Zns5 is a thin (~1–2 µm) green line
on each face, and the matrix is the unlabelled dark band. So any inflation from that cause is small.

### 2c. Statistics

- **Author (Azevedo, full-text):** "2 uncut controls" and "5–9 bony rays" per fin. The legend gives
  no error-bar type and no n.
- *Inference:* the bars are probably pooled over hemirays: about 20–36 measurements from 2 fish,
  which is pseudoreplicated. If the bars are SD across hemirays, then individual walls at mean − 2 SD
  ≈ **10.6 µm** (proximal) are within the distribution. That assumes normality; the type is unknown.
- The claim's "±bar" envelope (16.3–25.3 µm) is therefore not a confidence interval on the fish mean.

### 2d. Age

- The author infers that the uncut controls were "~2 yr" old.
- **Author (Azevedo, full-text):** the protocol started at 1 year, "three amputations every month",
  and Fig. 4 compares against "uncut age-matched siblings" of the **14-cut** fins.
- *Inference:* 14 cuts at 3 per month is about month 5, so the fish were ~17 months old. That is
  still older than Puri's 6–12-month fish.
- The author already says the direction is that younger fish have thinner walls and higher E. I agree.
- Separately, the fish were kept at 30 °C (full-text), not the standard 28 °C.

## 3. Hidden assumption 1: the "most sensitive input" is a flat-plate artifact

- The ranking "t is most sensitive, E ∝ t⁻³" holds only inside the uncoupled **flat-plate** model.
  Challenge 88 already showed (calc) that for crescents, E ∝ t^-1.07 (semicircle) to t^-1.31 (60°).
- Fig. 4I, which S9-D-D cites as agreeing with S9-D, shows **deeply curled crescents, at or beyond a
  semicircle**. For that geometry the controlling inputs are crescent depth and arc angle, not t.
- *Inference:* the flat plate is the minimum-I bound, so testing conclusion 4 at that corner is a
  legitimate worst case. But calling t "S9-D's most sensitive input" without saying "within the
  flat-plate bound" overstates it.
- Under the observed crescent shape, conclusion 4 holds by a wide margin **whatever t is**:
  30–490 MPa (challenge 88, calc). That supports "carry measured EI" independently of this claim's
  new input.

## 4. Hidden assumption 2: the ≥23 GPa tissue reference

The forward check depends linearly on E_tissue = 23 GPa. That value is zebrafish **vertebral**
nanoindentation, held at search-summary level in S9 and never re-read.

Counter-evidence, from one standard web search (search-summary):
- **Hydration.** In equine cortical bone, nanoindentation E rose from 11.7 ± 1.7 GPa (wet) to
  15.0 ± 2.2 (dehydrated) to 19.4 ± 2.1 GPa (embedded) (Cambridge *J. Mater. Res.* listing). If the
  23–25 GPa is dry or embedded, which is unknown, the wet-tissue value could be ~0.6× lower.
- **Fin-ray models.** A fin-ray curvature-stiffening model (Nguyen et al., arXiv 1608.05891) uses
  E_bone = 4–20 GPa for fin-ray bone, citing earlier studies. That is a search-summary of the PDF; I
  did not verify the method behind its sources.
- **Negative result, scope stated.** I found no direct nanoindentation E for teleost hemitrichs or
  lepidotrichia. That rests on 1 standard web search, plus S9-D-D's Europe PMC scope, which did not
  target mechanics.

Recompute (calc), forward check at the flat-plate minimum-I corner (w = 100 µm, 17 rays, compared
with EI = 4e-9 N m²):

| t | E = 23 GPa | E = 11.7 GPa (wet, equine analog) | E = 4 GPa (low end of 4–20) |
|---|---|---|---|
| 12 µm (Fig. 4I reading) | 2.8× too stiff | 1.4× | **0.49× (reproduces EI)** |
| 14 µm | 4.5× | 2.3× | 0.78× |
| 16.3 µm (claim's lower t) | 7.1× | 3.6× | 1.2× |

The t below which flat plates need E ≥ E_ref (calc):
- E_ref = 23 GPa: t < 8.7 µm;
- E_ref = 11.7 GPa: t < **10.9 µm**, which is roughly where S9-D's old dorsal t sat.

## 5. What survives and what does not

| Part of the claim | Status |
|---|---|
| Arithmetic | **Survives** (§1) |
| "t is S9-D's most sensitive input; factor-2 flips C4" | **Weakened.** True only within the flat-plate bound. For the observed crescents, depth and arc angle control E (§3). |
| Replacement t = 19–20.4 µm is the better caudal value | **Weakened.** The "consistency check" is a definition (§2a). The paper's own image scales to ~12–14 µm (§2b, my reading, inference). n = 2 fish, pooled bars (§2c). |
| E envelope 0.15–3.5 GPa | Arithmetically correct. It depends on the contested t. With t = 12–14 µm it is 0.9–8.7 GPa (calc). |
| "Tissue E is 7–141× too stiff" | **Weakened.** It needs both t ≈ 19 µm *and* E_tissue ≥ 23 GPa. Relaxing either one gives ≈1.4–4.5×. Relaxing both lets wet fin-ray E reproduce Puri's EI at the flat-plate corner (§4). |
| "Becomes harder to overturn" | **Not supported.** The margin is back near S9-D's original ~2×. |
| "Carry measured EI rather than any E" | **Survives.** It is structural, and the crescent model supports it for any t. |

**What would settle it.** The author's own proposal still applies, with one sharper specification:
scan the same bending-tested caudal fins at ≤2 µm voxel and report both t **and** the arc depth and
angle of each hemiray. Pair that with **wet** nanoindentation or microbeam bending of excised
hemitrichs, not vertebrae.

## Sources

- Azevedo AS et al. 2011. *PLoS One* 6:e22820. PMC3145768. **full-text** (XML: methods, results,
  Fig. 4 legend). Fig. 4 image read from
  https://journals.plos.org/plosone/article/figure/image?size=large&id=10.1371/journal.pone.0022820.g004
  (my pixel readings).
- S9-D-D deliverable and script (commit `cd18bca3`). **full-text** (repository).
- Challenge 88 (commit `94431ba4`): crescent t-scaling, and the Puri load and fixation critique.
  **full-text** (repository).
- Puri et al. 2018. *J. Exp. Biol.* PMC5868929. Not re-read; values taken as quoted in challenge 88
  (full-text there).
- Equine cortical bone nanoindentation, wet vs dehydrated vs embedded. *J. Mater. Res.*
  (resolve.cambridge.org listing). **search-summary**.
- Nguyen K et al. "Curvature-induced stiffening of a fish fin", arXiv 1608.05891 (E_b 4–20 GPa).
  **search-summary**.
- Zebrafish vertebral nanoindentation 23–25 GPa (via S9). **search-summary**, not re-read.

```swarm-challenge
{"claim_id": 127, "outcome": "weakened", "reason": "Arithmetic is correct and 'carry measured EI' stands, but the upgrade to 'harder to overturn / 7-141x' rests on a replacement t whose own source image scales to ~12-14 um (the cited 2t+intra consistency check is a definition in Azevedo, not a check) and on a dry/embedded vertebral E>=23 GPa; relaxing either returns the flat-plate margin to ~1.4-4.5x, and with wet fin-ray E (4-12 GPa) flat plates can reproduce Puri's EI.",
  "corrected_value": "flat-plate tissue-E overprediction ~1.4-7x (not 7-141x); implied uncoupled flat-plate E 0.15-8.7 GPa spanning t=12-25 um",
  "depends_on": [
    "full-text: Azevedo et al. 2011 PMC3145768 defines fin thickness as sum of bone thickness and intra-ray space; n=2 uncut fins, 5-9 rays; boundary for bone thickness not stated",
    "my pixel reading: Azevedo Fig 4I uncut wall/intra-ray ratio ~0.14 vs plotted 0.24, implying t ~12-14 um (single image, no scale bar, +-1.3 um)",
    "calc: uncoupled flat-plate I = 2wt^3/12 with Puri EI 1.5-4e-9 N m^2 over 16-18 rays, w = 100-200 um",
    "challenge 88 calc: crescent hemirays give E ~ t^-1.07..-1.31 and 30-490 MPa",
    "search-summary: wet vs embedded bone nanoindentation 11.7 vs 19.4 GPa (equine cortical, J Mater Res)",
    "search-summary: fin-ray bone E 4-20 GPa used in arXiv 1608.05891",
    "search-summary: zebrafish vertebral nanoindentation E 23-25 GPa (via S9)",
    "full-text via challenge 88: Puri et al. 2018 fin EI 1.5-4e-9 N m^2, foam-pad fixation"
  ]}
```
