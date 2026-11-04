# S24-D-D: deepening S24-D by attacking its weakest input (the 52 Hz frequency ceiling)

Project `zebrafish-flight`, subproblem S24 (behaviour), second deepening pass. This is a desk
study. I ran no experiment and filmed no fish. Every number is tagged **measured** (literature,
with read-level), **calc** (my arithmetic, in `S24-D-deepen_calc.py` in this directory), or
**assumed**.

**The recorded answer under attack (S24-D, commit aeb90402, branch
`claude/s24-deepen-launch-gap-2motub`, full-text read by me).** At the taxi operating point
(Re ≈ 7.8 × 10⁴), measured fish stride gives a requirement of **≈ 61–81 Hz**. That is
**1.2–1.6×** the 52 Hz adult zebrafish escape maximum. The earlier "132–199 Hz, a fortiori" claim
therefore falls, and S24 reverts to "not shown to close, not refuted" for the 3-BL target
(1.95 m/s). Challenge 85 reviewed this and it survived.

**Short result.** Once stride had been fixed, S24-D's answer came to rest on **f_max = 52 Hz**.
I went to the primary source, Kyriakatos et al. 2011, and read it myself. The 52 Hz figure is the
**single highest instantaneous EMG burst frequency across all animals**. The paper's own usual
escape range is **"30 to slightly >40 Hz"**. Those escapes lasted **3–5 cycles**. The fish were
**18–30 mm** long, not the 40 mm premise, and the authors note that frequency falls with body size.

Read as a frequency a 40 mm fish could plausibly reach, the ceiling is about **30–43 Hz** (calc,
partly assumed). Against that ceiling the 3-BL shortfall becomes **≈ 1.4–2.7×**. The taxi would also
need to hold that frequency for 12–46 beats, against 3–5 cycles observed. S24-D's negative
**STRENGTHENS**. It does not become a measured refutation, and it does not restore the 132–199 Hz
figure.

---

## 1. Which input is S24-D's answer most sensitive to? (calc)

S24-D's conclusion is the ratio R = f_req / f_max, with f_req = U/(λL):

- U = 1.95 m/s
- L = 40 mm
- λ = 0.6–0.8 L/beat
- f_max = 52 Hz

This gives R = 1.17–1.56. The verdict "not shown to close" needs R > 1. The verdict "not refuted,
thin margin" relies on R being small.

| Perturbation (one input at a time) | R |
|---|---|
| S24-D as recorded | 1.17–1.56 |
| f_max × 2 | **0.59–0.78** (the gap closes on frequency) |
| f_max ÷ 2 | **2.34–3.12** (S24's wide margin returns) |
| λ × 2 | 0.59–0.78 |
| λ ÷ 2 | 2.34–3.12 |

The break-even points are f_max = 61–81 Hz, or λ = 0.94 L/beat at 52 Hz (calc).

U and L are not candidates for this pass. U is fixed by the glide target. The L effect (40 vs
33 mm) is about 1.2× and was already reported by S24-D and challenge 85.

λ and f_max enter the formula symmetrically, so a factor of two in either one flips the
conclusion. I chose between them on **how well each is established**:

- **λ has been checked four independent ways, and they agree.** Wardle 1975 gives 0.6–0.8.
  Bainbridge 1958 (via Seo 2025) gives about 0.75. A flying-fish taxi stride gives 0.48–0.8
  (challenge 85, calc on relayed observations). Eloy's model gives 72–83 Hz (replicate-52, calc).
  All four fall within 0.48–0.8, a 1.67× spread, and none comes near the 0.94 that would close the
  gap.
- **f_max rests on one number from one paper.** S24, replicate-36, S24-D and challenge 85 all
  relayed it, and none of them examined what kind of number it is. Its plausible range on record
  (21 Hz sustained to 52 Hz peak) spans 2.48×, and that range straddles the point that matters.

**So f_max is the weakest input.** Its doubling flips the conclusion as surely as λ's does, and
it is the less established of the two.

## 2. How well is f_max = 52 Hz established?

**Primary source:** Kyriakatos A, Mahmood R, Ausborn J, Porres CP, Büschges A, El Manira A (2011),
"Initiation of locomotion in adult zebrafish", *J. Neurosci.* 31:8422, PMC6623330. **Read-level:
full-text**, read through an automated summariser: characters 0–100,000 of 101,006, in two passes.
The last 1,006 characters were not read.

What the paper says (authors' claims, quoted from the summariser's verbatim extracts):

- **The measurement is real, in vivo EMG.** EMG wires were inserted in myotomal muscle of intact
  fish, which then swam freely in a 0.35 × 0.25 × 0.25 m aquarium.
- **52 Hz is a peak, not a typical value.** "Across animals, the maximal frequency reached during
  escape was 52 Hz." Elsewhere: "The frequencies generated during escape were much faster, ranging
  from 30 to slightly >40 Hz", and "We never observed motor activity during escape lower than
  29 Hz."
- **Escapes are very short.** "These sequences consisted of a few, in general three to five, short
  cycles of large EMG activity."
- **The fish were small.** "The animals used in this study were 8–15 weeks old (body length
  18–30 mm)", n = 8. The authors also state that "with larger body dimension, the swimming
  frequency decreases". The summariser found no coefficient attached to that statement.
