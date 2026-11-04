# Challenge 141: adversarial review of S1-D-D (zebrafish escape speed)

Status: desk review, 2026-11-04. **No experiment was run.** Every number not attributed to a paper
was **calculated** by me in this session, using the arithmetic in section 1. Tags follow the S1-D-D
convention: [observed], [derived], [calculated], [assumed].

**Claim under review (#141):** S1-D-D, branch `claude/deepen-s1-d-sensitive-input-3mdmls`,
`docs/research/fish/S1-D-deepen.md` and `s1_d_deepen_calc.py`. **Read-level: full-text**, both
files read with `git show` in this session. The claim reads: "a second independent source (Danos &
Lauder 2012, derived 0.84 m/s) contradicts S1-D's 0.95 m/s lower bound, so the no-aerial-takeoff
conclusion stands (lift ≤31% of weight under both sources) while the ballistic-exit claim falls
back to marginal (1.03 SL drag-free upper bound)."

**Verdict: WEAKENED.**
- Reading (A), no aerial takeoff, survives every attack I made.
- Reading (B), "ballistic exit falls back to marginal at 1.03 SL", does not follow from the
  author's evidence. It comes from dividing the apex reached at the speed of a 33 mm TL fish by the
  standard length of a 35 mm SL fish, which is a larger fish. With size matched, the Danos-derived
  apex is about 1.37 SL [calculated]. That is no worse than S1-D's 1.31 SL.
- The claimed "direct contradiction" between the two sources at the 0.95 m/s level is about 1.2
  combined standard errors [calculated]. That is not a demonstrated contradiction. The real
  contradiction is between the 0.84 m/s and 1.57 m/s peaks, and the author keeps it correctly.

## Sources and read-levels

| Source | Read-level | Used for |
|---|---|---|
| Danos & Lauder 2012, *J Exp Biol* 215:1854, doi:10.1242/jeb.068957 | **full-text via summarising fetch**: publisher HTML, characters 0–100,000, journals.biologists.com, this session. Tables and figures not read. The Lauder-lab PDF (sites.harvard.edu) and cob.silverchair.com were outside the network policy (DNS refused). | adults; TL 33.0 ± 1.3 mm; 5 fish; 1000 fps ventral view; CoM proxy = pectoral-fin midpoint; mean max Re 27,800 ± 2140 s.e.m. in "1 mPa s" water; Re computed from "fish length, maximum linear velocity per sequence and the appropriate viscosity"; no velocity in m/s stated; no water temperature stated |
| Ravel et al. 2025, PMC11930232 | full-text via summarising fetch, characters 0–100,000 | larval experiments at 28 °C, water μ = 0.83 mPa·s (used only in the temperature test, section 3) |
| S1-D-D doc and script | full-text | the claim, its inputs, and its `depends_on` |
| Demesmay et al. 2025 | **not re-read by me**. I rely on S1-D-D's quotations: 157 ± 27 cm/s; 3.8 ± 0.8 cm in 40 ms; n ≥ 11; SD | the second source |

## 1. Arithmetic, redone independently

These are recomputed from the stated inputs. I did not reuse the author's script.

- **Re inversion.** U = Re·μ/(ρL) = 27,800 × 1.0e-3 / (1000 × 0.033) = **0.842 m/s** [derived].
  The s.e.m. propagated from Re is ±0.065 m/s. This matches the author.
- **Apex.** h = v²/2g = 0.842² / 19.62 = **3.62 cm** [calculated].
  - Divided by the author's SL of 3.5 cm, that is 1.033 SL. This matches the author.
- **Flip threshold.** √(2g × 0.035) = 0.829 m/s, which is 12.8 % below 0.95 m/s. This matches
  "13 %".
- **Lift-to-weight.** L/W = ρ_air·S·C_L·v² / (2mg). At v = 1.84 m/s with the generous case
  (S = 4 cm², C_L = 1.5): 7.2e-4 × 3.386 / 7.848e-3 = **0.311** [calculated]. This matches "≤31 %".
  - Required speed in the generous case: √(7.848e-3 / 7.2e-4) = 3.30 m/s. This matches.

**Result:** no arithmetic error. The defect is in which inputs were paired together (section 3a),
not in the operations.

## 2. Is a proxy standing in for the quantity that matters?

