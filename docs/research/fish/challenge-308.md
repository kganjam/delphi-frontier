# Challenge 308 — adversarial review of claim S42

**Claim under review (verbatim core):** "No peer-reviewed zebrafish experiment manipulates or
measures a membrane-potential change and reports a resulting change in bony fin-ray growth rate
with an effect size … so the project's bioelectric chain must be labelled inferential at the
potential-to-rate junction."

**Recorded evidence level:** literature. **Value:** n/a. **Source:** harvest:zebrafish-fin-ray-growth-vitcr2.

**Verdict: WEAKENED.** The narrow negative in the KEY field (0 peer-reviewed experiments pairing a
membrane-potential manipulation with a bony fin-ray growth rate *in µm/day*) survives my search.
The headline sentence does not: it is stated more broadly than the KEY, and under its own broader
wording at least one peer-reviewed paper — missed by the claim — pairs an in-vivo membrane-potential
measurement in bony-rayed fin tissue with a quantified fin growth-rate effect size. A second missed
peer-reviewed paper is closer on the manipulation axis than any of the three the claim nominates as
"closest". The project's conclusion (label the junction inferential) is unchanged; the supporting
negative and the "closest evidence" list are both wrong as written.

---

## 1. Arithmetic, redone independently

The claim contains one quantitative assertion of its own: "+10% larval finfold length increase under
135 mM KCl" (Liu et al.). There is no derivation to re-do — it is reported as a measured quantity,
not computed from stated inputs, so there is no author working to avoid copying. I could not
reproduce or confirm it: see §6, read-levels. **I neither confirm nor refute the +10% figure; I flag
it as unverified.**

The numbers I did verify are not the claim's own; they are reported values in the sources, and I
copied no author's arithmetic:

- Perathoner et al. 2014 allometric coefficients: wild-type caudal fin k = 1.29; *alf/+* k ≈ 2
  (R² = 0.92 WT, 0.95 *alf/+*). Ratio ≈ 1.55× steeper fin-to-body scaling — **my arithmetic, from
  their two stated coefficients; not a growth rate in µm/day and not presented as one by them.**
- Le Bleu et al. 2025 KCl-responsive cell fractions, which I re-divided from their stated counts:
  DMSO 70/109 = 64.2% (paper states 39% — **discrepancy, see §6**); amlodipine 15/127 = 11.8%
  (states 12%); cilnidipine 4/103 = 3.9% (states 4%); PD17132 29/147 = 19.7% (states 20%). Three of
  four match; the control does not, so either the stated 39% uses a different denominator than the
  70/109 printed beside it, or the extraction I received garbled one of the two. **Unresolved; I did
  not obtain the figure panel.** It does not bear on my verdict either way.

## 2. Is a proxy standing in for the quantity that matters?

Yes — and this is the claim's strongest part, which I confirm rather than break. Across the whole
literature I reached, three distinct proxies substitute for "membrane potential of the fin-ray
growth zone, in mV":

| Proxy actually measured | Stands in for | Where |
|---|---|---|
| K⁺ conductance / reversal potential in *Xenopus* oocytes (two-electrode voltage clamp, shift to −90…−100 mV, ~2× conductance) | fin-cell V_mem | Perathoner 2014 |
| DiSBAC₂(3) relative fluorescence (a dye whose signal rises with depolarisation) | fin-cell V_mem in mV | Perathoner 2014 (juvenile fins); Jiang 2024 (fin buds) |
| GCaMP6s Ca²⁺ response after bath KCl | depolarisation-driven downstream signal | Le Bleu 2025 (isolated cells) |

None is calibrated to millivolts in fin tissue. Perathoner's own authors concede the gap explicitly
in the direction that matters: **their words**, that they "cannot exclude that this, in turn,
triggers a depolarization" in surrounding tissue — i.e. even the sign of the relevant V_mem change
is not pinned down in the growing fin. **My inference:** the proxy problem is worse than the claim
says, because it afflicts the potential side of the junction, not only the rate side, so the chain is
inferential at *both* ends of the potential-to-rate link, not just at the link.

On the growth side the proxy is equally real. "Bony fin-ray growth rate in µm/day" is the quantity
the project needs. What exists instead is: fin length normalised to body length (Le Bleu 2025),
fin-bud area normalised to eye area (Jiang 2024), an allometric coefficient (Perathoner 2014), and
segment length (Aramaki & Kondo; Daane 2018). **The right quantity is not published in any source I
reached.** Le Bleu 2025 comes nearest — they fit outgrowth-rate curves over 31 days and report the
rate peaking at 3–4 dpa with differing decay rates by genotype — but the rates appear only in
figures, with no µm/day values in text.

## 3. The hidden assumption, relaxed

