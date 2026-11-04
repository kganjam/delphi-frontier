# Challenge 227: adversarial review of S29's "energy per stroke is the binding term"

**Claim under review** (S29-organism.md §5 and §6, commit `44ed2195`, branch `claude/s29-launch-energy-2iuixr`):

> ENERGY PER STROKE IS THE BINDING TERM: one-sided axial muscle (30% body) at the best measured spring-loading work (frog 53, max 81 J/kg muscle) supplies only 54-82% of need. The muscle would have to store 98.5 J/kg against the 8.6 J/kg it effectively delivers today, an 11.5x gap, and slow loading buys only 3.7-9.4x.

- Recorded evidence level: **derived**.
- Recorded value: **98.5 J/kg muscle required**.

**Status of this review:** derived. I re-did the calculation on S29's stated inputs, ran sensitivity tests and searched the literature. **I made no new measurement.**

**Verdict: WEAKENED, and only on the secondary framing.**

- **The headline survives.** I reproduced the 98.5 J/kg requirement and the 54–82 % supply figure exactly. The "derived" label on them is honest.
- **The comparison to "today" does not hold as stated.** The 8.6 J/kg is not something the muscle is measured to deliver per stroke. It is built from a *swimming* burst speed and charged to a single one-sided stroke. So the "11.5× gap" and "slow loading buys 3.7–9.4×" are ratios against an unmeasured proxy. The 3.7–9.4× is also a frog-over-fish ratio, not a gain measured in any one muscle.
- **The binding conclusion rests almost entirely on one input.** That input is a pike efficiency transferred to zebrafish, η_h = 0.37. If η_h is 0.45 or higher, the best measured frog value already closes the gap.

---

## 1. Independent arithmetic

I worked from S29's stated inputs: V = 4.37 m/s, m = 0.40 g, Cd 0.2, A = 24 mm², stroke s = 1.09 cm, η_h = 0.37, η_spring = 0.93, f = 0.30, w = 32/53/81 J/kg. I computed in Python from scratch and did not reuse S29's script.

| Quantity | My value | S29 | Match |
|---|---|---|---|
| KE per kg body, ½V² | 9.548 J/kg | 9.55 | yes |
| Drag work over the stroke, ½ρCdAV²·s/2 ÷ m | 0.624 J/kg | 0.250 mJ = 0.625 J/kg | yes |
| Need at the body | 10.173 J/kg | 10.17 | yes |
| Required w = 10.173 / (0.30 · 0.93 · 0.37) | **98.55 J/kg muscle** | 98.5 | yes |
| Supply ÷ need at w = 32 / 53 / 81 | 0.325 / 0.538 / 0.822 | (×0.32 / 0.54 / 0.82) | yes |
| "Today": ½·1.38² / 0.37 / 0.30 | 8.578 J/kg muscle | 8.6 | yes |
| 98.5 / 8.58 | 11.48× | 11.5× | yes |
| 32 / 8.58 and 81 / 8.58 | 3.73× and 9.44× | 3.7–9.4× | yes |

**No arithmetic error.**

**Units are consistent.** The 98.5 J/kg is energy *stored* per kg of muscle, which is the same quantity Mendoza & Azizi 2021 report. The muscle must do at least that much work to store it. That makes the like-for-like comparison with "muscle work today" valid in kind: the 11.5× contains the 10.0× KE ratio, plus 6.5 % for drag, plus 1/0.93 for spring loss.

## 2. Proxy check

**The proxy in the binding comparison (98.5 vs 32–81 J/kg) is reasonable.**
- Mendoza & Azizi measured energy stored in a series tendon per kg of muscle, in a single slow contraction. That is the right quantity for a single-load spring.
- The limitation is taxon: frog plantaris standing in for teleost fast myotomal muscle. S29 discloses this as ASSUMED (§7).

