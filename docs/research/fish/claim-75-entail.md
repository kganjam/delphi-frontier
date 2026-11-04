# Claim 75: what it requires at the organism and ecology scales

**Source claim (behaviour scale, evidence: measured).** S21-D VERDICT STRENGTHENS: directly
measured adult zebrafish fast-start maxima span 0.45–1.38 m/s (Miln et al. 2021, n=50, 120 fps,
full text, values digitised from Fig 1a). That range brackets the Reynolds-derived 0.842 m/s, and the
fastest individual is still about 4.2× below the 5.84 m/s threshold.

**Adjacent scales checked:** organism, ecology.

**Date:** 2026-11-04.

## Before the constraints: what I could and could not verify

- **Miln, Ward & Seebacher 2021**, *R. Soc. Open Sci.* (PMC8025299). Read level: **full-text**,
  through an automated page summary (WebFetch). From the text I confirmed n = 50 (10 groups of
  5), 120 frames s⁻¹, **23 °C (± 0.5 °C)**, and the method: best of four escapes per fish, with the
  centre of mass placed at 0.35 BL from the snout. **The text gives no fast-start speeds; they
  appear only in Fig 1.** I did not digitise the figure, so I have **not** independently checked
  the 0.45–1.38 m/s span. The text also gives **no standard length**. It says only that fish in a
  group were "within 2 mm standard length of each other". U10 sprint values are also given only in
  figures.
- **The 5.84 m/s threshold.** I searched this repository (`findings/`, `seeds/`, `results/`,
  `ledger/`, `specs/`) for `5.84`, `0.842`, `Reynolds`, `fast-start` and `Miln`, and found nothing.
  So I do not know what process the threshold gates. I have therefore **not** written ecology
  constraints about whatever needs 5.84 m/s. Doing so would mean guessing what the threshold is.
- **Arithmetic.** 5.84 / 1.38 = 4.23. This is calculated and agrees with the claim's "~4.2×".
- **Hosts I could not reach.** `pubmed.ncbi.nlm.nih.gov`, `scholarlypublications.universiteitleiden.nl`
  and `webarchiv.lib.cas.cz` do not resolve from this session (network policy). Because of that,
  Plaut 2000 and Spence et al. 2006 are known to me only at search-summary level or not at all.

## Constraints

### C1 (organism, `range`): the escape maximum must be at least the fish's prolonged-swimming maximum

**Requirement.** If 0.45–1.38 m/s are true per-individual *maximal* burst speeds, then each fish's
fast-start peak should be no lower than its prolonged-swimming (aerobic-to-anaerobic) maximum,
Ucrit, at the same temperature. A burst that is slower than the fish's sustained maximum would
mean the "maximum" was not maximal.

- Bound: the lower end of the fast-start range ≥ Ucrit. Comparator Ucrit ≈ 0.560 m/s.
- Evidence found: wild-type zebrafish Ucrit = **0.560 ± 0.048 m/s (15.5 SL s⁻¹) at 28 °C**,
  attributed to Plaut 2000 (*J. Exp. Biol.*) by Palstra et al. 2010. Read level:
  **search-summary**. It is a secondary citation, Plaut's full text was not reached, and the "±" was
  garbled in the snippet. The same snippet reports Palstra's own fish at about 0.549 m/s
  (18.0 SL s⁻¹). Plaut's abstract (search-summary) calls wild-type zebrafish "one of the
  fastest-swimming fishes ever measured" on a size-scaled basis.
- **Status: open, with a recorded tension.** The slowest fast-start maximum in the claim,
  0.45 m/s, is **below** the mean Ucrit of 0.560 m/s. The two numbers come from different fish,
  different labs and different temperatures (23 °C versus 28 °C), so I am not treating this as a
  contradiction.

  The following is my inference, not a measurement: an assumed Q10 of 1.5–2 over 5 °C would lower
  a 28 °C Ucrit by roughly 20–30%, to about 0.40–0.46 m/s, which overlaps 0.45 m/s.

  The decisive comparison is Miln's own per-fish U10 against per-fish fast-start, measured on the
  same fish at the same temperature. Those values exist, but only in the paper's figures, which I
  did not extract.

### C2 (organism, `range`): the implied length-specific speed must be within what fish muscle delivers

**Requirement.** The absolute speeds, divided by body length, must give relative speeds no higher
than the fastest teleost fast-starts that have been measured.

