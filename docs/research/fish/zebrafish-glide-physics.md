# Can a zebrafish glide? A physics budget for a 0.4 g, 4 cm *Danio rerio*

**Status:** desk calculation only. No experiment was run and nothing here was measured by us.
Every number marked *calc* comes from `zebrafish_glide_calc.py` in this folder (run it to
reproduce the tables). Literature values carry a read-level tag, and each claim is labelled
`retrieved` or `remembered`, following `CONTRIBUTING-VERIFICATION.md` §3 and §9.

**How sources were accessed in this session.** Web *search* worked. Web *fetch* to the journal
hosts (cob.silverchair.com, pmc.ncbi.nlm.nih.gov, typeset.io) was **blocked by the session
network policy**. So no full text and no abstract was opened directly. The best read-level
anywhere in this report is `search-summary`: a search engine's excerpt of the page. I had no
way to check it against the paper. Treat every literature number below at that confidence.

## Inputs

| Symbol | Value | Provenance |
|---|---|---|
| m | 0.4 g = 4.0e-4 kg | given in brief |
| L (SL) | 4 cm = 0.04 m | given in brief |
| W = m·g | 4.0e-4 × 9.81 = **3.924e-3 N** | calc |
| ν_air | 1.5e-5 m²/s | given in brief |
| ρ_air | 1.2 kg/m³ | assumed (sea level, ~20 °C) |
| g | 9.81 m/s² | standard |

---

## 1. Reynolds regime

Re = V·c/ν. Example: V = 4 m/s, c = 0.02 m → 4 × 0.02 / 1.5e-5 = 0.08 / 1.5e-5 = 5,333.

| chord c | V = 1 m/s | 2 m/s | 4 m/s | 8 m/s |
|---|---|---|---|---|
| 0.5 cm | 333 | 667 | 1,333 | 2,667 |
| 1.0 cm | 667 | 1,333 | 2,667 | 5,333 |
| 2.0 cm | 1,333 | 2,667 | 5,333 | 10,667 |
| 3.0 cm | 2,000 | 4,000 | 8,000 | 16,000 |

All 16 cells (calc) are between **333 and 16,000**. Every cell is one to three orders of
magnitude below the 1e5–1e6 quoted in the brief for Exocoetidae. This is the insect/small-bird
regime: laminar boundary layers, separation without reattachment at moderate angles of attack,
and no turbulent-transition lift recovery.

**The Re is pinned by weight, not by speed (inference, derived here).** Suppose the wing is
sized to carry W at a given C_L. Then S = 2W/(ρV²C_L) and c = √(S/AR), so

  Re = V·c/ν = √(2W / (ρ·C_L·AR)) / ν, with **V cancelling out**.

For C_L = 0.6, AR = 5: √(2 × 3.924e-3 / (1.2 × 0.6 × 5)) = √(2.180e-3) = 0.04669;
0.04669 / 1.5e-5 = **3,113** (calc; matches the §2 table). The range over AR 3–8 and
C_L 0.6–1.0 is **1,906 – 4,018** (calc). A 0.4 g glider therefore cannot buy its way to a
higher Re by flying faster. Only more weight or a lower aspect ratio raises it, and both make
other barriers worse.

**On the Exocoetidae premise.** A sciencegate listing for Park & Choi (2010) gives a mean-chord
Re of 3.26e4 – 6.79e4 for flying-fish wind-tunnel tests, with C_L,max 1.5 and best L/D 6.8
[S1, `listing`, `retrieved`]. The search summary itself flagged that the listing did not clearly
tie these numbers to the 2010 paper. If they are correct, they do **not** support the brief's
1e5–1e6. I could not resolve this, so the flying-fish Re is **unknown** to the confidence this
report requires. It does not affect the zebrafish numbers.

### What C_L,max is attainable at Re ≈ 2e3 – 4e3?

What was retrieved:
- **Laitone (1997)** tested rectangular wings down to Re ≈ 20,000 in a low-turbulence tunnel.
  The search summary reports that, for one wing at Re ≈ 20,700, C_L,max at stall **rose from
  0.455 to 0.59** when the tunnel turbulence changed. A 5 %-camber thin plate gave the best
  L/D, **13.3** [S2, `search-summary`, `retrieved`]. The summary did not identify which section
  produced the 0.455/0.59 values.
