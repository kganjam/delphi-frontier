# Challenge 88: adversarial review of the S9-D "deepen" verdict (fin-ray E vs measured EI)

Claim under review (author: S9-D, branch `claude/deepen-s9-fin-ray-ixdx5u`, `S9-deepen.md`):

> "S9-D deepen verdict FALLS: bluegill fin-ray E=1.34 GPa is EI/I with I assumed; with zebrafish
> in-vivo caudal EI 1.5-4e-9 N m^2 and micro-CT hemitrich wall 11-16.5 um the implied modulus spans
> ~3 MPa to ~0.6-11 GPa (E ~ t^-3); carry measured EI, not bare E. (... per-ray EI ~0.8-2.5e-10
> assuming ~16-18 rays: 1.5e-9/18=0.83e-10, 4e-9/18=2.2e-10.)"
>
> Recorded: evidence level *derived*; value 2.5e-09 N m^2 (caudal fin EI midpoint).

Date: 2026-11-04. Read-level legend: full-text | abstract | listing | search-summary | could-not-access.
In this file, **calc** means I computed it. **Author** means S9-D or a cited paper states it.
**Inference** means it is my reasoning.

**Verdict: WEAKENED.** The main recommendation stands: carry the measured EI and not a bare E, and
the 1.34 GPa figure is not a usable organ-scale input. Four parts of the claim are wrong or
overstated as written. The most serious is the scaling law "E ~ t^-3", which is false for the
cross-section the micro-CT actually shows.

---

## 1. Independent arithmetic (calc)

I redid every step from the stated inputs. I wrote my own expressions and also ran the author's
script `S9-deepen_calc.py` as a cross-check. The two agree.

| Quantity | Inputs | My result (calc) | Claim says |
|---|---|---|---|
| Per-ray EI, low | 1.5e-9 / 18 | 8.33e-11 N m^2 | 0.83e-10 ✔ |
| Per-ray EI, high | 4e-9 / 16 | 2.50e-10 N m^2 | 2.5e-10 ✔ in range, but… |
| Per-ray EI, high, as the claim's own parenthetical writes it | 4e-9 / 18 | 2.22e-10 N m^2 | "2.2e-10" |
| Solid rod I, D = 150 µm | πD⁴/64 | 2.49e-17 m⁴ | 2.5e-17 ✔ |
| E, solid rod | EI_ray / I | 3.4–10.1 MPa | "~3 MPa" ✔ |
| Flat hemitrich pair I, w = 150, t = 15 µm | 2wt³/12 | 8.44e-20 m⁴ | ✔ |
| E, flat pair, t = 15 µm | | 0.99–2.96 GPa | ✔ |
| Envelope, flat pair: t = 16.5 µm with D = 200 µm, up to t = 11 µm with D = 100 µm | | 0.56–11.3 GPa | "~0.6–11 GPa" ✔ |
| Semicircular crescent pair I, R = 67.5 µm, t = 15 µm | thin-arc formula | 2.75e-18 m⁴ | ✔ (S9-D table) |
| Arithmetic midpoint of 1.5–4e-9 | | 2.75e-9 N m^2 | recorded 2.5e-9 |
| Geometric midpoint | √(1.5·4)·1e-9 | 2.45e-9 N m^2 | |

Arithmetic defects, both small:

- **(a)** The parenthetical divides both bounds by 18, giving 0.83–2.2e-10. The headline range,
  0.8–2.5e-10, needs the upper bound divided by 16. The claim's working does not produce its own
  stated range.
- **(b)** The recorded "midpoint" of 2.5e-9 is neither the arithmetic midpoint (2.75e-9) nor
  exactly the geometric one (2.45e-9). Also, Puri's EI is a **position-dependent profile**, not
  scatter around one value (§3). So a single midpoint is the wrong summary statistic.

## 2. Hidden assumption that carries "E ~ t^-3": it is false for crescents (calc)

E ∝ t⁻³ holds **only** in the uncoupled **flat-plate** model, where I = 2wt³/12. The claim attaches
it to the whole span, but the other models scale differently:

- **Solid rod** (the "~3 MPa" end): E does not depend on t at all.
- **Uncoupled crescents**: the wall's bending about the fin-plane axis is dominated by the arc
  depth term, I_own ≈ k·R³·t. So I scales roughly linearly in t. I recomputed by finite difference
  over t = 7.5 → 30 µm with R fixed at 67.5 µm (calc):
  - semicircular crescent: **E ∝ t^-1.07**
  - 60° half-angle crescent: **E ∝ t^-1.31**
  - Caveat: the thin-arc formula is approximate when t/R approaches 0.4.

This matters for three reasons:

1. **The cross-section that was measured is a crescent.** The micro-CT source S9-D relies on
   (PMC12956070, Fig. 7D, as S9-D read it at full-text) shows "( )" crescent hemirays. Taft 2011
   (abstract, as cited by S9-D) also describes them as crescents. S9-D itself calls the flat plate
   an **upper bound**, not the observed shape. So the t⁻³ law, and the GPa endpoint, belong to the
   geometry the evidence argues *against*.
2. **The controlling input is different.** For the observed crescent shape, the input that controls
   E is **crescent depth/curvature (≈ R³ and the arc angle)**, not wall thickness t. Recomputed
   from the author's own table (calc), at fixed t = 15 µm, changing the arc half-angle from 90° to
   30° moves E from 30–89 MPa to 1.6–4.7 GPa. That is ~50×. Changing t by 2× moves it only ~2×.
   - Author claim (S9-D §3): micro-CT at "≤ 2 µm" resolution is needed because "E ∝ t⁻³ needs t to
     within ~5%".
   - Inference: that resolution argument is therefore misdirected. What is needed is the full
     crescent outline, not t alone.
3. **The observed shape does not reproduce 1.34 GPa.** Under the physically favoured model
   (uncoupled, after Das et al. 2023, abstract, as cited) with the observed crescent shape, the
   implied E is **30–490 MPa** (calc, t = 15 µm, half-angles 90°–60°). So the observed geometry
   gives a value *below* 1.34 GPa. Only a near-flat crescent (≤ ~30°) or a flat plate reaches GPa.
   - Inference: this **strengthens** "1.34 GPa falls". It also means the claim's headline
     "~0.6–11 GPa" overstates where the physically supported model lands.

## 3. Proxy check: is "measured EI" the quantity that matters?

I read Puri et al. 2018 (*J. Exp. Biol.* 221:jeb171777, PMC5868929) at **full-text**, via the
Europe PMC XML, through an automated summariser. The quotes below are as it returned them.

- **Whole-fin EI.** "overall bending moments of 1.5×10⁻⁹–4×10⁻⁹ N m²" along the proximal–distal
  axis, "a peak … at ∼2–4 mm from the fixation". This **confirms** the input values.
- **But the EI is itself a model inversion.** It comes from a "mechanical line force load" applied
  with a 0.4 mm pin at six positions, on a fish whose peduncle is "held by two opposing foam pads".
  - Inference: it is a *structural* stiffness inferred through a cantilever model. It is not a
    direct observation of EI.
  - Its boundary condition (the foam-pad root compliance) is uncharacterised in the text I read.
  - The claim calls it "measured EI". That is acceptable shorthand, but the honest level is
    "measured force–deflection, EI derived by beam model".
- **Per-ray division is an extra assumption.** The text describes a single pin contact. It does
  **not** say the load spans all 16–18 rays.
  - Interray tissue was shown to be negligible to the overall stiffness (author claim, Puri). That
    supports treating the rays as parallel and independent.
  - It does **not** establish that the rays share the load equally. Caudal rays differ in length
    and diameter between lobes and centre.
  - So "per ray EI = EI/17" is a crude average. It should not be read as a per-ray measurement.

## 4. Evidence-level honesty

- **"with I assumed" is overstated.** S9-D's own text says: "**How Lauder et al. estimated I is
  unknown**" (Lauder 2011 at search-summary; full text could-not-access). The claim upgrades
  "unknown" to "assumed".
  - That 1.34 GPa is an E = EI/I figure is plausible: the 2024 *Interface Focus* paper, read by
    S9-D at full-text, calls a related "~1 GPa" a "homogenized flexural modulus".
  - But whether its I was assumed or measured from sections is **unknown**. It should be written
    that way.
- **The recorded value.** Recording the EI midpoint as *derived* is honest in level. As shown in §1
  and §3, though, the number is not the stated midpoint, and a midpoint is not a meaningful
  descriptor of a position profile.

## 5. Possible counter-evidence the author missed (unresolved, preserved, not averaged)

S9-D's inference that "1.34 GPa must rest on a hemitrich-only thin-wall I" depends on one bluegill
input: a ray EI of **3.8×10⁻⁶ N m²**. S9-D took it from Flammang et al. 2013 **as cited by Puri**,
and never accessed the primary.

- **Conflicting value.** A web search summary (read-level: **search-summary**) attributes to a 2013
  bluegill pectoral-ray study a flexural stiffness of **565×10⁻⁶ N m²**. That is ~150× larger.
- **Primary not checked.** I tried the Flammang 2013 PDF on sites.harvard.edu: **could-not-access**,
  because the host is blocked by this session's network policy.
