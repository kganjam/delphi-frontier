# Challenge 94: adversarial review of S2-D-D ("S2-D's whole-animal L/D 3–5 falls")

**Claim under review (harvested).** "S2-D-D deepen FALLS S2-D's whole-animal L/D 3–5: model
overpredicts the flying-fish measured L/D (Park & Choi 2010; max 4.4 search-summary, 5.9 relayed) by
~2–4×; back-solved span efficiency 0.10–0.18 vs assumed 0.7; zebrafish-scale AR 4 gives L/D ~1.2–2.7
(1.0–3.6 over AR 1.5–8). Back-solve NOT re-derived by harvester (S2D_calcs.py not run); Re transfer to
3e3 is an assumption." Recorded evidence level: *derived*, value 1.95 (midpoint of 1.2–2.7).

**Source read.** `docs/research/fish/S2-D-deepen.md`, `S2DD_calcs.py` and `S2D_calcs.py` on branch
`claude/deepen-s2-d-imobtp` (commit `c584a1ec`): full-text. I confirmed that the `S2D_calcs.py` copy is
byte-identical to the one on `claude/deepen-s2-lift-drag-6xxrv3` (`diff`, no output).

**Verdict: WEAKENED.** The direction holds. S2-D's model overpredicts the only measured fin-wing
animal, so a fin wing at AR 4 probably sits below S2-D's 4.1–5.5. But the specific "1.2–2.7, falls"
depends on a transfer rule the author did not state or test. Under an equally simple alternative rule,
the calibrated AR-4 value is **2.95–3.8 (computed)**, which lies inside S2-D's 3–5 band.

---

## 1. Independent arithmetic (computed)

First I ran the author's script, `python3 -I S2DD_calcs.py`, against the verbatim `S2D_calcs.py`.
Every table in S2-D-D §1, §3b and §4 reproduces to the printed digit. That clears the harvester's
caveat "S2D_calcs.py not run".

I then wrote `challenge-94_calcs.py`. It is self-contained: it re-types S2-D's inputs and imports
neither author script. A control in it reproduces S2-D's AR-4 value of 4.80.

**Hand checks:**
- chord = Re·ν/U = 2×10⁴ × 1.5×10⁻⁵ / 12 = **25.0 mm**.
- Two-sided Blasius at 2×10⁴ is 0.01878, and ×1.4 gives **0.0263**.
- At AR 9, the wing area is 5.625×10⁻³ m².
- For the 200 × 25 mm body:
  - wetted area = 0.0118 m²;
  - Re_L = 1.6×10⁵, so C_f = 0.00332;
  - CdA = 1.5 × C_f × wetted area = 5.87×10⁻⁵ m², which is 0.0104 on wing area.
- CD0 = 0.0367, so L/D_max = ½·√(π·0.7·9 / 0.0367) = **11.6**. This matches the author's value.
- e·AR needed for an L/D of 4.4 = (8.8)² × 0.0367 / π = **0.905**, so e_eff = **0.101**. This matches.

**Results across the author's own flying-fish grid** (AR 9/10.7 × λ 1.0/1.4/2.0 × body 25/35 mm):

| anchor | measured ÷ model | overprediction | e_eff | e·AR_eff |
|---|---|---|---|---|
| 4.4 (search-summary) | 0.30–0.45 | 2.2–3.3× | 0.063–0.143 | 0.68–1.29 |
| 5.9 (relayed by S2) | 0.40–0.61 | **1.7–2.5×** | 0.114–0.257 | 1.22–2.31 |

The author also included e = 0.9 in the forward model, which widens the 4.4 row to 0.27–0.45.

There is one small inaccuracy in the harvested claim: **"~2–4×" holds only for the 4.4 anchor.** On the
5.9 anchor, the model overpredicts by 1.7–2.5×. The source's own ratio of 0.36–0.60 for 5.9 agrees
with this.

## 2. Proxy: "span efficiency" is not what was back-solved

The back-solve puts the *entire* model-vs-measurement gap into the induced-drag term. The quantity it
produces is therefore a **whole-configuration lift-dependent drag factor**, i.e. an Oswald factor. That
factor absorbs:
- lift-dependent viscous pressure drag at Re 2×10⁴;
- body–fin and pelvic-fin interference;
- non-planar fin rays;
- any error in the 4.4 itself.

