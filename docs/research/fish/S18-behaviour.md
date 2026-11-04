# S18 — Could a zebrafish control attitude in air? (scale: behaviour)

Project: `zebrafish-flight`. Subproblem S18.
Date written: 2026-11-04.
Evidence level of the answer: **derived** (my arithmetic on assumed geometry, combined with literature read mostly at abstract or search-summary level). Nothing in this file is a new observation.

---

## 1. The question, restated with the numbers that make it hard

Take the project's baseline animal: *Danio rerio*, length L ≈ 4 cm, mass m ≈ 0.4 g. (These two values come from the project brief. I did not re-source them.) Weight is W = m·g ≈ 3.9 × 10⁻³ N.

The question has two parts:

- **(a) Passive.** Can an engineered planform at this size be *statically and dynamically stable* in pitch, roll and yaw, so that it does not tumble without any feedback?
- **(b) Active.** Could a zebrafish nervous system and set of control surfaces *correct* attitude in air quickly enough? In particular, is vestibular sensing fast enough compared with the airframe's own dynamics?

Four facts make it hard:

1. **Little time aloft.** A ballistic jump by a fish of this size lasts about 0.23 s. That figure is computed from a measured guppy jump height (§2, §3). A useful glide would last much longer than the natural attitude timescales.
2. **Airframe dynamics are fast.** At glide speeds of a few m/s, the computed pitch dynamics sit at about 1–3 Hz (§3). An *unstable* configuration doubles its pitch error in roughly 40–120 ms.
3. **The vestibular data are slow and larval.** The zebrafish vestibular-reflex data I could find are larval or early-juvenile, and measured only at ≤ 0.5 Hz. I found no frequency response for the adult semicircular-canal reflex (§2).
4. **In ballistic flight the otoliths lose their gravity reference.** This is physics, not an observation. A body in free fall feels zero specific force, so a gravity-sensing utricle has no gravity vector to read. In a steady glide it reads the aerodynamic load instead (§3.6).

## 2. What is measured

Read-levels: full-text | abstract | listing | search-summary | could-not-access. Where my access went through a fetch tool that summarised the page for me, I say so. That is weaker than reading the page myself.

### 2.1 Zebrafish vestibular and gaze reflexes

