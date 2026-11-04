# Replication of claim 224: muscle work behind a 0.4 g teleost launch

## Contamination disclosure (read this first)
The file `S29-organism.md` is not on this branch. I found it only on `origin/claude/s29-launch-energy-2iuixr`. I meant to pull out just the input lines, so I grepped it for `0.37|0.93|6.5 %|4.37|0.4 g`. That grep also printed the lines holding the recorded result (S29 lines 108–115: "11.00 mJ", "11.83 mJ = 29.56 J/kg body"). I worked out the arithmetic below **before** running that grep, and the steps are closed-form, so the result did not steer my numbers. Still, this replication is **not blind**. Weigh it as weaker evidence than a fully independent re-derivation.

## Question (as given, truncated)
A 0.4 g body at 4.37 m/s needs 3.82 mJ (9.55 J/kg). With 6.5 % in-water drag, the best measured C-start hydromechanical efficiency of 0.37, and 0.93 tendon return, t[...]

I take the missing part to ask for the **muscle (spring-loading) work needed per launch**. That is my interpretation of the truncated text.

## Inputs
| Input | Value | Source | Read-level | Status |
|---|---|---|---|---|
| Body mass | 0.40 g | question / S29 | full-text (S29 line 82) | given; brief's design value |
| Target speed | 4.37 m/s | question; S29 says it is from S28 | full-text (S29 line 5) | given; S28 not re-checked |
| Kinetic energy | 3.82 mJ | **calculated here**: ½·0.40e-3·4.37² = ½·0.40e-3·19.0969 = 3.819 mJ; /0.40e-3 kg = 9.55 J/kg | — | calculated, matches question |
| Drag loss | 6.5 % of KE (0.250 mJ) | S29 line 103, which **models** it with an ASSUMED Cd 0.2, 24 mm² area and 1.09 cm stroke | full-text (S29) | modelled, not observed. I re-checked the arithmetic: 0.5·1000·0.2·24e-6·19.10·0.00545 = 0.250 mJ |
| Hydromechanical efficiency η_h | 0.37 (range 0.34–0.39, C-start; S-start 0.27, range 0.16–0.37) | Frith, H.R. 1990, UBC thesis on northern pike (*Esox lucius*) fast-start energetics, https://open.library.ubc.ca/collections/831/items/1.0100459. The peer-reviewed version is Frith & Blake 1995, J. Exp. Biol. 198:1863–1873 | thesis: **search-summary** (abstract text quoted in search results); JEB paper: **listing** only | measured (pike, much larger fish). I could not confirm the 1995 JEB paper's own figures |
| Tendon/spring energy return | 0.93 | question / S29 | not independently sourced here | I did not verify a primary source. The figure matches the ~93 % tendon resilience often cited (Bennett, Ker & Alexander 1986), but that link is my recollection, not a source read in this session |

## Arithmetic (all calculated)
Treat drag as an additive load on top of KE. The chain is muscle → spring (×0.93) → hydromechanics (×0.37) → useful KE + drag work.

1. Useful work at the body: 3.819 + 0.250 = 4.069 mJ (same as 3.819 × 1.065 = 4.067).
2. Divide by η_h: 4.069 / 0.37 = **10.997 mJ**.
3. Divide by spring return: 10.997 / 0.93 = **11.825 mJ**.
4. Per body mass: 11.825e-3 / 0.40e-3 = **29.56 J/kg body**.

**Alternative reading:** if "6.5 % drag" means 6.5 % of the *total* useful output, divide by 0.935 instead of multiplying by 1.065. That gives 3.819 / 0.935 / 0.37 / 0.93 = 11.87 mJ (29.7 J/kg). The difference is 0.4 %.

## Result
**≈ 11.8 mJ of muscle work per launch (29.6 J/kg body).** The uncertainty from the arithmetic and the drag convention is ±0.05 mJ. That is swamped by input uncertainty:
- η_h measured in pike ranges 0.34–0.39, which gives 10.9–13.0 mJ.
- η_h is from a much larger fish at higher Re, and it enters linearly, so the true value for a 0.4 g fish is **unknown**.
- Drag rests on an assumed Cd.

This is a calculated number, not an observation.

## Comparison with the recorded value
S29 records 11.00 mJ after η_h and **11.83 mJ = 29.56 J/kg body** after spring return (lines 112–115, seen incidentally; see the disclosure). My value is 11.82–11.83 mJ. **AGREE**, with two caveats: the comparison is not blind, and agreement checks the arithmetic only, not whether η_h = 0.37 (pike) carries over to a 0.4 g fish.

Sources: [Frith 1990 UBC thesis record](https://open.library.ubc.ca/collections/831/items/1.0100459) (search-summary).

```swarm-replication
{"claim_id": 224, "my_value": "11.8 mJ muscle work per launch (29.6 J/kg body); 10.9-13.0 mJ over pike eta_h 0.34-0.39", "agrees": true,
  "note": "Closed-form 3.819 mJ x 1.065 / 0.37 / 0.93 = 11.83 mJ matches the record, but the replication is not blind because a grep for inputs incidentally exposed S29's result lines."}
```
