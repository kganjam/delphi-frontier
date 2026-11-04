# Replication of claim 144 (S24-D-D): f_max as a 40 mm fish's escape ceiling

Independent re-derivation. I did **not** read `docs/research/fish/S24-D-deepen.md` or
`S24-D-deepen_calc.py` on `claude/deepen-s24-sensitive-input-j77gqs`, which hold the recorded
working. I saw only their file names in a `git diff --stat`. I took the upstream inputs from
the earlier S24 documents named below, and I read the primary source myself.

## 1. My value

- **Escape-frequency ceiling for a 40 mm adult zebrafish: ≈ 30–45 Hz (calc).** It could be as low
  as ≈ 23 Hz if frequency scales as L⁻¹. This is a size correction based on an **assumed** exponent.
  It is not a measurement.
- **Shortfall against the 61–81 Hz requirement: ≈ 1.35–2.7× (calc)**, and up to ≈ 3.5× under
  L⁻¹ scaling. At the unscaled 52 Hz maximum the shortfall is 1.17–1.56×.
- **Duration:** the inherited taxi needs 0.22–0.89 s at the target frequency (calc, S24). That
  is ≈ 12–46 beats at 52 Hz, or ≈ 13–72 beats at the required 61–81 Hz. The source reports escape
  sequences of "in general three to five" cycles.
- **Direction:** the negative strengthens. This is still a calculation, not a measured
  refutation, and none of it touches the 132–199 Hz Strouhal figure.

## 2. Inputs

| Input | Value | Source | Read-level | Kind |
|---|---|---|---|---|
| Target speed U | 1.95 m/s (3 BL glide) | S24 lineage, `S24-deepen_calc.py` on `claude/s24-deepen-launch-gap-2motub` (inherited from zebrafish-glide-physics.md) | full-text (repo) | calc, inherited |
| Body length L | 40 mm | same file, "project premise TL" | full-text (repo) | assumption |
| Stride length λ | 0.6–0.8 L per beat | Wardle 1975, as cited in `S24-deepen.md` | not read by me; inherited | measured in other species, applied to zebrafish by inference |
| Taxi time to 1.95 m/s | 0.22–0.89 s (net force 2–0.5 mN) | `S24-behaviour.md` §3.4 on `claude/s24-surface-taxiing-launch-tsepbn` | full-text (repo) | calc, assumed constant net force |
| Max escape frequency | **52 Hz**: "Across animals, the maximal frequency reached during escape was 52 Hz." | Kyriakatos et al. 2011, *J. Neurosci.*, PMC6623330 | **full-text** (100,000 of 101,006 characters read; the unread tail is the end of the page) | measured (EMG burst frequency) |
| Usual escape frequencies | "ranging from 30 to slightly >40 Hz"; "never observed motor activity during escape lower than 29 Hz" | Kyriakatos 2011 | full-text | measured (EMG) |
| Cycles per escape | "a few, in general three to five, short cycles of large EMG activity" | Kyriakatos 2011 | full-text | measured; author's description |
| n, animal size | "similar across animals (n = 8)"; "8–15 weeks old (body length 18–30 mm)" | Kyriakatos 2011 | full-text | measured |
| Size-scaling exponent b, f ∝ L⁻ᵇ | 0 (none), 0.3, 0.5 or 1.0 | **my assumption**. I looked up no source for zebrafish escape-frequency scaling, so its value for this species is `unknown` | — | assumption |

**What the source says, kept separate from what I infer.**

- *Author's claim:* 52 Hz is the maximum "across animals". Escape frequencies range "from 30 to
  slightly >40 Hz". Escapes come as 3–5 cycles. The fish were 18–30 mm long.
