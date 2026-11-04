# S21-D — Deepening S21: adult zebrafish fast-start peak velocity

**Parent question (S21, behaviour):** What is the measured PEAK velocity of an adult zebrafish fast-start?
**Recorded S21 answer:** 0.842 m/s (25.5 TL/s), *derived* from a measured Reynolds number rather than read
directly; ~7x below the 5.84 m/s refutation threshold, so it narrows the gap without closing it.

**Provenance caveat:** the S21 write-up is not in this repository (searched every tracked file in
`kganjam/delphi-frontier` on branches `claude/zebrafish-fast-start-velocity-pgqbck` and
`work/frontier-foundation` for `S21`, `zebrafish`, `fast-start`, `5.84`, `0.842`, `Reynolds`: no S21 record;
the only "zebrafish" hits are unrelated triage JSON). So I could not read which paper supplied the
Reynolds number, what velocity it was built from, or where the 5.84 m/s threshold came from. Everything
below that reconstructs S21's derivation is **my inference from the two recorded numbers**, labelled as such.

---

## 1. Which input is the answer most sensitive to? (recomputed)

The derivation had to be U = Re · ν / L. From the recorded pair, L = 0.842 / 25.5 = **0.0330 m (33.0 mm TL)**.
This is my calculation from S21's numbers, not a measurement. Back-calculating, the Re S21 used would be about
27,700 if ν = 1.004×10⁻⁶ m²/s (20 °C) and about 33,300 if ν = 0.836×10⁻⁶ m²/s (28 °C). Both are calculated,
and I don't know which one S21 used.

U is linear in all three inputs, so a 2x error in any one moves U by 2x:

| Perturbation (calculated) | U (m/s) | Threshold / U |
|---|---|---|
| As recorded | 0.842 | 6.9x |
| Any input pushes U up 2x (Re x2, ν x2, or L ÷2) | 1.684 | 3.5x |
| Any input pushes U down 2x | 0.421 | 13.9x |
| Change needed to reach the threshold | 5.84 | 1.0x → needs a **6.9x** error in one input |

**Result of the sensitivity test (calculated):** no single input, wrong by 2x, changes the conclusion
"below threshold, gap not closed". The conclusion is robust to 2x errors. The quantitative claim ("~7x")
is not robust: it is exactly as uncertain as the product Re·ν/L.

Of the three, **Re is the weakest input**, so it is the one attacked here. My reasons:

- ν is a tabulated property of water. Across 20–28 °C, the plausible range for zebrafish work, it varies by
  only about 1.2x.
