# Claim 309: what it requires at the cell and organ scales

**Source claim (tissue scale, evidence: measured).** Fast myotomal fibres of
*Scorpaena notata* (small red scorpionfish, family Scorpaenidae) deliver a mean
muscle-mass-specific power of 142.7 W/kg at 20 °C. This was measured by work-loop
at in vivo strain and shortening duration. The same paper reports that power
predicted from swimming sequences matched the work-loop values at every
temperature tested.

**Subject on every line below.** The subject is *Scorpaena notata* unless
another animal is named. The claim is not about zebrafish, and nothing below
treats it as one. No measurement from another species is used to refute or
satisfy a constraint. Such numbers appear only as cross-species context, and the
animal is named beside each.

## Sources and read-levels

| # | Source | Animal | Read-level |
|---|--------|--------|------------|
| S1 | Wakeling JM & Johnston IA (1998) *J Exp Biol* 201:1505–1526, doi:10.1242/jeb.201.10.1505, PMID 9556535 | *Sc. notata* plus 5 other teleosts | **abstract** (Europe PMC). Full text paywalled at journals.biologists.com ("You do not currently have access") |
| S2 | Johnston IA, van Leeuwen JL, Davies MLF, Beddow T (1995) *J Exp Biol* 198:1851, doi:10.1242/jeb.198.9.1851 | *Myoxocephalus scorpius* (short-horned sculpin, Cottidae), 15 °C | abstract |
| S3 | James RS & Johnston IA (1998) *J Exp Biol* 201:913, doi:10.1242/jeb.201.7.913 | *M. scorpius* | abstract |
| S4 | Wakeling JM (2001) *Comp Biochem Physiol A* 131:31, doi:10.1016/s1095-6433(01)00461-5 | review of teleosts, mostly carp | abstract |
| S5 | Askew GN & Marsh RL (2002) *J Exp Biol* 205:2153, doi:10.1242/jeb.205.15.2153 (its comparison table) | quail; table row said to be "scorpion fish" | **search-summary only**. The table was not seen: scispace.com is blocked from this session and the JEB page is paywalled |
| S6 | An unidentified secondary paper, quoted by a web-search summary, giving *Sc. notata* V0 | *Sc. notata*? | **search-summary only**. The source was not identified or opened; fishlab.ucdavis.edu is blocked from this session |

**What I could not reach.** I did not see Table 2 of S1, which holds the
*Sc. notata* contractile properties. S1's strain, shortening duration, cycle
frequency, fast-muscle mass fraction and predicted hydrodynamic powers are all
unknown to me. Every number attributed to S5 or S6 below comes from an AI search
summary and is treated as unverified. I do not use any of them to set a status.

**A sentence that failed verification.** One web-search summary attributed to S1
the statement that power "declined at cycle frequencies simulating unsteady
swimming (burst-and-glide, 10 Hz; C-start, 15 Hz)". That sentence is **not** in
the S1 abstract retrieved from Europe PMC. I cannot place it, so it is not used.

## A definitional issue that affects every constraint

S1's abstract calls 142.7 W/kg a "mean muscle-mass-specific power", but it does
not say what the mean is taken over.

S2 is from the same lab and the same kind of preparation, but on a different
animal, the sculpin at 15 °C. It reports two figures:

- **Averaged over the whole cycle:** "in the range 24–31 W kg-1 wet muscle mass".
- **Instantaneous, during shortening:** "175–265 W kg-1".

S3 (sculpin) gives maximum instantaneous powers of 307 and 222 W/kg.

**My inference, not the authors' statement:** 142.7 W/kg is far above the
sculpin's cycle-averaged values and below its instantaneous peaks. That position
is consistent with a mean taken over the shortening phase only, but I cannot
confirm it without S1's methods. The species and temperature differ (sculpin at
15 °C versus scorpionfish at 20 °C), so this is context only. It does not
contradict claim 309.

It matters below: whether the mean covers the shortening phase or the whole
cycle changes the energy each contraction needs by roughly the inverse of the
duty cycle.

## Constraints

### C1 — cell — range: shortening velocity must lie below the fibre's unloaded maximum

**Requirement.** To produce net positive power, the fibres' strain rate during
the work loop must lie strictly between 0 and V0, the maximum unloaded
shortening velocity of *Sc. notata* fast fibres at 20 °C. To deliver power near
the peak of the power–velocity curve, V/V0 should sit in roughly [0.15, 0.5].

