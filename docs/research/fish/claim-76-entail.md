# Claim 76: entailments at the organism and ecology scales

**Source claim (behaviour scale, evidence: derived).** "The launch margin should be read as ~4-7x rather than a single
~7x, because the measured population spans a factor of three and 120 fps likely underestimates the instantaneous peak."

**Where it comes from.** `docs/research/fish/S21-deepen.md` §4, on branch `origin/claude/zebrafish-fast-start-velocity-pgqbck`
(read-level: **full-text**). The claim's inputs are:

- **The numerator, 5.84 m/s.** This is the speed a 0.4 g, 4 cm zebrafish needs to glide on a 1-body-length-span wing
  (AR 5, C_L 0.6). Source: `zebrafish-glide-physics.md` §"1 BL", branch `origin/claude/zebrafish-glide-physics-j176og`,
  read-level **full-text**. It is a **calculated** threshold, not a measurement.
- **The denominators.** These are adult zebrafish fast-start maxima from Miln, Ward & Seebacher 2021 (*R Soc Open Sci*
  8:210146, doi:10.1098/rsos.210146), digitised from Fig. 1a by S21-D and independently re-digitised by
  `challenge-75.md`:
  - range 0.45–1.38 m/s;
  - fastest fish 1.38 m/s;
  - median about 0.8 m/s.

**The animal throughout is the zebrafish, *Danio rerio*.** Every measured number below is labelled with its species. Where
the only number available is from another species, the constraint stays `open`.

**Prior same-scale review.** `challenge-76.md` (branch `origin/claude/challenge-launch-margin-a2dn77`, read-level
**full-text**) already rated this claim **weakened**:

- the 4–7x band mixes a maximum (which gives 4.2x) with a median (which gives about 7x);
- a 120 fps under-read would push the margin *below* 4.2x, not bound it at 4.

That is a defect inside the behaviour scale. It is not repeated as a constraint here. The constraints below ask only what
the claim's two stated reasons need from the organism and ecology scales.

**Everything numeric that is not quoted from a source is a calculation.** The script is
`docs/research/fish/claim-76-entail_calc.py` (run with `python3 -I`). Nothing here is a new measurement.

## Verdict in one paragraph

- **Unsatisfiable: none.** No measured zebrafish number contradicts any of the five constraints.
- **Satisfied: one, C3.** The 23 °C test temperature lies inside the thermal range in which wild *Danio rerio* have been
  found, 12.3–38.6 °C.
- **Open: the other four.**
  - **C1, the claim's second reason (timescale).** It needs the adult zebrafish centre-of-mass speed peak to be narrower
    than about 17–35 ms. No adult zebrafish measurement of that width was reachable. The only measured stage durations
    found are for **5 dpf larvae**, and those are the wrong life stage.
  - **C2, body size (spatial).** The Miln fish lengths are in an inaccessible data deposit. The calculation shows that the
    margin is insensitive to size anyway (±10 %).
  - **C4, the thermal sensitivity of fast-start speed.** This is the most fragile. If the zebrafish behaved like the two
    species for which I have a Q10 (whiting and *Eleginops*), the fastest fish's margin at 28 °C would be about 3.1x,
    which is outside the band. Those species are not zebrafish, so this is `open`, not `unsatisfiable`.
  - **C5, whether lab fish represent wild fish (range).** It is `open`. The one wild-versus-laboratory zebrafish
    comparison found shows that wild fish are faster in *sustained* swimming. That points the same way as C4: toward a
    smaller margin.

## 1. Entailments

If the claim is true, the following must hold at the adjacent scales.

