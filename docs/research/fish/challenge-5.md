# Challenge 5: "Re is pinned at ~2e3–4e3 by body weight, so C_L,max is probably ≤ 0.6"

**Claim under attack** (from `docs/research/fish/zebrafish-glide-physics.md`, §1 and §5, on branch
`origin/claude/zebrafish-glide-physics-j176og`):

> "Reynolds number is pinned at ~2e3–4e3 by body weight, so CL_max is probably ≤ 0.6; the value at
> that Re is unknown." Evidence level as recorded: *derived*. Value: 3000 Re.

**Reviewer's status:** I ran no experiment and built no wing. Every number below is labelled as one
of four things: calculated by me, measured by others and relayed to me, simulated by others, or my
own inference. Read-levels follow the brief's scale.

**Verdict in one line:** **weakened.** The Reynolds half is right: I redid the arithmetic and it
survives. The C_L,max half does not hold up. The ≤ 0.6 ceiling comes from a proxy that is
probably a thick NACA 0012 section at Re ≈ 2e4. The measurements that do exist for thin wings at
Re 7e2–1e4 report a steady C_L,max of about 0.9–1.15, and that agrees with this repository's own
`S2-low-reynolds-aero.md`. The correction does not overturn the parent report's overall verdict,
for the reason given in §6.

---

## 1. Arithmetic: redone independently. It survives.

**Calculated (mine).** I size a wing to carry W at lift coefficient C_L and speed V:
S = 2W/(ρV²C_L). With chord c = √(S/AR):

Re = V·c/ν = V·√(2W/(ρV²C_L·AR))/ν = √(2W/(ρ·C_L·AR)) / ν. The V terms cancel exactly.

Inputs: W = 4.0e-4 kg × 9.81 = 3.924e-3 N, ρ = 1.2 kg/m³, ν = 1.5e-5 m²/s.

| C_L \ AR | 1 | 2 | 3 | 5 | 8 |
|---|---|---|---|---|---|
| 0.6 | 6,960 | 4,922 | **4,018** | **3,113** | 2,461 |
| 0.8 | 6,028 | 4,262 | 3,480 | 2,696 | 2,131 |
| 1.0 | 5,391 | 3,812 | 3,113 | 2,411 | **1,906** |
| 1.5 | 4,402 | 3,113 | 2,542 | 1,969 | 1,556 |

The author's figures are 3,113 at (0.6, 5) and a range of 1,906–4,018 over AR 3–8 and C_L 0.6–1.0.
I reproduce all three exactly. **The arithmetic is correct.**

## 2. Hidden assumptions in the Re half: named and relaxed

1. **"Pinned" holds only at the design point.** V cancels only because the wing is sized so that
   it flies at C_L. A wing that already exists has a fixed S, so its Re rises in proportion to V
   once it flies faster at a lower C_L. Example (calculated): a 3.2 cm², AR 5 wing (c = 8 mm)
   flying at 8 m/s has Re = 4,267. The claim is right for the case it is used in, which is the
   minimum-size wing at its operating C_L. It is not a general cap.
2. **Aspect ratio is the main free variable, and the claim's AR 3–8 range leaves out the
   fin-like case.** A pectoral-fin-derived wing is plausibly low-AR. `S2-low-reynolds-aero.md`
   assumes a per-wing span/chord of about 2. At AR 1–2, Re rises to 4,900–7,000 at C_L 0.6
   (calculated). That stays below 1e4, so the regime does not change.
3. **Weight includes the wing.** Re ∝ √W, so a 50 % mass increase from the membrane raises Re by
   only 22 % (calculated: 3,113 → 3,812 at C_L 0.6, AR 5).
4. **The C_L in the Re formula is circular with the C_L,max conclusion.** A higher C_L lowers Re,
   but only as C_L^-½. Using C_L = 1.07 instead of 0.6 moves the design Re from 3,113 to 2,331 at
   AR 5 (calculated).

**Net (inference):** relaxing every assumption gives a design-point Re of about 1.5e3–7e3, all
inside 1e3–1e4. "Re ≈ 2e3–4e3" is a fair central band for AR 3–8. **This half survives.**

## 3. Input data: a proxy is setting the C_L,max ceiling

The author gives one retrieved number as the basis for the ≤ 0.6 ceiling: Laitone (1997),
"C_L,max at stall rose from 0.455 to 0.59 when tunnel turbulence changed, at Re ≈ 20,700". The
author notes that the summary "did not identify which section produced the 0.455/0.59 values".

