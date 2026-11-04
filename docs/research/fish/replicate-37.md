# Replicate 37: is the zebrafish taxi ceiling at sustainable tail-beat frequency equal to Ucrit?

**Claim, with the answer removed:** "At sustainable tail-beat frequencies the calculated taxi ceiling
is ~[X] m/s, which is Ucrit itself, so taxiing adds essentially nothing to the launch."
Inputs were said to live in `S24-behaviour.md`.

## Method and what I read, in order

1. `S24-behaviour.md` is **not on this branch or on `main`**. Code search for `filename:S24-behaviour.md`
   and for `taxi Ucrit` in `kganjam/delphi-frontier` returned 0 hits. I found it on branch
   `claude/s24-surface-taxiing-launch-tsepbn` through the branch listing. **I did not open it until
   after I had my own value** (see Comparison).
2. I built the estimate from primary literature. Several hosts were blocked by this session's
   network policy (pubmed.ncbi.nlm.nih.gov, researchgate.net, par.nsf.gov), so most reads below are
   abstract or search-summary level.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Ucrit, wild-type, 28 °C | 0.560 ± 0.048 m/s = 15.5 SL/s (N = 21) | Plaut 2000, *J. Exp. Biol.* 203:813–820 | abstract (journals.biologists.com) |
| Ucrit | 0.548 ± 0.007 m/s = 18.0 SL/s | Palstra et al. 2010, *PLoS ONE* 5:e14483 | search-summary |
| Implied SL (Plaut) | 0.560 / 15.5 = 36.1 mm | calc | n/a |
| Implied SL (Palstra) | 0.548 / 18.0 = 30.4 mm | calc | n/a |
| Speed–frequency relation (model A) | U = L(0.75 f − 1), for f > 5 Hz | Bainbridge 1958, cited in arXiv 2507.11665 | search-summary (Bainbridge not read) |
| Stride length, general fish | 0.6–0.8 L per beat | Wardle 1975, *Nature* 255:725, citing Bainbridge | search-summary |
| Speed–frequency relation (model B) | TBF ≈ 3.09 + 1.71·U (U in BL/s; fit over 0.8–3.2 BL/s; R² = 0.82; fish ≈ 3.5 cm) | Han et al. 2024, *J. Fish Biol.*, doi:10.1111/jfb.15922 | search-summary. **I could not confirm the units of U** |
| "Sustainable" maximum tail-beat frequency, adult zebrafish | **unknown** to me before comparison. I bracketed **20–25 Hz** as an assumption | assumption (no zebrafish source found; searches: adult *Danio rerio* tail-beat frequency vs swim-tunnel speed, 3 queries, standard and extended) | n/a |

**Disagreement preserved:** Plaut and Palstra report nearly the same Ucrit in m/s but different
values in SL/s, so the body lengths they imply differ by about 19% (36.1 vs 30.4 mm). I carry both.

## Arithmetic (all calculated, none observed)

**Model A (Bainbridge), U = L(0.75 f − 1):**

| L | f = 20 Hz | 21 Hz | 22 Hz | 25 Hz |
|---|---|---|---|---|
| 30.4 mm | 0.0304 × 14.00 = 0.426 m/s | 0.0304 × 14.75 = 0.448 | 0.0304 × 15.50 = 0.471 | 0.0304 × 17.75 = 0.540 |
| 36.1 mm | 0.0361 × 14.00 = 0.505 m/s | 0.0361 × 14.75 = 0.532 | 0.0361 × 15.50 = 0.560 | 0.0361 × 17.75 = 0.641 |

Working backwards, model A needs f = (15.5 + 1)/0.75 = **22.0 Hz** to reach Plaut's Ucrit and
(18.0 + 1)/0.75 = **25.3 Hz** to reach Palstra's.

**Model B (Han 2024 fit), U = (f − 3.09)/1.71 BL/s, with L = 35 mm:**
f = 20 Hz gives 9.89 BL/s = 0.346 m/s. f = 21 Hz gives 10.47 BL/s = 0.367 m/s. f = 25 Hz gives
12.81 BL/s = 0.448 m/s. This extrapolates the fit 3–4× beyond the speeds it was measured over, so I
weight it less than model A.

**Extra check (my inference, not in the claim):** at the surface, wave-making drag rises steeply near
Froude number about 0.4, at U ≈ 0.4·√(gL) = 0.4·√(9.81 × 0.033) ≈ **0.23 m/s**. A partly emerged,
surface-taxiing 3 cm fish therefore probably can't hold even its submerged kinematic speed. That
would push the real taxi ceiling *below* Ucrit, not above it. I did not model this quantitatively.

## My value

**Taxi ceiling at sustainable tail-beat frequency ≈ 0.5 m/s, range 0.37–0.64 m/s (calculated).**
Model A alone gives 0.43–0.64 m/s. Model B gives 0.35–0.45 m/s. Every case is **at or below Ucrit
(0.548–0.560 m/s)**. Model A reaches Ucrit only by assuming f ≥ 22–25 Hz is sustainable.

One structural point, which is my inference: a ceiling set by "the sustainable frequency" is close to
Ucrit *by construction*. Ucrit is the top of prolonged swimming, so the frequency held at Ucrit is the
sustainable frequency. Any kinematic model calibrated to steady swimming will return roughly Ucrit.
"Taxiing adds nothing" is therefore nearly tautological for a fully submerged kinematic model. It is
a real constraint only because no measured adult value says sustained frequencies can go higher.

## Comparison with the recorded value (read only after the above)

I then opened `docs/research/fish/S24-behaviour.md` on `claude/s24-surface-taxiing-launch-tsepbn`.
I read only the lines that match the inputs and the result (grep on the frequency, Ucrit and ceiling
terms), not its full working. It records:

- a **taxi ceiling of 0.56 m/s at 21 Hz**, described as "Ucrit itself (0.56 vs 0.548 m/s)";
- 21 Hz as the measured adult steady-swimming maximum ("never exceeding 21 Hz (n = 8)", Kyriakatos
  et al. 2011, *J. Neurosci.*, recorded there as full-text; I did not read it myself);
- a Strouhal model, U = fA/St, with A ≈ 0.2 TL and TL = 33 mm, rather than a stride-length model.

S24 also lists Wakamatsu et al. 2019 Ucrit values of 0.19–0.28 m/s, which I had not found. If those
are the right Ucrit, the "≈ Ucrit" comparison changes, though the speed in m/s does not.

**Verdict: AGREE.** The two derivations use independent routes: Bainbridge stride-length scaling for
me, a Strouhal amplitude model for S24. At f = 21 Hz my model A gives 0.45–0.53 m/s and model B
gives 0.37 m/s, against S24's 0.56 m/s. I agree with the qualitative conclusion (ceiling ≤ Ucrit,
taxiing adds nothing). I agree with the number to within about 20%, with my central value somewhat
lower. One caveat: S24's Strouhal calibration also anchors fA at Ucrit (its line "At Ucrit 0.548 m/s
and St 0.3, fA = 0.164 m/s"). That shares the near-tautology I describe above, so the match on "≈
Ucrit" is weaker evidence than the match on order of magnitude.

```swarm-replication
{"claim_id": 37, "my_value": "~0.5 m/s (range 0.37-0.64 m/s, calculated; 0.45-0.53 m/s at 21 Hz)", "agrees": true,
  "note": "Independent Bainbridge stride-length estimate puts the sustainable-frequency taxi ceiling at or below Ucrit (0.55-0.56 m/s), agreeing with S24's 0.56 m/s within ~20%, though both models are near-tautologically anchored to steady swimming."}
```
