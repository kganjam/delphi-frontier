# Challenge 37: the "sustained taxi ceiling ≈ Ucrit" claim (S24)

**Claim under review** (author: S24, `docs/research/fish/S24-behaviour.md` on branch
`claude/s24-surface-taxiing-launch-tsepbn`, §3.2 and §4; the claim is quoted here, not mine):
"At sustainable tail-beat frequencies the calculated taxi ceiling is ~0.56 m/s, which is Ucrit
itself -- so taxiing adds essentially nothing to the launch." Recorded evidence level: derived.
Value: 0.56 m/s.

**Verdict: WEAKENED.** The arithmetic is correct. But the match to Ucrit is built into the
calibration, so it is not an independent result. The conclusion also rests on an assumption that
the author's own cited simulation contradicts: that a taxiing tail runs at the same Strouhal
number as a fully submerged swimmer.

Read-levels for everything I used: `S24-behaviour.md` and `S24_calcs.py` were read in **full-text**.
For Kyriakatos et al. 2011 (*J. Neurosci.*, PMC6623330) I read only the **abstract**, via Europe PMC;
the full-text XML endpoint returned HTTP 500. Deng et al. 2019 (bioRxiv 10.1101/765560) I know
only as the **abstract-level** figures quoted in S24, which I did not re-fetch. Taylor, Nudds &
Thomas 2003 I also know only as cited in S24 (**abstract** per S24).

---

## 1. Independent arithmetic (calc, mine)

The ceiling formula is U_max = f·A/St, with A the peak-to-peak tail amplitude.

- With f = 21 Hz, A = 0.20 × 40 mm = 8 mm and St = 0.3: U = 21 × 0.008 / 0.3 = **0.560 m/s**.
  This reproduces the author's number.
- Calibration step in S24 §3.2: A was picked by demanding St = 0.3 at Ucrit = 0.548 m/s with
  f = 21 Hz. That gives A = 0.3 × 0.548 / 21 = **7.83 mm = 0.196 TL**, which the author rounded to
  0.20 TL.
- Put the unrounded calibrated A back into the ceiling formula: U = 21 × 7.83 mm / 0.3 =
  **0.548 m/s, which is Ucrit exactly**.

No arithmetic error. The numbers are right.

## 2. The defect: the "= Ucrit" result is circular (my inference)

The central ceiling uses the same f (21 Hz), St (0.3) and A as the calibration. A was chosen so
that f·A/St = Ucrit. Inverting the formula therefore has to return Ucrit, up to the rounding of A
(0.548 → 0.56). So "the taxi ceiling is Ucrit itself" is an identity of how the model was set up.
It is not something the calculation found.

What the calculation actually says is narrower: **if a taxiing tail is subject to the same
kinematic limit as a submerged fish swimming at Ucrit, then it reaches the same speed.** That
condition is the very thing in question, and the claim's wording ("which is Ucrit itself")
presents it as a conclusion.

To the author's credit, S24 §3.2 calls the calibration "consistency checks, not validation", and
§5 flags the Strouhal band as an assumption. The swarm-result summary and the headline claim
drop those caveats.

## 3. Proxy and hidden assumption: cruise Strouhal standing in for net-thrust cutoff

**The proxy.** St ≈ 0.2–0.4 is the band where animals cruise efficiently (Taylor et al. 2003, as
cited). In submerged cruise, thrust equals the drag of the whole wetted body. The quantity that
matters for taxiing is different: **the speed at which the tail's net thrust falls to zero when
most of the body's water drag is gone**. Taxiing exists because it removes body drag (S24 §1,
§3.3). With less drag to overcome, the tail can run at a higher advance ratio, which means lower
St, and still produce net thrust. Holding St fixed at the submerged cruise value assumes away
exactly the effect taxiing is supposed to exploit.

**Counter-example inside the author's own sources** (simulated, not observed; abstract-level as
quoted in S24 §2.2). Deng et al. 2019 simulated a 0.25 m flying fish. Taxiing at 10 m/s needed
**50 Hz**; submerged cruising at the same 10 m/s needed **145 Hz**. Same speed, about 2.9× lower
frequency. If amplitude were similar in the two modes, the taxi St would be about one third of
the submerged St. The abstract gives a 15° deflection for the taxi case and no submerged
amplitude, so this ratio is **not cleanly a Strouhal ratio**. It is an indication of direction
and rough size, not a calibration.

