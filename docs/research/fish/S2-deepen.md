# S2-D: deepening "what lift-to-drag is physically available at Re 10³–10⁴?"

**Parent.** S2 (organism), `docs/research/fish/S2-low-reynolds-aero.md` on branch
`claude/s2-low-reynolds-aero-acdwr7`. The task prompt that started this work quoted the S2 answer
as blank. I took the answer from that file, which I read in full, rather than from the prompt.

**What S2 concluded**, as I read it (S2 §4 and §7):
- (a) The steady **wing-alone L/D ceiling is ≈ 6–7**. This comes from the locust (Jensen 1956, as
  relayed by Wang 2004) and from a dragonfly forewing value of 5.8. Both are read-level **S**
  (relayed).
- (b) The **whole animal, a fin wing plus a fish body, gets ≈ 3–5**. S2 calls this "an
  engineering estimate, not a measurement or a computation from data".
- (c) From a 0.5 m launch, **L/D barely matters**.

**Everything numerical below is computed** by `S2D_calcs.py` in this directory (run with
`python3 -I docs/research/fish/S2D_calcs.py`). None of it is an observation. I ran no experiment.

---

## 1. Which input is the answer most sensitive to? (computed)

S2's 3–5 had no explicit model behind it. To test its sensitivity, I first had to make the inputs
explicit. I used the standard parabolic polar for the whole animal:

`L/D_max = 1 / (2·√(CD0_eff · k))`, where `CD0_eff = CD0_wing + CdA_body/S` and
`k = 1/(π·e·AR)`.

The baseline uses S2's own geometry and numbers:
- S = 9 cm² (two fins, each 3 × 1.5 cm): **assumed** in S2.
- AR = b²/S = 4: **assumed**.
- e = 0.7: **assumed**, never retrieved.
- CD0_wing = 0.05: S2's implicit value, from Kesel 2000's "CD,min < 0.06".
- Body drag area 0.21 cm²: **computed** from laminar friction × a form factor of 1.5 on an
  assumed 32 × 7 × 4 mm ellipsoid plus 2 cm² of median fins. All of that geometry is assumed.

This baseline gives a **wing-alone L/D_max of 6.63 and a whole-animal value of 5.49**, at
CL* = 0.80. Wing-alone matches S2's "6–7". Whole-animal sits just above S2's 3–5. The model
reproduces S2's ceiling, but **the agreement shows the model is consistent with S2. It does not
validate either one.**

Each input multiplied by 0.5 and by 2 (computed):

| input | ×0.5 → whole-animal L/D | ×2 → whole-animal L/D | swing |
|---|---|---|---|
| **e·AR (effective aspect ratio)** | **3.88** | **7.76** | **2.00** |
| e alone (×2 capped at e = 1) | 3.88 | 6.56 | 1.69 |
| CD0_wing (profile drag) | 6.77 | 4.23 | 1.60 |
| body drag area | 5.98 | 4.78 | 1.25 |

AR and e enter only as their product, so they are one input: **effective aspect ratio, e·AR**.
A factor-of-2 error in it moves the whole-animal L/D from 5.5 to **3.9 or 7.8**. That is the
only input whose ×2 error crosses **both** edges of S2's answer: below the 3–5 band's midpoint
on one side, above the 6–7 "ceiling" on the other. Profile drag comes second; its swing is
diluted by body drag. Body drag comes last.

Controls in the script:
- **Known answer:** CD0 ×4 with no body drag must halve L/D exactly. It does.
- **Must-fail direction:** doubling body drag must lower L/D. It does.

**Answer to step 1:** the answer is most sensitive to the **effective aspect ratio e·AR** of a
fin-derived wing. Profile drag CD0 at the operating Re is the runner-up.

## 2. How well is that input established?

| Input | Value used | Evidence level | Read-level | Honest status |
|---|---|---|---|---|
| AR of a zebrafish pectoral-fin wing | 4 (two 3 cm × 1.5 cm fins) | **assumption** | n/a | S2 §3 states it as "assumed per-wing span/chord ≈ 2". It was labelled honestly as an assumption. It was *not* repeated as a measurement. |
| span efficiency e | 0.7 | **assumption** | n/a | Never retrieved, in S2 or here. |
| AR implied by the 6–7 "ceiling" | that of a locust or dragonfly wing | **proxy** | locust AR: `unknown` (not retrieved) | This is the subtle problem. S2's ceiling of 6–7 was measured on **insect wings**, whose planforms are not fin planforms. Importing that number as "what is physically available" silently imports the insect's aspect ratio. |
| Zebrafish adult pectoral fin span, chord or area | — | **unmeasured in anything I could reach** | — | See the negative search below. |

