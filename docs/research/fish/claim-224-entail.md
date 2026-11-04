# Claim 224: what it requires at the organ and behaviour scales

**Source claim (organism scale, evidence: derived).**
A 0.4 g body at 4.37 m/s needs 3.82 mJ (9.55 J/kg). With 6.5% in-water drag, the best measured
C-start hydromechanical efficiency of 0.37 and 0.93 tendon return, the spring must store 11.8 mJ
(29.6 J/kg).

**Adjacent scales:** organ, behaviour.

**Status of this document.** I wrote down five constraints and checked each against the literature.
None is `satisfied` and none is `unsatisfiable`. Four are `unsatisfied`, each with a stated search
scope. One (C3) has two sources that disagree, and I record both. All literature access in this session was
at **search-summary** level. Direct fetches of journal pages (cob.silverchair.com,
open.library.ubc.ca, sciencegate.app) failed because those hosts are outside this session's network
allow-list. So no number below was read from a full text or from an abstract I opened myself. Every
literature number carries that limitation.

---

## 0. Re-deriving the claim's arithmetic (calculation, not observation)

| Quantity | Calculation | Result |
|---|---|---|
| Kinetic energy | ½ · 0.0004 kg · (4.37 m/s)² | 3.819 mJ, i.e. 9.55 J/kg ✔ |
| Required spring store | 3.819 mJ · 1.065 / (0.37 · 0.93) | 11.82 mJ, i.e. 29.55 J/kg ✔ (the claim rounds to 29.6) |

The arithmetic reproduces. It is **calculated**. Every input (mass, speed, 6.5% drag, 0.37, 0.93)
is an assumption taken from the claim. I did not re-measure any of them here.

Two further derived quantities are used below. Both are **calculations, not observations**:

- **Body length.** For a 0.4 g fish with condition factor K ≈ 1 (assumed): L ≈ (0.4/0.01)^(1/3) ≈ 3.4 cm.
  Then 4.37 m/s ≈ **128 body lengths/s**.
- **Power without a spring.** If 3.82 mJ · 1.065 / 0.37 = 11.0 mJ of muscle work had to be delivered
  directly within an assumed 10, 20 or 40 ms propulsive window, the required muscle power at an assumed
  muscle mass fraction of 0.5 is 5,500, 2,750 or 1,370 W/kg muscle. This calculation is what motivates
  the spring at all. Compare the measured in-vivo peak instantaneous fast-muscle power of
  **307 W/kg** (C-bend) and **222 W/kg** (contralateral contraction) in *Myoxocephalus scorpius*
  (James & Johnston 1998, J. Exp. Biol. 201:913–923; read-level: search-summary).
  Wakeling & Johnston (1998, J. Exp. Biol. 201:1505–1526; read-level: search-summary) report a mean
  of 142.7 W/kg at 20 °C. *My inference, not the authors' claim:* the measured direct muscle power
  falls short of the required power by about one order of magnitude. If the 4.37 m/s figure is real,
  some power amplifier is therefore required, which is what the claim asserts.

---

## 1. Constraints

### Organ scale

**C1 · energetic.** An elastic element must exist in the propulsive apparatus that stores
**≥ 11.8 mJ (≥ 29.6 J/kg body)** and returns ≥ 93% of it, and it must be loaded before release.

- *Status:* **unsatisfied** (with a scope).
- *What I found:* latch-mediated spring actuation in fishes is documented for **feeding strikes in
  Syngnathiformes**. In seahorses, mass-specific suction power is reported at about 3× the maximum
  recorded for any vertebrate muscle. The sternohyoideus tendon is reported to release about 72% of the
  power that accelerates water into the mouth, and epaxial tendons act as the spring for head rotation
  ("A power amplification dyad in seahorses", PMC10089724; read-level: search-summary). Snipefish use
  a similar latched tendon recoil for feeding (read-level: search-summary, popular-press report).
  These systems rotate the head. They are not trunk/axial locomotor springs, and I found no stored-energy
  figure for them in J/kg body mass.
- *Scope of the negative:* web searches for elastic energy storage, tendon, myosepta, power
  amplification and catapult in combination with "fish fast-start". I also searched for fish
  myoseptal-tendon stiffness and material properties (Summers & Koob 2002, Comp. Biochem. Physiol.
  133A:1159–1170, found as a listing only, content not read) and for tendon strain-energy density.
  For tendon energy density I found only mammalian and avian data, and no J/kg value I could quote.
  I found **no measurement** of elastic energy stored in, or returned from, axial or myoseptal tendons
  during a teleost C-start. This is "not found in my searches", **not** "people looked and found
  nothing". The full texts of the myoseptal-tendon literature were not read.
