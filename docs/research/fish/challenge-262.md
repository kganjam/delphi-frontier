# Challenge 262: adversarial review of S28-D (the S28 fin-length sensitivity claim)

**Claim under review.** S28-D, harvest `claude/deepen-s28-daane-heterozygote-b7kpn8` (commit 511ecf7b): `docs/research/fish/S28-deepen.md` and `S28-deepen_calc.py`. I read both in full with `git show`. Read-level: full-text (repository).

**Evidence level recorded for the claim:** measured.

**My arithmetic.** `docs/research/fish/challenge-262_calc.py`. I wrote it from the stated inputs and did not reuse the author's code:
- it uses an RK4 integrator on (vx, vy, x, y);
- it finds the apex by linear interpolation at vy = 0;
- the author's script uses explicit Euler.

Every number below that has no source beside it is a **calculation** from that script. None is an observation. Date: 2026-11-04.

**Verdict: WEAKENED.**
- The organism-level negative survives.
- The claim's evidence level is mislabelled.
- Its "at most 2.4 % / likely 1–3 %" bound is not a bound. It holds only under two unsourced assumptions that the author did not relax: aspect ratio (AR) 5 at a given fin length, and a 45° launch.

---

## 1. Independent arithmetic

These are calculations. Inputs are as the claim states them:
- 45° launch; AR 5 at span = 2·L_fin + body width (rule C);
- SL 3.0 cm, m 0.25 g;
- CL 1.07, CD0 0.08, e 0.8;
- body drag CD 0.3 on 24 mm², scaled with SL².

| Check | Author | Mine (RK4) |
|---|---|---|
| S at 0.45 SL/fin | 192 mm² | 192.2 mm² |
| Reduction in ascent deceleration, 0.15 SL / 1.38 m/s | 0.9 % | 0.89 % |
| Same, 0.45 SL / 1.57 m/s | 6.2 % | 6.21 % |
| Same, 0.25 SL / 1.57 m/s | 2.4 % | 2.43 % |
| 5 % threshold, SL 3.0 cm; 1.38 / 1.57 m/s | 0.46 / 0.39 SL | 0.457 / 0.394 SL |
| 5 % threshold, SL 3.6 cm / 0.43 g; 1.38 / 1.57 m/s | 0.51 / 0.44 SL | 0.507 / 0.437 SL |
| 2 % threshold, all four cases | 0.22–0.29 SL | 0.220–0.290 SL |
| V_to and flight deficit at 0.45 SL, vs 2.11 m/s | 4.41 m/s, ×2.09 | 4.41 m/s, ×2.09 |
| Same at the 0.79 SL ceiling, vs 2.11 m/s | ×1.26 | ×1.26 |
| Rule A (chord fixed) best case, 0.45 SL / 2.11 m/s | 3.5 % | 3.53 % |

**Result.** The arithmetic reproduces to within 0.01 percentage points. I found no error in it.

**One scope note.** The "0.9–6.2 %" range is for the 3.0 cm / 0.25 g body only. For the isometric 3.6 cm / 0.43 g body:
- the low end falls to 0.75 % (0.15 SL at 1.38 m/s);
- the high end falls to 5.24 % (0.45 SL at 1.57 m/s).

This is a minor omission and does not change the direction of anything.

## 2. Is a proxy standing in for the quantity that matters?

There are two proxies. Both are disclosed by the author, but they affect how the claim reads.

**Exit speed.** The claim uses in-water escape peaks as the speed at which the fish leaves the water:
- Miln 1.38 m/s, read-level listing via the repository;
- Demesmay 1.57 ± 0.27 m/s, read-level listing via the repository.

No surface-exit speed for adult zebrafish exists in the record. The author's case that fin length, not exit speed, is the weak input rests on exit speed being "within ×1.14 of a conspecific measurement". That measurement is of the proxy, not of exit speed.

By the author's own ×2 table, exit speed is the **more** sensitive input:

| Input | ×0.5 | ×2 |
|---|---|---|
| Exit speed | 1.27 % | 16.3 % |
| Fin length | 1.61 % | 14.8 % |

So "most sensitive … to pectoral fin length" mixes up sensitivity with uncertainty. My inference: fin length is the most *uncertain* high-leverage input, which is a defensible statement. It is not the most *sensitive* one.

**Percentage reduction in deceleration.** This metric is itself a proxy for detectability. At shallow launch angles the percentage rises while the absolute apex rise shrinks (§3b). The metric and the detectable quantity can therefore move in opposite directions.

## 3. Hidden assumptions, tested relaxed

The claim's sub-bound is "at most 2.4 % if Fig. 4B shows 0.25 SL or less". That sentence states no geometry or angle. Two assumptions sit under it, and the author's sensitivity table never relaxed either of them in the direction that raises the effect.