- *My inference:* 52 Hz is the single most extreme value in the dataset, not a typical
  ceiling. The text does not say which fish or what size produced it, so it could come from an
  18 mm fish. The values are EMG burst frequencies, not kinematic tail-beat frequencies. The paper
  does not show that the tail follows the EMG one-to-one at 52 Hz. That the source calls the
  values "instantaneous" is also my reading of the figure legends ("instantaneous burst
  frequency"), not a sentence written about the 52 Hz value.

## 3. Arithmetic

**Requirement** (recomputed): f_req = U / (λ L).
- λ = 0.8: 1.95 / (0.8 × 0.040) = 1.95 / 0.032 = **60.9 Hz**
- λ = 0.6: 1.95 / (0.6 × 0.040) = 1.95 / 0.024 = **81.25 Hz**

This reproduces the 61–81 Hz requirement S24-D states.

**Size correction** (calc, assumed b): f₄₀ = f_obs × (L_ref / 40)ᵇ, with L_ref from 18 to 30 mm.

| b | scale (L_ref 18 / 24 / 30 mm) | 52 Hz → | 30 Hz → | 42 Hz → |
|---|---|---|---|---|
| 0 | 1 / 1 / 1 | 52 | 30 | 42 |
| 0.3 | 0.787 / 0.858 / 0.917 | 40.9 / 44.6 / 47.7 | 23.6 / 25.7 / 27.5 | 33.1 / 36.0 / 38.5 |
| 0.5 | 0.671 / 0.775 / 0.866 | 34.9 / 40.3 / 45.0 | 20.1 / 23.2 / 26.0 | 28.2 / 32.5 / 36.4 |
| 1.0 | 0.450 / 0.600 / 0.750 | 23.4 / 31.2 / 39.0 | 13.5 / 18.0 / 22.5 | 18.9 / 25.2 / 31.5 |

I take the ceiling at 40 mm to be roughly 30–45 Hz. The low end is the usual unscaled escape
band, which needs no exponent. The high end is 52 Hz scaled with b = 0.5 from a mid-size fish,
or b = 0.3 from the smallest fish. With b = 1 the band drops to about 23–39 Hz. The band is a
judgement on assumed exponents, not a confidence interval.

**Shortfall** = f_req / f_ceiling:
- 52 Hz: 60.9/52 = 1.17; 81.25/52 = 1.56
- 45 Hz: 1.35–1.81
- 43 Hz: 1.42–1.89
- 40 Hz: 1.52–2.03
- 30 Hz: 2.03–2.71
- 23 Hz (b = 1, worst case): 2.65–3.53

The central band is therefore **≈ 1.35–2.7×**.

**Beats:**
- Time at a given frequency: 0.22–0.89 s (S24 §3.4, calc).
- At 52 Hz that is 11.4–46.3, so **12–46 beats**, matching S24.
- At 61–81 Hz it is 0.22 × 61 = 13 up to 0.89 × 81 = 72, so **13–72 beats**.
- The observed escape length is "in general three to five" cycles. The required run is
  therefore ≈ 2.4–24× longer than an observed escape sequence.

Caveat: the beat count assumes the S24 constant-net-force taxi, which is itself a calculation.

## 4. Limits

- Search scope: one full-text read of Kyriakatos 2011 (PMC6623330, 100k of 101k characters).
  I did no search for zebrafish escape-frequency scaling with length, or for kinematic (not EMG)
  maximum tail-beat frequency. Both remain `unknown` here.
- 52 Hz may not be a hard upper bound for an *untrained, motivated or designed* fish. This work
  is a calculation about the observed ceiling, not a measured impossibility.
- The 132–199 Hz Strouhal-based figure fell in S24-D on separate grounds. Nothing here restores it.

## 5. Comparison with the recorded value (done after §1–4)

I compared only against the claim text given in the task. I did not open the recorded working.

- **Ceiling:** recorded ~30–43 Hz; mine ≈ 30–45 Hz.
- **Shortfall:** recorded ~1.4–2.7×; mine ≈ 1.35–2.7×.
- **Duration:** recorded 12–46 beats vs 3–5 observed; I get 12–46 at 52 Hz and 13–72 at the
  required frequency. The recorded framing is the conservative one.

**Agreements:**
- 52 Hz is a single across-animal maximum, measured by EMG.
- The fish were 18–30 mm, n = 8.
- Escapes normally run 3–5 cycles.
- The usual escape band is 30 to slightly >40 Hz.

**Small difference:** the recorded upper ceiling (43 Hz) is a little below mine (45 Hz). This
comes from the choice of exponent and reference length, not from a different source.

**Verdict: AGREE.** The direction, the size of the shortfall and its status as a calculation all
match. I also agree that this does not restore 132–199 Hz.

```swarm-replication
{"claim_id": 144, "my_value": "40 mm escape ceiling ~30-45 Hz (calc, assumed exponent; ~23 Hz if f~L^-1); shortfall vs 61-81 Hz ~1.35-2.7x; needs 12-46 beats at 52 Hz (13-72 at 61-81 Hz) vs 3-5 observed", "agrees": true, "note": "Full-text Kyriakatos 2011 confirms 52 Hz is a single across-animal EMG maximum in 18-30 mm fish with usual escapes 30 to slightly >40 Hz in 3-5 cycles, and my independent size-corrected ceiling and shortfall match the recorded ~30-43 Hz / ~1.4-2.7x within exponent choice."}
```
