"""JASPAR PWM scan: does the likelihood result survive at motif level?

The Evo 2 result says real windows beat their own dinucleotide-preserving
scrambles. That demonstrates structure above k=2 and NOTHING more specific --
it could be repeat structure or higher-order Markov statistics rather than
transcription-factor binding sites. This job asks the narrower question the
likelihood cannot answer: do these windows carry MORE JASPAR motif hits than
composition-matched scrambles of themselves?

Design decisions that matter:

* The control is the same dinucleotide-preserving Eulerian shuffle used for the
  likelihood work, so mononucleotide AND dinucleotide composition are held
  exactly fixed. CpG content drives PWM hit rates hard; a mononucleotide shuffle
  would have made any result uninterpretable.
* N_SHUFFLES per sequence, averaged, because a single shuffle is a noisy control.
* ONE pooled background for the log-odds, the mononucleotide composition of
  all 19 real held-out windows together, so the 879 PSSMs and their thresholds
  are built once. Per-sequence backgrounds were the first design and are
  unaffordable: Biopython's threshold_fpr costs ~244 s for 879 motifs, so
  rebuilding per sequence would have taken ~3.8 h instead of ~6 min. Fairness
  does not depend on it -- real and its shuffle are scored with identical PSSMs
  and identical thresholds, and the shuffle preserves composition exactly, so
  the paired contrast stays composition-controlled. What this does forfeit is
  cross-sequence hit-count comparison, which is therefore reported as
  descriptive only.
* Zero-count PWM positions give -inf log-odds and make threshold_fpr return
  NaN. JASPAR's own sqrt(N)/4 pseudocounts fix it. Without them only 6 of 879
  motifs built, and an `except: continue` would have hidden that and silently
  scanned with 0.7% of the motif set.
* ONE pre-registered primary endpoint: total hits across all motifs, real vs
  its own mean shuffle, paired across the 19 windows. Per-motif results are
  reported descriptively with Holm correction and are explicitly secondary, to
  avoid fishing across ~800 motifs for a story.
* Threshold is a per-motif false-positive rate, not a fraction of max score, so
  the hit rate is comparable between motifs of different lengths and
  information content.
"""
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import os
import random
import subprocess
import sys
import time

SEED = 0
N_SHUFFLES = 5
FPR = 1e-4


