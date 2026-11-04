# Challenge 126: adversarial review of S2-D-D ("fin-wing whole-animal L/D falls to 1.2–2.7")

**Claim under review** (from `harvest:deepen-s2-d-imobtp`, recorded evidence level *measured*):

> S2-D's model overpredicts the measured flying-fish L/D by about 2–4x. Back-solving gives an effective
> span efficiency of ~0.10–0.18, not the assumed 0.7. So a zebrafish-scale fin wing at AR 4 gets a
> computed whole-animal L/D of about 1.2–2.7 (1.0–3.6 over AR 1.5–8), not 3–5. VERDICT: falls.

**What I read.**
- `docs/research/fish/S2-D-deepen.md`, `S2DD_calcs.py` and `S2D_calcs.py`, all on branch
  `origin/claude/deepen-s2-d-imobtp`. Read-level: full-text.
- I re-ran the author's script unchanged. I also wrote my own independent back-solve and three
  relaxations; that script is described in §1 and §3.
- I ran no experiment. **Every number below that I produced is computed.** Sources carry read-levels.

**Verdict: WEAKENED.** I could not fault the arithmetic. The "falls" verdict, however, is carried by an
unstated transfer rule: that e is constant across AR. It is also carried by an uncorrected
specimen-method bias, and the source itself hints at that bias. Under an equally defensible transfer
rule, the band overlaps S2-D's 3–5. The recorded evidence level "measured" is wrong.

---

## 1. Independent arithmetic (computed)

I wrote a fresh back-solve from the closed form L/D_max = ½·√(π·e·AR / CD0), which gives
e·AR = (2·L/D)²·CD0/π. Its inputs are the same as the author's:
- Re 2×10⁴ at 12 m/s, which implies a chord of 25 mm;
- λ·Blasius wing friction;
- a laminar body with a 1.5 form factor.

| Quantity | Author | My recompute | Comment |
|---|---|---|---|
| Implied flying-fish chord | 25 mm | 25.0 mm | agrees |
| Model L/D_max over the author's grid | 9.7–16.6 | reproduced (script output) | agrees |
| Model ÷ measured, anchor 4.4 | "2–4×" | **2.2–3.8×** | agrees |
| Model ÷ measured, anchor 5.9 | "2–4×" | **1.6–2.8×** | low end is 1.6×, not 2×. Minor overstatement. |
| e·AR_eff, anchor 4.4 (AR 9, λ 1.4, 200×25 mm body) | 0.91 → e_eff 0.101 | 0.91 → 0.101 | agrees |
| e·AR_eff, anchor 5.9 (same case) | 1.63 → e_eff 0.181 | 1.63 → 0.181 | agrees |
| **e_eff over the author's own full input grid** (AR 9/10.7, λ 1.0/1.4/2.0, both bodies) | not reported | **0.063–0.143 (4.4); 0.114–0.257 (5.9)** | the headline "0.10–0.18" comes from a single grid cell. Across the author's own grid the range is **0.06–0.26**. |
| Zebrafish AR 4, attribution (A), anchor 4.4 / 5.9 | 2.09 / 2.68 | 2.09 / 2.68 | agrees |
| AR 4 band across attributions A–C | 1.2–2.7 | 1.17–2.68 | agrees. The low end, 1.17, comes from attribution (B), not from the e_eff in the KEY. |
| AR 1.5–8 band | 1.0–3.6 | 0.98–3.61 | agrees |

**Arithmetic: no fault**, apart from two items:
- the "2–4×" should read **1.6–3.8×**;
- the e_eff range is narrower than the author's own grid supports.

## 2. Proxy: the "effective span efficiency" is a residual, not a span efficiency

- e_eff is defined as whatever closes the gap between the parabolic-polar model and *one* wind-tunnel
  number. This is my inference.
- It therefore absorbs every unmodelled loss:
  - fins fixed in place on preserved specimens;
  - strut drag and blockage. Whether either was subtracted is `unknown`, per the author.
  - the 5° α grid;
  - body–fin interference;
  - camber or twist mismatch.
- Calling it "span efficiency" and then transferring it as a span-efficiency property of a fin wing is a
  proxy substitution. The quantity that matters is **the whole-animal L/D of a living (or designed)
  fin-wing glider at Re ~3×10³**. The author says this too, in §3c, and proposes a drop-glide test to get
  it.
- The author's own source points only loosely toward induced drag. Park & Choi say induced drag is "one
  of the dominant" components (full-text, via the author). That does not make it *all* of a 2–4× gap.

## 3. Hidden assumptions, relaxed (computed)

### 3a. The transfer rule: constant e versus constant e·AR

- The author transfers e_eff (a ratio) from geometric AR 9 to AR 4, which gives e·AR = 0.40–0.72.
  **This rule is not stated or justified anywhere.**
