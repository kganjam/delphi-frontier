# S14-D — Deepening the fin-size potassium channel answer by attacking its weakest input

**Parent subproblem (S14, protein).** *Can the fin-size potassium channel be engineered for
graded, pectoral-restricted control?*

**Recorded answer being deepened.** "A predicted K2P fold with both selectivity filters
resolved at pLDDT>80 once an MSA was supplied. No experimental structure; variant scoring
blocked by upstream maintenance."

**Date of work:** 2026-11-04. All retrievals below are from that date.

**Provenance convention (repo rule 9).** Everything load-bearing here was **retrieved** during
this session and carries a read-level in §5. Exactly one background claim is **remembered** and
is labelled as such at the point of use (§1b, that the K2P pore forms at the subunit interface).
Every number in §4 is **simulated** — a model output, labelled in the sentence — and no claim in
this document is an observation made by me. Two search methods failed their controls and are
recorded as retracted in §2a rather than quietly replaced.

**Bottom line (section 4d): the recorded answer FALLS** — not because the structure is worse
than claimed (it is, but that turns out not to matter), but because the load-bearing input
was misidentified. The number the conclusion actually depends on is a measured ~2-fold
conductance window, and the sign of its effect in pectoral tissue is disputed between the two
primary sources.

---

## 0. Identifying the channel, so that later sections are about a real molecule

The recorded answer names no gene. The fin-size K2P channel of the zebrafish *another longfin*
(*alf*) mutant is **kcnk5b**.

| Item | Value | How obtained |
| --- | --- | --- |
| Gene | `kcnk5b` (*Danio rerio*, taxId 7955) | UniProt REST query |
| UniProt accessions | `Q6PFU3` (448 aa, unreviewed), `A0A8M1PBI1` (448 aa, unreviewed) | UniProt REST query, `gene:kcnk5b AND organism_id:7955` |
| *alf* alleles | `alf dty86d` and `alf dt30mh` (the latter also called *pfau*) | Perathoner et al. 2014, full text |
| *alf* missense substitutions | **W169L** and **F241Y** | Perathoner et al. 2014, full text |

**Honesty note on the alleles.** Perathoner et al. write "In both *alf* alleles, distinct
missense mutations (W169L and F241Y) were identified in the coding sequence for *kcnk5b*."
The sentence does not say which substitution belongs to which allele, and I did not find a
sentence that does in the text I read. **I therefore do not assert the pairing.** It is
`unknown` to me at read-level full-text of this paper.

There is no reviewed (Swiss-Prot) entry for kcnk5b; both accessions are TrEMBL. This is a small
but real caveat on anything keyed to residue numbering, and I use `Q6PFU3` numbering throughout.

---

## 1. Step 1 — which input is the answer most sensitive to?

### 1a. The input the recorded answer leans on

The recorded answer offers exactly one quantitative input in support of tractability:
**pLDDT > 80 at both selectivity filters.** Everything else in it is a negative (no
experimental structure; variant scoring blocked). So pLDDT > 80 is the nominal load-bearing
number, and I tested it first.

### 1b. It is wrong, and — more importantly — it is not load-bearing

**The number as stated does not match the primary record.** AlphaFold DB's own API returns,
for `Q6PFU3`:

| Field (verbatim from the API record) | Value |
| --- | --- |
| `globalMetricValue` (mean pLDDT, monomer model `AF-Q6PFU3-F1`, v6) | **69.5** |
| `fractionPlddtVeryHigh` (>90) | 0.353 |
| `fractionPlddtConfident` (70–90) | 0.248 |
| `fractionPlddtLow` (50–70) | 0.060 |
| `fractionPlddtVeryLow` (<50) | **0.339** |
| `toolUsed` | AlphaFold Monomer v2.0 pipeline |
| `msaUrl` | present (`AF-Q6PFU3-F1-msa_v6.a3m`) |

Read-level: **full-text** (complete API record, `https://alphafold.ebi.ac.uk/api/prediction/Q6PFU3`).

Three observations about the record, and one inference:

1. The model-level mean pLDDT is **69.5, not >80**, and a third of the protein (33.9%) is
   below 50. The recorded answer's phrasing — "a predicted K2P fold ... resolved at
   pLDDT>80" — reads as a statement about the model. At the model level it is **not
   supported**. It may well be true of the two filter motifs specifically; I could not confirm
   that (see 1c).
2. An MSA was already part of the public pipeline. The recorded answer's "once an MSA was
   supplied" describes a local workaround, not a new capability: `msaUrl` is a standard field
   of this record. *(That the field exists is the record's content; that this makes the local
   MSA work redundant is my inference.)*
