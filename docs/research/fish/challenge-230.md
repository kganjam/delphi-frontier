# Challenge 230: zebrafish spring-loading work threshold (99 J/kg)

**Claim under review (author's, not mine):** "DECISIVE TEST: in-situ single-stroke spring-loading work of
zebrafish fast myotomal muscle. A value at or above ~99 J/kg closes the energy term. Second: zebrafish
C-start PIV efficiency." Recorded evidence level: *derived*. Value: 99 J/kg threshold. Source: `S29-organism.md`.

**Verdict: WEAKENED.** I could not reproduce the 99 J/kg threshold, because its inputs are not available to me.
But on my own calculation, single-stroke work from zebrafish fast muscle is bounded well below 99 J/kg. That
makes the test's result predictable before anyone runs it, so it cannot be "decisive" in the sense the claim
intends. The quantity it proposes to measure is also a proxy for the one that matters.

## 0. The source could not be accessed

`S29-organism.md` is **could-not-access**. I searched for it:
- the working tree of this repository;
- the history of all 30 commits on every local and remote branch (`git grep` for zebrafish, spring-load,
  C-start and J/kg). The only hits are unrelated entries in `findings/gemini-*.json`;
- GitHub code search across the repositories this session can reach (`S29-organism`, `"99 J/kg"`,
  `spring-loading zebrafish user:kganjam`). Every search returned 0 relevant hits.

So I do not know what energy budget the 99 J/kg is meant to close, what body or muscle mass it is normalised
to, or what efficiency was assumed. **The arithmetic behind 99 J/kg is therefore unverified (`unknown`), not
confirmed.** Everything below tests whether the threshold can be reached, not how it was derived.

## 1. Independent arithmetic: what can zebrafish fast muscle deliver in one stroke?

All numbers in this section are **calculated by me** from the inputs listed. None of them is a measurement.

**Upper bound from stress × strain.** The work per unit muscle mass is at most σ·ε/ρ, where σ is the stress
held across the whole shortening, ε is the strain and ρ is about 1060 kg/m³ (an assumed generic muscle
density).
- Strain: C-start muscle strain in larval zebrafish reaches about **0.19** (Müller & van Leeuwen 2004,
  J Exp Biol 207:853; read-level: search-summary).
- Stress: larval myotomal muscle develops "relatively low stress" (Biophys J 2020; read-level: abstract via
  search-summary; the numeric value is `unknown` to me). I therefore used a deliberately generous range of
  100–300 kPa. This is my assumption, not a cited value for zebrafish.

| σ (kPa) | ε = 0.05 | ε = 0.10 | ε = 0.19 |
|---|---|---|---|
| 100 | 4.7 | 9.4 | 17.9 |
| 200 | 9.4 | 18.9 | 35.8 |
| 300 | 14.2 | 28.3 | **53.8** J/kg |

To reach 99 J/kg at ε = 0.19, the muscle would have to hold **about 550 kPa through the entire shortening**
(calculated). That is roughly twice the most generous stress I assumed, and it ignores the drop in force with
shortening speed (the force–velocity relation). Real stress–strain loops enclose much less than the full
rectangle.

**Cross-check against a measured work loop.** "Mechanical characteristics of ultrafast zebrafish larval
swimming muscles" (Biophys J 119:806–820, 2020; read-level: abstract via search-summary) reports a net power of
134 ± 20 W/kg at 80 Hz. Dividing power by cycle frequency (my calculation, not the authors') gives
134 / 80 ≈ **1.7 J/kg per cycle**. That is net work per full cycle. Positive work in the shortening half is
larger, but not by the factor of about 60 needed to reach 99 J/kg.

**Cross-check in another species.** For northern pike (*Esox lucius*) C-starts, a UBC thesis reports a
metabolic cost of 26.5 J/kg (by excess post-exercise oxygen consumption, EPOC) and a muscle efficiency of about
0.252 (read-level: abstract). Multiplying these (my inference) gives about 6.7 J/kg of mechanical muscle work
per C-start. I do not know the normalisation mass. This is a different taxon at adult size, and it is also an
order of magnitude below 99.

**Disagreement between sources, kept separate.**
- Sculpin fast muscle: about 3.5 J/kg per cycle (Johnston et al. 1993; read-level: search-summary).
- Sculpin in vivo C-bend power: up to 222 W/kg (J Exp Biol 201:913; read-level: search-summary).
- A whole-body larval estimate: 20 W/kg (SICB abstract; read-level: listing).

These figures come from different methods and use different normalisation masses. I have not averaged them.
None of them implies single-stroke work anywhere near 99 J/kg.

**Inference (mine):** every independent route I tried places zebrafish single-stroke muscle work between about
2 and 54 J/kg, with 54 J/kg as a generous ceiling. The 99 J/kg threshold is roughly 2× above that ceiling and
roughly 15–60× above the values measured or derived here.

## 2. Proxy: the measurement is not the quantity that closes an energy term

Muscle work per stroke is a proxy. The quantity that can close an energy term for a spring-loaded escape is the
**elastic energy stored and then returned to the body and fluid**, which equals muscle work × the storage
fraction × the return efficiency. This is always less than or equal to muscle work.

An in-situ single-stroke work-loop measurement records muscle work. It does not separate stored elastic energy
from work delivered directly. The right measurement is a quick-release or energy-balance experiment on the
myosepta and the series compliance: the elastic energy recovered after a latch is released, normalised to the
same mass the energy budget uses.

## 3. Hidden assumption: that zebrafish C-starts are spring-loaded at all

The claim assumes a mechanism that stores energy and then releases it from a latch. A zebrafish C-start
begins with a Mauthner-cell-triggered contraction lasting a few milliseconds. In the sources I read, I found no
latch and no elastic structure stiff enough to store tens of J/kg. Myosepta are thin collagen sheets, not
tendons.

- **If the assumption is dropped and the C-start is driven directly by muscle,** the spring-loading term is
  zero by construction. The budget then has to be closed by muscle power alone. The work-loop figures above are
  far short of 99 J/kg.
- **If the threshold refers to body mass rather than muscle mass,** it rises to 99 / f, where f is the
  fraction of body mass that is fast muscle, a number below 1. That makes the threshold even harder to reach.
- **Scope of the negative search:** I found no evidence of a latch in the four web searches listed here and
  the abstracts they surfaced. This is not a systematic review.

## 4. Is the evidence level honest?

The claim calls the 99 J/kg figure "derived", which is the correct type of label for a threshold. But I
cannot see the derivation, so I cannot confirm that the label is accurate rather than merely plausible. The
word "DECISIVE" overstates things. A test whose outcome existing data already predict (on my calculation, a
failure to reach the threshold) adds confirmation, not a decision. Running it would most likely yield a negative
result that could be anticipated now.

## 5. Regimes and taxa the author may have missed

- **Ontogeny:** larval and adult zebrafish differ in strain, cycle frequency and fibre type. A single
  threshold that does not name the stage is underspecified.
- **The second test (C-start PIV efficiency):** efficiency multiplies a work input that already falls short.
  Even a hydrodynamic efficiency of 1 cannot raise the input to 99 J/kg. The PIV test can only tighten the
  shortfall, not close it.

## Sources (read-levels)
- `S29-organism.md`: could-not-access (searches listed in §0).
- Biophys J 119:806–820 (2020), larval zebrafish work loops, https://www.biorxiv.org/content/10.1101/2020.04.02.010298.full.pdf : abstract (via search-summary).
- Müller & van Leeuwen 2004, J Exp Biol 207:853, https://cob.silverchair.com/jeb/article-pdf/207/5/853/1251455/853.pdf : search-summary.
- Pike fast-start energetics, UBC thesis, https://open.library.ubc.ca/collections/831/items/1.0100459 : abstract (via search-summary).
- Johnston et al. 1993, sculpin fast muscle, https://pure.uhi.ac.uk/ar/publications/recruitment-patterns-and-contractile-properties-of-fast-muscle-fi/ : search-summary.
- Sculpin escape-response power, J Exp Biol 201:913, https://cob.silverchair.com/jeb/article-pdf/201/7/913/3399524/jexbio_201_7_913.pdf : search-summary.
- Larval whole-body power, SICB abstract, https://sicb.org/?p=21722 : listing.

```swarm-challenge
{"claim_id": 230, "outcome": "weakened", "reason": "The 99 J/kg derivation could not be accessed or reproduced, and on my own calculation zebrafish fast-muscle single-stroke work is capped at about 54 J/kg (stress x strain, generous) and measures about 1.7 J/kg per cycle in larval work loops, so the test is not decisive (its negative result can be predicted now) and it measures muscle work as a proxy for returned elastic energy.", "corrected_value": null,
  "depends_on": ["larval zebrafish C-start muscle strain about 0.19 (Muller & van Leeuwen 2004, search-summary)", "assumed fast-muscle stress range 100-300 kPa (my assumption, not measured for zebrafish)", "larval zebrafish work-loop net power 134 W/kg at 80 Hz (Biophys J 2020, abstract)", "muscle density about 1060 kg/m3 (assumed)", "absence of a latch or tendon-like elastic store in the zebrafish C-start (negative search, 4 web queries)", "S29-organism.md inputs unknown (could-not-access)"]}
```
