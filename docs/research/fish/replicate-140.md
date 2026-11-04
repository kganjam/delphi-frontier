# Replication of claim 140 (S20-D-D-D): *Danio* exit speed from a guppy jump/C-start ratio

Independent re-derivation. **I did not read the original derivation.** The inputs pointer
(`harvest:deepen-s20-d-subproblem-b4iz3k`) contains `docs/research/fish/S20-D-D-deepen.md` and
`S20-D-D-deepen_calc.py`. Those files are the working under test. I saw their names in a
`git diff --stat` and opened neither. I took only the upstream *Danio* C-start input from the
parent S20 and S20-D documents (`claude/deepen-s20-zebrafish-flight-9smifx`,
`claude/s20-d-sensitive-input-77m8c9`), and I read only the lines that mention the burst value.

## My value (calculated, not measured in *Danio*)

- **Typical *Danio* exit speed: 1.39 m/s (1.20–1.61).** Calculated.
- **Upper tail (guppy mean + 2 SD): 2.06 m/s (1.79–2.39).** Calculated.
- **1 m aerial escape (needs 3.13 m/s): out of reach.** The calculated speed floor is 3.13/2.39 = **1.31×**
  at the most generous corner, and 1.52× at the central upper-tail value.
- **0.5 m escape (needs 2.21 m/s):** excluded at the central upper tail (2.06 m/s). Not excluded at
  the most generous corner (2.39 m/s).

## Inputs

| # | Input | Value | Source | Read-level | Measured or estimated |
|---|---|---|---|---|---|
| 1 | Guppy max velocity **in air**, mean ± SD | 123.57 ± 30.0 cm/s (Table 1). The Discussion gives "123±30.0". | Soares & Bierman 2013, *PLoS ONE* 8:e61617, PMC3629028 | full-text (via a WebFetch summary that quotes the text verbatim) | measured: 20 jumps by 5 male fish, 1000 fps |
| 2 | Guppy max velocity **in water** | 102.36 ± 33.75 cm/s (Table 1 and Results). The Discussion gives 100.16 ± 33.9. **The paper disagrees with itself; I report both.** | same | full-text | measured |
| 3 | Guppy C-start burst speed | "about 70 to 80 cm/sec" | same, Discussion | full-text | **not measured.** The authors extrapolated it from Chappell & Odell 2004 and their own study. Fig. 1D shows a startle trace with no speed reported. |
| 4 | *Danio* adult C-start burst | 0.842 m/s (0.78–0.91), from a reported Re of 27,800 at 33 mm TL | Danos & Lauder 2012, *JEB* 215:1854, as carried by the upstream S20 doc | **Re value: could-not-access.** The Europe PMC abstract was read and has no numbers. The journal URL returned an unrelated page. sites.harvard.edu and researchgate.net are blocked by this session's network policy. | **calculated** from Re, not a reported speed |
| 5 | Speed for a 1 m escape | 3.13 m/s | given in the question (S20) | — | calculated |
| 6 | g | 9.81 m/s² | — | — | constant |

I checked input 4 arithmetically: Re·ν/L = 27,800 × 1.0×10⁻⁶ / 0.033 = **0.842 m/s**, so the inversion
assumes ν = 1.0×10⁻⁶ m²/s, which is water at ~20 °C. At 28 °C, a usual zebrafish husbandry
temperature, ν ≈ 0.84×10⁻⁶ m²/s and the same Re gives **0.708 m/s**. This is my inference: I do not know the
temperature Danos & Lauder used. An unattributed search snippet attached to the Danos & Lauder
ResearchGate listing reads "maximum velocity … 0.71±0.03 m s⁻¹ … 17.1±1.4 m s⁻² (N=7 fish)". I could
not open it or confirm which paper or life stage it describes. If 0.71 m/s were the right *Danio* burst
speed, every output below would fall by about 16 %.

## Arithmetic (`replicate-140_calc.py`)

