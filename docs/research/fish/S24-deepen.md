# S24-D: deepening S24 by attacking its weakest input (the Strouhal number)

Project `zebrafish-flight`, subproblem S24 (behaviour), deepening pass. This is a desk study. I
ran no experiment. Every number here is tagged **measured** (from the literature, with
read-level), **calc** (my arithmetic, `S24-deepen_calc.py` in this directory), or **assumed**.

**The recorded answer under attack.** "Taxiing does not close the gap, and by a wider margin than
first computed. Using the Strouhal band that applies to a small low-Re swimmer, the requirement is
132–199 Hz against a 52 Hz measured maximum: a 2.5–3.8× shortfall. The conclusion holds a
fortiori."

**Short result.** The input this answer depends on most is the **Strouhal number at the taxi
operating point**. The recorded answer uses St 0.54–0.82, borrowed from swimmers at Re ≈ 7 × 10³.
Measured kinematics of fish swimming at the operating Reynolds number (Re 2 × 10⁴ – 10⁶; Bainbridge
1958, as reduced by Seo, Zhou & Mittal 2025) give a peak-to-peak **St ≈ 0.24–0.27**. That is
equivalent to a measured stride of **0.6–0.8 body lengths per tail beat** (Wardle 1975). With that
input, the requirement falls to **≈ 61–81 Hz** at L = 40 mm (calc), which is **1.2–1.6×** the
52 Hz maximum. The "wider margin, a fortiori" claim **falls**. The qualitative negative survives
only by a margin that is now smaller than the uncertainty in several other inputs.

---

## 1. Which input is the answer most sensitive to? (calc, recomputed)

The requirement is f_req = St·U/A. The verdict is the ratio f_req/f_max. In the recorded answer:
St = 0.54–0.816, U = 1.95 m/s, A = 8 mm peak-to-peak (0.20 TL, assumed in S24), f_max = 52 Hz.

| Perturbation (one input at a time) | Ratio at St 0.54 | Ratio at St 0.816 |
|---|---|---|
| Recorded answer | **2.53** | **3.82** |
| St ÷ 2 | 1.27 | 1.91 |
| A × 2 | 1.27 | 1.91 |
| U ÷ 2 | 1.27 | 1.91 |
| f_max × 2 | 1.27 | 1.91 |

Break-even values, where the ratio reaches 1 with everything else held at the recorded values
(calc):

- **St\* = 0.213.** That is 2.5–3.8× below the recorded St.
- **A\* = 20–31 mm** (0.51–0.76 TL).
- **f_max\* = 132–199 Hz.**
- **U\* = 0.51–0.77 m/s.**

All four inputs enter linearly, so the formula alone does not pick one out. The difference is in
**how far each input moves between sources**:

- **St:** the values on record run from 0.20 (cruise-band lower edge) to 1.03 (Mwaffo et al. 2017,
  zebrafish burst, converted to peak-to-peak in challenge 52). That is a **5.1× spread**, and it
  straddles the break-even value of 0.213.
- **A:** 0.15–0.25 TL in S24, a 1.7× spread. To reach break-even it would need 0.5–0.76 TL, which
  is outside every amplitude measurement I saw (§3).
- **U:** fixed by the glide target. Challenge 3 moves the target for the 1-BL wing, not the 3-BL
  wing.
- **f_max:** 52 Hz is a single EMG value. It is open to question (§5), but no source on record puts
  it at 132–199 Hz in adult fish.

So **St is the input whose plausible range crosses the decision line**. A factor of two on St
alone takes the shortfall from 2.5× to 1.3×, and the margin claim goes with it. The full sourced
range (down to 0.20) reverses the conclusion.

## 2. How well established is the St value that was used?

**Evidence level: proxy, not measured at the operating point.** The values 0.54 (goldfish), 0.79
(tadpole) and 1.02 (lungfish) are measured values. They come from Eloy 2012, as relayed by the
project law library; I did not read Eloy. But they were measured at **Re ≈ 7 × 10³**, and most of
them come from elongate swimmers. The taxi requirement applies at **Re = 7.8 × 10⁴** (L 40 mm) or
6.4 × 10⁴ (L 33 mm) (calc).

The recorded answer reasons "small fish, so low Re, so high St". That uses body size as a proxy for
Re. At 1.95 m/s the proxy fails, because the fish is small but fast. Challenge 52 already showed
this, and it also found that the upper bound of 199 Hz needs St 0.816, which none of the cited taxa
supplies. I re-ran that arithmetic and it holds (calc).

