# Replicate 183: independent re-derivation of S20-D (zebrafish exit speed and aerial phase)

**Claim under test (answer removed when it was set):** replacing S20's back-solved exit speed of 3.13 m/s
with a burst speed taken from Danos & Lauder 2012 (stated as 0.84 m/s, calculated) limits the aerial
phase to about 7 cm and 0.12 s. The launch stays energetically trivial (~1e-4 of daily SMR). The
0.1–1 m escape is out of reach by at least 2.1× in speed, even against a guppy-class jumper.

**Order of work.** I tried to derive every input from primary sources first. Only after the arithmetic
below was done did I open the original working (`origin/claude/deepen-s20-zebrafish-flight-9smifx`,
`docs/research/fish/S20-deepen.md` and `S20-deepen_calc.py`) to compare.

## 1. Inputs and where each one came from

| Input | Value used | Source | Read-level |
|---|---|---|---|
| g | 9.81 m s⁻² | standard constant | n/a |
| Burst / exit speed, adult *D. rerio* | 0.84 m/s, **taken from the claim and not verified** | Danos N, Lauder GV 2012, *J Exp Biol* 215:1854–1862, doi:10.1242/jeb.068957 | **abstract** (Europe PMC REST record). Full text: **could-not-access** |
| Fish size in Danos & Lauder 2012 | **contested, see §3** | Domenici P et al. 2019, *Conserv Physiol* (PMC6839432), which cites Danos & Lauder 2012 | full-text (Europe PMC XML; one sentence quoted in §3) |
| Escape speed needed for 0.1 m and 1 m ranges | from range = v²/g (45°, no drag) | my own calculation | n/a |
| Guppy-class jump comparator | **unknown** | Chang B et al. 2019, *J R Soc Interface* 16:20190014 (PMC6451394) | **could-not-access** (Europe PMC full-text endpoint returned HTTP 500) |
| Fish mass, launch efficiency, daily SMR | **unknown** to me | none reached | Not searched beyond this session's blocked hosts. I did not invent values |

**What I tried for Danos & Lauder 2012:**
- doi.org redirects to journals.biologists.com. One URL there resolved to an unrelated JEB paper, and the
  correct URL returned a bot-check page.
- sites.harvard.edu (author PDF), dash.harvard.edu, zendy.io, researchgate.net, api.semanticscholar.org,
  api.unpaywall.org and core.ac.uk were all refused by the session's network policy.
- The Europe PMC abstract contains no numbers and does not state the developmental stage. It is not open
  access and not in PMC.

**Scope of negative searches:**
- Europe PMC full-text search for `"Danos and Lauder" AND zebrafish AND escape` returned 8 hits. I read the
  citing sentences in three of them (PMC6839432, PMC10065801, PMC6906632). None reports an adult escape
  velocity attributed to the paper.
- One extended web search also found no adult velocity value.

## 2. Arithmetic (calculated, not observed)

The model is ballistic: the fish launches from the surface with no air drag.
- Range at 45°: R = v²/g
- Time aloft at 45°: T = 2·v·sin45°/g
- Apex at 45°: H = v²/(4g)

| v (m/s) | R at 45° | T at 45° | H at 45° | T if vertical (2v/g) | KE per kg (½v²) |
|---|---|---|---|---|---|
| 0.84 | 0.84²/9.81 = 0.0719 m = **7.2 cm** | 2·0.84·0.7071/9.81 = **0.121 s** | 1.8 cm | 0.171 s | 0.353 J/kg |
| 3.13 | 3.13²/9.81 = 0.999 m | 0.451 s | 25 cm | 0.638 s | 4.90 J/kg |

**Speed needed to reach a given range:** v = √(gR).

| Target range | Speed needed | Shortfall at 0.84 m/s |
|---|---|---|
| 0.1 m | 0.990 m/s | 0.990/0.84 = **1.18×** in speed (1.39× in KE) |
| 1.0 m | 3.132 m/s | 3.132/0.84 = **3.73×** in speed (13.9× in KE) |

So S20's 3.13 m/s is simply √(g · 1 m), the 45° speed needed for a 1 m range. I confirm that range scales
as v².

**Energy fraction:** I could not derive it. It needs mass, launch efficiency and SMR, and I had no primary
source for any of the three. Per unit mass, the kinetic energy at 0.84 m/s is 0.353 J/kg, 13.9× less than
at 3.13 m/s.

## 3. Disagreement between sources on the Danos & Lauder fish (preserved, not resolved)

Domenici et al. 2019 (full-text) say: "Viscosity was found to have an overall effect on the escape
response kinematics of **larval zebrafish (*Brachydanio rerio*) (3.3 mm in body length)** … (Danos and
Lauder, 2012)."

