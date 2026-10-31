"""Adversarial design review of the genotype → fin growth → whole-organism chain.

The flying-fish mission implies a causal chain. Each arrow is an interface where
an inference can fail, and the point of this review is to attack them, not to
defend them:

    designed sequence → expression in the right cells at the right time
                      → altered bioelectric state
                      → altered fin size / proportion
                      → altered organism-level capability (gliding)

Grounded in primary sources fetched from Europe PMC, with read levels attached.
The model is asked to classify each interface as SUPPORTED, PLAUSIBLE-UNTESTED
or UNSUPPORTED **by the supplied text**, and to give a falsifiable check for
each — not an opinion about whether the design will work.

**No success probability is requested or produced.** A number attached to
"will this work biologically" would be fabricated confidence: there is no
reference class to draw it from and no experiment behind it. The output is a
list of interfaces, what the literature does and does not establish at each, and
what measurement would settle it.
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
    "You are an adversarial reviewer. Your job is to find where a proposed causal chain breaks, "
    "using ONLY the source text supplied in the prompt. Every claim you make cites the PMCID it "
    "came from. Where the supplied text does not settle something, write exactly 'NOT SETTLED BY "
    "SUPPLIED TEXT' rather than filling the gap from memory. Never invent citations, numbers, "
    "species, alleles or author names. Where a source is an ABSTRACT only, say so whenever you "
    "rely on it, and treat an abstract as weaker evidence than a full text. "
    "Do NOT give any probability, percentage, odds or likelihood that the design will work "
    "biologically; there is no reference class for such a number and inventing one is the error "
    "this review exists to prevent. Prefer 'this is not established' over 'this is unlikely'."
)

CHAIN = """THE PROPOSED CHAIN UNDER REVIEW

A generative DNA model (Evo 2) produces candidate regulatory sequences for zebrafish
genes. The implied engineering argument runs:

  (1) designed DNA sequence
  (2) -> transcription of the intended gene, in the intended cells, at the intended time
  (3) -> altered bioelectric state (membrane potential / intracellular K+)
  (4) -> altered fin size or proportion
  (5) -> altered whole-organism capability (gliding flight, as in flying fishes)

Known context you must use rather than assume: the candidates were generated from
zebrafish promoter-proximal sequence by a sequence model that does NOT model chromatin
accessibility. No accessibility predictor exists for zebrafish (Enformer and Borzoi
cover human and mouse). The candidates have NOT been transfected, expressed, or assayed
in any organism. Measured so far: candidates are indistinguishable from real zebrafish
promoters under the generating model's own likelihood, and under an independent motif
scan their enrichment interval overlaps that of real promoters."""

PROMPT = """{chain}

Review the chain above adversarially, grounded strictly in the supplied sources.

For EACH of the five interfaces (1->2, 2->3, 3->4, 4->5, and the sequence-design step
itself), give:

**A. Status** — exactly one of SUPPORTED / PLAUSIBLE-UNTESTED / UNSUPPORTED, by the
   supplied text, with the PMCID(s).
**B. The strongest evidence the sources actually provide**, and in what system
   (species, developmental stage, tissue, developmental vs regenerative context).
**C. The specific way the inference fails** — what is being assumed that the cited
   experiment did not test. Be concrete about context mismatches: embryonic fin bud
   versus adult fin, development versus regeneration, zebrafish versus flying fish,
   fin SIZE versus fin FUNCTION.
**D. A falsifiable check** — one experiment or measurement that would settle it,
   stated so that a specific outcome would refute the step.

Then, separately:

**E. Hypotheses that are uncertain and must not be stated as fact**, listed individually.
**F. The single weakest link in the chain**, with your reason.
**G. Anything the sources show that ARGUES AGAINST the chain**, which a proponent would
   be tempted to omit.

Be concise and specific. Do not give a probability of biological success.

--- SOURCES ---
{sources}
"""


def _strip_xml(xml: str) -> str:
    body = re.sub(r"<ref-list.*?</ref-list>", " ", xml, flags=re.S)
    body = re.sub(r"<back.*?</back>", " ", body, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="Adversarial design review of the fin chain")
    ap.add_argument("--litcache", required=True)
    ap.add_argument("--abstracts", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--ledger", required=True)
    ap.add_argument("--model", default="gemini-3.1-pro-preview")
    ap.add_argument("--chars-per-fulltext", type=int, default=55000)
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
                         "chars_supplied": len(kept), "chars_total": len(text),
                         "xml_sha256": sha256_file(str(path))})
    for pmcid, rec in json.load(open(args.abstracts)).items():
        b, ab = rec["brief"], re.sub(r"<[^>]+>", " ", rec.get("abstract") or "")
        blocks.append(f"\n### {pmcid} — READ LEVEL: ABSTRACT ONLY — {b.get('doi')} "
                      f"({b.get('year')})\nTitle: {b.get('title')}\n{ab}\n")
        manifest.append({"pmcid": pmcid, "read_level": "abstract", "doi": b.get("doi"),
                         "title": b.get("title"), "abstract_sha256": sha256_text(ab)})

    prompt = PROMPT.format(chain=CHAIN, sources="\n".join(blocks))
    client = gc.Gemini()
    n_in = client.count_tokens(args.model, prompt, SYSTEM)
    print(f"{len(manifest)} sources; prompt {len(prompt)} chars; {n_in} input tokens (cap {MAX_IN})")
    if n_in > MAX_IN:
        raise SystemExit(f"{n_in} tokens over cap; lower --chars-per-fulltext")

    rec = client.generate(args.model, prompt, system=SYSTEM, max_output_tokens=9000,
                          temperature=0.1, label="design-review-critique", out_dir=out_dir)
    um = rec.get("usage_metadata", {})
    ledger = json.loads(Path(args.ledger).read_text())
    write_json(str(out_dir / "critique_receipt.json"), {
        "task": "adversarial review of genotype -> fin growth -> whole-organism interfaces",
        "run_utc": utc_now(),
        "chain_under_review": CHAIN,
        "sources": manifest,
        "model_requested": rec["model_requested"],
        "model_version_returned": rec["model_version_returned"],
        "http_status": rec["http_status"], "finish_reason": rec["finish_reason"],
        "usage": {"input_tokens": um.get("promptTokenCount"),
                  "output_tokens": um.get("candidatesTokenCount"),
                  "thinking_tokens": um.get("thoughtsTokenCount")},
        "ledger_totals": {k: ledger.get(k) for k in ("calls", "input_tokens", "output_tokens")},
        "no_success_probability": ("no probability of biological success was requested or "
                                   "produced; there is no reference class for one"),
        "epistemic_status": ("model analysis of supplied primary text; a LEAD until checked "
                            "against the cited source. Not verified truth, and not a review "
                            "by a person."),
        "prompt_sha256": rec["prompt_sha256"],
    })
    (out_dir / "critique.md").write_text(rec["response_text"])
    print("\n--- CRITIQUE ---\n")
    print(rec["response_text"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
