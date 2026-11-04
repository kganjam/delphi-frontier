# Replicate 96: the hemitrich-locking factor against the size-corrected gap

**Claim under test (answer removed):** "The single measured hemitrich-locking factor (~12x, Alben, Madden & Lauder
2007, clamped 1.98 N/m vs one-base-free) closes a 2.1x gap with 5.7x margin, so ACTIV[e stiffening …]".

**Blindness disclosure.** I did not read `S26-deepen.md` or `S26_deepen_calc.py` before finishing my derivation.
I did see the S26-D **commit message** (`95578def`) while finding the file. It states the conclusion: "~2.1x gap,
which the single measured ~12x hemitrich-locking factor closes". So this is **not fully blind** on the
direction of the verdict. I took the requirement inputs from the upstream S6-D-D document
(`origin/claude/deepen-s6-d-sensitive-input-fc1hm8:docs/research/fish/S6-D-deepen.md`). I took the 12x, the
1.98 N/m and the 40.3 mm from the primary paper, which I read myself.

## 1. Result

- **Arithmetic as framed (calculated):** gap = **2.11x**, margin of 12x = **5.68x ≈ 5.7x**. This reproduces.
- **My preferred value (calculated): the margin is 1.6x to 5.7x, not a point value of 5.7x.** 5.7x is the upper
  end. It holds only if the 3.8e-6 N m² baseline is a *one-base-free* stiffness. If I use Alben's own clamped
  stiffness as the locked state, so that the baseline and the locking factor come from the same specimen, the
  margin is 1.6x to 2.8x. In every case I tried, the factor still closes the gap (margin > 1). That is
  conditional on isometric L⁴ scaling and on muscles reproducing the excised-ray clamp in vivo. Both are
  assumptions, and neither has been tested.

## 2. Inputs

| Input | Value | Kind | Source | Read-level |
|---|---|---|---|---|
| Clamped point-load stiffness | 1.98 N m⁻¹. The caption says the force–displacement curve "may be fit with a slope of 1.98 N m⁻¹, about 12 times the value when one hemitrich is free" | measured | Alben, Madden & Lauder 2007, *J R Soc Interface* 4:243, doi:10.1098/rsif.2006.0181, Fig. 7a caption | **full-text** (PMC2359861 HTML from ncbi.nlm.nih.gov, read by me) |
| Clamped/one-free ratio | ~12. The text says "In the experiment, the factor is 12, which occurs when G ≈ 100 in the model". The model range is 3–100 (4 at G = 3, 100 at G > 10⁵) | measured (ratio); model range calculated by the authors | same | full-text |
| Load point | "approximately two-thirds of the distance from the base to the tip". Force is "measured as a function of tip deflection" | method | same | full-text |
| Specimen | The single-ray experiments use "fin ray 4" (of 13) from a bluegill. I found no n or spread for the 12x in the passages I read | method | same, Fig. 2, App. A | full-text |
| Bluegill max ray length | 40.3 ± 0.8 mm (mean ± s.e., six fish) | measured | same, §2 | full-text |
| Alben EI | "B = EI ≈ 10⁻⁶–10⁻⁵ J m" (= N m²), from three-point bending (composite E ≈ 10⁸–10⁹ Pa, I ≈ 10⁻⁶ cm⁴). The base condition is not stated | measured / reported | same, §3 | full-text |
| Passive bluegill ray EI | 3.8e-6 N m² | reported (relay) | Puri et al. 2018, citing Flammang 2013, as relayed in this repo. S25 in this repo says it is **untraced** in Flammang 2013. Flammang's abstract gives 565e-6 instead (a ~150x disagreement, preserved and unresolved) | **could-not-access** by me. I used the repo relay only |
| Required EI per ray | 6.31e-4 N m² = P L²/(8c), P = mg/(2N) | calculated from assumptions m = 0.10 kg, N = 14, L = 0.12 m, c = δ/L = 0.10 | S6-D, as restated in S6-D-deepen.md §1 | repo document (listing-level relay of S6-D) |
| Size transfer | EI ∝ L⁴ (isometry, constant modulus) | **assumption** | none | n/a |

## 3. Arithmetic