- Calculated: Miln gives no SL, so I took the mean SL from a different zebrafish cohort in the
  same lab, **3.28 ± 0.02 (s.e.) cm** (Bamford & Seebacher 2024, *Biol. Open*, PMC11340812, read
  level **full-text** via page summary). On that SL, 0.45–1.38 m/s is **13.7–42.1 SL s⁻¹**. This
  is derived and depends on an SL borrowed from another cohort. Adult zebrafish can reach 4–5 cm
  (Parichy 2015, *eLife*, full-text), and at 4.5 cm the range would be about 10–31 SL s⁻¹.
- Comparator: a search result describes archerfish predictive C-starts as "among the fastest
  C-starts known so far among teleost fish, with peak linear speed beyond 20 body lengths per
  second". Read level: **search-summary**. The search engine linked it to an archerfish
  hunting-start paper, and I have not verified the authorship. The same search summarised the
  Domenici & Blake 1997 review (*J. Exp. Biol.* 200:1165) as saying that relative speed in SL s⁻¹
  falls with body size. Read level: search-summary, with no numbers obtained.
- **Status: open, with a recorded tension.** The upper end, about 42 SL s⁻¹ on a 3.28 cm SL, is
  about twice the ">20 SL s⁻¹" quoted as among the fastest teleost C-starts. Zebrafish are smaller
  than archerfish, and the size trend favours smaller fish, so this is not a contradiction. It
  does mean the 1.38 m/s top value is unusually high per body length. Either that fish was long,
  or the value should be re-checked against the figure.

  Scope of the negative: I searched once for adult-zebrafish C-start peak velocity in SL s⁻¹ or
  m/s and found no adult zebrafish values. One search returning nothing does not show that nobody
  has measured them.

### C3 (organism, `timescale`): the sampling interval must be short relative to the C-start stages

**Requirement.** A camera that samples too slowly smooths a brief velocity peak and records it as
lower than it was. For a peak to be resolved, the frame interval should be much shorter than the
duration of stage 1 and stage 2. I am assuming a factor of at least 5. That factor is my choice,
not a literature value.

- Measurement: 120 fps (Miln 2021, full-text), so a frame interval of **8.33 ms**.
- Calculated: at 1.38 m/s, a fish moves 11.5 mm per frame, which is about 0.35 SL on a 3.28 cm SL.
- Comparator, measured but in **larvae**: in 5 dpf zebrafish at 28 °C, the C-bend lasts
  0–11 ms, the counter-bend 11–21 ms, and fast swimming 21–54 ms (PMC11930232, Fig 2 legend, read
  level **full-text** via page summary). At 120 fps, larval stage 1 would get about 1.3 frames.
- Adult zebrafish stage durations: **unknown**. I did not find them, from one search; see C2 for
  its scope. Adults are larger, so their stage durations are probably longer than the larval ones.
  That is my inference, and I have no number for it.
- **Status: open.** For larvae this constraint would fail by a wide margin, but larvae are not the
  claim's subject.

  My inference, not a quantified result: if the constraint also fails for adults, the measured
  maxima are *under*-estimates. The true peaks would then sit *closer* to 5.84 m/s than the claim
  says, which works against the "STRENGTHENS" verdict. I have not calculated how large the
  underestimation would be. So I cannot say whether it is small next to the 4.2× margin.

### C4 (ecology, `range`): habitat flow speeds must sit below the fish's swimming capacity

**Requirement.** Fish whose escape maxima are 0.45–1.38 m/s, and whose prolonged speeds are lower
still, cannot hold station in habitats where the current exceeds those speeds. So the flows at
which wild zebrafish are found must be below the lowest individual capacity.

- Bound: habitat flow ≤ 0.45 m/s.
- Measured: at Indian zebrafish field sites, mean flow rates were **0 (still, vegetated),
  0 (still, non-vegetated), 6 ± 0.8 cm/s (flowing, vegetated), and 16 ± 8.1 cm/s (flowing, mixed)**,
  reported as mean (SE). Source: Shelton et al. 2020, "Collective Behavior in Wild Zebrafish",
  *Zebrafish* 17(4):243–252, doi:10.1089/zeb.2019.1851, Table 1, read level **full-text** via page
  summary. Their flow method is cited to Suriyampola et al. 2016, which I did not read. Parichy
  2015 (*eLife*, full-text) describes the typical habitat as "shallow, slow moving streams" and
  still monsoon pools, with no numbers.
- **Status: satisfied.** The highest site mean, 0.16 m/s, is about 2.8× below the slowest escape
  maximum (0.45 m/s), and it is also below the Ucrit in C1.

  The scope is four sites in a single study. I could not reach Spence et al. 2006 (Bangladesh) or
  Engeszer et al. 2007 (NE India), and do not know whether they report flow numbers.