### (a) AR 5 at a given length

S28-D calls rule C "generous". It is generous only compared with rule A (chord fixed at 0.1 SL).

At a fixed fin length, a **lower** aspect ratio means a broader fin, so the area is larger. AR 5 at total span corresponds to a mean fin width of about 0.5 × fin length. Nothing in the record measures the chord or the spread planform of the zebrafish pectoral:
- S28-D's own access table found no fin area or span;
- my web search for zebrafish pectoral-fin area or aspect ratio found nothing zebrafish-specific (scope below).

I relaxed AR at 0.25 SL per fin, 45° launch. CL is corrected for the finite-AR lift slope at the same angle of attack, using CL ∝ 1/(1 + 2/AR), so I do not just inflate the area. All values are calculations:

| AR | 1.38 m/s | 1.57 m/s |
|---|---|---|
| 5 (claim) | 1.89 % | 2.43 % |
| 3.5 | 2.35 % | 3.01 % |
| 2.5 | 2.79 % | 3.57 % |

### (b) 45° launch

The author tested only 60° and 80°, both of which shrink the effect. At ×0.5 (22.5°), more of the lift points upward. All values are calculations:
- at baseline (0.45 SL, 1.38 m/s), the reduction rises from 4.88 % to 8.14 %;
- at 0.25 SL, AR 5, 22.5°: 3.09 % at 1.38 m/s and 3.99 % at 1.57 m/s;
- at 22.5°, the 5 % threshold falls from 0.39–0.46 SL to **0.29–0.34 SL** (3.0 cm body).

The zebrafish leap angle is `unknown`. The author's own depends_on says "zebrafish leap angle unknown". Values at 22.5° are therefore as well supported as values at 45°.

At 22.5°, the absolute apex rise is smaller: 0.45–0.77 mm, against 0.97–1.63 mm at 45°. So the larger percentage does not make the effect easier to see.

### (c) Both relaxed together

At AR 2.5 (CL-corrected), 30° launch and 0.25 SL, the reduction is **4.13 % at 1.38 m/s and 5.31 % at 1.57 m/s** (calculation).

**What this means (my inference).**
- The "≤ 2.4 %" and "likely 1–3 %" figures are conditional on AR 5 and 45°. Neither is sourced, and neither is conservative.
- With both relaxed within unexcluded ranges, a fin of ≤ 0.25 SL gives up to about 3.6–4.0 % with one relaxed and up to about 5.3 % with both.
- The claim's KEY does label its *thresholds* "45 deg, AR-5 rule". The ≤ 2.4 % sentence and the "likely 1–3 %" headline do not carry that condition.
- **Corrected value:** for a fin ≤ 0.25 SL per fin, a reduction ≤ 2.4 % at 45° and AR 5; up to about 3.6 % (AR 2.5) or about 4.0 % (22.5°) with one assumption relaxed; up to about 5.3 % with both relaxed (30°, AR 2.5). All are calculated.

I do **not** claim that the zebrafish fin is AR 2.5 or that it leaps at 22.5°. Both are `unknown`. The point is that the claim's bound assumes values that nobody has measured.

## 4. Is the evidence level honest?

**No.** The ledger records this claim as "measured". The source document says:
- "No number is an observation. I made no new measurement."
- its swarm-result has evidence "derived (calculation …)".
- the key input is `unknown`.

Every quantitative value in the claim is a calculation, and its most sensitive input is unmeasured. The correct label is **derived/calculated**.

This mislabelling is a defect in the record, not in the author's text. The author's text is honest about it.

## 5. Regime or counter-example that would flip the negative

**The negative survives.** No single ×2 change flips it. I independently checked the inputs the author did not vary:

| Input | ×0.5 → ×2 | Reduction (baseline 4.88 %) |
|---|---|---|
| CD0 | 0.04 → 0.16 | 5.00 % → 4.64 % |
| Oswald e | 0.4 → 1.0 | 4.60 % → 4.93 % |
| Body drag CD | ×0.5 → ×2 | 4.86–4.88 % |

None of these touches V_to.

Flight (lift equal to weight) appears only with a **two-input stack**:
- fin length at the Davenport 0.79 SL ceiling (search-summary via challenge 189), together with an exit speed of 2 × 1.38 = 2.76 m/s;
- this gives V_to 2.66 m/s, a deficit of ×0.96;
- 2.76 m/s is 4.4 SD above the Demesmay mean, a proxy at listing read-level.

The claim's scope is single-input ×2 changes, so this stack does not breach it. I also found no published report of zebrafish gliding or of a counter-example taxon that would rescue the leap. My search for that was limited to the record and the one web search below, so this is a limited negative, not an exhaustive one.

