# Challenge 293: the fin voltage decay length (S41)

**Claim under review (written by someone else):** "[S41] The only fitted voltage decay length in zebrafish fin tissue is ~0.19 mm (apical 186+/-39 um, basal 197+/-22 um; injury-induced transepithelial gradient in 2 dpf larval fin, Liu et al. 2025 preprint, cable theory l=sqrt(D/Lambda)); ... ~26x short of an adult Danio ray and ~632x short of the 120 mm design target ... requiring a 4.2e5-fold rise in D*R that diffusivity cannot supply ... the primary authors claim outgrowth-duration tuning and explicitly deny changing positional information."
Recorded level: derived. Source: `harvest:kcnh2a-gradient-decay-aticbh`. That harvest file is **not in this repository**. I searched the whole repo for `aticbh`, `kcnh2a`, `kcnk5b` and `decay length` and found only unrelated hits, so I could not read the author's own working.

**Verdict: WEAKENED.** The order of magnitude holds: the one fitted fin voltage length I could find is about 0.2 mm, which is hundreds of times shorter than 120 mm. But the quoted inputs don't match the published paper, one derived figure uses a different input from the headline, and the "D*R" closing argument puts the wrong physical quantity in place of the one that matters.

## Sources and read-levels

| # | Source | Read-level | What I took from it |
|---|---|---|---|
| A | Liu, Nerli, Duclut, ... Jülicher, Mateus. "Injury-induced electrochemical coupling triggers organ growth", *Sci. Adv.* 2026, 12(6):eaec0687, PMC12871474 | full-text (main text, read through the PMC HTML; supplementary theory notes S1 to S6 **not** read) | apical **206 ± 48 µm**, basal **187 ± 24 µm**; fit made at **0.1 s post-cut** to the Voltron2 −ΔF/F profile (Fig. 1K; error is the 95% CI of the fit, n = cells); l set by ion diffusion D and the tight-junction leak Λ; Λ = 0.05 s⁻¹ estimated *from* l; 2 dpf finfold; Voltron2 held "over the next 5 s" |
| B | Same group, bioRxiv 10.1101/2025.04.03.647033 (the "Liu et al. 2025 preprint") | could-not-access (HTTP 429 on four tries) | I could not check whether 186 ± 39 / 197 ± 22 µm appear in it. An exact-number web search found no indexed source containing those numbers. |
| C | Stewart et al. 2021, *Development*, "longfin causes cis-ectopic expression of the kcnh2a ... to autonomously prolong fin outgrowth" (PMC8217709) | search-summary | The authors conclude that ion signalling tunes outgrowth periods "rather than altering positional information". The claim's attribution holds. |
| D | Aramaki & Kondo, bioRxiv 10.1101/2024.03.27.587111 | abstract | kcnk5b(W169L) expressed in **epidermis** changes fin size; in osteoblasts it changes segment length. No Vm measurement. |

## 1. Arithmetic, redone independently

