# Replicate 291: does S30-D close the realisable LaMSA window?

**Status:** an independent re-derivation. **Every number below was calculated by me from stated inputs. None of them is an observation.**
**Claim tested:** S30-D, the deepening of S30, makes the realisable single-impulse LaMSA launch window fall away.

## 0. Contamination disclosure (read first)

- **What I saw:** to find where the inputs live, I ran `git show --stat` on `origin/claude/deepen-s30-launch-budget-jb7qj4`. Its commit message printed the S30-D result: "m\* drops from 38.9 mg to 0.94 mg (0.22–14 mg)", "w ≈ 15 J/kg muscle", derived as 0.5·σ0·ε/ρ, and "below the 37.5 mg … no realisable single-impulse window".
- **What I did not read:** `S30-deepen.md` and `S30-deepen_calc.py`. I also did not open `challenge-259.md` or `S30-D-deepen.md` on the other S30 branches.
- **What I did read:** the parent S30 document and script, `docs/research/fish/S30-organism.md` and `S30_scaling.py` on `origin/claude/s30-launch-budget-mass-k71prf`. That is where the model and its inputs live.
- **How I limited the contamination:** I deliberately did **not** reuse the σ0·ε/2ρ route for w. I estimate w from a different kind of evidence instead: measured teleost work-loop work per cycle. The comparison in §4 should still be read knowing that I saw their numbers first.

## 1. The model (from S30, read in full)

S30 writes the supply-to-need ratio at the anchor mass as R₀ = supply / need, with:

- supply = f · w · η_d · η_h
- f = 0.30: the fraction of body mass that is one side of the axial muscle
- η_d = 0.93: S29's drag factor
- η_h = 0.37: pike hydromechanical efficiency, inherited by S30 via S29 at abstract level
- need = 10.17 J/kg

The crossover is m\* = m₀ · R₀^(1/β), with m₀ = 0.25 g, α = 0 (LaMSA) and β ∈ {1/3, 0.533}.

**Sanity check of the transcription:** at w = 53, the supply is 0.30·53·0.93·0.37 = 5.471 J/kg. That matches S30's 5.47.

**Validity floor (my calculation, from S30's stated numbers).** S30 gives wing Re_air ≈ 712 at 38.9 mg. Re ∝ V·c ∝ m^(1/6)·m^(1/3) = m^(1/2). Re therefore reaches 700, the lower edge of S2's CL_max data, at 38.9·(700/712)² = **37.6 mg**. Below that mass, S30's CL_max input is an extrapolation.

## 2. My input: teleost spring-loading density w

**The only input I change is w.** S30 used 53 J/kg, a frog value. A teleost value is the point of S30-D.

| Input | Value | Source | Read-level |
|---|---|---|---|
| Teleost fast-fibre work per cycle, short-horned sculpin, isolated fibres | 2.7–3.7 J/kg at 4 °C; 1.2–1.6 J/kg at 15 °C | Springer-hosted study (link.springer.com/doi/10.1007/BF00373004) | **search-summary** |
| Sculpin fast fibres, optimal strain and stimulation | 3.5 J/kg | Johnston et al. 1993, J Exp Biol | **search-summary** |
| Optimal strain amplitude | ±5 % of resting length | same Springer study | **search-summary** |
| Upper envelope: vertebrate whole-muscle work density | 15 J/kg | Sutton et al. 2019 (bullfrog plantaris), as reported in S30, which read it FULL | **project** (I did not re-read it). **This is a frog value, not a teleost one.** |
| Fast-fibre power: *Scorpaena notata* 142.7 W/kg; Antarctic rock cod up to 290 W/kg | — | Wakeling & Johnston 1998, JEB 201:1505; St Andrews portal listing | **abstract / search-summary**. **Not used**: converting power to work needs a stage-1 duration, and I have no sourced duration. |

**What I tried and could not access:** the James et al. 1998 JEB PDF (cob.silverchair.com) and core.ac.uk 161930761. Both hosts are outside this session's network allowance: getaddrinfo failed, so the read-level is could-not-access. If those hosts were allowed in the network settings, the per-stage work values could be read directly.

**Negative search (scope: three web searches this session, standard mode):** I found **no measured single-contraction, spring-loading work density for any teleost muscle.** w for a teleost is therefore `unknown` as a direct measurement.

**My inference, separate from the authors' claims:**
- Work-loop net work per cycle is plausibly a *floor* for single-shot spring-loading work. A single shortening against a spring pays no re-lengthening cost.
- Whole-muscle work density of ~15 J/kg is a generous *ceiling*.

So my bracket is **w = 1.2 (low) / 3.5 (central) / 15 (envelope) J/kg muscle**.

## 3. Arithmetic (calculated)

R₀ = 0.30 · w · 0.93 · 0.37 / 10.17 = 0.010151 · w

| w (J/kg) | supply (J/kg body) | R₀ | m\* at β = 1/3 (R₀³ · 0.25 g) | m\* at β = 0.533 (R₀^1.876 · 0.25 g) |
|---|---|---|---|---|
| 1.2 | 0.124 | 0.0122 | 0.00045 mg | 0.064 mg |
| **3.5** | **0.361** | **0.0355** | **0.011 mg** | 0.48 mg |
| 15 | 1.549 | 0.152 | 0.88 mg | 7.3 mg |

**My value:**
- **Central:** m\* ≈ 0.01 mg, at w = 3.5 J/kg with isometric β.
- **Full range:** 0.0005–7.3 mg.
- The uncertainty spans roughly four orders of magnitude, and it is dominated by w.
- **Every cell is below the 37.6 mg validity floor.** The largest cell, 7.3 mg, is about 5× below it.
- **Conclusion (calculated, not observed):** with any teleost-plausible w that I could source, **no single-impulse LaMSA window exists in the regime where S30's inputs are valid.**
- For the window to reach 37.6 mg at β = 1/3, R₀ would need to be (37.6/250)^(1/3) = 0.532. That requires w ≈ 52 J/kg, essentially the frog value.

## 4. Comparison with the recorded value (made only after §3)

**Recorded value:** m\* = 0.94 mg (0.22–14 mg), at w ≈ 15 J/kg. I know it only from the commit message.

**Where we agree:**
- **The qualitative claim.** Both derivations put the whole window below the ~37.5 mg CL_max validity floor. Neither leaves a realisable window. I **AGREE** on this.

**Where we disagree:**
- **The central number.** My central estimate is ~85× lower (0.011 vs 0.94 mg). My central w is a measured work-loop value; their central w is a derived σ0·ε/2ρ upper bound.
- **The overlap.** My 15 J/kg envelope row (0.88–7.3 mg) overlaps their range. The overlap comes from a coincidentally equal w taken from a different source, a frog whole-muscle value. It is not two independent teleost measurements agreeing.
- **Not averaged:** I preserve the disagreement. Their figure is consistent with the *top* of my bracket.

**Caveats on independence:**
- The model structure (f, η_d, η_h, need, m₀, β) is shared, because both derivations inherit it from S30. **This replication tests only the w substitution and the floor, not S30's model.**
- I saw the recorded number before deriving (see §0).

```swarm-replication
{"claim_id": 291, "my_value": "m* ≈ 0.011 mg central (0.0005–7.3 mg), all below the ~37.6 mg Re_air=700 validity floor: no realisable LaMSA window", "agrees": true,
  "note": "Agree that the realisable window vanishes. My central m* is ~85x below the recorded 0.94 mg because I used measured teleost work-loop work (1.2–3.7 J/kg, search-summary) rather than a derived 15 J/kg bound. I saw the recorded value in a commit message before deriving."}
```