## 6. Fig. 4B access (the decisive datum)

| Target | Result | Read-level |
|---|---|---|
| `pmc.ncbi.nlm.nih.gov/articles/PMC9172250/` | HTTP 200, 21 kB shell page. It gives the figure URL `cdn.ncbi.nlm.nih.gov/pmc/blobs/b3db/9172250/187bcb7df244/nihms-1735542-f0004.jpg` | listing |
| That image URL | Proxy CONNECT 403 | could-not-access |
| Europe PMC fulltextRepo for the f0004 image | HTTP 500 | could-not-access |
| `zfin.org/ZDB-FIG-221222-34` | No connection | could-not-access |
| Web search, "zebrafish pectoral fin aspect ratio OR "pectoral fin area" adult morphometrics standard length" (standard) | Nothing zebrafish-specific. Only formulas, e.g. AR = PtL²/PtA (scielo.br ecomorphology abstract), and other species | search-summary |

**Pectoral fin length/SL in the double heterozygote: `unknown`.** I agree with the author on this.

Spread pectoral-fin chord / aspect ratio in zebrafish: `unknown`.

## 7. Verdict

| Part of the claim | Outcome |
|---|---|
| Negative (no flight, glide, skim or meaningful leap extension) under single-input ×2 changes | **Survives**. Independently reproduced. |
| Arithmetic of the grid and thresholds | **Survives**, to ±0.01 pp |
| 0.45 SL is unsourced; fin length is `unknown` | **Survives**. Fig. 4B is still inaccessible. |
| "Most sensitive to fin length" | **Weakened in wording**. Exit speed is as sensitive or more; fin length is the most *uncertain* input. |
| "At most 2.4 % if ≤ 0.25 SL"; "likely 1–3 %" | **Weakened**. Conditional on AR 5 and 45°, both unsourced and not conservative. Relaxed, it is up to about 3.6–5.3 %. |
| Evidence level "measured" | **Defect**. It is calculated/derived. |

## Sources

| Source | Read-level |
|---|---|
| S28-deepen.md, S28-deepen_calc.py @ 511ecf7b | full-text (repository) |
| Daane JM et al. 2021, *Curr Biol* 31:5052, PMC9172250 (article page shell only; Fig. 4B image could not be reached) | listing; Fig. 4B could-not-access |
| Miln et al. 2021; Demesmay et al. 2025; Davenport 1992/1994 (as relayed in S28-D) | listing / search-summary, via the repository |
| scielo.br ecomorphology table (fin AR and area definitions, not zebrafish) — https://scielo.br/j/ni/a/psBgPk3YmMtytc6pYCpxVRJ/abstract/?lang=pt | search-summary |

```swarm-challenge
{"claim_id": 262, "outcome": "weakened", "reason": "The negative and all arithmetic reproduce independently, but the claim is recorded as 'measured' when every value is calculated, and its 'at most 2.4% if fin <=0.25 SL / likely 1-3%' bound holds only at an unsourced AR 5 and 45 deg launch; relaxing either within unexcluded ranges (AR 2.5 with CL corrected for lift slope, or a 22.5 deg launch) gives up to ~3.6-4.0%, and up to ~5.3% with both relaxed (calculated).",
  "corrected_value": "fin <=0.25 SL per fin: ascent-deceleration reduction <=2.4% at 45 deg/AR 5, up to ~3.6% (AR 2.5) or ~4.0% (22.5 deg), up to ~5.3% (30 deg, AR 2.5); 5% threshold 0.29-0.34 SL at 22.5 deg (all calculated); evidence level = derived, not measured",
  "depends_on": ["S28-D claim and script @ 511ecf7b (S28-deepen.md, S28-deepen_calc.py)", "S28 inputs: SL 3.0 cm, m 0.25 g, CL 1.07, CD0 0.08, e 0.8, body drag CD 0.3 on 24 mm2 (assumptions)", "isometric 3.6 cm / 0.43 g body (inference from Plaut 2000 abstract)", "exit speed proxied by in-water escape peaks: Miln 1.38 m/s, Demesmay 1.57 +/- 0.27 m/s (listing)", "pectoral fin length/SL in double het = unknown (Daane 2021 Fig. 4B could-not-access)", "spread pectoral fin aspect ratio = unknown (no zebrafish source found; tested 2.5-5)", "zebrafish leap angle = unknown (tested 22.5-90 deg)", "finite-AR lift-slope correction CL ~ 1/(1+2/AR) (textbook approximation, my assumption)", "Davenport 0.79 SL ceiling (search-summary via challenge 189)", "law: point-mass quasi-steady lift/drag trajectory, RK4"]}
```
