# Claim 76: entailment at the adjacent scales (`behaviour` → `organism`, `ecology`)

**Source claim (scale `behaviour`, evidence: derived).** From S21-D,
`docs/research/fish/S21-deepen.md`, branch `claude/zebrafish-fast-start-velocity-pgqbck`, commit
9ae82754. I read it in full.
> "The launch margin should be read as ~4-7x rather than a single ~7x, because the measured population
> spans a factor of three and 120 fps likely underestimates the instantaneous peak."

**Subject animal:** adult zebrafish, *Danio rerio*. Every number below is labelled with its animal.
Every number I use as a measurement is about adult *D. rerio*. No flying-fish (exocoetid) numbers are
used anywhere in this file.

**What "margin" means here.** The margin is the threshold divided by the in-water peak fast-start speed,
with the threshold at 5.84 m/s. The provenance of 5.84 m/s is **unknown**. S21-D says the S21 record is not
in the repository, and I did not find it either. So **4–7x is equivalent to an attainable peak speed of
0.834–1.46 m/s**. That is calculated as 5.84/7 and 5.84/4.

**Prior review.** Challenge 76 (`docs/research/fish/challenge-76.md`, branch
`claude/challenge-launch-margin-a2dn77`, read in full) already **weakened** this claim on internal logic.
Its corrected reading is margin ≲ 4.2x. This file does something different. It derives what the claim
requires at the adjacent scales and checks those requirements against measurements.

**Date of checks:** 2026-11-04.

## Access limitations, stated up front

These hosts were unreachable from this session:
- `sites.harvard.edu`, which hosts the Danos & Lauder 2012 PDF (DNS refused).
- `bio.uib.no`, which hosts the Sundin et al. 2019 PDF (DNS refused).
- `webarchiv.lib.cas.cz`, which hosts the Spence et al. Bangladesh survey PDF (proxy 403).

Europe PMC (`www.ebi.ac.uk`) worked, and was my only primary literature route. Danos & Lauder 2012 is the
one 1000 fps adult *D. rerio* dataset. Its peak-velocity numbers are therefore still **unknown**: I did not
read them, and I do not supply any.

Search control: a Europe PMC query `zxqvblorph AND zebrafish` returned **0 hits**. That is the must-fail
check. The broad topical queries below returned hundreds of hits, so the search endpoint can come back
empty and does discriminate.

---

## 1. ENTAIL: what claim 76 requires

| id | scale | kind | requirement |
|----|-------|------|-------------|
| O1 | organism | range | The attainable in-water peak fast-start speed of an adult must lie in **[0.834, 1.46] m/s**. That is the 4–7x band re-expressed as speed: 5.84/7 to 5.84/4. If the attainable peak is above 1.46 m/s, the margin is below 4x. |
| O2 | organism | timescale | The claim's second reason is that 120 fps under-reads the peak. For that to be possible at all, the rise from escape onset to peak speed must be short compared with the sampling interval: **≤ ~16.7 ms**, i.e. about two frames at 120 fps (8.3 ms per frame). |
| O3 | organism | spatial | The fish whose speeds set the band must match, within a factor of about 1.5, the body length that anchors the 0.842 m/s / 25.5 TL/s figure: **22–50 mm**, i.e. 33 mm ÷ 1.5 to 33 mm × 1.5. Absolute burst speed scales roughly with length, so a band taken from fish of a different size is a band for a different animal. |
| E1 | ecology | range | The band is read as the species' launch margin. For that, the band-setting speeds must be measured at a temperature inside the species' natural habitat range. The test temperature of the Miln et al. data, **23 °C**, must therefore fall within the field range of wild *D. rerio* water temperatures. |
| E2 | ecology | spatial | If the attainable in-water peak is ≤ 1.46 m/s, then any aerial excursion by wild or captive adults is ballistically capped. The cap is the maximum leap height above the surface **≤ v²/2g = 0.109 m**: no drag, vertical exit, full in-water peak carried through the surface. This is a generous cap, because exit costs only lower it. A measured adult *D. rerio* leap above ~0.11 m would contradict the band. |

