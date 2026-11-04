# S24 (behaviour): Could surface taxiing close the zebrafish launch gap?

Project `zebrafish-flight`. Scale: behaviour. This is a desk study. I ran no experiment and
filmed no fish. Every number below is tagged as one of three kinds. **Measured** means a value
from the literature, given with its read-level. **Calc** means my own arithmetic, produced by
`S24_calcs.py` in this directory. **Assumed** means an input I chose.

**Short answer.** Taxiing **cannot** close the 1-BL-wing gap (5.84 m/s). For that case the
derivation fails by a wide margin. For the 3-BL wing (1.95 m/s) the case is **not refuted, and
not shown feasible**. The binding constraint is **not thrust force**. It is **tail-beat
frequency**. A tail that has to stay in the water and keep producing thrust at 1.95 m/s needs
about **49–73 Hz** (calc; St 0.2–0.3, amplitude 0.2 TL). The highest frequency measured in an
adult zebrafish is **52 Hz**, reached transiently during an escape. In steady swimming the
measured adult ceiling is **21 Hz** (Kyriakatos et al. 2011, full-text). No measured adult
zebrafish caudal-fin thrust was found, so the refutation test named in the brief **cannot be
run** on measured data.

---

## 1. The question, restated with the numbers that make it hard

**Surface taxiing** is a two-stage launch. The fish first leaves the water at its burst exit
speed U₀. It then keeps the lower caudal lobe in the water and beats it while the body and wings
are in air. The question is whether this second stage can carry a 4 cm, 0.4 g zebrafish
(W = 3.92 mN) from U₀ up to the steady glide speed V_g, before the wings can carry its weight.

The numbers that make it hard:

- **V_g, inherited from the glide analysis** (`zebrafish-glide-physics.md`, AR 5, C_L 0.6; calc
  there, reproduced in challenges 2 and 3):
  - **5.84 m/s** for a 1-body-length span;
  - **1.95 m/s** for a 3-BL span.
  - Challenge 3 showed that the 1-BL figure falls to 2.0–3.7 m/s at AR 1–2. I keep the brief's
    two targets and do not re-litigate them.
- **U₀ candidates:**
  - Ucrit = **0.548 m/s** (Palstra 2010) is a prolonged-swimming speed, not a burst (challenge 2).
  - The adult burst speed back-calculated in §3.1 is **0.84 m/s** (calc, from measured Re).
- **Gap:** 1.95/0.84 = **2.3×** in speed (5.4× in KE) for the 3-BL wing, and 5.84/0.84 =
  **6.9×** (48× in KE) for the 1-BL wing (calc).
- **Weight support:** wing lift scales as (U/V_g)². At U₀ = 0.84 m/s the wings carry only
  **18.7 %** of W for the 3-BL wing and **2.1 %** for the 1-BL wing (calc). Something other than
  the wings must carry the remaining 81–98 % of the weight during the early taxi, or the body
  never leaves the water (§3.5).

## 2. What is measured

### 2.1 Zebrafish (Danio rerio), adult