- **Usherwood & Ellington (2002, Part II)**: "high force coefficients" for revolving model and
  real wings from mayfly to quail, **Re 1,100–26,000**, which they attribute to a
  leading-edge vortex [S3, `search-summary`, `retrieved`]. The coefficient values themselves:
  **not retrieved**. I remember them as roughly 1.5–1.8 (`remembered`, not used below).
- **Okamoto group, corrugated thin aerofoils, Re 1,000–10,000**: their claim is "good" C_L and
  L/D below Re ≈ 5,000. No numbers were retrieved [S4, `search-summary`].
- **NACA 0012 at Re 5.3e3–2.0e4 (PolyU thesis, 2022)**: their claim is that C_L,max data
  collapse when scaled with an effective Re. No numbers were retrieved [S5, `search-summary`].
- **Dickinson et al. (1999)**, Robofly, Re ≈ 140: per a 2023 arXiv paper, the translational
  lift slope was ≈ 3.8 rad⁻¹, against 2π for thin-aerofoil theory [S6, `search-summary`]. C_L,max:
  **not retrieved**.

**Inference (mine):** a revolving or flapping wing gets high coefficients from an attached
leading-edge vortex. A *translating* glide wing does not get that mechanism in steady flow, so
the revolving-wing numbers are not glide numbers. The only steady-wing C_L,max actually
retrieved (0.455–0.59) is at Re ≈ 20,700, about 5–7× above the design Re of 3e3. The steady
C_L,max at Re ≈ 3e3 for a fish-fin-like membrane is **unknown**. Below I use **C_L = 0.6** as
the central design value (the Laitone upper figure, which is probably generous at the lower Re)
and **C_L = 1.0** as an optimistic sensitivity case (cambered or corrugated membrane, unproven).
C_L = 1.5 is not used.

---

## 2. Wing loading and required span

Level glide (shallow, so L ≈ W): S = W / (½ρV²·C_L), b = √(AR·S).

Worked example (V = 2 m/s, C_L = 0.6): q = ½ × 1.2 × 2² = 2.40 Pa. S = 3.924e-3 / (2.40 × 0.6) =
3.924e-3 / 1.44 = 2.725e-3 m² = 27.25 cm². At AR 5: b = √(5 × 27.25) = √136.25 = 11.67 cm,
and 11.67 / 4 = **2.92 body lengths**.

**C_L = 0.6** (calc):

| V (m/s) | q (Pa) | S (cm²) | W/S (N/m²) | span AR 3 | span AR 5 | span AR 8 |
|---|---|---|---|---|---|---|
| 1 | 0.60 | 109.0 | 0.36 | 18.1 cm = **4.5 BL** | 23.4 cm = **5.8 BL** | 29.5 cm = **7.4 BL** |
| 2 | 2.40 | 27.3 | 1.44 | 9.0 cm = 2.3 BL | 11.7 cm = 2.9 BL | 14.8 cm = 3.7 BL |
| 4 | 9.60 | 6.81 | 5.76 | 4.5 cm = 1.1 BL | 5.8 cm = 1.5 BL | 7.4 cm = 1.8 BL |
| 8 | 38.4 | 1.70 | 23.0 | 2.3 cm = 0.57 BL | 2.9 cm = 0.73 BL | 3.7 cm = 0.92 BL |

**C_L = 1.0** (calc): S = 65.4 / 16.4 / 4.09 / 1.02 cm² at V = 1 / 2 / 4 / 8 m/s. Spans at AR 5
are 4.5 / 2.3 / 1.1 / 0.57 BL.

Plainly:
- **At V ≤ 2 m/s the wing is anatomically absurd.** It needs 2–7 body lengths of span and
  16–109 cm² of area on a fish whose whole lateral profile is only a few cm². Zebrafish
  pectoral-fin area: **unknown** (not retrieved), so I cannot state the scale-up factor.
- **At V ≈ 4 m/s it is large but not absurd**: about 1.1–1.8 BL of span, 4–7 cm².
- **At V ≈ 8 m/s it is small**: under 1 BL. The wing is not the binding problem at high speed.
  The speed is (§3).
