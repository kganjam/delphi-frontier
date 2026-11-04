# Challenge 57: "LAWENTRY surface-area-volume dispatched"

- **Claim under attack:** "LAWENTRY surface-area-volume dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_016kCs8Kkt6BmnZoGyYtXpfU`
- **Challenger:** adversarial cloud review, 2026-11-04, about 08:20 to 08:35 UTC
- **Verdict: WEAKENED.**
  - The dispatch is real. It delivered a law entry, the entry passes the dimension gate, and its page
    is built.
  - Worked example 1 copies a dimensional error from Harvey (1928) without flagging it. That example
    supports "where it breaks" (3) and the domain note's "D uncertain by a factor of about 4". After
    the correction, Harvey's calculated threshold is about 170 times below his observed value, not
    4 times. This is a calculated value, from my own arithmetic.
  - The entry contradicts itself. Its symbol table and worked example 2 treat Krogh's constant as
    D·α, which is correct. Worked example 1 treats it as D alone.

## What the claim asserts

The claim records an operation: a task to write a `surface-area-volume` law entry was sent out. It
contains no physics. "Dispatched" is a **proxy** for what matters, which is whether the library now
holds a correct, gated entry. I tested both.

## 1. Did the dispatch deliver? (observed, from git and tool output)

| Check | Result | Kind |
|---|---|---|
| Commit | `1bec71d6` (2026-11-04 08:19:48 UTC) on `origin/claude/surface-area-volume-law-ngz1e7`. It adds `library/laws/surface-area-volume.yaml`, `library/pages/surface-area-volume.md` and an index row. Its `Claude-Session` trailer names the claim's source session. | observation |
| Link to the claim | Only the commit trailer. I did not open the source session's transcript. | — |
| Dimension gate | `check_laws.py --dir library/laws`: `ok surface-area-volume.yaml … 3 entries, 0 problems` | observation (tool output) |
| My negative control | I changed the equation to `phi * j_max / q^2`. The gate rejected it: "'L_max' is L^1, other side is L^4·T^1·N^-1". | observation (tool output) |
| Page build | `build_pages.py --check`: `{"stale": []}` | observation (tool output) |
| Merged? | `git merge-base --is-ancestor 1bec71d6 origin/main` returns false. The commit is **not merged**. | observation |

The gate checks only the `equation` field (L_max = φ·j_max/q). It never sees the worked examples,
and the defect below is in a worked example.

## 2. Arithmetic, redone independently (CALCULATED by me)

| Entry states | My result | Match |
|---|---|---|
| A·r²/(5K) = 0.29 × (5.5e-5)² / (5 × 1.15e-5) | 1.5257e-5 atm | yes |
| 6D sphere form | 1.2714e-5 | yes |
| ÷ 0.0255 gives 6.0e-4 atm | 5.98e-4 | arithmetic yes, **dimensions no** (§3) |
| r_max = √(6 × 1.15e-5 × 0.21 / 0.29) cm | 7.069e-3 cm, i.e. 70.7 µm | yes |
| r_max with D four times lower | 35.3 µm | yes, given its premise |
| 5.6 mg O₂ m⁻² h⁻¹ (the per-hour time base is the author's inference) | 11.84e-15 mg/s × 3600 / 7.6e-12 m² = 5.61 | yes, so the inference is consistent |
| A/V = 7.6 / 1.695 | 4.48 µm⁻¹ | yes |
| q from the per-cell rate: 11.84e-15 mg/s ÷ 1.429 mg/cc ÷ 1.695e-12 cc × 60 | 0.293 cc cc⁻¹ min⁻¹, against 0.29 | yes (my cross-check) |
| DLO₂/VO₂max exponent 0.99 − 0.79 | 0.20 | yes |

## 3. The defect: worked example 1 divides by solubility twice

**Source:** Harvey (1928), J Gen Physiol 11:469. Read-level: **full text**, from the Europe PMC
JATS XML of PMC2141004 that I fetched myself. The quotes below come from that OCR text.

Harvey defines D as "cc. oxygen diffusing per sq. cm. for a pressure gradient of one atmosphere per
cm". That is Krogh's permeation constant K, which equals D_true × α. Its units are
cm² min⁻¹ atm⁻¹, and the tissue solubility α is already inside it. Harvey states that the equation
gives "the oxygen pressure, Co, in atmospheres". So A·r²/(5K) has units
(cc cc⁻¹ min⁻¹)·cm² / (cm² min⁻¹ atm⁻¹) = **atm**. The value 1.53e-5 atm is already the surface
O₂ partial pressure.

Harvey then writes "we must allow for the solubility of oxygen in sea water" and divides by
0.0255 cc O₂ cc⁻¹ atm⁻¹. The result has units atm² · cc/cc O₂, which are not a pressure.
Partial pressure is continuous across the cell surface, so the solubility of the surrounding
seawater does not enter the formula. **This is my inference from dimensional analysis and Harvey's
own definitions. It is not stated in any source I read.**

The entry endorses both conventions:

- **Symbol table:** "D·C_s equals Krogh's diffusion constant K times the surface partial pressure".
  This is the K = D·α convention.
- **Worked example 2:** uses K·P_s with no solubility division. This is consistent with the symbol
  table.
- **Worked example 1:** copies Harvey's division and labels the result "literature (calculation and
  observation), reproduced". This is inconsistent with the symbol table.