The zebrafish-specific values, St ≈ 0.73 cruising and ≈ 1.03 bursting (peak-to-peak; Mwaffo et
al. 2017, *PeerJ* 5:e4041), are **measured**. They were taken at Re ≈ 900–3,400, which is 23–75×
below the operating Re. I took them as relayed in challenge 52 (whose author read the full text);
I did not re-read them. Read-level for me: **listing** (secondary, from a sibling document).

So the recorded St is **measured values applied outside the Reynolds number range they were
measured in**, and that was presented as a correction. It is an assumption that reads as a
measurement.

## 3. Improving the input: what do fish actually do at Re 10⁴–10⁶?

What is needed is **St, or an equivalent kinematic quantity, measured in fish swimming at
Re ≈ 6–8 × 10⁴**. No zebrafish measurement at that speed exists in what I could reach (scope in
§6). The best primary-source substitute is the classic body of kinematic data on fish of other
species that swim at that Reynolds number.

**Bainbridge 1958**, *J. Exp. Biol.* 35:109, "The speed of swimming of fish as related to size and
to the frequency and amplitude of the tail beat." Fish: dace, trout and goldfish up to 30 cm.

- **Read-level: abstract** (journals.biologists.com). The PDF returned HTTP 404, and the USGS
  summary host was blocked by this session's network policy.
- **Measured, author's claim (abstract):** above about 5 beats/s, speed depended only on frequency
  and length.
- **Measured, author's claim (abstract):** amplitude reached a maximum of "about one-fifth of the
  body length", the same for all fish tested.
- **Formula, not visible in the abstract text:** V = ¼·L·(3f − 4) (V in cm/s, L in cm, f in Hz).
  I read this in Seo et al. 2025 (full-text) and in a search summary. The two agree.

**Seo, Zhou & Mittal 2025**, "Scaling laws for caudal fin swimmers incorporating hydrodynamics,
kinematics, morphology, and scale effects", arXiv 2507.11665. Their page says it was published in
*J. Fluid Mech.* 1030 (2026); I did not verify that.

- **Read-level: full-text**, through an automated summariser, first 100k of 197k characters.
- **Authors' claims:**
  - Bainbridge's fish swam at Re ≈ 2 × 10⁴ to 10⁶.
  - Bainbridge's formula rewrites as St_A = (4/3)(A_F/L)(1 + f₀L/U), with f₀ = 1 Hz.
  - That expression "approaches 0.24 at high speed" with A_F/L ≈ 0.18, **peak-to-peak**.
  - Their own simulations give **St_A 0.28 at Re 36,000** against 0.91 at Re 110, and a minimum
    St of 0.23. These are **simulated, not observed**.
  - "At higher Re, the free swimming Strouhal number gets smaller."

**Wardle 1975**, *Nature* 255:725. **Read-level: search-summary** (the abstract, plus a secondary
French review).

- **Measured, author's claim:** one tail-beat cycle advances the fish **0.6–0.8 body lengths**.
- The secondary source attributes to Wardle a mean of 0.7.

**Videler & Wardle 1991**, *Rev. Fish Biol. Fish.* 1:23, doi:10.1007/BF00042660. **Read-level:
search-summary.**

- **Author's claim:** steady swimmers keep a species-specific stride length and tail amplitude
  across speeds, so speed = stride length × frequency.

**Li et al. 2021**, *Proc. R. Soc. B* 288:20211601. **Read-level: full-text** (main text, through a
summariser).

- **Measured:** tail-beat amplitude 0.153–0.17 L in dace, trout and tetra. The amplitude convention
  was not stated in the text I read.

**Improved input (measured kinematics; the application to zebrafish is my inference).** Stride
length λ = U/(fL) ≈ 0.6–0.8, which is the same as a peak-to-peak St ≈ 0.24–0.27 at Re ≥ 2 × 10⁴.

Stride length is the better input because it is **measured directly**. It also removes the need for
S24's **assumed** amplitude, since f_req = U/(λL).

## 4. Recomputing the conclusion (all calc)

| Input | L = 40 mm (premise) | L = 33 mm (Danos & Lauder fish) |
|---|---|---|
| λ 0.8 L/beat | 61 Hz (1.17×) | 74 Hz (1.42×) |
| λ 0.75 (Bainbridge asymptote) | 65 Hz (1.25×) | 79 Hz (1.52×) |
| Bainbridge formula, f = (4/3)(U/L + 1 Hz) | **66 Hz (1.28×)** | 80 Hz (1.54×) |
| λ 0.7 (Wardle mean) | 70 Hz (1.34×) | 84 Hz (1.62×) |
| λ 0.6 (Wardle low end) | 81 Hz (1.56×) | 98 Hz (1.89×) |
| λ 1.0 (tuna-like; Wardle & Videler 1980, search-summary) | 49 Hz (0.94×) | 59 Hz (1.14×) |
| Seo 2025 simulated St 0.28, with S24's A of 8 mm | 68 Hz (1.31×) | — |
| Recorded answer, St 0.54–0.816 | 132–199 Hz (2.5–3.8×) | — |

