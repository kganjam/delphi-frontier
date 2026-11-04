# Replicate 137: frequency-matched zebrafish myotome power at 21.9 Hz (S10-D-D-D)

**Task.** Independently re-derive the mass-specific power that larval zebrafish myotome
could supply at the wing frequency (21.9 Hz, R = 4 cm), to replace the 80 Hz comparator
(134.4 W/kg) in S10-D-D's burst verdict.

## Blinding disclosure (read this first)

- **The repository holds none of the inputs.** I searched the working tree for
  `S10-D-D`, `challenge-77`, `zebrafish` and `deepen-s10`. The only hits were two
  unrelated Gemini triage JSON files under `findings/`. No branch named
  `harvest:deepen-s10-d-d-juuuwn` exists locally or on `origin`. I read nobody else's
  working.
- **The question text was not blind.** It already contained the recorded result
  ("58-67 W/kg (58-88 at the measured 8% strain; hard ceiling 126)", "x9.2-10.6"). I saw
  those numbers before deriving anything, so this is **not a blinded replication**. What
  I could do independently was re-read the primary source and redo the arithmetic.
  Give the agreement below less weight because of this.

## Sources

| # | Source | Read level |
|---|---|---|
| S1 | Mead AF, Kennedy GG, Palmer BM, Ebert AM, Warshaw DM. *Mechanical characteristics of ultrafast zebrafish larval swimming muscles.* Biophys J 119(4):806-820 (2020). doi:10.1016/j.bpj.2020.06.036, PMID 32755560, PMCID PMC7451861 | **full-text**, with caveats. Read at pmc.ncbi.nlm.nih.gov/articles/PMC7451861 through a summarising fetch tool, which returned verbatim quotes. It covered characters 0-100,000 of 119,992; the tail, probably references and back matter, was not read. Fig. 8D/E were not read as images. Europe PMC fullTextXML returned nothing (not OA). par.nsf.gov could not be reached (DNS blocked). bioRxiv returned HTTP 429. |
| S2 | The S10-D-D power requirements: the central R = 4 cm hover margin of x4.6 against 134.4 W/kg, and the forward-flight requirement of 97-121 W/kg from challenge-77 | **could-not-access**. These are taken **only from the question text** and I have not verified them. |

## Inputs (from S1, quoted)

- Work-loop protocol: "preparation length was varied by 8% sinusoidally at 40, 60, 80,
  100, and 120 Hz at 28°C". Length varied between 1.01 and 1.09 L0, over 10 cycles. A single
  0.4 ms supramaximal twitch pulse was given per stimulated cycle, with phase optimised in
  0.5 ms steps. n = 5.
  **No frequency below 40 Hz was tested** (scope: the Methods sentence above and the
  Results text I read).
- Net work: "2.63 ± 0.18 J/kg of muscle at 40 Hz to 0.43 ± 0.27 J/kg at 120 Hz". The values at
  60/80/100 Hz appear in Fig. 8D only, which I did not read numerically.
- Net power: 134.4 ± 19.9 W/kg at 80 Hz, and 122.9 ± 11.1 W/kg at 100 Hz. Power at 40/60 Hz is
  not stated in the text.
- Maximal isometric (tetanic) stress: 76 ± 3 mN/mm² (= 76 kPa). Twitch/tetanus ratio: 0.91 ± 0.05.
- Twitch: full width at half-maximal stress is 11 ± 1 ms. Force "returned to baseline within 25 ms".
- Muscle density used for mass: 1.06 g/cm³.

One internal inconsistency in S1, preserved rather than resolved: the Methods say the
first five cycles were stimulated, while the Fig. 8A legend says the first two. This does
not change any number used below.

## Arithmetic (all of it is calculation, none is observation)

f = 21.9 Hz (the wing frequency, taken from the question). P = W_cycle × f.

1. **Floor: hold work/cycle at its lowest-frequency measured value (40 Hz).**
   2.63 J/kg × 21.9 = **57.6 W/kg**. Carrying ±1 SD of 0.18 gives 53.7-61.5 W/kg.
   It is a floor in the sense that net work per cycle in S1 falls monotonically as
   frequency rises across 40→120 Hz. My inference is that it should not fall when going
   *down* to 21.9 Hz, because the 11 ms twitch fits easily inside the 22.8 ms shortening
   half-cycle.
