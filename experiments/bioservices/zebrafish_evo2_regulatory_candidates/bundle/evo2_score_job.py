"""Evo 2 scoring job — completes the artifact run 1 failed to write.

Run 1 (`aijob-e00pwp8khfdwnwm9ps`) generated 16 candidates and 32 controls and
then crashed in scoring, so `scores.json` was never written. The crash was a
logits-unwrapping bug: Evo 2 returns ``outputs, _`` with the logits at
``outputs[0]``, and treating ``outputs`` as the logits made ``[:-1]`` slice the
batch axis of a ``(1, L, V)`` tensor to length 0.

This job scores the sequences run 1 already produced, so no generation has to be
repeated and the expensive part of the budget is spent on the missing artifact.
Arm B generation runs only if time remains, and is skipped cleanly otherwise.

Self-contained: standard library, torch and evo2 only. Writes after every stage
and emits the bundle as base64 on stdout, because a job can exit non-zero and
still have produced usable science.
"""

from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import io
import json
import os
import random
import sys
import tarfile
import time

SEED = 0
GENERATE_BP = 1000
TEMPERATURE = 1.0
TOP_K = 4
FEWSHOT_K = 4
N_SAMPLES_PER_ARM = 2
N_DESIGN_TARGETS = 8


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def dinucleotide_shuffle(seq: str, rng: random.Random, max_attempts: int = 200) -> str:
    """Exact dinucleotide-preserving shuffle by Eulerian-walk rejection."""
    if len(seq) < 2:
        return seq

    def counts(s):
        d = {}
        for i in range(len(s) - 1):
            d[s[i:i + 2]] = d.get(s[i:i + 2], 0) + 1
        return d

    target = counts(seq)
    for _ in range(max_attempts):
        edges = {}
        for a, b in zip(seq, seq[1:]):
            edges.setdefault(a, []).append(b)
        for v in edges.values():
            rng.shuffle(v)
        out, cur = [seq[0]], seq[0]
        for _ in range(len(seq) - 1):
            bucket = edges.get(cur)
            if not bucket:
                break
            nxt = bucket.pop()
            out.append(nxt)
            cur = nxt
        if len(out) == len(seq):
            cand = "".join(out)
            if counts(cand) == target:
                return cand
    raise RuntimeError(f"no dinucleotide-preserving shuffle in {max_attempts} attempts")


