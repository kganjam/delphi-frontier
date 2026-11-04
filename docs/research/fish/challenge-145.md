# Challenge 145 — adversarial review of [S24-D-D] (52 Hz frequency ceiling)

**Claim under review (the author's, not mine):** S24-D's 3-BL verdict is most sensitive to the 52 Hz
ceiling. Kyriakatos et al. 2011 measured it as an EMG maximum across 8 intact adults 18–30 mm long, with
escapes typically 30 to slightly >40 Hz and the recording temperature not reported. The author takes the
improved ceiling for a 40 mm fish as ~36–52 Hz, so the taxi shortfall widens from 1.2–1.6x to 1.2–2.3x.
Verdict: strengthens. Recorded evidence level: derived.

**My verdict: WEAKENED.** The facts the claim quotes from the source check out. But the claim calls the
number a "maximum tail-beat frequency" when it is an *escape-burst* EMG maximum. The same paper gives a much
lower ceiling for ordinary swimming in the same fish. The claim does not say which of the two the taxi task
needs. One Q10 range is also arithmetically inconsistent.

## Sources and read-levels

| Source | Read-level | Notes |
|---|---|---|
| Kyriakatos A, Mahmood R, Ausborn J, Porres CP, Büschges A, El Manira A (2011) *Initiation of locomotion in adult zebrafish*, J Neurosci 31(23):8422–8431, doi:10.1523/JNEUROSCI.1012-11.2011, PMC6623330 | full-text (PMC HTML, read through a fetch tool that summarises; I checked the key sentences in a second targeted fetch; the last ~1,000 characters were not read) | jneurosci.org would not resolve from this session; the PMC copy was used |
| Danos & Lauder (peak-speed cross-check) | not checked | I did not re-read it, so I make no claim either way |
| Adult fast-fibre Ca²⁺ half-fusion at 53 Hz | not checked | Citation not given in the claim; not traced |
| S24-D definition (what "3-BL" and "taxi" mean) | could-not-access | Searched this repository for `S24-D`, `Kyriakatos`, `52 Hz`, `zebrafish`, `tail-beat`, `taxi` (all files, all branches in the local clone): no hits |

## 1. What the source says (quoted or close-quoted from the PMC full text)

- "Across animals, the maximal frequency reached during escape was 52 Hz." — **confirmed.**
- Escape frequencies were "ranging from 30 to slightly >40 Hz"; "We never observed motor activity during
  escape lower than 29 Hz." — **confirmed.**
- n = 8 intact animals carrying bilateral EMG wires, swimming freely in a 0.35 × 0.25 × 0.25 m aquarium. —
  **confirmed.**
- "The animals used in this study were 8–15 weeks old (body length 18–30 mm)." — **confirmed.** This is a
  study-wide statement, not one given specifically for the EMG fish.
- Temperature: the in vitro preparations were perfused "at 20–22°C". **No temperature is given for the
  intact EMG recordings or for housing.** The claim's "unreported" is correct for the in vivo data, but the
  paper does report a temperature for its other preparation.
- **Ordinary swimming in the same intact fish:** "the frequencies of swimming activity ranged from 2 to
  21 Hz", and "never exceeding 21 Hz".

## 2. Proxy problem (main fault)

The claim uses 52 Hz as a "maximum tail-beat frequency". In the source it is the fastest EMG burst rate
during **escape** sequences: short, Mauthner-initiated bursts that interrupt swimming. The same eight fish
**never exceeded 21 Hz during ordinary swimming** (measured, Kyriakatos 2011).

Which ceiling applies depends on what S24-D's "taxi" requires, and I could not find its definition (see the
table above).

- **If the taxi is a sustained or repeated swimming task**, the right ceiling is the ~21 Hz swimming maximum,
  not the escape maximum. Applying the author's own inverse scaling (shortfall × 52/21), the shortfall becomes
  about **2.9–4.0x (calc)**, not 1.2–2.3x. The direction ("not shown to close") gets stronger. But the
  "not refuted" corners collapse: a Q10 lift of 21 Hz (1.2–2.1 over 6–8.5 °C gives ~23–39 Hz, calc) does
  not close a 2.9x gap.
- **If the taxi is a single brief burst**, the escape ceiling is the right quantity and the claim's
  framing holds.

