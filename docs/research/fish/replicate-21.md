# Replication 21: adult zebrafish (*Danio rerio*) peak fast-start speed

**Result (calculated, not observed):** U ≈ **0.84 m/s ≈ 25.5 TL/s**. The range at ±1 s.e.m. of Re is 0.78–0.91 m/s (23.6–27.5 TL/s).
I worked this out from a Reynolds number the authors report. The paper does not report a speed in the text.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Mean maximum Re per escape sequence, 1 mPa s water | 27,800 ± 2,140 s.e.m. | Danos N. & Lauder G. V. (2012) *J. Exp. Biol.* 215:1854–1862, doi:10.1242/jeb.068957, Results | full-text (publisher HTML, read through an automated fetch/summarise tool; sentences relayed as quotes) |
| Length scale | 33.0 ± 1.3 mm **total length**. The authors do not say whether ±1.3 is s.d. or s.e.m. | same, Materials and methods: "Fish (mean total length 33.0±1.3 mm)…" | full-text (same caveat) |
| Number of fish | 5 | same | full-text (same caveat) |
| Dynamic viscosity of the control treatment | 1 mPa s (the authors' nominal value) | same | full-text (same caveat) |
| Density | **Not given.** The authors state only that "the differences in fluid density were negligible". I assume 1000 kg m⁻³. | same, plus my assumption | full-text (same caveat) |
| How Re was computed | "fish length, maximum linear velocity per sequence and the appropriate viscosity for each treatment". There is no explicit formula. | same, Results | full-text (same caveat) |

Context sentences from the paper (the higher-viscosity treatments, not used here): Re = 2,350 ± 160 in 10 mPa s and 820 ± 60 in 20 mPa s.
Water temperature: `unknown`. The fetched text did not give an experimental temperature.

## Arithmetic

ν = μ/ρ = 1.0×10⁻³ Pa s / 1000 kg m⁻³ = 1.0×10⁻⁶ m² s⁻¹ (my assumption about how the authors converted).

U = Re·ν/L = 27,800 × 1.0×10⁻⁶ / 0.0330 = **0.8424 m/s**

U/L = 0.8424 / 0.0330 = **25.53 TL/s**. This is the same as Re·ν/L² = 0.0278/0.001089.

±1 s.e.m. of Re:
- 25,660 × 10⁻⁶ / 0.0330 = 0.7776 m/s (23.56 TL/s)
- 29,940 × 10⁻⁶ / 0.0330 = 0.9073 m/s (27.49 TL/s)

## Caveats (my inference, not the authors' claims)

1. **This is an inversion, not a measurement.** The paper presents linear velocity only graphically, in Fig. 3G–I. I did not read the figure values, and the fetched text gives no number in m/s, cm/s or BL/s.
2. **The inversion only holds if my ν matches the authors' ν.** If they used ν = 1.0×10⁻⁶ m² s⁻¹, inverting recovers their underlying speed whatever the true water temperature was. If they used another density or a temperature-corrected viscosity, U scales with that ν. For example, real water at 20 °C has ν ≈ 1.004×10⁻⁶ m² s⁻¹, a negligible change.
3. **Mean of ratios versus ratio of means.** Re was presumably computed per sequence with that fish's length. Dividing the mean Re by the mean length is therefore approximate. With TL varying 33.0 ± 1.3 mm (about 4%), the bias is small next to the 7.7% s.e.m. of Re. Treating the length spread as an extra independent error would widen the band to about ±0.07 m/s. I report the Re-only band above, as the question frames it.
4. **Which stage the peak comes from is not stated.** "Maximum linear velocity per sequence" could come from stage 1 or stage 2.
5. **Not checked:** I could not open the Harvard-hosted PDF (sites.harvard.edu was blocked by the session's network policy). So I did not check the tables or figure values against the HTML.

## Comparison with the recorded value

I searched the repository for "27800" and "27,800" in `*.md` files and found no recorded derivation. However, the task prompt itself states the value: 0.84 m/s, 25.5 TL/s, 0.78–0.91. My independent arithmetic gives 0.842 m/s, 25.5 TL/s and 0.778–0.907 m/s, which matches to the stated precision. I **AGREE**.
One limit on that agreement: both derivations rest on the same single Re figure and the same assumed ν. This shows the arithmetic is right, not that the underlying speed is right. A real check would read the velocity bars in Fig. 3.

```swarm-replication
{"claim_id": 21, "my_value": "0.84 m/s (25.5 TL/s; 0.78-0.91 m/s at +/-1 s.e.m. of Re), calculated as U = Re*nu/L with nu = 1.0e-6 m^2/s and L = 33.0 mm TL", "agrees": true,
  "note": "Recomputed from Danos & Lauder 2012 (Re 27,800 +/- 2,140, mean TL 33.0 mm, 1 mPa s), read as full text; the arithmetic matches, but the paper's speed figure was not read and density was assumed to be 1000 kg/m^3."}
```
