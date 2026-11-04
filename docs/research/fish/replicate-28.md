# Replicate 28: is zebrafish And2 intrinsically disordered?

**Claim being replicated (answer withheld from me):** "and2 is NOT supported as intrinsically disordered"
(context: sequence analysis by the running agent; kcnk5b +0.166 used as the positive control).

**Blindness statement.** I searched the repository (all branches, `git log --all`, and grep for `kcnk5b`, `0.166`, `and2`, `disorder`, `replicate`)
for the earlier working before deriving anything. I found **no** prior working: the only `kcnk5b` hit is an unrelated
problem statement in `findings/gemini-triage-267-problems.json`, and `docs/research/fish/` did not exist. So I could not
see the recorded number. I also could not learn **which metric** produced "+0.166". That is the central limit on this
replicate.

Every number below is **calculated** by me from sequence. None of it is an experimental observation of disorder.

## Inputs

| Input | Value | Source | Read-level |
|---|---|---|---|
| And2 sequence, *Danio rerio* | 508 aa, "Actinodin2 precursor", PE=1 | UniProt A0ACM8QEN9 (identical to A9JRX1), `rest.uniprot.org` FASTA | full-text (sequence record) |
| Kcnk5b sequence, *Danio rerio* | 448 aa | UniProt Q6PFU3 (identical to A0A8M1PBI1) | full-text (sequence record) |
| Kyte–Doolittle hydropathy scale | standard 20 values | memory of Kyte & Doolittle 1982; not re-fetched | could-not-access (not re-checked this session) |
| Uversky charge–hydropathy boundary `<H>b = (<R> + 1.151)/2.785` | | memory of Uversky et al. 2000 (*Proteins*); not re-fetched | could-not-access (not re-checked this session) |
| TOP-IDP scale | 20 values | memory of Campen et al. 2008; not re-fetched | could-not-access (not re-checked this session) |
| Disorder-/order-promoting residue sets (ARGQSPEK / WCFIYVLN) | | memory of the Dunker-lab convention | could-not-access (not re-checked this session) |
| metapredict | v3.1.01, default network | `pip install metapredict` (PyPI) | software, run locally |

Signal peptide: I assumed residues 1–23 (`MARLIKIFATALVIVFMSDFLSA`) as a hydrophobic N-terminal signal, judging only by eye, and report results with and without it.
This is my inference. I did not run SignalP.
Kcnk5b C-terminal tail: I tried several start positions (251, 256, 261, 271, 281, 291) because I don't know the boundary the earlier agent used.
metapredict independently puts the kcnk5b IDR at residues 262–448.

## Arithmetic

Uversky: `<H>` = mean over residues of (KD + 4.5)/9. `<R>` = |n(K+R) − n(D+E)|/N. Distance = `<H>b − <H>`. A positive distance means the protein falls on the disordered side.

**And2, full length (N = 508):** `<H>` = 0.4434. Net charge = −7, so `<R>` = 7/508 = 0.0138.
`<H>b` = (0.0138 + 1.151)/2.785 = 0.4182. **Distance = 0.4182 − 0.4434 = −0.025** (ordered side).
**And2 24–508 (N = 485):** `<H>` = 0.4319. Net = −8, so `<R>` = 0.0165. `<H>b` = 0.4192. **Distance = −0.013.**

Summary of all metrics (calculated by `replicate-28-scripts/*.py`, which read FASTA files from `dl/`):

| Sequence | Uversky dist. | TOP-IDP mean | f(D-prom) − f(O-prom) | metapredict mean | metapredict frac ≥ 0.5 |
|---|---|---|---|---|---|
| kcnk5b full (1–448) | −0.060 | +0.052 | +0.031 | 0.373 | 0.346 |
| kcnk5b 251–448 | +0.057 | +0.192 | +0.308 | 0.769 | 0.854 |
| kcnk5b 262–448 | ~+0.046 | +0.187 | +0.300 | – | – |
| **and2 full (1–508)** | **−0.025** | **+0.161** | **+0.189** | **0.632** | **0.772** |
| **and2 24–508** | **−0.013** | **+0.176** | **+0.204** | **0.647** | **0.746** |

