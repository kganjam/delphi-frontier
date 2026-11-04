# Replicate claim 186 — ABORTED ON CONTAMINATION

**Verdict: I cannot deliver an independent value for claim 186. I read the prior
derivation's conclusion before I knew what it was. Everything below separates what I
established from primary sources (usable) from what I must not now claim (the
compounding question itself).**

## 0. What claim 186 asks

The question as handed to me, with its answer removed:

> The two reference failures COMPOUND ___
> Context for where the inputs live: inference from the two verified findings

So the task was to re-derive, from primary sources, the consequence of two
previously-verified reference-database failures acting together on a downstream
implementer.

## 1. The contamination, stated precisely

The question gave me no file paths — only "inference from the two verified findings" —
so locating the inputs required searching the repository. `docs/research/fish/` does not
exist on the default branch; the fish research corpus lives on 599 remote branches. I
ran `git log --all --oneline` filtered for the claim number to find which branch carries
the relevant work.

That listing returned, as a **commit subject line**:

> `42a68da4 Challenge 186: REFUTED — the truncation does not block guide RNA design`

and `git show --stat 42a68da4`, run to identify which files the branch touched, printed
the commit **body**, which states the guide-RNA codon range, that all five published
guides fall inside the truncated reference model, and the conclusion that the two
reference failures do **not** compound before guide design — naming where each failure
bites instead.

That is the prior working for this claim, including its answer and its reasoning. I read
it before I could tell it apart from branch-location metadata. I stopped there: I did
**not** open `docs/research/fish/challenge-186-*` or `replicate-186*` on any branch, and
I left unread the output of a cross-branch grep I had launched for the same
locating purpose (`/tmp/.../tasks/bc9hpxvro.output`), whose only function was to surface
prior work on this claim.

**Why I will not now "just do the arithmetic anyway."** My next planned step was to map
the five published gRNA protospacers onto NM_200251.2 to obtain their codon
coordinates — which is precisely the arithmetic the compounding question turns on, and
precisely the result I had already seen asserted. An agent that re-derives a number it
has already been told is not producing independent evidence; it is producing a
confirmation it cannot distinguish from reasoning. Two independent derivations agreeing
is evidence. One agent agreeing with material it has already read is not. So the
compounding inference is recorded here as `unknown`.

## 2. What I did establish from primary sources, before and independent of that

These were retrieved from NCBI and UniProt directly, not from the repository, and they
stand on their own. They are the two reference failures as *inputs*; I draw no
compounding conclusion from them.

### Finding A — the symbol `lat4a` does not resolve in the public reference record

**Source:** NM_200251.2 GenBank flatfile, NCBI E-utilities `efetch`
(`db=nuccore&id=NM_200251.2&rettype=gb`), retrieved 2026-11-04.
**Read-level: full-text** (complete flatfile, 3,230 bp record).

Verbatim from that record:

```
     gene            1..3230
                     /gene="slc43a2a"
                     /gene_synonym="si:dkey-118k5.2; slc43a2; zgc:56271"
                     /note="solute carrier family 43 member 2a"
                     /db_xref="GeneID:393221"
                     /db_xref="ZFIN:ZDB-GENE-040426-964"
```

The approved symbol is `slc43a2a`. The synonym list is
`si:dkey-118k5.2; slc43a2; zgc:56271`. **`lat4a` appears nowhere in it.**

Corroborating, same read-level: UniProt REST
(`query=slc43a2+AND+organism_id:7955`, `fields=accession,length,gene_names`) returns one
zebrafish entry, A0A8N7V006, gene names `slc43a2a si:dkey-118k5.2 slc43a2 zgc:56271` —
again no `lat4a`.

The paper's own usage, for contrast — **author's claim, not my inference** — Daane et
al. 2021 use `lat4a` throughout as the gene's name, e.g. "the L-type amino acid
transporter, lat4a", and their Key Resources table names the alleles "lat4 nr21
(dmh26)" and "lat4a del (mh152)". So an implementer who takes the symbol from the paper
and queries the public databases with it gets no hit on the gene the paper means.

**Scope of this negative:** searched NCBI Gene/Nucleotide via the NM_200251.2 record's
own gene feature, and UniProtKB restricted to taxon 7955. I did not search ZFIN
directly, and I could not reach Ensembl at all (see §4), so I do not state that `lat4a`
is absent as an alias everywhere — only that it is absent from the RefSeq gene feature
and from the UniProt zebrafish entry for this gene.

### Finding B — that reference protein model is 153 aa, truncating the paper's numbering

**Source:** same NM_200251.2 flatfile. **Read-level: full-text.**

Verbatim:

```
     CDS             175..636
                     /protein_id="NP_956545.1"
```

My arithmetic on the author-independent record:

```
CDS span        = 636 - 175 + 1 = 462 nt
codons          = 462 / 3       = 154   (including the terminator)
coding residues = 154 - 1       = 153 aa
```

This is a **calculated** value from the stated CDS coordinates. It is confirmed as an
**observation** by two independent records: NCBI `esummary` for NP_956545 reports
`Length = 153`, and UniProt reports length 153 for both A0A8N7V006 and Q7ZUS0
(**read-level: full record** for each).

The paper's residue coordinates against that 153-aa model — the subtraction is mine, the
positions are the authors':

| Paper's residue (Daane et al. 2021) | Position | Inside a 153-aa model? | Overshoot |
|---|---|---|---|
| `L106Rfs39` revertant frameshift | 106 | yes | — |
| `T200K` (the `nr21` lesion) | 200 | **no** | 47 residues past the end |
| `F326L` (the convergent flying-fish substitution) | 326 | **no** | 173 residues past the end |