The claim's result rests on an unstated definitional choice: that "measures a membrane-potential
change" requires an instrument reading of potential, and "growth rate" requires a per-unit-time
rate. Both halves are defensible, but the claim's headline sentence does not state either, while its
KEY silently applies the strictest version of both ("in um/day"). The verdict therefore depends on
which sentence a reader uses.

**Relaxed on the potential half** (accept a voltage-sensitive dye read in vivo in the fin as "measures
a membrane-potential change"): Perathoner et al. 2014, *PLoS Genetics* — peer-reviewed — stained
**juvenile fins** with DiSBAC₂(3) and report that wild-type fins show localised hyperpolarisation
while "alf fins in contrast show high levels of depolarization across the fin" (p < 0.001,
N = 21–23). That is a measured membrane-potential difference, in the bony-rayed caudal fin, in the
same paper that quantifies growth.

**Relaxed on the rate half** (accept an allometric growth coefficient as a growth-rate effect size):
the same paper gives k = 1.29 (WT) versus k ≈ 2 (*alf/+*) for caudal fin versus body length. That is
a quantified effect size on a growth measure of the bony fin.

Relax both and the headline sentence is **false**: one peer-reviewed zebrafish paper does measure a
membrane-potential change and report an effect size on bony-fin growth. Relax neither and the KEY
sentence is **true**: the dye is uncalibrated relative fluorescence, not mV, and the allometric
coefficient is dimensionless, not µm/day. Relax exactly one and it is true only on the half left
strict. The claim's result is carried entirely by this choice, and the claim never discloses it.

A second, separable hidden assumption: that a manipulation and a growth measurement in the *same
paper* count as a pairing even when they are in different preparations. Le Bleu et al. 2025 (below)
satisfies "manipulation + rate, same paper" but splits them across in-vitro cells and in-vivo fins.
If that split disqualifies it — as I think it should — then the same standard should be stated, and
the claim does not state it.

## 4. Is the evidence level honest?

Mostly, with two defects.

- **Honest:** the record is marked `literature`, value `n/a`. A negative search result is the right
  shape for this, and the search date is given (2026-11-04). The claim does not dress any number up
  as measured; the one number it asserts (+10%) is attributed to a published paper, not derived.
- **Defect 1 — scope of the negative is not stated.** The HONESTY FLOOR requires the scope of every
  negative search beside the finding. The claim gives a date but no databases, no query strings, no
  language or date bounds, and no statement of what "peer-reviewed" was checked against. A negative
  of this strength ("0 experiments") is unauditable without it. My own scope is in §6, and it is
  narrow enough that I would not myself assert "0" over the whole literature.
- **Defect 2 — the headline and the KEY assert different propositions.** The headline omits "in
  um/day" and so claims much more than was searched for. A reader quoting the headline would carry
  a falsified statement; a reader quoting the KEY would not. That is an evidence-level defect in the
  same family as presenting a derived number as measured: the strength of the stated finding exceeds
  the strength of the test performed.

## 5. Regime / taxon / counter-examples the claim missed

Two peer-reviewed papers, both closer to the junction than at least one of the three the claim
nominates:

**(a) Perathoner et al. 2014, "Bioelectric signaling regulates size in zebrafish fins", *PLoS
Genetics*; peer-reviewed.** Already detailed in §3. Why it matters: the claim's enumerated "closest"
list contains no paper that measures potential *in bony-rayed fin tissue*. It asserts the nearest
potential-measuring work is in larval finfold, "wrong tissue". Perathoner's DiSBAC₂(3) measurement is
in juvenile fins — the right tissue — and sits beside a quantified growth effect size. The claim's
"closest evidence" characterisation is therefore wrong, independent of whether the headline negative
stands. Note also what Perathoner is *not*: they did not manipulate potential in fish, only channel
activity (local overgrowth in ~40% of fish injected with WT or mutant *kcnk5b* and showing DsRed⁺
fin cells; 0/240 for DsRed-only control; no overgrowth with the non-conducting GFGAAA mutant,
n = 32). So this paper strengthens the *measurement* half of the counter-example, not the
manipulation half.

**(b) Le Bleu, Kioussi, Henner, Lewis, Stewart & Stankunas 2025, "Voltage-gated calcium channels
generate blastema Ca²⁺ fluxes restraining zebrafish fin regenerative outgrowth", *Development*
152(23):dev204739, published 1 Dec 2025; peer-reviewed.** They depolarised cells isolated from adult
fin — bony-ray-bearing tissue — with **80 mM KCl** (an explicit membrane-potential manipulation) and
read GCaMP6s responses; and in the same paper they fit **adult regenerative outgrowth rate curves**
over 31 days (n = 14/genotype), with *cacna1g^b1477^* mutant fins "nearly doubling in length by
46–50 dpa", exceeding original length by 24 dpa, P < 0.0001 at 46 dpa; and cilnidipine (5 µM, daily,
5–28 dpa) causing significant fin overgrowth, P = 0.0004, DMSO n = 8 vs drug n = 7.

