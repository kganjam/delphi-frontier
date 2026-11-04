# Challenge 264 — adversarial review of [S11-D] Ca²⁺/calcineurin brake and its claimed coupling to long-fin K⁺ channels

**Claim under review (verbatim):**

> "[S11-D] The Ca2+/calcineurin brake on fin outgrowth stands (cacna1g LOF, FK506, Cav blockers), but its claimed
> coupling to long-fin K+ channels via fibroblast hyperpolarisation falls as an established premise: hyperpolarisation
> was measured only in Xenopus oocytes, the only in vivo fin readouts (DiSBAC2(3), Perathoner 2014; Jiang 2024) show
> depolarisation, and fibroblast resting Vm has never been measured.
> KEY: in vivo fin-cell dVm for alf/lof: unknown in mV; sign by DiSBAC2(3) in whole fin = depolarising (relative
> fluorescence, p<0.001, N=21-23); oocyte dVm = toward -90 to -100 mV with ~2x gK
> VERDICT: falls"

Recorded evidence level: `measured`. Value: `n/a`. Source: `harvest:deepen-s11-fin-size-6bhrjv`
(the harvest record is not present in this repository; the claim was therefore re-tested against primary literature).

**My outcome: SURVIVED — the verdict `falls` holds, and is better supported than the claim states.**
Two defects are nonetheless recorded below: one mislabelled quantity in the KEY (§4) and one over-unified citation
framing (§4). Neither reverses the verdict. One missed source (§5c) is the single live risk to it and I could not
read it in full.

---

## 0. Sources and read-levels

| Source | Read-level | What I used it for |
|---|---|---|
| Perathoner S, Daane JM, et al. *PLoS Genet* 2014;10(1):e1004080 | **full-text** (via journals.plos.org) | Fig. S4 dye data; Fig. 5 oocyte electrophysiology; Methods |
| Daane JM, Lanni J, Rothenberg I, Seebohm G, Higdon CW, Johnson SL, Harris MP. *Sci Rep* 2018;8:10391 | **full-text** (PMC6039437) | FK506/VIVIT oocyte conductance direction; absence of fin Vm |
| Stewart S, Le Bleu HK, Yette GA, Henner AL, Robbins AE, Braunstein JA, Stankunas K. *Development* 2021;148:dev199384 | **full-text** (PMC8217709) | `lof`/`kcnh2a` cell type; absence of Vm; absence of a hyperpolarisation assertion |
| Daane JM, Blum N, Lanni J, et al. *Curr Biol* 2021 (flying fishes) | **full-text** (PMC9172250) | taxon extension; absence of any Vm or heterologous electrophysiology |
| Jiang X, Zhao K, Sun Y, … Antos CL. *PLoS Biol* 2024;22(3):e3002565 | **full-text, first ~100 kB of 211 kB** (journals.plos.org) | DiSBAC2(3) in pectoral fin bud; Na⁺-channel two-step model |
| Le Bleu HK, Kioussi RG, Henner AL, Lewis VM, Stewart S, Stankunas K. *Development* 2025;152(23):dev204739 | **full-text, first 100 kB of 106 kB** (PMC13078715) | `cacna1g` LOF phenotype; Ca²⁺ blockers; confirms *no* voltage dye used |
| Kujawski S, Lin W, … Antos CL. *Dev Cell* 2014;28:573–587 | **listing** (Europe PMC metadata only) | citation verification for the FK506 result only |
| Silic MR, Zhang G. *Cells* 2023;12(8):1148 | **full-text, first 100 kB of 314 kB** (PMC10137051) | independent corroboration that no fin-cell Vm exists; GEVI inventory |
| Aramaki T, Kondo S. bioRxiv 10.1101/2024.03.27.587111 | **abstract + search-summary** — see §5c | cell-type-specific `kcnk5b` W169L; optogenetic Vm manipulation |

**Access failure, stated precisely:** I could not read the Aramaki & Kondo full text. bioRxiv returned HTTP 429 /
Cloudflare error 1015 on **eight** attempts across ~35 minutes (direct HTML, `.full`, `.full.pdf`, v1 and v2, three
of them on a long backoff); Europe PMC `fullTextXML` for `PPR830054` returned HTTP 500;
`europepmc.org/article/PPR/PPR830054` returned HTTP 403; `api.semanticscholar.org` and `api.unpaywall.org` are both
blocked by this environment's egress proxy (HTTP 403 on CONNECT). I therefore report its abstract, plus one
**search-summary**-level pass over indexed full-text snippets (§5c) which I flag as unverified against the source.

