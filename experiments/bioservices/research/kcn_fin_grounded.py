"""Grounded literature analysis on zebrafish kcnh2a / kcnk5b fin patterning.

**OpenResearch is not available on this workspace.** Four direct id probes
against Nebius Scientific AI returned `NOT_FOUND: "The requested operation,
artifact or App was not found in your workspace."`, and neither catalogue (26
scientific models, 66 general) contains any research or literature model. The
exact errors and request ids are carried in the receipt this writes.

So this is the authorized fallback: primary sources fetched **first** from
Europe PMC, then a model asked to analyse *only the supplied text*. The ordering
is the point. A model asked about this topic from memory produces fluent
citations that cannot be checked; a model handed the fetched text can be checked
against it, and is instructed to say so when the text does not support an item.

Every source carries a read level, `full-text` or `abstract`. An abstract is
never summarised in the voice of having read the paper.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

GPUOPS = "/data/worktrees/delphi-evolve/gpuops"
sys.path.insert(0, GPUOPS)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))

from connectors.bioservices.receipts import sha256_file, sha256_text, utc_now, write_json  # noqa: E402

MAX_CALLS, MAX_IN, MAX_OUT = 6, 120_000, 24_000

SYSTEM = (
    "You analyse ONLY the source text supplied in the prompt. You have no other sources. "
    "Every factual statement you make must be traceable to a passage in that text, and you "
    "cite the PMCID it came from. When the supplied text does not contain something asked "
    "for, write exactly 'NOT IN SUPPLIED TEXT' for that item rather than supplying it from "
    "memory. Do not invent citations, numbers, p-values, concentrations, allele names or "
    "author names. Distinguish what a paper measured from what it concluded. Where a source "
    "is an ABSTRACT only, say so whenever you draw on it."
)

PROMPT = """Below are primary sources on potassium-channel control of zebrafish fin size and
proportion, fetched from Europe PMC. Each is labelled with its PMCID, DOI and READ LEVEL.

Answer these, grounded strictly in the supplied text:

1. **Exact primary citations.** For each distinct claim about kcnh2a or kcnk5b in fin
   patterning, give the PMCID and DOI of the source that supports it.
2. **Experimental conditions.** Genotypes, alleles, stages, temperatures, drug names and
   concentrations, transgenic lines, and the tissue or cell types involved, where the text
   states them. Where it does not, write NOT IN SUPPLIED TEXT.
3. **Quantitative parameters.** Any numbers the text gives: fin-length ratios, fold changes,
   membrane-potential values, ion concentrations, segment lengths, sample sizes, statistics.
   Quote the number and the PMCID. Do not estimate or round anything that is not stated.
4. **Mechanistic picture, and where the sources DISAGREE or leave gaps.** Be explicit about
   what is correlation, what is intervention, and what is inference.
5. **Next experiments** that the supplied text itself motivates, each with the specific gap it
   would close. Mark any that would require a capability the sources do not demonstrate.

Keep it compact and factual. A short answer that is fully supported beats a long one that is
not.

--- SOURCES ---
{sources}
"""


def _strip_xml(xml: str) -> str:
    body = re.sub(r"<ref-list.*?</ref-list>", " ", xml, flags=re.S)
    body = re.sub(r"<back.*?</back>", " ", body, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", body)
    return re.sub(r"\s+", " ", text).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Grounded kcnh2a/kcnk5b fin literature analysis")
    ap.add_argument("--litcache", required=True)
    ap.add_argument("--abstracts", required=True)
    ap.add_argument("--availability-probe", required=True,
                    help="JSON recording the OpenResearch NOT_FOUND probes")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--model", default="gemini-3.1-pro-preview")
    ap.add_argument("--chars-per-fulltext", type=int, default=60000)
    args = ap.parse_args()

    from scientific_services import gemini_client as gc

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    gc.LEDGER = Path(args.ledger)
    gc.MAX_CALLS, gc.MAX_IN, gc.MAX_OUT = MAX_CALLS, MAX_IN, MAX_OUT

    blocks, manifest = [], []
    for path in sorted(Path(args.litcache).glob("PMC*.xml")):
        text = _strip_xml(path.read_text())
        kept = text[: args.chars_per_fulltext]
        blocks.append(f"\n### {path.stem} — READ LEVEL: full-text "
                      f"({len(kept)} of {len(text)} characters supplied)\n{kept}\n")
        manifest.append({"pmcid": path.stem, "read_level": "full-text",
                         "chars_total": len(text), "chars_supplied": len(kept),
                         "xml_sha256": sha256_file(str(path))})

    abstracts = json.load(open(args.abstracts))
    for pmcid, rec in abstracts.items():
        b, ab = rec["brief"], (rec.get("abstract") or "")
        ab = re.sub(r"<[^>]+>", " ", ab)
        blocks.append(f"\n### {pmcid} — READ LEVEL: ABSTRACT ONLY — "
                      f"{b.get('doi')} ({b.get('year')})\nTitle: {b.get('title')}\n{ab}\n")
        manifest.append({"pmcid": pmcid, "read_level": "abstract", "doi": b.get("doi"),
                         "year": b.get("year"), "title": b.get("title"),
                         "abstract_sha256": sha256_text(ab)})

    prompt = PROMPT.format(sources="\n".join(blocks))
    print(f"{len(manifest)} sources; prompt {len(prompt)} characters")

    client = gc.Gemini()
    n_in = client.count_tokens(args.model, prompt, SYSTEM)
    print(f"model {args.model}; counted input tokens {n_in} (cap {MAX_IN})")
    if n_in > MAX_IN:
        raise SystemExit(
            f"prompt is {n_in} tokens, over the {MAX_IN} cap; lower --chars-per-fulltext")

    rec = client.generate(args.model, prompt, system=SYSTEM, max_output_tokens=9000,
                          temperature=0.1, label="kcn-fin-grounded", out_dir=out_dir)
    um = rec.get("usage_metadata", {})
    ledger = json.loads(Path(args.ledger).read_text()) if Path(args.ledger).exists() else {}
    write_json(str(out_dir / "grounded_receipt.json"), {
        "task": "zebrafish kcnh2a/kcnk5b fin patterning: bioelectric and mechanobiology",
        "run_utc": utc_now(),
        "openresearch_availability": json.load(open(args.availability_probe)),
        "fallback_reason": ("OpenResearch is not present on this Nebius workspace; the exact "
                            "NOT_FOUND probes are recorded above. Fallback is Europe PMC "
                            "primary sources plus a grounded model analysis, as authorized."),
        "sources": manifest,
        "model_requested": rec["model_requested"],
        "model_version_returned": rec["model_version_returned"],
        "usage": {"input_tokens": um.get("promptTokenCount"),
                  "output_tokens": um.get("candidatesTokenCount"),
                  "thinking_tokens": um.get("thoughtsTokenCount")},
        "caps": {"max_calls": MAX_CALLS, "max_input_tokens": MAX_IN, "max_output_tokens": MAX_OUT},
        "ledger_totals": {k: ledger.get(k) for k in ("calls", "input_tokens", "output_tokens")},
        "epistemic_status": ("model analysis of supplied primary text; every claim is a LEAD "
                             "until checked against the cited source. Not verified truth."),
        "prompt_sha256": rec["prompt_sha256"],
    })
    print("\n--- RESPONSE ---\n")
    print(rec["response_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
