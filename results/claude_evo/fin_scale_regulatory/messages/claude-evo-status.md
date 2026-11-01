# claude-evo status — Evo 2 fin/scale regulatory sequences

**This file is mine** (the claude-evo harness, Claude Opus 5 session of
2026-11-01). My predecessor left no status file at this path, so nothing here is
attributed to them; where I rely on their work I name the commit or job id.

- **Updated:** 2026-11-01 15:25 UTC / 08:25 PDT
- **Worktree:** /data/worktrees/delphi-frontier/claude-evo
- **Branch:** `claude/evo2-fin-scale-20261101` @ `412fdcb` (pushed)
- **Job prefix:** `claude-evo-`
- **State: GOAL MET.** Both my jobs COMPLETED, outputs recovered and verified,
  manifest written, handoff delivered. No blockers.

## Jobs — CLI-read states, exit codes from the job logs

| job | name | state | exit |
| --- | --- | --- | --- |
| `aijob-e00cd0nepn7c42q9sm` | `claude-evo-finscale-a1` | **COMPLETED** | `EVOFS_RC=0` |
| `aijob-e00pya60nwmwjd5df7` | `claude-evo-finscale-baseline-a1` | **COMPLETED** | `EVOBL_RC=0` |

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

## Next action
None required for the brief. If more GPU budget appears, the open pieces are a
JASPAR/FIMO motif scan on these 19 windows against their shuffles (CPU, would
turn "structure above k=2" into motif-level evidence) and the miniprot/window
cross-check I handed to claude-zf2ff.
