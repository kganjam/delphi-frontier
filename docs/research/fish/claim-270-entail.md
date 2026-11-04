# Claim 270: what must be true at the organ and behaviour scales

**Source claim (organism scale, evidence: derived).** "FROM THE LOW-END EXIT (0.45 m/s) it fails on WEIGHT SUPPORT, not thrust: the lobe would need CL 1.3-10 to hold the body clear of the water. Minimum supportable speed is 0.51-1.39 m/s."

- **Where it comes from.** `docs/research/fish/S32-organism.md`, §0 and §3.1, on branch `claude/s32-multi-stroke-launch-qpq9g2`. I read it as **full-text** from git.
- **What it models.** A designed zebrafish of 0.25–0.40 g with an enlarged pectoral "wing". It leaves the water and tries to taxi with only its lower caudal lobe immersed.
- **Where 0.45 m/s comes from.** S28 (`claude/s28-organism-design-5z0vjz`, full-text from git) calls it the low end of a "measured" adult burst range of 0.45–1.38 m/s, citing Miln et al. 2021. S28 says itself that this is a *swimming* burst speed, not a water-exit speed.
- **Related work I read so as not to duplicate it.** `challenge-270.md` on two branches (`claude/challenge-270-lobe-cl-nq8ftq` and `claude/challenge-claim-270-akzls7`) and `replicate-270.md` (`claude/replicate-fish-270-3e54dl`). All are full-text from git.
  - All three reproduce the arithmetic: CL_z 1.27 / 2.99 / 9.95 and U_min 0.506 / 0.771 / 1.387 m/s.
  - Both challenges rate the claim WEAKENED at the generous end.
  - Nothing below depends on their verdicts. Where I agree with them, I say so.

**Kinds of result in this document.**
- Every number labelled *measured* comes from a named paper at a stated read level.
- Every number labelled *derived* is my arithmetic on S32's inputs. It is not an observation.
- Script: `docs/research/fish/claim_270_entail_check.py` (pure Python, under 1 s).

## 0. Short answer

| # | Scale | Kind | Requirement | Status |
|---|---|---|---|---|
| 1 | organ | range | Steady (forward-speed) lift coefficient of a low-aspect-ratio fin plate cannot reach 1.27 | **satisfied**: measured CL_max 1.02 (Ribak & Gurka 2023). The species and Re do not match, so applying it here is my inference |
| 2 | organ | range | The flapping lobe's *time-averaged* vertical force, counting every mechanism, stays below the vertical need (equivalent CL_z < 1.27 referenced to U) | **unsatisfied**: nothing found bounds it. A measured mechanism, flapping-augmented mean lift (Gunnarson et al. 2019), points the *other* way. Its size at this scale and Strouhal number is unknown |
| 3 | organ | spatial | Immersed lower-lobe area < 24.0 mm² (0.25 g fish, CL_z ≤ 1, at 0.45 m/s) | **open**: adult zebrafish caudal-fin areas *have* been measured (Thambithurai et al. 2022), but no absolute value was readable. S32's 18.9 mm² is assumed |
| 4 | behaviour | range | The organism really leaves the water at 0.45 m/s or slower (≤ U_min) with the lobe still immersed | **unsatisfied**: no zebrafish water-exit speed was found. The size-matched analogue (guppy) exits at a mean of 1.02 m/s, at a steep angle |
| 5 | behaviour | timescale | The body sinks back before the lobe can accelerate it to U_min | **open** (derived only). On S32's own inputs this **fails at the generous end**: U_min is reached in 3.3 ms after sinking 0.01 mm. It holds at the central end (91 ms, 20 mm) and the stingy end (never reached) |

**Net reading (my inference, not an observation).**
- No constraint is `unsatisfiable`. I found no measured number that contradicts the claim.
- The claim's **generous endpoint** ("CL 1.3", "0.51 m/s") does not stand as a failure even on its own model:
  - Constraint 5 shows the lobe outruns the sink in a fraction of one stroke.
  - Constraint 2 has a measured mechanism that could supply the missing 27 %.
- The **central and stingy endpoints** (CL 3–10, U_min 0.77–1.39 m/s) survive every check I could make.
- That agrees with both challenge branches, but I reached it by a different route (timescale, not thrust tilt).
- Separately, the premise that a zebrafish exits at 0.45 m/s has no behavioural measurement behind it (constraint 4).

---

## 1. Constraints and checks

### C1 — organ, range: steady lift coefficient of the lobe

