# Adversarial review — claim 185 (slc43a2a 153-aa build blocker)

## Claim under review

> BUILD BLOCKER: every UniProt slc43a2a entry (Q7ZUS0, A0A8N7V006) and RefSeq
> NP_956545.1 are 153 aa — a truncated gene model that CANNOT carry a residue
> 200, so the T200K substitution is unrepresentable in the databases anyone
> would reach for first. Only Ensembl GRCz11 has the full-length product.

- recorded evidence level: `measured`, value `153 aa`
- source: verified against UniProt REST; agent finding from fish-alleles/README.md

## What I did

All lookups below were run live during this review (read-level: **full-text**,
i.e. direct API/JSON records, except where marked). Ensembl's own REST endpoint
(`rest.ensembl.org`) was blocked by the environment proxy (`could-not-access`,
403 CONNECT), so I reached the Ensembl-derived product through UniProt's UniParc
mirror instead — see the regime note.

### 1. The three "first-reach" accessions — independent re-check

Queried UniProt REST and NCBI eutils directly:

| Accession | Source | Length | Status |
|---|---|---|---|
| Q7ZUS0 | UniProtKB/TrEMBL | **153 aa** | unreviewed; seq version 1; protein existence: transcript level; xrefs EMBL BC047854, RefSeq NP_956545.1, ZFIN ZDB-GENE-040426-964 |
| A0A8N7V006 | UniProtKB/TrEMBL | **153 aa** | unreviewed; predicted; derived from RefSeq NP_956545.1 |
| NP_956545.1 | NCBI RefSeq | **153 aa** | "solute carrier family 43 member 2a [Danio rerio]" |
| AAH47854.1 | GenBank (BC047854, the mRNA behind Q7ZUS0/NP_956545) | **153 aa** | "Si:dkey-118k5.2" |

A UniProt gene-name search (`gene:slc43a2a AND organism_id:7955`) returns **only**
these two entries, both 153 aa. A broader `txid7955 AND slc43a2a` protein search
on NCBI returns exactly one RefSeq (NP_956545.1). So the claim's enumeration of
the live, first-reach entries is complete, not cherry-picked.

### 2. Arithmetic (redone independently)

A protein of length 153 is indexed 1…153. Residue 200 > 153, so position 200
does not exist in that chain. No substitution *at* position 200 (whatever the
identities) can be written against a 153-residue coordinate system. This is not
a computed biological result — it is the trivial fact that 200 > 153. **Confirmed.**

### 3. Does the full-length product exist, and does it actually carry a residue 200?

Yes to both. The Ensembl translation ENSDARP00000120945 is mirrored in UniParc as
**UPI000188A62B, length 571 aa**, organism *Danio rerio*, gene slc43a2a, active
Ensembl cross-reference (read-level: full-text, UniParc JSON + FASTA). I
retrieved its sequence and confirmed it is 571 residues and that **position 200
is occupied (residue = Thr)**.

I then independently anchored this to genomic DNA rather than trusting the stored
length. Using NCBI's current *Danio rerio* assembly (gene 393221, locus on
NC_133190.1), I fetched the locus, translated all three forward frames, and tiled
the 571-aa sequence back onto the genome in 8-mer windows: **569 / 571 residues
map to in-frame exonic codons** (the 2 gaps are exon-junction windows, expected).
Residue 200 maps to codon **ACA → Thr** at NC_133190.1:30,897,361. So the
full-length model is real genomic coding sequence, and residue 200 is a genuine
Thr. This independently corroborates the *wild-type* identity "T" in the "T200K"
nomenclature — the mutation label is self-consistent with the full-length model.

### 4. Is the 153-aa model truncated, or just a different real isoform?

I aligned the 153-aa chain (Q7ZUS0) against the 571-aa chain. They are **identical
for the first ~139 residues**, then the 153-aa chain diverges into a frameshifted
tail and hits a premature stop: its C-terminus translates in a different genomic
frame (`…SVQLYYQ*`). So the 153-aa entry is not an alternative full transporter —
it is a short/mis-extended gene model (frameshift → early stop) sharing the
N-terminus. This supports the claim's word "truncated gene model." (The full-length
tail at the same position instead reads `…ISYGASDPQNLSIL…`, i.e. a different,
longer ORF.) A 12-transmembrane SLC transporter is ~550–600 aa; 153 aa is far too
short to be the functional protein, consistent with the paralogs slc43a2b (592–598
aa) and slc43a1a (536 aa) returned by the same search.

## Where the claim is slightly loose (weakening, not refuting)

- **"Only Ensembl GRCz11 has the full-length product."** A deleted UniProt/TrEMBL
  entry, **F1Q5Y9 (571 aa)**, also once carried the full-length slc43a2a product;
  it is now deleted from UniProtKB and survives only in UniParc (UPI000188A62B).
  So historically the full-length was not *only* in Ensembl. But as a **live entry
  someone would reach today**, Ensembl (via its translation / UniParc mirror) is
  indeed the accessible full-length source, and the current first-reach UniProt and
  RefSeq records are all 153 aa. The practical thrust of "only Ensembl" holds; the
  word "only" is imprecise about history. I could not confirm the specific assembly
  label "GRCz11" vs a newer assembly from the blocked Ensembl endpoint
  (`could-not-access`); the full-length genomic coding sequence is present in the
  current NCBI assembly regardless of label.

- **Evidence level.** `153 aa` is an honest `measured` value — it is a direct
  database field retrieved from UniProt/RefSeq, not a derived or simulated number.
  The downstream inference ("cannot carry residue 200") is the author's logical
  consequence, correctly flagged as a blocker rather than as an observation. No
  measured/derived mislabeling.

## Verdict

The build blocker is real and correctly reasoned: the entries one reaches first
(UniProt TrEMBL Q7ZUS0 / A0A8N7V006, RefSeq NP_956545.1, and the underlying
GenBank AAH47854.1) are all 153 aa and cannot express a residue-200 coordinate,
while the genuine full-length product (571 aa, residue 200 = Thr) is only
accessible via the Ensembl-derived model. The single imprecision is the absolute
word "only Ensembl," which overlooks a now-deleted 571-aa UniProt entry; this does
not change the operational conclusion for anyone building against current
databases. I classify this as **survived** (the one caveat is a footnote, not a
fault in the blocker).

```swarm-challenge
{"claim_id": 185, "outcome": "survived", "reason": "First-reach UniProt (Q7ZUS0, A0A8N7V006) and RefSeq NP_956545.1 are all independently confirmed 153 aa and cannot index residue 200, while the real full-length product (571 aa, position 200 = Thr, mapped to genomic coding sequence) is reachable only via the Ensembl-derived model.",
  "corrected_value": "153 aa (truncated model); full-length product is 571 aa with Thr at position 200",
  "depends_on": ["UniProt Q7ZUS0 length 153 aa", "UniProt A0A8N7V006 length 153 aa", "RefSeq NP_956545.1 length 153 aa", "Ensembl ENSDARP00000120945 / UniParc UPI000188A62B length 571 aa", "position 200 present and = Thr in the 571-aa model", "153 < 200"]}
```