1. P = 0.10 × 9.81 / (2 × 14) = 0.03504 N. EI_req = 0.03504 × 0.12² / (8 × 0.10) = **6.31e-4 N m²**. This matches S6-D.
2. λ = 120 / 40.3 = 2.978. λ⁴ = **78.6**.
3. Scaled passive EI = 3.8e-6 × 78.6 = **2.99e-4 N m²**.
4. Gap = 6.31e-4 / 2.99e-4 = **2.11x**. Without the size correction the gap is 6.31e-4 / 3.8e-6 = 166x.
5. Margin = 12 / 2.11 = **5.68x**. If the factor is read as 10 to 14, the margin is 4.7x to 6.6x.
6. The margin is sensitive to the flying-fish ray length. At 105 mm the gap is 3.6x and the margin 3.3x. At
   160 mm the gap is 0.67x (no locking needed).

**Consistency check (calculated; my inference, not the authors' claim).** I converted Alben's 1.98 N m⁻¹ to a
cantilever-equivalent EI. This assumes a uniform Euler–Bernoulli beam, a rigid root, L = 40.3 mm and load at
a = 2L/3:
- deflection read at the load point, k = 3EI/a³: EI_clamped = **1.28e-5**, EI_one-free = 1.07e-6 N m²;
- deflection read at the tip, which the main text describes: EI_clamped = k·28L³/162 = **2.24e-5**,
  EI_one-free = 1.87e-6 N m².

The relayed baseline, 3.8e-6, is **2x to 3.6x stiffer than Alben's one-free state**. 3.8e-6 × 12 = 4.6e-5. That
is 2x to 3.6x **above** Alben's own measured clamped state. So multiplying 3.8e-6 by 12 assumes the 3.8e-6 ray
was in a one-base-free condition. Nothing I read establishes that.

If instead I take Alben's clamped equivalent directly as the locked EI and scale it by λ⁴:
1.28e-5 × 78.6 = 1.01e-3, a **1.6x** margin. 2.24e-5 × 78.6 = 1.76e-3, a **2.8x** margin. If the tested ray 4 is
shorter than 40.3 mm, the margin rises: the back-calculated EI goes as L³, the scale factor as L⁻⁴, so the net is
∝ 1/L.

## 4. Caveats

- The 12x comes from one excised ray, with no n or spread reported in the passages I read. The authors' own model
  makes the ratio depend on G (3 to 100), so the ratio need not transfer to another species or size unless the
  dimensionless groups are preserved. Isometry with constant material properties would preserve them, but that
  is an assumption.
- "Locking" here means the experimenter clamped both bases. That muscles hold such a clamp through a glide is
  unmeasured.
- The disagreement between the 3.8e-6 relay and Flammang's 565e-6 is not resolved here.
- Negative-search scope: I did not search for any other measurement of a clamped/free hemitrich ratio. I only
  checked the Alben 2007 full text. Europe PMC fullTextXML returned HTTP 500, royalsocietypublishing.org returned
  a 403 challenge, and ncbi.nlm.nih.gov/pmc returned the full HTML.

## 5. Comparison with the recorded value (read after the derivation)

The S26-D document (`95578def`) records the gap as **2.1x** and the margin as **5.7x**, from 3.8e-6 × (120/40.3)⁴.
My arithmetic **AGREES** with this exactly, and I agree with the direction: the gap closes. S26-D also computed
Alben's clamped and one-free equivalents (1.28e-5 and 1.07e-6), as I did. It still applied 12x to the 3.8e-6
baseline, which sits between those two states. I therefore read 5.7x as the **upper end** of a 1.6x to 5.7x
margin, not as a central value. The conclusion "closes" survives at the low end. The size of the margin does not.

```swarm-replication
{"claim_id": 96, "my_value": "gap 2.11x, margin 5.68x as framed (calculated); margin 1.6-5.7x when the locked state is taken from Alben's own clamped 1.98 N/m (EI-equivalent 1.3e-5 to 2.2e-5 N m^2 scaled x78.6) rather than 12 x 3.8e-6", "agrees": true,
  "note": "Arithmetic (2.1x gap, 5.7x margin) and the closes-the-gap verdict reproduce from the Alben 2007 full text, but 5.7x is the upper end because 3.8e-6 x 12 exceeds Alben's own measured clamped state by 2-3.6x, so a baseline-consistent margin is 1.6-2.8x (all conditional on isometric L^4 scaling and in-vivo locking)."}
```