1. Midpoint of the C-start estimate: (70 + 80)/2 = 75 cm/s.
2. Typical ratio (air mean / C-start): 123.57/75 = **1.648**. Range: 123.57/80 = 1.545 to 123.57/70 = 1.765.
3. Typical *Danio* speed: 0.842 × 1.648 = **1.387 m/s**. Low corner 0.78 × 1.545 = 1.205. High corner 0.91 × 1.765 = 1.606.
4. Upper tail: 123.57 + 2 × 30.0 = 183.57 cm/s, so the ratio is 183.57/75 = 2.448. Then 0.842 × 2.448 = **2.061 m/s**.
   Low corner 0.78 × 183.57/80 = 1.790. High corner 0.91 × 183.57/70 = 2.386.
5. Ballistic range at 45° is R = v²/g, so 3.13²/9.81 = 0.999 m, which checks the 1 m figure. A 0.5 m range needs v = √(0.5 × 9.81) = **2.215 m/s**.
6. Speed floor for 1 m. Old: 3.13/1.82 = **1.72×**. New: 3.13/2.386 = **1.31×** at the most generous corner, or 3.13/2.061 = 1.52× at the central tail.
7. 0.5 m test: the most generous corner (2.386 m/s) is above 2.215 m/s, so a 0.5 m escape is not excluded there. The central tail (2.061 m/s) is below it.

Sensitivity to choices the question does not pin down (calculated):
- An upper tail of mean + **1** SD instead of mean + 2 SD gives 1.72 m/s.
- An **in-water** jump peak (102.36) instead of the in-air peak gives a ratio of 1.365 and a typical speed of 1.15 m/s.
  The paper puts the peak in-air speed "immediately after breaking the interface". So the in-air figure is the exit speed, but it is the more generous of the two readings.

## Caveats (my inference, not the authors' claims)

- The ratio's denominator is an **estimate by the authors, not a measurement**. Calling the ratio "within-species" is fair as to species, but it is a measured jump divided by an extrapolated C-start.
- Applying a guppy jump/C-start ratio to *Danio* assumes *Danio* jumps like a guppy relative to its own C-start. I found no *Danio* exit-speed measurement. Scope of that negative: three web searches in this session (Soares & Bierman details; adult zebrafish C-start peak velocity; adult zebrafish escape velocity in BL/s or m/s, extended mode), plus the "0.71/17.1" snippet search.
- The SD of 30 cm/s pools 20 jumps from 5 fish. Mean + 2 SD is a parametric tail, not an observed maximum.

## Comparison with the recorded value

The question states 1.39 m/s (1.20–1.61) typical, 2.06 m/s (1.79–2.39) upper tail, a 1 m escape out of
reach, a floor falling from 1.7× to ~1.3×, and 0.5 m not excluded at the most generous corner. My
re-derivation gives 1.387 (1.205–1.606), 2.061 (1.790–2.386), 1.72× → 1.31×, and the same 0.5 m
verdict. **AGREE.** The agreement is on the arithmetic from shared inputs. Both derivations inherit the
unverified Re 27,800 and the ν = 1.0×10⁻⁶ assumption. Both also rest on an extrapolated guppy C-start denominator rather than a measured one.

Sources:
- Soares D, Bierman HS (2013) Aerial jumping in the Trinidadian guppy. *PLoS ONE* 8:e61617. https://pmc.ncbi.nlm.nih.gov/articles/PMC3629028 (full-text)
- Danos N, Lauder GV (2012) Challenging zebrafish escape responses by increasing water viscosity. *JEB* 215:1854–1862. doi:10.1242/jeb.068957 (abstract read via Europe PMC; numbers could-not-access)

```swarm-replication
{"claim_id": 140, "my_value": "typical 1.39 m/s (1.20-1.61), upper tail 2.06 m/s (1.79-2.39), calculated; 1 m floor 1.31x", "agrees": true,
  "note": "Arithmetic reproduces exactly from Soares & Bierman's 123.57+/-30 cm/s air peak over their extrapolated 70-80 cm/s C-start times the 0.842 m/s Danio burst, but that burst assumes nu=1.0e-6 (0.71 m/s at 28 C) and the guppy C-start is an author estimate, so both derivations share those unverified inputs."}
```