- Hidden cost, not modelled: a membrane of 5–100 cm² adds mass (raising W) and adds drag in
  water during the launch run. Both push the required speed up. Magnitude **unknown**.

---

## 3. Launch energy

### What is measured

- **Critical swimming speed (Ucrit)** of adult wild-type zebrafish: **0.548 ± 0.007 m/s =
  18.0 SL/s** (n = 10). This was reported in a study surfaced alongside Tudorache's author
  record [S7, `search-summary`, `retrieved`]. I *remember* this as Palstra et al. 2010,
  PLoS ONE, but that attribution is `remembered` and unverified.
- Plaut (2000, J. Exp. Biol. 203:813) measured Ucrit at 28 °C [S8, `listing`: ZFIN record,
  abstract excerpt only]. A *later paper* attributes **0.560 ± 0.048 m/s = 15.5 SL/s** to Plaut
  [S9, `search-summary`, secondary]. Not confirmed against Plaut directly.
  Cross-check (calc): 0.560 / 15.5 = 3.6 cm SL, which is consistent with the 4 cm brief.
- A protocol paper warns that absolute Ucrit in adults varies with the swim-tunnel equipment
  [S10, `search-summary`].
- **Ucrit is not burst speed.** It is a stepped-velocity, minutes-long test. **Adult fast-start
  peak speed: unknown.** I searched three times and found no measured adult value. The adjacent
  values, none of which is an adult zebrafish measurement:
  - 5 dpf larva (4.2 mm), peak 0.15 m/s ≈ 36 BL/s [S11, `search-summary`, observed in larvae].
  - A self-propelled **simulation** of a 3.31 cm zebrafish-like body peaking at 17.5 L/s
    (≈ 0.58 m/s) [S12, `search-summary`; simulated, not observed].
  - Archer fish predictive C-starts > 20 BL/s, among the fastest teleost starts known
    [S13, `search-summary`, other species].

I therefore bracket adult burst speed as follows. The 20 and 30 BL/s values are **assumptions**,
not measurements.

### Ballistic arithmetic (vertical exit, no air drag, no water-exit losses)

h = v²/(2g); R_max = v²/g (45° launch); KE = ½mv².

| Exit speed | basis | h_max | R_max (45°) | KE |
|---|---|---|---|---|
| 0.548 m/s | Ucrit, measured [S7] | 0.548² / 19.62 = **1.53 cm** | 3.06 cm | 0.060 mJ |
| 0.560 m/s | Ucrit, secondary [S9] | 1.60 cm | 3.20 cm | 0.063 mJ |
| 0.80 m/s | **assumed** 20 BL/s | 3.26 cm | 6.52 cm | 0.128 mJ |
| 1.20 m/s | **assumed** 30 BL/s | 7.34 cm | 14.7 cm | 0.288 mJ |

Surface tension is not the barrier (calc): Weber number ρ_w v² L / σ = 1000 × 0.56² × 0.04 /
0.072 = **174** ≫ 1. Inertia dominates the water exit.

### Against what §2 needs

The speed needed to glide with a given span (AR 5, C_L 0.6) is V = √(2W/(ρ·S·C_L)), with
S = b²/5 (calc):

| span | S | required V | V ÷ 0.56 | KE ratio (V/0.56)² |
|---|---|---|---|---|
| 0.5 BL | 0.80 cm² | 11.7 m/s | 20.8× | 434× |
| **1 BL** | 3.20 cm² | **5.84 m/s** | **10.4×** | **109×** |
| 2 BL | 12.8 cm² | 2.92 m/s | 5.2× | 27× |
| 3 BL | 28.8 cm² | 1.95 m/s | 3.5× | 12× |

Gaining speed by diving instead (h = V²/2g) requires drop heights of 0.05 / 0.20 / 0.82 / 3.26 m
to reach 1 / 2 / 4 / 8 m/s (calc). The fish reaches 1.5–7 cm. So even the most favourable case,
a 3-BL wing, needs an exit at about 3.5× the measured Ucrit and about 12× its kinetic energy.
The assumed 30 BL/s burst (1.2 m/s) still falls short of the 1.95 m/s this most generous wing
needs: (1.95/1.2)² = **2.6× in energy**.