The ratios in brackets are against the 52 Hz measured escape maximum.

**Disagreement preserved: the low-Re extrapolation route.** If I instead start from the measured
zebrafish St values and carry them up in Re, I get a different answer.

- Method: start from Mwaffo's peak-to-peak St (0.73 cruising, 1.03 bursting), measured at Re 900–3,400.
- Apply the laminar scaling St ∝ Re^(−1/4). This follows from Re ∼ Sw^(4/3) (Gazzola, Argentina &
  Mahadevan 2015, *PNAS* 112:3874, PMC4386394, full-text through a summariser; the paper gives no
  prefactors).
- Hold St constant above an unknown laminar–turbulent transition Re_t. The paper gives no numerical
  transition.

Results:

- **St 0.24–0.79**, which is **58–192 Hz (1.1–3.7×)** (calc).
- The result depends almost entirely on the unknown Re_t and on which Mwaffo point is used.

Comparing the two routes:

- This route **does not exclude** the recorded answer's range. It is a two-parameter extrapolation
  across 1.5 decades of Re.
- The Bainbridge and Wardle route uses **measurements taken at the operating Re**, in fish 2–7× the
  length of a zebrafish. Its weakness is taxon and size: no 4 cm subcarangiform fish was measured.
- I weight the Bainbridge and Wardle route more heavily because it removes the Re extrapolation.
  That weighting is my judgment. I do not average the two routes.

**Verdict on the recorded answer: FALLS.** "132–199 Hz, 2.5–3.8×, a fortiori" depends on St values
taken from the wrong Reynolds number. With St measured at the operating Re, the requirement returns
to **≈ 61–81 Hz (1.2–1.6×)**. That is essentially S24's original 49–73 Hz, and it is
**not** a wider margin.

**What remains of the negative (inference, mine).** A 1.2–1.6× shortfall against a *transient* EMG
maximum is real, but it is thin. Every remaining input could now move the result across the line:

- **Taxiing removes most of the body's water drag.** The Bainbridge strides were measured in fully
  submerged fish, where thrust balances the drag of the whole body. A taxiing lobe needs less
  thrust, so it can run at lower St. Challenges 36 and 37 estimate 23–42 Hz with a heaving-foil
  thrust law (calc, theirs). The submerged-swimming stride therefore probably **overstates** the
  frequency a taxi needs.
- **f_max = 52 Hz** is an EMG frequency during escape, not a kinematic tail-beat frequency, and it
  is not sustained (S24 §5). Wardle's twitch-time argument predicts higher maximum frequencies in
  smaller fish, but I found no zebrafish twitch time. As context only: Videler 1993's
  V_max = 0.4 + 7.4 L (search-summary, secondary) gives **0.70 m/s** for a 4 cm fish (calc). That
  is near the 0.84 m/s burst speed back-calculated in S24, and far below 1.95 m/s.
- **The L basis** (40 vs 33 mm) alone moves the ratio by 1.2×.

So the honest statement is that S24's original position is restored: **not shown to close the gap,
and not refuted for the 3-BL target**. The 1-BL target (5.84 m/s) still needs
5.84/(0.75 × 0.04) ≈ 195 Hz (calc), which is 3.7× the maximum. That case stays closed on every
input.

## 5. What measurement would settle it

1. **Adult zebrafish tail-beat frequency and peak-to-peak amplitude at U ≥ 0.5 m/s (Re ≥ 2 × 10⁴),
   in the same fish that set Ucrit.** This gives the zebrafish's own stride length at the
   operating Re and replaces both λ and the cross-taxon inference.
   - Method: high-speed video at 1,000 fps or more, in a flume capable of 1 m/s, together with the
     Ucrit protocol.
   - Cost (assumed, an order-of-magnitude estimate, not a quote): standard swim-tunnel and
     high-speed-camera equipment, plus a few days of rig time per strain. No new methods are needed.
2. **Kinematic, not EMG, maximum tail-beat frequency during escape bouts, and how long it lasts.**
   This turns 52 Hz into a tail-beat frequency that can be sustained for a given number of beats. It
   can be done with the same video rig.
