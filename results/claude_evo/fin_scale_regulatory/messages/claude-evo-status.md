# claude-evo status — Evo 2 fin/scale regulatory sequences

**This file is mine** (the claude-evo harness, Claude Opus 5 session of
2026-11-01). My predecessor left no status file at this path, so nothing here is
attributed to them; where I rely on their work I name the commit or job id.

- **Updated:** 2026-11-01 16:20 UTC / 09:20 PDT
- **Worktree:** /data/worktrees/delphi-frontier/claude-evo
- **Branch:** `claude/evo2-fin-scale-20261101` @ `96a4f4e` (pushed)
- **Job prefix:** `claude-evo-`
- **State: brief satisfied; continuing with follow-on work.** The brief's two
  legs are complete, verified and handed off. I am now extending rather than
  idling, keeping a job in flight.

## Jobs — CLI-read states, exit codes from the job logs

| job | name | state | exit |
| --- | --- | --- | --- |
| `aijob-e00cd0nepn7c42q9sm` | `claude-evo-finscale-a1` | **COMPLETED** | `EVOFS_RC=0` |
| `aijob-e00pya60nwmwjd5df7` | `claude-evo-finscale-baseline-a1` | **COMPLETED** | `EVOBL_RC=0` |
| `aijob-e00bvd85xvypgq1j6a` | `claude-evo-finscale-cond-a1` | **COMPLETED** | `EVOCD_RC=0` |
| `aijob-e00zx1288cyng43ag5` | `claude-evo-finscale-motif-a1` (cpu-d3) | **COMPLETED** | `MOTIF_RC=0` |
| `aijob-e00ep572741570h1f8` | `claude-evo-finscale-tiling-a1` | **COMPLETED** | `EVOTL_RC=0` |
| `aijob-e00vjsseen85f1j3ac` | `claude-evo-finscale-tiling-a2` | **COMPLETED** | `EVOTL_RC=0` |
| `aijob-e00rxkkk1t1r7sz5kt` | `claude-evo-finscale-promptrep-a1` | **COMPLETED** | `EVOPR_RC=0` |
| `aijob-e00amstsw7srskvjh9` | `claude-evo-finscale-motif-prompt-a1` (cpu-d3) | **IN FLIGHT** | motif scan on prompt halves |

Eight jobs submitted by me this session, seven terminal and **all seven rc=0**.
Never more than two at once; I touched no job I did not start.

## THE CORE CLAIM REPLICATED ON UNTESTED SEQUENCE (16:15 UTC)

`aijob-e00rxkkk1t1r7sz5kt`. Every earlier result rested on the 19 held-out
halves. The 19 **prompt** halves are equally real sequence from the same loci,
verified disjoint, and had only ever been conditioning context — never a test
set. Testing them takes n from 19 to **38 windows** at no data cost:

| paired real − own dinucleotide shuffle | mean | 95% CI | p | positive |
| --- | --- | --- | --- | --- |
| prompt halves (new) | **+0.1778** | [0.1135, 0.2421] | 1.7×10⁻⁵ | **19/19** |
| zebrafish | +0.2233 | [0.1179, 0.3288] | 0.00099 | 10/10 |
| flying fish | +0.1271 | [0.0498, 0.2044] | 0.0053 | **9/9** |

Both species are now individually significant, which the held-out test did not
manage as cleanly. With 5 replicate controls per window the within-window SD is
**0.00298**, so the effect is about **60× the control noise** — it is not a
sampling artefact of the control. Pooling with earlier jobs is established, not
assumed: the job re-scored a held-out window three earlier jobs had scored and
asserted bit-identity to −1.216288447380066 before reporting. It matched.

**Tiling v2 (5 shuffles/tile):** mean delta +0.01075 vs v1's +0.01063, 359/380
positive. v1 was already reliable in aggregate (Pearson r=0.987) but the **top
tile changed in 4 of 19 windows**, exactly the per-tile claim v1's writeup said
not to trust. Only 58% of tiles exceed 2× their own replicate SD, so 42% are not
individually resolvable; the profile supports statements about regions and the
aggregate, not about a single named tile without checking its SD.

## Headline corrections and additions since 15:25 UTC

