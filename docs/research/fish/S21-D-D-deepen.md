# S21-D-D-D: deepening S21-D-D on its weakest input

Project: `zebrafish-flight` · Scale: behaviour · Written 2026-11-04
Branch: `claude/s21-d-d-sensitive-input-c6ylbu` · Script: `docs/research/fish/S21-D-D-deepen-sim.py`
(numpy, seed fixed; **every number it prints is calculated or simulated, none is observed**).

## The parent answer being attacked

S21-D-D is `docs/research/fish/S21-D-deepen.md`, commit `6b64006b`, branch
`claude/deepen-s21-sensitive-input-mxp5t8`. Read-level: full-text (repo doc). Its claims:

- The fastest adult fish in Miln, Ward & Seebacher 2021 reads **1.38 m/s** (S21-D-D's digitisation of
  Fig. 1a; 120 fps, max of 4 trials).
- S21-D-D ran a simulation of the frame-rate and noise bias, scaled to 1.38 m/s. It puts the true peak
  at **0.99–1.58 m/s**.
- Against the corrected stall threshold, 4.37 m/s (C_L,max 1.07; band 4.22–4.77), the margin is
  **≈2.7–4.8×**.
- **Verdict: stands**, meaning the fish's burst speed does not reach take-off stall speed.

> **Short answer.**
>
> - **Most sensitive input:** still U_fast, the fastest fish's true peak speed (elasticity −1).
> - **The weakest part of U_fast** is the one assumption that guards the gap-closing direction: S21-D-D's
>   speed-pulse rise time, t_p ≥ 5 ms. S21-D-D labelled it "an assumption; I have no adult zebrafish
>   source for it".
> - **Searches did not find a measured value for that rise time** (scope in §2).
> - **I replaced that assumption with a physical bound** (calculated, not observed):
>   - For a 120 fps under-read to hide a true peak at the stall speed, the rise time must be
>     **t_p ≤ 1.4–1.7 ms**.
>   - That implies about **600–860 g** of peak acceleration and **≥11,000–38,000 W/kg of muscle**, even
>     before added mass and drag are counted.
>   - The highest muscle power in the project's law library that I could trace to a primary source is
>     **461 W/kg**.
> - **Even S21-D-D's own corner case (t_p = 5 ms at 1.58 m/s) needs ≈945 W/kg of muscle.** That is
>   already above the verified ceilings.
> - **The self-consistent upper bound on the true peak is ≈1.41–1.48 m/s** against the 461 W/kg ceiling.
>   It is **≤1.76 m/s** even against an unverified 1,200 W/kg ceiling.
> - **Verdict: STRENGTHENS.** "The gap is not closed" no longer rests on an assumed rise time. Closing it
>   would need muscle power ≥23× the traced ceiling, and ≥9× even the unverified one.
> - **The lower end of the margin is now set by C_L,max, not by U_fast.** Admitting the law library's
>   bird C_L,max of 1.6 lowers the floor to about 2.4× (about 2.0× under the unverified ceiling).

---

## 1. Which input is the conclusion most sensitive to? (recomputed)

The margin is M = V_s / U_true, with V_s = √(2mg / (ρ·S·C_L,max)). The conclusion "gap not closed" is
equivalent to M > 1. All values below are calculated by the script, §1–2.

| Perturbation, from central V_s = 4.37 m/s and U = 1.38 m/s (M = 3.17) | M |
|---|---|
| U ×2 alone | 1.58 |
| m ÷2, C_L,max ×2 or S ×2, alone (each enters as a square root) | 2.24 |
| U ×2 **and** m ÷2 (or U ×2 and C_L,max ×2) | 1.12 |
| m ÷2, C_L,max ×2 and S ×2 together (all threshold inputs) | 1.12 |
| U ×2, m ÷2 and C_L,max ×2 together | **0.79 (flips)** |

