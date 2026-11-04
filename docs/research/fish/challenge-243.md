# Challenge 243: "the generator is demonstrated, the reader is not"

**Date:** 2026-11-04. **Status:** adversarial desk review. I ran no experiment and no simulation.
**Verdict: REFUTED.** Both halves of the central asymmetry fail as stated, and so does the
"produced mechanically" clause. A narrower statement survives; it is given in §6.

## 0. The claim and where it comes from

> "The published bioelectric mechanism therefore has an UNSATISFIED EXISTENCE CONSTRAINT at its
> centre: the generator is demonstrated, the reader is not. That is sharper than 'not fully
> understood', and it was produced mechanically by propagating a DNA-scale claim down one scale
> rather than by intuition."
> Recorded evidence level: `derived`. Source: cross-scale constraint framework plus the GXL check.

I located the sources on the `origin/swarm-architecture` branch, reading the full text of each:

- `docs/architecture/cross-scale-constraints.md`, from commit `415dae51` (2026-11-04 01:21 −0800).
  Its §6 table marks C1 (generator) **satisfied**, described as "the channels themselves,
  demonstrated". It marks C3 (a voltage-sensitive transducer) as **open, and the load-bearing gap**.
- The message of commit `de44fffd` (2026-11-04 01:28 −0800). It moves C3 from `open` to
  `unsatisfied`, on the strength of a GXL `claims/support` query that returned
  **0 supports / 1 refutes / 34 neutral** for *"A voltage-sensitive transducer reads membrane
  potential in zebrafish fin mesenchyme to control ray growth"*. The positive control was
  *"Potassium channel mutations regulate fin size in zebrafish"*, which returned 28 / 0 / 7.
- The schema `db/designswarm/0013_cross_scale_constraints.sql` defines `unsatisfied` as
  "nothing known satisfies it".

The claim therefore asserts three things:

- **(a)** C1 is satisfied by demonstration.
- **(b)** C3 is unsatisfied: nothing known reads the voltage.
- **(c)** The procedure that produced (a) and (b) was mechanical.

## 1. Arithmetic, redone independently

There is little arithmetic in the claim. What exists checks out:

- GXL test query: 0 + 1 + 34 = 35 passages. Control: 28 + 0 + 7 = 35. Both scored the same
  35-passage budget, so the two results are comparable in size. These are counts reported by the
  author (`de44fffd`). I did not re-run the GXL query, because I have no access to that API from
  this session.
- The §6 table: 6 constraints, of which 1 is satisfied, 4 are open (C2–C5) and 1 is
  "plausible, unmeasured" (C6). After `de44fffd` the commit reports
  "6 entailed, 1 satisfied, 3 open and 1 unsatisfied". That sums to 5, not 6. C6's status is not
  stated there; I assume it was recorded as `assumed`. This is a minor bookkeeping gap. It is not
  load-bearing.

None of the defects below is arithmetic.

## 2. Half (b) fails: a voltage-sensitive reader is published, in fin fibroblasts

**Le Bleu HK, Kioussi RG, Henner AL, Lewis VM, Stewart S, Stankunas K (2025).** *Voltage-gated
calcium channels generate blastema Ca2+ fluxes restraining zebrafish fin regenerative outgrowth.*
*Development* 152(23): dev204739, doi:10.1242/dev.204739, PMC13078715.
Read-level: **full-text** (first 100 000 of 105 812 characters, via WebFetch). This is the same
paper that the sibling study S11-D read independently (commit `aae8754b`).

What the paper reports. These are quotations or close paraphrases of the authors:

- **Phenotype.** Two *cacna1g* loss-of-function alleles give long fins: *"both
  cacna1g^b1477/b1477 and cacna1g^b1478/b1478 fish regenerated exceptionally long caudal fins"*.
  Cacna1g is a T-type voltage-gated Ca²⁺ channel.
- **Pharmacology.** Daily 5 µM cilnidipine, a Cav blocker, from 5 to 28 dpa *"caused significant fin
  overgrowth"*.
- **Voltage dependence in the right cell type.** *"Membrane depolarization of isolated fin
  fibroblasts triggered voltage-gated Ca2+ channel-dependent Ca2+ spikes."* S11-D's scan gives the
  counts: 70/109 cells (39 %) responded to 80 mM KCl, and 4/103 (4 %) did so under cilnidipine.
- **The authors' conclusion.** *"'bioelectricity' for fin size control reflects voltage-modulated
  Ca2+ fluxes"* in fibroblast-lineage blastema cells. Calcineurin is named as the likely effector.

That is a named, voltage-gated transducer, expressed and functional in fin mesenchyme (the
fibroblast lineage), with a loss-of-function phenotype on fin size. It was published in 2025,
before the framework was written. The framework defines `unsatisfied` as "nothing known satisfies
it". Le Bleu 2025 is a known candidate satisfier, so **C3 is not unsatisfied by that definition.**