- *Modelling only (simulated, not observed):* Richards & Sawicki (SICB abstract, sicb.org/?p=23880;
  read-level: search-summary) model a Hill-type muscle–tendon unit driving a fin in water. Under some
  conditions it gives about 18% more power than muscle alone. A related robotic study (sicb.org/?p=21951;
  read-level: search-summary) gives up to about 33% above the muscle-only limit, with no gain in swimming
  speed. Both figures are far below the ~10× amplification computed in §0.

**C2 · range.** The muscle work delivered into the spring during loading must be
**≥ 29.6 J/kg body**. At an assumed fast-muscle fraction of 0.4–0.6 of body mass, that is
**≈ 49–74 J/kg muscle** (calculated) in one loading contraction.

- *Status:* **unsatisfied**. This status is **not** `unsatisfiable`, and the reason is stated below.
- *Measured values found:*
  - Net work per cycle of sculpin fast fibres under optimal strain and stimulation is **3.5 J/kg**
    (Johnston et al. 1993; read-level: search-summary).
  - Another work-loop study reports **2.7 J/kg at 15 °C** (search-summary; the species was not identified
    in the summary).
  - In-vivo peak instantaneous power is 307 W/kg (James & Johnston 1998, above). I found no in-vivo work
    per C-bend in J/kg.
- *Why not unsatisfiable:* the 2.7–3.5 J/kg figures are **net cyclic work under sinusoidal work loops**.
  They are not the maximum work of a single slow loading contraction against a spring, which is what
  C2 bounds. The measured values are one order of magnitude below the requirement, but they measure a
  different quantity, so they do not contradict it. *My inference:* this is the most likely place for
  the claim to fail. A single-contraction maximum-work measurement for teleost fast muscle would settle
  it, and I did not find one.
- *Scope:* searches for fish fast-muscle work per cycle and fast-start work-loop maxima. No full texts
  were read.

**C3 · range.** The efficiency of converting stored elastic energy into forward kinetic energy
(hydromechanical) must be **≥ 0.37** (with the 0.93 tendon return applied separately).

- *Status:* **unsatisfied, with sources in disagreement**. I have not averaged the two sources.
- *Source A (live fish):* Frith & Blake 1995 (J. Exp. Biol. 198:1863–1873) report northern pike C-start
  hydrodynamic efficiency of **0.37 on average (range 0.34–0.39)**, and 0.27 (range 0.16–0.37) for
  S-starts. Read-level: search-summary of a UBC library record; the record may be the thesis version.
  As reported, their efficiency relates **muscle mechanical power output to inertial/hydrodynamic power**.
  It is not defined as kinetic energy over stored elastic energy. The same abstract states, as the
  **authors' claim**, that "power output during fast-starts appears limited by muscle physiology". That
  statement is in tension with a spring-amplified start.
- *Source B (mechanical fish, not a live animal):* a pike-shaped robotic fish (MIT, DSpace 1721.1/39203
  and related; read-level: search-summary) defines efficiency as **final kinetic energy ÷ potential
  energy initially stored in the body beam**. It reports **≈ 0.10**. Related models report 0.11–0.12.
  This is the definition the claim's chain actually needs, and it is about 3.7× lower than 0.37.
  It is a measurement on an **engineered analogue**, not on a fish, so I do not treat it as refuting C3.
- *Consequence (calculated):* with 0.10 in place of 0.37, the required store becomes **43.7 mJ
  (109 J/kg body)**. With 0.12 it becomes 36.4 mJ (91 J/kg). Either value makes C1 and C2 harder by the
  same factor.
- *My inference:* the claim's label "best measured C-start hydromechanical efficiency" uses Source A's
  number under Source B's definition. Which definition applies is unresolved here.

### Behaviour scale

**C4 · timescale.** Spring loading must be **slower than, and must precede**, release. A
latched or held preparatory phase (t_load ≫ t_release) must therefore appear in the behaviour before
the propulsive stroke. The release must fall within the propulsive stage of the start.