- **No single 2× error flips the conclusion.** This repeats S21-D-D's finding.
- **A coordinated error can flip it.** That needs U wrong by about 2× *together with* at least two
  threshold inputs. Every flipping combination includes a ~2× error in U, the only input with
  elasticity 1.
- So U_true remains the input to attack. Whether a 2× error in U is possible depends on S21-D-D's
  bias band, specifically its lower edge: the 120 fps reading **under**-reads the true peak by at most
  0.875×. That edge is fixed by the assumed rise time, t_p ≥ 5 ms. Tracking noise biases the reading
  *upward*, which only helps the conclusion. So the rise time is the only sub-input that could open a
  path to closing the gap.

## 2. How well established is the rise time? Not at all; it is an assumption

- **S21-D-D's own label:** "t_p = 5, 10 or 20 ms. This range is an assumption; I have no adult
  zebrafish source for it." (full-text, repo).
- **Danos & Lauder 2012, J Exp Biol 215:1854** (doi:10.1242/jeb.068957, PMID 22573764). Read-level:
  **abstract** (Europe PMC).
  - The authors filmed adult escapes at 1000 fps.
  - They report that viscosity "increased … time to maximum linear velocity of the center of mass".
  - They also report displacement "during stage 1 and after 30 ms".
  - So the quantity was measured. **Its value is not in the abstract.** Table 1 is
    **could-not-access**: `dash.harvard.edu` does not resolve from this session, and
    journals.biologists.com returns 403.
- **Miln et al. 2021** (PMC8025299). Read-level: full-text.
  - Confirms the method: 120 fps GoPro Hero 6, 405 × 600 mm tank with 30 mm water depth, a submerged
    300 mm ruler as scale, manual Tracker tracking at 0.35 BL, fastest of 4 trials, 23 °C.
  - It gives no rise time, no fish masses and no standard lengths.
  - The review history in the Europe PMC supplementary bundle has none of these either (full-text,
    keyword-scanned).
- **Miln Dryad data** (doi:10.5061/dryad.v15dv41tr): **could-not-access**. `datadryad.org` gave no
  connection from this session.

**Scope of the negative search for an adult time-to-peak value:**

- Europe PMC query `(zebrafish OR "Danio rerio") AND ("fast start" OR "fast-start" OR "C-start" OR
  "escape response") AND (acceleration OR "peak velocity" OR "maximum velocity") AND adult`:
  - 158 hits; the first 60 titles screened.
  - Five full texts keyword-scanned: PMC11930232, PMC12180146, PMC12604801, PMC12783434, PMC9247716.
  - None gave an adult zebrafish time to peak COM speed. The modelling and kinematic papers appear to
    concern larvae. I keyword-scanned them and did not read them in full.
- Two standard web searches, read-level search-summary. They surfaced only the Danos & Lauder abstract.
- Not covered: paywalled journals, theses, non-English literature.

**Evidence level of t_p: assumption (unmeasured in any source I could read).**

## 3. Improving it: a power bound in place of the assumed rise time

These results are calculated and simulated, not observed. I used S21-D-D's pulse model:

- an alpha pulse, v(t) = V·(t/t_p)·e^(1−t/t_p);
- 120 fps sampling with random phase, max of 4 trials;
- **zero tracking noise**. Noise inflates the reading, so zero noise is the setting most favourable to
  closing the gap.

**Step A: the under-read factor r = reading / true peak, simulated (script §3).**

| t_p (ms) | 0.5 | 1.0 | 1.5 | 2.0 | 2.5 | 3.0 | 4.0 | 5.0 |
|---|---|---|---|---|---|---|---|---|
| r | 0.062 | 0.188 | 0.342 | 0.479 | 0.602 | 0.696 | 0.813 | 0.878 |

At t_p = 5 ms this reproduces S21-D-D's 0.875 to within Monte Carlo error.

**Step B: what closing the gap would require** (calculated from Step A).

