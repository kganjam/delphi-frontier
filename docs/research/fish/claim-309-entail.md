# Claim 309: what it requires at the cell and organ scales

**Source claim (tissue scale, evidence: measured).** Fast myotomal fibres of *Scorpaena notata*
(small red scorpionfish, family Scorpaenidae) deliver a mean muscle-mass-specific power of
142.7 W/kg at 20 °C. This was measured by work loop at in vivo strain and shortening duration.
Source: Wakeling J.M. & Johnston I.A. (1998), "Muscle power output limits fast-start performance
in fish", *J. Exp. Biol.* 201(10):1505–1526, doi:10.1242/jeb.201.10.1505.

**Subject of every constraint below:** *Scorpaena notata* fast (white) myotomal muscle at 20 °C.
Zebrafish is **not** the subject. The claim limits itself to what teleost fast muscle has been
*measured* to deliver, and so do these constraints. When a number below comes from a different
animal, that animal is named in the same sentence.

## How much was read (affects every verdict)

This session's network policy blocked the full text. `journals.biologists.com`/`cob.silverchair.com`
and `acnpsearch.tweb-dev.unibo.it` did not resolve, so every literature read below is at
**search-summary** level unless marked otherwise. I could not read the paper's tables, which
should hold the *S. notata* shortening durations, strains, twitch times and fast-muscle mass
fractions. Because of that, several constraints remain `open` even though the paper probably
contains the number that would close them. Not being able to read it is a different situation
from finding that nobody has measured it, and each verdict below says which applies.

| Source | Animal | Read-level | Used for |
|---|---|---|---|
| Wakeling & Johnston 1998, JEB 201:1505 | *S. notata* and five other teleosts (incl. *Serranus cabrilla*) | search-summary (abstract fragments) | 142.7 W/kg; whether predicted and measured power match; gearing ratio falls toward the tail |
| Secondary citation of Wakeling & Johnston 1998 (citing paper not identified) | *S. notata* | search-summary; **attribution unverified** | V_max 13.2 L/s, isometric stress ~240 kN/m² (rostral fast muscle, 20 °C) |
| Askew & Marsh 2002, JEB 205:2153 (comparison table) | lists *S. notata* | search-summary; **not re-confirmed on a second search** | work-loop mean stress 99 kN/m², net power 143 W/kg |
| Wakeling & Johnston 1999, JEB 202:521 | *Cyprinus carpio* (common carp) | search-summary (abstract) | white-muscle strain predicted from spine curvature and gearing ratio |
| Isolated dogfish white-fibre ³¹P-NMR study (1997; authors not retrieved) | *Scyliorhinus canicula* (elasmobranch, not a teleost) | search-summary | ~half of PCr consumed by a single tetanus |
| Bullrout fast-fibre work-loop study (citation not retrieved) | *Myoxocephalus scorpius* | search-summary | 25–35 W/kg at 5–7 Hz sinusoidal cycling |

---

## Constraints

### C1 — cell, `range`: the fibres' intrinsic maximum power must be at least the measured mean

**Requirement.** The mean power over a work loop cannot exceed the peak isotonic power on the
fibre's force–velocity curve. Single fast fibres or fibre bundles of *S. notata* at 20 °C must
therefore reach **peak isotonic power ≥ 142.7 W/kg**.

**Derived bound.** This is a calculation, not an observation. It assumes muscle density
1060 kg/m³ and a peak-power ratio W_max/(P0·V_max) of 0.08–0.12, typical of Hill-curve
curvature in vertebrate fast muscle. On those assumptions it needs
P0·V_max ≥ 142.7 × 1060 / 0.12 ≈ 1.26 × 10⁶ to 142.7 × 1060 / 0.08 ≈ 1.89 × 10⁶ N m⁻² L s⁻¹.

**Check.** A search summary credits Wakeling & Johnston (1998) with V_max = 13.2 L/s and
isometric stress ≈ 240 kN/m² for *S. notata* rostral fast muscle at 20 °C. If those values are
correct, P0·V_max ≈ 3.2 × 10⁶ N m⁻² L s⁻¹. That would meet the bound by about 1.7–2.5×, and the
implied peak isotonic power is ≈ 250–360 W/kg. This last figure is my calculation, not a
reported number. I could not confirm the attribution. A direct search for "Scorpaena notata" with
"13.2" returned nothing on muscle. I also cannot tell whether the force and velocity came from
the same preparation.

