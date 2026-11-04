# Replication 85: S24-D deepen verdict ("FALLS")

This is a desk re-derivation. I ran no experiment. Every number below is either **calc** (my
arithmetic) or an input taken from a named source with its read-level.

## Disclosure: blinding was breached

The task said the inputs live in `S24-deepen.md` on branch `claude/s24-deepen-launch-gap-2motub`.
Two things on that branch reveal the recorded result before any input can be read:

- the commit message, "the low-Re Strouhal correction falls at the taxi operating point";
- the file's opening "Short result" paragraph.

I saw both, so this replication is **not blind to the verdict**. I read §§1–3 of that file to get
the inputs, then stopped. I did **not** read §4 (their recomputation) or `S24-deepen_calc.py`. The
original S24 document is not on this branch or on `work/frontier-foundation` (I searched for "S24"
and "Strouhal" in `*.md`), so I could not check the S24 inputs against S24 itself.

## Question as I understand it

S24 recorded this answer: taxiing needs 132–199 Hz of tail beat against a 52 Hz measured maximum,
a 2.5–3.8× shortfall, "a fortiori". The question is whether that margin survives once the Strouhal
number, or stride length, appropriate to the operating Reynolds number (Re ≈ 6–8 × 10⁴) replaces
the low-Re St of 0.54–0.82.

## Inputs

| Input | Value | Source | Read-level for me |
|---|---|---|---|
| U, taxi speed | 1.95 m/s | S24 target, as relayed in S24-deepen §1 | listing (secondary; original S24 not found) |
| L, body length | 40 mm (also 33 mm) | as relayed in S24-deepen §2 | listing |
| A, peak-to-peak tail amplitude | 8 mm (0.20 L, **assumed** in S24) | as relayed in S24-deepen §1 | listing |
| f_max | 52 Hz (a single EMG value) | as relayed in S24-deepen §1 | listing |
| Stride length λ = U/(fL) | 0.6–0.8 L per beat | Wardle 1975, *Nature* 255:725, as relayed | listing (I did not re-access it) |
| Bainbridge relation | V = ¼·L·(3f − 4), in cm/s, cm and Hz | Bainbridge 1958, *J. Exp. Biol.* 35:109, as relayed | listing; see note below |
| Peak-to-peak St at high Re | ≈ 0.24 (S24-deepen also quotes 0.27; I use 0.24–0.27) | Seo, Zhou & Mittal, arXiv 2507.11665, as relayed | listing for the value; abstract for the paper |
| Amplitude | ≈ 0.18 L | Seo et al., as relayed | listing |

Notes on the sources:

- **Bainbridge 1958: could-not-access.** The journals.biologists.com URL I tried returned an
  unrelated *Aedes* sodium-balance abstract, so I could not confirm the formula from the primary
  source.
- **Seo et al.: abstract.** I fetched the arXiv abstract. It confirms the title and authors, and
  that the paper derives scaling laws from simulations of a mackerel-like swimmer. The abstract
  gives **no** St or Re values and does not mention Bainbridge. So the St ≈ 0.24 value is unverified
  by me.

## Arithmetic (all calc)

**Route 1, stride length:** f_req = U/(λL).

| L | λ = 0.8 | λ = 0.7 | λ = 0.6 |
|---|---|---|---|
| 40 mm | 1.95/0.032 = 60.9 Hz (1.17×) | 69.6 Hz (1.34×) | 1.95/0.024 = 81.2 Hz (1.56×) |
| 33 mm | 73.9 Hz (1.42×) | 84.4 Hz (1.62×) | 98.5 Hz (1.89×) |

**Route 2, Bainbridge extrapolated:** f = (4V/L + 4)/3.

- L = 4 cm: (4·195/4 + 4)/3 = 199/3 = 66.3 Hz, which is 1.28×.
- L = 3.3 cm: (236.4 + 4)/3 = 80.1 Hz, which is 1.54×.

**Route 3, Strouhal:** f = St·U/A.

| St | A = 8 mm | A = 7.2 mm |
|---|---|---|
| 0.24 | 58.5 Hz (1.12×) | 65.0 Hz (1.25×) |
| 0.27 | 65.8 Hz (1.27×) | 73.1 Hz (1.41×) |

Each ratio in brackets is f_req / 52 Hz.

## My value

The shortfall ratio at the taxi operating point is **≈ 1.1–1.9×** across all routes and both body
lengths. The central value at L = 40 mm is **≈ 1.3×**, which means f_req ≈ 59–81 Hz against 52 Hz
(calc).

**Verdict:** the claim that the shortfall is "wider, a fortiori" (2.5–3.8×) **FALLS**. The
shortfall shrinks by a factor of about 2–3. The bare negative, that the requirement exceeds f_max,
survives in every case I computed, but only by 12–89%. That margin is comparable to the
uncertainty in f_max (one EMG value), L and A.

**Uncertainty, and my inference rather than any author's claim:**

- λ and St come from dace, trout, goldfish and mackerel models, not zebrafish.
- The relative speed required is about 49 L/s (1.95/0.04). That is far beyond the speeds at which
  Bainbridge's fish were measured, so Route 2 in particular is a large extrapolation.
- The zebrafish value at this speed is **unknown**. I found no zebrafish measurement at Re ≈ 10⁵.
  Search scope: this repository, plus the two web fetches above.

## Comparison with the recorded value

Their recorded value is ≈ 61–81 Hz at L = 40 mm, a 1.2–1.6× shortfall, and the "a fortiori" claim
falls. I saw this in the file header, so it was not blind. My Route 1 at L = 40 mm reproduces it
exactly, and Routes 2 and 3 fall inside or near it. **AGREE.**

Caveats on that agreement:

- Every numeric input reached me through their document. I could not independently access
  Bainbridge, Wardle or Seo's St value, so this agreement checks their **arithmetic and logic**,
  not their **inputs**.
- I was not blind to their verdict.

```swarm-replication
{"claim_id": 85, "my_value": "f_req ≈ 59–81 Hz at L=40 mm (≈1.1–1.6× the 52 Hz max; 1.1–1.9× including L=33 mm) — 'a fortiori' 2.5–3.8× margin FALLS, bare shortfall survives narrowly", "agrees": true,
  "note": "Arithmetic re-derived three ways agrees, but inputs were only available via the author's document (primary sources could-not-access/abstract) and the verdict was visible in the commit message and file header, so this is not a blind or input-independent replication."}
```
