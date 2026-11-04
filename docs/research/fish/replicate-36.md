# Replicate 36: tail-beat frequency as the binding limit on surface taxiing

**Claim (answer withheld from me):** "Surface taxiing cannot close the launch gap, and the binding
limit is TAIL-BEAT FREQUENCY not thrust force". The inputs were said to live in `S24-behaviour.md`
(the Strouhal-law entry).

**Process note.** The prompt said the inputs were "reproduced here exactly", but no numbers came
with it. `S24-behaviour.md` is not on this branch or on `main`. It exists only on
`origin/claude/s24-surface-taxiing-launch-tsepbn`. I did **not** open that file until §4. Before
that I chose all my inputs from primary sources. The one exception is the target speed, which I
took from a different document, `challenge-24.md`, which records claim 24, not claim 36. I did not
open `S24_calcs.py` at any point.

Every number in §1–§3 is **calc** (my arithmetic on the inputs listed), **measured** (a literature
value, with read-level) or **assumed**. Nothing here is observed or simulated by me.

## 1. Inputs

| # | Input | Value | Kind | Source | Read-level |
|---|---|---|---|---|---|
| 1 | Required take-off airspeed | 4.37 m/s | project-derived (not observed) | Claim-24 text quoted in `docs/research/fish/challenge-24.md` (branch `claude/challenge-takeoff-speed-claim-bsocad`). It is derived from a corrected CL_max that I could not inspect. | full-text (of the repo doc). The upstream derivation: could-not-access |
| 2 | Strouhal band for thrust/cruise, St = fA/U | 0.2–0.4 | measured (comparative) | Taylor, Nudds & Thomas 2003, *Nature* 425:707, doi:10.1038/nature02000 | search-summary |
| 3 | Adult zebrafish body length | 3.4 ± 0.2 cm | measured | Mwaffo et al. 2017, *PeerJ* 5:e4041 (12 wild-type adults) | full-text (automated fetch summary) |
| 4a | Peak-to-peak tail amplitude, maximum | ≈ 0.2 L (one-fifth of length) → 6.8 mm | measured (dace, trout, goldfish, not zebrafish) | Bainbridge 1958, *J. Exp. Biol.* 35 | search-summary (abstract snippet) |
| 4b | Zebrafish burst tail amplitude | "on the order of 10 mm" | measured, second-hand | Gilbert et al. 2014, as cited in Mwaffo 2017 | listing (second-hand citation; Gilbert not read) |
| 5 | Max freely-swimming adult zebrafish frequency | 21 Hz ("never exceeding 21 Hz") | measured | Kyriakatos et al. 2011, *J. Neurosci.* 31:8422, PMC6623330 | full-text (automated fetch summary) |
| 6 | Max frequency during escape | 52 Hz | measured | Kyriakatos et al. 2011, same | full-text (automated fetch summary) |
| 7 | Speed–frequency relation (independent cross-check) | U = ¼ L (3f − 4), U in cm/s, L in cm, valid for f > 5 Hz | empirical fit (other species) | Bainbridge 1958 | search-summary |

Caveats on the inputs. Input 4a was fitted on other species, and input 7 was fitted on fish up to
30 cm and at frequencies far below 50 Hz, so applying either to a 3.4 cm zebrafish at more than
100 Hz is an extrapolation. Input 6 is the maximum during an escape, measured by electrophysiology
in Kyriakatos 2011. It is not a sustained tail-beat frequency.

## 2. Arithmetic (calc)

Frequency needed to keep a tail inside the Strouhal band at U = 4.37 m/s, using f = St·U/A:

| A | St 0.2 | St 0.3 | St 0.4 |
|---|---|---|---|
| 6.8 mm (0.2 × 34 mm) | 0.2·4.37/0.0068 = **128.5 Hz** | **192.8 Hz** | **257.1 Hz** |
| 10 mm (Gilbert, second-hand) | **87.4 Hz** | **131.1 Hz** | **174.8 Hz** |

Cross-check with Bainbridge's fit, solved for f: f = (4U/L + 4)/3 = (4·437/3.4 + 4)/3 = (514.1 + 4)/3 =
**172.7 Hz**.

Sensitivity to body length, at St 0.3 and A = 0.2 L: L = 3.0 cm gives 218.5 Hz (Bainbridge 195.6
Hz); L = 4.0 cm gives 163.9 Hz (Bainbridge 147.0 Hz).

Inverse: the fastest taxi the measured frequency ceilings could sustain, U = fA/St:

- At **52 Hz** the full corner range is 0.88–2.60 m/s, with 1.18 m/s at A 6.8 mm and St 0.3.
  Bainbridge gives 0.85 × 152 = 1.29 m/s.
- At **21 Hz** the range is 0.36–1.05 m/s. Bainbridge gives 0.50 m/s.

Ratio of required to available frequency: 87–257 Hz against 52 Hz is **1.7×–4.9×**; against 21 Hz
it is **4.2×–12.2×**.

## 3. My value

**Required tail-beat frequency at 4.37 m/s ≈ 170 Hz (range 87–257 Hz; calc).** That is
1.7–4.9× the highest frequency measured in an adult zebrafish (52 Hz, during escape). By the same
calc, the taxi speed reachable at 52 Hz is about 0.9–2.6 m/s, central about 1.2–1.3 m/s.
Inference: no corner of this input box reaches 4.37 m/s, so under these inputs taxiing cannot
close that gap.

