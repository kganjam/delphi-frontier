# Challenge 86 — adversarial review of the replication-5 CL_max claim

**Claim under review** (author: replicate-5, branch `claude/zebrafish-glide-replication-ptg7f5`,
file `docs/research/fish/replicate-5.md`, read at full text):

> "Replication: Re 1.9e3-4.0e3 reproduces, but measured steady CL_max near Re 3e3 is ~1.0
> (0.9-1.1) for cambered/corrugated thin wings (snake section 1.1, dragonfly 0.93-1.07); <=0.6
> holds only for a flat plate on weak evidence; fin value unknown."
> Recorded evidence level: derived. Value: 1 CL_max.

Read-levels used here: full-text | abstract | listing | search-summary | could-not-access.

**Verdict: WEAKENED.** The Re half survives. The CL_max ≈ 1.0 central number is not refuted,
but four things are wrong with it. The sentence calls it "measured" when it is a synthesis. One
of its two supports is mislabelled. The other support is at a lower Re and is not a CL_max. And
CL_max may be a proxy for the operating C_L, which is the quantity the claim it rebuts was
actually about.

---

## 1. Arithmetic, redone independently

Inputs, as stated in replicate-5: m = 4.0e-4 kg, g = 9.81 m/s², ρ = 1.2 kg/m³,
ν = 1.5e-5 m²/s.

**Formula.** I started from lift = weight with S = AR·c²:
- V = √(2W / (ρ·AR·c²·C_L))
- Re = Vc/ν = √(2W / (ρ·AR·C_L)) / ν

So c cancels. This is my own derivation, and it matches the author's.

**Weight.** W = 3.924e-3 N, so 2W = 7.848e-3 N.

**Range ends (my calculation):**
- AR 3, C_L 0.6: ρ·AR·C_L = 2.16. 7.848e-3 / 2.16 = 3.633e-3. √ = 0.06028. Re = **4,019**.
- AR 8, C_L 1.0: ρ·AR·C_L = 9.6. 7.848e-3 / 9.6 = 8.175e-4. √ = 0.02859. Re = **1,906**.

**Result: Re 1.9e3–4.0e3 reproduces (calculated, not observed).** No defect.

One hidden assumption sits here: AR 3–8. No fin geometry was retrieved, so this range is the
author's assumption. Pectoral fins are often low aspect ratio (AR ≈ 1–2). That is my
inference; I did not retrieve a zebrafish fin AR. If I relax the range to AR 1.5 at C_L 1.0,
I get Re = √(7.848e-3 / 1.8) / 1.5e-5 = **4,402** (calculated). That is still O(10³), so the
regime conclusion holds. But the stated upper bound depends on the assumed AR.

## 2. Is a proxy standing in for the quantity that matters?

Yes, in two ways.

**(a) CL_max versus operating C_L.** The Re formula and the wing-area tables need the C_L the
glider actually flies at. A glider does not cruise at stall. It flies near (L/D)_max, or below
CL_max by a stall margin. The original claim, "CL_max is probably ≤ 0.6", was used to set the
working design C_L = 0.6.

The replication rebuts it with section or isolated-wing **CL_max** values of about 1.0. Its
final line then says the required wing area "falls by a factor of 1/0.6 ≈ 1.67". That step
swaps CL_max in for operating C_L. A flight at C_L ≈ 1.0 is a flight at or near stall, so
the 1.67 area saving is an upper bound, not an expected value. This is my inference.

The right quantity is the C_L at (L/D)_max, or CL_max times a stall margin. For a fin-like
membrane at Re ≈ 3e3 that value is **unknown**. The replication itself notes that
arXiv:2605.19468 reports CL/CD optima but not CL_max. I did not re-read that paper.

**(b) A 2-D or isolated-wing section versus a low-aspect-ratio 3-D fin.** The author says low
AR "would usually reduce the usable 3-D C_L below the section CL_max". That is true for lift
slope. It is not reliably true for CL_max: on low-AR plates, tip-vortex lift and delayed stall
can hold CL_max near or above 2-D values. This is my inference from general aerodynamics. I
found no number at Re ≈ 3e3 to settle the sign of the effect, so it is **unknown**. The
caveat's direction is therefore unsupported, though not shown to be wrong.

## 3. The supports, examined

| Support | What the claim says | What I found | My read-level |
|---|---|---|---|
| Snake section, 1.1 | Listed under "cambered/corrugated thin wings" | Holden et al. 2014 is a **thick, bluff** body cross-section. The author's own Section 2 says so ("L1 is a thick bluff section, not a membrane"). The headline sentence drops that caveat. The abstract-level summary I retrieved gives max CL **1.9**, lift rising to 35°, Re 3,000–15,000. It does not tie a value to Re 3,000. The 1.1 low-Re figure comes from the author's full-text read of Krishnan et al. (arXiv:1309.2969), which I did not re-read. | search-summary |
| Dragonfly, 0.93–1.07 | "measured steady CL_max near Re 3e3" | Wakeling & Ellington 1997 (J. Exp. Biol. 200:543). The summary I retrieved says **0.93 is the maximum C_L recorded in free glides, and "this is not necessarily the maximum possible from the wings"**, so 0.93 is an operating value, not a CL_max. **1.07** (wind tunnel) appeared only as a secondary citation in a later CFD paper. Isolated-wing tests were at **Re 700–2,400**, below "near 3e3". | search-summary (PDF on cob.silverchair.com; I did not attempt it, and the author reports it could-not-access) |
| Sunada et al. 1997, cambered plate 1.06 at Re 4,000 | Not cited in the claim sentence, though it is in the author's table | This is actually the only thin cambered-plate datum at this Re in the evidence set, and it is at the top of the range (4e3). My search confirmed the paper's bibliographic details and an abstract fragment about leading-edge vortices. It did **not** return the 1.06 or any flat-plate value. | search-summary (bibliographic only) |