| # | Scale | Kind | Requirement (generic) | Bound (calculated) |
|---|---|---|---|---|
| C1 | organism | timescale | For the 120 fps frame interval (8.33 ms) to under-read the true peak by a material amount (≥ 5 %), the speed pulse of the fast-start must be short compared with a few frame intervals | FWHM of the centre-of-mass speed peak ≤ 17.5 ms (1-frame difference, best phase) to ≤ 35 ms (worst phase, or a 2-frame central difference) |
| C2 | organism | spatial | The measured fish must be the same size, within a factor, as the fish for which the 5.84 m/s threshold was computed. Otherwise the ratio compares two animals | measured BL ∈ [33, 48] mm (40 mm ÷/× 1.2) |
| C3 | ecology | range | The test temperature at which the population spread was measured must lie inside the temperatures the species actually occupies | 23 °C ∈ [wild T_min, wild T_max] |
| C4 | ecology | range | Over the ecologically normal temperature span, the thermal sensitivity of fast-start peak speed must be small enough that the margin of the fastest fish stays ≥ 4 | Q10 of peak fast-start speed ≤ 1.12 over 23 → 28 °C |
| C5 | ecology | range | The lab-reared population must represent wild conspecifics. Wild fast-start peaks must not exceed lab peaks by more than the slack between 4.2x and 4x | wild/lab fast-start peak ratio ≤ 1.06 for the band's floor to hold (≤ 1.75 for the band to be anywhere near right) |

How the bounds were derived (all calculation):

- **C1.**
  - **Model.** The speed pulse is modelled as a Gaussian. A one-frame displacement difference is a box average over Δt =
    8.33 ms. A central difference over ±1 frame is a box average over 16.7 ms. I could not confirm which of the two
    Tracker 4 uses, because its documentation host was not reachable.
  - **Result.** The read-out peak falls ≥ 5 % below the true peak when FWHM ≤ 17.5 ms (best phase, 1-frame) or ≤ 35 ms
    (worst phase, or 2-frame). It falls ≥ 10 % below when FWHM ≤ 12.1 or 24.1 ms.
  - **Gap closure.** Closing the whole 4.23x gap by frame-averaging alone would need a pulse FWHM well under 5 ms. At
    FWHM 5 ms the worst-phase read-out is still 0.32 of the true peak, i.e. a 3.1x under-read.
  - **Why this constraint is needed.** If the real pulse is wider than about 35 ms, "120 fps likely underestimates" is
    true only trivially (< 5 %), and the claim loses its second reason.
- **C2.** For a 1-BL-span wing the glide threshold scales as V ∝ √(W/S) ∝ L^0.5 (with m ∝ L³ and S ∝ L²). If fast-start
  speed scales as L^a, the margin scales as L^(0.5−a). Between 33 mm (S21's derived length) and 40 mm (the threshold
  model), the margin shifts by 1.10x for a = 0, 1.00x for a = 0.5 and 0.91x for a = 1. So the factor-1.2 tolerance costs
  at most about 10 % on the margin.
- **C4.** The fastest fish's margin at 23 °C is 5.84 / 1.38 = 4.23. For it to stay ≥ 4 at 28 °C (the husbandry standard,
  and inside the wild range), the speed may rise by at most 1.058x over 5 °C. That gives Q10 ≤ 1.058² = 1.12.
- **C5.** The same arithmetic applies: 4.23 / 4 = 1.058. The looser 1.75 is the band's own width ratio (7 / 4). It is quoted
  only to show how far wrong the band could be before it is wrong everywhere.

## 2. Checks

### C1 — timescale: the speed pulse of an adult zebrafish fast-start must be ≲ 17.5–35 ms FWHM. **Status: open**

- **Adult zebrafish, measured.** I found no width of the centre-of-mass speed pulse, and no stage-1 or stage-2 duration in
  ms.
  - **Danos & Lauder 2012**, *J Exp Biol* 215:1854, doi:10.1242/jeb.068957, PMID 22573764. Read-level: **search-summary**
    (snippets, with the abstract quoted). The authors filmed at 1000 fps and report "maximum velocity of the center of
    mass" during stage 1. A secondary summary says a 20x viscosity increase "did not significantly affect the duration of
    stage 1 or stage 2". None of the snippets gave a duration in ms or the fish's age.
  - The full text was **could-not-access**. The Harvard DASH copy failed because `dash.harvard.edu` is outside this
    session's network allowance. The journal copy returned a Cloudflare 403 in challenge-76's session, and I did not retry
    it.