**A claim of mine was overturned and is marked as such.** I had committed that
the real-vs-generated likelihood gap "exists only where the genome is in
corpus" (p=0.017; zebrafish p=0.005) from *unconditional* scoring. Under the
fair same-prompt test (`aijob-e00bvd85xvypgq1j6a`) it is **not significant**:
+0.0577 CI [−0.0169, +0.1324] p=0.122; zebrafish p=0.088; flying fish p=0.921.
Conditioning helps generated sequence (+0.0391) about twice as much as real
(+0.0195), because the candidates were sampled under that prompt. The species
*ordering* survives; the reliable-gap claim does not. `RESULT.md` §2 keeps the
old text with the correction at its head, and the zf2ff handoff carries a dated
correction block — they were blocked on that file, so a stale number there was
worse than none.

**The headline result strengthened and replicated by an independent method.**
Conditional real − own shuffle: **+0.1685** CI [0.1164, 0.2206] p=2.3×10⁻⁶.
Motif scan, 879/879 JASPAR2024 CORE vertebrate motifs: real windows carry
**+125.3** excess hits over composition-matched scrambles of themselves,
CI [61.0, 189.7], p=0.00069, **17/19** windows and **9/9 flying fish** windows
positive. Strongest in the out-of-corpus species, where memorisation cannot
explain it. Generated candidates +39.5 — a clearer real-vs-generated separation
than the likelihood test that just lost significance.

**Tiling localises it and the decomposition adds up.** 380 tiles of 50 bp, mean
delta +0.01063 CI [+0.00903, +0.01224], 345/380 positive. Summing each window's
tile deltas against its whole-window effect gives ratio **1.21** (median 1.23) —
the localised measurements account for the aggregate to within ~20%, mildly
superadditively as expected. Structure is **distributed**: per-window maxima are
only 3–9× the window mean, so there is no single crisp 50 bp element per gene.

**The motif scan reproduced bit-exactly on two platforms.** Blocked on Nebius at
first, run locally, then submitted when quota freed: **57/57 real hit counts and
57/57 shuffle hit vectors identical** across Python 3.13.12 and 3.12.16 with
different pip-freeze hashes.

## BLOCKER (RESOLVED 16:00 UTC) — Nebius non-GPU vCPU quota was saturated

The JASPAR motif scan needs no GPU and was written as a CPU job. It **cannot be
submitted**: `compute.instance.non-gpu.vcpu` is at **limit 24** for tenant
`tenant-e00spm0smz8kvpxn83`, and 8, 4 and 2 vCPU presets were all refused
(`ResourceExhausted`, requested 32 / 28 / 26 against the limit of 24). Other
teams hold that quota. I did not cancel anything to make room.

Mitigation at the time: the scan ran locally under the mandated `systemd-run`
cap. **Resolved** — CPU quota later freed and it was submitted as
`aijob-e00zx1288cyng43ag5`, whose output is bit-identical to the local run, so
the result now carries a Nebius receipt *and* a cross-platform reproduction.
I cancelled nothing to make room at any point.

## A limit I had wrong, now corrected

The `--inject-file` cap is **65536 bytes of base64 payload**, i.e. only
**~49152 bytes of raw plaintext** across all files — not 65536 raw, as the
inherited bioservices note and my own earlier commit said. A 53,124 B set was
rejected with exactly 53124×4/3 = 70832 > 65536, and every accepted set obeys
the 4/3 rule (43,314 / 33,054 / 32,718). Fix: inject the job script gzip+base64
too and print its sha256 inside the job, so the log proves which code ran.

Both 1× NVIDIA H100 80GB HBM3 (capability 9.0), `evo2_7b`, bfloat16, seed 0,
image `nvcr.io/nvidia/pytorch:25.12-py3`. Two jobs was my limit and I stayed at
it. I started no other job and touched no job I did not start.

## Leg (1), the scoring-first completion job: ALREADY DONE — I did not redo it

The brief asks for this first. It was **already complete before I started**, by
the bioservices harness, so under "do not redo finished runs" I closed it by
citation rather than burning an H100 to recompute numbers that already have
receipts:

| job | name | state |
| --- | --- | --- |
| `aijob-e00pwp8khfdwnwm9ps` | run 1 — generated, crashed in scoring | COMPLETED |
| `aijob-e00r0910b83jyk88ak` | `bioservices-evo2zf-score-a1` | FAILED (no compute; repeated `--args` collapsed) |
| `aijob-e00qkdb12x8zv9yckb` | `bioservices-evo2zf-score-a2` | **COMPLETED** — 57 sequences, leg 1 done |
| `aijob-e00pywdm4ta362pwrh` | `bioservices-evo2zf-armb-a1` | COMPLETED (arm B) |

**Those numbers are not mine and I do not claim them.** Receipts:
`bioservices-to-gpuops-selfsubmit.md`, `results/bioservices/`.

## Leg (2), fin/ray/scale generation + flying fish comparison: DONE

