# Replicate 1 — stall speed of a 1-body-length-span wing on a 0.4 g zebrafish

Claim under test (with the answer removed): stall speed for a wing whose span is 1 body length, AR 5, CL 0.6, on a 0.4 g zebrafish.

Everything below is **calculated** with the textbook lift equation. None of it is an observation. No fish was measured and no experiment was run.

## Method

Lift equals weight at stall: `m·g = ½·ρ·V²·S·CL`, so `V_stall = sqrt(2·m·g / (ρ·S·CL))`.
Wing area comes from the aspect ratio: `AR = b²/S`, so `S = b²/AR`, with `b` = 1 body length (L).

## Inputs

| Input | Value used | Source | Read-level |
|---|---|---|---|
| Mass m | 0.4 g = 4.0e-4 kg | Given in the claim. I did not verify it independently. | n/a (premise) |
| Aspect ratio | 5 | Given in the claim (a design assumption) | n/a (premise) |
| CL | 0.6 | Given in the claim (a design assumption) | n/a (premise) |
| g | 9.80665 m/s² | Standard gravity (definition) | n/a |
| Air density ρ | 1.225 kg/m³ (ISA sea level, 15 °C). Sensitivity check with 1.204 (20 °C) and 1.2. | ISA standard atmosphere (standard value) | n/a |
| Body length L (= span b) | **The claim does not give it.** I used a central value of 3.8 cm, with a range of 3.4 to 4.0 cm. | FishBase *Danio rerio* summary: "Max length: 3.8 cm SL male/unsexed". FishBase generic subfamily length-weight relationship (not zebrafish-specific): W = 0.00977·TL^3.04 (g, cm). | **search-summary**. The direct fetch of fishbase.se failed because the host is outside this session's network allowlist, so I only have the search engine's excerpt. |

### Body length is the input that controls the answer, so here is where the range comes from

- 3.8 cm is FishBase's *maximum* standard length, which is a ceiling and not a typical adult size. Standard length also leaves out the tail fin. (FishBase claim, search-summary.)
- If I invert the generic length-weight relationship for 0.4 g, I get TL = (0.4/0.00977)^(1/3.04) = **3.39 cm**. This is my own inference from a relationship fitted at subfamily level, not a zebrafish measurement. It suggests a 0.4 g fish is about 3.4 cm in total length.
- "Body length" in the claim is ambiguous. It could mean standard length or total length. I treat 3.4 to 4.0 cm as the plausible range for this mass.

## Arithmetic (central case: L = 3.8 cm, ρ = 1.225)

- b = 0.038 m → b² = 1.444e-3 m²
- S = 1.444e-3 / 5 = 2.888e-4 m² (2.888 cm²)
- W = m·g = 4.0e-4 × 9.80665 = 3.9227e-3 N
- 2W = 7.8453e-3 N
- ρ·S·CL = 1.225 × 2.888e-4 × 0.6 = 2.1227e-4 kg/m
- V² = 7.8453e-3 / 2.1227e-4 = 36.96 m²/s²
- **V = 6.08 m/s**

### Sensitivity (computed)

| L (cm) | S (cm²) | V at ρ=1.225 | V at ρ=1.204 | V at ρ=1.2 |
|---|---|---|---|---|
| 3.0 | 1.800 | 7.70 | 7.77 | 7.78 |
| 3.39 | 2.298 | 6.82 | 6.87 | 6.89 |
| 3.5 | 2.450 | 6.60 | 6.66 | 6.67 |
| 3.8 | 2.888 | 6.08 | 6.13 | 6.14 |
| 4.0 | 3.200 | 5.78 | 5.83 | 5.84 |

V scales as 1/L, so a 10 % uncertainty in L becomes a 10 % uncertainty in V. Changing ρ within normal sea-level conditions shifts V by less than 1 %.

**My value: 6.1 m/s (range 5.8 to 6.8 m/s for L = 4.0 to 3.4 cm). Calculated, not observed.**

## Comparison with the recorded value

I compared only after deriving my own value. The recorded value is 5.84 m/s, as stated in the claim text. I searched this repository for `zebrafish-glide-physics.md` and for "5.84" in `*.md` files and found nothing. So I could not read the recorded working, and I cannot tell which inputs it used.

My inference: 5.84 m/s is exactly what the formula gives for L = 4.0 cm with ρ ≈ 1.20 kg/m³ (5.835 m/s), or with ρ = 1.204 (5.83 m/s). At ρ = 1.225 the same length gives 5.78 m/s. The recorded arithmetic is therefore consistent with the formula. However, it sits at the **long-body end** of the plausible length range for a 0.4 g fish. 4.0 cm is longer than FishBase's maximum SL of 3.8 cm, though it would be reasonable as a total length.

**Verdict: AGREE on method and order of magnitude (about 6 m/s). The exact 5.84 depends on assuming L = 4.0 cm, which I could not confirm.** My central estimate is about 4 % higher (6.08 m/s). The recorded value falls inside my range, but at its low edge. The length-weight relationship points to a shorter fish and so a higher stall speed (about 6.8 m/s).

## Searches and their scope

- Web search: "adult zebrafish standard length body mass grams Danio rerio length-weight" (one query, standard mode). It found FishBase and some growth studies. I did not get a zebrafish-specific length-weight equation, and none of the snippets paired SL with mass.
- Direct fetch of fishbase.se: could-not-access (network allowlist).
- Repository: `zebrafish-glide-physics.md` does not exist on this branch. No `*.md` file contains "5.84".

```swarm-replication
{"claim_id": 1, "my_value": "6.1 m/s (range 5.8-6.8 m/s; calculated)", "agrees": true,
  "note": "Same formula reproduces 5.84 m/s only at L=4.0 cm and rho~1.2; with FishBase max SL 3.8 cm and rho=1.225 I get 6.08 m/s, and a 0.4 g length-weight inversion (~3.4 cm) gives ~6.8 m/s, so the recorded value is at the low edge of a plausible range."}
```