| # | Value | Source | Year | Read-level |
|---|---|---|---|---|
| V1 | Linear (utricle-driven) VOR first seen at 72 hpf. Normalised amplitude rises from 0.04 ± 0.04 at 60 hpf to 0.62 ± 0.27 at 120 hpf. Only one stimulus was used: 0.25 Hz, ±45° tilt about an earth-horizontal axis. Rotation about an earth-vertical axis gave 0.01 ± 0.05, i.e. no canal-driven response. **No gain-vs-frequency curve exists in this paper.** | Mo, Chen, Nechiporuk, Nicolson, *BMC Neurosci* 11:110, doi:10.1186/1471-2202-11-110 | 2010 | full-text, via fetch-tool summary of PMC2941499 |
| V2 | Angular (canal) VOR was "undetectable until 35 dpf" in zebrafish. Larval fish lack a significant angular VOR at actively feeding stages. OKR gain was > 0.8 at low frequency and fell to < 0.3 at 3 Hz (multi-species statement). | Beck, Gilland, Tank, Baker, *J Neurophysiol* 92:3546–3561, doi:10.1152/jn.00311.2004 | 2004 | abstract (ZFIN / Princeton listing, via search summary). Full text **could-not-access**: journals.physiology.org is blocked by this session's network policy, and the ZFIN page returned HTTP 503. The "35 dpf" figure is quoted second-hand from Sun et al. 2018 (V4) and Mo et al. 2010 (V1). |
| V3 | Angular VOR present at 3 dpf, about 1 h after OKR onset. Its development was qualitatively normal in dark-reared fish. | Easter & Nicola, *Dev Psychobiol* (Wiley 1997) | 1997 | search-summary |
| — | **Disagreement, preserved:** V2 puts canal VOR onset at about 35 dpf. V3 puts it at 3 dpf. Beck et al. suggest that the Easter & Nicola result partly reflects OKR leakage (reported by Sun et al. 2018). I do not resolve this. | | | |
| V4 | VOR measured at 6 dpf with a 30 rpm (≈ 0.5 Hz) stimulus. Reported as a unitless "VOR score": WT 0.0657 ± 0.0128. *dlx3b* morphants, which have only the saccular otolith, gave 0.0056 ± 0.0042. Conclusion: the utricle is required for the linear VOR. | Sun et al., *Front Cell Neurosci* 12:257 | 2018 | full-text, via fetch-tool summary |
| V5 | Vertical (roll-axis) VOR at 4 dpf: **gain peaks at 0.33** (at 90 deg s⁻¹, about 0.25 Hz). Tested only at 0.0625–0.25 Hz. Phase lag < 2°. Vertical OKR: no response above 0.5 Hz; maximum gain 0.19 at 0.25 Hz. **No formal cutoff frequency or bandwidth is reported.** | Burkhardt, Möller, Deligand, Fichtner, Hladnik, Arrenberg, *J Exp Biol* 229(8): jeb251770 | 2026 | full-text (first ~100k of ~121k characters), via fetch-tool summary of PMC13091498 |
| V6 | Larval canals are too small to transduce normal head movement, so the utricle is the only functional vestibular sensor in larvae. Canals begin to work "as larvae become juveniles". Swim bouts occur about once per second. At 3 dpf there are no measurable eye movements to pitch or roll tilt; by 10 dpf compensation is full. **The review gives no canal radius and no adult bandwidth.** | Bagnall & Schoppik, *Curr Opin Neurobiol* 53:83–89 | 2018 | full-text, via fetch-tool summary of PMC6242715 |
| V7 | Larval zebrafish have their centre of mass rostral to their centre of volume, which gives a constant nose-down torque in water. Larvae time swim initiation to restore posture. | Ehrlich & Schoppik, *Curr Biol* 27(3):334–344 | 2017 | abstract (via search summary) |
| V8 | A utricle-dependent VOR for pitch and roll tilts, mediated by the tangential nucleus, in larvae without functional canals. | Bianco et al. (Schoppik a co-author), *Curr Biol* | 2012 | search-summary. Full text **could-not-access**: cell.com PDF returned 403. |
| V9 | **Adult zebrafish angular-VOR gain and phase versus frequency: not found.** One search summary says that adult fish VOR gain is near unity and set by visual experience (Easter & Nicola 1997), but the text it came from was garbled, so I do not rely on it. | — | — | **unknown**. Searches tried: "adult zebrafish vestibulo-ocular reflex frequency response gain"; "adult zebrafish semicircular canal angular vestibulo-ocular reflex sinusoidal rotation gain phase Hz" (extended). |

### 2.2 Aerial behaviour of small non-exocoetid teleosts (the refutation test)

