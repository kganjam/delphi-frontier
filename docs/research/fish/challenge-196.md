# Challenge 196: surface taxiing and the launch-speed gap ([S24])

**Claim under review (author's text, not mine):** "[S24] Surface taxiing cannot close the 1-BL (5.84 m/s) launch gap and does not demonstrably close the 3-BL (1.95 m/s) gap: the binding limit is tail-beat frequency, not thrust force, because keeping a caudal lobe producing thrust at 1.95 m/s needs ~49-73 Hz (St 0.2-0.3, A 0.2 TL; calc) against measured adult zebrafish maxima of 21 Hz sustained and 52 Hz transient escape, and at sustained frequencies the calculated taxi ceiling (~0.56 m/s) is Ucrit itself. KEY: ~73 Hz tail-beat frequency needed to taxi at 1.95 m/s (range 29-98 Hz) vs 52 Hz measured adult escape maximum"

Recorded evidence level: derived. Source: `harvest:s24-surface-taxiing-launch-tsepbn`.

**Verdict: WEAKENED.** The 1-BL half survives with a wide margin. The 3-BL half does not hold up as worded. The KEY line compares the top of the author's own Strouhal band with the frequency maximum. At the bottom of that same band, the required frequency (49 Hz) is *below* the 52 Hz escape maximum.

## 0. What I could and could not check

- The harvest source `s24-surface-taxiing-launch-tsepbn` is not in this repository. I searched the working tree for "taxi" and checked both branches (`claude/challenge-surface-taxiing-claim-h5kk8h`, `work/frontier-foundation`). Read-level: **could-not-access**. I don't know how the author derived 5.84 m/s and 1.95 m/s, so I treat both as given inputs.
- The zebrafish maxima (21 Hz sustained, 52 Hz escape) are the author's inputs. One standard web search for adult zebrafish tail-beat maxima and Ucrit did not surface those values. It found Ravel et al. 2025, *iScience* ([PMC11930232](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11930232/)), on adult escape kinematics, read-level **search-summary**, and its Hz values were not visible in what I retrieved. So I neither confirm nor refute 21 Hz or 52 Hz. **unknown.**
- The flying-fish counter-example sources are listed in §5. A biorxiv fetch returned HTTP 429. `meetings-archive.aps.org` is outside this session's allowed network domains and has to be allowed in the session's network settings before it can be fetched.

## 1. Independent arithmetic (calc, mine)

Steady flapping kinematics give f = St·U/A, where A is the peak-to-peak tail excursion. With A = 0.2 TL, the author's 49–73 Hz is reproduced by TL = 0.040 m (A = 8.0 mm). The author did not state TL; I back-solved it, and 4 cm is a plausible adult zebrafish total length.

| U (m/s) | St 0.10 | St 0.15 | St 0.20 | St 0.25 | St 0.30 | St 0.40 |
|---|---|---|---|---|---|---|
| 1.95 (3-BL) | 24.4 Hz | 36.6 | **48.8** | 60.9 | **73.1** | 97.5 |
| 5.84 (1-BL) | 73.0 | 109.5 | 146.0 | 182.5 | 219.0 | 292.0 |

- 49–73 Hz: reproduced. 98 Hz: reproduced as St 0.4.
- 29 Hz: this low end needs A = 13.4 mm at St 0.2, i.e. A ≈ 0.34 TL for a 4 cm fish. That is a different amplitude assumption, and the author did not state it. The bounds of the range come from mixed assumptions.
- Inverting the relation, the Strouhal number a fish could reach at its frequency maxima (calc):
  - At 52 Hz and 1.95 m/s: **St = 0.213**, which is *inside* the author's 0.2–0.3 thrust band.
  - At 21 Hz and 1.95 m/s: St = 0.086.
  - At 52 Hz and 5.84 m/s: St = 0.071.
- Sustained taxi ceiling at 21 Hz (calc): 0.56 m/s at St 0.3, as stated, but **0.84 m/s at St 0.2**. "The ceiling is Ucrit itself" holds only for the St 0.3 choice.

## 2. Proxy check

Tail-beat frequency stands in for "the lobe can still produce net thrust at U". The quantity that actually decides this is the ratio of the lobe's lateral (or heave) velocity to U. That ratio is set by f·A, not by f alone. Frequency is a fair proxy only if A is held at 0.2 TL at the frequency maximum. In fish, amplitude usually falls as frequency rises toward the burst limit. Relaxing A would therefore make the author's argument *stronger*, not weaker. The proxy is defensible, but it hides the amplitude assumption.

A second check: the body wave must travel faster than the fish (slip ratio below 1). With wavelength λ ≈ 1 TL, wave speed V = f·λ needs f > 1.95/0.04 ≈ 49 Hz (calc). This is independent of Strouhal and agrees with the author's lower bound, not their KEY 73 Hz.

## 3. Hidden assumptions, relaxed

1. **The St band.** The KEY figure (73 Hz) uses St 0.3, the most demanding end of the band. At St 0.2, which the author also accepts, 49 Hz is needed against 52 Hz available. The frequency criterion alone therefore does not rule out 3-BL taxiing. Net thrust from flapping foils is also often reported to begin below St 0.2 (roughly 0.1–0.15, depending on pitch). That is my recollection of the foil literature and I did not re-verify it here. If it holds, 37 Hz would suffice at St 0.15.
2. **Transient vs sustained.** What actually saves the 3-BL conclusion is that 52 Hz is a C-start burst lasting a few half-beats. A taxi run needs repeated cycles over a run-up distance. That is a **duration and endurance** limit, not the "frequency vs thrust" dichotomy the claim states. The claim's hedge, "does not demonstrably close", is honest. The KEY line, which compares 73 Hz to 52 Hz, overstates the margin.
3. **"Not thrust force".** The source offers no thrust-vs-drag (surface/wave drag) calculation. Frequency and thrust are not independent, because thrust scales roughly with (f·A)². The statement that thrust is not binding is asserted, not shown.

## 4. Evidence level

"derived" is honest for the frequency numbers, and the claim labels them "calc". Calling 21 Hz and 52 Hz "measured" is acceptable only if the harvest source cites the measurements, and I could not access it (§0). "Ucrit itself" equates a calculated ceiling with a measured quantity. It should read "≈ reported Ucrit" and name the St value used.

## 5. Counter-examples and other regimes

- **Flying fish (Exocoetidae)**, read-level **search-summary**:
  - A bioRxiv hydrodynamic model (Deng et al., [10.1101/765560](https://www.biorxiv.org/content/10.1101/765560.full.pdf)) describes 50–70 Hz tail beating with the lower lobe submerged. It uses 50 Hz for a 10 m/s taxi.
  - A 2024 APS meeting abstract ([link](https://meetings-archive.aps.org/mar/2024/s27/13)) reports surface slapping at ~13.5 Hz.
  - These two sources disagree, and I could not resolve it. Speed, size and species are unknown for the 13.5 Hz figure, so I cannot compute its St.
  - In my inference, 50–70 Hz at 10 m/s in a larger fish is consistent with Strouhal-band scaling, which supports the author's method. The 13.5 Hz report, *if* it were at taxi speed, would mean a low-St slapping regime (support plus thrust from impact). The author's model leaves that regime out. Unverified.
- Scope of the negative search: two standard web searches (zebrafish maxima; flying-fish taxi frequency) and one failed fetch each of the biorxiv paper (HTTP 429) and the APS abstract (domain not allowed). I did no exhaustive literature search.

## 6. Net

- **1-BL (5.84 m/s): SURVIVES.** It needs at least 73 Hz even at St 0.1, and 146 Hz at St 0.2, against a 52 Hz burst maximum (calc).
- **3-BL (1.95 m/s): WEAKENED.**
  - Corrected framing: the requirement is 49–73 Hz for St 0.2–0.3, with A 0.2 TL and TL ≈ 4 cm (calc).
  - The 52 Hz escape maximum falls inside that band, at St ≈ 0.21.
  - The gap stays open only because 52 Hz cannot be sustained, at an unquantified cost. Frequency alone does not keep it open.
  - The KEY line ("73 Hz vs 52 Hz") should cite the band, not its top.
  - The "taxi ceiling = Ucrit" line holds only at St 0.3; at St 0.2 the ceiling is 0.84 m/s.

```swarm-challenge
{"claim_id": 196, "outcome": "weakened", "reason": "Recomputed f = St·U/A shows the 3-BL requirement at the claim's own St 0.2 bound (49 Hz) sits below the 52 Hz escape maximum (St≈0.21 at 52 Hz), so the 73-vs-52 Hz KEY cherry-picks St 0.3 and the 3-BL gap rests on burst non-sustainability, not frequency; the 1-BL conclusion survives (>=73 Hz even at St 0.1).", "corrected_value": "49-73 Hz needed at 1.95 m/s (St 0.2-0.3, A = 0.2 TL, TL ~0.040 m back-solved; calc); 52 Hz escape max corresponds to St ~0.21; sustained 21 Hz ceiling 0.56-0.84 m/s (St 0.3-0.2; calc)", "depends_on": ["U_3BL = 1.95 m/s and U_1BL = 5.84 m/s (author input, derivation not accessible)", "A = 0.2 TL with TL ~0.040 m (back-solved from author's 49-73 Hz)", "thrust Strouhal band 0.2-0.3 (author input)", "adult zebrafish tail-beat maxima 21 Hz sustained / 52 Hz escape (author input, not independently verified)", "f = St*U/A steady-flapping kinematic relation"]}
```
