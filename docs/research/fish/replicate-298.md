# Replicate-298: independent re-derivation of S5-D-D (Fish 1990 AR convention → single-fin bars)

**Date:** 2026-11-04. **Status:** desk calculation. No experiment was run. Every number below is labelled
**quoted** (from a source, with a read-level), **search-summary** (from a search tool's summary, never
opened), **assumed**, or **calculated** (by [`replicate-298_calc.py`](replicate-298_calc.py), run with
`python3 -I replicate-298_calc.py`).

## Independence statement

- The harvest branch `claude/s5-d-sensitive-input-ol0bzg` named as the input context contains only one
  commit, and that commit **is** the S5-D-D derivation (`docs/research/fish/S5-D-deepen.md`). I saw its
  commit message, which repeats the question. **I stopped there and did not open the file** until §5.
- I also did not open `claude/challenge-298-fish-planform-szaskg`, which is probably an earlier challenge
  of this claim.
- Before deriving, I read only S5-D itself (`claude/deepen-s5-pectoral-fin-ajxurw`, `S5-deepen.md`). That
  note sets the thresholds being converted (A0 ≥ 3.0 / 9.0) and the measurement protocol (one fin; span
  measured base to farthest tip perpendicular to the base; area as a polygon). I also read the repo
  source card for Fish 1990 and the primary PDF.

## 1. Primary source: what Fish 1990 actually computed

**Fish FE 1990**, *J Zool Lond* 221:391–403. Read-level: **full-text**. I fetched the author-hosted PDF
(`health-sciences.wcupa.edu/.../1990JZWing design.pdf`, 13 pp, sha256 `1efed334…f8ea`) and extracted it
with pdftotext.

Methods, quoted:
- *"Wing area was defined as the combined areas of the pectoral and pelvic fins continuous through the
  body"*
- *"only one pectoral and pelvic fin per specimen was measured … Areas were doubled to compute the total
  areas for each type of fin."*
- *"Total wing area was equal to the sum of the areas of the pectoral and pelvic fins and the rectangles of
  the intervening body segments. Wing span of the pectoral fins represented the sum of twice the distance
  from the fin base to tip plus the body width"*
- AR *"is calculated as the wing span squared divided by the wing area"*

Results p.395, quoted: *"The aspect ratios (AR) of individual flying fish pectoral fins range from 3.0 to
16.9"*. Table III gives Cypselurus 3.0–12.2 and Exocoetus 8.9–19.9.

**Inference (mine):** "individual" refers to individual fish. The Methods define AR as a whole-wing
quantity:

`AR_F = b² / S`, with `b = 2l + w` and `S = 2A_pect + 2A_pelv + body rectangles`.

As a check, Table I's span and area fits reproduce Table III's AR to within about 3 % for Cypselurus at
0.1 kg (calculated: 8.47 against 8.74).

**Disagreement preserved:** the repo card `P-AR-PECTORAL-RANGE` (`data/research/flying-fish-source-cards.json`
on `origin/main`) reads Fish's AR as *"(pectoral span)² / (pectoral fin area)"*. Fish's Methods, as quoted
above, contradict that reading. The card's own meta note says the denominators differ.

## 2. Conversion to S5-D's single-fin quantity

S5-D's protocol measures `AR_1 = l² / A_pect` on one fin. Its sector model, AR = 2/θ, is the same
single-fin quantity. The conversion factor follows by algebra:

`R = AR_F / AR_1 = (2l+w)² A_pect / (l² S) = 2 · P · (b/2l)²`, with `P = 2A_pect / S`.

### Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| P, Cypselurus | 0.7599 | Fish 1990 Table IV, "percentage of wing area composed of pectoral fins" | full-text |
| P, Exocoetus | 0.9183 | Fish 1990 Table IV | full-text |
| b/SL | span = a·M^b and SL = a·M^b, r.m.a. fits | Fish 1990 Table I: Cypselurus span 0.651, 0.375; SL 0.460, 0.355. Exocoetus span 0.774, 0.380; SL 0.462, 0.347 | full-text |
| Fish AR fit | Cypselurus 12.717·M^0.163; Exocoetus 23.410·M^0.195 (r not significant) | Fish 1990 Table III | full-text |
| l/SL, Cypselurus | 0.606–0.714 | "1.4–1.65 in SL", Shakhovskoy & Parin, Zootaxa (Plazi treatment), via a search summary. Not opened | search-summary |
| l/SL, Exocoetus volitans | 0.732–0.771 | "73.2–77.1 % SL", FishBase / Fishes of Texas, via a search summary. fishesoftexas.org is outside the network allowlist | search-summary |
| Evaluation masses | Cypselurus 0.003–0.3 kg; Exocoetus 0.01–0.1 kg; "typical adult" 0.1 kg | assumed, inside Fish's 0.003–0.53 kg sample |
| Floor w ≥ 0 | applied where the taxonomic l exceeds Fish's b/2 | assumed (physical) |

I did **not** take body width w from any source; none was found. Instead w is bounded by
`w = b − 2l`, using Fish's span and the taxonomic fin-length range. This bound is only as good as two
search-summary inputs, and it assumes that the taxonomic "pectoral fin length" equals Fish's "fin base to
tip". The resulting w/SL is 0 to 0.17 for Cypselurus and 0 to 0.09 for Exocoetus (calculated).

I read Table IV's P as the fins-only share. If it instead includes the pectoral body rectangle, the true
2A_pect/S is a few percent lower, which would lower R. The size of that correction is **unknown**.

### Arithmetic