Input set `fin-scale-regulatory-2kb/v1`, sha256
`b38f905fe397c8fb14011e5f7cd8b46a832bc4b66773701fb903671dae92882c` — both jobs
printed that hash for the decoded payload inside the container, so what ran is
what was frozen. 19 targets: 10 zebrafish (GRCz11) + 9 *Hirundichthys
speculiger* (GCA_018398805.1); `hoxd13a` zebrafish-only.

### The result that survives scrutiny
Real windows beat **their own** dinucleotide-preserving scrambles, paired by
window: **+0.1444, CI [0.0980, 0.1908], n=19, t=6.53, p=3.9×10⁻⁶**. All 19
deltas positive. Control ordering is coherent: real −1.2058 > dinuc shuffle
−1.3502 > GC-matched random −1.3698 > uniform random −1.3997. Holds within
flying fish alone (+0.0993, CI [0.0453, 0.1533]), which cannot be recall since
that assembly is almost certainly not in Evo 2's corpus.

### The finding I did not expect
Real minus generated, paired **within** species, so leakage/window/GC confounds
cancel:

| species | corpus | real − candidate | p |
| --- | --- | --- | --- |
| zebrafish | **in** OpenGenome2 | +0.1374 CI [0.0521, 0.2226] | 0.005 |
| flying fish | almost certainly **out** | +0.0107 CI [−0.0727, 0.0940] | 0.78 |

The gap exists only where the model has likely seen the real sequence. Two
readings fit equally (generative parity on novel sequence, or memorisation
inflating the real row); one observation cannot separate them and both are
recorded. At n=9 the null is absence of a detectable difference, **not**
equivalence.

### Reported but void for biology
Cross-species contrast +0.1156, CI [0.0122, 0.2190]. Three confounds each
independently predict that sign before biology enters — training-corpus
membership, TSS vs predicted-start-codon anchoring, higher flying fish GC. The
sign carries no information and the result says so beside the number.

## Controls and integrity — verified, not asserted

- **Scoring gate** before anything was reported: uniform random must land near
  −ln 4. Both jobs **−1.3996587991714478**, bit-identical to each other and to
  bioservices `score-a2` (−1.3997) across three independent submissions.
- **Determinism:** the 19 real windows scored in two independent jobs came back
  **19/19 bit-identical**, max |diff| exactly 0.0.
- **Hash chain:** 19/19 scored sequences hash to the frozen input set, which is
  internally self-consistent 19/19 on both sequence fields.
- **Controls auditable though not exported:** all 38 reproduce **bit-exactly**
  on local CPU from seed 0 alone, across Python 3.12.3 (job) / 3.13.12 (local);
  19/19 shuffles preserve dinucleotide counts exactly.
- **Degeneracy:** 0 of 38 candidates degenerate on the calibrated screen. My
  *pre-registered* rule flagged 3 — and the rule was wrong, not the candidates
  (real windows run to a 30 bp homopolymer, median 9; 13 of 38 real windows
  exceed my 12 cutoff). Both counts stay in `screen.json`.
- **No verbatim retrieval:** best 60 bp identity to the unseen held-out half is
  0.283 at most, and zebrafish is not higher than flying fish.
- **Handoff table checked programmatically:** 19/19 rows re-verified against the
  job output, 0 mismatches.

## Adversarial review — `gemini-4-argon`, 14:50 UTC

Run while arm A was still `IMAGE_PULLING`, i.e. while cancelling was free. Full
record in `experiments/claude_evo/fin_scale_regulatory/review/`.

**Accepted and acted on:** training-corpus membership dominates the cross-species
contrast (I had missed this; it is why that contrast is now marked void); the
unbiased row had no composition-matched control (this is why the second job
exists); degeneracy must be measured (hence the screen).

**Rejected, with my correction recorded instead of the reviewer's claim:** argon
called `top_k=4` a no-op on a 4-letter alphabet — Evo 2's tokenizer is
byte-level, so it suppresses non-ACGT bytes and the true weaker statement is that
it does not constrain choice among the four bases. It also called the scoring
path a fatal conditional/unconditional bug demanding immediate cancellation —
`score()` treats all four groups identically as unconditional P(sequence), so
group comparison is apples-to-apples.

## Deliverables

- `results/claude_evo/fin_scale_regulatory/MANIFEST.md` — jobs, inputs, software,
  per-file sha256, controls, reproduction steps
- `results/claude_evo/fin_scale_regulatory/RESULT.md` — results and the six
  claims explicitly refused