| Quantity | Value | Source, year | Read-level |
|---|---|---|---|
| Ucrit | **0.548 ± 0.007 m/s = 18.0 SL/s** (n = 10) | Palstra et al. 2010, *PLoS ONE* 5:e14483 | search-summary (abstract quoted); full text could-not-access (challenge 2) |
| Ucrit (secondary) | ≈ 0.56 m/s = 15.5 SL/s, 28 °C | Plaut 2000, *J. Exp. Biol.* 203:813, via Palstra abstract | search-summary |
| Ucrit, **disagreeing** | **0.193–0.282 m/s** across strains (AB 0.259, TU 0.251, TL 0.236, WIK 0.193, TU×TU offspring 0.282) at 26 °C; peak 0.238 m/s at 28 °C; 0.116 m/s at 12 °C | Wakamatsu, Ogino & Hirata 2019, *Sci. Rep.* 9:16307 (PMC6841939) | full-text |
| Effect of caudal-fin length on Ucrit | Long-fin PET fish: 0.234 m/s intact (fin 14–30 mm) vs **0.271 m/s** clipped to 5 mm | Wakamatsu et al. 2019 | full-text |
| Caudal-fin length, short-fin strains | 5.6–6.5 mm (AB, TU, WIK) | Wakamatsu et al. 2019 | full-text |
| Max intact swimming frequency (EMG) | 2–21 Hz per animal; "never exceeding 21 Hz (n = 8)" | Kyriakatos et al. 2011, *J. Neurosci.* (PMC6623330) | full-text (first 100k of 101k characters) |
| Max frequency during **escape** | **52 Hz** ("maximal frequency reached during escape") | Kyriakatos et al. 2011 | full-text (same) |
| Escape mean max Reynolds number, 1 mPa·s water | **27,800 ± 2140 s.e.m.**; 2350 ± 160 at 10 mPa·s; 820 ± 60 at 20 mPa·s; computed with "fish length, maximum linear velocity per sequence and the appropriate viscosity" | Danos & Lauder 2012, *J. Exp. Biol.* 215:1854, doi:10.1242/jeb.068957 | full-text (first 100k of 121k characters; Table 1 and Fig. 3 are images and were not readable) |
| Fish size in that study | TL 33.0 ± 1.3 mm; mass not reported; water temperature not stated | Danos & Lauder 2012 | full-text |
| **Caudal-fin thrust (force), adult** | **unknown**; no measurement found | — | see §2.4 for search scope |
| Larval C-start acceleration | "up to 28 g" (zebrafish larvae; credited to Müller & van Leeuwen 2004) | larval-swimming review, *J. Exp. Biol.* 221 jeb149583 | search-summary; primary not read. Larval only, **not used numerically** |
| Larval tail-beat frequency | up to ~100 Hz in cyclic swimming | search result, unidentified larval kinematics paper | search-summary. Larval only, not used |

**Disagreement preserved: Ucrit.** Palstra (0.548 m/s) and Plaut (≈ 0.56 m/s) agree with each
other. Wakamatsu et al. report 0.19–0.28 m/s, which is **2–2.8× lower**. Wakamatsu give no SL
values, so the gap cannot be converted to BL/s. Possible causes include protocol (step length
and increment), tunnel geometry, strain, and temperature (26 vs 28 °C). Neither paper explains
the difference, and this report does not resolve it. The argument below does not depend on
which value is right, because both sit far below 1.95 m/s.

**Inference, mine, from Wakamatsu's fin-clip data:** a *longer* caudal fin *lowered* Ucrit, by
about 14 % between intact long fins and fins clipped to 5 mm. More fin area is therefore not
free thrust at prolonged speeds. This matters for any "bigger tail lobe" design (§6).

### 2.2 Flying fishes (Exocoetidae), for comparison only

| Quantity | Value | Source, year | Read-level |
|---|---|---|---|
| Stroke (tail-beat) frequency at the leap | **21.2 ± 4.6 Hz** | Makiguchi et al. 2013, *Aquatic Biology* 18:105–111, doi:10.3354/ab00494; *Cypselurus heterurus doederleini*, acceleration loggers | search-summary (int-res.com and doaj.org blocked by network policy) |
| Leap speed | **3.9–5.2 m/s**, reported as "39–52 % of previously reported maximum swimming speeds" | Makiguchi et al. 2013 | search-summary |
| Taxiing tail-beat frequency | **13.5 Hz**; the minimum tail force for a 200 g fish is estimated at ~2 N | APS March Meeting 2024 abstract, "Flying fish taxiing on the water's surface" (authors not retrieved) | search-summary; could-not-access (host blocked) |
| Taxiing tail-beat frequency | "about 50 Hz based on the observation by Hertel (1966)" | quoted inside Deng et al. 2019 | search-summary (secondary); Hertel not read |
| Tail-beat frequency | "0.5–1.0 Hz" | Sci. Rep. 2023 sailfish–flying-fish acoustics paper (PMC10449807) | search-summary. Conflicts with every other source, and its context is probably not taxiing; recorded, not used |
| CFD taxi, 0.25 m, 0.191 kg fish | taxiing at 10 m/s needs **36 W** at 50 Hz (15° deflection). Submerged cruising at 10 m/s needs **350 W** at 145 Hz. With 350 W, taxiing reaches **16.5 m/s** | Deng, Wang, Zhang & Mao 2019, bioRxiv 10.1101/765560 | abstract (full text returned HTTP 429). **Simulated, not observed** |
| "Taxiing ... can probably accelerate the flying fish to 15–20 m/s" | — | Deng et al. 2019 | search-summary. Authors' speculation |

