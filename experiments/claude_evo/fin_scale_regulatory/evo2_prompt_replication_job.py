"""Independent replication on the PROMPT halves, with replicate controls.

Every result in this work so far rests on the 19 held-out halves. The prompt
halves are equally real genomic sequence from the same 19 loci and have never
been tested against their own scrambles -- the baseline job scored them, but
never generated controls for them. Testing them doubles n for the core claim
from 19 to 38 windows at no data cost, on sequence that has been used only as
conditioning context and never as a test set.

This is a replication, not a reanalysis: the sequences are disjoint from the
held-out halves, so if "real beats its own composition-matched scramble"
reproduces here it reproduces on genuinely new sequence.

Two improvements over the baseline job:
  * N_REPLICATES controls of each kind per window instead of one, so the control
    mean is an average rather than a single draw
  * GC-matched random as well as dinucleotide shuffle, both replicated

Scoring is unconditional: these windows have no upstream context inside the
frozen input set, so there is nothing to condition on without going back to the
genome. That matches how the baseline job scored them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import statistics as st
import subprocess
import sys
import time

def dinucleotide_shuffle(seq: str, rng: random.Random, max_attempts: int = 200) -> str:
    """Shuffle preserving EXACT dinucleotide counts, by Eulerian-walk rejection.

    A mononucleotide shuffle preserves only base composition, which is too weak
    a control for DNA: dinucleotide content, CpG above all, carries much of what
    a motif scan responds to. Preserving it means a surviving difference is not
    merely a difference in dinucleotide composition.

    **A naive version of this is wrong and was used here before being caught.**
    Treating the dinucleotides as edges of a multigraph and walking them in
    random order gets stuck whenever a vertex runs out of outgoing edges early;
    falling back to a random base at that point silently breaks the very
    property the control exists to preserve. Measured on a real 1 kb promoter:
    the naive version deviated by up to 6 of 999 dinucleotides and did not even
    preserve mononucleotide composition.

    The fix is rejection sampling. A random edge ordering is accepted only if
    the walk from ``seq[0]`` consumes every edge, which is exactly the condition
    for an Eulerian path and therefore for identical dinucleotide counts. A walk
    that stalls is discarded, not patched. The result is verified before being
    returned, so the guarantee is checked rather than argued.
    """
    if len(seq) < 2:
        return seq
    for _ in range(max_attempts):
        edges: dict[str, list[str]] = {}
        for a, b in zip(seq, seq[1:]):
            edges.setdefault(a, []).append(b)
        for v in edges.values():
            rng.shuffle(v)
        out, cur = [seq[0]], seq[0]
        for _ in range(len(seq) - 1):
            bucket = edges.get(cur)
            if not bucket:
                break           # stalled: this ordering is not an Eulerian path
            nxt = bucket.pop()
            out.append(nxt)
            cur = nxt
        if len(out) == len(seq):
            candidate = "".join(out)
            if _dinucleotide_counts(candidate) == _dinucleotide_counts(seq):
                return candidate
    raise RuntimeError(
        f"no dinucleotide-preserving shuffle found in {max_attempts} attempts "
        f"for a {len(seq)} bp sequence"
    )


def _dinucleotide_counts(seq: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for i in range(len(seq) - 1):
        k = seq[i : i + 2]
        counts[k] = counts.get(k, 0) + 1
    return counts


def gc_matched_random(length: int, gc: float, rng: random.Random) -> str:
    """Independent bases drawn at a target GC fraction."""
    half_gc, half_at = gc / 2, (1 - gc) / 2
    return "".join(rng.choices("GCAT", weights=[half_gc, half_gc, half_at, half_at], k=length))


def gc_fraction(seq: str) -> float:
    return (seq.count("G") + seq.count("C")) / len(seq) if seq else 0.0


SEED = 0
N_REPLICATES = 5


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-set", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--model", default="evo2_7b")
    ap.add_argument("--replicates", type=int, default=N_REPLICATES)
    ap.add_argument("--budget-seconds", type=float, default=1800.0)
    args = ap.parse_args()
    started = time.time()
    os.makedirs(args.out_dir, exist_ok=True)
    inputs = json.load(open(args.input_set))
    targets = inputs["targets"]
    for t in targets:
        t["key"] = f"{t['species'].split('_')[0][:3]}:{t['symbol']}"
    import torch
    from evo2 import Evo2
    torch.manual_seed(SEED)
    rng = random.Random(SEED)
    t0 = time.time()
    model = Evo2(args.model)
    load_seconds = time.time() - t0
    log(f"loaded {args.model} in {load_seconds:.1f}s")

    def score(seq: str) -> float:
        ids = torch.tensor(model.tokenizer.tokenize(seq), dtype=torch.int).unsqueeze(0).to("cuda:0")
        with torch.inference_mode():
            outputs, _ = model(ids)
        logits = outputs[0] if isinstance(outputs, (tuple, list)) else outputs
        if logits.dim() == 3:
            logits = logits[0]
        if logits.dim() != 2 or logits.shape[0] != ids.shape[1]:
            raise RuntimeError(f"unexpected logits shape {tuple(logits.shape)} for {ids.shape[1]} tokens")
        lp = torch.log_softmax(logits[:-1].float(), dim=-1)
        return float(lp.gather(-1, ids[0, 1:].long().unsqueeze(-1)).squeeze(-1).mean())

    chk = {"iid_random": score("".join(rng.choices("ACGT", k=1000))),
           "expected_about": -1.3863, "poly_C": score("C" * 1000)}
    chk["scoring_path_sane"] = bool(chk["iid_random"] < -1.30)
    # Cross-job anchor: re-score the first HELD-OUT window, which three earlier
    # jobs already scored. It must come back bit-identical, or this job's numbers
    # are not comparable with theirs however sane they look on their own.
    chk["heldout_anchor_target"] = targets[0]["key"]
    chk["heldout_anchor_score"] = score(targets[0]["held_out_seq"])
    chk["heldout_anchor_expected"] = -1.216288447380066
    chk["anchor_matches_earlier_jobs"] = bool(
        chk["heldout_anchor_score"] == chk["heldout_anchor_expected"])
    json.dump(chk, open(os.path.join(args.out_dir, "scoring_self_check.json"), "w"), indent=2)
    log(f"self-check {chk}")
    if not chk["scoring_path_sane"]:
        log("SELF-CHECK FAILED; reporting nothing")
        _emit(args.out_dir)
        return 3
    if not chk["anchor_matches_earlier_jobs"]:
        # Not fatal to this job's internal comparison, but it would invalidate
        # pooling these numbers with the earlier jobs', so it must be loud.
        log("WARNING: held-out anchor does NOT match earlier jobs; "
            "these scores must not be pooled with them")

    rows = []

    def dump():
        with open(os.path.join(args.out_dir, "prompt_scores.json"), "w") as fh:
            json.dump(rows, fh, indent=2)

    for t in targets:
        if time.time() - started > args.budget_seconds:
            log("budget spent; stopping cleanly")
            break
        p = t["prompt_seq"]
        gc = (p.count("G") + p.count("C")) / len(p)
        real = score(p)
        shuf, shuf_sha = [], []
        for _ in range(args.replicates):
            s = dinucleotide_shuffle(p, rng)
            if _dinucleotide_counts(s) != _dinucleotide_counts(p):
                raise RuntimeError("shuffle did not preserve dinucleotide counts")
            shuf.append(score(s))
            shuf_sha.append(sha(s))
        gcr, gcr_sha = [], []
        for _ in range(args.replicates):
            g = gc_matched_random(len(p), gc, rng)
            gcr.append(score(g))
            gcr_sha.append(sha(g))
        rows.append({
            "target": t["key"], "species": t["species"], "symbol": t["symbol"],
            "region_basis": t["window_basis"], "half": "prompt",
            "prompt_sha256": t["prompt_sha256"], "rescored_sha256": sha(p),
            "gc": round(gc, 4), "real_logprob": real,
            "dinuc_shuffle_logprobs": shuf, "dinuc_shuffle_mean": st.mean(shuf),
            "dinuc_shuffle_sd": (st.stdev(shuf) if len(shuf) > 1 else None),
            "dinuc_shuffle_sha256": shuf_sha,
            "gc_random_logprobs": gcr, "gc_random_mean": st.mean(gcr),
            "gc_random_sd": (st.stdev(gcr) if len(gcr) > 1 else None),
            "gc_random_sha256": gcr_sha,
            "delta_vs_dinuc_shuffle": real - st.mean(shuf),
            "delta_vs_gc_random": real - st.mean(gcr)})
        dump()
        log(f"{t['key']} prompt: real {real:.4f} vs shuffle {st.mean(shuf):.4f} "
            f"(delta {real - st.mean(shuf):+.4f})")
    json.dump({
        "job": "fin-scale-evo2-prompt-replication/v1", "model": args.model,
        "precision": "bfloat16", "seed": SEED, "replicates": args.replicates,
        "question": "does 'real beats its own composition-matched scramble' "
                    "replicate on the 19 PROMPT halves, which no test has used?",
        "why": "doubles n for the core claim from 19 to 38 windows on sequence "
               "disjoint from the held-out halves, at no data cost",
        "scoring": "unconditional P(sequence), as the baseline job scored these "
                   "same prompt halves",
        "outcome_kind": "computed likelihoods under one model; NOT observation, NOT function",
        "self_check": chk,
        "inputs": {"input_set_id": inputs["input_set_id"], "n_targets": len(targets)},
        "software": _software_versions(), "gpu": _gpu_info(),
        "runtime": {"load_seconds": round(load_seconds, 1),
                    "total_seconds": round(time.time() - started, 1),
                    "n_windows": len(rows)}},
        open(os.path.join(args.out_dir, "manifest.json"), "w"), indent=2)
    log(f"done: {len(rows)} prompt windows")
    _emit(args.out_dir)
    return 0


def _emit(out_dir: str) -> None:
    import base64, gzip, io, tarfile
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        tf.add(out_dir, arcname=".")
    blob = base64.b64encode(gzip.compress(buf.getvalue())).decode()
    print("EVOPR_BEGIN", flush=True)
    for i in range(0, len(blob), 800):
        print("EVOPR_B64 " + blob[i:i + 800], flush=True)
    print("EVOPR_END", flush=True)


def _software_versions() -> dict:
    out = {"python": sys.version.split()[0]}
    for mod in ("torch", "evo2", "transformer_engine", "flash_attn", "vortex"):
        try:
            out[mod] = getattr(__import__(mod), "__version__", "present")
        except Exception:
            out[mod] = "absent"
    try:
        out["pip_freeze_sha256"] = hashlib.sha256(
            subprocess.run([sys.executable, "-m", "pip", "freeze"],
                           capture_output=True, text=True, timeout=120).stdout.encode()
        ).hexdigest()
    except Exception:
        out["pip_freeze_sha256"] = "unavailable"
    return out


def _gpu_info() -> dict:
    try:
        import torch

        return {"count": torch.cuda.device_count(),
                "name": torch.cuda.get_device_name(0),
                "capability": list(torch.cuda.get_device_capability(0)),
                "total_memory_gb": round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)}
    except Exception as exc:
        return {"error": str(exc)[:200]}



if __name__ == "__main__":
    raise SystemExit(main())