- **Why it matters (calc).** If 565e-6 N m² is correct and applies to the same ray, a **solid-rod**
  I with D = 1–2 mm gives E = **0.72–11.5 GPa**. That would bring 1.34 GPa within reach *without*
  any thin-hemitrich I, and S9-D's "must" inference would fail.
- **Not resolved.** I cannot tell which figure is right. The two may refer to different
  positions, rays or units. Both are recorded here.

Negative-search scope: one standard web search for the Lauder 2011 I method, which found nothing
on the method. One fetch of the Flammang 2013 PDF, which was blocked. I did not search Scopus or
Web of Science, and did not try the IOP or Wiley full texts.

## 6. What survives

- All headline arithmetic reproduces, within the two small defects in §1.
- The core point stands: the same in-vivo EI maps to E values spanning >10³ across cross-section
  models. A bare E without its I is not a usable organ-scale input. Carrying the Puri EI profile
  (1.5–4e-9 N m², position-dependent) is the right move.
- The reinterpretation of Puri's ~8 MPa as a solid-rod ray modulus is consistent with my
  independent solid-rod calculation: 17 × 2.49e-17 = 4.2e-16 m⁴, inside the S5B range that S9-D
  read.

## 7. Corrections to carry forward

1. Replace "E ~ t^-3" with: "E ∝ t⁻³ only for flat uncoupled plates; ≈ t⁻¹ to t⁻¹·³ for the
   observed crescents (calc); t-independent for a solid rod". The controlling geometric unknown is
   the crescent outline and depth, not t alone.
2. Replace "I assumed" with "I unknown (method not accessed)".
3. Per-ray EI is 8.3e-11 to 2.5e-10 N m² (calc, /18 to /16), assuming equal load sharing, which
   Puri does not establish.
4. Do not record a single EI midpoint. Record the profile: 1.5–4e-9 N m², peak ~2–4 mm from the
   fixation (Puri, full-text). If one number is forced, the geometric mean is 2.45e-9 (calc).
5. Flag the open conflict in bluegill ray EI (3.8e-6 vs 565e-6 N m²) against S9-D's bluegill
   inference.

## Sources

- Puri S et al. 2018. *J. Exp. Biol.* 221:jeb171777. PMC5868929. **full-text** (Europe PMC XML,
  read through an automated summariser; supplementary figures not read by me).
- S9-D, `docs/research/fish/S9-deepen.md` and `S9-deepen_calc.py`, branch
  `claude/deepen-s9-fin-ray-ixdx5u`. **full-text** (the claim under review). Its readings of
  PMC12956070, Das 2023, Taft 2011 and Interface Focus 2024 are used here **as reported by S9-D**,
  not re-read by me.
- Flammang BE et al. 2013. *J. Morphol.* **could-not-access** (host blocked). The 565×10⁻⁶ N m²
  figure is **search-summary** only.
- Lauder GV et al. 2011. *Smart Mater. Struct.* 20:094014. **could-not-access**. Searched once;
  no method for I found.

```swarm-challenge
{"claim_id": 88, "outcome": "weakened", "reason": "The carry-EI-not-E conclusion survives and its arithmetic reproduces, but 'E ~ t^-3' holds only for the flat-plate bound, while the micro-CT-observed crescents give E ~ t^-1.1 to t^-1.3 and only 30-490 MPa (calc); 'I assumed' overstates an unknown method; the per-ray working (/18 for both bounds) does not give its own 2.5e-10 bound; the recorded 2.5e-9 midpoint is neither the arithmetic (2.75e-9) nor the geometric (2.45e-9) midpoint of a position-dependent profile; and an unresolved bluegill EI conflict (3.8e-6 vs 565e-6 N m^2, search-summary) threatens the author's bluegill inference.",
  "corrected_value": "1.5-4e-9 N m^2 whole caudal fin EI (position-dependent profile, peak ~2-4 mm from fixation; geometric mean 2.45e-9 if one number is forced); per ray 8.3e-11 to 2.5e-10 N m^2 (calc, equal-sharing assumed)",
  "depends_on": ["Puri et al. 2018 JEB 221:jeb171777 whole-fin EI 1.5-4e-9 N m^2, 16-18 rays, D 0.1-0.2 mm (full-text)", "PMC12956070 Fig 7 WT hemiray thickness ~11-16.5 um and crescent cross-section (as read by S9-D, not re-read)", "Das, Hannard & Barthelat 2023 uncoupled-hemitrich claim (abstract, as cited by S9-D)", "thin-arc second-moment formula with R = 67.5 um", "Flammang 2013 bluegill ray EI conflict 3.8e-6 (via Puri) vs 565e-6 N m^2 (search-summary)", "Lauder 2011 method for I unknown (could-not-access)"]}
```
