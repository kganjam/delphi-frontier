# Replicate 169 — S20-D "guppy-class" comparator, rebuilt from the primary guppy paper

**Claim:** [S20-D-D] S20-D's most flip-prone input is its "guppy-class" comparator (1.51 m/s, from a
review's "3.5 BL" × the 33 mm zebrafish length under an unstated size-invariance). This file rebuilds
that comparator from the primary guppy measurements (Soares & Bierman 2013).

**Independence note:** I searched this repository for the earlier derivation and found none. `git grep -i`
for `guppy`, `soares` and `s20-d` across every remote branch (`claude/s20-d-guppy-comparator-8bxzcv`,
`work/frontier-foundation`) returned no hits. The harvest tag `harvest:s20-d-sensitive-input-77m8c9` does not
resolve to anything in this checkout. So I did not see the earlier working. I also cannot see the
recorded *rebuilt* value. The only earlier number I have is the 1.51 m/s quoted in the question.

## Source

| Source | What it supplies | Read-level |
|---|---|---|
| Soares D, Bierman HS (2013). *Aerial jumping in the Trinidadian guppy (Poecilia reticulata).* PLoS ONE 8(4): e61617. doi:10.1371/journal.pone.0061617 (journals.plos.org HTML and PMC3629028) | Table 1 and the Results/Discussion text quoted below | **full-text** (HTML fetched; the Results and Discussion strings below were checked verbatim against the PLOS page) |
| The "review" that S20-D took 3.5 BL from | — | **could-not-access**: I don't have its identity. I did not look it up, so that I would stay independent of the earlier derivation. |

### Primary values (author's measurements, quoted)

- Fish standard length: **1.85 ± 0.35 cm** (Table 1). The same table gives the fish weight as "98±10 gm". That cannot
  be right for a 1.85 cm guppy. It is probably mg, but that is my inference; the paper prints gm.
- Sample: 20 jumps by 5 males (set-up 1) and 22 jumps by 4 other fish (set-up 2). Video at 1000 fps. Values are mean ± s.d.
  The authors do not say whether the s.d. is taken over jumps or over fish. Jumps are nested within fish, so the
  effective n is about 9 fish, not 42 jumps.
- Jump **height**: "6.54±1.92 cm (**3.52±0.96 body lengths**)".
- "In water, maximum velocities (**102.36±33.75 cm/sec**) were observed right before or at the moment the fishes'
  head broke the water/air interface."
- Peak velocity in air: **123.57 ± 30.0 cm/sec**.
- Discussion, same paper, inconsistent with the Results: "the fastest speed we recorded in water was **100.16±33.9 cm/sec**, and in
  the air ... 123±30.0 cm/sec." I keep both water figures and do not reconcile them. They differ by 2%.
- Discussion: "The burst speed, achieved with a C-start in animals of the same species and length, is **about 70 to
  80 cm/sec** (extrapolated from [45] and this study)." This is the **authors' extrapolation, not a measurement**.
- Example jump (Fig. 2): 128 cm/s in water and 150 cm/s in air. These are single observations.

## Key finding on the "3.5 BL" input

The only "3.5 body lengths" in the primary paper is the **jump height**, 3.52 ± 0.96 BL. It checks out:
6.54 cm / 1.85 cm = 3.54. The paper does **not** report any speed in body lengths per second. *My inference,
not the authors' claim:* if the review's "3.5 BL" came from this paper, it is a height. Multiplying it by
33 mm gives a length, 3.5 × 0.033 m = 0.116 m, not a speed. I cannot reconstruct how 1.51 m/s was obtained
from it without the review. I record that step as **unknown**.

## Rebuilt comparator (calculated from observed means; not itself an observation)

**A. Absolute, no size-scaling (recommended):** guppy peak in-water velocity = 102.36 ± 33.75 cm/s
→ **1.02 ± 0.34 m/s** (s.d.; Discussion variant 1.00 ± 0.34 m/s). This is the observed guppy number, with no
size assumption added. It describes a 1.85 cm fish **jumping**, which is not the same as a free-swimming escape.

**B. BL-normalised, then rescaled to the 33 mm zebrafish.** This uses the same size-invariance assumption the
claim flags, and I show it only so the sensitivity is visible:
- 102.36 cm/s ÷ 1.85 cm = 55.3 BL/s
- 55.3 BL/s × 3.3 cm = 182.6 cm/s = **1.83 m/s**
- Error propagation treats the two s.d.s as independent, which is an assumption: CV = √(0.330² + 0.189²) = 0.38,
  so ±0.69 m/s. This is a rough spread, because a ratio of means is not the mean of per-fish ratios.

**C. C-start burst (authors' extrapolation):** 0.70–0.80 m/s unscaled. With B-style rescaling:
(0.70–0.80)/1.85 × 3.3 = 1.25–1.43 m/s.

| Variant | Value | Basis |
|---|---|---|
| A, in-water jump peak, unscaled | 1.02 ± 0.34 m/s | observed mean (calculated unit conversion) |
| A′, in-air peak, unscaled | 1.24 ± 0.30 m/s | observed mean; not an in-water speed |
| B, in-water peak, BL-rescaled to 33 mm | 1.83 ± ~0.69 m/s | calculated under size-invariance |
| C, C-start burst, unscaled / rescaled | 0.70–0.80 / 1.25–1.43 m/s | authors' extrapolation / calculated |

**My value: 1.02 ± 0.34 m/s** (variant A). Across the defensible variants it spans **0.70–1.83 m/s**, and
the choice of variant matters more than the measurement s.d.

## Comparison with the recorded value

I could not find the recorded *rebuilt* value. Searching every branch of this repository for guppy, Soares and
S20-D found nothing. So for agreement with the rebuild: **CANNOT TELL**.

Against the original 1.51 m/s comparator: my value (1.02 m/s) is about 32% lower, and 1.51 lies just outside
1.02 ± 0.34. Under the size-invariance rescaling, 1.51 lies inside 1.83 ± 0.69. The primary paper supports neither
"3.5 BL" as a speed nor the specific figure 1.51 m/s.

```swarm-replication
{"claim_id": 169, "my_value": "1.02 ± 0.34 m/s (guppy peak in-water velocity, unscaled; range 0.70–1.83 m/s across scaling choices)", "agrees": null,
  "note": "The primary paper's only 3.5 BL figure is jump height (3.52±0.96 BL), not a speed, and I could not locate the recorded rebuilt value to compare against."}
```
