# Challenge 178: [S6-D] passive lepidotrichial ray cannot carry glide lift

**Verdict: WEAKENED.** The arithmetic is right. The conclusion that the passive-ray mechanism falls
is not supported. Every stiffness in the claim comes from a bluegill or labrid ray, and none is
scaled to the size of a flying-fish ray. Under isometric scaling, the gap the claim reports is
about the size that a ~3.6x difference in ray length would close. The right status is
**indeterminate (untested)**, not *falls*.

Reviewer: adversarial challenge. No experiment was run. Every number below is either relayed from
a source (with its read-level) or **calculated** by me, and each sentence says which.

## Sources and read-levels

| Source | What I used | Read-level |
|---|---|---|
| Flammang, Alben, Madden & Lauder 2013, *J. Morphol.* 274:1044–1059 | Abstract sentence "Flexural stiffness of the fin ray was calculated to be 565 × 10⁻⁶ N m²". The ray is the bluegill pectoral ray 3, chosen because it is the longest. | search-summary. The full text (sites.harvard.edu) and the record (deepblue.lib.umich.edu) both failed DNS in this session (could-not-access). |
| Puri et al. 2018 (relaying Flammang 2013 as 3.8e-6 N m²) | Only the value as the claim states it | could-not-access. I did not find or read it, so this value is taken from the claim. |
| Aiello et al. 2018, *J. Morphol.* 279:1031–1044 | Labrid range 1e-10 to 1.51e-6 N m², taken from the claim. Search summary: EI falls exponentially from base to tip and from leading edge to trailing edge, and the second moment of area *I* explains most of the variance. | search-summary |
| Alben, Madden & Lauder 2007 (PMC2359861) | The fin-ray mechanism lets the fish vary ray stiffness over more than an order of magnitude | search-summary |
| Flying-fish fin-ray mechanics | **None found.** Scope: two web searches for flying fish / *Cypselurus* / Exocoetidae pectoral fin-ray stiffness, lepidotrichia and bending. Neither returned an Exocoetidae ray-stiffness measurement. | n/a |

## 1. Independent arithmetic (calculated)

The claim does not state its load inputs. I rebuilt them and got the claim's numbers exactly.
The inputs below are **my reconstruction, not the author's stated values**:

- Fish mass 0.1 kg, so glide lift = weight = 0.981 N.
- 28 load-bearing rays (2 fins × 14), each carrying an equal share: F = 0.0350 N per ray.
- Ray length L = 0.12 m.
- Each ray is a uniform-EI cantilever under a uniformly distributed load: δ = F L³ / (8 EI), so δ/L = F L² / (8 EI).
- Pass criterion: δ/L ≤ 0.1.

Results (calculated):

- Required EI = 0.0350 × 0.0144 / 0.8 = **6.31e-4 N m²**. This matches the claim's ~6.3e-4.
- With EI = 3.8e-6, δ/L = 16.6. With EI = 1.51e-6, δ/L = 41.8. These match the claim's "17–42".
- With EI = 565e-6, δ/L = 0.112. This matches "passes only marginally".
- With a tip point load instead (δ = F L³ / 3EI), required EI = 1.68e-3 N m², which is stricter.

The arithmetic is internally consistent. I found no error in it.

**Minor defect:** δ/L of 17 or 42 is outside the range where small-deflection beam theory holds,
because a ray cannot deflect more than its own length. Those figures are linear-theory artifacts.
The shortfall should be stated as a stiffness ratio instead: the required EI is ~166x the
3.8e-6 value and ~420x the 1.51e-6 value (calculated).

## 2. Proxy: the defect that carries the verdict

The quantity that matters is the EI of a **flying-fish** pectoral ray, at flying-fish size. The
claim substitutes rays from bluegill (*Lepomis*) and labrids, which are much smaller fish whose
pectoral rays are much shorter. It never rescales them.

For a beam, EI = E·I, and I scales with cross-sectional size to the fourth power. Under geometric
similarity with ray length ratio k, EI scales as k⁴. Aiello 2018 (search-summary) reports that
variation in I dominates variation in EI, so size, not material, is the main lever.

Break-even length ratios (calculated):

- From 3.8e-6 to 6.3e-4 needs k = (6.31e-4 / 3.8e-6)^(1/4) ≈ **3.6**.
- From 1.51e-6 (the labrid maximum) needs k ≈ **4.5**.
- If k = 4, scaled EI = 3.8e-6 × 256 = 9.7e-4 N m², giving δ/L = 0.065. **That passes.**
- If k = 3, scaled EI = 3.1e-4 N m², giving δ/L = 0.20. That is marginal.

I could not find a sourced length for the bluegill ray that the 3.8e-6 value was measured on, so
**k is unknown**. The search summaries did not give ray length in mm, and I could not open the
full texts. My inference, not a measurement: a 12 cm flying-fish ray compared with a bluegill
pectoral ray of a few centimetres puts k in the ~3–5 range, and that range straddles the
break-even point. So the reported numbers cannot decide pass or fail. The claim's "falls" rests on
an unscaled cross-taxon proxy.

