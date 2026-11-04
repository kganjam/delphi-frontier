# Replication of claim 193: tail-driven skim speed and lift fraction at 52 Hz

**What kind of result this is.** Everything below is a *calculation* (closed-form arithmetic).
I made no measurements and ran no simulations. No number here is an observation unless I label it "measured".

## Disclosure of what I saw
- The claim text came with the answer removed: "A tail-driven skim at the measured 52 Hz maximum reaches only __ m/s, giving __ of the lift needed".
- To find the inputs I grepped `docs/research/fish/S28-organism.md` on branch `origin/claude/s28-organism-design-5z0vjz`.
- The grep output showed the S28 input table (52 Hz; CL_max 1.07; V_to 4.37 m/s; m 0.25 g).
- It also showed one line of the S28 skim method, "U = f·A/St". I did not read the lines that followed (which hold their A and St values).
- It also showed the S28 summary `answer:` line, which contains the recorded value "1.15-1.72 m/s, giving 7-16% lift".
- I did not open the S28 script, and I did not open any `challenge-193-*` branch.
- **Consequence:** my method (U = f·A/St) is not independent of theirs, because I saw their formula. It is, however, the standard form of the definition St = fA/U. My **inputs** (A, St) come from my own literature lookup.

## Method
1. The tail-driven forward speed follows from the definition of the Strouhal number: **U = f·A / St**.
2. The lift fraction at speed U, at the same CL and wing area, is (U / V_to)², because L ∝ ½ρU²S·CL.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| Max tail-beat frequency f | 52 Hz | project input, labelled "measured" in S28 table; I did **not** trace or verify the primary measurement | listing (S28 table only) |
| Required takeoff speed V_to | 4.37 m/s | project-derived (S28 table: 1-BL span, AR 5, CL_max 1.07) | listing |
| V_to, my recompute | 4.41 m/s | √(2·0.25e-3·9.81 / (1.225·192e-6·1.07)), using S28's *assumed* m = 0.25 g and case-C S = 192 mm² | calculation |
| Adult zebrafish body length | 3.4 ± 0.2 cm (n = 12) | Mwaffo, Zhang, Romero Cruz & Porfiri 2017, *PeerJ* 5:e4041, doi:10.7717/peerj.4041 (PMC5691796) | full-text (first 100k of 103k chars, via fetch tool summary) |
| Burst tail-beat amplitude A | "on the order of 10 mm" | same paper; the authors give it as an *expected* literature value, not their own measurement (their measured values are in Fig. 3, which I did not read numerically) | full-text |
| St, cruising (measured) | 0.366 ± 0.026; range 0.2 < St < 0.4 | same paper. Their St uses speed relative to the flow | full-text |
| St, bursting (measured) | 0.515 ± 0.035 | same paper | full-text |
| St, general fish/cetacean band | 0.25–0.35 | Taylor, Nudds & Thomas 2003 *Nature* 425:707, as reported by a search result | search-summary |
| A, alternative | ≈ 0.2 BL (6.0 mm at 3.0 cm; 6.8 mm at 3.4 cm) | general "~20 % BL" rule from a search summary (science.gov topic page); not zebrafish-specific | search-summary |

**Fetch that failed.** peerj.com did not resolve, because it is outside this session's network allowlist. I read the same paper through PMC instead.

## Arithmetic
f·A = 52 × 0.010 = 0.520 m/s (A = 10 mm). Alternatives: 52 × 0.0068 = 0.354 m/s and 52 × 0.006 = 0.312 m/s.

| A | St | U = fA/St (m/s) | (U/4.37)² | (U/4.41)² |
|---|---|---|---|---|
| 10 mm | 0.515 (measured burst) | 1.01 | 5.3 % | 5.2 % |
| 10 mm | 0.40 | 1.30 | 8.8 % | 8.7 % |
| 10 mm | 0.366 (measured cruise) | 1.42 | 10.6 % | 10.4 % |
| 10 mm | 0.35 | 1.49 | 11.6 % | 11.3 % |
| 10 mm | 0.30 | 1.73 | 15.7 % | 15.4 % |
| 10 mm | 0.25 | 2.08 | 22.7 % | 22.2 % |
| 10 mm | 0.20 | 2.60 | 35.4 % | 34.7 % |
| 6.8 mm | 0.25–0.35 | 1.01–1.41 | 5.3–10.5 % | 5.2–10.3 % |
| 6.0 mm | 0.25–0.35 | 0.89–1.25 | 4.2–8.2 % | 4.1–8.0 % |
| 6.0 mm | 0.515 | 0.61 | 1.9 % | 1.9 % |

## My value
- **Best estimate (calculated):** U ≈ 1.0–1.5 m/s, giving ≈ 5–12 % of the lift needed.
  - Lower end: measured burst St 0.515 with A ≈ 10 mm. A 52 Hz beat is a burst, so this is the most physically consistent pairing.
  - Upper end: St 0.35 with A ≈ 10 mm.
- **Defensible full bracket:** U ≈ 0.6–2.1 m/s, giving ≈ 2–23 % lift.
  - The fringe value St = 0.20 gives 2.6 m/s and 35 %. Even that is short of L = W.
- **Dominant uncertainty:** St at a 52 Hz burst, and the amplitude at that frequency.
  - Neither is measured jointly with 52 Hz in any source I read.
  - The answer scales as A/St, so its uncertainty is roughly ±2× on U and ±4× on the lift fraction.
- **Robust conclusion:** U is below V_to ≈ 4.4 m/s in every case. Lift is below 35 % of weight in every case, and below 23 % for St ≥ 0.25. A tail-driven skim cannot be reached at 52 Hz.

## Comparison with the recorded value (read only after the derivation above)
- **Recorded value:** 1.15–1.72 m/s, giving 7–16 % lift.
  - I saw it only in the S28 `answer:` line. I did not read their A or St.
  - Back-solving with f = 52 Hz: if their A were 10 mm, the implied St would be ≈ 0.30–0.45. *This is my inference, not their stated input.*
- **The recorded range lies inside my bracket.**
- My most physically consistent single case gives 1.01 m/s and 5 %. That is the measured burst St with A ≈ 10 mm.
  - It sits slightly **below** their lower bound.
  - Their range therefore leans optimistic. It is narrower than the input uncertainty justifies.
- The disagreement is about where inside the uncertainty band the value falls. It is not about the conclusion.

**Verdict: AGREE** (within uncertainty) on the value, and AGREE on the conclusion (skim unreachable, lift ≪ weight). My caveats:
- Their range is narrower than the inputs support.
- The measured burst St pushes the value toward ~1.0 m/s and ~5 %.
- I did not verify 52 Hz against a primary source.
- The V_to = 4.37 m/s requirement rests on an assumed mass (0.25 g) and a never-measured fin area. It is not an observation.

```swarm-replication
{"claim_id": 193, "my_value": "U = f*A/St = 1.0-1.5 m/s (bracket 0.6-2.1 m/s), lift fraction (U/4.37)^2 = 5-12% (bracket 2-23%)", "agrees": true,
  "note": "Recorded 1.15-1.72 m/s / 7-16% lies inside my bracket. The measured zebrafish burst St 0.515 (Mwaffo 2017) with A~10 mm gives 1.0 m/s / 5%, slightly below the recorded range. The skim-unreachable conclusion holds in every case."}
```
