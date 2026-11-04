# Challenge 159: adversarial review of S26 "No on current evidence"

**Claim under review.** This is the S26 swarm-result in `docs/research/fish/S26-organ.md` on
`origin/claude/active-fin-ray-stiffening-l53vks`. I read the file in full.

> No on current evidence: the only measured active (hemitrich base-locking) stiffening factor is ~12x (one
> bluegill ray). That leaves a zebrafish-scale ray ~14x short of 6.3e-4 N m^2, and even the modelled ~100x
> ceiling is 1.65x short. It could close only if the requirement is per-fin and shared across >=14 rays, or if
> an unverified in-vivo bluegill EI of 5.65e-4 N m^2 reflects a much larger active effect.
> KEY: 12x vs 165x.

The recorded evidence level is *derived*.

**Verdict: WEAKENED.**

- The arithmetic is right.
- The comparison is mislabelled. Neither number is "zebrafish-scale":
  - 6.3e-4 N m^2 is a per-ray requirement for an assumed **100 g flying fish with 120 mm rays**.
  - 3.8e-6 N m^2 is a **bluegill** ray of 40 mm or less.
- The first escape route is already used up: the requirement is per ray, with 14 rays already divided out.
- The "12x" is not an active factor. It is a clip-clamped boundary-condition ratio measured on a dead, excised
  ray.

When I re-run the question at true zebrafish scale, using the project's own S6 numbers, the answer becomes
wing-size dependent and is not a flat "no". Everything below is **calculated** by me (`python3 -I`), unless it
is tagged as a source. I measured nothing.

## 1. Independent arithmetic

- 6.3e-4 / 3.8e-6 = **165.8x**. This matches "165x".
- 165.8 / 12 = **13.8x short**. 3.8e-6 x 12 = 4.56e-5 N m^2.
- 165.8 / 100 = **1.66x short**. 3.8e-6 x 100 = 3.8e-4 N m^2.

I also re-derived S6-D's requirement from its stated inputs: m = 0.10 kg, N = 14, L = 0.12 m, n = 1,
δ/L = 0.1.

- P = n·m·g/(2N) = 0.0350 N
- EI = P·L^2/(8·0.1) = **6.31e-4 N m^2**

**There is no arithmetic fault.**

## 2. Where the inputs came from: the "zebrafish-scale" label is wrong (main defect)

The S26 author could not find S6, took 6.3e-4 and 165x "as given", and inferred that the passive ray was a
zebrafish ray (S26-organ.md §0). Neither part of that holds. I read both upstream files.

- **6.3e-4 N m^2** comes from S6-D (`S6-deepen.md` §1 on `origin/claude/deepen-fin-ray-s6-cj2i2x`, read in
  full). S6-D states its reference scenario explicitly as "assumptions, not measurements of any flying fish":
  - body mass 0.10 kg
  - **14 load-bearing rays per fin**
  - ray span 120 mm
- **3.8e-6 N m^2** is the bluegill pectoral ray stiffness as relayed by Puri et al. 2018, citing Flammang et
  al. 2013 (S6-D §2 table). It is not a zebrafish value.
- The original zebrafish S6 (`S6-organ.md` on `origin/claude/s6-fin-ray-load-kqweu7`, read in full) uses a
  **0.4 g, 4 cm *Danio rerio***. It derives a completely different requirement. It uses the only zebrafish
  measurement it found, Puri et al. 2018: whole caudal fin EI 1.5–4e-9 N m^2, in vivo, anaesthetised.

So "a zebrafish-scale ray ~14x short of 6.3e-4" compares a bluegill ray against a 100 g flying-fish
requirement. **This is a proxy standing in for the target.** The quantity that matters for `zebrafish-flight`
is the zebrafish per-ray requirement against the zebrafish per-ray EI.

## 3. The right comparison, at zebrafish scale (calculated from S6-organ's inputs)

S6-organ's inputs are: m = 0.4 g; two square fin-wings of span L = chord; δ/L ≤ 0.1; 10–14 pectoral rays
spread across L (Zool. Lett. 2019, search-summary as relayed by S6-organ). The required per-ray EI is:

| Wing span L | Required per-ray EI (10–14 rays) | Factor needed over zebrafish per-ray EI 0.83–2.5e-10 | Does 12x close it? |
|---|---|---|---|
| 3 mm | 1.6–2.2e-9 N m^2 | **6.3–27x** | closes at the stiff end only |
| 5 mm | 4.4–6.1e-9 | 18–74x | no |
| 10 mm | 1.75–2.45e-8 | 70–290x | no |
| 15 mm | 3.9–5.5e-8 | 160–660x | no |

The zebrafish per-ray EI here is S6-organ's division of Puri's whole-fin EI by 16–18 caudal rays. That
division is itself an inference.

At true zebrafish scale, then, the required active factor runs from **6x to 660x**, depending on wing size. It
is not a single 165x. The measured 12x can close the smallest wing, and S6-organ already noted this (its §5
item 2). So "No" is right only for wings of about 5 mm or more. That is my inference, from the project's own
upstream numbers.

