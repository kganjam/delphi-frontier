# Challenge 286: adversarial review of the challenge to the "unsatisfied existence constraint"

**Date:** 2026-11-04. **Status:** adversarial desk review of claim 286. **I ran no experiment and no
simulation.** Every number below is either a literature value with its read-level stated, or my own
arithmetic, labelled as such in the sentence.

**Verdict: WEAKENED.** Two of the claim's three limbs survive independent checking and one is
strengthened by evidence the claim omitted. The third limb is **wrong**: "produced mechanically"
does not contradict the framework's §7, because the framework's own §2 calls the same step
"mechanical". The molecular attribution inside limb 1 is also conflated, and the claim conceals a
live sign conflict between its own two load-bearing sources.

---

## 0. The claim under review

> "Challenge to the 'unsatisfied existence constraint': a voltage-gated reader (Cacna1g/Cav:
> cacna1g LOF long fins, cilnidipine overgrowth, Cav-dependent depolarisation-evoked Ca2+ spikes in
> cultured fin fibroblasts) was published in Le Bleu 2025, so reader is not 'undemonstrated'; but
> the generator voltage effect in fibroblasts is unmeasured and in-vivo fin readouts (DiSBAC2(3))
> show depolarisation, so 'generator demonstrated' also fails; and 'produced mechanically'
> contradicts the framework own section 7 ('Nothing automates entailment'). Fibroblast Vm
> unmeasured. Not re-read by harvester."

Recorded evidence level `derived`, value `n/a`.
Source: branch `claude/challenge-243-bioelectric-claim-g6xwy2`, `docs/research/fish/challenge-243.md`
(read-level: **full-text**, read from git).

Four limbs: **(1)** the reader is not undemonstrated; **(2)** "generator demonstrated" also fails;
**(3)** "produced mechanically" contradicts §7; **(4)** fibroblast Vm is unmeasured.

Primary sources I read myself:

| Source | Read-level |
|---|---|
| Le Bleu et al. 2025, *Development* 152: dev204739, PMC13078715 | **full-text** (two WebFetch passes, chars 0–100 000 and 30 000+; final 5 812 chars unread) |
| Perathoner et al. 2014, *PLoS Genet* 10: e1004080, PMC3894163 | **full-text** (chars 0–100 000; final 18 025 unread) |
| Jiang et al. 2024, *PLoS Biol* 22: e3002565 | **full-text** (chars 0–100 000 of 210 783) |
| `docs/architecture/cross-scale-constraints.md`, `origin/swarm-architecture` | **full-text** (read from git) |
| `docs/research/fish/challenge-243.md` | **full-text** (read from git) |
| GXL `claims/support` query behind the `unsatisfied` upgrade | **could-not-access** — no API from this session |
| Hegle et al. 2006, *PNAS* 103: 2886 | **not consulted** — not load-bearing for claim 286 |

---

## 1. Arithmetic, redone independently from the stated inputs

I recomputed everything in the chain from the numerators and denominators, without copying the
author's working. Script: `/tmp/claude-0/-workspace-delphi-frontier/d4692297-6bff-5535-9790-d09dcf387d2b/scratchpad/recheck.py`.

**(a) One number in the chain is wrong — and it is wrong in the published paper, not only in the
challenge.** Le Bleu 2025's KCl-excitable fibroblast fractions, as printed in the paper, against my
recomputation:

| Condition | Printed | n/d | My recomputation |
|---|---|---|---|
| DMSO | 39 % | 70/109 | **64.22 %** — mismatch |
| Amlodipine (L) | 12 % | 15/127 | 11.81 % — ok |
| Cilnidipine (L/N) | 4 % | 4/103 | 3.88 % — ok |
| PD17132 (N) | 20 % | 29/147 | 19.73 % — ok |

Three of four agree to within rounding. The DMSO control does not: 70/109 is 64 %, not 39 %. For
39 % to be right the numerator would have to be ≈ 42.5/109, which is not an integer count. So
either the printed percentage or the printed count for the control is in error; **which one is
`unknown`**, and I did not open the figure source data. Challenge 243 transcribed the pair
"70/109 cells (39 %)" verbatim and **did not flag the inconsistency**. That is a transcription
defect in the parent document.

