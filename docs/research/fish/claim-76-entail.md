# Claim 76: what it requires at the organism and ecology scales

**Source claim (behaviour scale, evidence: derived):**
> The launch margin should be read as ~4-7x rather than a single ~7x, because the measured
> population spans a factor of three and 120 fps likely underestimates the instantaneous peak.

**Adjacent scales checked:** organism, ecology.
**Date:** 2026-11-04.
**Subject animal:** adult zebrafish (*Danio rerio*). Every number used below is from adult zebrafish
unless I say otherwise in the same sentence. No flying-fish (exocoetid) number is used as evidence.

## 0. What the claim is made of (reconstructed from the repository, not from the claim text)

`docs/research/fish/` is empty on this branch. I rebuilt the claim's inputs from sibling branches.
These are repository documents, and I give the read-level of each.

| Input | Value | Where it comes from | Read-level |
|---|---|---|---|
| Threshold ("launch" speed) | 5.84 m/s: stall speed of a 1-BL-span (4 cm, AR 5) fin wing at C_L 0.6 on a 0.4 g fish. This is a **calculation**, not a measurement. | `zebrafish-glide-physics.md` §3 (branch `claude/zebrafish-glide-physics-j176og`) | full-text (repo) |
| Fastest individual | 1.38 m/s, from Miln et al. 2021 Fig. 1a (120 fps, best of 4 trials), as digitised by S21-D | `claim-75-entail.md` (branch `claude/claim-75-entail-h913pb`), `S21-D-D-deepen.md` | full-text (repo); I did not digitise it myself |
| Population span | ~0.45–1.38 m/s (n = 50), i.e. a factor of 1.38/0.45 = 3.07 | same | full-text (repo) |
| Typical adult | 0.842 m/s, Reynolds-inverted from Danos & Lauder 2012 (mean of per-sequence maximum Re 27,800 ± 2,140 s.e.m., TL 33 mm, 1000 fps) | S21, relayed by S21-D | I confirmed Re 27,800 ± 2,140, TL 33.0 ± 1.3 mm, 1000 fps and unsmoothed frame differencing myself in the publisher's HTML (full-text, first 100k of 121k characters). Water temperature is not reported there. |

**How I read the "~4-7x" (my inference):** 5.84 / 1.38 = 4.23 and 5.84 / 0.842 = 6.94, both calculated.
So the lower end is the *fastest individual* and the upper end is the *typical adult*.

**Two context facts the claim does not state. Both are recorded in the repository, and neither is my
finding:**

1. **The threshold has since been corrected inside the project.** S21-D-D
   (`claude/deepen-s21-d-sensitive-input-no42sx:docs/research/fish/S21-D-deepen.md`) replaces 5.84 m/s
   with 4.37 m/s (C_L,max 1.07 from replicate-24) and says, in its own words, "S21-D's ~4-7x margin is
   withdrawn".
   - At 4.37 m/s, the same two speeds give 4.37/1.38 = 3.17x and 4.37/0.842 = 5.19x (calculated).
   - S21-D-D-D (same branch, `S21-D-D-deepen.md`) gives ≈2.9–5.3x.
   - This is a behaviour-scale correction, so I do not re-litigate it here. The entailments below are
     written for the claim as stated (5.84 m/s). Wherever a bound depends on the threshold, I give it
     at both values.
2. **The claim's two reasons point in opposite directions from what its band needs.**
   - A population spanning a factor of 3.07 gives a margin spanning a factor of 3.07: from 4.23x to
     5.84/0.45 = 13.0x (calculated). It does not give 4–7x.
   - The band 4–7x spans only 1.75x. So the claim reads the margin from the fastest fish and the
     *typical* fish, not from the full population.
   - `replicate-76.md` already flagged this arithmetic. Constraint C2 turns it into a requirement on
     where the bulk of the population sits.

---

## Constraints

### C1 · organism · `timescale`: the speed peak must last longer than the camera's differencing window