**The authors' own limit, preserved.** Le Bleu et al. state that Ca²⁺ fluxes and *"their potential
origins from dynamic membrane voltages have not been directly linked"*, and they measured no Vm.
The voltage dependence is shown in **cultured** fibroblasts under KCl. In vivo, the link from the
K⁺-channel genotype to Cav gating is not shown. So C3 should read **"candidate satisfier named
(Cacna1g / Cav); in-vivo coupling to Vm undemonstrated"**. It should not read "unsatisfied". This
paragraph is my inference from the authors' text.

**Why the GXL check said zero.** This is my inference. The paper's title nearly paraphrases the GXL
query, yet the engine returned 0 supports. That means one of three things:

- the GXL corpus does not contain Le Bleu 2025 (corpus coverage: `unknown`, because I cannot
  inspect it);
- the engine did not match it;
- it is the single "refutes" passage (that passage's content is `unknown`; the author did not
  record it).

The control does not license reading the zero as informative. The control was a short, generic,
heavily-replicated claim. The test was a five-clause, cell-type-specific claim. A control that
shows the engine finds well-established generic facts says nothing about its **sensitivity** for
recent, specific facts. This is the same mismatch the author later measured as "limitation one"
in commit `699f320d`. A matched control would be a specific claim known to be in the literature,
at comparable specificity. None was run.

## 3. Half (a) fails: the generator is not demonstrated where the constraint needs it

The framework's own C1 reads "a generator of a potential difference **across fin mesenchyme**".
The evidence the channels actually have, as tabulated from full-text reads in S11-D (commit
`aae8754b`, `docs/research/fish/S11-deepen.md`), is:

- **Perathoner et al. 2014** (*PLoS Genet* 10:e1004080, PMC3894163). Two-electrode voltage clamp in
  Xenopus oocytes shows about 2× K⁺ conductance, with Vm moving toward −90 to −100 mV. This is
  **heterologous**. The same paper's Fig. S4 uses DiSBAC2(3) in juvenile fins and reports that
  *alf* fins show **depolarisation**, not hyperpolarisation (N = 21–23).
- **Jiang et al. 2024** (*PLoS Biol* 22:e3002565). Overexpressing Kcnk5b **depolarises** fin-bud
  cells, as read by DiSBAC2(3).
- **Daane 2018, Yi 2021 and Stewart 2021** measured no fin Vm. Stewart 2021 calls "characterizing
  membrane potentials" a future step.

Read-levels: these are S11-D's full-text reads, and I did not re-read them. For **Daane 2018**
(*Sci Rep* 8:10391, PMC6039437) and **Yi 2021** (*eLife* 10:e60691), my own read-level is
**search-summary**. Both summaries agree that the work measured channel conductance and its
calcineurin regulation (S345, in Yi), not fin Vm.

So what is demonstrated is that **the alleles alter K⁺ conductance** (in oocytes and HEK cells) and
alter **fin size**. A potential difference across fin mesenchyme, of known sign, is **not
demonstrated**. The only in vivo fin readouts point the opposite way from the canonical sign. The
resting Vm of fin fibroblasts is `unknown`: S11-D searched Europe PMC and the web, with a positive
and a negative control on that search. The status of C1 should therefore be **"candidate generator
with heterologous conductance evidence; in-vivo ΔVm sign disputed and unmeasured in the relevant
cells"**. This is my inference.

**Proxy named.** The claim uses *"the channel alters K⁺ conductance in a heterologous cell"* as a
proxy for *"a potential difference exists across fin mesenchyme"*. The quantity that matters is
in-vivo ΔVm, and resting Vm, of fibroblast-lineage blastema cells in *alf*/+ and *lof*/+ fins.
It is `unknown`.

**Net effect.** The asymmetry is close to **inverted**. The reader has a named molecule, a
loss-of-function fin phenotype, and voltage-dependent function in fin fibroblasts (in vitro). The
generator has a fin phenotype and heterologous conductance data, but in vivo voltage data of the
**wrong sign**. Neither link to fin Vm is demonstrated in vivo. "Generator demonstrated, reader not"
is therefore false in both halves. "Neither coupling to in-vivo Vm is demonstrated" is supported.
This is my inference.

## 4. Half (c) fails: "produced mechanically" contradicts the framework's own text

The source document's §7 says: *"Nothing automates entailment. A human or agent writes the
constraints a claim implies, and a wrong or incomplete set produces false confidence."* The six
constraints were hand-written. The statuses were assigned by reasoning, and the document's §7 says
so: *"derived by reasoning from the mechanism, not extracted from the literature."*

"Mechanically" overstates this. The procedure is a **checklist applied by an agent**, which is
useful but not mechanical. It also produced a false negative in this very case, because nobody ran
the "you look" step that §3 says makes existence cheap to test. Le Bleu 2025 is the obvious place
to look.

On "down one scale": the source sentence that gets propagated, *"A bioelectric gradient patterns fin
ray length"*, is a tissue-scale claim. Moving from it to cell-scale requirements is a step down.
Calling the starting claim "DNA-scale" (the alleles) and the target "cell-scale" would be a step
**up**. The wording in §6 and in the commits mixes the two. This is a minor framing inconsistency.