- **Larval zebrafish, measured (wrong life stage).** Ravel et al. 2025 (*iScience*, PMC11930232; read-level **full-text
  via an automated summarizer**, characters 0–100,000 of 153,097) give, for **5 dpf larvae** of 4.08 mm TL filmed at
  10,000 fps:
  - stage 1 (C-bend) "0–11 ms";
  - stage 2 "11–21 ms".
  - **My inference, not theirs:** stage durations lengthen with body size, so a 4 mm larva is expected to have a shorter
    pulse than a 30–40 mm adult. The larval number therefore does not satisfy the adult constraint, and it cannot
    contradict it either.
- **Other adult zebrafish papers screened.** These had no pulse widths or adult fast-start stage durations:
  - PMC12021243 (NaV1.4 knockout; adult escapes in methylcellulose, 500–1000 fps, turn angles only);
  - PMC12604801 (adult escapes at 240 fps, qualitative only);
  - PMC12180146 (larvae).
- **Scope of the negative:**
  - one Europe PMC query, `(zebrafish OR "Danio rerio") AND ("C-start" OR "fast-start" OR "escape response") AND adult
    AND ("stage 1" OR duration) AND (velocity OR speed)`, returned 348 hits, of which I screened the first 40 titles;
  - three of those were full-text keyword-scanned;
  - two web searches.
- **Finding.** This is "looked and not found within that scope", not "people looked and found nothing". The measurement
  exists in principle (Danos & Lauder recorded at 1000 fps); I could not read it.

### C2 — spatial: measured BL ∈ [33, 48] mm. **Status: open**

- **Miln et al. 2021**, read-level **full-text** (Europe PMC XML for PMC8025299, keyword-scanned in this session). The
  fish were weighed and photographed for standard length. They were "size matched so that they were within 2 mm standard
  length of each other". The text gives **no numeric length or mass**.
- The per-fish data are in the figshare deposit (doi:10.6084/m9.figshare.c.5359401). It was **could-not-access**: S21-D
  and challenge-76 both reported a proxy 403, and I did not retry it.
- S21's 33 mm is **derived** (0.842 m/s ÷ 25.5 TL/s), not measured on the Miln fish.
- **Calculated mitigation.** Even a full 1.2x mismatch moves the margin by ≤ 10 % (§1). So this constraint is unlikely to
  decide the claim, but it is unverified.

### C3 — ecology range: 23 °C inside the occupied thermal range. **Status: satisfied**

- **Morgan et al. 2019**, *Conserv Physiol* 7:coz036 (PMC6589993). Read-level: **full-text via an automated
  summarizer**. They write that wild zebrafish "have been found in water temperatures ranging from 12.3–38.6°C", citing
  Engeszer et al. 2007, Spence et al. 2008 and Arunachalam et al. 2013.
  - I did **not** read those three primary sources.
  - The Engeszer 2007 entry was found only as a **listing** (ZFIN, journal abstract page).
  - A hobbyist page attributes "24.6–38.6 °C in July" to it. That page is a **search-summary** of an unsourced page and is
    not relied on.
- **Corroboration.** Morgan et al. 2022, *PNAS* 119:e2201919119 (PMC9295802). Read-level: **full-text** (XML, keyword
  scan). They acclimated wild-caught F1 *Danio rerio* (offspring of fish from West Bengal) to 10–36 °C and phenotyped them
  there. Their statistical models were centred on 23 °C.
- **Species on both sides:** *Danio rerio* in the claim (Miln's adults) and *Danio rerio* in the source (wild
  populations). 23 °C lies inside 12.3–38.6 °C under either reading. **Satisfied, evidence: literature.**