That band is a generic property of the Hill-type force–velocity curve; it is
**assumed** here, not measured for this species. The hard requirement is the
open interval (0, 1).

**Check.** No primary value was retrieved for either side:

- **V0 of *Sc. notata* fast fibres:** S1's Table 2 is not accessible.
- **In vivo strain rate:** not in S1's abstract.

The only numbers come from search summaries (S5, S6):

- **Strain rate 5.1 L/s** in a "scorpion fish" row (S5).
- **V0 13.2 L/s at 20 °C** for *Sc. notata* (S6).

If both were confirmed, V/V0 would be about 0.39. That is **derived from two
unverified search-summary numbers**. It is not an observation and is not used
for the status.

**Status: open.** Nobody's measurement contradicts the requirement. The check
needs S1's Table 2.

### C2 — cell — timescale: activation and relaxation must fit inside one shortening phase

**Requirement.** Fibres must activate and then relax largely within one half
tail-beat. Otherwise they resist re-lengthening on the next half-cycle and
destroy net work. This means the twitch time-to-peak plus the time to 50%
relaxation must be no longer than the in vivo shortening duration.

I write the bound as a ratio: the twitch duration (time-to-peak plus 50%
relaxation) divided by the shortening duration, with lo = 0 and hi = 1. A ratio
near 1 implies a large loss of work. The value of 1 is a generic work-loop
expectation that I **assumed**; it is not a measured threshold.

**Check.** I searched Europe PMC for:

- "Scorpaena notata" with muscle, swimming or fast-start: 32 hits, none on
  muscle physiology. They were on parasites, peptide hydrolysates, ecology and
  metal content.
- "white muscle" fish twitch with "time to peak", "half-relaxation" or
  "contraction time": no *Scorpaena* hit.

S1's Table 2 probably holds the twitch kinetics, going by its listed contents in
the search summary, but it is not accessible.

**Status: open.** This is a case of "not found, because the source holding it
was paywalled". It is not "people looked and found nothing".

### C3 — cell — energetic: chemical energy must be on hand without waiting for oxidative supply

**Requirement.** A fast-start lasts tens to hundreds of ms. That is too short for
blood-borne oxidative supply to matter, so the work must come from stores
already inside the fibre (ATP plus a phosphagen buffer, then glycolysis).

**Energy needed per contraction (derived):**

- Mechanical work per kg of muscle = P × t. The mean power P is 142.7 W/kg, over
  whatever interval the mean covers (see the definitional issue above). The
  value of t is unknown for *Sc. notata*.
- Chemical energy per kg of muscle = (P × t) / η, where η is the fibres'
  mechanical efficiency.

**Value of t (illustration only):** if the unverified frequency of 10.9 Hz from
S5 were right, one half-cycle would be about 46 ms. That would give about 6.5 J
of mechanical work per kg of muscle for one shortening. This is **derived from
an unverified input**.

**Check.** I found no measurement of phosphocreatine or ATP content, or of
mechanical efficiency, for *Sc. notata* fast muscle. Searches:

- Europe PMC, (phosphocreatine OR "creatine phosphate") AND "white muscle" AND
  fish with burst or exhaustive exercise: 8 hits, none giving a fast-start-scale
  depletion figure for a scorpaenid.
- Europe PMC, phosphocreatine or high-energy phosphate in fish muscle by title:
  mostly human and rat hits.

I have not retrieved phosphagen values for any teleost in this session, so I
quote none.

**Status: open.** This is an unchecked case, not a negative finding. The
requirement is real, but its size cannot be computed without S1's shortening
duration.

### C4 — organ — conservation (energy): muscle power must account for whole-body hydrodynamic power

**Requirement.** Over the fast-start, the mechanical power delivered to the body
and water by the whole fast muscle mass (142.7 W/kg × fast-muscle mass) must be
at least the rate at which kinetic energy appears in the fish and its added mass
of water, plus losses. If the muscle delivered too little, the observed
acceleration would need an energy source that does not exist. If the muscle
delivered far more than the hydrodynamic requirement, transmission efficiency
must be correspondingly low.

The quantity bounded is the ratio of predicted muscle power (from kinematics) to
measured work-loop power. My tolerance window of [0.5, 2] is **assumed**.

**Check.** S1's abstract states: "At all temperatures, the predicted mean
muscle-mass-specific power outputs, as calculated from swimming sequences, were
similar to the muscle power outputs measured from work-loop experiments."

**Caveats:**