---

## 4. Power, if it must flap

Gliding fails at the launch, so I computed the power for sustained flapping flight. This is a
quasi-steady **lower bound**: induced + profile + parasite. Real flapping costs more, because of
inertial power, unsteady losses, and wing speed above flight speed.

P = k·2W²/(ρπb²V) + ½ρV³·S·C_D,pro + ½ρV³·A_body·C_D,body

Assumed: k = 1.2; C_D,pro = 0.08 (laminar flat-plate skin friction alone is 2 × 1.328/√3,000 ≈
0.048, plus pressure drag); A_body = 0.30 cm²; C_D,body = 0.4; AR = 5; C_L capped at 0.6.
These are **assumptions**, and zebrafish body frontal area is **unknown**. In every case the
minimum-power speed lands at the C_L cap, i.e. at stall speed.

| span | V | P_ind | P_pro | P_par | **total** | per kg body |
|---|---|---|---|---|---|---|
| 1 BL | 5.84 m/s | 1.05 mW | 3.06 mW | 1.43 mW | **5.54 mW** | 13.9 W/kg |
| 2 BL | 2.92 m/s | 0.53 mW | 1.53 mW | 0.18 mW | **2.23 mW** | 5.6 W/kg |
| 3 BL | 1.95 m/s | 0.35 mW | 1.03 mW | 0.05 mW | **1.43 mW** | 3.6 W/kg |

Example for the 1 BL induced term: 1.2 × 2 × (3.924e-3)² / (1.2 × π × 0.04² × 5.84) =
3.695e-5 / 3.523e-2 = 1.05e-3 W.

Taking off from a ~0.6 m/s water exit means producing near-hover lift first. The crude hover
model (full actuator disc πb²/4; wing C_L 1.0 and C_D 1.0 with stroke-averaging factor 0.5, all
**assumed**) gives 14.2 / 7.1 / 4.8 mW for 1 / 2 / 3 BL (calc), i.e. **36 / 18 / 12 W/kg body**.

### Muscle supply (literature)

- Sculpin (*Myoxocephalus scorpius*) fast fibres, work loop, cycle-averaged maximum
  **25–35 W/kg wet muscle** at 5–7 Hz (Altringham & Johnston 1990) [S14, `search-summary`]. This
  is a cold-water species, and the test temperature was not retrieved.
- Fast myotomal fibres driven with in-vivo-like strain: **142.7 W/kg at 20 °C** [S15,
  `search-summary`]. The summary named the species inconsistently ("*Sc. notata*" / saithe), so
  the attribution is unverified.
- Instantaneous (not cycle-averaged) values of 175–265 W/kg, from a 1995 follow-up
  [S14 summary, `search-summary`]. Not comparable to cycle-averaged demand, so not used.
- Zebrafish-specific maximum muscle power: **unknown**. Ravel et al. (2025) model maximum
  neuromuscular power in *larval* escapes, but the value was not retrieved [S16].
- Fraction of a zebrafish's mass in pectoral (wing-driving) muscle: **unknown**. I would expect
  it to be very small, since the fish's power muscle is axial, but that is not measured here.
  I use 10 % and 25 % as **assumed** design targets. 25 % is in the range I *remember* for bird
  flight muscle (`remembered`).

### Deficit ratios (demand ÷ supply; > 1 means short), all calc

| case | demand @ 25 % muscle | ÷ 30 W/kg | ÷ 142.7 W/kg | demand @ 10 % muscle | ÷ 30 | ÷ 142.7 |
|---|---|---|---|---|---|---|
| cruise, 1 BL | 55 W/kg | **1.8×** | 0.39× | 139 W/kg | **4.6×** | 0.97× |
| cruise, 2 BL | 22 W/kg | 0.7× | 0.16× | 56 W/kg | 1.9× | 0.39× |
| hover, 1 BL | 142 W/kg | **4.7×** | 1.00× | — | — | — |
| hover, 2 BL | 71 W/kg | 2.4× | 0.50× | — | — | — |