- **What this does not show.** Satisfying C3 says the test temperature is ecologically real. It does not say 23 °C is
  representative; that question is C4.

### C4 — ecology range: thermal sensitivity of zebrafish fast-start peak speed, Q10 ≤ 1.12 over 23 → 28 °C. **Status: open**

- **Zebrafish, fast-start peak speed versus temperature:** `unknown`. I found no measurement.
  - **Morgan et al. 2022** (full-text, above) measured two things across 10–36 °C:
    - a *sustained* maximum swim speed, "the speed at which the fish were able to maintain their position in the water
      column for at least 1 min";
    - startle **latency** at 1000 fps.
  - They did not measure fast-start peak speed. Sustained speed is a different trait (aerobic, red-muscle-limited), so its
    thermal curve cannot be transferred to fast-start speed. I also did not extract that curve's values from their
    Fig. 3D.
  - One web search for a Seebacher-lab zebrafish fast-start thermal study returned none. The hits were
    Bamford & Seebacher 2024 (U_Cfast, a sustained protocol) and Grigaltchik et al. 2012 (mosquitofish and bass).
- **Other species: these are not zebrafish, so they cannot refute the claim.** Read-level for each: **search-summary**.
  - Whiting, maximum swimming speed: Q10 1.81 (Özbilgin 2002, *Turk J Zool*).
  - *Eleginops maclovinus*, fast-start V_max: Q10 1.90 (Fernandez et al. 2002, *Polar Biol*).
  - **Calculated:** if zebrafish had these values, the 1.38 m/s fish would reach 1.86–1.90 m/s at 28 °C, and its margin
    would be **3.07–3.15x**. That is below the band's floor.
  - **Disagreement, preserved.** Other species show little or no acute or acclimated thermal effect on fast-start
    maximum speed. Coral-reef damselfish showed "no effect of temperature … on maximum swimming speed". In mummichog,
    performance was "similar across temperatures" after acclimation. Read-level for both: **search-summary**.
  - Across species, then, Q10 spans roughly 1 to 1.9. The bound of 1.12 sits inside that spread. Whether the zebrafish
    sits on the flat side or the steep side is exactly what is unknown.
- **Why this matters more than its `open` label suggests.** The claim's lower end (4.2x) was measured at 23 °C. The
  species is normally kept at 28 °C and is found up to 38.6 °C in the wild. For "~4x" to describe the species and not just
  one cool trial, zebrafish fast-start speed must be nearly temperature-independent. That has not been shown.

### C5 — ecology range: wild/lab fast-start peak ratio ≤ 1.06 (floor) / ≤ 1.75 (band). **Status: open**

- **Zebrafish, fast-start peak speed in wild versus laboratory fish:** `unknown`. I found no direct comparison.
- **Nearest zebrafish evidence (a different trait and a different life stage).** Morgan et al. 2022 (full-text) compared
  juvenile wild-caught F1 fish with the AB laboratory line. For *sustained* maximum swim speed, they report: "the thermal
  performance breadth of laboratory fish was within 1 °C of the wild fish, but the peak performance was lower". The size
  of the difference was not extracted.
  - **My inference, not theirs:** if fast-start speed followed the same direction, wild fish would be faster, and the
    wild margin would be *smaller* than the lab 4.2x. That points the same way as C4. It is not evidence about fast-start
    speed.
- **Miln's fish.** They are "adult short-fin zebrafish". Their strain or source was not found in my keyword scan of the
  methods.
- **Scope of the negative:**
  - one web search, "wild-caught versus laboratory zebrafish escape response fast-start speed";
  - the full-text scan of PMC9295802.
  - I did not read the 2024 *Sci Rep* wild-versus-AB/TU/WIK behaviour paper (s41598-024-71451-x) beyond its
    search-summary, which concerns aggression and not escape speed.

## 3. What this propagation adds to challenge-76

Challenge-76 weakened the claim from inside the behaviour scale. The adjacent scales add three findings:

