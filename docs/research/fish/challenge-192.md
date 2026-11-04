# Challenge 192: "3× leap needs 2.39 m/s (1.73×); flight needs 4.37 m/s (3.2× speed, 10× KE)"

**Claim under review (S28, branch `origin/claude/s28-organism-design-5z0vjz`, file
`docs/research/fish/S28-organism.md`, §0, §3.2, §3.6, §5 row 1).**

> A 3x leap would require a 2.39 m/s exit, 1.73x the measured maximum. Flight requires 4.37 m/s:
> 3.2x the speed and 10x the kinetic energy.

Recorded evidence level: `derived`. Value: 3.2 (speed ratio).

**Verdict: WEAKENED.**
- The arithmetic reproduces exactly.
- The flight conclusion (no fish reaches 4.37 m/s) survives every input I tried.
- What does not hold is the denominator, "the measured maximum" of 1.38 m/s. It is
  one fish's *swimming* fast-start in one study (Miln et al. 2021). A second full-text adult
  *D. rerio* study reports a control **mean** of 1.57 ± 0.27 m/s. That is above 1.38.
- So the 1.73× and 3.2× are ratios against one dataset. They are not ratios against "the
  measured maximum". Against the other dataset they are 1.52× and 2.78× (mean), or 1.13× and
  2.07× (mean + 2 s.d.).
- The source document flags that burst speed stands in for exit speed. The claim sentence drops
  that flag.

Every number below without a cited source is a **calculation** from
`docs/research/fish/challenge-192_calc.py`. None of them is an observation.

---

## 1. Independent arithmetic (my script, not the author's)

| Quantity | Claim | Mine |
|---|---|---|
| Exit for 3× range, vacuum: 1.38·√3 | 2.39 m/s | 2.3902 m/s |
| Ratio to 1.38 | 1.73× | 1.7321× |
| Exit for 3× range, body drag included (re-integrated) | — | 2.397 m/s |
| Flight speed ratio 4.37/1.38 | 3.2× | 3.167× |
| KE ratio (4.37/1.38)² | 10× | 10.03× |

**Reproduces.** The range ratio is a pure V² law. It does not depend on mass, fin or Reynolds
number, so √3 = 1.73 holds for 3× *any* ballistic leap. Body drag moves it by less than 0.3 %.

## 2. Proxy check: is 1.38 m/s the quantity that matters?

No. Two substitutions are made, and only one is disclosed in the claim sentence.

**(a) Swimming burst stands in for water-exit speed.**
- S28 §3.1 and §4 say this openly and call it "generous", meaning they assume exit ≤ burst.
- That direction is **not established**. Challenge 140 (branch
  `origin/claude/challenge-danio-exit-speed-35kkas`) relays guppy jump/C-start ratios of about
  1.5–1.8 (Soares & Bierman 2013, relayed, not read by me). Those ratios put exit speed *above*
  C-start burst in a related small cyprinodontiform.
- The sign of the burst → exit correction is therefore `unknown`. It is not known to be ≤ 1.
- **No zebrafish water-exit speed is measured** anywhere I looked. Scope of that search:
  this repository's branches (`git grep` for "exit", "Miln", "1.38 m/s"), plus challenge
  documents 75 and 140. I ran no new literature search.

**(b) One study's single fastest fish stands in for "the measured maximum".**
- Miln, Ward & Seebacher 2021: per-fish maxima 0.45–1.38 m/s at 120 fps, n = 50. The 1.38 is
  one fish. (Read-level: listing; relayed by challenge 75, which digitised Fig. 1a.)
- Demesmay et al. 2025, *PLoS Biol* 23(11):e3003484, PMC12604801. **Read-level: full-text.** I
  fetched the Europe PMC XML this session. The verbatim author statement is: "the calculated
  maximal speed (157 ± 27 cm/s for controls and 161 ± 33 cm/s for mutants)". Escape responses
  were recorded at "240 frames/s".
  - This is a *mean*. Individual fish in it must run above 1.57, and so above 1.38.
  - Caveat, my inference: the peak arrives in "8 ± 4 ms", about two frames at 240 fps. Peak speed
    from frame-differenced manual tracking is biased upward by position noise. The 1.57 may
    therefore overstate the true peak. That is a reason to hold the two studies in tension. It
    is not a reason to discard either.
- **The two measurements disagree. I do not average them.**

Ratios recomputed against each branch (calculation):

| Denominator | 3× leap (2.39) ratio | Flight (4.37) speed ratio | KE ratio |
|---|---|---|---|
| Miln fastest fish 1.38 (the claim) | 1.73× | 3.17× | 10.0× |
| Demesmay control mean 1.57 | 1.52× | 2.78× | 7.7× |
| Demesmay mean + 1 s.d. 1.84 | 1.30× | 2.38× | 5.6× |
| Demesmay mean + 2 s.d. 2.11 | 1.13× | 2.07× | 4.3× |

**Consequence (my inference).** "Flight is out of reach" survives every row: the smallest
shortfall is still about 2× in speed and 4× in energy. But "3.2×" is not "the" deficit. It is the
deficit against one study. On the Demesmay branch, a 3× leap stops looking clearly out of reach,
because 2.39 m/s sits at about mean + 3 s.d. That would still need exit ≈ burst, which is unmeasured.