metapredict IDRs for and2 (0-based, half-open): [0,54), [120,197), [235,508). For kcnk5b: [261,448).

**Can I reproduce "kcnk5b +0.166"?** Not uniquely.
- No whole-protein metric above gives +0.166 for kcnk5b.
- The Uversky distance never reaches +0.166 on any kcnk5b C-terminal tail. The best window of at least 30 aa anywhere in the protein is +0.274, at residues 257–286.
- The TOP-IDP mean equals 0.166 for kcnk5b only on the tails 296–448 and 406–448. Both boundaries are arbitrary.

So I can't identify the earlier agent's metric. Treat "+0.166" as being on an unknown scale.

## Result

**My value:** And2's calculated disorder signal depends on the method, and the methods disagree. I am preserving that disagreement here, not averaging it.
- **Charge–hydropathy (Uversky):** distance −0.025 (full length) or −0.013 (mature). This is just on the **ordered** side of the boundary, by a margin that is small next to the ~±0.05 spread the kcnk5b tail boundary alone produces. On this metric alone, "not supported as disordered" holds, but only weakly.
- **TOP-IDP mean:** +0.161 (full) or +0.176 (mature). That is **essentially equal to the kcnk5b positive-control value of +0.166**. On this scale, And2 looks as disorder-prone as the control.
- **Composition (D-promoting − O-promoting):** +0.19 to +0.20, positive.
- **metapredict v3.1:** mean 0.63. 75–77 % of residues score ≥ 0.5, and residue ~236 to the C-terminus is a single long IDR. That is a **disordered** call, though below the kcnk5b tail (0.77 mean).

Uncertainty: the sign on the Uversky metric is within about 0.03 of the boundary. The other three predictors put And2 on the disordered side. All of these are sequence-based predictions.

My inference, not a claim in any source: And2's C-terminal half contains repeated Cys-containing motifs (`C-x-P-x-x-D-P-x-C`, e.g. `CNPYLDPYC`, `CDPTKDPYC`, `CDPRYDPYC`, `CDPEIDYNC`). If these form disulfides in the secreted actinotrichia environment, sequence predictors that ignore disulfides could over-call disorder. I did not test this. No experimental structure or disorder measurement of And2 was searched for or found in this session. Scope of that negative: none attempted beyond UniProt sequence retrieval.

## Comparison with the recorded value

I could not find the recorded value or its metric anywhere in the repository (scope: all local and remote branches, full-text grep).

On the qualitative claim: I **disagree** that the sequence evidence says "not supported as disordered." Only one of four methods I ran (Uversky charge–hydropathy) puts And2 on the ordered side, and only marginally. On TOP-IDP, And2 (+0.161 / +0.176) is indistinguishable from the kcnk5b control (+0.166). If the earlier agent used TOP-IDP-like scoring with a cutoff above 0.166, that cutoff would separate And2 from the control only by thousandths, which is not a meaningful separation.

Numerically I **CANNOT TELL**, because the metric and the recorded number are unknown to me.

```swarm-replication
{"claim_id": 28, "my_value": "and2 Uversky charge-hydropathy distance -0.025 (full) / -0.013 (mature); TOP-IDP mean +0.161 / +0.176 (vs kcnk5b-tail control ~0.17-0.19); metapredict mean 0.63, 77% residues >=0.5 (calculated, not observed)", "agrees": null, "note": "Could not identify the metric behind 'kcnk5b +0.166' or find the recorded value; only Uversky charge-hydropathy marginally supports 'not disordered', while TOP-IDP, composition and metapredict all place And2 at or near the positive-control level, so the qualitative claim looks method-dependent rather than supported."}
```