- *Status:* **unsatisfied**.
- *What I found:* the descriptions of C-starts that I found (Domenici & Blake 1997 review, J. Exp. Biol.
  200:1165–1178, listing only; zebrafish larval inverse-dynamics work by Voesenek et al. 2019, J. Exp.
  Biol. 222:jeb203091, search-summary) describe stage 1 as a muscle-driven bend into a C, stage 2 as
  straightening and propulsion, with propulsive force peaking in stage 2. Neither describes a held,
  latched pre-load. Latched pre-load is documented in fishes for syngnathiform **feeding** (see C1).
- *Scope:* searches on C-start stage structure and stage-1 duration for zebrafish, killifish, archerfish
  and the Domenici & Blake review. I did **not** obtain a stage-1 duration in ms from any source, and I
  did not read any full text. "No latch phase was described in the summaries I saw" is weaker than
  "a latch phase has been shown to be absent", and I claim only the former.

**C5 · range.** The behaviour must reach a take-off speed of **≈ 4.37 m/s** for a body of about 0.4 g
(about 3.4 cm, calculated), i.e. **≈ 128 body lengths/s**.

- *Status:* **unsatisfied**.
- *Measured values found:* in seven teleost species, maximum fast-start sprint speeds were *estimated*
  at **6.5–17.8 L/s** (Webb, "Fast-start performance and body form in seven species of teleost fish",
  J. Exp. Biol. 74:211; read-level: listing/search-summary). Archerfish predictive starts exceed
  **20 L/s** (read-level: search-summary). Terrestrial tail-flip jumps of killifishes take off at about
  45° (Minicozzi et al. 2024, Integr. Comp. Biol. 65:107–118, doi:10.1093/icb/icae155; read-level:
  search-summary). I obtained no take-off speed in m/s from that paper.
- *Why not unsatisfiable:* the measured L/s values come from larger fish. Relative speed is reported to
  rise as body size falls, and none of the measurements I found is on a ~0.4 g fish. So the gap does not
  contradict the requirement. Even so, the gap is large: 128 L/s is about 6–20× the values found.
- *Scope:* searches for small-fish C-start and leap take-off velocities, killifish jump allometry and the
  Domenici & Blake review. None of the summaries gave a measured m/s value for a fish of about 0.4 g.

---

## 2. Summary for the ledger

- The organism-level arithmetic reproduces (calculated).
- No constraint is satisfied by a named, measured mechanism.
- The pressure point is **C2/C3 together**. The measured fish fast-muscle work figures are cyclic
  values of 2.7–3.5 J/kg, about 10–20× below the loading requirement of roughly 50–75 J/kg muscle,
  although they are not the same quantity. Separately, the only efficiency measured under the claim's own
  definition (a robot, 0.10) would raise the requirement by about 3.7×.
- Nothing measured on a fish contradicts the claim, so nothing is `unsatisfiable`. The decisive
  measurements would be:
  1. single-contraction maximum work of teleost fast muscle;
  2. energy stored in axial or myoseptal tendons during a C-start;
  3. kinetic energy over stored energy in a live fish.

None of these three was found in the searches stated above.

## 3. Sources (all read-level: search-summary unless stated)

- Frith & Blake 1995, J. Exp. Biol. 198:1863–1873 (UBC record): search-summary.
- James & Johnston 1998, J. Exp. Biol. 201:913–923: search-summary.
- Wakeling & Johnston 1998, J. Exp. Biol. 201:1505–1526: search-summary.
- Johnston et al. 1993 (sculpin fast-fibre work loops): search-summary.
- Seahorse power amplification dyad, PMC10089724: search-summary.
- MIT mechanical pike, DSpace 1721.1/39203: search-summary.
- Richards & Sawicki, SICB abstract sicb.org/?p=23880; sicb.org/?p=21951: search-summary.
- Webb, J. Exp. Biol. 74:211: listing.
- Domenici & Blake 1997, J. Exp. Biol. 200:1165–1178: listing.
- Voesenek et al. 2019, J. Exp. Biol. 222:jeb203091: search-summary.
- Minicozzi et al. 2024, Integr. Comp. Biol. doi:10.1093/icb/icae155: search-summary.
- Summers & Koob 2002, Comp. Biochem. Physiol. 133A:1159–1170: listing.
- Direct fetches failed (could-not-access; host not on the network allow-list): cob.silverchair.com,
  open.library.ubc.ca, www.sciencegate.app.