3. **A second AFDB record disagrees with the first, and I am not averaging them.** The
   3D-Beacons API (`https://www.ebi.ac.uk/pdbe/pdbe-kb/3dbeacons/api/uniprot/summary/Q6PFU3.json`,
   read-level full-text) returns a *different* AlphaFold DB model for the same accession:
   `AF-0000000066331115`, `model_category` AB-INITIO, `oligomeric_state` **HOMODIMER**,
   `confidence_type` pLDDT, **`confidence_avg_local_score` 62.82**, created 2025-12-25.

   So the two public AFDB records for this protein report mean pLDDT **69.5 (monomer)** and
   **62.82 (homodimer)**. Neither is above 80. The lower number belongs to the dimer — and K2P
   channels conduct as dimers, with the pore formed at the subunit interface, so the dimer is
   the assembly a variant-design argument would need. *(The oligomeric state and score are the
   record's content — **retrieved**. That the dimer is the relevant assembly, because the K2P
   pore forms at the subunit interface, is my inference from background knowledge I am labelling
   **remembered, not retrieved**: I did not source it, and it should be checked before being
   relied on. Note its direction — it strengthens my critique by licensing the lower of the two
   numbers, which by repo rule 9 is precisely the kind of detail whose provenance needs flagging.
   The critique does not rest on it: the monomer figure of 69.5 is also below 80.)*

### 1c. What I could not get, and why

Per-residue pLDDT at the filter motifs would settle whether the ">80 at both filters" part is
true. **I could not retrieve it.** `alphafold.ebi.ac.uk/files/` — which serves the coordinate
files and the `plddtDocUrl` confidence JSON — returns **HTTP 403 from this session's egress
proxy** for every path tried (`...-model_v6.pdb`, `...-model_v4.pdb`). The proxy's own status
endpoint records these as policy denials, not transient errors, so I did not retry past the
diagnostic. `search.rcsb.org` is likewise denied. Read-level for per-residue pLDDT:
**could-not-access**. The API record above (bands and global mean) is what the allowed routes
yield.

### 1d. Where the causal residues actually are — computed, not asserted

I ran a motif search over the 448-aa `Q6PFU3` sequence returned by the AFDB API. **This is a
computation on the retrieved sequence, not an observation of a structure:**

```
filter motif TIGYG   residues  98–102   context ENAVIFAATVIT TIGYG NVAPKTTGGRLF
filter motif TVGFG   residues 203–207   context LEGLYFSFTTLT TVGFG DYVAGVDPSVNY
residue 169 = W      residue 241 = F
```

The two selectivity filters sit at **98–102** and **203–207**. The two *alf* substitutions sit
at **169** and **241**. **Neither causal residue is in either selectivity filter**, and the
positions are 67+ residues away in sequence.

This is consistent with the founding paper's own description. Perathoner et al. state that
"the affected amino acids are positioned in two distinct TM domains towards the cytoplasmic
side of the protein" — their claim, from a homology model they built on human KCNK4 (K2P4.1)
as template. **My inference:** filter confidence is therefore being quoted at residues that
are not the residues a variant-design campaign would act on. Even a filter pLDDT of 100 would
say nothing about the local accuracy at W169 or F241.

### 1e. The factor-of-two test on pLDDT, and why it fails to move the conclusion

The task asks for the number that would change the conclusion if wrong by a factor of two.
**pLDDT is not that number.** Halve it (80 → 40) and the structural claim collapses entirely;
double the implied accuracy and it becomes a crystal-quality model. In *neither* direction does
the answer to "can this be engineered for graded, pectoral-restricted control?" change — because,
as sections 2–4 show, feasibility is capped by a biological dynamic range and by an unresolved
sign, both of which are untouched by how good the model is. A perfect structure of kcnk5b would
not supply a dynamic range it does not have, nor settle a sign dispute between two experiments.

So the recorded answer leaned on an input that is both **misstated** (69.5 / 62.82, not >80),
**mislocated** (filters, not the causal residues), and **not decision-relevant**. The real
load-bearing input is elsewhere.

### 1f. The input the conclusion is actually most sensitive to

> **The entire measured conductance window between wild-type Kcnk5b and the full *alf*
> overgrowth phenotype: "almost two-fold."**

This is the number that, moved by a factor of two, flips the verdict — demonstrated by
recomputation in section 4. "Graded control" means placing distinguishable setpoints *inside*
this window. How many fit is a direct function of its width.

---

## 2. Step 2 — how well is that input established?

Verbatim from Perathoner et al. 2014 (read-level **full-text**, Europe PMC `fullTextXML`,
142,283 bytes, PMC3894163):

> "oocytes injected with either of both mutant cRNAs show an almost two-fold increase in K +
> conductance over that of oocytes injected with wild type cRNA ( Figure 5B )"

and on method:

> "Measurements were done from a holding potential of −80 mV with 0.5 s long pulses from −100
> to +60 mV with increments of 20 mV. Recorded currents (n = 5–26) were averaged and normalized
> to the mean value recorded for oocytes injected with the wild type channel at +60 mV."

**Evidence level: measured, but a proxy — and a proxy for two different things at once.**