**Disagreement preserved: flying-fish tail-beat frequency.** The sources give 13.5 Hz (taxi,
APS 2024), 21.2 Hz (leap, loggers, 2013), and ~50 Hz (taxi, Hertel 1966, second-hand). These
may be different phases of the launch, different species, or different methods. I cannot tell
which, and I do not average them.

### 2.3 Other small fish that leave the water

- **Guppy** (*Poecilia reticulata*, SL 1.85 ± 0.35 cm): peak in-water velocity
  **1.02 ± 0.34 m/s** just before or at the interface, and **1.24 ± 0.30 m/s** peak in air
  "immediately after breaking the interface". Jump height 6.54 ± 1.92 cm. Fish "continue with
  whole body thrusts and tail beats, even when out of the water". The authors *hypothesise* that
  these movements help reach peak velocity and attribute part of the gain to lower drag.
  Source: Soares & Bierman 2013, *PLoS ONE* (PMC3629028), full-text. The paper's Discussion
  gives 100.16 cm/s, which differs from the Results figure.
- **Hatchetfishes (Gasteropelecidae):** jumping is ballistic (Wiest 1995, via challenge 3,
  search-summary). A 2026 *ICB* abstract (Kapoor et al., doi:10.1093/icb/icag131, abstract)
  quantifies aerial escapes, but its abstract gives no speeds. Take-off speed: **unknown**.

The guppy is the closest measured analogue of a small-fish partial taxi. Its in-air peak is
~21 % above its in-water peak. How much of that comes from tail thrust and how much from
shedding water drag is not separated in the paper.

### 2.4 Scope of negative searches

**Adult zebrafish caudal-fin thrust.** I searched for a direct force measurement:
- web searches: "zebrafish caudal fin thrust force measurement mN adult"; larval/adult PIV wake
  impulse and fast-start force (extended mode);
- Europe PMC queries on adult escape velocity.

None of these returned a measured adult thrust. The only zebrafish caudal-fin forces found are
**µN-scale bending-stiffness probes** (*J. Exp. Biol.* 221 jeb171777, search-summary), and those
are not thrust. Inverse-dynamics force estimates exist for **5 dpf larvae** only (bioRxiv
570812, search-summary). Not searched: Web of Science, Google Scholar, theses.

**Danos & Lauder numerical velocities.** These were not retrieved, because Table 1 is an image.
The value in §3.1 is back-calculated from their published Reynolds number.

## 3. What I computed (all calc; script `S24_calcs.py`)

### 3.1 Adult zebrafish burst speed from Danos & Lauder's Reynolds number

U = Re·μ/(ρL). The measured inputs are Re = 27,800 and μ = 1 mPa·s. ρ = 1000 kg/m³ is assumed.
The paper says only "fish length". I assume L = TL = 33 mm, with an assumed SL ≈ 0.8 TL as an
alternative.

- L = TL: **U = 0.842 ± 0.065 m/s (25.5 TL/s)**.
- L = SL: **U = 1.05 ± 0.08 m/s**.
- Consistency check: the 10 and 20 mPa·s data give 0.71 and 0.50 m/s (TL basis). These fall in
  the order the paper reports (velocity drops with viscosity).

This is the mean, across sequences, of each sequence's **peak** speed. It is not an exit speed.
It is the first adult zebrafish burst value in this project. It is **derived from a measured
quantity**, not read from a table. It sits 1.5× above Palstra's Ucrit and 3–4× above
Wakamatsu's.

### 3.2 The kinematic (Strouhal) ceiling: the binding constraint

A flapping tail makes net thrust only while its lateral speed is a sizeable fraction of the
forward speed. Swimming and flying animals cruise at St = fA/U ≈ 0.2–0.4 (Taylor, Nudds &
Thomas 2003, *Nature* 425:707, abstract). I use **St 0.15** as an assumed, generous lower edge
for thrust production. A is the peak-to-peak tail amplitude, assumed to be 0.15–0.25 TL.