The author does list "or a stiffer flying-fish ray" as one escape route. But the claim then treats
the passive mechanism as refuted. The evidence supports only "bluegill- and labrid-sized rays
would fail", which is not the proposition at issue.

## 3. Hidden assumptions, relaxed (calculated or inferred, as marked)

- **Size scaling** (above). This one carries the result.
- **Uniform EI.** Aiello 2018 (search-summary) reports EI falling exponentially toward the tip.
  It is not stated whether 3.8e-6 is a base, mean or whole-ray value. A stiff base with a flexible
  tip gives tip deflection that cannot be judged from one scalar EI. Direction of the effect:
  unknown.
- **Equal share per ray.** Aiello 2018 reports leading-edge rays as stiffer. Lift carried mainly
  by those stiffer rays would favour the passive mechanism. This is my inference, not tested.
- **δ/L ≤ 0.1 threshold.** This is arbitrary. Relaxing it to 0.3 lowers the required EI 3x, to
  2.1e-4 (calculated).
- **Mass 0.1 kg and L = 0.12 m.** These are my reconstruction and unsourced. A 0.25 kg fish with
  the same L raises δ/L at 3.8e-6 to 41.5 (calculated). But a heavier fish also has longer, thicker
  rays, and under isometry δ/L grows only linearly with size.
- **Membrane and inter-ray load sharing**, and the active stiffening that Alben 2007 reports
  (search-summary: more than an order of magnitude). The claim names this. It is unmeasured in
  flying fish.

## 4. Evidence level

The claim is recorded as **measured**. That is wrong. The required EI of 6.3e-4, the δ/L values
and the pass/fail verdict are all **calculated**, from load inputs that are not stated and from
stiffness values **measured in other taxa** (bluegill, labrids). No flying-fish ray was measured.
The correct level is *calculated (from cross-taxon measured proxies)*. This is a defect even
though the numbers reproduce.

## 5. Source disagreement, preserved

- Flammang 2013 abstract (search-summary): 565 × 10⁻⁶ N m². The PDF text layer garbles the
  exponent as "1026", which reads as 10⁻⁶ with the minus sign mis-encoded. The repository record
  gives 10⁻⁶.
- Puri 2018 relaying Flammang 2013: 3.8e-6 N m² (could-not-access; value taken from the claim).

The two differ ~149x. I could not resolve the discrepancy and do not average it. Note that
565e-6 N m² is far above the whole labrid range (≤1.51e-6). That fits an abstract-level unit or
exponent error, but this is my inference, not verified. Either way, under size scaling the verdict
does not hinge on which value is right.

## 6. Counter-examples

I found no published measurement of flying-fish ray stiffness, so none confirms or refutes the
claim. Search scope is listed in the source table. The absence of data is the finding.

## Corrected statement

On reconstructed inputs, a single passive ray carrying an equal share of glide lift needs
EI ≈ 6.3e-4 N m² (calculated). Raw stiffnesses of bluegill and labrid rays (≤3.8e-6 N m²) fall
~166x short (calculated). But that comparison is across taxa and unscaled. Under isometric
scaling, a length ratio of ≈3.6 closes the gap (calculated), and the actual length ratio is
unknown. The passive-ray mechanism is therefore **untested, not falsified**, until a flying-fish
ray EI (or the measured ray length behind the proxy values) is in hand.

```swarm-challenge
{"claim_id": 178, "outcome": "weakened", "reason": "Arithmetic reproduces (6.31e-4 N m^2 required; delta/L 16.6 and 41.8), but the verdict compares unscaled bluegill/labrid ray EI against a flying-fish-sized ray; since EI scales as length^4, a ray-length ratio of ~3.6 (unknown, plausibly 3-5) closes the gap, so the passive mechanism is untested rather than falsified, and the result is calculated, not measured.", "corrected_value": "required EI ~6.3e-4 N m^2 (calculated, reconstructed inputs: 0.1 kg, 28 rays, L=0.12 m, UDL, delta/L<=0.1); break-even proxy-to-flying-fish ray length ratio ~3.6 (calculated); verdict: indeterminate", "depends_on": ["fish mass 0.1 kg (reconstructed, unsourced)", "28 load-bearing rays with equal share (reconstructed)", "ray length L=0.12 m (reconstructed, unsourced)", "uniform-EI cantilever under distributed load, delta/L<=0.1 criterion", "EI 3.8e-6 N m^2 (Puri 2018 relaying Flammang 2013; could-not-access)", "EI 565e-6 N m^2 (Flammang 2013 abstract; search-summary)", "labrid EI max 1.51e-6 N m^2 and dominance of second moment of area (Aiello 2018; search-summary)", "isometric scaling EI proportional to length^4", "bluegill ray length behind the proxy value: unknown"]}
```