- 0.19/0.1 = 1.9, so it is within a factor of 3 of the 0.1 mm end. **OK.**
- 120 mm / 0.190 mm = **632×**. **OK** at 0.19. Across the claim's own two values (186 to 197 µm) the ratio is 609 to 645×. Across the published values (187 to 206 µm, source A) it is **583 to 642×**.
- Required fold rise in the squared length (l ∝ √(D/Λ), so the factor needed is (L/l)²): at 0.190 mm it is **3.99 × 10⁵**, not 4.2 × 10⁵. The author's 4.2 × 10⁵ matches (120/0.186)² = 4.16 × 10⁵, which uses the *apical* value, not the 0.19 mm headline. This is a small internal inconsistency. With source A's values the range is **3.4 × 10⁵ to 4.1 × 10⁵**.
- "~26× short of an adult Danio ray" implies an adult ray of about 4.9 mm (26 × 0.19). The claim never states that ray length or cites it, so this ratio rests on an unstated input. I did not verify an adult ray length and leave it `unknown`.
- Consistency check (my inference, not the paper's): √(D/Λ) with Λ = 0.05 s⁻¹ and D(Na⁺) = 1334 µm²/s (the value source A quotes elsewhere) gives 163 µm. With the textbook D(Cl⁻) ≈ 2030 µm²/s it gives 202 µm. Both bracket the measured l, so the square-root form in the claim is dimensionally right. Source A's HTML renders it as "l = D/Λ", most likely because the square-root sign was lost.

## 2. Inputs do not match the published record

Source A, the peer-reviewed version, gives **apical 206 ± 48 µm and basal 187 ± 24 µm**. The claim gives apical 186 ± 39 and basal 197 ± 22. That is a different value and different error for each layer, and the **apical/basal order is reversed** (published: apical > basal; claimed: basal > apical). The claim's numbers may be the preprint's, but I could not access the preprint (B), so this is unresolved rather than shown to be wrong. Either way the claim cites a superseded version when a published one exists. The headline "~0.19 mm" should read **~0.19 to 0.21 mm**.

## 3. Proxy: the wrong length stands in for the one that matters

The design question is whether a **standing**, channel-driven (kcnh2a/kcnk5b) Vm pattern could carry information along a ray. The measured quantity is something else on every axis:

| | Measured (source A) | What the design needs |
|---|---|---|
| Timing | transient, 0.1 s post-cut, followed for ≤5 s | steady state over days to weeks of outgrowth |
| Trigger | wound breaching the epithelium | channel expression, with no wound |
| Medium | ion electrodiffusion in the **interstitial space** between two epithelial layers, leaking through tight junctions (Λ) | Vm spread through **gap-junction-coupled intra-ray mesenchyme**. Stewart et al. place kcnh2a action there, and Cx43 is a fin-size gene. |
| Tissue | 2 dpf **finfold**, which has no bony rays (lepidotrichia) yet | adult or regenerating ray |

The length that matters is the syncytial electrotonic length λ = √(r_m/r_i) of coupled mesenchyme, set by membrane and junctional resistance. **That quantity is unknown.** I found no measurement of it in the sources above. The claim's last step ("a 4.2e5-fold rise in D*R that diffusivity cannot supply") applies a diffusion-limited argument to a medium that isn't diffusion-limited. The leak term Λ, and in a syncytium r_m and junctional conductance, are biologically tunable over orders of magnitude. D is not. So "diffusivity cannot supply it" is true but beside the point. It does **not** show that the length cannot be reached. It only shows that this measured length isn't it. The claim should say "unmeasured", not imply "physically excluded".

## 4. Hidden assumption: one source spanning the whole ray, tested relaxed

The 632× figure assumes a single exponential from one boundary must cover the full 120 mm. Fin outgrowth adds tissue at a distal blastema that is about a few hundred µm thick and moves with the growing tip. A ~0.2 mm gradient anchored at the tip would cover the blastema at any final length. Relaxing the assumption therefore removes the 632× gap as a *mechanistic* barrier for tip-local signalling. It does not rescue a body-length positional gradient. This is my inference; no source here tests it.

## 5. Counter-examples and scope of negative searches

- "The **only** fitted voltage decay length in fin tissue." Search scope: two web searches (standard and extended) on zebrafish fin depolarization, decay length and cable theory, plus the repository. I found no other fitted fin length. Source A does give a *second* length scale, about 100 µm, for proliferation and strong depolarization. That is not a fitted Vm decay length, so it doesn't contradict "only", but "only" rests on a shallow search.
- "No kcnh2a/kcnk5b-driven standing gradient has ever been measured." Same scope. I found no counter-example. Source D manipulates kcnk5b without measuring Vm.
- **Disagreement to keep:** Stewart et al. (C) place kcnh2a action in intra-ray mesenchyme. Aramaki & Kondo (D) find fin-size control by kcnk5b through **epidermis**. Which tissue would host a gradient is contested, and that changes which length constant matters. I have not averaged the two.
- The "duration, not positional information" attribution to Stewart et al. 2021 **survives** (source C, search-summary level).

## Evidence level

"Derived" is honest for the ratios. The decay lengths themselves are **measured, model-fitted values**: an exponential fit to Voltron2 data at 0.1 s, not a cable-theory calculation. The claim's wording, "cable theory l=sqrt(D/Lambda)", could be read as saying the length was computed. Source A instead fits l from data and *then* infers Λ from it.

## Corrected statement

The one fitted fin voltage length found is **~0.19 to 0.21 mm** (published: apical 206 ± 48 µm, basal 187 ± 24 µm). It is a transient (0.1 s post-cut) interstitial electrodiffusion length in a ray-less 2 dpf finfold, not a standing channel-driven Vm length. That is **583 to 642×** short of 120 mm, and a single-source exponential would need a (3.4 to 4.1) × 10⁵-fold rise in D/Λ. Whether a gap-junction syncytium could reach the needed length is **unknown**, because its λ has not been measured. It is not excluded by diffusivity.

```swarm-challenge
{"claim_id": 293, "outcome": "weakened", "reason": "The order of magnitude (~0.2 mm, ~600x short of 120 mm) holds, but the quoted apical/basal values disagree with the published Sci Adv version (206±48 / 187±24 um, ordering reversed), the 4.2e5 factor uses 186 um not the 0.19 mm headline (0.19 mm gives 4.0e5), and the 'D*R diffusivity cannot supply' step applies a transient 0.1 s interstitial electrodiffusion length (set by D/Lambda in a ray-less 2 dpf finfold) as a proxy for the unmeasured syncytial gap-junction length of a standing kcnh2a/kcnk5b Vm pattern, so it shows unmeasured, not excluded.", "corrected_value": "0.19-0.21 mm (published: apical 206±48 um, basal 187±24 um, at 0.1 s post-cut); 583-642x short of 120 mm; required (L/l)^2 = 3.4e5-4.1e5", "depends_on": ["Liu et al. Sci Adv 2026 eaec0687 (PMC12871474) Fig 1K characteristic lengths apical 206±48 um, basal 187±24 um at 0.1 s post-cut, main text read; supplement not read", "Liu et al. bioRxiv 10.1101/2025.04.03.647033 values could-not-access (HTTP 429)", "120 mm design target as stated in the claim", "Stewart et al. 2021 Development longfin/kcnh2a duration-not-positional conclusion (search-summary)", "Aramaki & Kondo bioRxiv 2024.03.27.587111 epidermal kcnk5b fin-size result (abstract)", "negative search scope: 2 web searches + repo grep, no other fitted fin Vm decay length or standing kcnh2a/kcnk5b gradient found"]}
```
