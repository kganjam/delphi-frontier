# Challenge 280 — adversarial review

**Claim under review (claim_id 280), verbatim:**

> "THE MINIMAL DEMONSTRATED STACK IS TWO ALLELES: `kcnh2a^lof(dt2)`, a *cis*-ectopic longfin
> allele giving coordinated fin overgrowth, and `lat4a^nr21/dmh26`, a dominant T200K that acts as
> a fin-size SUPPRESSOR. Their viable transheterozygote is the published flying-fish-like
> fin-allometry phenocopy"

Recorded evidence level: `literature` · recorded value: 2 alleles · source: `S15-dna.md`

**Reviewer: did not write the claim.** I went looking for a break on all five axes and did not
find one that changes the value. I did find three precision defects worth recording, and I closed
one open question the parent document left open. Verdict and reasoning below.

---

## 0. Sources and read-levels

| Source | What I used it for | Read-level |
|---|---|---|
| Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP. "Modulation of bioelectric cues in the evolution of flying fishes." *Current Biology* 31(22):5052–5061 (2021), DOI 10.1016/j.cub.2021.08.054 — read via PMC9172250 | Every substantive element of the claim | **full-text** — two passes covering the whole document (offsets 0–100000, 100000–end). Caveat below. |
| ZFIN `ZDB-PUB-210918-31`, ZFIN gene record `slc43a2a` / `ZDB-GENE-040426-964`, figure records `ZDB-FIG-221222-34/35` | Nomenclature; allele coordinates | **search-summary** — direct fetch of `zfin.org/action/publication/ZDB-PUB-210918-31/all-figures` returned **HTTP 503**; these facts reached me only through web-search result summaries, not a page read. |
| bioRxiv 2021.03.05.434157 full text | Would have reconciled preprint vs journal | **could-not-access** — HTTP 429 (rate-limited). The parent document read this full-text; I did not. |
| `docs/research/fish/S15-dna.md` @ `origin/claude/zebrafish-glide-edit-stack-7kna51` | The claim's provenance; the allele table minimality rests on | **full-text** (read from git) |
| `crick.zfin.org` mirror | attempted ZFIN figure legend read | **could-not-access** — DNS does not resolve in this session; `crick.zfin.org` would have to be allowed in the session's network settings. |

**Caveat on my "full-text" read-level, stated because it bounds every negative below:** I read the
PMC document through `WebFetch`, which converts the page to text and answers a prompt against it
with a summarizing model. I did **not** view the figure images. Numbers that exist only inside
Figure 4B–C or Figure 1B panels are therefore outside my read, and I cannot and do not assert they
are absent from the figures — only that they are absent from the text.

---

## 1. Arithmetic, redone independently

The claim's only number is "2 alleles". I counted from the genotype, not from the author's working.

Genotype as published: `lat4a^nr21/+ ; kcnh2a^lof/+`

| Quantity | Independent count |
|---|---|
| Loci carrying a mutation | **2** — `kcnh2a` (chr 2) and `lat4a` (chr 15, per ZFIN `slc43a2a`) |
| Mutant alleles | **2** — `nr21`, `lof` |
| Total allele copies at those loci | 4 (2 mutant + 2 wild-type; both loci heterozygous) |
| Engineering lesions to build *de novo* | **2**, but see §3 — they are not of one kind |

"2 alleles" is correct under the two readings that matter (2 loci, 2 mutant alleles). **The
arithmetic does not break.** No fold-changes or derived quantities appear in the claim, so there is
nothing else to recompute.

---

## 2. Is a proxy standing in for the quantity that matters?

**Yes — and this is the strongest surviving criticism, though it does not refute the claim.**

The claim's operative phrase is "the published flying-fish-like fin-allometry **phenocopy**".
*Allometry* is a quantitative concept: the scaling of a part against body size. An allometric
phenocopy claim should therefore rest on a measured match — pectoral-fin-length/SL in the
transheterozygote compared against the same ratio in Exocoetidae, with overlap tested.

What the published text actually contains (my read, quoting the paper):

- Transheterozygote fins are measured **against their own littermate genotypes**: "Pectoral fin
  length (B) and caudal fin length (C) suppression of overgrowth in medial fin by `lat4a` mutation",
  "length normalized by SL", "p values are generated through Tukey's HSD".
- The comparison **to flying fishes** is qualitative: the pattern is "remarkably similar to that of
  flying fishes", and "the interaction between these two genes is sufficient to phenocopy this key
  innovation".
- Flying-fish allometry appears in a *separate* figure (Fig 1B), and its values are not stated in
  the text.