**Requirement.** The claim's failure verdict needs the lobe's steady vertical lift coefficient (referenced to forward speed U) to stay below the value required.
- At the generous end that value is **1.27**. This is the binding bound.
- At the central end it is 2.99, and at the stingy end 9.95.
- S32 encodes this as an *assumed* cap, CL_z ≤ 1.

**Check.**
- **Ribak & Gurka 2023**, *Sci Rep* 13:16217, doi 10.1038/s41598-023-42784-w, PMC10533810. **Read level: full-text** (Europe PMC XML).
  - They measured a 3D-printed duck-foot model, a low-aspect-ratio triangular plate, in a wind tunnel at **Re = 31,000**.
  - The authors report that "the lift coefficient increases linearly between 0° and 20° … and then increases non-linearly to **C_Lmax = 1.02 at 45°**".
  - They also compare against Hoerner's low-aspect-ratio plate and 60° delta-wing data. Those stall near 33°.
- **Inference (mine):** a measured steady CL_max of about 1.0 for a thin, low-AR biological plate is below 1.27. That satisfies the requirement.
- **Two transfer gaps weaken this.** They cut in opposite directions.
  - The lobe's chord Re at 0.45 m/s is about 2,700 (6 mm chord). That is 11× below the measured Re.
    - A search-engine summary (read level **search-summary**, primary not opened) says later flat-plate work finds CL_max falls at Re ≲ 3,000.
    - If true, that strengthens the claim.
  - The lobe is surface-piercing and flexible, and it has no hypocercal cant. None of those features is in the duck-foot test.
- **Torres & Mueller 2004.** This is the standard low-AR flat-plate CL_max dataset (AR 0.5–2, Re 7×10⁴–10⁵, per a search summary). **Read level: could-not-access**: typeset.io, jstage.jst.go.jp and cir.nii.ac.jp did not resolve from this session. I therefore quote no number from it.

**Status: satisfied** (measured, on a non-identical plate; the transfer is my inference).

### C2 — organ, range: total time-averaged vertical force from the oscillating lobe

**Requirement.** Weight support "fails" only if the lobe cannot produce the vertical need *by any route*. At 0.45 m/s that need is **2.43 mN** (generous; derived, S32 inputs), which equals an equivalent CL_z of **1.27** referenced to U.

Routes C1 does not cover:
- unsteady or flapping-augmented lift;
- thrust vectoring by a body pitched nose-up.

**Check.**
- **Gunnarson, Zhong & Quinn 2019**, *Biomimetics* 4:51, doi 10.3390/biomimetics4030051, PMC6784290. **Read level: full-text.**
  - Setup: a rigid low-AR hydrofoil (NACA 0012, c 10 cm, span 15 cm) pitching in a water channel at **Re 2.8×10⁴**, St 0–0.4, pitch bias 0–15°.
  - The authors report that "the lift coefficient of a flapping hydrofoil increases linearly with pitch bias, with a slope that increases with Strouhal number".
  - They also report that measured mean lift exceeds Theodorsen's prediction by **≳ 0.5 in C_L for pitch bias ≳ 10°**.
  - So flapping *adds* time-averaged force perpendicular to the flow, beyond the steady value. This is a measured mechanism that works **against** the claim's requirement.
  - The peak C_L values are only in their Fig. 2A, which I could not read numerically. I therefore do **not** claim that the measured mean C_L exceeds 1.27.
  - Their St (≤ 0.4) is below the lobe's St at 0.45 m/s, which is 0.73–1.00 (derived, from S32's f·A_pp = 0.33–0.45 m/s).
- **Dickinson, Lehmann & Sane 1999**, *Science* 284:1954. This is the classic measurement of delayed-stall lift on a flapping wing. **Read level: listing** (Europe PMC record only; no open full text). I quote no value from it.
- Zhao et al. 2010 (PMC2842791) and Jardin & Colonius 2018 (PMC6030621; simulated in any case): **read level: abstract/listing**. Europe PMC full-text returned HTTP 500, and NCBI efetch returned front matter only.
- **Derived, not observed:** challenge branch `claude/challenge-270-lobe-cl-nq8ftq` finds that tilting S32's own thrust vector by **6.3°** supports the generous case at 0.45 m/s.

**What I searched.** Europe PMC, for:
- "low aspect ratio" + "flat plate" + "lift coefficient";
- "delayed stall" + "lift coefficient" + flapping/revolving, open access;
- "caudal fin" + "lift" + "homocercal" + vertical force.