**Requirement.** The lower end (~4x) is the 120 fps reading of the fastest fish, nudged down because
"120 fps likely underestimates the instantaneous peak". For that lower end to stay near 4 (not near
2–3), the under-read must be small. That holds only if the time the fish spends near its peak speed is
long compared with the window over which a 120 fps two-point difference averages.

- Quantity: (120 fps differencing window) / (time centre-of-mass speed stays ≥ 90 % of its peak).
- Bound: ≤ 1. This cut-off is **my choice**, not a literature value. At a ratio of ~1 the box-average
  under-read is of order 10–20 % for a peaked profile; that is my calculation for a Gaussian pulse, not
  a measurement. An under-read of 20 % would move the lower end from 4.23x to ~3.4x.
- The window: Miln et al. say speed is the "maximum speed calculated across two video frames". That
  is either one frame interval (8.3 ms, the reading S21-D-D used) or two intervals (16.7 ms, the
  reading claim-75-entail used). The wording does not settle which, and I keep both.

**Check. Both sides are adult zebrafish.**

- Danos & Lauder 2012, *Challenging zebrafish escape responses by increasing water viscosity*,
  J Exp Biol 215:1854, doi:10.1242/jeb.068957. Adults, TL 33.0 ± 1.3 mm, 1000 fps.
- From that paper's figures, as **digitised by S21-D-D-D** (repo; I could not re-digitise: `curl` of
  the PDF returned 403 this session):
  - time to maximum COM velocity **25.6 ± 1.8 ms (s.e.m.)**, Fig. 4B;
  - one sample trace (Fig. 2B) rises over 16.5 ms and then holds **≥ 90 % of peak for 19.4 ms**.
- Ratio: 8.3/19.4 = 0.43, or 16.7/19.4 = 0.86 (calculated). Both are ≤ 1.

**Status: `satisfied`.** It rests on a measured time course of the same species and life stage. The
caveats:

- The plateau width is from **one** sequence, by the authors' description "a sample". That trace
  peaks at 0.62 m/s, below the 0.86 m/s group mean.
- The digitisation is S21-D-D-D's, not mine.
- Danos & Lauder do not report water temperature. Miln filmed at 23 °C. Their stimuli also differ
  (dropped object vs tail touch).

**What this does to the claim (my inference, from a simulation that is not mine).** S21-D-D-D ran a
120 fps max-of-4 simulation on the measured shape. Its results are **simulated, not observed**:

- **Noise-free,** the reading is 0.964–0.977 of the true peak. That is an under-read of only
  2.3–3.6 %, which moves 4.23x to ~4.08–4.13x.
- **With tracking noise σ_x ≥ 0.25 mm,** the reading is 1.06–1.66 of the true peak. That is an
  *over*-read.
- Miln's σ_x is `unknown`.

So the timescale requirement is met, but meeting it leaves the claim's second reason ("likely
underestimates") nearly empty. The under-read is a few per cent at most, and it may have the opposite
sign. This does not refute the band. It removes the reason given for widening it downward.

### C2 · organism · `range`: the typical adult peak must sit near 0.83 m/s, and the fastest fish near 1.46 m/s

**Requirement.** For the upper end to be ~7x and the lower end ~4x against 5.84 m/s:

- the typical adult's peak fast-start speed must be ≈ 5.84/7 = **0.83 m/s**;
- the fastest individual's true peak must be ≈ 5.84/4 = **1.46 m/s**.

Bound: the central (mean or median) adult peak must lie in **[0.83, 1.46] m/s**. Against the corrected
4.37 m/s threshold, the same band of speeds gives 3.0–5.3x (calculated).

**Check. All values are adult zebrafish.**

- **Danos & Lauder 2012, mean of per-sequence maxima:**
  - 0.856 ± 0.065 m/s (s.e.m.) in normal water, Fig. 3I as digitised by S21-D-D-D;
  - 0.842 m/s by inverting Re 27,800 with ν = 1.0 × 10⁻⁶ m² s⁻¹ (I confirmed the Re and the TL in
    full text).
  - **A caveat I derived:** the Re inversion depends on water temperature, which the paper does not
    state. With ν ≈ 0.84 × 10⁻⁶ m² s⁻¹ (≈ 28 °C; a textbook value I remember and did not check),
    the same Re gives 27,800 × 0.84e-6 / 0.033 ≈ 0.71 m/s (calculated).
  - The digitised direct value (0.856) does not carry this ambiguity, and it agrees with the
    ν = 1.0e-6 inversion.