Consequence (my inference): **no measured CL_max for a thin cambered or corrugated wing at
Re ≈ 3e3 was retrieved, by the author or by me.**
- The value nearest Re 3e3 is from a thick bluff body (snake).
- The thin-wing values are either at Re ≤ 2,400 (dragonfly) or at Re 4,000 on an
  unconfirmed search summary (Sunada).
- The ~1.0 is plausible as an interpolation, but it is an interpolation.

## 4. Is the evidence level honest?

The record labels it **derived**, which is correct. The claim sentence, however, says
**"measured steady CL_max near Re 3e3 is ~1.0 (0.9–1.1)"**. Under the honesty floor, that
wording presents a derived synthesis as an observation, and that is a defect. "Steady" is also
wrong for the 0.93: it is a free-glide operating value, not a steady-flow wing CL_max.

The 0.9–1.1 band is also not a measurement uncertainty. It is the spread of three heterogeneous
values (a bluff body at 1.1, a free-glide value at 0.93, a secondary-citation tunnel value at
1.07), each with different geometry and Re.

## 5. Missed regimes or counter-examples

- **Flat plate at low Re.** The claim's "≤ 0.6 holds only for a flat plate" rests on the
  author's own arithmetic on an ambiguous summary of Sunada ("100–150 % higher"). The author
  already flags that this may refer to L/D. I searched for a direct steady flat-plate CL_max at
  Re 1e3–1e4 (2 standard web searches) and found none: only unsteady pitching or plunging
  data, suction- or forcing-controlled plates, and Re ≥ 5e4 plates. So the flat-plate figure
  is **unknown** rather than "≤ 0.6 on weak evidence". The claim's own qualifier covers this,
  so I count it as a minor point.
- **Okamoto, Yasuda & Azuma 1996** (J. Exp. Biol. 199:281) tested dragonfly wings and
  flat-plate comparisons and is directly relevant. My search returned the citation only, with
  no numbers (listing-level). Its values are unknown to me.
- **Gliding fish taxa.** Flying fish (Exocoetidae) are the obvious biological counterpart, but
  they glide at much higher Re. I did not retrieve their data and do not use it here. For
  small freshwater "flying" fish such as hatchetfish, which are closer in mass, I found no
  fin CL data (not searched in depth). The fin value stays **unknown**, as the claim says.

**Scope of my negative searches.** 5 standard web searches, on 2026-11-04:
1. Sunada 1997 flat-plate CL_max
2. Wakeling & Ellington 1997 CL_max
3. Holden 2014 CL at Re 3000
4. Generic steady flat-plate CL_max at Re 1e3–1e4
5. Okamoto 1996

I fetched no full texts.

## 6. What survives and what changes

- **Survives:** Re ≈ 1.9e3–4.0e3 (calculated, for AR 3–8 and C_L 0.6–1.0). It is still
  O(10³) at AR ≈ 1.5. The fin CL_max is unknown. The "≤ 0.6" figure, read as a CL_max, is
  not well supported.
- **Weakened:**
  - "Measured ... ~1.0" should read "derived, not measured: interpolated from a thick snake
    section (≈1.1, Re 3e3), dragonfly wings at Re 700–2,400 (1.07 wind tunnel, secondary
    citation; 0.93 is a free-glide operating value, not CL_max), and a cambered plate at
    Re 4e3 (1.06, search-summary)".
  - The snake value must not be grouped with "thin wings".
  - The replication's ×1.67 wing-area saving uses CL_max as the operating C_L, so it is an
    upper bound.

**Corrected statement (my wording):** CL_max ≈ 1.0 (0.9–1.1) for a thin cambered or corrugated
wing at Re ≈ 3e3 is a **derived interpolation**, not a measurement at that Re. The operating
glide C_L that sets wing area is lower by an unknown stall margin, and its value is unknown.

```swarm-challenge
{"claim_id": 86, "outcome": "weakened", "reason": "Re reproduces, but the ~1.0 CL_max is a derived interpolation worded as 'measured': no thin-wing CL_max at Re~3e3 was retrieved. The snake support is a thick bluff section, the dragonfly support is at Re 700-2400 and its 0.93 is a free-glide operating value rather than CL_max, and CL_max is used as a proxy for the lower operating glide C_L that sets wing area.", "corrected_value": "CL_max ~1.0 (0.9-1.1), derived interpolation rather than measured, for a thin cambered wing at Re ~3e3; operating glide C_L lower by an unknown margin; fin value unknown", "depends_on": ["replicate-5.md Re derivation inputs (m=0.4 g, rho=1.2, nu=1.5e-5, AR 3-8 assumed)", "Holden et al. 2014 snake cross-section is a thick bluff body (search-summary; 1.1 at low Re via author's full-text of arXiv:1309.2969)", "Wakeling & Ellington 1997: 0.93 is free-glide max, not wing max; isolated wings at Re 700-2400; 1.07 from secondary citation (search-summary)", "Sunada et al. 1997 cambered plate 1.06 at Re 4000 (author's search-summary; not confirmed by my search)", "Assumption that a glider operates below CL_max (standard flight mechanics, my inference)"]}
```
