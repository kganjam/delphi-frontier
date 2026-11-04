# S24-D-D: deepening S24-D by attacking its weakest input (the 52 Hz frequency ceiling)

Project `zebrafish-flight`, subproblem S24 (behaviour), second deepening pass. This is a desk study.
I ran no experiment and filmed no fish. Every number is tagged **measured** (literature, with
read-level), **calc** (my arithmetic, `S24-D-deepen_calc.py` in this directory), **assumed**, or
**inherited** (from S24 or S24-D, not re-derived).

**The answer under attack (S24-D, branch `claude/s24-deepen-launch-gap-2motub`, commit aeb9040;
survived challenge 85).** At the taxi Reynolds number, measured stride lengths (0.6–0.8 L per beat)
put the tail-beat frequency needed to taxi a 40 mm zebrafish at 1.95 m/s at **61–81 Hz**. That is
**1.2–1.6×** the 52 Hz adult escape maximum. So for the 3-BL wing S24 is "not shown to close, not
refuted". The 1-BL wing stays closed.

**Short result.** Once the stride input had been corrected, the input the S24-D answer is most
sensitive to is **f_max = 52 Hz**. A factor of 1.17–1.56 on it flips the verdict (calc). S24-D,
challenge 85 and S24 all held that number only second-hand. I read the primary source in full
(Kyriakatos et al. 2011). The number is real and measured as described, an EMG burst frequency in
intact, free-swimming adult fish. But it is:

- the **maximum across 8 animals**, not a typical value. In the paper's own words, escape
  frequencies ranged "from 30 to slightly >40 Hz" in the example animal;
- measured in fish of **18–30 mm**, smaller than the 40 mm premise. Contraction time rises with
  length, so the size correction lowers the ceiling;
- recorded at an **unreported temperature**.

Two independent checks agree with a ceiling near or below 52 Hz. One is the kinematics implied by
Danos & Lauder's measured Reynolds number: about 32–53 Hz (calc). The other is adult zebrafish
fast-fibre Ca²⁺ fusion, which reaches half-fusion at 53 Hz (measured, 20–22 °C). No source I
reached puts an adult zebrafish tail-beat frequency above 52 Hz.

With the improved band, f_max ≈ **36–52 Hz** for a 40 mm adult, the 3-BL shortfall becomes
**1.2–2.3×** (calc). **Verdict: STRENGTHENS.** The "not shown to close" side of S24-D strengthens.
The "not refuted" side survives in one place only. Temperature is unmeasured, and a Q10 of
1.2–2.1 between the recording temperature and 28 °C would lift 52 Hz to the requirement (calc).
Temperature is now the weakest input.

---

## 1. Which input is S24-D most sensitive to? (calc, recomputed)

S24-D's conclusion is the ratio R = f_req/f_max, with f_req = U/(λL). The inherited values are
U = 1.95 m/s, L = 40 mm, λ = 0.6–0.8 L/beat and f_max = 52 Hz, giving **R = 1.17–1.56**.

| One input changed by 2× | R | Conclusion |
|---|---|---|
| none (S24-D) | 1.17–1.56 | not shown to close |
| f_max × 2 | 0.59–0.78 | **flips** |
| λ × 2 | 0.59–0.78 | **flips** |
| L × 2 | 0.59–0.78 | **flips** |
| U ÷ 2 | 0.59–0.78 | **flips** |

The break-even values are **f_max\* = 61–81 Hz**, a rise of only 17–56 %, and **λ\* = 0.94** L/beat
(calc).

All four inputs enter the formula linearly, so the formula does not single one out. What separates
them is **how much each one has already been tested**:

- **U = 1.95 m/s** is a design target inherited from the glide analysis. It is a premise, not a
  fact about the fish.
- **L = 40 mm** is the project premise. Its 33 mm alternative has already been carried as a bracket
  (challenge 85: 1.4–1.9×).
- **λ** has been attacked twice, by S24-D and by challenge 85. Its sourced range is 0.48–1.0, and
  only the tuna-like λ = 1.0 corner reaches break-even.
