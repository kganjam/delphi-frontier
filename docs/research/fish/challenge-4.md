# Challenge 4: "Adult zebrafish fast-start peak velocity is unknown; no retrieved fish measurement of any species approaches 5.8 m/s"

**Claim under review.** This claim comes from `docs/research/fish/zebrafish-glide-physics.md`
(branch `claude/zebrafish-glide-physics-j176og`), §3 and §5. The recorded evidence level is
`unknown` and the recorded value is n/a. I did not write the claim.

**Verdict: WEAKENED.** Both halves are worded more strongly than the evidence allows. The
conclusion they support still stands: the launch-speed barrier is real, and by this review's
numbers it is larger than the source report's 10.4× speed gap and 109× energy gap.

**Network limits in this session.** Web search worked. Fetches to int-res.com and
pearl.plymouth.ac.uk were blocked by the session network policy (`ENOTFOUND`). Every new
literature value below is therefore read at `search-summary` level, unless it is marked as coming
from the repository's own S21 report.

---

## 1. Independent arithmetic

I recomputed everything below from the stated inputs. I did not reuse the author's working.

- **Weight:** W = 4.0e-4 kg × 9.81 m/s² = 3.924e-3 N.
- **Wing area:** a 1-BL span wing at AR 5 has S = b²/AR = 0.04² / 5 = 3.2e-4 m².
- **Required glide speed:** V = √(2W / (ρ·S·C_L)) = √(7.848e-3 / (1.2 × 3.2e-4 × 0.6)) =
  √34.06 = **5.84 m/s** (calc). This matches the author's figure.
- **In body lengths:** 5.84 / 0.04 = **146 BL/s** (calc). The author wrote "~146 BL/s", which
  agrees.

So the 5.8 m/s threshold is reproduced. It is a *derived* number: it depends on the assumed
C_L = 0.6, AR = 5, 1-BL span and ρ = 1.2. It is not a measurement.

## 2. First half: "adult zebrafish fast-start peak velocity is unknown"

The author searched three times and reports no adult value. Their scope did not include the study
below.

**Danos, N. & Lauder, G.V. (2012)**, *J. Exp. Biol.* 215:1854–1862, doi:10.1242/jeb.068957.

- The fish were adults, 33.0 ± 1.3 mm total length, filmed at 1000 fps.
- The paper reports a **measured** mean maximum Reynolds number of 27,800 ± 2,140 (s.e.m.) in
  1 mPa·s water. The authors computed it from fish length and the maximum linear velocity in each
  sequence.
- Read-level: full-text HTML, as reported by the repository's sibling report
  `docs/research/fish/S21-behaviour.md` (branch `claude/zebrafish-fast-start-velocity-pxsv7e`).
- I could not re-open it myself. My own search found the paper, and its summary confirms that
  viscosity reduced the centre-of-mass maximum velocity. The search did **not** surface the
  27,800 figure, so for me that number is second-hand.

**Inverting Re = U·L/ν** with ν = 1.0e-6 m²/s and L = 0.033 m (assumptions inherited from S21,
recomputed here) gives:

| Re | U (m/s, calc) | TL/s (calc) |
|---|---|---|
| 25,660 (−1 s.e.m.) | 0.78 | 23.6 |
| 27,800 (mean) | **0.84** | 25.5 |
| 29,940 (+1 s.e.m.) | 0.91 | 27.5 |

**This is a calculation from a measured quantity, not an observed velocity.** It is a mean of
per-sequence peaks, not the single fastest event. If the authors used a different length, it
shifts: with L = 0.030 m it is about 0.93 m/s.

**Defect (evidence level).** `unknown` is honest only in the narrow sense that no paper *prints*
an adult peak speed in m/s that either author could read. As a statement of what is known, it
understates the evidence. A ≥1000 fps adult measurement exists, and it pins the order of
magnitude at about 0.8–0.9 m/s. The right label is something like *derived from a measured Re,
≈0.84 m/s (0.78–0.93), Table 1 not read*, not `unknown`.

**Effect on the source report's verdict (my inference).** The verdict divides by Ucrit
(0.548 m/s). Replace that with the derived peak of 0.84 m/s:

- **1-BL case:** 5.84 / 0.84 = **6.9× in speed** and 48× in kinetic energy (calc), against the
  report's 10.4× and 109×.
- **3-BL case:** this needs 1.95 m/s. Since 1.95 / 0.84 = 2.3×, it is still out of reach.

So the gap shrinks by about half in energy, but nothing flips.

## 3. Second half: "no retrieved fish measurement of any species approaches 5.8 m/s"

As a statement about the author's *own retrievals*, this is true. As a statement about the
literature, it is false, and the report's §5 wording ("No fish number I retrieved, from any
species, approaches that") invites the second reading.

**Counter-examples I retrieved** (all `search-summary`; full text could not be accessed):

- **Sailfish, *Istiophorus platypterus*.** Marras et al. (2015), *Integr. Comp. Biol.*
  55(4):719, "Not so fast". Per the search summary, sailfish burst at about **7 m/s** and do not
  exceed **10 m/s** during predator–prey interactions. These were estimated from high-speed video
  of tail-beat frequency plus accelerometry. The summary does not show an instantaneous
  displacement-based velocity.
  - A blog quotes 8.19–9.77 m/s. That figure is unverified, so I do not use it.
  - **This exceeds 5.8 m/s.**
- **Flying fish, *Cypselurus heterurus doederleini*.** Makiguchi et al. (2013), *Aquat. Biol.*
  18:105–111. Accelerometer loggers estimate leap speed at the water surface as **3.9–5.2 m/s**.
  - This is **water-exit speed**, which is exactly the quantity the barrier argument needs.
  - It reaches 67–89% of 5.8 m/s. Most readers would say that "approaches" 5.8.
  - It was retrieved in the very taxon (Exocoetidae) that the source report used as its
    comparison premise.
- **Juvenile flying fish, 1–5 cm.** An SICB / APS-DFD abstract by Yang et al. reports launch
  accelerations of about 5 g and gliding speeds of about 1.3 m/s. This is a conference abstract
  (`search-summary`) and preliminary.
- **Simulation, not observed.** A bioRxiv CFD preprint (Deng et al.) has a 0.25 m flying fish
  taxiing to 16.5 m/s at 350 W. It is excluded as evidence. I list it only so that nobody
  mistakes it for a measurement.

**Disagreement preserved.** The sailfish figure in the paper's own abstract (≈7 m/s burst, ≤10 m/s
maximum) and the blog's 8.19–9.77 m/s do not match. I report both and adopt neither as a point
value.

## 4. Proxy check: m/s across species is the wrong metric

The claim compares absolute speed across species. Fast-start speed scales with body size, so a
2-metre sailfish reaching 7 m/s says nothing about a 4 cm fish. The quantity that matters is
**size-specific speed at water exit: about 146 BL/s at 4 cm** (calc).

- **Sailfish:** at 7 m/s, the speed is a few BL/s. Body length was not retrieved. I *remember*
  adults as roughly 2 m (`remembered`), which gives about 3.5 BL/s.
- **Flying fish leap:** 3.9–5.2 m/s. Body length was not retrieved in my search summary, so I
  cannot convert it to BL/s. That is `unknown`.
- **Juvenile flying fish, 1–5 cm:** their glide speed of about 1.3 m/s is far below 5.8 m/s.
- **Zebrafish:** the derived adult peak is about 25 TL/s.
- **Larval and other fast-starts:** the highest values retrieved in this repository are
  ">50 BL/s" (larval zebrafish, conference abstract, `search-summary`, via S21) and >20 BL/s
  (archer fish, `search-summary`).

**Inference (mine).** Even granting 50 BL/s to an adult, the 1-BL case needs about 3× more speed
and about 9× more kinetic energy. On the correct metric, the author's conclusion is *stronger*
than their wording suggests. The fault is in how the claim is stated, not in the barrier.

## 5. The hidden assumption, relaxed

The claim assumes that **peak fast-start speed is the right stand-in for exit speed**. That
assumption fails in both directions:

- **The exit can be slower than the peak.** A C-start peak lasts only milliseconds, and it occurs
  in an arbitrary direction, usually horizontal. Exiting at a useful angle at that instant, while
  carrying a wing membrane in water, is undemonstrated. So the derived 0.84 m/s is an upper-ish
  bound on exit speed, not a typical value.
- **The exit can be faster than a single start.** Flying fish use surface taxiing, with the tail
  still in the water, to keep accelerating after the start. Makiguchi's 3.9–5.2 m/s exit speed is
  the evidence that this regime exists. The source report already lists taxiing as a design
  change, so the claim is not blind to it. But calling the speed "unknown" hides that, in the
  only taxon that actually does this, exit speeds within 11–33% of the threshold have been
  measured.

Relaxing the assumption does not close the zebrafish gap: no small-fish taxiing data were
retrieved. It does make the absolute-speed half of the claim untenable.

## 6. What I searched (scope of negative results)

- **Searches:** three standard web searches, on sailfish burst speed (Marras 2015), flying-fish
  take-off/exit speed, and the Danos & Lauder 2012 Reynolds-number figure.
- **Sibling report:** I read `S21-behaviour.md` from the repository.
- **Fetch attempts:** int-res.com and pearl.plymouth.ac.uk were both blocked by network policy.
- **Not searched:** wahoo, tuna, barracuda or other pelagic burst records; Chinese-language
  literature; theses; figure digitisation of Danos & Lauder Table 1 or Condon et al. 2010 Fig. 1.
- **Not found:** an adult zebrafish peak in m/s *printed* in a paper. I did not find one, and
  S21 did not either.

## 7. Sources

| Source | Read-level | Used for |
|---|---|---|
| `zebrafish-glide-physics.md` (branch `claude/zebrafish-glide-physics-j176og`) | full-text (repo) | claim under review |
| `S21-behaviour.md` (branch `claude/zebrafish-fast-start-velocity-pxsv7e`) | full-text (repo) | Danos & Lauder Re, second-hand |
| Danos & Lauder 2012, *J. Exp. Biol.* 215:1854, doi:10.1242/jeb.068957 | search-summary (me); full-text HTML per S21 | adult ≥1000 fps escape; max Re 27,800 |
| Marras et al. 2015, *Integr. Comp. Biol.* 55:719 ([OUP PDF](https://academic.oup.com/icb/article-pdf/55/4/719/1774345/icv017.pdf); [Plymouth record](https://pearl.plymouth.ac.uk/handle/10026.1/11448), could-not-access) | search-summary | sailfish ≈7 m/s burst, ≤10 m/s |
| Makiguchi et al. 2013, *Aquat. Biol.* 18:105 ([abstract page](https://int-res.com/abstracts/ab/v18/n2/p105-111), could-not-access) | search-summary | flying-fish leap 3.9–5.2 m/s |
| Yang et al., SICB / APS-DFD 2013 abstract ([APS](https://archive.aps.org/dfd/2013/g18/1)) | search-summary | juvenile flying fish, 5 g, ~1.3 m/s glide |
| Deng et al., bioRxiv ([node 903826](https://www.biorxiv.org/node/903826)) | search-summary | **simulated** taxiing 16.5 m/s, excluded as evidence |
| [marine-bio-images blog](https://www.marine-bio-images.com/blog/?p=455) | search-summary | 8.19–9.77 m/s sailfish, unverified, not used |

```swarm-challenge
{"claim_id": 4, "outcome": "weakened", "reason": "Adult zebrafish peak is not unknown but bounded by a measured 1000-fps Re (Danos & Lauder 2012) implying a derived ~0.84 m/s, and fish of other species do reach or approach 5.8 m/s in absolute terms (sailfish ~7 m/s burst; flying-fish water exit 3.9-5.2 m/s), though on the correct size-scaled metric (~146 BL/s) none comes close, so the launch barrier itself survives.", "corrected_value": "~0.84 m/s (0.78-0.93 m/s, ~25 TL/s) for adult zebrafish mean peak escape speed, derived from measured max Re 27,800 at 33 mm TL, not directly observed"}
```