### C5 (ecology, `range`): the 4.2× margin must survive the temperatures zebrafish live at

**Requirement.** Miln measured at 23 °C, and wild zebrafish have been recorded at **12–39 °C**
(Parichy 2015, *eLife*, full-text). For "the fastest individual is ~4.2× below 5.84 m/s" to hold
across the species' ecological range, warming must not raise fast-start speed by 4.23× or more.

- Bound: v(39 °C) / v(23 °C) < 4.23. Derived: over 16 °C, that is equivalent to an effective
  Q10 < **2.46** for fast-start peak speed. For illustration, calculated: Q10 = 2 gives 3.0×, which
  passes, and Q10 = 3 gives 5.8×, which fails.
- Evidence found: I found **no** Q10 for zebrafish fast-start speed. Scope: one search on
  zebrafish escape speed with temperature, Q10 and Seebacher. What I did find, all at
  search-summary level and none of it the quantity bounded here:
  - zebrafish developmental rate Q10 = 2.33 for 22–32 °C;
  - a coral-reef damselfish study that found no temperature effect on maximum escape speed (a
    different taxon);
  - golden grey mullet, where maximum fast-start velocity rises with temperature up to a
    threshold (attributed to Beddow et al. 1995);
  - a 2026 larval zebrafish preprint saying developmental temperature partly compensates the
    effect of environmental temperature on muscle mechanics.

  Also, 39 °C is a temperature at which the fish has been *found*. It is not a temperature at
  which performance has been measured.
- **Status: open.** No measured zebrafish value either meets or contradicts the bound. The one
  related zebrafish Q10 I found (2.33, for development) is below 2.46. It measures a different
  process, though, so I am not counting it.

## Summary

| # | scale | kind | status |
|---|---|---|---|
| C1 | organism | range: fast-start max ≥ Ucrit | open (tension: 0.45 < 0.560 m/s, cross-study, 23 vs 28 °C) |
| C2 | organism | range: SL-specific speed plausible | open (tension: ~42 SL/s vs ">20 SL/s among fastest") |
| C3 | organism | timescale: frame interval ≪ stage duration | open (fails for larvae; adult durations unknown) |
| C4 | ecology | range: habitat flow < capacity | **satisfied** (≤ 0.16 m/s measured) |
| C5 | ecology | range: thermal gain < 4.23× | open (no zebrafish fast-start Q10 found) |

None of the constraints is `unsatisfiable`. No measured number I found contradicts the claim.

What I found does not strengthen the claim beyond C4. The claim's "STRENGTHENS" verdict rests on
figure-digitised values that I could not see. Two of its numbers sit in tension with neighbouring
measurements: the lower end (C1) and the upper end in body lengths per second (C2). The sampling
rate is also coarse relative to the known larval C-start timescale (C3).

**Most useful next check:** extract Miln Fig 1 (fast-start and U10 per fish) together with
per-fish SL. That one step would settle C1 and C2 on the same fish at the same temperature.

## Sources