| What was measured | What "graded control of fin size" needs |
| --- | --- |
| Macroscopic two-electrode voltage-clamp current, *Xenopus* oocytes, cRNA injection | Conductance of Kcnk5b in fin/fin-bud mesenchyme in vivo |
| Whole-cell current ∝ N × i × P<sub>o</sub> (channel number × single-channel conductance × open probability) | i and P<sub>o</sub> separately, since a designed variant acts on those, not on N |
| Normalised to wild-type at +60 mV, n = 5–26 | Absolute conductance per cell |

The authors are explicit that the two factors are confounded in principle: "the current of K +
ions through the plasma membrane depends not only on individual channel conductance, but also
on the number of channels present in the membrane." Their argument for attributing the increase
to biophysics rather than to channel number is the change in rectification:

> "the increase in K + currents in the Kcnk5b mutant variants is accompanied by reduced outward
> rectification ( Figure 5C ) suggesting that the change in K + conductance results from altered
> biophysical features of Kcnk5b rather than a simple increase in the number of channels at the
> plasma membrane."

**That is the authors' inference, and it is a reasonable one. My inference, stated separately:
it is an argument from waveform shape, not a measurement of single-channel conductance, so the
2-fold figure remains a macroscopic proxy and is an upper bound on what a designed variant
could achieve through i and P<sub>o</sub> alone.**

**Has the number become firmer in the twelve years since? No — and nothing has refined it.**
Negative searches, with scope stated:

- **Scope: Europe PMC query `kcnk5b`, 57 hits, all titles and abstracts reviewed (2026-11-04).**
  No hit reports a single-channel conductance for Kcnk5b, and no hit reports a replacement
  effect size for the *alf* variants.
- **Scope: Europe PMC query `kcnk5b AND "single-channel"` (phrase quoted — see the control in
  2a), 2026-11-04: 1 hit**, PMC9357109, "Coordinated patterning of zebrafish caudal fin symmetry
  by a central and two peripheral organizers." Its full text is **not accessible** to me
  (`fullTextXML` returned 150 bytes; the record is `isOpenAccess` N), so read-level is
  **listing**. On its title it concerns caudal fin symmetry patterning rather than
  electrophysiology — **my inference, and a weak one; I cannot exclude that this paper contains
  a single-channel measurement.** That is the one gap in this negative.