**Publication status checked, not assumed:** the bioRxiv API (`api.biorxiv.org/pubs/...`) returns
`no articles found for published version` for 10.1101/2024.03.27.587111; `api.biorxiv.org/details/...` lists v1
2024-03-29 and v2 2026-08-24. It is an unpublished preprint as of 2026-11-04.

---

## 1. Arithmetic redone independently

I recomputed from the primary inputs without reference to the author's working. Inputs: Perathoner 2014 Methods
state oocytes in ND96 (2 mM KCl) at 18 °C, holding potential −80 mV; Xenopus oocyte intracellular [K⁺] ≈ 110 mM
(standard value for the preparation, not a figure from the claim).

**(a) Where "−90 to −100 mV" actually comes from — this is a *calculated* thermodynamic ceiling, not a measurement.**

E_K = (RT/F)·ln([K⁺]_out/[K⁺]_in) = 25.09 mV · ln(2/110) = **−100.5 mV** (my calculation).

This reproduces the figure the claim quotes. Critically, Perathoner et al. label it as such themselves — the paper's
own words for the −90 to −100 mV range are "the equilibrium potential for K⁺ in Xenopus oocytes." So the number is
right, and it is not a measured membrane potential: it is the asymptote a K⁺-dominated membrane approaches.

**(b) A ~2× gK increase cannot produce that potential from a normal oocyte baseline.** Using a linear
two-conductance model V_m = (g_K·E_K + g_L·E_L)/(g_K + g_L) with E_L = 0 mV and E_K = −100.5 mV
(**my calculation, a model result, not an observation**):

| WT-injected baseline V_m | implied g_K/g_L | V_m after 2× g_K | ΔV_m bought by 2× g_K |
|---|---|---|---|
| −40 mV | 0.66 | −57.2 mV | −17.2 mV |
| −50 mV | 0.99 | −66.8 mV | −16.8 mV |
| −60 mV | 1.48 | −75.2 mV | −15.2 mV |
| −70 mV | 2.29 | −82.5 mV | −12.5 mV |
| −80 mV | 3.90 | −89.1 mV | −9.1 mV |

Fold-increase in g_K required to *reach* −95 mV: ×26.0 from −40 mV, ×17.3 from −50 mV, ×11.6 from −60 mV,
×4.4 from −80 mV.

**Consequence.** The KEY's pairing "oocyte dVm = toward −90 to −100 mV with ~2x gK" is internally strained. A
two-fold conductance increase buys at most ~17 mV, and lands at −90 mV only if the wild-type-injected oocyte already
sat near −80 mV — in which case the *increment* attributable to the `alf` mutation is ~9 mV, not the ~50 mV that
"toward −90 to −100 mV" connotes. The two numbers in that KEY field describe different things and should not be
juxtaposed as a single effect size.

**(c) "dVm" is not a delta in the source at all.** Perathoner et al. report a *correlation across oocytes* —
"the higher the conductance for K⁺ measured at 50 mV, the more negative the membrane potential of the oocyte"
(full-text) — with each point one oocyte (Fig. 5D). They report no paired pre/post shift and no mean ΔV_m. Calling
this "oocyte dVm" imports a quantity the experiment did not produce.

None of (a)–(c) damages the claim's verdict. All three *deepen* it: the one piece of hyperpolarisation evidence in the
whole dossier is weaker, and more theoretical, than the KEY presents it as.

---

## 2. Is a proxy standing in for the quantity that matters?

Yes — **two** proxies, and the claim names only one.

**Proxy 1 (named by the claim): DiSBAC2(3) relative fluorescence for resting V_m in mV.** The claim flags this
honestly ("relative fluorescence", "unknown in mV"). But it under-states the confound. DiSBAC2(3) is an anionic
oxonol that partitions into cells and membranes as they depolarise, so its intensity is a joint function of V_m,
dye loading and penetration, membrane area per unit volume, cell density, and optical path length. Perathoner's
Fig. S4C is a **whole-fin pixel average compared across genotypes whose fins differ in size and tissue
composition** — exactly the condition under which geometry and dye access, not voltage, can carry a difference.
Jiang et al. 2024 concede the same hazard in their own system, acknowledging "substantial variation and possible
dye-penetration effects" (full-text). So the *depolarising sign* that the claim rests part of its case on is itself
proxy-limited. The claim's verdict does not depend on that sign being right (see §3), so this does not break it.