The 1.38 m/s reading must hide a true peak equal to V_s. The power figure is the peak rate of change of
the COM's kinetic energy: P/m = max(v·a) = 0.852·V²/t_p. It ignores added mass, drag and lateral body
motion, so it is a **lower bound** on the true demand.

| Threshold V_s | Required r | Required t_p | Peak accel. e·V/t_p | P per kg body | P per kg muscle (muscle fraction 0.3 / 0.45 / 0.6, *assumed*) |
|---|---|---|---|---|---|
| 4.21 m/s (C_L 1.15) | ≤0.327 | ≤1.45 ms | 804 g | 10,400 W/kg | 34,700 / 23,100 / 17,400 |
| 4.37 m/s (C_L 1.07) | ≤0.316 | ≤1.42 ms | 856 g | 11,500 W/kg | 38,300 / 25,500 / 19,200 |
| 3.57 m/s (C_L 1.6) | ≤0.386 | ≤1.66 ms | 596 g | 6,500 W/kg | 21,800 / 14,500 / 10,900 |

**The ceilings to compare against** come from the project law library,
`library/laws/muscle-power-density.yaml`, branch `claude/muscle-power-density-thmr16`, commit
`ee469aeb`. Read-level: full-text (repo). Its own sources are relayed at search-summary level unless
marked otherwise.

- Quail pectoralis cyclic: 390 W/kg.
- Frog plantaris isotonic, temperature-adjusted to 28 °C: 397–461 W/kg. This is Marsh 2022's
  extrapolation, which the library read in full text via PMC.
- The "highest instantaneous" 1,200 W/kg. The library itself flags this as "could NOT find the number
  in the abstracts of the primary papers … Do not design against it without the primary text."
- **No fish white-muscle value is in the library.** It records scup white-muscle power as `unknown`.

**Inference (mine):** closing the gap needs ≥10,900 W/kg of muscle even at the most generous corners
(C_L 1.6, muscle fraction 0.6, no added mass or drag). That is **≥23× the 461 W/kg traced ceiling** and
**≥9× the unverified 1,200 W/kg**. The rise time needed for the gap to close is physically excluded.

**S21-D-D's own lower corner fails the same test** (script §4, calculated). A true peak of 1.58 m/s
with t_p = 5 ms needs 425 W/kg of body mass, which is **≈945 W/kg of muscle** at an assumed muscle
fraction of 0.45. That is above every traced ceiling.

**Step C: the self-consistent bound** (script §5, simulated and calculated). I took the largest true
peak V = 1.38 / r(t_p) for which the power demand 0.852·V²/t_p stays within (ceiling × muscle
fraction).

| Power ceiling | Muscle fraction (assumed) | Max true peak | at t_p | M at V_s 3.57 / 4.21 / 4.37 |
|---|---|---|---|---|
| 461 W/kg (traced) | 0.30 | 1.41 m/s | 12.3 ms | 2.53 / 2.98 / 3.09 |
| 461 W/kg (traced) | 0.45 | 1.45 m/s | 8.6 ms | 2.47 / 2.91 / 3.02 |
| 461 W/kg (traced) | 0.60 | 1.48 m/s | 6.8 ms | 2.40 / 2.84 / 2.94 |
| 1,200 W/kg (unverified) | 0.30 | 1.54 m/s | 5.6 ms | 2.32 / 2.74 / 2.84 |
| 1,200 W/kg (unverified) | 0.45 | 1.66 m/s | 4.3 ms | 2.16 / 2.54 / 2.64 |
| 1,200 W/kg (unverified) | 0.60 | 1.76 m/s | 3.7 ms | 2.02 / 2.39 / 2.48 |