def dinucleotide_shuffle(seq: str, rng: random.Random, max_attempts: int = 200) -> str:
    """Eulerian-walk rejection sampling; exact dinucleotide counts or raise.

    Same algorithm and same guarantee as the likelihood jobs: a walk that stalls
    is discarded, never patched, and the result is verified before return.
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
                break
            nxt = bucket.pop()
            out.append(nxt)
            cur = nxt
        if len(out) == len(seq):
            cand = "".join(out)
            if _dinuc(cand) == _dinuc(seq):
                return cand
    raise RuntimeError(f"no dinucleotide-preserving shuffle in {max_attempts} attempts")


def _dinuc(seq: str) -> dict[str, int]:
    c: dict[str, int] = {}
    for i in range(len(seq) - 1):
        c[seq[i:i + 2]] = c.get(seq[i:i + 2], 0) + 1
    return c


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-set", required=True)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--budget-seconds", type=float, default=2400.0)
    ap.add_argument("--collection", default="CORE")
    ap.add_argument("--tax-group", default="vertebrates")
    args = ap.parse_args()
    started = time.time()
    os.makedirs(args.out_dir, exist_ok=True)

    import numpy as np
    from Bio.Seq import Seq
    from Bio import motifs as biomotifs
    from pyjaspar import jaspardb

    inputs = json.load(open(args.input_set))
    cands = json.load(open(args.candidates))
    log(f"input set {inputs['input_set_id']}, {len(inputs['targets'])} targets, {len(cands)} candidates")

    jdb = jaspardb(release="JASPAR2024")
    motifs = jdb.fetch_motifs(collection=args.collection, tax_group=[args.tax_group])
    log(f"JASPAR2024 {args.collection}/{args.tax_group}: {len(motifs)} motifs")

    rng = random.Random(SEED)

    def bg_of(seq: str) -> dict[str, float]:
        n = len(seq)
        d = {b: seq.count(b) / n for b in "ACGT"}
        # guard against a zero that would make the log-odds infinite
        for b in "ACGT":
            d[b] = max(d[b], 1e-6)
        s = sum(d.values())
        return {b: v / s for b, v in d.items()}

    # PSSMs and thresholds depend on the background, and all our sequences share
    # one background per window-family, so cache per rounded background.
    pooled = "".join(t["held_out_seq"] for t in inputs["targets"])
    BG = bg_of(pooled)
    log(f"pooled background over {len(inputs['targets'])} real windows: "
        + ", ".join(f"{b}={BG[b]:.4f}" for b in "ACGT"))

    from Bio.motifs.jaspar import calculate_pseudocounts
    t0 = time.time()
    BUILT = []
    failures: dict[str, int] = {}
    for m in motifs:
        try:
            m.pseudocounts = calculate_pseudocounts(m)   # JASPAR sqrt(N)/4
            m.background = BG
            pssm = m.pssm
            thr = pssm.distribution(background=BG, precision=10 ** 3).threshold_fpr(FPR)
            if not np.isfinite(thr):
                raise ValueError("non-finite threshold")
            BUILT.append((m.matrix_id, m.name, pssm, pssm.reverse_complement(), float(thr)))
        except Exception as exc:
            failures[f"{type(exc).__name__}: {str(exc)[:60]}"] = \
                failures.get(f"{type(exc).__name__}: {str(exc)[:60]}", 0) + 1
    log(f"built {len(BUILT)}/{len(motifs)} PSSM+threshold in {time.time() - t0:.1f}s")
    if failures:
        log(f"build failures: {failures}")
    # Hard gate. Scanning with a silently decimated motif set would produce
    # plausible hit counts that mean nothing, which is the failure mode that
    # cost this job its first prototype (6 of 879 built, no error raised).
    if len(BUILT) < 0.95 * len(motifs):
        log(f"ABORT: only {len(BUILT)} of {len(motifs)} motifs usable")
        json.dump({"error": "motif build gate failed", "built": len(BUILT),
                   "total": len(motifs), "failures": failures},
                  open(os.path.join(args.out_dir, "ERROR.json"), "w"), indent=2)
        _emit(args.out_dir)
        return 4

    def hits(seq: str) -> tuple[int, dict[str, int]]:
        """Hit counts on BOTH strands at each motif's FPR threshold."""
        s = Seq(seq)
        total = 0
        per: dict[str, int] = {}
        for mid, name, pssm, rcpssm, thr in BUILT:
            fwd = np.asarray(pssm.calculate(s))
            rev = np.asarray(rcpssm.calculate(s))
            n = int((fwd >= thr).sum() + (rev >= thr).sum())
            if n:
                per[mid] = n
            total += n
        return total, per

    results = []

    def do(group: str, label: str, species: str, symbol: str, seq: str, sha: str):
        real_total, real_per = hits(seq)
        sh_totals, sh_pers = [], []
        for _ in range(N_SHUFFLES):
            sh = dinucleotide_shuffle(seq, rng)
            t, p = hits(sh)
            sh_totals.append(t)
            sh_pers.append(p)
        rec = {"group": group, "label": label, "species": species, "symbol": symbol,
               "sha256": sha, "length": len(seq),
               "gc": round((seq.count("G") + seq.count("C")) / len(seq), 4),
               "hits": real_total,
               "shuffle_hits": sh_totals,
               "shuffle_mean": round(sum(sh_totals) / len(sh_totals), 3),
               "per_motif": real_per,
               "per_motif_shuffle_mean": {k: round(sum(d.get(k, 0) for d in sh_pers) / len(sh_pers), 3)
                                          for k in set().union(*[set(d) for d in sh_pers]) if sh_pers}}
        results.append(rec)
        with open(os.path.join(args.out_dir, "motif_hits.json"), "w") as fh:
            json.dump(results, fh, indent=2)
        log(f"{group} {label}: real {real_total} vs shuffle mean {rec['shuffle_mean']}")

    for t in inputs["targets"]:
        if time.time() - started > args.budget_seconds:
            log("budget spent; stopping cleanly")
            break
        key = f"{t['species'].split('_')[0][:3]}:{t['symbol']}"
        do("real_held_out", key, t["species"], t["symbol"], t["held_out_seq"], t["held_out_sha256"])

    for c in cands:
        if time.time() - started > args.budget_seconds:
            log("budget spent; stopping cleanly")
            break
        do("generated", f"{c['target']}:{c['sample']}", c["species"], c["symbol"],
           c["sequence"], c["sha256"])

    with open(os.path.join(args.out_dir, "manifest.json"), "w") as fh:
        json.dump({
            "job": "fin-scale-jaspar-motif-scan/v1",
            "question": "do these windows carry more JASPAR motif hits than "
                        "dinucleotide-preserving scrambles of themselves?",
            "outcome_kind": "computed motif hit counts; NOT observed binding, "
                            "NOT functional evidence, NOT a claim about any live fish",
            "primary_endpoint": "total hits across all motifs, real vs own mean "
                                "shuffle, paired across windows (ONE test)",
            "secondary": "per-motif, Holm-corrected, descriptive only",
            "jaspar_release": "JASPAR2024", "collection": args.collection,
            "tax_group": args.tax_group, "n_motifs": len(motifs),
            "fpr_threshold": FPR, "n_shuffles": N_SHUFFLES, "seed": SEED,
            "both_strands": True,
            "n_motifs_built": len(BUILT),
            "pseudocounts": "JASPAR sqrt(N)/4 via Bio.motifs.jaspar.calculate_pseudocounts; "
                            "without them only 6 of 879 motifs yield a finite threshold",
            "background": {"kind": "single pooled background over all real held-out windows",
                           "values": {b: round(BG[b], 5) for b in "ACGT"},
                           "why": "threshold_fpr costs ~244 s for 879 motifs, so a "
                                  "per-sequence background was unaffordable; real and "
                                  "its shuffle share identical PSSMs and thresholds, so "
                                  "the paired contrast remains composition-controlled",
                           "forfeits": "cross-sequence hit-count comparison is "
                                       "composition-confounded and descriptive only"},
            "inputs": {"input_set_id": inputs["input_set_id"],
                       "n_targets": len(inputs["targets"]), "n_candidates": len(cands)},
            "software": _software(),
            "runtime": {"total_seconds": round(time.time() - started, 1),
                        "n_scanned": len(results)}}, fh, indent=2)
    log(f"done: {len(results)} sequences scanned")
    _emit(args.out_dir)
    return 0


def _emit(out_dir: str) -> None:
    import io, tarfile
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as tf:
        tf.add(out_dir, arcname=".")
    blob = base64.b64encode(gzip.compress(buf.getvalue())).decode()
    print("MOTIF_BEGIN", flush=True)
    for i in range(0, len(blob), 800):
        print("MOTIF_B64 " + blob[i:i + 800], flush=True)
    print("MOTIF_END", flush=True)


def _software() -> dict:
    out = {"python": sys.version.split()[0]}
    for mod in ("numpy", "Bio", "pyjaspar"):
        try:
            out[mod] = getattr(__import__(mod), "__version__", "present")
        except Exception:
            out[mod] = "absent"
    try:
        out["pip_freeze_sha256"] = hashlib.sha256(
            subprocess.run([sys.executable, "-m", "pip", "freeze"],
                           capture_output=True, text=True, timeout=120).stdout.encode()).hexdigest()
    except Exception:
        out["pip_freeze_sha256"] = "unavailable"
    return out


if __name__ == "__main__":
    raise SystemExit(main())
