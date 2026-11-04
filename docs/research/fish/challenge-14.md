# Challenge 14: are the actinodins collagen-like?

**Claim under review (the author's words):** "The actinodins are NOT collagen-like despite actinotrichia being
historically termed elastoidin: glycine is 5.4% and 4.5%, where a Gly-X-Y collagen repeat requires about 33%."
Recorded evidence level: *derived*. Value: 5.4 percent glycine. Source: computed from UniProt E7F5V5 and A0ACM8QEN9.

**Verdict: SURVIVED.** The conclusion holds under a stricter test than the one the author used. I found two
weaknesses in how the argument is made. Neither changes the result.

---

## 1. Independent arithmetic

I downloaded the FASTA files from `rest.uniprot.org` today (2026-11-04) and counted residues with my own script.
I did not reuse the author's working. Every number below is **computed by me**, not measured.

| Accession | Entry | Length (aa) | Gly | Gly % (whole precursor) | Gly % (mature chain, after UniProt SIGNAL) |
|---|---|---|---|---|---|
| E7F5V5 | Actinodin1 precursor, *D. rerio*, `and1` | 570 | 31 | **5.44** | 5.34 (chain 27–570) |
| A0ACM8QEN9 | Actinodin2 precursor, *D. rerio*, `and2` | 508 | 23 | **4.53** | 4.74 (chain 24–508) |

The stated 5.4% and 4.5% are reproduced. Removing the signal peptide moves either value by at most 0.2 points.

## 2. Is a proxy standing in for the real quantity?

**Yes.** Whole-protein glycine percentage is a proxy. What actually makes a protein collagen-like is an
uninterrupted Gly-X-Y triple-helical domain. The roughly 33% figure applies only *inside that domain*. It does not
apply to a whole precursor, and the comparison is loose in both directions:

- **A real collagen falls below 33% as a whole protein.** Human COL1A1 (P02452, a positive control I added)
  computes to **26.7% Gly** over the full 1464-aa precursor, because its propeptides dilute the helix.
- **Short collagenous domains hide inside low-glycine proteins.** Human C1QA (P02745) computes to **16.7% Gly**
  and MBL2 (P11226) to **12.5% Gly**. Both have well-known collagen-like stalks. On its own, a low overall Gly %
  cannot rule out a short collagenous segment.

**The correct test.** For each of the three reading phases I scanned for the longest run of consecutive triplets
that begin with G. Results (computed):

| Protein | Longest consecutive G-X-Y run |
|---|---|
| COL1A1 (control) | 338 triplets |
| C1QA (control) | 16 triplets |
| MBL2 (control) | 12 triplets |
| Actinodin1 E7F5V5 | **2** |
| Actinodin2 A0ACM8QEN9 | **2** |

The positive controls are detected easily, even though their overall Gly % is far below 33%. The actinodins never
reach more than 2 consecutive Gly-X-Y triplets, so they cannot form a triple helix. Under the right test the claim
gets **stronger**. The author's proxy happens to give the correct answer, but "requires about 33%" is the wrong way
to frame the threshold for whole proteins.

## 3. Hidden assumptions, relaxed

- **"The actinodins" is generalised from 2 of 4 zebrafish paralogs.** I tested the other two (computed):
  `and3` Q7SZZ6 has 2.71% Gly and a longest run of 1. `and4` A0AC36IS99 has 3.92% Gly and a longest run of 1.
  Both hold.
- **Taxon scope.** Actinodin1 orthologs (computed): *Polyodon spathula* A0A142C693 (a fragment) 4.31% Gly, run 1;
  *Salmo salar* A0A1S3NHX9 5.04%, run 2; *Takifugu rubripes* A0A3B5K018 3.88%, run 2; *Cottoperca gobio*
  A0A6J2RWQ5 4.78%, run 2. None is collagen-like. Scope of this check: 6 sequences picked by hand from a UniProt
  `gene:and1` search, plus `gene:and3` and `gene:and4` searches restricted to *D. rerio*. It is not an exhaustive
  phylogenetic survey, and I did not look at chondrichthyan sequences.
- **Sequence reliability.** All actinodin entries are unreviewed TrEMBL records. E7F5V5 and A0ACM8QEN9 carry
  PE=1 (evidence at protein level). Gene-model errors could shift the composition slightly, but they could not
  create a triple helix of more than 300 residues that the scan missed.

## 4. Is the evidence level honest?

**Yes.** The level is recorded as *derived* and the source says "computed here". That is accurate. The number is
correct to the stated precision.

## 5. Counter-examples and framing

The "despite … elastoidin" clause creates a contrast that does not really exist. It could also mislead a reader
into concluding that actinotrichia themselves are not collagenous. They are. Durán et al. 2011,
*Dev Biol* 354:160–172, PMID 21420398, reports that actinotrichia contain Collagen I and a fish-specific
Collagen II encoded by `col2a1b`. It calls the actinodins the *non-collagen* components of actinotrichia.
[Read-level: **search-summary**, via ZFIN ZDB-PUB-110425-4. I did not read the full text.] A collagenous fibril with
non-collagenous partners proteins is consistent with the claim. The contrast is a rhetorical flaw, not a factual
error about the actinodins.

Negative search, scope stated: one standard web search ("actinotrichia collagens col1a1 col2a1 Durán 2011
elastoidin actinodin") found nothing on elastoidin's historical amino-acid composition. Whether the older
elastoidin analyses reported collagen-level glycine is **unknown** from this review.

I found no published report, and no sequence among those I checked, of an actinodin with a collagenous domain.

## Why it survives

The arithmetic reproduces. The evidence level is honest. The proxy is crude, but the direct test (scanning for
Gly-X-Y runs) confirms the conclusion with a margin of two orders of magnitude: 2 triplets against 12 to 338 in the
controls. The conclusion also holds for `and3` and `and4` and across teleost and paddlefish orthologs.

Recommended wording edits, which do not change the value:

1. Replace "requires about 33%" with "has no Gly-X-Y run longer than 2 triplets. A collagen triple-helical domain
   is about 33% Gly, but a whole collagen precursor can be lower (COL1A1 is 26.7%)."
2. Note that the collagen in actinotrichia comes from Col1/Col2 (Durán et al. 2011), not from the actinodins.

```swarm-challenge
{"claim_id": 14, "outcome": "survived", "reason": "Glycine values reproduce (5.44% and 4.53%, computed). The whole-protein Gly% proxy is crude, but a direct Gly-X-Y run scan finds at most 2 consecutive triplets in all four zebrafish actinodins and four other species' orthologs, against 12-338 in collagenous controls.", "corrected_value": null}
```

Sources: [ZFIN ZDB-PUB-110425-4 (Durán et al. 2011)](https://zfin.org/ZDB-PUB-110425-4) · UniProt REST
(`rest.uniprot.org/uniprotkb/{E7F5V5,A0ACM8QEN9,Q7SZZ6,A0AC36IS99,A0A142C693,A0A1S3NHX9,A0A3B5K018,A0A6J2RWQ5,P02452,P02745,P11226}.fasta`)