**Reading (inference):** on raw mechanical power the deficit is modest. It ranges from about
0.4× to 4.7× depending on which muscle figure is true at zebrafish temperature (~28 °C), and it
closes entirely if the 142.7 W/kg figure applies and a quarter of the body is flight muscle. Two
things this table hides:
1. Fast (white) fish muscle is the burst-power fibre type. Its sustainable duration is short,
   and I have no zebrafish number for it (**unknown**). Cruise demand is sustained.
2. The fish has no pectoral power plant of that size. The 10–25 % figure is a re-engineering
   target, not an existing tissue.

---

## 5. Verdict

**The hardest barrier is launch speed (kinetic energy at water exit).** Take a wing of one body
length span (AR 5, already 3.2 cm² of new membrane) at C_L 0.6. It needs **5.84 m/s** to glide.
The only measured adult swimming speed retrieved is Ucrit, **0.548 m/s**. That is a **10.4×**
speed deficit and a **109×** kinetic-energy deficit. The best ballistic reach is about **1.5 cm
of height**, and gaining 5.84 m/s by diving would need a 1.74 m drop (5.84²/19.62). Even with an
absurd 3-BL wing and an assumed 30 BL/s burst, the energy is still 2.6× short.

The Reynolds barrier (Re pinned at ~2e3–4e3 by weight, so C_L,max is probably ≤ 0.6, value at
that Re **unknown**) is what *inflates* the speed requirement. It is a multiplier on the launch
barrier, not a separate wall. Power is a lesser barrier: 0.4–4.7× in demand ÷ supply, fixable on
paper by a large enough flight muscle.

Caveat on the verdict: the denominator is Ucrit, a sustained speed. True adult burst speed is
**unknown** and is surely above Ucrit, by my inference. It would need to exceed ~5.8 m/s
(~146 BL/s) to close the 1-BL case. No fish number I retrieved, from any species, approaches
that.

---

## WHAT WOULD CHANGE THIS VERDICT

