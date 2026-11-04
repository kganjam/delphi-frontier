# Challenge 39: lat4a nr21/+ ; kcnh2a lof/+ fin phenotype

**Claim under review (not written by me):** "The double heterozygote shows elongated paired fins, a
hypocercal caudal fin with elongated ventral lobe, and wild-type-sized medial fins."
Recorded evidence level: `literature`. Value: n/a. Source: Daane et al. 2021.

**Verdict: SURVIVED**, with two scope notes (below). Neither one changes the claim's wording.

## Sources and read-levels

| Source | Read-level | Notes |
|---|---|---|
| Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP. "Modulation of bioelectric cues in the evolution of flying fishes." *Curr Biol* 31(22):5052–5061 (2021). doi:10.1016/j.cub.2021.08.054; PMID 34534441; PMCID PMC9172250 | **full-text, partial**: PMC HTML, characters 0–100,000 of about 149,000. I read it through a fetch tool that returns extracted quotes, not the raw page. The last part (about 49k characters, likely the methods and references) was not read. | Primary source |
| Europe PMC REST record for the DOI | listing | Used for the PMID, PMCID and an abstract summary |
| ZFIN ZDB-PUB-210918-31 / ZDB-FIG-221222-35 (Fig. 4) | search-summary | Direct fetch failed (503, and the mirror host was blocked) |
| Quanta Magazine, 2022-01-05 | search-summary | Fetch blocked: the host is not on the session's network allowlist |
| cell.com full text | could-not-access | HTTP 403 |

## 1. Arithmetic

The claim contains no numbers, so there is nothing to recompute. The paper's text and legends give
no numeric fin lengths for the double mutant; they report only Tukey's HSD p-value thresholds. I did
not try to read values off the plots.

## 2. Does the source say this?

Yes, almost word for word. These are excerpts from the full text as the fetch tool returned them
(the tool cut long sentences into fragments):

- "the lat4a nr21/+;kcnh2a lof/+ fish show wild-type-sized medial fins, while the paired fins are overgrown"
- "lat4a nr21/+ is a medial fin suppressor of kcnh2a lof/+"
- "the caudal fin of kcnh2a lof/+;lat4a nr21/+, while generally wild type in size, is hypocercal, with an elongated ventral lobe."
- Fig. 4 legend: "As in flying fishes, the nr21/lof trans-heterozygotes exhibit elongated paired fins and a hypocercal caudal fin."

Each part of the claim (paired fins overgrown, hypocercal caudal fin with an elongated ventral lobe,
wild-type-sized medial fins) is stated by the authors. The genotype is right: both alleles are
heterozygous (nr21/+ and lof/+). The paper says "double mutants" and "trans-heterozygotes", so
"double heterozygote" is a fair paraphrase.

## 3. Proxy check (does not refute)

My reading of the legend, not the authors' statement: the quantitative support for "wild-type-sized
medial fins" seems to come from **caudal fin length** only (Fig. 4C: "Pectoral fin length (B) and
caudal fin length (C) suppression of overgrowth in medial fin by lat4a mutation"). The legends I
read report no dorsal- or anal-fin length measurement. In the portion I read, the only dorsal-fin
data are qRT-PCR of *kcnh2a* (Fig. 4D). So for the dorsal and anal fins, "wild-type-sized" appears to
rest on images, not a measured length. Likewise, "elongated paired fins" is measured for the
pectoral fin only. I found no length data for the pelvic fins in the legends or results I read.
Scope: this is based on the figure legends and results text I read. The unread last part of the page
or the supplementary material could contain dorsal, anal or pelvic measurements. I did not check the
supplement.

The "elongated ventral lobe" also seems to be a qualitative description: the asterisk in Fig. 4A
marks the hypocercal fin, and I saw no lobe-length ratio. The caudal fin is described as "generally
wild type in size". That fits the claim and does not contradict it.

This is a caveat about how strong the evidence is. The claim is still a faithful report of what the
authors say.

## 4. Hidden assumption

The claim assumes the reader knows what "lof" is. My note from background knowledge, not checked
against the text: zebrafish *longfin* (lof) is a dominant overgrowth allele. The paper describes it
as a chromosomal rearrangement that changes *kcnh2a* regulation and upregulates *kcnh2a* (Fig. 3G),
so it is a gain of function. One search summary I got called it a "loss-of-function line". That is
wrong, but the error is in the summary, not in the claim. Anyone extending claim 39 should not
repeat it. I also did not find penetrance (how many double mutants show the hypocercal fin) in the
text I read. That figure is `unknown`.

## 5. Evidence level

`literature` is honest. This is an observation made by the authors in zebrafish and reported in a
peer-reviewed paper. The claim does not present it as a value measured by this project, and it adds
no derived number.

## 6. Counter-examples and missed regimes

- Taxon scope: the claim is about zebrafish (*Danio rerio*) carrying both alleles. It does not say
  that flying fishes have this genotype. The paper itself notes an exception among flying fishes, the
  sailfin flying fish *Parexocoetus brachypterus*, which has an elongated dorsal fin. That limits how
  far the analogy to flying fishes goes, but it does not break the zebrafish claim.
- I found no published replication or contradiction of the double-mutant phenotype. Scope of that
  negative search: two web searches (standard mode) plus the Europe PMC record; I did not search for
  citing papers.

## Bottom line

The claim matches the primary source's results text and Fig. 4 legend. My attempts to break it were
proxy concerns (medial fins measured through the caudal fin, paired fins through the pectoral fin)
and a missing penetrance figure. Both are caveats on evidence strength, not errors in the claim.

```swarm-challenge
{"claim_id": 39, "outcome": "survived", "reason": "Daane et al. 2021 full text states nearly verbatim that lat4a nr21/+;kcnh2a lof/+ fish have overgrown paired fins, wild-type-sized medial fins, and a hypocercal caudal fin with an elongated ventral lobe; the only caveat is that medial-fin size appears quantified via caudal length (and paired via pectoral), with dorsal/anal size apparently qualitative.", "corrected_value": null}
```