- **Steady swimming never exceeded 21 Hz** (n = 8).
- **The paper does not say how the 52 Hz was computed** (for example, one interburst interval or
  a mean over cycles). The general method is "the interval between two consecutive activity
  peaks", stated in an analysis paragraph that mostly concerns in-vitro data. No kinematic video
  frequency is reported.

**Evidence level of f_max as S24 used it: measured, but misapplied in three ways (my inference).**

1. **It is an extreme, not a capacity.** It is the maximum of the instantaneous EMG frequencies
   pooled across 8 animals. A typical escape tops out at about 40 Hz.
2. **It comes from the wrong size of fish.** It was measured in 18–30 mm fish and applied to a
   40 mm premise fish. The source itself says frequency falls as size grows.
3. **It comes from the wrong duration.** It was reached within a 3–5-cycle burst, and applied to
   a taxi that S24 §3.4 calculated needs **12–46 consecutive beats** at that rate.

All three misapplications push the same way: they make the frequency available to the fish look
higher than it is. The 52 Hz is a measurement. Using it as "the adult zebrafish can drive its tail
at 52 Hz" is an assumption, and four documents repeated it until it read as a measurement.

## 3. Improving the input

**What would ideally be measured:** the kinematic tail-beat frequency that a 40 mm adult zebrafish
can hold for about 12–46 beats. **Nothing I found measures this** (search scope in §6). The
improvements below are the best available. Each step says what kind of evidence it is.

**(a) The source's own usual escape range: 30–42 Hz (measured, full-text).** "Slightly >40" is
read as at most 42 Hz. That reading is my assumption.

**(b) Size correction from 18–30 mm to 40 mm (calc and assumed).** Assume f_max ∝ L^(−x).

- The exponent x is **unknown**.
- I bracket it at 0–1 (assumed). The value 1 is the steepest plausible dependence, the one in
  which stride frequency carries all of a constant burst speed in body lengths per second.
- Larval zebrafish give a weak anchor. Search-summary sources report larval burst tail-beat
  frequencies of about 95–100 Hz (replicate-36; the summaries cite Budick & O'Malley 2000 and
  others), and roughly 45–63 Hz in other larval escape studies. Larval length is **assumed** to be
  about 4 mm; I did not source it.
- Pairing 95–100 Hz at 4 mm with 52 Hz at 18–30 mm gives **x ≈ 0.30–0.43** (calc).
- That anchor compares two different studies, two methods (kinematic and EMG) and two life stages.
  It is an inference, not a measurement.
- With x = 0.35 and a reference length of 24 mm, the 52 Hz peak becomes **43 Hz** and the 42 Hz
  usual top becomes **35 Hz** at 40 mm (calc). The full grid is in the script, §3.

**(c) Duration (measured against calc).** The escapes observed lasted 3–5 cycles. The taxi needs
12–46 beats, which is 2.4–15× longer (calc). No measurement tells me how far frequency drops
across 12–46 beats. The only frequency measured over long bouts is the **21 Hz** steady-swimming
ceiling.

**Improved input:** an f_max of **≈ 30–43 Hz** for a 40 mm fish, held for no more than 3–5 beats
(measured, then size-corrected; the size correction is calc on an assumed exponent). For 12 beats
or more, the only measured ceiling is 21 Hz.

## 4. Recomputing S24-D's conclusion (all calc)

Required frequency at L = 40 mm: λ 0.8–0.6 gives **61–81 Hz**. The flying-fish lower stride,
λ 0.48, gives 102 Hz (challenge 85).