def main() -> int:
    ap = argparse.ArgumentParser(description="Evo 2 scoring of existing zebrafish candidates")
    ap.add_argument("--payload",
                    help="gzip+base64 bundle of input_set, candidates and controls in one file; "
                         "the injected-file size limit is on the TOTAL plaintext, not per file")
    ap.add_argument("--input-set")
    ap.add_argument("--candidates")
    ap.add_argument("--controls")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--model", default="evo2_7b")
    ap.add_argument("--budget-seconds", type=float, default=900.0)
    ap.add_argument("--armb-seconds", type=float, default=0.0,
                    help="seconds to spend generating arm B; 0 skips it")
    args = ap.parse_args()

    started = time.time()
    os.makedirs(args.out_dir, exist_ok=True)
    if args.payload:
        packed = json.loads(gzip.decompress(base64.b64decode(open(args.payload).read())))
        inputs, candidates, controls = (packed["input_set"], packed["candidates"],
                                        packed["controls"])
        log(f"payload unpacked: {len(candidates)} candidates, {len(controls)} controls")
    else:
        if not (args.input_set and args.candidates and args.controls):
            raise SystemExit("give --payload, or all of --input-set --candidates --controls")
        inputs = json.load(open(args.input_set))
        candidates = json.load(open(args.candidates))
        controls = json.load(open(args.controls))
    targets = inputs["targets"]
    design = targets[:N_DESIGN_TARGETS]
    log(f"{len(candidates)} candidates, {len(controls)} controls, {len(targets)} targets")

    import torch
    from evo2 import Evo2

    torch.manual_seed(SEED)
    rng = random.Random(SEED)
    t0 = time.time()
    model = Evo2(args.model)
    load_seconds = time.time() - t0
    log(f"loaded {args.model} in {load_seconds:.1f}s")

    def score(seq: str) -> float:
        """Mean log-probability per base. Shapes asserted: one shot per run."""
        ids = torch.tensor(model.tokenizer.tokenize(seq), dtype=torch.int).unsqueeze(0).to("cuda:0")
        with torch.inference_mode():
            outputs, _ = model(ids)
        logits = outputs[0] if isinstance(outputs, (tuple, list)) else outputs
        if logits.dim() == 3:
            logits = logits[0]
        if logits.dim() != 2:
            raise RuntimeError(f"expected (length, vocab) logits; got {tuple(logits.shape)}")
        if logits.shape[0] != ids.shape[1]:
            raise RuntimeError(
                f"logits length {logits.shape[0]} != {ids.shape[1]} input tokens")
        lp = torch.log_softmax(logits[:-1].float(), dim=-1)
        tgt = ids[0, 1:].long()
        return float(lp.gather(-1, tgt.unsqueeze(-1)).squeeze(-1).mean())

    # --- Self-check before scoring anything that matters -------------------
    # A uniform random sequence must score near -ln(4) = -1.3863 per base. If it
    # does not, the scoring path is wrong and every later number is worthless.
    checks = {}
    iid = "".join(rng.choices("ACGT", k=1000))
    checks["iid_random"] = {"mean_logprob": score(iid), "expected_about": -1.3863}
    homo = "C" * 1000
    checks["poly_C"] = {"mean_logprob": score(homo),
                        "note": "degenerate repeat; near-zero NLL proves nothing about quality"}
    natural = targets[0]["held_out_seq"]
    checks["natural_first_target"] = {"mean_logprob": score(natural),
                                      "symbol": targets[0]["symbol"]}
    ok = (checks["iid_random"]["mean_logprob"] < -1.30
          and checks["natural_first_target"]["mean_logprob"] > checks["iid_random"]["mean_logprob"])
    checks["scoring_path_sane"] = bool(ok)
    json.dump(checks, open(os.path.join(args.out_dir, "scoring_self_check.json"), "w"), indent=2)
    log(f"self-check: iid {checks['iid_random']['mean_logprob']:.4f} (expect ~ -1.3863), "
        f"natural {checks['natural_first_target']['mean_logprob']:.4f}, sane={ok}")
    if not ok:
        log("SELF-CHECK FAILED; refusing to report scores")
        _emit(args.out_dir)
        return 2

    scored = []

    def add(kind, label, seq, extra=None):
        rec = {"kind": kind, "label": label, "sha256": sha(seq), "length": len(seq),
               "gc": round((seq.count("G") + seq.count("C")) / max(1, len(seq)), 4),
               "evo2_mean_logprob": score(seq)}
        if extra:
            rec.update(extra)
        scored.append(rec)
        json.dump(scored, open(os.path.join(args.out_dir, "scores.json"), "w"), indent=2)

    for t in targets:
        add("real_held_out", t["symbol"], t["held_out_seq"],
            {"fully_held_out": t not in design})
    log(f"scored {len(targets)} real held-out halves")
    for c in candidates:
        add("generated", f"{c['arm']}:{c['target']}:{c['sample']}", c["sequence"],
            {"arm": c["arm"], "target": c["target"], "candidate_sha256": c["sha256"]})
    log(f"scored {len(candidates)} candidates")
    for c in controls:
        add(c["kind"], f"{c.get('arm', '')}:{c['target']}", c["sequence"],
            {"arm": c.get("arm"), "target": c["target"], "of": c.get("of")})
    log(f"scored {len(controls)} controls; total {len(scored)}")

    # --- Arm B, only if explicitly budgeted and time remains ---------------
    armb = []
    if args.armb_seconds > 0:
        deadline = time.time() + args.armb_seconds
        for t in design:
            if time.time() > deadline:
                break
            others = [o for o in design if o["symbol"] != t["symbol"]]
            for s in range(N_SAMPLES_PER_ARM):
                if time.time() > deadline:
                    break
                picks = random.Random(f"{SEED}:{t['symbol']}:{s}").sample(others, FEWSHOT_K)
                shots = "".join(p["held_out_seq"] for p in picks)
                out = model.generate(prompt_seqs=[shots + t["prompt_seq"]], n_tokens=GENERATE_BP,
                                     temperature=TEMPERATURE, top_k=TOP_K)
                seq = out.sequences[0].upper()
                rec = {"arm": "B_fewshot_in_context", "target": t["symbol"], "sample": s,
                       "fewshot_examples": [p["symbol"] for p in picks],
                       "sequence": seq, "sha256": sha(seq), "length": len(seq)}
                armb.append(rec)
                json.dump(armb, open(os.path.join(args.out_dir, "candidates_armB.json"), "w"), indent=2)
                log(f"arm B {t['symbol']} s{s}: {len(seq)} bp")
        for c in armb:
            add("generated", f"B_fewshot_in_context:{c['target']}:{c['sample']}", c["sequence"],
                {"arm": "B_fewshot_in_context", "target": c["target"]})
            shuf = dinucleotide_shuffle(c["sequence"], rng)
            add("dinucleotide_shuffle", f"B:{c['target']}", shuf,
                {"arm": "B_fewshot_in_context", "target": c["target"], "of": c["sha256"]})
        log(f"arm B produced {len(armb)} candidates")

    manifest = {
        "job": "zebrafish-evo2-scoring/v1",
        "completes": "aijob-e00pwp8khfdwnwm9ps, whose scoring stage crashed before writing scores.json",
        "outcome_kind": "sequence scores and candidate generation; NOT functional design, no epigenetic claim",
        "model": {"checkpoint": args.model, "precision": "bfloat16",
                  "license": "Apache-2.0 (ArcInstitute/evo2)"},
        "inference": {"generate_bp": GENERATE_BP, "temperature": TEMPERATURE, "top_k": TOP_K,
                      "fewshot_k": FEWSHOT_K, "armb_seconds": args.armb_seconds},
        "seeds": {"torch": SEED, "python_random": SEED},
        "inputs": {"input_set_id": inputs["input_set_id"], "assembly": inputs["assembly"],
                   "n_candidates_in": len(candidates), "n_controls_in": len(controls)},
        "scoring_self_check": checks,
        "counts": {"scored": len(scored), "arm_b_generated": len(armb)},
        "runtime": {"model_load_seconds": round(load_seconds, 1),
                    "total_seconds": round(time.time() - started, 1)},
        "software": _versions(),
        "gpu": _gpu(),
    }
    json.dump(manifest, open(os.path.join(args.out_dir, "manifest.json"), "w"), indent=2)
    log(f"done in {time.time() - started:.1f}s")
    _emit(args.out_dir)
    return 0


