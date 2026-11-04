# Challenge 147: adversarial review of [S22-D-D-D] (wild zebrafish pectoral-fin length / SL)

**Claim under review** (author: harvest:deepen-s22-d-d-j5x0vq, not me): wild *Danio rerio* pectoral-fin
length is 18–26 % SL, with column means of 19.3–23.8 % (Praveenraj et al. 2017, *Acta Ichthyol. Piscat.*
47:391, Table 1, read at search-summary level). That range falls inside S22-D-D's inferred 0.17–0.26 SL and
rules out the literal 0.104 reading. So the double mutant from Daane et al. 2021 falls short of flying-fish
pectoral/SL by about 1.3–2.3x, "calculated on the alf/+ proxy", and S22-D-D stands.

**Verdict: WEAKENED.** The wild-type number holds up and so does the arithmetic. The phrase "the Daane et al.
2021 double mutant" does not hold up. The genotype behind the shortfall is not the double mutant, and the
real double-mutant value exists in Daane 2021 but was never read.

## Sources and read-levels

| Source | Read-level | What I got |
|---|---|---|
| Praveenraj et al. 2017, *Acta Ichthyol. Piscat.* 47(4):391–396, doi 10.3750/AIEP/02242 | **search-summary**. I tried the full text at krishi.icar.gov.in and aiep.pensoft.net; both are blocked by this session's network policy (could-not-access). | Pectoral-fin length, % SL, in three columns: 19.6–22.5 (20.7 ± 1.3); 18.0–20.7 (19.3 ± 0.9); 18.2–25.8 (23.8 ± 2.7). The first two columns are North and Middle Andaman. The search summary did not label the third column; it is probably the mainland topotypes, but that is unconfirmed. n per column: unknown. |
| Daane et al. 2021, *Curr. Biol.* 31:5052, PMC9172250 | **full-text (text only)**. I read the article body and back matter. Figure images and Data S1 could not be read. | The double mutant is **lat4a^nr21/+ ; kcnh2a^lof/+** (a trans-heterozygote), Fig. 4A. Fig. 4B plots pectoral-fin length "normalized by SL" for that cross. No numbers appear in the text. kcnk5b *alf* is cited only as a separate fin-overgrowth mutant (Perathoner et al. 2014). |
| ZFIN figure page ZDB-FIG-221222-35 | could-not-access (HTTP 503, and the mirror is blocked) | — |

## 1. Arithmetic, redone independently

The claim does not state its flying-fish input or its alf/+ fold-change k. I worked back from its own
endpoints instead. With shortfall = FF / (k · WT), the endpoints 1.3x at WT = 0.26 and 2.3x at WT = 0.17
imply FF/k ≈ 0.338–0.391. I then used Praveenraj's values for WT (this is calculation, not observation):

| WT pectoral/SL | Shortfall (calculated) |
|---|---|
| 0.180 (lowest value in the table) | 1.88–2.17x |
| 0.193 (lowest column mean) | 1.75–2.03x |
| 0.238 (highest column mean) | 1.42–1.64x |
| 0.258 (highest value in the table) | 1.31–1.52x |
| 0.104 (the rejected literal reading) | 3.25–3.76x |

Across the measured range the result is about 1.3–2.2x, and about 1.4–2.0x on the column means. That agrees
with the claimed 1.3–2.3x; the upper end is slightly high only because 0.17 sits below the lowest measured
value. **The arithmetic survives.** The Praveenraj values also agree with what the claim quotes (19.3–23.8
means, 18.0–25.8 range). One oddity: the third column's mean of 23.8 lies near the top of its range
(18.2–25.8). That is possible, but it is a reason to check the table against the PDF before relying on it.

## 2. Proxy: this is where the claim breaks

The claim says "the recomputed shortfall **of the Daane et al. 2021 double mutant**". In Daane 2021 the
double mutant is lat4a^nr21/+ ; kcnh2a^lof/+ (full text, Fig. 4A caption). *alf* is a gain-of-function
allele of **kcnk5b**, which is neither of those two genes. So alf/+ is a different genotype at a different
locus. It is not a reduced version of the double mutant.