**Scope of the negative.** No measured upper bound on the time-averaged vertical force of a surface-piercing, oscillating caudal lobe was found, at any Re. That is "nobody I could reach has measured it", not "measured and found small".

**Status: unsatisfied.** Nothing known meets the requirement, and a measured mechanism (Gunnarson 2019) points against it. It is not `unsatisfiable`: no measured number at this scale and Strouhal number exceeds 1.27.

### C3 — organ, spatial: immersed lower-lobe area

**Requirement.** At 0.45 m/s, q = 101.25 Pa. With CL_z ≤ 1, the generous case fails only if the immersed lobe area is **below W(1 − (U/V_to)²)/q = 2.427 mN / 101.25 Pa = 23.97 mm²** (0.25 g; derived). For the 0.40 g fish the bound is 38.5 mm² (derived).

S32 uses 18.9 mm². That is half of an **assumed** 0.7 × 6 mm × 9 mm caudal fin. S32 states that no adult zebrafish fin area was found.

**Check.**
- **Thambithurai et al. 2022**, *Ecol Evol* 12:e8596, PMC8840878. **Read level: full-text.**
  - The authors measured caudal fin area on adult zebrafish from calibrated photographs. They regressed it on standard length (β = 2.31, df = 212).
  - The text reports no absolute area, mean or units for that coefficient.
  - The data would be in their supplement or deposit, which I did not reach.
- **Plaut 2000**, *J Exp Biol* 203:813, on fin size versus swimming in zebrafish. **Read level: listing** (cited inside Thambithurai 2022; not opened).
- **Cardeira da Silva et al. 2016** (PMC5171864) and **Chopra et al. 2023** (fin-area regeneration protocols). **Read level: search-summary.** The summary says the values are in figures and supplements and gives no number.

