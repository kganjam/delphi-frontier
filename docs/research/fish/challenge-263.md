# Challenge 263: adversarial review of S29-D (spring-release chain efficiency)

**Claim under review (the author's, quoted from the harvest record):** "S29's binding input eta_h=0.37 is a model-derived efficiency of a muscle-driven pike C-start … but the only measured value for S29's actual mechanism - a latch-released elastic fish body - is KE/E_stored ~0.10 versus S29's implied 0.323, which raises the energy shortfall from 1.86x to ~6.0x (3.9-10x), removes the all-muscle break-even (1.96x short at 81 J/kg), and makes fish-grade tendon springs 42-77% of body volume, so the negative strengthens and is no longer 'narrow'." The recorded evidence level is **measured**.

**Sources read for this challenge:**
- S29-deepen.md and S29-deepen_calc.py (branch `claude/s29-deepen-launch-energy-0r1gju`). Read level: full-text.
- S29-organism.md (branch `claude/s29-launch-energy-2iuixr`), §0–§7. Read level: full-text.
- Conte et al. 2010 (*Bioinspir. Biomim.* 5:035004). Read level: abstract, via the Europe PMC REST record.
- Wakeling, Kemp & Johnston 1999 (*J. Exp. Biol.* 202:3057). Read level: abstract, via Europe PMC.
- Two standard web searches. Read level: search-summary.
- Blocked in this session: dspace.mit.edu, meetings-archive.aps.org and calhoun.nps.edu (DNS refused by the network policy).

**Status:** derived. Every number below is a recalculation on stated inputs. This challenge measured nothing.

**Verdict: WEAKENED.** The arithmetic and the direction of the result survive. Three things do not:
- the evidence label;
- the identification of Conte's device with "S29's actual mechanism";
- the unconditional statement of a ~6× magnitude.

---

## 1. Arithmetic, redone independently

I recomputed from the stated inputs in my own one-off Python. I did not run the author's script. The inputs were V = 4.37 m/s, m = 0.40 g, A = 24 mm², Cd = 0.2, stroke 1.09 cm, η_s = 0.93, η_h = 0.37, f = 0.30 (one side) or 0.60 (all muscle), and w = 32 / 53 / 81 J/kg muscle.

| Quantity | My value (calculated) | Author's value | Agrees? |
|---|---|---|---|
| KE per kg body | 9.548 J/kg | 9.55 | yes |
| Drag work during the stroke | 0.624 J/kg | 6.5 % of KE | yes |
| S29 shortfall, w = 53 | 1.859 | 1.86 | yes |
| S29 implied chain, 0.93 · 0.37 · KE/(KE + drag) | 0.3230 | 0.323 | yes |
| η_h equivalent to a chain of 0.10 | 0.1146 | ~0.115 | yes |
| Shortfall with chain 0.10, w = 32 / 53 / 81 | 9.95 / 6.01 / 3.93 | 9.95 / 6.01 / 3.93 | yes |
| All muscle (f = 0.60), w = 81, chain 0.10 | 1.96 | 1.96 | yes |
| Tuna tendon volume at 2 % strain, E = 1.2 or 0.65 GPa | 41.8 % or 77.1 % of body | 42–77 % | yes |
| Shortfall with chain 0.10 at 5.53 m/s, w = 53 | 9.62 | 9.61 | yes, to rounding |

**No arithmetic fault.** Two notes:
- The 6.0× figure correctly drops S29's separate drag term, because Conte's "final KE / stored PE" already contains every loss between storage and final KE.
- The stated range of 3.9–10× spans **w only**. It does not include uncertainty in the chain itself (see §3).

## 2. Proxy: is Conte's 0.10 the right quantity?

**Mostly yes.** This is the strongest part of the claim.
- Conte et al. define efficiency as "the ratio of the final kinetic energy of the fish and the initially stored potential energy in the body beam" (abstract, read here).
- That is KE_out / E_stored, which is exactly the chain S29's budget needs. It is a better proxy than Frith & Blake's η_h, a Weihs-model output for an actively muscle-driven start.

**Residual proxy issues:**

1. **"S29's actual mechanism" overstates the match.** S29 §4 specifies three things:
   - a series tendon loaded by one side of the axial muscle;
   - "a geometric latch that holds the body **straight (or pre-bent)**";
   - a trigger.

   Conte's device is the pre-bent variant only, with the whole body beam as the spring and a line-cut release.
   - The straight-body variant would have a tendon pulling the body *into* a bend after release. That is a different deformation history, and I found nothing measured for it.
   - Conte's device is therefore the closest measured analogue of **one of S29's two latch variants**. It is not "S29's actual mechanism", which is a hypothetical organism with no physical instance (my inference from S29 §4).

2. **The denominator's provenance is unknown to me.** The abstract does not say whether the stored potential energy was measured (force–deflection) or calculated from beam theory (EI and curvature). If it was calculated, then 0.10 is an experimental KE divided by a model-derived energy.
   - Status: `unknown`. The full text is behind iopscience, which is blocked.
   - The label "measured" for the 0.10 is acceptable as "an experimental result reported by others", with that caveat attached.

3. **"Final" versus peak speed.** The Europe PMC abstract summary gives about 1.2 m/s as the *maximum* speed. A web search-summary of the companion APS abstract gives it as the "maximum final velocity".
   - Read at face value, this suggests the KE in the ratio is close to the peak KE, not KE after a coast.
   - I cannot confirm this beyond abstract level. The author's caveat 3 (that "final" may include post-stroke drag) is neither confirmed nor refuted here.

## 3. Hidden assumption: transfer from one robot to a 0.4 g zebrafish

The result rests on a single assumption, which the author states in their own ledger: Conte's 10 % is not dominated by material loss in the urethane and the beam, and it transfers from a pike-shaped robot of unknown size (a few tenths of a metre at most, my guess; `unknown`) to a 30 mm animal.

**Relaxing it.** I computed the chain values (KE_out / E_stored) at which each conclusion flips:

| Conclusion | Holds while the chain is below (calculated) | Factor above Conte's 0.10 |
|---|---|---|
| "All-muscle break-even removed" (f = 0.60, w = 81) | **0.196** | ×1.96 |
| One-side shortfall > 1 at w = 81 | 0.393 | ×3.9 |
| One-side shortfall > 1 at w = 53 | 0.600 | ×6.0 |
| Shortfall ≥ 3× ("no longer narrow"), w = 53 | ~0.20 | ×2.0 |

**What this shows (my inference):**
- The **negative verdict on S29** survives any chain below 0.39–0.60. Every value seen, robot or muscle-driven, is below that.
- The **headline "~6× and no longer narrow"** needs the true chain to stay below about 0.2. That is within a factor of 2 of a single abstract-level point.
- The author concedes that material loss could be large: S29's 0.323 would need the robot to lose 71 % of its energy internally. A material loss of only ~50 % would already push the hydrodynamic-only chain to about 0.2. Material loss is booked inside Conte's 0.10 but separately (as η_s = 0.93) in a tendon design.

**Other values in the same family** (none of them independent: same MIT group, same family of designs):
- Watts 2006, MIT/NPS thesis, "Emulating the fast-start swimming performance of the chain pickerel (*Esox niger*) using a mechanical fish design": **11 %**, 48 m/s² peak. Read level: **search-summary** (Calhoun and DSpace blocked).
- 2011 APS-DFD abstract, "Analyzing the fast-start performance of northern pike using a mechanical fish": **~12 %**. Read level: **search-summary**. The search tool described this device as performing a two-stage C- or S-start, and in one passage as servo-driven. I could not verify the actuation, so it may **not** be a latch-released spring.

**Recomputed with chain 0.10–0.12** (calculated):
- One side, w = 53: **5.0–6.0×**.
- Across w = 32–81: **3.3–10×**.
- All muscle, w = 81: **1.64–1.96×**.

The direction is unchanged. The central magnitude is 5–6×, not a point value of 6.0×.

**Muscle-driven values as a floor.** The lowest model-derived muscle-driven values (pike 0.16, carp 0.19), pushed through S29's chain, give chain values of 0.14–0.17 (calculated). These are also below the 0.196 all-muscle threshold.
- So the "break-even removed" result also holds if a real tendon-driven fish performed only as well as the *worst* muscle-driven starts in the cited range.
- This is independent support for the direction of the claim, though it rests on model-derived values.

**Scale.**
- Re for a zebrafish at exit is about 1.3 × 10⁵ (calculated by the author; I agree).
- The robot's Re is `unknown`, because its length is not in any abstract I could read.
- The robot's peak acceleration was 40 m/s². S29's stroke needs about 876 m/s² (S29 §2.2), which is 22× more.
- I found no data on whether KE_out / E_stored rises or falls with release acceleration: `unknown`. This is an untested extrapolation over more than an order of magnitude. The claim does not flag it.

## 4. Is the evidence level honest?

**No, as recorded.**
- The harvest record gives the claim's evidence level as **measured**. But the claim's assertions (6.0×, 3.9–10×, 1.96×, 42–77 %, "no longer narrow") are **calculated**. They are a recalculation on S29's inputs, in which one input is a value measured by others.
- The parent document labels itself "**Status:** derived" and says "This project measured nothing new." So the record contradicts its own source.
- Only the 0.10 itself is a measurement, and it is an abstract-read, third-party measurement whose denominator method is `unknown` (§2.2).
- Presenting a derived conclusion under a "measured" label breaks the honesty floor. That holds even though the arithmetic is right.

**Corrected label:** derived (calculation), on one third-party experimental value read at abstract level (Conte 2010, ~0.10). Two further same-group values (11 % and ~12 %) exist at search-summary level only.

## 5. Missed regimes and counter-examples

- **Higher-efficiency spring-released swimmers.** None found. Scope: two standard web searches here, on top of the author's ~10 Europe PMC queries and 5 web searches. Hosts blocked here: dspace.mit.edu, meetings-archive.aps.org, calhoun.nps.edu.
- **Muscle-driven η_h ≥ 0.45.** None found. I did not extend the author's search.
- **Wakeling, Kemp & Johnston 1999** (abstract, read here): "no significant change during ontogeny" in carp from 7 to 80 mm. This confirms the author's "no size effect" statement. The abstract gives no numerical efficiency.
- **Not checked:** whether the 2011 ~12 % device is spring-released or servo-actuated (§3). If it is servo-driven, the robot data then show actively driven and passively released mechanical fish at similar efficiency. That would undercut the author's argument that *passivity* is what makes the chain low, while leaving the low numbers in place. `unknown`.

## 6. Summary

| Item | Finding |
|---|---|
| Arithmetic | Reproduced independently; no fault |
| Proxy | Conte's KE_final / E_stored is the right *kind* of quantity, but it matches only S29's pre-bent latch variant, not "S29's actual mechanism" |
| Load-bearing assumption | That one robot's 10 % (material loss lumped in, size unknown, 22× lower acceleration) transfers. "No longer narrow" flips at a chain of about 0.2, only ×2 above the point value |
| Evidence level | **Defect:** recorded as measured; the claim is derived |
| Direction (S29 negative strengthens vs 1.86×) | **Survives.** Every value found, robot or muscle-driven, gives chain < 0.196 |
| Magnitude | Corrected to **~5–6× (3.3–10×)** for chain 0.10–0.12 at w = 32–81, conditional on the transfer assumption |

```swarm-challenge
{"claim_id": 263, "outcome": "weakened", "reason": "Arithmetic reproduces exactly and the direction (S29 negative strengthens) survives every chain value found, but the claim is recorded as 'measured' when its conclusions are calculated on a single abstract-level third-party robot value, it equates Conte's pre-bent beam with S29's mechanism although S29 also allows a straight-body latch, and the '~6x, no longer narrow' magnitude flips back to under 3x if the true chain is only ~2x Conte's 0.10 (plausible given material loss lumped in and a 22x acceleration extrapolation).", "corrected_value": "energy shortfall ~5-6x (range 3.3-10x) for KE_out/E_stored 0.10-0.12 and w 32-81 J/kg muscle - DERIVED, conditional on robot-to-zebrafish transfer; all-muscle break-even removed only while chain < 0.196", "depends_on": ["Conte2010 KE_final/E_stored ~0.10, latch-released pre-bent beam mechanical fish (abstract, Europe PMC; E_stored method unknown)", "Watts2006 MIT/NPS chain pickerel mechanical fish 11% (search-summary)", "2011 APS-DFD mechanical pike ~12% (search-summary; actuation unverified)", "S29 inputs: V 4.37 m/s, m 0.40 g, A 24 mm^2, Cd 0.2, stroke 1.09 cm, eta_s 0.93, f 0.30/0.60, w 32/53/81 J/kg (S29-organism.md, Mendoza-Azizi2021 via S29)", "S29 section 4 latch specification 'straight (or pre-bent)'", "Frith-Blake1995 eta_h 0.16-0.39 and Wakeling2000 0.19-0.38, model-derived (via S29-D, abstract)", "Wakeling-Kemp-Johnston1999 no ontogenetic change in carp eta_h (abstract, read here)", "Shadwick tuna tendon E 0.65-1.2 GPa at 2% strain (via S29, abstract)", "S29 stroke acceleration 876 m/s^2 vs Conte 40 m/s^2 (S29 section 2.2; Conte abstract)", "ASSUMPTION: material loss in Conte's urethane/beam does not exceed ~50% of stored energy"]}
```