**Negative search, with scope:** I found **no** quantitative transheterozygote-versus-Exocoetidae
comparison — no ratio, no fin/SL value for the transheterozygote, no fold-change, no sample size,
no statistical test against flying-fish values — in the full text of PMC9172250 across both
read passes (the second pass covered references, Key Resources table and data-availability only).
Scope limits: figure panels not read off (see §0); bioRxiv preprint could-not-access; ZFIN figure
page HTTP 503.

**The proxy, named:** *pattern concordance* (which fins are enlarged, which are wild-type sized,
caudal asymmetry) stands in for *allometric equivalence*. **The right quantity** is the paired-fin
length/SL ratio of `lat4a^nr21/+;kcnh2a^lof/+` set against measured Exocoetidae paired-fin/SL
ratios. **My inference, separated from the authors':** the authors assert a phenocopy of allometry;
what their text demonstrates is a phenocopy of *proportional pattern*. Those are not the same
claim, and the stronger word is theirs, not the claim-writer's.

**Why this does not refute claim 280:** the claim says "the **published** ... phenocopy". That is
an assertion about what the literature states, and the literature states exactly this — the
Figure 4 title reads "Intersection of bioelectric and Lat4a-mediated growth pathways is sufficient
to phenocopy the evolved flying fish fin allometry." The claim transcribes the published wording
faithfully, including the word *allometry*. The imprecision is upstream in the paper, not
introduced by the claim. A downstream user who reads claim 280 as a *measured* allometric match
would be wrong, so the caveat belongs in the record — but the claim as written is not.

---

## 3. The hidden assumption, and what happens when it is relaxed

**Hidden assumption: that an allele count is an edit count.**

The claim's value is "2 **alleles**", which is defensible. But the number will be consumed as
engineering burden, and the parent document makes exactly that slide in its own §4.1: "**A1 × A2 is
the minimal demonstrated stack, and it is two edits.**"

Relaxed, the two are not of one kind:

- `lat4a^nr21` is a **single missense substitution**, T200K. ZFIN places `dmh26` at chr15:28,390,802
  (GRCz11) (read-level: search-summary). This is one point edit.
- `kcnh2a^lof(dt2)` is a **chromosomal inversion**. Per the published paper, "this inversion
  juxtaposes the regulatory region of `prrx1a` upstream of the `kcnh2a` transcription start site."
  That is a structural rearrangement, not a point edit. The parent document additionally records
  that the characterised line available at ZIRC (`ZL1494`) is a multi-gene deletion,
  `lof^Df(Chr02:csnk1g2a,rnf2,kifap3b)j6g1`, and that the revertant alleles `lfr1`/`lfr2`/`WL7`
  are no longer maintained or frozen.

**Consequence of relaxing it:** "2" survives as an allele count and as a count of lesions, but it
does **not** support "two edits" in any engineering sense, because one of the two is a large *cis*
regulatory rearrangement whose phenotype depends on the native `kcnh2a` coding sequence remaining
intact in *cis* (the revertant series is what shows this). Anyone budgeting two CRISPR point edits
from this number is misreading it. **This is a defect in the parent document's §4.1, which I am
recording here; it is not a defect in claim 280 as recorded.**

A second assumption worth naming and testing: **that "suppressor" means uniform suppression.** It
does not. The published Results say `lat4a^nr21/+` "is a **medial fin** suppressor of
`kcnh2a^lof/+`, exposing fin-type-specific regulation of size." In the transheterozygote the
*paired* fins remain **overgrown**; only the medial fins return to wild-type size, and the caudal
becomes hypocercal. The paper calls the interaction "specific, **non-additive**". The claim's
unqualified "fin-size SUPPRESSOR" is true of the *single* mutant (`nr21/+` alone shortens all
fins) but flattens the fin-type specificity — and that specificity **is** the mechanism that
produces the flying-fish shape. Compressing it loses the actual content of the result. Precision
defect; does not change the value.

---

## 4. Is the evidence level honest?

**Yes, and it is if anything understated.** Recorded as `literature`; nothing in the claim is
presented as a measurement made by the author, and no derived number is dressed as an observed
one — the claim contains no computed quantity at all.

Each element, checked against the published paper at full-text read-level:

| Claim element | Published text | Verdict |
|---|---|---|
| `kcnh2a^lof(dt2)` is *cis*-ectopic | inversion juxtaposes `prrx1a` regulatory region upstream of `kcnh2a` TSS | confirmed |
| gives coordinated fin overgrowth | "all fins of `kcnh2a^lof/+` are overgrown" | confirmed |
| `lat4a^nr21` is dominant T200K | T200K; `nr21/+` heterozygotes show the short-fin phenotype | confirmed |
| acts as a fin-size suppressor | "a medial fin suppressor of `kcnh2a^lof/+`"; "`lat4a` is a fin suppressor of overgrowth caused by increased potassium channel function" | confirmed, see §3 on specificity |
| transheterozygote is viable | "double mutants between `kcnh2a^lof/+` and `lat4a^nr21/+` are **viable**" | confirmed |
| published flying-fish-like fin-allometry phenocopy | Fig 4 title: "sufficient to phenocopy the evolved flying fish fin allometry" | confirmed as published wording; see §2 |