**Relaxing the assumption** (calc, mine; f = 21 Hz, A = 8 mm):

| Taxi St | U_max at 21 Hz | U_max at 52 Hz |
|---|---|---|
| 0.3 (S24 central) | 0.56 m/s | 1.39 m/s |
| 0.2 | 0.84 m/s | 2.08 m/s |
| 0.15 | 1.12 m/s | 2.77 m/s |
| 0.1 (≈ 0.3 / 2.9, Deng-like) | 1.68 m/s | 4.16 m/s |

The author's own corner table already spans **0.32–1.40 m/s** at 21 Hz. Once taxi St is allowed
to fall below the cruise band, the 21 Hz ceiling goes up to roughly 1.1–1.7 m/s. That is 2–3×
Ucrit, and above the 0.84 m/s burst speed that S24 back-calculated. The phrase "adds essentially
nothing" holds only at the single St = 0.3 point.

I do **not** claim taxiing works. Nobody has measured zebrafish caudal thrust against flow speed
(S24 §2.4; I did not repeat that search). The low-St rows above are as unmeasured as the St 0.3
row. My point is narrower: the 0.56 m/s figure is not robust, because it moves by up to 3×
within the assumption's own plausible range.

## 4. A second proxy: "sustainable" frequency for a sub-second manoeuvre

The claim uses the 21 Hz steady-swimming maximum. The Kyriakatos et al. 2011 abstract
(abstract-level) describes EMG frequencies in **freely moving** adult fish used as a reference
for an in-vitro preparation. Nothing there (at the level I read) ties 21 Hz to swimming at Ucrit
in a flume. S24 itself estimates the taxi lasts **0.2–0.9 s, or 12–46 beats** (§3.4). The
frequency that matters is the one an adult can hold for about 0.2–1 s. That lies somewhere
between 21 Hz (steady) and 52 Hz (escape peak), and its actual value is **unknown**. I did not
search further for it. Using the steady-swimming ceiling for a burst-length manoeuvre biases the
claim towards "nothing".

The 21 Hz ↔ Ucrit pairing in the calibration is also an assumption. Unless the full text says
otherwise (I could not access it), no source shows that the fish reached 21 Hz at 0.548 m/s.

## 5. Evidence level

"Derived" is honest in that this is arithmetic on literature inputs plus assumptions, and S24
never presents it as measured. But calling the agreement with Ucrit a finding overstates what the
derivation contains, because the agreement was put in by calibration. A more accurate label is
**derived, self-calibrated (agreement with Ucrit is by construction)**.

## 6. Disagreements preserved, not resolved

- Ucrit: Palstra 2010 0.548 m/s and Plaut 2000 ≈ 0.56 m/s, against Wakamatsu 2019 0.19–0.28 m/s
  (all as tabulated in S24). Had the calibration used Wakamatsu, the "ceiling = Ucrit" identity
  would still hold, because it is an identity, but at about 0.24 m/s. That again shows the number
  follows the calibration input.
- Flying-fish taxi frequency: 13.5 / 21.2 / ~50 Hz (S24 §2.2). I used only Deng's simulated
  50 vs 145 Hz, and only for direction.

## 7. What would settle it

The same measurement S24 names: tethered adult zebrafish thrust as a function of inflow speed and
tail-beat frequency, ideally with the body out of the water and a submerged lower lobe. That
measurement would set the zero-net-thrust St directly and replace both proxies.

```swarm-challenge
{"claim_id": 37, "outcome": "weakened", "reason": "The 0.56 m/s arithmetic is correct but equals Ucrit by construction (tail amplitude was calibrated so that 21 Hz x A / St 0.3 = Ucrit), and the conclusion rests on assuming a taxiing tail keeps the submerged-cruise Strouhal number, which the author's own cited CFD (Deng 2019: 50 Hz taxi vs 145 Hz submerged at the same 10 m/s, simulated) contradicts; relaxing St to 0.1-0.2 lifts the 21 Hz ceiling to 0.84-1.68 m/s.", "corrected_value": "0.56 m/s only at St 0.3 (circular with Ucrit); calc range at 21 Hz is 0.32-1.40 m/s across S24's own corners and up to ~1.7 m/s if taxi St ~0.1; unmeasured either way"}
```