The claim's headline ("adult zebrafish maximum tail-beat (EMG) frequency ~36–52 Hz") is wrong as a
general statement either way. It is an escape figure; this source's swimming maximum is 21 Hz.

A secondary proxy issue: an EMG burst rate at one myotomal site is not the same as a kinematic tail-beat
frequency. The first cycle of an escape is a C-bend, not a tail beat. This probably matters less than the
escape-versus-swimming issue, and I have not quantified it.

## 3. Arithmetic, redone independently

- Flip thresholds: a 17% or 56% rise in the ceiling flips the verdict only if the unrounded shortfalls are
  1.17x and 1.56x. Rounded to 1.2x and 1.6x, the rises would be 20% and 60%. This is consistent with
  rounding, not an error.
- Widened shortfall: 1.56 × 52/36 = 2.25 and 1.6 × 52/36 = 2.31, so "≤2.3x" reproduces (calc).
- **Q10 range is internally inconsistent (calc).** To lift 52 Hz to 61 Hz with Q10 = 1.2 needs a
  temperature rise of 8.8 °C. To lift it to 81 Hz with Q10 = 2.1 needs 6.0 °C. No single temperature rise
  produces both ends of "61–81 Hz".
  - At a 6 °C rise the range is 58–81 Hz.
  - At an 8.5 °C rise (e.g. 20 → 28.5 °C) it is 61–98 Hz.

  The range the claim quotes appears to be reverse-fitted to the flip thresholds rather than computed from
  one assumed temperature.
- **Hidden assumption in the Q10 corner:** it assumes the fish were recorded *colder* than the taxi
  scenario. If the intact fish were in standard ~28 °C housing water (unknown; not reported), there is no
  uplift at all. The temperature uncertainty is two-sided in its *effect on the argument*, not only
  upward.

## 4. Evidence level

"Derived" is honest for the 36–52 Hz figure for a 40 mm fish (a size extrapolation) and for the 1.2–2.3x
shortfall. The 52 Hz, 30–>40 Hz, n = 8 and 18–30 mm figures are *measured* values in the source and are
quoted correctly. I found no case of a calculated value presented as an observation. The fault is in the
label "tail-beat", not in the evidence level.

## 5. Counter-example the author missed

The counter-example is in the author's own source: the 21 Hz swimming ceiling (Kyriakatos 2011, measured,
same animals).

Scope of the negative search: I searched only this paper and this repository. I did not survey kinematic
(high-speed video) studies of adult zebrafish tail-beat frequency.

## What survives

The source facts survive. So does the size-scaled 36–52 Hz *if and only if* the relevant quantity is the
escape-burst frequency. The direction "strengthens 'not shown to close'" survives in both readings.

What does not survive:
- the label "maximum tail-beat frequency" with no task qualifier;
- the claim that "not refuted" rests *only* on temperature and λ = 1.0. Under the sustained-swimming
  reading, it rests on the taxi being escape-like;
- the 61–81 Hz Q10 range as stated.

```swarm-challenge
{"claim_id": 145, "outcome": "weakened", "reason": "Kyriakatos 2011 (full-text) confirms 52 Hz but as an escape-burst EMG maximum; the same 8 intact fish never exceeded 21 Hz in ordinary swimming, so calling 36-52 Hz the 'maximum tail-beat frequency' is a proxy that holds only if the taxi task is escape-like (otherwise the shortfall is ~2.9-4.0x, calc), and the 61-81 Hz Q10 range implies two different temperature rises (8.8 vs 6.0 C).", "corrected_value": "52 Hz = escape-burst EMG maximum (measured, 18-30 mm fish); sustained-swimming EMG maximum = 21 Hz (measured, same fish); Q10 1.2-2.1 over a single 6 C rise lifts 52 Hz to 58-81 Hz (calc)", "depends_on": ["Kyriakatos et al. 2011 J Neurosci 31:8422, PMC6623330: escape max 52 Hz, escapes 30 to >40 Hz, swimming 2-21 Hz never >21 Hz, n=8 intact, 18-30 mm, in vivo temperature unreported", "S24-D taxi shortfall 1.2-1.6x at a 52 Hz ceiling, scaling inversely with the ceiling (author's figures, not independently derived)", "S24-D taxi task definition (sustained vs burst) - could-not-access"]}
```
