# Challenge 82 — adversarial review

**Claim under review (claim 82, evidence level recorded as `derived`, value `n/a`, source: "inference
from the two claims above"):**

> CONSEQUENCE FOR BUILD: a construct ordered against the symbol `lat4a` would not resolve. The
> buildable target is slc43a2a (GeneID 393221), and the T200K substitution must be numbered against
> that sequence, not against a gene record that does not exist.

**Verdict: REFUTED** — specifically, the *prescriptive* half is refuted. The claim's diagnostic half
(`lat4a` is not a zebrafish gene symbol; the official symbol is `slc43a2a`, GeneID 393221) is
correct and I confirmed it independently. But the remedy the claim prescribes cannot be carried out:
the only annotated protein for GeneID 393221 is **153 aa long**, so **position 200 does not exist in
it**, and a T200K substitution cannot be numbered against that sequence at all. A build pipeline
that obeyed this claim verbatim would order an unbuildable construct — the same class of failure the
claim was written to prevent.

All sequence facts below are **retrieved database records** (NCBI/UniProt, accessed 2026-11-04), not
observations I made at a bench, and the two length/position computations are **my own calculations**
over the retrieved sequences. Both are labelled as such in the sentence.

---

## 1. Arithmetic redone independently from the stated inputs

The claim states no arithmetic of its own, so what I re-derived is the only quantity its prescription
depends on: **does residue 200 exist in the sequence it tells you to number against, and is it a
threonine?**

I did not take any length from the author or from a database summary field. I downloaded the
sequences and counted the characters myself.

| Record | What it is | Length (**counted by me**, `len(seq)` over the FASTA) | Residue 200 (**read by me**, `seq[199]`) |
|---|---|---|---|
| `NP_956545.1` (from `NM_200251.2`) | the **only** RefSeq protein of GeneID 393221, *slc43a2a* | **153 aa** | **does not exist** |
| `NP_001008585.1` | *slc43a2b*, GeneID 494042 (the other zebrafish paralog) | 592 aa | **M** (Met), not Thr |
| `XP_087125491.1`, `XP_087125490.1`, `XP_087077278.1`, `XP_009303545.2` | *slc43a2b* isoform X1 predictions | 598 aa each | **M** each |

So against the sequence the claim names, `T200K` is not a wrong substitution — it is an **unassignable**
one.

I then checked, in case `T200` was anchored to an ortholog, every RefSeq protein of the two mammalian
reference genes (**my own position read** on each downloaded sequence):

- **Human `SLC43A2`** (GeneID 124935), all 11 RefSeq proteins (`NP_689559.1`, `NP_001271427.1`,
  `NP_001271428.1`, `NP_001308293.1`, `NP_001308294.1`, `XP_016879668.1`, `XP_047291287.1`,
  `XP_047291288.1`, `XP_054171013.1`, `XP_054171014.1`, `XP_054171015.1`): lengths 569, 573, 573,
  573, 536, 536, 432, 411, 411, 393, 393; residue 200 is `I` (the 569/573/393 aa forms), `P` (536 aa
  forms), `R` (432 aa form), `K` (411 aa forms). **No isoform has Thr at 200.**
- **Mouse `Slc43a2`** (GeneID 215113), all 15 RefSeq proteins: residue 200 is `I` in 14 of them and
  `L` in the 398-aa prediction `XP_036012405.1`. **None is Thr.**

**Negative result, with its scope:** across every RefSeq protein of *slc43a2a* (Danio rerio, 1 record),
*slc43a2b* (Danio rerio, 5 records), human `SLC43A2` (11 records) and mouse `Slc43a2` (15 records) —
32 protein records retrieved 2026-11-04 — **no record carries threonine at position 200**. I did not
search Ensembl (host blocked for this session, see §6) or non-RefSeq GenBank translations. So I cannot
say where `T200K` came from; I can say it is not anchored to position 200 of any of these. That is a
question for the upstream claims, not for this one, and my verdict is flagged against them in
`depends_on`.

### Why the 153 aa is not a database glitch I should have looked past

I checked this specifically, because "the annotation is just truncated, use the real ORF" would have
rescued the claim. It does not.

`NM_200251.2` is 3,230 bp (**my count**). Its annotated CDS is `175..636` with `/codon_start=1` and a
`/note="upstream in-frame stop codon"`. I ran **my own six-frame ORF scan** over the transcript
(standard genetic code, longest `M…*` run per frame). Longest ORF: **153 aa at nt 175**, i.e. exactly
the annotated CDS. Next longest: 122 aa, 76 aa, 52 aa, 48 aa, 48 aa. **There is no full-length ~590-aa
ORF hidden in this transcript** — the 2.6 kb downstream of the stop is 3'UTR inside exon 5
(`584..3214`). The record is flagged `PROVISIONAL REFSEQ`, derived from a single cDNA clone
(`BC047854.1`, MGC:56271), with `RNAseq introns :: partial sample support`.

Structural corroboration that the *slc43a2a* annotation is a fragment, not a short gene (retrieved
gene summaries, **listing** read-level): *slc43a2a* has **5** annotated exons over ~39.9 kb;
*slc43a2b* has **15**; human `SLC43A2` has **18**. A 153-aa product would cover roughly 3–4 of the
~12 transmembrane helices expected of an L-type transporter.

**My inference, separated from the record:** the most likely state of the world is that GeneID 393221
is genuinely the *slc43a2a* locus but its *reference CDS is incomplete*. That does not rescue the
claim — it makes it worse. The claim says to number against "that sequence". There is currently no
public reference sequence for that gene in which position 200 exists, so the instruction has no
executable referent.

## 2. The proxy

**Yes, and it is the load-bearing word.** The claim substitutes a **GeneID** for the quantity that
actually determines a numbering: a **versioned protein accession** (or a specific CDS). "Numbered
against that sequence" names a gene record, and a gene record is not a sequence.

This is not pedantry; I can quantify the failure from my own reads above. For human `SLC43A2`, one
GeneID, the residue *at the same number 200* is `I`, `P`, `R` or `K` depending on which isoform you
picked. One gene, four different residues at position 200. Had *slc43a2a* been annotated with
multiple isoforms, "numbered against GeneID 393221" would have been ambiguous even if position 200
existed.

**The right quantity:** the substitution must be stated as `accession.version:p.Thr200Lys` — e.g.
`NP_956545.1:p.…` — and for GeneID 393221 that statement is presently **impossible to form**, because
`NP_956545.1` is the only protein accession and it is 153 residues long. The honest corrected
instruction is: *establish a full-length slc43a2a CDS first (it does not exist in RefSeq), then
re-map the position by alignment; do not renumber by assertion.*

## 3. The hidden assumption, tested relaxed

**Assumption:** that `lat4a`, had it been intended, means the **`a` paralog** — and therefore that
resolving the symbol error and choosing the build target are the *same* step.

**Relaxed:** zebrafish has two SLC43A2 paralogs (`slc43a2a`/393221/chr15 and `slc43a2b`/494042/chr10,
both retrieved). Human `SLC43A2`'s only NCBI alias is **`LAT4`** — no suffix (retrieved, **listing**).
So `lat4a` reads equally well as (i) "the `a` paralog of lat4" or (ii) someone appending the teleost
paralog suffix to the human alias while meaning *the zebrafish LAT4 ortholog* generically. Under
reading (ii), the full-length ortholog — the one you can actually build a 200-residue-deep construct
against — is **`slc43a2b`**, not `slc43a2a`.

Relaxing the assumption therefore **flips the build target**, and it flips it toward the only paralog
where position 200 exists. The claim's identification step and its build step are not the same step,
and the claim collapses them. My verdict does not depend on reading (ii) being correct — the 153-aa
finding refutes the prescription under *either* reading — but it shows the claim's confidence
("the buildable target is") is not earned by the evidence it cites.

## 4. Is the evidence level honest?

**Partly, and the honest part is the label, not the hedge.** `derived` is the right label for an
inference drawn from two upstream claims, and `value: n/a` is appropriate.

Two defects in presentation, though:

1. **"would not resolve" and "a gene record that does not exist" are presented as flat fact with no
   search scope.** A negative lookup needs its database, field and date beside it. Mine are in §5.
2. **The sentence mixes evidence levels without marking the seam.** "The buildable target is slc43a2a
   (GeneID 393221)" is *lookup-grade* and checkable — and it checks out. "the T200K substitution must
   be numbered against that sequence" is *prescriptive*, and it is the part that fails. Labelling the
   whole sentence `derived` lets a correct lookup carry an unexecutable instruction across the same
   confidence boundary. Under this repo's rule 6 (separate columns), these belong in different cells.

**What the claim does not do:** it does not invent a gene, an accession or a number. GeneID 393221 →
`slc43a2a` → *Danio rerio* is exactly right, official nomenclature status, chromosome 15 (retrieved,
**listing**). Credit where it is due; the claim is wrong in its remedy, not fabricated.

## 5. Counter-example the author missed

**`LAT4A` does exist as a gene name — in the wrong organism.** UniProtKB query `gene:lat4a` (all
organisms) returns exactly one entry: **`A0A9P6H1T5`** / `A0A9P6H1T5_9MICR`, gene names `LAT4A
NGRA_1094`, organism *Nosema granulosis* (a microsporidian), length 171 aa (read-level:
**search-summary**, UniProt REST TSV, 2026-11-04).

This does not rescue the claim's target assignment — the *Nosema* protein is not an SLC43A2 ortholog,
is not a zebrafish gene, and at 171 aa has no residue 200 either. But it does refute the claim's
wording "**a gene record that does not exist**" as stated without qualification, and it matters
operationally in a direction the claim did not consider: a naive symbol lookup against a
pan-organism database **resolves `lat4a` to a microsporidian parasite protein** rather than failing
loudly. "Would not resolve" is the benign failure mode; silent cross-taxon resolution is the
dangerous one, and the claim's framing would not catch it.

**Scopes of my negative searches, stated beside the findings:**

- NCBI Gene, `lat4a[gene]` AND `"Danio rerio"[orgn]`: **0** hits; NCBI reported the phrase itself not
  found.
- NCBI Gene, `lat4a[gene]`, **all organisms**: **0** hits.
- NCBI Gene, `lat4a[All Fields]`, **all organisms, all fields**: **0** hits, phrase not found. (So
  `lat4a` is not even a listed synonym anywhere in NCBI Gene — the strongest form of the claim's
  diagnostic half survives, for that database, on that date.)
- NCBI Gene, `LAT4[gene]` AND `human[orgn]`: **1** hit, GeneID **124935** = `SLC43A2`. So the
  unsuffixed alias *does* resolve; only the suffixed form does not.
- UniProtKB, `gene:slc43a2a AND organism_id:7955`: 2 entries, `Q7ZUS0` and `A0A8N7V006`, **both 153
  aa** — independent second-database corroboration of the length that breaks the claim.
- **Not searched (tool access, not choice):** Ensembl (`rest.ensembl.org` refused by this session's
  egress proxy — `connect_rejected`) and ZFIN (`zfin.org` likewise unreachable, HTTP 000). Either
  could hold a longer *slc43a2a* model than RefSeq does. **If one does, my §1 length finding is
  scoped to RefSeq+UniProt and the claim's prescription could become executable against that other
  model — but not against the accession the claim's own GeneID resolves to.** Read-level for both:
  **could-not-access**.

**Disagreement between sources, preserved:** none to preserve on the length — NCBI RefSeq
(`NP_956545.1`), the source cDNA (`BC047854.1`, 3,231 bp, "complete cds") and UniProt (`Q7ZUS0`,
`A0A8N7V006`) all give **153 aa**, and my own ORF scan of the transcript agrees. The disagreement
that does exist is *structural, between paralogs*: 5 exons/153 aa (*slc43a2a*) against 15 exons/592 aa
(*slc43a2b*) and 18 exons/569 aa (human). I am not averaging that away — I read it as the annotation
of 393221 being incomplete, and I have marked that reading as my inference, not as a record.

## 6. Method and provenance

- NCBI E-utilities (`esummary`, `esearch`, `elink`, `efetch`) over HTTPS; UniProt REST. Read-level
  **full-text** for the GenPept record `NP_956545.1` and the GenBank record `NM_200251.2`;
  **listing** for gene summaries; **search-summary** for the UniProt TSV queries.
- Lengths, residue reads and the six-frame ORF scan: **my own computation** in Python over the
  downloaded FASTA, not copied from any summary field and not copied from the author.
- The paralog correspondence in §1 ("the 153-aa fragment aligns to roughly *slc43a2b* positions
  23–175") is from **my own crude ungapped offset scan** — best offset 22, 62/153 identities (40.5%)
  — **not** a published or gap-aware alignment. It is indicative only, and I do not rest the verdict
  on it. Treat it as calculated, low-confidence.
- I did not perform any experiment, order any construct, or observe any sequence at a bench.

## 7. What a corrected claim would say

> `lat4a` is not a *Danio rerio* gene symbol (NCBI Gene, all fields, 0 hits, 2026-11-04), and a
> pan-organism symbol lookup will mis-resolve it to *Nosema granulosis* `LAT4A` rather than fail.
> The intended locus is almost certainly `slc43a2a`, GeneID 393221. **However, that gene is not
> buildable as a T200K-bearing construct:** its only reference protein, `NP_956545.1` (from
> `NM_200251.2`), is 153 aa and has no position 200, and no RefSeq protein of *slc43a2a*,
> *slc43a2b*, human `SLC43A2` or mouse `Slc43a2` carries Thr at 200. Before any construct is
> ordered, two things must be resolved upstream: (i) which paralog is intended — `slc43a2b`
> (GeneID 494042, `NP_001008585.1`, 592 aa) is the full-length zebrafish SLC43A2, and its residue
> 200 is **Met**, not Thr; and (ii) what sequence `T200K` was originally numbered against, since
> it matches none of the 32 records checked. The substitution must then be restated as
> `accession.version:p.Thr200Lys` against a specific protein accession, never against a GeneID.

---

```swarm-challenge
{"claim_id": 82, "outcome": "refuted", "reason": "GeneID 393221's only reference protein (NP_956545.1, from NM_200251.2) is 153 aa and has no position 200 — independently counted and corroborated by UniProt and by my own six-frame ORF scan of the transcript — so the claim's prescription to number T200K against that sequence is unexecutable, and no RefSeq protein of slc43a2a, slc43a2b, human SLC43A2 or mouse Slc43a2 carries Thr at 200.",
  "corrected_value": "GeneID 393221 reference protein NP_956545.1 = 153 aa (position 200 absent; T200K unassignable). Full-length zebrafish SLC43A2 paralog is slc43a2b, GeneID 494042, NP_001008585.1 = 592 aa, residue 200 = Met. Thr200 found in 0 of 32 SLC43A2-family RefSeq proteins checked (Danio rerio, human, mouse).",
  "depends_on": ["upstream-claim: the symbol `lat4a` is unresolvable (claim 80 or 81 — the two claims named as this claim's source; their ids are not recorded in this repo and I did not confirm them)", "upstream-claim: the intended locus is slc43a2a, GeneID 393221", "upstream-claim: the substitution of interest is T200K (its source numbering is unknown and matches none of the 32 records I checked; if T200K is itself misattributed upstream, this verdict must be re-examined)", "NCBI Gene/RefSeq records for GeneID 393221, 494042, 124935, 215113 and protein NP_956545.1, NM_200251.2, NP_001008585.1, NP_689559.1, retrieved 2026-11-04", "UniProtKB entries Q7ZUS0, A0A8N7V006 (slc43a2a, both 153 aa) and A0A9P6H1T5 (Nosema granulosis LAT4A), retrieved 2026-11-04", "scope caveat: Ensembl and ZFIN were unreachable from this session, so the 153-aa finding is scoped to RefSeq + UniProt"]
}
```