- **Miln et al. 2021, n = 50 (as digitised by S21-D):** range 0.45–1.38 m/s; next-fastest fish
  1.16 m/s. I did not find their mean or median in the text (full-text via WebFetch; the speeds are
  only in Fig. 1a). The Dryad deposit (doi:10.5061/dryad.v15dv41tr) is recorded in the repo as
  `could-not-access`, and I did not retry it.

**Status: `satisfied` for the central value (Danos & Lauder mean ≈ 0.84–0.86 m/s, at the bottom edge of
the band).** I am not averaging away a disagreement:

- Miln's slowest fish (0.45 m/s) gives a 13x margin. So for some of the measured population the margin
  is well outside 4–7x.
- The claim's "~4-7x" is a statement about fish at or above the Danos & Lauder mean, not about the
  whole population it cites.
- The share of Miln's fish below 0.83 m/s is `unknown` to me, because I have not seen the per-fish
  values.

### C3 · organism · `spatial`: the measured fish and the design fish must be the same size, within ~1.25x

**Requirement.** The threshold is computed for a 4 cm, 0.4 g fish with a 1-BL wing. Under isometry I
assume m ∝ L³ and S ∝ L². Then stall speed scales as √L, while burst speed in body lengths per second
gives U ∝ L. So the margin scales roughly as L^−½ (my derivation, not a literature result).

- Quantity: L_measured / L_design.
- Bound: within [0.8, 1.25]. A 25 % length mismatch moves the margin by ~12 % (√1.25 = 1.118,
  calculated), which is inside the "~" of the claim. The 1.25 cut-off is my choice.

**Check.**

- **Danos & Lauder (the ~7x end):** TL 33.0 ± 1.3 mm, which I confirmed in full text. 33/40 = 0.825.
  That is inside the bound.
  - Rescaling the threshold to a 33 mm fish gives 5.84 × √0.825 = 5.30 m/s and a margin of 5.30/0.856
    = 6.2x instead of 6.8–6.9x. This is calculated, under the isometry assumption.
  - TL vs the design's "BL": the design document does not say whether its 4 cm is total or standard
    length. `unknown`.
- **Miln et al. (the ~4x end):** the text says only that groups were size-matched "within 2 mm
  standard length". It gives no mean SL (full-text via WebFetch). The fish lengths are `unknown`.
- **The design mass, 0.4 g:** the primary source is `unknown`. S21-D-D-D flags this too.

**Status: `open`.** The ~7x end meets the bound. The ~4x end cannot be checked, because the Miln
lengths are not in the paper text and the data deposit was not reachable. This is "not accessed",
not "nobody measured".

### C4 · ecology · `range`: across the wild thermal range, peak speed must not rise by more than ~1.2x over its 23 °C value

**Requirement.** The ~4x end is measured at 23 °C (Miln). The margin describes the animal in its
habitat only if fast-start peak speed does not rise much at the temperatures wild zebrafish occupy.
Otherwise the habitat lower end falls below ~4.

- Quantity: peak fast-start speed at a wild operating temperature ÷ peak at 23 °C.
- Bound: ≤ 1.2. That keeps the lower end at or above 5.84/(1.38 × 1.2) = 3.5x (calculated; the 1.2
  is my tolerance for "~4").

**Check.**

- **Wild temperature range:** other papers cite Engeszer et al. 2007 (Zebrafish 4:21) for
  **12.3–38.6 °C**. I read only a search summary of the citing source, not Engeszer's table
  (read-level: search-summary). Claim-75-entail separately relays ~18–36 °C from a different
  secondary source, also at search-summary level. The two secondary figures disagree at both ends;
  I report both. Either way, 23 °C lies inside the range.
