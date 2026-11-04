# S22-D-D-D: Deepening S22-D-D by attacking its weakest input (the pectoral fold-overgrowth `f`)

**Parent (S22-D-D, dna):** *Deepen S22-D: attack its most sensitive input.*
**What S22-D-D recorded** (branch `claude/s22-d-sensitive-input-pwechp`, commit `4c6dbee3`,
`docs/research/fish/S22-D-deepen.md`): S22-D-D replaced S22-D's assumed wild-type pectoral/SL with a
same-lab figure-read (Daane et al. 2018 Sci Rep Fig 1A), giving `p0` ≈ 0.21 SL (0.17–0.26). That figure-read
rests on an inference about what the dashed line means. S22-D-D used the dominant `kcnk5b^alf/+` allele as a
**proxy** for the double mutant's pectoral fold-overgrowth (`f` ≈ 1.74–2.05×). From these it concluded
(calculated) that the `lat4a^nr21/+; kcnh2a^lof/+` "phenocopy" most likely falls short of flying-fish
pectoral/SL (0.65–0.77) by about 1.5–2.1×. Verdict on S22-D: STRENGTHENS.

I ran no experiment for this note. Every number below is either (a) quoted from a source with its read-level,
or (b) **calculated** by `S22-D-D-deepen_calc.py` (in this directory), and each sentence says which. No
figure was read in this pass. The only figure-read values are S22-D-D's, carried over and labelled as such.

---

## 0. Sources and read-levels

| # | Source | Read-level | What I took from it |
|---|---|---|---|
| P1 | Daane JM et al. (2021) *Modulation of bioelectric cues in the evolution of flying fishes.* Curr Biol 31:5052. doi:10.1016/j.cub.2021.08.054, PMC9172250 | **full-text** (text only, via S22-D-D). Article HTML loaded from pmc.ncbi.nlm.nih.gov in this session. **Fig 4 image and Data S1: could-not-access** (§3a) | Nothing new beyond S22-D-D |
| P1-pre | Daane JM, Blum N, Lanni J, Boldt H, Iovine MK, Higdon CW, Johnson SL, Lovejoy NR, Harris MP. *Novel regulators of growth identified in the evolution of fin proportion in flying fish.* bioRxiv 10.1101/2021.03.05.434157 v1 (2021-03-07, CC BY-NC-ND; bioRxiv API lists `published: NA`) | **full-text** (HTML, sha256 `80f69a8a…54b4`). **Figure images could-not-access** (Cloudflare 1015 on every image request, retried at 60/120/240 s) | Text of the "Sufficiency…" paragraph and the Fig 8 legend. Fig 8B is the same measurement as P1 Fig 4B (pectoral length/SL, Tukey's HSD) |
| S21 | Stewart S, Le Bleu HK, Yette GA, Henner AL, et al. (2021) *longfin causes cis-ectopic expression of the kcnh2a ether-a-go-go K+ channel to autonomously prolong fin outgrowth.* Development 148:dev199384. PMID 34061172, **PMC8217709** | **full-text** (PMC HTML, sha256 `041c662e…e145`). Figures not read | Mechanism and kinetics of `lof^t2/+` overgrowth. No pectoral/SL value |
| IJ00 | Iovine MK, Johnson SL (2000) *Genetic analysis of isometric growth control mechanisms in the zebrafish caudal fin.* Genetics 155:1321. PMID 10880491, PMC1461173 | **abstract** (NCBI efetch returned front matter only; academic.oup.com 403; Europe PMC fullTextXML HTTP 500) | lof = positive allometry; wild-type adult fins isometric; sof fins one-half wild-type length |
| P14 | Perathoner S et al. (2014) PLoS Genet 10:e1004080, PMC3894163 | **full-text** (S3 `.txt`, sha256 `245faa42…a58c`, same file as S22-D-D) | Re-searched for "lof" and "pectoral" |
| D18 | Daane JM et al. (2018) Sci Rep 8:10391, PMC6039437 | Carried over from S22-D-D (full-text + figure images, read there, not here) | `p0` and the alf pectoral ratio, both S22-D-D figure-reads |
| C1–C4 | Flying-fish pectoral/SL, *E. volitans* | Carried over from S22-D-D, **search-summary**, sources disagree (0.65–0.70 / 0.70–0.75 / 0.73–0.77) | Target FF |

Correction to S22-D-D's access log: S22-D-D tried `cell.com/…/S0960-9822(21)01142-8`. Crossref
(`api.crossref.org/works/10.1016/j.cub.2021.08.054`, this session) gives the PII as **S0960982221011908**,
so the right path is `S0960-9822(21)01190-8`. I tried that path. It also returned HTTP 403. The wrong PII did
not cost S22-D-D any data, but the log was wrong.

---

## 1. The input S22-D-D's answer is most sensitive to: shown by recomputation

S22-D-D's conclusion is a shortfall, **S = FF / (p0 · f)**, with baseline S = 1.52–2.13× (calculated). I
doubled and halved each input in turn (calculated, `S22-D-D-deepen_calc.py`):

| Perturbation | Shortfall | Effect on the conclusion |
|---|---|---|
| `p0` ×2 | 0.76–1.06× | **flips** (straddles a match) |
| `p0` ÷2 | 3.05–4.26× | holds, stronger |
| `f` ×2 | 0.76–1.06× | **flips** |
| `f` ÷2 | 3.05–4.26× | holds, stronger |
| FF ×2 | 3.05–4.26× | holds, stronger |
| FF ÷2 | 0.76–1.06× | **flips** |

The formula is a product, so all three inputs carry equal elasticity. Each one flips the conclusion when
moved by a factor of two in the unfavourable direction. Sensitivity alone cannot single out one input.
The tie is broken by **how plausible a factor-of-two error is in each** (calculated break-even values):

- **`p0`** would have to be 0.32–0.44 SL. On S22-D-D's own reading of D18 Fig 1A, that means only 24–33% of
  the fin was resected, against the legend's "~50%" (author's claim). That reading is an inference, but a
  factor of two upward is not plausible here. The *literal* reading of the legend moves `p0` **down**
  (0.104), which strengthens the shortfall.