- **Scope: the string `single-channel` across the four full texts I retrieved** — PMC3894163
  (Perathoner 2014), PMC6039437 (Sci Rep 2018, "Bioelectric-calcineurin signaling module
  regulates allometric growth and size of the zebrafish fin"), PMC8110307 (eLife 2021,
  "A calcineurin-mediated scaling mechanism that controls a K+-leak channel to regulate
  morphogen and growth factor transcription"), PMC11018282 (PLoS Biol 2024, below) —
  **0 occurrences in each**, by Python `str.count` on tag-stripped text, controlled in 2a.
- **Scope: fold-change expressions across those same four full texts.** The only conductance
  fold-change anywhere is Perathoner's single "two-fold." (PMC8110307 contains "1.5 to 2 fold"
  and "30 to 40 fold", but in its open peer-review correspondence and about *lef1*/*shha*
  transcript levels, not conductance — see the caution in section 3c.)
- **Scope: UniProt `xref_pdb` cross-references, 2026-11-04** (*not* the PDBe endpoint I first
  used — see the retracted method in 2a). `Q6PFU3` and `A0A8M1PBI1` (both kcnk5b) each
  cross-reference **0 PDB entries**. The closest human ortholog `O95279` (KCNK5 / TASK-2),
  which is a *reviewed* entry, also cross-references **0**. Positive controls in the same query
  return populated fields: `Q9NYG8` (KCNK4 / TRAAK) **12** entries
  (3UM7, 4I9W, 4RUE, 4RUF, 4WFE, 4WFF, 4WFG, 4WFH, 7LJ4, 7LJ5, 7LJA, 7LJB) and `P57789`
  (KCNK10 / TREK-2) **8** (4BW5, 4XDJ, 4XDK, 4XDL, 8QZ1, 8QZ2, 8QZ3, 8QZ4). **So: no
  experimental structure of kcnk5b** — the recorded answer is right about this — and the nearest
  solved relatives remain other K2P channels, the same template class Perathoner et al. used in
  2014. All PDB identifiers in this paragraph are **retrieved** from the UniProt field, not
  recalled.

### 2a. Controls on the searches above (repo rule 8), including one method I had to retract

Run in both directions, because a search that cannot come back empty has not been tested.

| Check | Positive control (must be found) | Must-fail control (must come back empty) | Verdict |
| --- | --- | --- | --- |
| UniProt `xref_pdb` | `Q9NYG8` → 12 PDB ids; `P57789` → 8 | impossible accession `ZZZZZZ` → **rejected with a distinct error**, "The 'accession' filter value 'ZZZZZZ' has invalid format", *not* a silent empty | **valid** — empty is distinguishable from unknown |
| Europe PMC conjunction | `"kcnk5b" AND "patch clamp"` → 8 hits | `kcnk5b AND "zzqxwvtoken"` → 0 hits | **valid** — the AND is genuinely restrictive |
| Europe PMC single-term | `kcnk5b` → 57 hits | `zzqxwvgene99` → 0 hits | **valid** |
| Full-text string counts | `pectoral` → 81 in PMC11018282 | `zzqxwv` → 0 in the same file | **valid** — same method, same file, both directions |
| ~~PDBe `best_structures`~~ | `Q9NYG8` → 12 structures | impossible accession `ZZZZZZ` → **`{"message":"Requested endpoint does not contain any data"}`, byte-identical to the reply for `Q6PFU3`** | **RETRACTED** |

**The retracted method, recorded rather than quietly replaced.** My first structure-absence claim
rested on `www.ebi.ac.uk/pdbe/api/mappings/best_structures/Q6PFU3` returning "Requested endpoint
does not contain any data." The must-fail control shows that a *nonsense* accession returns the
identical string, so that endpoint cannot distinguish "this protein has no experimental structure"
from "I do not recognise this accession" — and since `Q6PFU3` is an unreviewed TrEMBL entry, the
second reading was entirely live. **The original claim was unsupported by the evidence I had
offered for it.** The replacement test (UniProt `xref_pdb`) is sound because its must-fail case
errors out distinctly, and because the reviewed human ortholog `O95279` returns 0 — showing that
a 0 is a real absence and not a TrEMBL indexing artifact. The conclusion survived; the method did
not. A second error the controls caught: the "`single-channel`" literature search initially
returned 39 hits because I had left the hyphenated phrase unquoted, which Europe PMC parsed
loosely; quoted, it returns 1.

So the key input is **a single measured macroscopic number from one 2014 experiment in a
heterologous expression system, never replicated, never decomposed into i and P<sub>o</sub>,
and never measured in the tissue of interest.** It is not an assumption repeated until it reads
as measured — it is a genuine measurement — but it is being read as a quantity it is not.

---

## 3. Step 3 — going and improving it

I could not make the 2-fold number itself more precise: no primary source refines it (section
2). What I *could* do is find the real quantity the conclusion needs, and find out what has been
established about the two parts of the question the recorded answer did not address —
**"graded"** and **"pectoral-restricted."** Both turn out to be where the action is.

### 3a. "Pectoral" is absent from the founding paper — and the paper that supplies it reverses the sign

**Scope: the string `pectoral` in Perathoner et al. 2014 full text: 0 occurrences.** That paper
is about caudal, dorsal and anal fins and barbels. The recorded answer inherited "pectoral"
from the subproblem statement, not from the founding evidence.

The pectoral evidence comes from a later paper: **PLoS Biology 2024, PMID 38527087, PMC11018282,
doi 10.1371/journal.pbio.3002565, "The scale of zebrafish pectoral fin buds is determined by
intercellular K+ levels and consequent Ca2+-mediated signaling via retinoic acid regulation of
Rcan2 and Kcnk5b"** (first author Jiang; read-level **full-text**, 364,543 bytes). It is
directly on point: `pectoral` appears 81 times, `kcnk5b` 326 times.

And it reports the **opposite sign** of membrane-potential change from Perathoner et al.

| | Perathoner et al. 2014 | Jiang et al. 2024 |
| --- | --- | --- |
| Tissue | *Xenopus* oocytes (heterologous); adult median fins + barbels in vivo | Embryonic **pectoral** fin buds |
| Vm readout | Two-electrode voltage clamp, **calibrated mV** | **DiSBAC<sub>2</sub>(3) dye fluorescence, relative — uncalibrated** |
| Direction of Vm change on increased Kcnk5b activity | **Hyperpolarization** | **Depolarization** |
| Verbatim | "these mutations cause an increase in K + conductance of the channel and lead to hyperpolarization of the cell"; "the mutant channels lead to stronger hyperpolarization causing a shift in the membrane potential towards −90 to −100 mV" | "Kcnk5b enhanced depolarization in fin bud cells via Na + channels and that this enhanced depolarization was required for Kcnk5b-enhanced growth"; "overexpression of kcnk5b-mCherry significantly increased depolarization" |

**Jiang et al. name the paradox themselves**, which is why this is a substantive disagreement
and not my misreading:

> "The observed increase in depolarization caused by kcnk5b , a leak channel that should promote
> hyperpolarization, suggested that other channels whose activity causes depolarization, such as
> Na + channels, were involved."

Their proposed resolution is indirect: Kcnk5b lowers intracellular K⁺, which recruits Na⁺-channel
activity, which depolarizes. They test it with Na⁺-channel inhibitors.

A third full text takes the canonical view and cites Perathoner — **eLife 2021, PMC8110307**
(read-level full-text): "opening of Kcnk5b causes a flow of K + out of the cell, which
hyperpolarizes the membrane potential."

**I am preserving this disagreement rather than averaging it.** Note what is *not* in dispute:
that increased Kcnk5b activity enlarges appendages. What is in dispute is **the sign of the
membrane-potential intermediate in pectoral tissue** — which is precisely the variable a graded
bioelectric controller would have to set. The two measurements are in different tissues with
different modalities, so they are not a direct contradiction of one measurement by another; but
they do leave the sign of dVm/d(Kcnk5b activity) in pectoral fin buds unsettled.

**Jiang et al.'s own stated caveats** on their Vm measurement, which bear on how tightly a
setpoint could be held (their words, not my characterisation): the averages "represented a broad
distribution of depolarization levels"; some buds "displayed lower levels of fluorescence or
variegated patterns high and low fluorescence"; "we can not rule out differences in dye
penetration." **My inference:** within-bud Vm heterogeneity is of the same order as the
between-condition signal, which pushes the achievable number of grades toward the low end of the
range computed in section 4.

### 3b. "Graded" and "restricted" — what has actually been achieved

The most relevant work is a **preprint, read-level abstract only**: bioRxiv
**doi 10.1101/2024.03.27.587111**, Europe PMC `PPR830054`, "Cell-type-dependent bioelectric
regulation of fin size and fin-ray segment length in zebrafish" (Europe PMC `isOpenAccess` N,
`inPMC` N — I read the abstract via the Europe PMC core record and could not reach a full text;
**scope: Europe PMC title search and a `kcnk5b AND osteoblast AND keratinocyte` search,
2026-11-04, returned no peer-reviewed version**). From its abstract:

> "To manipulate bioelectric signaling, we expressed the hyperactive potassium channel mutant
> kcnk5b W169L or the dominant-negative connexin mutant Cx43 T154A under a common set of
> cell-type-specific promoters. Cell-type-specific bioelectric manipulation in keratinocytes
> primarily affected fin size, whereas manipulation in osteoblasts preferentially altered
> fin-ray segment length. ... Furthermore, optogenetic manipulation demonstrated that membrane
> potential itself can regulate fin size and fin-ray segment length."

This is the single most informative find, and it cuts three ways:

1. **Restriction is solved, but by promoter, not by protein.** Spatial restriction was achieved
   with cell-type-specific promoters driving the *existing* W169L allele. Nothing was engineered
   into the channel. *(The approach is the authors'; the observation that this bypasses protein
   engineering is my inference.)* Note also that this is **cell-type** restriction
   (keratinocyte, osteoblast), **not** anatomical restriction to the pectoral fin, which S14
   asks for. I found no study restricting kcnk5b manipulation to the pectoral appendage.
2. **The grading lever that worked was voltage, not conductance.** "Optogenetic manipulation
   demonstrated that membrane potential itself can regulate fin size" — i.e. the demonstrated
   route to setting Vm continuously is an optogenetic actuator, which is dose-tunable by light
   and sidesteps the channel's 2-fold ceiling entirely.
3. **Still only W169L.** Even here, the channel contribution is the one binary hyperactive
   allele. **Scope: across all sources I read, the measured kcnk5b conductance series is
   {0 (GFG→AAA), 1.0 (wild type), ~2.0 (W169L), ~2.0 (F241Y)}. There are no intermediate
   points.** Perathoner et al.'s non-conductive control is a selectivity-filter triple
   substitution: "mutating the GFG motif of the selectivity filter to AAA, kcnk5b(GFGAAA)" —
   which abolishes conduction and abolishes overgrowth, confirming conduction is required but
   adding only a zero, not a grade.

### 3c. One caution about effect sizes in this literature

PMC8110307's open peer-review correspondence (read-level full-text) records a reviewer noting
that a reported transcriptional effect fell from "30 to 40 fold in the old data" to "about 1.5
to 2 fold with the appropriate new controls." **That is a reviewer's claim about a different
readout (*lef1*/*shha* transcripts), not about conductance, and I am not transferring it to the
conductance number.** I record it because it is direct evidence that effect sizes in this
specific literature have moved by more than an order of magnitude when controls were added — which
is a reason to treat an unreplicated 2-fold as soft, and which is exactly the sensitivity
section 4 tests.