1. This is the authors' claim, read at **abstract** level. I have not seen the
   numbers, so I cannot say how close "similar" is.
2. The "predicted" side is **calculated** from kinematics through a muscle
   model. It is not an independent measurement of force or work.
3. It is the same paper's internal consistency, not an outside replication.

S4 (abstract, a carp-dominated review) supports the same mechanism generally:
central trunk muscle produces most of the power, and it reaches the water
through caudal myotomes. That is a different animal and not used for the status.

**Status: satisfied**, on the authors' explicit statement. The evidence is
literature at abstract level, and the size of the agreement is unknown.

### C5 — organ — spatial: whole-body curvature must produce the strain the work loop imposed

**Requirement.** A work-loop strain is "in vivo" only if it follows from body
geometry. Fibre strain equals spine curvature times the fibre's distance from
the neutral axis, divided by the gearing ratio set by fibre helicity. That
product must match the strain used in the work loop within a factor of about 2.
The factor is **assumed**.

**Check.** S1 says the work loops used strains similar to those found in vivo.
It also says gearing ratios "must decrease towards the tail with a corresponding
change in muscle geometry, resulting in similar white muscle fibre strains in
all the myotomes". In S1 the strain is an input chosen from kinematics, so the
match holds by construction, and it is not an independent test.

I did not see the *Sc. notata* strain value. A "strain 0.14" is attributed to
the scorpion fish in S5, but only by search summary.

Cross-species context only: in sculpin at 15 °C (S2), the peak-to-peak strain
calculated from backbone curvature was about 0.16 at 0.32 L, 0.19 at 0.52 L and
0.15 at 0.77 L. That is a calculation from silhouettes, not sonomicrometry.

**Status: open.** S1's numbers are not accessible, and the S1 check is circular
by design. No independent sonomicrometry for *Sc. notata* was found. The
Europe PMC search on "Scorpaena notata" turned up no muscle-strain paper.

## Summary

| ID | Scale | Kind | Status | Why |
|----|-------|------|--------|-----|
| C1 | cell | range | open | V0 and strain rate are in S1's Table 2, which is paywalled; the only numbers are unverified search summaries |
| C2 | cell | timescale | open | no *Sc. notata* twitch kinetics reachable; the Europe PMC search found nothing |
| C3 | cell | energetic | open | the size of the requirement depends on a shortening duration not available; no phosphagen data for a scorpaenid |
| C4 | organ | conservation | satisfied | the authors state that predicted and measured power agree at all temperatures (abstract-level) |
| C5 | organ | spatial | open | the strain is circular by construction in S1; no independent *Sc. notata* strain was found |

**Nothing is unsatisfiable.** No measured number about *Sc. notata* that I could
reach contradicts any constraint. The sculpin numbers (S2, S3) are a different
family and temperature. They neither refute nor confirm claim 309, and the
"mean" in claim 309 may be defined differently from S2's cycle average.

**The most useful next step** is to get S1's full text (Table 2 and the work-loop
methods). That single document would probably settle C1, C2 and C5 and fix the
size of C3.