- **Thermal sensitivity of adult zebrafish fast-start peak speed:** not found.
  - What I searched (this session): three web searches combining zebrafish / *Danio rerio* with
    fast-start, C-start, escape, temperature, acclimation and Q10, one of them in extended mode.
  - What turned up instead:
    - Scott & Johnston 2012 (PNAS): Ucrit only, not fast-start (search-summary).
    - Ackerly & Ward 2016 (J Exp Zool A 325:25): *developmental* temperature, with startle tested
      at a common temperature. The abstract summary says more vertebrae gave higher C-start velocity,
      so it does not give a test-temperature effect. The publisher page returned 403
      (read-level: search-summary).
    - An SICB abstract on early-development temperature and adult startle: states a hypothesis,
      with no result retrieved (search-summary).
    - A 2026 bioRxiv preprint on *larval* muscle thermal acclimation (listing only).
  - Not covered: paywalled journals, theses, non-English literature.
- **Cross-species illustration only. This is NOT evidence for or against the zebrafish claim.**
  - In *Eleginops maclovinus*, a sub-Antarctic notothenioid tested at 2–10 °C, the Q10 of maximum
    length-specific velocity is 1.90 (search-summary).
  - If that Q10 applied to zebrafish, 23 → 28 °C would give 1.9^0.5 = 1.38x, which exceeds the bound
    (calculated). The species, the thermal regime and the temperature range all differ, so this is a
    reason to measure, not a refutation.

**Status: `unsatisfied`.** Within the search scope above, I found no zebrafish measurement that meets
or breaks the bound. This means "I looked and did not find it". It does not mean "it was measured and
found absent".

### C5 · ecology · `range`: lab-evoked maxima must not be beaten by more than ~1.2x in natural escapes

**Requirement.** Both measured ends come from lab stimuli: tail touch (Miln) and a dropped object
(Danos & Lauder). The margin describes the animal's ecological ceiling only if its fastest escapes in
the wild, against a real predator strike, are not much faster than these lab maxima.

- Quantity: maximal predator-evoked peak speed ÷ maximal lab-evoked peak speed.
- Bound: ≤ 1.2. This is my tolerance, chosen for the same reason as in C4.

**Check.**

- The only adult zebrafish predator-evoked figure in the repository is from McKee & McHenry 2020
  (Integr Org Biol, PMC7750966), as relayed by S21-D (full-text, keyword-scanned there; I did not
  re-read it). It reports a "mean escape speed ... (v = 3.7 cm s⁻¹, N = 63)" over an unspecified
  window.
- That is a mean, not a peak, so it cannot be compared with a peak. I do not treat its ~20x
  difference from the lab peaks as a contradiction.
- I ran no separate search for wild or predator-evoked adult zebrafish peak speeds.

**Status: `open`.** I did not check it against a comparable peak measurement.

---

## Summary

| # | Scale | Kind | Status | One line |
|---|---|---|---|---|
| C1 | organism | timescale | satisfied | The adult peak lasts ~19 ms (one trace) against an 8.3–16.7 ms window. Met, but the under-read is then only ~2–4 % (simulated) and may be an over-read. |
| C2 | organism | range | satisfied (central value) | Danos & Lauder mean 0.84–0.86 m/s sits at the bottom of [0.83, 1.46]. Miln's slow fish (0.45 m/s → 13x) fall outside the claimed band. |
| C3 | organism | spatial | open | 33/40 = 0.825 meets the bound at the ~7x end. Miln lengths are unknown. |
| C4 | ecology | range | unsatisfied | No adult zebrafish test-temperature data on fast-start speed was found within the stated scope. |
| C5 | ecology | range | open | No comparable predator-evoked peak exists in the repository, and I did not search further. |

**Nothing here is `unsatisfiable`.** No measured adult zebrafish number contradicts a constraint.

The strongest finding is C1, and it cuts against the claim's *reasoning*, not its band:

- The measured adult time course makes a large 120 fps under-read implausible.
- So "120 fps likely underestimates the instantaneous peak" contributes at most a few per cent.
- The width of the band therefore comes entirely from the fastest-vs-typical split. Read against the
  claim's own cited population, that split under-states the spread (4.2–13x, C2).

