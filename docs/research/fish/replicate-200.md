# Replication of claim 200 ([S21]): adult zebrafish peak fast-start speed from the Danos & Lauder (2012) Reynolds number

Independent re-derivation. I did not look for the original deriver's working. The harvest context
`harvest:zebrafish-fast-start-velocity-pxsv7e` is **not present** in this repository: I grepped the
working tree for `pxsv7e`, `27,800`, `27800` and `Danos` and found no matches, and the only branches are
`claude/zebrafish-fast-start-velocity-lawcjs` and `work/frontier-foundation`. So I saw no prior working.

## Result

**My value: a calculated mean peak speed of 0.84 m/s (≈25.5 TL/s), with a ±1 s.e.m. band of 0.78–0.91 m/s.
This is a calculation, not an observation.** It holds only if Danos & Lauder defined
Re = U·TL/ν with ν = 1.0×10⁻⁶ m² s⁻¹. If Re were recomputed with the kinematic viscosity of pure water at 28 °C
(ν ≈ 0.84×10⁻⁶ m² s⁻¹), the same Re would give **0.71 m/s** (0.65–0.76 m/s). I have not seen the paper's
definition of Re, so I cannot choose between these two values from the source. The structural uncertainty
(about 16%) is larger than the s.e.m. band (about 8%).

## Inputs, sources and read-levels

| Input | Value | Source | Read-level |
|---|---|---|---|
| Mean maximum Reynolds number, 1 mPa s water | 27,800 ± 2,140 (s.e.m.) | Danos & Lauder 2012, *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957 | **could-not-access** for this number. I took it from the question text and could not check it against the paper. |
| Fish total length | 33.0 ± 1.3 mm | Same paper | **search-summary** (a WebSearch result summary quoted "mean total length of 33.0±1.3mm"). I did not read it in the paper. |
| Frame rate | 1000 frames s⁻¹ | Same paper | **abstract** (Europe PMC, PMID 22573764) |
| Nominal water viscosity | 1 mPa s | Same paper | **abstract** |
| Definition of Re (which length, which velocity, which ν) | `unknown` | Same paper | **could-not-access** |
| ν of water at 28 °C (alternative case) | ≈0.84×10⁻⁶ m² s⁻¹ (μ ≈ 0.836 mPa s, ρ ≈ 996 kg m⁻³) | Standard water-property tables, from my own background knowledge. The rearing and test temperature in the paper is `unknown` to me. | none (background knowledge) |

### Access attempts, so the negative search has a stated scope

- journals.biologists.com, both the article page and the PDF, returned HTTP 403 (a Cloudflare challenge). WebFetch of the
  article URL returned a different JEB article.
- sites.harvard.edu, the Lauder lab PDF `Danos.Lauder.2012.pdf`, was blocked by the network policy.
- core.ac.uk/download/151422416.pdf, dash.harvard.edu, zendy.io, unpaywall and scholar.archive.org were all blocked by the proxy.
- Europe PMC lists the paper as not open access and not in PMC. From there I got the abstract only.
- I searched Europe PMC full text of PMC11930232 (Ravel et al. 2025, *iScience*, which cites Danos & Lauder) for the
  Re or speed values. It cites the paper but reports no Re or speed numbers from it (read-level: full-text).

The question says Danos & Lauder 2012 was read in full text. **I could not confirm that read-level.** I can vouch only
for the abstract.

## Arithmetic

Re = U·L/ν, so U = Re·ν/L, with L = TL = 0.033 m.

Case A, ν = 1.0×10⁻⁶ m² s⁻¹ (μ = 1 mPa s as stated, ρ = 1000 kg m⁻³):
- Mean: 27,800 × 1.0e-6 / 0.033 = 0.02780 / 0.033 = **0.842 m/s**, and 0.842 / 0.033 = **25.5 TL/s**
- −1 s.e.m.: 25,660 × 1e-6 / 0.033 = **0.778 m/s** (23.6 TL/s)
- +1 s.e.m.: 29,940 × 1e-6 / 0.033 = **0.907 m/s** (27.5 TL/s)
- If the TL s.d. (±1.3 mm) is also allowed to work against Re, in the worst-case corners: 25,660e-6/0.0343 = 0.748 and 29,940e-6/0.0317 = 0.944 m/s. This corner-stacking is my own sensitivity check and not a confidence interval.

Case B, ν = 0.839×10⁻⁶ m² s⁻¹ (water at about 28 °C):
- Mean: 27,800 × 0.839e-6 / 0.033 = **0.707 m/s** (21.4 TL/s). The ±1 s.e.m. band is 0.652–0.761 m/s.

Caveats (my inference, not the authors' claims):
1. If Re used the centre-of-mass velocity and TL, then U is the peak centre-of-mass speed. If it used another length,
   such as a fin or body depth, or another velocity, such as the tail tip, U is a different quantity. That definition is `unknown`.
2. The question reports s.e.m. The spread across individual fish would be wider. The "range" is therefore a band for the mean,
   not the range of individual fish.
3. The comparisons in the claim ("1.5× the Ucrit proxy", "~7× below 5.8 m/s") depend on inputs I was not given.
   I checked only the second: 5.8 / 0.842 = 6.9×, which is consistent with "~7×". Under case B it is 5.8 / 0.707 = 8.2×.
   I did not check the Ucrit ratio because I do not have the Ucrit proxy value.

## Comparison with the recorded value

The question itself records ~0.84 m/s (~25 TL/s), range 0.78–0.93 m/s. I saw it only because it is part of the question,
and I found no separate record of it in the repository.

- Central value: **AGREE** under case A (0.842 m/s, 25.5 TL/s).
- Lower bound 0.78: **AGREE** (0.778).
- Upper bound 0.93: **DISAGREE slightly.** +1 s.e.m. gives 0.907 m/s, not 0.93. Adding the TL s.d. in the worst-case corner
  gives 0.944 m/s, so 0.93 is reproduced by neither simple method. I cannot tell how it was obtained.
- Inputs: **CANNOT TELL.** The arithmetic agreement is not independent evidence for the Re value (27,800 ± 2,140) or for
  the Re definition. Both were taken from the question, and I could not read either in the paper. If the authors used real
  28 °C water properties, the speed would be about 0.71 m/s, not 0.84.

The safe conclusion survives in both cases. A mean peak speed of 0.71–0.84 m/s is 7–8× below a 5.8 m/s threshold.

```swarm-replication
{"claim_id": 200, "my_value": "0.84 m/s (25.5 TL/s; ±1 s.e.m. 0.78-0.91 m/s), calculated, not observed; 0.71 m/s if Re used nu=0.84e-6 m2/s", "agrees": true,
  "note": "The arithmetic U = Re*nu/TL reproduces 0.84 m/s with nu = 1e-6 m2/s, but I could not access the Danos & Lauder full text to verify Re = 27,800 or its definition, and the upper bound 0.93 m/s does not reproduce (I get 0.91 m/s)."}
```
