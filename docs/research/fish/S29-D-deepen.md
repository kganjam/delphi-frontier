# S29-D-D: deepening S29-D by attacking its most sensitive input, the spring-release chain efficiency

**Parent:** S29-D, `docs/research/fish/S29-deepen.md` and `S29-deepen_calc.py` on branch
`claude/s29-deepen-launch-energy-0r1gju` (commit `f5a61183`), read in full. Grandparent: S29,
`docs/research/fish/S29-organism.md` on `claude/s29-launch-energy-2iuixr`, read in full.

**Status:** derived. Every number below is **calculated** by
`python3 docs/research/fish/S29-D-deepen_calc.py` from S29/S29-D inputs plus the values found
in this pass. **This project measured nothing.** Literature values carry their read level beside them.

**A note on the task prompt.** It quoted S29-D's recorded answer as blank. I recovered that
answer from the S29-D branch (its `swarm-result` block), and this document deepens that answer.

**Result: STANDS, with a narrower range and a weakened explanation.**
- With every value found (0.10–0.158), S29-D's three quantitative conclusions all hold:
  - the shortfall stays well above S29's 1.86×;
  - there is still no all-muscle break-even;
  - fish-grade tendon still does not fit comfortably.
- **But the improved input is a range, not a point.** The central one-side shortfall is
  **3.8–6.0×**, not "~6×".
- **S29-D's *explanation* for the low value does not survive.** S29-D argued that the low
  value comes from *passive* latch release. A *servo-driven* robot from the same group reports
  about the same efficiency (~12 %). The low number therefore does not distinguish passive from
  active drive.

---

## 1. The input S29-D's conclusion is most sensitive to (recomputed)

S29-D's central shortfall is ½V² / (f · w · chain) = 9.548 / (0.30 · 53 · 0.10) = **6.01**. This
reproduces S29-D §4 exactly (script §0).

Each input was multiplied by 2 and divided by 2 (script §1):

| Input | ×2 | ÷2 | Comment |
|---|---|---|---|
| **chain = KE_exit / E_stored (0.10, Conte 2010)** | 3.00 | 12.0 | elasticity −1 |
| w, muscle spring-loading work (53 J/kg) | 3.00 | 12.0 | elasticity −1 |
| f, muscle fraction (0.30) | 3.00 | 12.0 | elasticity −1, but capped at 0.60 = ×2.00 |
| V target (4.37 m/s) | 24.0 | 1.50 | the *specification*; its uncertainty belongs to S28 |

Chain, w and f tie on elasticity. **Where each of S29-D's claims flips** (script §2, calculated):

| S29-D claim | Fails if chain ≥ | Multiple of 0.10 |
|---|---|---|
| Fish-tendon spring ≤ 25 % of body (E 1.2 GPa, 2 % strain) | 0.167 | ×1.67 |
| **"The all-muscle break-even S29 left open no longer exists" (f 0.60, w 81)** | **0.196** | **×1.96** |
| "Not narrow": shortfall < 2× at f 0.30, w 53 | 0.300 | ×3.00 |
| One-side loading closes at w 81 | 0.393 | ×3.93 |

**So a factor-of-two error in the chain value flips S29-D's headline "break-even gone" claim.**
That was shown by recomputing it (script §2).

**Why the chain, rather than w or f** (my judgement, with reasons):
- **f is physically capped.** Doubling it is already the all-muscle row.
- **w is the right kind of quantity**, a measured series-tendon loading work (Mendoza & Azizi
  2021, via S29). Only the taxon is wrong.
- **The chain is the input S29-D itself names as load-bearing.** Its §7 ledger says: "If caveat 1
  (material loss) explains most of the gap, the verdict reverts to **stands**."
- **It rested on one abstract sentence**, "around 10%", for a device of unknown size, with a
  definition of "final" KE that was never pinned down.

## 2. How well is chain = 0.10 established?

**Conte, Modarres-Sadeghi, Watts, Hover & Triantafyllou 2010**, *Bioinspir. Biomim.* 5:035004,
doi:10.1088/1748-3182/5/3/035004, PMID 20729571.

**Read level: abstract.** I re-retrieved the abstract verbatim from the Europe PMC REST API in this
pass. Europe PMC lists it as `isOpenAccess = N`, "Subscription required". The full text was
could-not-access: iopscience.iop.org was refused by the session proxy (HTTP 403).