Cypselurus at M = 0.1 kg (calculated):
- b/SL = 0.651·0.1^0.375 / (0.460·0.1^0.355) = 0.2745 / 0.2032 = 1.352.
- With l/SL = 0.606: (b/2l)² = (1.352/1.212)² = 1.243, so R = 2 × 0.7599 × 1.243 = **1.89**.
- With l/SL = 0.714: b/2l < 1, the floor applies, so R = 2 × 0.7599 = **1.52**.

Over the full grid of masses and fin lengths (calculated):

| Genus | R = AR_F / AR_1 |
|---|---|
| Cypselurus | **1.52–1.97** |
| Exocoetus | **1.84–2.07** |
| Pooled | **1.5–2.1** |

### Bars

**Bar 1: Fish envelope low end, AR_F = 3.0.** Table III puts that minimum in Cypselurus, so the
Cypselurus R applies:
- A0 ≥ 3.0/1.97 to 3.0/1.52 = **1.52–1.97** (calculated).
- Using the pooled R instead gives 1.45–1.97.

**Bar 2: typical genus planform at 0.1 kg** (calculated):

| Genus | AR_F from Table I | AR_F from Table III | Single-fin AR_1 |
|---|---|---|---|
| Cypselurus | 8.47 | 8.74 | 8.47/1.97 to 8.74/1.52 = **4.3–5.7** |
| Exocoetus | 12.47 | 14.94 | 12.47/2.07 to 14.94/1.84 = **6.0–8.1** |

**Park & Choi 2010, AR 9.0–10.7 (S5-D's second bar).** I could not access the full text: the JEB PDF
returned 403, typeset.io does not resolve, and the monash IUTAM mirror was refused by the proxy. Europe
PMC has the abstract only, which gives no AR definition. **The convention of their AR is unknown.**
- If it matches Fish's convention, 9.0 converts to 4.6–5.9 single-fin (calculated).
- If it is already single-fin, the bar stays at 9.0.

## 3. My value

- **Conversion factor:** Fish-1990 AR ÷ single-fin span²/area = **1.5–2.1** (dimensionless; calculated;
  Cypselurus 1.52–1.97, Exocoetus 1.84–2.07).
- **Bars on A0** (calculated):
  - **≥ 1.5–2.0** to enter Fish's envelope;
  - **≥ 4.3–5.7** for a typical 0.1 kg Cypselurus planform;
  - **≥ 6.0–8.1** for Exocoetus.
- **Uncertainty:** dominated by the unknown body width w, which I bounded via search-summary fin lengths,
  and by the reading of Table IV.

**S5-D's qualitative conclusion is unaffected:** A0 is still unknown, and the dilated planform is still
the answer's structure. The thresholds do fall by roughly 2×.

## 4. Negative-search scope

- Body width of Exocoetidae: 2 standard web searches.
- Not reached (outside the allowlist): fishesoftexas.org, www.cambridge.org (Davenport 1992), typeset.io.
- The Shakhovskoy & Parin Zootaxa tables were not opened.
- No primary source giving w/SL for either genus was read.

## 5. Comparison with the recorded value, done only after §1–4

The recorded S5-D-D note is `S5-D-deepen.md` on `claude/s5-d-sensitive-input-ol0bzg`. I read it only
after finishing §1–4. It reports:
- k = 2.03 (Cypselurus) and 2.64 (Exocoetus);
- bars 1.14–1.48 (Fish envelope), 4.30 (Cypselurus) and 5.66 (Exocoetus).

**Where we agree:**
- The Cypselurus factor: 2.03 recorded against my upper end of 1.97.
- The Cypselurus single-fin planform: 4.30 recorded against my 4.3–5.7.
- The conclusion that S5-D stands.

**Where we disagree:**

1. **The Exocoetus factor (2.64).** My inference is that the record divides the Table III AR at 0.1 kg
   (14.94) by a single-fin AR built from the Table I span and area fits (implied 5.66). The Table III fit
   is 1.20× the Table I value at that mass, and Fish flags that regression as non-significant (r = 0.211).
   Using one source for both, the recorded inputs give about 2.2. My bound on w (≤ 0.09 SL) gives ≤ 2.07.
   The record's w (0.0279 m, about 0.13 SL) is a **design assumption** taken from project JSONs, not a
   measurement.
2. **The Fish-envelope bar (1.14–1.48).** The record divides by the Exocoetus k. The 3.0 specimen is a
   Cypselurus (Table III), so only the Cypselurus factor applies. That gives about 1.5 on the record's own
   numbers, and 1.5–2.0 on mine.
3. **Source access.** The record lists Fish 1990 as could-not-access. I read it in full text. Its Methods
   confirm the whole-wing convention on which the record's direction of correction rests.

**Verdict: DISAGREE.**
- The headline factor "2.0–2.6×" and the bar "1.1–1.5" do not replicate. I get 1.5–2.1× and 1.5–2.0.
- The 4.3 (Cypselurus) bar and the qualitative conclusion do replicate.
- I get 6.0–8.1 for the Exocoetus bar, against the record's 5.7.

```swarm-replication
{"claim_id": 298, "my_value": "Fish-1990 AR / single-fin span^2/area = 1.5-2.1 (dimensionless; Cypselurus 1.52-1.97, Exocoetus 1.84-2.07); bars A0 >= 1.5-2.0 (Fish envelope low end 3.0, a Cypselurus) and >= 4.3-5.7 (Cypselurus at 0.1 kg), >= 6.0-8.1 (Exocoetus)", "agrees": false,
  "note": "Fish 1990 full text confirms the whole-wing convention and the Cypselurus bar of about 4.3 replicates, but the 2.0-2.6x factor and the 1.1-1.5 envelope bar do not: the 2.64 Exocoetus factor mixes the Table III and Table I fits and is applied to a Cypselurus-set minimum, and my independent bound gives 1.5-2.1x and A0 >= 1.5-2.0."}
```