| Barrier | Measurement that could move it | Design change that could move it | What it would take |
|---|---|---|---|
| **Launch speed** (hardest) | Adult zebrafish fast-start peak velocity, high-speed video ≥ 1000 fps, in m/s and SL/s (currently **unknown**) | Extending the in-water acceleration run before exit (surface taxiing with a tail still in the water) | Closing the 1-BL case needs ~5.8 m/s at exit. Closing the 3-BL case needs 1.95 m/s, ~49 BL/s |
| | Whether a zebrafish can exit at a chosen angle while carrying wing membrane, and the drag penalty of that membrane in water | Launch from height (perch, leaf, jump from a bank) instead of from water | Drop heights 0.82 m for 4 m/s and 0.20 m for 2 m/s (calc) |
| **Low-Re C_L,max** | Steady C_L,max of a fin-ray-supported membrane at Re 2e3–4e3 in a wind tunnel (currently **unknown**; the nearest retrieved is 0.455–0.59 at Re ≈ 2.1e4) | Camber/corrugation (fin rays already give a corrugated membrane; inference), low-AR wings that hold a leading-edge vortex at high angle of attack | Each doubling of C_L halves the area or cuts required V by √2. C_L = 1.0 moves the 1-BL speed from 5.84 to 4.52 m/s. Still about 8× Ucrit |
| | Full text of Usherwood & Ellington 2002 and Laitone 1997 (blocked this session) to replace the recalled and summary numbers | — | Would pin the C_L inputs. Unlikely to change the order of magnitude |
| **Wing size/mass** | Zebrafish pectoral-fin area and fin-ray length (currently **unknown** here) | Elongated pectoral fin rays. The 2–3 BL spans needed at 2–3 m/s are the morphology that brings speed within reach | Area/mass of 13–29 cm² membrane; added mass raises W, and Re scales as √W |
| **Power** (only if flapping) | Work-loop power of zebrafish fast and red muscle at 28 °C, cycle-averaged, at the 20–50 Hz a 4–12 cm wing would need (currently **unknown**) | A dedicated pectoral flight muscle of 10–25 % body mass | At 142.7 W/kg and 25 % mass the cruise deficit is gone; at 30 W/kg it is 1.8–4.7× |
| **Premise** | Park & Choi 2010 full text, to settle flying-fish Re (listing says 3.3e4–6.8e4, against the brief's 1e5–1e6) | — | Changes the comparison, not the zebrafish numbers |

---

## Sources

Read levels: full-text | abstract | listing | search-summary | could-not-access. In this session
every direct fetch attempt to a journal host returned a network-policy block, so no entry is
above `search-summary`.

| # | Source | Read-level | Used for |
|---|---|---|---|
| S1 | Park, H. & Choi, H. (2010) Aerodynamic characteristics of flying fish in gliding flight. *J. Exp. Biol.* 213:3269–3279, doi:10.1242/jeb.046052 | listing (sciencegate) for numbers; search-summary for qualitative; typeset.io PDF **could-not-access** | Exocoetidae Re premise |
| S2 | Laitone, E.V. (1997) Wind tunnel tests of wings at Reynolds numbers below 70 000. *Exp. Fluids* 23:405–409 | search-summary | C_L,max 0.455–0.59 at Re ≈ 20,700 |
| S3 | Usherwood, J.R. & Ellington, C.P. (2002) The aerodynamics of revolving wings II. *J. Exp. Biol.* 205:1565–1576 | search-summary; PDF **could-not-access** | Re 1,100–26,000; LEV coefficients (value not retrieved) |
| S4 | Okamoto group, corrugated thin aerofoils at Re 1,000–10,000 (J-STAGE / KAKEN 16K06894 report); Okamoto, Yasuda & Azuma (1996) *J. Exp. Biol.* 199:281–294 | search-summary (later work); listing (1996 paper) | qualitative low-Re corrugated performance |
| S5 | PolyU thesis (2022), NACA 0012 at Re 5.3e3–2.0e4, theses.lib.polyu.edu.hk/handle/200/12163 | search-summary | C_L,max scaling with effective Re |
| S6 | arXiv:2302.09602, quasi-steady model citing Dickinson, Lehmann & Sane (1999) *Science* 284:1954 | search-summary (arXiv); listing (Science) | lift slope ≈ 3.8 at Re ≈ 140 |
| S7 | Adult zebrafish Ucrit 0.548 ± 0.007 m/s = 18.0 SL/s, n = 10, surfaced via scite author page for C. Tudorache (attribution to Palstra et al. 2010 PLoS ONE is `remembered`) | search-summary | measured swimming speed |
| S8 | Plaut, I. (2000) Effects of fin size on swimming performance... *J. Exp. Biol.* 203:813–820 (ZFIN ZDB-PUB-000201-23) | listing | Ucrit method, 28 °C |
| S9 | Later paper quoting Plaut's 0.560 ± 0.048 m/s = 15.5 SL/s (PMC7842627) | search-summary; PMC **could-not-access** | secondary Ucrit |
| S10 | Bio-protocol e3712 (2020), zebrafish Ucrit protocol | search-summary | equipment dependence of Ucrit |
| S11 | Voesenek et al., Reorientation and propulsion in fast-starting zebrafish larvae, *J. Exp. Biol.* 222:jeb203091 (bioRxiv 570812) | search-summary | larval peak 0.15 m/s |
| S12 | Self-propelled simulation of zebrafish C-escape (html.rhhz.net, 2019) | search-summary | simulated 17.5 L/s, not observed |
| S13 | Archer fish predictive start (ResearchGate 6590357) | search-summary | > 20 BL/s, other species |
| S14 | Altringham, J.D. & Johnston, I.A. (1990) *J. Exp. Biol.* 148 / 151 (exact paper not confirmed), sculpin fast fibres | search-summary | 25–35 W/kg cycle-averaged |
| S15 | Fast myotomal fibres, 142.7 W/kg at 20 °C (species and paper attribution unverified; possibly the saithe study, *J. Exp. Biol.* 182:191, listing) | search-summary | upper muscle power |
| S16 | Ravel et al. (2025) *iScience*, doi:10.1016/j.isci.2025.112056, PMID 40124491 | search-summary; PMC **could-not-access** | larval max power (value not retrieved) |

Not used, but seen: Rome & Swank scup **red** muscle, 27.9 W/kg at 20 °C (search-summary; red,
not white). A dystrophic-strain escape value of 18 BL/s (source not identified). Davenport
(1994) *Rev. Fish Biol. Fish.* and Fish (1990) *J. Zool.* 221 on flying-fish wing loading
(listing only, no numbers).
