# S20-D — Deepening S20 (ecology): would flight pay for a zebrafish?

Parent: `docs/research/fish/S20-ecology.md` (branch `origin/claude/zebrafish-flight-ecology-z4f08c`).
Arithmetic: `docs/research/fish/S20-deepen_calc.py`. Run it from the repository root. Every number
below that is not attributed to a source is a **calculation** from that script, not an observation.
Date: 2026-11-04.

**What S20 said.** A launch through 0.1–1 m of air would cost a zebrafish about 10⁻⁴ to 10⁻³ of its
daily standard metabolism (SMR). That cost is *derived*. The predation benefit that would make such
a launch pay is *unknown*, and probably absent. Evidence level: `unknown`.

---

## 1. Which input is the answer most sensitive to? (recomputed)

S20 makes two claims. Each is recomputed below with every input set to ×0.5 and ×2. The full output
is in the script, section 1.

**(a) "A launch is energetically almost free."** Cost per launch as a fraction of SMR is
½·m·g·d / (η·E_SMR), which is linear in every input:

| Input changed (×0.5 or ×2) | Cost per 1 m launch ÷ daily SMR |
|---|---|
| none (S20 baseline) | 5.3×10⁻⁴ – 1.3×10⁻³ |
| efficiency η (0.10 assumed) | 2.6×10⁻⁴ – 2.6×10⁻³ |
| SMR (Lucas et al. 2014, units ambiguous) | 2.6×10⁻⁴ – 2.6×10⁻³ |
| mass | 2.6×10⁻⁴ – 2.6×10⁻³ |
| aerial range d | 2.6×10⁻⁴ – 2.6×10⁻³ |

The worst case at ×2 is 0.26 % of a day's SMR per launch. **No factor-of-two error flips this
claim.** S20 said the same, and the recomputation confirms it. The energy inputs are therefore not
the weak point.

**(b) "A 0.1–1 m aerial escape is on the menu."** The whole S20 cost-benefit frame prices a
launch whose aerial phase is long enough to matter ecologically. S20's own phrase was "a short
glide-scale escape". Every aerial quantity is set by one input, **exit speed v**. S20 did not
measure v. It solved v backwards from the range it wanted (v = √(g·d)), and it recorded adult
*Danio* peak fast-start speed as `unknown`.