**Improved input, calculated and not measured.** The true peak of the fastest Miln fish is
**U_true ≤ ≈1.41–1.48 m/s** under the traced 461 W/kg ceiling, and **≤1.76 m/s** under the
unverified 1,200 W/kg. The lower edge stays S21-D-D's 0.99 m/s, which comes from noise inflation and is
not re-examined here. A 2× error in U (a true peak of 2.76 m/s) would need t_p ≈ 2.1 ms. That is
≈3,100 W/kg of body mass, or ≈6,900 W/kg of muscle at fraction 0.45, so it is excluded.

**What would replace this bound with a measurement, and the cost** (my estimates):

1. **Read Danos & Lauder 2012 Table 1** for the time to maximum linear COM velocity of adults at
   1000 fps. Allow `dash.harvard.edu` in the session's network settings: $0. Or use library access:
   ~$0–50.
2. **Read the Miln Dryad data** for per-fish values and lengths. Allow `datadryad.org`: $0.
3. **Measure fish white-muscle power directly**, for example zebrafish fast-muscle work loops. This is a
   lab study of several person-weeks. It would replace the mammal, bird and frog ceilings.
4. **Measure a definitive adult escape at ≥1000 fps**, as S21-D-D specified: ~1–2 person-weeks with a
   borrowed camera.

## 4. Recomputed conclusion

- **STRENGTHENS.**
  - S21-D-D's "gap not closed" depended on the assumed rise time (t_p ≥ 5 ms). It now rests on a
    physical bound instead.
  - Closing the gap needs a ≤1.7 ms speed rise, ≈600–860 g, and ≥10,900 W/kg of muscle as a lower
    bound. That excludes it by more than an order of magnitude against every ceiling in the law library.
- **The upper edge of U_true tightens** from S21-D-D's 1.58 m/s to ≈1.48 m/s (traced ceiling). Within
  S21-D-D's own C_L,max band (0.9–1.15), the margin floor moves from 2.67× to **≈2.84×**.
- **The margin's weakest input is now C_L,max, not U.** The law library
  (`library/laws/takeoff-stall-speed.yaml`, commit `0e202f2f`; full-text repo, sources at
  search-summary) lists measured whole-animal values for gliding animals: Harris hawk ≥1.6 (a lower
  bound), bat 1.5. If a fin-wing could match them, V_s drops to 3.57 m/s. The margin floor is then
  **≈2.4×**, or ≈2.0× under the unverified power ceiling.
- **The disagreement over C_L,max is preserved, not averaged.** The dragonfly-wing proxy is 1.07–1.15.
  The bird and bat values are 1.5–1.6. Which applies to a pectoral-fin membrane is `unknown`.
- **The defensible margin for the fastest adult is ≈2.4–4.8×**, with C_L,max up to 1.6 admitted. It is
  **≈2.8–4.8×** within S21-D-D's C_L band. **None of the combinations I tested reaches M ≤ 1.**

### Caveats

- **The power bound uses an assumed pulse shape (alpha), COM kinetic energy only, and an assumed muscle
  fraction (0.3–0.6) for which I have no zebrafish source** (`unknown`). Added mass, drag and lateral
  motion would all *raise* the demand, so the bound is conservative toward closing the gap. A
  differently shaped pulse would change the 0.852 factor and the r(t_p) curve. I did not test other
  shapes.
- **None of the power ceilings is a fish white-muscle measurement.** A fish white-muscle ceiling above
  ~10,000 W/kg would be needed to reopen the question. I have no evidence of one, but I also have no
  fish value at all.
- The design premises are unchanged from S21-D-D, and the primary source for the 0.4 g mass is still
  `unknown`. Air density is 1.2 kg/m³.
- This is still an in-water burst speed used as a proxy for water-exit speed.

## Sources