**Is it load-bearing? No.** The cilnidipine block is 3.88 % against a control of either 39 % or
64 %, i.e. a **10.0× or 16.5× reduction** (my calculation). The direction and the order of magnitude
survive either reading. Claim 286 drops the numbers entirely, so it does not inherit the error — but
anything downstream that quotes "39 %" is quoting a figure its own counts contradict.

**(b) GXL tallies check out.** Test 0 + 1 + 34 = **35**; control 28 + 0 + 7 = **35**. Equal budgets,
so comparable in size. I could **not** re-run the query (read-level **could-not-access**), so these
remain author-reported.

**(c) The §6 bookkeeping gap is an omission, not an arithmetic error.** Before the upgrade:
1 satisfied + 4 open + 1 "plausible, unmeasured" = **6** ✓. After commit `de44fffd` moved C3 to
`unsatisfied`: 1 satisfied + 3 open + 1 unsatisfied = 5 enumerated, + C6 unenumerated = **6** ✓.
Challenge 243 said this "sums to 5, not 6"; my independent count shows the missing item is C6 and
the entailment total is consistent. Minor, and challenge 243 said as much.

**(d) A quantity nobody in the chain computed.** 80 mM KCl, the stimulus behind the entire
"depolarisation-evoked" demonstration, clamps Vm to a calculable value. **This is my calculation,
not an observation.** Nernst slope at 28 °C = 59.75 mV/decade; with [K⁺]ᵢ assumed 120–140 mM
(**unmeasured in these cells — assumed, not observed**) and [K⁺]ₒ 80–83 mM:

> E_K = **−9.6 to −14.5 mV**

Against the generator's hypothesised set-point — Perathoner's oocyte E_K of −90 to −100 mV — the
assay therefore applies a step of **+77 to +87 mV in the depolarising direction** (my calculation).
See §3 and §5 for why that matters.

---

## 2. Is a proxy standing in for the quantity that matters? Yes — three of them

**Proxy 1: DiSBAC2(3) relative fluorescence for Vm.** Claim 286 writes "in-vivo fin readouts
(DiSBAC2(3)) show depolarisation" as a flat statement. What the dye delivers is **uncalibrated
relative intensity**. Perathoner reports Fig. S4 as "average pixel intensity, not calibrated
voltage" (full-text); Jiang reports "photon counts per pixel" by time-correlated single photon
counting and **gives no mV** (full-text). DiSBAC2(3) is a slow-response anionic oxonol whose signal
arises from the dye physically redistributing and binding intracellular protein and membrane, at
roughly **1 % fluorescence change per mV**, and the oxonol literature treats it as semi-quantitative
unless calibrated under voltage clamp (read-level **search-summary**, general slow-oxonol and
DiBAC₄(3) literature; I found **no** dedicated DiSBAC2(3) limitations study). Perathoner's own
Discussion hedges: the dye experiments "suggest that this might indeed be the case."

**The right quantity** is calibrated resting Vm and ΔVm, in mV, of fibroblast-lineage cells in
*alf*/+ and *lof*/+ fins and in the regenerate blastema. It is **`unknown`** (§4).

**Proxy 2: a +80 mV KCl step for a physiological bioelectric signal.** The reader was demonstrated
in the regime my §1(d) calculation puts near −13 mV, roughly +80 mV away from the hypothesised
generator set-point. The hypothesised physiological signal's magnitude is `unknown`. So the assay
establishes *that these cells carry functional Cav channels*, which is a weaker proposition than
*that they read a bioelectric gradient*.

**Proxy 3: "fin" for three different structures.** Claim 286's "in-vivo fin readouts" silently pools
**embryonic pectoral fin bud at 48 hpf** (Jiang 2024, full-text), **juvenile caudal fin** (Perathoner
Fig. S4, full-text) and **adult caudal fin regenerate blastema** (Le Bleu 2025, full-text). These are
different structures at different stages. Pooling them is a regime conflation, and §5 shows it hides
a contradiction.

---

## 3. Limb-by-limb, against the framework's own definitions

### Limb 1 — "reader is not 'undemonstrated'": **survives, and is understated**