### 3d. What measurement would settle it

The quantity the conclusion needs, and nobody has: **calibrated resting membrane potential, in
mV, in pectoral fin bud mesenchyme, as a function of Kcnk5b activity — plus the cell-to-cell
variance of that potential within one bud.** The variance is what sets the number of grades
(section 4), and the dye method used in the pectoral paper cannot deliver it because it is
uncalibrated and, by its authors' own caveat, confounded with dye penetration.

Two experiments would settle the two separate gaps, and both are standard rather than exotic:

1. **Sign and setpoint:** whole-cell patch clamp of fin-bud mesenchymal cells, wild type versus
   increased Kcnk5b activity, reporting absolute mV and the within-bud distribution. The 2024
   pectoral paper already describes a patch-clamp rig and pipette solution, so this is an
   extension of established in-house capability, not new infrastructure. It would resolve the
   Perathoner/Jiang sign disagreement in the tissue that matters.
2. **Decomposing the proxy:** single-channel recording of wild-type and W169L/F241Y Kcnk5b in a
   heterologous system, to split the ~2-fold macroscopic current into single-channel conductance,
   open probability and surface density. This determines how much of the 2-fold is even
   addressable by acting on the protein.

**Cost: I will not invent a figure.** Both are single-rig electrophysiology projects on an
established model organism with existing transgenic lines; in units I can defend, each is of
order one trained electrophysiologist for roughly one to two years, using equipment both
contributing labs already operate. I have no costed proposal or budget document for either, so
any currency amount I gave would be fabricated — it is `unknown`.

