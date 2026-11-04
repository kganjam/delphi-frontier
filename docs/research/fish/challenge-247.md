# Challenge 247: replication of claim 203 (sustained flapping power)

**Claim under review** (claim 247; source `docs/research/fish/replicate-203.md` on branch
`claude/s10-flapping-power-rederivation-ygs05k`, read in full together with `replicate-203_calc.py`):

> Replication (blind): ~16 W/kg body = 65-165 W/kg flight muscle at f=0.10-0.25; at 0.4 g hover
> ~33 W/kg muscle, forward flight ~10-14 W/kg muscle; available ectotherm red muscle up to ~28 W/kg
> (scup 20 C, search-summary) not 5-10, so "not supported even in the most generous case" does not
> hold; red-muscle power at ~20 Hz unknown and could restore the claim. DISAGREES with claim 203 in
> magnitude, agrees in direction for ordinary red muscle.

Recorded evidence level: derived. Recorded value: 28 W/kg (fish red-muscle maximum, search-summary).

**Verdict: WEAKENED.** The arithmetic all reproduces. The claim's central move, though, puts a
work-loop maximum measured at **2.5 Hz** in place of red-muscle power at the **~17–22 Hz** wingbeat.
The claim calls power at that frequency "unknown and could restore the claim". The published
frequency dependence I found (search-summary) points clearly toward restoring it: skipjack red-muscle
power is described as "near zero at 15 Hz". So the claim's headline, that 203's "not supported even in
the most generous case" does not hold, is **not established**. Several smaller defects add to this.

Other files read for context (all read in full): `S10-tissue.md` (branch
`claude/s10-tissue-flapping-power-2kag3x`, the source of claim 203), `challenge-203.md` (branch
`claude/fish-flapping-power-challenge-bquvmd`) and `S10-deepen.md` (branch
`claude/deepen-s10-flapping-muscle-wr33g7`).

---

## 1. Independent arithmetic (CALCULATED, not observed)

Script: `docs/research/fish/challenge_247_calc.py`. I wrote it fresh. Where the author's script
searched over speeds numerically, mine uses the closed-form minimum of P = A/V + BV³
(V⁴ = A/3B, P_am = 4A/3V). The inputs are the ones the claim states.

| Quantity | Claim | My calculation |
|---|---|---|
| Blind central case (0.1 kg, b = 0.3 m) | ~16 W/kg body | 16.31 W/kg body, V_mp 12.0 m/s |
| Same, per kg muscle at f = 0.10 / 0.25 | 165 / 65 | 163 / 65 W/kg |
| 0.4 g forward flight, b = 8 cm, C_Db 0.1–0.4, f = 0.3 | 10–14 | 10.0–14.1 W/kg muscle (V_mp 2.6–3.7 m/s) |
| 0.4 g hover, R = 4 cm, k = 1.2, M = 1.5, f = 0.3 | ~33 | 33.2 W/kg muscle |
| Ideal hover floor, k = 1, M = 1, f = 0.3 | (~19, quoted from challenge-203) | 18.5 W/kg muscle |

**The arithmetic is correct.** The faults are in the inputs and in what is compared with what.

## 2. The proxy that carries the result: power at 2.5 Hz standing in for power at ~17–22 Hz

- **What was used.** 27.9 W/kg is the scup red-muscle work-loop *maximum* at 20 °C. The search
  summary I retrieved says this maximum occurred "near 2.5 Hz", and that scup "do not appear to swim
  with such a low tailbeat frequency". Source: Rome & Swank 1992, *J Exp Biol* 171:261; read-level
  search-summary.