- **If that is right**, a 0.84 m/s burst would be about 255 body lengths per second for a 3.3 mm larva. It
  could not be read from that paper as an *adult* burst speed. My inference is that this would be
  implausible.
- **The original working says otherwise.** Read only after my derivation, it uses an adult total length of
  33 mm and a Reynolds number of 27,800. It relays both from repository note replicate-21, not from its
  own reading of the paper.
- **The two inputs are self-consistent with an adult.** U = Re·ν/L = 27,800 × 1e-6 / 0.033 = 0.84 m/s,
  whereas Re = 27,800 at L = 3.3 mm would imply 8.4 m/s.
- **My inference:** "3.3 mm" in Domenici et al. may be a unit slip for 3.3 cm. I cannot confirm this
  without the primary text. **The fish's size is unresolved at full-text level.**

## 4. My value

- **Conditional on v = 0.84 m/s:** maximum ballistic range **7.2 cm** and time aloft **0.12 s** (45°,
  no drag). Calculated. The arithmetic carries no meaningful uncertainty.
- **The input itself:** **unknown** to me. I could not reach Danos & Lauder 2012, and a full-text citing
  source disagrees about which life stage they studied.
- **Speed shortfall at 0.84 m/s:** **1.18× to 3.73×** across the 0.1–1 m range (calculated).

## 5. Comparison with the recorded value

The recorded value, read after the derivation, is: "adult peak burst speed 0.84 m/s (0.78–0.91;
calculated from reported Re 27,800 at 33 mm TL), giving a 7.2 cm maximum ballistic range".

| Part of the claim | Verdict | Why |
|---|---|---|
| 7.2 cm / 0.12 s given 0.84 m/s | **AGREE** | I get 7.19 cm and 0.121 s independently |
| 0.84 m/s itself | **CANNOT TELL** | The original also never read the primary paper: its read-level is "relayed" from replicate-21. A full-text secondary source describes the Danos & Lauder fish as 3.3 mm larvae |
| "~1e-4 of daily SMR" | **CANNOT TELL** | It rests on S20's assumed mass (0.4 g), η = 0.10 and SMR of 15–37 J/day, which I did not verify. Their own inputs give 1.41e-4 J ÷ 0.10 ÷ (15–37 J/day) = 3.8e-5 to 9.4e-5, consistent with "~1e-4" |
| "0.1–1 m … out of reach by at least 2.1× in speed even against a guppy-class jumper" | **DISAGREE** | See below |

**Why I disagree with the 2.1× wording:**
- The 2.1× is 3.13 / 1.51, where 1.51 m/s is the original's guppy-class comparator (3.5 BL vertical jump
  at 33 mm). That ratio applies **only to the 1 m end**.
- At the 0.1 m end, the zebrafish burst speed is short by only 1.18×.
- A guppy-class 1.51 m/s would *exceed* the 0.99 m/s needed for 0.1 m. My calculation gives 23 cm at 45°.
- So the 0.1 m end of S20's 0.1–1 m range is not "out of reach by at least 2.1×".
- The direction of the conclusion (a 1 m escape is unreachable) survives. The quantitative wording, as a
  statement about the whole 0.1–1 m range, does not.

**Overall:** my kinematics match the recorded ones, but I cannot verify the headline input, and one
quantitative clause is overstated. So I record `agrees: null`, not true.

## Sources

- Danos & Lauder 2012, doi:10.1242/jeb.068957 — abstract via Europe PMC; full text could-not-access.
- Domenici et al. 2019, PMC6839432 — full-text (Europe PMC XML).
- Citing articles PMC10065801 and PMC6906632 — full-text, citing sentences only. Neither gives adult
  velocities.
- Chang et al. 2019, PMC6451394 — could-not-access.
- Original working, `S20-deepen.md` and `S20-deepen_calc.py` on `origin/claude/deepen-s20-zebrafish-flight-9smifx`
  — full-text (repository), read only after the derivation.

```swarm-replication
{"claim_id": 183, "my_value": "7.2 cm range and 0.121 s aloft at 45 deg (calculated, conditional on v = 0.84 m/s); speed shortfall 1.18x (0.1 m) to 3.73x (1 m); the 0.84 m/s input itself unknown", "agrees": null,
  "note": "Ballistic arithmetic agrees exactly, but the 0.84 m/s Danos & Lauder input could not be reached (and a full-text citer describes their fish as 3.3 mm larvae), and the 'at least 2.1x' shortfall holds only at the 1 m end, not at 0.1 m where a guppy-class jump would suffice."}
```