**Negative search (scope stated).**
- Europe PMC REST, two queries:
  - `"zebrafish" AND "pectoral fin" AND ("aspect ratio" OR "fin area" OR "fin width") AND adult AND OPEN_ACCESS:y`
    returned 23 hits.
  - `"pectoral fin" AND "aspect ratio" AND (Danio OR cyprinid OR zebrafish)` returned 16 hits.
  - I read only the titles (read-level: listing). No title reported adult zebrafish pectoral fin
    planform dimensions.
- Two earlier repo documents had already searched for the same thing and found nothing:
  - S6 (`claude/s6-fin-ray-load-kqweu7`, `S6-organ.md`) found no measured *D. rerio* pectoral fin
    span or chord, searching web plus PMC full text.
  - challenge-40 (`claude/daane-fin-area-challenge-*`) read Daane et al. 2021 (PMC9172250) in full
    text. That paper reports pectoral fin **length / SL** only, with no area, width or aspect
    ratio.
- This is a negative result about what I could reach. It is not a claim that no measurement
  exists.

**Answer to step 2:** the most sensitive input is an **assumption**. Its measured stand-in (the
insect-wing L/D) is a **proxy** from a different planform. **It has never been measured for a
zebrafish fin.**

## 3. Going after it

### 3a. Effective aspect ratio: could not improve it from the literature

- **Planform.** I found no zebrafish fin AR (scope above). For this deliverable, AR therefore
  stays a design variable, and I scan it instead of guessing it (§4).
- **The measurement that would settle the planform.** Photograph the spread pectoral fins of
  about 10 anaesthetised adult zebrafish on a millimetre grid (dorsal view, fin held at full
  abduction) and compute span, area and AR = b²/S.
  - Cost: **hours of work on existing lab fish**, with a dissecting scope or a phone camera.
    Under $100 in consumables. (Inference: no specialised equipment is needed.)
- **The measurement that would settle e, and profile drag, together.** Measure a polar of an
  excised fin, or a ray-and-membrane replica, at the operating Reynolds number.
  - **This can be done in water.** At c = 15 mm and Re = 3,000, the water speed is
    U = Re·ν/c = 3,000 × 1.0×10⁻⁶ / 0.015 = **0.20 m/s** (computed; ν_water ≈ 1.0×10⁻⁶ m²/s,
    remembered textbook value).
  - The dynamic pressure would be about 0.5 × 1000 × 0.2² = **20 Pa**, against about **5.4 Pa**
    for air at 3 m/s (computed). So a water test loads the fin about 3.7× harder than the air
    case would. That is a known bias, and it needs to be stated alongside the result.
  - Cost: a small flume and a 6-axis micro force/torque sensor. **Weeks, and an equipment budget I
    have not priced**: `unknown`. I did not retrieve sensor prices.

### 3b. Profile drag at the operating Re: improved

This is the runner-up input, and the one where I could reach the primary literature at a
higher read-level than S2 did. In this session the publisher's article pages loaded through the
fetch tool. In S2's session they were blocked.