Separately, the project's own later work has replaced the 5.84 m/s threshold with 4.37 m/s and
withdrawn the 4–7x band (S21-D-D, S21-D-D-D). That is a behaviour-scale change, recorded here only
as context.

## Sources

| Source | What I used | Read-level |
|---|---|---|
| Danos & Lauder 2012, J Exp Biol 215:1854, doi:10.1242/jeb.068957 | TL 33.0 ± 1.3 mm, 1000 fps, max Re 27,800 ± 2,140, frame-differenced velocity, temperature not reported | full-text (publisher HTML via WebFetch, first 100k of 121k chars); figures could-not-access (PDF 403 via curl) |
| Same paper, Figs. 2B, 3I, 4B values | 25.6 ± 1.8 ms to max, 19.4 ms ≥ 90 % plateau, 0.856 ± 0.065 m/s | listing: relayed from S21-D-D-D's digitisation (repo, branch `claude/deepen-s21-d-sensitive-input-no42sx`) |
| Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146, PMC8025299 | 23 ± 0.5 °C, 120 fps GoPro, best of 4 trials, "across two video frames", size-matched within 2 mm SL, no numeric speeds in text | full-text (via WebFetch) |
| Miln Fig. 1a values (0.45–1.38 m/s; 1.16 m/s next-fastest) | population span | listing: relayed from S21-D / S21-D-D (repo) |
| Miln Dryad deposit doi:10.5061/dryad.v15dv41tr | per-fish speeds and lengths | could-not-access (recorded in the repo; not retried) |
| `zebrafish-glide-physics.md` (repo) | origin of 5.84 m/s | full-text (repo) |
| S21-D-D, S21-D-D-D (repo) | corrected 4.37 m/s threshold; simulated 120 fps bias b | full-text (repo) |
| `replicate-76.md`, `claim-75-entail.md` (repo) | prior checks | full-text (repo) |
| Engeszer et al. 2007, Zebrafish 4:21 (wild temperature, as cited by others) | 12.3–38.6 °C | search-summary |
| Ackerly & Ward 2016, J Exp Zool A 325:25 | developmental temperature, not test temperature | search-summary (publisher 403) |
| Scott & Johnston 2012, PNAS | Ucrit thermal acclimation, not fast-start | search-summary |
| *E. maclovinus* fast-start Q10 1.90 (other species) | cross-species illustration only | search-summary |
| McKee & McHenry 2020, Integr Org Biol, PMC7750966 | predator-evoked mean speed 3.7 cm/s | listing: relayed from S21-D (repo) |