- **FF** would have to be ≤ 0.36–0.43 SL for a size-matched flying fish. This is plausible: P1 and P1-pre
  both state that flying-fish pectoral length is positively allometric (author's claim). But no number is
  available (Fig 1B and S1 Table could-not-access in both versions).
- **`f`** would have to be ≥ 3.1–3.7×. S22-D-D took `f` from a **different gene** (`kcnk5b^alf/+`), and
  §2 shows the proxy is weaker than S22-D-D treated it.

**Chosen input: `f`, the double-mutant pectoral fold-overgrowth.** It flips the conclusion at ×2, it is a
proxy rather than a measurement, and the real quantity behind it, Rz = `p0`·`f` (double-mutant pectoral/SL),
is plotted in a published figure. A direct read of Rz would replace `p0` and `f` at once.

---

## 2. How well is `f` established?

**Evidence level in S22-D-D: proxy, from a different locus, on a figure-read.** `f` = 1.74× is the ratio of
two S22-D-D figure-reads (D18 Fig 1A, alf/+ vs wt pectoral regrowth targets). 2.05× is an eye-read of P14
Fig 1E (caudal). Neither concerns `kcnh2a^lof`, and neither concerns the double mutant. S22-D-D labelled it a
proxy, correctly. Read in full text this session, the new sources make the proxy weaker in three ways. Each
point below is the authors' claim, and my inference about what it does to `f` follows it:

1. **Different pathway position.** S21 (full-text): "Kcnh2a activity, unlike Kcnk5b/alf (Daane et al., 2018),
   is not downstream of calcineurin." P14 (full-text): lof and rpz "have an increased number of ray segments
   … whereas … alf mutants tend to have elongated segments." *My inference:* the two alleles overgrow fins
   by different mechanisms. Nothing licenses transferring a fold-change from one to the other.
2. **lof overgrowth is a duration effect that grows with size.** S21 (full-text): in `lof^t2/+`
   regenerates "the growth rate declined slower … progressively increasing the fin length difference compared
   with wild-type animals. Wild-type fins largely ceased regenerative outgrowth by 21 dpa, whereas lof^t2 fins
   continued to extend through the 30 dpa period." IJ00 (abstract): "Fins of lof mutants continue to grow
   rapidly even after wild-type fin growth slows, resulting in positive allometric growth." *My inference:*
   `f` for lof/+ is **not a constant**. It depends on the age and SL of the fish measured, and the fish SL in
   P1 Fig 4B is **unknown**. The alf proxy has the same problem (P14 Fig 1D: alf/+ caudal allometric
   coefficient k = 1.88 vs 1.29 wt, author's values via S22-D-D).
3. **The `lat4a^nr21/+` modifier is confirmed to shorten fins.** P1-pre (full-text): "While all fins of kcnh2a
   lof/+ are overgrown and all fins of lat4a nr21/+ are shortened, the … transheterozygous fish showed
   wild-type sized medial fins while the paired fins were overgrown." *My inference:* this cuts against
   `f`. If nr21/+ shortens the pectoral by any factor s < 1, break-even `f` rises: s = 0.9 → 3.5–4.1×,
   s = 0.8 → 3.9–4.6× (calculated, s values illustrative, not measured). The magnitude of s is
   **unknown** (P1-pre Fig 5D could-not-access).

**One check that supports S22-D-D's figure-read method.** The D18 ratio sof/wt = 0.043/0.104 = 0.41 (calculated
from S22-D-D's figure-reads, pectoral). IJ00 (abstract) says sof fins are "one-half the length of wild-type
fins" (caudal, author's claim). These agree to within 20%. This cross-validates the *ratio* method that
produced `f` = 1.74×. It does nothing for the choice of alf as a stand-in for lof.

**Honest grade.** `f` is a cross-locus proxy whose value depends on body size in both loci, applied to a
fish of unknown size. No source I could open gives any pectoral fold-change for `kcnh2a^lof/+`. Points 2 and 3
push `f` in opposite directions, and I cannot net them out.

---

## 3. Going to improve it

### 3a. The real quantity Rz (double-mutant pectoral/SL): still **could-not-access**
Attempts in this session, in addition to S22-D-D's:

| Route | Result |
|---|---|
| bioRxiv full-text HTML, v1 | **200, read** (this is how P1-pre was obtained; S22-D-D got 1015 here) |
| bioRxiv `F8.large.jpg`, `F8.medium.gif`, `F1.large.jpg`, `.full.pdf`, `.supplementary-material` | Cloudflare "error code: 1015" (rate limit), retried after 60, 120 and 240 s, all refused |
| pmc.ncbi.nlm.nih.gov/articles/PMC9172250/ | **200, HTML read**. Figure URL found: `cdn.ncbi.nlm.nih.gov/pmc/blobs/b3db/9172250/187bcb7df244/nihms-1735542-f0004.jpg` |
| cdn.ncbi.nlm.nih.gov (Fig 4 image) | **Session egress policy denial** (proxy 403 on CONNECT). Not routed around |
| pmc.ncbi.nlm.nih.gov `…/bin/NIHMS1735542-supplement-2.xlsx` (Data S1) and `-supplement-1.pdf` | Served a proof-of-work bot gate ("Preparing to download …", `POW_CHALLENGE`). I did not attempt to defeat it |
| europepmc.org figure path | HTTP 403 |
| Europe PMC REST `PMC9172250/supplementaryFiles` | "Article … is not open access" |
| Europe PMC REST `PPR293816/fullTextXML` (preprint) | HTTP 500 |
| ars.els-cdn.com (Cell figure CDN), sciencedirect.com, web.archive.org | Session egress policy denial (proxy 403) |
| cell.com with corrected PII `S0960-9822(21)01190-8` | HTTP 403 |

**Rz remains `unknown`.** I did not estimate it from any image, because I opened none.

### 3b. A measured `f` for `kcnh2a^lof/+`: none found. Scope of the negative search
- S21 full text, string search for "pectoral", "standard length", "fold", "%", "times", "longer", "ratio",
  "normalized", "mm". The only pectoral mentions are qualitative (CRISPR-mosaic asymmetry, Fig 4B). Every
  quantitative length is a caudal regenerate normalised to DMSO-treated controls, never to SL, and the numbers
  are in figures I did not read.
- P1-pre full text: string search for "pectoral", "SL", "standard length", "fold", "%". No numeric
  zebrafish fin length appears in the text.
- P14 full text: "lof" occurs 4 times, all mechanistic. "pectoral" occurs 0 times.
- IJ00: abstract only. The full text (Genetics) was not reachable, and it likely holds caudal lof/+ data.
- Not searched: Goldsmith et al. 2003 Dev Biol 259:303 (lof caudal growth; Elsevier, CDN blocked); ZFIN
  phenotype annotations (TLS failure through the proxy, as in S22-D); Iovine-lab later papers.

### 3c. What would settle it, and the cost (my estimates)
1. **Read P1 Fig 4B (or P1-pre Fig 8B) in an ordinary browser** that passes the PMC proof-of-work or bioRxiv
   Cloudflare check. Download Data S1 (`NIHMS1735542-supplement-2.xlsx`) the same way. This gives Rz
   directly, ideally per fish with SL. Cost: under 1 hour, no money. **This is the single highest-value
   action, and it is blocked only by this session's access, not by the science.**
2. Failing that, ask the corresponding author (M.P. Harris) for the Fig 4B per-fish values with SL. Cost: one email.
3. Failing that, measure it: cross `lat4a^nr21` × `kcnh2a^lof^dt2` (or `lof^t2`), raise to adult, and record
   pectoral length and SL in about 20 fish per genotype (wt, lof/+, nr21/+, double) at a stated SL. Calipers
   or photo plus Fiji. Roughly 4–6 months of fish time and one or two days of measuring. This also gives s
   (the nr21/+ shortening) and `f` at a known body size, which removes the size dependence in §2.2.

---

## 4. Recomputed conclusion

The number for `f` did not improve. No measured `kcnh2a^lof/+` pectoral fold-change was found (scope §3b).
What improved is the **evidence on `f`'s validity**. That changes the conclusion even though the central
number does not move:

| Claim in S22-D-D | Status after this pass |
|---|---|
| Daane et al. never compared zebrafish and flying-fish pectoral/SL numerically | **Stands.** Confirmed in the preprint full text too: the cross-species statement is "the overall fin morphology pattern, and general bauplan, … is remarkably similar", and the only statistics are within-zebrafish Tukey's HSD |
| The double mutant "most likely falls short by ~1.5–2×" | **Falls to undetermined.** It needed `f` ≈ 1.7–2.0×, taken from alf/+. Per S21 and P14 (author's claims) alf and lof overgrow by different mechanisms. Per S21 and IJ00 (author's claims) lof overgrowth keeps increasing with time and size, so a lof/+ `f` ≥ 3.1–3.7× (the break-even, calculated) is not excluded by anything I could read. Per P1-pre (author's claim) nr21/+ shortens fins, which raises the break-even (calculated, §2.3). The proxy does not support "most likely" in either direction |
| A size-matched flying-fish target would be lower than 0.65 | Stands as stated (author's claim of positive allometry, P1 and P1-pre). Magnitude still unknown |

A further point concerns the authors' wording, and it is my inference. P1-pre's Fig 8 title says the genotype is
"sufficient to phenocopy the evolved flying fish fin **allometry**". The legend describes length/SL compared
between genotypes (B–C), with no slope against SL. An allometry is a scaling relationship across body sizes,
and a single-size ratio cannot show one. On the text alone (the figure was not seen), the claim of an
allometry phenocopy is not supported by the measurement the legend describes.

**Verdict on S22-D-D: FALLS**, for its quantitative headline. "Most likely short by 1.5–2×" rested on a proxy
that the primary sources, read in full text this session, show to be mechanistically and allometrically
inapplicable. What survives is the qualitative finding that the "phenocopy" is a verbal, single-size match.
Whether the double mutant reaches flying-fish pectoral/SL is **unknown**, and resolving it needs one
figure (P1 Fig 4B) that this session could not open. This verdict is an inference about the evidence. It is
not an observation that the zebrafish does or does not match.

```swarm-result
{"subproblem": "S22-D-D-D", "evidence": "full-text (Daane 2021 bioRxiv preprint text; Stewart 2021 Development; Perathoner 2014) + abstract (Iovine & Johnson 2000); decisive figure (Daane 2021 Fig 4B / preprint Fig 8B) and Data S1 could-not-access; no figure read in this pass; flying-fish target search-summary carried over", "answer": "S22-D-D's shortfall FF/(p0*f) is equally elastic in all three inputs, and its weakest input, the double-mutant pectoral fold-overgrowth f (~1.74-2.05x, borrowed from kcnk5b alf/+), is shown by full-text primary sources to come from a mechanistically different allele whose overgrowth (like lof's) grows with body size, so the needed lof/+ f of >=3.1-3.7x (calculated) is not excluded and the claim that the Daane et al. phenocopy 'most likely falls short by 1.5-2x' falls to undetermined; the qualitative point that no numerical cross-species comparison was made stands.", "key_number": "break-even pectoral fold-overgrowth f = 3.1-3.7x (calculated; rises to ~3.5-4.6x if lat4a nr21/+ shortens the pectoral by 10-20%, illustrative); measured kcnh2a lof/+ pectoral fold-change: unknown", "verdict": "falls", "depends_on": ["S22-D-D: shortfall = FF/(p0*f), baseline 1.52-2.13x (calculated, branch claude/s22-d-sensitive-input-pwechp)", "S22-D-D figure-read: D18 Fig 1A dashed lines wt 0.104, alf/+ 0.181, sof 0.043 Growth/STL", "S22-D-D inference: p0 ~0.208 SL from D18 Fig 1A at ~50% resection (dashed line = resected part)", "D18 legend: pectoral fins resected to ~50% (author's claim)", "S22-D-D proxy: f ~1.74x (alf/+ pectoral, D18) to ~2.05x (alf/+ caudal, Perathoner 2014 Fig 1E eye-read)", "Stewart 2021 (full-text): Kcnh2a, unlike Kcnk5b/alf, is not downstream of calcineurin", "Stewart 2021 (full-text): lof t2/+ regenerates keep growing through 30 dpa while wild type stops by 21 dpa", "Iovine & Johnson 2000 (abstract): lof fins show positive allometric growth; wild-type adult fins isometric; sof fins one-half wild-type length", "Perathoner 2014 (full-text): lof/rpz add segments, alf elongates segments; alf/+ caudal allometric k 1.88 vs wt 1.29", "Daane 2021 preprint (full-text): all fins of lat4a nr21/+ are shortened; double mutant has wild-type medial fins and overgrown paired fins", "Daane 2021 preprint Fig 8 legend: pectoral length normalized by SL, Tukey's HSD, single-size comparison", "Daane 2021 / preprint: flying-fish pectoral/SL positively allometric (author's claim; values could-not-access)", "Flying-fish target pectoral/SL 0.65-0.77, E. volitans (C1-C3 search-summary, sources disagree)", "Double-mutant pectoral/SL Rz unknown (P1 Fig 4B, preprint Fig 8B, Data S1 could-not-access)", "Fish SL at measurement in P1 Fig 4B unknown", "Magnitude of nr21/+ pectoral shortening unknown"]}
```