O1, O2, O3 and E2 can all be checked against measured numbers with no simulation. All arithmetic in this
file is **calculated** by me with python. None of it is observed.

---

## 2. CHECK

### O1 (range): attainable adult peak speed in [0.834, 1.46] m/s. **UNSATISFIABLE** at face value of a same-species measurement

**The measurement.** Demesmay et al. 2025, *PLoS Biol*, doi:10.1371/journal.pbio.3003484, PMC12604801.
Read-level: **full-text** (Europe PMC full-text XML, fetched this session).
- Subject: **adult *Danio rerio***, 4–12 months, body length 2.6 ± 0.2 cm (4 months) to 3.6 ± 0.2 cm
  (12 months). Reared at 28 ± 0.5 °C.
- Escapes filmed at **240 frames/s**, which is twice Miln et al.'s frame rate, on a Xiaomi Redmi Note 13 Pro+.
  The stimulus was a 1 g object dropped from ~30 cm into a 1.6 L tank. Tracking used the Fiji manual
  tracking plugin.
- Authors' numbers: "calculated maximal speed (**157 ± 27 cm/s** for controls and **161 ± 33 cm/s** for
  mutants)". Latency to maximal speed was 8 ± 4 ms and 9 ± 3 ms. The two genotypes did not differ.
  Challenge 143, which read the same paper in full, gives n ≥ 11 per genotype. The methods do not state the
  test-water temperature for the escape trials. They do not state the tracked body point. They give no
  tracking-error estimate.

**Animal on both sides:** the claim is about adult *D. rerio*, and the measurement is of adult *D. rerio*.
The species match.

