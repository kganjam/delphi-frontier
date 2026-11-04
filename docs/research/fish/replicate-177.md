# Replication 177: S24-D, the tail-beat frequency needed at the taxi operating point

Desk re-derivation. I ran no experiment. Every number below is tagged **measured** (from a source,
with its read-level), **calc** (my arithmetic), or **assumed**.

## What I saw before deriving (contamination disclosure)

- **The prompt states the recorded value.** It was meant to be removed but was not: "~61-81 Hz
  (1.2-1.6x the 52 Hz escape EMG maximum)". So I was not blind to the answer.
- **The harvest branch.** To find the operating-point inputs I opened the first ~60 lines of
  `docs/research/fish/S24-deepen.md` on branch `claude/s24-deepen-launch-gap-2motub`. Its summary
  paragraph repeats the 61-81 Hz result. I stopped reading there. I did not open the rest of the
  file or `S24-deepen_calc.py`.
- **Inputs I took from that file** (read-level: full-text of those lines; they are project inputs,
  not values I checked against primary sources):
  - U = 1.95 m/s (the glide-target taxi speed)
  - A = 8 mm peak-to-peak (0.20 TL; S24 marks this as assumed)
  - f_max = 52 Hz (escape EMG maximum)
- **Assumed by me.** L = 40 mm, from the prompt's Re and the file's "L = 40 mm". ν = 1.0 × 10⁻⁶ m²/s
  (water at about 20 °C).

So this is **independent arithmetic and independent source-checking on shared inputs**. It is not
blind. Weigh any agreement accordingly.

## Sources

| Source | What I used | Read-level |
|---|---|---|
| Bainbridge 1958, *J Exp Biol* 35:109–133 | U = L(¾f − 1), derived for f > 5 Hz; amplitude about 0.2 L at the higher frequencies | search-summary (publisher page paywalled; the WebFetch returned nothing usable) |
| Seo, Zhou & Mittal 2025, arXiv 2507.11665v2, "Scaling Laws for Caudal Fin Swimmers…" | Quotes Bainbridge's relation. Gives peak-to-peak tail amplitude A_F ≈ 0.18 L at the higher speeds. Gives St_A = (4/3)(A_F/L)[1 + f₀L/U] → 0.24 for U ≫ 1 L/s. Estimates Bainbridge's fish at Re ≈ 2 × 10⁴ – 10⁶ | full-text (first 100 k of 175 k characters, via WebFetch) |
| Wardle 1975, *Nature* 255:725–727, doi:10.1038/255725a0 | Stride 0.6–0.8 L per tail beat; 0.7 used as a mean | search-summary (secondary quotes only; full text not read) |

**The sources disagree on amplitude.** Bainbridge's own summary, as quoted secondhand, gives about
1/5 L (0.20 L). Seo et al.'s reduction of the same data gives 0.18 L peak-to-peak. I keep both.

## Arithmetic (calc)

**Re** = U·L/ν = 1.95 × 0.040 / 1.0e-6 = **7.8 × 10⁴**. This lies inside Seo et al.'s estimate of
Bainbridge's Re range, so the measured kinematics apply in Reynolds number.

**Route A: Bainbridge's relation inverted.**

- U/L = 1.95 / 0.040 = 48.75 L/s
- f = (4/3)(U/L + 1) = (4/3)(49.75) = **66.3 Hz** (1.28 × 52 Hz)
- Implied St with A = 0.18 L: 0.18 × 0.040 × 66.3 / 1.95 = 0.245
- Implied St with A = 8 mm: 0.008 × 66.3 / 1.95 = 0.272
- Implied stride: U/(fL) = 0.735 L/beat

**Route B: Strouhal number with S24's amplitude.** f = St·U/A.

| St | A | f | Ratio to 52 Hz |
|---|---|---|---|
| 0.24 | 8 mm | 0.24 × 1.95 / 0.008 = **58.5 Hz** | 1.13× |
| 0.27 | 8 mm | **65.8 Hz** | 1.27× |
| 0.24 | 0.18 L = 7.2 mm | **65.0 Hz** | 1.25× |

**Route C: Wardle's stride.** f = U/(λL).

| Stride λ (L/beat) | f | Ratio to 52 Hz |
|---|---|---|
| 0.8 | **60.9 Hz** | 1.17× |
| 0.7 | **69.6 Hz** | 1.34× |
| 0.6 | **81.3 Hz** | 1.56× |

## My value

**f_req ≈ 66 Hz (calc). The central range across the three routes is 59–81 Hz, which is 1.1–1.6×
the 52 Hz maximum.**

- **Where the routes agree.** Routes A and B are consistent with each other, at 65–66 Hz, when the
  Strouhal number and the amplitude are taken from the same source. Bainbridge's implied stride,
  0.735 L, falls inside Wardle's 0.6–0.8.
- **Where the upper end comes from.** The high end, around 81 Hz, comes only from Wardle's
  shortest stride (0.6 L). The St route with A = 8 mm never exceeds about 66 Hz.
- **Caveat on extrapolation (my inference).** Both empirical relations are extrapolated to about
  66 Hz and about 49 L/s for a 4 cm fish. I could not confirm, from what I read, the frequency
  range Bainbridge or Wardle actually measured. The upper limit of those measurements is `unknown`.
- **Not checked.** The 52 Hz maximum and the 8 mm amplitude are carried over from the project. I did
  not check them against primary sources.

## Comparison with the recorded value

The recorded value is ~61–81 Hz, which is 1.2–1.6× the 52 Hz maximum.

- **Their 61–81 Hz is exactly my Route C** (Wardle stride 0.8–0.6).
- **Their St 0.24–0.27 does not, with A = 8 mm, produce 61–81 Hz (my inference).** It produces
  58.5–65.8 Hz. The two characterisations bundled in the claim are not numerically identical. With
  A = 0.2 L, a stride of 0.6 L corresponds to a peak-to-peak St of 0.33, not 0.24.
- **What this changes.** It moves the bottom of the shortfall from 1.2× to about 1.1×. It does not
  change the qualitative verdict.

**AGREE** on the substance: about 60–80 Hz, roughly 1.1–1.6× the maximum. The "wider margin, a
fortiori" claim, at 132–199 Hz (2.5–3.8×), does not survive measured kinematics at Re ≈ 7.8 × 10⁴.
The 3-BL target is better described as "not shown to close, not refuted".

**CANNOT TELL** on the separate sub-claim that the 1-BL target (~195 Hz) stays closed. I did not
derive the 1-BL operating speed, and I did not read where it is stated.

```swarm-replication
{"claim_id": 177, "my_value": "~66 Hz (range 59-81 Hz; 1.1-1.6x the 52 Hz maximum), calc", "agrees": true,
  "note": "Independent arithmetic on shared inputs (not blind: the prompt stated the answer); 61-81 Hz reproduces only via Wardle stride 0.6-0.8, while St 0.24-0.27 with A=8 mm gives 58.5-65.8 Hz, so the low end of the shortfall is ~1.1x not 1.2x, verdict unchanged; 1-BL sub-claim not checked."}
```