There is a further caveat that cuts against even the 3 mm case. Puri's fins were intact, with both hemitrich
bases attached. Alben's 12x is clamped versus **one base free**. So the 12x may not stack on top of Puri's
baseline at all. S6-organ flags this as well. If it does not stack, the realisable gain over the zebrafish
baseline is `unknown` and is probably below 12x.

## 4. The first escape route is incoherent

The claim says it "could close only if the requirement is per-fin and shared across >=14 rays". But S6-D's
6.3e-4 is **already per ray**, with N = 14 divided out (P = n·W/(2N)). Dividing by 14 again would count the
load sharing twice. Challenge-92 reached the same conclusion: the C6 route is removed. That escape route does
not exist.

## 5. The proxy inside the key number: the "12x" is not an active stiffening factor

I fetched Alben, Madden & Lauder 2007 (*J R Soc Interface* 4:243, PMC2359861) this session. Read-level:
**full-text via automated page summarizer**. It reports:

- The fish were euthanised with MS-222. Fins were removed and rays dissected and tested in water within 48 h.
- Muscle action was reproduced with **clips** holding each hemitrich.
- Clamped-base stiffness is "about 12 times the value when one hemitrich is free".
- The model ratio rises to about 100 for G > 1e5. The measured 12x corresponds to G ≈ 1e2. The text says
  "4 at G = 3" while the Fig. 7b caption says "from 3 to 100". That is an internal inconsistency in the
  paper, which I preserve here.

So the 12x is a **passive boundary-condition ratio in a dead, excised ray**. It is not a measured active
(muscle-driven) stiffening of a living ray. Calling it "the only measured active stiffening factor" overstates
it. The S26 body text (§5) says this correctly, but the swarm-result headline does not. Whether living muscle
reaches, exceeds or falls short of the clip condition is `unknown`.

## 6. Size mismatch inside the claim's own frame

This point comes from challenge-92 on `origin/claude/challenge-s26-active-stiffening-acr1ha`, which I read in
full. I re-checked its scaling arithmetic.

The 165x compares a ray of 40 mm or less with a 120 mm requirement. Under ray-only L^4 scaling the required
factor drops to:

- **2.1x** on the relay baseline
- **7.5x** on the primary-derived one-free baseline (1.07e-6 N m^2)

Under whole-fish isometry it rises to **6.3–22x**. In every one of these framings the 165x figure is an
artefact of comparing structures of different sizes, so the "~14x short" does not stand.

## 7. Evidence level

"Derived" is honest. The claim does not present a calculation as a measurement. The defects are about which
quantities are being compared, not about fabricated numbers:

- the zebrafish label
- the active label on the 12x
- the double-counted escape route

## 8. What survives

- The arithmetic.
- The statement that the single measured locking ratio (n = 1 ray, clip-clamped) is far below 165x.
- The disagreement between the 565e-6 and 3.8e-6 bluegill values, which remains unresolved.
- The conclusion that active locking alone does not rescue zebrafish wings of about 5 mm or more (§3).

What does not survive:

- the 14x/165x figures presented as a zebrafish-scale result
- the per-fin escape route
- "No" as an unconditional answer

**Scope of negative searches.** I ran no new literature search for zebrafish pectoral ray EI, length or d/t. I
relied on the S6-organ and S26 searches as they describe them. My one new source read was the Alben 2007 PMC
page.

```swarm-challenge
{"claim_id": 159, "outcome": "weakened", "reason": "Arithmetic is correct (165.8x, 13.8x, 1.66x), but 6.3e-4 N m^2 is S6-D's per-ray requirement for an assumed 100 g flying fish with 120 mm rays and N=14 already divided out, and 3.8e-6 is a bluegill ray, so the result is not zebrafish-scale and the per-fin escape route double-counts; the 12x is a clip-clamped ratio on dead excised rays, not active stiffening; at true zebrafish scale (S6-organ inputs) the required factor is 6-27x for a 3 mm wing (12x can close it at the stiff end) up to 160-660x for a 15 mm wing, so 'No' holds only for wings of about 5 mm or more.", "corrected_value": "required active factor at zebrafish scale 6.3-27x (3 mm wing) to 160-660x (15 mm wing) per ray; in S6-D's flying-fish frame 166x unscaled, 2.1-7.5x under ray-only L^4 scaling", "depends_on": ["S6-D: EI_req 6.3e-4 N m^2 per ray from P = n m g/(2N), m=0.10 kg, N=14, L=0.12 m, delta/L=0.1 (S6-deepen.md, full-text)", "S6-D: 3.8e-6 N m^2 is bluegill ray EI relayed by Puri 2018 citing Flammang 2013", "S6-organ: Danio rerio m=0.4 g, square fin-wings, delta/L<=0.1, 10-14 pectoral rays (ray count search-summary)", "Puri et al. 2018: zebrafish whole caudal fin EI 1.5-4e-9 N m^2 in vivo anaesthetised, 16-18 rays (as read full-text by S6-organ)", "inference: zebrafish per-ray EI = whole-fin EI / ray count (0.83-2.5e-10 N m^2)", "Alben, Madden & Lauder 2007 PMC2359861: ~12x clamped vs one hemitrich free, dead excised rays held with clips; model ratio ~100 for G>1e5 (full-text via summarizer)", "challenge-92: ray-only L^4 scaled required factor 2.1x (relay) to 7.5x (primary-derived)"]}
```