| # | Taxon, size | Finding | Source | Year | Read-level |
|---|---|---|---|---|---|
| A1 | *Poecilia reticulata* (guppy), SL 1.85 ± 0.35 cm | Jump height 6.54 ± 1.92 cm (3.52 BL). Maximum air speed 123.57 ± 30.0 cm s⁻¹. Tail beats continue after leaving the water. **No in-air rotation or attitude analysis.** (The paper also lists mass as "98 ± 10 gm", which looks like a unit error. Its in-water maximum speed differs between sections: 102.36 vs 100.16 cm s⁻¹.) | Soares & Bierman, *PLoS ONE* 8:e61617 | 2013 | full-text, via fetch-tool summary |
| A2 | Gasteropelecidae (freshwater hatchetfish; *Carnegiella* adults are about 3 cm, a size I did not re-source) | High-speed video at 200 fps. Take-off is pectoral abduction plus a C-start. Aerial paths are **ballistic**. "Active flight … unlikely." | Wiest, *J Zool* 236:571–592 | 1995 | listing / search-summary (Wiley abstract page seen only through the search tool) |
| — | **Disagreement, preserved:** a University of Michigan teaching slide (no citation) and some hobbyist pages say hatchetfish flap their pectoral fins to gain altitude. Wiest 1995 says otherwise. | | | | search-summary |
| A3 | Hatchetfish pectoral motor pools | High-velocity, large-amplitude pectoral motions for "aerial excursions". Fins are moved forward before the downstroke. **I could not find out whether any of this happens while airborne.** | Gutjahr, Bothe, Jonsson, Chagnaud, *PNAS*, doi:10.1073/pnas.2413415121 | 2024 | listing / search-summary. Full text **could-not-access** (pnas.org 403). |
| A4 | *Pantodon buchholzi* (African butterflyfish) | Startle jump is "ballistic-like", "well-modeled by a parabola". In-flight trunk and fin movements do **not** increase distance travelled. | Saidel, Strain, Fornari, *Environ Biol Fish*, doi:10.1023/B:EBFI.0000043153.38418.cd | 2004 | abstract (via search summary) |
| A5 | *Toxotes microlepis* (archer fish), SL 6.8–11.1 cm, 7.9–28.3 g | Orientation is set before leaving the water. The snout trajectory is predominantly vertical. Posture changes in the "glide" (ballistic) phase are small. Fins stay abducted until exit; fin use after exit is not described. Ballistic phase about 84 ms. | Shih, Mendelson, Techet, *J Exp Biol* 220:1411–1422 | 2017 | full-text (first 100k of 171k characters), via fetch-tool summary |
| A6 | Arowana, aerial prey capture | Larger-amplitude body motions in aerial feeding. Whether this involves in-air attitude correction: **unknown**. | *Proc R Soc B* 292:20251308 (authors not retrieved) | 2025 | listing only. Full text **could-not-access** (403). |
| A7 | *Euleptorhamphus viridis* (ribbon halfbeak; Beloniformes, Hemiramphidae, **not** Exocoetidae) | Reported to glide by twisting the rear body 90° so that the dorsal and anal fins act as wings. A wind-tunnel 3D-printed model shows the rear body must sit above the pectoral "wings". Reported 50 m in two jumps. | AsianScientist press piece about a 2017 wind-tunnel study; primary citation **not retrieved**. Distance figure from an encyclopedia.com Beloniformes overview with no primary source. | 2017 | search-summary |

### 2.3 Flying-fish stability (context only; not a template)

| # | Finding | Source | Year | Read-level |
|---|---|---|---|---|
| F1 | Stuffed *Cypselurus hiraii* in a wind tunnel: lift-to-drag ratio comparable to birds. Press reports say the fish was unstable with fins swept back, and that the pectoral-plus-pelvic arrangement gave pitch stability. Ground effect raised lift-to-drag ratio. | Park & Choi, *J Exp Biol* 213:3269–3279, doi:10.1242/jeb.046052 | 2010 | abstract + press (search-summary). The stability statements are **unconfirmed against the paper**. |

### 2.4 Values I did not get

- Danio pectoral/caudal fin areas and spans, adult body moment of inertia, and adult fast-start exit speed: **unknown**. I did not search for these specifically; they belong to other subproblems.
- The "designed surfaces" this question asks about: **unknown.** I found no other S-subproblem document in this repository (`grep -ril zebrafish` over `*.md` returned nothing). I could not read the designed geometry, so §3 uses a stated reference design.
- Mauthner-cell or vestibulospinal loop latency: not searched in this session, so **unknown here**. §3 states the latency a controller would *need* rather than claiming what the fish has.

## 3. What I computed

**Everything in this section is my computation, not a measurement.** It uses textbook rigid-body and strip-theory aerodynamics. Script: inline below, run with Python 3. Constants: ρ_air = 1.2 kg m⁻³, g = 9.81 m s⁻², ν_air = 1.5 × 10⁻⁵ m² s⁻¹.

### 3.1 Assumptions for the reference design (not measured; chosen to be plausible, change them freely)

- m = 0.4 g and L = 4 cm (project brief).
- Pitch inertia: slender rod, I_y = m L²/12 = 5.3 × 10⁻⁸ kg m². Fin mass is ignored.
- Roll inertia: cylinder of radius 3 mm, I_x = m r²/2 = 1.8 × 10⁻⁹ kg m². Fin mass is ignored. **The 3 mm radius is assumed, not measured.**
- Rear stabilising surface (enlarged caudal and/or pelvic fin): S_t = 1 cm², moment arm l_t = 2 cm behind the centre of mass, lift slope a_t = 1.6 rad⁻¹ (low aspect ratio).
- Main lifting surface (enlarged pectorals): S = 10 cm², span b = 6 cm, lift slope a = 2.5 rad⁻¹.
- Glide speeds V = 1, 2, 3 m s⁻¹. For anchoring only: the guppy's measured maximum air speed is 1.24 m s⁻¹ (A1).