def _versions():
    out = {"python": sys.version.split()[0]}
    for m in ("torch", "evo2", "vortex", "flash_attn"):
        try:
            out[m] = getattr(__import__(m), "__version__", "present")
        except Exception:
            out[m] = "absent"
    return out


def _gpu():
    try:
        import torch
        return {"name": torch.cuda.get_device_name(0),
                "count": torch.cuda.device_count(),
                "total_memory_gb": round(torch.cuda.get_device_properties(0).total_memory / 1e9, 1)}
    except Exception as exc:
        return {"error": str(exc)[:200]}


def _emit(out_dir: str) -> None:
    """Emit the output directory as base64 on stdout.

    The job may exit non-zero and still hold usable results, and this container
    has no bucket mounted, so the log is the delivery channel. Each line is
    prefixed so a reader can strip it; run 1 taught that lesson by costing a
    decode attempt.
    """
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        tf.add(out_dir, arcname=".")
    blob = base64.b64encode(gzip.compress(buf.getvalue())).decode()
    print("SCOREJOB_BEGIN", flush=True)
    for i in range(0, len(blob), 800):
        print("SCOREJOB_B64 " + blob[i:i + 800], flush=True)
    print("SCOREJOB_END", flush=True)


if __name__ == "__main__":
    raise SystemExit(main())