It is not lifting-line span efficiency. A planar wing with e ≈ 0.1 would need a span loading far from
anything lifting-line theory gives (inference). Calling it "span efficiency 0.10–0.18" invites a
reader to treat it as a planform property that can be carried to another AR. That carry-over is
exactly the step §3 tests. The right name is **effective Oswald factor of the whole flying-fish model
at Re 2×10⁴**.

## 3. The hidden assumption that carries the result: how e_eff is transferred to AR 4

To get from the flying fish to AR 4, the author keeps the **ratio** e_eff = e·AR_eff / AR_geom fixed. This
is not stated as an assumption. The stated assumptions concern only Re and size. If instead the
flying-fish shortfall works as a ceiling on **effective** aspect ratio, the absolute e·AR_eff carries
over, which this approach does not exclude. Such a ceiling could come from tip vortices or a body
gap, and then a longer span buys little. The two rules give (computed, `challenge-94_calcs.py`; zebrafish λ 1.4, CL cap 0.9):

| anchor | rule (i), the author's: e_eff ratio | rule (ii): absolute e·AR_eff |
|---|---|---|
| 4.4 | 2.09 | **2.95** |
| 5.9 | 2.68 | **3.80** |

Two other relaxations:
- **Rule (i) over the full flying-fish grid × zebrafish λ 1.0–2.0:** 1.47–2.77 for the 4.4 anchor and
  1.88–3.57 for the 5.9 anchor. The author's single central case (AR 9, λ 1.4, 25 mm body) is a narrow
  slice of their own input space.
- **The low end, 1.17, comes from attribution (B), wing CD0 × 9.3, i.e. CD0_wing ≈ 0.245.** The author
  rejected attribution (C) for needing a body CD of 2.6. A thin fin plate at α ≈ 0 with CD0 ≈ 0.25 at
  Re 2×10⁴ is about as implausible (my inference; laminar Blasius is 0.019 there). Yet (B) was kept and
  sets the lower bound of the harvested 1.2–2.7.

**Net (computed):** the calibrated AR-4 L/D ranges from ~1.2 (B, 4.4) to ~3.8 (rule ii, 5.9).
Excluding (B) on the same grounds as (C) gives **~1.5–3.8**. The upper part overlaps S2-D's 3–5 band.
So the band does not clearly "fall": it is pushed down and widened. Which transfer rule is right is
`unknown`. No source either of us reached measures e or e·AR for fin wings at two different ARs.

## 4. Evidence level

- The value 1.95 labelled *derived* is honest that it is computed, not measured.
- But **1.95 is the harvester's midpoint, not an author number.** The source's central statement is
  "most likely ~2 at AR 4", taken from attribution (A). The midpoint averages across attributions the
  source itself ranks unequally, including one I argue is unphysical (§3). It should not be carried as
  a point estimate.
- The anchor 4.4 is still **search-summary**. My attempt:
  - Fetched journals.biologists.com/jeb/article/213/19/3269/9762/ in full: full-text body, two passes.
    It has **no numeric L/D in the text**, and Table 2 is an image.
  - Got the same 4.4 again by web search: the IUTAM 2007 version, "model 3", "greater than hawk (3.8)
    and petrel (4.0)". Read-level: search-summary.
  - typeset.io could not be accessed: the host did not resolve in this session.
- The JEB text says, in the authors' words, that performance is "comparable to those of wings of birds
  such as the hawk, petrel and wood duck". This is *qualitatively* consistent with 4.4. It does not
  raise the number's read-level.

## 5. Things the author missed

1. **Strut drag was subtracted.** S2-D-D lists "whether strut drag was subtracted" as `unknown`. The
   JEB full text, which the author says they read, states: "The lift, drag and pitching moment on the
   struts alone were separately measured" and "used for the correction". So that limitation is
   resolved in favour of the measurement. I found no statement on blockage correction, so that stays
   `unknown`.
2. **The comparator birds are probably detached wings.** Park & Choi's reference list includes Withers
   1981, "An aerodynamic analysis of bird wings as fixed aerofoils" (title only, read at listing level
   inside the JEB text). If hawk 3.8 and petrel 4.0 come from that kind of preparation, then 4.4
   belongs to a class of measurements on fixed, preserved wings. Live gliding birds measure much
   higher L/D (remembered, not retrieved: Tucker & Parrott 1970 falcon, also cited by Park & Choi).
   This is my inference. It sharpens the author's limitation 2: preserved-specimen L/D may be a
   *lower bound* on what a designed fin wing achieves. That further weakens the transfer.