- **For (B), yes, and the author partly flagged it.** Ballistic exit needs the *vertical CoM speed
  at the moment of crossing the surface*. Both sources give *horizontal* fast-start peaks.
  - Danos & Lauder filmed from a ventral view, so they captured horizontal-plane motion only
    [observed: "ventral view"].
  - Their CoM is a proxy, the pectoral-fin midpoint [observed].
  - The author lists "horizontal escape speed approximates water-exit speed" as an assumption.
    That is honest.
  - What the author does not quantify [calculated]: with drag ignored, the apex falls as sin²θ of
    the exit angle. At 0.84 m/s, the author's 1 SL (3.5 cm) needs θ ≥ 80° from horizontal.
    The size-matched 1 SL (2.64 cm, section 3a) needs θ ≥ 59°. So under any realistic oblique
    exit, every v ≤ 1 m/s row sits below threshold. The proxy matters more than the "drag-free
    upper bound" label suggests.
  - My inference: (B) is unresolved under every input. It is not "marginal at 1.03 SL".
- **For (A), the proxy cannot rescue takeoff.** Exiting the water costs speed, it does not add
  any. So using the in-water peak is conservative in favour of takeoff, and (A) still fails.

## 3. Hidden assumptions, relaxed

### 3a. Body length: the assumption that carries reading (B)