### 3.2 Wing area needed to glide (computation)

S_req = 2W / (ρ V² C_L):

| V (m s⁻¹) | C_L = 0.8 | C_L = 1.2 |
|---|---|---|
| 1.0 | 82 cm² | 55 cm² |
| 1.24 | 53 cm² | 35 cm² |
| 2.0 | 20 cm² | 14 cm² |
| 3.0 | 9 cm² | 6 cm² |

At the one measured speed for a fish of this size class (1.24 m s⁻¹), the animal needs 35–53 cm² of wing. That is roughly ten times the lateral silhouette of a 4 cm fish; I did not measure that silhouette, I estimate it at about 4 cm × 0.8 cm ≈ 3 cm². The 10 cm² reference wing is therefore **undersized** at 2 m s⁻¹. I keep it for the attitude calculation because a larger wing only increases roll damping, so this choice is conservative for roll.

### 3.3 Time aloft without gliding (computation on a measured input)

t = 2√(2h/g) with h = 6.54 cm (A1) gives **t ≈ 0.23 s**.

### 3.4 Pitch dynamics (computation)

- Static pitch stiffness from the rear surface: M_α = q S_t l_t a_t, with q = ½ρV².
- Natural frequency: ω_n = √(M_α / I_y).
- Damping from the rear surface: M_q = q S_t l_t² a_t / V, giving ζ = M_q / (2 I_y ω_n).

| V | q (Pa) | M_α (N m rad⁻¹) | ω_n (rad s⁻¹) | f_n (Hz) | ζ (tail only) | e-fold / doubling time if the margin were **negative** |
|---|---|---|---|---|---|---|
| 1 | 0.60 | 1.9 × 10⁻⁶ | 6.0 | **0.95** | 0.06 | 116 ms |
| 2 | 2.40 | 7.7 × 10⁻⁶ | 12.0 | **1.91** | 0.06 | 58 ms |
| 3 | 5.40 | 1.7 × 10⁻⁵ | 18.0 | **2.86** | 0.06 | 39 ms |

ω_n scales as V√(S_t l_t / I_y). The tail-only ζ ≈ 0.06 is a lower bound, because the wing and body add pitch damping that I have not modelled.

**Stability margin.** The pitch result above assumes the rear surface makes the centre of mass sit ahead of the neutral point, i.e. a positive static margin. For a glider with forward pectoral wings and a rear caudal/pelvic stabiliser, this is the same qualitative arrangement that press reports attribute to Park & Choi (F1). I cannot give a numerical static margin without the designed planform; it is **unknown** (§2.4). With no rear surface, a forward wing ahead of the centre of mass is destabilising, and the airframe diverges on the timescales in the last column.

### 3.5 Roll damping and control authority (computation)

- Strip-theory roll damping: D = q S a b² / (12 V). Roll time constant τ_roll = I_x / D gives **4.0, 2.0 and 1.3 ms** at V = 1, 2 and 3 m s⁻¹. Roll rate is therefore damped almost instantly; roll *angle* is neutrally stable unless there is dihedral or a keel effect.
- Pitch control authority from deflecting the rear surface by δ = 0.2 rad (about 11°): angular acceleration M_α·δ / I_y = **7, 29 and 65 rad s⁻²**. At 2 m s⁻¹ that can change pitch by about 0.5 rad within 0.18 s. It is ample *if* the surface exists and is actuated.
- Reynolds number: about 2.7–8 × 10³ (body) and 0.7–2 × 10³ (1 cm fin chord). This is the low-Re regime, where lift slopes and lift-to-drag ratio are degraded; the lift slopes assumed in §3.1 may be optimistic.

### 3.6 Sensing and feedback (derived)