- **f_max = 52 Hz** has been relayed by three documents and never read at source by any of them.
  S24-D holds it at **listing** level ("relayed by S24; not re-read"). S24 read the paper but
  quoted only the one sentence. It is a **single value**, a cross-animal maximum, and it is an EMG
  quantity standing in for a kinematic one.

So f_max is the input that is equally sensitive and least examined. It is the one to attack.

## 2. How well established was the 52 Hz value?

**Evidence level before this pass:** measured, but held at listing level, as a proxy (EMG burst
frequency standing in for tail-beat frequency) and as an extreme (a maximum standing in for an
operating ceiling). In S24-D the downstream text treats it as "the 52 Hz measured maximum". That is
accurate wording, but it hides three conditions: whose maximum, in what size of fish, and at what
temperature.

## 3. Improving it: the primary source and two independent checks

### 3.1 Primary source, read in full

**Kyriakatos A, Mahmood R, Ausborn J, Porres CP, Büschges A, El Manira A (2011). "Initiation of
locomotion in adult zebrafish." *J. Neurosci.* 31(23):8422–8431, doi:10.1523/JNEUROSCI.1012-11.2011,
PMC6623330.** Read-level: **full-text** (first 100,000 of 101,006 characters, read through an
automated summariser; the quoted sentences below were requested verbatim).

What the paper reports (author's claims, quoted):

- Escape frequency, across animals: "Across animals, the maximal frequency reached during escape was
  52 Hz."
- Escape frequency, example animal: "The frequencies generated during escape were much faster,
  ranging from 30 to slightly >40 Hz." The single-animal example (Fig. 4D, as described in the
  text) reaches "slightly >40 Hz".
- Lower bound on escape: "We never observed motor activity during escape lower than 29 Hz."
- Swimming: "never exceeding 21 Hz (n = 8)".
- Preparation: intact fish. "After recovery from anesthesia (15–20 min), animals could swim and
  produce spontaneous escape". Escape was sometimes "evoked by casting a shadow over the animal."
  The aquarium was 0.35 × 0.25 × 0.25 m. Recording was by EMG wire electrodes in myotomal muscle,
  digitised at 12.5 kHz.
- Animals: "8–15 weeks old (body length 18–30 mm)", ABC and AB/Tübingen strains.
- **Temperature for the in vivo recordings: not reported.** The 20–22 °C stated in the paper
  applies to the in vitro preparation only.

What changes in how the input should be read:

1. **It is real and it comes from intact fish.** Neither S24 nor S24-D got this wrong. *Inference,
   mine:* an EMG burst frequency in a myotome on one side corresponds to one burst per tail-beat
   cycle, so it is a fair proxy for the frequency of body undulation. It cannot show whether the tail
   tip follows at that frequency with full amplitude.
2. **It is a maximum across 8 fish, and the example animal tops out just above 40 Hz.** The value a
   taxi could *hold* is lower than 52, and S24 §3.4 shows the taxi would need it held for 12–46
   beats.
3. **The fish were 18–30 mm, not 40 mm.** Wardle (1975; Nature 255:725; search-summary) states that
   contraction time rises with fish length, and a later Nature letter relays that it "increases with
   the length of the fish and decreases with increase of temperature" (search-summary). I found **no
   zebrafish exponent** for this scaling. With an **assumed** f ∝ L^−b and b = 0.5–1.0, 52 Hz in a
   30 mm fish becomes 39–45 Hz at 40 mm, and 52 Hz in an 18 mm fish becomes 23–35 Hz (calc). At
   b = 0 it stays 52 Hz. The paper does not say which fish produced the 52 Hz value.
4. **Temperature is unknown.** This is the one correction that could push f_max **up** (see §4).

### 3.2 Independent check A: the tail-beat frequency implied by a measured adult burst speed (calc)

Danos & Lauder 2012 (*J. Exp. Biol.* 215:1854, doi:10.1242/jeb.068957; full-text first
100,000 of 120,936 characters, tables not readable) give these measured values:

- fish TL 33.0 ± 1.3 mm;
- filmed at 1000 fps;
- mean maximum Re 27,800 in 1 mPa·s water.

S24 back-calculated a peak speed of 0.84 m/s (TL basis) or 1.05 m/s (SL basis) from these (calc,
inherited). The paper's text gives **no tail-beat frequency** (I asked for it explicitly). Dividing
the peak speed by S24-D's steady stride (λ 0.6–0.8) gives:

- **32–43 Hz** on the TL basis (calc);
- **40–53 Hz** on the SL basis (calc).

**Caveat, mine:** applying a steady-swimming stride to the peak of a fast start is an assumption.
Fast-start strides are not measured here. The check is therefore not independent of λ. What it does
show is that the measured peak speed of an adult zebrafish needs no tail-beat frequency above about
53 Hz at any stride on record. It agrees with Kyriakatos's 30–52 Hz.

### 3.3 Independent check B: muscle kinetics

Idoux R, Bretaud S, Berthier C, Ruggiero F, Jacquemond V, Allard B (2022). "Superfast
excitation–contraction coupling in adult zebrafish skeletal muscle fibers." *J. Gen. Physiol.*
154(9):e202213158, PMC9247716. Read-level: **full-text** (first 100,000 of 103,758 characters,
through a summariser).

**Measured** (isolated fast fibres from 11–13-month-old males, 20–22 °C):

- Ca²⁺ transient decay τ = 8.8 ± 3.4 ms.
- Indo-1 signal half fusion at **53 ± 3 Hz** stimulation.
- 95 % fusion at 156 ± 9 Hz.

**Not reported:** twitch force kinetics.

The authors cite "up to … 50 Hz in … adult" for maximal swimming frequency. They credit this to
Buss & Drapeau 2001, Müller & van Leeuwen 2004 and Kyriakatos 2011. By their titles, the first two
are **larval** studies, so for adults the figure rests on Kyriakatos alone. **It is not an
independent confirmation**, and I do not count it as one.

*Inference, mine:* each side's muscle is activated once per tail-beat cycle. At 61–81 Hz the
half-period is 8.2–6.2 ms, which is 0.93–0.70 τ (calc), and the Ca²⁺ signal from successive beats
would be more than half-fused. That would leave less time to relax before the opposite side
contracts. This is consistent with a cyclic ceiling near 50 Hz **at 20–22 °C**. It is not a
measurement of one. Larval zebrafish fibres need 190 Hz for full fusion (Dou et al. 2008, relayed by
Idoux; not read), so the adult figure here is specific to adults.

### 3.4 Scope of negative searches

**Adult zebrafish kinematic tail-beat frequency above 52 Hz: none found.** What I searched:

- one extended web search ("adult zebrafish tail beat frequency fast start escape high-speed video
  kinematics Hz");
- a standard search on Müller & van Leeuwen 2004, which is larval, 2–21 dpf, up to 100 Hz (abstract
  via search-summary, not used for adults);
- a standard search on Wardle 1975;
- the full texts of Kyriakatos 2011, Idoux 2022 and Danos & Lauder 2012 (text only).

The results were larval studies, head-fixed adult preparations at 7–12 Hz (a 2022 *Neuron* paper,
search-summary, not used), and the "50 Hz adult" citation, which traces back to Kyriakatos.

Not searched: Web of Science, Google Scholar, theses, or the image-only Table 1 of Danos & Lauder.
**Temperature of the Kyriakatos in vivo recordings: unknown.** I asked for it directly in two reads
of the full text and it is not stated. **Q10 of adult zebrafish fast-muscle cycling frequency:
unknown.** I did not find it, and I did not search for it specifically.

## 4. Recomputing the conclusion (all calc)

| f_max used | Basis | R for 3-BL, 1.95 m/s, L 40 mm |
|---|---|---|
| 52 Hz | EMG maximum across 8 fish of 18–30 mm (S24-D's value) | 1.17–1.56 |
| 45 Hz | 52 Hz from a 30 mm fish, size-corrected with assumed b = 0.5 | 1.35–1.81 |
| 42 Hz | "slightly >40 Hz", single-animal escape | 1.45–1.93 |
| 36 Hz | Danos & Lauder peak speed, λ 0.7, TL basis | 1.69–2.26 |
| 30 Hz | bottom of the "30 to slightly >40 Hz" escape range | 2.03–2.71 |

**Improved input: f_max ≈ 36–52 Hz for a 40 mm adult at the recording temperature.** 52 Hz is the
upper bound, and nothing reached supports a higher value. This gives **R ≈ 1.2–2.3** (calc), against
1.2–1.6 in S24-D.

The corners that could still open the 3-BL case are these:

- **Long-stride corner:** λ = 1.0 (tuna-like) gives f_req = 49 Hz. Against 52 Hz that is R = 0.94.
  Against the size- or animal-typical 42 Hz it is 1.16 (calc). This corner was already open in
  S24-D, and it closes against any f_max below 49 Hz.
- **Temperature corner:** suppose the in vivo recordings were made at about 20–22 °C (assumed, not
  reported) and the fish operates at 28 °C. Lifting 52 Hz to 61–81 Hz then needs a Q10 of only
  **1.2–2.1** over 6–8 °C (calc). Whether that is plausible for zebrafish fast muscle is **unknown**
  to me, and I do not supply a Q10 value. This is now the input most able to reverse the conclusion.
  Its direction is the opposite of the size correction, and I do not net the two against each other.

**1-BL target (5.84 m/s).** It needs 146–243 Hz, which is 2.8–4.7× even the 52 Hz upper bound
(calc). It stays closed on every input.

**Verdict on S24-D: STRENGTHENS.**

- What strengthens: the claim "not shown to close". The 52 Hz used by S24-D is an upper bound, taken
  from smaller fish and as a cross-animal extreme. Every correction I can source moves f_max down,
  and the margin widens from 1.2–1.6× to 1.2–2.3×.
- What does not change: the claim "not refuted". It survives only through the unmeasured temperature
  corner and the λ = 1.0 corner.
- What this pass did not do: it did not refute the 3-BL case. A refutation needs a measured f_max at
  28 °C, or a measured taxi stride.

## 5. What measurement would settle it, and what it would cost

1. **Kinematic maximum tail-beat frequency of 35–45 mm adult zebrafish during escape, at a
   controlled 28 °C, with the number of consecutive beats above a threshold.**
   - Method: high-speed video at ≥ 1000 fps, the same setup as Danos & Lauder.
   - This replaces the EMG proxy, the size correction and the temperature unknown in one experiment.
   - It also measures how long the frequency can be sustained, which S24 §3.4 needs (12–46 beats).
   - Cost (assumed, an order-of-magnitude estimate, not a quote): existing camera and tank, about a
     week of work, no new methods.
2. **The same recording at 22 °C and 28 °C.** This measures the Q10 that §4 shows could reverse the
   result. It is the decisive comparison.
3. **Twitch force kinetics (not only Ca²⁺) of adult fast fibres at 28 °C.** This is a mechanistic
   ceiling, and an extension of the Idoux et al. protocol.

## Sources

| # | Source | Read-level | Used for |
|---|---|---|---|
| 1 | S24-deepen.md and S24-deepen_calc.py (branch `claude/s24-deepen-launch-gap-2motub`, aeb9040) | full-text | the answer under attack; λ, U, L |
| 2 | S24-behaviour.md and S24_calcs.py (branch `claude/s24-surface-taxiing-launch-tsepbn`, 0227955) | full-text | U targets, burst-speed back-calculation, required beat count |
| 3 | challenge-85.md (branch `claude/s24-deepen-verdict-challenge-j52cqu`) | full-text | λ 0.48–1.0 range; L 33 mm bracket |
| 4 | Kyriakatos et al. 2011, *J. Neurosci.* 31:8422, PMC6623330 | full-text (100k of 101k characters, through a summariser) | 52 Hz across animals; 30 to >40 Hz example; 18–30 mm; intact EMG; temperature not reported |
| 5 | Danos & Lauder 2012, *J. Exp. Biol.* 215:1854, doi:10.1242/jeb.068957 | full-text (100k of 121k characters; tables are images) | TL 33 mm, 1000 fps, Re 27,800; no tail-beat frequency in the text |
| 6 | Idoux et al. 2022, *J. Gen. Physiol.* 154(9):e202213158, PMC9247716 | full-text (100k of 104k characters, through a summariser) | Ca²⁺ τ 8.8 ms; half fusion at 53 Hz (20–22 °C); "50 Hz adult" citation traced to #4 |
| 7 | Wardle 1975, *Nature* 255:725 | search-summary | contraction time limits frequency and rises with length; stride 0.6–0.8 |
| 8 | Nature letter (284:445) relaying that contraction time rises with length and falls with temperature | search-summary | direction of the size and temperature corrections only |
| 9 | Müller & van Leeuwen 2004, *J. Exp. Biol.* 207:853 | search-summary (abstract) | larval 100 Hz; not used for adults |
| 10 | Brainstem circuits in adult zebrafish, *Neuron* 2022 (S0896627322009941) | search-summary | head-fixed 7–12 Hz; not used |

```swarm-result
{"subproblem": "S24-D-D", "evidence": "derived", "answer": "S24-D's 3-BL verdict is most sensitive to the 52 Hz frequency ceiling (a rise of 17-56% flips it); read at source (Kyriakatos 2011, full-text) it is an EMG maximum across 8 intact adults of only 18-30 mm, with escapes typically 30 to slightly >40 Hz and recording temperature unreported, and two cross-checks (Danos & Lauder peak speed implying ~32-53 Hz; adult fast-fibre Ca2+ half-fusion at 53 Hz) agree, so the improved ceiling for a 40 mm fish is ~36-52 Hz and the taxi shortfall widens from 1.2-1.6x to 1.2-2.3x (calc) - strengthening 'not shown to close', with 'not refuted' now resting only on the unmeasured temperature (Q10 1.2-2.1 would lift 52 Hz to 61-81 Hz) and the lambda=1.0 corner.", "key_number": "adult zebrafish maximum tail-beat (EMG) frequency ~36-52 Hz for a 40 mm fish; 52 Hz is the cross-animal upper bound measured in 18-30 mm fish at unreported temperature", "verdict": "strengthens",
  "depends_on": ["S24-D f_req = U/(lambda*L) model and its 61-81 Hz result (branch claude/s24-deepen-launch-gap-2motub, aeb9040)", "U = 1.95 m/s 3-BL glide target (inherited from zebrafish-glide-physics.md, AR 5, C_L 0.6)", "U = 5.84 m/s 1-BL glide target (inherited)", "L = 40 mm project premise (33 mm alternative)", "stride lambda 0.6-0.8 L/beat (Wardle 1975, search-summary via S24-D); range 0.48-1.0 (challenge 85)", "Kyriakatos 2011 J Neurosci 31:8422: 52 Hz max escape EMG across 8 intact adults, example 30 to >40 Hz, fish 18-30 mm, in vivo temperature not reported (full-text)", "assumption: one-sided EMG burst frequency approximates tail-beat frequency", "assumption: f_max scales as L^-b with b 0-1 (no zebrafish exponent found; direction from Wardle 1975 search-summary)", "Danos & Lauder 2012 Re 27,800, TL 33 mm, and S24's back-calculated 0.84 m/s (TL) / 1.05 m/s (SL) burst speed", "assumption: steady-swimming stride applied to fast-start peak speed (check A)", "Idoux 2022 J Gen Physiol: adult fast-fibre Ca2+ tau 8.8 ms, half-fusion 53 Hz at 20-22 C (full-text)", "assumption: recording temperature ~20-22 C vs operating 28 C for the Q10 corner (unmeasured; Q10 unknown)", "S24 section 3.4 requirement of 12-46 consecutive beats (inherited)"]}
```
