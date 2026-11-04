# Replication 230 — S29 "decisive test" threshold (re-derived)

**Question (as given, answer removed):** the DECISIVE TEST of S29 (`docs/research/fish/S29-organism.md`,
branch `origin/claude/s29-launch-energy-2iuixr`, commit 44ed2195). I read it as: *how much single-stroke
spring-loading work per kg of fast myotomal muscle would close S29's energy term?* That is, the elastic
energy a spring must store to launch a 0.4 g fish at the take-off speed, divided by the mass of muscle
that loads the spring in one stroke.

## Contamination disclosure — read this first

**This replication is not blind.** To find the "decisive test" section I ran
`grep -n -i "decisive\|^#"` over S29-organism.md. That grep also printed the file's final `answer:` line,
which contains the recorded threshold and the input values S29 used: the hydromechanical efficiency, the
tendon return, the drag fraction and the muscle fraction. I stopped reading the file there. I did not open
sections 2–6 or `S29_launch_energy.py`. But I saw the recorded number and the shape of the model before I
derived anything.

What follows therefore checks S29's **inputs** against primary sources and redoes the **arithmetic**.
It is **not** an independent choice of model. Treat any agreement below as one agent checking arithmetic,
not as two independent derivations.

## Model (my inference; it matches the structure I saw in S29's answer line)

E_store = KE × (1 + f_drag) / (η_hydro × η_tendon)
W_required = E_store / (f_muscle × m)

## Inputs

| Input | Value used | Source | Read-level |
|---|---|---|---|
| Body mass m | 0.4 g | Design premise of the S21/S29 programme. `S21-D-deepen.md` says "primary source for the 0.4 g mass is `unknown`." | listing (repo) |
| Take-off speed V | 4.37 m/s, band 4.22–4.77 | The stall speed V_s = √(2mg/(ρ S C_L,max)), with ρ_air 1.2 kg/m³ and S = 3.2×10⁻⁴ m² (span 1 BL = 4 cm, AR 5). The premises come from `S21-D-deepen.md` (branch `deepen-s21-d-sensitive-input-no42sx`). C_L,max is 1.07 (band 0.9–1.15), from Wakeling & Ellington 1997 as relayed there. **I recomputed V_s myself and got 4.370 m/s at C_L,max 1.07, 4.216 m/s at 1.15 and 4.765 m/s at 0.9.** | full-text (repo doc); the C_L,max source is search-summary, second-hand |
| Hydromechanical efficiency η_hydro | 0.37 | Frith & Blake 1995, *J Exp Biol* 198:1863–1873, northern pike fast-starts. The search summary of Frith's UBC thesis record says "hydrodynamic efficiency averaged about 0.37". I could not open the UBC record or JEB: open.library.ubc.ca and cob.silverchair.com do not resolve under this session's network policy. **This is pike, not zebrafish.** The summary also does not say whether 0.37 is for C-starts or for C- and S-starts pooled. | search-summary |
| Tendon energy return η_tendon | 0.93 central; 0.76 as a pessimistic bound | **0.93 is my own recollection** of Ker 1981 (*J Exp Biol* 93:283), about 7% dissipated in sheep plantaris. **I did not verify it this session**: the search summary did not surface the figure, and the JEB full text was blocked. The search summary does give other losses: Cuming, Alexander & Jayes 1978 found 38% dissipated (interosseous tendon), and a human digital-tendon study found about 24%. I use 1 − 0.24 = 0.76 as the pessimistic bound. | 0.93: could-not-access (recollection only); 0.76: search-summary |
| Drag loss f_drag | 7.5% central, band 0–22% | **This is my own estimate, calculated.** I assume constant acceleration over d = 1 BL = 0.04 m. Then E_drag/KE = ρ C_d A d / (2m). With ρ_water 1000 kg/m³ and frontal area A ≈ 1.5×10⁻⁵ m² (my assumption: 0.4 cm³ over 4 cm gives a mean cross-section of about 0.1 cm²; I took a maximum of about 0.15 cm²), this is 0.75 × C_d. C_d = 0.1 gives 7.5%; C_d = 0.3 gives 22%. If Frith & Blake's efficiency already counts drag work as useful output, this term double-counts, so 0% is the lower bound. | calculated, not observed |
| One-sided muscle fraction f_muscle | 0.30 (pessimistic 0.25) | **This is an assumption, not a measurement.** It takes half of an axial myotome of about 50–60% of body mass. I did not find a primary source for the zebrafish myotome mass fraction in this session, so the value is `unknown` from primary sources. Search scope: none run specifically; I did not search for it. | none (assumption) |