**Calibration (calc).** At Ucrit 0.548 m/s and St 0.3, fA = 0.164 m/s. At the measured 21 Hz
ceiling that implies A = 7.8 mm = 0.20 TL, a plausible amplitude. The same model, applied to a
0.25 m exocoetid at 10 m/s, gives 60 Hz. That is close to the ~50 Hz attributed to Hertel and
used in Deng's CFD. These are consistency checks, not validation.

**Frequency needed to keep producing thrust at the target speed (calc), f = St·U/A:**

| Target | A | St 0.15 | St 0.2 | St 0.3 | St 0.4 |
|---|---|---|---|---|---|
| 1.95 m/s (3-BL) | 0.15 TL (6 mm) | 49 Hz | 65 | 97 | 130 |
| 1.95 m/s | 0.20 TL (8 mm) | 37 | **49** | **73** | 98 |
| 1.95 m/s | 0.25 TL (10 mm) | 29 | 39 | 58 | 78 |
| 5.84 m/s (1-BL) | 0.25 TL (10 mm) | **88** | 117 | 175 | 234 |
| 5.84 m/s | 0.20 TL (8 mm) | 110 | 146 | 219 | 292 |

**Maximum taxi speed at the measured frequency ceilings (calc), U = fA/St:**

| f | central (A 0.2 TL, St 0.3) | generous (A 0.25 TL, St 0.15) | stingy (A 0.15 TL, St 0.4) |
|---|---|---|---|
| 21 Hz (max steady swimming, measured) | **0.56 m/s** | 1.40 | 0.32 |
| 52 Hz (max escape, measured) | **1.39 m/s** | 3.47 | 0.78 |

So at the frequencies an adult zebrafish can **sustain**, the central estimate of the taxi
ceiling is Ucrit itself (0.56 vs 0.548 m/s). Even the most generous corner reaches only
1.40 m/s. At the **transient** escape maximum, the central estimate (1.39 m/s) still falls short
of 1.95 m/s. Only generous corners clear it. The 1-BL target needs 88–292 Hz, which is
**1.7–5.6×** the highest frequency measured in any adult zebrafish.

### 3.3 Is thrust *force* the limit? Probably not at 1.95 m/s

**Thrust capacity at Ucrit.** At Ucrit, steady thrust equals body drag. Assumed inputs: wetted
area 6 cm², laminar Blasius friction, form factor 1.2, and a ×1–3 undulation multiplier. This
gives **1.1–3.3 mN** at 0.548 m/s, and 0.3–0.9 mN at Wakamatsu's 0.236 m/s (calc).

**Thrust needed at the end of the taxi, wings carrying W.** This is air drag W/(L/D) plus
two-sided laminar friction on the submerged lower lobe. Assumed inputs: L/D 4–8; lobe chord
6 mm (measured fin length); lobe area 0.15–0.30 cm² per side. Spray, ventilation, wave drag and
pressure drag are **omitted**, so these figures are lower bounds.

| Target | Thrust needed | Power at η = 0.5 / 0.2 |
|---|---|---|
| 1.95 m/s | **1.2–2.4 mN** | 12–58 W/kg body |
| 5.84 m/s | **4.1–8.2 mN** (lobe friction dominates: 3.6–7.3 mN) | 120–600 W/kg body |

