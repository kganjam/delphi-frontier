# Review record

**Reviewer:** Google `gemini-4-argon`, one call, 2026-11-01. Prompt: hostile-but-fair critique of
`PLAN.md`, `RESULTS.md` and `LOCI.md` (46,538 bytes sent), asked specifically for overclaims,
abstract-level reads treated as fact, factual errors, the most important missing experiment, and
anything the computed results cannot support. HTTP 200, `finishReason: STOP`.

**This is a model critique, not an independent human review.** The project remains single-operator and
unreviewed in the sense SPEC-002 means. A model's objection is a lead, and each one below was either
verified against the data or rejected with a reason.

## Accepted and acted on

| # | Finding | What was verified | What changed |
| --- | --- | --- | --- |
| 1 | The identity metric was documented as "NM/blocklen", which names edit distance and would give ~0.011 for the positive control, not 0.989. | Checked the actual PAF line for `actb1_POSITIVE_CONTROL`: `375 0 375 + ... 1113 1125`; 1113/1125 = 0.989. The **code** always used column 10 (residue matches) ÷ column 11 (block length); only the **prose** was wrong. So this was a documentation error, not a miscomputation — reported here as the smaller thing it is, not the "critical" the reviewer called it. | Corrected the definition in `RESULTS.md`, in the generated `LOCI.md` scope line, and in both mapping scripts' docstrings. Added the verification to `RESULTS.md`. |
| 2 | "Splitting on scaffold boundaries … does not change per-scaffold results" is false: `-N5` and `--outs=0.6` were applied per chunk, so secondary hits are chunk-relative. | Confirmed from our own output: `tbx5a` has 13 alternative hits, `actb1` 12, `msxb` 10 — impossible under a single global `-N5`. | Replaced the claim with an explicit correction in `RESULTS.md` §R2: best hits are unaffected (no scaffold was split), alternative-hit counts are chunking artefacts and must not be read as copy number. Added the same caveat to the generated `LOCI.md` and to `PLAN.md` §4.1. |
| 3 | Only `a` paralogs were queried; with the teleost whole-genome duplication, a `kcnh2a` best hit could be the `b` paralog's region — and a 278 kb span at 0.61 identity is suspicious. | **Ran round 3 to test it.** `kcnh2b` best-hits the *same* scaffold region as `kcnh2a`, starting at the identical coordinate 1,301,510, at **higher** identity (0.762 vs 0.610). The reviewer was right and the consequence is worse than stated: the plan's primary candidate locus cannot be assigned to the `a` paralog. Controls for `tbx5`, `fgf10` and `kcnk5` resolved to different scaffolds, so those rows survive. | New round-3 run (`data/round3/`, 6 queries + 1 control, exit 0). New paralog check output in `LOCI.md`. `RESULTS.md` internal check #3 rewritten; the `kcnh2a` row is now flagged in the headline table. Claim `zf2ff-claim-candidate-loci-detectable` carries it as a limitation. |
| 4 | Long spans need a gap/intron audit before being called detections. | **Wrote and ran `scripts/audit_long_spans.py`** over all three PAFs. Result: N fraction is **0.0** in every window, so the spans are not bridged assembly gaps; but `cacna1g` (298 kb), `kcnh2a` (278 kb) and `kcnh2b` (239 kb) are each dominated by one ~0.1 Mb intron-like gap, the two `kcnh2*` queries share the identical 105,952 bp gap, and those rows carry 2–4 frameshifts. | New artifacts `SPAN-AUDIT.md` and `data/span_audit.json`. `RESULTS.md` gained a span-audit section naming those three rows as the least trustworthy. New analysis row G1b in `PLAN.md` §3. |
| 5 | The decomposition covered the fin blade and omitted the **pectoral girdle, endoskeletal radials and fin musculature** — a long stiff blade folds at the body wall. Also, `hhip` and the Hox cluster deletions were cited in §2.3 but had no perturbation row. | Accepted as a design error, not a wording problem. Ran a targeted Europe PMC query (`data/epmc3/pectoral_girdle_musculature.json`, 1,346 hits) and found two usable zebrafish reads: the cleithrum forms from four embryonic populations (PMID 39060278) and a `gli3`/Hedgehog ossification trade-off shifts girdle character toward stem-tetrapod form (PMID 40442084). | New trait **T11** (girdle and musculature), new §2.4 girdle module, new perturbation rows **P13** (`gli3`/Hh girdle dosage) and **P14** (`hhip`, which the reviewer noted was missing), and new conflict §4.1 #6 stating plainly that the root was forgotten. |
| 6 | §1 T4 described Exocoetid rays as "long, unbranched-looking" while marking the row `U` — an unsourced anatomical claim smuggled into an unknown row. The reviewer asserts the rays are in fact branched distally. | The reviewer's own counter-claim is unsourced too, so neither description is adopted. What is certain is that the original cell was a guess in a `U` row, which is the rule violation. | Removed the description; the cell now says no ray-level description is available and that an earlier draft contained a guess. Row P7's rationale no longer rests on it. |
| 7 | §1 T9 wrote "2n = 50 (not read here)" — a specific number with no source. | Accepted outright. | Replaced with `U`. |
| 8 | §6 listed thirteen abstract-level statements under the heading **Known**, which conflates "a paper's abstract says X" with "X". | Accepted. | §0's `S-abs` definition now says every such row reads as "the abstract states X"; the §6 heading and lead sentence were rewritten accordingly. |
| 9 | §2.2 claimed "three independent papers converge" on outgrowth duration, merging an embryonic bud-scaling result with two adult regeneration results. | Accepted after re-reading our own table: PMID 38527087 is the embryonic bud and describes proportion, not duration; 34061172 and 41321290 are adult regeneration. | §2.2's synthesis paragraph rewritten to split them and to say that the regeneration evidence is the weaker half **for this project's purpose**, despite being the larger half. |
| 10 | Europe PMC relevance ranking surfaces recent papers; citing a 2026 paper for the actinodin phenotype misrepresents the primary evidence base (the reviewer names Zhang et al. 2010, *Nature*). | Partly verified: ran a targeted provenance query (`data/epmc3/actinodin_primary_2010.json`, 28 hits) and the original knockdown report did **not** appear in the top results, so this project cannot establish priority either way. The reviewer's specific citation was not confirmed from a retrieved record and is not repeated as fact. | Added a provenance caution to §0 stating that every `S-abs` row establishes presence in the recent literature, not priority or original evidence, with the actinodin case named as the clearest example. |
| 11 | Missing failure mode: enlarged fins impose a locomotor/viability cost in water. | Accepted and sourced: a published comparison of wildtype vs **longfin** zebrafish tested tail-flip jump kinematics, voluntary jumping and exhaustion (PMID 38232499, `data/epmc3/longfin_drag_cost.json`). Its abstract states the hypothesis and design; this project did **not** read the result, so the effect's direction and size stay `U`. | New trait **T12**, new perturbation row **P15** (measure the cost first, because it is cheap and can kill the programme), new conflict §4.1 #7. |