**Note on read-level improvement:** the parent document's read of the *journal* version was
`search-summary`, with its full-text read on the preprint (whose title differs: "Novel regulators
of growth identified in the evolution of fin proportion in flying fish"), and it explicitly flagged
that it had not reconciled the two. I read the journal version full-text via PMC. **Every claimed
element is present in the published version.** The preprint/journal reconciliation the parent
document left open is, for the elements claim 280 asserts, now closed in the claim's favour. One
wording difference I can see: the published text adds "specific, **non-additive**" where the
preprint quote in the parent document says "specific variation in proportion among fins".

**No invented identifiers.** I checked each one the claim uses rather than assuming it:
`kcnh2a`, `lof`, `dt2`, `lat4a`, `nr21`, `dmh26`, T200K all appear in the sources above.

---

## 5. Regime, taxon, or counter-example the author missed

I looked for four kinds of break and found none that lands.

**5.1 Is two really minimal? Could one allele do it?** No demonstrated single allele produces the
flying-fish *pattern*. From the parent document's allele table, the available single-allele
overgrowth mutants — `kcnh2a^lof`, `kcnk5b^alf`, `slc12a7a^schleier` — all enlarge fins
**coordinately**, across all fins (and barbels, for the latter two); `lat4a^nr21` alone shortens all
fins. The flying-fish pattern requires *differential* change: enlarged paired, wild-type medial,
hypocercal caudal. No single demonstrated allele delivers that. **Two is minimal over the
demonstrated set**, which is what the claim says ("minimal **demonstrated**"). Minimality is not
proven in principle — an undemonstrated single regulatory edit could in principle do it — but the
claim does not assert that, so this is not a break.

**5.2 Does the taxon comparison hold up?** Partially sharper than the claim suggests, in the
*authors'* favour: the paper reports a convergent Lat4a amino-acid substitution in a highly
conserved region, found in both flying-halfbeak lineages and in all Exocoetidae **except** the
sailfin flying fish *Parexocoetus brachypterus*. That exception is a published non-universality
within the taxon, but it concerns the *evolutionary* convergence argument, not the zebrafish
two-allele phenocopy the claim asserts. It does not touch claim 280.

**5.3 Is there a mechanistic counter-example inside the paper?** The paper notes "no significant
change in expression of `kcnh2a` is observed in fins containing the `nr21` mutation" and no
significant difference in `lat4a` expression across fins and genotypes. So the interaction is not
explained by reciprocal expression change. This complicates the *mechanism* but is consistent with
— and in fact is the reason for — the claim's framing of `lat4a` as a genetic suppressor rather
than a transcriptional one. Not a break.

**5.4 Nomenclature — the parent document's open question, now closed.** The parent document
recorded: "ZFIN search returned **no gene with the symbol `lat4a`**; the closest record is
`slc43a2a` (`ZDB-GENE-040426-964`) ... I did not verify that the authors' `lat4a` is ZFIN
`slc43a2a`." My search resolves this: ZFIN's `slc43a2a` (`ZDB-GENE-040426-964`, solute carrier
family 43 member 2a) carries alleles **`dmh26`** and **`mh152`** on chromosome 15, attributed
DIRECT to Daane et al. 2021. `dmh26` is therefore a real ZFIN allele designation for the gene the
paper calls `lat4a`, exactly as the claim's "`lat4a^nr21/dmh26`" asserts. Read-level for this:
**search-summary** (the ZFIN page itself returned HTTP 503 on direct fetch), so it should be
re-confirmed against the ZFIN record by anyone relying on it. **This finding supports the claim; I
report it because a review that only hunts for faults is not a review.**

**5.5 Scope of my negative searches.** Two web searches (one standard, one extended) aimed at a
quantitative transheterozygote-versus-flying-fish fin-ratio comparison; two full-text passes over
PMC9172250. Not searched to exhaustion: the figure image data, the bioRxiv preprint (429), the
ZFIN figure pages (503/DNS). I did not search for independent replication of the transheterozygote
cross by any other group, so claim 280 rests on a single publication — worth noting, not a fault
in the claim.

---

## 6. Verdict

**SURVIVED.**

I tried to break the arithmetic (§1), the proxy (§2), the load-bearing assumption (§3), the
evidence level (§4), and the taxon (§5), and the recorded value **2 alleles** stands unchanged.
Every element of the claim is confirmed in the *published* version at a read-level **better** than
the parent document had, and the parent's open nomenclature question resolves in the claim's
favour. The claim invents nothing.

