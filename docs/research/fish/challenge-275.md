# Challenge 275: adversarial review of S3 (organism mass and power budget)

**Claim under review** (from `harvest:s3-organism-mass-budget-000ync`; source document `docs/research/fish/S3-organism.md` and `S3_budget.py` on branch `origin/claude/s3-organism-mass-budget-000ync`, commit `d0fd062f`; I read the full document):

> No: charging wing mass from measured zebrafish fin tissue (40-281 um thick, 1.05-1.56 g/cm3 proxies, areal density 0.042-0.44 kg/m2) the mass budget closes for small wings (S28 192 mm2 wing = 2-21% of body, V_to 5.8-6.0 m/s) but large wings that lower V_to to 2.3-3.4 m/s weigh 31-211% of the 0.4 g body at central-to-high thickness (exceeding it from ~1300 mm2 at the high bracket), central-thickness fin tissue cannot lift even itself at the measured 1.38 m/s burst (V_self 1.44 m/s), and the launch needs 409-23,000 W/kg muscle at measured eta_h 0.37 versus 142.7 W/kg measured fast-start fish white-muscle power, so the power budget fails for every designed planform (even at eta_h = 1 the best case is 1.06x short).
>
> KEY: 2.9x launch-power shortfall in the most generous case (409 W/kg muscle required vs 142.7 W/kg measured; S10 1070 mm2 wing, 2 BL run-up, 60% muscle, eta_h 0.37); 20-161x for the S28 192 mm2 headline wing

**Verdict: WEAKENED, narrowly.** The power conclusion and the KEY number survive every relaxation I tried. One part of the mass clause does not hold: its upper bound (211 %, and the ">body" findings that use the 281 µm "high+" case) gives hydrated-bone density to tissue that the source itself identifies as *inter-ray* soft tissue. With a density that matches that tissue, the upper bound falls to about 140–175 % of body mass. The S10 wing then no longer outweighs the body at the thickest measured tissue. Everything in this file is **computation** (mine) on the author's stated inputs, unless a line says otherwise. I made no new measurements.

My independent script is `docs/research/fish/challenge-275_check.py`. I wrote it from the stated formulas and did not reuse `S3_budget.py`.

## 1. Independent arithmetic (computed)

Constants: g = 9.81, ρ_air = 1.225, CL = 1.07, m_body = 0.40 g, BL = 4 cm.

| Quantity | Claim | My value | Agrees? |
|---|---|---|---|
| σ low / central / high / high+ (kg m⁻²) | 0.042 / 0.138 / 0.311 / 0.44 | 0.0420 / 0.1380 / 0.3114 / 0.4375 | yes |
| V_self, central | 1.44 m/s | 1.437 m/s | yes |
| Lift per area at 1.38 m/s | 0.127 kg m⁻² | 0.1272 | yes |
| S28-C (192 mm²) wing / body | 2–21 % | 2.0–21.0 % | yes |
| S28-C V_to, central / high | 5.77 / 5.99 | 5.77 / 5.99 | yes |
| Large wings (900–1925 mm²), central→high+ | 31–211 % | 31.1–210.6 % | yes (arithmetic) |
| Large-wing V_to, central–high | 2.3–3.4 | 2.28–3.36 | yes |
| Area where wing = body at high σ | ~1300 mm² | 1285 mm² | yes |
| S10, 2 BL, η 0.37, f_m 0.6 | 409 W/kg (2.9×) | 409 (2.86×) | yes |
| S28-C, 0.5 BL, η 0.37, f_m 0.3 | 23,000 (161×) | 23,021 (161×) | yes |
| S28-C range (η 0.37) | 20–161× | 20.2–161× | yes |
| S10, 2 BL, η = 1 | 1.06× | 151 W/kg, 1.06× | yes |
| Calibration (1.38 m/s, 1 BL, f_m 0.3, η 0.37) | 148 | 148.0 | yes |

The power model is mean power = ½V²/t with t = 2s/V under constant acceleration. That equals V³/(4s), which is dimensionally sound. **No arithmetic error found.**

## 2. Proxies

