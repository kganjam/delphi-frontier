# Challenge 239: "smallest fish glider needs the same 4.23 m/s as the zebrafish design"

**Claim under review (from S30-organism.md, branch `claude/s30-launch-budget-mass-k71prf`):**
"The smallest real fish glider is ~1-2 g at wing loading 11.7 N/m2, needing 4.23 m/s, essentially THE SAME
takeoff speed as the zebrafish design requires. The difference is not the speed; it is the mode of reaching it."
Recorded evidence level: **literature**. Value: 4.23 m/s. Source: Fish 1990, via S30.

**Verdict: WEAKENED.** The arithmetic is right. The evidence level is wrong: 4.23 m/s is a number derived
with an assumed CL_max, not a figure from the literature. Three parts of the sentence also say more than the
evidence supports: "glider", "the same as the design", and "the difference is the mode".

## Sources and read-levels

| Source | Read-level | What I used |
|---|---|---|
| S30-organism.md and S30_scaling.py (branch above) | full-text | the claim, the inputs (ρ 1.225, CL_max 1.07), the WL_FIT table |
| `connectors/fish_controls/fish1990.py` on `main` (the project's transcription of Fish 1990 Tables I–III) | full-text of the transcription. **The paper itself was not read by me.** | Table II, where Hirundichthyes WL ranges from 11.7 to 141.9 N/m², with fit a = 390.069 and b = 0.526. Table I, where Hirundichthyes length is L = 0.429·M^0.314. The recorded inconsistency between "0.001 kg" in the text and 0.003 kg as the minimum mass in the methods |
| S28-organism.md and S28_organism.py (branch `claude/s28-organism-design-5z0vjz`) | full-text | design cases A/B/C, m = 0.25 g, S = 57/125/192 mm² |
| Park & Choi 2010, J Exp Biol 213:3269 | search-summary | flying-fish CL peaks at 30–35° angle of attack. The search did not give me the peak value |
| Wiest 1995, J Zool 236:571 (hatchetfish) | search-summary, via a hobbyist site | reportedly no powered flight in Gasteropelecidae. Hobbyist pages say they glide |

## 1. Independent arithmetic

V_to = √(2·WL / (ρ·CL_max)) with ρ = 1.225 kg/m³. I recomputed every number below myself; none is copied from S30.

- WL 11.7, CL_max 1.07 → **4.225 m/s**. This matches the claimed 4.23 m/s.
- WL 12.5, CL_max 1.07 → **4.367 m/s**. This matches the claimed 4.37 m/s.
- Ratio of the two: √(11.7/12.5) = **0.967**. **CL_max cancels in this ratio as long as both animals are given the same CL_max.** The "same speed" comparison therefore does not depend on the CL_max value. Only the absolute 4.23 m/s does.
- Mass check, my calculation from the transcribed Hirundichthyes fit: WL 11.7 gives M = (11.7/390.069)^(1/0.526) = **1.27 g**, and the length fit gives L ≈ **53 mm**. That agrees with the ~1–2 g in the claim and with the ~50 mm flight onset attributed to Davenport 1994. On mass, the claim survives.
- 4.225 m/s at 53 mm is **≈ 80 BL/s**. S30 says ~85 BL/s, but that uses a rounded 50 mm length. The difference is immaterial.

## 2. Proxy check

- **CL_max stall speed is standing in for takeoff speed.** The quantity that matters is the speed at which the animal can support its weight once it leaves the water. That depends on the CL the fish can actually reach at its angle of attack, plus any ground-effect gain. Park & Choi 2010 (search-summary) report that flying fish gain lift-to-drag ratio near the surface, so the free-air stall speed is, if anything, an upper bound on what is needed.
- **CL_max 1.07 is assumed for flying fish.** S30 says this itself in §3. If the true value is 0.93, the low end of S2's range, the requirement becomes **4.53 m/s**, again my calculation. The absolute value is therefore 4.2–4.5 m/s, not a literature point value.
- **"Glider" is standing in for "museum specimen with a measured wing loading".** The 11.7 N/m² value comes from a preserved (ethanol) specimen. Fish 1990 reports morphology, not flight. Nothing I read shows that this individual, or Hirundichthyes at ~1 g, glides. That rests on a separate source, Davenport 1994, which I have not read and know only through S30/S20. So "smallest real fish glider" joins two different datasets: one gives the size at flight onset, the other gives the wing loading of a specimen.

## 3. Hidden assumption: what "the zebrafish design" is

- The 4.37 m/s figure belongs to S28 **case C**, where AR 5 is *imposed*, giving S = 192 mm². That fin area has never been measured.
- I recomputed S28's own two other cases at 0.25 g: **case B (isometric fin, 125 mm²) gives 5.47 m/s, and case A (length-only, 57 mm²) gives 8.10 m/s.** Relative to the small flying fish, those are 1.3× and 1.9× the speed, or 1.7× and 3.7× the kinetic energy per kg.
- Small correction: at 0.25 g, case C works out to WL **12.77 N/m²** and **4.41 m/s**. The 12.5 N/m² and 4.37 m/s are the project's earlier anchor numbers. This shifts the ratio from 0.967 to 0.957 and does not change the conclusion.
- **Conclusion on this point:** "essentially the same speed" is true only for the design case with the most favourable *assumed* fin area. Drop that assumption, and the speeds still match only if the mutant's real fin area turns out to be ≥ ~190 mm².

## 4. Is the evidence level honest?

**No.** Fish 1990 (in the project transcription) prints the wing loading 11.7 N/m². It prints no speed. The 4.23 m/s figure is **derived** from that printed WL, an assumed CL_max of 1.07, and ρ = 1.225. It should be recorded as `derived (from literature WL + assumed CL_max)`, not `literature`. The number is right, but the label is a defect.

The mass also needs a qualifier. The paper is internally inconsistent: the text says 0.001 kg, while the methods give 0.003 kg as the minimum. The transcription keeps both. The fit supports ~1.3 g. If the specimen was really 3 g, its WL of 11.7 would be far below the genus fit (18.4 N/m² at 3 g, my calculation), but the speed would stay the same, because it depends only on the printed WL.

## 5. The "mode" sentence, and possible counter-examples

- "The difference ... is the mode of reaching it" is an **inference**. S30 itself says the multi-stroke route at ~1 g is "inferred, not verified", and that it "found no measurement of how the smallest exocoetids leave the water". The claim states it as a finding, and it is not one.
- **A possible counter-example to "smallest real fish glider ~1–2 g": freshwater hatchetfishes (Gasteropelecidae, e.g. *Carnegiella*).** Hobbyist sources (search-summary) say they leap and glide. Wiest 1995 (search-summary only, not read) reportedly found no flapping flight. I found **no** measured mass, wing loading or glide trajectory, so I cannot say whether they glide below 1 g. Mass: `unknown`. Search scope: two web searches, for Park & Choi 2010 and for hatchetfish/Wiest 1995. I did not search for *Pantodon* or for juvenile exocoetids below 50 mm. The claim's "smallest" is therefore unrefuted but unsecured.

## Corrected statement

The smallest exocoetid wing loading in Fish 1990's tables (11.7 N/m², preserved Hirundichthyes, ~1.3 g by the genus fit; the paper is internally inconsistent on mass) implies a **derived** stall takeoff speed of **4.23 m/s at an assumed CL_max of 1.07 (4.53 m/s at 0.93)**. That is ~0.96–0.97× the zebrafish design's requirement, but only for design case C, whose AR-5 fin area is assumed. S28's cases A and B need 1.3–1.9× more speed. That flight at this size uses a multi-stroke mode is an inference, not an observation.

```swarm-challenge
{"claim_id": 239, "outcome": "weakened", "reason": "The arithmetic (4.23 m/s, ~0.97x the design) reproduces, but 4.23 m/s is derived from a printed wing loading plus an assumed CL_max of 1.07, not literature; the speed match holds only for the assumed-area design case C (cases A/B need 5.5-8.1 m/s); a museum specimen stands in for a demonstrated glider; and the 'mode' difference is unverified inference.",
  "corrected_value": "4.23 m/s derived (CL_max 1.07 assumed; 4.53 m/s at CL_max 0.93), not literature",
  "depends_on": ["Fish 1990 Table II Hirundichthyes WL min 11.7 N/m2 and fit a=390.069 b=0.526 (project transcription connectors/fish_controls/fish1990.py)", "Fish 1990 Table I Hirundichthyes length fit L=0.429*M^0.314 (project transcription)", "CL_max 1.07 (S2/S30, assumed for flying fish) and 0.93 (S2 lower bound)", "rho_air 1.225 kg/m3", "S28 design cases A/B/C: m=0.25 g, S=57/125/192 mm2 (S28_organism.py)", "S30 statement that the 1 g multi-stroke route is inferred, not verified"]}
```
