# Challenge 200 — adult zebrafish peak fast-start speed derived from Re (claim S21)

**Claim under review (author's, not mine):** mean peak fast-start speed of adult zebrafish ≈ 0.84 m/s
(~25 TL/s, "range 0.78–0.93 m/s"), back-calculated from a mean maximum Reynolds number of
27,800 ± 2,140 s.e.m. (Danos & Lauder 2012, TL 33 mm, 1000 fps), with ν = 1.0e-6 m²/s. Evidence level
recorded as *derived*.

## 1. Independent arithmetic (calculated, not observed)

U = Re·ν / L, with the author's stated inputs (L = 0.033 m, ν = 1.0e-6 m²/s):

| Re | U (m/s) | U (TL/s) |
|---|---|---|
| 25,660 (mean − 1 s.e.m.) | 0.778 | 23.6 |
| 27,800 (mean) | 0.842 | 25.5 |
| 29,940 (mean + 1 s.e.m.) | 0.907 | 27.5 |

- The central value 0.84 m/s and ~25 TL/s **reproduce**.
- The stated upper bound **0.93 m/s does not reproduce** from ±1 s.e.m.: it would need Re ≈ 30,700.
  The ±1 s.e.m. interval is 0.78–0.91 m/s. The claim does not say where 0.93 comes from, so that bound
  is unsupported as written. (Also, an s.e.m. band is an uncertainty on the mean, not a "range" of
  individual peak speeds. Calling it a range understates the spread between fish.)

## 2. Proxy check

The quantity that matters is the peak centre-of-mass speed during the escape. The claim inverts a
*Reynolds number*, so it gets back whatever velocity and length scale Danos & Lauder put into Re. I
could not confirm which those were (see §4). Possibilities: centre-of-mass speed or a midline point
speed, and total length or standard length. If Re was built on a point speed rather than the
centre of mass, the inverted U is not the fast-start speed. That is unresolved, not refuted.

Mean(max Re)·ν / mean(L) is also not the same as mean(max U) when fish lengths vary. The bias is
small for a narrow size range, but it means the number is not exactly "mean peak speed".

## 3. Hidden assumption relaxed: ν

An inversion is only correct if it uses the same ν the source authors used to compute Re.
ν = 1.0e-6 m²/s corresponds to water at about 20 °C. Zebrafish are usually held at 26–28 °C
(ν ≈ 0.83–0.87e-6; the 28 °C, 0.83 mPa·s figure is stated in PMC11930232, which I read). Danos &
Lauder describe their control medium as about 1 mPa·s (search summary). If they computed Re with a
lower, temperature-correct ν, the speed falls (my calculation, same L):

| ν (m²/s) | U at mean Re | ±1 s.e.m. |
|---|---|---|
| 1.0e-6 | 0.84 | 0.78–0.91 |
| 0.894e-6 (25 °C) | 0.75 | 0.70–0.81 |
| 0.836e-6 (28 °C) | 0.70 | 0.65–0.76 |

So the ν assumption alone moves the headline by up to about 17 %. If Re used standard length (shorter
than TL) and the same Re, U rises in proportion to TL/SL. The point estimate is therefore uncertain
by roughly −17 % / +20 %, which is more than the s.e.m. band the claim reports.

## 4. Evidence level and source access

- "derived" is the honest level. The claim says plainly that no direct velocity was read, and it shows
  the derivation. No defect there.
- My own access: Danos & Lauder 2012, J Exp Biol 215:1854–1862, doi:10.1242/jeb.068957. **Read level:
  search-summary only.** The Harvard reprint host (sites.harvard.edu) and zendy.io do not resolve in
  this session, and the journal URL I tried returned an unrelated paper. So I **could not independently
  confirm** the values 27,800 ± 2,140, 33 mm or 1000 fps (the search summary does confirm 1000 fps and
  viscosities of about 1, 10 and 20 mPa·s), the Re definition, or the water temperature. My verdict
  takes those inputs as the author reported them.
- Negative search, with its scope: in one web search and two page reads (PMC11930232, which is about
  larvae), I found no directly reported adult zebrafish peak escape speed in m/s. The value is `unknown`
  from what I read.

## 5. Regime / counter-example

- Taxon/regime: these are adult fish at Re ~10⁴, in the inertial regime, so the Re inversion is
  physically meaningful. Larval data (Re 10–900, PMC11930232) are a different regime and should not
  be mixed in.
- The comparison that matters downstream is against the 5.8 m/s refutation threshold. Even with every
  relaxation stacked in the unfavourable direction (ν = 1.0e-6, standard length about 20 % shorter,
  upper s.e.m.), U stays around 1.1 m/s, a factor of about 5 below 5.8 m/s. **The qualitative
  conclusion survives with a wide margin.** I could not check the "1.5× Ucrit" ratio: this claim does
  not give the Ucrit value, and that ratio inherits the ν/length uncertainty above.

## Verdict: WEAKENED

The central arithmetic holds, and the conclusion that the speed is far below 5.8 m/s is robust. But
(a) the stated upper bound 0.93 m/s does not follow from the stated s.e.m. (it should be 0.91), (b) an
s.e.m. band is presented as a "range", and (c) the 0.84 m/s point value depends on ν = 1.0e-6 and on
Re using TL with centre-of-mass speed. I could not verify those assumptions. Relaxing ν alone gives
0.70–0.84 m/s.

```swarm-challenge
{"claim_id": 200, "outcome": "weakened", "reason": "Central arithmetic (0.84 m/s, 25.5 TL/s) reproduces and the conclusion of ~7x below 5.8 m/s is robust, but the stated 0.93 m/s upper bound does not follow from ±1 s.e.m. (0.91), an s.e.m. band is called a range, and the point value rests on an unverified nu=1.0e-6 / TL / centre-of-mass Re definition that, relaxed to 26-28 C water, gives ~0.70-0.75 m/s.",
  "corrected_value": "0.84 m/s (±1 s.e.m. 0.78-0.91 m/s) if Re used nu=1.0e-6 m^2/s and TL; 0.70-0.84 m/s across nu 0.836-1.0e-6 m^2/s",
  "depends_on": ["Danos & Lauder 2012 mean max Re = 27,800 ± 2,140 s.e.m. (as reported by claim author; not independently read)", "adult TL = 0.033 m (as reported by claim author)", "Re definition in Danos & Lauder 2012 (velocity type, length scale, nu) — unverified", "kinematic viscosity of water 0.836e-6 (28 C) to 1.0e-6 (20 C) m^2/s", "refutation threshold 5.8 m/s (from upstream claim)"]}
```