| f_max reading | f_max | R (λ 0.8–0.6) | R (λ 0.48) |
|---|---|---|---|
| S24-D input: single peak across animals | 52 Hz | 1.17–1.56 | 1.95 |
| Usual escape, top ("slightly >40") | 42 Hz | **1.45–1.93** | 2.42 |
| 52 Hz size-scaled to 40 mm (x 0.35) | 43 Hz | **1.40–1.87** | 2.34 |
| 42 Hz size-scaled to 40 mm (x 0.35) | 35 Hz | **1.73–2.31** | 2.89 |
| Usual escape, bottom | 30 Hz | **2.03–2.71** | 3.39 |
| 42 Hz size-scaled, steepest bracket (x 1) | 25 Hz | 2.42–3.22 | 4.03 |
| Maximum steady swimming (the only long-bout figure) | 21 Hz | 2.90–3.87 | 4.84 |

**Verdict: STRENGTHENS.** S24-D's negative for the 3-BL target stands, and its margin widens.
On the most generous reading of the source that still respects size and typical values (43 Hz),
R = 1.4–1.9. On the usual escape range it is 1.45–2.7.

To close the gap on frequency, a 40 mm fish would need **61–81 Hz**. That is above the **single
highest instantaneous value** recorded in smaller fish. It would also have to hold that rate
**3–15× longer** than any escape the source observed.

What this does **not** do:

- **It is not a measured refutation.** No taxi thrust has been measured, and no adult tail-beat
  frequency has been measured kinematically (S24 §5 still applies). "Not refuted" becomes "not
  refuted by measurement, and now not closable on any frequency recorded". It does not become
  "refuted".
- **It does not bring back S24's 132–199 Hz / 2.5–3.8× claim.** That claim fell on Strouhal
  number, and it stays fallen. The wider margin here comes from a different input. The ranges
  overlap only at their ends (2.4–3.2× at the steepest size bracket). I do not merge the two
  arguments.
- **It leaves the 1-BL target (5.84 m/s, about 195 Hz) closed,** and more firmly: 4.5–7.8× against
  25–43 Hz (calc).

**Disagreement preserved.**

- **Size scaling may run the other way.** A 40 mm fish has longer muscle fibres, and a larger fish
  might also recruit faster fibre types differently. I found no adult zebrafish twitch time.
  Wardle's twitch-time argument says only that contraction time rises with length (relayed by
  search-summary; Wardle 1975 not read). x = 0 is kept in the grid: it gives R = 1.17–1.56 at
  52 Hz and 1.45–1.93 at 42 Hz.
- **EMG frequency may undercount tail beats in principle, but I have no evidence that it does.**
  For a body wave, motor bursts and tail beats run 1:1. Nothing I read reports a mismatch.
- **The vendor protocol table** that challenge 85 found (26–33 Hz at Ucrit) is still unused. Its
  provenance is unknown.

## 5. What measurement would settle it

1. **Beat-by-beat kinematic tail-beat frequency over the first 20–50 beats of repeated escape and
   burst bouts, in 35–40 mm adult zebrafish, at 28 °C.**
   - Method: 1,000 fps high-speed video. Ideally add simultaneous EMG, to calibrate the
     Kyriakatos values against kinematics.
   - What it decides: (i) the true f_max at the premise size; (ii) how fast frequency decays
     across 12–46 beats. A held frequency of 61 Hz or more would open the 3-BL case on frequency.
     A held frequency of 45 Hz or less would close it on frequency alone, within the stride band.
   - Cost (**assumed**, order of magnitude, not a quote): a single high-speed camera, standard
     husbandry, a few days of filming and digitising. No new method is needed.
2. **Same rig, a size series from 18 to 40 mm**, to measure the exponent x instead of assuming it.
3. **The tethered lower-lobe thrust test at 1–2 m/s inflow** (S24 §6, S24-D §5). This is still the
   only test that would replace a submerged-swimming stride with the stride of a real taxi.

## 6. Scope of negative searches