## Rejected, with reasons

| # | Finding | Why not accepted |
| --- | --- | --- |
| R1 | The reviewer's framing of finding 1 as "Critical — Miscomputed Amino Acid Identity", including speculation that `blocklen` might be in base pairs and that indels may inflate it. | The computation was never wrong. The positive control's PAF line and the table agree exactly, which is the direct check the reviewer did not do. Downgraded to a documentation fix. Retained as a known limit: identity is computed over the aligned block, not the whole query, which is now stated. |
| R2 | That `eda` and `fgf20a` being used in the plan but absent from the mapping is a *results* error. | They were never claimed as mapped; the gap was between the plan's gene list and the computed list. Addressed by mapping them in round 3 rather than by changing a claim. |
| R3 | That `and1`/`and2` and `hoxa13a`/`hoxd13a` secondary hits should have been cross-checked for overlap. | The merge script already checks overlaps across **all** best hits of all queries in all rounds, which is how both flagged pairs were found; `and1`/`and2` and the two `hox13` queries do not overlap. Checking *secondary* hits for overlap would be uninterpretable given finding 2 (secondary-hit sets are chunk artefacts). Declined with that reason. |
| R4 | That specific future-dated PMIDs are "fabricated". | Every PMID cited is backed by a saved Europe PMC response body with a recorded sha256 and request URL (`SOURCES.md`). The retrievals are receipted; the reviewer's model cutoff is not evidence about them. The *provenance* half of the same finding was accepted — see 10. |

## Follow-up run after the review

Finding 3 left the paralog question open, so analysis G2 was then run as well
(`scripts/reciprocal_check.py`, exit 0, `RESULTS.md` §R3): miniprot `--trans` predictions from each
collision scaffold, aligned back against every member of the zebrafish gene family. It **resolved**
the `shha`/`shhb` collision in favour of `shha` (5 of 5 predictions), showed that `kcnh2a`'s
second-best scaffold is a `kcnh6a`-like locus, and **did not resolve** the `kcnh2a`/`kcnh2b`
collision: alignment score and percent identity rank the same predicted sequence differently. That
non-resolution is reported as such and carried as claim `zf2ff-claim-kcnh2-paralog-unresolved`. A
gene tree with outgroups is now the top open item.

## What the review did not fix

The deepest limitations are untouched by this round: **no full text was read for any source**;
**no gene tree or synteny analysis was run**, which is what the unresolved `kcnh2` collision needs;
and traits T3, T5, T6 and T8 still have **no candidate gene**. Nothing in this
review made the project an observation of a flying fish, and nothing in it was run on a fish.

## Second, quick pass

A short check with Google `gemini-3.8-flash` (1 call, HTTP 200, truncated at `MAX_TOKENS`) was run on
the README and the honesty-critical plan sections, asking only for sentences that still overclaim or
blur "an abstract says X" into "X". It returned one finding before truncating: the README's
"conflicts" takeaway stated five abstract-level statements as facts and said an enlarged fin "has a
measured locomotor cost", when this project read only that the comparison was performed. Accepted:
the takeaway now labels all five as abstract-level, downgrades the KCNH cardiac point to the general
family statement it is, and says plainly that the longfin performance **result** was not read. Trait
row T12 was corrected the same way. Because the response truncated, this pass is **not** a complete
check, and the changes made after it are themselves unreviewed.