| Source | Read-level now (S2's) | Authors' claim, verbatim from the abstract |
|---|---|---|
| Wakeling & Ellington 1997, *J Exp Biol* 200:543–556, doi 10.1242/jeb.200.3.543 | **abstract**, fetched from journals.biologists.com (was **S**) | "The drag coefficient at zero angle of attack ranged between 0.07 and 0.14, being little more than the Blassius value predicted for flat plates." Measured on isolated wings "at Reynolds numbers of 700–2400 for the wings". "The maximum lift coefficients (CL,max) were 1.07 for S. sanguineum and 1.15 for C. splendens". In free glides: "The maximum lift coefficient (CL) recorded from these glides was 0.93". **No L/D or glide angle is stated in the abstract.** |
| Kesel 2000, *J Exp Biol* 203:3125–3135, doi 10.1242/jeb.203.20.3125 | **abstract**, fetched (was **A** via search summary) | "all cross-sectional geometries have very low drag coefficients (CD,min<0.06) closely resembling those of flat plates", at "Re of 7880 and 10 000". No per-profile L/D or CL,max appears in the abstract. |
| Okamoto, Yasuda & Azuma 1996, *J Exp Biol* 199:281–294, doi 10.1242/jeb.199.2.281 | **abstract**, fetched (was **A**) | Wind-tunnel and glider free-flight tests "with Reynolds numbers (Re) as low as 10³ to 10⁴". **No numbers appear in the abstract.** The full text is paywalled. |
| Jensen 1956, *Phil Trans R Soc B* 239:511, doi 10.1098/rstb.1956.0009 (the locust L/D 6–7) | **could-not-access**: the publisher page returned HTTP 403; the relay copy (Wang 2004 PDF at dragonfly.tam.cornell.edu) was outside the allowed network | Still **S**. The locust L/D ceiling remains relayed and unread. |
| Dragonfly forewing 5.8 vs hindwing 17.9 (S2's unattributed review) | could-not-access | **The disagreement is preserved, not resolved.** A 17.9 on any wing in this band would break the 6–7 ceiling. I could not trace whose polar it is. |

Hosts that did not resolve in this session, so the fetch tool could not reach them:
- `cob.silverchair.com` (Kesel full-text PDF)
- `typeset.io` (Wang 2004 copy)
- `dragonfly.tam.cornell.edu`
- `jaxa.repo.nii.ac.jp` (a corrugated-vs-flat-plate record)

Each of these has to be allowed in the session's network settings before it can be read.

**Search-tool controls (rule 8).**
- Europe PMC: the positive control `AUTH:"Kesel" AND TITLE:"aerodynamic"` returned the 2000 paper
  (1 hit).
- Europe PMC: the must-fail gibberish query `zzqxjv wqpzzk flurbo` returned 0 hits.
- One caution on the fetch tool: it served an unrelated turtle abstract when given a guessed JEB
  URL. Only the URLs reached by **resolving the DOI** were accepted here.

**What the improved input says.**
- **Authors' claim.** Real dragonfly wings at Re 700–2,400 have CD(α = 0) = 0.07–0.14, "little
  more than" Blasius.
- **My inference.** I model profile drag as **CD0 = λ · 2·1.328/√Re** (Blasius, both sides).
  Taking "little more than" at face value gives **λ ≈ 1.0–1.4**.
  - The bracket rests on this check: Blasius gives 0.100 at Re 700 and 0.054 at Re 2,400
    (computed). The measured 0.07–0.14 then sits at 1.3–1.4× Blasius if the values pair with
    Re in the natural order.
  - Without the full text I cannot pair each CD with its Re. With the worst pairing, λ ranges
    from 0.7 to 2.6. That is why the recompute below also runs **λ = 2.0**.
- **Consistency with Kesel.** On the λ model, Kesel's CD,min < 0.06 at Re 8,000–10,000 is
  consistent (Blasius gives 0.027–0.030 there). The two sources do **not** disagree once Re is
  accounted for. They measured different Re, and **S2's single "CD_min ≈ 0.05–0.06" was taken at
  Re ~10⁴, which is 3–4× above where the fish operates.**

## 4. Recompute (computed)

The operating point is solved self-consistently: wing loading sets V, V sets Re, and Re sets
CD0. Everything else is as in §1.

**Wing-alone and whole-animal L/D_max, AR = 4 (S2's planform):**

| λ (× Blasius) | Re at optimum | CD0_wing | wing-alone L/D | whole-animal L/D | CL* |
|---|---|---|---|---|---|
| 1.0 (clean laminar plate) | 3,009 | 0.048 | 6.74 | 5.48 | 0.80 |
| 1.4 (W&E "little more than Blasius") | 2,814 | 0.070 | **5.60** | **4.79** | 0.92 |
| 2.0 (rough / worst pairing) | 2,603 | 0.104 | 4.60 | 4.10 | 1.07 (at the measured steady CL,max) |

**Scan over the unmeasured effective aspect ratio** (λ = 1.4, e = 0.7). CL is capped at 0.9,
about 85% of W&E's CL,max of 1.07; the margin is my assumption:

| AR | e·AR | whole-animal L/D | wing-alone L/D |
|---|---|---|---|
| 1.5 | 1.05 | 3.15 | 3.63 |
| 2 | 1.40 | 3.56 | 4.11 |
| 3 | 2.10 | 4.24 | 4.89 |
| 4 | 2.80 | 4.80 | 5.56 |
| 6 | 4.20 | 5.74 | 6.86 |
| 8 | 5.60 | 6.37 | 7.77 |

Without the cap, AR 8 at λ = 1.4 or 2.0 would put CL* at 1.36–1.59. That is above every steady
CL,max measured in this band, so the uncapped §3 rows for AR 8 are **not physically available**.

**Downstream: glide from 0.5 m, 2 m/s horizontal launch, CL = 0.6.** This reuses S2's
integrator, but drag is now recomputed from the local Re at every step:

| case | range |
|---|---|
| S = 9 cm², S2 fixed L/D = 6 / 3 | 23.5 / 22.0 BL |
| S = 9 cm², Re-dependent drag, λ = 1.0 / 1.4 / 2.0 | 23.1 / 22.7 / 22.2 BL |
| S = 18 cm², S2 fixed L/D = 6 / 4 | 63.0 / 36.7 BL |
| S = 18 cm², Re-dependent drag, λ = 1.4 / 2.0 | **39.7 / 33.8 BL** |
| wingless ballistic | 16.0 BL |

The script also asserts a control: the fixed L/D = 6 case reproduces S2's 0.94 m.

## 5. Verdict: **STANDS**, with one sub-claim weakened

- **(b) Whole-animal L/D ≈ 3–5: stands.** With the improved, Re-matched profile drag, the
  computed whole animal gives **4.1–5.5 at S2's AR of 4**, and **3.2–4.8 for AR 1.5–4**. Those
  are planforms a pectoral fin could plausibly have, though the actual planform is unmeasured.
  The band is right. It could sit up to about 0.5 higher for a clean laminar fin.
- **(a) The "6–7 ceiling" stands as an insect-wing number. It overstates what a fin planform can
  reach.**
  - At AR 4, the computed wing-alone value is **5.6** (range 4.6–6.7).
  - A fin wing reaches 6–7 only with AR ≥ 6 or a perfectly laminar surface.
  - This is inference from a model. The 6–7 itself is still read-level S (Jensen not accessed).
  - The unresolved dragonfly 5.8-vs-17.9 conflict could still overturn it from above.
- **(c) "L/D barely matters from 0.5 m": strengthens for the 4.5–9 cm² wings.** Once drag rises
  correctly at the low speeds of the launch transient, the range spread is 22.2–23.1 body
  lengths, against S2's 22.0–23.5.
- **S2's best case falls.** S2's top figure of 63 body lengths (18 cm², L/D 6) assumed an L/D
  that the recompute does not support at AR 4. Its replacement is **34–40 body lengths**
  (computed).

**What remains weakest.** The answer's most sensitive input, effective aspect ratio, is
**still an assumption**. I improved the runner-up input (profile drag, from S to abstract-level
and Re-matched). I did **not** improve the input that matters most. The measurements in §3a would
settle it:
- fin planform photographs: hours, under $100;
- a water-flume polar at 0.2 m/s: weeks, cost `unknown`.

Until one is done, the honest statement is a function, not a number: **whole-animal L/D ≈ 3–5 for
e·AR ≈ 1–3, rising toward 6 only if the fin's effective aspect ratio is ≳ 4**.

## Sources

| Source | Read-level |
|---|---|
| S2-low-reynolds-aero.md and S2_calcs.py (branch `claude/s2-low-reynolds-aero-acdwr7`) | full-text |
| Wakeling & Ellington 1997, doi 10.1242/jeb.200.3.543, https://journals.biologists.com/jeb/article/200/3/543/20259/ | abstract |
| Kesel 2000, doi 10.1242/jeb.203.20.3125, https://journals.biologists.com/jeb/article/203/20/3125/8553/ | abstract |
| Okamoto, Yasuda & Azuma 1996, doi 10.1242/jeb.199.2.281, https://journals.biologists.com/jeb/article/199/2/281/7462/ | abstract |
| Jensen 1956, doi 10.1098/rstb.1956.0009 | could-not-access (HTTP 403) |
| Wang 2004, *J Exp Biol*, "The role of drag in insect hovering" (PMID 15498960) | listing (Europe PMC); PDF could-not-access |
| Daane et al. 2021, PMC9172250 (via challenge-40 in this repo) | full-text, read by that document's author, not by me; I am relaying their read |
| S6-organ.md (branch `claude/s6-fin-ray-load-kqweu7`), the scope of the earlier negative search for fin dimensions | full-text |
| Europe PMC search listings cited in §2 | listing |

```swarm-result
{"subproblem": "S2-D", "evidence": "computed from abstract-level measured profile drag (Wakeling & Ellington 1997, CD(alpha=0) 0.07-0.14 at Re 700-2,400); the most sensitive input (effective aspect ratio of a fin wing) remains an unmeasured assumption", "answer": "With Re-matched profile drag, a fin-wing fish gets a computed whole-animal L/D of about 3-5 (4.1-5.5 at AR 4, 3.2-4.8 for AR 1.5-4), so S2's band stands, but the 6-7 'ceiling' is an insect-planform number a fin reaches only if its effective aspect ratio is at least about 4, which nobody has measured.", "key_number": "profile drag CD0 = 0.07-0.14 at Re 700-2,400 (measured, abstract-level), i.e. about 1.0-1.4x laminar Blasius, giving CD0 of about 0.07 at the operating Re of about 2,800; effective aspect ratio e*AR = unknown (assumed 2.8)", "verdict": "stands"}
```
