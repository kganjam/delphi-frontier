# Replication of claim 200: adult zebrafish peak fast-start speed from Danos & Lauder (2012)

**What this is:** an independent re-derivation. The speed below is **calculated** from a Reynolds number. It is **not** an observed velocity.

## Result

**Mean peak centre-of-mass speed ≈ 0.84 m/s (≈ 25.5 TL/s).**
- This assumes ν = 1.0 × 10⁻⁶ m² s⁻¹ (1 mPa s, ρ ≈ 1000 kg m⁻³) and that Re was computed with total length (TL).
- ± 1 s.e.m. on Re gives a range of **0.78–0.91 m/s**.
- **Systematic uncertainty is larger than the s.e.m.** If the authors used a viscosity for 26–28 °C water (ν ≈ 0.84–0.87 × 10⁻⁶ m² s⁻¹), the mean falls to **0.70–0.73 m/s**. If their length scale was not TL, the value moves in proportion to 1/L.
- Overall defensible band: **~0.70–0.91 m/s**.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Mean max Reynolds number, adults in normal water | 27,800 ± 2,140 (s.e.m.) | Danos & Lauder 2012, *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957, as quoted in the task statement | **could-not-access** by me (see below). The value is taken from the claim text, not verified. |
| Fish length | TL = 33 mm | same as above | could-not-access (taken from claim text) |
| Frame rate | 1000 frames s⁻¹ | Danos & Lauder 2012 abstract, via Europe PMC REST API | abstract |
| Viscosity of "normal water" | 1 mPa s | Danos & Lauder 2012 abstract ("1 mPa s (normal water)") | abstract |
| Density of water | 1000 kg m⁻³ | standard physical value (my assumption) | n/a |
| Water temperature | **unknown** | not in the abstract; full text not reachable | n/a |
| Length scale and velocity used in the authors' Re definition | **unknown** (I assume Re = U·TL/ν with U = peak centre-of-mass speed) | full text not reachable | n/a |

**Access attempts** (all failed, so the full-text items could not be checked):
- sites.harvard.edu author PDF: blocked by the proxy (403 / ENOTFOUND).
- cob.silverchair.com JEB PDF: ENOTFOUND.
- zendy.io: ENOTFOUND.
- journals.biologists.com: the URL I guessed returned an unrelated article.
- A 2025 PMC paper (PMC11930232): does not cite the Danos & Lauder values in the first 100k characters.

**Scope of the negative search:** the abstract does not report a peak escape speed in m/s. I could not search the full text for a directly reported adult peak speed, so I can neither confirm nor rule out that the paper reports one (for example in a table of maximum centre-of-mass velocity).

## Arithmetic

Re = U·L/ν, so U = Re·ν/L.

- U = 27,800 × 1.0×10⁻⁶ / 0.033 = **0.842 m/s**. U/TL = 0.842 / 0.033 = **25.5 TL/s**.
- Re − s.e.m. = 25,660 → 0.778 m/s (23.6 TL/s).
- Re + s.e.m. = 29,940 → 0.907 m/s (27.5 TL/s).
- Sensitivity to temperature (my inference, not stated by the authors):
  - ν = 0.87×10⁻⁶ (≈26 °C) → 0.733 m/s.
  - ν = 0.836×10⁻⁶ (≈28 °C) → 0.704 m/s.
- Ratio to the 5.8 m/s refutation threshold: 5.8 / 0.842 = **6.9×** below it.

## Comparison with the recorded value

I found the recorded value only in the task statement; the repository has no prior working for it. The statement gives ~0.84 m/s (~25 TL/s), a range of 0.78–0.93 m/s, and ~7× below 5.8 m/s.

- **Mean: AGREE.** I get 0.842 m/s and 25.5 TL/s under the same assumptions (ν = 1 mPa s / 1000 kg m⁻³, L = TL).
- **Ratio to the threshold: AGREE.** I get 6.9×.
- **Upper end of the range: minor disagreement.** ± 1 s.e.m. gives 0.907 m/s, not 0.93. I cannot tell how 0.93 was obtained.
- **The "~1.5× the Ucrit proxy" figure: CANNOT TELL.** No Ucrit input was available to me.
- **Caveats.** The agreement depends on two things I could not verify in the full text: ν = 1.0×10⁻⁶ and the TL length scale. If the authors used ν for warm water, the true mean is ~0.70–0.73 m/s. Either way, the conclusion that it is far below 5.8 m/s holds.

Both derivations share the same unverified Re and TL inputs, which I took from the claim text. The agreement therefore checks the arithmetic, not the source reading.

```swarm-replication
{"claim_id": 200, "my_value": "0.84 m/s (25.5 TL/s); ±1 s.e.m. 0.78-0.91 m/s; 0.70-0.73 m/s if nu for 26-28 C water was used", "agrees": true,
  "note": "Same mean from U = Re*nu/TL with nu = 1e-6 m2/s, but the upper range comes out 0.91 not 0.93, and Re, TL, temperature and the Re definition could not be checked because the full text was unreachable (abstract only)."}
```