1. **Bone density on inter-ray tissue (a real defect).** The "high+" case pairs 281 µm with 1.557 g cm⁻³. The author's own table T6 labels the 281 µm value (Murciano et al. 2018, via the author, full-text-partial) as *branch inter-ray* thickness. Inter-ray tissue is the soft tissue between the bony hemirays, so hydrated albacore bone density is the wrong proxy for it. Using the author's own soft or mixed densities for that thickness gives the following (computed):

   | t | ρ (g cm⁻³) | σ (kg m⁻²) | Area where wing = body | 1925 mm² wing | S2-large 1800 | S10 1070 |
   |---|---|---|---|---|---|---|
   | 281 µm | 1.05 | 0.295 | 1356 mm² | 142 % | 133 % | 79 % |
   | 281 µm | 1.15 | 0.323 | 1238 mm² | 156 % | 145 % | 86 % |
   | 281 µm | 1.30 (my assumption: ~50 % ray fraction) | 0.365 | 1096 mm² | 176 % | 164 % | 98 % |
   | 200 µm | 1.15 | 0.230 | 1739 mm² | 111 % | 103 % | 62 % |

   So the claim's **211 % upper bound becomes ≈140–175 %**. The source document says "the S10 wing already outweighs the body (117 %)" (§0 item 3). That statement **does not survive** a coherent density: S10 stays below body mass (79–98 %).

   The "high" case (200 µm × 1.557) is a caliper total-thickness value given a full-bone density. That combination is extreme but not strictly incoherent, since the proximal fin is ray-dominated. The "~1300 mm² at the high bracket" sub-claim is therefore arithmetically right for its stated proxy. It is better read as an outer bound than as a "high" estimate.

   **Large wings still exceed body mass at the coherent upper bound** (≳1100–1350 mm²). The qualitative mass statement stands; its magnitude is overstated.

2. **Mean thickness, a minor point.** The central 120 µm is a length-mean of a 200→40 µm taper. Weighted by the measured width growing 5→8 mm (T2), the area-weighted mean is **113.8 µm** (computed). That is 5 % lower and does not change any conclusion. V_self falls from 1.44 to about 1.40 m/s, which is still above 1.38.

3. **Caudal, not pectoral.** The author already flags this (no pectoral thickness measured). I did not search for a pectoral value myself.

4. **Muscle comparator.** P1 (142.7 W/kg) comes from *Scorpaena* at 20 °C and is abstract-level via the author. It is not zebrafish muscle at 28 °C. The author's P2 (larval zebrafish, 28 °C, 134 W/kg net) agrees with it, which limits how much a temperature correction can move the comparator. **Inference:** even a Q10-style uplift to ~200–300 W/kg (my assumption, not measured) leaves the most generous case 1.4–2× short at η_h 0.37.

## 3. Hidden assumptions, tested relaxed (computed)

- **Run-up length.** This is the assumption that matters most. In the author's model, the S10 2-BL case would close at η 0.37, f_m 0.6 only if the run-up were **5.7 BL**. The constant-η model ignores that drag rises with speed. Reaching 2.77 m/s in water means sustaining roughly (2.77/1.38)³ ≈ 8× the drag power at the measured burst speed (my scaling inference, drag ∝ V²). A longer run-up therefore makes things worse, not better, and it does not rescue the case. The model's "2 BL" bracket is optimistic for this reason.
- **Comparator choice and f_m.** I anchored the winged requirement to the wingless performance zebrafish demonstrably achieve (1.38 m/s, model calibration). In that ratio η_h, f_m and the muscle comparator all cancel. The required power ratio is (M/m_b)(V_to/1.38)³(s₀/s): **S10 5.5× (2 BL) to 11× (1 BL); S2-mid 6.4–13×; S28-C 39–78×** (computed). So the KEY's "2.9×, most generous" is, if anything, lenient. It owes part of its leniency to using f_m 0.6 while the calibration matched at f_m 0.3.
- **CL_max.** With CL raised to 1.5 (my assumption), S10's V_to falls to 2.34 m/s and the 2-BL requirement to 246 W/kg: **still 1.7× short**.
- **Peak vs mean power.** Only treating the P3 *instantaneous* peak (499–640 W/kg) as a sustained mean closes the large wings. The author already rejects that, and I agree. No measurement of a sustained mean at peak level was presented or found.

## 4. Evidence-level honesty