3. **A conflict with the source's sub-claim (a).** The JEB text says the fish's performance "is better
   than that of flying insect wings" (full-text, authors' claim). The source says S2-D's "6–7 is an
   insect number" *strengthens*. But Park & Choi themselves place insect wings *below* about 4.4. These
   two sources disagree, and I keep the disagreement rather than resolve it. It is outside claim 94's
   number, but it bears on how the 4.4 is read: if insect wings also measure low at these Re, the
   shortfall may be a generic low-Re effect rather than a fin effect. That would *support* the Re
   transfer, which partly offsets point 2. (Inference.)

## 6. What survives

- Both independent recomputation and the original script reproduce S2-D-D's arithmetic.
- S2-D's parabolic-polar model, with e = 0.7, does overpredict the flying fish: by 1.7–3.3× on either
  anchor, or 2.2–3.3× on the 4.4 anchor alone.
- At AR 4, the calibrated L/D lies below S2-D's 4.1–5.5 under every rule I tried (computed).

## 7. What does not survive as stated

- "Falls" and "1.2–2.7". Under an equally simple, untested transfer rule, AR 4 gives 2.95–3.8, which is
  inside the 3–5 band.
- "~2–4×" on the 5.9 anchor, where it is 1.7–2.5×.
- The midpoint 1.95 as a point value.

The decisive test is unchanged from the source's own suggestion: a drop-glide of a zebrafish-scale
replica measures whole-animal L/D at the right Re with no transfer rule at all.

## Sources

| Source | Read-level |
|---|---|
| S2-D-deepen.md, S2DD_calcs.py, S2D_calcs.py (branch `claude/deepen-s2-d-imobtp`, commit c584a1ec) | full-text (scripts executed) |
| S2D_calcs.py (branch `claude/deepen-s2-lift-drag-6xxrv3`), byte-compared | full-text |
| Park H, Choi H (2010) *J Exp Biol* 213:3269, doi 10.1242/jeb.046052, journals.biologists.com page | full-text body (Table 2 and figures are images; no numeric L/D in the text) |
| Park & Choi IUTAM 2007 (max L/D ≈ 4.4, model 3; hawk 3.8, petrel 4.0) | search-summary (eng-web77-v02.ocio.monash.edu not fetched; the author found it unresolvable) |
| Withers 1981 *J Exp Biol* 90:143; Tucker & Parrott 1970 *J Exp Biol* 52:345 | listing (titles in Park & Choi's reference list); falcon L/D is remembered, not retrieved, and not used numerically |
| typeset.io PDF of Park & Choi 2010 | could-not-access (host not resolvable in this session) |

```swarm-challenge
{"claim_id": 94, "outcome": "weakened", "reason": "The arithmetic reproduces independently and S2-D's model does overpredict the flying fish (1.7-3.3x across anchors, not 2-4x for 5.9), but the 1.2-2.7 'falls' result rests on an unstated rule that carries e_eff as a ratio of geometric AR; carrying the back-solved e*AR_eff as an absolute value instead gives a computed AR-4 L/D of 2.95-3.8, inside S2-D's 3-5 band, and the 1.2 low end comes from a wing-CD0 attribution (x9.3) as unphysical as the body attribution the author rejected.", "corrected_value": "computed whole-animal L/D at AR 4 = ~1.5-3.8 (transfer-rule dependent; ~1.2 only under the implausible CD0x9.3 attribution); no meaningful point value", "depends_on": ["S2D_calcs.py S2-D model and inputs (0.4 g, S=9 cm^2, chord 15 mm, 32x7x4 mm body, form 1.5, lam 1.4, CL cap 0.9), branch claude/deepen-s2-lift-drag-6xxrv3", "Park & Choi 2010 JEB: Re 1.9-2.2e4 on mean chord at 12 m/s, pectoral AR 9.0-10.7 (full-text)", "Park & Choi flying-fish max L/D ~4.4 (search-summary, IUTAM 2007) and 5.9 (relayed by S2)", "S2-D-D assumed flying-fish body 200 x 25-35 mm", "Park & Choi 2010 JEB: strut forces measured separately and used for correction (full-text)", "Park & Choi 2010 JEB authors' claim: performance better than flying insect wings, comparable to hawk/petrel/wood duck wings (full-text)", "assumption: shortfall transfers from Re 2e4 to ~3e3 (inherited from S2-D-D; untested)", "my inference: CD0_wing ~0.245 at alpha~0, Re 2e4 is unphysical vs Blasius 0.019"]}
```