- The quantity that matters is the trans-heterozygote's pectoral length / SL, and it exists in Daane 2021
  Fig. 4B. I could not read the figure image or Data S1, so its value is **unknown** here.
- The fold change over wild type, and so the shortfall, scales directly with that unknown value. If the
  trans-het elongates the pectoral fin more than alf/+ does, the shortfall shrinks. If it elongates less, the
  shortfall grows. My inference: the claim's own tag ("calculated on the alf/+ proxy") shows the author knew
  this was a proxy, but the headline sentence still attributes the number to the double mutant.

## 3. Hidden assumption: same way of measuring fin length

The claim "excludes" 0.104 by comparing a wild-fish taxonomic measurement against a value whose origin I
cannot trace; S22-D-D is not in this repository. Taxonomic tables like Praveenraj's usually measure
pectoral-fin length from fin origin to the tip of the longest ray. Daane 2021's text does not say how
zebrafish fin length was measured (full text checked). If 0.104 was read from Daane's own normalized axis
using a different landmark, wild-fish data cannot rule it out. In that case the right comparison would be
mutant/WT within Daane's own axis. Whether this applies is **unknown**: the source of 0.104 was not
available to me. I am raising it as an untested assumption, not as a demonstrated error. A second small
mismatch: Praveenraj measured wild Andaman and mainland fish, while Daane used laboratory lines. My search
found no lab-strain pectoral/SL measurement (scope: two web searches plus the Daane full text).

## 4. Evidence level

The claim's recorded level is "unknown". It should read **search-summary** for the Praveenraj measurement,
which is an observation by Praveenraj et al. read second-hand with uncertain column mapping and unknown n.
It should read **calculated** for the shortfall. The claim does call the shortfall "calculated", which is
honest. "Independent direct measurement" is fair as a description of Praveenraj's work, but no one has
checked it against the table itself.

## 5. Counter-examples searched

I searched for other wild or lab *D. rerio* pectoral/SL data that might contradict Praveenraj. Scope: two
web searches and the Daane 2021 full text. Nothing contradicting turned up, and nothing independently
confirming either. This negative result is limited to that scope.

## Bottom line

The wild-type range (about 0.18–0.26 SL) is corroborated at search-summary level, and the shortfall
arithmetic (about 1.3–2.2x) checks out. Both apply only to the **alf/+ (kcnk5b) proxy**. The shortfall for
the real Daane 2021 double mutant (lat4a^nr21/+ ; kcnh2a^lof/+) remains **unknown** until someone reads
Fig. 4B or Data S1. The exclusion of 0.104 also depends on both sources measuring fin length the same way,
which nobody has checked.

```swarm-challenge
{"claim_id": 147, "outcome": "weakened", "reason": "The wild-type pectoral/SL range (0.18-0.26, Praveenraj 2017, search-summary) and the ~1.3-2.2x calculated shortfall check out, but they describe the kcnk5b alf/+ proxy, not the Daane 2021 double mutant (lat4a nr21/+; kcnh2a lof/+), whose Fig. 4B value was not read, and ruling out 0.104 assumes both sources measured fin length the same way, which is untested.", "corrected_value": "~1.3-2.2x shortfall (calculated, valid only for the alf/+ proxy with WT pectoral/SL 0.180-0.258); double-mutant shortfall unknown", "depends_on": ["Praveenraj et al. 2017 Acta Ichthyol. Piscat. 47:391 Table 1 pectoral-fin %SL (search-summary; columns 19.6-22.5/20.7, 18.0-20.7/19.3, 18.2-25.8/23.8)", "Daane et al. 2021 Curr. Biol. 31:5052 Fig. 4A genotype lat4a nr21/+; kcnh2a lof/+ (full-text, text only)", "S22-D-D implied FF/k = 0.338-0.391, back-calculated from the claim's 1.3-2.3x endpoints over 0.17-0.26 SL", "alf = kcnk5b allele (Perathoner et al. 2014, as cited in Daane 2021)"]}
```