```swarm-entail
{"source_claim": 224, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "energetic",
      "statement": "An elastic element in the propulsive apparatus must store at least the required energy before release and return >=93% of it",
      "quantity": "elastic energy stored per body mass", "lo": 29.6, "hi": null, "units": "J/kg body",
      "status": "unsatisfied",
      "satisfied_by": "Searched fish fast-start + elastic storage/tendon/myosepta/power amplification/catapult and fish tendon material properties. Found latched tendon springs only in syngnathiform feeding strikes (head rotation), not in axial/locomotor C-starts; no measured stored energy in axial tendons during a C-start found.",
      "satisfied_evidence": "unknown",
      "note": "Seahorse power amplification dyad PMC10089724 (search-summary); Summers & Koob 2002 CBP 133A:1159 (listing only). Modelling: Richards & Sawicki SICB (simulated, ~18% amplification). Negative is 'not found in my web searches, full texts not read', not 'shown absent'."},
    {"target_scale": "organ", "kind": "range",
      "statement": "Muscle must deliver at least the stored energy as work in a single loading contraction",
      "quantity": "muscle work per loading contraction per muscle mass (at assumed muscle fraction 0.4-0.6)", "lo": 49, "hi": 74, "units": "J/kg muscle",
      "status": "unsatisfied",
      "satisfied_by": "Measured fish fast-muscle net cyclic work 2.7-3.5 J/kg and in-vivo peak power 307 W/kg found; no single-contraction maximum work for teleost fast muscle found. Cyclic net work is a different quantity, so it does not contradict the bound.",
      "satisfied_evidence": "measured",
      "note": "Johnston et al. 1993 sculpin 3.5 J/kg per cycle; 2.7 J/kg at 15 C (species unidentified); James & Johnston 1998 JEB 201:913 (307/222 W/kg); all search-summary. lo/hi are the required lower bound evaluated at muscle fractions 0.6 and 0.4 (calculated)."},
    {"target_scale": "organ", "kind": "range",
      "statement": "Conversion efficiency of stored elastic energy to forward kinetic energy must be at least the value assumed in the claim",
      "quantity": "stored-energy-to-kinetic-energy hydromechanical efficiency", "lo": 0.37, "hi": 1.0, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "Sources disagree: live pike 0.37 (0.34-0.39) but defined as muscle power vs inertial power, not KE/stored energy; mechanical pike robot defined as KE/stored beam energy gives ~0.10 (0.11-0.12 in related models). At 0.10 the required store becomes 43.7 mJ (109 J/kg), calculated.",
      "satisfied_evidence": "measured",
      "note": "Frith & Blake 1995 JEB 198:1863 (search-summary of UBC record; authors also state fast-start power appears muscle-limited); MIT DSpace 1721.1/39203 (search-summary; engineered analogue, not a fish, so not treated as refutation)."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "Spring loading must precede and be slower than release: a held/latched preparatory phase must occur before the propulsive stroke, with release inside the propulsive stage",
      "quantity": "t_load / t_release", "lo": 1, "hi": null, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "C-start descriptions found (stage 1 muscle-driven bend, stage 2 propulsion) describe no latched pre-load; latched pre-load in fishes found only for syngnathiform feeding.",
      "satisfied_evidence": "unknown",
      "note": "Domenici & Blake 1997 JEB 200:1165 (listing); Voesenek et al. 2019 JEB 222:jeb203091 (search-summary). No stage-1 duration in ms obtained; negative is 'not described in summaries seen', not 'shown absent'."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The escape/leap behaviour must reach the claimed take-off speed for a body of this size",
      "quantity": "take-off speed (about 128 L/s for a 3.4 cm body, calculated)", "lo": 4.37, "hi": null, "units": "m/s",
      "status": "unsatisfied",
      "satisfied_by": "Found estimated max fast-start speeds 6.5-17.8 L/s in seven larger teleosts and >20 L/s in archerfish; no measured take-off speed for a ~0.4 g fish found. Size mismatch means no contradiction.",
      "satisfied_evidence": "measured",
      "note": "Webb JEB 74:211 (listing/search-summary); archerfish predictive start (search-summary); Minicozzi et al. 2024 ICB doi:10.1093/icb/icae155 (search-summary, no m/s value obtained). Scope: web searches on small-fish C-start and leap take-off velocity."}
  ]}
```