3. **Net streamwise force on a tethered fish with only the lower caudal lobe immersed, at 1–2 m/s
   inflow.** This is the direct taxi test (S24 §6). It replaces the submerged-swimming St with the
   taxi St, which, as argued above, is the input that would actually decide the 3-BL case.

## 6. Scope of negative searches

- **Zebrafish St, amplitude or frequency at U > 0.6 m/s:** none found.
  - Searched with one web search ("adult zebrafish tail beat frequency amplitude swimming speed
    burst kinematics body lengths per second").
  - This adds to challenge 52's one search and one paper.
  - The results were larval studies and other species.
  - Not searched: Web of Science, Google Scholar, theses, or Müller et al. adult burst-and-coast
    papers. A search summary suggested these, but I did not retrieve them.
- **Bainbridge 1958 full text:** could-not-access. The PDF returned 404, and www.umesc.usgs.gov is
  not in this session's allowed network domains. The amplitude convention in the primary source is
  therefore **unknown** to me. Seo et al. state that it is peak-to-peak.
- **Videler & Wardle 1991 and Wardle 1975 full texts:** not retrieved (search-summary only).
- **Eloy 2012:** not read; its values are as relayed by the law library and challenge 52.

## Sources

| # | Source | Read-level | Used for |
|---|---|---|---|
| 1 | S24-behaviour.md, S24_calcs.py (branch `claude/s24-surface-taxiing-launch-tsepbn`, commit 02279553) | full-text | all baseline inputs |
| 2 | challenge-52.md (branch `claude/strouhal-zebrafish-challenge-a41f13`) | full-text | origin and critique of the 132–199 Hz figure; Mwaffo values relayed |
| 3 | challenge-36.md, challenge-37.md (sibling branches) | full-text (36: first 120 lines; 37: first 80 lines) | taxi-St and force-balance arguments |
| 4 | Bainbridge 1958, *J. Exp. Biol.* 35:109 | abstract; formula via #5 and search-summary | amplitude ≈ L/5; V = L(3f−4)/4 |
| 5 | Seo, Zhou & Mittal 2025, arXiv 2507.11665 | full-text (summariser, 100k of 197k chars) | St_A → 0.24 from Bainbridge; Re 2e4–1e6; simulated 0.28 at Re 3.6e4 |
| 6 | Wardle 1975, *Nature* 255:725 | search-summary | stride 0.6–0.8 L per beat |
| 7 | Videler & Wardle 1991, *Rev. Fish Biol. Fish.* 1:23, doi:10.1007/BF00042660 | search-summary | constant stride-length model |
| 8 | Wardle & Videler 1980 (tuna, ~2× stride), via marineinfo.org | search-summary | λ ≈ 1.0 corner |
| 9 | Videler 1993, V_max = 0.4 + 7.4 L, via secondary review | search-summary | context only |
| 10 | Gazzola, Argentina & Mahadevan 2015, *PNAS* 112:3874, PMC4386394 | full-text (summariser) | Re ∼ Sw^(4/3) laminar, Re ∼ Sw turbulent; no prefactors |
| 11 | Gazzola, Argentina & Mahadevan 2014, *Nature Phys.* 10:758 | search-summary | same scaling, >1000 measurements |
| 12 | Li et al. 2021, *Proc. R. Soc. B* 288:20211601 | full-text main text (summariser) | measured amplitudes 0.15–0.17 L |
| 13 | Mwaffo et al. 2017, *PeerJ* 5:e4041 | listing (relayed by #2; not re-read) | zebrafish St at Re ~10³ |
| 14 | Kyriakatos et al. 2011, *J. Neurosci.* | listing (relayed by #1; not re-read) | 52 Hz escape EMG maximum |

```swarm-result
{"subproblem": "S24-D", "evidence": "derived", "answer": "The recorded 132-199 Hz (2.5-3.8x) requirement rests on Strouhal numbers measured at Re ~7e3, but the taxi operates at Re ~7.8e4, where measured fish kinematics (Bainbridge 1958 via Seo et al. 2025; Wardle 1975 stride 0.6-0.8 L/beat) give peak-to-peak St ~0.24-0.27 and a requirement of ~61-81 Hz (1.2-1.6x the 52 Hz escape EMG maximum; calc), so the 'wider margin, a fortiori' claim falls and S24 reverts to 'not shown to close, not refuted' for the 3-BL target, while the 1-BL target (~195 Hz) stays closed.", "key_number": "St ~0.24-0.27 peak-to-peak at Re 2e4-1e6 (stride 0.6-0.8 body lengths per tail beat), giving f_req ~61-81 Hz at 1.95 m/s", "verdict": "falls"}
```