- Suppose instead that the shortfall is a saturated effective aspect ratio. For example, the body
  interrupts the span, or the tip vortices of a low-stiffness fin dominate, so that e·AR_eff stays
  ≈ 0.91–1.63 whatever the geometric AR.
- Under that rule, the author's `solve()` returns:

| Transfer rule | Zebrafish whole-animal L/D at AR 4 (computed) |
|---|---|
| constant e_eff (author) | 2.09–2.68 |
| constant e·AR_eff | **2.96–3.80** |
| constant measured/model ratio (0.27–0.60 × S2-D's 4.80) | 1.30–2.88 |

Under the second rule, which is no less defensible, **the upper end returns into S2-D's 3–5 band**.

The headline "not 3–5" depends on which transfer rule is chosen. That choice is an assumption, and
nothing in the source constrains it.

### 3b. Specimen-method bias: the source points at it, and the author did not correct for it

The author lists "preserved fins … biases the measurement against fin wings" as a limitation. The full
deficit is nevertheless attributed to the fin-wing physics.

New evidence from my search, at **read-level search-summary**:
- The IUTAM 2007 version of Park & Choi compares its max L/D ≈ 4.4 (model 3) with **hawk 3.8 and
  petrel 4.0**, citing a reference [10] that I could not see.
- The host pages were could-not-access in this session: `typeset.io` and
  `eng-web77-v02.ocio.monash.edu` both fail to resolve.

My inference, flagged as such:
- Hawk and petrel at ~4 are far below what I remember for live gliding birds. My recollection, which
  is **remembered, not retrieved**, is that Tucker & Parrott 1970 gave a Laggar falcon max L/D of
  about 10.
- If that recollection is right, the comparator values come from a prepared-specimen or detached-wing
  method that also under-reads live animals.
- In that case the 4.4 benchmark sits inside a measurement class that under-reads live gliders by a
  similar factor of about 2–3×.
- Part or all of the "model overpredicts by 2–4×" would then be a property of the platform, not of fin
  wings.
- Reference [10]'s identity is `unknown`, so this remains an inference.

Sensitivity to a specimen under-read factor f (computed; AR 9, λ 1.4, 200×25 mm body; e capped at 1):

| f | anchor 4.4 → e_eff → zebrafish L/D at AR 4 | anchor 5.9 → e_eff → L/D |
|---|---|---|
| 1.0 (author) | 0.10 → 2.09 | 0.18 → 2.68 |
| 1.5 | 0.23 → 2.95 | 0.41 → 3.80 |
| 2.0 | 0.40 → 3.78 | 0.72 → 4.88 |
| 2.6 | 0.68 → 4.73 | 1.00 (cap) → 5.63 |

- **At f ≈ 2, S2-D's original 3–5 band is recovered.**
- The author's own reversal condition says a Table 2 value of ≥ ~8 would reverse the verdict. A
  corrected value of 4.4 × 2 = 8.8 meets it.
- The verdict therefore hinges on an unmeasured correction. The author acknowledged the possibility of
  this correction but set it to 1.

### 3c. Re transfer

The author flags the transfer from Re 2×10⁴ to Re 3×10³ as an assumption. I agree, and I have nothing
to add beyond this:
- S2-D's model already carries the Re dependence through λ·Blasius.
- A residual calibrated at 2×10⁴ may therefore double-count or under-count viscous losses at 3×10³.
- The direction is `unknown`.

## 4. Evidence level

- The claim is recorded as **measured**. That is a defect.
- Every number in the claim is **computed**:
  - the 2–4× ratio is model ÷ anchor;
  - e_eff is a back-solve;
  - 1.2–2.7 is a forward model.
- The only measured input is the flying-fish L/D. Its numeric value is at **search-summary** level
  (4.4) or was relayed by S2 (5.9). Table 2 of the JEB paper was not read, by the author or by me.
- The correct label is: *computed, calibrated on a search-summary measurement, with an assumed
  transfer.*
- The author's own document labels this honestly ("on a search-summary anchor, with an assumed
  transfer"). The defect is in the harvested record, not in the source text.

## 5. Regimes and counter-examples

- **Counter-example (search-summary):** the same measurement line puts hawk and petrel at 3.8–4.0.
  Read literally, the identical model-vs-anchor logic would also "show" that bird wings have
  e_eff ≈ 0.1. That conclusion would be absurd for live birds, if my remembered live-raptor values hold.
  This is the strongest reason to doubt that the residual is a fin-wing property. (Inference.)
- **Live flying fish.** Field glide-angle data for live Exocoetidae would be the right comparator. I
  did not retrieve any. Scope of that negative: two web searches only, both centred on Park & Choi;
  no dedicated field-glide search was made. The value is `unknown`.
- **Sub-claim "insect-only 6–7 ceiling strengthens": weakened, not strengthened.** The argument is
  that flying fish at AR 9–10.7 reach only 4.4–5.9. That argument inherits the same specimen bias. If
  f ≈ 1.5–2, the corrected flying-fish L/D is 6.6–11.8, which reaches or exceeds 6–7.
- **Sub-claim "L/D barely matters from 0.5 m": survives.** I re-ran the integrator: 23.1 BL at L/D 4.8,
  19.8 BL at L/D 1.5, and 16.0 BL ballistic. Those are computed values, and they agree with the author.
  The sub-claim is insensitive to everything above.

## 6. Verdict

**WEAKENED.**
- The arithmetic reproduces.
- The headline "1.2–2.7, not 3–5" is not robust:
  - **Transfer rule:** holding e·AR_eff constant instead of e gives 3.0–3.8 at AR 4 (computed).
  - **Specimen bias:** a specimen under-read of f ≈ 2 restores 3.8–4.9 (computed). The source's own
    bird comparators (hawk 3.8, petrel 4.0; search-summary) make that bias plausible.
- The e_eff range is wider than reported, at 0.06–0.26 over the author's own grid.
- The evidence level should be *computed on a search-summary anchor*, not *measured*.
- What survives:
  - the model has never been validated against any fin wing;
  - the S2-D band is at best uncertain;
  - "L/D barely matters from 0.5 m".

**Corrected statement (computed):** zebrafish-scale fin wing at AR 4, whole-animal L/D ≈ **1.2–3.8**.
- The value depends on the transfer rule.
- It rises to ~4.9 if the preserved-specimen benchmark under-reads by 2×.
- e_eff ≈ 0.06–0.26, and it is a lumped residual rather than a span efficiency.
- The decisive measurement is unchanged from the author's proposal: a drop-glide test of a
  zebrafish-scale replica, or a read of Park & Choi Table 2 together with the identity of IUTAM
  reference [10].

**Hosts to allow in the session's network settings to go further:** `typeset.io`,
`eng-web77-v02.ocio.monash.edu`, `koreascience.kr`.

## Sources

| Source | Read-level |
|---|---|
| S2-D-deepen.md, S2DD_calcs.py, S2D_calcs.py (branch `claude/deepen-s2-d-imobtp`) | full-text |
| Park & Choi 2010 *J Exp Biol* 213:3269 (statements relayed by the author) | via author (full-text body per author); not re-read by me |
| Park & Choi IUTAM 2007 "S1_Park.pdf": max L/D ≈ 4.4 (model 3); hawk 3.8, petrel 4.0 citing ref [10] | search-summary (host could-not-access) |
| Korean 2008 congress version: ≈ 4.4 for model C, "similar to petrel and hawk" | search-summary (koreascience.kr not fetched) |
| Press coverage (phys.org, ScienceDaily, EurekAlert 2010): "glide as well as birds such as petrels and wood ducks" | listing |
| Tucker & Parrott 1970, live falcon L/D ~10 | **remembered, not retrieved**. Used only to motivate the bias hypothesis. |

```swarm-challenge
{"claim_id": 126, "outcome": "weakened", "reason": "Arithmetic reproduces, but the 'falls to 1.2-2.7' headline rests on an unstated constant-e transfer rule (constant e*AR gives 3.0-3.8) and on an uncorrected preserved-specimen benchmark whose own bird comparators (hawk 3.8, petrel 4.0, search-summary) suggest a ~2x under-read that would restore 3.8-4.9; the evidence level is computed-on-search-summary, not measured.", "corrected_value": "zebrafish AR-4 whole-animal L/D ~1.2-3.8 (computed, transfer-rule dependent; ~4.9 if specimen under-read is 2x); e_eff 0.06-0.26 over the author's own input grid (lumped residual, not span efficiency)", "depends_on": ["S2DD_calcs.py / S2D_calcs.py model as published on branch claude/deepen-s2-d-imobtp (re-run, reproduced)", "Park & Choi flying-fish max L/D ~4.4 (search-summary) and S2-relayed 5.9", "Park & Choi 2010: AR 9.0-10.7 and Re 1.9-2.2e4 at 12 m/s (full-text via author)", "Park & Choi IUTAM 2007 comparator values hawk 3.8, petrel 4.0 citing unseen ref [10] (search-summary)", "remembered (not retrieved) live-raptor glide L/D ~10 (Tucker & Parrott 1970), used only to motivate the specimen-bias relaxation", "assumed flying-fish body 200 x 25-35 mm (author's assumption, reused)", "alternative transfer rule: constant e*AR_eff (assumption, as unsupported as the author's constant e)", "S2/S2-D point-mass glide integrator, 0.5 m drop, 2 m/s launch"]}
```
