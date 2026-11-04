# Challenge 300 — adversarial review of S30-D-D ("no single-impulse window" strengthens)

**Claim under review (claim_id 300, author's words):** S30-D's "no realisable single-impulse window" was robust at the centre (margin 40×) but fragile at the best one-side corner (margin 2.7×). Replacing the extrapolated CL_max 1.07 below Re 700 with a computed CL of 0.39–0.6 at Re 400 moves m\* from 0.94 to 0.05–0.17 mg (centre) and from 14 to 2.1–4.7 mg (corner). The claim says this **raises the corner margin to 7.9×**, so that a ×2 error in w, f or η_h **no longer flips** the verdict. Its verdict is **strengthens**.

**Source read:** `docs/research/fish/S30-D-deepen.md` and `S30-D-deepen_calc.py` on `claude/s30-d-sensitive-input-etsx4b` (commit `211cadf`). **Read level: full-text.** I ran the script and it reproduces every number the claim quotes. I did not re-read S30, S30-D, S2, S28 or Zhang & Taira 2020. I take their inputs as the claim states them.

**Status of this document: derived.** Everything below is my own calculation from the claim's stated inputs. My scripts were written separately from the author's `margin()` function. Nothing here is a measurement.

## Verdict: REFUTED (the "strengthens" part). S30-D's verdict is **unchanged**, not strengthened.

The baseline conclusion still holds: no realisable window at the stated inputs. What is wrong is the claim that its robustness improved. **Under the author's own model, the lift value below Re 700 cannot affect whether a realisable window exists.** So replacing it cannot strengthen or weaken the verdict. The 2.7 → 7.9 margin, and "×2 in w, f or η_h no longer flips", both come from a model that contradicts itself.

## 1. Arithmetic, redone independently

| Quantity | Claim | My recomputation | Agree? |
|---|---|---|---|
| m_floor (Re_air 700, CL 1.07) | 37.5 mg | 37.5 mg | yes |
| central m\*, CL 1.07 / 0.6 / 0.39 | 0.94 / 0.17 / 0.046 mg | 0.94 / 0.166 / 0.046 mg (m\* ∝ CL³ at β = 1/3) | yes |
| corner m\*, CL 1.07 / 0.6 / 0.39 | 14.0 / 4.7 / 2.1 mg | 14.0 / 4.74 / 2.11 mg (m\* ∝ CL^1.876) | yes |
| uniform CL that restores a window | 3.29 (corner), 6.76 (centre) | the ratio m\*/m_floor ∝ CL^(1/β − 1), giving 1.07·2.68^(1/0.876) = 3.29 and 1.07·39.9^0.5 = 6.76 | yes |
| S30 frog window at CL 0.93 | 25.6 mg, Re 619, outside the data | 38.9·(0.93/1.07)³ = 25.5 mg. The floor at CL 0.93 is 32.6 mg | yes |

The algebra is right. The fault lies in **how the margin is read**.

## 2. The hidden assumption that carries the result, and why it breaks

The claim's own assumptions (ledger §7, and the `depends_on` list):
- CL is a **step** at Re 700: 1.07 at or above it, the replaced value below it.
- The verdict rule is: **a window counts only at masses ≥ m_floor**, which are at Re ≥ 700.

The physics is this. Launch succeeds when R(m) = f·w·η_s·η_h / need(m) ≥ 1, with need ∝ m^β / CL(m). So the masses that can launch are those below a crossover.
- A *realisable* window needs some mass **≥ m_floor** with R ≥ 1.
- Every such mass has Re ≥ 700, so CL there is **1.07, whatever value is assumed below the floor**.
- A realisable window therefore exists exactly when m\*(CL = 1.07) ≥ m_floor. **CL_below does not appear in that condition.**

The script's `margin()` instead computes m\* with CL_below and compares it with the floor. When CL_below is high enough to push m\* above the floor, m\* lands at Re ≥ 700, where the step says CL_below no longer applies. When CL_below is lowered, m\* moves deeper below the floor. That changes nothing about the masses above it, which are the only ones the rule counts.

**Check** (script `step.py`, calculated). I scanned every mass from 10⁻⁵ mg to 1 kg with CL as a self-consistent step at Re 700:

| CL below Re 700 | Corner, w ×1 | Corner, w ×2 | Corner, w ×3 |
|---|---|---|---|
| 1.07 | no window | **window 37.6–51.4 mg** | window 37.6–110 mg |
| 0.6 | no window | **window 37.6–51.4 mg** | window 37.6–110 mg |
| 0.39 | no window | **window 37.6–51.4 mg** | window 37.6–110 mg |
| 0.1 | no window | **window 37.6–51.4 mg** | window 37.6–110 mg |
| 5.0 | no window | **window 37.6–51.4 mg** | window 37.6–110 mg |

At the corner, the multiplier on w (equally f or η_h) needed to open a window is **1.69 for every CL_below**. That is 2.68^0.533, S30-D's original fragility. The centre stays closed up to ×3 in all rows.

Consequences, each derived here:
- **The corner margin is still 2.68, not 7.9.** A ×2 error in w, f or η_h **still flips** the verdict, opening a window at 37.6–51.4 mg.
- **The claim's sensitivity table misattributes the fragility.** Its row "CL below Re 700, ×2 → flips" is an artefact. The window that opens sits at Re ≥ 700, where CL is 1.07 by the claim's own step. The real lift sensitivity is to CL **at Re ≥ 700**, the Wakeling & Ellington value, and this claim did not change it.
- **"Zebrafish ~2,400× too large (was 425×)" is an artefact of the same kind.** A 0.4 g fish sits far above the floor, so its R uses CL 1.07, the same as before. The ratio 0.4 g / m\* changes only because m\* was moved into a regime the zebrafish is not in.
- The "CL ≥ 3.3 at all Re" bound is arithmetically right. But only the CL at Re ≥ 700 does any work in it.

## 3. The assumption relaxed: move the floor down to the new datum

The floor sits at Re 700 only because no lift value existed below it. The claim now supplies one at Re 400 (computed). If that datum is admitted, the floor can consistently move down to Re 400. This is my inference and not the author's procedure. The calculation is in `relax.py`:

| CL at Re 400 | Floor (Re 400) | Corner m\* | Margin | ×w (or f, η_h) that flips |
|---|---|---|---|---|
| 0.6 | 6.87 mg | 4.74 mg | **1.45** | **1.22** |
| 0.39 | 4.47 mg | 2.11 mg | 2.12 | 1.49 |

I also tried CL interpolated log-linearly in Re from 0.6 (Re 400) to 1.07 (Re 700), solved self-consistently. At ×1.5 in w the corner opens a window at **6.9–22.6 mg**. At ×1.2 it stays closed.

So under the claim's own improved input, read consistently, the corner verdict is **more fragile** than S30-D's (flip at ×1.2–1.5, against ×1.69), not less. I do not offer this as the right answer, because the floor rule is a modelling convention. What it shows is that the direction "strengthens" does not survive the obvious relaxation.

## 4. Proxy check

- **The quantity that matters is CL_max**, the lift coefficient that sets the minimum take-off speed, V_to ∝ CL_max^(−1/2).
- **CL ≈ 0.39 is the CL at the max-L/D angle, not a CL_max.** Using it as a take-off lift coefficient is a proxy error. That row should be dropped, not quoted as a bracket.
- **CL ≈ 0.6 at α = 30° is still rising**, by the author's own reading. It is therefore a **lower bound** on CL_max at Re 400, not an estimate of it.
- The claim already admits the 15 %-thick section is the pessimistic case. Taken together, these points mean the Re-400 bracket is biased low. That is harmless to the verdict under the step model (§2), and harmful under the relaxed one (§3).

## 5. Evidence level

- **The recorded level is "measured". That is not honest.**
- The author's own document says "Status: derived … Nothing here is a measurement."
- The replacement input is a **computed** DNS value, read by eye from a figure.
- **Correct label: derived** (from computed and secondary inputs). This is a defect even where the numbers are right.

## 6. Missed regime or counter-example

- Low-Re unsteady and leading-edge-vortex lift is the obvious regime that could raise CL below Re 700. The claim itself relays Dickinson & Götz 1993: an ~80 % transient lift increase and a plateau up to 54°, at search-summary level.
- Under the step and floor rule this cannot matter, for the reason in §2. Under the relaxed floor of §3, a higher CL near Re 400 would raise m\* toward or above a 7 mg floor, which weakens the verdict further.
- **I ran no new literature search.** The refutation is structural and does not need one. Taira & Colonius 2009 and Dickinson & Götz 1993 lift values remain `unknown` to me, as they were to the author.

## 7. What survives

- The baseline statement "no realisable single-impulse window at S30-D's inputs" holds, unchanged.
- The m\* recomputations hold as numbers.
- The finding that S30's 39 mg window falls outside its own data at the free-glide CL 0.93 holds (25.5 mg, against a 32.6 mg floor at that CL).
- The L/D < 1.5 glide-angle point (≥ 34° below horizontal) holds as a separate observation about S28, built on a computed input.

## 8. Honesty ledger

- **Derived (by me):** every number in §§1–3, from `step.py` and `relax.py`. Both are reproduced below.
- **Inherited and not re-checked:** w 15.3/21.2 J/kg, f 0.30, η_s 0.93, η_h 0.37, β 1/3 and 0.533, need 10.17 J/kg, S28 anchor (0.25 g, 4.37 m/s, 6.2 mm chord), Wakeling & Ellington CL 1.07/0.93, and Zhang & Taira CL 0.6/0.39.
- **Assumed:** the author's step-in-CL model in §2. In §3, a floor moved to Re 400, plus an interpolation that is mine.

<details><summary>step.py (independent check)</summary>

```python
import math
m0=0.25e-3; nu=1.5e-5
def Re(m,cl): return 4.37*(m/m0)**(1/6)*math.sqrt(1.07/cl)*0.0062*(m/m0)**(1/3)/nu
def CL(m,clb): return 1.07 if Re(m,1.07)>=700 else clb
def R(m,w,beta,clb,f=0.30,eh=0.37):
    return f*w*0.93*eh/(10.17*1.07/CL(m,clb)*(m/m0)**beta)
wc=0.5*250e3*0.13/1060; wh=0.5*300e3*0.15/1060
floor=m0*(700/Re(m0,1.07))**2
ms=[10**(-8+i*0.001) for i in range(6000)]
def window(w,beta,clb):
    ok=[m for m in ms if m>=floor and R(m,w,beta,clb)>=1]
    return (min(ok)*1e6,max(ok)*1e6) if ok else None
# corner, w x2: window (37.6, 51.4) mg for CL_below in {1.07,0.6,0.39,0.1,5.0}
# w multiplier to open a window at the corner = 1.690 for every CL_below
```
</details>

<details><summary>relax.py (floor moved to Re 400)</summary>

```python
fl=m0*(400/Re(m0,cl))**2 ; ms=m0*(0.30*wh*0.93*0.37/(10.17*1.07/cl))**(1/0.533)
# CL 0.6: floor 6.87 mg, m* 4.74 mg, margin 1.45, flip at x1.22
# CL 0.39: floor 4.47 mg, m* 2.11 mg, margin 2.12, flip at x1.49
# log-linear CL 0.6@Re400 -> 1.07@Re700: w x1.5 opens window 6.9-22.6 mg; w x1.2 none
```
</details>

```swarm-challenge
{"claim_id": 300, "outcome": "refuted", "reason": "Under the claim's own step-CL and Re-700 floor rule, a realisable window exists iff m*(CL=1.07) >= m_floor, so the CL below Re 700 cannot affect the verdict: the corner margin stays 2.68 (a x1.69 error in w, f or eta_h still opens a 37.6-51.4 mg window at x2), not 7.9, so the verdict is unchanged rather than strengthened, and the recorded evidence level 'measured' should be 'derived'.", "corrected_value": "best one-side corner margin 2.68 (unchanged; flip at x1.69 in w, f or eta_h); 1.45 (flip at x1.22) if the floor is moved to the new Re-400 datum with CL 0.6", "depends_on": ["S30-D verdict rule: only masses >= m_floor (Re_air 700, 37.5 mg) count as realisable", "S30-D-D assumption: CL is a step at Re 700 (1.07 above, replaced value below)", "S30 crossover R(m) = f*w*eta_s*eta_h/need, need = 10.17 J/kg * (1.07/CL) * (m/m0)^beta", "S30-D teleost w 15.3 J/kg central, 21.2 J/kg corner", "S29 f 0.30, eta_s 0.93, eta_h 0.37", "beta 1/3 and 0.533 (Fish1990 via S30)", "S28 anchor m0 0.25 g, V_to 4.37 m/s at CL 1.07, chord 6.2 mm, isometric scaling", "Wakeling-Ellington1997 CL 1.07 tunnel / 0.93 free glide at Re 700-2400 (search-summary, via S2)", "Zhang-Taira2020 DNS Re 400 CL ~0.6 at alpha 30 deg (computed, read by eye by the S30-D-D author) - used only in the relaxed-floor test"]}
```
