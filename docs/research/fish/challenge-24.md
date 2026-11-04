# Challenge 24 — "5.2x speed / 27x kinetic-energy take-off deficit"

**Claim under review (not written by this reviewer):** "Current best evidence: required takeoff
4.37 m/s against a measured burst of 0.842 m/s is a 5.2x speed and 27x kinetic-energy deficit.
Both corrections tonight were favourable and the conclusion survives both."
Recorded evidence level: *derived*, value 5.2 (ratio). Source: "computed here from the corrected
CL_max and the S21 burst speed".

**Verdict: WEAKENED.** The arithmetic is right. The claim, though, reads a still-air,
submerged-swimming ratio as a fixed deficit. The "27x kinetic-energy" figure is the same number
squared, so it adds no new evidence.

## 0. What I could and could not inspect

- I searched this repository on every branch (`git grep` across all refs for
  `flying|takeoff|fish|burst|0.842|4.37`, plus a file search for `CL_max`, `burst speed` and
  `take-off`). I found **no** CL_max derivation, no mass, no wing area, no source "S21" and no
  record of "tonight's two corrections". The search ran on the repo snapshot at commit `3272d3e`.
  I checked that the search works: it does find known strings such as `fisher-ftns` and
  `zebrafish`.
- So I **cannot** check the inputs 4.37 m/s and 0.842 m/s, the taxon, or whether the two
  corrections were favourable. Status of each: `unknown`. I take both inputs as given and test
  only what follows from them.

## 1. Arithmetic, redone independently (calculated, not observed)

- Speed ratio: 4.37 / 0.842 = **5.190**, which rounds to 5.2. ✔
- Kinetic-energy ratio at equal mass: (4.37/0.842)² = **26.94**, which rounds to 27. ✔
- These are not two pieces of evidence. The KE ratio is the speed ratio squared, with no new
  input. Calling it a "27x deficit" next to the "5.2x" suggests a second, independent shortfall
  when there is only one.

## 2. Proxy check

- **Burst speed is standing in for the top speed the animal can reach at take-off.** If 0.842 m/s
  is a burst speed measured fully submerged (I cannot confirm this, since S21 is unavailable), it
  is the speed where thrust equals drag with the whole body in water. A surface-taxiing animal
  with its body out of the water has far less water drag, so its top speed can exceed its
  submerged burst speed. The quantity that matters is the **maximum taxi speed at the surface**,
  and the claim does not report it.
- **Kinetic energy is a proxy for the wrong constraint.** Take-off does not need an energy store
  spent all at once. It needs thrust to exceed drag all the way up to lift-off airspeed, with
  energy delivered over a taxi run. If burst speed is the thrust-equals-drag limit, the speed
  ratio already captures that limit. The KE framing adds nothing and suggests a budget problem
  that is not what is being tested.
- **Water speed is standing in for airspeed.** Lift depends on airspeed, but 0.842 m/s is a
  speed relative to the water.

## 3. The hidden assumption: still air

The required 4.37 m/s is an airspeed: V = sqrt(2W / (rho · S · CL_max)). The deficit compares it
with a speed through water, which assumes **zero wind** at the animal's height. With that
assumption relaxed (all calculated here):

- A headwind of 4.37 − 0.842 = **3.53 m/s** at the animal's height closes the airspeed gap
  completely, even at the claimed swimming speed.
- Wind near the sea surface is weaker than at the standard 10 m height. I used a log profile with
  roughness length z0 = 2×10⁻⁴ m, which is a typical open-sea value (an assumed value, not
  measured here). At these heights the 3.53 m/s target needs these 10 m winds:
  - **8.3 m/s** at 2 cm
  - **6.9 m/s** at 5 cm
  - **6.1 m/s** at 10 cm

  These correspond to a moderate breeze, around Beaufort 4. That is ordinary at sea, not an
  extreme case.
- So the gap is set by conditions, not by the animal. The claim's 5.2x holds **in still air
  only**. The general form is deficit = 4.37 / (v_water + U_wind(z)), and it reaches 1.0 at
  ordinary sea-state winds.

Assumptions I checked that do **not** weaken the claim (calculated):

- **Ground effect** raises effective CL. A 10–30% rise cuts the required speed to 4.17–3.83 m/s,
  and the ratio stays at 4.9–4.6x. The gap survives.
- **Closing the gap with CL alone** would need a 26.9x higher CL_max, or a wing loading 26.9x
  lower. Neither is physically plausible. The claim's robustness to CL corrections is real.
- **Lift-off above stall speed.** Aircraft practice is about 1.1–1.2 V_stall. If 4.37 m/s is a
  stall speed, the true take-off speed is higher and the gap gets *larger*. That is in the
  claim's favour.

## 4. Evidence level

- The *derived* label is honest for the ratio. ✔
- The word "measured" on 0.842 m/s cannot be checked from here (S21 is unavailable). I flag it as
  unverified, not wrong.
- "Current best evidence" and "the conclusion survives both" are an interpretation. The ratio
  itself is not evidence that take-off is impossible. It is evidence that take-off is impossible
  **in still air from a submerged burst**. The scope statement is missing.

## 5. Regime and published counter-examples

All read-level **search-summary** (I read search snippets only, not the full papers):

- **Flying fish (Exocoetidae)** reach take-off by *surface taxiing*: the body is out of the water
  and only the lower caudal lobe sculls. Speeds well above underwater swimming speeds are
  reported. One CFD study (bioRxiv, Deng et al., per the snippet) models a 0.25 m fish taxiing to
  about 16.5 m/s at 350 W, assuming a 10 m/s underwater speed as its baseline; that is a
  simulation, not a measurement. A popular source (Living Oceans Foundation) gives about 60 km/h,
  which is not peer-reviewed. A 2022 Princeton paper (Saro-Cortes et al.) and a 2023 APS DFD
  abstract describe taxi as thrust until lift-off but give no measured take-off speed I could see.
  These sources were not read in full, and the simulated and popular figures disagree in kind;
  I have not averaged them. Use them only to show the regime exists: an animal that taxis is not
  limited to its submerged burst speed.
- If the subject animal can taxi like this, the 0.842 m/s input is not the binding speed. If it
  cannot, that is a premise the claim needs to state.

## Reviewer's inference, kept apart from the author's claim

The author's arithmetic is correct, and the author's robustness to CL_max corrections is real.
**My inference** is that the conclusion rests on two unstated conditions: still air, and a top
speed limited to the submerged burst speed. The first fails at a moderate breeze, by my
calculation. The second fails for any animal that can taxi at the surface, per the literature
(read at search-summary level only). The claim should be restated as "5.2x in still air, from a
submerged burst". The 27x KE figure should be dropped as a separate line of evidence.

Sources (search-summary):
- https://www.biorxiv.org/node/903826
- https://www.livingoceansfoundation.org/fantastic-flying-fishes
- https://bamlab.princeton.edu/_files/ugd/8339e9_3ef94b52b27c46ef8209801c2d9961fc.pdf
- https://archive.aps.org/dfd/2023/a09/8

```swarm-challenge
{"claim_id": 24, "outcome": "weakened", "reason": "Arithmetic is correct (5.19x, 26.9x) and robust to CL_max, but the deficit compares a still-air airspeed to a submerged water speed: a 3.53 m/s headwind at the animal's height (~7 m/s at 10 m) closes it, surface taxiing can exceed burst speed, and the 27x KE figure is the same ratio squared, not independent evidence.", "corrected_value": "5.19 (still air, submerged burst only); general form 4.37 m/s / (0.842 m/s + U_wind at the animal's height)"}
```
