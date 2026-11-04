# Claim 37: entailment to the organism and ecology scales, and checks against the literature

**Source claim** (S24, `docs/research/fish/S24-behaviour.md` §3.2, branch
`claude/s24-surface-taxiing-launch-tsepbn`; behaviour scale; recorded evidence: **derived**):

> At sustainable tail-beat frequencies the calculated taxi ceiling is ~0.56 m/s, which is Ucrit
> itself -- so taxiing adds essentially nothing to the launch.

**The calculation behind it** (S24, calculated, not observed): U_max = f·A/St, with
- f = 21 Hz, the maximum voluntary EMG frequency in intact adult *D. rerio*;
- A = 0.20 × 40 mm = 8 mm, the peak-to-peak tail amplitude;
- St = 0.3, the cruising Strouhal number.

**What has already been said about it.**
- Challenge-37 (`claude/challenge-37-taxi-ceiling-ymvxah`) rated the claim **weakened**:
  - the arithmetic is right;
  - but "= Ucrit" holds by construction, because A was calibrated so that 21 Hz × A / 0.3 = Ucrit;
  - and the conclusion depends on assuming a taxiing tail keeps the Strouhal number of a submerged swimmer.
- Replicate-37 (`claude/replicate-37-taxi-ceiling-kybegi`) **agreed**, getting 0.50–0.59 m/s for a 36–40 mm fish. It found:
  - the 21 Hz figure was measured in **18–30 mm** fish, not 40 mm fish;
  - the kinematic model has no term for the free surface.

I do not repeat either. This document asks a different question: **if the claim is true, what has to be
true one scale down (organism) and one scale up (ecology), and is it?**

**Subject on the claim side, throughout: adult zebrafish, *Danio rerio*.** Every verdict below names the
animal or object each number comes from.

---

## 1. Constraints entailed

For "taxi ceiling at sustainable frequency ≈ Ucrit, so taxiing adds nothing" to be true:

| # | Scale | Kind | Requirement (generic) |
|---|---|---|---|
| C1 | organism | range | The submerged steady-swimming Strouhal number of the adult must lie in the cruise band the calculation assumes: **St ∈ [0.2, 0.4]**. The tail amplitude needed to support it must be about 0.15–0.25 body length. |
| C2 | organism | range | The tail-beat frequency an adult uses at its own Ucrit must be about the "sustainable" ceiling used in the claim: **f(Ucrit) ∈ [17, 25] Hz**. That is ±20 % around 21 Hz, which keeps fA/St within roughly ±20 % of Ucrit. |
| C3 | organism | range | A tail beating while the body is partly out of the water must stop producing net thrust at a Strouhal number no lower than the submerged one. Otherwise the same 21 Hz drives a higher speed. To keep the ceiling ≤ 1.2 × Ucrit (0.66 m/s) at 21 Hz and A = 8 mm, the zero-net-thrust Strouhal number must satisfy **St₀ ≥ 0.255**. |
| C4 | organism | timescale | Tail-beat frequencies above the sustainable ceiling (>21 Hz) can be held only for times short compared with a taxi. S24 calculates a taxi lasts 0.22–0.89 s. So any >21 Hz bout must be **≤ ~0.2 s**. If it could be held longer, "at sustainable frequencies" would be the wrong limit for a sub-second manoeuvre. |
| C5 | ecology | existence | Free-living *Danio* must have **no** surface-locomotion mode (body partly emerged, tail still in the water) that carries them faster than their submerged prolonged-swimming speed. |

**Why the scales split this way.**
- C1–C4 are the organism-level properties the calculation silently relies on: kinematics, the thrust law, and frequency endurance.
- C5 is what the claim predicts about behaviour in the field.

**No `conservation` or `energetic` constraint.** The claim is a kinematic ceiling, and forces and power do not enter it. S24 §3.3 itself argues that force is not the limit.

---

## 2. Checks

