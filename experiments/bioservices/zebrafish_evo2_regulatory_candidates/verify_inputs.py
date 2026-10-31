"""Independently re-verify the frozen input set against Ensembl.

The input set is frozen, so this **never modifies it**. It re-reads each region
from Ensembl and compares against the committed sequence, writing a separate
receipt. Verification accrues as a second artifact; the frozen one stays frozen.

This exists because Ensembl was unavailable for 6 of 9 regions when the set was
frozen, and those were recorded as unchecked rather than skipped. Run it again
whenever Ensembl is healthy; each run reports its own coverage, and a run that
verifies nothing says so.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from connectors.bioservices import ensembl, ucsc  # noqa: E402
from connectors.bioservices.receipts import sha256_text, utc_now, write_json  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Re-verify the frozen zebrafish input set")
    ap.add_argument("--input-set", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--species", default="danio_rerio")
    args = ap.parse_args()

    frozen = json.load(open(args.input_set))
    results = []
    for t in frozen["targets"]:
        lo, hi = t["upstream_region_forward"]
        committed = t["prompt_seq"] + t["held_out_seq"]
        row = {"symbol": t["symbol"], "region": [lo, hi], "strand": t["strand"],
               "committed_sha256": sha256_text(committed)}
        try:
            seq, _ = ensembl.sequence(t["chromosome"], lo, hi, t["strand"], args.species,
                                      retries=1, timeout=20)
            row.update({"verified": True, "identical": seq == committed,
                        "ensembl_sha256": sha256_text(seq)})
            if seq != committed:
                row["comparison"] = ucsc.agrees(seq, committed)
        except Exception as exc:
            row.update({"verified": False,
                        "reason": f"{type(exc).__name__}: {str(exc)[:140]}"})
        results.append(row)
        state = ("identical" if row.get("identical")
                 else "DIFFERS" if row.get("verified") else "unavailable")
        print(f"  {t['symbol']:9s} {state}")

    verified = [r for r in results if r.get("verified")]
    agreeing = [r for r in verified if r.get("identical")]
    payload = {
        "verification_of": os.path.basename(args.input_set),
        "input_set_id": frozen["input_set_id"],
        "verified_utc": utc_now(),
        "source": "Ensembl REST, compared against the committed UCSC-derived sequence",
        "n_targets": len(results),
        "n_verified": len(verified),
        "n_identical": len(agreeing),
        "n_unavailable": len(results) - len(verified),
        "all_verified_agree": len(verified) == len(agreeing),
        "note": ("the frozen input set is NOT modified by this script; coverage below 100% "
                 "means Ensembl was unavailable for those regions, not that they disagree"),
        "results": results,
    }
    digest = write_json(args.out, payload)
    print(f"\n{len(agreeing)}/{len(verified)} verified regions identical; "
          f"{payload['n_unavailable']} unavailable of {len(results)}")
    print(f"receipt {args.out} sha256={digest}")
    return 0 if payload["all_verified_agree"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