## 3. Hidden assumptions, tested relaxed

**(a) "The wing contributes nothing" to the 3× leap (S28 §3.2).**
- At 2.39 m/s the case-C wing lifts (2.39/4.37)² = 30 % of W at exit, not ~0.
- I re-integrated with S = 192 mm² and AR 5. The exit speed needed for 3× the wild-type range
  (calculation):

| Wing setting | Exit needed | Ratio to 1.38 |
|---|---|---|
| None (body drag only) | 2.397 m/s | 1.74× |
| CD0 0.20, CL 1.07 | 2.348 m/s | 1.70× |
| CD0 0.08, CL 1.07 | 2.318 m/s | 1.68× |
| Drag-free wing, CL 1.07 (upper bound) | 2.276 m/s | 1.65× |

- So the wing does contribute, by up to about 5 % in exit speed. The claim's 2.39 m/s is right
  for wild type and slightly high for the designed fish. This does not change the conclusion, and
  I do not count it as a material fault.

**(b) 4.37 m/s is the most generous V_to in S28's own table.** Relaxing it makes the claim
*stronger*, not weaker:

| V_to case (S28 §2.2) | Speed ratio vs 1.38 | KE ratio |
|---|---|---|
| C, AR 5, 0.25 g (claim) | 3.17× | 10.0× |
| B, isometric fin | 3.96× | 15.7× |
| A, length-only fin | 5.87× | 34.4× |
| C at 0.40 g | 4.01× | 16.0× |

- The mass of 0.25 g is **back-solved** so that 4.37 m/s comes out self-consistent. It is not
  measured.
- The claim reads "flight requires 4.37 m/s". It should read "at least 4.37 m/s". 3.2× is a
  floor on the speed deficit, not a point value.

**(c) "Flight requires a 4.37 m/s *exit*."**
- This holds only for a pure ballistic launch. A taxiing launch (tail in the water) can reach
  V_to after exit.
- S28 handles taxiing separately (§5 row 2: 132–199 Hz needed vs 52 Hz measured), so the joint
  verdict holds.
- As a stand-alone sentence, though, "flight requires a 4.37 m/s exit" overstates. Flight
  requires 4.37 m/s *airspeed*. Exit at that speed is one route.
- I did not quantify ground effect on CL_max over the water surface. Its size here is `unknown`.

## 4. Evidence level

- `derived` is honest for the ratios.
- The claim sentence calls 1.38 "the measured maximum". S28 §1 labels it more carefully:
  "measured" swimming burst, "not water-exit speed". The claim drops that qualifier.
  - A derived exit-speed deficit is being reported against a measured *burst*, presented as a
    measured *exit*. This is a labelling defect.
  - The number itself is right.

## 5. Counter-examples and regimes

- **Demesmay et al. 2025**, as above: an adult *D. rerio* mean above the claimed maximum.
- **Guppy jump/C-start ratio**, as above (relayed): exit can exceed burst in a small teleost.
- **Flying fishes (Exocoetidae)**: they reach takeoff speed by taxiing, not at exit. This is the
  regime that §3(c) addresses. I give no speeds for them, because I did not read a source this
  session.

## Sources

| Source | Read-level |
|---|---|
| S28-organism.md and S28_organism.py (`origin/claude/s28-organism-design-5z0vjz`) | full-text |
| Demesmay et al. 2025, *PLoS Biol*, PMC12604801 (Europe PMC fullTextXML, fetched this session) | full-text |
| Miln, Ward & Seebacher 2021, *R Soc Open Sci* 8:210146, via challenge-75.md | listing (repository relay) |
| Soares & Bierman 2013 guppy ratios, via challenge-140.md | listing (repository relay) |

```swarm-challenge
{"claim_id": 192, "outcome": "weakened", "reason": "The arithmetic reproduces (1.732x, 3.167x, 10.0x) and flight stays out of reach on every input, but '1.38 m/s measured maximum' is one fish's swimming burst in Miln 2021 standing in for an unmeasured exit speed, and a full-text adult D. rerio study (Demesmay 2025) reports a control MEAN of 1.57 +/- 0.27 m/s, which gives 2.78x speed / 7.7x KE (2.07x / 4.3x at mean+2sd), so 3.2x is the deficit against one dataset, not the measured maximum.", "corrected_value": "flight speed deficit 2.07-3.17x (KE 4.3-10x) across the two disagreeing burst datasets, and >=3.2x up to 5.9x across S28's own V_to cases; 3x-leap exit 2.28-2.40 m/s (1.65-1.74x of 1.38)", "depends_on": ["Miln et al. 2021 burst maxima 0.45-1.38 m/s (listing, via challenge-75)", "Demesmay et al. 2025 PMC12604801 escape max speed 157 +/- 27 cm/s at 240 fps (full-text)", "V_to = 4.37 m/s (derived, S28 case C, back-solved m = 0.25 g)", "S28 case-C wing S = 192 mm2, AR 5, CL 1.07 (extrapolated)", "exit speed ~ burst speed (unmeasured proxy)", "guppy jump/C-start ratio (listing, via challenge-140)"]}
```