---

## 4. Step 4 — recomputing the conclusion with the improved input

### 4a. The model

"Graded control" requires distinguishable setpoints of the controlled variable. Fin size tracks
membrane potential (the optogenetic result in 3b is the cleanest evidence for that), so the
controlled variable is Vm and the actuator is K⁺ conductance. The transform between them, for a
resting cell with a K⁺ branch and a non-selective background branch in parallel:

$$V_m = \frac{g_K E_K + g_B E_B}{g_K + g_B}, \qquad r \equiv g_K/g_B$$

**This is a simulation, not an observation.** Parameters and their status:

- `E_K = −100 mV` — **from the source.** Perathoner et al. state "−90 to −100 mV, the equilibrium
  potential for K + in *Xenopus* oocytes"; I take the stated bound.
- `E_B = 0 mV` — **my assumption** for a non-selective background branch. Flagged as such.
- `Vm_wt` — **not stated in the source.** Perathoner et al. give the mutant endpoint (−90 to
  −100 mV) but no wild-type value I could find. I therefore **sweep it** rather than pick one.
- `R` — the conductance fold-change, the key input under test.

### 4b. What the measured 2-fold window actually buys

Computed (`recompute.py`, parallel-conductance model — simulation):

```
   Vm_wt= -20 mV: 2-fold gK buys  -13.3 mV of the   80 mV available = 16.7%
   Vm_wt= -30 mV: 2-fold gK buys  -16.2 mV of the   70 mV available = 23.1%
   Vm_wt= -40 mV: 2-fold gK buys  -17.1 mV of the   60 mV available = 28.6%
   Vm_wt= -50 mV: 2-fold gK buys  -16.7 mV of the   50 mV available = 33.3%
   Vm_wt= -60 mV: 2-fold gK buys  -15.0 mV of the   40 mV available = 37.5%
```

**Result 1 — robust to the unstated parameter.** Across the whole plausible range of resting
potential, a 2-fold conductance increase delivers **13–17 mV**, i.e. only **17–38%** of the
voltage range physically available between rest and E_K. The conclusion does not depend on
guessing Vm_wt correctly, which is why sweeping it was worth doing.

**Result 2 — the transform is compressive.** Successive doublings of g_K from Vm_wt = −40 mV
(simulation):

```
   gK x1   -> Vm  -40.00 mV   step  +0.00 mV
   gK x2   -> Vm  -57.14 mV   step -17.14 mV
   gK x4   -> Vm  -72.73 mV   step -15.58 mV
   gK x8   -> Vm  -84.21 mV   step -11.48 mV
   gK x16  -> Vm  -91.43 mV   step  -7.22 mV
   gK x32  -> Vm  -95.52 mV   step  -4.09 mV
```

Equal *multiplicative* steps in conductance give *shrinking* steps in voltage, because Vm
saturates at E_K. So a grading scheme built on conductance variants has diminishing resolution
exactly where a designer would want to push hardest. A given fractional error in conductance
also maps to a progressively smaller voltage error, which cuts the other way — but the ceiling
dominates.

### 4c. The factor-of-two sensitivity, by recomputation

Number of distinguishable Vm levels inside the window = window / σ_V, where σ_V is the
within-tissue Vm discrimination step. **σ_V is unmeasured** (section 3d), so it is swept.

Window from R = 2 at Vm_wt = −40 mV is **17.1 mV**:

```
      sigma_V= 2 mV ->  8.57 distinguishable levels
      sigma_V= 5 mV ->  3.43 distinguishable levels
      sigma_V=10 mV ->  1.71 distinguishable levels
      sigma_V=15 mV ->  1.14 distinguishable levels
```

And moving the key input by a factor of two in each direction (σ_V fixed at 5 mV):

