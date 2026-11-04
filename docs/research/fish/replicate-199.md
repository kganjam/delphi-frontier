# Replicate claim 199: [S6] can a lepidotrichial fin ray carry gliding load?

The question text I was given was cut short to "[S6] No". To recover it, I read only the **title and the first paragraph of §1** of `docs/research/fish/S6-organ.md` on branch `claude/s6-fin-ray-load-kqweu7`. That much told me the question and the body mass, m = 0.4 g, so W = 3.92 mN. I stopped reading there and did the derivation below. Only after that did I read the rest of the original (§Comparison).

Companion script: [`replicate-199_calc.py`](replicate-199_calc.py). Run `python3 docs/research/fish/replicate-199_calc.py`. Every number in §3 is **calculated, not observed**.

## 1. My value

**No. A passive (anaesthetised-stiffness) lepidotrichial pectoral fin cannot hold a lifting shape under 1 g glide load for a 0.4 g zebrafish.**

This verdict is **calculated**, from one measured whole-fin stiffness and stated assumptions. It is not observed.

- **Key number (calculated):** the flexural rigidity needed for tip deflection ≤ 10 % of span is **7–120×** the rigidity I infer for a zebrafish pectoral fin, across fin lengths L = 3–7 mm. At L = 5 mm it is **20–61×**.
- **Tip deflection under the glide load (linear theory, calculated):** δ/L = 0.55–12. Every value above about 0.3 lies outside the linear model. Physically, it means the fin folds rather than holding its shape.
- **Uncertainty:** the range is dominated by fin length, which is unmeasured (`unknown`), and by the caudal-to-pectoral transfer. Even the most generous corner (L = 3 mm with the whole-caudal-fin EI) gives a shortfall of about 5.5×.

## 2. Inputs