1. **The second reason has a checkable condition (C1), and it is unchecked.** "120 fps likely underestimates" is true to a
   material degree only if the adult zebrafish speed pulse is narrower than about 17–35 ms. The 1000 fps adult zebrafish
   dataset that would decide it exists (Danos & Lauder 2012), but it was not reachable from this session.
2. **The 4x floor is temperature-conditional (C4).** It needs a fast-start Q10 ≤ 1.12. That has not been measured for
   zebrafish. Two other species exceed it, and two others are consistent with it.
3. **Nothing measured on zebrafish contradicts the claim from below.** No constraint is `unsatisfiable`. The two
   cross-species numbers that would break C4 are recorded as cross-species, and they are why C4 is `open`, not
   `unsatisfiable`.

### Sources and read-levels

- `S21-deepen.md` (origin/claude/zebrafish-fast-start-velocity-pgqbck): **full-text**
- `challenge-76.md` (origin/claude/challenge-launch-margin-a2dn77): **full-text**
- `challenge-75.md` (origin/claude/challenge-75-zebrafish-fast-start-im1x80): **full-text** (first 60 lines)
- `zebrafish-glide-physics.md` (origin/claude/zebrafish-glide-physics-j176og): **full-text** (keyword scan for the
  threshold's inputs)
- Miln, Ward & Seebacher 2021, *R Soc Open Sci* 8:210146, PMC8025299: **full-text** (XML keyword scan)
- Miln et al. figshare doi:10.6084/m9.figshare.c.5359401: **could-not-access** (reported by S21-D and challenge-76; not
  retried)
- Danos & Lauder 2012, *J Exp Biol* 215:1854, doi:10.1242/jeb.068957: **search-summary**. The full text was
  **could-not-access** (`dash.harvard.edu` is not in this session's network allowance).
- Ravel et al. 2025, *iScience*, PMC11930232: **full-text via summarizer**, first 100k of 153k characters
- Morgan et al. 2019, *Conserv Physiol* 7:coz036, PMC6589993: **full-text via summarizer**
- Engeszer et al. 2007, *Zebrafish* 4:21, doi:10.1089/zeb.2006.9997: **listing**
- Morgan et al. 2022, *PNAS* 119:e2201919119, PMC9295802: **full-text** (XML keyword scan)
- PMC12021243, PMC12604801, PMC12180146: **full-text** (XML keyword scan)
- Özbilgin 2002 (*Turk J Zool* 26) and Fernandez et al. 2002 (*Polar Biol*), Q10 values: **search-summary**
- Damselfish and mummichog thermal fast-start results: **search-summary**
- Tracker 4 velocity algorithm: **could-not-access** (`physlets.org` is not in the network allowance)

**To make progress:** allow `dash.harvard.edu` or `journals.biologists.com` (Danos & Lauder, for C1), and allow
`figshare.com`/`api.figshare.com` (Miln per-fish SL, for C2) in the session's network settings.

```swarm-entail
{"source_claim": 76, "source_scale": "behaviour",
  "constraints": [
    {"target_scale": "organism", "kind": "timescale",
      "statement": "For a 120 fps frame interval (8.33 ms) to under-read the true peak by a material amount (>=5%), the centre-of-mass speed pulse of the adult fast-start must be short compared with a few frame intervals",
      "quantity": "FWHM of the centre-of-mass speed peak during an adult zebrafish fast-start", "lo": null,
      "hi": 35, "units": "ms",
      "status": "open",
      "satisfied_by": "No adult zebrafish pulse width or stage duration found. Only larval (5 dpf, 4 mm) stage 1 = 0-11 ms and stage 2 = 11-21 ms (Ravel et al. 2025), which is the wrong life stage",
      "satisfied_evidence": "unknown",
      "note": "Bound calculated with a Gaussian-pulse box-average model: 17.5 ms best-phase 1-frame, 35 ms worst-phase or 2-frame. Danos & Lauder 2012 (J Exp Biol 215:1854, 1000 fps, zebrafish) would decide it; search-summary only, full text could-not-access. Negative scope: Europe PMC query, 348 hits, first 40 titles screened, 3 full texts scanned, 2 web searches."},
    {"target_scale": "organism", "kind": "spatial",
      "statement": "The fish whose fast-start speeds form the denominator must match, within a factor of 1.2, the body size for which the glide-speed threshold in the numerator was computed",
      "quantity": "body length of the Miln et al. 2021 adults", "lo": 33, "hi": 48, "units": "mm",
      "status": "open",
      "satisfied_by": "Miln et al. 2021 measured SL and mass but the full text gives no numbers; per-fish data are on figshare (could-not-access). S21's 33 mm is derived, not measured",
      "satisfied_evidence": "unknown",
      "note": "Calculated: margin scales as L^(0.5-a), so a 1.2x size mismatch shifts the margin by at most ~10%. Miln et al. 2021 PMC8025299 full-text keyword scan; figshare doi:10.6084/m9.figshare.c.5359401 could-not-access."},
    {"target_scale": "ecology", "kind": "range",
      "statement": "The test temperature at which the population spread was measured must lie inside the temperature range the species occupies in the wild",
      "quantity": "wild habitat water temperature of Danio rerio, which must contain 23 C", "lo": 12.3, "hi": 38.6, "units": "degC",
      "status": "satisfied",
      "satisfied_by": "Wild zebrafish found at 12.3-38.6 C (Morgan et al. 2019, citing Engeszer 2007, Spence 2008, Arunachalam 2013). Wild-caught F1 Danio rerio acclimated and phenotyped at 10-36 C (Morgan et al. 2022)",
      "satisfied_evidence": "literature",
      "note": "Same species on both sides (Danio rerio). Morgan et al. 2019 Conserv Physiol 7:coz036 PMC6589993, full-text via summarizer; the three primary sources were not read (Engeszer 2007 listing only). Morgan et al. 2022 PNAS PMC9295802, full-text."},
    {"target_scale": "ecology", "kind": "range",
      "statement": "Across the ecologically normal temperature span, the thermal sensitivity of fast-start peak speed must be small enough that the fastest fish's margin stays at or above 4",
      "quantity": "Q10 of adult zebrafish fast-start peak speed between 23 and 28 C", "lo": null, "hi": 1.12, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No zebrafish fast-start speed versus temperature measurement found. Morgan et al. 2022 measured sustained max swim speed and startle latency (a different trait) across 10-36 C",
      "satisfied_evidence": "unknown",
      "note": "Bound calculated: 4.23/4 = 1.058 over 5 C. Cross-species only, not a refutation: whiting Q10 1.81 (Ozbilgin 2002) and Eleginops maclovinus Q10 1.90 (Fernandez 2002) would give a 28 C margin of 3.07-3.15 (calculated). Damselfish and mummichog show little thermal effect. All read-level search-summary. Negative scope: 2 web searches plus the PMC9295802 full text."},
    {"target_scale": "ecology", "kind": "range",
      "statement": "The lab-reared measured population must represent wild conspecifics: wild fast-start peak speed must not exceed the lab value by more than the slack between the 4.2x and 4x margins",
      "quantity": "wild/lab ratio of adult zebrafish fast-start peak speed", "lo": null, "hi": 1.06, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No wild-versus-lab fast-start speed comparison found. Morgan et al. 2022 report lower peak sustained max swim speed in AB lab juveniles than in wild F1 juveniles (a different trait and life stage; this points toward a smaller wild margin)",
      "satisfied_evidence": "unknown",
      "note": "Bound calculated: 4.23/4. The looser 1.75 is the band's own width. Morgan et al. 2022 PNAS 119:e2201919119 PMC9295802 full-text. Negative scope: 1 web search plus that full text; the 2024 Sci Rep wild-versus-lab paper was read as search-summary only (it covers behaviour, not escape speed)."}
  ]}
```