```swarm-entail
{"source_claim": 76, "source_scale": "behaviour",
  "constraints": [
    {"target_scale": "organism", "kind": "timescale",
      "statement": "The time the fish holds near-peak centre-of-mass speed during a fast-start must be at least as long as the 120 fps two-point differencing window, so that the 120 fps reading under-reads the peak by a small amount and the lower end of the margin stays near 4x",
      "quantity": "120 fps differencing window / duration of speed >= 90% of peak", "lo": null, "hi": 1.0, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Adult zebrafish (Danos & Lauder 2012, TL 33 mm, 1000 fps): time to max COM velocity 25.6 +/- 1.8 ms s.e.m. (Fig 4B) and a sample trace holding >=90% of peak for 19.4 ms (Fig 2B), giving a ratio of 0.43 (8.3 ms window) or 0.86 (16.7 ms window). A simulation on that shape (S21-D-D-D, not mine) gives a noise-free 120 fps under-read of only 2.3-3.6%, and an over-read with tracking noise >= 0.25 mm",
      "satisfied_evidence": "measured",
      "note": "Same species and life stage on both sides (adult Danio rerio). Figure values were digitised by S21-D-D-D on branch claude/deepen-s21-d-sensitive-input-no42sx (relayed; I could not re-digitise because the PDF returned 403); methods confirmed by me in full-text HTML. Plateau width rests on one sample sequence. Temperature unreported in Danos & Lauder vs 23 C in Miln. Meeting this constraint makes the claim's 'underestimates' reason contribute at most a few per cent, possibly with the opposite sign."},
    {"target_scale": "organism", "kind": "range",
      "statement": "The central (typical) adult peak fast-start speed must lie near threshold/7 and the fastest individual near threshold/4, i.e. the bulk of the population must lie in the band that maps onto 4-7x",
      "quantity": "central adult peak fast-start speed", "lo": 0.83, "hi": 1.46, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "Danos & Lauder 2012 mean of per-sequence maxima 0.856 +/- 0.065 m/s (Fig 3I, digitised by S21-D-D-D) and 0.842 m/s from Re 27,800 with nu = 1.0e-6 (Re and TL confirmed by me in full text)",
      "satisfied_evidence": "measured",
      "note": "Adult zebrafish. The value sits at the bottom edge of the band. Disagreement preserved: the Re inversion gives ~0.71 m/s if the water was ~28 C (temperature unreported; my calculation). Miln et al. 2021's own population (0.45-1.38 m/s, digitised by S21-D) implies a 4.2-13x margin, so the 4-7x band describes only fish at or above the typical speed. Miln mean/median unknown (not in text; Dryad not accessed)."},
    {"target_scale": "organism", "kind": "spatial",
      "statement": "The body length of the fish whose speeds set the margin must match the body length assumed in the threshold calculation within a factor ~1.25, because under isometry the margin scales roughly as L^-0.5",
      "quantity": "L_measured / L_design (design L = 40 mm)", "lo": 0.8, "hi": 1.25, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "~7x end: Danos & Lauder TL 33.0 +/- 1.3 mm gives 0.825, inside the bound (rescaled margin ~6.2x, calculated). ~4x end: Miln et al. report only size-matching within 2 mm SL; absolute lengths are not in the text",
      "satisfied_evidence": "unknown",
      "note": "Miln full text read via WebFetch: no mean SL. Dryad doi:10.5061/dryad.v15dv41tr recorded as could-not-access in the repo and not retried. Design L (TL vs SL) and the 0.4 g mass have no stated primary source. This is 'not accessed', not 'not measured'."},
    {"target_scale": "ecology", "kind": "range",
      "statement": "Over the temperatures wild fish occupy, peak fast-start speed must not rise by more than ~1.2x above its 23 C value, or the in-habitat lower end of the margin falls well below ~4x",
      "quantity": "peak fast-start speed at wild operating temperature / peak at 23 C", "lo": null, "hi": 1.2, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "Searched and not found: no adult zebrafish measurement of fast-start peak speed versus test temperature. 23 C itself lies inside the wild range (12.3-38.6 C as cited from Engeszer et al. 2007; ~18-36 C from another secondary source, both search-summary)",
      "satisfied_evidence": "unknown",
      "note": "Scope: three web searches this session (zebrafish/Danio rerio x fast-start/C-start/escape x temperature/acclimation/Q10, one extended). Found only Scott & Johnston 2012 (Ucrit), Ackerly & Ward 2016 (developmental temperature, common test temperature; publisher 403), an SICB hypothesis abstract, and a larval bioRxiv preprint. Not covered: paywalled journals, theses, non-English literature. The Eleginops maclovinus Q10 of 1.90 (other species, 2-10 C) would give 1.38x for 23->28 C if it transferred; that is a cross-species illustration, not a refutation."},
    {"target_scale": "ecology", "kind": "range",
      "statement": "Maximal escapes evoked by natural predators must not exceed the lab-evoked maxima (tail touch, dropped object) by more than ~1.2x, or the margin does not describe the animal's ecological ceiling",
      "quantity": "predator-evoked peak speed / lab-evoked peak speed", "lo": null, "hi": 1.2, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Not checked against a comparable measurement. The only predator-evoked adult zebrafish value in the repository (McKee & McHenry 2020, mean escape speed 3.7 cm/s over an unspecified window, relayed by S21-D) is a mean, not a peak, so it is not comparable",
      "satisfied_evidence": "unknown",
      "note": "No separate search for wild or predator-evoked adult zebrafish peak speeds was run this session."}
  ]}
```