- The level is **derived**, and the source document states that the result is computed throughout. It is not presented as measured. This is correct.
- **Wording defect in the claim sentence.** It says "measured eta_h 0.37" without the taxon. η_h is measured only in **pike** (via S29, abstract), not zebrafish or any ~4 cm fish. The source document says this clearly in §2c and §5, but the one-sentence claim drops it. It should read "η_h 0.37 (measured in pike)". In the same way, "142.7 W/kg measured" is *Scorpaena* at abstract level.

## 5. Counter-examples searched

- **Freshwater hatchetfishes (Gasteropelecidae)** are small characiforms with an enlarged pectoral girdle. Secondary sources put their pectoral musculature at up to ~25 % of body mass. Search scope: one standard web search. Read-level: **search-summary** only (Seriously Fish, FishBase family page, a Wikipedia mirror). The summary attributes to Wiest (1995, *J Zool* 236:571–592; title and pages from search-summary, paper not read) the finding, made with high-speed video, that they do **not** achieve powered flight, but jump and skitter. If correct, that is consistent with the claim, not a counter-example. The exact wording is unconfirmed.
- **Exocoetidae taxi launch.** The author already lists this as not computed. It is the open regime, but it needs sustained surface thrust, which S28 found to be short.
- I found **no** published small fish (<1 g) achieving powered aerial take-off. Scope: the single search above, plus the author's §5 scope. This is not an exhaustive literature search.

## 6. What the verdict rests on

The power verdict rests on these: the S10/S2/S28 planform areas; CL 1.07; the 1.38 m/s burst (Miln 2021 via S28); η_h 0.37 (pike, via S29); f_m 0.3/0.6 (via S29, not measured); the 142.7 W/kg (P1, abstract) and 134 W/kg (P2) comparators; and the central thickness and density (Puri 2018 caliper, a 1.15 g/cm³ assumption). The weakening rests on the reading of Murciano 2018 Table 1 "branch IR" as inter-ray soft tissue, as the author's own T6 row labels it.

Sources (this challenge): [FishBase Gasteropelecidae](https://www.fishbase.se/summary/FamilySummary.php?ID=109), [Seriously Fish – Gasteropelecus sternicla](https://seriouslyfish.com/species/gasteropelecus-sternicla), [Gasteropelecidae wiki mirror](https://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq.ipfs.4everland.io/wiki/Gasteropelecidae.html). Read-level: search-summary for all three.

```swarm-challenge
{"claim_id": 275, "outcome": "weakened", "reason": "All arithmetic and the 2.9x / 20-161x power shortfall reproduce and survive relaxed run-up, CL and comparator tests (a performance-anchored ratio gives 5.5x, harsher), but the mass upper bound applies hydrated-bone density (1.557 g/cm3) to 281 um inter-ray soft tissue; a density matching that tissue cuts the large-wing upper bound from 211% to ~140-175% of body and the S10 wing no longer outweighs the body, and the claim sentence calls eta_h 0.37 'measured' without saying it is pike.", "corrected_value": "large-wing mass upper bound ~140-175% of 0.4 g body (1925 mm2 wing, 281 um at 1.05-1.30 g/cm3), not 211%; power KEY unchanged at 2.9x (409 vs 142.7 W/kg)", "depends_on": ["Murciano et al. 2018 Table 1 branch inter-ray thickness 281 um read as soft inter-ray tissue (via S3 T6)", "Puri et al. 2018 caudal fin thickness 200-40 um and width 5-8 mm (via S3 T1/T2)", "fin tissue density bracket 1.05-1.30 g/cm3 (D1 measured body proxy; 1.15-1.30 assumed ray-fraction mixes)", "eta_h 0.37 pike (Frith & Blake via S29, abstract)", "muscle fraction 0.3/0.6 (S29, not measured)", "142.7 W/kg Scorpaena fast-start muscle (Wakeling & Johnston 1998, abstract via S3)", "134 W/kg larval zebrafish net power (Mead et al. 2020 via S3)", "zebrafish burst 1.38 m/s (Miln et al. 2021 via S28)", "CL_max 1.07 (project value S2/S28)", "planform areas S28 192 mm2, S2 900/1800 mm2, S10 1070 mm2, 1925 mm2", "m_body 0.40 g, BL 4 cm"]}
```
