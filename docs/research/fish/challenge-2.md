# Challenge 2 — "The only retrieved adult Danio swimming speed is Ucrit = 0.548 m/s, a SUSTAINED speed, not a burst"

Adversarial review of a claim in `docs/research/fish/zebrafish-glide-physics.md`
(branch `origin/claude/zebrafish-glide-physics-j176og`, §3 and §5). I am not the author.

**Outcome: weakened.** The number survives and its attribution got stronger. Two parts of
the sentence fail. The word "sustained" is the wrong physiological class. The word "only" is
false by the author's own document. Neither failure changes the downstream verdict
(launch speed is the binding barrier). One small arithmetic slip in §5 is also noted.

---

## 1. Arithmetic, redone independently

These are calculations from the stated inputs, not observations (m = 0.4 g, g = 9.81 m/s²,
ρ_air = 1.2 kg/m³, AR 5, C_L 0.6, 1-BL span ⇒ S = 3.2 cm²):

| Quantity | My calculation | Author | Match |
|---|---|---|---|
| SL implied by 0.548 m/s ÷ 18.0 SL/s | 3.04 cm | (not stated) | consistent with a 3–4 cm adult |
| SL implied by 0.560 m/s ÷ 15.5 SL/s | 3.61 cm | 3.6 cm | yes |
| h_max = v²/2g at 0.548 m/s | 1.53 cm | 1.53 cm | yes |
| KE = ½mv² at 0.548 m/s | 0.060 mJ | 0.060 mJ | yes |
| Required glide V, 1-BL span | 5.84 m/s | 5.84 m/s | yes |
| Speed deficit, 5.84 ÷ **0.548** | **10.65×** | "10.4×" | **no** |
| KE deficit, (5.84 ÷ 0.548)² | **113×** | "109×" | **no** |
| 3-BL case, 1.95 ÷ 0.548 | 3.56× speed, 12.7× KE | 3.5×, 12× | rounding only |

**Finding (calc):** §5 says "Ucrit, **0.548 m/s**. That is a **10.4×** speed deficit and a
**109×** kinetic-energy deficit." But 10.4× and 109× come from the *secondary* Plaut value of
0.560 m/s (5.84/0.560 = 10.42; squared = 108.6). Against the 0.548 value named in the same
sentence, the figures are 10.65× and 113×. The error is about 2–4%. It points the
conservative way (it understates the deficit), and it changes no conclusion. It is still a
defect, because two different inputs are mixed in one sentence.

## 2. Is the input the right quantity?

**The value itself: confirmed, and the attribution got stronger.** The author recorded S7 as
`search-summary` and the Palstra et al. 2010 attribution as `remembered`. My search returned
the abstract text for Palstra, A.P. et al. (2010) "Establishing zebrafish as a novel exercise
model: swimming economy, swimming-enhanced growth and muscle growth marker gene expression",
*PLoS ONE* 5(12): e14483 (DOAJ record; ZFIN ZDB-PUB-110119-10). The abstract quotes "a
critical swimming speed (U(crit)) of 0.548±0.007 m s(-1) or 18.0 standard body lengths (BL)
s(-1)". **Read-level: search-summary** of the abstract. Full text was **could-not-access**:
`scholarlypublications.universiteitleiden.nl` is blocked by this session's network policy.
So the attribution moves from `remembered` to `search-summary (abstract quoted)`.

**The label "SUSTAINED": wrong class.** The standard three-way split of fish swimming
(attributed to Beamish 1978 in secondary sources; I did not read Beamish) is:

- **sustained**: more than about 200 min, aerobic, red muscle;
- **prolonged**: about 20 s to 200 min, ends in fatigue;
- **burst**: less than about 20 s, white muscle, anaerobic.

Ucrit, introduced by Brett, is the standard measure of **prolonged** performance. Two sources
(both search-summary) say that its final velocity steps run on aerobic and anaerobic
metabolism together. One of them, a 2015 gilthead sea bream study, *Frontiers in Physiology*
doi:10.3389/fphys.2015.00043, reports a plateau in O₂ uptake. Near fatigue, those fish
switched to white-muscle **burst-and-coast** swimming. That is evidence from another species;
I found no zebrafish-specific statement either way.

My inference: Ucrit is a prolonged speed with a burst component at its top, not a sustained
one. Palstra's own data show the difference. Their optimal (most economical) speed,
0.396 ± 0.019 m/s = 72% of Ucrit, is the better candidate for a "sustained" adult speed
(search-summary of the same abstract).