2. **Linear extrapolation of work/cycle below 40 Hz (an inference: no data exist there).**
   - Derived work at 80 Hz = 134.4/80 = 1.68 J/kg. Slope 40→80 Hz = (2.63 − 1.68)/40 = 0.02375 J/kg/Hz.
     That gives W(21.9) = 2.63 + 18.1 × 0.02375 = 3.06 J/kg, so P = **67.0 W/kg**.
   - Using the 40→120 Hz slope instead, (2.63 − 0.43)/80 = 0.0275, gives W = 3.13 J/kg and P = 68.5 W/kg.
   - The extrapolation is optimistic in one respect. One twitch per cycle returns to
     baseline within 25 ms, so at 45.7 ms per cycle the extra time cannot all be used.
     Work/cycle should saturate rather than keep rising linearly.
3. **Upper plausible value at the measured 8% strain.** At 40 Hz the loop delivers
   2.63 / 5.74 = 0.46 of the rectangular-loop work (see step 4). Allowing the loop to fill
   up to ~0.70 of the rectangle at low frequency (my assumption, not a measurement) gives
   4.0 J/kg, so P = **≈ 88 W/kg**.
4. **Hard ceiling: a rectangular loop at full tetanic stress over the full 8% strain.**
   - W = σ·ε/ρ = 76,000 Pa × 0.08 / 1060 kg/m³ = 5.74 J/kg, so P = **125.6 W/kg**.
   - At twitch stress (0.91 × 76 = 69.2 kPa, which is my product and not a reported value):
     W = 5.22 J/kg, so P = **114.3 W/kg**.
   - This ceiling holds only at 8% strain. A larger, unmeasured strain raises it in proportion.

**My value:** frequency-matched comparator **≈ 58-67 W/kg** (central ~62). The plausible
range at 8% strain is 58-88 W/kg. The ceiling is 126 W/kg at tetanic stress, or 114 W/kg at
twitch stress. Every one of these is calculated and extrapolated beyond S1's tested range.

## Consequences for the verdict (calculation; requirements unverified, from S2)

- Implied central R = 4 cm hover requirement = 4.6 × 134.4 = 618 W/kg. This is inferred from the
  question's "x4.6" read as required/available.
  - Against 67 W/kg: x9.2. Against 57.6 W/kg: x10.7. So the shortfall factor roughly doubles,
    which matches the question's ×9.2-10.6 to within rounding (I get 10.7 at 57.6).
- Forward flight requires 97-121 W/kg:
  - Against 58-67 W/kg: fails at every corner (×1.45-2.10 short).
  - Against 88 W/kg: still fails (97 > 88).
  - Against the 126 W/kg ceiling: the 121 W/kg corner is met (0.96), so the verdict flips.
- **One nuance the recorded statement does not mention.** If the ceiling uses twitch stress
  (114 W/kg), a 97 W/kg corner flips but the 121 W/kg corner does not. Whether "the most
  generous corner still flips" therefore depends on which corner is the generous one and on
  whether a single-twitch loop can reach tetanic stress. My inference is that it cannot:
  the twitch/tetanus ratio is 0.91.

## Comparison with the recorded value

The recorded value, visible in the question, is 58-67 W/kg, 58-88 at 8% strain, and a hard
ceiling of 126. I get 57.6-67.0 (68.5 with the alternative slope), ~88, and 125.6.
**AGREE**, with two caveats. First, the derivation was not blind, because the numbers
were in the prompt. Second, the ceiling falls to 114 W/kg at twitch stress, which weakens
the claim that the most generous forward-flight corner flips. The fail/flip conclusions
also rest on requirement figures (618, 97-121 W/kg) that I could not access and did not
verify.

```swarm-replication
{"claim_id": 137, "my_value": "58-67 W/kg at 21.9 Hz (2.63 J/kg x 21.9 = 57.6 floor; linear work extrapolation 67-68.5); 8%-strain plausible <=~88; rectangular ceiling 125.6 W/kg (114.3 at twitch stress)", "agrees": true,
  "note": "Recomputed from the Mead et al. 2020 full text (40 Hz is the lowest tested), but the recorded figures were visible in the prompt so this is not blind; the ceiling drops to 114 W/kg at twitch stress, which would un-flip the 121 W/kg forward-flight corner."}
```