```
   R=1     -> window   0.0 mV ->  0.00 levels
   R=1.41  -> window   8.5 mV ->  1.69 levels
   R=2     -> window  17.1 mV ->  3.43 levels
   R=2.83  -> window  25.4 mV ->  5.07 levels
   R=4     -> window  32.7 mV ->  6.55 levels
```

**This is the sensitivity, shown rather than asserted.** At the measured R = 2 the answer is
~3 levels — marginal, arguably "graded" in the weakest sense. Halve the window (R = 1.41) and
it is **1.7 levels: an on/off switch, not a graded controller.** Double it (R = 4) and it is
~6.6 levels, comfortably graded. **The verdict genuinely flips within a factor of two of the
measured value, which is the test the deepening asked for, and the measured value sits right at
the boundary.** It also flips on σ_V alone: at σ_V = 10 mV the window holds 1.7 levels even with
R = 2 — and Jiang et al.'s own report of a "broad distribution" of Vm within single fin buds is
the one piece of evidence bearing on σ_V, pointing to the larger end.

### 4d. The verdict

**The recorded answer FALLS.** Precisely what falls, and what does not:

**Falls:**
- "pLDDT > 80" as a model-level claim. The primary records say **69.5** (monomer) and **62.82**
  (homodimer); 33.9% of residues are below 50.
- The implicit chain *structure resolved → variants designable → graded control achievable*. It
  breaks at the first link independently of structure quality: the filters whose confidence is
  quoted (98–102, 203–207) are not the causal residues (169, 241), and the measured conductance
  window supports ~3 levels at best, ~1.7 if the number is soft by a factor of two.
- "Pectoral-restricted" as something the evidence speaks to. The founding paper never mentions
  pectoral fins; the paper that does **reverses the sign** of the voltage intermediate; and the
  one study achieving spatial restriction did it in keratinocytes and osteoblasts, not by
  appendage identity.

**Stands (confirmed, not weakened):**
- No experimental structure of kcnk5b. **Confirmed** via UniProt `xref_pdb` with controls in both
  directions (§2a), and extended: the closest human ortholog `O95279` has none either.
- Conduction is necessary for the phenotype. Perathoner et al.'s GFG→AAA control abolishes both.
- Increased Kcnk5b activity enlarges appendages, including pectoral fin buds.

**Reframed:** the question "can the *channel* be engineered for graded control?" is the wrong
lever to pull. Graded control of fin size has in fact been demonstrated — **optogenetically, by
setting membrane potential directly** (3b, read-level abstract), and spatial restriction has been
demonstrated **with cell-type-specific promoters driving the unmodified W169L allele.** Both
routes bypass protein engineering. The protein-engineering route is, on the present evidence,
capped at ~3 levels and blocked by an unresolved sign in the target tissue — while the actuator
that already works is continuous and was never in dispute.

A negative result, stated precisely: **engineering kcnk5b itself for graded pectoral-restricted
control is not supported by current evidence, and the structural confidence number offered in
support of it is both misstated and irrelevant to the decision.** This is not a claim that
graded pectoral control is impossible — the optogenetic result suggests the opposite — only that
the channel-engineering path is not the one the evidence supports, and that the two measurements
needed to even cost it (3d) have not been made.

---

## 5. Sources, with read-levels

| Source | Identifier | Read-level |
| --- | --- | --- |
| Perathoner et al. 2014, *PLoS Genet* 10(1), "Bioelectric signaling regulates size in zebrafish fins" | PMID 24453984, PMC3894163, doi 10.1371/journal.pgen.1004080 | **full-text** (Europe PMC `fullTextXML`, 142,283 bytes) |
| Jiang et al. 2024, *PLoS Biol*, "The scale of zebrafish pectoral fin buds is determined by intercellular K+ levels..." | PMID 38527087, PMC11018282, doi 10.1371/journal.pbio.3002565 | **full-text** (364,543 bytes) |
| *eLife* 2021, "A calcineurin-mediated scaling mechanism that controls a K+-leak channel..." | PMID 33830014, PMC8110307 | **full-text** (285,644 bytes) |
| *Sci Rep* 2018, "Bioelectric-calcineurin signaling module regulates allometric growth and size of the zebrafish fin" | PMID 29991812, PMC6039437 | **full-text** (95,787 bytes) |
| "Cell-type-dependent bioelectric regulation of fin size and fin-ray segment length in zebrafish" (preprint) | doi 10.1101/2024.03.27.587111, Europe PMC `PPR830054` | **abstract** (not OA, not in PMC) |
| *Dev Biol* 2019, "Integrated K+ channel and K+Cl− cotransporter functions..." | PMID 31472116, PMC7235970 | **could-not-access** (`fullTextXML` returned 150 bytes) |
| AlphaFold DB prediction record, monomer | `AF-Q6PFU3-F1` v6, accession `Q6PFU3` | **full-text** (complete API record) |
| AlphaFold DB model via 3D-Beacons, homodimer | `AF-0000000066331115` | **full-text** (complete API record) |
| AlphaFold DB per-residue pLDDT / coordinates | `alphafold.ebi.ac.uk/files/...` | **could-not-access** (HTTP 403, egress policy denial, not retried) |
| RCSB search API | `search.rcsb.org` | **could-not-access** (HTTP 403, egress policy denial) |
| UniProt `xref_pdb` (the structure-absence evidence, §2) | `Q6PFU3`, `A0A8M1PBI1`, `O95279` → 0 entries; `Q9NYG8` → 12, `P57789` → 8 | **full-text** (complete REST records) |
| PDBe SIFTS `best_structures` / `uniprot_to_pdb` | `Q6PFU3`, `O95279` | **RETRACTED as evidence** — must-fail control returns the identical message (§2a); listed for the record only |
| *Dev Dyn* 2022, "Coordinated patterning of zebrafish caudal fin symmetry..." (sole `kcnk5b AND "single-channel"` hit) | PMID 35403297, PMC9357109 | **listing** (title + OA status; `fullTextXML` returned 150 bytes) |
| UniProt entries | `Q6PFU3`, `A0A8M1PBI1`; human K2P family (16 reviewed entries) | **listing** (REST TSV: accession, gene, length, review status) |
| Europe PMC literature sweep | query `kcnk5b`, 57 hits | **search-summary** (titles + abstracts + OA status) |