The author's argument still holds in direction. Ucrit is not a burst speed, and a true
single-tail-beat fast-start peak should exceed it. "Not a burst" survives. "Sustained" does
not.

**Proxy substitution, named.** The design question in §3 needs the *peak exit speed* of a
fast start, a burst lasting under about 0.1 s. Ucrit is a stand-in for that, and the author
says so in §3 and §5 ("the denominator is Ucrit, a sustained speed"). This stand-in is
disclosed, not hidden. The correct quantity is the peak centre-of-mass velocity of an adult
C-start.

**Does the correct quantity exist? Yes. Was it retrieved? No.**
Danos, N. & Lauder, G.V. (2012) "Challenging zebrafish escape responses by increasing water
viscosity", *J. Exp. Biol.* 215(11): 1854–1862, doi:10.1242/jeb.068957. Per the search-summary
of the abstract and record, it filmed zebrafish escapes at 1000 fps. Its fish had a mean
total length of 33.0 ± 1.3 mm, which is adult-sized. It reports the maximum centre-of-mass
velocity in stage 1 at 1, 10 and 20 mPa·s. A 2025 *iScience* paper (PMC11930232, full text
read to 100k of 153k characters) says in its introduction that "the impacts of fluid viscosity
on adult zebrafish escape swims have been evaluated regarding kinematics", which supports
calling the Danos & Lauder fish adults.

**Numerical value: unknown.** What I tried:

- the Harvard DASH record and the Lauder-lab PDF (`dash.harvard.edu`, `sites.harvard.edu`), both blocked by network policy;
- the journals.biologists.com URL, which returned an unrelated article;
- two searches aimed at the 1 mPa·s value, which returned no number.

So the author's "Adult fast-start peak speed: **unknown** … found no measured adult value"
holds as a *retrieval* statement. As a statement about the literature it is false: the
measurement exists and is cited by name above. Anyone who can open the PDF should take
Table 1 or the stage-1 velocity figure. That is the single most valuable number for §3.

**A trap I hit and am reporting so nobody else falls in.** One search-summary offered "maximum
velocity 0.71 ± 0.03 m/s, acceleration 17.1 ± 1.4 m/s², N = 7" as an adult zebrafish escape
value. Tracing the exact string showed it comes from "Muscle power output during escape
responses in an Antarctic fish", *J. Exp. Biol.* 200(4): 703. It is **not zebrafish** and must
not be used as such. The same abstract calls 0.71 m/s "the lower end of the range reported
for temperate-zone fish". That is weak, qualitative evidence, from other species, that
small-fish burst speeds sit near or above 0.7 m/s, not near 5.8 m/s.

## 3. "The only retrieved" — false by the author's own document

The author's own §3 retrieved at least three adult zebrafish swimming speeds:

1. Ucrit 0.548 m/s (Palstra 2010, as above);
2. Ucrit 0.560 ± 0.048 m/s = 15.5 SL/s (Plaut 2000, via a secondary paper; Palstra's abstract
   also quotes Plaut at about 0.56 m/s, which independently supports S9 at search-summary level);
3. implicitly, the 18 BL/s "dystrophic-strain escape value" listed under "Not used". The
   only dystrophic zebrafish kinematics paper I could read (PMC12180146, full text to 100k of
   105k characters) uses **6–7 dpf larvae**, not adults, and gives no numeric peak speed in
   the text. So that value should not be counted as adult. The source of the 18 BL/s figure
   stays unidentified.

In addition, Palstra's Uopt 0.396 m/s is a measured adult swimming speed in the same abstract.
The accurate statement is: "the only retrieved adult *speeds* are prolonged-swimming
measurements (Ucrit about 0.55–0.56 m/s from two labs, and Uopt 0.40 m/s); no adult burst
speed was retrieved." Two labs agreeing within about 2% on Ucrit is a real strength that the
word "only" hides. The two labs **disagree in SL/s**, 18.0 versus 15.5, because their fish
differed in length (3.0 versus 3.6 cm). I keep both values and do not average them.

## 4. Hidden assumptions, relaxed

- **Ucrit as the denominator.** If the true adult burst peak were, for example, 2× or 3× Ucrit
  (a hypothetical, not a number from any source), the 1-BL case would still need 5.84 m/s.
  That is a 5.3× or 3.6× speed shortfall. The verdict "launch speed is the hardest barrier"
  is robust to any burst speed below about 5.8 m/s, as the author already states. Relaxing
  the assumption weakens the *size* of the deficit, not its existence.
- **Equipment dependence of Ucrit** (S10). This changes Ucrit by an amount that is unknown
  here. It cannot plausibly move a 10× gap.