**Proxy 2 (NOT named by the claim, and the more serious one): the Xenopus oocyte standing in for the fin cell.**
This is the load-bearing substitution in the hyperpolarisation premise, and it is worse than a measurement-quality
problem — it is a category problem. The voltage consequence of a given increase in g_K is **entirely determined by
the host cell's background conductances**, as §1(b) makes quantitative: the same ~2× g_K yields −57 mV in a cell
whose baseline is −40 mV and −89 mV in one whose baseline is −80 mV. An oocyte's conductance background bears no
established relationship to an intra-ray mesenchymal cell's. Therefore *even if the oocyte hyperpolarisation is
exactly right, it does not transfer*, and no amount of additional oocyte work can establish the fin coupling.

**The right quantity.** Resting V_m, in mV, of the `kcnk5b`/`kcnh2a`-expressing intra-ray mesenchymal
(fibroblast-lineage) cell and of fin keratinocytes, measured by patch clamp or a calibrated genetically encoded
voltage indicator, in wild-type versus `alf` and `lof`. **This does not exist.** Scope of that negative: I searched
Europe PMC and the open web for zebrafish fin fibroblast / mesenchyme / blastema resting membrane potential and
patch-clamp measurements, and read the Silic & Zhang 2023 review specifically for it. That review states
"Although direct evidence of bioelectricity in zebrafish fin development is still lacking" and classes the fin
mutants as "indirect evidence" (full-text); its GEVI inventory lists ASAP1–3, Bongwoori, VSFP, QuasAr, Archon1,
Voltron/Voltron2, Positron as applied to zebrafish **brain, heart, spinal cord and olfactory tissue — not fin**.
The only fibroblast values it tabulates (−25 to −16 mV) are generic vertebrate fibroblast figures, neither zebrafish
nor fin, and I did not treat them as fin data.

---

## 3. The hidden assumption, tested relaxed

The assumption carrying the claim's *framing* is that **a single sign-consistent V_m shift is the coupling variable
at all** — that K⁺-channel gain-of-function and calcineurin inhibition must converge by moving V_m the same way.

Relaxed, the claim gets **stronger**, because of a sign inconsistency the author missed. From Daane et al. 2018
(full-text, verbatim): oocytes expressing wild-type Kcnk5b "show decreased conductance when treated with FK506";
the calcineurin peptide inhibitor VIVIT "showed a comparable decrease in conductance"; and Kcnk5b/I290A "had lower
conductance than wildtype" and was non-responsive to FK506. Yet FK506 *enlarges* fins, and `alf` — which
*increases* conductance — also enlarges fins. The authors state the tension themselves and do not resolve it:

> "This difference of the direction of conductance with similar growth outcomes may also point to the importance of
> signaling events downstream of changes in conductance that drive fin growth."

**My inference (not the authors', and not the claim's):** two manipulations that move g_K in *opposite* directions
produce the *same* phenotype. No monotonic V_m variable can be the coupling term for both. This is independent of
any dye, any proxy, and any oocyte-to-fin extrapolation — it is an internal contradiction in the hyperpolarisation
model, sourced from the primary paper that proposed the bioelectric–calcineurin module. It is the strongest available
argument for the claim's verdict, and the claim does not use it.

**A second hidden assumption, which cuts the other way: that "fibroblast" is the relevant cell.** The claim frames
the coupling as "via *fibroblast* hyperpolarisation". For `lof`/`kcnh2a` that cell assignment is correct — Stewart
et al. 2021 conclude "ectopic Kcnh2a functions in intra-ray mesenchyme and/or blastema cells derived from this
lineage", and their Discussion speaks of "intra-ray fibroblasts and derived blastema mesenchyme cells" (full-text);
Daane et al. 2021 likewise report human *KCNH2* overexpression in fin mesenchyme causing localised overgrowth
(full-text). For `alf`/`kcnk5b` it is contested: Aramaki & Kondo's abstract reports that cell-type-specific
manipulation "in keratinocytes primarily affected fin size, whereas manipulation in osteoblasts preferentially
altered fin-ray segment length" (abstract-level). **I preserve this disagreement rather than resolving it:**
Perathoner 2014 localises `kcnk5b` to fin mesenchyme, Aramaki & Kondo localise the *size* effect to keratinocytes,
and they are not reconciled in the literature I read. Under the Aramaki & Kondo assignment, "fibroblast resting Vm
has never been measured" remains factually true but would be interrogating a cell that does not carry the `alf` size
signal — which weakens that *particular* sub-argument without touching the verdict, since fin keratinocyte resting
V_m has never been measured either.