For reference, Deng's simulated exocoetid taxi at 10 m/s costs 36 W / 0.191 kg ≈ **190 W/kg
body** (calc from their abstract's numbers).

**Inference, mine.** At 1.95 m/s the force needed is about what the tail already makes at Ucrit,
and the power is within the range the glide analysis cites for fish muscle. So force and power
are not what fails. What fails is the tail's ability to make that force *while the water
streams past it at 1.95 m/s*. That takes the frequency in §3.2. At 5.84 m/s, force, power and
frequency all fail together.

### 3.4 Taxi run length (calc)

From 0.84 m/s to the target under an assumed constant **net** force:

| Target | Net force | Distance | Time | Tail beats at 52 Hz |
|---|---|---|---|---|
| 1.95 m/s | 2 mN | 0.31 m (8 BL) | 0.22 s | 12 |
| 1.95 m/s | 1 mN | 0.62 m | 0.44 s | 23 |
| 1.95 m/s | 0.5 mN | 1.24 m | 0.89 s | 46 |
| 5.84 m/s | 0.5–2 mN | 3.3–13.4 m (83–334 BL) | 1–4 s | 52–208 |

The 3-BL taxi would therefore have to hold an escape-level tail-beat frequency for roughly
12–46 consecutive beats. Kyriakatos et al. report 52 Hz only as a maximum reached during escape.
Whether it can be sustained for 0.2–0.9 s is **unknown**.

### 3.5 Weight support during the taxi (calc + inference)

At U₀ = 0.84 m/s the wings carry 18.7 % of W (3-BL) or 2.1 % (1-BL). The remaining 81–98 %
(3.2–3.8 mN) must come from somewhere: vertical force from the beating lobe, planing lift on the
body, or both. Otherwise the body sits in the water. A fish sitting in the water is
**surface-swimming**, not taxiing, and surface swimming pays wave drag on top of the submerged
drag.

**Inference.** A symmetric zebrafish caudal fin has no long ventral lobe to stay submerged while
the body rides high. Exocoetids taxi with an elongated lower lobe. That geometry is an input the
zebrafish lacks, and its required size is **not computed here**.

**Froude numbers (calc).** At 1.95 m/s, Fr = U/√(gL) = 3.1 for the zebrafish. At 10 m/s,
Fr = 6.4 for a 0.25 m exocoetid. The zebrafish would taxi at a lower Froude number, which means
gravity matters relatively more and the case for planing support is weaker. This is an
inference only. No planing coefficient was computed.

## 4. The answer, with its evidence level

**Evidence level: derived.** The numbers are arithmetic on measured literature inputs (Ucrit,
Re, tail-beat frequencies, fin length) combined with stated assumptions (St band, amplitude,
areas, L/D). Nothing here is observed or simulated by me.

- **1-BL wing (5.84 m/s): taxiing cannot close the gap.** It would need the tail to keep
  producing thrust at 88–292 Hz (calc). That is 1.7–5.6× the 52 Hz escape maximum measured in
  adult zebrafish. It would also need 4–8 mN of thrust at 5.84 m/s and a taxi run of 3–13 m.
  Every element fails, and they fail independently.
- **3-BL wing (1.95 m/s): not refuted, not shown feasible.** The central estimate needs
  ~73 Hz. The best corner needs 29 Hz. The measured ceilings are 21 Hz sustained and 52 Hz
  transient. At sustained swimming frequencies, the central estimate says the taxi **cannot
  exceed Ucrit meaningfully** (0.56 m/s). That is the brief's refutation condition, met by
  **calculation, not by measured thrust**. At escape frequency, a 1.4 m/s taxi is the central
  case (calc), and 1.95 m/s needs favourable amplitude and Strouhal values held for 12–46 beats.
- **Taxiing does change the barrier's character.** It turns a single-impulse exit-speed problem
  (a 5.4× KE gap from 0.84 m/s for the 3-BL wing) into a **sustained high-frequency tail-beat
  problem plus a weight-support problem**. The force and power needed at 1.95 m/s are not the
  obstacle (calc).

## 5. What this does NOT establish

- **It is not a measurement of caudal thrust.** The brief asked for measured caudal-fin thrust.
  None exists in what I could reach for adult zebrafish (scope in §2.4). The thrust figures in
  §3.3 are drag balances on assumed areas and coefficients. They could be wrong by 2–3×.
- **The Strouhal band is a cruise-efficiency band, not a hard thrust cutoff.** Taylor et al.
  2003 describe where animals *cruise efficiently*. Accelerating fish, and the CFD flying fish,
  may produce net thrust at lower St, and thrust from a surface-piercing lobe may follow
  different rules. If net thrust persists down to St ≈ 0.1, every frequency in §3.2 falls by
  a third or more. St 0.15 is my assumption, not a measured threshold.
- **Amplitude is assumed.** I did not retrieve adult zebrafish tail-beat amplitude. A taxiing
  lobe may sweep differently from a swimming tail, and the body pivoting in air could raise it.
- **The 52 Hz value** is an EMG frequency maximum during escape (Kyriakatos 2011). It is not a
  sustained tail-beat frequency. It may not equal a kinematic tail-beat frequency in a
  steady-state taxi, and it was measured in normal fish, not in fish with a taxiing posture.
- **The 0.84 m/s burst speed** is back-calculated, and the length basis (TL vs SL) is uncertain:
  with SL it is 1.05 m/s. It is a mean of per-sequence peaks, not a verified exit speed. The
  fish were 33 mm TL, not 40 mm.
- **The Ucrit disagreement** (0.548 vs 0.19–0.28 m/s) is unresolved. If Wakamatsu is right, the
  thrust-capacity estimate in §3.3 falls about 3×, which strengthens the negative.
- **Weight support during the taxi was not modelled quantitatively.** No planing or lobe-lift
  coefficient was computed. This could be a second, independent barrier, or it could be solved
  by a lobe design. I do not know which.
- **Drag terms omitted:** spray, ventilation (air drawn down onto the lobe), wave drag, the
  membrane's water drag before exit, and the transition from submerged to surface. All of these
  increase the thrust needed. None is quantified.
- **Muscle performance at 50–75 Hz is unknown** for adult zebrafish fast muscle at 28 °C. This
  includes power output, fatigue over 0.2–0.9 s, and whether the twitch kinetics allow it.
  Larvae reach ~100 Hz (search-summary), but larval muscle and body size differ.
- **The exocoetid comparison is weak.** The tail-beat frequency sources disagree 13.5 / 21.2 /
  ~50 Hz. Deng et al. is a simulation, read at abstract level only. I could not read the APS
  abstract or Makiguchi beyond search summaries.
- **The 1.95 and 5.84 m/s targets are inherited** from one AR 5, C_L 0.6 geometry. Lower-AR
  wings lower V_g (challenge 3). At V_g ≈ 2 m/s (1-BL, AR 1, C_L 1.0) the 1-BL case would
  resemble the 3-BL case here.
- **Behaviour was not tested.** Nothing here shows that a zebrafish would hold a tail-down
  posture, or that its escape circuit could drive a long, steady high-frequency bout rather
  than a C-start followed by a decay.

## 6. What would change the answer

| Measurement or change | What it would settle | Direction |
|---|---|---|
| **Adult zebrafish caudal thrust vs flow speed and tail-beat frequency** (tethered fish on a force sensor in a flume, or PIV wake impulse), up to 2 m/s inflow | Whether the tail makes net thrust at St < 0.2. This directly runs the brief's refutation test | Thrust gone above ~0.6–1.4 m/s → negative confirmed. Net thrust at 2 m/s at ≤ 52 Hz → the 3-BL case becomes open |
| **Danos & Lauder 2012 Table 1** (PDF) | Replaces the back-calculated 0.84 m/s with the measured value, and gives the length basis | ±25 % on U₀. Small effect on the verdict |
| **Duration over which an adult can hold ≥ 50 Hz** (EMG or kinematics in long escape bouts) | Whether 12–46 beats at escape frequency are possible | Short bursts only → 3-BL closed by calculation |
| **Tail-down surface swimming trials** with an artificial lower-lobe extension (gene-free test: a glued fin prosthesis) | Weight support, and the drag of a surface-piercing lobe at 1–2 m/s | Direct test of §3.5 |
| **Design: an elongated lower caudal lobe** (hypocaudal; a developmental question for the organ/tissue scales) | Keeps thrust area in the water while the body rides high. Wakamatsu's data warn that a longer fin cost Ucrit in long-fin strains | Needed for any taxi; not sufficient by itself |
| **Design: faster axial fast muscle** (higher twitch frequency; a muscle-scale question) | The kinematic ceiling scales directly with f | Doubling the sustained f to ~42 Hz moves the central taxi ceiling to ~1.1 m/s, which is still short |
| **Design: lower V_g** (low-AR, high-C_L wing) | Brings the target down to the 1.4 m/s that escape-frequency taxiing reaches in the central case | The most effective single lever on paper. It is a wing-scale question, not a behaviour one |
| **Full texts:** Deng et al. 2019, Makiguchi et al. 2013, APS 2024 abstract, Hertel 1966 | Settles the 13.5 / 21 / 50 Hz disagreement and the exocoetid St during taxi | Calibrates §3.2 |

## Sources

| # | Source | Read-level | Used for |
|---|---|---|---|
| 1 | Palstra et al. 2010, *PLoS ONE* 5:e14483 | search-summary (abstract quoted); full text could-not-access | Ucrit 0.548 m/s |
| 2 | Plaut 2000, *J. Exp. Biol.* 203:813 (via #1) | search-summary | Ucrit ≈ 0.56 m/s |
| 3 | Wakamatsu, Ogino & Hirata 2019, *Sci. Rep.* 9:16307, PMC6841939 | full-text | Ucrit 0.19–0.28 m/s (disagreement); fin length; fin-clip effect |
| 4 | Danos & Lauder 2012, *J. Exp. Biol.* 215:1854, doi:10.1242/jeb.068957 | full-text (first 100k of 121k characters; tables are images) | Re 27,800; TL 33 mm; burst speed back-calculation |
| 5 | Kyriakatos et al. 2011, *J. Neurosci.*, PMC6623330 | full-text (first 100k of 101k characters) | 21 Hz swimming, 52 Hz escape maxima |
| 6 | Taylor, Nudds & Thomas 2003, *Nature* 425:707, doi:10.1038/nature02000 | abstract | St 0.2–0.4 |
| 7 | Deng, Wang, Zhang & Mao 2019, bioRxiv doi:10.1101/765560 | abstract (full text HTTP 429); Hertel 50 Hz quote at search-summary | simulated taxi 36 W at 10 m/s, 50 Hz |
| 8 | Makiguchi et al. 2013, *Aquatic Biology* 18:105, doi:10.3354/ab00494 | search-summary (host blocked) | 21.2 Hz, leap 3.9–5.2 m/s |
| 9 | APS March Meeting 2024, "Flying fish taxiing on the water's surface" | search-summary; could-not-access (host blocked) | 13.5 Hz, ~2 N for 200 g |
| 10 | Sailfish–flying-fish acoustics, *Sci. Rep.* 2023, PMC10449807 | search-summary | 0.5–1.0 Hz (conflicting, not used) |
| 11 | Soares & Bierman 2013, *PLoS ONE*, PMC3629028 | full-text | guppy 1.02 → 1.24 m/s across the interface |
| 12 | Kapoor et al. 2026, *Integr. Comp. Biol.*, doi:10.1093/icb/icag131 | abstract | hatchetfish aerial escapes; no speeds |
| 13 | Larval swimming review, *J. Exp. Biol.* 221 jeb149583 (citing Müller & van Leeuwen 2004) | search-summary | 28 g, larval only, not used |
| 14 | *J. Exp. Biol.* 221 jeb171777, caudal-fin stiffness in vivo | search-summary | shows only µN stiffness forces exist; not thrust |
| 15 | `zebrafish-glide-physics.md`, `challenge-2.md`, `challenge-3.md` (sibling branches) | full-text | V_g targets, Ucrit framing, AR sensitivity |

Hosts blocked this session: meetings-archive.aps.org, int-res.com, doaj.org. biorxiv.org
returned rate-limit errors (HTTP 429).

```swarm-result
{"subproblem": "S24", "evidence": "derived", "answer": "Surface taxiing cannot close the 1-BL (5.84 m/s) launch gap and does not demonstrably close the 3-BL (1.95 m/s) gap: the binding limit is tail-beat frequency, not thrust force, because keeping a caudal lobe producing thrust at 1.95 m/s needs ~49-73 Hz (St 0.2-0.3, A 0.2 TL; calc) against measured adult zebrafish maxima of 21 Hz sustained and 52 Hz transient escape, and at sustained frequencies the calculated taxi ceiling (~0.56 m/s) is Ucrit itself.", "key_number": "~73 Hz tail-beat frequency needed to taxi at 1.95 m/s (range 29-98 Hz) vs 52 Hz measured adult escape maximum", "blocked_on": "No measured adult zebrafish caudal-fin thrust vs flow speed exists in the sources reachable; Danos & Lauder 2012 Table 1 velocities (image), Deng et al. 2019 full text, Makiguchi 2013 and APS 2024 abstracts were not accessible"}
```