- **Temperature.** Plaut used 28 °C. Palstra's test temperature was not retrieved (unknown).
  Burst muscle power depends on temperature, so a burst value measured at a lower temperature
  would underestimate it. This is unquantified.

## 5. Evidence level

The claim is recorded as `literature`. Split it:

| Part | Honest level |
|---|---|
| 0.548 ± 0.007 m/s, 18.0 SL/s | literature, read-level **search-summary (abstract quoted)**; full text could-not-access |
| "Ucrit is not a burst" | literature (Ucrit definition, secondary sources, search-summary) |
| "Ucrit is SUSTAINED" | **author's interpretation, contradicted** by the standard sustained/prolonged/burst classification |
| "the only retrieved adult speed" | **false** against the author's own S9 and Palstra's Uopt |
| "no adult burst value exists" (implied in §3) | retrieval gap only; Danos & Lauder 2012 measured it (value unknown to me) |

## 6. Scope of negative searches

- Six web searches (standard and extended) on adult zebrafish fast-start or C-start peak
  velocity, the Danos & Lauder values, and Ucrit classification.
- Four fetch attempts:
  - blocked: dash.harvard.edu, sites.harvard.edu, the Leiden repository;
  - wrong page: the journals.biologists.com URL;
  - read: two PMC full texts (PMC11930232, PMC12180146), each to 100k characters.
- Not searched: Google Scholar, Web of Science, theses, Dryad datasets.

## 7. Recommended correction to the source document

Replace the claim with: "Adult zebrafish Ucrit is 0.548 ± 0.007 m/s (18.0 SL/s; Palstra et al.
2010) and about 0.56 m/s (15.5 SL/s; Plaut 2000, secondary). Ucrit is a **prolonged**
(minutes-long, partly anaerobic at the top) speed, not a sustained or burst speed. An adult
burst value has been measured (Danos & Lauder 2012, TL 33 mm, 1000 fps) but was not retrieved
(unknown)." In §5, recompute the deficit against 0.548 m/s: **10.65×** in speed and **113×**
in KE. Alternatively, keep 10.4× and 109× but name 0.560 m/s as their basis.

## Sources

| # | Source | Read-level | Used for |
|---|---|---|---|
| C1 | Palstra et al. 2010, *PLoS ONE* 5(12): e14483 (DOAJ; ZFIN ZDB-PUB-110119-10) | search-summary (abstract quoted); full text could-not-access | Ucrit 0.548, Uopt 0.396, Plaut ≈ 0.56 |
| C2 | Danos & Lauder 2012, *J. Exp. Biol.* 215: 1854, doi:10.1242/jeb.068957 | search-summary; PDF could-not-access | an adult burst measurement exists, TL 33 mm |
| C3 | Ravel et al. 2025, *iScience*, PMC11930232 | full-text (first 100k of 153k chars) | the 1–20 mPa·s viscosity range was used in adult kinematics work; no numbers |
| C4 | Dystrophic zebrafish kinematics, PMC12180146 | full-text (first 100k of 105k chars) | larval 6–7 dpf, not adult |
| C5 | Antarctic fish escape muscle power, *J. Exp. Biol.* 200(4): 703 | search-summary | 0.71 m/s is **not zebrafish** (misattribution trap) |
| C6 | Gilthead sea bream Ucrit study, *Front. Physiol.* 2015, doi:10.3389/fphys.2015.00043 | search-summary | burst-and-coast and anaerobic recruitment near Ucrit (other species) |
| C7 | Secondary sources on the Beamish/Brett classification (e.g. Archimer/Ifremer PDF, 2026 *J. Appl. Ichthyol.* review) | search-summary | sustained/prolonged/burst definitions; Ucrit = prolonged |

```swarm-challenge
{"claim_id": 2, "outcome": "weakened", "reason": "The 0.548 m/s Ucrit value is confirmed (Palstra et al. 2010 abstract) and is correctly not a burst speed, but Ucrit is a prolonged (partly anaerobic) speed rather than a sustained one, it is not the only adult speed retrieved (Plaut 0.560 m/s, Uopt 0.396 m/s), an adult burst measurement exists in Danos & Lauder 2012 though its value was not retrieved, and the 10.4x/109x deficits quoted beside 0.548 were computed from 0.560 (against 0.548 they are 10.65x/113x).", "corrected_value": "0.548 ± 0.007 m/s (Ucrit, prolonged-swimming class, 18.0 SL/s); deficit vs 5.84 m/s = 10.65x speed, 113x KE"}
```
