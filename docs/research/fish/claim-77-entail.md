# Claim 77: what it requires at the cell and organ scales

**Source claim (tissue scale, evidence: derived).** S10-D verdict strengthens. The measured teleost
pectoral-muscle fraction is about 1.4% of body mass for both fins (*Abudefduf saxatilis*, 0.69% per
fin, Mansuit & Herrel 2021 Table 1). The computed threshold is 7.5–20%. Hover demand is
730–1950 W/kg, which is 5–15× above measured warm zebrafish fast muscle.

**Adjacent scales:** cell (muscle fibre, contractile power) and organ (pectoral fin with its
muscles; whole-animal momentum balance).

---

## 0. Reconstructing the claim's arithmetic (my calculation, not a measurement)

The claim's numbers fit together exactly if the muscle-power denominator is the larval zebrafish
value in Mead et al. 2020: 134.4 W/kg net power at 80 Hz, at 28 °C (see C1). This is my inference
from the arithmetic. The claim does not name its source.

| quantity | value | how |
|---|---|---|
| demand / available | 730/134.4 = **5.4×**, 1950/134.4 = **14.5×** | matches the claim's "5–15×" |
| hover power per kg **body** | 0.0138 × (730–1950) = **10.1–26.9 W/kg body** | demand is per kg pectoral muscle at a 1.38% fraction |
| required muscle fraction at 134.4 W/kg | 1.38% × (730–1950)/134.4 = **7.5–20.0%** | matches the claim's threshold exactly |
| required fraction if muscle reached ~400 W/kg (quail-level, see C1) | **2.5–6.7%** | still above 1.38% |

Two things follow:
1. Inside the claim, the threshold and the 5–15× ratio are one fact stated twice, not two
   independent pieces of evidence.
2. Even if the subject's muscle matched the best cycle-averaged vertebrate value reported, the
   required fraction (≥2.5%) would still be above the one measured fraction (1.38%). This is
   derived, not observed.

**What "hover" means.** I take it to mean aerial hovering, with the whole body weight supported
by the pectoral fins. In water, buoyancy makes hovering nearly free, and a demand of 730 W/kg
would make no sense. This is my reading. The claim text does not say it.

**Repo context.** I grepped this repository for `Mansuit`, `S10-D`, `S32`, `exocoet`, `flying fish`
and `zebrafish fast muscle`. Nothing matched. The S10 model, its body mass, fin area and subject
species are not in this repository, so I could not read its inputs. That is why C4 stays `open`.

---

## 1. Constraints

### C1 — cell — energetic: the subject's fast muscle cannot supply ≥730 W/kg cycle-averaged

**Requirement.** For the claim to hold, the cycle-averaged, mass-specific mechanical power of the
fin's fast muscle must be **below 730 W/kg muscle**. That is the low end of the hover demand. If
the muscle could deliver it, the claimed shortfall would vanish at the measured fraction.

**Check: satisfied for larval zebrafish, `open` for adult zebrafish.**
- **Zebrafish, 5 dpf larvae, 28 °C.** Net power in work loops was **134.4 ± 19.9 W/kg at 80 Hz**
  and **122.9 ± 11.1 W/kg at 100 Hz**. The preparation was intact ~1 mm tail sections whose cross
  section is 61% fast fibres (Mead, Kennedy, Palmer, Ebert & Warshaw 2020, *Biophys. J.*
  119:806–820, doi:10.1016/j.bpj.2020.06.036; read-level: full-text via PMC7451861). This is a
  measurement, but of **axial myotomal** muscle, **not pectoral fin muscle**. That gap is a
  tissue-type mismatch inside the same species. I treat axial fast muscle as a proxy for fin
  fast muscle, and that is an assumption. One source reports that late larval pectoral fin
  musculature is all fast fibres (search-summary only, from a ZFIN/Thorsen & Hale 2005 hit; not
  verified).
- **Other teleosts, cross-species, context only.** Fast myotomal fibres of *Scorpaena notata*
  averaged ~142.7 W/kg at 20 °C (Wakeling & Johnston 1998, *J. Exp. Biol.* 201:1505–1526;
  read-level: search-summary). The species is wrong for a verdict, but the value lies in the same
  range.