For scale, and as a separate primary-source input: the reviewed human ortholog
SLC43A2 (UniProt Q8N370) is **569 aa** (**read-level: full record**, UniProt REST TSV).
A full-length LAT4 is therefore ~569 aa, and 153 / 569 = **0.269** — the zebrafish
reference model carries about 27% of the expected length. That ratio is my calculation
from the two reported lengths, not anything either database asserts.

### Finding C — the paper's guide-RNA inputs exist and are quotable

**Source:** Daane et al. 2021, *Curr Biol* 31(22):5052–5061, PMID 34534441,
PMC9172250, retrieved 2026-11-04 from PMC (325,748 bytes of HTML).
**Read-level: full-text.** Note: Europe PMC reports `isOpenAccess = N` for this record
and its `fullTextXML` endpoint returned HTTP 500; the full text came from PMC directly.

Verbatim from METHOD DETAILS:

> "CRISPR guide RNAs (gRNAs) were designed against the third coding exon of lat4a using
> the online ChopChop tool to limit predicted off-target gRNA cutting. [...] a 'blanket'
> of 5 gRNAs targeting the same exon were synthesized and injected as a pool."

The five protospacers, verbatim from the Oligonucleotides table (the invariant
`ATTTAGGTGACACTATA` SP6 leader and `GTTTTAGAGCTAGAAATAGCAAG` tracrRNA scaffold stripped,
leaving the targets the paper itself underlines):

| Guide | Target sequence (5'→3') |
|---|---|
| Lat4a gRNA #1 | `GGCCCTGTACCGTTACCTGG` |
| Lat4a gRNA #2 | `GGTGAATGCCACAAGACTTG` |
| Lat4a gRNA #3 | `GGATGCCACAAGACTTGAGG` |
| Lat4a gRNA #4 | `GGCCACAAGACTTGAGGAGG` |
| Lat4a gRNA #5 | `GGAGTGTGATGGCGCTCAGG` |

A caveat the paper states itself, which any downstream mapping must carry: "For
transcription efficiency, the first two bases of each gRNA were changed to 'GG'", so the
leading `GG` of each sequence above is **not necessarily genomic** and an exact-match
search on the full 20-mer may fail for that reason alone.

**I deliberately did not align these to NM_200251.2.** That alignment is the contaminated
step (§1).

## 3. The value

**`unknown`.**

I have both reference failures verified from primary sources with full-text read-level
(§2 A, B) and the downstream inputs in hand (§2 C). I do not have, and will not
manufacture, an independent inference about whether they compound, because I read the
recorded conclusion to that question before deriving my own.

Uncertainty on the inputs, for whoever derives this properly:
- 153 aa is exact and triply sourced; no uncertainty.
- 200 and 326 are exact as printed by the authors; the overshoots 47 and 173 are exact
  subtractions.
- The `lat4a` symbol negative is scoped as stated in §2 A, not global.
- The five guide 20-mers carry the authors' own `GG` substitution caveat.

## 4. What I tried and could not get

- **Ensembl REST** (`rest.ensembl.org/lookup/symbol/danio_rerio/slc43a2a`) — the session's
  egress proxy refused the connection (`connect_rejected`). **Read-level:
  could-not-access.** This matters: Ensembl's gene model for this locus may well be
  full-length where RefSeq's is 153 aa, and I could not check. A proper derivation should
  resolve that, since it determines whether Finding B is a RefSeq-specific defect or a
  genome-annotation-wide one.
- **Europe PMC `fullTextXML` for PMC9172250** — HTTP 500, twice. Worked around via PMC
  HTML, which is why Finding C's read-level is full-text rather than could-not-access.
- **Protas et al. 2006 and ZFIN** — not attempted; not needed for the inputs above.

## 5. Comparison with the recorded value

**CANNOT TELL** — and here the honest answer is not symmetric with the usual one. I know
what the recorded conclusion says, because reading it is what aborted this work. I
therefore have no independent value of my own to set beside it. Recording agreement on
the strength of having read the answer would be the exact failure this protocol exists
to prevent, so I record no comparison.

**Recommended remedy:** hand claim 186 to a fresh agent with only the primary-source
pointers in §2 (NM_200251.2; PMC9172250 Key Resources and METHOD DETAILS) and an explicit
instruction not to run `git log`, `git show`, or any cross-branch grep. The inputs are all
public; a blind re-derivation is cheap. It is the reading of this repository that is
hazardous, and the question as posed does not require it.

## 6. Disagreement I am preserving, not averaging

Finding A and Daane et al.'s own text are in flat conflict about what this gene is
called, and Finding B and Daane et al. are in flat conflict about how long its protein
is. I am not reconciling either. The paper is internally consistent and the databases are
internally consistent; they describe the same locus with incompatible names and
incompatible coordinates. That conflict *is* the pair of reference failures, and
flattening it would destroy the input.

```swarm-replication
{"claim_id": 186, "my_value": "unknown", "agrees": null,
  "note": "Aborted: I read commit 42a68da4's subject and body — the prior derivation's conclusion and reasoning — while locating the claim's inputs, before I could identify it as prior working; both reference failures are independently verified from primary sources (slc43a2a has no lat4a alias in RefSeq/UniProt; NP_956545.1 is 153 aa from CDS 175..636, so T200K and F326L overshoot by 47 and 173 residues), but the compounding inference itself cannot now be derived independently by me."}
```
