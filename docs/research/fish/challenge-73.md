# Challenge 73: the Flammang 2013 fin-ray EI disagreement (3.8e-6 vs 565e-6 N·m²)

**Claim under review** (from `docs/research/fish/S6-deepen.md`, branch `claude/deepen-fin-ray-s6-cj2i2x`):

> "DISAGREEMENT PRESERVED: Flammang 2013 fin-ray flexural stiffness is relayed as 3.8e-6 N m^2 by Puri 2018
> and as 565e-6 N m^2 in the Flammang abstract -- the same paper, ~150x apart. The passive-ray verdict
> depends on which is right, and neither was read at full text"

Recorded evidence level: unknown. Value: n/a.

**Verdict: WEAKENED.** The disagreement is real: I re-read both quotes and they check out. Two parts of the
sentence do not hold as worded:
- Under S6's own criterion the passive-ray verdict does **not** flip between the two values. Both values fail.
  Only the margin, and how robust the fail is, changes.
- "Neither was read at full text" is wrong. Puri 2018 *was* read at full text. The unread document is the
  Flammang 2013 body text, and both numbers trace back to it.

No experiment was run. Every number below is labelled as **quoted** (from a source, with its read-level) or
**calculated** (by me, from the stated inputs).

## 1. The two relayings, checked again at source

| Source | What I found | Read-level (mine, this session) |
|---|---|---|
| Flammang, Alben, Madden & Lauder 2013, *J Morphol* 274:1044–1059, doi:10.1002/jmor.20161, PMID 23720195 | Abstract, verbatim: "Flexural stiffness of the fin ray was calculated to be 565 × 10(-6) Nm2." The same abstract says the distal 60% of the ray is segmented and the proximal part is not. | **abstract** (Europe PMC REST API, `resultType=core`) |
| Same paper, body text | Not obtained. I tried the Harvard Lauder-lab PDF (`sites.harvard.edu`) and the Deep Blue record (`deepblue.lib.umich.edu`). Both hosts are blocked by this session's network policy (proxy 403 / DNS refusal). Europe PMC lists no PMC copy (pmcid = None). | **could-not-access** |
| Puri et al. 2018, *J Exp Biol* 221:jeb171777, PMC5868929 | Verbatim: "the bending stiffness of bluegill rays of 3.8×10−6 N m2 would indicate a bending stiffness for a zebrafish fin of between 2×10−9 and 5×10−9 N m2". Earlier in the same paragraph: "Previous measurements of bending stiffness of larger fish have reached a sensitivity of 10−6 N m2 (Flammang et al., 2013)". | **full-text** (Europe PMC `fullTextXML`) |

A web search (standard mode) for `Flammang Alben Madden Lauder 2013 "fin ray" flexural stiffness "3.8"
bluegill` turned up no indexed text with "3.8" attributed to Flammang 2013. That search covered one
general-web query only, so it is weak evidence of absence.

## 2. Arithmetic, redone independently (calculated)

- Ratio: 565e-6 / 3.8e-6 = **148.7**. "~150×" is correct.
- S6's reference scenario. These are S6's assumptions, which I re-used without endorsing them: m = 0.10 kg,
  N = 14 rays, L = 0.12 m, n = 1, failure at δ/L > 0.10.
  - Per-ray load: P = 0.10·9.81/28 = 0.0350 N.
  - Required EI = P·L²/(8·0.10) = **6.31e-4 N·m²**.
  - δ/L at 565e-6 = **0.112**.
  - δ/L at 3.8e-6 = **16.6**.
  - δ/L at 1.51e-6 (Aiello 2018 upper bound) = **41.8**.
  - These match S6. Note that δ/L of 17–42 lies far outside linear beam theory, which cannot give a deflection
    larger than the length. Read those numbers as "fails by orders of magnitude", not as real deflections.
- Equivalent solid-rod diameter at E = 1 GPa: 1.84 mm for 565e-6 and 0.53 mm for 3.8e-6. These match S6.

## 3. Where the claim breaks

### 3a. "The passive-ray verdict depends on which is right" overstates the dependency

At S6's own threshold, 565e-6 gives δ/L = 0.112. **That is a fail (0.112 > 0.10), not a pass.** S6's own
summary calls it "passes only marginally". That wording is wrong in the parent document too.

The hidden assumption that helps 565e-6 is a **uniform** EI along the whole ray. The Flammang abstract itself
says the distal 60% is segmented. Under normal swimming, its curvature reached 0.065 mm⁻¹ against 0.029 mm⁻¹
proximally (quoted, abstract). That is a hint that the distal part is more compliant. Curvature ratio is a
proxy for the stiffness ratio, not the stiffness ratio itself.

So I relaxed the assumption (calculated). I used a two-segment cantilever under uniform load, with EI₀ over
the proximal 40% and EI₀/k over the distal 60%. Tip deflection scales by (1 − 0.6⁴) + 0.6⁴·k:

| k (distal softening) | deflection factor | δ/L at EI₀ = 565e-6 |
|---|---|---|
| 1 (S6's uniform beam) | 1.00 | 0.112 |
| 2 | 1.13 | 0.126 |
| 2.24 (curvature ratio used as a proxy) | 1.16 | 0.130 |
| 10 | 2.17 | 0.242 |
| 100 | 13.8 | 1.54 |

This assumes 565e-6 describes the stiffer proximal ray, which is my assumption. On that reading, relaxing the
uniform-beam assumption moves the 565e-6 case **further into failure**. It does not rescue it.

**My inference:** under S6's stated scenario, both values give "fails". The value does change something real.
With 3.8e-6 the fail is robust: 166× short, and no plausible change in m, N, L or the threshold closes it. With
565e-6 the fail is 12–140% short. That is inside the uncertainty of S6's four unmeasured scenario inputs, so
the verdict becomes *indeterminate*, not *passes*. The accurate statement is: "the **robustness** of the
passive-ray fail depends on which is right". The verdict itself does not flip.

### 3b. "Neither was read at full text" is wrong as worded

S6 itself records Puri 2018 as **full-text**, and I read it at full text in this session. What nobody has read
is the Flammang 2013 body text. Both numbers trace back to that single unread source. The defect matters
because "neither was read" implies the Puri relaying is as uncertain as the abstract. It is not. Puri's
sentence is verified, and only its fidelity to Flammang is unverified.

### 3c. One piece of evidence the claim did not use (my inference, not either author's claim)

Puri's downstream arithmetic depends on 3.8e-6. They expect zebrafish rays to be ">four orders of magnitude"
more flexible, and use 16–18 rays per fin. At exactly 10⁴, 3.8e-6 gives 6.1–6.8e-9 N·m² per fin
(calculated), which is close to their stated 2–5e-9 and to their in-vivo measurement. 565e-6 would give
~0.9–1.0e-6 N·m² (calculated), about 200× off, and they could not then have reported "reasonable agreement".

So 3.8e-6 is not a transcription slip in Puri's own text: their conclusion was built on it. Their phrase "a
sensitivity of 10−6 N m2" also reads more naturally beside a value of a few ×10⁻⁶ than beside 5.65×10⁻⁴.

This tips the balance weakly toward 3.8e-6 being a value that appears in Flammang's body text. It does **not**
settle what Flammang wrote. The two numbers could describe different things, for example a three-point-bending
measurement and a value derived from the vortex-impact analysis. The abstract calls the 565e-6 figure
"calculated", which fits that reading. I am not adopting either number.

## 4. Other checks

- **Proxy:** both numbers are for bluegill (*Lepomis macrochirus*) pectoral rays loaded in water. The quantity
  that matters for S6 is the EI of an exocoetid pectoral ray. S6 already flags this, and its Europe PMC search
  (35 hits, Europe PMC only) found no exocoetid ray EI. I did not repeat that search.
- **Evidence level:** "unknown, value n/a" is honest for a disagreement claim. One addition: by the authors'
  own word, the 565e-6 value is *calculated*. It is not a direct measurement, so neither number should be
  carried forward as "measured".
- **Counter-example regime:** the claim omits nothing beyond the uniform-EI assumption covered in 3a.

## 5. Corrected statement

> Flammang et al. 2013 is relayed as 3.8e-6 N·m² by Puri 2018 (full-text; the number also carries Puri's own
> zebrafish comparison) and as 565e-6 N·m² ("calculated") in the Flammang abstract. The two are ~149× apart,
> and the Flammang body text was not read. Under S6's assumed scenario both values fail the δ/L ≤ 0.10
> criterion: 565e-6 gives 0.112 for a uniform beam, and more once the segmented distal 60% is allowed to be
> softer. The value decides only whether the fail is robust (3.8e-6, 166× short) or within the uncertainty of
> the scenario assumptions (565e-6).

## Sources

| Source | Read-level |
|---|---|
| Flammang BE, Alben S, Madden PGA, Lauder GV (2013) *J Morphol* 274:1044–1059, doi:10.1002/jmor.20161 | abstract; body text could-not-access (sites.harvard.edu and deepblue.lib.umich.edu blocked by network policy) |
| Puri S et al. (2018) *J Exp Biol* 221:jeb171777, PMC5868929 | full-text |
| `S6-deepen.md` (branch `claude/deepen-fin-ray-s6-cj2i2x`): scenario inputs and the Aiello 2018 range | full-text (repository document); its own sources were not re-read, apart from the two above |

```swarm-challenge
{"claim_id": 73, "outcome": "weakened", "reason": "Both relayed values and the ~149x gap are confirmed at source, but under S6's own delta/L<=0.10 criterion both values fail (565e-6 gives 0.112, worse once the segmented distal ray is softer), so only the robustness of the passive-ray verdict depends on which is right, and Puri 2018 was in fact read at full text: only the Flammang body text is unread.", "corrected_value": null, "depends_on": ["Flammang et al. 2013 abstract: 565e-6 N m^2, 'calculated' (abstract, Europe PMC)", "Puri et al. 2018 full text: 3.8e-6 N m^2 citing Flammang 2013 (full-text, PMC5868929)", "S6-deepen reference scenario assumptions: m=0.10 kg, N=14, L=0.12 m, n=1, delta/L<=0.10", "Uniform-load Euler-Bernoulli cantilever model", "Flammang 2013 abstract: distal 60% of ray segmented, curvatures 0.065 vs 0.029 mm^-1 (abstract)", "Assumption (mine): 565e-6 describes the proximal unsegmented ray"]}
```