- **Vertebrate ceiling, cross-taxon, context only.** The blue-breasted quail pectoralis during
  take-off required on average ~390 W/kg, up to 530 W/kg in one bird (Askew, Marsh & Ellington
  2001, *J. Exp. Biol.* 204:3601–3619; read-level: search-summary). That value is derived from
  kinematics and aerodynamics, not measured directly. A later review (Askew 2023,
  *J. Muscle Res. Cell Motil.*; read-level: search-summary, full text could-not-access because the
  host is blocked) is reported to give ~400 W/kg cycle-averaged and ~1200 W/kg instantaneous as the
  highest skeletal-muscle values. Even the bird figures are below 730 W/kg.
- **Adult zebrafish.** I found no work-loop power measurement. Searched: web search for
  "adult zebrafish fast muscle work loop power output W/kg". The hits were larval or other-species.
  This scope is narrow (one search engine, English). Read as "not found", not "shown absent".

**Animals on both sides.** The claim's denominator is larval zebrafish. The check is larval
zebrafish. They match for larvae. If the claim's subject is an **adult** zebrafish, the life
stage differs, and the 134 W/kg figure becomes a proxy.

### C2 — cell — timescale: beating faster must not close the gap

**Requirement.** A fish could try to meet a power deficit by raising the fin-beat frequency. For
the claim to hold, power per unit muscle mass must not keep rising with cycle frequency past the
muscle's optimum. Above the optimum, P(f) must stay at or below P_max. Quantity: the ratio
P(100 Hz)/P(80 Hz) in larval zebrafish must be ≤ 1.

**Check: satisfied (larval zebrafish, 28 °C).** Mead et al. 2020 measured 134.4 W/kg at 80 Hz and
122.9 W/kg at 100 Hz. The ratio is **0.91**: power falls as the cycle frequency rises past 80 Hz
(full-text via PMC7451861). Two caveats:
1. The difference is within one SD of each value. The decline is the reported mean trend, not a
   test I ran.
2. The frequencies come from axial swimming. Whether pectoral fin muscle shares the same optimum
   is unknown.

### C3 — organ — range: the hovering subject's total pectoral muscle fraction is below 7.5% of body mass

**Requirement.** Both pectoral fins' muscle mass, as a fraction of body mass, must lie **below
7.5%**, the low end of the computed threshold. Otherwise the subject would already have enough
muscle.

**Check: `open`, because the only measured value is from a different animal.**
- **Measured value.** *Abudefduf saxatilis* (sergeant major damselfish, Pomacentridae, a
  labriform pectoral-fin swimmer): pectoral muscle 0.13 + 0.23 + 0.15 + 0.18 = **0.69% of body
  mass** for one pectoral appendage (Mansuit & Herrel 2021, *Front. Ecol. Evol.* 9:702576, Table 1;
  read-level: full-text, PDF extracted and the row read directly). The paper says actinopterygian
  data came from Thorsen & Westneat 2005, Dickson & Pierce 2019 and Crawford et al. 2020. Both fins
  together give 1.38%, which is below 7.5% by a factor of 5.4.
- **The general statement rests on one species.** Mansuit & Herrel write that "in actinopterygians
  and Latimeria, each appendage has a mass relative to the body mass inferior to 1%". But in their
  Table 1, the only actinopterygian normalised to body mass is *Abudefduf saxatilis*. The other
  fish rows (*Cryptopsaras*, *Antennarius*, *Carassius*) report PCSA in mm² and cannot be compared.
  So the claim's "measured teleost fraction" means **n = 1 species**.
- **The source survey reports wide variation.** Thorsen & Westneat 2005 (*J. Morphol.*,
  doi:10.1002/jmor.10173; read-level: abstract via search-summary) measured 12 labriform species and
  report "broad variation" in pectoral muscle masses. I could not get their per-species
  percentages. Whether any species comes near 7.5% is **unknown**.
- **Zebrafish: unknown.** Searched: web for "zebrafish adult pectoral fin muscle mass abductor
  adductor body mass fraction". The hits were developmental anatomy (Thorsen & Hale 2005;
  Patterson, Mook & Devoto 2008), with no mass fractions, read at search-summary level. One hit
  stated there is "little information available about the adult musculature" of zebrafish fins.
  This looks like **nobody has measured it** in an accessible source. It is not "measured and found
  small".