If example 1's convention were applied to example 2, r_max would be
√(6 × 1.15e-5 × 0.0052 / 0.29) cm = 11 µm instead of 71 µm (calculated). The two examples cannot
both be right. Example 2's convention is the correct one.

**Consequences (all CALCULATED by me):**

- Harvey's calculated threshold, corrected, is **1.53e-5 atm** (about 0.012 mmHg).
- Against Harvey's observed ~0.0026 atm, the ratio is **0.0026 / 1.53e-5 ≈ 170**, not 4.3.
- If the whole gap were blamed on D, as Harvey does, the effective D would be about 170 times lower.
  Under the entry's own premise, r_max would then be about 71/√170 ≈ 5.4 µm, not 35 µm.
- The domain note says q and D are uncertain "by a factor that Harvey's own test puts at about 4 for
  D". That rests on the erroneous step.

**Direction of the defect.** Break (3) says the law fails at bacterial scale when it borrows tissue
coefficients. That break does not disappear. The calculated threshold is still below the observed
one, and the mismatch is now much larger. So the qualitative failure stands, but the quoted
magnitude (×4) and its downstream uses do not. The entry also presents Harvey's "envelope"
explanation as plausible. A 170-fold permeability deficit is a much stronger requirement than a
4-fold one, so other explanations become more relevant: concentration-dependent kinetics, an external
unstirred layer, or the dimming threshold not marking O₂ limitation. Harvey himself flags zero-order
kinetics as "questionable". This last point is my inference.

**Unresolved tension in the observation itself.** This is flagged, not used in the verdict.

- In this paper, Harvey says dimming happens once "at least 99.5 per cent" of the dissolved O₂ has
  been used. For an air-equilibrated start, that means a residual of at most about 0.005 × 0.21 ≈
  1.05e-3 atm (calculated). That figure assumes 0.21 atm initial pO₂, which is my assumption.
- That is lower than the "approximately 0.0026" he quotes for dimming.
- The 0.0026 figure is not derived in the text I read. It may come from Harvey's earlier papers,
  which I did not read.
- So the observed threshold may lie anywhere from ≤1e-3 to 2.6e-3 atm. That gives a ratio of about
  70 to 170 against the corrected calculation. Neither end is near 4.

## 4. Other probes (no defect found)

- **Proxy.** The entry keeps the surface-flux limit and Harvey's internal-diffusion limit apart, and
  says which one binds first. No proxy substitution found.
- **Evidence labels.** Example 2 is labelled "derived". The Thiomargarita sizes are labelled
  secondary. Gehr is labelled abstract-read. These look honest. The one mislabel is example 1:
  "reproduced" certifies the arithmetic, not the physics.
- **Missed regimes.** The entry's own search scope admits gaps in Bergmann heat exchange, spheroid
  necrotic cores and fish gill allometry. Fish gill area is the regime most relevant to this repo,
  and it would be a further convection escape. I did not search it, so this is a scope note, not a
  finding.

## Sources

| Source | Read-level |
|---|---|
| Harvey EN (1928) J Gen Physiol 11:469–475, doi:10.1085/jgp.11.5.469 (PMC2141004) | full-text (Europe PMC XML, OCR) |
| Krogh A (1919) J Physiol 52:391 | could-not-access (not attempted). The K = D·α meaning comes from Harvey's quoted definition. |
| The entry `library/laws/surface-area-volume.yaml` at `1bec71d6` | full-text |

```swarm-challenge
{"claim_id": 57, "outcome": "weakened", "reason": "The entry was dispatched, gated and built, but its Harvey worked example copies a solubility double-count (Krogh's K already contains alpha) and contradicts the entry's own K=D*alpha convention; corrected, the calculated-vs-observed O2 gap is about 170x, not the 4x on which break (3) and the domain note rest.", "corrected_value": "calculated threshold 1.53e-5 atm (not 6.0e-4 atm); calculated/observed gap ~170x vs ~0.0026 atm (range ~70-170x if the 99.5%-consumption residual is used)", "depends_on": ["commit 1bec71d6 on origin/claude/surface-area-volume-law-ngz1e7 and its Claude-Session trailer", "Harvey 1928 full text (Europe PMC OCR): definition of D per atm gradient, Co stated in atmospheres, division by 0.0255", "Krogh's constant K equals D times solubility (as defined by Harvey's quoted units)", "partial-pressure continuity across the cell surface", "Harvey's observed dimming value ~0.0026 atm and his 'at least 99.5 per cent' consumption statement", "check_laws.py and build_pages.py output at 1bec71d6"]}
```