**Verbatim from the abstract:**

> "We measured the resulting acceleration, and calculated the efficiency of propulsion for the
> mechanical fish model, defined as the ratio of the final kinetic energy of the fish and the
> initially stored potential energy in the body beam. … The maximum start-up acceleration was
> measured to be around 40 m s(-2), with the maximum final velocity around 1.2 m s(-1). … The
> hydrodynamic efficiency of the fish was found to be around 10%."

**Assessment:**

| Question | Answer |
|---|---|
| Measured or calculated? | **Mixed, by the authors' own wording.** The acceleration is "measured"; the efficiency is "calculated". The calculation is from measured kinematics and, presumably, a stored-energy estimate for the beam. Whether that stored energy was *measured* (force–deflection) or *computed* (beam theory) is not in the abstract: `unknown`. S29-D labelled the 0.10 "MEASURED by the authors". That overstates what the abstract supports. |
| Which KE? | "final kinetic energy" alongside "maximum final velocity ~1.2 m/s". It is not stated whether "final" is the peak or a post-stroke value. S29 needs the KE **at the instant of exit**, i.e. near the peak. |
| Material loss separated? | Not in the abstract: `unknown`. This is S29-D's caveat 1. |
| Size / Re | Not in the abstract: `unknown`. |
| Evidence level as S29-D used it | **A single abstract-level, author-calculated efficiency, n = 1 device, definition partly unknown.** It is better than a proxy, because it is the right *kind* of quantity, but it is not established. |

## 3. Improving it

The primary full text was blocked, so I went after (a) the device's own predecessor, (b) other
devices from the same group, and (c) papers that cite Conte 2010.

### 3a. Watts 2006: the predecessor device (now identified)

S29-D had this source only as "Watts, MIT thesis, title unknown". It is now identified.

**Matthew N. Watts, 2006, SM thesis, MIT/WHOI Joint Program**, "Emulating the fast-start swimming
performance of the chain pickerel (*Esox niger*) using a mechanical fish design". DSpace handle
1721.1/39203; a copy is on calhoun.nps.edu (handle 10945/24376).

**Read level: search-summary.** dspace.mit.edu and calhoun.nps.edu are both outside this session's
network allowlist; WebFetch reported both as unresolvable.

Per the search summary (not read by me):

| Quantity | Value |
|---|---|
| Device | Thin metal beam under a urethane rubber body; stored beam energy released into the water |
| Peak acceleration | 48 m/s² |
| Velocity | **peak 0.96 m/s, "averaged maximum" 0.8 m/s** |
| Efficiency | "calculated by the transfer of energy": **11 %** |
| Beam | 1095 spring steel, cut to 14.75 in (37.5 cm) |

**What this improves** (calculated, script §3–4; each step is conditional on the search summary
being accurate):

1. **The definition of "final" KE matters by a factor of 1.44.** The thesis reports both a peak
   (0.96) and an averaged (0.80) velocity, and (0.96/0.80)² = 1.44.
   - If the 11 % used the averaged velocity, the **peak-KE chain**, which is what S29 needs, is
     0.11 × 1.44 = **0.158**.
   - If it used the peak, the chain is 0.11.
   - Which one was used is `unknown`. Answering it needs the thesis full text.
   - **The improved input is therefore a range, 0.10–0.158, not the point 0.10.**
2. **Scale.** If the body length is about the beam length (ASSUMED; the tail probably makes it
   longer), the device is ~12.5× a 30 mm zebrafish. Its Re is ≈ 3.6 × 10⁵, against ≈ 1.3 × 10⁵
   for a zebrafish at 4.37 m/s. **These are the same order of magnitude.** S29-D's caveat 2
   (Re unknown) is therefore mostly answered, conditional on the assumption.
3. **Material.** 1095 spring steel is a low-loss spring material. That fact is remembered, not
   retrieved, and **not load-bearing**: no number from it is used. The urethane body's share of
   the stored energy and its hysteresis remain `unknown`.

### 3b. A servo-driven robot from the same group, which undercuts S29-D's explanation

**Feng, Bonafilia, Modarres-Sadeghi & Triantafyllou 2011**, "The Mechanics of Fast-Start
Performance of Pike Studied Using a Mechanical Fish", IMECE2011-65035, doi:10.1115/IMECE2011-65035,
DSpace 1721.1/120737.

