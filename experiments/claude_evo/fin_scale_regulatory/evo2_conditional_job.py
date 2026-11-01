"""Conditional scoring: given the SAME prompt, is real continuation likelier?

This closes the one methodological residue left by the gemini-4-argon review.
Arm A generated candidates as P(x | 1 kb prompt) but scored everything as
unconditional P(x). That treats all groups identically, so arm A's group
comparison is sound -- but it means a candidate's reported score is not the
quantity its own sampling optimised, and the fairest real-vs-generated test was
never run.

This job runs it. For each window it feeds prompt+continuation as ONE sequence
and averages log-probs over the continuation positions only, for:

  * the real held-out continuation  -- P(real | its own prompt)
  * each generated candidate        -- P(candidate | the same prompt)
  * a dinucleotide shuffle of the real continuation, same prompt

Every arm therefore shares an identical 1 kb conditioning prefix, and the
comparison is paired within window. This is the quantity generation actually
optimised, so if generated sequence still fails to beat real sequence here, that
cannot be blamed on a mismatch between the sampling and scoring objectives.
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
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-set", required=True)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--model", default="evo2_7b")
    ap.add_argument("--budget-seconds", type=float, default=1800.0)
    args = ap.parse_args()
    started = time.time()
    os.makedirs(args.out_dir, exist_ok=True)
    inputs = json.load(open(args.input_set))
    cands = json.load(open(args.candidates))
    targets = inputs["targets"]
    for t in targets:
        t["key"] = f"{t['species'].split('_')[0][:3]}:{t['symbol']}"
    bykey = {}
    for c in cands:
        bykey.setdefault(c["target"], []).append(c)
    log(f"{len(targets)} targets, {len(cands)} candidates")
    import torch
    from evo2 import Evo2
    torch.manual_seed(SEED)
    rng = random.Random(SEED)
    t0 = time.time()
    model = Evo2(args.model)
    load_seconds = time.time() - t0
    log(f"loaded {args.model} in {load_seconds:.1f}s")

    def _lp(seq: str):
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

    def uncond(seq: str) -> float:
        return float(_lp(seq).mean())

    def cond(prompt: str, cont: str) -> float:
        """Mean log-prob of `cont` given `prompt`, from one forward pass.

        _lp returns one entry per PREDICTED token, so entry j is the log-prob of
        token j+1 of the concatenation. The continuation occupies the final
        len(cont) tokens, hence the final len(cont) entries. Asserted, because an
        off-by-one here would silently mix prompt positions into the mean and
        there would be nothing in the output to reveal it.
        """
        lp = _lp(prompt + cont)
        expected = len(prompt) + len(cont) - 1
        if lp.shape[0] != expected:
            raise RuntimeError(f"logprob length {lp.shape[0]} != expected {expected}")
        return float(lp[-len(cont):].mean())

    # Same gate as every other job in this set.
    iid = "".join(rng.choices("ACGT", k=1000))
    chk = {"iid_random": uncond(iid), "expected_about": -1.3863, "poly_C": uncond("C" * 1000),
           "natural_first_target": uncond(targets[0]["held_out_seq"])}
    chk["scoring_path_sane"] = bool(chk["iid_random"] < -1.30 and chk["natural_first_target"] > chk["iid_random"])
    # A second gate specific to THIS job: conditioning on a real upstream prompt
    # must not make a uniform random continuation look good.
    chk["cond_iid_given_real_prompt"] = cond(targets[0]["prompt_seq"], iid)
    chk["cond_gate_sane"] = bool(chk["cond_iid_given_real_prompt"] < -1.30)
    json.dump(chk, open(os.path.join(args.out_dir, "scoring_self_check.json"), "w"), indent=2)
    log(f"self-check {chk}")
    if not (chk["scoring_path_sane"] and chk["cond_gate_sane"]):
        log("SELF-CHECK FAILED; reporting nothing")
        _emit(args.out_dir)
        return 3

    rows = []

    def dump():
        with open(os.path.join(args.out_dir, "conditional_scores.json"), "w") as fh:
            json.dump(rows, fh, indent=2)

    for t in targets:
        if time.time() - started > args.budget_seconds:
            log("budget spent; stopping cleanly")
            break
        p, h = t["prompt_seq"], t["held_out_seq"]
        rows.append({"kind": "real_held_out", "target": t["key"], "species": t["species"],
                     "symbol": t["symbol"], "sha256": sha(h),
                     "cond_logprob": cond(p, h), "uncond_logprob": uncond(h)})
        sh = dinucleotide_shuffle(h, rng)
        rows.append({"kind": "dinuc_shuffle_of_real", "target": t["key"], "species": t["species"],
                     "symbol": t["symbol"], "sha256": sha(sh),
                     "cond_logprob": cond(p, sh), "uncond_logprob": uncond(sh)})
        for c in bykey.get(t["key"], []):
            rows.append({"kind": "generated", "target": t["key"], "species": t["species"],
                         "symbol": t["symbol"], "sample": c["sample"], "sha256": c["sha256"],
                         "cond_logprob": cond(p, c["sequence"]),
                         "uncond_logprob": uncond(c["sequence"])})
        dump()
        log(f"{t['key']}: conditioned on its own prompt")
    json.dump({
        "job": "fin-scale-evo2-conditional/v1", "model": args.model, "precision": "bfloat16",
        "question": "given the SAME 1 kb prompt, is the real continuation more "
                    "likely than the model's own sample?",
        "outcome_kind": "computed likelihoods under one model; NOT observation, NOT function",
        "scoring": "mean log-prob over continuation positions only, from one "
                   "forward pass over prompt+continuation; unconditional score "
                   "of the same sequence reported alongside for comparability "
                   "with arm A",
        "seed": SEED, "self_check": chk,
        "inputs": {"input_set_id": inputs["input_set_id"], "n_targets": len(targets),
                   "n_candidates": len(cands)},
        "software": _software_versions(), "gpu": _gpu_info(),
        "runtime": {"load_seconds": round(load_seconds, 1),
                    "total_seconds": round(time.time() - started, 1), "n_rows": len(rows)}},
        open(os.path.join(args.out_dir, "manifest.json"), "w"), indent=2)
    log(f"done: {len(rows)} rows")
    _emit(args.out_dir)
    return 0


def _emit(out_dir: str) -> None:
    import base64, gzip, io, tarfile
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        tf.add(out_dir, arcname=".")
    blob = base64.b64encode(gzip.compress(buf.getvalue())).decode()
    print("EVOCD_BEGIN", flush=True)
    for i in range(0, len(blob), 800):
        print("EVOCD_B64 " + blob[i:i + 800], flush=True)
    print("EVOCD_END", flush=True)


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
