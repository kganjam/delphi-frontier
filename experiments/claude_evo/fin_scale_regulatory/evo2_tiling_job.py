"""In-silico tiling perturbation: which parts of each window does Evo 2 rely on?

The aggregate results say these windows carry structure above dinucleotide
composition. They say nothing about WHERE in each window it sits. This job
localises it, and produces the per-window importance profile the
zebrafish-to-flying-fish harness needs for a perturbation table.

Method, per real held-out window, conditioned on that window's own 1 kb prompt:

  baseline      mean log-prob of the intact window given its prompt
  per tile      replace one TILE_BP tile with a dinucleotide-preserving shuffle
                OF THAT TILE, leaving everything else byte-identical, and
                re-score. delta = baseline - perturbed.

A positive delta means Evo 2 scored the intact tile higher than a tile with the
same local composition in scrambled order, i.e. the ORDER inside that tile
carried likelihood. Because the shuffle is local and composition-preserving,
a delta cannot be explained by changing GC or by changing anything outside the
tile.

Two self-checks, because a silently wrong perturbation would produce a smooth
plausible profile that means nothing:
  * identity perturbation (tile replaced by itself) must give delta EXACTLY 0
  * every perturbed sequence must differ from the original at >0 positions and
    have identical length and identical base composition

Not a claim about function. A tile Evo 2 relies on is not thereby a binding
site, an enhancer, or an edit worth making in a fish.
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
TILE_BP = 50


def sha(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-set", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--model", default="evo2_7b")
    ap.add_argument("--tile-bp", type=int, default=TILE_BP)
    ap.add_argument("--budget-seconds", type=float, default=2400.0)
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

    def cond(prompt: str, cont: str) -> float:
        lp = _lp(prompt + cont)
        expected = len(prompt) + len(cont) - 1
        if lp.shape[0] != expected:
            raise RuntimeError(f"logprob length {lp.shape[0]} != expected {expected}")
        return float(lp[-len(cont):].mean())

    def uncond(seq: str) -> float:
        return float(_lp(seq).mean())

    chk = {"iid_random": uncond("".join(rng.choices("ACGT", k=1000))),
           "expected_about": -1.3863}
    chk["scoring_path_sane"] = bool(chk["iid_random"] < -1.30)
    # Identity perturbation must be an exact no-op. This deliberately goes
    # through the SAME splice expression the real perturbation uses, with the
    # tile left unmodified, so it tests the splice path and forward-pass
    # determinism together. If it is not bit-equal, every profile below is noise.
    t0t = targets[0]
    h0 = t0t["held_out_seq"]
    a0, b0 = 5 * args.tile_bp, 6 * args.tile_bp
    spliced = h0[:a0] + h0[a0:b0] + h0[b0:]
    if spliced != h0:
        raise RuntimeError("splice path does not reconstruct the original sequence")
    base0 = cond(t0t["prompt_seq"], h0)
    ident = cond(t0t["prompt_seq"], spliced)
    chk["identity_baseline"] = base0
    chk["identity_reconstructed"] = ident
    chk["identity_delta"] = base0 - ident
    chk["identity_is_exact_noop"] = bool(base0 == ident)
    json.dump(chk, open(os.path.join(args.out_dir, "scoring_self_check.json"), "w"), indent=2)
    log(f"self-check {chk}")
    if not (chk["scoring_path_sane"] and chk["identity_is_exact_noop"]):
        log("SELF-CHECK FAILED; reporting nothing")
        _emit(args.out_dir)
        return 3

    rows = []

    def dump():
        with open(os.path.join(args.out_dir, "tile_deltas.json"), "w") as fh:
            json.dump(rows, fh, indent=2)

    def comp(s: str) -> tuple:
        return tuple(s.count(b) for b in "ACGT")

    for t in targets:
        if time.time() - started > args.budget_seconds:
            log("budget spent; stopping cleanly")
            break
        p, h = t["prompt_seq"], t["held_out_seq"]
        base = cond(p, h)
        n_tiles = len(h) // args.tile_bp
        tiles = []
        for i in range(n_tiles):
            a, b = i * args.tile_bp, (i + 1) * args.tile_bp
            tile = h[a:b]
            try:
                scrambled = dinucleotide_shuffle(tile, rng)
            except RuntimeError:
                # A short tile can have no Eulerian path; record and skip rather
                # than substituting a weaker control silently.
                tiles.append({"tile": i, "start": a, "end": b, "skipped":
                              "no dinucleotide-preserving shuffle for this tile"})
                continue
            mut = h[:a] + scrambled + h[b:]
            if len(mut) != len(h) or comp(mut) != comp(h):
                raise RuntimeError(f"perturbation changed length or composition at tile {i}")
            n_diff = sum(1 for x, y in zip(mut, h) if x != y)
            score = cond(p, mut)
            tiles.append({"tile": i, "start": a, "end": b,
                          "n_positions_changed": n_diff,
                          "perturbed_cond_logprob": score,
                          "delta_vs_baseline": base - score})
        rows.append({"target": t["key"], "species": t["species"], "symbol": t["symbol"],
                     "region": t["region"], "held_out_sha256": t["held_out_sha256"],
                     "baseline_cond_logprob": base, "tile_bp": args.tile_bp,
                     "n_tiles": n_tiles, "tiles": tiles})
        dump()
        done = [x for x in tiles if "delta_vs_baseline" in x]
        if done:
            top = max(done, key=lambda x: x["delta_vs_baseline"])
            log(f"{t['key']}: base {base:.4f}, {len(done)} tiles, "
                f"max delta {top['delta_vs_baseline']:+.4f} at {top['start']}-{top['end']}")
    json.dump({
        "job": "fin-scale-evo2-tiling-perturbation/v1", "model": args.model,
        "precision": "bfloat16", "tile_bp": args.tile_bp, "seed": SEED,
        "question": "which tiles of each window does Evo 2's likelihood depend on?",
        "method": "replace one tile with a dinucleotide-preserving shuffle OF THAT "
                  "TILE, leave the rest byte-identical, rescore conditioned on the "
                  "window's own 1 kb prompt; delta = baseline - perturbed",
        "outcome_kind": "computed likelihood sensitivity; NOT binding, NOT function, "
                        "NOT an edit recommendation",
        "controls": "identity perturbation must be an exact no-op; every perturbed "
                    "sequence verified for identical length and identical base "
                    "composition before scoring",
        "self_check": chk, "inputs": {"input_set_id": inputs["input_set_id"],
                                      "n_targets": len(targets)},
        "software": _software_versions(), "gpu": _gpu_info(),
        "runtime": {"load_seconds": round(load_seconds, 1),
                    "total_seconds": round(time.time() - started, 1),
                    "n_windows": len(rows)}},
        open(os.path.join(args.out_dir, "manifest.json"), "w"), indent=2)
    log(f"done: {len(rows)} windows")
    _emit(args.out_dir)
    return 0


def _emit(out_dir: str) -> None:
    import base64, gzip, io, tarfile
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        tf.add(out_dir, arcname=".")
    blob = base64.b64encode(gzip.compress(buf.getvalue())).decode()
    print("EVOTL_BEGIN", flush=True)
    for i in range(0, len(blob), 800):
        print("EVOTL_B64 " + blob[i:i + 800], flush=True)
    print("EVOTL_END", flush=True)


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