**Read level: search-summary.** DSpace and core.ac.uk could-not-access.

Per the search summary:
- It is a **servo-driven** pike-mimicking fast-start robot, which is *actively* driven, not
  spring-released.
- Peak acceleration 2.0 m/s², peak velocity 0.09 m/s.
- "Efficiency was about 12%".
- The efficiency's definition is `unknown`, and so is its denominator: electrical, or mechanical
  shaft work.

**Author's claim versus my inference.** The authors report ~12 %. **My inference** is that an
actively driven device lands at about the same efficiency as the two spring-released ones (10 %,
11 %). If so, S29-D's argument does not hold. S29-D argued that the passive device is low *because
it cannot control its body wave after release*. A ~10 % result is then **not diagnostic of passive
release**. It is equally consistent with:
- (i) robot bodies and fins underperforming fish at any drive; or
- (ii) a difference in *method*. The robot values are energy ratios from measured kinematics and
  input energy. Frith & Blake's 0.16–0.39 is a **Weihs-model** output (S29-D §2).

The definitions differ and the Feng denominator is unknown, so this is a weak inference. I do not
use it to move any number. It removes the *mechanistic reason* S29-D gave for preferring 0.10 over
0.37 as the analogue for a spring.

### 3c. Papers citing Conte 2010 (looking for anyone who restated its numbers)

Europe PMC lists **11 citing papers**. I checked the three that looked most relevant:

| Paper | What I could read | Result |
|---|---|---|
| **Anastasiadis et al. 2023**, *Sci Rep*, PMC10497532 | full-text, keyword-searched | Cites Conte only in a list of robots that "replicate high swimming speeds and accelerations". **No number restated.** |
| **Thandiackal et al. 2021**, *Proc R Soc B*, PMC8190629 | via WebFetch summary, so search-summary grade | Cites Conte only within a range of references. Reports that the Tunabot's mechanical power to the fluid "was only about 5% of the electrical input power", during a linear acceleration. That is a **different quantity** (electrical denominator, motor drive) and is **not used**. |
| **Witt, Wen & Lauder 2015**, *Integr Comp Biol* 55:728, doi:10.1093/icb/icv016 | search-summary; academic.oup.com HTTP 403, mirror host not allowlisted | Flexible panels with prescribed heave+pitch. Per the summary, a medium-stiffness panel reproduced the fish three-jet wake. **No efficiency number found.** |

**Scope of the negative searches in this pass:**
- 4 web searches (2 extended, 2 standard).
- Europe PMC: record lookup and the citations endpoint for PMID 20729571.
- Full-text XML of PMC10497532.
- Not reachable here: iopscience.iop.org, api.unpaywall.org, api.semanticscholar.org, core.ac.uk,
  dspace.mit.edu, calhoun.nps.edu, osti.gov, researchgate.net, scholar.archive.org,
  academic.oup.com, softrobotics.buaa.edu.cn, and pmc.ncbi.nlm.nih.gov via curl (reCAPTCHA page).

**Not found:**
- any measured KE_exit / E_stored for a spring-released body under 5 cm;
- any separation of material loss from hydrodynamic loss in Conte or Watts.

Both are `unknown`.

## 4. Recomputation and verdict

All values below are calculated (script §5).

| Chain KE_exit / E_stored | Source / read level | One-side shortfall, w = 32 / 53 / 81 | All muscle, w = 53 / 81 | 5.53 m/s, w = 53 |
|---|---|---|---|---|
| 0.10 | Conte 2010, abstract | 9.95 / **6.01** / 3.93 | 3.00 / 1.96 | 9.61 |
| 0.11 | Watts 2006 as reported, search-summary | 9.04 / 5.46 / 3.57 | 2.73 / 1.79 | 8.74 |
| 0.12 | Feng 2011, servo (not a spring), search-summary | 8.29 / 5.00 / 3.27 | 2.50 / 1.64 | 8.01 |
| **0.158** | **Watts, peak-KE reading (my conditional calculation)** | 6.28 / **3.79** / 2.48 | 1.90 / **1.24** | 6.07 |
| 0.323 | S29's implied chain | 3.08 / 1.86 / 1.22 | 0.93 / 0.61 | 2.97 |

Knock-on effects (script §5–6):