**Contradiction (calculated from the authors' measured values):**

| Speed (m/s), adult *D. rerio*, 240 fps | Margin = 5.84 / v |
|---|---|
| Control mean, 1.57 | **3.72x** |
| Mutant mean, 1.61 | 3.63x |
| Control mean + 2 SD, 2.11 | 2.77x |
| Band's lower speed bound (7x end), 0.834 | 7.0x |

- The control **mean** of 1.57 m/s already exceeds the band's upper speed bound of 1.46 m/s.
- The attainable peak is the population's upper tail, not its mean, so it lies higher still.
- The band's 7x end requires an attainable peak near 0.834 m/s. That sits **2.7 SD below** the measured
  control mean (calculated). On this dataset, no part of the 4–7x band describes the attainable peak.

The constraint is contradicted at both ends by a measured value about the same animal.

**What would overturn this verdict.** I am stating this so the verdict can be attacked, not to soften it.
The refutation would fail only if Demesmay et al.'s maximal-speed values are inflated by measurement method.
For the mean to fall to the band edge, the inflation would need to be **≥ 0.11 m/s (≥ 7%)**. For the upper
tail to fall inside the band, it would need to be much larger, ~0.65 m/s at +2 SD.

An upward bias is plausible in direction. It comes from taking the maximum of frame-to-frame differences of
hand-clicked positions. Challenge 143 calculated ±0.24 m/s per 1 mm click error at 240 fps. The paper
reports no error budget, so the size of the bias is **unknown**.

Two further possible confounds:
- Test temperature: possibly 28 °C (Demesmay) against 23 °C (Miln). This is unconfirmed, since Demesmay
  state only the rearing temperature.
- Lab and strain.

These would explain *why* the two datasets differ. They do not rescue the band, because the claim states the
band for the species, not for 23 °C.

**Disagreement preserved, not averaged.**
- Miln et al. 2021 (R Soc Open Sci 8:210146, PMC8025299). Read-level: **full-text** for methods. The speeds
  themselves are S21-D's digitisation of Fig. 1a, which I did not redo. Values: adult *D. rerio*, 120 fps,
  best of 4 escapes per fish, 23 °C, per-fish maxima **~0.45–1.38 m/s**. Its fastest fish (1.38 m/s, 4.23x)
  sits inside the band.
- Demesmay et al. 2025, at twice the frame rate, puts the **mean** fish above the band.

The direction of the disagreement fits the claim's own second reason, that 120 fps under-reads. But a
correction in that direction moves the margin *below* 4x. That is the same point challenge 76 made from
logic alone. Here it is made from a measurement.

### O2 (timescale): onset-to-peak rise ≤ ~16.7 ms. **SATISFIED** (with a stated limit)

Demesmay et al. 2025 (adult *D. rerio*, full-text) report latency to maximal speed of **8 ± 4 ms**
(controls) and **9 ± 3 ms** (mutants), measured. That is about one 120 fps frame interval, well inside the
16.7 ms bound. So the precondition for a 120 fps under-read is met. The acceleration to peak is short enough
that one or two frames at 120 fps can straddle it.

Limits:
1. The 240 fps measurement is itself resolution-limited. 8 ms is ~2 frames at 4.17 ms per frame, so the true
   rise time is known only to about ±4 ms.
2. Rise time is not the width of the velocity peak. The *size* of the under-read depends on the peak width,
   and that is **unknown** here. It is in Danos & Lauder 2012 (1000 fps), which I could not access
   (read-level **abstract**, via an earlier session's Europe PMC read, quoted in S21-D; the PDF host is
   blocked this session).

This constraint establishes that the mechanism *can* operate. It does not establish its magnitude.

### O3 (spatial): band-setting fish 22–50 mm long. **OPEN**

- Miln et al. 2021 measured standard length for every fish. The full-text methods state they were
  photographed and measured in Tracker. But the numeric lengths are only in the figshare collection
  (doi:10.6084/m9.figshare.c.5359401). That collection was **could-not-access** in the S21-D and challenge-76
  sessions (proxy 403 on `api.figshare.com`), and I did not retry it.
- The main text gives no length values. The only length information is that group members were matched
  "within 2 mm standard length of each other".
- The band is built from Miln's data, so the constraint is unchecked for the dataset that sets it.
- For comparison only: the Demesmay fish (2.6–3.6 cm, measured) satisfy it. That supports treating the two
  datasets as describing similarly sized animals, so their disagreement in O1 is not obviously a size effect.

### E1 (range): 23 °C inside the wild habitat temperature range. **OPEN**, and sources disagree

What I searched:
- Europe PMC, `TITLE:(zebrafish OR "Danio rerio") AND TITLE:(wild OR "natural history" OR habitat OR
  "natural populations" OR field)`, 222 hits. I screened the first 25 titles. A broader full-text query
  returned 541 hits that were mostly off-topic; I screened the first 15.
- One standard web search.

Results:
- **Sundin et al. 2019**, *Zebrafish* 16:546–553, doi:10.1089/zeb.2019.1778. Read-level: **abstract**
  (Europe PMC). It records water-chemistry data at 12 wild *D. rerio* sites in West Bengal. The temperature
  values are in its Table 1, and the PDF host (`bio.uib.no`) was unreachable, so the values are **unknown**.
- Secondary figures, read-level **search-summary** only (a search engine's summary of aquarist and
  encyclopaedia sites; not primary, not verified):
  - "24.6–38.6 °C" in native waters in July (Seriously Fish).
  - "16.5–34 °C" across Bangladeshi and Indian surveys (animalia.bio).
  These **disagree**:
  - Under the first, 23 °C lies *below* the recorded range.
  - Under the second, it lies inside.
  - The first is a single-month (monsoon) range, so it is not evidence about the annual minimum.
  I do not average them, and I do not use either as a verdict.
- On the size of the temperature effect: **Miller et al. 2023**, *Am Nat* 202:519–533,
  doi:10.1086/726011. Read-level: **abstract**. They measured *D. rerio* sprint speed at six temperatures
  between 16 and 34 °C, but the abstract gives no speed values. So the size of a 23 → 28 °C effect on
  adult escape speed remains **unknown**.

Status: open. A primary field temperature table exists (Sundin 2019, Table 1) but I could not read it.

### E2 (spatial): wild or captive adult leap height ≤ 0.109 m. **UNSATISFIED**: no measurement located

What I searched:
- Europe PMC, `(zebrafish OR "Danio rerio") AND (jump OR leap OR leaping) AND (height OR "out of water")`,
  415 hits, first 15 screened. None was an adult *D. rerio* leap-height measurement.
- One standard web search. It returned cross-species leaping-scaling work and a poster on zebrafish
  *terrestrial* tail-flip jumps, which had no heights in the excerpt.

Scope of the negative: this is **"I looked, within that scope, and found no measurement"**. It is not
"people looked and found zebrafish leaps are low". Whether anyone has measured adult *D. rerio* leap height
is **unknown** to me. Hits 16–415 were not screened.

Cross-species leaping data (for example guppy jumps of ~3.5 body lengths, from a search summary) are about a
different animal. I note them only as a reason the check is worth doing. At 3.5 × ~3 cm ≈ 0.1 m, an
equivalent zebrafish leap would sit right at the cap. **That is an inference from another species, not a
verdict.**

Sensitivity of the cap (calculated, ballistic, no drag):
- At Miln's fastest fish (1.38 m/s): 0.097 m.
- At Demesmay's control mean (1.57 m/s): 0.126 m.
- At Demesmay's +2 SD (2.11 m/s): 0.227 m.

A single measured adult leap of ~0.15–0.2 m would therefore separate the two datasets in O1 from above.

---

## Net effect on claim 76

- **O1 is unsatisfiable on a same-species measurement.**
  - Adult *D. rerio* filmed at 240 fps reach a **mean** maximal speed of 1.57 m/s (Demesmay et al. 2025,
    full-text). That gives a margin of 3.72x at the mean and 2.77x at +2 SD (calculated).
  - Both values are outside 4–7x, and the attainable peak lies above the mean.
  - The refutation stands unless that dataset's manual-tracking maximum is inflated by ≥ 7%. That is
    possible in direction and unquantified in size. It is stated above as the one route that would overturn
    the verdict.
  - This agrees with challenge 76's logic-only correction (margin ≲ 4.2x), and goes further: the evidence
    now points to the margin being **below 4x**, not 4–7x.
  - What survives is the qualitative point that one ~7x number was wrong, and wrong in the direction of
    being too generous.
- **O2 is satisfied.** The rise to peak (8 ± 4 ms) is short enough for 120 fps to under-read. The claim's
  second *reason* is supported in mechanism. Its consequence is to lower the margin, not to bound it at 4x.
- **O3 and E1 are open**, each blocked by one unreadable primary table: Miln's figshare lengths, and Sundin
  2019 Table 1.
- **E2 is unsatisfied.** I found no leap-height measurement for adult *D. rerio*, within the stated search
  scope.
- **The threshold 5.84 m/s has unknown provenance.** Every margin here inherits that.

### Sources and read-levels
- S21-D, `docs/research/fish/S21-deepen.md` (branch `claude/zebrafish-fast-start-velocity-pgqbck`). **full-text**
- Challenge 76, `docs/research/fish/challenge-76.md` (branch `claude/challenge-launch-margin-a2dn77`). **full-text**
- Challenge 143, `docs/research/fish/challenge-143.md` (branch `claude/challenge-143-danio-speed-u4d1t2`). **full-text**
- Demesmay et al. 2025, PLoS Biol, doi:10.1371/journal.pbio.3003484, PMC12604801. **full-text** (Europe PMC XML; methods, results, Fig 4 legend)
- Miln, Ward & Seebacher 2021, R Soc Open Sci 8:210146, PMC8025299. **full-text** (methods). Speeds are S21-D's digitisation, which I did not redo.
- Miln et al. figshare, doi:10.6084/m9.figshare.c.5359401. **could-not-access** (per S21-D and challenge 76; not retried)
- Danos & Lauder 2012, J Exp Biol 215:1854, doi:10.1242/jeb.068957. **search-summary** this session (the PDF host `sites.harvard.edu` is not in this session's allowed network domains); abstract-level per earlier sessions
- Sundin et al. 2019, Zebrafish 16:546, doi:10.1089/zeb.2019.1778. **abstract** (PDF host `bio.uib.no` unreachable)
- Miller et al. 2023, Am Nat 202:519, doi:10.1086/726011. **abstract**
- Ackerly & Ward 2016, J Exp Zool A 325:25, doi:10.1002/jez.1993. **abstract**. Read, not used for a verdict. It shows that adult *D. rerio* C-start velocity relates to anatomy, and that survival against a native predator (*Xenentodon cancila*) relates to caudal vertebral number.
- Habitat temperatures from Seriously Fish and animalia.bio. **search-summary** (secondary; not used for a verdict)

To close O3, E1 and the size of O2, allow `api.figshare.com`, `bio.uib.no` and `sites.harvard.edu` in the
session's network settings.

```swarm-entail
{"source_claim": 76, "source_scale": "behaviour",
  "constraints": [
    {"target_scale": "organism", "kind": "range",
      "statement": "The attainable in-water peak fast-start speed of an adult of the species must lie between threshold/7 and threshold/4, i.e. the 4-7x margin band re-expressed as a speed.",
      "quantity": "attainable adult peak fast-start centre-of-mass speed (threshold 5.84 m/s, provenance unknown)", "lo": 0.834,
      "hi": 1.46, "units": "m/s",
      "status": "unsatisfiable",
      "satisfied_by": "Measured contradiction, same species: adult Danio rerio (4-12 months, 2.6-3.6 cm) filmed at 240 fps reach maximal speed 157 +/- 27 cm/s SD (controls) and 161 +/- 33 cm/s (scn4aa/scn4ab mutants), n>=11 per genotype. The control MEAN 1.57 m/s already exceeds the 1.46 m/s upper bound (margin 3.72x, calculated); +2 SD = 2.11 m/s gives 2.77x (calculated); the band's 7x end (0.834 m/s) lies 2.7 SD below the measured mean. Miln et al. 2021 (adult D. rerio, 120 fps, 23 C) fastest fish ~1.38 m/s (4.23x) sits inside the band; the two datasets disagree and the disagreement is in the direction the claim itself predicts (120 fps under-reads), which moves the margin below 4x.",
      "satisfied_evidence": "measured",
      "note": "Demesmay et al. 2025 PLoS Biol doi:10.1371/journal.pbio.3003484 PMC12604801, read-level full-text (Europe PMC XML). Animal on both sides: adult Danio rerio. Would be overturned only if that dataset's manual-tracking (Fiji, smartphone slow-motion, tracked point and error unreported) inflates the mean maximal speed by >=0.11 m/s (>=7%); upward bias of max-of-frame-differences is plausible in direction, unquantified in size. Test-water temperature of the escape trials not stated (rearing 28 C) vs Miln 23 C -- a possible explanation of the difference, not a rescue of a species-level band. Miln et al. 2021 PMC8025299 methods full-text; its speeds are S21-D's digitisation of Fig 1a."},

    {"target_scale": "organism", "kind": "timescale",
      "statement": "For a 120 fps camera to under-read the peak, the rise from escape onset to peak centre-of-mass speed must be no longer than about two 120 fps frame intervals.",
      "quantity": "latency from escape onset to maximal speed", "lo": null,
      "hi": 16.7, "units": "ms",
      "status": "satisfied",
      "satisfied_by": "Adult Danio rerio latency to maximal speed 8 +/- 4 ms (controls) and 9 +/- 3 ms (mutants), measured at 240 fps -- about one 120 fps frame, inside the bound. The precondition for a 120 fps under-read holds.",
      "satisfied_evidence": "measured",
      "note": "Demesmay et al. 2025 PMC12604801, read-level full-text. Limits: the 240 fps measurement resolves rise time only to ~+/-4 ms; rise time is not velocity-peak width, and the MAGNITUDE of the under-read depends on the width, which is unknown here -- it is in Danos & Lauder 2012 J Exp Biol 215:1854 (1000 fps, adult D. rerio), could-not-access this session (sites.harvard.edu not in allowed network domains). Satisfied as a mechanism, not as a magnitude."},

    {"target_scale": "organism", "kind": "spatial",
      "statement": "The fish whose speeds set the margin band must match, within a factor of about 1.5, the body length that anchors the derived 0.842 m/s (25.5 TL/s) value, since absolute burst speed scales with length.",
      "quantity": "body length of the band-setting fish", "lo": 22,
      "hi": 50, "units": "mm",
      "status": "open",
      "satisfied_by": "Not checked for the band-setting dataset: Miln et al. 2021 measured standard length for every fish, but numeric values are only in the figshare collection, which could not be accessed. For comparison only, the Demesmay et al. 2025 adults (2.6 +/- 0.2 to 3.6 +/- 0.2 cm, measured) fall inside the window.",
      "satisfied_evidence": "unknown",
      "note": "Miln et al. 2021 PMC8025299 full-text methods (lengths measured; main text gives only 'within 2 mm standard length' matching within groups). figshare doi:10.6084/m9.figshare.c.5359401 could-not-access (proxy 403 in S21-D and challenge-76 sessions; not retried). 33 mm anchor is S21-D's calculation from S21's 0.842 m/s and 25.5 TL/s."},

    {"target_scale": "ecology", "kind": "range",
      "statement": "For the band to stand as the species' launch margin, the temperature at which the band-setting speeds were measured must lie inside the species' natural habitat water-temperature range.",
      "quantity": "test temperature of the band-setting data (Miln et al. 23 C) relative to wild habitat range", "lo": null,
      "hi": null, "units": "degC",
      "status": "open",
      "satisfied_by": "Primary field temperature data exist (Sundin et al. 2019, water chemistry at 12 wild Danio rerio sites, West Bengal) but the table was unreadable. Secondary search-summary figures disagree: 24.6-38.6 C (July, aquarist site) would put 23 C below range; 16.5-34 C (animalia.bio) would put it inside. Not averaged, not used for a verdict. Size of the temperature effect on D. rerio speed also unknown: Miller et al. 2023 measured sprint speed at 16-34 C but the abstract gives no values.",
      "satisfied_evidence": "unknown",
      "note": "Sundin et al. 2019 Zebrafish 16:546 doi:10.1089/zeb.2019.1778 read-level abstract (PDF host bio.uib.no unreachable). Miller et al. 2023 Am Nat 202:519 doi:10.1086/726011 read-level abstract. Search scope: Europe PMC title query for zebrafish AND (wild OR natural history OR habitat OR natural populations OR field), 222 hits, first 25 titles screened; a broader full-text query (541 hits, first 15 screened); one web search. Must-fail control query returned 0 hits."},

    {"target_scale": "ecology", "kind": "spatial",
      "statement": "If the attainable in-water peak is at most threshold/4, any leap of an adult out of water is ballistically capped: maximum height above the surface must not exceed v^2/2g at that speed (no drag, vertical exit, full in-water peak carried through the surface -- a generous cap).",
      "quantity": "maximum measured leap height of adult fish above the water surface", "lo": null,
      "hi": 0.109, "units": "m",
      "status": "unsatisfied",
      "satisfied_by": "No measurement of adult Danio rerio leap height located. Cap sensitivity, calculated: 0.097 m at 1.38 m/s (Miln fastest), 0.126 m at 1.57 m/s (Demesmay mean), 0.227 m at 2.11 m/s (Demesmay +2 SD); a measured leap of ~0.15-0.2 m would discriminate the datasets in the organism-range constraint from above.",
      "satisfied_evidence": "unknown",
      "note": "Scope of the negative: Europe PMC (zebrafish OR Danio rerio) AND (jump OR leap OR leaping) AND (height OR out of water), 415 hits, first 15 screened, none an adult D. rerio leap-height measurement; one web search returning only cross-species leaping-scaling work and a zebrafish terrestrial tail-flip poster without heights. This is 'I looked within that scope and found nothing', NOT 'people looked and found leaps are low'; whether anyone has measured it is unknown. Cross-species leap data (e.g. guppy ~3.5 body lengths, search-summary) concern a different animal and are not used for a verdict."}
  ]}
```
