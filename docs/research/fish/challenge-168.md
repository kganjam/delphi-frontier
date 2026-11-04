# Challenge 168: adversarial review of S1-D (zebrafish takeoff speed)

**Claim under review** (from `harvest:zebrafish-takeoff-deepen-2gwq0o`, file
`docs/research/fish/S1-deepen.md` on branch `claude/zebrafish-takeoff-deepen-2gwq0o`, read in full):

> "No: replacing Plaut's sustained U_crit (0.56 m/s) with a measured adult escape burst speed
> (0.95 m/s robust lower bound, 1.57 m/s reported peak) still leaves a 0.4 g zebrafish ~3.6x short
> of the ~5.7 m/s airspeed its body could need to support its weight in air (calculated), although
> the same speed would, drag-free, suffice to throw it clear of the water (calculated, not
> observed)." Recorded evidence level: **measured**. Verdict: **stands**.

No experiment was run for this review. Everything below is either the author's statement (marked
as such), my **[calculated]** result, or my **[inference]**. I did no new literature retrieval. I
read only the author's document and script. Where I make a point about the literature, I give the
scope of what I did not search.

## 1. Independent arithmetic [calculated]

Inputs as stated: m = 0.4 g, g = 9.81 m s⁻², ρ_air = 1.20 kg m⁻³. For the central case, S = 2 cm²
and C_L = 1. Both of those are **assumed** by the author; neither was measured.

- W = 0.4e-3 × 9.81 = 3.924 mN.
- v_req = √(2W / (ρ S C_L)) = √(7.848e-3 / 2.4e-4) = √32.7 = **5.72 m s⁻¹**. This matches the "~5.7".
- 5.72 / 1.57 = **3.64×**. This matches the "~3.6×", but **only against the reported peak**.
  Against the 0.95 m s⁻¹ lower bound, which is quoted in the same sentence, the shortfall is
  **6.0×**.
- 0.038 m / 0.040 s = 0.95 m s⁻¹. This is a valid lower bound on peak speed: the mean of a
  displacement over a window cannot exceed the window's maximum speed. If the 40 ms window starts
  at the stimulus rather than at response onset, the bound is only made more conservative.
- Ballistic height: h = v²/2g. That gives 4.6 cm at 0.95 m s⁻¹ and 12.6 cm at 1.57 m s⁻¹. Both
  match the author.

No arithmetic error found.

## 2. Proxy check

The author already replaced the sustained-speed proxy (U_crit) with burst speed. Two proxies remain:

1. **Horizontal in-tank escape speed standing in for water-exit speed.** The author flags this.
   [inference] An exit through the surface is slower than a free horizontal escape, because of
   surface tension, wave drag and a non-optimal posture. After exit there is no thrust, because a
   zebrafish has no taxiing tail-in-water phase that has been documented. Airspeed can therefore
   only **decay** below the exit speed. Both effects push the true airspeed *below* 0.95–1.57 m s⁻¹.
   So this proxy biases the claim toward feasibility. It cannot overturn the "No".
2. **S = 2 cm², C_L = 1 standing in for the fish's real lifting capacity.** These are assumed. The
   author's own bracket (S = 1–4 cm², C_L = 0.5–1.5) gives v_req = **3.3–11.4 m s⁻¹** [calculated,
   reproduced]. [inference] For a ~3.5 cm cyprinid, a planform of 2 cm² with C_L = 1 is generous:
   the pectoral fins are small and the body is a low-aspect-ratio lifting surface. So the central
   5.7 m s⁻¹ is more likely an underestimate than an overestimate. I did not retrieve a measured
   zebrafish planform area or a body C_L. Both remain `unknown` as measurements.

## 3. Hidden assumption, relaxed [calculated]

The "~3.6×" figure rests on the assumed S·C_L. Here is the shortfall across the author's own bracket:

| Case | v_req (m s⁻¹) | vs 0.95 | vs 1.57 | vs 1.84 (peak + 1 SD) |
|---|---|---|---|---|
| Most generous: S = 4 cm², C_L = 1.5 | 3.30 | 3.5× | 2.1× | **1.8×** |
| Central: S = 2 cm², C_L = 1 | 5.72 | 6.0× | 3.6× | 3.1× |
| Least generous: S = 1 cm², C_L = 0.5 | 11.4 | **12.0×** | 7.3× | 6.2× |

Ground effect: a ~1.5× boost to C_L in the central case gives v_req = 4.67 m s⁻¹, which is still
3.0× above the 1.57 m s⁻¹ peak.