---

## 4. Is the evidence level honest?

Mostly yes; one component is mislabelled, and one citation framing is over-unified.

**Honest:**
- "in vivo fin-cell dVm for alf/lof: unknown in mV" — a correctly stated negative, and I independently confirmed it
  across six primary papers plus a review (§2 scope).
- "sign by DiSBAC2(3) in whole fin = depolarising (relative fluorescence, p<0.001, N=21-23)" — **verified verbatim.**
  Perathoner Fig. S4: "DiSBAC2(3) staining in wild type fins exhibited hyperpolarization localized to discrete
  regions of the fin"; "alf fins in contrast show high levels of depolarization across the fin"; Fig. S4C legend
  "***: p<0.001, N = 21–23". Also corroborated internally: "DiBAC4(3), another dye sensitive to depolarization,
  showed similar effects, while DiSC3(5), a dye sensitive to hyperpolarized states, was uninformative (data not
  shown)." Statistics: unpaired Student's t-test, juveniles at STL 16–18 mm. The claim's qualifier "relative
  fluorescence" is the right disclosure.

**Defect 1 — a derived number carried as measured.** "oocyte dVm = toward −90 to −100 mV" sits under an evidence
level of `measured`. Per §1(a) it is the K⁺ equilibrium potential — a quantity the source itself names as the
equilibrium potential and which I reproduce by calculation as −100.5 mV. It is a thermodynamic ceiling, not a
measured mean, and not a delta (§1c). Under this challenge's own standard — "a derived number presented as measured
is a defect even when the number is right" — this is a defect, and the number *is* right.

**Defect 2 — two readouts presented as one evidence class.** The claim writes "the only in vivo fin readouts
(DiSBAC2(3), Perathoner 2014; Jiang 2024)". I initially suspected "Jiang 2024" was miscited, because the `cacna1g`
paper the claim leans on elsewhere is Le Bleu et al. — and I confirmed Le Bleu et al. 2025 use **no voltage dye at
all** (GCaMP6s plus KCl depolarisation; full-text). But Jiang 2024 is real, is a distinct paper, and does use
DiSBAC2(3): *PLoS Biol* 22(3):e3002565, Antos lab. The citation stands. The framing does not: the two are different
regimes and are not independent replications —

| | Perathoner 2014 Fig. S4 | Jiang 2024 Fig. 5 |
|---|---|---|
| appendage | caudal fin | **pectoral fin bud** |
| stage | juvenile, STL 16–18 mm | **embryonic, 32–56 hpf** |
| genetics | `alf` allele (endogenous GOF) | **`kcnk5b-mCherry` overexpression** |
| tissue scored | whole fin average | ectoderm and mesenchyme, 4 positions |
| statistics reported | p<0.001, N = 21–23 | N ≥ 3 experiments, ≥6 embryos each; **no p-values in text** (S5 Data) |

**Defect 2b — Jiang 2024 is not flat counter-evidence to hyperpolarisation, and the claim reads it as if it were.**
Jiang et al. report that "overexpression of kcnk5b-mCherry significantly increased depolarization", note this is
counterintuitive for a K⁺ leak channel, and then **propose that Kcnk5b first hyperpolarises the membrane, which
activates Na⁺ channels to depolarise the cells** — supported by vinpocetine and dibucaine blocking both the
depolarisation and the Kcnk5b-enhanced growth. Their own model therefore *retains* hyperpolarisation as the upstream
step. The claim's use of Jiang as evidence against hyperpolarisation flattens a two-step model into a sign
contradiction. **I preserve the disagreement.** It does not rescue the premise, because Jiang et al. present the
hyperpolarising first step explicitly as a hypothesis, not a demonstration, and never measure V_m in mV or with an
electrode — which is precisely the claim's point, reached by a different route than the claim takes.

---

## 5. Regimes, taxa, and counter-examples the author missed