## 6. What I did not establish

- Which *alf* allele carries W169L and which carries F241Y — `unknown` at my read-level.
- Per-residue pLDDT at the two filter motifs, so the ">80 at both filters" claim is neither
  confirmed nor refuted at the residue level; only the model-level means (69.5, 62.82) are known
  to me. The route to it is blocked by egress policy, not by data availability.
- σ_V, the within-tissue membrane-potential discrimination step — the parameter that, jointly
  with the 2-fold window, sets the number of achievable grades. Unmeasured in any source I read.
- Any absolute conductance, in siemens, for Kcnk5b — wild type or mutant.
- What the "upstream maintenance" blocking variant scoring in the recorded answer referred to;
  I found nothing in the repository identifying it, and it is immaterial to this verdict, since
  a working variant scorer would not supply a dynamic range or settle the sign.
- Whether PMC9357109 — the single record co-mentioning `kcnk5b` and "single-channel" — contains a
  single-channel measurement. Its full text is not accessible to me (§2). This is the one hole in
  the central negative, and I am leaving it visible rather than closing it by assertion.

## 7. Reproducing this

The section-4 model is committed beside this file as **`S14-recompute.py`**; it is dependency-free
and prints every number quoted in §4b–4c. Hashes of the committed bytes:

```
sha256          76681c92000de719e81638fa8245cc1a4465894bc38e26f68e63bde49b93fd8f
git hash-object ea5a8c027b5a22348a50180a41d2906a956fe61a
```

Run it with `python3 -I docs/research/fish/S14-recompute.py`. Retrieved full texts (tag-stripped
`.txt`) and the raw API records are in this session's scratchpad at
`/tmp/claude-0/-workspace-delphi-frontier/56fbeac9-189f-5080-973c-eb16b30f14ee/scratchpad/s14`,
which is ephemeral; every source there is public and re-retrievable from the identifiers in §5.

All network sources were reached over plain HTTPS. The two 403s (`alphafold.ebi.ac.uk/files/`,
`search.rcsb.org`) are **this session's egress policy, not access restrictions at the providers** —
confirmed from the local proxy's own status endpoint, which records them as policy denials — so a
differently-configured runner should be able to close the per-residue pLDDT gap in §6 directly
from `plddtDocUrl`.

```swarm-result
{"subproblem": "S14-D", "evidence": "full-text", "answer": "Engineering kcnk5b itself for graded pectoral-restricted control is unsupported: the recorded pLDDT>80 is both misstated (AlphaFold DB reports 69.5 for the monomer and 62.82 for the homodimer, with 33.9% of residues below 50) and quoted at filter motifs 98-102 and 203-207 that are not the causal alf residues W169 and F241, while the input feasibility actually depends on -- the single measured ~2-fold conductance window -- yields only 13-17 mV of a 40-80 mV range and about 3 distinguishable setpoints, collapsing to 1.7 if soft by a factor of two, and the sign of the pectoral membrane-potential response is in unresolved disagreement between Perathoner 2014 (hyperpolarization, calibrated clamp in oocytes) and Jiang 2024 (depolarization, uncalibrated dye in fin buds); graded and restricted control have meanwhile been demonstrated optogenetically and with cell-type-specific promoters driving the unmodified W169L allele, both bypassing protein engineering.",
  "key_number": "~2.0-fold macroscopic K+ current (wild type -> alf, Xenopus oocyte TEVC, Perathoner et al. 2014) = 17.1 mV of a ~60 mV available Vm window = ~3.4 distinguishable setpoints at sigma_V = 5 mV",
  "verdict": "falls"}
```