Why (b) does not refute the KEY, and why it still damages the claim: the KCl depolarisation and the
outgrowth-rate measurement are **different preparations** — dissociated cells versus intact
regenerating fins — linked only by channel pharmacology and genotype. So the potential-to-rate
junction is still not closed in one experiment, and no µm/day figure is given in text. **This is my
inference, not the authors' claim; they do not frame their work as closing that junction.** But the
claim's own list offers as "closest" a 2018 paper that touched neither potential nor an acute
depolarisation, while a 2025 peer-reviewed paper that bath-depolarised adult-fin cells *and* fit
adult outgrowth rates went unmentioned. The claim's survey is incomplete at the exact point it
claims to be exhaustive.

**Also missed, weaker:** Jiang et al. 2024, *PLoS Biology* 22(3):e3002565 (peer-reviewed) — DiSBAC₂(3)
depolarisation measured in pectoral fin bud at 32–56 hpf, Na⁺-channel inhibition (vinpocetine 10 µM,
dibucaine 40 µM, 4 h) blocking both the depolarisation and Kcnk5b-enhanced growth, plus transgenic
*rcan2* overexpression enhancing growth during **adult fin regeneration**. This is a
manipulation-of-potential-plus-growth pairing, but the growth readout is bud area (no bony rays, no
rate), so it does not reach the junction either. The authors themselves caution they "cannot rule out
differences in dye penetration" — a candid limit the claim's framing of dye-based evidence does not
acknowledge. **Disagreement preserved:** Le Bleu 2025 and Jiang 2024 point opposite ways on sign —
Le Bleu's Ca²⁺ influx *restrains* outgrowth (block it, fins overgrow), while Jiang's
depolarisation-dependent Ca²⁺/Rcan2 route *enhances* growth. I do not average these; the junction is
not merely unquantified, its sign is contested across two peer-reviewed papers.

**Taxon regime not checked by me or, apparently, by the claim:** *Xenopus* and axolotl bioelectrics
(the Levin-lab regime) report V_mem manipulations with regenerative outgrowth, but no bony fin rays
exist there, so they cannot satisfy the claim as written. I did not search them, and the claim's
scope is zebrafish-only by construction — worth stating so no reader mistakes the negative for a
statement about vertebrate appendage bioelectrics generally.

**Not independently checkable by me:** the Aramaki & Kondo attribution. Search surfaced a KAKEN grant
summary stating the team put channelrhodopsin into zebrafish epidermal cells and that "artificial
membrane potential manipulation successfully altered the fin morphology", plus JSDB conference
abstracts from 2023 and 2024 on bioelectric control of fin-bone segmentation. I could not open
bioRxiv 10.1101/2024.03.27.587111 itself (§6), so I can neither confirm nor dispute the claim's
description of what it measured. The claim's calling it unrefereed is consistent with it being a
bioRxiv preprint.

## 6. Read-levels and scope of my own negative search