The framework's schema defines `unsatisfied` as "nothing known satisfies it", and §6's C3 reads
"a voltage-sensitive transducer that reads the potential", flagged "open — and this is the
load-bearing gap", with §6 arguing from "if **no voltage-sensitive transducer is known in fin
mesenchyme**". One named candidate refutes that. Le Bleu 2025 supplies several, and **two pieces of
evidence stronger than anything claim 286 cites**, both of which claim 286 omits:

- **In-vivo, genotype-dependent Ca²⁺ dynamics.** GCaMP6s imaging in regenerating fins:
  *"In contrast, very few cacna1g^b1477/b1477 fin regenerate cells showed Ca2+ transients"*,
  concluding *"the Cacna1g T-type channel enables Ca2+ dynamics in the distal fibroblast-lineage
  blastemal mesenchyme"* (full-text). This is in vivo, in the right cell lineage, in the right
  structure.
- **Localisation.** Single-cell transcriptomics and in situ place L-, N- and T-type Cav channels in
  fibroblast-lineage blastema mesenchyme (full-text).

So limb 1 is right, and claim 286 argued it on its *weakest* available evidence (a culture assay)
while leaving the in-vivo result on the table. **My inference:** C3 should read "candidate satisfiers
named and localised in fin mesenchyme (L-, N-, T-type Cav); in-vivo coupling to Vm undemonstrated" —
not `unsatisfied`.

**But the molecular label inside limb 1 is conflated, and this is a real defect.** Claim 286 bundles
three items under one heading, "(Cacna1g/Cav: ...)". They do not belong to one molecule:

- *cacna1g* LOF long fins and the in-vivo GCaMP result → **T-type, Cacna1g**. Genetics.
- cilnidipine overgrowth → the authors call cilnidipine *"the dual L/N-type Ca2+ channel blocker"*
  (full-text, verbatim). This is evidence about **L- and/or N-type channels, not Cacna1g.**
- the cultured-fibroblast spikes → blocked most potently by cilnidipine. The Discussion says
  *"The L- and N-type Ca2+ inhibitor, cilnidipine, displayed the most potent block of
  depolarization-induced Ca2+ flux"*, and proposes that T- and L/N-type channels **cooperate**
  (full-text).
- **The T-type-selective blocker's result is not reported.** ML218 (5 µM) appears only in Le Bleu's
  Methods. The Results never mention it; the Discussion gives only a general statement about L-, N-
  and T-type inhibition. So **the voltage-dependence of Cacna1g specifically, in cultured
  fibroblasts, is unreported** — the one molecule claim 286 names.

Limb 1's *existence* conclusion is unaffected: the satisfier set is larger, not smaller. But the
label "Cacna1g/Cav" as the carrier of "cilnidipine overgrowth" and of the "Cav-dependent
depolarisation-evoked Ca2+ spikes" is **wrong as attribution**, and it is exactly the kind of label
that propagates.

### Limb 2 — "'generator demonstrated' also fails": **survives**

Confirmed independently against C1's own wording, "a generator of a potential difference **across
fin mesenchyme**":

- Perathoner's conductance and voltage data are **heterologous**: ≈ 2-fold K⁺ conductance increase
  over wild-type cRNA, Vm shifted "towards −90 to −100 mV", in **Xenopus oocytes** (full-text). No
  wild-type per-construct mV is given in the text.
- **No absolute in-vivo mV anywhere.** Perathoner: none for fin cells (full-text). Jiang: none
  (full-text). Le Bleu: none — it refers only to "differential resting membrane potential" as a
  possible explanation for heterogeneous cell states (full-text).

So what is demonstrated is that the alleles change K⁺ conductance in heterologous cells and change
fin size. A potential difference across fin mesenchyme, of known sign and magnitude, is **not**
demonstrated. Limb 2 holds.

**One correction to how claim 286 states it.** "In-vivo fin readouts show depolarisation" is an
incomplete rendering of Perathoner Fig. S4, whose legend reports **both** directions: wild-type fins
"showed localized hyperpolarization", and *"alf fins in contrast show high levels of depolarization
across the fin"* (N = 21–23, p < 0.001, pixel intensity). **My inference:** a *localised* wild-type
polarisation that is *flattened* in the long-finned mutant is not obviously "the wrong sign" for a
gradient mechanism — it is closer to what a gradient mechanism predicts. Claim 286's one-word
summary drops the spatial structure that is the most mechanism-relevant part of the figure.