- **Flying fish (Exocoetidae): unknown.** Searched: web for exocoetid pectoral fin musculature and
  muscle mass. I found fin-area and fin-length morphometrics (Fish 1990; Davenport) and an old
  fibre-histology scan, but no muscle-mass fraction.

**Animals on both sides.** The measured value is from a **damselfish**. The claim's subject is
**zebrafish** (named for the muscle power) or possibly a hypothetical flier. The species differ,
so the status is `open`, not `satisfied`. My inference, not a measurement: *Abudefduf* is a
pectoral-fin specialist, so its fin muscle fraction is more likely to be high than low among
teleosts, which favours the constraint holding for zebrafish, a body–caudal-fin swimmer. That
reasoning is a prior, not evidence.

### C4 — organ — conservation: fin momentum flux must equal body weight

**Requirement.** In steady hover, the fins must push air downward with a momentum flux equal to
the body weight, mg. The ideal induced power for swept area A is then
P/m ≥ √(m g³ / (2 ρ_air A)). For the claim to hold, the 10.1–26.9 W per kg body (section 0,
derived) must be consistent with the subject's body mass and fin swept area under this bound, plus
profile and other losses.

**Check: `open`.** I could not find the S10 model's body mass, fin span or swept area. They are not
in this repository (see section 0), and the claim text does not state them. Without them I cannot
tell whether 730–1950 W/kg is near the actuator-disc minimum or inflated by loss terms. Making up
a body mass and fin area to run the check would break the honesty floor. Next step: read the S10-D
inputs and evaluate the bound. If the actuator-disc minimum alone exceeds what the muscle can
deliver at 1.38%, the claim is robust to every loss-model choice.

---

## 2. Summary

| # | scale | kind | requirement | status | animal behind the check |
|---|---|---|---|---|---|
| C1 | cell | energetic | fast muscle < 730 W/kg cycle-averaged | **satisfied** (larva); adult unknown | zebrafish 5 dpf, axial muscle |
| C2 | cell | timescale | power does not rise past the optimum frequency | **satisfied** | zebrafish 5 dpf, axial muscle |
| C3 | organ | range | pectoral muscle fraction < 7.5% body mass | **open** | measured in damselfish only |
| C4 | organ | conservation | momentum flux = mg; demand consistent with disc bound | **open** | model inputs not available |

**Nothing is `unsatisfiable`.** No measured number contradicts the claim from below.

**The claim is weaker than "strengthens" suggests.**
- The measured fraction comes from one damselfish species.
- The muscle-power figure is larval, axial and at 28 °C, applied to a pectoral fin.
- The threshold and the 5–15× ratio are the same calculation, not two separate pieces of evidence.

**Robust direction (derived).** Even with quail-level muscle power (~400 W/kg), the required
fraction is 2.5–6.7%, still above the one measured value of 1.38%.

## Sources and read-levels

- Mansuit R. & Herrel A. 2021. The evolution of appendicular muscles during the fin-to-limb
  transition. *Front. Ecol. Evol.* 9:702576. **full-text** (PDF, Table 1 read).
- Mead A.F., Kennedy G.G., Palmer B.M., Ebert A.M., Warshaw D.M. 2020. Mechanical characteristics
  of ultrafast zebrafish larval swimming muscles. *Biophys. J.* 119:806–820. **full-text**
  (PMC7451861; first ~100k of 120k characters read). The publisher's site was could-not-access
  (host blocked).
- Wakeling J.M. & Johnston I.A. 1998. Muscle power output limits fast-start performance in fish.
  *J. Exp. Biol.* 201:1505–1526. **search-summary**.
- Askew G.N., Marsh R.L. & Ellington C.P. 2001. *J. Exp. Biol.* 204:3601–3619 (quail take-off
  power). **search-summary**. Journal host could-not-access.
- Askew G.N. 2023, review in *J. Muscle Res. Cell Motil.* **search-summary**. could-not-access
  (eprints host blocked).
- Thorsen D.H. & Westneat M.W. 2005. *J. Morphol.* doi:10.1002/jmor.10173. **abstract**
  (search-summary).
- Thorsen D.H. & Hale M.E. 2005, *J. Morphol.*; Patterson S.E., Mook L.B. & Devoto S.H. 2008,
  *Dev. Dyn.* Zebrafish fin muscle development. **search-summary**.