What I retrieved about Laitone 1997 (*Exp. Fluids* 23:405, doi 10.1007/s003480050128; read-level
**search-summary**, relaying an abstract and full-text excerpt; my direct fetch of the Springer PDF
failed because `link.springer.com` does not resolve in this session):
"The 5% camber and all of the thin plates tested were relatively insensitive to either a variation
in the Reynolds number, or an increase in the wind tunnel turbulence level, whereas the NACA 0012
was very seriously affected by either", below Re ≈ 5e4.

**Inference (mine, not stated in any source I read):** the 0.455 → 0.59 values change with
turbulence, and Laitone reports that only the NACA 0012 was sensitive to turbulence. So the pair
almost certainly belongs to the **NACA 0012**, a 12 %-thick symmetric section, which is the
section Laitone shows to be the *worst* performer in this regime. A ray-supported fin membrane is
a thin, sharp-edged and possibly cambered plate, which is the section type Laitone found to be
insensitive to Re. The author's proxy is the wrong section family for this design.

A second substitution: the author takes the proxy from **above** the design Re (2e4) and
extrapolates it *downward*, assuming C_L,max falls as Re falls. That trend is the laminar
separation-bubble behaviour of thick, rounded-nose sections. Laitone's abstract-level statement
says thin plates do not follow it.

## 4. Counter-evidence at or near Re 3e3 that the claim missed

Disagreements between these sources are kept as they appear, not averaged.

| Source | Re | Kind | Value | Read-level |
|---|---|---|---|---|
| Wakeling & Ellington 1997, *J. Exp. Biol.* 200:543, real dragonfly wings, wind tunnel | 700–2,400 | **measured** (steady) | C_L,max **1.07** (*Sympetrum sanguineum*), **1.15** (*Calopteryx splendens*) | search-summary (abstract-level text and a 2008 citing paper; the 1.15 rests on the abstract alone) |
| Same paper, free-gliding dragonflies | 700–2,400 | **observed** in glides | highest C_L recorded in glides **0.93**. The abstract says this is not necessarily the wings' maximum. | search-summary |
| `S2-low-reynolds-aero.md` (this repo), citing Wakeling & Ellington | 700–2,400 | relayed | "Sympetrum ≈ 1.05–1.07; other species ≈ 0.7–0.9" | that document's level S (secondary) |
| Holden et al. 2014, *J. Exp. Biol.* 217, anatomically accurate flying-snake cross-section, water tunnel, 2D section | 3,000–15,000 | **measured** | max C_L "between 1.1 and 1.9, increasing with Reynolds number" | **full-text** of Krishnan et al. (arXiv:1309.2969), which relays Holden. Holden itself not read (secondary). |
| Krishnan, Socha, Vlachos & Barba, arXiv:1309.2969 ("Lift and wakes of flying snakes"), 2D snake section | 500–3,000 | **simulated**, 2D | C_L ≈ 1.5 at α 25–30° at all Re tested; "jumps to above 2 at aoa 35°" for Re ≥ 2,000. The authors say their simulated values exceed the experiments. | **full-text** (PDF retrieved, text extracted) |
| Citation in *Sci. Rep.* 6:25706 (2016) | 1e4 | relayed | "maximum lift coefficient of a thin airfoil is about 0.8" | S, via `S2-low-reynolds-aero.md`; not re-read by me |

How to read these (inference):
- **The ≤ 0.6 ceiling sits below every steady thin-wing value I found in or near this Re band.**
  The lowest relevant figure, the *Sci. Rep.* "about 0.8" for a thin aerofoil at 1e4, is already
  above it. The direct match in Re and wing type, real insect wings at Re 700–2,400, gives
  0.7–1.15 across species. These were measured on *finite* real wings, so the finite-span
  penalty is already included.
- The snake values are a **2D section** of a thick lifting bluff body in water. A finite wing
  would lose some of that lift, so I do not use 1.1 as a fin-wing estimate. The point they make
  is narrower: at Re 3,000 a non-airfoil section measured above 1.0. My reading that "1.1" is the
  Re-3,000 end of the range comes from the words "increasing with Reynolds number". The source
  does not tabulate it.
- **Possible mechanism the claim does not consider:** low-AR wings at high incidence can carry
  stable tip and leading-edge vortices. Taira & Colonius 2009 (*J. Fluid Mech.* 623:187) studied
  translating low-AR flat plates at Re 300 and 500 by simulation. I retrieved only the abstract
  scope (search-summary), and **no C_L values**. I list it as an unretrieved lead, not evidence.