### Limb 3 — "'produced mechanically' contradicts the framework's own §7": **refuted**

This limb is wrong, and I can show it from the framework's own text.

§2 of `cross-scale-constraints.md`, introducing the very propagation step at issue, reads:

> "This is the whole idea, and **it is mechanical rather than clever**."

§7 reads:

> "**Nothing automates entailment.** A human or agent writes the constraints a claim implies, and a
> wrong or incomplete set produces false confidence..."

These are different predicates. §7 denies **automation** — that the constraint set writes itself.
§2 asserts **mechanicalness** in the sense of following by routine entailment rather than by
insight, and §7's own next clause ("a human or agent writes the constraints") is perfectly
consistent with an agent executing a routine procedure. The parent claim's phrase was "produced
mechanically by propagating a DNA-scale claim down one scale" — which is §2's word, for §2's step.
§6 even uses the matching scale language: "It took a claim at the DNA scale, propagated it to the
cell scale."

So there is **no contradiction**. Challenge 243 quoted §7 and appears not to have reached §2's
sentence. Challenge 243 itself hedged to "overstates this"; claim 286 hardened that into
"contradicts", which the text does not support. **Limb 3 fails.**

(What *does* survive, and is worth keeping: §7's own caveat that C2–C6 "are marked open because
**nobody has looked**, which is different from having looked and found nothing." The defect in the
parent framework is the upgrade of C3 from `open` to `unsatisfied` on one unmatched query — a
procedure the framework's §3 says should instead be settled by "you look". That is a real criticism
of the *status assignment*. It is not a criticism of the word "mechanically".)

### Limb 4 — "fibroblast Vm unmeasured": **survives**

My own negative result, with scope stated. **Scope:** one extended web search for a measured
resting membrane potential of zebrafish fin mesenchyme / blastema fibroblasts (patch clamp,
microelectrode or calibrated indicator), plus full-text checks of all three primary papers above.
**Finding:** no measured value found. The nearest hit is zebrafish **fast skeletal muscle** at
≈ −82 mV by intracellular microelectrode in situ (read-level **search-summary**) — a different
tissue, so not an answer. I did not search Europe PMC programmatically and did not open Le Bleu's or
Jiang's supplementary data; a value hiding there is possible. On this scope, **fin fibroblast Vm is
`unknown`**, and claim 286 is right.

Claim 286 nonetheless states this negative **without any scope**, which the honesty floor requires
beside the finding. "Not re-read by harvester" flags provenance, not search extent. Minor defect.

---

## 4. The hidden assumption, tested relaxed

**The assumption carrying the verdict:** that limbs 1 and 2 may be judged at **different evidence
thresholds** — limb 1 at "is a candidate named?", limb 2 at "is in-vivo ΔVm measured?" Relax it and
require one uniform threshold, and the conclusion changes:

- **Uniform lenient** ("named molecule + heterologous/in-vitro voltage dependence + LOF or GOF fin
  phenotype"): the generator passes *and* so does the reader. The parent claim's "generator
  demonstrated" is then **true**, and only "reader not demonstrated" fails.
- **Uniform strict** ("in-vivo coupling to measured Vm"): the generator fails *and* so does the
  reader — Le Bleu states that Ca²⁺ fluxes and *"their potential origins from dynamic membrane
  voltages"* "have not been directly linked to fin size restoration" (full-text, verbatim). The
  parent claim's "reader not demonstrated" is then **true**, and only "generator demonstrated" fails.

Under **either** uniform threshold, **exactly one** half of the parent asymmetry fails — not both.
"Both halves fail", and challenge 243's stronger "the asymmetry is close to inverted", hold only
under the mixed threshold.

**Is the mixed threshold illegitimate? Not entirely** — and this is the claim's best defence. The
framework's two labels genuinely have different thresholds *in the framework's own schema*:
`unsatisfied` means "nothing known satisfies it", a universal negative that one candidate refutes;
`satisfied` means demonstrated, which "not measured in the relevant cells" refutes. So the claim is
exploiting an asymmetry the framework wrote, not one it invented. **My inference:** the defensible
statement is the symmetric one — *neither* side's coupling to in-vivo Vm is demonstrated, and the
chain is open at its Vm link on both sides — which is what challenge 243's own §6 concedes, and
which does **not** support "the asymmetry is inverted".

**A second assumption, relaxed:** that generator and reader are distinct parts. Jiang 2024 breaks
this cleanly and claim 286 does not use it. Jiang's proposal (full-text, flagged by the authors as a
Discussion hypothesis, not a tested result) is that *"the increased K+-channel activity first
hyperpolarizes the membrane potential, and this increase... immediately activates Na+ channels to
depolarize the cells"*, so that *"Kcnk5b activity promotes depolarization via Na+ channels"*. On that
account the in-vivo generator of the measured potential is **Na⁺ channels**, not the K⁺ channel —
a named in-vivo generator route that claim 286's "generator ... unmeasured" framing passes over.
Still no mV, so limb 2 stands; but "nothing generates" would be wrong.