- Miln, Ward & Seebacher 2021, *R. Soc. Open Sci.*: https://pmc.ncbi.nlm.nih.gov/articles/PMC8025299 (full-text, via summary; figures not read)
- Bamford & Seebacher 2024, *Biol. Open*: https://pmc.ncbi.nlm.nih.gov/articles/PMC11340812/ (full-text, via summary)
- Larval zebrafish escape modelling, viscosity: https://pmc.ncbi.nlm.nih.gov/articles/PMC11930232/ (full-text, first 100k chars, via summary)
- Parichy 2015, *eLife* 4:e05635: https://elifesciences.org/articles/05635 (full-text, via summary)
- Shelton et al. 2020, *Zebrafish* 17:243: https://pmc.ncbi.nlm.nih.gov/articles/PMC7869874/ (full-text, via summary)
- Plaut 2000, *J. Exp. Biol.* (PMID 10648223), and Palstra et al. 2010: search-summary only
- Domenici & Blake 1997, *J. Exp. Biol.* 200:1165: search-summary only
- Archerfish C-start ">20 BL/s" statement: search-summary only (https://typeset.io/pdf/the-predictive-start-of-hunting-archer-fish-a-flexible-and-j9vuaer6vd.pdf, not opened)
- Temperature/Q10 items in C5: search-summary only
- Spence et al. 2006; Engeszer et al. 2007: could-not-access

```swarm-entail
{"source_claim": 75, "source_scale": "behaviour",
  "constraints": [
    {"target_scale": "organism", "kind": "range",
      "statement": "Each individual's measured fast-start maximum must be no lower than its prolonged-swimming maximum (Ucrit) at the same temperature, or the 'maximum' was not maximal",
      "quantity": "lower end of fast-start maxima relative to Ucrit", "lo": 0.56, "hi": null, "units": "m/s",
      "status": "open",
      "satisfied_by": "Cross-study comparator only: Ucrit 0.560 +/- 0.048 m/s (15.5 SL/s) at 28 C, attributed to Plaut 2000 via Palstra et al. 2010. Slowest claimed fast-start max 0.45 m/s is below it, but at 23 C in different fish; same-fish U10 from Miln exists only in figures, not extracted",
      "satisfied_evidence": "literature",
      "note": "Plaut 2000 J Exp Biol (PMID 10648223) via Palstra 2010: search-summary. Miln 2021 PMC8025299: full-text, figures not read. Temperature-correction overlap (Q10 1.5-2 assumed) is my inference, not measured"},
    {"target_scale": "organism", "kind": "range",
      "statement": "Speed divided by body length must lie within the relative fast-start speeds teleost muscle is known to deliver",
      "quantity": "length-specific fast-start speed", "lo": 13.7, "hi": 42.1, "units": "SL/s",
      "status": "open",
      "satisfied_by": "Derived 13.7-42.1 SL/s using SL 3.28 cm from a different cohort (Bamford & Seebacher 2024); Miln reports no SL. Upper end ~2x the '>20 BL/s, among the fastest teleost C-starts' quoted for archerfish. Tension, not contradiction (smaller fish have higher relative speed). No adult zebrafish SL/s fast-start values found",
      "satisfied_evidence": "derived",
      "note": "Bamford & Seebacher 2024 PMC11340812 full-text; archerfish statement search-summary, authorship unverified; Domenici & Blake 1997 search-summary. Negative scope: one web search for adult zebrafish C-start peak velocity"},
    {"target_scale": "organism", "kind": "timescale",
      "statement": "Camera frame interval must be short (assumed factor >=5) relative to C-start stage 1/2 durations for peak speed to be resolved",
      "quantity": "frame interval / stage-1 duration", "lo": null, "hi": 0.2, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Frame interval 8.33 ms (120 fps, Miln 2021). Larval (5 dpf, 28 C) C-bend 0-11 ms gives ratio ~0.76 (fails for larvae). Adult zebrafish stage durations not found. At 1.38 m/s displacement per frame = 11.5 mm ~ 0.35 SL (calculated)",
      "satisfied_evidence": "unknown",
      "note": "Miln PMC8025299 full-text; larval durations PMC11930232 full-text (Fig 2 legend). Factor 5 is my assumption. Negative scope: one web search, no adult stage durations returned"},
    {"target_scale": "ecology", "kind": "range",
      "statement": "Water flow in occupied habitats must be below the fishes' swimming capacity (below the slowest individual's escape maximum)",
      "quantity": "habitat flow velocity", "lo": 0.0, "hi": 0.45, "units": "m/s",
      "status": "satisfied",
      "satisfied_by": "Measured site mean flows 0, 0, 0.06 +/- 0.008 and 0.16 +/- 0.081 m/s at Indian wild zebrafish sites (Shelton et al. 2020 Table 1); max mean is ~2.8x below 0.45 m/s",
      "satisfied_evidence": "measured",
      "note": "Shelton et al. 2020 Zebrafish 17:243 doi:10.1089/zeb.2019.1851 PMC7869874, full-text. Scope: 4 site types, one study; Spence 2006 and Engeszer 2007 could-not-access"},
    {"target_scale": "ecology", "kind": "range",
      "statement": "Thermal enhancement of fast-start speed between the 23 C test temperature and the warmest habitat temperature (39 C) must be less than the 4.23x margin to the threshold",
      "quantity": "effective Q10 of fast-start peak speed over 23-39 C", "lo": null, "hi": 2.46, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No zebrafish fast-start Q10 found. Related but non-qualifying: zebrafish developmental-rate Q10 2.33 (22-32 C); damselfish max escape speed unaffected by temperature (other taxon); mullet fast-start velocity rises with temperature to a threshold",
      "satisfied_evidence": "unknown",
      "note": "Habitat range 12-39 C from Parichy 2015 eLife (full-text); thermal items search-summary only. Negative scope: one web search; 'not found by me' not 'nobody has looked'. Bound 2.46 = 4.23^(10/16), calculated"}
  ]}
```