**Disagreement to preserve.** A second search summary (Askew & Marsh 2002 table) lists a
*work-loop mean* stress of 99 kN/m² for *S. notata*. It does not contradict 240 kN/m². My
inference is that 240 is maximum isometric stress and 99 is the cycle-averaged stress during the
work loop. The authors do not say this; I am inferring it.

**Status: `open`.** A candidate satisfying value exists, but I read it only at search-summary
level and could not verify its attribution. Marking C1 `satisfied` on that basis would be
marking it satisfied because it looks plausible.

### C2 — cell, `timescale`: activation and relaxation must fit inside the in vivo shortening phase

**Requirement.** To deliver net positive work at the in vivo shortening duration, the fibre has
to activate and largely relax within the shortening phase. Otherwise force persists into
re-lengthening and produces negative work. The fibre's twitch time to half-relaxation at 20 °C
therefore has to be **shorter than the in vivo shortening duration**, within a factor of about 1.
The ratio t_half-relax / t_shortening must be ≲ 1.

**Check.** Neither number could be retrieved for *S. notata*. The paper's shortening durations
are in its tables, which I could not reach. Three searches for *S. notata* fast-fibre twitch
kinetics found no value. The only relaxation time that came up (~135 ms) was for Atlantic cod
(*Gadus morhua*). That is a different species and a different temperature regime, so it is
**not** used.

**Status: `open`.** Scope of the negative: three web searches (standard and extended) on
*S. notata* twitch, half-relaxation and work-loop terms. The finding is "could not access",
not "measured and absent". The 1998 paper probably reports twitch times, because work-loop
studies usually do, but I have not seen them. A small piece of indirect support: the authors
report that the work loops reproduced in vivo power, which implies that relaxation was fast
enough in their preparation. That support is borrowed from the claim itself, so it is not
independent.

### C3 — cell, `energetic`: stored high-energy phosphate must pay for a fast-start

**Requirement.** A fast-start finishes in tens of milliseconds. That is too fast for oxidative
or glycolytic flux to set the supply rate, so the ATP + phosphocreatine already in the fibre must
cover the chemical cost of the work.

**Derived bound.** This is a calculation with assumed inputs. Mechanical work is 142.7 W/kg ×
t_shortening. I assume t_shortening ≤ 0.1 s (a placeholder, because the paper's value was not
read), which gives ≤ 14.3 J/kg. At an efficiency of 0.2–0.5 the chemical cost is 29–71 J/kg.
At ~50 kJ/mol free energy of ATP hydrolysis, that is **≈ 0.6–1.4 µmol high-energy phosphate per
g muscle per fast-start**.

**Check.** I found no *S. notata* value for the ATP + PCr pool. The closest measurement is in
isolated white fibres of the dogfish *Scyliorhinus canicula* (an elasmobranch, not a teleost).
There a single tetanus consumed about half the PCr pool (³¹P-NMR, search-summary, pool size not
retrieved). Teleost white-muscle ATP and PCr concentrations of several µmol/g are widely reported
for trout and tuna, but I did not retrieve an actual figure this session and am not quoting one.

**Status: `open`.** The requirement is probably met with a wide margin, but I have no measured
*S. notata* number. Scope of the negative: one search on PCr in fish white muscle during escape
or fast-start; no *S. notata* data came up.

### C4 — organ, `conservation`: muscle power must close the whole-body energy budget

**Requirement.** Over the fast-start, the whole axial fast musculature must supply power equal
to the rate of increase of body and added-mass kinetic energy plus hydrodynamic dissipation.
Whole-body power is fast-muscle mass fraction × 142.7 W/kg. The ratio of hydrodynamic power
required to muscle power available must be within about 1. A ratio well above 1 would mean the
measured power cannot drive the observed start. A ratio well below 1 would mean the tissue
number overstates what the organ uses.