- **What the otoliths read in air** (physics). An otolith organ senses specific force: (total force − gravity)/m = aerodynamic force/m. In ballistic flight that is ≈ 0, so the utricle loses its "down" reference. In steady gliding it reads about 1 g along the lift vector, which tells it the load, not the attitude relative to the vertical. Utricle-only sensing, which is the measured larval configuration (V1, V4, V6), therefore **cannot by itself sense attitude in air**. Angular-rate sensing (canals) and vision would be needed.
- **Required loop speed** (derived control rule of thumb). Stabilising an unstable mode of rate λ needs a loop crossover at or above λ. A pure delay τ_d costs phase ω τ_d, and keeping it below about 0.5 rad requires τ_d ≲ 0.5/λ, which is **≲ 40 ms at 2 m s⁻¹ and ≲ 28 ms at 3 m s⁻¹**. Damping a stable but lightly damped (ζ ≈ 0.06) 1–3 Hz mode needs rate feedback with useful gain at 1–3 Hz.
- **Comparison with measurement.** The only zebrafish vestibular-reflex frequency data I found were taken at ≤ 0.5 Hz in larvae or early juveniles. The best roll-VOR gain was 0.33 at about 0.25 Hz (V5); vertical OKR showed no response above 0.5 Hz (V5); OKR gain was < 0.3 at 3 Hz (V2). The required band of 1–3 Hz lies **above every measured zebrafish vestibular/gaze frequency I found, by a factor of about 2–10**. **This is not evidence that adult canals cannot do it.** The adult canal frequency response is unknown (V9), and gaze reflexes are not postural reflexes.

## 4. The answer

**Evidence level: derived.**

The answer differs for the two parts of the question:

- **(a) Passive.** A 0.4 g zebrafish-derived glider *could* be stable in pitch only if the design adds a rear stabilising surface and places the centre of mass ahead of the neutral point. Roll rate would then be strongly damped (τ ≈ 1–4 ms, computed). The pitch mode would be fast and lightly damped (≈ 1–3 Hz, ζ ≳ 0.06, computed). This is a design requirement, not a feature the wild-type animal has. The wild-type has no surface remotely large enough even to glide: it needs 35–53 cm² at 1.24 m s⁻¹, computed.
- **(b) Active.** Whether the zebrafish nervous system could close an attitude loop in air is **not established**, and the evidence leans against relying on it. The utricle, the only vestibular organ with measured function in larvae, loses its gravity reference in flight (physics). Every measured zebrafish vestibular or gaze-reflex frequency I found is ≤ 0.5 Hz, whereas the computed airframe needs 1–3 Hz and, for an unstable design, ≲ 40 ms loop delay. Adult canal bandwidth is unknown.
- **Refutation test.** In the sources I could read, no small non-exocoetid teleost has been shown to control attitude in air. Guppy, hatchetfish, butterflyfish and archer fish are each described as ballistic, or as setting orientation before leaving the water. **Scope of that negative:** 13 web searches (10 standard, 3 extended), mostly at abstract or search-summary read-level. Wiest 1995, Gutjahr et al. 2024 and the 2025 arowana paper were **not** read in full. The ribbon halfbeak (A7) is a partial exception: it is non-exocoetid but a beloniform close relative and much larger than 4 cm, and it is reported (search-summary only) to glide with a posture change. That is evidence of an aerial *configuration* change, not of closed-loop correction.

**Net: design for passive stability, and do not assume the fish can fly the airframe actively.** Within the current evidence, an engineered zebrafish could hold attitude in air only if the airframe is passively stable, and it could not be expected to correct attitude by vestibular feedback.

## 5. What this does NOT establish

- It does **not** show that zebrafish *cannot* sense or correct attitude in air. It shows that I found no measurement saying they can, and some physics and larval data saying the obvious route (utricle) will not work.
- It does **not** bound the adult semicircular-canal bandwidth. Canal mechanics depend on duct radius, which grows with age, and I have no adult radius or adult frequency response. Fish canals in *other* species may well respond above 1 Hz; I did not search for that and do not claim it either way.
- It does **not** use the project's actual designed surfaces. All of §3 runs on a reference geometry I made up and labelled. Static margin, wing area, tail volume and lift slopes could all differ.
- The pitch damping (ζ ≈ 0.06) is a **tail-only lower bound**. The real airframe would be better damped.
- Inertias treat the fish as a rod or cylinder with massless fins. Enlarged fins add inertia, and fin bending adds aeroelastic modes I have not modelled.
- Yaw and roll-angle (spiral) stability were **not computed**. I only computed roll *rate* damping.
- Low-Reynolds-number aerodynamics are approximated with constant lift slopes. That is not validated at Re ≈ 10³.
- Gusts are not analysed. At a 2 m s⁻¹ glide, a 1 m s⁻¹ gust is a 27° flow-angle change. This is my inference that small gliders are very gust-sensitive; I did not compute a gust response.
- Vision in air was not assessed. A fish eye's refraction is set for water, and I have no measured value for zebrafish acuity or OKR in air.
- The guppy jump (A1) is used only as a size-class anchor for speed and time aloft. It is not a zebrafish measurement.
- The negative literature search is shallow (§4 scope). Primary full texts for hatchetfish (Wiest 1995; Gutjahr et al. 2024), flying-fish stability (Park & Choi 2010) and the arowana study (2025) were not read.
- Nothing here addresses whether passive stability is *developmentally or genetically buildable*. That belongs to other subproblems.