- L is bounded by adult zebrafish anatomy. Seebacher's lab describes "1-3 body lengths s⁻¹ (0.03-0.1 m s⁻¹)"
  for adult zebrafish ([Bamford & Seebacher 2024](https://doi.org/10.1242/bio.060543), full-text). My
  inference from that: BL ≈ 30–33 mm, consistent with S21's 33 mm. TL vs SL is at most about a 1.2x
  ambiguity.
- Re is the only input that is itself a velocity in disguise, so it carries every ambiguity about
  *which* velocity. In this literature Re is routinely built from the **mean** speed, not the peak. For
  example, Ravel et al. 2025 define "Re = ρ V_mean L / μ where … V_mean [is] the mean computed speed during
  the six simulated tail beats" ([PMC11930232](https://doi.org/10.1016/j.isci.2025.112056), full-text). The
  quoted Re values are also sometimes **assumed**, not measured: Li et al. 2014 write "We assumed that the
  larvae performed their C-starts at a Reynolds number (Re) of 2000"
  ([doi:10.1098/rsif.2014.0848](https://doi.org/10.1098/rsif.2014.0848), full-text via PMC4223905).

## 2. How well established is that input?

**Evidence level of S21's input: proxy (derived), read-level `unknown` for S21's own source**, because the
S21 record and its citation are not available to me.

A Reynolds number is not an independent measurement of speed. It is a speed multiplied by a length and
divided by a viscosity. Converting it back to a velocity recovers whatever velocity went in, and that might
be a mean, a peak, a simulated value or an assumption. So S21's "derived from a measured Re" is
circular at best. At worst it is an assumption that has been repeated until it reads as a measurement.
If S21's Re came from a mean swimming speed, 0.842 m/s is a **lower bound on peak**, not the peak itself.
I could not establish how big the peak/mean ratio is for adult zebrafish, so I give no number for it:
`unknown`.

## 3. Improving it: a direct measurement replaces the proxy

**Primary source found:** Miln C, Ward AJW, Seebacher F (2021). *Social rank and not physiological capacity
determines competitive success in zebrafish (Danio rerio).* R Soc Open Sci 8:210146,
[doi:10.1098/rsos.210146](https://doi.org/10.1098/rsos.210146). **Read-level: full-text** (Europe PMC
PMC8025299 XML, plus Figure 1 image from the Europe PMC supplementary bundle).

What the authors state (author's claims, quoted or closely paraphrased from the full text):
- Subjects were "Adult short-fin zebrafish of mixed sex": 10 groups of five fish (n = 50), at 23 °C (± 0.5 °C).
- Escapes were "induced by a mechanical stimulus to the tail" in a 30 mm-deep tank and filmed "from above
  at 120 frames s⁻¹ (with a GoPro Hero 6)".
- Speed was tracked at the centre of mass, defined as 0.35 BL from the snout.
- "Four escape responses were analysed for each fish and the fastest speed was used", which they call
  'fast start'. This is a direct per-fish maximum velocity in m/s.
- No numeric summary of fast-start speed is given in the text. The values exist only as Figure 1a
  (x-axis "fast start speed (m s⁻¹)"). Underlying data are on figshare (doi:10.6084/m9.figshare.c.5359401),
  which I **could-not-access** because the proxy returned 403.

**What I extracted (my digitisation of Fig. 1a, not the authors' numbers).** I calibrated from the axis ticks
(0 → px 78.5, 1.5 m/s → px 323.5, 163 px per m/s, about ±0.01 m/s per pixel) and ran an automated ring
detector. The detector over-counts overlapping rings (it found 54–142 rings per colour against 50 fish), so
only the range is reliable:
- **Per-fish maximum fast-start speed: about 0.45 to 1.38 m/s.** A single fish reaches about 1.38 m/s.
  The bulk lies between about 0.55 and 1.15 m/s.
- The detector gives a median of about 0.70–0.85 m/s, depending on which colour series is used. I treat
  this as approximate.

**Caveats on this improved input.** These are my inferences, not the authors' claims:
- 120 fps is about 8.3 ms per frame. Fast-start stage 1 in fish of this size lasts on the order of 10–20 ms,
  so frame-to-frame differencing at 120 fps smooths the true instantaneous peak. That makes these values a
  likely **underestimate** of the instantaneous peak. I could not quantify how big the bias is: `unknown`.
- The 23 °C test temperature is cooler than the 28 °C husbandry standard, which would also tend to lower
  speed.
- Body length for these fish is not given numerically in the main text (it is in the figshare data, which I
  could-not-access). Using S21's 33 mm for illustration only (calculated): 0.45–1.38 m/s ≈ 14–42 TL/s.

**Disagreement and other sources (preserved, not averaged):**
- Danos & Lauder 2012, *Challenging zebrafish escape responses by increasing water viscosity*,
  J Exp Biol 215:1854 ([doi:10.1242/jeb.068957](https://doi.org/10.1242/jeb.068957)). **Read-level:
  abstract** (via Crossref); the full text is **could-not-access** because journals.biologists.com served a
  Cloudflare challenge and sites.harvard.edu was blocked by the network policy. It used 1000 fps, which is
  the right tool for instantaneous peak, and it reports "maximum velocity of the center of mass". The
  abstract gives no number. This is the single most valuable unread source: it would directly test the
  120 fps underestimate.
- Li et al. 2014 (full-text) give larval (5 dpf) peaks of "46 l s⁻¹" measured and 38 l s⁻¹ simulated. These
  are *larval* body-length rates; they are not adult and not comparable in m/s.
- Bhattacharyya et al. / IOB 2020 ([PMC7750966](https://doi.org/10.1093/iob/obaa023), full-text keyword scan
  only) concerns visual-loom evasion strategy. My scan found no adult peak m/s value, only a model
  parameter "prey velocity (V) = 3.7 cm s⁻¹".
- **Scope of the negative search:** I ran Europe PMC queries for (zebrafish OR Danio rerio) AND
  (fast-start OR C-start OR escape response) AND (adult OR velocity), which returned 996 hits. I screened
  only the first 100 titles (newest-first ordering). I also searched Seebacher-authored zebrafish escape
  papers (5 hits) and ran two web searches. Among the papers I could read in full, Miln et al. 2021 is the
  only adult zebrafish fast-start with velocities in m/s. Hits 101–996 were not screened.

## 4. Recomputed conclusion

All arithmetic below is calculated, using the measured Miln et al. values as the input:

| Input | U (m/s) | Threshold / U |
|---|---|---|
| S21 derived (Re proxy) | 0.842 | 6.9x |
| Miln 2021, digitised bulk median (≈0.70–0.85) | ~0.8 | ~7x |
| Miln 2021, fastest individual of 50 | ~1.38 | **4.2x** |
| Fastest individual if 120 fps under-reads the peak 2x (hypothetical, not measured) | ~2.8 | 2.1x |

- S21's 0.842 m/s sits **inside** the directly measured adult distribution, near its centre. A direct
  measurement now supports the magnitude, not just a back-calculation.
- The **gap narrows** once individual variation is respected. The fastest measured adult is about 1.38 m/s,
  so the margin is about 4.2x, not 7x. Quoting one derived number had hidden that spread.
- Reaching 5.84 m/s would still need the fastest fish to be under-read by about 4.2x. I found no evidence
  for a bias that large. Settling it needs an instantaneous peak at ≥1000 fps, which is exactly what
  Danos & Lauder 2012 recorded.

**Verdict: STRENGTHENS.** The conclusion "adult zebrafish fast-start peak is well below 5.84 m/s; gap not
closed" now rests on direct measurement (n = 50 adults, m/s, full text) instead of a Re-derived proxy. The
quoted margin should be revised from "~7x" to **"~4–7x"**, with the lower end set by the fastest individual.

### What would settle the residual uncertainty, and what it would cost (estimates, not quotes)
1. **Cheapest:** read the Danos & Lauder 2012 full text (1000 fps, centre-of-mass maximum velocity).
   The cost is library access, about $0 to $50 per article. Alternatively, allow `journals.biologists.com`
   or `sites.harvard.edu` in this session's network settings.
2. Download the Miln et al. figshare data (allow `api.figshare.com`/`figshare.com`) to replace my
   digitisation with the exact per-fish values and standard lengths. This costs nothing.
3. **Definitive:** film about 20 adult zebrafish (28 °C, TL measured) at ≥1000 fps with a calibrated scale,
   and take the instantaneous centre-of-mass peak from a smoothed position trace. A borrowed high-speed
   camera and an existing fish facility would cover it, at roughly 1–2 person-weeks. This is my estimate.

### Sources
- Miln, Ward & Seebacher 2021, R Soc Open Sci, doi:10.1098/rsos.210146. **full-text** (+ Fig. 1 image)
- Danos & Lauder 2012, J Exp Biol, doi:10.1242/jeb.068957. **abstract** (full text could-not-access)
- Li, Müller, van Leeuwen & Liu 2014, J R Soc Interface, doi:10.1098/rsif.2014.0848. **full-text**
- Ravel et al. 2025, iScience, doi:10.1016/j.isci.2025.112056. **full-text** (keyword-scanned)
- Bamford & Seebacher 2024, Biol Open, doi:10.1242/bio.060543. **full-text** (keyword-scanned)
- Bhattacharyya et al. 2020, Integr Org Biol, doi:10.1093/iob/obaa023. **full-text** (keyword-scanned)
- Miln et al. figshare collection doi:10.6084/m9.figshare.c.5359401. **could-not-access**
- S21 original record and its Re source. **could-not-access** (not in repo)

```swarm-result
{"subproblem": "S21-D", "evidence": "direct measurement (Miln et al. 2021, n=50 adults, 120 fps, full-text; values digitised from Fig. 1a by me)", "answer": "Directly measured per-fish maximum fast-start speeds of adult zebrafish span ~0.45-1.38 m/s, bracketing S21's Re-derived 0.842 m/s; the fastest individual is still ~4.2x below 5.84 m/s, so the conclusion holds on firmer evidence but the margin should read ~4-7x, not ~7x.", "key_number": "~1.38 m/s (fastest of 50 adults; bulk ~0.55-1.15 m/s; 120 fps, likely an underestimate of instantaneous peak)", "verdict": "strengthens"}
```
