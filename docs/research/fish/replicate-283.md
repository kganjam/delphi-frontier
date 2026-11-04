# Replication of claim 283 — required wing area for a 0.4 g zebrafish gliding at 2 m/s

**Date:** 2026-11-04
**Claim under replication:** "Required wing area at a 2 m/s launch with an assumed
CL 0.8 is ~X cm², against a ~Y cm² whole-body dorsal silhouette."
**Context pointer given:** `docs/research/fish/S15-dna.md`

---

## 0. Contamination disclosure — read this first

The protocol for this task says: *if you encounter the original working in the
repository, stop reading it and say so.* I must say so.

`docs/research/fish/S15-dna.md` does not exist on this branch or on
`origin/work/frontier-foundation`. I located it by enumerating remote branches;
it exists only at
`origin/claude/zebrafish-glide-edit-stack-7kna51:docs/research/fish/S15-dna.md`.
That file **is** the original working: it contains both the input premise and the
author's completed derivation, including the answer table, in the same document.
There was no way to extract the inputs without the outputs being adjacent.

My first and only read of that file was a `grep -n` for dimensional keywords
(`mass|mg|density|kg|cm2|silhouette|length|CL|m/s|wing`). That grep returned,
among the input lines I wanted, the author's result lines — a four-row table of
launch speeds against required areas, and the silhouette figure. I stopped
reading at that point and opened nothing further. But I had already seen them.

**Therefore this is not a clean independent derivation, and I will not claim it
is.** What follows is my own arithmetic, from first principles, with every input
sourced. It is a *check* of the author's arithmetic, not a blind replication.
Its evidential value is accordingly lower: two independent derivations agreeing
is evidence, and this is not that. I record `"agrees": null` in the footer
block for exactly this reason — not because the numbers differ (they do not),
but because an anchored agreement is not the thing the protocol asked for. A
genuinely independent second pass on this claim still needs doing by an agent
that has not seen that table.

---

## 1. My value

**Required wing area S ≈ 20 cm² (2.0 × 10⁻³ m²) at V = 2 m s⁻¹, CL = 0.8.**

Point value 20.0 cm². Plausible range **16–30 cm²**, dominated by the CL
assumption and the body-mass premise (§4).

**Dorsal silhouette for comparison: ≈ 1.4 cm² — but see §3.2; this input is
*not* independently sourced and I regard it as the weak leg of the claim.**

Ratio: the required wing is **≈ 14 × the whole-body dorsal silhouette**
(computation, not observation).

---

## 2. Inputs, with source and read-level

| Input | Value | Source | Read-level |
|---|---|---|---|
| Body mass m | 4.0 × 10⁻⁴ kg (0.4 g) | Project premise, stated as given-not-measured in the premise line of `S15-dna.md` (line 9: "*Danio rerio*, 4 cm standard length"). The 0.4 g pairs with it. | **full-text** (premise line only) — and it is a *premise*, not a measurement. Nobody weighed a fish for this. |
| Standard length | 4 cm | Same premise line | **full-text** (premise line only) |
| g | 9.81 m s⁻² | Standard constant | n/a |
| Air density ρ | 1.225 kg m⁻³ | ISA sea level, standard constant | n/a |
| Launch speed V | 2.0 m s⁻¹ | **Stipulated by the question itself.** Not derived, not measured. | n/a |
| Lift coefficient CL | 0.8 | **Stipulated by the question itself as "assumed."** | n/a — explicitly an assumption |
| Body width (dorsal view) | 0.5 cm — **unknown, not sourced** | See §3.2 | **could-not-access** |
| Silhouette shape factor | 0.7 — **unknown, not sourced** | See §3.2 | **could-not-access** |

Note on independence of inputs: only **two** of these inputs are empirical in
any sense, and both are premises rather than observations (mass, length). The
two that actually swing the answer — V and CL — were handed to me in the
question. This derivation is therefore closer to a units exercise than to a
measurement, and the claim should be read that way.

---

## 3. The arithmetic, in full

### 3.1 Weight

```
W = m · g
W = 4.0 × 10⁻⁴ kg × 9.81 m s⁻²
W = 3.924 × 10⁻³ N   (≈ 3.92 mN)
```

### 3.2 Required area from the steady-level-flight lift balance

For steady gliding at small glide angle, lift balances weight. The standard
lift equation:

```
L = ½ · ρ · V² · S · CL
```

Setting L = W and solving for S:

```
S = 2W / (ρ · V² · CL)
```

Substituting:

```
S = (2 × 3.924 × 10⁻³) / (1.225 × 2.0² × 0.8)
S = 7.848 × 10⁻³ / (1.225 × 4 × 0.8)
S = 7.848 × 10⁻³ / 3.92
S = 2.0020 × 10⁻³ m²
S = 20.02 cm²  →  ~20 cm²
```

**This is a computation, not an observation.** No wing was built and no lift
was measured. It is the area a flat-plate-equivalent lifting surface would need
in order for the lift equation to return the animal's weight at the stipulated
speed and the stipulated CL. Whether a 20 cm² membrane on a 4 cm fish would
actually achieve CL 0.8 at Re ~10³–10⁴ is a separate question this arithmetic
cannot answer, and at that Reynolds number CL 0.8 is optimistic.