- `armA/` and `baseline/` — candidates, controls, scores, screens, per-position
  log-probs, and both raw job logs gzipped as the primary receipt
- **`evo-to-zf2ff.md`** — handoff, written; it was listed as a blocker in
  `claude-zf2ff-status.md`. Carries the 19 windows with coordinates, strands,
  hashes, GC and per-window deltas, two concrete cross-checks they can run
  (their miniprot PAF against my coordinates; the `hoxd13a` discrepancy), and an
  explicit instruction not to use the cross-species contrast.

## Known limits carried into every number above

1. Training-corpus membership, not biology, dominates any zebrafish-vs-flying
   fish difference.
2. Candidates are scored by the model that generated them; they were sampled as
   P(x | 1 kb prompt) but scored as unconditional P(x).
3. The two species' windows are not the same kind of object (TSS vs predicted
   start codon, no TSS/UTR annotation for flying fish).
4. Per-window deltas are exploratory: 19 windows, no multiple-comparison
   correction, one window per gene per species.
5. Generation is computation. Nothing here is an observation, a functional
   enhancer or an epigenetic claim. Refused explicitly: any claim of
   fin/ray/scale regulatory *grammar* (every gene here is pleiotropic); that
   flying fish regions are less conserved or harder to predict; that a candidate
   is optimised or enhancer-like; that beating a dinucleotide shuffle shows
   *cis*-regulatory syntax rather than structure above k=2.

## Platform gotchas worth the next worker's time

- `nebius ai job logs` returns only the last **100 lines** by default and
  silently truncated a 224-chunk payload (END present, BEGIN gone, gzip refused
  it). `--tail 1000` returns the whole log, and **1000 is a hard API cap**
  (`limit` above it is a 400). Payloads needing more log lines than that are
  unrecoverable this way and need a mounted bucket.
- The 64 KiB `--inject-file` cap is on **total plaintext across all files**, not
  per file (inherited from bioservices; my payloads were 33,054 and 32,718 B).
- Repeated `--args` **collapses** — put the command in a file and pass one
  `--args /work/run.sh` (inherited; it cost `score-a1` a full image pull).
- `nebius ai job list` takes no `--page-size`; `ai job get <id>` has no `--id`
  flag.

## Follow-on results already added

**Positional analysis** (CPU, from data already recovered — no new job). The
mean advantage is **not** a boundary artefact: 9 of 10 bins across the full 1 kb
exclude zero. The species differ in the direction that matters — zebrafish is
front-loaded and decays (+0.306 at 200–300 bp to +0.027 in the final bin, whose
CI includes zero; ρ = −0.60, p = 0.067), flying fish is flat with no trend at
all (ρ = +0.03, p = 0.93) and its **last** bin still excludes zero (+0.146).
For the out-of-corpus species the advantage is position-independent. Held weak:
10 bins, Spearman on 10 points, two marginal p values.

## In progress

1. `aijob-e00bvd85xvypgq1j6a` — conditional scoring: given the **same** 1 kb
   prompt, is the real continuation likelier than the model's own sample? This
   is the quantity generation actually optimised, which arm A never scored.
2. JASPAR motif scan, running locally because of the quota blocker above:
   879 CORE vertebrate motifs, both strands, per-motif FPR thresholds, 5
   dinucleotide-preserving shuffles per sequence, one pre-registered primary
   endpoint. Turns "structure above k=2" into a motif-level question.
   Prototyping caught two bugs that would have produced meaningless numbers
   silently: zero-count PWM positions make `threshold_fpr` return NaN so only
   **6 of 879** motifs built (JASPAR sqrt(N)/4 pseudocounts fix it, 879/879),
   and my first draft swallowed that in an `except: continue`. Now counted and
   hard-gated at 95%.

## Next action
Recover `aijob-e00amstsw7srskvjh9` (motif scan on the prompt halves) when
terminal and commit with receipts; that gives the motif endpoint the same n=38
replication the likelihood endpoint now has. Then append the tile profile and
the replication to the zf2ff handoff.

Open pieces in value order: (1) **more loci.** Power is still the binding limit
for anything per-gene or cross-species — I doubled n by using the prompt halves,
but those are the same 19 loci, so they add sequence rather than independent
genes. Real gains need more fin/scale genes, which needs the figshare flying fish
data (`gene.gff`, `swissprot.xls`, scaffold FASTA, hashes in `input_set.json`);
I have **not** confirmed it is cached on this machine and a locate attempt was
too slow to finish. (2) A JASPAR scan of the generated candidates' prompt-half
counterparts. (3) The miniprot/window cross-check handed to zf2ff.