```swarm-entail
{"source_claim": 77, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "cell", "kind": "energetic",
      "statement": "The cycle-averaged mass-specific mechanical power of the subject's fin fast muscle must lie below the lower bound of hover demand, so the shortfall cannot be met at the measured muscle fraction.",
      "quantity": "cycle-averaged net muscle power", "lo": null, "hi": 730, "units": "W/kg muscle",
      "status": "satisfied",
      "satisfied_by": "Larval zebrafish (5 dpf) myotomal muscle, 61% fast fibres: 134.4 +/- 19.9 W/kg at 80 Hz, 28 C, work loops. Context only, other taxa: Scorpaena notata fast fibres ~142.7 W/kg at 20 C; quail pectoralis take-off ~390 W/kg (max 530), derived from kinematics, also below 730.",
      "satisfied_evidence": "measured",
      "note": "Mead et al. 2020 Biophys J 119:806-820 (full-text, PMC7451861). Satisfied for LARVAL zebrafish AXIAL muscle only. Pectoral fin muscle not measured. Adult zebrafish: no work-loop power found (web search 'adult zebrafish fast muscle work loop power output W/kg'); not found, not shown absent. Wakeling & Johnston 1998 and Askew et al. 2001 at search-summary only."},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "Power per unit muscle mass must not keep rising with cycle frequency past the optimum, so a higher fin-beat frequency cannot close the deficit.",
      "quantity": "ratio of net power at 100 Hz to net power at 80 Hz", "lo": null, "hi": 1, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Larval zebrafish work loops at 28 C: 134.4 W/kg at 80 Hz, 122.9 W/kg at 100 Hz; ratio 0.91.",
      "satisfied_evidence": "measured",
      "note": "Mead et al. 2020 (full-text, PMC7451861). The decline is within 1 SD; it is the reported mean trend, not a significance test. Axial muscle at swimming frequencies; whether pectoral fin muscle has the same frequency optimum is unknown."},
    {"target_scale": "organ", "kind": "range",
      "statement": "The total pectoral muscle mass (both fins) of the hovering subject must lie below the lowest computed threshold for hover.",
      "quantity": "pectoral muscle mass / body mass, both fins", "lo": null, "hi": 7.5, "units": "% body mass",
      "status": "open",
      "satisfied_by": "Only measured value: Abudefduf saxatilis (damselfish) 0.69% per pectoral appendage, 1.38% both fins. This is not the claim's subject animal. Zebrafish and exocoetid fractions not found.",
      "satisfied_evidence": "measured",
      "note": "Mansuit & Herrel 2021 Front Ecol Evol 9:702576 Table 1 (full-text). It is the ONLY actinopterygian row normalised to body mass, so the 'teleost' generalisation is n=1. Thorsen & Westneat 2005 report 'broad variation' across 12 labriform species; per-species values not accessed (abstract only). Zebrafish searched (web; developmental anatomy only, Thorsen & Hale 2005, Patterson et al. 2008, search-summary): appears unmeasured, i.e. nobody has looked, not looked-and-found-small. Exocoetidae searched (web): fin morphometrics only, no muscle mass. Species mismatch: damselfish vs zebrafish, so open, not satisfied."},
    {"target_scale": "organ", "kind": "conservation",
      "statement": "In steady aerial hover, the fins' downward momentum flux must equal body weight. The claimed demand (10.1-26.9 W per kg body, derived as 1.38% x 730-1950 W/kg) must be consistent with the actuator-disc minimum sqrt(m g^3 / (2 rho_air A)) for the subject's mass and fin swept area.",
      "quantity": "hover power per unit body mass", "lo": 10.1, "hi": 26.9, "units": "W/kg body",
      "status": "open",
      "satisfied_by": "Not checked: the S10-D model's body mass and fin swept area are not in this repository (grep for Mansuit, S10-D, S32, exocoet, flying fish found nothing) and not stated in the claim.",
      "satisfied_evidence": "unknown",
      "note": "The lo/hi bounds are my calculation from the claim's own numbers, not measurements. Treating 'hover' as aerial is my inference. Next step: read the S10-D inputs and evaluate the actuator-disc bound."}
  ]}
```