## 6. What would change the answer

- **The designed planform from the wing and fin subproblems.** Its static margin, rear-surface volume (S_t·l_t), wing area and span would replace §3.1. A rear surface large enough to give a positive margin keeps answer (a) at "stable"; removing it makes the airframe divergent in 40–120 ms (computed).
- **Adult *D. rerio* angular-VOR or canal-afferent frequency response.** Measured gain ≳ 0.5 and phase lag ≲ 45° at 2–3 Hz in adults would make active pitch damping plausible and would upgrade (b). Gain falling off below 1 Hz would make (b) a firm negative.
- **Vestibulospinal and pectoral motor-loop latency in adults.** A measured sensor-to-fin latency ≲ 30–40 ms would satisfy the derived delay bound for an unstable design. ≳ 60 ms would rule it out at 2 m s⁻¹.
- **Full text of Wiest 1995, Gutjahr et al. 2024 or the 2025 arowana paper** showing in-air fin or trunk movements that change attitude, quantified as a rotation rate correlated with fin action. In a ~3 cm hatchetfish that would directly meet the refutation criterion and upgrade (b) to literature-supported.
- **A primary paper on ribbon-halfbeak gliding with closed-loop corrections** (posture changes that respond to perturbation). This is weaker evidence because the animal is larger and a close relative of flying fish.
- **A higher glide speed.** Raising exit speed shrinks the needed wing area (V⁻²) but makes the pitch mode faster (∝ V), which tightens the active-control requirement. This trade-off is a design decision, not a fact to look up.

### Reproduction (computation, §3)

```python
import math
rho,g=1.2,9.81; m,L=0.4e-3,0.04; W=m*g
Iy=m*L**2/12; Ix=m*0.003**2/2
for V in (1.0,2.0,3.0):
    q=0.5*rho*V**2; St,lt,at=1e-4,0.02,1.6; S,b,a=1e-3,0.06,2.5
    Ma=q*St*lt*at; w=math.sqrt(Ma/Iy); zeta=(q*St*lt**2*at/V)/(2*Iy*w)
    tau_roll=Ix/(q*S*a*b**2/(12*V))
    print(V, w/(2*math.pi), zeta, math.log(2)/w, tau_roll, Ma*0.2/Iy)
print(2*math.sqrt(2*0.0654/g))  # ballistic time aloft
```

```swarm-result
{"subproblem": "S18", "evidence": "derived",
  "answer": "An engineered 0.4 g zebrafish glider could hold attitude only passively (rear stabiliser, positive static margin; computed pitch mode ~1-3 Hz, roll-rate damping 1-4 ms); active vestibular attitude control is not supported: the utricle loses its gravity reference in flight, all measured zebrafish vestibular/gaze reflex data are larval and <=0.5 Hz, adult canal bandwidth is unknown, and no small non-exocoetid teleost was found controlling attitude in air (search scope: 13 web searches, mostly abstract-level).",
  "key_number": "computed pitch short-period ~1.9 Hz at 2 m/s (reference design) versus highest measured zebrafish vestibular-reflex test frequency 0.5 Hz",
  "blocked_on": "adult Danio angular-VOR / canal frequency response and sensorimotor latency; the project's designed planform (static margin); full text of Wiest 1995, Gutjahr et al. 2024 PNAS, Beck et al. 2004 (journals.physiology.org blocked by network policy)"}
```