**Negative search scope:** I ran four web searches (Wakeling & Ellington; Laitone; Holden/Socha;
Taira & Colonius) and five fetch attempts. Fetches to link.springer.com, scilit.com and
acnpsearch.tweb-dev.unibo.it failed: those hosts do not resolve in this session. arxiv.org
succeeded. I found **no measured steady C_L,max on a fish-fin membrane in air at any Re.** That
search was limited to these queries and is not exhaustive.

## 5. Evidence level

- "Re ≈ 2e3–4e3": **derived** is honest. The algebra is closed-form from stated inputs and I
  reproduce it.
- "so C_L,max is probably ≤ 0.6": this is **not derived**. Re does not determine C_L,max. Getting
  from one to the other needs an empirical C_L,max(Re) relation for the right section type. What
  the author actually did is extrapolate from a single search-summary number for (inference) a
  thick NACA 0012 at Re 2e4. The honest label is **inference from a proxy, contradicted by
  relayed measurements on thin wings in the target Re band.** The "so" in the sentence presents a
  proxy extrapolation as a consequence of a derivation. That is the defect.
- "the value at that Re is unknown": **half true.** For a zebrafish fin membrane it is unknown, and
  I found nothing that changes that. For thin, cambered or corrugated wings in general it is not
  unknown: relayed measurements put steady C_L,max at about 0.9–1.15 around Re 7e2–2.4e3.

## 6. Does this change the parent report's verdict? No (calculated)

Required speed for a 1-BL span, AR 5 wing: V ∝ C_L^-½.
- C_L 0.6: 5.84 m/s (author)
- C_L 1.07: 5.84 × √(0.6/1.07) = **4.37 m/s**, which is 8.0× the measured Ucrit of 0.548 m/s
  and 64× the kinetic energy (calculated)

The launch-speed barrier remains, and so does the author's ranking of it as the hardest barrier.
The correction mainly moves the author's "optimistic sensitivity case" (C_L 1.0) to roughly the
*central* case. C_L 0.6 becomes a conservative case rather than a probable ceiling.

## 7. What would settle it

A steady wind-tunnel polar for a fin-ray-supported membrane (thin, sharp leading edge, ray
corrugation) at Re 2e3–4e3 and AR 1–5. The second most useful thing is a full-text read of
Laitone 1997, to confirm which section the 0.455/0.59 values come from, and of Wakeling &
Ellington 1997, to replace the relayed 1.07/1.15.

## Sources

| Source | Read-level | Used for |
|---|---|---|
| `zebrafish-glide-physics.md` (branch `claude/zebrafish-glide-physics-j176og`) | full-text | the claim, inputs, downstream use |
| `S2-low-reynolds-aero.md` (branch `claude/s2-low-reynolds-aero-acdwr7`) | full-text (repo document; its own sources are S/A) | internal disagreement: C_L,max 0.8–1.07 |
| Krishnan, Socha, Vlachos & Barba, "Lift and wakes of flying snakes", arXiv:1309.2969 | full-text | simulated 2D snake C_L at Re 500–3,000; relayed Holden 2014 and Miklasz 2010 values |
| Holden et al. 2014, *J. Exp. Biol.* 217 | secondary (via Krishnan full text), not read directly | max C_L 1.1–1.9 at Re 3,000–15,000 |
| Wakeling & Ellington 1997, *J. Exp. Biol.* 200:543 | search-summary | C_L,max 1.07 / 1.15 (tunnel), 0.93 (glides) |
| Laitone 1997, *Exp. Fluids* 23:405 | search-summary; PDF could-not-access (host not resolvable) | thin plates insensitive to Re; NACA 0012 sensitive |
| Taira & Colonius 2009, *J. Fluid Mech.* 623:187 | search-summary (abstract scope only) | unretrieved lead on low-AR plates; no numbers used |

```swarm-challenge
{"claim_id": 5, "outcome": "weakened", "reason": "The Re ≈ 2e3–4e3 arithmetic reproduces exactly, but the C_L,max ≤ 0.6 ceiling is extrapolated from what is probably a thick NACA 0012 section at Re 2e4, while relayed measurements on thin real insect wings at Re 700–2,400 give steady C_L,max ≈ 0.9–1.15; that changes the central design value but not the parent report's launch-speed verdict.", "corrected_value": "Re ≈ 1.9e3–4.0e3 (derived, design point, AR 3–8); steady C_L,max ≈ 0.9–1.15 for thin insect-type wings at Re 7e2–2.4e3 (measured by others, relayed at search-summary level); fin-membrane value unknown"}
```