---

## 5. The counter-example the claim missed: its own two sources disagree on sign

This is the most substantial thing claim 286 omits, and the honesty floor forbids averaging it away.

- **Jiang et al. 2024** (embryonic pectoral fin bud, 48 hpf; DiSBAC2(3), relative photon counts;
  full-text): depolarisation **promotes** growth. *"Kcnk5b-induce depolarization is required for
  Kcnk5b-enhanced growth."* Blocking Na⁺ channels with vinpocetine and dibucaine impaired
  Kcnk5b-induced bud growth. Depolarisation is reported to **increase** during outgrowth.
- **Le Bleu et al. 2025** (adult caudal fin regenerate; full-text): depolarisation-activated Cav
  channels **restrain** growth. Blocking them (cilnidipine, 5 µM in vivo, 4 h/day, 5–28 dpa) causes
  overgrowth; *cacna1g* LOF gives long fins. Title: *"restraining ... regenerative outgrowth"*.

**My inference, stated as mine:** these two cannot both describe one monotonic
depolarisation→growth relation. If depolarisation opens Cav channels and Cav channels restrain
growth, depolarisation should restrain growth — the opposite of Jiang. The two can be reconciled by
stage, structure or non-monotonicity (embryonic bud vs adult regenerate; Na⁺- vs Ca²⁺-mediated), but
**no published reconciliation is known to me** (scope: the three full-text reads above plus the
searches in §2 and §3; I did not search specifically for a reconciling paper).

Claim 286 leans on Jiang/Perathoner for "in-vivo readouts show depolarisation" and on Le Bleu for
"the reader", and presents the result as a tidy symmetric gap. It is not tidy: **its two load-bearing
sources are in direct sign conflict on the sign of the effect the mechanism is supposed to have.**
That conflict strengthens limb 2 — "generator demonstrated" is in even worse shape than claim 286
says, since the field disagrees about which direction the signal even runs — while making limb 1's
"reader" harder to interpret, because what the reader is supposed to be reading is itself disputed.

**A regime point, as my inference from standard biophysics, not from either paper:** T-type channels
activate at relatively negative potentials and their availability *increases* on hyperpolarisation as
steady-state inactivation is relieved. So under a *hyperpolarising* generator (Perathoner's oocyte
−90/−100 mV), Cacna1g availability should rise → more Ca²⁺ → more restraint → **shorter** fins, which
contradicts the long-finned *alf*. Under Jiang's *depolarising* in-vivo picture, L/N-type channels fit
the direction naturally. So the sign logic closes for **L/N-type**, not for the T-type molecule claim
286 names — a further reason the attribution in §3 matters.

---

## 6. Is the evidence level honest?

**`derived` is defensible for the verdict; `derived` understates the provenance problem in one
place.** Claim 286 is a reasoning verdict over literature, so `derived` is the right kind, and
`value: n/a` is right because there is no scalar in dispute. The honest part is "Not re-read by
harvester" — provenance flagged rather than hidden. Challenge 243 was likewise explicit that it did
not re-read Perathoner or Jiang.

Two honesty defects, both minor:

1. **"In-vivo fin readouts (DiSBAC2(3)) show depolarisation"** is stated flatly, as if observed at
   the level the sentence implies. It is an **uncalibrated, hedged, pixel-intensity proxy** in two
   papers, one of which also reports the *opposite* direction in wild type, and neither 243 nor 286
   read it at source. Honest form: "relative DiSBAC2(3) intensity, uncalibrated; *alf* fins
   depolarised across the fin while wild type shows localised hyperpolarisation (N = 21–23); authors
   present it as suggestive."
2. **"Fibroblast Vm unmeasured"** is a negative with no stated search scope (§3, limb 4).

And one defect inherited from the parent: the unflagged 39 % / 70-of-109 inconsistency (§1a).

---

## 7. What I could not do

- **GXL not re-queried** (read-level **could-not-access**). Its corpus contents, and the content of
  the single "refutes" passage, remain `unknown`. Whether Le Bleu 2025 is in the corpus is `unknown`.
  Claim 286 does not rest on the query, so this does not affect my verdict.
- **Three papers read to 100 000 characters only** (Le Bleu final 5 812 chars; Perathoner final
  18 025; Jiang final 110 783 of 210 783). Supplementary data and figure source data not opened. A
  measured Vm or an ML218 result hiding there would change §3.
- **Daane 2018, Yi 2021, Stewart 2021, Hegle 2006: not consulted by me.** They carry none of claim
  286's four limbs.
- **Negative search scopes** are stated beside each negative finding in §2, §3 and §5 rather than
  collected here.

---

## 8. Verdict

Claim 286's core survives: the framework's C3 was not `unsatisfied` under the framework's own
definition, "generator demonstrated" does not hold for fin mesenchyme Vm, and fin fibroblast Vm is
unmeasured on the scope I searched. Limb 1 is in fact **stronger** than the claim argued, since the
in-vivo GCaMP result in *cacna1g* mutants goes unmentioned.

It is **weakened**, not refuted, by four findings:

1. **Limb 3 is wrong.** The framework's §2 calls the propagation step "mechanical rather than
   clever"; §7 denies *automation*, a different predicate. No contradiction. The real defect in the
   parent is the `open` → `unsatisfied` upgrade on one unmatched query, which is a criticism of the
   status assignment, not of the word "mechanically".
2. **The molecular attribution is conflated.** Cilnidipine is the authors' "dual L/N-type blocker";
   it is not evidence about Cacna1g. The T-type-selective blocker's in-vitro result is **unreported**
   in Le Bleu's Results. The satisfier is a fibroblast-lineage Cav *ensemble*, L/N by pharmacology
   and T-type by genetics, not "Cacna1g/Cav".
3. **"Both halves fail" needs a mixed evidence threshold.** Under either uniform threshold exactly
   one half fails. The defensible statement is the symmetric one.
4. **Its two load-bearing sources disagree on sign** — Jiang 2024 has depolarisation promoting
   growth, Le Bleu 2025 has depolarisation-gated channels restraining it — and the claim does not
   say so.

Plus the inherited, unflagged arithmetic defect of §1(a).