| Exit speed v | Ballistic range (45°) | Apex | Time aloft | Glide area needed (C_L = 1) |
|---|---|---|---|---|
| 3.13 m/s (S20's 1 m case) | 100 cm | 25 cm | 0.45 s | 6.7 cm² |
| 1.57 m/s (½ of that) | 25 cm | 6.2 cm | 0.23 s | 27 cm² |
| 0.84 m/s | 7.2 cm | 1.8 cm | 0.12 s | 93 cm² |
| 0.42 m/s (½ of 0.84) | 1.8 cm | 0.45 cm | 0.06 s | 371 cm² |

Range and the required lifting area both scale as v². **A factor of two in v is a factor of four
in reach.** That is the difference between "a hop of about one body length" and "an escape of
several body lengths". It also moves the glide-area requirement from a plausible fin planform to
one ten times the body planform. This is the input the conclusion is most sensitive to: **adult
*Danio rerio* surface-exit (peak burst) speed.**

## 2. How well was that input established in S20?

**Not established. It was an assumption presented as a scenario.** S20 C1 lists v only as "what
would be required" for 0.1, 0.3 and 1 m, and C4 says "Adult *Danio* aquatic fast-start peak speed
is unknown". The 0.1 m scale was anchored to M8, a SICB meeting abstract on jumps of *stranded*
fish (read-level `search-summary`). The 1 m case had no anchor. In the S20 headline, "a launch
covering 0.1 to 1 m of air costs about 10⁻⁴ to 10⁻³ of daily standard metabolism", the 1 m figure
is a **hypothetical priced as if it were an option**.

- Evidence level of v in S20: `assumed` (back-solved), not `measured`.
- Read-level of the only anchor (M8): `search-summary`. It is also a *terrestrial* jump, which
  Gibb et al. 2011 describe as kinematically distinct from an aquatic fast start (abstract via
  search summary). So it is a **proxy** for a different behaviour.

## 3. Improving it

### 3.1 What I tried this session (access record)

| Source / host | Result |
|---|---|
| Danos & Lauder 2012, *J. Exp. Biol.* 215:1854–1862, doi:10.1242/jeb.068957: journals.biologists.com | Two article URLs resolved to unrelated JEB papers. I did not reach the article (`could-not-access`) |
| cob.silverchair.com PDF, sites.harvard.edu author PDF, dash.harvard.edu, zendy.io | DNS blocked by the session network policy (`could-not-access`). These hosts must be allowed before anyone can re-read the paper here |
| Europe PMC REST record for the DOI | Reached. Authors and abstract confirmed. Not open access and not in PMC (`abstract`) |
| Chang et al. 2019, *J. R. Soc. Interface* 16:20190014, "Jumping dynamics of aquatic animals" (PMC6451394) | Reached, through an automated fetch-and-summarise tool (`full-text`, relayed) |
| Web search, two queries for adult zebrafish C-start peak velocity and zebrafish leaping from water | Returned no zebrafish exit-speed or leap-height measurement (`search-summary`) |

### 3.2 The real quantity: adult peak escape speed

This repository already holds the best available number. `docs/research/fish/replicate-21.md`
(branch `origin/claude/danio-fast-start-speed-m0xilg`) records the following author claims from
Danos & Lauder 2012, read there as publisher full text through a fetch tool:

- mean maximum Re per escape sequence of 27,800 ± 2,140 (s.e.m.)
- 1 mPa s water
- fish with mean total length 33.0 ± 1.3 mm
- N = 5

**My read-level for these figures is `relayed`.** I could not re-open the paper this session (§3.1),
so I am relying on that note's reading.

From those, I recomputed U = Re·ν/L with ν = 1.0×10⁻⁶ m² s⁻¹, an assumed value since the
authors give no density. The result is a **calculated** U = **0.842 m/s (25.5 TL/s)**, with a
±1 s.e.m. band of **0.78–0.91 m/s**. It matches replicate-21. This is an inversion of a reported
Re, not a speed read off the paper. The paper shows speed only in Fig. 3, which neither session
read.

**Why this is the right quantity, and its limits** (my inference throughout):

- It is a *burst* peak from 1000 fps video of adults. That makes it a direct measure of the
  fast-start capability that an exit would draw on. Ucrit (Palstra et al. 2010, 0.548 m/s,
  `search-summary` per challenge-2) is a prolonged-swimming speed and serves only as a lower bound.
- It is a *submerged, mostly horizontal* peak. A surface exit also needs the fish to reorient
  upward and to punch through the interface. Both should cost speed. So the inversion is
  probably an *upper* bound on the exit speed of an unspecialised jump. That is my inference and
  it is unmeasured.
- N = 5, at one size (33 mm TL), and the temperature is `unknown`.

### 3.3 Sources that disagree (kept separate, not averaged)

| Line of evidence | v (m/s) | Range at 45° | What kind of number |
|---|---|---|---|
| Ucrit, Palstra 2010 | 0.548 | 3.1 cm | measured; prolonged speed, lower bound |
| Burst, inverted from Danos & Lauder 2012 | **0.842** (0.78–0.91) | **7.2 cm** (6.2–8.4) | calculated from a reported Re |
| Minimum v for the M8 "~0.10 m" stranded jump | 0.99 | 10 cm | calculated from a `search-summary` distance; a terrestrial push-off |
| Guppy "around 3.5 body lengths" jump height (Chang et al. 2019), scaled to a 33 mm fish | 1.51 | 23 cm | cross-species; the H/L ratio is the authors' claim, the scaling to *Danio* is mine |
| S20's 1 m launch | 3.13 | 100 cm | assumption |

M8 implies a speed about 18 % above the aquatic burst inversion. Possible reasons:

- a land push-off has a solid substrate to push against;
- "average distance per jump" may include sliding or body length;
- the Danos & Lauder maximum may come from stage 1 and miss the stage 2 peak, which they do not
  state.

The guppy comparator shows that a small fish *specialised for* vertical leaps may beat a
horizontal C-start peak by roughly 1.8×. I found no evidence that *Danio* does this. The
negative-search scope is §3.1 plus S20's ~12 searches.

**Agreement across the table.** Every line of evidence, the optimistic guppy-class value included,
sits **2.1× to 5.7× below** the exit speed S20's 1 m case needs. In kinetic energy that is 4.3× to
33× below.

## 4. Recomputing S20 with the improved input

All of the following is calculation, using v = 0.84 m/s (band 0.78–0.91) and S20's own m, η and SMR.

- **Reachable aerial phase:** 7.2 cm range (6.2–8.4), 1.8 cm apex at 45° (3.6 cm if vertical),
  0.12 s aloft. That is about two body lengths of air, and only a few centimetres above the surface.
- **Energy cost of that launch:** 1.4×10⁻³ J at η = 0.10, which is **3.8×10⁻⁵ to 9.5×10⁻⁵ of
  daily SMR**. The "almost free" claim **stands**, and becomes cheaper still.
- **The 1 m launch S20 priced:** it needs 3.7× the inferred burst speed and 13.8× its kinetic
  energy. It is **not available to an adult zebrafish**, so pricing it as "almost free" answered a
  question the animal cannot pose.
- **Gliding at the reachable speed:** needs about 93 cm² of lifting surface at C_L = 1. That is
  roughly 30× the planform of a 4 cm body, and could not be carried. This agrees with the
  sibling physics notes S1 and challenge-24 (deficits of 4–13× in speed), which I did not re-derive.
- **The benefit term, reconsidered (my inference, unmeasured):** what is on offer is a 7 cm,
  0.12 s hop that re-enters the water within about two body lengths. That is all the aerial phase
  has to buy. It is too short to break pursuit from the sub-surface predators S20 named as the
  only plausible beneficiary case (*Xenentodon*, *Barilius*). It still exposes the fish above the
  surface to the herons, egrets and kingfishers S20 listed. No attack rates or strike distances
  are measured for any of these predators against *D. rerio*. Parichy 2015, as relayed by S20,
  says predation impact is entirely unknown. So the size of the benefit remains `unknown`.
  What has changed is how large an escape the benefit would have to come from.

**Net effect on the answer.** S20 framed the question as "a cheap launch with an unknown benefit".
With the improved input it becomes "a cheap launch that **cannot reach flight scale**". The binding
constraint is exit speed, not energy and not ecology. Two parts of S20 change in different ways:

- The cost sub-claim *stands*.
- The "0.1–1 m" option *falls* at its 1 m end. What remains is 6–10 cm.

The overall conclusion, that flight would not pay a zebrafish, **strengthens**. It no longer rests
only on an unmeasured benefit. It now also rests on a capability gap of at least 2.1× in speed,
even against the most optimistic comparator.

## 5. What would settle the input, and what it would cost

**Measurement.** Use a side-view high-speed camera (≥ 1000 fps) at the water surface. Startle
adult wild-type *D. rerio* from below, with a tap or a looming stimulus, so that the escape is
directed toward the surface. Measure the following:

- exit velocity at the interface;
- exit angle;
- aerial range and apex;
- fraction of startles that clear the water.

Run about 10 to 20 fish with about 10 trials each. Include a *Danio*-sized jumper such as
*Esomus*, which S20 flagged, as a comparator. Separately, read Danos & Lauder 2012 Fig. 3 and
Table 1 to replace the Re inversion with the authors' own velocity values. That step needs
sites.harvard.edu or cob.silverchair.com to be allowed.

**Cost (my estimate, not a sourced figure).** For a lab that already has a zebrafish facility
and a high-speed camera, about 1–2 person-weeks plus fish. Without a camera, add the cost of
renting or buying a ≥ 1000 fps camera. I have no sourced price for that. Reading the PDF costs
nothing once the host is reachable.

**What would flip this verdict.** A measured adult exit speed of at least 3 m/s, which is 3.7×
the burst inversion. Anything near the guppy-class 1.5 m/s still leaves a ~23 cm hop and does
not restore the 1 m case.

## 6. What this does not establish

- It does not measure exit speed. 0.84 m/s is a *calculation* from a reported Reynolds number. I
  did not re-read that number this session; the figures come from a repository note.
- It does not show that the 7 cm hop is useless against every predator. That remains an
  inference, because predator strike kinematics against *Danio* are unmeasured.
- It does not address juveniles or larvae.
- It does not address dispersal between monsoon pools, where a short hop over a barrier could
  still pay. S20 left that open, and it stays open.
- The surface-taxiing route to higher speed (challenge-24) is not modelled here. It needs
  hypocaudal-lobe morphology that *D. rerio* lacks, which is the morphology subproblems' scope.

### Sources

| Source | Read-level |
|---|---|
| S20-ecology.md (parent; its M1–M15 read-levels carry over unchanged) | full-text (repository) |
| replicate-21.md, challenge-2.md, challenge-24.md, S1-launch-velocity.md (repository notes) | full-text (repository) |
| Danos N, Lauder GV 2012, *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957 | abstract (Europe PMC record). Figures relayed from replicate-21. Full text could-not-access this session |
| Palstra AP et al. 2010, *PLoS ONE* 5:e14483 | search-summary (via challenge-2) |
| Chang B et al. 2019, *J R Soc Interface* 16:20190014, PMC6451394 | full-text (automated fetch summary; quotes relayed) |
| Gibb AC et al. 2011, *J Exp Zool A* 315:649, doi:10.1002/jez.711 | search-summary (via S20) |
| SICB abstract on stranded *Danio* / *Gambusia* (M8) | search-summary (via S20) |

```swarm-result
{"subproblem": "S20-D", "evidence": "derived", "answer": "The input S20 is most sensitive to is adult exit speed (range and required glide area both scale as v^2), and replacing S20's back-solved 3.13 m/s with the burst speed inverted from Danos & Lauder 2012 (0.84 m/s, calculated) caps the reachable aerial phase at about 7 cm and 0.12 s, so the launch stays energetically trivial (~1e-4 of daily SMR) but the 0.1-1 m escape S20 priced is out of reach by at least 2.1x in speed even against a guppy-class jumper, which strengthens the conclusion that flight would not pay a zebrafish.", "key_number": "adult peak burst speed 0.84 m/s (0.78-0.91; calculated from reported Re 27,800 at 33 mm TL), giving a 7.2 cm maximum ballistic range versus the 3.13 m/s S20 assumed for a 1 m launch", "verdict": "strengthens"}
```