- **Adult zebrafish kinematic escape or burst tail-beat frequency (any study):** none found.
  - Searches: one extended search ("adult zebrafish escape C-start tail beat frequency Hz
    kinematics high-speed video stage 2"); one extended search ("adult zebrafish burst swimming
    tail beat frequency Hz swim tunnel maximum …"); one standard search for Gilbert, Zerulla &
    Tierney 2014.
  - Results: larval studies, adult guppy and angelfish C-starts, Mwaffo 2017 at low speed, and
    Kyriakatos 2011 itself.
  - Mwaffo 2017 (as summarised) reports that adult bursting fish show *lower* tail-beat frequency
    than cruising fish, at 26–52 mm/s. Read-level: search-summary.
  - Not searched: Web of Science, Google Scholar, theses, and Müller, Stamhuis & Videler 2000
    (named in a search summary, not retrieved).
- **Adult zebrafish muscle twitch or contraction time:** none found. One extended search on the
  Wardle twitch-time relation returned only tuna, sailfish and review material.
- **Wardle 1975 full text:** not read (search-summary only). Its length–twitch equation is
  **unknown** to me.
- **Kyriakatos 2011:** the final 1,006 characters (of 101,006) were not read. They are most likely
  references; that is my assumption.

## Sources

| # | Source | Read-level | Used for |
|---|---|---|---|
| 1 | S24-deepen.md, S24-deepen_calc.py (branch `claude/s24-deepen-launch-gap-2motub`, aeb90402) | full-text | the answer under attack; λ inputs |
| 2 | S24-behaviour.md (branch `claude/s24-surface-taxiing-launch-tsepbn`) | full-text (§1, §3.2–§5, sources) | U, L, 12–46 beat run length, origin of 52 Hz |
| 3 | challenge-85.md (branch `claude/s24-deepen-verdict-challenge-j52cqu`) | full-text | flying-fish stride 0.48–0.8; review status |
| 4 | replicate-36.md (two branches `claude/tail-beat-frequency-limit-*`) | grep extracts | relayed larval 45–100 Hz; relays of 52 Hz |
| 5 | Kyriakatos et al. 2011, *J. Neurosci.* 31:8422, PMC6623330 | full-text (summariser, 100,000 of 101,006 chars) | 52 Hz peak; 30–>40 Hz usual escape; 3–5 cycles; 18–30 mm; n = 8; 21 Hz steady |
| 6 | Larval zebrafish burst frequencies (Budick & O'Malley 2000 and others, as summarised) | search-summary | size-scaling anchor only |
| 7 | Mwaffo et al. 2017, *PeerJ* 5:e4041 | search-summary | adult burst frequency lower than cruise at low speed |
| 8 | Wardle 1975, *Nature* 255:725; Wardle 1989 *J. Fish Biol.* | search-summary | twitch time rises with length (direction only) |
| 9 | replicate-52.md (relayed by #3) | listing | Eloy-route 72–83 Hz, for λ convergence |

```swarm-result
{"subproblem": "S24-D-D", "evidence": "derived", "answer": "S24-D's 3-BL verdict (61-81 Hz needed, 1.2-1.6x the 52 Hz maximum) is most sensitive to f_max, and the primary source (Kyriakatos 2011, full-text) shows 52 Hz is the single highest instantaneous EMG escape frequency across 8 fish of 18-30 mm in 3-5-cycle bursts, with usual escapes at 30 to slightly >40 Hz; read as a 40 mm fish's ceiling (~30-43 Hz, size correction calc on an assumed exponent) the shortfall widens to ~1.4-2.7x and would have to be held for 12-46 beats against 3-5 observed, so the negative strengthens (still calc, not a measured refutation, and it does not restore the fallen 132-199 Hz Strouhal figure).", "key_number": "f_max ~30-43 Hz for a 40 mm adult zebrafish over <=5 beats (vs 52 Hz single peak in 18-30 mm fish; 21 Hz for long bouts), giving f_req/f_max ~1.4-2.7", "verdict": "strengthens",
  "depends_on": ["S24-D answer: f_req 61-81 Hz at 1.95 m/s, L 40 mm (commit aeb90402)", "U = 1.95 m/s 3-BL glide target (inherited from zebrafish-glide-physics.md)", "L = 40 mm premise body length", "stride lambda 0.6-0.8 L/beat (Wardle 1975, search-summary via S24-D)", "Bainbridge 1958 V = L(3f-4)/4 via Seo et al. 2025 (lambda convergence)", "flying-fish taxi stride 0.48-0.8 L/beat (challenge 85, calc on Hertel 1966 / Davenport 1994 relayed via Deng et al. 2019)", "replicate-52 Eloy-route 72-83 Hz (lambda convergence)", "Kyriakatos 2011: 52 Hz max escape EMG frequency across animals (measured, full-text)", "Kyriakatos 2011: usual escape 30 to slightly >40 Hz, 3-5 cycles, fish 18-30 mm, n=8, steady max 21 Hz (measured, full-text)", "Kyriakatos 2011: swimming frequency decreases with body size (author claim, no coefficient)", "size-scaling exponent x 0-1 (assumed), central 0.35 anchored on larval 95-100 Hz at assumed ~4 mm (search-summary)", "EMG burst frequency = tail-beat frequency 1:1 (assumed)", "S24 taxi run 12-46 beats at 52 Hz (S24 sec 3.4, calc on assumed net force 0.5-2 mN)", "1-BL target 5.84 m/s (inherited)"]}
```