Three precision defects go on the record. None changes the value, and I decline to inflate any of
them into a refutation:

1. **"fin-allometry phenocopy" is the paper's own phrase, but the paper's text demonstrates
   pattern concordance, not a measured allometric match** (§2). No transheterozygote-versus-
   Exocoetidae ratio comparison appears in the full text; figure panels unread. Claim 280 is a
   faithful transcription of published wording, so the claim survives — but it must not be
   consumed as a quantitative allometric equivalence.
2. **"fin-size SUPPRESSOR" flattens the published "medial fin suppressor"** (§3). Suppression is
   fin-type-specific and explicitly non-additive; paired fins stay overgrown. That specificity is
   the mechanism, and the compressed phrasing loses it.
3. **An allele count is not an edit count** (§3). `kcnh2a^lof(dt2)` is a chromosomal inversion
   dependent on the *cis* `kcnh2a` coding sequence, not a point edit. The claim's "2 alleles" is
   correct; the parent document's "it is two edits" (`S15-dna.md` §4.1) is the overreach, and it is
   outside claim 280.

One thing claim 280 does **not** assert, and which I confirm it is right not to assert: no gliding,
launch, or any aerial measurement on these fish appears in the published text. The claim is scoped
to fin allometry, and it stays there. The parent document's separate refusal of the *flight* stack
(six empty capability slots) does not bear on this claim, and I note it only so a later reader does
not mistake claim 280 for the flight claim.

```swarm-challenge
{"claim_id": 280, "outcome": "survived", "reason": "Every element — two loci, the cis-ectopic kcnh2a^lof inversion, the dominant T200K lat4a^nr21/dmh26 suppressor, transheterozygote viability, and the 'phenocopy the evolved flying fish fin allometry' wording — is confirmed verbatim in the published Current Biology version at full-text read-level, the allele count recomputes to 2 independently, and the parent document's open lat4a-to-ZFIN nomenclature question resolves in the claim's favour; the three defects found (allometry asserted on pattern concordance rather than a measured Exocoetidae ratio comparison, 'suppressor' flattening the published fin-type-specific 'medial fin suppressor', and allele-count being misread downstream as edit-count given that lof is a chromosomal inversion) are precision defects that leave the recorded value unchanged.",
  "corrected_value": null,
  "depends_on": [
    "Daane et al. 2021, Current Biology 31(22):5052-5061, DOI 10.1016/j.cub.2021.08.054, read full-text via PMC9172250 (text only; figure panels not read): transheterozygote 'are viable'; 'specific, non-additive variation in proportion among fins'; 'all fins of kcnh2a lof/+ are overgrown and all fins of lat4a nr21/+ are shortened'; 'wild-type-sized medial fins, while the paired fins are overgrown'; caudal 'is hypocercal, with an elongated ventral lobe'; 'remarkably similar to that of flying fishes'",
    "Same source, Results: lat4a nr21/+ 'is a medial fin suppressor of kcnh2a lof/+, exposing fin-type-specific regulation of size'",
    "Same source, Figure 4 title: 'Intersection of bioelectric and Lat4a-mediated growth pathways is sufficient to phenocopy the evolved flying fish fin allometry'",
    "Same source: kcnh2a^lof is an inversion that 'juxtaposes the regulatory region of prrx1a upstream of the kcnh2a transcription start site'",
    "Same source: lat4a^nr21 is a dominant T200K substitution with the short-fin phenotype in nr21/+ heterozygotes",
    "ZFIN slc43a2a / ZDB-GENE-040426-964 carrying alleles dmh26 (chr15:28,390,802 GRCz11) and mh152, attributed DIRECT to Daane et al. 2021 (read-level: search-summary; zfin.org direct fetch returned HTTP 503)",
    "S15-dna.md section 2.1 allele table (origin/claude/zebrafish-glide-edit-stack-7kna51): kcnh2a^lof, kcnk5b^alf and slc12a7a^schleier each enlarge all fins coordinately, and lat4a^nr21 shortens all fins — the basis for no single demonstrated allele producing the differential paired-versus-medial pattern, on which the word 'minimal' rests",
    "S15-dna.md Methods row: revertant alleles lfr1/lfr2/WL7 in cis were 'essential for expression of the long-finned phenotype', and the ZIRC line ZL1494 is the multi-gene deletion lof^Df(Chr02:csnk1g2a,rnf2,kifap3b)j6g1 — the basis for the allele-count-is-not-edit-count finding",
    "Negative: no quantitative transheterozygote-versus-Exocoetidae fin-ratio comparison in the full text of PMC9172250 across both read passes; scope excludes figure image data, bioRxiv 2021.03.05.434157 (HTTP 429, could-not-access), and ZFIN figure pages (HTTP 503 / DNS unresolved)"
  ]}
```
