# Challenge 200: adult zebrafish peak fast-start speed worked back from Re (Danos & Lauder 2012)

**Claim under review (S21, harvest:zebrafish-fast-start-velocity-pxsv7e):** mean peak fast-start speed ≈ 0.84 m/s
(~25 TL/s, "range 0.78–0.93 m/s"). It is worked back from a mean maximum Re of 27,800 ± 2,140 s.e.m., with L = 0.033 m
and ν = 1.0e-6 m²/s. The author says this is about 1.5× the Ucrit proxy and about 7× below the 5.8 m/s refutation threshold.
Recorded evidence level: derived.

**Verdict: WEAKENED.** The central number is arithmetically correct. The stated range is wrong, and the "range" is really an s.e.m. band.
Two unverified assumptions carry the conversion: which velocity defines Re, and what ν was used. Neither assumption can
change the qualitative conclusion (far below 5.8 m/s).

## Sources and read-levels
- Danos N., Lauder G.V. (2012) *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957.
  **My read-level: search-summary.** Here is what I tried. The Harvard reprint PDF (sites.harvard.edu) and zendy.io were both
  blocked by this session's network policy (DNS failure). The JEB URL I tried returned an unrelated "Outside JEB" page.
  A web search confirmed the design: viscosities of 1, 10 and 20 mPa·s, filmed at 1000 fps. It also confirmed the authors' stated rationale,
  "higher angular velocities are reached during stage 1 resulting in higher Reynolds numbers". I could **not**
  check the value 27,800 ± 2,140, the 33 mm TL, the Re formula, the velocity definition or the water temperature.
  These are the claim author's readings (they say full-text). I have not verified them.

## 1. Independent arithmetic (U = Re·ν/L)
Calculated by me, not observed:

| Re | ν (m²/s) | U (m/s) | TL/s |
|---|---|---|---|
| 27,800 | 1.0e-6 | 0.842 | 25.5 |
| 25,660 (−1 s.e.m.) | 1.0e-6 | 0.778 | 23.6 |
| 29,940 (+1 s.e.m.) | 1.0e-6 | **0.907** | 27.5 |

- Central value 0.84 m/s: **correct**.
- Upper bound 0.93 m/s: **not reproducible** from the stated inputs. The +1 s.e.m. value gives 0.91 m/s. Getting 0.93 m/s
  needs Re ≈ 30,690, which is neither +1 s.e.m. nor any other stated quantity. This is a defect, though a small one.
- Calling the band a "range" is wrong. ±1 s.e.m. describes how uncertain the mean is, not how spread out the individual fish are.
  The spread between fish is SD = s.e.m.·√n. n is `unknown` to me because I could not read the paper. With any n > 1 the spread
  between individuals is wider than 0.78–0.91 m/s.

## 2. Proxy: is "Re" carrying the speed that matters?
The conversion only recovers peak centre-of-mass (COM) speed if Danos & Lauder used
**U = peak COM translational speed and L = TL** in their Re. I could not confirm this (see read-level). The search summary
links their Re argument to the *angular* velocities of stage 1. That leaves open that their Re was built from a local or
rotational velocity, for example the tail tip or angular velocity × length, rather than COM speed.
- If Re used tail-tip or segment speed, then 0.84 m/s overstates COM peak speed. Tail tips move faster than the COM.
- If Re used standard length rather than TL, U would rise by about the ratio TL/SL.
Which way the error goes, and how large it is, is `unknown` until someone reads the Methods. This is my inference, not something the source says.

## 3. Hidden assumption: ν = 1.0e-6 m²/s
The inversion is only valid if it uses **the same ν the authors used**, not whatever the water physically was.
- Suppose the authors used nominal 1 mPa·s (their treatment label) with ρ ≈ 1000 kg/m³. Then ν = 1.0e-6 is the right inverse
  and 0.84 m/s stands.
- Suppose instead they used the viscosity of water at the holding temperature. Zebrafish are typically kept at about 26–28 °C. I did not
  confirm the experimental temperature. In that case ν ≈ 0.83–0.89e-6 m²/s and U ≈ **0.70–0.75 m/s** (calculated): 11–17 % lower.
I relaxed this assumption and the result moves 11–17 %. It does not flip.

## 4. Evidence-level honesty
The level "derived" is honest, and the claim says "I compute" in the sentence. That meets the floor. There is a minor inconsistency:
"value: n/a" is recorded while the KEY carries 0.84 m/s. The ratio "1.5× the Ucrit proxy" cannot be checked here
because the claim does not state the Ucrit value.

## 5. Counter-examples and regimes
I searched only one web query and did not find a directly reported adult zebrafish peak fast-start speed. That leaves the claim's
negative ("no directly reported value could be read") standing at the search-summary level. I am not quoting any literature speed from memory.
Larval zebrafish (5 dpf) work exists (PMC11930232, listing only). It is a different size and Re regime and cannot stand in for adults.

## Bottom line
- 0.84 m/s is correct arithmetic **given** ν = 1.0e-6, L = TL = 0.033 m and Re built on peak COM speed.
- The ±1 s.e.m. band should read 0.78–0.91 m/s (not 0.93), and it should be labelled as an s.e.m. band, not a range.
- If the authors used a temperature-specific ν, the plausible value falls to about 0.70 m/s.
- For any plausible combination (0.65–0.91 m/s), the speed is still about 6–9× below 5.8 m/s. The refutation-threshold conclusion survives.

```swarm-challenge
{"claim_id": 200, "outcome": "weakened", "reason": "Central 0.84 m/s reproduces from the stated inputs, but the stated upper bound (0.93) does not (+1 s.e.m. gives 0.91 m/s), the band is an s.e.m. not a range, and the conversion rests on unverified assumptions about which velocity and which viscosity Danos & Lauder used in Re (temperature-specific nu would give ~0.70 m/s); the far-below-5.8 m/s conclusion is unaffected.",
  "corrected_value": "0.84 m/s (±1 s.e.m. band 0.78-0.91 m/s) if nu=1.0e-6 m^2/s and Re uses peak COM speed and TL; ~0.70 m/s if nu at 28 C (0.83e-6 m^2/s)",
  "depends_on": ["Danos & Lauder 2012 mean max Re = 27,800 ± 2,140 s.e.m. (claim author's full-text reading; not verified by me, my read-level search-summary)", "L = 0.033 m TL (claim author's reading)", "Re in Danos & Lauder defined with peak centre-of-mass speed and TL (unverified)", "nu used by Danos & Lauder = 1.0e-6 m^2/s vs temperature-specific (unverified)", "5.8 m/s refutation threshold (as stated in claim)"]}
```
