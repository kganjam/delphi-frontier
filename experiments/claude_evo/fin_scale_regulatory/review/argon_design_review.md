# Adversarial design review of the fin/scale Evo 2 job

**Reviewer model:** `gemini-4-argon` (Google), HTTP 200, called 2026-11-01
~14:50 UTC / 07:50 PDT, one turn, raw response in `argon_raw_response.json`.
Prompt: the full design plus the three caveats I had already written down, with
an instruction to be adversarial and unencouraging.

Reviewed while `aijob-e00cd0nepn7c42q9sm` was still `IMAGE_PULLING`, i.e. while
cancelling was still free. I did not cancel; the reasoning is below.

## Accepted — and this is the one I had missed

**Training-set membership, not biology, likely dominates the cross-species
comparison.** GRCz11 is in Evo 2's training corpus (OpenGenome2); the flying
fish assembly `GCA_018398805.1` (figshare, 2021) almost certainly is not. A
zebrafish-vs-flyingfish likelihood gap therefore measures in-distribution
memorisation against out-of-distribution generalisation. Critically it
**predicts zebrafish > flyingfish whatever the biology is**, so the sign of that
gap carries no evolutionary information.

Change made: the cross-species comparison is demoted from a headline result to a
reported number with this caveat attached, and the leakage confound is named
first, ahead of the window-definition and GC confounds I already had.

**Fish 5' UTRs often contain large introns**, so windows anchored upstream of a
predicted start codon may sample UTR exons, first introns or intergenic
sequence rather than a core promoter. This sharpens my existing
window-definition caveat rather than adding a new one.

**No composition-matched baseline exists for the real held-out row.** My
controls are shuffles of *candidates*, which answers "is a candidate better than
its own scramble" but leaves the one unbiased row — the real held-out windows —
with nothing to sit against. This is a genuine gap in the design, and it is the
reason for the follow-up job rather than a reason to cancel this one.

**Degeneracy must be measured, not assumed absent.** At temperature 1.0 a
1000 bp autoregressive sample can collapse into homopolymer or microsatellite
repeats, which score near zero log-prob and would beat real sequence as a pure
artefact. Run 1 already hit this ("degenerate repeat; near-zero NLL proves
nothing about quality"). Complexity therefore has to be computed for every
candidate before any likelihood is reported.

## Rejected as stated

**"`top_k = 4` does literally nothing because DNA has 4 letters."** Evo 2's
tokenizer is byte-level with a vocabulary of several hundred tokens, not a
4-token nucleotide vocabulary. `top_k = 4` does real work: it suppresses
non-ACGT bytes. What is true is the weaker claim — it imposes essentially no
constraint *among* the four bases, so it is not a quality filter. Argon assumed
the wrong vocabulary. I am recording the precise version, not the reviewer's.

**"Fatal unconditional-vs-conditional scoring bug; cancel immediately."** Not a
bug here. `score()` is applied identically to all four groups — real held-out,
candidates, dinucleotide shuffles and GC-matched randoms — as unconditional
P(sequence). Group comparison is therefore apples-to-apples. The valid residue
of the point is narrower and I will state it: candidates were *generated* as
P(x | 1 kb prompt) but *scored* as P(x), so a candidate's reported score is not
the quantity its sampling optimised.

## Why I did not cancel

The dominant costs of this job are the image pull and the 7B weight download,
both already in flight; the candidates it produces are what the downstream
zebrafish-to-flying-fish handoff actually needs. None of the accepted points
corrupt the arm A outputs — they change what may be *claimed* from them, and
they add analyses, most of which need no GPU at all. The one GPU-bound addition
(a composition-matched baseline for the real held-out windows, plus per-position
log-probs) has no dependency on this job's outputs and is a clean second job.

## Added to the plan as a result

CPU-only, from the recovered bundle, no GPU:
- gzip compression ratio and distinct-k-mer complexity for k = 3,4,6 on every
  candidate, to expose repetition collapse
- 3-mer and 4-mer Jensen-Shannon divergence, candidate against its own held-out
- best local-alignment identity, candidate against the held-out window, to test
  whether high zebrafish likelihood is retrieval of memorised GRCz11 sequence

GPU, as a second job if arm A completes:
- the 19 real held-out windows scored against their own dinucleotide shuffles
  and GC-matched randoms, giving the unbiased row a baseline
- per-position log-prob curves rather than means alone

## Claims now forbidden in any output of this work

1. No claim that Evo 2 has learned fin, ray or scale regulatory grammar. Every
   gene here (`shha`, `tbx5a`, `runx2b`, `lef1`, …) is a pleiotropic regulator,
   not a fin- or scale-exclusive one.
2. No claim that flyingfish regulatory regions are less conserved, more complex
   or harder to predict than zebrafish. Leakage, GC and annotation basis explain
   the expected direction on their own.
3. No claim that a candidate out-scoring real sequence is optimised or
   enhancer-like. That pattern is the signature of mode-seeking degeneracy.
4. No claim that beating a dinucleotide shuffle demonstrates cis-regulatory
   syntax. It demonstrates higher-order Markov structure above k = 2.
5. No claim that `top_k = 4` constrained base choice.