| Quantity | At chain 0.10 | At chain 0.158 |
|---|---|---|
| Stored energy needed | 38.2 mJ | 24.1 mJ |
| Tuna-grade tendon spring, % of body | 42–77 % | 26–49 % |
| One-side loading contractions at w 53 | 7 | 4 |
| Internal loss the device would need for S29's 0.323 to be right | 71 % | 54 % |

**Verdict on S29-D: STANDS.**

| S29-D claim | Status with the improved input (0.10–0.158) |
|---|---|
| Shortfall far above S29's 1.86× | **Stands**, at 3.8–6.0× rather than "~6×" |
| All-muscle break-even is gone | **Stands**: 1.24–1.96× short at w 81. It needs ≥ 0.196, and nothing found reaches that |
| Fish-grade tendon spring does not fit | **Stands**, weaker: 26–77 % of body |
| "Not narrow" | **Stands**: narrow would need ≥ 0.30 |
| *Why* the chain is low: passive release cannot shape the wave | **Weakened.** A servo-driven robot reports about the same ~12 % (search-summary; definition unknown) |

**The disagreement is preserved, not averaged away.**
- **Robot energy ratios: 0.10–0.12** (three devices, one group).
- **Live-fish Weihs-model efficiencies: 0.16–0.39** (pike and carp, via S29-D).
- These are different quantities from different methods. Nothing found here says which one a
  zebrafish axial spring would follow. S29's negative holds on **either**:
  - with the robot values, by 3.8–6.0×;
  - with the best fish values, by 1.76–1.86× (S29-D §3a).

## 5. What would settle it, and what it would cost

1. **Cheapest, decisive for this document: read the two texts.** Conte 2010 full text and the
   Watts 2006 thesis would answer:
   - peak or averaged KE;
   - measured or computed E_stored;
   - any loss test of the beam in air.
   - **Cost:** library access, or allowlisting dspace.mit.edu / calhoun.nps.edu /
     iopscience.iop.org for this environment. That is about an hour of reading.
   - **Decision rule:** if the peak-KE chain is ≥ 0.196, S29-D's break-even claim falls.
2. **The measurement itself: S29-D §5's bench test.** A 30 mm, 0.4 g spring-shim body in a
   silicone cast, line-cut latch, ≥ 5,000 fps video, with an in-air material-loss control.
   - S29-D estimated it at under US$500 in materials plus borrowed camera time. That figure is an
     estimate, not a quote.
   - It must report **peak** KE / E_stored, the quantity S29 needs, and say so.
   - **Add one arm that neither predecessor ran:** the same body driven actively. That is the only
     way to test S29-D's passive-versus-active explanation, which §3b puts in doubt.

## 6. Sources

| # | Source | Read level | Used for |
|---|---|---|---|
| 1 | S29-D: `S29-deepen.md`, `S29-deepen_calc.py` (branch `claude/s29-deepen-launch-energy-0r1gju`, f5a61183) | full-text | the conclusion under test; all inputs |
| 2 | S29: `S29-organism.md`, `S29_launch_energy.py` (branch `claude/s29-launch-energy-2iuixr`) | full-text | baseline inputs |
| 3 | Conte et al. 2010, *Bioinspir. Biomim.* 5:035004, PMID 20729571 | abstract (Europe PMC, verbatim); full text could-not-access | chain ≈ 0.10; definition; "calculated" |
| 4 | Watts 2006, MIT/WHOI SM thesis, DSpace 1721.1/39203 | search-summary; could-not-access | 11 %; v_peak 0.96, v_avg 0.80 m/s; beam 37.5 cm 1095 steel |
| 5 | Feng et al. 2011, IMECE2011-65035, DSpace 1721.1/120737 | search-summary; could-not-access | servo-driven ~12 %; definition unknown |
| 6 | Anastasiadis et al. 2023, *Sci Rep*, PMC10497532 | full-text (keyword-searched) | citing paper; no Conte number restated |
| 7 | Thandiackal et al. 2021, *Proc R Soc B*, PMC8190629 | search-summary (WebFetch); curl got a captcha | citing paper; 5 % electrical→fluid, not used |
| 8 | Witt, Wen & Lauder 2015, *ICB* 55:728 | search-summary; could-not-access | citing paper; no efficiency found |
| 9 | Europe PMC citations endpoint for PMID 20729571 | listing | 11 citing papers |