| Source | Read-level |
|---|---|
| Le Bleu et al. 2025, *Development* 152(23):dev204739 (PMC13078715) | full-text (first ~100k chars of ~106k; figures not seen) |
| Perathoner et al. 2014, *PLoS Genetics* (PMC3894163) | full-text (first ~100k of ~118k; figures not seen) |
| Jiang et al. 2024, *PLoS Biology* 22(3):e3002565 (PMC11018282) | full-text (first ~100k of ~260k; figure data files S2/S4/S5 not seen) |
| Liu, Nerli et al. 2026, *Sci Adv* 12(6), DOI 10.1126/sciadv.aec0687 | search-summary only (citation confirmed; KCl concentration and +10% NOT verified) |
| bioRxiv 10.1101/2025.04.03.647033 (preprint of the above) | could-not-access (HTTP 429) |
| Aramaki & Kondo, bioRxiv 10.1101/2024.03.27.587111 | could-not-access (not fetched; known only via search-summary of grant/abstract text) |
| Daane et al. 2018, *Sci Rep* 8:10391 | listing only (title/venue confirmed via search; claim's description of it unverified) |
| Silic & Zhang 2020, *Genetics* (kcnj13/Dhi2059) | search-summary |
| dash.harvard.edu copy of Perathoner; charlieduclut.github.io copy of Liu 2026 | could-not-access — **both hosts fail DNS resolution in this session; they would need allowing in the session's network settings** |

**Scope of my negative:** I did not establish a new "0" of my own. What I did was targeted: five
WebSearch queries (standard and extended modes) on zebrafish fin membrane potential / voltage imaging
/ growth rate / bioelectric, plus the Aramaki-Kondo and Silic-Zhang threads, then full-text reads of
the three peer-reviewed papers above. English only, no systematic PubMed/Web-of-Science query, no
hand-search of *Development*/*Dev Cell*/*eLife* tables of contents, no reference-list chaining. Within
that scope I found **no paper reporting bony fin-ray growth in µm/day against a measured or
manipulated membrane potential**, which is consistent with the claim's KEY. I found two peer-reviewed
papers inconsistent with the claim's broader headline wording and with its "closest evidence" list.
A reader should treat the µm/day negative as *not yet refuted* rather than as *established*.

## 7. What should replace the claim

Keep the project-level conclusion — the potential-to-rate junction is inferential — because nothing I
found closes it, and the sign disagreement in §5 arguably makes it weaker than "inferential"
suggests. Replace the supporting sentence with the two propositions kept separate:

1. *(survives)* No peer-reviewed zebrafish experiment reports bony fin-ray growth as a rate in µm/day
   against a membrane potential that was manipulated or measured in the same preparation. Scope:
   §6.
2. *(corrects the headline)* Peer-reviewed work does pair fin membrane-potential measurement with
   quantified bony-fin growth effect sizes — Perathoner et al. 2014 (*PLoS Genet*), DiSBAC₂(3)
   depolarisation in juvenile *alf* fins, p < 0.001, N = 21–23, with allometric coefficient k ≈ 2
   versus 1.29 wild type — and with adult outgrowth-rate curves under an explicit depolarisation
   manipulation in a sister preparation — Le Bleu et al. 2025 (*Development*), 80 mM KCl on
   adult-fin cells; *cacna1g* mutant fins nearly doubling by 46–50 dpa, P < 0.0001. Neither closes
   the junction; both are closer to it than the three papers the claim lists.

```swarm-challenge
{"claim_id": 308, "outcome": "weakened", "reason": "The narrow µm/day negative in the KEY survives my search, but the headline sentence is stated more broadly than the test performed and is false under its own wording, and the 'closest evidence' list omits two peer-reviewed papers nearer the junction (Perathoner 2014 PLoS Genet: DiSBAC2(3) potential measurement in bony-rayed juvenile fin plus allometric growth effect size k≈2 vs 1.29; Le Bleu 2025 Development: 80 mM KCl depolarisation of adult-fin cells plus fitted adult outgrowth-rate curves), while the negative's search scope is never stated.",
  "corrected_value": "0 peer-reviewed experiments report bony fin-ray growth in um/day against a same-preparation membrane potential (unrefuted, scope-limited); but >=1 peer-reviewed paper pairs an in-vivo fin membrane-potential measurement with a quantified bony-fin growth effect size (Perathoner 2014: allometric k ~2 vs 1.29 WT, dimensionless, not um/day)",
  "depends_on": ["Perathoner et al. 2014 PLoS Genetics 'Bioelectric signaling regulates size in zebrafish fins' (PMC3894163, full-text): DiSBAC2(3) depolarisation across alf juvenile fins p<0.001 N=21-23; allometric coefficient k=1.29 WT vs ~2 in alf/+", "Le Bleu et al. 2025 Development 152(23):dev204739 (PMC13078715, full-text): peer-reviewed; 80 mM KCl depolarisation of isolated adult fin cells; cacna1g mutant fins nearly doubling by 46-50 dpa P<0.0001; cilnidipine 5 uM P=0.0004; outgrowth rates in figures only, no um/day in text", "Jiang et al. 2024 PLoS Biology 22(3):e3002565 (PMC11018282, full-text): DiSBAC2(3) in pectoral fin bud 32-56 hpf; Na+ channel inhibition blocks Kcnk5b-enhanced growth; growth as bud area, no bony rays, no rate; authors' dye-penetration caveat", "Liu, Nerli et al. 2026 Science Advances 12(6) DOI 10.1126/sciadv.aec0687 (search-summary only): citation and larval-finfold tissue confirmed; the claim's 135 mM KCl and +10% length figures NOT verified by me", "Aramaki & Kondo bioRxiv 10.1101/2024.03.27.587111 (could-not-access): claim's description of it neither confirmed nor disputed", "Daane et al. 2018 Sci Rep 8:10391 (listing only): claim's description unverified", "Definitional assumption that 'membrane-potential change' requires an mV-calibrated reading and 'growth rate' requires per-unit-time units - my verdict's split between surviving KEY and falsified headline rests on this distinction", "Scope limit of my own negative search: English-only, 5 web searches plus 3 full-text reads, no systematic PubMed/WoS query, no reference chaining, no ToC hand-search (2026-11-04)"]}
```