**(a) Stewart et al. 2021 (`lof`/`kcnh2a`) — missed; strengthens the claim decisively.** The claim's KEY invokes
`lof` but cites nothing for it. The primary `lof` paper (full-text) reports **no** V_m measurement by any method,
the word "hyperpolarization" **does not appear**, and the authors never assert that Kcnh2a hyperpolarises fin cells —
their channel-physiology statements are generic to the EAG/KCNH class. Their stated future work is:
"Key future steps include characterizing membrane potentials and putative **depolarizing** signals." So for one of
the two long-fin K⁺ channels the claim's premise was never asserted by the source in the first place, and the
source's own expectation points depolarising.

**(b) Daane et al. 2018 conductance-sign inconsistency — missed; strongest available support for the verdict.**
Treated in §3.

**(c) Aramaki & Kondo (bioRxiv 10.1101/2024.03.27.587111) — missed; the strongest counter-pressure on the claim's
*reasoning*, though not on its verdict.** Abstract-level plus search-summary only (access failure documented in §0).

From the **abstract** (reliable): they expressed "the hyperactive potassium channel mutant kcnk5b W169L or the
dominant-negative connexin mutant Cx43 T154A under a common set of cell-type-specific promoters"; manipulation
"in keratinocytes primarily affected fin size, whereas manipulation in osteoblasts preferentially altered fin-ray
segment length"; and "optogenetic manipulation demonstrated that membrane potential itself can regulate fin size and
fin-ray segment length."

From **search-summary level only, NOT verified against the full text** — I flag this because it is load-bearing and
my read-level for it is weak: indexed snippets indicate the optogenetic actuator was **ChR2, a depolarising tool**,
and that the resulting phenotypic changes were **opposite to those of `kcnk5b` W169L** fish. No hyperpolarising
actuator (ACR/Arch-class) appeared anywhere in my searches.

**If that is right, it matters in two opposite directions, and I will not collapse them.**

*Against the claim's reasoning.* Imposed depolarisation shrinking fins, mirroring a hyperactive-K⁺-channel
enlargement, is the first **causal in vivo** evidence that V_m *sign* governs fin size, and it points the way the
hyperpolarisation model predicts. That puts it in direct tension with the claim's second pillar — the DiSBAC2(3)
depolarising sign in long fins. The two cannot both be straightforwardly true: dye says `alf` long fins are *more
depolarised*, while ChR2 says *imposing* depolarisation makes fins *smaller*. The claim leans on the dye sign as
counter-evidence without knowing that a causal manipulation points the other way. **This is a genuine weakness in
the claim's argument that I did not find by any other route.** It is also, independently, a further reason to
distrust the whole-fin dye average as a V_m proxy (§2).

*For the claim's verdict nonetheless.* Three things keep the verdict standing. (i) The manipulations are in
**keratinocytes / epidermal cells, not fibroblasts** — so this evidence does not establish the "fibroblast
hyperpolarisation" premise the claim names; it relocates the size-controlling cell *away* from fibroblasts.
(ii) ChR2 establishes that *imposing depolarisation* changes size; it neither imposes nor measures
*hyperpolarisation*, so the hyperpolarising limb remains inferred from the mirror-image phenotype, not demonstrated.
(iii) No resting V_m in mV is measured in any fin cell type, which is the KEY's actual quantity, and it remains an
unpublished preprint after ~2.6 years (§0).

**Anyone relying on this verdict should read that preprint's optogenetics section directly.** I could not, my
actuator identification is search-summary level, and I am not treating it as established.

**(d) Taxon check — flying fishes; no counter-example found.** Daane et al. 2021 (full-text) extends the
bioelectric fin-size model across beloniforms. It reports **no membrane potential measurement in any fish fin cell
and no heterologous electrophysiology at all**; "hyperpolarization" does not appear; its bioelectric claims rest on
genetics, qRT-PCR, and *KCNH2* overexpression in fin mesenchyme. The taxon extension adds no V_m data in either
direction, so it neither rescues nor damages the premise.

**(e) Regime distinction the claim glosses in the half it affirms.** The claim lists `cacna1g` LOF as supporting the
Ca²⁺/calcineurin brake without noting that the phenotype is overwhelmingly **regenerative, not developmental**.
Le Bleu et al. 2025 (full-text): homozygous mutants regenerate fins exceeding original length by 24 dpa and
"nearly doubling in length by 46-50 dpa" (P < 0.0001), whereas developmental overgrowth is "modest, with slightly
longer ray segments and otherwise normal morphology". `alf` and `lof`, by contrast, are developmental long-fin
alleles. So the brake and the K⁺-channel phenotypes are partly established in different growth regimes — an
additional, independent reason the coupling is not established, which again the claim does not use.

