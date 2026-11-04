# Replicate 196: S24, can surface taxiing close the zebrafish launch gap?

Claim (answer removed in the brief): *Surface taxiing cannot close the 1-BL (5.84 m/s) launch gap
and does not demonstrably close the 3-BL (1.95 m/s) gap.*

Date: 2026-11-04. Script: `docs/research/fish/replicate-196_calc.py`, run with
`python3 -I docs/research/fish/replicate-196_calc.py`. Every number in §3 that has no citation is a
**calculation** from that script, not an observation.

## 0. Independence disclosure (read this first)

This replication is **not fully blind**, and I am saying so up front.

- The inputs were not on this branch. The brief pointed to the harvest branch
  `claude/s24-surface-taxiing-launch-tsepbn`. To find what "1-BL" and "3-BL" meant, I grepped the
  headings of `S24-behaviour.md` on that branch. The grep output included the author's short
  answer, two table rows and the closing JSON. The JSON contains their key number: a tail-beat
  frequency, with a range, and the measured maxima they compared it against. **I stopped reading
  that file at that point.** I did not open `S24_calcs.py` or the S24-deepen branch.
- I also read the top of `challenge-183.md`, a review of S20 and a different claim, for context. It
  gave me the S20 exit speed, 0.84 m/s, and the Demesmay et al. 2025 adult escape speed, 1.57 m/s,
  which I did not read myself.
- So I knew the shape of the author's argument before computing: a Strouhal frequency ceiling,
  with the order of magnitude of their frequency. I chose my own inputs below (body length,
  amplitude, St range, frequency ceiling) from sources I fetched myself. Treat my agreement as
  **weaker than a blind replication.**

## 1. Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Target launch speed, 3-BL wing | 1.95 m/s | Given in the question. These are the brief's design values, not measurements | n/a (given) |
| Target launch speed, 1-BL wing | 5.84 m/s | Given in the question | n/a (given) |
| Adult zebrafish total length (TL) | 0.036 m (3.60 cm TL; 3.05 ± 0.04 cm BL) | Palstra et al. 2010, *PLoS ONE* 5:e14483 | full-text (via a fetch tool that returns quoted extracts) |
| Adult body mass | 0.43 ± 0.03 g | Palstra et al. 2010 | full-text (same caveat) |
| Adult Ucrit | 0.548 ± 0.007 m/s (18.0 BL/s) | Palstra et al. 2010 | full-text (same caveat) |
| Exit speed from S20 | 0.84 m/s | S20 Re-inversion, as reproduced in challenge-183 | listing (second-hand) |
| Thrust-efficient Strouhal band | 0.2 < St < 0.4 | Taylor, Nudds & Thomas 2003, *Nature* 425:707 | abstract |
| Peak-to-peak tail amplitude | 0.2 TL, varied over 0.15–0.25 TL | Conventional carangiform/subcarangiform value (Bainbridge 1958 lineage). From memory, not fetched this session | could-not-access (memory) |
| Adult/juvenile zebrafish tail-beat frequency range | ~1–21 Hz, mean ~6 Hz | Frontiers in Neural Circuits 2018 review (doi 10.3389/fncir.2018.00073), citing Kyriakatos et al. 2011 and Ampatzis et al. | search-summary |
| Adult zebrafish *escape* tail-beat frequency | **unknown** | Searched: "adult zebrafish tail beat frequency maximum escape Hz", "Demesmay 2025 … tail beat frequency", and a JEB-scoped adult C-start query. All hits were larval: 57 ± 8 Hz larval C-start (JEB 222:jeb203091), up to ~100 Hz in 3 dpf larvae (JEB 207:853). Those are not adult values | search-summary |

Scope of the negative search: three web searches (standard and extended), on 2026-11-04. I did not
search PubMed or Google Scholar directly. I did not read Kyriakatos 2011 or Ampatzis.

## 2. Method

Taxiing means the body is lifted by the wings while the caudal fin stays in the water and keeps
making thrust. For the tail to make net thrust while the fish moves at U, it has to beat in the
efficient-thrust Strouhal band (my modelling assumption, based on Taylor et al. 2003):

  f = St · U / A

Here A is the peak-to-peak tail amplitude. Compare f against what an adult zebrafish can produce.

I also checked the given targets. With lift = weight, V = √(2mg / (ρ C_L S)). If wing area scales
as span², then V ∝ 1/span. A 3× span should therefore give exactly one third of the speed.

## 3. Arithmetic (all calculation)

**Check on the targets.** 5.84 / 1.95 = **2.995**, which is 3 to rounding. So the targets are
consistent with geometrically similar wings, area ∝ span². With m = 0.43 g, ρ = 1.2 kg/m³ and
TL = 0.036 m:

- C_L·S = 2mg / (ρV²).
  - 3-BL: 2·0.43e-3·9.81 / (1.2·1.95²) = 18.49 cm².
  - 1-BL: 2.06 cm².
- The implied aspect ratio at C_L = 1 is b²/(C_L·S) = 6.3 for both wings.

I cannot pin the brief's actual m, TL, C_L and AR, so I can confirm the targets only as
internally consistent. I have not re-derived them from first principles.

**Required tail-beat frequency**, f = St·U/(A_frac·TL), with TL = 0.036 m:

| Target | A | St 0.2 | St 0.3 | St 0.4 |
|---|---|---|---|---|
| 1.95 m/s (3-BL) | 0.15 TL | 72 Hz | 108 Hz | 144 Hz |
| 1.95 m/s (3-BL) | 0.20 TL | **54 Hz** | **81 Hz** | 108 Hz |
| 1.95 m/s (3-BL) | 0.25 TL | 43 Hz | 65 Hz | 87 Hz |
| 5.84 m/s (1-BL) | 0.15 TL | 216 Hz | 324 Hz | 433 Hz |
| 5.84 m/s (1-BL) | 0.20 TL | 162 Hz | 243 Hz | 324 Hz |
| 5.84 m/s (1-BL) | 0.25 TL | 130 Hz | 195 Hz | 260 Hz |

Worked example, 3-BL central case: 0.3 × 1.95 / (0.2 × 0.036) = 0.585 / 0.0072 = 81.25 Hz.

**Inverse check.** At the review's upper frequency of 21 Hz with A = 0.2 TL, the speed is
U = f·A/St = 21 × 0.0072 / St:

- St 0.2: 0.76 m/s
- St 0.3: 0.50 m/s
- St 0.4: 0.38 m/s

These bracket the measured Ucrit, 0.548 m/s (Palstra 2010). That is a sanity check that the
Strouhal model with these inputs reproduces measured sustained swimming.

**Gaps (calc).**

| Exit speed | ΔV, 3-BL | KE ratio, 3-BL | ΔV, 1-BL | KE ratio, 1-BL |
|---|---|---|---|---|
| 0.84 m/s | 1.11 m/s | 5.4× | 5.00 m/s | 48× |
| Ucrit 0.548 m/s | 1.40 m/s | 12.7× | 5.29 m/s | 114× |

## 4. My value

**3-BL (1.95 m/s):** taxiing at the target needs **≈ 81 Hz tail-beat frequency** (St 0.3,
A 0.2 TL, TL 36 mm). The range is **43–144 Hz** over St 0.2–0.4 and A 0.15–0.25 TL. The lowest
corner, 43 Hz, is still about 2× the ~21 Hz upper range reported for adult and juvenile zebrafish
(search-summary).

I could not find a measured adult escape frequency, so I record it as `unknown`. If an adult can
briefly reach about 45–55 Hz, the generous corners of the 3-BL case would be reachable for a few
beats. That is why the 3-BL result is "not demonstrated" and not "refuted". This is my inference.

**1-BL (5.84 m/s):** needs **130–433 Hz**, central 243 Hz. That is at least 6× the sustained range
and above anything I found even for larvae (≤ ~100 Hz). On this model, taxiing cannot close the
1-BL gap. This is a calculation, conditional on the Strouhal thrust assumption.

Uncertainty: the dominant terms are A (±25 %) and St (×2 across the band). Body length enters
linearly. The author appears to have used a 40 mm TL; I used 36 mm, which makes my frequencies
about 11 % higher.

## 5. Comparison with the recorded value

The recorded key number, seen as disclosed in §0, is about 73 Hz to taxi at 1.95 m/s, with a range
of 29–98 Hz. They compare it against 21 Hz sustained and 52 Hz transient escape maxima.

- My central value is 81 Hz. The ~11 % difference is fully explained by TL: 36 mm from
  Palstra 2010 against their apparent 40 mm. Their 73 Hz equals 0.3 × 1.95 / (0.2 × 0.040).
- My low end, 43 Hz, is higher than their 29 Hz. They must have used a lower St (< 0.2) or a larger
  amplitude than I allowed. I cannot tell which without reading their script, and I did not read it.
- I could not verify their 52 Hz adult escape maximum.

On the claim as worded, both directions agree. 1-BL is impossible by a wide margin, and 3-BL is not
demonstrated because the required frequency exceeds the sustained adult range. On the headline
frequency I **agree within uncertainty**. That agreement is weakened by my prior exposure to their
key number.

## Sources

- Palstra AP et al. 2010. *Establishing zebrafish as a novel exercise model.* PLoS ONE
  5:e14483. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0014483 — full-text
  (fetch-tool extracts)
- Taylor GK, Nudds RL, Thomas ALR 2003. Nature 425:707–711.
  https://ideas.repec.org/a/nat/nature/v425y2003i6959d10.1038_nature02000.html — abstract
- Frontiers in Neural Circuits 2018 review.
  https://www.frontiersin.org/journals/neural-circuits/articles/10.3389/fncir.2018.00073/full —
  search-summary
- JEB 222:jeb203091 (larval C-start, 57 ± 8 Hz).
  https://journals.biologists.com/jeb/article/222/14/jeb203091/20809 — search-summary (larval; not
  used as an adult value)
- JEB 207:853 (larval ontogeny). https://journals.biologists.com/jeb/article/207/5/853/34509 —
  search-summary (larval; not used)
- challenge-183.md (repository, S20 review): source of 0.84 m/s — listing (second-hand)

```swarm-replication
{"claim_id": 196, "my_value": "~81 Hz tail-beat needed to taxi at 1.95 m/s (range 43-144 Hz; St 0.2-0.4, A 0.15-0.25 TL, TL 36 mm) vs ~21 Hz adult sustained; 1-BL needs 130-433 Hz", "agrees": true,
  "note": "Same verdict and the 3-BL frequency agrees within ~11% (explained by 36 vs 40 mm TL), but I saw the recorded key number before computing, so this is not a blind replication."}
```