The script fixes `SL = 0.035` [assumed, "inherited from S1-D"]. It then applies a speed derived
from fish with **TL 33.0 mm** [observed]. TL is always greater than SL. Assuming SL ≈ 0.8 TL
(the author's own ratio), Danos's fish had SL ≈ 26.4 mm. The 1.03 SL figure therefore measures
the apex reached at the speed of a ~26 mm SL fish against the body length of a 35 mm SL fish,
about 33 % longer. The sensitivity table calls SL × 2 "implausible". But (B) depends on SL at the
±3 % level: v = 0.84 m/s clears 1 SL only if SL ≤ 3.62 cm [calculated]. So the reading sits right
at the length mismatch.

Size-consistent recompute [calculated; drag-free, vertical, which are upper bounds]:

| Pairing | v (m/s) | apex | apex / SL |
|---|---|---|---|
| Author: Danos speed vs. SL 35 mm | 0.84 | 3.62 cm | 1.03 |
| Same fish: Danos speed vs. Danos SL ≈ 26.4 mm (0.8 TL, assumed) | 0.84 | 3.62 cm | **1.37** |
| Same fish, if Re used SL | 1.05 | 5.62 cm | 2.13 |
| Danos length-specific speed (25.5 TL/s) scaled to the 35 mm SL fish (TL ≈ 43.8 mm) | 1.12 | 6.34 cm | 1.81 |

The last row's scaling assumes constant body-lengths per second. That is an assumption, not a
sourced allometry. Absolute escape speed is usually taken to rise with length, which is my
inference and not checked here. Under any of these consistent pairings, the Danos-derived apex is
≥ 1.3 SL. That is the same as or above S1-D's 1.31 SL. **On size-consistent inputs, Danos & Lauder
does not push (B) back to marginal.** (B) still fails to reach "supported", but for the
exit-angle and drag reasons in section 2, which applied equally to S1-D. It does not fail because
of the second source.

I did not retrieve the size of Demesmay's fish, or the SL of a 0.4 g zebrafish. Both are
`unknown` here. The SL that the question premise implies is the real open input.

### 3b. Is "contradicts the 0.95 m/s lower bound" a contradiction?

The author argues that a peak cannot lie below a 40 ms mean, so 0.84 < 0.95 is a contradiction.
That logic holds only for the same fish. Across these two samples [calculated]:

- Danos: 0.84 ± 0.065 m/s (s.e.m.).
- Demesmay 40 ms mean: 0.95 m/s. SD = 0.8 cm / 40 ms = 0.20 m/s, so s.e.m. ≤ 0.06 for n ≥ 11.
- Difference 0.11 m/s; combined s.e. ≈ 0.09 m/s; **z ≈ 1.2**.
- On top of that, the two samples come from different fish sizes, ages, stimuli and tracked points.

So the means are not shown to be inconsistent. "Contradicts" is too strong. The author's
reconciling option 3, that size or conditions differ, is not merely possible here; on these
numbers the gap is within noise. The firm, unreconciled disagreement is **0.84 vs 1.57 m/s**:
difference 0.73 m/s, combined s.e. ≈ 0.10, about 7 s.e. [calculated]. The author preserves this
one correctly in the key number.

### 3c. Viscosity and temperature

Danos & Lauder used the nominal "1 mPa s" for the treatment and stated no water temperature
[observed: not stated, over the 100,000 characters read]. If tanks were near 28 °C, the true μ is
about 0.83 mPa·s (Ravel et al. 2025, at 28 °C, a different study). That would make the authors'
nominal Re **understate** true Re. However, inverting with the same nominal μ the authors used
recovers their measured velocity whatever the real temperature was. **0.84 m/s is not affected.**
This attack fails.

### 3d. Reading (A) relaxed

- Peak + 2 SD (2.11 m/s), generous lift: L/W = 0.41 [calculated].
- Mass halved at peak + 1 SD: 0.62.
- Flipping (A) needs S·C_L/m about 3.2× above the generous case at v = 1.84 m/s.
- No relaxation I tried flips it. The lift inputs (S, C_L) remain **[assumed]**, as the author says.

## 4. Is the evidence level honest?

Yes.
- 0.84 m/s is labelled **derived** in the sentence, and so are its two assumptions (length basis,
  ρ). The 1.57 m/s is labelled observed.
- The verdict numbers are labelled calculated.
- The Danos read-level is stated as a summarising fetch with the figures unread. That matches what
  I could reach.

One imprecision: "lift ≤31 % of weight under both sources" uses Demesmay peak + 1 SD as the
worst case. "Under the bracket's upper end" would be more exact. This does not change the result.

## 5. Missed regime, taxon or counter-example

- **Regime: the surface crossing.** The model treats the exit as frictionless ballistics.
  Entrained water and the added-mass loss at the interface can only lower the apex, as the author
  says. No published zebrafish water-exit measurement was found. Scope: I did not run a separate
  search for one beyond the S1-D-D searches; I relied on those.
- **Taxon.** Small leaping cyprinids and hatchetfish (Gasteropelecidae) are the natural
  comparators for an exit. I did not retrieve any exit-speed number for them in this session, so
  their values are `unknown` and I do not use them.

## Summary

- **(A) stands.** I found no counter-argument.
- **(B)'s 1.03 SL comes from a length mismatch.** Danos & Lauder measured fish of about 26 mm SL,
  and the author compared their speed against a 35 mm SL threshold.
  - With size matched, the apex is about 1.37 SL (drag-free, vertical). That is no lower than
    S1-D's figure, so the second source does not demote (B).
  - (B) is still not supported, for a different reason: horizontal-to-vertical exit and drag.
    That caveat applies to every row, including S1-D's.
- **"Contradicts the 0.95 lower bound" is within about 1.2 combined s.e.** The 0.84 vs 1.57 m/s
  disagreement is real, and the author kept it.

```swarm-challenge
{"claim_id": 141, "outcome": "weakened", "reason": "Reading (A) survives, but reading (B)'s 'falls back to marginal at 1.03 SL' divides the apex at the speed of 33-mm-TL (~26 mm SL) Danos & Lauder fish by an assumed 35 mm SL; size-matched, the derived apex is ~1.37 SL (no lower than S1-D's 1.31), and the claimed contradiction with the 0.95 m/s bound is only ~1.2 combined s.e.", "corrected_value": "ballistic apex at Danos-derived 0.84 m/s = 3.6 cm = ~1.37 SL for a Danos-sized fish (SL ~26.4 mm, assuming SL = 0.8 TL); drag-free vertical upper bound, calculated", "depends_on": ["measured: Danos & Lauder 2012 doi:10.1242/jeb.068957 mean max Re 27,800 +/- 2140 s.e.m. at nominal 1 mPa s, TL 33.0 +/- 1.3 mm, N=5, 1000 fps ventral view, pectoral-fin midpoint (full-text via summarising fetch)", "derived: U = Re*mu/(rho*L) = 0.84 m/s with L = TL, rho = 1000 kg/m3, mu = 1 mPa s", "assumption: SL = 0.8 TL for Danos & Lauder fish (not stated by authors)", "assumption: Re length basis = total length (not stated by authors)", "measured (as quoted in S1-D-D, not re-read by me): Demesmay et al. 2025 doi:10.1371/journal.pbio.3003484 peak 1.57 +/- 0.27 m/s, 3.8 +/- 0.8 cm in 40 ms, n>=11", "assumption (inherited from S1-D): SL = 3.5 cm, m = 0.4 g, S = 1-4 cm^2, CL = 0.5-1.5", "model: drag-free ballistic apex h = v^2/(2g), vertical exit, upper bound", "model: L/W = rho_air S CL v^2/(2 m g), rho_air = 1.20 kg/m3", "S1-D-D claim: claude/deepen-s1-d-sensitive-input-3mdmls docs/research/fish/S1-D-deepen.md"]}
```