**The "No" survives every corner of the bracket.** Even the most favourable combination still
leaves a shortfall of 1.8× in speed, which is 3.2× in dynamic pressure. Pushing it to "yes" would
need S·C_L above ~20 cm² at 1.84 m s⁻¹. That is not credible for a 3.5 cm fish [inference].
However, **"~3.6×" is a point value of an assumed-input calculation**. The defensible statement is
a range: **1.8×–12×**, with a central value of 3.6× against the peak and 6.0× against the lower
bound. The single figure, quoted in a sentence that also names the 0.95 m s⁻¹ lower bound,
overstates precision. It also silently picks the favourable speed.

## 4. Is the evidence level honest?

- The claim *sentence* is honest: it tags both conclusions "(calculated)", and the ballistic one
  "(calculated, not observed)".
- The *recorded* evidence level, **"measured"**, is not honest for the claim as a whole. The
  headline result (3.6× short of 5.7 m s⁻¹) is **calculated** from one measured input (burst
  speed) and two **assumed** inputs (S, C_L). The author's own `swarm-result` evidence string says
  "lift inputs assumed; result calculated". The "measured" label therefore contradicts the source
  it was harvested from.
- In the KEY number, 0.95 m s⁻¹ is **derived** (3.8 cm ÷ 40 ms), not measured directly. The
  author labels it [calculated] in the source, but the KEY places it under "measured". The
  derivation is trivial and robust, so this matters less. It is still a calculated value.
- The 1.57 m s⁻¹ is the authors' "calculated maximal speed" (Demesmay et al. 2025, as reported by
  the S1-D author at full-text read-level; I did not re-read it). It is derived from manual
  tracking at 240 fps, and the S1-D author notes it may be biased upward. The per-fish data were
  not deposited (author's report). A *lower* true peak only strengthens the "No".

Correct label: **calculated (from one measured burst speed plus assumed lift inputs)**.

## 5. Missed regime, taxon or counter-example

- **Freshwater hatchetfishes (Gasteropelecidae)** are the obvious small-fish counter-example
  class: small characins that leave the water. [inference, from background knowledge, not
  retrieved in this session] I am not aware of published evidence that they achieve
  lift-supported flight, rather than a leap or skitter. **Scope: I ran no search on this.** It is
  a gap in both the S1-D work and this review. Their exit speeds and masses are `unknown` here.
  Even so, the "No" concerns *zebrafish*, and the calculation above does not depend on any taxon
  comparison.
- **Regime:** the "support its weight in air" criterion assumes steady lift. A leap supported
  ballistically (Reading B) is a different regime. The claim correctly keeps the two apart and
  does not count the ballistic exit as takeoff.
- I found no counter-example that flips Reading A. My negative scope is limited to reasoning:
  I did no literature search beyond reading the author's document.

## Verdict: WEAKENED (narrowly). The substance survives; the stated precision and the evidence label do not.

The core answer, **No**, survives every test I could apply. The arithmetic reproduces. The
remaining proxies all bias *toward* feasibility. Even the author's most generous lift assumptions
leave a ≥1.8× speed gap. Two defects remain. First, the recorded evidence level "measured" is
wrong for a result that is calculated and rests on assumed lift inputs. Second, "~3.6×" is
presented as the shortfall when it is the central case against the most favourable speed. Across
the author's own input bracket and speed range, the shortfall is 1.8×–12×. Neither defect changes
the yes/no answer.

```swarm-challenge
{"claim_id": 168, "outcome": "weakened", "reason": "Conclusion 'No' is reproduced and robust across the author's own S and C_L bracket, but the ~3.6x shortfall is a point value from assumed lift inputs against the most favourable speed (range 1.8x-12x), and the recorded evidence level 'measured' should be 'calculated (measured burst speed + assumed S, C_L)'.", "corrected_value": "speed shortfall 1.8x-12x (calculated; central 3.6x vs 1.57 m/s peak, 6.0x vs 0.95 m/s lower bound; v_req 3.3-11.4 m/s, central 5.7 m/s)", "depends_on": ["m = 0.4 g (given)", "rho_air = 1.20 kg/m^3, g = 9.81 m/s^2 (standard)", "S = 1-4 cm^2 and C_L = 0.5-1.5 (assumed by S1-D author, not measured)", "Demesmay et al. 2025 adult zebrafish escape: 1.57 +/- 0.27 m/s peak and 3.8 cm in first 40 ms (as reported by S1-D author, full-text; not re-read by me)", "assumption that airspeed after water exit cannot exceed underwater burst speed (no taxiing phase documented for zebrafish)"]}
```