```swarm-challenge
{"claim_id": 286, "outcome": "weakened", "reason": "Limbs 1, 2 and 4 survive independent full-text checking and limb 1 is stronger than argued (in-vivo GCaMP in cacna1g mutants, unmentioned), but limb 3 is refuted because the framework's own section 2 calls the propagation step 'mechanical rather than clever' while section 7 denies only automation, the 'Cacna1g/Cav' label wrongly attributes cilnidipine (the authors' 'dual L/N-type blocker') and the depolarisation-evoked spikes to Cacna1g while Le Bleu's T-type-selective blocker result is unreported, 'both halves fail' requires a mixed evidence threshold, and the claim's own two sources contradict each other on whether depolarisation promotes or restrains growth.",
  "corrected_value": "Le Bleu 2025 DMSO-control KCl-excitable fibroblast fraction = 64% (70/109), not the 39% printed in the paper and copied unflagged by challenge-243; cilnidipine block is therefore 16.5x not 10x (dimensionless fractions, my recomputation). 80 mM KCl clamps Vm to -9.6 to -14.5 mV (my Nernst calculation at 28 C, assuming [K]in 120-140 mM, unmeasured), i.e. a +77 to +87 mV depolarising step from the hypothesised generator set-point.",
  "depends_on": ["LeBleu2025-Development-152-dev204739-PMC13078715 (full-text, read here): cacna1g b1477/b1477 and b1478/b1478 long fins; cilnidipine 5 uM 4 h/day 5-28 dpa overgrowth, authors' words 'the dual L/N-type Ca2+ channel blocker'; 80 mM KCl excitable fractions DMSO 70/109 printed 39%, amlodipine 15/127, cilnidipine 4/103, PD17132 29/147; ML218 in Methods only, no Results data; GCaMP6s 'very few cacna1g b1477/b1477 fin regenerate cells showed Ca2+ transients'; no Vm in mV anywhere; 'their potential origins from dynamic membrane voltages have not been directly linked to fin size restoration'",
    "Perathoner2014-PLoSGenet-10-e1004080-PMC3894163 (full-text, read here): ~2-fold K+ conductance over wild-type cRNA in Xenopus oocytes, Vm 'towards -90 to -100 mV'; Fig S4 DiSBAC2(3) wild-type 'localized hyperpolarization' and alf 'high levels of depolarization across the fin', N=21-23, p<0.001, average pixel intensity; no in-vivo mV",
    "Jiang2024-PLoSBiol-22-e3002565 (full-text, read here): embryonic pectoral fin bud 48 hpf; DiSBAC2(3) photon counts per pixel, no mV; 'Kcnk5b activity promotes depolarization via Na+ channels'; 'Kcnk5b-induce depolarization is required for Kcnk5b-enhanced growth'; depolarisation PROMOTES growth",
    "cross-scale-constraints.md section 2 (origin/swarm-architecture, full-text, read here): 'This is the whole idea, and it is mechanical rather than clever' -- THE INPUT THAT REFUTES LIMB 3",
    "cross-scale-constraints.md section 7 (same, full-text): 'Nothing automates entailment'; and 'C2-C6 are marked open because nobody has looked, which is different from having looked and found nothing'",
    "cross-scale-constraints.md section 6 (same, full-text): C1 'satisfied -- the channels themselves, demonstrated'; C3 'open -- and this is the load-bearing gap'; 'a generator of a potential difference across fin mesenchyme'",
    "db/designswarm/0013_cross_scale_constraints.sql definition of 'unsatisfied' as 'nothing known satisfies it' (via challenge-243, NOT read by me) -- limb 1 rests on this definition",
    "challenge-243.md on claude/challenge-243-bioelectric-claim-g6xwy2 (full-text, read from git)",
    "unknown: resting Vm and dVm in mV of fin fibroblast-lineage cells in vivo. Negative search scope: one extended web search for patch-clamp/microelectrode/calibrated-indicator values in zebrafish fin mesenchyme or blastema, plus full-text checks of the three papers above; no value found; supplementary data not opened",
    "unknown: whether Le Bleu 2025's DMSO control error is in the printed percentage or in the printed count; figure source data not opened",
    "could-not-access: GXL claims/support query (0/1/34 test, 28/0/7 control, author-reported in commit de44fffd, arithmetic re-verified to 35 each but not re-run); corpus contents and the single 'refutes' passage remain unknown",
    "search-summary: slow-response oxonol / DiBAC4(3) literature on DiSBAC2(3) being uncalibrated and semi-quantitative, ~1% fluorescence change per mV; no dedicated DiSBAC2(3) limitations study found",
    "search-summary: zebrafish fast skeletal muscle resting potential ~-82 mV by intracellular microelectrode in situ (different tissue; cited only to show what a measured value would look like)",
    "my inference, not from either paper: T-type availability rises on hyperpolarisation as steady-state inactivation is relieved, so a hyperpolarising generator predicts the wrong fin phenotype for Cacna1g while the sign logic closes for L/N-type",
    "my calculation, not an observation: Nernst E_K at 28 C for [K]out 80-83 mM and assumed [K]in 120-140 mM",
    "assumption I tested and found load-bearing: that limb 1 may be judged at 'is a candidate named?' while limb 2 is judged at 'is in-vivo dVm measured?'. Under either uniform threshold exactly one half of the parent asymmetry fails, not both"]}
```