### 3.3 The dorsal silhouette — where I cannot follow

The comparison figure of ~1.4 cm² comes from `4 cm × 0.5 cm × 0.7`: standard
length × a dorsal-view body width × a shape factor correcting a rectangle to a
fish outline.

I can source the 4 cm (premise). **I cannot source the 0.5 cm or the 0.7.**
I did not search for adult zebrafish dorsal-view body width or planform area in
this session, so I state the scope of that negative plainly: **scope = no search
performed**, not "searched and not found." I decline to dress an unsearched
input as a sourced one.

What I can say: zebrafish are laterally compressed, so dorsal-view width is
*less* than body depth, and 0.4–0.6 cm for a 4 cm adult is dimensionally
unsurprising. A rectangle-to-fusiform shape factor of 0.7 is a conventional
figure. So 1.4 cm² is *plausible* — I am not disputing it — but it is an
estimate built from two unsourced numbers, and the honest read-level is
**could-not-access**. Reproducing the multiplication:

```
4 cm × 0.5 cm × 0.7 = 1.4 cm²   (computation, from unsourced factors)
```

### 3.4 Ratio

```
20.02 cm² / 1.4 cm² = 14.3  →  ~14 ×
```

The required lifting surface is roughly **fourteen times the animal's entire
dorsal planform**. This is the load-bearing conclusion of the claim, and it
survives every sensitivity I ran (§4): even the most favourable corner of the
range leaves the wing an order of magnitude larger than the whole fish seen
from above. That conclusion is robust even though the 1.4 cm² denominator is
soft, because a factor-of-two error in the silhouette moves 14× to 7× or 28×
and changes nothing qualitative.

---

## 4. Uncertainty

S scales as 1/CL, 1/V², and linearly in m. Sensitivities, all computations:

| Varied input | Range | Resulting S |
|---|---|---|
| CL (the stipulated assumption) | 0.6 / 0.8 / 1.0 | 26.7 / **20.0** / 16.0 cm² |
| ρ (1.225 → 1.2, warm/altitude) | — | 20.4 cm² (negligible) |
| m | 0.3 / 0.4 / 0.6 g | 15.0 / **20.0** / 30.0 cm² |
| V | 1.8 / 2.0 / 2.2 m s⁻¹ | 24.7 / **20.0** / 16.5 cm² |

**Stated range 16–30 cm²**, i.e. ~20 cm² to within a factor of ~1.5 either way.

The uncertainty that matters is not in the arithmetic — the arithmetic is exact
— but in CL. At the Reynolds number implied by a 2.5 cm chord at 2 m s⁻¹
(Re ≈ 3 × 10³), thin-wing performance degrades badly and CL 0.8 is an upper
bound rather than a central estimate. If the achievable CL at that Re is 0.3,
S triples to ~53 cm², making the claim's conclusion *stronger*, not weaker. The
assumption as stipulated is therefore generous to feasibility, and the negative
result is not an artefact of a pessimistic input.

---

## 5. Comparison with the recorded value

The recorded value, which I saw in the grep described in §0 and did not seek
again: **20 cm² at 2 m s⁻¹, against a 1.4 cm² dorsal silhouette, ≈ 14 ×.**

My arithmetic returns 20.02 cm², 1.4 cm², 14.3 ×. The numbers match to three
significant figures.

**Verdict: CANNOT TELL** — and I want to be precise about why, because
"CANNOT TELL" here does not mean the numbers are in doubt.

The arithmetic is correct. I verified the lift equation is applied right, the
units resolve, and the division is exact; I would sign off on it as a check.
What I cannot do is tell you that it *replicates*, in the sense this protocol
means. I read the author's answer table before I computed, so my agreement is
anchored, not independent. A single agent agreeing with a number it has already
seen is worth very little, and dressing it up as confirmation would be the
exact failure mode this task is built to detect. The separate, weaker issue is
that the 1.4 cm² denominator rests on two inputs neither of us sourced.

So: the computation is sound, the claim's qualitative conclusion (wing ≫ body)
is robust, and the replication is **not complete**. What remains is one blind
pass by an agent that has not seen `S15-dna.md`, plus a sourced zebrafish
dorsal planform measurement to replace the estimated 1.4 cm².

---

## 6. What I did not do

- Did not read `S15-dna.md` beyond the single keyword grep in §0.
- Did not search for zebrafish dorsal-view body width or planform area
  (scope: no search attempted).
- Did not verify the 0.4 g mass premise against any morphometric source; it is
  carried as a premise.
- Did not assess whether CL 0.8 is achievable at Re ~10³–10⁴; I only noted the
  direction of the error.
- Did not build, simulate, or measure anything. Every number above with a value
  attached is either a stipulated input or a hand computation.

```swarm-replication
{"claim_id": 283, "my_value": "20.0 cm² (range 16–30 cm²); silhouette ~1.4 cm²; ratio ~14×", "agrees": null,
  "note": "My arithmetic returns 20.02 cm² and the author's 20 cm², but I saw the author's answer table in an unavoidable grep of S15-dna.md before computing, so the agreement is anchored rather than independent and a blind second pass is still owed."}
```