On "sharper than not fully understood": the need for a transducer, and Cav channels as the
standard candidate, is stated in the field's own literature. Le Bleu 2025 frames its whole study
that way. So the observation is not a novel product of the framework. It is the field's current
open question, and the field has already proposed a specific answer. This is my inference.

## 5. Hidden assumption: generator and reader are distinct parts

The framework assumes that a voltage signal needs a separate, dedicated reader. With that
assumption relaxed:

- **The generator can be its own reader.** EAG-family K⁺ channels can signal through
  voltage-dependent conformation, independently of ion flux. Hegle, Marble & Wilson 2006 (*PNAS*
  103:2886–2891, PMID 16477030; read-level **search-summary**) found that non-conducting EAG still
  drives fibroblast and myoblast proliferation, and that open-state-favouring mutations suppress
  it. *kcnh2a* is an ERG-subfamily member of the same KCNH family. Whether this applies to *kcnh2a*
  or to fins is `unknown`, and I cite it only as a precedent that the roles can coincide in one
  molecule.
- **The reader need not be voltage-gated.** Any electrodiffusive flux of a signalling ion depends
  on Vm through its driving force. That is physics, not a hypothesis. Yi 2021 measured
  intracellular [K⁺] with KIRIN FLIM (per S11-D), which is a non-voltage readout of channel
  activity.

So in its generic form ("something reads it"), the existence constraint is close to unfalsifiable.
In its specific form ("a dedicated voltage-sensitive transducer"), it has a published candidate.
Neither form yields "unsatisfied". This is my inference.

## 6. Is the evidence level honest?

Recording the claim as `derived` is honest about the constraint **table**. It is not honest about
the status upgrade to `unsatisfied`. That upgrade rests on an **observation**: one search-engine
query, at search-summary level, with an unmatched control. That observation is presented as
confirming a derivation. The right label for the negative is
**"one GXL query, corpus unknown, sensitivity for specific claims unmeasured; contradicted by
Le Bleu 2025"**.

**What survives, in narrower form.** In zebrafish fin, neither the K⁺-channel alleles' effect on
in-vivo membrane voltage nor the voltage gating of the proposed Cav/Cacna1g reader has been
demonstrated in vivo. The mechanism chain is therefore open **at its Vm link on both sides**, not
specifically at a missing reader. This matches S11-D's independent conclusion.

## 7. Scope of my searches

- **Repository.** `git log --all --grep` over all 642 remote branches for "existence", "GXL",
  "cross-scale", "transducer", "calcineurin" and "S31". I also ran `git grep` of three branches for
  the claim text. No S31 result file exists: S31 was dispatched but I found no deliverable.
- **Web.** Three standard searches, for Yi 2021, Daane 2018 and Hegle 2006, plus one full-text
  WebFetch of PMC13078715. I did **not** re-read Perathoner 2014, Jiang 2024 or Stewart 2021
  myself; those rest on S11-D's full-text reads.
- **GXL.** Not re-queried, because I have no access. Its corpus contents and the one refuting
  passage are `unknown`.

```swarm-challenge
{"claim_id": 243, "outcome": "refuted", "reason": "A voltage-gated reader (Cacna1g/Cav: cacna1g LOF long fins, Cav-dependent depolarisation-evoked Ca2+ spikes in fin fibroblasts) was published in Le Bleu 2025, so C3 is not 'unsatisfied', while the generator's in-vivo voltage effect is unmeasured in fibroblasts and the only in-vivo fin readouts show the opposite sign, so 'generator demonstrated, reader not' fails in both halves and 'mechanical' contradicts the framework's own section 7.", "corrected_value": null, "depends_on": ["LeBleu2025-Development-dev204739-PMC13078715: cacna1g-/- long fins; cilnidipine overgrowth; depolarisation of cultured fin fibroblasts triggers Cav-dependent Ca2+ spikes; no Vm measured (full-text, read here)", "S11-D (commit aae8754b, docs/research/fish/S11-deepen.md): full-text reads of Perathoner2014, Jiang2024, Stewart2021, Yi2021, Daane2018", "Perathoner2014-PMC3894163: Fig5 oocyte hyperpolarisation (heterologous); FigS4 alf fins depolarised by DiSBAC2(3), N=21-23 (via S11-D)", "Jiang2024-PLoSBiol-e3002565: Kcnk5b overexpression depolarises fin bud cells (via S11-D)", "unknown: in-vivo resting Vm and dVm of fin fibroblast-lineage cells", "cross-scale-constraints.md section 7 (origin/swarm-architecture, commit 415dae51): 'Nothing automates entailment'", "commit de44fffd: GXL 0/1/34 for reader query, 28/0/7 control (author-reported, not re-run)", "assumption: GXL control of a generic claim does not establish sensitivity for a specific claim", "Hegle2006-PNAS-103-2886: ion-independent voltage-driven EAG signalling (search-summary; precedent only, not shown for kcnh2a)"]}
```