```swarm-entail
{"source_claim": 309, "source_scale": "tissue",
  "constraints": [
    {"target_scale": "cell", "kind": "range",
      "statement": "During the work loop, fast-fibre shortening velocity must lie strictly below the fibres' unloaded maximum shortening velocity (V/V0 in (0,1)), and for near-maximal power it should lie roughly at 0.15-0.5 of V0",
      "quantity": "V/V0 of Sc. notata fast fibres during in vivo-strain work loops at 20 C", "lo": 0, "hi": 1, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "Not checked against a primary value. Sc. notata V0 and in vivo strain rate are in Wakeling & Johnston 1998 Table 2 and methods, which are paywalled. Search summaries attribute 5.1 L/s strain rate (Askew & Marsh 2002 table) and V0 13.2 L/s at 20 C (unidentified source) to Sc. notata; neither was seen, and the derived V/V0 of about 0.39 is not used for the status",
      "satisfied_evidence": "unknown",
      "note": "Wakeling & Johnston 1998 J Exp Biol 201:1505, doi:10.1242/jeb.201.10.1505 (abstract only). Askew & Marsh 2002 doi:10.1242/jeb.205.15.2153 (search-summary only; scispace.com blocked, JEB paywalled). The 0.15-0.5 optimum band is a generic Hill-curve assumption, not a measurement for this species"},
    {"target_scale": "cell", "kind": "timescale",
      "statement": "Fast-fibre activation and relaxation (twitch time-to-peak plus 50% relaxation) must complete within about one in vivo shortening duration, so that the fibres do not resist re-lengthening on the next half-cycle",
      "quantity": "(twitch time-to-peak + 50% relaxation time) / in vivo shortening duration, Sc. notata fast fibres at 20 C", "lo": 0, "hi": 1, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "No Sc. notata twitch kinetics reached. Europe PMC search 'Scorpaena notata' AND (muscle OR swimming OR fast-start) gave 32 hits, none on muscle contractile physiology; a fish white-muscle twitch-time search gave no scorpaenid hit. Wakeling & Johnston 1998 Table 2 likely holds the values but is paywalled",
      "satisfied_evidence": "unknown",
      "note": "This means the data were not reachable; it is not a finding that people looked and found nothing. hi=1 is an assumed generic work-loop threshold"},
    {"target_scale": "cell", "kind": "energetic",
      "statement": "Chemical energy for one fast-start contraction (mechanical work / efficiency, i.e. 142.7 W/kg times the averaging interval divided by efficiency) must already be stored in the fibre (ATP, phosphagen, glycolytic flux), because oxidative supply cannot respond within tens of ms",
      "quantity": "intracellular high-energy phosphate available per kg fast muscle vs (142.7 W/kg x shortening duration)/efficiency", "lo": null, "hi": null, "units": "J/kg muscle",
      "status": "open",
      "satisfied_by": "The size of the requirement cannot be computed: the shortening duration and the averaging interval of the 'mean' are not available from the abstract. Illustration (derived from an unverified 10.9 Hz search-summary frequency): about 6.5 J/kg mechanical work per 46 ms half-cycle. No phosphagen, ATP or efficiency measurement for a scorpaenid was found",
      "satisfied_evidence": "unknown",
      "note": "Europe PMC searches: phosphocreatine/creatine phosphate AND 'white muscle' AND fish AND burst/exhaustive (8 hits, none usable); phosphocreatine in fish muscle by title (mostly mammalian). Same lab, different animal: sculpin at 15 C, Johnston et al. 1995 doi:10.1242/jeb.198.9.1851, reports cycle-average power 24-31 W/kg vs instantaneous 175-265 W/kg, so the averaging definition changes this requirement several-fold"},
    {"target_scale": "organ", "kind": "conservation",
      "statement": "Whole-body energy balance: power from the fast-muscle mass must account for the rate at which kinetic energy is given to the body and added water mass during the fast-start, plus losses",
      "quantity": "predicted muscle-mass-specific power from swimming kinematics / measured work-loop power, Sc. notata and the other 5 species", "lo": 0.5, "hi": 2, "units": "dimensionless",
      "status": "satisfied",
      "satisfied_by": "Wakeling & Johnston 1998 abstract: 'At all temperatures, the predicted mean muscle-mass-specific power outputs, as calculated from swimming sequences, were similar to the muscle power outputs measured from work-loop experiments.' This is the authors' claim; the 'predicted' side is calculated from kinematics through a muscle model, not separately measured",
      "satisfied_evidence": "literature",
      "note": "Read at abstract level; how close 'similar' is was not seen. The check is internal to one paper. The 0.5-2 window is assumed. Wakeling 2001 review doi:10.1016/s1095-6433(01)00461-5 (abstract, mostly carp) supports the mechanism of central muscle power transmitted to the tail, but in a different animal"},
    {"target_scale": "organ", "kind": "spatial",
      "statement": "Fibre strain implied by whole-body curvature (curvature x distance from the neutral axis / gearing ratio) must match the strain imposed in the work loop within about a factor of 2",
      "quantity": "kinematic in vivo fast-fibre strain / work-loop strain, Sc. notata", "lo": 0.5, "hi": 2, "units": "dimensionless",
      "status": "open",
      "satisfied_by": "In Wakeling & Johnston 1998 the work-loop strain is chosen from kinematics, so a match holds by construction and is not an independent test; the Sc. notata strain value was not seen (0.14 in the Askew & Marsh 2002 table by search summary only). No independent sonomicrometry for Sc. notata was found",
      "satisfied_evidence": "unknown",
      "note": "Context from a different animal only: sculpin at 15 C, Johnston et al. 1995, peak-to-peak strain about 0.16/0.19/0.15 at 0.32/0.52/0.77 L, calculated from backbone curvature. The factor-2 window is assumed"}
  ]}
```
