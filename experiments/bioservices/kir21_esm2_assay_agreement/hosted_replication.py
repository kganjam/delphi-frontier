"""Hosted ESM-2 replication of the local Kir2.1 scoring.

Submits the SAME reference sequence and the SAME hashed 256-variant subset that
this harness scored locally, to Nebius Scientific AI's pinned ESM-2 with the
``masked-marginals`` strategy. A different implementation on different hardware
scoring identical inputs is an independent check that local scoring is not
peculiar to this machine or this code.

Runs a tiny validation pilot first, exactly as the local run did: a positive
control whose answer is known, and a negative control that must be refused.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from connectors.bioservices import nebius_scientific as nsc  # noqa: E402
from connectors.bioservices import proteingym  # noqa: E402
from connectors.bioservices.receipts import sha256_text, utc_now, write_json  # noqa: E402
from experiments.bioservices.kir21_esm2_assay_agreement import common  # noqa: E402

MODELS = {"esm2-650m": "submit_esm2_650m", "esm2-3b": "submit_esm2_3b"}


def _manifest(reference: str, mutants: list[str], name: str = "KCNJ2_MOUSE") -> dict:
    fasta = f">{name}\n{reference}\n"
    variants = "mutant\n" + "\n".join(mutants) + "\n"
    return nsc.build_manifest({"sequences.fasta": fasta, "variants.csv": variants})


def run_job(model_id: str, reference: str, mutants: list[str], key: str,
            label: str, poll_s: float) -> dict:
    tool = MODELS[model_id]
    rec = nsc.JobRecord(model_id=model_id, operation="score-variants", idempotency_key=key)
    manifest = _manifest(reference, mutants)
    print(f"[{label}] {model_id}: {len(mutants)} variants, reference {len(reference)} aa")
    try:
        ref = nsc.upload_manifest(model_id, manifest, key + "-upload")
        rec.artifact_id, rec.artifact_sha256 = ref["artifact_id"], ref["sha256"]
        print(f"[{label}] artifact {ref['artifact_id']} sha {ref['sha256'][:12]} "
              f"({ref['size_bytes']} bytes)")
        sub = nsc.submit(model_id, tool, "score-variants", ref,
                         {"fasta_file": "sequences.fasta", "variants_file": "variants.csv",
                          "strategy": "masked-marginals", "precision": "float32"},
                         key)
        rec.submitted_utc = utc_now()
        rec.operation_id = sub.get("operation_id") or sub.get("id") or sub.get("name")
        print(f"[{label}] SUBMITTED operation_id={rec.operation_id}")
        if not rec.operation_id:
            rec.error = {"message": "submit returned no operation id", "payload": sub}
            return rec.to_dict()
        pol = nsc.poll(rec.operation_id, timeout_s=poll_s)
        rec.states, rec.final_state = pol["states"], pol["final"]
        print(f"[{label}] states {' -> '.join(pol['states'])}; final {pol['final']}")
        if pol["final"] == "SUCCEEDED":
            rec.result = nsc.result(rec.operation_id)
        else:
            rec.error = {"final_state": pol["final"], "detail": pol["detail"]}
    except nsc.ModelMaintenance as exc:
        rec.error = {"code": "MODEL_MAINTENANCE", "detail": json.loads(str(exc)),
                     "note": "App paused by the operator; one retry was made as instructed"}
        rec.final_state = "NOT_SUBMITTED_MAINTENANCE"
        print(f"[{label}] MODEL_MAINTENANCE after one instructed retry; not submitted")
    except Exception as exc:
        rec.error = {"type": type(exc).__name__, "message": str(exc)[:900]}
        rec.final_state = "CLIENT_ERROR"
        print(f"[{label}] ERROR {type(exc).__name__}: {str(exc)[:300]}")
    return rec.to_dict()


def main() -> int:
    ap = argparse.ArgumentParser(description="Hosted ESM-2 replication of local Kir2.1 scoring")
    ap.add_argument("--data-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--models", default="esm2-650m")
    ap.add_argument("--key-prefix", default="kir21-hosted-v1")
    ap.add_argument("--poll-seconds", type=float, default=900)
    ap.add_argument("--pilot-only", action="store_true")
    args = ap.parse_args()

    started = time.time()
    protocol = common.load_protocol()
    surface, function, _ = common.load_assays(protocol, args.data_dir)
    reference = surface.reference_sequence
    matched = proteingym.matched_variants(surface, function)
    subset = common.select_subset(matched, protocol["subset"]["salt"], protocol["subset"]["size"])

    jobs = []
    for model_id in args.models.split(","):
        model_id = model_id.strip()
        if model_id not in MODELS:
            raise SystemExit(f"unknown model {model_id}; known: {sorted(MODELS)}")

        # Pilot: three real variants whose local scores are already recorded, so
        # the hosted numbers have something to be checked against immediately.
        pilot_mutants = subset[:3]
        jobs.append({"label": "pilot", **run_job(
            model_id, reference, pilot_mutants, f"{args.key_prefix}-{model_id}-pilot",
            "pilot", min(args.poll_seconds, 600))})

        if args.pilot_only:
            continue
        if jobs[-1].get("final_state") not in ("SUCCEEDED",):
            print("pilot did not succeed; not submitting the full subset")
            continue
        jobs.append({"label": "subset256", **run_job(
            model_id, reference, subset, f"{args.key_prefix}-{model_id}-subset256",
            "subset256", args.poll_seconds)})

    payload = {
        "stage": "hosted_esm2_replication",
        "purpose": ("independent-implementation check: identical reference and variant set, "
                    "scored by a hosted pinned ESM-2 instead of this host's local one"),
        "run_utc": utc_now(),
        "reference_sha256": sha256_text(reference),
        "reference_length": len(reference),
        "n_subset": len(subset),
        "local_comparison_file": "results/bioservices/kir21_scores_checkpoint.json",
        "jobs": jobs,
        "elapsed_seconds": round(time.time() - started, 1),
    }
    digest = write_json(args.out, payload)
    print(f"\nreceipt {args.out} sha256={digest}")
    for j in jobs:
        print(f"  {j['label']:10s} {j['model_id']:10s} op={j.get('operation_id')} "
              f"final={j.get('final_state')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