**(f) Reporting defects in a supporting source, flagged for downstream users.** In Le Bleu et al. 2025, compound
concentrations disagree between figure legends and Methods (amlodipine 500 nM vs 5 µM; PD17132 500 nM vs 2 µM), and
ML218 (T-type) appears in the Methods at 5 µM with no results reported. The in vivo Ca²⁺-blocker result the claim
leans on is cilnidipine, 5–28 dpa, DMSO n = 8 vs cilnidipine n = 7, P = 0.0004. FK506 appears in that paper's
Methods at 500 nM but with no results of its own; the FK506 overgrowth evidence comes from Kujawski et al. 2014
(listing-level here) and from Daane et al. 2018 (full-text: 100 nM, dose-dependent coordinated overgrowth), not from
Le Bleu et al.

---

## 6. Verdict

**SURVIVED.** The claim's verdict — that coupling of the Ca²⁺/calcineurin brake to long-fin K⁺ channels *via
fibroblast hyperpolarisation* is not an established premise — holds, and three of the five lines of attack I ran
returned evidence *for* it that the claim had not collected:

1. The sole hyperpolarisation evidence is heterologous (Perathoner 2014 Fig. 5; Daane 2018 Fig. 3, both Xenopus
   oocytes), and §1–2 show it cannot transfer in principle, because the voltage consequence of a g_K change is set
   by the host cell's conductance background.
2. FK506/VIVIT *decrease* Kcnk5b conductance while `alf` *increases* it, and both enlarge fins — a sign
   contradiction conceded by the primary source (§3).
3. For `lof`/`kcnh2a`, the primary source never asserts hyperpolarisation and expects *depolarising* signals (§5a).
4. No fin-cell resting V_m in mV exists in any cell type, confirmed against a dedicated review that says so in
   its own words (§2).

**But the verdict survives on a materially narrower basis than the claim argues**, and one of its three stated
pillars is now contested. Per §5c, at search-summary read-level, Aramaki & Kondo's optogenetic ChR2 result indicates
that *imposing* depolarisation changes fin size **opposite** to the hyperactive K⁺ channel — causal in vivo evidence
pointing the way the hyperpolarisation model predicts, and in direct tension with the DiSBAC2(3) depolarising sign
the claim relies on as counter-evidence. The verdict holds anyway because that work is in **keratinocytes, not
fibroblasts**, imposes depolarisation rather than hyperpolarisation, measures no resting V_m in mV, and is an
unpublished preprint. Had it hyperpolarised a defined fin cell type and enlarged fins, I would be returning
`weakened` instead.

Corrections the claim should carry: the KEY's "oocyte dVm = toward −90 to −100 mV" is the calculated K⁺ equilibrium
potential, not a measured ΔV_m (§4, Defect 1); the measured oocyte quantity is a ~2× g_K increase, correlated across
oocytes with more negative V_m, worth ≤ ~17 mV of hyperpolarisation in a linear two-conductance model
(my calculation). The two in vivo dye readouts are different appendages, stages and genetic manipulations and are not
independent replications (§4, Defect 2); Jiang 2024's authors retain an upstream hyperpolarising step as a
hypothesis (§4, Defect 2b); the dye sign is further undercut by the ChR2 result (§5c); and the claim's "fibroblast"
cell assignment is correct for `lof`/`kcnh2a` but contested for `alf`/`kcnk5b` (§3).

I did not manufacture a fault in the verdict because I did not find one. The source that could overturn it (§5c) I
could not read at full-text level, and I report what indexed snippets say about it, labelled as such, rather than
either guessing its content or suppressing it because it cuts against the claim.

---

