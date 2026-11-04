# S11 — Network reachability + zebrafish fin-overgrowth allele table

Date of probes: 2026-11-04 (cloud session, outbound HTTPS via the session's agent proxy, `curl` with the proxy CA bundle).

## Step 1 — Reachability (verbatim probe results)

| URL | reachable yes/no | status-or-error |
|---|---|---|
| https://pmc.ncbi.nlm.nih.gov/articles/PMC7240457/ | **no** (in practice) | HTTP 200, but the body (21 KB) is a Google reCAPTCHA challenge page (`productName: 'RecaptchaChallengePageUi'`), not the article |
| https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=zebrafish+longfin+kcnk5b&retmode=json | **yes** | HTTP 200, valid JSON: count=2, idlist=[28760345, 24453984] |
| https://zfin.org/action/quicksearch?query=kcnk5b | **no** | `curl: (60) SSL certificate problem: unable to get local issuer certificate` (proxy tunnels zfin.org without re-signing; upstream chain fails verification — also fails with `--cacert /root/.ccr/ca-bundle.crt`; verification was NOT disabled) |
| https://journals.biologists.com/jeb | **no** | HTTP 403, `server: cloudflare`, "Just a moment..." bot challenge |
| https://europepmc.org/search?query=danio%20fast%20start | **no** | HTTP 403, `server: cloudflare`, "Just a moment..." bot challenge |

Additional probes (not in the requested list, useful for the swarm):

| URL | reachable | status |
|---|---|---|
| https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=kcnk5b&format=json (Europe PMC REST API) | yes | HTTP 200 |
| https://api.crossref.org/works?query=kcnk5b&rows=1 | no (rate-limited) | HTTP 429 |
| `eutils efetch db=pmc&id=<PMCID>&retmode=xml` | yes | returns full JATS body **for open-access-licensed PMC articles**; for some publisher-restricted PMC records (e.g. Development, JBC, Dev Biol author manuscripts here) it returns front matter only, no `<body>` |

**Infrastructure conclusions**

1. The PMC *website* is unusable (CAPTCHA wall, despite HTTP 200 — a status-code-only check would wrongly call it reachable). The **NCBI E-utilities API is the working route**: esearch/esummary/efetch for PubMed abstracts, and `efetch db=pmc` for full text of OA articles.
2. Europe PMC website and Company of Biologists journals (JEB, Development) are behind Cloudflare bot challenges. Europe PMC's REST API works.
3. ZFIN fails TLS verification through this proxy.
4. Note: PMC7240457 (the test article) is *not* a fish paper — eutils maps it to PMID 32252362, "Flight Muscle and Wing Mechanical Properties are Involved in Flightlessness of the Domestic Silkmoth, *Bombyx mori*" (Insects 2020).

## Step 2 — Zebrafish fin-size allele table

Read-levels: **full-text** = full JATS body retrieved via `efetch db=pmc` and searched; **abstract** = PubMed abstract retrieved via `efetch db=pubmed`; **search-summary** = only title/metadata seen. Nothing below is from memory alone; where a value was not found in retrieved text, the cell says so.

| Gene (locus name) | Allele(s) | Molecular lesion | Measured fin-size effect | Mechanism | Sources (read-level) |
|---|---|---|---|---|---|
| *kcnk5b* — **another longfin (alf)** | *alf^dty86d* (original, dominant); second allele written *alf^d30mh* / *alf^dt30mh* (paper uses both spellings); revertant *kcnk5b^j131x8* | Missense **W169L** and **F241Y** (one per allele; the retrieved text says "in both alf alleles, distinct missense mutations (W169L and F241Y)" without stating in prose which allele carries which — assignment is in Fig. 3B, not extracted). Revertant j131x8: 384 bp intragenic deletion → frameshift/PTC, truncated protein lacking 3 TM domains, restores WT fin size | No fold-change in fin length stated in text. Allometric coefficient of fin vs body growth: **WT k = 1.29** (≈isometric), **alf/+ k ≈ 2**. Mutant channels give an **"almost two-fold increase in K⁺ conductance"** in *Xenopus* oocytes. Mosaic ef1a:kcnk5b (WT or W169L) → local overgrowth in ~40% of DsRed+ fish | Gain-of-function two-pore K⁺ (K2P/TASK-2) channel; increased K⁺ conductance, hyperpolarization; acts locally in fin/barbel mesenchyme; requires K⁺ conduction (GFGAAA pore-dead mutant fails); ↑ cell proliferation, not cell size. No epistasis with *sof^dj7e2* | Perathoner et al. 2014, *PLoS Genet* 10:e1004080, PMID 24453984, PMC3894163 (**full-text**) |
| *kcnh2a* — **longfin (lof)** | *lof^dt2* (dominant, dose-sensitive: homozygotes larger); cis revertants *lfr1* (Y669N), *lfr2* (L739Q), *WL7* (Y418X), *WL4*; deficiency *lof^j6e1* | **Chromosome 2 inversion** with breakpoints between 5′ *prrx1a* and 5′ *kcnh2a* (one breakpoint within a DNA transposon between *kcc4a* and *kcnh2a*), coding regions intact → regulatory allele; cis loss-of-function *kcnh2a* mutations revert the phenotype | No fold-change in fin length found in retrieved text (Daane Fig. 3E shows lof/+ vs lof/lof; values not in prose). qRT-PCR shows *kcnh2a* **upregulated** in adult and regenerating lof caudal fins (fold value in figure only) | Cis-ectopic overexpression of the hERG-type voltage-gated K⁺ channel Kcnh2a in fin intra-ray mesenchyme; prolongs the **duration** of outgrowth (late-stage Kcnh2a inhibition fully suppresses overgrowth); Kcnh2a inhibits calcineurin output, overriding growth-cessation signals. Segmentation remains regular (unlike alf). *lof*; *lat4a^nr21* phenocopies flying-fish fin proportions | Daane et al. 2021, *Curr Biol* 31:5052, PMID 34534441, PMC9172250 (**full-text**); Stewart et al. 2021, *Development* 148:dev199384, PMID 34061172, PMC8217709 (**abstract** — efetch returned no body) |
| *slc12a7a / kcc4a* — **schleier (schl)** | *schl^dmh39* (dominant for fin/barbel overgrowth; recessive pigment phenotype); CRISPR in-frame deletions (3-aa, 6-aa) also dominant overgrowth; truncation (99-aa) allele: **no** fin phenotype het or hom | Missense **C583Y** (removes predicted disulfide-bond cysteine); absent in WT siblings (0/56) | No fold-change stated. Log-log caudal-fin length vs standard length: **WT slope 0.9209 (R² 0.97)**, **schleier/+ slope 1.3498 (R² 0.89)**. Isolated as an additive enhancer of *lof* fin length | Loss of K⁺-Cl⁻ cotransport (oocyte Rb⁺ flux); acts as dominant-negative on the Kcc4a dimer (full-length inactive protein worse than haploinsufficiency); ↓ *kcc4b* expression; overgrowth attenuated by *kcnk5b* inactivation → common bioelectric pathway with Kcnk5b. Also enlarged fin veins (↑ vein:artery diameter ratio) | Lanni et al. 2019, *Dev Biol* 456:164, PMID 31472116, PMC7235970 (**full-text**) |
| *cx43 / gja1* — **short fin (sof)** *(short-fin, included as the opposite-direction control)* | *sof^b123* (original; reduced *cx43* expression); three ENU missense alleles (incl. dominant *sof^dj7e2*, named in Perathoner 2014) | *b123*: reduced *cx43* mRNA (no coding lesion described in abstract); others: missense (specific residues not in retrieved abstracts) | ***sof^b123* fins "half the length of wild-type fins"** (≈0.5×); shorter fin-ray segments; reduced proliferation | Gap-junction intercellular communication among dividing blastemal cells sets proliferation and segment length; fin-length defect correlates with loss of junctional coupling | Iovine et al. 2005, *Dev Biol* 278:208, PMID 15649473 (**abstract**); Hoptak-Solga et al. 2008, *Dev Biol* 317:541, PMID 18406403, PMC2429987 (**abstract** — efetch PMC gave no body) |
| *cx43* — **steopsel (stp)** *(contrast allele)* | *stp^tl28d* | Cx43 mutation (residue not in abstract) | Adult vertebrae 59–81% of WT length; fin rays only **~95%** of WT | Reduced gap-junction coupling (shared with sof) **plus** ~50× WT hemichannel current (unique to stp) | Misu et al. 2016, *J Biol Chem* 291:12601, PMID 27129238 (**abstract**) |

### Related, not yet read (search-summary only)
- Kujawski et al. 2014, *Dev Cell*, "Calcineurin regulates coordinated outgrowth of zebrafish regenerating fins", PMID 24561038 — calcineurin inhibition → longfin-like overgrowth (**search-summary**).
- *eLife* 2021, "A calcineurin-mediated scaling mechanism that controls a K⁺-leak channel...", PMID 33830014, PMC8110307 — calcineurin ↔ Kcnk5b (**search-summary**; title only seen, first author not checked).
- Silic et al. 2020, *Genetics*, "Potassium channel-associated bioelectricity of the dermomyotome determines fin patterning", PMID 32546498, PMC7404225 (**search-summary**).
- Lanni et al. 2026, *MicroPubl Biol*, lof^t2 fin vasculature, PMID 41728344, PMC12924073 (**search-summary**).

### Gaps
- **Fold-change in fin length is not stated numerically in the prose** of the alf, lof or schleier papers retrieved; it is reported as allometric slopes or in figures. Only *sof^b123* (~0.5×) and *stp* (~0.95×) have explicit ratios. Getting fold-change for overgrowth alleles needs figure-data extraction (supplementary tables) or ZFIN phenotype annotations (ZFIN currently unreachable).
- Allele↔residue assignment for alf (W169L vs F241Y) is in Perathoner Fig. 3B, not in text.
- Stewart 2021 full text (Development, CoB) unavailable via efetch and website is Cloudflare-blocked; try Europe PMC REST `fullTextXML` endpoint next.
