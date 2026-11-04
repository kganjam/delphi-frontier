# Replication 260 — [S18] passive attitude modes of an engineered 0.4 g zebrafish glider

**Method:** I re-derived this independently from first-principles flight mechanics. I did **not** read the original derivation. I found no `harvest:zebrafish-aerial-attitude-k8hgr8` branch on `origin`: I ran `git ls-remote` and grepped for "zebra|attitude|k8hgr8|aerial". There are several `challenge-*zebrafish*` branches, and I deliberately did not open any of them. The only "recorded value" I compare against is the one quoted in the task prompt (pitch mode ~1–3 Hz, roll damping ~1–4 ms).

**Every number below is CALCULATED from a linear rigid-body model with assumed geometry. None of it is an observation.** No zebrafish glider exists. The "engineered" fin and wing dimensions are design assumptions I chose, not measurements.

## Inputs

| Input | Value / range used | Source | Read-level |
|---|---|---|---|
| Mass m | 0.4 g (fixed by the claim) | Claim text. Consistency check: FishBase length–weight relation for the subfamily, W = 0.00977·TL^3.04 (g, cm), gives 0.44 g at TL 3.5 cm. FishBase max SL is 3.8 cm. | claim: full-text. FishBase: **search-summary** (fishbase.se fetch blocked by network policy) |
| Body length L (pitch inertia arm) | 2.8–3.5 cm | My inference from the FishBase relation above (0.4 g ↔ TL ≈ 3.4 cm) | inference from search-summary |
| Body cross-section | height 0.2 L, width 0.1 L | **Assumed** (zebrafish are laterally compressed). No source read. | none (assumption) |
| Wing span b (engineered pectoral fins) | 4–7 cm | **Design assumption** | none |
| Mean chord c | 0.8–1.4 cm | **Design assumption** | none |
| Fin mass fraction | 3–8 % of m | **Assumption** | none |
| Glide C_L | 0.5–1.0 | **Assumption** (typical low-Re trimmed glide) | none |
| Lift slope a | 2πAR/(AR+2) (≈4.5 /rad at AR 5) | Standard finite-wing approximation, from memory | textbook, not re-read |
| Static margin SM | 0.05–0.25 c̄ | **Assumption**. This is the dominant uncertainty. | none |
| Pitch inertia I_yy | m L²/12 × (1.0–1.3) | Slender-rod approximation plus fin/tail add-on (assumption) | none |
| Air density ρ | 1.2 kg m⁻³ | standard | — |

Scope of literature search: two WebSearch queries, on zebrafish mass/length and on the strip-theory roll-damping coefficient. The second returned NACA/NASA listings but not the formula, so I derived the formula below myself. I fetched no zebrafish vestibular-latency source. Because of that, the claim's final clause ("active vestibular attitude control is not supported") is **not** tested here.

## Arithmetic (central case: L = 3.1 cm, b = 5.5 cm, c = 1.1 cm, C_L = 0.75, fin fraction 5 %)

- S = b·c = 6.05e-4 m². AR = b²/S = 5.0. a = 2π·5/7 = 4.49 /rad.
- Weight W = 0.4e-3 × 9.81 = 3.92e-3 N. Glide speed V = √(2W/(ρ S C_L)) = √(7.85e-3/(1.2 × 6.05e-4 × 0.75)) = **3.80 m/s**. Dynamic pressure q = ½ρV² = 8.65 Pa.
- Pitch stiffness M_α = q S c̄ a·SM. Inertia I_yy = 4e-4 × 0.031²/12 × 1.15 = 3.68e-8 kg m².
- Undamped short-period frequency f = √(M_α/I_yy)/2π:
  - SM 0.02 → 1.9 Hz
  - SM 0.05 → 3.0 Hz
  - SM 0.10 → 4.2 Hz
  - SM 0.15 → 5.2 Hz
  - SM 0.25 → 6.7 Hz
- Short-period damping ratio (rough hand estimate): the Z_α/(mV) term gives ≈14 s⁻¹ and the tail M_q term adds a little, so ζ ≈ 0.2–0.3. The damped frequency is therefore only ~3–5 % below the undamped value.
- Roll damping, by strip theory on a rectangular wing. Each strip sees Δα = p·y/V, so L_p = ∫ ½ρV² c a (p y/V) y dy over ±b/2 = ½ρV c a p · b³/12, which gives **L_p = ρ V S a b²/24**. Numerically: 1.2 × 3.80 × 6.05e-4 × 4.49 × 0.055²/24 = 1.56e-6 N m s.
- I_xx = body (m−m_f)(h²+w²)/12 + fins m_f b²/12 = 6.56e-9 kg m².
- Roll time constant τ = I_xx/L_p = **4.2 ms**.

Monte Carlo over the ranges in the table (2×10⁵ uniform draws; script at `replicate-260-model.py`), 5th / 50th / 95th percentiles:

| Quantity | 5 % | 50 % | 95 % |
|---|---|---|---|
| V (m/s) | 3.0 | 3.9 | 5.0 |
| Pitch short-period f (Hz) | 3.1 | 5.0 | 7.2 |
| Roll-rate τ (ms) | 2.7 | 4.6 | 7.5 |

## My value

- **Pitch mode ≈ 5 Hz (90 % range 3–7 Hz) for SM 0.05–0.25 c̄.** It reaches 2–3 Hz only for a small margin (SM ≲ 0.05 c̄).
- **Roll-rate damping time constant ≈ 4.6 ms (90 % range 2.7–7.5 ms).**
- Both are calculated, not observed. Both depend on assumed engineered geometry.

## Comparison with the recorded value (as quoted in the prompt)

- **Roll damping: AGREE in order of magnitude.** My range is 2.7–7.5 ms; the recorded range is 1–4 ms. They overlap at 2.7–4 ms. My central value (4.6 ms) sits just above the recorded upper bound. The difference is within plausible inertia and span choices.
- **Pitch mode: DISAGREE on the band.** My central value is 5 Hz, and my 90 % range is 3–7 Hz. The recorded range is 1–3 Hz. The bands meet only at ~3 Hz. Reproducing 1–3 Hz needs a static margin ≤ ~0.05 chord, or a pitch inertia ~3–5× larger than a slender-rod body gives. I cannot tell which assumption the original used, because I did not read it.
- **Qualitative claim ("only passive attitude holding is possible"):** my numbers support the passive half. A rear stabiliser with positive SM gives a stable, few-Hz, moderately damped pitch mode, and roll rate is damped within a few ms. I did not test the "active vestibular control is not supported" half, because I fetched no latency data. My inference is this: if vestibulo-motor latency is ≥ tens of ms, it is much longer than the ~5 ms roll and ~30–50 ms pitch time scales. That inference is unverified.

Overall: the order of magnitude and direction agree, but the specific pitch band does not reproduce. That makes this a partial disagreement driven by an unstated input (static margin and inertia), not an arithmetic error that I can identify.

```swarm-replication
{"claim_id": 260, "my_value": "pitch short-period ~5 Hz (90% 3-7 Hz); roll-rate damping tau ~4.6 ms (90% 2.7-7.5 ms); both calculated, not observed", "agrees": false, "note": "Roll damping overlaps the recorded 1-4 ms, but my pitch mode (3-7 Hz) is above the recorded 1-3 Hz unless static margin is <=0.05 chord; the passive-stability conclusion holds, and the vestibular clause was not tested."}
```