| Source | Read-level |
|---|---|
| S21-D-D: `docs/research/fish/S21-D-deepen.md` + `-sim.py` (commit 6b64006b) | full-text (repo) |
| Law library `muscle-power-density.yaml` (commit ee469aeb) | full-text (repo); its sources search-summary except Marsh 2022 (full-text via PMC, as stated by the library) |
| Law library `takeoff-stall-speed.yaml` (commit 0e202f2f) | full-text (repo); its sources search-summary |
| Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146, PMC8025299, incl. review history | full-text |
| Miln et al. Dryad, doi:10.5061/dryad.v15dv41tr | could-not-access |
| Danos & Lauder 2012, J Exp Biol 215:1854, doi:10.1242/jeb.068957 | abstract (Europe PMC); Table 1 could-not-access |
| PMC11930232, PMC12180146, PMC12604801, PMC12783434, PMC9247716 | full-text, keyword-scanned only |

```swarm-result
{"subproblem": "S21-D-D-D", "evidence": "calculated + simulated bound (my Monte Carlo and kinetic-energy power bound, not observation) on a measured input (Miln et al. 2021 Fig. 1a, full-text, digitised by S21-D-D); rise time itself remains unmeasured (Danos & Lauder 2012 Table 1 could-not-access)", "answer": "S21-D-D's conclusion is still most sensitive to the fastest adult's true peak speed, and its only gap-closing path was the assumed >=5 ms speed rise time; replacing that assumption with a muscle-power bound shows that hiding a stall-speed peak behind the 120 fps reading needs a <=1.7 ms rise, ~600-860 g and >=10,900 W/kg of muscle (>=23x the 461 W/kg traced ceiling), so the true peak is <=~1.48 m/s (<=1.76 m/s even at an unverified 1200 W/kg) and the gap stays open, with the remaining margin uncertainty (~2.4-4.8x) now set by C_L,max rather than fish speed.", "key_number": "fastest adult zebrafish true peak fast-start speed <= ~1.41-1.48 m/s (power-bounded at 461 W/kg muscle; <= 1.76 m/s at 1200 W/kg); closing the gap requires t_p <= 1.4-1.7 ms and >= 10,900 W/kg muscle", "verdict": "strengthens", "depends_on": ["S21-D-D (commit 6b64006b): fastest Miln fish reads 1.38 m/s, true peak band 0.99-1.58 m/s, margin 2.7-4.8x", "Miln, Ward & Seebacher 2021 (doi:10.1098/rsos.210146) Fig. 1a fastest-fish 1.38 m/s, 120 fps, max of 4 trials, as digitised by S21-D-D", "simulation assumption: alpha-pulse speed profile v=V(t/tp)exp(1-t/tp), 120 fps random phase, max of 4, zero tracking noise", "assumption: power demand = peak COM kinetic-energy rate 0.852 V^2/t_p, no added mass, drag or lateral motion (lower bound)", "assumption: axial muscle fraction of body mass 0.3-0.6 (no zebrafish source; unknown)", "law muscle-power-density (commit ee469aeb): traced ceiling 461 W/kg (frog plantaris, Marsh 2022 28C-adjusted), 390 W/kg quail cyclic", "law muscle-power-density: 1200 W/kg instantaneous record, unverified secondary", "absence of any fish white-muscle power value (scup white muscle unknown in law library)", "law takeoff-stall-speed (commit 0e202f2f): V_s = sqrt(2mg/(rho S C_L,max))", "replicate-24 (commit 922d3d1d): corrected stall speed 4.37 m/s at C_L,max 1.07", "C_L,max 1.07-1.15 dragonfly-wing proxy (Wakeling & Ellington 1997, search-summary)", "C_L,max 1.5-1.6 bat and Harris hawk (Pennycuick 1971; Tucker & Heine 1990, search-summary) as alternative band", "design premise: fish mass 0.4 g (primary source unknown)", "design premise: reference wing span 0.04 m, AR 5, S = 3.2e-4 m^2", "air density 1.2 kg/m^3", "assumption: in-water burst speed is an upper proxy for water-exit speed", "Danos & Lauder 2012 abstract: time to maximum COM velocity was measured at 1000 fps (value could-not-access)"]}
```
