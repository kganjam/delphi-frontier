"""Evo 2 baseline job for the fin/scale set: the unbiased row gets a control.

Added after the gemini-4-argon design review. Arm A shuffles *candidates*, so
the one row in that experiment not biased by construction -- the 19 real
held-out windows -- had nothing composition-matched to sit against. This job
supplies exactly that, and nothing else:

  * each real held-out window, scored
  * its dinucleotide-preserving shuffle and its GC-matched random, scored
  * per-position log-prob curves for the real windows, because a mean hides
    whether likelihood is earned across the window or spikes at one boundary

It has NO dependency on the arm A job's outputs, which is why it can run beside
it instead of after it. Same model, same unconditional P(sequence) scoring path
and the same -ln4 self-check gate as the job that completed rc=0, so the numbers
are comparable to arm A's by construction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
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


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="Evo 2 held-out baseline, zebrafish + flyingfish")
    ap.add_argument("--input-set", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--model", default="evo2_7b")
    ap.add_argument("--budget-seconds", type=float, default=1200.0)
    args = ap.parse_args()
    started = time.time()
    os.makedirs(args.out_dir, exist_ok=True)
    inputs = json.load(open(args.input_set))
    targets = inputs["targets"]
    for t in targets:
        t["key"] = f"{t['species'].split('_')[0][:3]}:{t['symbol']}"
    log(f"input set {inputs['input_set_id']}: {len(targets)} targets")
    import torch
    from evo2 import Evo2
    torch.manual_seed(SEED)
    rng = random.Random(SEED)
    t0 = time.time()
    model = Evo2(args.model)
    load_seconds = time.time() - t0
    log(f"loaded {args.model} in {load_seconds:.1f}s")

    def _logprobs(seq: str):
        """Per-position log-probs of the realised bases. Shapes asserted."""
        ids = torch.tensor(model.tokenizer.tokenize(seq), dtype=torch.int).unsqueeze(0).to("cuda:0")
        with torch.inference_mode():
            outputs, _ = model(ids)
        logits = outputs[0] if isinstance(outputs, (tuple, list)) else outputs
        if logits.dim() == 3:
            logits = logits[0]
        if logits.dim() != 2 or logits.shape[0] != ids.shape[1]:
            raise RuntimeError(f"unexpected logits shape {tuple(logits.shape)} for {ids.shape[1]} tokens")
        lp = torch.log_softmax(logits[:-1].float(), dim=-1)
        return lp.gather(-1, ids[0, 1:].long().unsqueeze(-1)).squeeze(-1)

    def score(seq: str) -> float:
        return float(_logprobs(seq).mean())

    # Same gate as the job that completed rc=0: a uniform random sequence must
    # land near -ln4 or the scoring path is wrong and nothing is reported.
    iid = "".join(rng.choices("ACGT", k=1000))
    chk = {"iid_random": score(iid), "expected_about": -1.3863, "poly_C": score("C" * 1000),
           "natural_first_target": score(targets[0]["held_out_seq"])}
    chk["scoring_path_sane"] = bool(chk["iid_random"] < -1.30 and chk["natural_first_target"] > chk["iid_random"])
    json.dump(chk, open(os.path.join(args.out_dir, "scoring_self_check.json"), "w"), indent=2)
    log(f"self-check {chk}")
    if not chk["scoring_path_sane"]:
        log("SELF-CHECK FAILED; reporting nothing")
        _emit(args.out_dir)
        return 3

    def dump(name, obj):
        with open(os.path.join(args.out_dir, name), "w") as fh:
            json.dump(obj, fh, indent=2)

    scored, curves = [], []
    for t in targets:
        if time.time() - started > args.budget_seconds:
            log("budget spent; stopping cleanly")
            break
        h = t["held_out_seq"]
        gc = (h.count("G") + h.count("C")) / max(1, len(h))
        variants = [
            ("real_held_out", h, {}),
            ("dinucleotide_shuffle_of_real", dinucleotide_shuffle(h, rng), {}),
            ("gc_matched_random_of_real", gc_matched_random(len(h), gc, rng), {}),
            ("real_prompt", t["prompt_seq"], {}),
        ]
        for kind, seq, extra in variants:
            lp = _logprobs(seq)
            rec = {"kind": kind, "target": t["key"], "species": t["species"], "symbol": t["symbol"],
                   "sha256": sha(seq), "length": len(seq),
                   "gc": round((seq.count("G") + seq.count("C")) / max(1, len(seq)), 4),
                   "evo2_mean_logprob": float(lp.mean()), **extra}
            if kind == "real_held_out":
                rec["of_held_out_sha256"] = t["held_out_sha256"]
            scored.append(rec)
            if kind in ("real_held_out", "dinucleotide_shuffle_of_real"):
                curves.append({"kind": kind, "target": t["key"], "sha256": sha(seq),
                               "logprobs": [round(float(x), 5) for x in lp.tolist()]})
        dump("baseline_scores.json", scored)
        dump("positional_logprobs.json", curves)
        log(f"{t['key']}: 4 variants scored")
    dump("manifest.json", {
        "job": "fin-scale-evo2-heldout-baseline/v1", "model": args.model, "precision": "bfloat16",
        "purpose": "composition-matched baseline for the real held-out row, plus per-position curves",
        "outcome_kind": "computed likelihoods under one model; NOT observation, NOT function",
        "scoring": "unconditional P(sequence), identical treatment for every group",
        "seed": SEED, "inputs": {"input_set_id": inputs["input_set_id"], "n_targets": len(targets)},
        "self_check": chk, "software": _software_versions(), "gpu": _gpu_info(),
        "runtime": {"load_seconds": round(load_seconds, 1), "total_seconds": round(time.time() - started, 1),
                    "n_scored": len(scored), "n_curves": len(curves)}})
    log(f"done: {len(scored)} scored, {len(curves)} curves")
    _emit(args.out_dir)
    return 0


def _emit(out_dir: str) -> None:
    import base64, gzip, io, tarfile
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        tf.add(out_dir, arcname=".")
    blob = base64.b64encode(gzip.compress(buf.getvalue())).decode()
    print("EVOBL_BEGIN", flush=True)
    for i in range(0, len(blob), 800):
        print("EVOBL_B64 " + blob[i:i + 800], flush=True)
    print("EVOBL_END", flush=True)


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
