# S22-D — Deepening S22: how close is the Daane et al. 2021 "phenocopy", in numbers?

**Parent (S22, dna):** *What exactly did Daane et al. achieve in phenocopying flying-fish fin proportions?*
**Recorded answer:** Daane et al. 2021 crossed `lat4a^nr21/+` with `kcnh2a^lof/+` to phenocopy
flying-fish fin proportions. Length only; fin area never reported; no lift or glide measured.

No experiment was run for this note. Everything below is (a) quoted from a source, with a read-level,
or (b) a calculation, labelled as one in the same sentence.

---

## 0. Sources and read-levels

| # | Source | Read-level | What I took from it |
|---|---|---|---|
| P1 | Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP (2021). *Modulation of bioelectric cues in the evolution of flying fishes.* Curr Biol 31(22):5052–5061.e8. doi:10.1016/j.cub.2021.08.054. PMID 34534441, PMCID PMC9172250 | **full-text** (main text, figure legends, STAR Methods, key resources table, from the NCBI PMC efetch XML of the author manuscript; sha256 of the retrieved XML `a478d83a…5985b7`) | Every claim about what was done and measured |
| P1-fig | Figure 4 panel images (`nihms-1735542-f0004.jpg`) | **could-not-access** (PMC and Europe PMC served a Cloudflare or reCAPTCHA challenge; ZFIN failed with a 503 error and then a TLS error through the proxy) | The numbers plotted in Fig 4B/4C are **unknown** to me |
| P1-S1 | Data S1 (`NIHMS1735542-supplement-2.xlsx`), including Data S1A (museum fin and standard-length measurements) | **could-not-access** (same challenge pages; the Europe PMC supplementaryFiles API answered "not open access") | The flying-fish pectoral/SL values the authors measured are **unknown** to me |
| P2 | Stewart S et al. (2021) *longfin causes cis-ectopic expression of the kcnh2a ether-a-go-go K+ channel…* Development 148:dev199384. PMID 34061172 | **abstract** | Independent confirmation that `longfin^t2` is a regulatory `kcnh2a` allele |
| C1 | FAO species sheet for *Exocoetus volitans* (fao.org ad471e17.pdf) | **search-summary** (fao.org is outside this session's network allowlist) | Pectoral fin about 70–75% of SL |
| C2 | FAO identification key (fao.org ad468eDR.pdf) | **search-summary** | Pectoral fin 65–70% of SL |
| C3 | fishesoftexas.org account of *E. volitans* (compiled from McEachran & Fechhelm, using AI-assisted text extraction according to the summary) | **search-summary** | Pectoral fin 73.2–77.1% of SL |
| C4 | Davenport, *Wing-loading, stability and morphometric relationships in flying fish (Exocoetidae) from the north-eastern Atlantic*, JMBA (cambridge.org) | **search-summary** (cambridge.org is outside the allowlist) | Pectoral length cannot exceed about 78–79% of SL without impairing swimming (*E. obtusirostris*) |

**Disagreement preserved:** C1, C2 and C3 give 65–70%, 70–75% and 73–77% of SL for the same species. I have
not reconciled them, and they likely differ in body size, population, and how "pectoral length" was
measured. C3 passed through an AI extraction step, so it is the weakest of the three.

**Allele naming disagrees between sources.** P1 calls the longfin allele `lof^dt2` (ZIRC ZL86) and
writes the genotype as `kcnh2a^lof/+`. P2 calls it `longfin^t2`. P1's key resources table lists the lat4a
allele as "lat4 nr21 … dmh26" (note `lat4`, not `lat4a`) and a second allele as `lat4a del` (mh152).
The recorded answer's genotype matches P1's Figure 4 legend: "a lat4a nr21/+ × kcnh2a lof/+ cross".

---

## 1. Which input is the answer most sensitive to?

The answer is a scoped "yes": a two-locus zebrafish genotype reproduces flying-fish fin
*proportions*, measured by length only. The quantity carrying the weight is

> **R = (pectoral-fin length / SL) in `lat4a^nr21/+; kcnh2a^lof/+` zebrafish,
> compared against (pectoral-fin length / SL) in flying fishes.**

If R is close to the flying-fish value, "phenocopies proportions" is a quantitative statement. If it is
off by a factor of two, the phenocopy is directional only: longer paired fins, wild-type-size medial
fins, a hypocercal tail. That is a pattern match, not a proportion match.

**Sensitivity, recomputed (calculation only; the grid values are parameters, not observations).** Let
`p0` be wild-type zebrafish pectoral/SL and `FF` be the flying-fish target. The fold overgrowth the double
mutant needs to match the target is `FF / p0`:

| FF (target pectoral/SL) | p0 = 0.10 | p0 = 0.15 | p0 = 0.20 | p0 = 0.25 |
|---|---|---|---|---|
| 0.35 (target halved) | 3.5× | 2.3× | 1.75× | 1.4× |
| 0.65 (C2 low) | 6.5× | 4.3× | 3.25× | 2.6× |
| 0.70 | 7.0× | 4.7× | 3.5× | 2.8× |
| 0.77 (C3 high) | 7.7× | 5.1× | 3.85× | 3.1× |

Halving the target halves the overgrowth required (for example 3.5× becomes 1.75× at `p0 = 0.20`). That
is the difference between "plausibly met by a dominant longfin-type overgrowth" and "far beyond it".
The verdict on "closely phenocopies proportions" therefore depends entirely on two numbers: R itself
and the flying-fish comparator. I could read neither from the primary source.

---

## 2. How well is that input established?

**What the paper measured (author's claim, from P1 full text):**
- Zebrafish: "Pectoral fin length (B) and caudal fin length (C) … length normalized by SL", with Tukey's
  HSD comparisons between genotypes (Fig 4 legend). These are measurements, but only **within
  zebrafish**: the double mutant against its single-mutant and wild-type siblings.
- Flying fishes: "we measured fin length as a function of body size (standard length)" (Fig 1B; Data
  S1A). STAR Methods: "Paired fin and standard fish lengths were measured from beloniform specimens in
  the Harvard Museum of Comparative Zoology". These are measurements of museum specimens.

**What the paper did not do (my inference from the full text I read; scope below):**
- No sentence and no legend in P1 states a **numerical comparison** between zebrafish pectoral/SL
  and flying-fish pectoral/SL. The link is verbal: "remarkably similar to that of flying fishes",
  "closely phenocopies". So **R as a cross-species comparison is an assessment, not a measurement**:
  two separately measured quantities, never set against each other in print.
- The two sides are different kinds of quantity. Fig 1B is a static **allometric trajectory** (pectoral
  length across a range of SL). Fig 4B is a **size-normalized ratio** per genotype. Whether Fig 4B
  covers more than one body size is unknown, because the panel image was not accessible.
- The **medial-fin half** of the claim ("wild-type-sized medial fins") has **no flying-fish
  comparator** in the methods. Methods say paired fins and SL were measured in beloniforms, not
  caudal, dorsal or anal fins. Data S1A itself is unread, so it may contain more than the methods say.
- **Pelvic fins**: the text says "the paired fins are overgrown", but only pectoral length is plotted
  (Fig 4B). The word "pelvic" occurs once in the full text, in the Fig 1A flying-fish legend. No pelvic
  measurement is reported for zebrafish.
- **Hypocercal caudal fin**: shown by an asterisk on an image (Fig 4A). Fig 4C quantifies caudal
  *length* only. Ventral-lobe length and lobe asymmetry are not reported as numbers.
- **Area, lift, glide**: zero hits for "area", "aerodynam", "wing load" and "aspect ratio" in the full text.
  The single hit for "lift" is genomic read "liftover"; the single hit for "surface" is the water surface
  in the eye-evolution passage. This confirms the recorded answer.
- **Sample sizes** for Fig 4B/4C: **unknown** (not stated in the text or legend; possibly in the panel image).

**Scope of these negative searches:** case-insensitive string search over the full text of P1 as
returned by NCBI PMC efetch (main text, figure legends, STAR Methods, key resources table, reference
list), plus close reading of the "Sufficiency of simple genetic changes…" section and the Fig 1, 3
and 4 legends. **Not searched:** the figure images, Supplementary PDF (`supplement-1.pdf`, which holds
Figs S1–S4) and Data S1, because I could not access them.

**Evidence level of the key input:**
- Zebrafish R: measured within species (author's claim), but the value is **unknown to me** (could-not-access).
- Flying-fish comparator: the authors measured it, but the value is unknown to me. The replacement values
  (C1–C3) are **search-summary**, disagree with each other, and none was read in full.
- Cross-species match: **assessment from images and two separately measured datasets** (my inference
  from P1 full text). It has been repeated, in the abstract's word "closely phenocopies", until it reads
  as a measurement. It is not one.

---

## 3. Improving it

**What I recovered.** Flying-fish pectoral/SL from three independent secondary sources (all search-summary):
**about 0.65–0.77 of SL in *E. volitans*** (C2: 0.65–0.70; C1: 0.70–0.75; C3: 0.73–0.77), with a suggested
functional ceiling around 0.78–0.79 in *E. obtusirostris* (C4). This puts a number on the target the
zebrafish would have to reach. Because these sources are search-summaries that disagree, the target is a
range, not a point.

**What I could not recover.** The zebrafish double-mutant pectoral/SL and wild-type `p0`: **unknown**.
Attempts, all failed: PMC article page and `/bin/` figure and supplement URLs (Cloudflare or reCAPTCHA),
Europe PMC fullTextXML (HTTP 500) and supplementaryFiles (not OA), ZFIN figure pages ZDB-FIG-221222-34/35
(503 error, then TLS failure), and the NOAA repository mirror (host not in allowlist). P2 full text
returned only about 3.4 kB, so I read its abstract only. I did not find a published adult wild-type
zebrafish pectoral/SL value in the search I ran (one standard web search). I am not using any remembered
value.

**What would settle it, and what it would cost (my estimates, not quotes):**
1. **Digitize Fig 4B and Fig 1B / Data S1A.** This takes one person less than an hour once the figure and
   the xlsx can be opened, for example from a browser that passes the PMC challenge or through
   institutional access to Cell Press. It turns R into a number and gives the overlap or gap directly.
   This is the cheapest step and should come first.
2. **Re-measure in fish.** `lof^dt2` is listed at ZIRC (ZL86). The availability of `lat4a^nr21` (dmh26)
   outside the Harris lab is **unknown**. A cross of the two, raised to adult (about 3 months), with
   lateral images of about 20 fish per genotype class (4 classes), gives pectoral, pelvic, caudal-lobe
   and medial-fin lengths and **spread-fin areas** (polygon area in Fiji). Cost: mainly husbandry time
   plus one imaging session. No new equipment.
3. **The functional quantity (lift, glide).** Zebrafish are not a glider, so any "lift" number needs a
   scaled physical model or CFD of the fin planform, not a live-animal test. Calculation, with assumed
   body sizes of about 3 cm zebrafish SL and about 25 cm flying-fish SL: under isometry, mass scales as
   L³ and fin area as L², so wing loading scales as L. A zebrafish with *identical* proportions would have
   about **0.12×** the flying fish's wing loading. A proportion match by length therefore does not imply an
   aerodynamic match, and the two body sizes are assumptions, not measurements.

---

## 4. Recomputed conclusion

The recorded answer said length only, no area, no lift or glide. All of it holds on the full text. What
the deeper look adds, from the full text, is narrower:

- The genotype and cross are as recorded (`lat4a^nr21/+ × kcnh2a^lof/+`; P1 itself uses "lat4", "dmh26"
  and "lof dt2" in places).
- Even the *length* phenocopy is shown **qualitatively across species**. The statistics are within
  zebrafish only. No numerical zebrafish-vs-flying-fish comparison of pectoral/SL appears in the text,
  and the flying-fish comparator for medial fins and the hypocercal lobe was not measured according to the
  methods.
- Only pectoral (not pelvic) length and caudal length were quantified in zebrafish. The hypocercal tail
  is shown in an image.
- The target the zebrafish would need to hit is about 0.65–0.77 SL (secondary, disagreeing sources). The
  zebrafish value is **unknown** because the figure could not be accessed, so I cannot say whether the gap
  is small or a factor of 3–7 (the grid above is a calculation over assumed `p0`, not a finding).

**Verdict: STRENGTHENS.** The recorded scope ("length only") is correct, and it is an
*upper bound*. Inside length, the cross-species match is verbal. The decisive number (double-mutant
pectoral/SL against about 0.65–0.77 SL in flying fishes) is unread here and was not computed by the
authors in the text. The next step is to digitize Fig 4B and Data S1A.

```swarm-result
{"subproblem": "S22-D", "evidence": "primary full-text for what was measured; key figure values could-not-access; flying-fish comparator search-summary (sources disagree)", "answer": "Daane et al. measured pectoral and caudal length/SL only within zebrafish genotypes and never numerically compared the lat4a^nr21/+; kcnh2a^lof/+ value to flying-fish pectoral/SL, so the 'phenocopy' is a qualitative cross-species match even for length, and the decisive zebrafish value remains unknown here.", "key_number": "flying-fish target pectoral length about 0.65-0.77 x SL (E. volitans, search-summary, three sources disagree); zebrafish double-mutant pectoral/SL unknown (Fig 4B could-not-access)", "verdict": "strengthens"}
```