## 7. Honesty ledger

- **Reported by others (none of it re-measured):**
  - Conte: ~10 %, "calculated" (abstract).
  - Watts: 11 %, 0.96 / 0.80 m/s (search-summary).
  - Feng: ~12 %, servo-driven (search-summary).
- **Calculated here:**
  - every shortfall and flip point;
  - the 1.44 factor and the 0.158 peak-KE reading;
  - the Re values;
  - the spring volumes;
  - the internal-loss requirements.
- **Assumed here:**
  - the device's body length ≈ its beam length (Re only);
  - the search summaries of #4 and #5 are accurate.

  If #4 is wrong about the two velocities, the 0.158 upper end disappears and the range collapses
  to 0.10–0.11. That would make S29-D stronger, not weaker.
- **Remembered, not retrieved:** that 1095 spring steel is low-loss. No number depends on it.
- **Correction to S29-D:** S29-D labelled Conte's 0.10 "MEASURED". The abstract says
  "calculated" from measured acceleration.

```swarm-result
{"subproblem": "S29-D-D", "evidence": "derived (recalculation, script docs/research/fish/S29-D-deepen_calc.py) on S29/S29-D inputs; Conte 2010 at abstract read-level (verbatim, Europe PMC; efficiency 'calculated', not measured); Watts 2006 MIT thesis and Feng 2011 IMECE servo robot at search-summary read-level; primary full texts could-not-access", "answer": "S29-D's conclusion is most sensitive to the spring-release chain KE_exit/E_stored (a 1.96x error restores the all-muscle break-even it says is gone); improving it with the predecessor device (Watts 2006: 11% with peak 0.96 vs averaged 0.80 m/s) widens it to 0.10-0.158 for peak KE, which keeps the one-side shortfall at 3.8-6.0x and the all-muscle case 1.24-1.96x short, so S29-D stands, but a servo-driven robot from the same group reporting ~12% removes S29-D's mechanistic reason (passive release) for why the chain is low.", "key_number": "spring-release chain KE_exit/E_stored = 0.10-0.158 (dimensionless; 0.10 Conte 2010 abstract, 0.158 = Watts 2006 11% x (0.96/0.80)^2 if the 11% used averaged velocity, conditional, calculated); flip point for S29-D's break-even claim 0.196", "verdict": "stands", "depends_on": ["S29-D (S29-deepen.md, commit f5a61183): shortfall-with-chain formula and conclusions under test", "S29 (S29-organism.md): central inputs and the implied chain 0.323", "S28 V_exit 4.37 m/s target and S29 mass-consistent 5.53 m/s", "body mass 0.40 g (S29 brief)", "body density 1050 kg/m^3 (assumed, S29)", "S28 frontal area 24 mm^2, Cd 0.2, stroke 1.09 cm (assumed, S29) - enter only the S29 implied chain", "Mendoza-Azizi2021 frog spring-loading work 32/53/81 J/kg muscle (via S29)", "F_ONE_SIDE 0.30 (assumed, S29)", "F_ALL 0.60 zebrafish skeletal muscle fraction (secondary, S29)", "Ker1981 tendon return 0.93 (via S29) - enters S29 implied chain only", "Frith-Blake1995 pike eta_h 0.37 (model-derived, via S29/S29-D) - enters S29 implied chain only", "Shadwick tuna tendon E 0.65-1.2 GPa at 2% strain (via S29) - spring volume knock-on", "Conte2010 KE_final/E_stored ~0.10, calculated from measured acceleration (abstract)", "Watts2006 MIT thesis efficiency 11%, v_peak 0.96 m/s, v_avg 0.80 m/s, beam 14.75 in 1095 steel (search-summary)", "ASSUMPTION: Watts 11% may have used averaged velocity, giving the 0.158 upper bound (definition unknown)", "Feng2011 IMECE2011-65035 servo-driven pike robot efficiency ~12%, definition unknown (search-summary)", "ASSUMPTION: device body length ~ beam length (Re estimate only)", "ASSUMPTION: neither robot's efficiency is dominated by urethane/beam material loss (unresolved S29-D caveat 1)", "S29-D-a Frith-Blake/Wakeling live-fish eta_h 0.16-0.39 (model-derived) as the preserved competing range"]}
```
