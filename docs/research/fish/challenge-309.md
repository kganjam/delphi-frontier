# Challenge 309: *Scorpaena notata* fast-muscle power, 142.7 W/kg

**Verdict: WEAKENED.** The number, species, temperature, method and evidence level all hold. Three parts of the wording around the number go further than the source supports.

## Source re-read

- Wakeling JM, Johnston IA (1998) *Muscle power output limits fast-start performance in fish.* J Exp Biol 201:1505–1526. PMID 9556535, doi 10.1242/jeb.201.10.1505.
  **Read-level: abstract.** I fetched it in full from PubMed efetch on 2026-11-04. I did not access the full text.

Verbatim sentences from the abstract that bear on the claim:

> "A work-loop technique was used to measure mean muscle power output at similar strain and shortening durations to those found in vivo. The fast Sc. notata myotomal fibres produced a mean muscle-mass-specific power of 142.7 W kg-1 at 20 degrees C."
>
> "At all temperatures, the predicted mean muscle-mass-specific power outputs, as calculated from swimming sequences, were similar to the muscle power outputs measured from work-loop experiments."

## 1. Arithmetic

The claim contains no arithmetic. The value is quoted directly from the abstract, and I confirmed it is the same there: 142.7 W kg⁻¹, *Sc. notata*, 20 °C, fast myotomal fibres, mean, mass-specific. The abstract does not give the inputs needed to recompute it independently (work per cycle, cycle frequency, preparation mass). **Recomputation is not possible at abstract level.**

## 2. Proxy check

- **This is mean power, not peak power.** The value is a work-loop mean, averaged over the imposed strain cycle. A fast-start is a single, non-cyclic event, and power within stage 1 is not uniform. The instantaneous peak is not reported in the abstract and may be higher, so it is `unknown`. Using 142.7 W/kg as "what fast muscle can deliver" in a fast-start uses the cycle mean as a proxy for peak or stage-specific power. That is legitimate only if the target quantity is also a mean.
- **"At in vivo strain and shortening duration" is stronger than the source.** The abstract says "*similar* strain and shortening durations *to those found in vivo*". Those in vivo values were themselves *derived*: from spine positions estimated from silhouettes, combined with red-to-white gearing ratios from sonomicrometry cross-validation. The work-loop output is a measurement. The conditions it was measured under are model-estimated. My inference is that this does not demote the 142.7 value from "measured", but the claim should say "at estimated in vivo conditions".

## 3. Hidden assumption: one preparation's mean is representative

The claim's SCOPE line says the value "**bounds** what fast muscle has been MEASURED to deliver in a teleost fast-start." That framing assumes a single preparation's mean represents the fast muscle of the whole body, and of teleosts in general. Relaxing that assumption:

- Wakeling, Kemp & Johnston (1999) J Exp Biol 202:3057, PMID 10539954. **Read-level: abstract.** These authors report, from *calculated* (not work-loop-measured) contraction regimes in carp, "a decrease in muscle-mass-specific power output ... in a posterior direction along the body due to systematic variations in fibre strain." So mass-specific power varies with myotome position. One number depends on where the preparation was taken from, and a mean from one site is neither an upper nor a lower bound for the whole fish. Which myotomal position the 142.7 W/kg preparation came from is `unknown` at abstract level.
- One measured value in one species is a data point, not a bound. The paper's abstract reports only this one work-loop number. If there are higher or lower work-loop values for teleost fast muscle, they would be counter-examples to "bounds". My negative search here was limited: PubMed esearch for "work loop white muscle fish power output", "fast-start muscle power fish W kg", and "Wakeling JM Johnston IA". It returned no other abstract with a teleost work-loop W/kg figure. The scope of that search is tiny, so this is **not** evidence that 142.7 W/kg is a maximum.

## 4. Evidence level

`measured` is **honest** for the 142.7 W/kg value. It is a direct work-loop measurement on isolated fast fibres, and the claim does not present a derived number as measured. Two qualifications:
- The "in vivo" strain and duration settings are derived (see §2).
- The second half of the claim says power predicted from swimming sequences "**matched** the work-loop measurements at all temperatures tested." The abstract says "**similar to**". The predicted values are calculated, and the abstract quantifies neither the agreement nor the error bars, so "matched" overstates it. Also, the abstract reports a work-loop number for *Sc. notata* only. It does not state whether work loops were run in this paper at every habitat temperature (0 °C Antarctic through ~20 °C) or whether values from other studies were used for comparison. The phrase "the work-loop measurements at all temperatures tested" therefore cannot be verified from the abstract and is `unknown`.

## 5. Regime and taxon

The claim's own SCOPE line already says correctly that *Scorpaena* (Scorpaenidae) is not *Danio* and that 20 °C is not typical zebrafish rearing temperature. I endorse that. One addition: carp (*Cyprinus carpio*) is a cyprinid like *Danio*, and Wakeling et al. 2000, PMID 10938257 (**read-level: abstract**), show that thermal acclimation changes fast-start white-muscle strain (+33 % with acclimation temperature, −50 % with acute temperature) and contraction duration. That strengthens the existing caveat: the 142.7 W/kg value should not be carried across to zebrafish at a different temperature without adjustment.

The paper's title, "Muscle power output limits...", is the authors' interpretation, not a measurement. The claim quotes it correctly as the title.

## What survives and what is corrected

- **Survives:** 142.7 W/kg muscle; fast myotomal fibres; *Scorpaena notata*; 20 °C; work-loop; evidence level `measured`; correct citation.
- **Corrected wording:**
  1. "at in vivo strain and shortening duration" → "at strain and shortening duration similar to those estimated in vivo".
  2. "matched ... at all temperatures tested" → "were reported as similar (agreement not quantified in the abstract)". Whether work loops were measured at every temperature in this paper is `unknown`.
  3. "bounds what fast muscle has been measured to deliver" → "is one measured cycle-mean value from a single species and preparation site". It is not a bound, and peak power and position along the body are `unknown`.

```swarm-challenge
{"claim_id": 309, "outcome": "weakened", "reason": "The 142.7 W/kg work-loop value, species, temperature and 'measured' level are confirmed verbatim in the abstract, but the claim upgrades 'similar to' into 'matched' and 'at in vivo strain' when the source says strain was only similar to in vivo values that were themselves model-derived, and it calls a single-species, single-site cycle-mean value a 'bound' even though mass-specific power is shown to vary along the body.",
  "corrected_value": null,
  "depends_on": ["PMID 9556535 abstract (Wakeling & Johnston 1998), read-level abstract, fetched 2026-11-04", "PMID 10539954 abstract (Wakeling, Kemp & Johnston 1999), read-level abstract: longitudinal variation in calculated muscle-mass-specific power in carp", "PMID 10938257 abstract (Wakeling et al. 2000), read-level abstract: thermal acclimation effects on carp fast-start muscle strain", "Limited PubMed esearch (3 queries) for other teleost work-loop power values: none found, scope too narrow to establish a maximum"]}
```
