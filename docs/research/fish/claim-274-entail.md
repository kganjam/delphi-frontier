# Claim 274: what it requires at the organ and behaviour scales

**Source claim (organism scale, evidence: derived):**
> REOPENING CONDITION, falsifiable: an airborne zebrafish lobe beating at 1.4–2.2× its best
> measured burst tail speed (A_pp 12–19 mm at 52 Hz, or 72–117 Hz at burst amplitude), or
> surface-piercing lobe thrust at Re 1e4 measuring well above the 2-D foil law.

**Provenance note.** Claim 274 is not in this repository (searched `findings/`, `ledger/`,
`results/`, `frontier/`, `specs/` and the `work/frontier-foundation` branch for "274",
"zebrafish", "airborne", "foil law", "52 Hz", "tail beat"). This entailment works from the
claim text alone.

**What the claim says, as I read it (my inference, not the claim's own wording).** The claim
is a reopening condition on an earlier conclusion. That conclusion was probably that adult
zebrafish burst tail speed is capped by something inside the animal (muscle or motor rhythm),
not by the water's load. Taking the water away (an airborne lobe) is the test: if the ceiling
is internal, the unloaded lobe cannot go much faster. A surface-piercing lobe that beats the
2-D foil law would reopen a separate hydrodynamic arm.

**Numbers the claim implies (derived by me, arithmetic only):**
- Burst baseline amplitude: 12/1.4 = 8.57 mm and 19/2.2 = 8.64 mm, so baseline A_pp ≈ 8.6 mm
  at 52 Hz.
- 72/1.4 = 51.4 Hz and 117/2.2 = 53.2 Hz, which matches the 52 Hz baseline.
- Assuming sinusoidal motion, baseline peak lateral tail-tip speed is π·f·A_pp ≈ π·52·8.6 mm
  ≈ 1.40 m/s. The reopening band is therefore ≈ 1.97–3.09 m/s.
- At 72–117 Hz the beat period is 13.9–8.5 ms, so the half-period is 6.9–4.3 ms.

**Where the 52 Hz comes from (measured, and it matches).** Kyriakatos et al. 2011
(J Neurosci 31:8422, PMC6623330, *full-text*, first 100k characters read) recorded EMG from
freely swimming adult zebrafish, n = 8. They report: "the maximal frequency reached during
escape was 52 Hz", with escape bursts at about 30–52 Hz. Swimming bursts ranged "from ∼1 Hz to
slightly >20 Hz, but never exceeding 21 Hz". I infer that this is the "best measured burst" the
claim cites. The claim does not say so.

---

## Constraints

### C1 — organ, timescale: the muscle must turn on and off within a beat
**Requirement.** Fast axial muscle on each side must activate and relax well within one
tail-beat cycle. Otherwise the two sides co-contract and net work goes to zero. At 72–117 Hz,
the Ca²⁺ clearance time constant of fast fibres must be at most about one half-period,
4.3–6.9 ms. The upper bound, **≤ 6.9 ms**, is for 72 Hz, the easiest end of the band.

**Check.** Idoux et al. 2022, *Superfast excitation–contraction coupling in adult zebrafish
skeletal muscle fibers*, J Gen Physiol 154:e202213158 (PMC9247716, *full-text*, figures not
viewed):
- The decay time constant of a single Ca²⁺ transient in isolated adult fast fibres is
  **8.8 ± 3.4 ms (measured, 20–22 °C)**. The example traces in the Fig. 5D legend give 9 ms
  (zebrafish) and 20 ms (mouse).
- In stimulus trains, half fusion occurs at **53 ± 3 Hz** and 95 % fusion at 156 ± 9 Hz
  (measured, 20–22 °C). Single transients remain distinguishable at 100 Hz and are completely
  fused at 200 Hz.
- The authors cite maximal tail-beat frequencies of "up to 100 Hz and 50 Hz in larvae and adult".
- Dou et al. 2008 (as cited by Idoux; not read) reported twitch fusion near 190 Hz in larvae.

**Status: unsatisfied, and the measured evidence leans against the requirement.**
- At room temperature the measured mean, 8.8 ms, is 1.3× above the 6.9 ms bound. Half fusion,
  53 Hz, sits exactly at the burst baseline. That fits the reading that 52 Hz is close to a
  muscle-kinetics ceiling. This is my inference, not the authors'.
- I do **not** mark this unsatisfiable, for three reasons:
  1. The measurement is at 20–22 °C, but the fish live at 28.5 °C. With an assumed Q10 of 2–3,
     τ would be about 5.1–6.0 ms at 28.5 °C. That is *derived, not measured*, and it would put
     the 72 Hz end inside the bound.
  2. The SD (±3.4 ms) overlaps the bound.
  3. Ca²⁺ decay is not force relaxation. Force usually relaxes more slowly than Ca²⁺ decays
     (general muscle physiology, not checked for zebrafish here). That would make the
     requirement harder to meet, not easier.
- No measurement of Ca²⁺ decay or twitch relaxation in adult zebrafish fast fibres at 28 °C was
  found. A measured τ above 6.9 ms at 28 °C would make this constraint unsatisfiable at all
  frequencies in the band.

### C2 — behaviour, range: the motor rhythm must reach 72–117 Hz
**Requirement.** Whatever the load, the spinal motor output that drives the tail must produce
alternating bursts at **72–117 Hz** in an adult. The alternative route in the claim is
A_pp 12–19 mm at the 52 Hz that is already reached.

**Check.**
- Freely swimming adults, in water, reach a maximum escape EMG burst frequency of **52 Hz,
  measured** (Kyriakatos et al. 2011, *full-text*).
- The isolated adult brainstem–spinal cord preparation has no mechanical load at all. Its
  induced swimming frequency was **1–17 Hz, peak 6 Hz, measured at 20–22 °C** (same paper).
  Escape-like activity occurred but no frequency is given. This preparation is unloaded and
  slower, not faster, but it is swimming-mode, not escape, and it was run cold. So it does not
  test the escape ceiling.
- Larvae (2–21 dpf) maintain cyclic tail-beat frequencies up to about 100 Hz (Müller & van
  Leeuwen 2004, JEB 207:853, *abstract*). That is measured, but at a body length about 5–7×
  smaller. Frequency normally falls with size, so this is not evidence for adults. That last
  point is my inference.

**Status: unsatisfied.** In the sources I read, no adult zebrafish motor output above 52 Hz was
reported, loaded or unloaded. The 52 Hz value does not *contradict* an unloaded capacity above
it: it was measured under water load, and the reduced preparation is not an escape test. So this
is a gap, not a refutation. Search scope: four web searches (adult escape/burst tail-beat
frequency; adult maximum speed and tail-beat frequency; Kyriakatos fictive frequency; muscle
kinetics) plus the two full texts above. I found no study that measured an adult zebrafish tail
beating out of water. As far as I can tell, nobody has looked, rather than people looked and
found nothing.

### C3 — organ, spatial: the amplitude must fit the body
**Requirement.** For the amplitude route, the peak-to-peak excursion of the caudal tip must
reach **12–19 mm** on an adult whose body length is 18–30 mm. That range is the one Kyriakatos
et al. 2011 give for their animals. So A_pp/L must lie in **0.40–1.06** (derived), against a
baseline of 8.6 mm, which is 0.29–0.48 L (derived).

**Check.** I found no measured adult zebrafish burst A_pp or A_pp/L in the sources read. The
claim's own baseline of 8.6 mm has no traceable source in this repo. The upper end, about 1 L
peak-to-peak for an 18 mm fish, would need the tail tip to sweep roughly its own body length per
half-beat. That is geometrically possible for a C-bend but far outside cyclic swimming.
"Geometrically possible" is my inference; "far outside cyclic swimming" is general background I
did not check against a source in this session.

**Status: open.** Not checked against a measured adult amplitude. The obvious checks are
adult-zebrafish escape kinematics papers that report tail-tip excursion. My searches did not
surface one.

### C4 — behaviour, existence: there must be a behaviour that beats the tail out of water
**Requirement.** For the airborne test to be observable, rather than staged, adult zebrafish must
have a behaviour in which the caudal lobe is driven *cyclically* while out of water or piercing
the surface.

**Check.**
- Zebrafish stranded on land perform tail-flip jumps: a C-bend and then straightening against the
  substrate (Gibb, Ashley-Ross et al. 2011, J Exp Biol; read only at *search-summary* level via
  Wake Forest news and SICB abstract pages).
- A later study reports that "Danio showed a greater propensity to jump and traveled greater
  distances when stranded, relative to Gambusia" (*search-summary*).
- Both describe single propulsive flips against a substrate, not cyclic airborne beating, and
  give no tail-beat frequency.
- Zebrafish "are not known to voluntarily leave the water" (same news source, *search-summary*).
- Cyclic surface-piercing caudal-lobe beating is documented in flying fish (Exocoetidae)
  taxiing, not in zebrafish (see C5).

**Status: unsatisfied** for the cyclic, airborne form. The nearest behaviour that does exist is
terrestrial tail-flip jumping. Scope: one web search, plus the descriptions of terrestrial
jumping. No study of zebrafish surface skittering or taxiing was found. A preparation that forces
it (a restrained fish with the tail in air, plus a stimulus) would be needed, and none was found.

### C5 — organ, conservation: thrust above the 2-D law needs extra momentum
**Requirement.** Thrust from a surface-piercing lobe equals the rate at which it delivers
streamwise momentum to the water. For thrust "well above the 2-D foil law" at Re ≈ 1e4, the
added momentum (unsteady circulation, added mass, splash) must outweigh the losses a finite,
surface-piercing span suffers from the free surface and from ventilation.

**Check.**
- *Steady surface-piercing foils:* ventilation causes sudden lift loss. A Cambridge (JFM) review
  attributes to Wadlin (1958) a reduction of **up to 70 %** in the measured lift coefficient.
  This is *search-summary* only: I did not read the review's text or Wadlin. Harwood et al. 2016
  give ventilation stability maps; read at *listing/abstract* level, and their lift values were
  not extracted.
- *Flying-fish taxiing, the biological analogue:* the sources disagree, and I keep the
  disagreement.
  - A bioRxiv preprint (10.1101/765560) states 50–70 strokes s⁻¹ for the submerged lower lobe,
    and separately calculates about 41.7 s⁻¹. Read at *search-summary* level only; a full-text
    fetch returned HTTP 429.
  - An APS March Meeting 2024 abstract reports a measured **13.5 Hz** surface tail beat, and
    about 2 N as the minimum force to keep a 200 g fish above the surface (*search-summary*).
  - Neither compares thrust with a 2-D foil prediction.
- *Flapping (unsteady) surface-piercing foils at Re ~1e4:* no thrust measurement was found.

**Status: unsatisfied.** No measured mechanism or value meets the requirement. The only
quantitative evidence on surface-piercing foils is steady-state, and it points the other way:
measured lift is below 2-D because of ventilation. That evidence is *not* a contradiction of the
claim. It is steady, not flapping. It is at higher Re than 1e4 (my inference from hydrofoil test
practice, not checked). And I read it only at search-summary level. So this is not
unsatisfiable. Scope: one web search on surface-piercing ventilation and one on flying-fish
taxiing. I found no flapping surface-piercing foil experiment at Re 1e4.

---

## Summary

| # | Scale | Kind | Status | Bottom line |
|---|---|---|---|---|
| C1 | organ | timescale | unsatisfied (leans against) | measured Ca²⁺ decay 8.8 ms at 20–22 °C vs ≤ 6.9 ms needed; half fusion at 53 Hz ≈ the 52 Hz baseline; no 28 °C value |
| C2 | behaviour | range | unsatisfied | the measured adult maximum is 52 Hz (escape EMG); nothing above it, loaded or unloaded, has been reported; probably never tested out of water |
| C3 | organ | spatial | open | no measured adult burst A_pp found; needs 0.40–1.06 body lengths |
| C4 | behaviour | existence | unsatisfied | only terrestrial tail-flip jumps are known; no cyclic airborne beating |
| C5 | organ | conservation | unsatisfied | steady surface-piercing foils measure *below* 2-D (ventilation, up to 70 %, search-summary); no flapping data at Re 1e4 |

Nothing here is **unsatisfiable**. The closest is C1. If the Ca²⁺ decay or twitch relaxation of
adult fast fibres is measured at 28 °C and comes out above about 6.9 ms, the frequency route of
the reopening condition (72–117 Hz) is refuted from below, with no simulation needed. The
amplitude route (12–19 mm at 52 Hz) would remain open.

## Sources and read-levels
- Kyriakatos A. et al. 2011, *Initiation of locomotion in adult zebrafish*, J Neurosci. PMC6623330. **full-text** (first 100k chars).
- Idoux R. et al. 2022, *Superfast excitation–contraction coupling in adult zebrafish skeletal muscle fibers*, J Gen Physiol 154:e202213158. PMC9247716. **full-text** (figures not viewed; publisher host rupress.org was unreachable from this session).
- Müller U.K. & van Leeuwen J.L. 2004, *Swimming of larval zebrafish: ontogeny of body waves…*, J Exp Biol 207:853. **abstract**.
- Ravel G. et al. 2025, iScience 28:112056, PMC11930232. **full-text** (partial). Larval, modelled power; not used for any constraint because it gives no W/kg figure and concerns 5 dpf larvae.
- Gibb A.C., Ashley-Ross M.A. et al. 2011 (terrestrial jumping, Danio vs Gambusia). **search-summary**.
- Wadlin 1958 via a JFM review; Harwood et al. 2016. **search-summary / listing**.
- Flying-fish taxiing preprint, bioRxiv 10.1101/765560. **search-summary** (fetch failed, HTTP 429).
- APS March Meeting 2024 abstract, *Flying fish taxiing on the water's surface*. **search-summary**.

```swarm-entail
{"source_claim": 274, "source_scale": "organism",
  "constraints": [
    {"target_scale": "organ", "kind": "timescale",
      "statement": "Fast axial muscle on each side must activate and clear Ca2+ within about one half-period of the beat, so the two sides do not co-contract at 72-117 Hz",
      "quantity": "fast-fibre Ca2+ transient decay time constant (upper bound = half-period at 72 Hz)", "lo": null, "hi": 6.9, "units": "ms",
      "status": "unsatisfied",
      "satisfied_by": "Measured adult zebrafish fast-fibre Ca2+ decay tau = 8.8 +/- 3.4 ms at 20-22 C, above the bound; half fusion at 53 +/- 3 Hz. No 28 C measurement found; a Q10 correction (derived, not measured) would give about 5-6 ms",
      "satisfied_evidence": "measured",
      "note": "Idoux et al. 2022 J Gen Physiol 154:e202213158 (PMC9247716, full-text, figures not viewed). Not marked unsatisfiable: temperature mismatch (20-22 vs 28.5 C) and SD overlaps the bound. Becomes unsatisfiable if tau at 28 C > 6.9 ms"},
    {"target_scale": "behaviour", "kind": "range",
      "statement": "The adult spinal motor rhythm driving the tail must produce alternating bursts in the reopening band",
      "quantity": "motor burst / tail-beat frequency", "lo": 72, "hi": 117, "units": "Hz",
      "status": "unsatisfied",
      "satisfied_by": "Measured adult maximum is 52 Hz (escape EMG, freely swimming, in water); unloaded isolated preparation gives 1-17 Hz (swimming mode, 20-22 C). No adult value above 52 Hz found under any load; no out-of-water adult measurement found",
      "satisfied_evidence": "measured",
      "note": "Kyriakatos et al. 2011 J Neurosci (PMC6623330, full-text). Larvae reach about 100 Hz (Muller & van Leeuwen 2004, abstract) but at 5-7x smaller size. Negative scope: 4 web searches plus 2 full texts; the out-of-water test appears never to have been done (nobody looked), not looked-and-found-nothing"},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "Caudal tip peak-to-peak excursion must reach the required amplitude relative to body length (body length 18-30 mm)",
      "quantity": "A_pp / body length", "lo": 0.40, "hi": 1.06, "units": "body lengths",
      "status": "open",
      "satisfied_by": "Not checked: no measured adult zebrafish burst A_pp found; the claim's 8.6 mm baseline (derived from its ratios) has no traceable source in this repo",
      "satisfied_evidence": "unknown",
      "note": "Bounds derived from 12-19 mm over the 18-30 mm body lengths given in Kyriakatos et al. 2011. Needs an adult escape-kinematics paper reporting tail-tip excursion"},
    {"target_scale": "behaviour", "kind": "existence",
      "statement": "A behaviour must exist in which the adult caudal lobe is driven cyclically while out of water or piercing the surface",
      "quantity": null, "lo": null, "hi": null, "units": null,
      "status": "unsatisfied",
      "satisfied_by": "Only terrestrial tail-flip jumping when stranded is documented (a single C-bend against the substrate, not cyclic, no frequency reported); zebrafish are not known to leave water voluntarily",
      "satisfied_evidence": "literature",
      "note": "Gibb, Ashley-Ross et al. 2011 and a later Danio-vs-Gambusia stranding study, search-summary only. Negative scope: one web search; no zebrafish skittering or taxiing study found. Cyclic surface-piercing caudal beating is documented only in flying fish"},
    {"target_scale": "organ", "kind": "conservation",
      "statement": "Thrust above the 2-D foil law from a surface-piercing lobe requires extra streamwise momentum flux (unsteady circulation, added mass) exceeding free-surface and ventilation losses of a finite piercing span",
      "quantity": "surface-piercing lobe thrust / 2-D foil prediction at Re ~1e4", "lo": 1, "hi": null, "units": "dimensionless ratio",
      "status": "unsatisfied",
      "satisfied_by": "No measured mechanism found. Steady surface-piercing foils measure below 2-D (ventilation lift loss up to 70 %, Wadlin 1958 as cited in a JFM review). No flapping surface-piercing foil thrust data at Re 1e4 found",
      "satisfied_evidence": "literature",
      "note": "Wadlin 1958 / Harwood et al. 2016: search-summary or listing only. Flying-fish taxiing sources disagree (preprint 50-70 strokes/s vs APS 2024 abstract 13.5 Hz measured); neither compares with 2-D foil law. Not unsatisfiable: steady not flapping, Re not matched, not read in full. Negative scope: 2 web searches"}
  ]}
```