### C1. Submerged steady Strouhal number in [0.2, 0.4]. **SATISFIED** (measured, same species)

**Measured, adult *D. rerio*.** Source: Mwaffo, Zhang, Romero Cruz & Porfiri 2017, *PeerJ* 5:e4041, PMC5691796. Read-level: **full-text** (first 100,000 of 103,247 characters, via PMC; peerj.com is blocked by this session's network policy).
- **Fish:** wild-type, body length 3.4 ± 0.2 cm, n = 12, in a swim tunnel at 26, 39 and 52 mm/s.
- **Authors' result:** "The Strouhal number St was 0.366 ± 0.026 when cruising, compared to St = 0.515 ± 0.035 during bursting."
- **How St was computed:** St = fA/V, with V the fish's speed relative to the flow.

**Measured, adult *D. rerio*, at higher speeds.** Source: Jahn & Seebacher 2026, *J. Exp. Biol.* 229:jeb252605, PMC13405219.
- **Read-level:** full-text via Europe PMC XML. Fig. 1 and Fig. 2 were viewed as images from the Europe PMC supplementary bundle. The values below were **read off the figures by me** and are approximate, ±~0.3 Hz and ±~0.01 BL.
- **Fish:** commercial-supplier adults, SL 3.14–3.30 cm, N = 16–17 per treatment. They were filmed at 120 fps at 0.16 and 0.28 m/s during Ucrit trials.
- **Tail amplitude (TBA, control fish):** ≈ 0.20–0.22 BL at both speeds. TBA is defined as "the maximal displacement of the tail at the peduncle during a single tail beat cycle".
- **Tail-beat frequency (TBF, control fish):**
  - ≈ 9.5 Hz (24 °C) and 9.9 Hz (30 °C) at 0.16 m/s;
  - ≈ 13.1 Hz and 13.6 Hz at 0.28 m/s.
- **Speed effect:** speed had a strong effect on TBF (η² = 0.77, Table S2, read in full).

**Calculated by me from the Jahn values,** taking TBA as peak-to-peak and A = TBA × SL:
- **St ≈ 0.40–0.43** at 0.16 m/s;
- **St ≈ 0.33–0.34** at 0.28 m/s.

**The definition is ambiguous, and the result depends on it.**
- "Maximal displacement" could mean single-sided amplitude. In that case St doubles, to about 0.66–0.85, which is outside the band.
- The paper measures at the peduncle, not the fin tip. Fin-tip amplitude is larger, which would raise St further.
- I therefore rest the verdict on Mwaffo, whose St is reported directly. Jahn is supporting evidence only under the peak-to-peak reading.

**Amplitude.**
- The claim's 0.20 TL is fin-tip, total-length based.
- Jahn's ≈ 0.21 SL is peduncle, standard-length based.
- Converting with an *assumed* SL/TL ≈ 0.83 gives ≈ 0.17 TL at the peduncle. That is inside 0.15–0.25.

**Verdict and scope.**
- C1 is **satisfied** for steady submerged swimming at **≤ 0.28 m/s** (≈ 8.5 BL/s), on measured same-species data.
- It is **not** measured near 0.55 m/s.
- The *burst* St (0.515, Mwaffo) lies **above** the band. My inference: if adults move towards burst kinematics at high effort, fA/St falls. That lowers the ceiling, so it does not threaten the claim.

### C2. Tail-beat frequency at Ucrit in [17, 25] Hz. **OPEN** (no measurement at Ucrit; two extrapolations disagree)

**Searched:**
- Europe PMC: `(zebrafish OR "Danio rerio") AND ("tail beat frequency" OR "tail-beat frequency" OR "tailbeat frequency") AND adult`. 99 hits; titles of the first 40 screened; 3 full texts read (PMC13405219, PMC8634626, PMC12011485).
- WebSearch: 3 queries (standard and extended) on adult zebrafish tail-beat frequency against speed, near Ucrit, and in body lengths per second.

**No paper reports adult *D. rerio* tail-beat frequency at or near Ucrit.** The fastest measured speed I found is 0.28 m/s (Jahn & Seebacher 2026).

**Extrapolation A (calculated by me, linear, from measured Jahn control means).**
- Slope: 30.0–30.8 Hz per m/s, which is ≈ 1.0 Hz per BL/s.
- At Palstra's Ucrit of 0.548 m/s this gives **f ≈ 21.1–21.9 Hz**. That falls on the claim's 21 Hz.
- Jahn's own control Ucrit, read off Fig. 1E × SL (calculated), is **≈ 0.40 m/s at 24 °C and 0.43 m/s at 30 °C**. At those speeds the extrapolation gives **f ≈ 16.6–18.3 Hz**.
- The extrapolation runs from 0.28 m/s out to 0.40–0.55 m/s, which is 1.4–2.0× beyond the data. Fish often change gait near Ucrit (burst-and-coast), and a linear fit cannot see that.

**Extrapolation B (calculated by me from a search-summary relation).** Source: Han, Lombardelli, Peterson & Porfiri 2024, *J. Fish Biol.* 105, doi:10.1111/jfb.15922. Read-level: **abstract** via Europe PMC. The publisher page returned HTTP 403.
- **The abstract confirms:** adult-sized *D. rerio*, flow 0.8–3.2 BL/s, tail-beat motion extracted from video.
- **Known only at search-summary level:** a regression TBF ≈ 3.09 + 1.71·U (U in BL/s), and 8.43 Hz at 2.8 BL/s for a ~3.5 cm fish.
- Taken at face value, this gives ≈ **33.9 Hz at 18 BL/s** (Palstra's Ucrit) and ≈ **23.6–26.2 Hz at 12–13.5 BL/s**. That is a 4–6× extrapolation beyond its data.

**The two disagree, and I preserve that.**
- The Han slope (1.71 Hz per BL/s) is about 1.7× the Jahn slope (~1.0).
- The Han frequency at 2.8 BL/s (8.43 Hz) is also high compared with Jahn at 4.9 BL/s (~9.5–9.9 Hz).
- Possible causes I cannot test: protocol, fish size, temperature, schooling versus single fish. The Han numbers are search-summary only.

**Ucrit disagreement, carried forward unchanged.**
- Palstra 2010: 0.548 m/s (as relayed in S24).
- Jahn 2026: ≈ 0.40–0.43 m/s (my figure reading).
- Wakamatsu 2019: 0.19–0.28 m/s (as relayed in S24).

**Verdict.**
- The extrapolation from the stronger, full-text source (Jahn) is consistent with C2.
- The search-summary source (Han) would put f(Ucrit) above 25 Hz.
- Neither is a measurement at Ucrit, so C2 is **open**.
- **What would close it:** tail-beat frequency filmed at the final completed step of an adult Ucrit test. Jahn & Seebacher already film during Ucrit trials, so this is a small extension of an existing protocol.

**Related size check (replicate-37's point), same species.**
- The 21 Hz figure comes from 18–30 mm fish: Kyriakatos et al. 2011, PMC6623330, Methods. Read-level: **full-text** via WebFetch, first 100k of 101k characters.
- Jahn's fish (SL 3.1–3.3 cm) are about the claim's 40 mm TL, assuming SL/TL ≈ 0.83. Their extrapolation still lands at ~21 Hz.
- So the size mismatch does not, on this evidence, move f(Ucrit) far. That is an inference on calculated values.

### C3. Zero-net-thrust Strouhal number of a partly emerged tail ≥ 0.255. **UNSATISFIED**: nobody has measured it in any *Danio*

**Searched:**
- Inherited scope: S24 §2.4 searched for adult zebrafish caudal thrust and found none (web, extended, and Europe PMC). Challenge-37 §3 makes the same point.
- My additions: the Europe PMC tail-beat query above, and the jump/surface WebSearch below (C5).
- **Not searched:** Google Scholar, Web of Science, theses.

**Result:** no measurement of thrust against speed, or of the zero-thrust St, for a zebrafish caudal fin in any condition, submerged or emerged. This is **"nobody appears to have looked"**, not "looked and found nothing".

**Nearest evidence, all for the wrong subject, so none of it refutes anything.**

1. **Rigid 2-D pitching foil, not a fish.** Floryan, Van Buren, Rowley & Smits 2017, *J. Fluid Mech.*, relayed via S32-organism (`claude/s32-multi-stroke-launch-qpq9g2`), where it is recorded as read **full-text** (arXiv v1). I did not re-read it. Read-level for me: **relayed**.
   - **Measured on the foil:** C_T = 2.55 St² − 0.08, at Re 4,780–9,560.
   - **Calculated by me from that law:** C_T = 0 at **St₀ = √(0.08/2.55) = 0.177**. That is below 0.255.
   - **What it would mean (calculated):** at 21 Hz and A = 8 mm, U = 0.168 / 0.177 = **0.95 m/s = 1.73 × Ucrit**.
   - **This is the project's own model (S32), not an observation.** S32's ceiling formula U_max = f·A·√(c₆/C_D) is exactly this St₀, and C_D depends on Reynolds number in S32. A partly emerged zebrafish lobe is not a 2-D rigid foil: S32 itself lists yaw recoil in air as reducing the effective amplitude.
   - **So the project's simulated taxi physics disagrees with claim 37's 0.56 m/s.** It does so through St₀ = 0.18 rather than 0.3. Both are model outputs. **Neither is a measurement on a zebrafish.**
2. **Flying fish (Exocoetidae), simulated.** Deng, Wang, Zhang & Mao 2019, bioRxiv 10.1101/765560. Read-level: **abstract**, as quoted in S24 and challenge-37.
   - Taxiing at 10 m/s needs 50 Hz; submerged cruising at the same speed needs 145 Hz.
   - **This is the wrong animal and a simulation.** S32 states that its equations reproduce the exocoetid taxi to 15–20 m/s and fail for the zebrafish only through Reynolds-dependent lobe drag. An exocoetid number is therefore something the project's model *reproduces*. It is not a refutation of a zebrafish claim, and I do not use it as one.

**Verdict.** C3 is the load-bearing constraint, the one challenge-37 identified. It is **unsatisfied**: no zebrafish measurement exists, and the only quantitative proxies are a rigid foil and a simulated flying fish. Both point to St₀ below 0.255, but neither concerns the same animal.

### C4. >21 Hz bouts held for ≤ ~0.2 s. **OPEN** (measured behaviour consistent; capacity untested; margin < 2×)

**Measured, adult *D. rerio*, 18–30 mm, n = 8, EMG, free-swimming in a 0.35 × 0.25 × 0.25 m aquarium; temperature not stated.** Source: Kyriakatos et al. 2011, PMC6623330. Read-level: **full-text** via WebFetch, first 100,000 of 101,006 characters.
- Swimming frequencies "ranged from 2 to 21 Hz … but never exceeding 21 Hz (n = 8)".
- Escape: "the maximal frequency reached during escape was 52 Hz". "We never observed motor activity during escape lower than 29 Hz".
- Escape sequences "consisted of a few, in general three to five, short cycles".
- "The small number of swimming cycles with frequencies between 21 and 30 Hz resulted from transitions from swimming to escape and vice versa."

**Calculated by me:** 3–5 cycles at 29–52 Hz last **0.06–0.17 s**. The paper gives no escape durations in seconds.

**Assessment.**
- In spontaneous behaviour, adults spend >21 Hz only in escapes of ≤ ~0.17 s. That is consistent with C4.
- **But this is what fish did, not what they can do.** Nothing in the paper forced a maximal sprint, and the tank was 35 cm long.
- The margin is thin. 0.17 s against the shortest S24 taxi time of 0.22 s is a factor of 1.3.
- Burst swimming in fish generally is described as lasting up to ~20 s before fatigue. That figure is a general statement, not about *Danio*: PMC11444792, search-summary.
- I found **no adult *D. rerio* measurement of how long a >21 Hz tail beat can be held**. Searched: one WebSearch on adult zebrafish burst duration, fatigue and sprint, plus the Kyriakatos full text.

**Verdict:** **open**. Satisfied by the one same-species observation available, but not tested as a capacity.

### C5. No wild surface-locomotion mode faster than submerged prolonged speed. **UNSATISFIED**: nobody has looked

**Searched:**
- WebSearch: "zebrafish jumping out of water wild behaviour leap surface skittering Danio field observation".
- WebSearch: "zebrafish jump height out of water aquarium escape jumping adult Danio rerio cm measured".
- WebSearch: "wild zebrafish Danio rerio standard length field habitat Engeszer 2007 body size".

**Found:**
- **Field ethology is sparse.** An eLife review of zebrafish ecology (elifesciences.org/articles/05635; read-level **search-summary**) states that field observations of zebrafish behaviour are few and anecdotal.
- **Habitat.** Engeszer et al. 2007, *Zebrafish* 4:21, read-level **search-summary/abstract**, reports wild fish abundant in silt-bottomed, vegetated pools and rice paddies next to slow streams. Half of 28 sites had slow or no flow (secondary summary).
- **Field video.** Sundin et al. 2019 (bio.uib.no PDF, **listing only**, not read) filmed wild zebrafish underwater. The excerpt does not mention surface locomotion.
- **Jumping studies are all off-question.**
  - The SICB abstract on stranded *Danio* versus *Gambusia* (**search-summary**) concerns jumping **from land**.
  - Gibb et al. 2011, summarised by Practical Fishkeeping (**search-summary**), says *Danio* are "not known to voluntarily leave the water". That disagrees in emphasis with the SICB report of a greater propensity to jump when stranded. I preserve both.
  - **No measured jump height or surface-travel speed** for *D. rerio* from water was found.
- **Not searched:** Spence et al. 2008 *Biol. Rev.* (full text), Google Scholar, Web of Science, regional Indian ichthyology literature.

**Cross-species evidence, not used for the verdict.**
- **Guppy** (*Poecilia reticulata*; Soares & Bierman 2013, PMC3629028, full-text per S24): in-air peak 1.24 m/s against in-water peak 1.02 m/s.
- **Flying fish:** taxi measurements exist.
- **Both are the wrong animal.**

**Verdict:** **unsatisfied, scoped as "nobody has looked"**. No study of wild or lab *D. rerio* surface locomotion speed exists in what I searched. The absence of reports is not evidence that the mode is absent, because the field record is described as anecdotal.

---

## 3. Summary

| # | Scale | Kind | Status | Basis |
|---|---|---|---|---|
| C1 | organism | range: submerged St ∈ [0.2, 0.4] | **satisfied** | measured *D. rerio* St 0.366 ± 0.026 (Mwaffo 2017). Only up to 0.28 m/s. |
| C2 | organism | range: f(Ucrit) ∈ [17, 25] Hz | **open** | no measurement at Ucrit. Extrapolated (calculated) 21–22 Hz from Jahn 2026, full-text; ~34 Hz from Han 2024, search-summary. They disagree. |
| C3 | organism | range: taxi St₀ ≥ 0.255 | **unsatisfied** | nobody has measured it in *Danio*. Rigid-foil law (relayed) gives 0.177; the exocoetid result is simulated. Both are the wrong subject. |
| C4 | organism | timescale: >21 Hz bouts ≤ ~0.2 s | **open** | spontaneous escapes last 3–5 cycles, 0.06–0.17 s (calculated from measured *D. rerio*). Capacity untested. |
| C5 | ecology | existence: no wild surface mode faster than Ucrit | **unsatisfied** | nobody has looked; field record anecdotal |

**Nothing is unsatisfiable.** No measured value on adult *D. rerio* contradicts any constraint.
- The only numbers pointing against the claim come from a rigid foil and a simulated flying fish (C3), and from a search-summary regression extrapolated 4–6× (C2).
- These are the wrong subject, or not measurements, or both.

**My inference.**
- The claim's kinematic inputs hold up one scale down where they can be measured: C1 directly, and C2 by extrapolation.
- Its weak point remains C3: whether a partly emerged tail keeps a submerged Strouhal number. That is unmeasured for this animal.
- The project's own S32 physics implies it does not (St₀ ≈ 0.18, which gives ≈ 0.95 m/s at 21 Hz, calculated). So the project's models currently disagree with each other on this claim. No measurement decides between them.

**The measurements that would decide it**, both small:
1. Tail-beat frequency filmed at the last completed Ucrit step, which closes C2.
2. Tethered adult thrust against inflow speed, with the body emerged and the lower lobe immersed, which closes C3. Challenge-37 also names this one.

## 4. Sources and read-levels

| Source | Animal or object | Read-level |
|---|---|---|
| Mwaffo, Zhang, Romero Cruz & Porfiri 2017, *PeerJ* 5:e4041, PMC5691796 | adult *D. rerio* | full-text (100k of 103k characters) |
| Jahn & Seebacher 2026, *J. Exp. Biol.* 229:jeb252605, PMC13405219 | adult *D. rerio* | full-text and figures; values read off figures by me |
| Han, Lombardelli, Peterson & Porfiri 2024, *J. Fish Biol.* 105, doi:10.1111/jfb.15922 | adult-sized *D. rerio* | abstract; regression search-summary only; publisher returned 403 |
| Kyriakatos et al. 2011, *J. Neurosci.*, PMC6623330 | adult *D. rerio*, 18–30 mm | full-text (100k of 101k characters; Europe PMC XML failed, PMC page used) |
| Li, Liu, Müller, Voesenek & van Leeuwen 2021, *Proc. R. Soc. B* 288:20211601, PMC8634626 | CFD swimmers and larval zebrafish | full-text; context only (amplitude 0.14–0.17 L in carangiforms), not used for a verdict |
| Miller et al. 2025, *Curr. Zool.*, PMC12011485 | adult *D. rerio* Ucrit across strains | full-text; contains no tail-beat frequency; not used |
| Floryan, Van Buren, Rowley & Smits 2017, *J. Fluid Mech.* | rigid 2-D foil | relayed via S32-organism (S32 read full-text) |
| Deng, Wang, Zhang & Mao 2019, bioRxiv 765560 | flying fish, CFD | abstract, as relayed in S24 and challenge-37 |
| Palstra et al. 2010; Wakamatsu et al. 2019 | adult *D. rerio* Ucrit | relayed via S24 (search-summary and full-text respectively) |
| Engeszer et al. 2007, *Zebrafish* 4:21; eLife zebrafish-ecology review; Sundin et al. 2019 | wild *D. rerio* | search-summary; search-summary; listing |
| SICB stranded-jumping abstract; Gibb et al. 2011 via Practical Fishkeeping | *D. rerio* and *Gambusia*, on land | search-summary |
| Burst time-to-fatigue scaling, PMC11444792 | fishes generally | search-summary |
| peerj.com | — | could-not-access: host outside this session's network allow-list |

```swarm-entail
{"source_claim": 37, "source_scale": "behaviour",
  "constraints": [
    {"target_scale": "organism", "kind": "range",
      "statement": "The adult's submerged steady-swimming Strouhal number must lie in the cruise band the kinematic ceiling assumes, with a tail amplitude of order 0.15-0.25 body length to support it",
      "quantity": "submerged steady-swimming Strouhal number St = fA/U, adult Danio rerio", "lo": 0.2, "hi": 0.4, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Measured on adult D. rerio (3.4 +/- 0.2 cm, n=12): cruising St 0.366 +/- 0.026 (bursting 0.515 +/- 0.035, outside the band, which would lower not raise the ceiling). Supporting: Jahn & Seebacher 2026 control fish (SL 3.2-3.3 cm) peduncle TBA ~0.20-0.22 BL and TBF ~9.5-9.9 Hz at 0.16 m/s, ~13.1-13.6 Hz at 0.28 m/s (read off figures by me); St calculated 0.33-0.43 if TBA is peak-to-peak (0.66-0.85 if single-sided; definition ambiguous). Only measured at <=0.28 m/s, not near Ucrit",
      "satisfied_evidence": "measured",
      "note": "Mwaffo V, Zhang P, Romero Cruz S, Porfiri M 2017 PeerJ 5:e4041 PMC5691796, full-text (100k of 103k chars). Jahn M & Seebacher F 2026 J Exp Biol 229:jeb252605 PMC13405219, full-text + Fig 2 + Table S2 read. Same species on both sides (adult Danio rerio)."},
    {"target_scale": "organism", "kind": "range",
      "statement": "The tail-beat frequency the adult uses at its own critical swimming speed must be about the 'sustainable' ceiling the claim uses (21 Hz), within +/-20%",
      "quantity": "tail-beat frequency at Ucrit, adult Danio rerio", "lo": 17, "hi": 25, "units": "Hz",
      "status": "open",
      "satisfied_by": "No measurement at Ucrit found. Linear extrapolation (calculated by me) of measured Jahn & Seebacher 2026 control means (slope 30.0-30.8 Hz per m/s) gives 21.1-21.9 Hz at Palstra's 0.548 m/s and 16.6-18.3 Hz at Jahn's own control Ucrit (~0.40-0.43 m/s, read off Fig 1E x SL): consistent. Han et al. 2024 regression TBF ~3.09 + 1.71 U(BL/s) (search-summary only) extrapolated gives ~33.9 Hz at 18 BL/s and 23.6-26.2 Hz at 12-13.5 BL/s: inconsistent. Disagreement preserved; both are 1.4-6x extrapolations",
      "satisfied_evidence": "derived",
      "note": "Searched Europe PMC '(zebrafish OR \"Danio rerio\") AND (\"tail beat frequency\" OR \"tail-beat frequency\" OR \"tailbeat frequency\") AND adult' (99 hits, 40 titles screened, 3 full texts read) and 3 WebSearches; highest measured adult speed with TBF is 0.28 m/s. Jahn & Seebacher 2026 PMC13405219 full-text+figures; Han T, Lombardelli G, Peterson SD, Porfiri M 2024 J Fish Biol 105 doi 10.1111/jfb.15922 abstract (regression search-summary; publisher 403). 21 Hz itself: Kyriakatos 2011 PMC6623330 full-text, 18-30 mm fish. Ucrit disagreement carried: Palstra 0.548, Jahn ~0.40-0.43, Wakamatsu 0.19-0.28 m/s. All Danio rerio."},
    {"target_scale": "organism", "kind": "range",
      "statement": "A tail beating with the body partly emerged must stop producing net thrust at a Strouhal number no lower than the submerged cruise value; to keep the 21 Hz, 8 mm ceiling <= 1.2 x Ucrit the zero-net-thrust Strouhal number must be >= ~0.255",
      "quantity": "zero-net-thrust Strouhal number of a partly emerged caudal fin, adult Danio rerio", "lo": 0.255, "hi": null, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "No measurement of caudal thrust vs speed, or of the zero-thrust St, for any Danio caudal fin, emerged or submerged. Nearest proxies are other subjects and point the other way without refuting: rigid 2-D pitching foil (Floryan et al. 2017, measured on the foil, C_T = 2.55 St^2 - 0.08) gives St0 = 0.177 (calculated), i.e. 0.95 m/s = 1.73 x Ucrit at 21 Hz -- this is the project's own S32 model, so the project's simulated physics disagrees with claim 37; exocoetid CFD (Deng 2019, simulated) 50 Hz taxi vs 145 Hz submerged at 10 m/s, which S32 reproduces. Neither is a zebrafish measurement",
      "satisfied_evidence": "unknown",
      "note": "Scope: S24 section 2.4 searches for adult zebrafish caudal thrust (web extended, Europe PMC) found none; challenge-37 concurs; my Europe PMC tail-beat query and two surface/jump WebSearches added nothing. Not searched: Google Scholar, Web of Science, theses. 'Nobody appears to have looked', not 'looked and found nothing'. Floryan relayed via S32-organism (S32 read full-text arXiv v1). Deng 2019 bioRxiv 765560 abstract as relayed. Animal on each side: claim = adult Danio; proxies = rigid foil and flying fish, so not usable as refutation."},
    {"target_scale": "organism", "kind": "timescale",
      "statement": "Tail-beat frequencies above the sustainable ceiling must be held only briefly compared with a taxi (S24 calc 0.22-0.89 s), otherwise the sustainable frequency is the wrong limit for a sub-second manoeuvre",
      "quantity": "maximum duration of tail beating above 21 Hz, adult Danio rerio", "lo": null, "hi": 0.2, "units": "s",
      "status": "open",
      "satisfied_by": "Measured on adult D. rerio (18-30 mm, n=8, EMG, free swimming in a 35 cm aquarium): swimming never exceeded 21 Hz; escapes were >=29 Hz (max 52 Hz) and 'in general three to five, short cycles'; 21-30 Hz cycles occurred only in transitions. Calculated by me: 3-5 cycles at 29-52 Hz = 0.06-0.17 s, consistent with the bound but only 1.3x below the shortest taxi time. This is observed spontaneous behaviour, not a forced-capacity test; no measurement of how long an adult can hold >21 Hz was found",
      "satisfied_evidence": "measured",
      "note": "Kyriakatos A et al. 2011 J Neurosci PMC6623330, full-text (100k of 101k chars via WebFetch). Same species. Searched one WebSearch on adult zebrafish burst duration/fatigue/sprint; only general-fish statements found (burst Tf up to ~20 s, PMC11444792, search-summary, not Danio). Open because capacity, not behaviour, is what the claim needs."},
    {"target_scale": "ecology", "kind": "existence",
      "statement": "Free-living fish of this species must have no surface-locomotion mode (body partly emerged, tail in water) that carries them faster than their submerged prolonged-swimming speed",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "No observation either way. Field ethology of D. rerio is described as sparse and anecdotal; habitat is slow or still shallow water (Engeszer 2007). No measured surface-travel speed or jump-from-water height for D. rerio found. Only jumping data are from stranded fish on land (SICB abstract) and a report that Danio are 'not known to voluntarily leave the water' (Gibb 2011, secondary) -- these disagree in emphasis, both preserved. Cross-species (guppy in-air 1.24 vs in-water 1.02 m/s; flying-fish taxi) is the wrong animal and not used",
      "satisfied_evidence": "unknown",
      "note": "Searched three WebSearches (wild zebrafish jumping/surface/skittering; jump height out of water; wild body size/habitat Engeszer 2007). Read-levels: eLife zebrafish ecology review search-summary; Engeszer et al. 2007 Zebrafish 4:21 search-summary; Sundin 2019 listing; SICB stranded-jumping abstract search-summary; Gibb 2011 via Practical Fishkeeping search-summary. Not searched: Spence et al. 2008 Biol Rev full text, Google Scholar, Web of Science, regional Indian literature. 'Nobody has looked', not 'looked and found nothing'."}
  ]}
```