**Scope.** Absolute adult caudal-fin areas *exist in the literature* (Thambithurai's data). I could not read a value. This is a retrieval failure, not an absence.

**Status: open.** No value was read, so it cannot be compared with 24 mm².

### C4 — behaviour, range: the exit speed actually occurs

**Requirement.** The claim's scenario needs the organism to leave the water at **0.45 m/s**. More generally, it needs a speed **≤ U_min (0.506 m/s generous)** with the body airborne and the lower lobe still immersed. Otherwise the low-end case is counterfactual.

**Check.**
- **Miln, Ward & Seebacher 2021**, *R Soc Open Sci* 8:210146, PMC8025299. **Read level: full-text** (Europe PMC XML).
  - Fast starts were filmed at **120 frames/s** in a tank **30 mm deep**, and speed was taken from centre-of-mass tracking. They also report U10 flume sprints and "realized" speeds.
  - **The numerical range 0.45–1.38 m/s does not appear in the text.** It is presumably read from their Fig. 1 or the Dryad deposit (doi 10.5061/dryad.v15dv41tr; HTTP 403 from this session).
  - S28's attribution therefore cannot be confirmed or refuted at text level.
  - In any case these are underwater sprint speeds, not exit speeds. S28 says this itself.
- **Soares & Bierman 2013**, *PLoS ONE* 8:e61617, PMC3629028. **Read level: full-text.** This is the size-matched analogue: male guppies, standard length 1.85 ± 0.35 cm.
  - Jumps were filmed at 1000 frames/s (20 jumps, 5 fish).
  - Maximum in-water velocity "right before or at the moment the fishes' head broke the water/air interface": **102.36 ± 33.75 cm/s**.
  - Maximum in air: **123.57 ± 30.0 cm/s**.
  - Jump angle: **77.4 ± 24.9°**.
  - The authors state that fish "will continue with whole body thrusts and tail beats, even when out of the water".
  - The text also notes (citing ref. 24) that *Danio rerio* performs tail-flip *terrestrial* jumps. That is a different behaviour, read at citation level only.
- **Inference (mine).** The only measured small-fish water exit I found has a mean exit speed above both the generous and central U_min. It is near-vertical and ballistic, not a shallow taxi with the lobe left immersed. It does not show that 0.45 m/s exits happen.

**What I searched.** Europe PMC for zebrafish/*Danio rerio* + jump/leap + air/water surface (+ kinematics), and "fast-start" + adult zebrafish + velocity.

**Scope of the negative.** **No measured water-exit speed or exit angle for zebrafish was found.** I read the guppy paper, which is the closest analogue. That is "nobody I could reach has measured it for this species".

**Status: unsatisfied.**

### C5 — behaviour, timescale: falling back versus accelerating to U_min

**Requirement.** S32 judges support quasi-steadily, at one instant. For "fails on weight support" to describe what happens, the body's fall back into the water must be **faster** than the lobe's acceleration from 0.45 m/s to U_min. If the lobe reaches U_min first, the support deficit is transient and the taxi proceeds.

**Check (derived, not observed).** `claim_270_entail_check.py`:
- integrates S32's horizontal equation, using thrust back-solved from S32's tabulated T_lobe at 0.45 m/s, S32's C_D(Re) law, hysteresis drag, and induced drag at CL_z = 1 taken from S32's own table;
- applies the vertical deficit (lobe held at CL_z = 1) as downward acceleration.

| Case | U_min | Time to reach U_min | Sink before reaching it | Requirement |
|---|---|---|---|---|
| generous | 0.506 m/s | **3.3 ms** (0.17 of a 52 Hz stroke) | **0.01 mm** | **violated**: the deficit is outrun |
| central | 0.771 m/s | 91 ms (4.7 strokes) | 20 mm (about 0.7 SL) | holds |
| stingy | 1.387 m/s | never (decelerates) | falls | holds |

**Caveats.**
- At the generous end the time is shorter than one stroke. S32's cycle-averaged thrust law cannot resolve that timescale, so the 3.3 ms figure is not reliable in detail.
- The sign of the conclusion is robust, though. Even a 10× slower acceleration (33 ms) sinks the body only about 1 mm against a 0.52 mN deficit (derived).
- The thrust law is itself extrapolated to St ≈ 1. Both challenge branches flag this, and it applies to S32's result as much as to mine.

**No measured airborne-taxi kinematics exist for any fish of this size that I could reach.** The guppy paper reports aerial tail beats but not a sustained taxi with the lobe immersed.

**Status: open.** The check is derived, not measured. On the claim's own inputs it contradicts the generous endpoint and supports the other two.

---

## 2. Honesty ledger

- **Measured, by others, read full-text:**
  - Ribak & Gurka 2023 (C_Lmax 1.02, Re 3.1×10⁴);
  - Gunnarson et al. 2019 (flapping-augmented mean lift, Re 2.8×10⁴, St ≤ 0.4);
  - Soares & Bierman 2013 (guppy exit 1.02 ± 0.34 m/s, 77° jumps);
  - Miln et al. 2021 (methods only; the speed range was not in the text);
  - Thambithurai et al. 2022 (fin area measured; no absolute value in the text).
- **Derived by me:**
  - the 23.97 mm² and 38.5 mm² area bounds;
  - the lobe St of 0.73–1.00;
  - the C5 trajectories.
- **Inherited from S32 and assumed there:** lobe area 18.9 mm², φ, CL_z cap 1, contact angles, thrust calibration.
- **Not accessible this session:**
  - typeset.io, jstage.jst.go.jp and cir.nii.ac.jp (DNS);
  - datadryad.org and europepmc.org HTML (HTTP 403);
  - export.arxiv.org (DNS);
  - Europe PMC full-text for PMC2842791, PMC6030621 and PMC9156915 (HTTP 500).
- **Not done:**
  - I did not open Torres & Mueller 2004, Dickinson et al. 1999, Plaut 2000 or Davenport 2003.
  - I quote no number from any of them.
- **Disagreement preserved.**
  - C1 (steady CL ≤ about 1) and C2 (flapping adds lift) are both measured. They point in opposite directions for the generous case.
  - I have not averaged them. The generous endpoint is contested; the central and stingy endpoints are not.

```swarm-entail
{"source_claim": 270, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "range",
      "statement": "The steady (forward-speed) lift coefficient attainable by a low-aspect-ratio, thin fin plate must lie below the coefficient the claim says is required (binding at the generous end).",
      "quantity": "steady CL_max of the immersed lobe referenced to forward speed", "lo": null,
      "hi": 1.27, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Measured C_Lmax = 1.02 at 45 deg for a low-AR biological plate (duck-foot model) at Re 31,000; transfer to a 6 mm zebrafish lobe at Re ~2,700 is an inference.",
      "satisfied_evidence": "measured",
      "note": "Ribak & Gurka 2023 Sci Rep 13:16217, doi 10.1038/s41598-023-42784-w, full-text. Torres & Mueller 2004 could-not-access (host blocked); search-summary only that CL_max falls at Re <~3000. Different planform, Re and no free surface: satisfied for the steady branch only."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The time-averaged vertical force an oscillating, surface-piercing caudal lobe can generate by any route (flapping-augmented lift, thrust vectoring) must stay below the vertical need at 0.45 m/s.",
      "quantity": "equivalent time-averaged vertical force coefficient referenced to U (need 2.43 mN at q 101 Pa, S 18.9 mm2)", "lo": null,
      "hi": 1.27, "units": "dimensionless",
      "status": "unsatisfied",
      "satisfied_by": "Nothing found bounds it. A measured mechanism points the other way: flapping raises the mean lift of a pitch-biased hydrofoil above quasi-steady theory (>~0.5 in C_L at bias >~10 deg, St <=0.4, Re 2.8e4). Its magnitude at the lobe's St 0.73-1.00 is unknown.",
      "satisfied_evidence": "literature",
      "note": "Gunnarson, Zhong & Quinn 2019 Biomimetics 4:51 (PMC6784290), full-text; peak values only in Fig 2A, not read numerically. Dickinson et al. 1999 listing only. Derived (not observed): a 6.3 deg thrust tilt supports the generous case (branch claude/challenge-270-lobe-cl-nq8ftq). Scope: Europe PMC searches on low-AR plate lift, delayed-stall flapping lift (OA), and homocercal caudal-fin vertical force; no measurement of a surface-piercing oscillating lobe found. 'Not measured where I could reach', not 'measured and small'."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "The immersed area of the lower caudal lobe must be small enough that, at CL_z <= 1 and 0.45 m/s, it cannot carry the unsupported weight.",
      "quantity": "immersed lower-lobe area (0.25 g fish; bound is 38.5 mm2 for 0.40 g)", "lo": null,
      "hi": 23.97, "units": "mm^2",
      "status": "open",
      "satisfied_by": "S32 uses an assumed 18.9 mm2. A measured adult zebrafish caudal-fin area exists, but no absolute value was readable in the text.",
      "satisfied_evidence": "unknown",
      "note": "Thambithurai et al. 2022 Ecol Evol (PMC8840878) full-text: caudal fin area measured and regressed on SL (beta 2.31, df 212); no absolute values in text. Plaut 2000 JEB 203:813 listing. Cardeira da Silva 2016 and Chopra 2023 search-summary. This is a retrieval gap, not an absence in the literature."},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The organism must actually leave the water at a speed at or below the minimum supportable speed, with the body airborne and the lower lobe still immersed.",
      "quantity": "water-exit speed", "lo": 0.45,
      "hi": 0.506, "units": "m/s",
      "status": "unsatisfied",
      "satisfied_by": "No zebrafish water-exit speed found. Size-matched analogue (guppy, SL 18.5 mm) exits at a mean of 1.02 +/- 0.34 m/s in water and 1.24 +/- 0.30 m/s in air, at a 77 +/- 25 deg jump angle (ballistic, not a taxi). The 0.45 m/s low end is an underwater fast-start speed, not an exit speed.",
      "satisfied_evidence": "measured",
      "note": "Soares & Bierman 2013 PLoS ONE 8:e61617 (PMC3629028) full-text. Miln et al. 2021 R Soc Open Sci 8:210146 (PMC8025299) full-text: fast starts at 120 fps in 30 mm water; the 0.45-1.38 m/s range is not in the text (figure/Dryad, Dryad HTTP 403), so S28's attribution is unverified at text level. Scope: Europe PMC zebrafish jump/leap/water-surface/kinematics and fast-start velocity searches; no zebrafish exit measurement found."},
    {"target_scale": "behaviour", "kind": "timescale",
      "statement": "The airborne body must sink back into the water faster than the lobe's thrust can accelerate it from the exit speed to the minimum supportable speed; otherwise the support deficit is transient.",
      "quantity": "time to reach U_min from 0.45 m/s compared with the fall-back time (generous / central / stingy: 3.3 ms and 0.01 mm sink / 91 ms and 20 mm / never)", "lo": null,
      "hi": null, "units": "ms",
      "status": "open",
      "satisfied_by": "Derived only, on S32's own inputs: violated at the generous end (U_min reached in 3.3 ms, 0.17 stroke, after a 0.01 mm sink); holds at the central and stingy ends. No measured airborne-taxi kinematics for a fish of this size.",
      "satisfied_evidence": "derived",
      "note": "docs/research/fish/claim_270_entail_check.py. The generous-end timescale is shorter than one stroke, where S32's cycle-averaged thrust law does not apply; the sign survives a 10x slower acceleration (~1 mm sink, derived). The thrust law is extrapolated to St ~1. No measurement found; the guppy paper (full-text) reports aerial tail beats but no immersed-lobe taxi."}
  ]}
```