**The proxy in the "today" comparison (8.6 J/kg) is weak.** This is my finding, not the author's.
- S28 (§2 table, line 26) labels the 1.38 m/s figure as a **swimming burst** from Miln et al. 2021 (n = 50), "not water-exit speed". It is not a single C-start from rest.
- A swimming burst speed is built up over several tail beats driven by **both** sides alternately, while drag is acting. Charging all that KE to one stroke of one side's muscle at η_h 0.37 is therefore not a per-stroke muscle work. The real quantity, per-stroke myotomal work in a zebrafish fast-start, is **unknown**. Neither S29 nor I read a source for it.
- If the KE came from two half-strokes, one per side, the per-side figure is about 4.3 J/kg (my inference). On that reading, the "gap" would be about 23× and frog-like slow loading would "buy" 7.5–19×.

**Consequence.** The 11.5× and the 3.7–9.4× have the wrong denominator to support the word "only". Ironically, the uncertainty could make slow loading look *better* than S29 says, not worse. This does not change the binding comparison in §1, which never uses the 8.6.

"Slow loading buys 3.7–9.4×" is also stated as if it were a measured gain of slow over fast loading. It is not. It is frog spring-loading work divided by a derived fish swimming proxy, so it compares different taxa, contraction modes and muscles. A real slow-loading gain needs both kinds of contraction measured in the **same** muscle. I found no such measurement for any teleost (search scope in §5).

## 3. Hidden assumption that carries the result: η_h

The requirement is w_req = 10.17 / (0.30 · 0.93 · η_h). I relaxed η_h, with all else held at S29's values:

| η_h | w required (J/kg muscle) | Closes with frog max 81? | Closes with frog mean 53? |
|---|---|---|---|
| 0.27 (pike S-start, S29's own range) | 135.0 | no | no |
| **0.37 (S29 central)** | **98.5** | no (×0.82) | no (×0.54) |
| 0.45 | 81.0 | **break-even** | no |
| 0.50 | 72.9 | yes | no |
| 0.60 | 60.8 | yes | no |
| 0.69 | 53.0 | yes | **break-even** |
| 1.00 (no drag either: floor) | 34.2 | yes | yes |

**What the table shows** (my inference):
- Without η_h, frog-grade slow loading of one-sided muscle passes **even at the frog mean**. So the claim is really "energy per stroke × η_h is binding". S29's §0 and §6 say exactly that, but the claim sentence drops the η_h half.
- Break-even at w = 81 needs η_h ≥ 0.45, only 1.2× the pike value.
- The pike value transfers to zebrafish across a large size and Reynolds-number gap. It is also measured for a full C-start (stage 1 + stage 2), not for a single spring release.

**Why the direction of an η_h error is unknown.** A ~5 ms single-impulse release could shed more wake than a muscle-driven C-start, which would lower η_h. Equally, a spring release has no stage-1 turning phase, which could raise it. I found no measurement either way: **unknown**. S29 already names zebrafish C-start PIV as test 2, so this is a disclosed sensitivity, not a concealed one. It does mean the "binding" conclusion is a ~1.2× call resting on one transferred efficiency.

**Other assumptions, relaxed:**
- **f = 0.30 (one side, ASSUMED as half of a SECONDARY 60 %).** At w = 81 and η_h 0.37, break-even needs f = 0.37. That reproduces S29's §5 figure.
- **Single stroke.** A ratcheted spring loaded by several contractions would remove the per-stroke limit altogether. S29 scopes its claim to "a single stroke", so this is outside the claim rather than a defect in it. I did not search for a biological ratchet-loaded locomotor spring, so I make no claim about whether one exists.
- **Target speed.** At the mass-consistent 5.53 m/s, which S29 flags itself, w_req = 157.7 J/kg (my arithmetic). That makes the claim *more* negative, so it is optimistic as disclosed.

## 4. Evidence level

- **"derived" on 98.5 J/kg is honest.** S29 labels every input MEASURED, SECONDARY or ASSUMED, and labels §5's "today" framing "derived" in the sentence.
- **One wording defect.** "The 8.6 J/kg it effectively delivers today" reads as a measured property of the muscle. It is a derived proxy, and it rests on a swimming-burst speed that S28 itself says is not a per-stroke or exit quantity. The word "effectively" does not tell the reader that.

## 5. Counter-examples searched

**Locust (*Schistocerca gregaria*) jump, Bennet-Clark 1975, J. Exp. Biol. 63:53.**
- **Read level: search-summary.** Fetches of PubMed and Semantic Scholar failed because the session's network policy did not allow those domains.
- Per the search summary: jump energy is 9 mJ (males) and 11 mJ (females), 14 mJ is stored across both hind legs, and the extensor tibiae is ~80 mg per leg.
- **Derived here, not reported by the source:** 9–14 mJ ÷ 0.16 g gives **56–88 J/kg muscle**.
- This brackets the frog 53–81 range and does **not** exceed 98.5. It is consistent with the claim, not a counter-example.
- Caveat: Gabriel 1985, cited in the same search summary, says the stores hold the energy of "70 mg of muscle" without saying whether that is per leg or in total. If it were the total, the figure would be ~160 J/kg. I could not resolve this, so I do not use it.

**Mendoza & Azizi 2021 (PMC10658917).**
- **Read level: full-text,** via the PMC page, read through a summarising fetch.
- Confirms Cuban tree frog 53 J/kg mean, 32–81 J/kg range. Cane toad 22 and bullfrog 37 J/kg are lower.
- The same paper cites Olberding & Deban 2018 at "up to 73 J/kg" for the same muscle. That value is SECONDARY, and it does not exceed 81.

**Scope of the negative search.** Two standard web searches, one extended web search and two page fetches. Galago, flea, click-beetle and mantis-shrimp per-muscle *energy*, as distinct from power, were **not** searched. A counter-example above 98.5 J/kg muscle in those taxa is not excluded.

## 6. Bottom line

| Part of the claim | Outcome |
|---|---|
| 98.5 J/kg muscle required (derived) | **Survives.** Arithmetic and level are correct |
| Frog 53/81 J/kg supplies 54–82 % of need | **Survives** |
| "Binding" | **Survives conditionally.** It flips if zebrafish η_h ≥ 0.45 (w = 81) or ≥ 0.69 (w = 53). That input is a transferred pike value |
| "8.6 J/kg it effectively delivers today", "11.5× gap" | **Weakened.** The denominator is a swimming-burst proxy charged to one side and one stroke. True per-stroke work is unknown |
| "Slow loading buys only 3.7–9.4×" | **Weakened.** It is a cross-taxon ratio against that proxy, not a measured slow-vs-fast gain. "Only" is not supported |

```swarm-challenge
{"claim_id": 227, "outcome": "weakened", "reason": "The 98.5 J/kg-muscle requirement and 54-82% supply reproduce exactly and are honestly labelled derived, but the 8.6 J/kg 'today' denominator (hence the 11.5x gap and 'slow loading buys only 3.7-9.4x') charges a multi-beat swimming-burst speed (S28: not a per-stroke or exit quantity) to one stroke of one side and compares frog to fish, and the 'binding' verdict flips if zebrafish eta_h >= 0.45 versus the transferred pike 0.37.", "corrected_value": null, "depends_on": ["S29 inputs: V_exit 4.37 m/s (S28), Cd 0.2, A 24 mm^2, s 1.09 cm", "Frith-Blake pike C-start eta_h 0.37 (0.27-0.39)", "Ker1981 tendon return 0.93", "Mendoza-Azizi2021 frog 32-81 J/kg muscle (full-text via PMC)", "F_ONE_SIDE 0.30 (assumed)", "Miln2021 1.38 m/s swimming burst, labelled by S28 as swimming not exit speed", "Bennet-Clark1975 locust 9-14 mJ, ~80 mg extensor per leg (search-summary only)"]}
```