| # | Input | Value | Source | Read-level |
|---|---|---|---|---|
| I1 | Body mass, weight | 0.4 g; W = m·g = 3.924 × 10⁻³ N | S6 question statement (project brief, §1 para 1 of S6-organ.md) | full-text (that paragraph only) |
| I2 | Whole-fin bending stiffness EI, in vivo, anaesthetised | 1.5–4 × 10⁻⁹ N·m² (adult caudal fin, 16–18 rays, width about 5–8 mm, ray diameter 0.1–0.2 mm, loads about 100 µN) | Puri et al., *J. Exp. Biol.* 2018, [PMC5868929](https://pmc.ncbi.nlm.nih.gov/articles/PMC5868929/) | full-text (main text through a WebFetch summarising model; supplement not read) |
| I3 | Pectoral ray count | 12 is the mode (11: 6 fins, 12: 43 fins, 13: 9 fins); range 10–14 | *Zoological Letters* 2019, [doi 10.1186/s40851-019-0145-z](https://link.springer.com/doi/10.1186/s40851-019-0145-z) | search-summary |
| I4 | Pectoral fin span L | **unknown**. I used 3, 5 and 7 mm as an assumed bracket for an adult of roughly 26–32 mm SL. | Searches for "adult zebrafish pectoral fin length mm" (standard and extended) returned no numeric adult value | — |
| A1 | Load sharing | Two pectoral fins each carry W/2, uniformly distributed along the span | assumption | — |
| A2 | Aerodynamic tolerance | δ/L ≤ 0.10 | assumption | — |
| A3 | Caudal → pectoral transfer | Pectoral EI = (caudal EI ÷ 16–18 rays) × 12 rays, giving 1.0–3.0 × 10⁻⁹ N·m². As a generous check I also ran the full caudal value of 4 × 10⁻⁹. | assumption | — |

## 3. Arithmetic (calculated)

Each fin is treated as a cantilever under a uniform line load q = (W/2)/L.

- Tip deflection: δ = (W/2)·L³ / (8·EI)
- Rigidity needed for δ/L ≤ 0.1: EI_req = (W/2)·L² / (8 × 0.1)

**Per-ray and pectoral EI**

- EI per ray = 1.5 × 10⁻⁹/18 to 4 × 10⁻⁹/16 = 8.3 × 10⁻¹¹ to 2.5 × 10⁻¹⁰ N·m²
- Pectoral EI = per-ray EI × 12 = 1.0 × 10⁻⁹ to 3.0 × 10⁻⁹ N·m²

**Results by fin length**

In the table, "pect hi" and "pect lo" are the top and bottom of the pectoral EI range (3.0 × 10⁻⁹ and 1.0 × 10⁻⁹ N·m²). "caudal EI" is the generous check using the full 4 × 10⁻⁹ N·m².

| L | δ/L (pect hi / pect lo / caudal EI) | EI_req | Shortfall (EI_req / pect EI) |
|---|---|---|---|
| 3 mm | 0.74 / 2.21 / 0.55 | 2.2 × 10⁻⁸ | 7–22× |
| 5 mm | 2.04 / 6.13 / 1.53 | 6.1 × 10⁻⁸ | 20–61× |
| 7 mm | 4.01 / 12.0 / 3.00 | 1.2 × 10⁻⁷ | 40–120× |

Worked example at L = 5 mm with EI = 3 × 10⁻⁹:

- δ = 1.962 × 10⁻³ × (5 × 10⁻³)³ / (8 × 3 × 10⁻⁹) = 2.453 × 10⁻¹⁰ / 2.4 × 10⁻⁸ = 1.02 × 10⁻² m
- δ/L = 2.04

**Strength side-check (calculated, solid-rod idealisation)**

- Root moment per ray at L = 5 mm: (W/2)·(L/2)/12 = 4.1 × 10⁻⁷ N·m
- For a solid rod of d = 0.1–0.2 mm: σ = M·c/I = 0.5–4.2 MPa

This is far below any bone strength, so under this idealisation stiffness, not strength, is the limit. Fin-ray bone strength itself is `unknown`; I did not look it up.

**Consistency check (my inference)**

The same solid-rod geometry implies an *effective* whole-ray modulus of only 1–51 MPa. Mineralised bone is in the GPa range (general background, no source fetched). So the measured fin is far softer than a solid bony rod of its size would be. That points to architecture (segmentation and the paired hemirays) rather than material as the reason. This is my inference; Puri et al. do not claim it.

## 4. What this does not establish

- No pectoral-fin stiffness has been measured; I transferred the caudal value (A3).
- Pectoral span is `unknown`.
- The stiffness is from anaesthetised fish; active stiffening is not considered.
- The analysis is linear only; it does not show that a folded fin produces no lift.
- No flutter calculation was done.
- I used one primary stiffness source, the same one the original author used. So the **inputs are not independent**; only the modelling is.

## Comparison with the recorded value (read only after §1–3 were written)

The original (`S6-organ.md`, branch `claude/s6-fin-ray-load-kqweu7`) reports:

- **Answer:** "No".
- **Key number:** required/measured rigidity **9–196×** for square fin-wings of 3–15 mm, with 15–65× at 5 mm.
- **Model:** EI per unit width (D_w = EI/width), with chord = span, so wing EI grows with chord.

My model is different: it uses a fixed count of 12 rays, the pectoral ray count, and ignores chord. Even so, at the overlapping lengths I get:

| L | Mine | Original |
|---|---|---|
| 3 mm | 7–22× | 9–39× |
| 5 mm | 20–61× | 15–65× |

The two **agree** on the verdict, on the order of magnitude, and on the fact that stiffness rather than strength is decisive.

**Points of disagreement, kept rather than averaged:**

- **Root stress:** the original estimates about 70 MPa for decoupled 15 µm hemirays at L = 10 mm. My solid-rod idealisation at L = 5 mm gives 0.5–4 MPa. Both stress figures depend on an assumed cross-section, and neither changes the verdict.
- **Fin-length range:** the original covers 3–15 mm; I stopped at 7 mm.

**Verdict: AGREE.** This agreement comes with a caveat: both derivations rest on the single Puri et al. 2018 caudal-fin measurement.

```swarm-replication
{"claim_id": 199, "my_value": "No: required/available flexural rigidity 7-120x (20-61x at 5 mm span) for a 0.4 g zebrafish pectoral fin-wing at delta/L<=0.1 (calculated)", "agrees": true,
  "note": "Independent beam model (ray-count-scaled pectoral EI, not per-width) reproduces the original's 'No' and its 9-196x shortfall magnitude, but both rest on the same single Puri et al. 2018 caudal-fin stiffness, so inputs are not independent."}
```