```swarm-challenge
{"claim_id": 264, "outcome": "survived", "reason": "The verdict holds -- no fin-cell resting Vm in mV exists in any cell type, the hyperpolarisation premise rests only on Xenopus oocyte data that cannot transfer since a gK change's voltage effect is set by host conductance background, the lof/kcnh2a primary source never asserts hyperpolarisation and expects depolarising signals, and FK506/VIVIT decrease Kcnk5b conductance while alf increases it yet both enlarge fins (a sign contradiction conceded by Daane 2018) -- but on a narrower basis than argued, since the KEY's '-90 to -100 mV' is the calculated K+ equilibrium potential rather than a measured dVm, and a ChR2 optogenetic result (search-summary level) indicates imposed depolarisation changes fin size opposite to the hyperactive K+ channel, contesting the claim's dye-based depolarising pillar.", "corrected_value": "in vivo fin-cell resting Vm for alf/lof: unknown in mV (confirmed negative across Perathoner 2014, Daane 2018, Stewart 2021, Daane 2021, Jiang 2024, Le Bleu 2025, Silic & Zhang 2023). Oocyte figure corrected: measured effect is ~2x gK; E_K = -100.5 mV calculated (2 mM/110 mM K+, 18 C), which is a thermodynamic ceiling, not a measured dVm; a 2x gK increase yields 9-17 mV of hyperpolarisation in a linear two-conductance model, not ~50 mV.", "depends_on": ["Perathoner 2014 PLoS Genet 10(1):e1004080 Fig. S4C DiSBAC2(3) whole-fin depolarisation in alf, p<0.001, N=21-23 (full-text)", "Perathoner 2014 Fig. 5 Xenopus oocyte ~2x gK increase and -90 to -100 mV identified by the authors as the K+ equilibrium potential (full-text)", "Xenopus oocyte intracellular [K+] ~110 mM and ND96 bath 2 mM KCl at 18 C, used for my E_K calculation", "linear two-conductance model Vm=(gK*EK+gL*EL)/(gK+gL) with EL=0 mV -- my model assumption, not an observation", "Daane 2018 Sci Rep 8:10391 FK506 and VIVIT DECREASE wild-type Kcnk5b conductance in oocytes, I290A lower and FK506-insensitive, and the authors' concession that opposite conductance directions give similar growth outcomes (full-text)", "Daane 2018 absence of any fin membrane-potential measurement (full-text)", "Stewart 2021 Development 148:dev199384 -- kcnh2a acts in intra-ray mesenchyme/fibroblast lineage, no Vm measured, 'hyperpolarization' absent, future work framed as 'putative depolarizing signals' (full-text)", "Jiang 2024 PLoS Biol 22(3):e3002565 -- DiSBAC2(3) depolarisation on kcnk5b-mCherry overexpression in EMBRYONIC PECTORAL FIN BUD 32-56 hpf, with the authors' proposed hyperpolarisation-then-Na+-channel-depolarisation two-step model and no p-values in text (full-text, first 100 kB)", "Le Bleu 2025 Development 152(23):dev204739 -- cacna1g LOF overgrowth is predominantly REGENERATIVE; uses GCaMP6s not any voltage dye; cilnidipine in vivo P=0.0004, n=8 vs 7 (full-text, first 100 kB)", "Daane 2021 Curr Biol flying fishes -- no fin Vm and no heterologous electrophysiology; 'hyperpolarization' absent (full-text)", "Silic & Zhang 2023 Cells 12(8):1148 -- 'direct evidence of bioelectricity in zebrafish fin development is still lacking'; GEVIs applied to zebrafish brain/heart/spinal cord/olfactory but not fin (full-text, first 100 kB)", "NEGATIVE SEARCH SCOPE: Europe PMC and open-web searches for zebrafish fin fibroblast/mesenchyme/blastema resting membrane potential or patch clamp returned no mV value for any fin cell type", "PARTLY-UNREAD RISK: Aramaki & Kondo bioRxiv 10.1101/2024.03.27.587111, unpublished preprint (abstract-level, plus SEARCH-SUMMARY level for the optogenetics and NOT verified against full text; 8 failed bioRxiv fetches HTTP 429/1015, Europe PMC HTTP 500/403, Semantic Scholar and Unpaywall proxy-blocked) -- abstract: kcnk5b W169L in KERATINOCYTES affects fin size and in osteoblasts affects segment length, contradicting Perathoner 2014's mesenchyme assignment, and optogenetic manipulation shows membrane potential regulates fin size; search-summary: the actuator was ChR2 (depolarising) and phenotypes were OPPOSITE to kcnk5b W169L, which contests the claim's DiSBAC2(3) depolarising pillar and is the single input most likely to move this verdict to 'weakened' if confirmed at full-text level", "Kujawski 2014 Dev Cell 28:573-587 FK506 fin overgrowth -- listing-level citation verification only"]}
```