**Check.** The abstract says that power outputs predicted from swimming sequences matched the
work-loop measurements at all temperatures tested (author's claim, search-summary). Note what
kind of evidence this is. The "predicted" power is a model calculation from filmed kinematics.
It is not a direct measurement of hydrodynamic power. It is also part of the source claim, so it
is not an independent check from the organ scale. I could not read the mass fractions, the
added-mass model or the residuals.

**Status: `open`.** The only evidence is the source paper's own internal comparison, read at
search-summary level. Accepting it as `satisfied` would let the claim certify itself.
Independent closure would need a second group's kinematic or flow-field (PIV) energy budget for
*S. notata* or another scorpaenid. None was found. Scope: two searches on fast-start kinematics
for the six-species set; no independent *S. notata* energy budget turned up.

### C5 — organ, `spatial`: work-loop strain must be what body bending produces

**Requirement.** The strain imposed in the work loop has to equal the strain the myotome
actually undergoes. That strain is set by spine curvature × lateral distance from the backbone,
divided by the fibre gearing ratio from the helical fibre geometry. The ratio of work-loop strain
to curvature-derived in vivo fibre strain must lie within **[0.67, 1.5]**. This tolerance is my
choice, not a published one.

**Check.** The mechanism has been shown, but **in a different animal**. Sonomicrometry in common
carp (*Cyprinus carpio*; Wakeling & Johnston 1999, JEB 202:521; abstract, search-summary) shows
that white-muscle strain can be predicted from spine curvature if the red-to-white gearing ratio
is known. Whole-myotome strain varies with depth less than simple bending theory predicts. For
*S. notata*, the 1998 abstract says that gearing ratios must fall toward the tail, with geometry
changing to keep fibre strains similar along the body. I read that as the authors deriving
*S. notata* strains from curvature through a gearing model, but I have not seen the method. I
found no direct *S. notata* strain measurement (sonomicrometry or similar).

**Status: `open`.** The carp result supports the method, not the *S. notata* numbers. Scope:
one search on Wakeling & Johnston strain, curvature and fibre-angle work. The carp papers came
up; nothing on *S. notata* fibre angles or direct strain did.

---

## Cross-species numbers that are *not* refutations

- **Bullrout (*Myoxocephalus scorpius*) fast fibres: 25–35 W/kg at 5–7 Hz sinusoidal cycling**
  (search-summary). This is about 4–6× below 142.7 W/kg. The animal is different (Cottidae,
  close to Scorpaenidae but not the same species), the strain protocol is different (sinusoidal
  steady cycling, not the single asymmetric fast-start cycle at in vivo strain), and the
  temperature is probably different. It is **not** evidence against claim 309. The comparison is
  still informative: it shows that work-loop power depends strongly on protocol, so the 142.7
  figure should not be carried over to steady swimming. That is my inference.
- **Zebrafish:** nothing here concerns *Danio rerio*. No constraint in this file can refute or
  support a zebrafish claim.

## Summary

| # | Scale | Kind | Status | Why |
|---|---|---|---|---|
| C1 | cell | range | open | candidate *S. notata* V_max/P0 meets bound ~2×, but attribution unverified (search-summary) |
| C2 | cell | timescale | open | twitch and shortening times are in the paper's tables, which I could not access |
| C3 | cell | energetic | open | demand derived (~0.6–1.4 µmol/g); no *S. notata* pool size retrieved |
| C4 | organ | conservation | open | only check is the source paper's own model comparison (not independent) |
| C5 | organ | spatial | open | method shown in carp (*C. carpio*), not measured in *S. notata* |

No constraint is `unsatisfiable`. No measured *S. notata* number that contradicts the claim was
found. No constraint is `satisfied`, because none could be tied to a verified, same-species
measurement at the read level reached. The cheapest next step is to read the full text of
Wakeling & Johnston 1998 (its tables). That would probably close C1 and C2 and show what C4
rests on.

```swarm-entail
{"source_claim": 309, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "cell", "kind": "range",
      "statement": "Intrinsic peak isotonic power of the fast fibres (from their force-velocity relation) must be at least the measured work-loop mean power, since a cycle average cannot exceed the instantaneous maximum.",
      "quantity": "peak isotonic power of S. notata fast fibres at 20 C", "lo": 142.7, "hi": null, "units": "W/kg",
      "status": "open",
      "satisfied_by": "Candidate only: search-summary attributes to Wakeling & Johnston 1998 V_max = 13.2 L/s and isometric stress ~240 kN/m2 for S. notata rostral fast muscle at 20 C; P0*Vmax ~3.2e6 N m-2 L s-1 vs derived requirement 1.26e6-1.89e6 (calculation assuming density 1060 kg/m3 and power ratio 0.08-0.12). Attribution not verified; direct search for these numbers failed.",
      "satisfied_evidence": "unknown",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505, doi:10.1242/jeb.201.10.1505 (search-summary; full text blocked by network policy). Askew & Marsh 2002 JEB 205:2153 table lists S. notata work-loop mean stress 99 kN/m2 (search-summary, not re-confirmed); interpreted by me, not the authors, as cycle-mean rather than isometric stress. Animal on both sides: S. notata."},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "Fibre activation and relaxation must complete within the in vivo shortening phase, so that force does not persist into re-lengthening; twitch time to half-relaxation must not exceed the in vivo shortening duration.",
      "quantity": "t_half-relaxation / t_shortening (in vivo), S. notata fast fibres, 20 C", "lo": null, "hi": 1.0, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Not found. Three web searches (standard + extended) for S. notata fast-fibre twitch/half-relaxation times returned none; the only relaxation time found (~135 ms) was Atlantic cod (Gadus morhua) and was not used. The paper's tables likely contain the values but could not be accessed.",
      "satisfied_evidence": "unknown",
      "note": "Scope of negative: could-not-access, not measured-and-absent. Indirect support (work loops reproduced in vivo power) comes from the source claim itself and is not independent."},
    {"target_scale": "cell", "kind": "energetic",
      "statement": "The fibre's stored high-energy phosphate pool (ATP + phosphagen) must cover the chemical cost of one fast-start, since the event is too brief for oxidative or glycolytic flux to supply it.",
      "quantity": "high-energy phosphate consumed per fast-start", "lo": 0.6, "hi": 1.4, "units": "umol/g muscle",
      "status": "open",
      "satisfied_by": "Demand is a derived calculation (142.7 W/kg x assumed <=0.1 s shortening, efficiency 0.2-0.5, ~50 kJ/mol). No S. notata ATP/PCr pool size retrieved. Nearest measurement: isolated white fibres of dogfish Scyliorhinus canicula (elasmobranch) use ~half of PCr in one tetanus (31P-NMR, pool size not retrieved).",
      "satisfied_evidence": "unknown",
      "note": "Dogfish 31P-NMR study, 1997, search-summary, authors not retrieved; different animal (elasmobranch) so not used to satisfy. Scope of negative: one search on PCr in fish white muscle in escape/fast-start; no S. notata data."},
    {"target_scale": "organ", "kind": "conservation",
      "statement": "Power from the whole axial fast musculature (fast-muscle mass fraction x mass-specific power) must balance the rate of increase of body plus added-mass kinetic energy and hydrodynamic dissipation during the fast-start.",
      "quantity": "hydrodynamic power required / muscle power available", "lo": null, "hi": null, "units": "dimensionless (must be ~1)",
      "status": "open",
      "satisfied_by": "Only the source paper's own internal comparison: authors report power predicted from swimming sequences (a model calculation from filmed kinematics, not a measurement) matched work-loop power at all temperatures. Not independent of claim 309. No independent S. notata (or scorpaenid) kinematic/PIV energy budget found.",
      "satisfied_evidence": "unknown",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505 abstract (search-summary). Mass fractions, added-mass model and residuals not read. Scope: two searches on six-species fast-start kinematics."},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "The strain imposed in the work loop must match the fibre strain produced by whole-body bending (spine curvature x lateral distance / fibre gearing ratio) within a factor of 1.5.",
      "quantity": "work-loop strain / curvature-derived in vivo fibre strain", "lo": 0.67, "hi": 1.5, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Mechanism demonstrated in a different animal: sonomicrometry in common carp (Cyprinus carpio) shows white-muscle strain is predictable from spine curvature given the red:white gearing ratio. For S. notata the 1998 abstract states gearing ratios fall toward the tail to keep strains similar; no direct S. notata strain measurement found.",
      "satisfied_evidence": "unknown",
      "note": "Wakeling & Johnston 1999 J Exp Biol 202:521 (C. carpio; abstract, search-summary); Wakeling & Johnston 1998 (S. notata; search-summary). Tolerance band [0.67, 1.5] is my choice, not published. Scope: one search on strain/curvature/fibre-angle work; nothing on S. notata fibre angles or direct strain."}
  ]}
```
