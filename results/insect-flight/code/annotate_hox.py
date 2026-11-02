#!/usr/bin/env python3
"""Re-apply the post-hoc verification block to hox-identity.json.

`hox_identity.py` rewrites that file from scratch every run, which would drop
the verification block added after study 1 was built. This script is the
re-application step, so the annotation survives a re-run instead of being
retyped. Run it after `hox_identity.py`.
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCK = {
    "added_by": "the agent that completed the page, after study 1 was built",
    "what_was_checked": "Study 1 depends on four numbers attributed to Paul "
    "et al. 2021 (PMID 34001903). None of them is in that paper's PubMed "
    "abstract. The full text is open access and was fetched this session "
    "(Europe PMC, PMC8129201; stored at "
    "data/paul2021-PMC8129201-fulltext.xml, sha256 "
    "4e12dc00acaf5c3d21f2e8690ec56f53646cc3a80b87c656c45dfc56b59c6d92) and "
    "all four were confirmed verbatim.",
    "confirmed": {
        "39 percent of endogenous Ubx": "'characteristic wing-like phenotypic "
        "traits (including veins, hairs organization, and flattening) "
        "eventually appeared when the level decreased to 39% of endogenous "
        "Ubx (2.5 times lower than endogenous Ubx)'",
        "490 percent of endogenous Antp": "'the wing resembled a haltere in "
        "terms of size, shape, and hairs organization when the expression "
        "level corresponded to 490% of endogenous Antp'",
        "18.5x by antibody": "'Ubx was 18.5 times more strongly expressed "
        "than Antp'",
        "10.5x by GFP": "'Ubx expression levels were 10.5 times higher than "
        "Antp levels'",
    },
    "correction_to_this_study_s_framing": "This study's `prediction.note` "
    "calls the two protein-ratio measurements a disagreement that 'propagates "
    "directly' into the prediction. That is true arithmetically, but it "
    "understates what the paper says: Paul et al. do not leave the two "
    "numbers in conflict. They attribute the gap to antibody affinity and "
    "conclude that 'the Antp antibody is 1.85 times less affine', which "
    "makes the GFP-based 10.5x their own preferred measurement. The GFP arm "
    "is also the arm whose held-out prediction lands within 4%. So the model "
    "comparison and the paper's own reasoning select the same number, "
    "independently - which is a stronger result than this study originally "
    "claimed, not a weaker one.",
    "independent_support_for_the_graded_variant": "The paper states directly, "
    "of both the Antp and the Ubx series, that 'In both cases, intermediate "
    "levels led to intermediary phenotypes'. That is an OBSERVATION of "
    "intermediate organs at intermediate doses, which is what this study's "
    "graded variant predicts and what its bistable variant forbids. It was "
    "not used to build the model and it is not part of the 4% prediction; it "
    "is a separate, qualitative confirmation of the variant the quantitative "
    "test already selected.",
    "figure_fix": "The control figure's y-axis was pinned to (-0.03, 1.05) "
    "while the bistable variant's wing branch settles at about 1.61, so that "
    "curve ran off the top of the panel and the panel read as a MISSING curve "
    "rather than a high one. The axis now follows the data. No model code was "
    "changed.",
    "stale_result_found_and_refreshed": "The inherited hox-identity.json was "
    "NOT the output of the hox_identity.py beside it. Re-running the code "
    "unchanged - the only edit was a figure axis limit - moved the bistable "
    "variant's held-out prediction from 200 (i.e. it never crossed) to 6.82, "
    "flipped controls.all_variants_pass from false to true, rewrote both "
    "variant descriptions, and added a whole "
    "`hysteresis_test_model_independent` section that no earlier result "
    "carried. So the code had been revised and never re-run, and the emitted "
    "result described a superseded model. The refreshed result is the one in "
    "this file. It is also the better one: the bistable variant now passes "
    "the same controls as the graded one, which makes the comparison a fair "
    "test rather than a strawman, and the discrimination it reports (4.0% vs "
    "39.2% on the GFP protein ratio) is smaller and more credible than the "
    "40-fold gap the stale file implied.",
    "not_changed": "No model code, parameter, control or conclusion was "
    "altered by hand. The only edit to hox_identity.py was a figure axis "
    "limit; everything else here is that file's own output, refreshed.",
}


def main():
    p = ROOT / "hox-identity.json"
    d = json.loads(p.read_text())
    d["post_hoc_verification"] = BLOCK
    p.write_text(json.dumps(d, indent=1))
    print("post_hoc_verification re-applied to", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