- **What matters.** The quantity that decides the question is cycle-averaged red-muscle power **at
  the wingbeat frequency**:
  - The S10 design gives ~22 Hz (author's computation, S10 §3c).
  - The Pennycuick allometric wingbeat formula applied to the same wing (m = 0.4 g, b = 8 cm,
    S = 1.07 × 10⁻³ m²) gives **17.0 Hz**. That is my calculation, and it applies a bird-derived
    allometry well outside the range it was fitted on.
- **Temperature does not close the gap.**
  - The search summary gives Q₁₀ = 1.8 for scup red-muscle V_max.
  - Shifting the 2.5 Hz optimum from 20 °C to the zebrafish's 28 °C with that Q₁₀ gives
    **~4.0 Hz**. That is my extrapolation.
  - The wingbeat is therefore about **4× above the warm optimum**.
  - The same extrapolation lifts peak scup power to ~54 W/kg (Q₁₀ for power = 2.29). That raised
    figure applies only near 4 Hz.
- **Published frequency fall-off** (search-summary):
  - Syme & Shadwick 2002, *J Exp Biol* 205:189, skipjack tuna deep red muscle: "Mechanical power
    was maximal at a cycle frequency of 5 Hz, dropping to near zero at 15 Hz."
  - S10 reports sculpin slow fibres peaking at 2 Hz (Altringham & Johnston, search-summary).
- **My inference, not data.** Red muscle from a warm-bodied red-muscle specialist reaches near-zero
  power at 3× its optimum. It is then unlikely that scup-like ectotherm red muscle keeps anywhere near
  28 W/kg at ~4× its warm optimum. Red-muscle power at 17–22 Hz is still not measured in anything I
  found (`unknown`). Even so, the claim's "could restore" is better stated as "**probably
  restores**".
- **Consequence.** The forward-flight requirement (10–14 W/kg at f = 0.3) and the ideal hover floor
  (18.5 W/kg) are both met only if red muscle delivers more than 10–19 W/kg at ~17–22 Hz. The only
  frequency-resolved red-muscle evidence I retrieved argues against that. The claim's "does not
  hold" therefore rests on an off-frequency number.

## 3. The hidden assumption, relaxed: flight-muscle fraction f = 0.3

- The forward-flight and hover requirements in the claim use **f = 0.3**. That value is S10's
  "most generous" assumption, not a measurement.
- `S10-deepen.md` reports a measured teleost proxy:
  - *Abudefduf saxatilis*, 0.69% of body mass per pectoral fin, so **f ≈ 0.014** for both fins.
  - Source: Mansuit & Herrel 2021, Table 1, read at full-text by that author. I did not re-read it.
- Relaxing f to that proxy with the claim's own forward-flight model gives **213–302 W/kg muscle**
  (my calculation). That is about 4–6× above even the 54 W/kg Q₁₀ extrapolation of scup at its
  optimum frequency, and about 8–11× above 27.9 W/kg.
- Fairness to the claim: 203's own wording ("even in the most generous case") invites a test at
  f = 0.3, and the claim tested 203 on 203's own terms. That is legitimate. But the claim's reversal
  exists **only** inside that generous corner. It also needs the frequency proxy in §2 to hold.

## 4. Other defects

1. **"Blind" labels a non-blind result.**
   - The blind part of the replication (0.05–0.3 kg flier, 65–165 W/kg muscle) **agrees** with 203:
     27.9 W/kg is 2–6× short.
   - The disagreement comes entirely from the post-read §4 scale check. That section took the 0.4 g
     mass, the 8 cm span and f = 0.3 from `challenge-203.md`, and the author says it is "NOT
     independent".
   - The claim sentence opens with "Replication (blind)" and then reports the disagreement. A reader
     will take the disagreement as blind-replicated, and it is not.
2. **The cod value is not red muscle.**
   - replicate-203 §5 lists "small cod 27.5 W/kg" among "red-muscle maxima", while its own §2 says
     "fibre type not confirmed by me".
   - S10-tissue §2a attributes the 27.5 → 16.4 W/kg cod series to **fast** muscle (Anderson &
     Johnston; search-summary).
   - The two sources disagree. I preserve that and do not resolve it, since I did not reach the
     primary source. Either way, the value cannot support "red-muscle maxima up to ~28".
3. **The skipjack attribution conflict is dropped.**
   - replicate-203 attributes 79 / 133 W/kg to Syme & Shadwick 2002 (*J Exp Biol*).
   - S10-tissue attributes 79–133 W/kg to a SICB conference abstract, and 8.8 W/kg to the 2002
     paper's abstract.
   - My search returned the 2002 abstract text through a search summary, but **no W/kg value**, so I
     cannot settle it.
   - replicate-203 does not mention the 8.8 W/kg figure or the conflict, so the disagreement is lost.
     In either reading, the 2002 abstract also says that power was near zero at 15 Hz (§2).
4. **The profile-power model is calibrated on birds.**
   - The forward-flight figure sets profile power to X1 = 1.2 × the absolute-minimum power. That is
     a bird-scale calibration (Pennycuick).
   - At 0.4 g and Re ≈ 10³, profile power from the flapping velocity is relatively larger.
   - challenge-203 §3 charged hover-level profile power on top and got ~15 W/kg at f = 0.3 and ~22 at
     f = 0.2. This is calculated, and I did not recompute it.
   - The 10–14 band is therefore at the optimistic end. This is a minor point compared with §2.
5. **"Available" is a work-loop maximum, not a sustained power.** 27.9 W/kg is the in-vitro maximum
   under optimised strain, phase and stimulation. Whether red muscle can sustain that aerobically
   over minutes was not shown by any source I read (`unknown`).

## 5. Evidence level

- "Derived" fits the claim's conclusion, which compares a computed requirement with literature
  values.
- The **recorded value**, "28 W/kg (fish red-muscle maximum, search-summary)", is a **measured
  literature value** read at search-summary level. It is neither derived nor the claim's own result.
  Recording it under "derived" mislabels its kind.
- Recording it as the key value also hides two facts: it was measured at 2.5 Hz, and the claim's
  actual derived quantities are the 10–14 and ~33 W/kg muscle requirements.
- This is a labelling defect. It does not present a calculated number as an observation.

## 6. Regimes and counter-examples

- **Frequency regime.** This is the main counter-evidence. Red-muscle power falls to "near zero at
  15 Hz" in skipjack (search-summary), and the design wingbeat is 17–22 Hz (calculated).
- **Flap-gliding and water-surface ground effect.** Neither the claim, 203, nor I modelled them.
  Both would lower the requirement, and an intermittent gait turns the question into one about burst
  muscle, not red muscle. That would favour the claim's direction, but only by redefining "sustained".
- **Negative-search scope.**
  - Two web searches: Rome & Swank scup frequency and temperature; Syme & Shadwick skipjack abstract.
  - Two fetch attempts (sciencegate.app) failed because the host is outside this session's network
    allow-list.
  - I did not search for red-muscle work loops at ≥ 15 Hz in any other species, or for any measured
    power of a flapping or flying fish.
  - No database search (Web of Science, Scopus).

## Corrected statement (my wording)

The replication's arithmetic is correct: ~16 W/kg body (65–165 W/kg muscle) for the blind
0.05–0.3 kg case; at 0.4 g with f = 0.3, ~33 W/kg muscle for hover (18.5 at the ideal floor) and
10–14 W/kg for forward flight. All of these are calculated.

The 27.9 W/kg scup value (search-summary) is a red-muscle maximum at ~2.5 Hz and 20 °C (about
4 Hz at 28 °C by Q₁₀ extrapolation). It does not measure power at the ~17–22 Hz wingbeat. At that
frequency red-muscle power is unmeasured. The only frequency-resolved red-muscle data retrieved
(skipjack, near zero at 15 Hz, search-summary) suggest it is far below the 10–19 W/kg needed even in
the most generous corner.

So 203's direction (sustained flapping not supported by red muscle) stands, and so far it has not
been reversed. 203's wording still has the defects challenge-203 identified: "5–10" mixes cold and
warm values, "at least 34" is not a floor, and the computation covers hover only.

```swarm-challenge
{"claim_id": 247, "outcome": "weakened", "reason": "The arithmetic reproduces (16.3 W/kg body; 10.0-14.1 W/kg muscle forward flight and 33.2 hover at 0.4 g, f=0.3), but the claim overturns 203's 'most generous case' only by using scup red-muscle power measured at ~2.5 Hz (search-summary) in place of power at the ~17-22 Hz wingbeat, where skipjack red muscle is reported near zero at 15 Hz (search-summary); the disagreement also comes from the non-blind post-read check, requires f=0.3 (measured teleost proxy ~0.014 gives 213-302 W/kg), and counts a fast-muscle cod value as red.",
  "corrected_value": "Requirement (calculated) at 0.4 g, f=0.3: forward flight 10-14 W/kg muscle, hover 18.5-33 W/kg muscle; available red-muscle power at the ~17-22 Hz wingbeat: unknown, probably well below 10 W/kg (skipjack near zero at 15 Hz); 27.9 W/kg applies only at ~2.5 Hz, 20 C",
  "depends_on": ["Rome & Swank 1992 JEB 171:261: 27.9 W/kg max at 20 C, optimum near 2.5 Hz, Q10(power)=2.29, Q10(Vmax)=1.8 (search-summary)", "Syme & Shadwick 2002 JEB 205:189: skipjack deep red muscle power max at 5 Hz, near zero at 15 Hz (search-summary)", "design wingbeat ~17-22 Hz (S10 computation 22 Hz; my Pennycuick-allometry calculation 17.0 Hz for m=0.4 g, b=8 cm, S=1.07e-3 m2)", "S10 geometry: m=0.4 g, R=4 cm semispan, k=1.2, M=1.5, f=0.3 (assumptions)", "replicate-203 forward-flight model: Pennycuick-style, k=1.2, C_Db 0.1-0.4, X1=1.2, Sb=0.00813 m^0.666 (recalled constants)", "S10-deepen teleost pectoral muscle proxy f~0.014 (Abudefduf saxatilis, Mansuit & Herrel 2021, read full-text by that author, not by me)", "S10-tissue attribution of cod 27.5 W/kg to fast muscle (Anderson & Johnston, search-summary)"]}
```

Sources:
- [Rome & Swank 1992, J Exp Biol 171:261 (publisher page; not reachable from this session)](https://cob.silverchair.com/jeb/article/171/1/261/6442/The-influence-of-temperature-on-power-output-of): search-summary
- [Syme & Shadwick 2002, J Exp Biol 205:189 (ScienceGate listing; fetch blocked)](https://www.sciencegate.app/document/10.1242/jeb.205.2.189): search-summary
- [SICB abstract, skipjack anterior vs posterior power](https://sicb.org/?p=37437): listing (appeared in results; not opened)
