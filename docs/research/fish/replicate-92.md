# Replicate 92: does S26-D's "S26's 'no' falls" hold up when re-derived?

**Status:** an independent re-derivation. It uses only calculation and literature. **Nothing here is an
observation of mine.** Each number is tagged *measured* (by the cited authors), *calculated* (by me) or
*assumption*.

## 0. What I was given, and what I saw before deriving

The question arrived with its answer removed: "S26-D deepen FALLS the 'no'". The S26 source document is not
on `main`. The only place its inputs live is `docs/research/fish/S26-deepen.md` on
`origin/claude/deepen-s26-active-stiffening-48xj8q`.

**Disclosure.** Before deriving anything I saw two things:

- the commit title `S26-D: S26's 'no' falls once the 165x gap is size-corrected`, printed by `git log`;
- **§0 only** of S26-deepen.md, the part that sets out the inputs.

The commit title gives away the direction of their conclusion and the method (size correction). It does not
give the number. I did not read §1–§4, the result sections, or `S26_deepen_calc.py` until my own numbers
below were fixed.

The inputs from §0 (S26's own "no") are as follows:

| Input | Value | Their provenance | My read-level |
|---|---|---|---|
| EI_req, per ray | 6.3e-4 N m^2 | calculated by S6-D for a 100 g fish, **L = 120 mm** rays, 14 rays per fin | listing (§0 of S26-deepen.md; I did not re-derive S6-D) |
| EI_passive | 3.8e-6 N m^2 | a bluegill ray; relayed by Puri et al. 2018, citing Flammang et al. 2013 | listing (as above). I could not reach Puri 2018 myself: cob.silverchair.com is blocked |
| Gap | 165x | 6.3e-4 / 3.8e-6 | arithmetic: 165.8 (checked) |
| Locking factor F_a | ~12x | Alben et al. 2007 | **I read this in the primary source, full-text** (below) |
| Model ceiling | ~100x | Alben et al. 2007 | listing (not re-checked) |

## 1. Primary sources I read myself

- **Alben, Madden & Lauder 2007**, *J R Soc Interface*, PMC2359861. **Read-level: full-text.** I fetched the
  PMC HTML with curl and stripped the tags myself, with no summarizer in between. Verbatim fragments:
  - "Six fishes with fins of similar size (maximum ray length =40.3±0.8 mm, mean±s.e.)" → *measured*
    L_src ≤ 40.3 mm.
  - "L =4 cm for the length of a typical bluegill fin ray"
  - "the measured B = EI ≈10^−6 –10^−5 J m" (J m = N m^2) → *measured* range for bluegill ray EI, at ~40 mm
    length.
  - "a slope of 1.98 N m^−1 , about 12 times the value when one hemitrich is free" → *measured* F_a ≈ 12.
    The fragment I read gives no n.
- **Flammang, Alben, Madden & Lauder 2013**, *J Morphol* 274:1044. **Read-level: search-summary.** The search
  result quotes the abstract: "Flexural stiffness of the fin ray was calculated to be 565×10-6 Nm2".
  - The full text **could-not-access**: sites.harvard.edu gave a 403 from the proxy, and
    deepblue.lib.umich.edu failed DNS.
  - This **disagrees with the 3.8e-6 relay by ~150x**. I cannot resolve it, so I keep it open and do not
    average it.
- **Puri et al. 2018**. **Read-level: could-not-access**: cob.silverchair.com is blocked in this session.

**Scope of the negative searches:** two WebSearch "standard" queries and three fetch attempts. Nothing
else was searched.

## 2. Derivation (all calculated)

The S26 "no" compares passive EI of a **~40 mm** bluegill ray with a requirement for a **120 mm** ray.
- EI = E·I. For a solid or geometrically similar section, I ∝ d^4.
- **Under isometry** (*assumption*): d ∝ L, at constant E. So EI ∝ L^4.

Central case, with EI_src = 3.8e-6 N m^2 and L_src = 40.3 mm:

```
scale       = (120 / 40.3)^4 = 2.978^4 = 78.6
EI_p(120mm) = 3.8e-6 × 78.6 = 2.99e-4 N m^2
gap         = 6.3e-4 / 2.99e-4 = 2.11x
locked      = 12 × 2.99e-4 = 3.58e-3 N m^2
margin      = 3.58e-3 / 6.3e-4 = 12 / 2.11 = 5.69x   → requirement met
```

I also ran a sensitivity sweep. The script is outside the repo, in my scratchpad. The sweep varies:

- the scaling exponent n in EI ∝ L^n, from 4 down to 3, because thinner-than-isometric rays are possible;
- L_src over 37–43 mm, a window I chose that is wider than the reported s.d., which is ≈ 0.8·√6 ≈ 2.0 mm;
- EI_src over Alben's measured range 1e-6 to 1e-5.

| EI_src | n | gap at 120 mm (over the L_src window) | 12x margin | Does "no" fall? |
|---|---|---|---|---|
| 3.8e-6 | 4 | 1.5–2.8x | 4.4–7.8x | yes |
| 3.8e-6 | 3.5 | 2.8–4.6x | 2.6–4.4x | yes |
| 3.8e-6 | 3 | 5.0–7.7x | 1.6–2.4x | yes |
| 1e-6 (Alben low end) | 4 | 5.8–10.5x | 1.1–2.1x | yes, barely |
| 1e-6 | 3.5 | 10.5–17.5x | 0.69–1.15x | **marginal / no** |
| 1e-6 | 3 | 18.8–29.2x | 0.41–0.64x | **no** |
| 1e-5 (Alben high end) | 3–4 | 0.6–2.9x | 4–21x | yes |
| 565e-6 (Flammang abstract, unscaled) | any | ≤ 1.1x before scaling | ≫1 | yes |

## 3. My value

**Size-corrected passive gap ≈ 2.1x (calculated). The plausible range is ~1.5x to ~8x** for EI_src = 3.8e-6
and n = 3–4. The single measured 12x locking factor closes that gap, with a margin of **~5.7x (range
~1.6–7.8x)**. **So S26's "no" falls.**

My conditions, which are my inference and not any author's claim:

1. It requires roughly isometric EI scaling, n ≳ 3.
2. It fails only if EI_src is at Alben's low end (1e-6) **and** n ≤ 3.5.
3. It depends on F_a = 12 (effectively a single measurement) holding for a 120 mm ray in vivo.
4. The 565e-6 vs 3.8e-6 disagreement is unresolved. Both of its ends support "falls", so it does not change
   the direction.

## 4. Comparison with the recorded value

I read S26-deepen.md §1–§4 only after the above was fixed. Their recorded values are:

- passive EI at 120 mm = 3.0e-4 N m^2;
- active factor needed = 2.1x;
- margin of the measured 12x = 5.7x;
- verdict: FALLS.

All the numbers above match mine to two significant figures. **AGREE.**

The agreement is not fully independent:

- **Shared inputs.** Both derivations take EI_req = 6.3e-4 and EI_src = 3.8e-6 from the same upstream chain.
- **Shared assumptions.** Both use L_src = 40.3 mm and both assume isometric L^4 scaling. Every number we
  agree on rests on these.

The independent parts are these:

- **My read of Alben 2007.** I read it as direct full-text. Their record says it was read via a summarizer.
  My read confirms 40.3 ± 0.8 mm, EI ≈ 1e-6–1e-5, and the 12x.
- **My allometry sweep (n = 3–3.5).** They did not run one.
  - It shows the "falls" holds down to n = 3 at EI_src = 3.8e-6.
  - It **fails** at EI_src = 1e-6 with n ≤ 3.5.
  - They report the 1e-6 case only at n = 4 (8x needed). I get the same, 8.0x.

```swarm-replication
{"claim_id": 92, "my_value": "size-corrected passive gap ~2.1x (range ~1.5-8x for n=3-4); measured 12x locking clears it with ~5.7x margin -> S26 'no' falls (calculated)", "agrees": true,
  "note": "Matches the recorded 2.1x and 5.7x, but it shares their EI_req, the 3.8e-6 relay and the isometry assumption; the conclusion fails only if EI_src is near 1e-6 and EI scales as L^3.5 or less."}
```