What I did **not** establish:

- **The "not thrust force" half.** I had no zebrafish caudal thrust data, no mass, no lobe area
  and no taxi drag. I did not derive the force side. Whether force or frequency binds first is
  **unknown** from my work.
- **Whether frequency is truly binding.** The Strouhal band describes efficient cruising in
  Taylor et al. 2003. It is not a proven thrust cutoff. If net thrust persists below St 0.2, the
  required frequency falls in proportion.
- **Whether the taxiing posture changes the kinematics.** Amplitude and frequency in a
  surface-piercing posture have not been measured, and I found nothing on this.

## 4. Comparison with the recorded value (opened only after §1–§3)

I then opened `docs/research/fish/S24-behaviour.md` on `origin/claude/s24-surface-taxiing-launch-tsepbn`
(sections "Short answer", §3.2, §4 and §5). I read nothing else and did not open `S24_calcs.py`.

The author's claim (their numbers, not mine): it uses **two target speeds that differ from mine**,
5.84 m/s for a 1-BL wing and 1.95 m/s for a 3-BL wing, and neither is the 4.37 m/s recorded in
claim 24. It uses St 0.15–0.4, A = 0.15–0.25 TL, and a 4 cm fish. Their recorded values:

- 1.95 m/s needs **49–73 Hz** (St 0.2–0.3, A 0.2 TL = 8 mm). They call this "not refuted, not
  shown feasible".
- 5.84 m/s needs **88–292 Hz**, which is 1.7–5.6× the 52 Hz maximum. They call this "cannot
  close".
- Taxi ceilings: 0.56 m/s at 21 Hz and 1.39 m/s at 52 Hz (central, A 0.2 TL, St 0.3).
- The force side is "not the obstacle" at 1.95 m/s. It rests on drag balances with assumed
  areas that they say could be off by 2–3×.

My method on their inputs (calc). At 1.95 m/s, A 8 mm and St 0.2–0.3: 0.2·1.95/0.008 = 48.8 Hz and
0.3·1.95/0.008 = 73.1 Hz, which matches their 49–73 Hz. At 52 Hz, A 8 mm and St 0.3:
52·0.008/0.3 = 1.39 m/s, which matches. On my own inputs (L 3.4 cm, A 6.8 mm) the 1.95 m/s target
needs 57–86 Hz, slightly worse for the fish.

Points of disagreement, kept as found:

1. **Target speed.** The project's own documents give three take-off speeds: 4.37 m/s in claim 24,
   and 1.95 m/s and 5.84 m/s in S24. My verdict depends on which one applies. At 4.37 m/s and at
   5.84 m/s, taxiing fails on frequency by 1.7× or more (calc), both in my derivation and theirs.
   At 1.95 m/s the author's own conclusion is **not refuted**. So the unqualified claim "surface
   taxiing cannot close the launch gap" is stronger than S24's own short answer for the 3-BL wing.
2. **Fish size.** S24 assumes a 4 cm fish but notes the measured fish were 33 mm TL. I used
   3.4 cm. A smaller fish needs a higher frequency, which strengthens the negative.
3. **Force side.** I cannot tell. I did not replicate it.

**Verdict.** I **AGREE** on the frequency arithmetic: same formula, the same numbers on their
inputs, and an independent Bainbridge cross-check at about 170 Hz for 4.37 m/s. I agree that for
any target of about 2.6 m/s or more no plausible corner reaches it at 52 Hz. I **CANNOT TELL** on
"not thrust force", because I derived no force. The headline "cannot close the gap" holds only for
the 1-BL wing (5.84 m/s) and the 4.37 m/s target. It does not hold for the 3-BL wing (1.95 m/s),
which S24 itself leaves open.

## Sources

- Taylor, Nudds & Thomas 2003, *Nature* 425:707. https://ideas.repec.org/a/nat/nature/v425y2003i6959d10.1038_nature02000.html (search-summary)
- Kyriakatos et al. 2011, *J. Neurosci.* 31:8422. https://pmc.ncbi.nlm.nih.gov/articles/PMC6623330 (full-text, automated fetch summary)
- Mwaffo et al. 2017, *PeerJ* 5:e4041. https://pmc.ncbi.nlm.nih.gov/articles/PMC5691796 (full-text, automated fetch summary)
- Bainbridge 1958, *J. Exp. Biol.* 35. https://www.scilit.net/publications/f507e958ae9b8f6d8b192b1a4bc7b310 (search-summary; page numbers differ between sources)
- Negative search, scope: I web-searched "adult zebrafish maximum tail beat frequency escape burst"
  and "adult zebrafish swim tunnel tail beat frequency amplitude". Neither search found a
  kinematic (video) measurement of adult tail-beat frequency above 21 Hz in steady swimming, or of
  adult tail-beat amplitude. I read no paper past the ones listed.

```swarm-replication
{"claim_id": 36, "my_value": "~170 Hz (range 87-257 Hz) needed at 4.37 m/s vs 52 Hz measured max; 49-73 Hz on S24's 1.95 m/s inputs", "agrees": true,
  "note": "Frequency arithmetic replicates exactly and the gap holds for the 4.37 and 5.84 m/s targets, but the force-side half was not replicated and S24 itself leaves the 1.95 m/s (3-BL) case unrefuted, so the unqualified headline overstates it."}
```