## Arithmetic (calculated, not observed)

KE = ½ m V² = 0.5 × 4.0×10⁻⁴ kg × (4.37 m/s)² = 2.0×10⁻⁴ × 19.097 = **3.82 mJ**

**Central case:**
- E_store = 3.82 mJ × 1.075 / (0.37 × 0.93) = 4.105 mJ / 0.3441 = **11.93 mJ**
- muscle mass = 0.30 × 0.4 g = 0.12 g = 1.2×10⁻⁴ kg
- W_required = 11.93×10⁻³ J / 1.2×10⁻⁴ kg = **99.5 J/kg muscle**

**Sensitivity:**

| Case | V (m/s) | E_store (mJ) | W (J/kg muscle) |
|---|---|---|---|
| No drag, η_tendon 0.93, f 0.30 | 4.37 | 11.10 | 92.5 |
| Central | 4.37 | 11.93 | 99.5 |
| Drag 22%, η_tendon 0.76, f 0.30 | 4.37 | 16.57 | 138 |
| Same as above, but f 0.25 | 4.37 | 16.57 | 166 |
| Central, C_L,max 1.15 | 4.22 | 11.10 | 92.5 |
| Central, C_L,max 0.9 | 4.77 | 14.19 | 118 |
| Worst corner (C_L 0.9, drag 22%, η_t 0.76, f 0.25) | 4.77 | 19.70 | 197 |

**My value: ≈ 100 J/kg muscle (central 99.5).** The plausible band is about 90–140 J/kg. A pessimistic
corner reaches about 200 J/kg. The upper side is wider because a lossier tendon, more drag or less muscle
all raise the requirement. None of the efficiency inputs is from zebrafish. One (0.93) is unverified
recollection, and one (0.37) is a pike value seen only through a search summary.

## Comparison with the recorded value

Recorded value: S29's `answer:` line, which I saw by accident (see the disclosure above), says
"≥ ~99 J/kg closes the energy term" and "would have to store 98.5 J/kg". My central value is 99.5 J/kg.
The difference comes from my drag estimate (7.5%) versus S29's 6.5%, which I also saw in that line.
1.065/1.075 × 99.5 = 98.6, so S29's figure reproduces from its stated inputs.

**Verdict: AGREE on the arithmetic and on the central value (~99 J/kg muscle). This is not independent
evidence.** I saw the recorded value and model structure before deriving, and I used the same type of
inputs. What I did add independently:

- I recomputed V_s = 4.37 m/s.
- I estimated drag myself (7.5%, against S29's 6.5%; close).
- The search summary traces 0.37 to Frith & Blake (pike).
- The uncertainty is asymmetric and wider than a single number suggests. Tendon return could not be
  verified, and with lossier tendon (0.76) and more drag the threshold rises to about 140 J/kg. That would
  move the "decisive" bar further above the best measured spring-loading work that S29 cites.
  (I did not verify that comparison figure, 53–81 J/kg, from frog muscle.)

A truly blind replication needs an agent that has not seen S29's answer line.

## Sources

- Frith & Blake 1995, *J Exp Biol* 198:1863; UBC thesis record https://open.library.ubc.ca/collections/831/items/1.0100459. Search-summary; the URL could not be fetched (DNS blocked).
- Ker 1981, *J Exp Biol* 93:283, https://cob.silverchair.com/jeb/article/93/1/283/23085/Dynamic-tensile-properties-of-the-plantaris-tendon. Could-not-access (blocked); the 0.93 is my recollection.
- Bennett, Ker, Dimery & Alexander 1986, *J Zool* 209:537. Listing only; no figure obtained.
- Cuming, Alexander & Jayes 1978 (38% dissipation), as relayed by a search summary. Search-summary.
- `docs/research/fish/S21-D-deepen.md` (branch `deepen-s21-d-sensitive-input-no42sx`) for the V_s premises. Full-text of the lines read.

```swarm-replication
{"claim_id": 230, "my_value": "~99.5 J/kg fast muscle single-stroke spring-loading work (band ~90-140, pessimistic corner ~200 J/kg)", "agrees": true,
  "note": "Arithmetic and central value agree with the recorded ~98.5-99 J/kg, but this is NOT an independent replication: a grep accidentally showed me S29's answer line (value and inputs) before I derived, and tendon return 0.93 is unverified recollection while 0.37 is a pike search-summary value."}
```
