# Evaluation kernel: research report

**How to generate, rank, debate, grade and benchmark candidate designs with AI agents without
the evaluation quietly turning into fiction.**

| | |
|---|---|
| Status | Research report. **Not a spec.** §9 proposes a protocol; nothing in it is implemented. |
| Date | 2026-11-04 |
| Reviewer status | Single author. Not independently reviewed. |
| Domain caveat | **Not one of the ~70 sources below measures an LLM judging a protein, a genetic construct or any other engineered-biology artifact.** They study chat answers, summaries, QA, math, code, Atari, MNIST, and protein structure or function *prediction*. Carrying any of these numbers over to design evaluation is extrapolation. The only in-domain grader measurement cited here is this repo's own ([§0.2](#02-the-in-repo-warning-shot)). |

---

## 0. How to read this document

### 0.1 Provenance and read-levels

This follows `CONTRIBUTING-VERIFICATION.md` rules 3 and 9. Every citation carries a read-level:

- **`full-text`**: the body was retrieved this session (arXiv PDF or HTML converted to text, or Europe
  PMC open-access XML). Quoted numbers were found in that text.
- **`abstract-only`**: only the abstract or metadata was retrieved. Numbers are quoted only if they
  appear in the abstract.
- **`secondary`**: only a web-search snippet or another paper's description was retrieved. **No number from
  a secondary source is load-bearing in this document.** Each one is flagged where it appears.
- **`not-retrieved`**: named for orientation only. Nothing is quoted from it.

**How the retrieval was done, stated plainly.** Four research sub-agents fetched and read the
sources and wrote notes with verbatim quotes. I then:
- re-checked a sample of **21 load-bearing quotes and numbers** by grepping them against the downloaded text
  (Zheng, Wang, Wataoka, Chen, PoLL, Huang, Thakur, Prometheus, Dubois, Kenton ×2, Choi ×2, Khan, Arena ×2,
  Michael, Shah & Wainwright, Boubdir, Irving). All 21 matched, allowing for PDF line breaks.
- extracted every quote in §7 and §8 myself from the downloaded full texts, because the sub-agent's
  write-up for those sections was lost.

The rest are relayed from sub-agent notes whose quotes were grep-checked against the source by the
agent. **Treat any quote not in the 21-item sample as `full-text, agent-verified, not re-checked by
the author`.**

Things marked **[DERIVED]** are my own arithmetic or inference, not a source's claim.

### 0.2 The in-repo warning shot

This repo has already met the failure this document is about. `findings/README-third-assessor.md`
(retrieved: it is in this tree) ran Gemini as a third assessor over 40 claims that two other LLM
assessors had scored:

> "**The third assessor scores below the trivial baseline.** A rule that ignores the claim entirely
> and always answers "partially-resolvable" agrees with the existing consensus more often than
> Gemini does."

The numbers: agreement 24/40 = 60%, against 29/40 = 72% for a constant answer; Cohen's κ = 0.369. The two
original assessors agreed with each other 88% of the time, and the finding warns that this is *not*
evidence of correctness because both are frontier LLMs reading the same text.

Every structural element of the protocol in §9 is aimed at catching that situation **before** a ranking ships:
- a trivial baseline;
- chance-corrected agreement;
- correlated judges;
- the confound of not knowing the original prompt;
- a harness defect (`maxOutputTokens` swallowed by thinking) that almost became a finding.

### 0.3 The answer in one screen

1. **LLM judges have large, measured, systematic biases, and they are worst exactly where design selection
   lives: between candidates of similar quality.**
   - Position: 18–24% of verdicts flip on order swap even for strong 2024 judges.
   - Self-preference: GPT-4 agreed with humans 94.5% of the time when they preferred its own answer and
     42.5% when they did not.
   - Authority: a fake citation shifted Claude-3 in 70% of cases and GPT-4 in 66%, no better than random.
   - Gaming: a constant "null model" reached an 86.5% length-controlled win rate on AlpacaEval 2.0. (§1, §8)
2. **The mitigations with measured gains:**
   - reference-guided grading (math-grading failures 14/20 → 3/20);
   - order swapping with aggregation (GPT-4 accuracy 52.7% → 62.5%, still below humans at 71.7%);
   - routing uncertain items to humans (→ 73.8%);
   - diverse small-judge panels (κ 0.627 → 0.763 on one QA task);
   - checklists (46.4% → 52.2% exact agreement).

   **Chain-of-thought before the verdict, multi-agent judge debate and self-critique show null-to-small,
   sometimes negative, effects.** (§2)
3. **Ranking math sets the budget.**
   - Exact top-K needs on the order of **n log n / Δ_K²** comparisons, so halving the gap at the cut costs 4×.
   - Below about n log n random comparisons the comparison graph is not even connected.
   - Fit BT by regularized batch MLE or count wins. Do not use sequential Elo.
   - Report rank as 1 + the number of candidates whose CI lies wholly above yours.
   - Ties at the top are the normal, honest output. (§3)
4. **Debate**: it helps when the judge lacks evidence the debaters have *and* that evidence is verifiable.
   Without that asymmetry it gives "small or no advantage", and **giving the judge the evidence directly
   beat debate**. Majority voting matches or beats multi-agent debate at lower cost. (§4)
5. **A rubric is an instrument that must itself be validated**, with chance-corrected agreement against
   experts, known-groups tests and halo checks. Percent agreement above 80% can coexist with a
   chance-corrected π of 59. (§5)
6. **Credible benchmarks share a pattern**:
   - prospective blindness (time-delayed or pre-release);
   - naive baselines that every method must beat;
   - bootstrap significance with honest ties;
   - difficulty strata;
   - published warnings about the gold standard;
   - published non-progress. (§6)
7. **Generation collapses by default.** Responses from different LLM families show 71–82% average
   pairwise similarity on open-ended queries. Quality-diversity archives and island models are the
   standard countermeasure. (§7)
8. **Goodhart is quantitative, not anecdotal.** Gold reward rises and then falls with optimization
   pressure. Ensembles mitigate overoptimization but do not eliminate it, because all members share
   error patterns. Optimizing against a monitor teaches the optimizer to hide. (§8)
9. **Recommendation (§9).** A frozen, preregistered kernel that:
   - **qualifies each judge on known-answer and seeded known-bad items before any of its verdicts count**;
   - judges per criterion, pairwise, in both orders, with a cross-family panel that excludes the generator's family;
   - interleaves hidden controls into every round;
   - aggregates with bootstrap CIs and publishes indistinguishable sets rather than forced orders;
   - keeps the scorer hidden from the generator and holds out a judge the generator never trained against;
   - emits a `predicted` Evidence record whose credibility is earned later against prospective wet-lab or
     instrument outcomes.

   **When a control fails, the kernel emits "no ranking", not a ranking.**

---

## 1. LLM-as-judge: the measured failure modes

Effect sizes below come from the sources' own tables or text. Where a source reports none, the entry says so.

### 1.1 Summary table

| Bias | Strongest measured effect | Source (read-level) | Strength of evidence |
|---|---|---|---|
| **Position** | GPT-4 swap-consistency **65.0%**, Claude-v1 **23.8%** (near-equal pairs). Order alone let Vicuna-13B "beat ChatGPT on 66 over 80 tested queries with ChatGPT as an evaluator." 2024 judges: pairwise consistency **0.76–0.89** (GPT-4, Claude-3.5-Sonnet, Llama-3.3-70B), Claude-3-Haiku **0.23** on DevBench | Zheng 2023 (full-text); Wang 2023 (full-text); Shi 2024 (full-text, >150,000 instances) | **Strong, replicated.** Grows as the quality gap shrinks |
| **Verbosity** | "Repetitive list" padding fooled Claude-v1 and GPT-3.5 **91.3%**, GPT-4 **8.7%** (n = 23). Verbosity-instruction changes swung a model's AlpacaEval win rate from **22.9% to 64.3%** | Zheng 2023; Saito 2023; Dubois 2024 (all full-text) | Strong on open-ended text. **Weak or mixed for 2024 judges on fact-heavy data** (CALM robustness 0.900–0.977) |
| **Self-preference** | GPT-4 agrees with humans **94.5%** when humans preferred GPT-4's answer vs **42.5%** when they did not (gap 0.520). Self-recognition correlates linearly with self-preference after fine-tuning | Wataoka 2024; Panickssery 2024 (full-text) | **Real but contested in mechanism.** Wataoka attributes it to *familiarity* (low perplexity), not identity. Zheng 2023 called its own self-enhancement result inconclusive. Some judges show the reverse |
| **Authority / fake citation** | Adding a fake reference shifted preference in **70%** (Claude-3) and **66%** (GPT-4) of cases. Random baseline 37%; humans 37% | Chen 2024 (full-text, n = 142) | Moderate (small n). "Human and all LLM judges (except GPT-4o) perform no better than random baseline under reference perturbation" |
| **Bandwagon** | >70% of evaluations followed the bandwagon cue in 11/15 (2023, mostly open) models. 2024 frontier judges: robustness 0.61–0.79 | Koo 2023; Ye 2024 / CALM (full-text) | Large for 2023 models, smaller for 2024. CALM: "the percentage of people favoring an answer did not significantly impact model robustness rate" |
| **Sycophancy** (agreeing with a confident claim) | Under "Are you sure?" pushback, models changed answers in **32% (GPT-4) to 86% (Claude 1.3)** of cases. A preference model preferred sycophantic over truthful responses **95%** of the time on one set, **45%** on the hardest misconceptions | Sharma 2023 (full-text) | Strong for the *direction*. Feedback-sycophancy magnitudes are figure-only and **not quoted** |
| **Rubric / prompt sensitivity** | Some judges "lose alignment with increased instructions". GPT-4 Turbo and Llama-3 70B show low variance. A 2023 counterpoint finds results "only slightly vary" with instructions | Thakur 2024; Chiang & Lee 2023a (full-text) | **Contested; judge-dependent.** Measure it per judge; don't assume it |
| **Calibration / leniency** | Judges tend to mark answers "correct": P₊ "significantly higher than 0.5". GPT-4 self-consistency across samples **α = 0.587**, below human inter-annotator α = 0.659. Raw LLM rubric answers "often fail to agree well with human judges" | Thakur 2024; Stureborg 2024 (full-text); Hashemi 2024 LLM-Rubric (abstract-only) | Moderate |
| **Within-call anchoring** | Coherence τ = 0.400 when scored first in a multi-attribute call vs 0.359–0.368 when third or fourth | Stureborg 2024 (full-text) | Weak (one dataset, small effect) but cheap to avoid |
| **Headline agreement inflation** | "Llama-3 8B has a Scott's π score of only 59, its percent agreement is still well above 80%." JudgeLM's ">90% agreement" is with its **GPT-4 teacher**, not humans. Prometheus's Pearson 0.897 with humans rests on **45 instances**; on FLASK, Prometheus-13B gets **0.449** | Thakur 2024; Zhu 2023; Kim 2023, 2024 (full-text) | **Strong.** This is the most common way a judge paper overstates itself |

### 1.2 Position bias (detail)

- **Zheng et al. 2023**, "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena", arXiv 2306.05685, **full-text**.
  - Setup: two similar GPT-3.5 answers per MT-bench question.
  - Results: "Only GPT-4 outputs consistent results in more than 60% of cases."
  - Table 2 consistency: Claude-v1 23.8%, GPT-3.5 46.2%, GPT-4 65.0%.
  - Caveat: deliberately near-equal pairs, so this is a near worst case, and n is about 80.
- **Wang et al. 2023**, "Large Language Models are not Fair Evaluators", arXiv 2305.17926, **full-text**.
  - Results: with a GPT-4 judge on Vicuna-13B vs ChatGPT, the conflict rate after swap was 37/80 (46.3%); with a ChatGPT judge it was 66/80.
  - On the gap: "when the score difference between the two responses is small (e.g., score gap ≤ 1), the evaluation results of GPT-4 are significantly affected by the position".
  - The bias direction depends on the judge: GPT-4 favoured slot 1, ChatGPT slot 2.
- **Shi et al.**, "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge", arXiv 2406.07791 (v9), **full-text**.
  - Scale: 15 judges, 22 tasks, >150,000 instances.
  - Findings: "position bias is not due to random chance … strongly affected by the quality gap between solutions."
  - Repetition stability of the top models is >0.95. **So the swap flips are systematic, not sampling noise, and re-asking the same order adds no information.**
  - Direction is task-dependent. Claude-3.5-Sonnet is "nearly preference-fair on MTBench (PF=0.01)" but "exhibits a strong recency-preferred position bias on DevBench (PF=0.22)."
- Corroborating:
  - Panickssery 2024 (2404.13076, full-text) reports reversal rates of "25%, 58%, and 89%" for GPT-4, GPT-3.5 and Llama.
  - CALM (2410.02736, full-text): "Position bias increases with more answer candidates." **This argues for pairwise rather than list-wise judging.**

### 1.3 Verbosity

- **Zheng 2023** Table 3: the repetitive-list attack failed Claude-v1 91.3%, GPT-3.5 91.3% and GPT-4 8.7% of the time, on 23 answers.
- **Saito et al. 2023**, arXiv 2310.10076, **full-text**.
  - "When the word count difference is large enough, GPT-4 almost always prefers the longer answer".
  - Verbosity-bias metric: GPT-4 0.328, GPT-3.5 0.428.
- **Dubois et al. 2024**, "Length-Controlled AlpacaEval", arXiv 2404.04475, **full-text**.
  - Length control raised Spearman with Chatbot Arena "from 0.94 to 0.98" and cut gameability from 26% to 10%.
  - **Negative result:** the length-controlled metric was *more* exposed to the paper's adversarial attack (gain 8.5 vs 0.0 for raw win rate). One debiasing step opened a different hole.
- For a design dossier, verbosity bias means **the agent that writes the longest rationale wins**. The defence is structural: canonical, length-capped dossiers (§9 S1), not exhortation in the prompt.

### 1.4 Self-preference

- **Wataoka, Takahashi, Ri 2024**, "Self-Preference Bias in LLM-as-a-Judge", arXiv 2410.21819, **full-text**.
  - Data: Chatbot Arena human-labelled pairs.
  - GPT-4: "0.945 ≈ 1852/(108+1852) and 0.425 ≈ 118/(160+118). The difference between these values is 0.520".
  - Mechanism: "LLMs assign significantly higher evaluations to outputs with lower perplexity than human evaluators, regardless of whether the outputs were self-generated."
- **Panickssery, Bowman, Feng 2024**, arXiv 2404.13076, **full-text**.
  - "GPT-4 is 73.5% accurate distinguishing itself from two other LLMs and humans."
  - Fine-tuning for self-recognition produces "a strong linear correlation" with self-preference.
  - Summarization only, and the causal claim is hedged by the authors.
- **PoLL** (Verga 2024, 2404.18796, full-text): "the highest positive delta for each individual model being scored occurs when it is judged by itself."
- **Zheng 2023**: "our study cannot determine whether the models exhibit a self-enhancement bias." **This null belongs in the record.**
- **Design relevance [DERIVED, untested]:**
  - If the bias runs through likelihood or familiarity, a judge from the same model family as the generating agent should over-rate that agent's designs and rationales.
  - For protein sequences, likelihood under a protein language model is a plausible analogue confound.
  - No source tests either.

### 1.5 Agreeing with confident or authoritative claims

- **Chen et al. 2024**, "Humans or LLMs as the Judge?", arXiv 2402.10669, **full-text**.
  - Attack success rate (ASR) of the fake-reference perturbation: GPT-4o 0.32, Claude-3 0.70, GPT-4 0.66, human 0.37, random 0.37.
  - ASR of the planted-factual-error perturbation: GPT-4o 0.06, Claude-3 0.08, GPT-4 0.09. **Strong judges catch planted errors but are swayed by planted authority.**
- **Ye et al. 2024 (CALM)**, arXiv 2410.02736, **full-text**.
  - Authority robustness rate: 0.662 (ChatGPT) to 0.865 (Claude-3.5).
  - The no-perturbation consistency rate is 0.856–0.925, **so roughly 8–14% of verdicts change on a plain re-run.** Every bias flip rate should be read against that floor.
- **Sharma et al. 2023**, arXiv 2310.13548, **full-text**: "AI assistants frequently provide feedback that is more positive when the user states they like or wrote the passage of text."
- **Design relevance:** an agent's design rationale that cites literature, possibly hallucinated, is exactly the authority attack. So is any framing that says which agent proposed the design or that the swarm "favours" it.

### 1.6 Calibration and the agreement-metric trap

- **Thakur et al.**, "Judging the Judges: Evaluating Alignment and Vulnerabilities in LLMs-as-Judges", arXiv 2406.12624 (v6), **full-text**.
  - The current version reports Scott's π; an earlier version used Cohen's κ.
  - "even judges that have more than 90% may still differ more than 10 points in their assigned score."
  - Judges sometimes mark a verbatim gold answer wrong and accept "Yes"/"Sure" as correct.
- **Stureborg et al. 2024**, "Large Language Models are Inconsistent and Biased Evaluators", arXiv 2405.01724, **full-text**: GPT-4's agreement with itself across samples, α = 0.587, is below expert-expert α = 0.659.
- **G-Eval** (Liu 2023, 2303.16634, full-text).
  - Headline Spearman with humans is 0.514 on SummEval, which is moderate.
  - "G-Eval-4 always gives higher scores to GPT-3.5 summaries than human-written summaries, even when human judges prefer human-written summaries".
  - The human α on that comparison was 0.07, so the authors call it preliminary.
- **Prometheus 2** (Kim 2024, 2405.01535, full-text): on FLASK, the best judges reach Pearson 0.555–0.679 with humans (GPT-4-1106 0.679). **That is the realistic ceiling to expect, not 0.9.**

---

## 2. Mitigations: measured versus merely recommended

### 2.1 Measured

| Mitigation | Measured effect | Source | Caveats |
|---|---|---|---|
| **Reference-guided grading** (judge solves first, or is given a reference) | Math-grading failures **14/20 → 3/20**. Removing reference answers from Prometheus dropped Pearson with GPT-4 **0.860 → 0.642**, "the most significant amount of performance degradation". JudgeLM reference support: agreement 75.87 → 80.15 | Zheng 2023 Table 4; Kim 2023 Table 6; Zhu 2023 Table 6 (full-text) | Tiny n in Zheng (10 questions × 2 orders). Prometheus and JudgeLM ablations are measured against GPT-4, not humans. **A format mismatch (trained without references, tested with them) made JudgeLM worse than baseline** |
| **Swap order, then aggregate (Balanced Position Calibration) + multiple sampled verdicts** | GPT-4 accuracy vs human majority **52.7% → 62.5%**, κ 0.24 → 0.37. ChatGPT 44.4% → 58.7% | Wang 2023 Table 4 | n = 80. **Still below the human average of 71.7% (κ 0.54)**. Swap + 3 samples beat 6 samples without swap, so the swap adds value beyond resampling |
| **Swap and call a tie on disagreement** | Not scored on its own; recommended default | Zheng 2023 §3.4 | Converts position flips into ties instead of errors. Cheap |
| **Route the most uncertain 20% to humans** | GPT-4 → **73.8%** (κ 0.56), matching the human average, at $23.1 vs $30 for full human labelling | Wang 2023 Table 4 | Same n = 80 |
| **Diverse panel of smaller judges (PoLL)** | Cohen's κ vs humans **0.763 vs 0.627** (GPT-4 alone) on NQ; Arena Kendall τ 0.778 vs 0.667; "seven to eight times less expensive" | Verga 2024 (full-text) | QA correctness with references. **Haiku alone beat the panel on HotPotQA** (0.873 vs 0.867). A "don't overthink" prompt raised GPT-4 alone from 0.627 to 0.725, so part of the gap was prompt, not panel |
| **Checklist decomposition** | LLM–human exact agreement **46.4% → 52.2%**; human inter-annotator agreement **0.194 → 0.256** | Cook 2024, TICK (abstract-only) | Abstract-level numbers only |
| **Learned per-judge calibration** | RMS error <0.5 on a 1–4 scale, "a 2× improvement over the uncalibrated baseline" | Hashemi 2024, LLM-Rubric (abstract-only) | Requires human-labelled calibration data |
| **Swap augmentation (fine-tuned judges)** | Consistency 73.45 → 78.89 | Zhu 2023 Table 5 | Measured against the GPT-4 teacher |
| **Length control** (post-hoc regression) | Arena Spearman 0.94 → 0.98; gameability 26% → 10% | Dubois 2024 | **Adversarial gain 0.0 → 8.5** (worse) |
| **Few-shot examples** | GPT-4 consistency 65.0% → 77.5% | Zheng 2023 Table 13 | **Null on accuracy**: "performs similarly to zero-shot GPT-4". Shifted GPT-3.5's bias from first to second slot |

### 2.2 Measured to be null, small or negative

| Practice | Result | Source |
|---|---|---|
| **Chain-of-thought before verdict** | JudgeLM agreement 75.54 (CoT) vs 75.87 (score-first), no gain. G-Eval ρ 0.514 vs 0.500 without CoT. Chiang & Lee: differences "often … less than 0.02", and "using auto CoT results in a lower Pearson's r for fluency … statistically significant … For groundedness, auto CoT even drastically decreases the correlation". CALM: +0.7% (GPT-4-Turbo) to +7% (GLM-4). Kenton 2024 (debate judges): "CoT tends to harm performance or be insignificant" | 2310.17631, 2303.16634, 2310.05657, 2410.02736, 2407.04622 (all full-text) |
| **CoT on math grading** (positive exception) | Failures 14/20 → 6/20, but "GPT-4's chain-of-thought process can be significantly influenced by the given answers"; reference-guided reached 3/20 | Zheng 2023 |
| **Explanation *after* the rating** (positive) | "asking the LLM to explain its own ratings consistently improves the correlation between the ChatGPT and human ratings" | Chiang & Lee 2023b, 2310.05657 |
| **Multi-agent debate among judges** (ChatEval) | GPT-4 accuracy 61.3 → 63.8 on Wang's 80 items, about 2 items. Same-role debate = single agent. More turns: "stagnation or even degradation" | Chan 2023, 2308.07201 (full-text) |
| **Self-correction without external feedback** | GPT-4 GSM8K 95.5 → 91.5 → 89.0 over two rounds; GPT-3.5 CommonSenseQA 75.8 → 38.1. "after self-correction, the accuracies of all models drop across all benchmarks" | Huang 2023, 2310.01798 (full-text) |
| **Debate vs majority vote at equal compute** | Debate 83.0 vs self-consistency 88.2 on GSM8K: "multi-agent debate significantly underperforms simple self-consistency using majority voting" | Huang 2023 Table 7 |

### 2.3 Recommended but not measured (in what was retrieved)

- **Judges from different model families**, as distinct from different sizes within one family. Prometheus 2 reports
  GPT-4-1106 and Claude-3-Opus correlating with each other at 0.694–0.736. That is evidence of partial, not full,
  independence. No retrieved source measures cross-family panels against same-family panels at matched cost.
- **Anonymizing authorship** in the judge prompt. This is implied by Panickssery's label-swap result (judges
  favour the summary *labelled* as their own) and by Sharma's feedback sycophancy, but no source tests the fix itself.
- **Separate calls per criterion.** Supported only by Stureborg's small anchoring effect.
- **Temperature and paraphrase diversity** so that repeated judgments are independent. Shi's repetition stability
  above 0.95 shows that re-asking at temperature 0 buys nothing. Whether paraphrase buys independence is untested.

---

## 3. Pairwise ranking mathematics

### 3.1 The models

- **Bradley-Terry (BT)**: P(i beats j) = wᵢ/(wᵢ+wⱼ), equivalently logistic in score differences. It was
  independently proposed by Zermelo (1929) and Ford (1957).
  - Bradley & Terry 1952, Zermelo, Ford and Hunter 2004 were all **not-retrieved**.
  - The existence condition comes via **Yan 2014**, arXiv 1411.1168, **full-text**: "the following strong
    connection condition is necessary and sufficient due to Ford (1957). Condition A. The directed graph G(A)
    constructed by the win-loss matrix A = (aij) is strongly connected." If it fails, "the MLE does not exist."
  - **Practically: one undefeated candidate sends plain BT MLE to infinity. Use a regularized MLE or a weak prior.**
- **Elo** is an online, sequential, stochastic-gradient approximation of BT.
  - **Boubdir et al. 2023**, "Elo Uncovered", arXiv 2311.17295, **full-text**: "Elo ratings for LLMs are highly
    sensitive to the order of comparisons and the choice of hyperparameters."
  - For P(A wins) ≈ 0.5, "ratings exhibit significant instability for a single sequence". This is "markedly
    exacerbated at higher K-factors".
  - "The instability plateaus as Nperms exceeds 100", so the remedy is averaging over ≥100 random orderings.
  - **Chatbot Arena** (Chiang et al. 2024, arXiv 2403.04132, **full-text**) moved from Elo to BT coefficients
    "because the BT coefficients are better for the purpose of statistical estimation". That is the paper's
    only stated reason; the LMSYS blog with the fuller argument was not retrieved.
- **Non-transitivity and clones.** **Balduzzi et al. 2018**, "Re-evaluating Evaluation", arXiv 1806.02643, **full-text**:
  - "Elo is meaningless – it has no predictive power – in cyclic games like rock-paper-scissors."
  - "an agent's Elo rating can be inflated by instantiating many copies of an agent it beats".
  - "There is an Elo rating that generates probabilities P iff curl(logit P) = 0."
  - **A swarm that emits near-duplicate designs can inflate a rating this way, so deduplicate before ranking (§9 S1).**
- **TrueSkill** (Herbrich, Minka, Graepel 2006, NeurIPS, **full-text** from the MSR PDF):
  - It keeps a Gaussian (μ, σ) per entity and displays "a conservative skill estimate given by the 1% lower quantile μ − 3σ", so under-tested entries cannot top the board by luck.
  - Matchmaking picks the most uncertain matches: "the goals of matchmaking and finding the most informative matches are aligned!"
  - Its convergence figure is for 8-player free-for-all games, not head-to-head.
- **Win counting (Copeland).** **Shah & Wainwright 2018**, arXiv 1512.08949, **full-text**:
  - Counting wins against random opponents is minimax-optimal up to constants for top-k, and "theoretical guarantees impose no conditions on the underlying matrix of pairwise-comparison probabilities".
  - In simulations with a non-transitive outlier, "the counting algorithm continues to achieve an accuracy of 100% … The departure from the BTL model however prevents the Spectral MLE algorithm from identifying the top k items."
  - **LLM judges have no obligation to be BT-consistent, which makes this robustness directly relevant.**

### 3.2 Sample complexity: how many comparisons for a reliable top-k?

| Result | Statement | Source |
|---|---|---|
| Connectivity floor | "Ω(n log n) is a necessary number of (random) comparisons for any algorithm". With fewer, the random comparison graph is disconnected and some item "cannot be ranked" | Negahban, Oh, Shah, Rank Centrality, 1209.1688; Chen, Fan, Ma, Wang 2019, 1707.09971, Remark 1 (full-text) |
| Exact top-K, passive random design, BTL | Spectral method and regularized MLE "achieve a sample complexity on the order of n log n / Δ_K²", matching the minimax limit. Δ_K = (w_K − w_{K+1})/w_max | Chen & Suh 2015, 1504.07218; Chen et al. 2019 (full-text) |
| Model-free version | Counting succeeds when Δ_k ≥ α√(log n/(npr)) with α ≥ 8, and every estimator fails at α ≤ 1/7. Δ_k is measured in "probability of beating a random opponent" units | Shah & Wainwright 2018 (full-text; fractions reconstructed from garbled PDF math) |
| Active vs passive | Active: about Σ_{i≤k} 1/(τᵢ−τ_{k+1})² + Σ_{i>k} 1/(τ_k−τᵢ)², up to logs. The gain "can be as large as a factor of n". Parametric (BT) assumptions "offer at most logarithmic gains" | Heckel, Shah, Ramchandran, Wainwright 2019, 1606.08842 (full-text) |
| Empirical active-sampling gain | Arena replay: for **win-matrix** precision 0.2, random needs 6,800 vs adaptive 4,400 (54% more). For **score** precision 0.3, 17,200 vs 16,400 (**5%** more) | Chiang 2024 (full-text) |
| Deterministic noisy judge | With no resampling, even the best ordering has max displacement Θ(log n) | Braverman & Mossel 2008, 0707.1051 (abstract-only) |

**What this means in practice.** Items 2, 3 and 5 are **[DERIVED]**.

1. **The cost is governed by the gap at the cut, Δ_K, not by n.** Halving the gap quadruples the cost. Close
   designs are the expensive ones, and they are also where the judge biases in §1 are largest. Every term in
   the problem pushes the same way: **a forced strict ordering among close candidates is the most expensive
   and least trustworthy thing this kernel can produce.** The kernel should be built to say "these four are
   indistinguishable at this budget".
2. **Connectivity floor** (Erdős–Rényi threshold ≈ n·ln n / 2 distinct pairs): about 51 pairs for n = 30, 98 for
   n = 50, 230 for n = 100. Being connected is necessary for a ranking, not sufficient.
3. **The sufficient-count constants are not usable as a budget.** From Shah & Wainwright's α = 8 and α = 1/7, for
   n = 100 and Δ = 0.1 the required total lies somewhere between about 4,700 and about 1.5 million comparisons.
   **Do not quote either number as "the required count".** Budget empirically: run until the top-k CIs separate
   or the budget is exhausted, then report what separated.
4. **Round-robin versus Swiss versus adaptive.**
   - No retrieved source compares Swiss-system and round-robin designs for noisy ranking. That question is
     **open in what we retrieved**.
   - Sourced facts: random designs need about n log n comparisons for connectivity, and adaptive designs gain
     up to a factor of n when most items are far from the boundary but little when they are all near it
     (Heckel). Arena's gain on scores was only 5%.
   - Swiss pairing is an uncertainty-targeting heuristic in the same spirit as TrueSkill matchmaking, but it is
     unanalysed. Adaptive schedules also depend on early results, so a biased early verdict steers later sampling.
5. **Rule [DERIVED]:**
   - For n up to about 30, full round-robin in both orders is affordable and removes schedule design as a source of error.
   - Above that, start with a random connected design (several multiples of n ln n pairs), then adaptively spend the rest of the budget on pairs that straddle the top-k boundary.
   - Keep a fixed random fraction (say 20%) throughout so the adaptive part cannot hide a mis-ranked early loser.

### 3.3 Reporting uncertainty

- **Arena rank rule** (full-text):
  - "Rm = 1 + Σ 1{inf Cm′ > sup Cm}", i.e. rank = 1 + the number of entries whose CI lies entirely above yours, with the guarantee that "no model's performance is understated."
  - CIs are pivot bootstrap or "sandwich" robust standard errors. The sandwich form keeps MLE asymptotically normal "even when these assumptions do not hold".
  - Multiplicity correction "makes the intervals looser", and "the more models are included, the larger the intervals become."
- **CAFA** (full-text, §6) uses 10,000 bootstrap samples for head-to-head significance and openly reports that
  top methods are "statistically indistinguishable".
- **[DERIVED]** For this kernel:
  - **Bootstrap over artifacts *and* judges *and* prompt paraphrases**, not just over votes. Votes from one judge on one pair are not independent draws.
  - Michael et al. 2023 make the same point about their own statistics: the i.i.d. assumption "is not strictly true".

---

## 4. Debate: what the evidence actually says

### 4.1 Results

| Study | Setting | Result | Read-level |
|---|---|---|---|
| **Irving, Christiano, Amodei 2018**, "AI safety via debate", 1805.00899 | MNIST; a sparse classifier judge sees only the pixels the debaters reveal | Accuracy "from 59.4% to 88.9% given 6 pixels and from 48.2% to 85.2% given 4 pixels". Without precommitment, 74.4% and 59.7% | full-text |
| **Parrish et al. 2022a**, "Single-Turn Debate Does Not Help Humans…", 2204.05212 | Humans, QuALITY, 90 s | "We do not find that explanations in our set-up improve human accuracy, but … providing human-selected text snippets does improve accuracy." **Negative** | full-text |
| **Parrish et al. 2022b**, "Two-Turn Debate Doesn't Help…", 2210.10860 | Humans, 5 min | "humans perform similarly" with or without arguments. With arguments, judges were "more often confidently wrong". **Negative** | full-text |
| **Michael et al. 2023**, "Debate Helps Supervise Unreliable Experts", 2311.08702 | Skilled human debaters; judge without the passage | Human debate **84%** vs consultancy **74%** (p = 0.04). **GPT-4 debaters: 78% vs 80%, no significant difference** | full-text |
| **Khan et al. 2024**, "Debating with More Persuasive LLMs Leads to More Truthful Answers", 2402.06782 | QuALITY-hard, two options, judge without the text, verified-quote tool | Non-expert humans **88%**, LLM judges **76%** with debate, vs naive 60% / 48% and consultancy 78% / 54%. "Higher consultant skill leads to worse accuracy." "Identical judge accuracy between static and interactive debate" | full-text |
| **Kenton et al. 2024**, "On scalable oversight with weak LLMs judging strong LLMs", 2407.04622 | 9 tasks, about 5 million generation calls | "In extractive QA tasks with information asymmetry, debate outperforms QA without article … **but not QA with article**. For other tasks … either small or no advantage to debate over QA without article." No significant effect of turn count. Best-of-N debaters "doesn't significantly increase accuracy". "CoT tends to harm performance or be insignificant". In open consultancy, "the judge is equally convinced by the consultant, whether or not the consultant has chosen to argue for the correct answer." | full-text |
| **Du et al. 2023**, multi-agent debate, 2305.14325 | ChatGPT, 3 agents × 2 rounds | GSM8K 77.0 → 85.0, arithmetic 67.0 → 81.8. **Not compute-matched**: majority vote used 3 samples; GSM8K error bars overlap (81.0 ± 3.9 vs 85.0 ± 3.5) | full-text |
| **Smit et al. 2024**, "Should we be going MAD?", 2311.17371 | Medical QA etc. | MAD systems "do not reliably outperform other proposed prompting strategies, such as self-consistency". Multi-Persona is "about 7% worse than the Medprompt strategy" | full-text |
| **Wang et al. 2024**, "Rethinking the Bounds of LLM Reasoning", 2402.18272 | Reasoning tasks | "a single-agent LLM with strong prompts can achieve almost the same performance as the best existing discussion approach" | full-text |
| **Choi, Zhu, Li 2025**, "Debate or Vote", 2508.17536 | 7 benchmarks, N = 5 agents | "Majority Voting alone accounts for most of the performance gains typically attributed to MAD." Averages: Qwen2.5-7B voting **0.7691** vs best MAD 0.7377; Llama3.1-8B voting 0.7242 vs 0.6990. Longer debates often worse. The authors model debate as a martingale over beliefs, "implying that debate alone does not improve expected correctness" | full-text |
| **Brown-Cohen, Irving, Piliouras 2024**, "Doubly-efficient debate", 2311.14125 | Theory | Verification with "a constant number of queries" to the judge, **if** the debaters can produce reasoning traces that "careful human analysis could have been used to judge". Notes the "obfuscated argument problem" | full-text (intro only) |

### 4.2 Conditions under which debate helped

1. **Information asymmetry.** The judge lacks access that the debaters have.
2. **Verifiable evidence.** A quote-verification tool, or pixels revealed from the real image.
3. **A two-sided structure** compared against *single-advocate consultancy*. Consultancy is a weak baseline, and optimizing it for persuasion *lowers* accuracy (Khan).

### 4.3 Conditions under which it did not

1. **No information asymmetry.** Debate ≈ or < direct QA (Kenton).
2. **The judge can see the evidence directly.** Direct QA beat debate on extractive tasks (Kenton).
3. **Human-written single- or two-turn arguments** (Parrish ×2).
4. **GPT-4-class debaters in 2023** (Michael).
5. **Self-improvement debate against voting** at equal or lower compute (Choi, Smit, Wang, Huang).

### 4.4 Implication for this kernel [DERIVED]

- In our setting the judge can be handed the full dossier, including instrument outputs. **That is the "QA with
  article" condition, which beat debate.** So debate should not be in the default path.
- It earns a place only as a **dispute procedure**: when a claim rests on evidence the judge cannot read directly
  (a simulation trajectory, a raw assay file, a 300-page supplement), advocates point to *verified* excerpts.
  Even then it must beat the "give the judge the excerpt" baseline on calibration items before it is used.
- **Never use single-advocate consultancy.** An agent championing its own design to a judge is exactly the
  format where the judge "is equally convinced … whether or not the consultant has chosen to argue for the
  correct answer."

---

## 5. Rubric design

### 5.1 What the evidence supports

- **Decompose into binary or checklist items where possible.** TICK (Cook 2024, 2410.03608, abstract-only): checklists raised LLM–human exact agreement 46.4% → 52.2% *and* human–human agreement 0.194 → 0.256.
  - **Note the second number.** A rubric that helps humans agree is making the construct clearer, not just making the LLM more consistent.
- **Use instance-specific criteria rather than generic adjectives.**
  - BiGGen Bench (Kim 2024, 2406.05761, abstract-only) builds per-instance criteria because "abstract evaluation criteria like helpfulness and harmlessness … often lack the flexibility and granularity of human assessment."
  - WildBench (Lin 2024, 2406.04770, abstract-only) uses task-specific checklists plus an explicit length rule.
- **Calibrate rubric outputs per judge against human labels.** LLM-Rubric (Hashemi 2024, abstract-only): raw outputs "often fail to agree well with human judges -- indeed, the humans do not fully agree with one another". A small learned mapping halved the error.
- **Score each criterion in a separate call** (Stureborg's anchoring effect, §1.1).
- **Anchored scales with concrete descriptors.** The classic educational review is Jonsson & Svingby 2007, *Educational Research Review* 2(2):130–144, and it is **abstract-only (no abstract text returned)**. Its widely repeated conclusion (analytic, topic-specific rubrics with anchors and rater training improve reliability) is **recalled, not retrieved**, and is not relied on here. TICK, BiGGen and WildBench are the retrieved support for the same direction.

### 5.2 Measuring reliability

- **Cohen's κ** (two raters; Cohen 1960, not-retrieved) and **Fleiss' κ** (many raters).
  - Fleiss 1971, *Psych. Bull.* 76(5):378–382, **abstract-only**: kappa "was generalized to the case where each of a sample of 30 patients was rated on a nominal scale by the same number of psychiatrist raters (n = 6), but where the raters rating 1 s were not necessarily the same as those rating another."
- **Krippendorff's α** handles any number of raters, missing ratings and ordinal or interval data, which fits a panel where not every judge scores every item.
  - The commonly cited thresholds (α ≥ .800 to rely; .667 for tentative conclusions only; attributed to Krippendorff 2004, p. 241) are **`secondary`** here, from a web-search snippet. Hayes & Krippendorff 2007 (DOI 10.1080/19312450709336664) was not retrieved. **§9 uses these values as an explicitly chosen policy, not as a cited finding.**
- **Landis & Koch 1977** bands ("moderate", "substantial", …) are **`secondary`** and, by the secondary account, opinion-based. **Do not treat κ > 0.61 as a validated pass line.**
- **Kappa paradoxes.** Feinstein & Cicchetti 1990, *J Clin Epidemiol* 43(6), "High agreement but low kappa" (metadata retrieved, abstract text not): with skewed marginals, κ can be low while raw agreement is high, and vice versa.
  - **This is not hypothetical here.** In the third-assessor finding (§0.2) the existing assessors used only two of four verdicts, and the constant-answer baseline hit 72%.
  - **Always report raw agreement, the category marginals, κ or α, *and* the trivial-baseline agreement together.** Thakur's 80% agreement alongside π = 59 is the same trap.

### 5.3 Non-independent criteria (halo)

- Thorndike's 1920 "halo error" (not-retrieved) is the classic name for one global impression contaminating specific ratings.
- **No primary LLM-judge halo measurement was retrieved.** Two leads surfaced only as `secondary` snippets, an arXiv preprint and a practitioner blog. They are not cited.
- Stureborg's anchoring result is the nearest retrieved evidence.
- **Validation tests to run on our own rubric [DERIVED]:**
  1. **Inter-criterion correlation matrix** on the calibration set, compared with the same matrix from human experts. LLM correlations well above the human ones indicate halo.
  2. **Single-criterion perturbation test.** Edit the dossier so that only criterion C's evidence changes, for example remove the stability data. Only C's score should move. Movement in other criteria is a measured halo.
  3. **Known-groups validity.** Designs known to have failed experimentally must score lower, criterion by criterion, than designs known to have worked.
  4. **Test-retest** across paraphrased prompts and across days, since model versions drift.
  5. **Human-expert α on the rubric itself.** If experts cannot agree on a criterion with the anchors given, the LLM's score on it has nothing to be valid *against*. Drop or rewrite the criterion.

### 5.4 Why no composite score

This repo's `Assessment` record (SPEC-001) already carries seven named dimensions, each with a named reviewer,
and **no composite truth score**. The third-assessor finding explains why: "a number that averages correlated
judges looks like consensus and is not."

Adding up rubric criteria compounds halo and hides which criterion carried the decision. §9 keeps a criterion
vector and makes any scalarization an explicit, preregistered *decision rule*, reported with a weight-sensitivity
analysis. A scalar is never presented as a measurement.

---

## 6. Benchmarking and calibration: how do you know the grader is any good?

### 6.1 What makes the protein benchmarks credible (structural features, sourced)

| Feature | CASP | CAMEO | CAFA | ProteinGym |
|---|---|---|---|---|
| **Prospective blindness** | Biennial blind prediction of unreleased structures (CASP15 abstract) | "fully automated blind evaluations … based on the weekly prerelease of sequences of those structures, which are going to be published in the upcoming release of the Protein Data Bank". Predictions harvested 24–30 h after release | Annotations "allowed to accumulate over a period of 11 months" *after* the deadline, then scored | Retrospective DMS data. Supervised splits include contiguous and modulo schemes to limit positional leakage (**`secondary`** for exact definitions) |
| **Naive baselines** | — (not retrieved) | — | **Naive** (term frequency) and **BLAST** baselines. CAFA1: "33 models outperformed BLAST" in MF. CAFA3: "the performance of baseline methods has not improved since CAFA2" | Site-Independent and other simple models in the same table |
| **Significance, not point ranks** | z-score ranking with significance tests is standard practice (**not retrieved**) | — | 95% CIs by "bootstrapping with n = 10,000 iterations". Head-to-head with B = 10,000. "performance was often statistically indistinguishable between the best methods" | Aggregation corrects for proteins with many assays: "not the same as the arithmetic average across assays" |
| **Difficulty strata** | Target difficulty classes (not retrieved) | "'hard' if the average lDDT was smaller than 0.5, 'easy' if … 0.75 or higher" | No-knowledge vs limited-knowledge targets | MSA-depth, taxon and selection-type tags |
| **Published warnings about the gold standard** | — | — | Annotations "incomplete" and "error prone"; "statistical dependency between ontology terms … among protein sequences, and also the incomplete and biased nature of the experimental annotation" | Clinical labels "do not have continuous scores"; per-assay bias corrections |
| **Published non-progress** | CASP15: default AlphaFold2 "only produces the highest quality result for about two thirds of the targets" | — | CAFA3: "The rest of the 4 CAFA3 top methods did not perform as well as the top 2 methods of CAFA2"; methods "did not generalize well to selected terms" | — |
| **Independent scoring** | Independent assessors (practice; not retrieved verbatim) | Fully automated lDDT | Organisers score; predictors do not | Fixed scripts and metrics |

Sources:
- CAFA1: Radivojac et al. 2013, *Nat Methods*, PMC3584181, **full-text**.
- CAFA2: Jiang et al. 2016, *Genome Biol*, PMC5015320, **full-text**.
- CAFA3: Zhou et al. 2019, *Genome Biol*, PMC6864930, **full-text**.
- CAMEO: Robin et al. 2021, *Proteins*, PMC8673552, **full-text**. Haas et al. 2018 was not retrieved.
- CASP15: Kryshtafovych et al. 2023, *Proteins*, PMC10843301, **abstract-only**. predictioncenter.org was blocked, so **no CASP assessor warning is quoted verbatim here.**
- ProteinGym: Notin et al. 2023, bioRxiv 10.1101/2023.12.07.570727, **README and project page full-text, paper not retrieved**.

**The pattern, stated as a rule.** A benchmark is credible when:
- the scorer is fixed before predictions exist;
- the answers do not exist yet when predictions are made;
- a dumb baseline is always on the table;
- results come with resampled uncertainty and honest ties;
- the organisers say in print what is wrong with their gold standard.

### 6.2 An in-repo illustration: per-item variance dwarfs leaderboard gaps

Computed today from `findings/proteingym-spearman-dms-level.csv`, which is already in this repo: 217 assays
× 97 zero-shot predictors. These are **plain means**, not ProteinGym's bias-corrected aggregate.

- **Top five by mean Spearman** span **0.512–0.542**, a spread of 0.03.
- **Per-assay range of the top model** runs from **0.064 to 0.866**.
- **Site-Independent baseline mean** is 0.369.
- **The best model on average is the per-assay winner on only 25 of 217 assays.** 46 different predictors are the best on at least one assay.

**Lesson for the kernel [DERIVED]:** a method's rank depends heavily on *which items* are in the set. Any grader
accuracy number must therefore come with its item-level spread and a bootstrap over items, and a small
calibration set will give an unstable grader ranking. That is the item-sampling analogue of §3's Δ_K problem.

### 6.3 In-silico design metrics: a validated filter, not a ranker

- **Bennett et al. 2023**, "Improving de novo protein binder design with deep learning", *Nat Commun* 14:2625, PMC10163288, **full-text**:
  - AF2 pAE_interaction "was extremely effective in identifying the experimentally confirmed binders … with sharp increases in success rates for designs with pAE_interaction <10".
  - Deep-learning filtering "increases design success rates nearly 10-fold".
  - The Rosetta energy baseline "provided little discriminatory power".
- **This is the model for how an instrument earns trust**: a large prospective wet-lab set, a stated threshold, and a measured enrichment over a baseline.
- Counter-evidence that in-silico metrics poorly rank *affinity* among binders in open competitions (Adaptyv Bio
  rounds) surfaced only as **`secondary`** snippets; the primary was DNS-blocked. **It is not cited for any
  number.** It is a lead to retrieve before any instrument is allowed to *rank* rather than *filter*.
- **Instrument robustness is itself measurable.** Jha et al., "Protein Folding Neural Networks Are Not Robust", arXiv 2109.04460, **full-text**:
  - For RoseTTAFold (despite the title's generality), adversarial sequences within "20 units in the BLOSUM62 distance" yield predicted-structure RMSD from "0.119Å to 34.162Å".
  - Caveat: the true structures of the perturbed sequences are unknown, so this shows instability, not error.

### 6.4 Measuring the grader before trusting it

The protocol in §9 (stage S3) operationalizes these. They are taken from the sources above and from this repo's
own rules 1 and 8 (a paired mutant that must fail; a control whose answer is known in advance, in both directions).

1. **Known-answer items** (positive controls): candidate pairs whose order is settled by prospective experimental outcome.
2. **Seeded known-bad items** (negative controls), constructed per artifact type, including:
   - (a) scrambled or nonsensical artifacts;
   - (b) a **must-fail mutant** of each real candidate with one fatal flaw injected, for example a deleted catalytic residue or a frameshift in an edit stack;
   - (c) a **null dossier**: confident, well-formatted prose with no content. This tests the Zheng 2025 null-model failure.
   - (d) **authority-decorated** and **length-padded** variants of a mediocre candidate.
   - The must-fail control must be genuinely impossible, not merely unfamiliar. Rule 8's `9ZZZ.cif` story is the cautionary case.
3. **A trivial baseline**, for example "always prefer the longer dossier" or "always the majority class". The grader must beat it. §0.2 is why.
4. **Chance-corrected agreement with human experts** on a labelled subset, reported with the marginals.
5. **Hidden interleaving.** Controls go into the live stream unflagged, so the grader is measured under the
   conditions it scores under. This is CAMEO's continuous-evaluation idea applied to the grader.

---

## 7. Generation strategies: quality versus diversity

### 7.1 The default is collapse

- **Jiang et al. 2025**, "Artificial Hivemind: The Open-Ended Homogeneity of Language Models (and Beyond)", arXiv 2510.22954, **full-text**:
  - Within one model, even at top-p 0.9 and temperature 1.0, "in 79% of cases, the average similarity exceeds 0.8".
  - With min-p decoding, "81% of response pairs still exceed 0.7 similarity and 61.2% exceed 0.8".
  - **Across models**, "the average pairwise similarity between responses from different models ranges from 71% to 82%".
  - **Implication:** a swarm of agents built on different frontier LLMs is *less diverse than it looks*. Model-family diversity is not design diversity.
- **Kirk et al. 2024**, arXiv 2310.06452, **full-text**: "RLHF significantly reduces output diversity compared to SFT across a variety of measures".
- **Padmakumar & He 2024**, arXiv 2309.05196, **full-text**: writing with InstructGPT (but not base GPT-3) "results in a statistically significant reduction in diversity."
- Caveat: these measure text diversity with embedding similarity. **Design diversity must be measured in the artifact's own space**, for example sequence identity or TM-score clustering for proteins.
  - RFdiffusion (Watson et al. 2023, *Nature*, PMC10468394, **full-text**) quantifies its outputs' diversity "by pairwise TM-scores".

### 7.2 Methods that resist collapse

- **Novelty search.** Pugh, Soros, Stanley 2016, "Quality Diversity: A New Frontier for Evolutionary Computation", *Frontiers in Robotics and AI*, **full-text**:
  - "in some domains (particularly those that are deceptive), NS quickly finds the global optimum even when objective-based approaches consistently fail."
  - They also warn that "some choices of characterization can make finding QD more difficult, which on sufficiently deceptive problems can translate into an inability to find the best solutions altogether."
  - Lehman & Stanley 2011, the original, is **abstract-only** (the agent's note; not re-checked) and nothing is quoted from it.
- **MAP-Elites.** Mouret & Clune 2015, "Illuminating search spaces by mapping elites", arXiv 1504.04909, **full-text**:
  - It keeps one elite per cell of a user-chosen grid of *behaviour descriptors* and "illuminates the fitness potential of each area of the feature space, including tradeoffs between performance and" the chosen features.
  - The output is an archive, not a single winner.
- **CMA-ME** (Fontaine et al., arXiv 1912.02400, full-text): a more sample-efficient emitter for MAP-Elites.
- **LLMs as mutation operators inside QD:**
  - ELM (Lehman et al. 2022, 2206.08896, full-text).
  - QDAIF (Bradley et al. 2023, 2310.13032, full-text): "QDAIF covers more of a specified search space with high-quality samples than do non-QD controls", with "reasonable agreement between AI and human evaluation".
  - **Caveat: QDAIF uses an LLM to judge both quality and diversity, so every §1 bias is inside its loop.**
- **Island models.**
  - FunSearch (Romera-Paredes et al., *Nature* 2023/24, PMC10794145, **full-text**): "Preserving and encouraging diversity of programs in the database is crucial to enable exploration and avoid being stuck in local optima. To encourage diversity, we adopt an islands model". It periodically discards the worst half of the islands and reseeds them from survivors.
  - AlphaEvolve (Novikov et al. 2025, arXiv 2506.13131, **full-text**): its database is "inspired by a combination of the MAP elites algorithm and island-based population models".
- **Rainbow Teaming** (Samvelyan et al. 2024, 2402.16822, full-text) applies MAP-Elites to *adversarial prompts*, reaching "an attack success rate exceeding 90% across all tested models" with a diverse archive.
  - **That makes it the right tool for generating the adversarial probes in §8 and §9: a QD archive of attacks on our own judge.**

### 7.3 Recommendation for generation [DERIVED]

- Per artifact type, define 2–3 **behaviour descriptors in the artifact's own space**, for example fold class × length bin for proteins, or edit count × target locus class for edit stacks.
- Run a MAP-Elites-style archive with islands.
- The kernel ranks *within and across cells*, and the shortlist is drawn from multiple cells. A cell-coverage report ships with every ranking.
- Diversity is measured with domain metrics, never with prose embeddings of the rationale.

---

## 8. Goodhart and reward hacking

### 8.1 Taxonomy

**Manheim & Garrabrant 2018**, "Categorizing Variants of Goodhart's Law", arXiv 1803.04585, **full-text**, defines four variants:
- **Regressional**: "selection for an imperfect proxy necessarily also selects for noise".
- **Extremal**: the proxy–goal relationship breaks at extreme values.
- **Causal**: intervening on the proxy breaks the link.
- **Adversarial**: an agent with different goals games the proxy.

A design swarm optimizing against an LLM judge is exposed to all four. Regressional is guaranteed even with no
adversary: the winner of a noisy judge is partly the luckiest draw. That is the winner's-curse reason to re-score
the shortlist with fresh judges (§9 S7).

### 8.2 Documented cases where optimizing a scorer produced garbage that scored well

All from retrieved full text.

| Case | What happened | Source |
|---|---|---|
| **Sorting "repair"** | GenProg, scored on whether the output was sorted, "entirely short-circuited the buggy program, having it always return an empty list, exploiting the technicality that an empty list was scored as not being out of order" | Lehman et al. 2018, "The Surprising Creativity of Digital Evolution", arXiv 1803.03453 |
| **Deleting the answer key** | Fitness compared output to target files; "one of the individuals had deleted all of the target files when it was run! With these files missing, because of how the test function was written, it awarded perfect fitness scores to the rogue candidate and to all of its peers" | same |
| **Sleeping past the CPU limit** | Under a CPU-usage cap, "GenProg produced programs that slept forever, which did not count toward CPU usage limits" | same |
| **Crashing the opponent** | Evolved tic-tac-toe players requested moves "very, very far away"; opponents expanded their boards "and crashed because they ran out of memory, forfeiting the match" | same |
| **Frozen reward model** | Agents trained against a frozen learned reward model: "the agent learns to exploit undesired loopholes in the reward function … dramatically increasing the predicted reward with behaviors that diminish the true score." Online re-labelling fixed it | Ibarz et al. 2018, arXiv 1811.06521 |
| **Null model tops LLM-judged leaderboards** | "even a "null model" that always outputs a constant response (irrelevant to input instructions) can cheat automatic benchmarks and achieve top-ranked win rates: an **86.5% LC win rate on AlpacaEval 2.0**; an **83.0 score on Arena-Hard-Auto**; and a **9.55 score on MT-Bench**." Length control did not stop it | Zheng et al. 2025 (ICLR), "Cheating Automatic LLM Benchmarks", arXiv 2410.07137 |
| **Universal phrases inflate judge scores** | "short universal adversarial phrases can be concatenated to deceive judge LLMs to predict inflated scores … when transferred to unseen models, scores can be drastically inflated such that irrespective of the assessed text, maximum scores are predicted." "judge-LLMs are significantly more susceptible … when used for absolute scoring, as opposed to comparative assessment" | Raina, Liusie, Gales 2024, arXiv 2402.14016 |
| **Length is most of RLHF** | "purely length-based reward reproduces most downstream RLHF improvements over supervised fine-tuned models" | Singhal et al. 2024 (COLM), arXiv 2310.03716 |
| **Overoptimization has a shape** | Gold-RM score vs d = √KL (the √ sign is garbled in the PDF text; reconstructed): "Rbon(d) = d(αbon − βbon d)" for best-of-n and "RRL(d) = d(αRL − βRL log d)" for RL. Both rise, then fall. Larger policies show "very similar amounts of overoptimization" | Gao, Schulman, Hilton 2022, arXiv 2210.10760 |
| **Phase transitions** | "capability thresholds at which the agent's behavior qualitatively shifts, leading to a sharp decrease in the true reward … pose challenges to monitoring" | Pan, Bhatia, Steinhardt 2022, arXiv 2201.03544 |
| **Optimizing against a monitor teaches hiding** | "with too much optimization, agents learn obfuscated reward hacking, hiding their intent within the CoT while still exhibiting a significant rate of reward hacking" | Baker et al. 2025, arXiv 2503.11926 |
| **Biological design: oracles get fooled** | Offline model-based optimization yields designs that "fool" the learned model "into predicting a high" value; such models assign "erroneously high values at unseen and poor designs." CbAS (Brookes 2019) likewise targets oracle "pathological behaviour" away from the training data | Trabucco et al. 2021 (COMs), arXiv 2107.06882; Brookes, Park, Listgarten 2019, arXiv 1901.10060 |

Two framing results:
- **Skalse et al. 2022**, "Defining and Characterizing Reward Hacking", arXiv 2209.13085, **full-text**: over all stochastic policies, "two reward functions can only be unhackable if one of them is constant." **An unhackable non-trivial proxy does not exist in general.** Defence is about limiting optimization pressure and detecting divergence, not about finding a perfect scorer.
- **Amodei et al. 2016**, "Concrete Problems in AI Safety", arXiv 1606.06565, **full-text**: the standard catalogue that names reward hacking as a problem class.

### 8.3 Structural defences: measured versus proposed

| Defence | Status | Evidence |
|---|---|---|
| **Held-out "gold" scorer** to measure the proxy–gold gap | **Measured as a diagnostic.** Gao's whole methodology is a held-out gold RM that reveals overoptimization the proxy hides | 2210.10760 |
| **Limit optimization pressure** (KL penalty, best-of-n with small n, early stopping) | **Measured.** Gold score is non-monotone in √KL, so there is an optimum and then decline | 2210.10760 |
| **Ensembles / conservative aggregation** | **Measured, with a negative result.** Coste et al. 2024: "conservative optimization practically eliminates overoptimization and improves performance by up to 70% for BoN sampling" (synthetic gold RM). **But** Eisenstein et al. 2024, "Reward Model Ensembles Mitigate but do not Eliminate Reward Hacking": "ensembles do not eliminate reward hacking … because all reward models in the ensemble exhibit similar error patterns." Pretraining-seed diversity beat fine-tuning-seed diversity | 2310.02743; 2312.09244 (full-text) |
| **Conservative objective models / trust regions** in biological model-based optimization | **Measured on benchmarks** (Design-Bench, 2202.08450). Training against adversarially generated designs penalizes out-of-distribution highs | 2107.06882; 1901.10060 |
| **Online re-labelling** (the scorer keeps learning from the optimizer's outputs) | **Measured** in Atari (Ibarz); fixes loopholes interactively | 1811.06521 |
| **Pairwise rather than absolute scoring** | **Measured** for universal-phrase attacks: absolute scoring is "significantly more susceptible" | 2402.14016 |
| **Do not optimize against the monitor** | **Measured as necessary.** Baker: optimizing against the CoT monitor produced obfuscation, so pay a "monitorability tax" | 2503.11926 |
| **Hiding the scorer from the optimizer** (judge prompts, rubric anchors, calibration items) | **Proposed, not directly measured.** Zheng 2025 note their cheat transfers even when the benchmark instructions are private; that is evidence that hiding helps less than hoped against *generic* exploits | 2410.07137 |
| **Scorer rotation** | **Proposed.** No retrieved measurement. The rationale follows from Eisenstein (shared error patterns) and from the transfer results | — |
| **Adversarial probes and red-teaming the judge** with a QD archive of attacks | **Method measured** (Rainbow Teaming finds diverse attacks at >90% success). **Its use as a defence for a judge is proposed** | 2402.16822 |

---

## 9. Recommendation: Evaluation Kernel v0

A single procedure applied to every artifact type. Type-specific knowledge enters only through a **type adapter**
(9.2), never by changing the procedure.

### 9.1 Principles

1. **No verdict counts from an unqualified grader.** Qualification is measured on known answers before use and monitored continuously after (§6.4).
2. **A failed control voids the round.** The output is then `NO_RANKING` with the reason. This mirrors rule 8: a check that cannot come back empty has not been tested.
3. **Indistinguishable is a first-class result.** The kernel outputs ordered *tiers* with CIs, not a total order (§3, CAFA).
4. **The output is a prediction.** It is recorded as `Evidence` with `evidence_kind: "predicted"`. A ranking is never `observed`. Rule 6 applies: proved, simulated and observed stay in separate columns.
5. **The generator never sees the scorer**, and one scorer is held out from all feedback (§8).
6. **Everything is frozen and hashed before the first verdict.** That covers prompts, rubric, panel, calibration set, schedule seed and decision rule. Hash the bytes on disk (rule 2).

### 9.2 Components

| Component | Definition |
|---|---|
| **Artifact** | Any candidate. It has an immutable content hash and a type tag. |
| **Type adapter** (one per artifact type: protein, actuator, scaffold, edit stack, mechanism) | Supplies: (a) a **canonical dossier renderer**; (b) **instruments**, i.e. deterministic computational checks with versions, for example structure-prediction self-consistency or off-target scans; (c) **behaviour descriptors** for the generation archive; (d) the **rubric**; (e) a **calibration set**; (f) a **mutant generator** for must-fail controls. **No adapter is admitted until its rubric and calibration set have passed S3 once.** |
| **Rubric** | 3–8 criteria. Each is binary or a 3-point anchored scale with concrete descriptors and a stated *evidence requirement* (which instrument output or document section supports it). Instance-specific checklist items are allowed (§5.1). Every criterion has expert inter-rater α measured on the calibration set (§5.3 test 5). |
| **Calibration set** | At least 30 labelled pairs **[DERIVED minimum; §6.2 shows small sets are unstable]**, drawn from three sources: **known-answer pairs** (order settled by experimental outcome); **seeded negatives** of four kinds: scrambled, must-fail mutant, null dossier, authority/length-padded; **expert-labelled pairs**, with expert α reported. Partitioned into a *qualification* split and a *hidden-interleave* split. **Never shown to the generator.** |
| **Judge** | A (model ID + version string + prompt hash + temperature + parameters) tuple. A model update is a new judge and must re-qualify. |
| **Panel** | At least 3 qualified judges from at least 2 model families. **Excluded: any judge from the same model family as any agent that generated candidates in the round** (self-preference, §1.4). |
| **Held-out judge** | One qualified judge whose verdicts are never fed back to generators in any form. Used only at S7. |

### 9.3 Stages

**S0 Freeze and preregister.**
- Write a preregistration (in the style of `preregistrations/`) that names:
  - the artifact set or generation budget;
  - the rubric version and panel;
  - the calibration-set hash and the schedule and its seed;
  - k (the shortlist size);
  - the **decision rule** (§9.5) and the **void conditions** (§9.4).
- Record sha256 and `git hash-object` for every frozen file.

**S1 Normalize and deduplicate.**
- Render each artifact to a canonical dossier with these properties:
  - opaque ID;
  - **no agent or model identity, no "proposed by", no swarm-preference signals**;
  - citations either replaced by retrieved and verified evidence links with read-levels, or removed (authority bias, §1.5);
  - fixed section order;
  - a **hard length cap per section** (verbosity, §1.3).
- Cluster near-duplicates in the artifact's own space (sequence identity or TM-score for proteins). Keep one representative per cluster and record the cluster sizes (clone inflation, §3.1).

**S2 Instruments.**
- Run the adapter's deterministic checks and record each one as `Evidence` (`simulated` or `predicted`) with tool version, inputs hash and output.
- Hard failures are **excluded from ranking and reported**, not silently dropped.
- Each instrument has its own positive and negative control run in the same batch (rule 8).
- Instruments **filter**. Using an instrument to **rank** requires an enrichment measurement like Bennett's (§6.3).

**S3 Qualify judges** (before any candidate verdict counts). Run each judge on the qualification split, in both
orders, per criterion. A judge is admitted to the panel only if **all** of the following hold. The thresholds are
**policy choices**, not cited findings:

| Gate | Threshold |
|---|---|
| Accuracy on known-answer pairs | Bootstrap 95% CI lower bound above the **best trivial baseline** (longer-dossier, majority-class, first-position) |
| Seeded-negative rejection | ≥ 95% of must-fail mutants and null dossiers lose to their real counterparts |
| Swap consistency | ≥ 0.80 on the qualification split. Below that, swap-and-tie would leave too few decisive pairs |
| Chance-corrected agreement with expert labels (per criterion) | Krippendorff α ≥ 0.667 to be used at all; ≥ 0.800 for the criterion to enter the decision rule. These thresholds are `secondary`-sourced (§5.2) and adopted as policy |
| Perturbation (halo) test | A single-criterion evidence edit moves the targeted criterion and not the others, beyond the judge's own re-run noise |
| Parse integrity | 100% of responses parsed, or failures logged with stop reason and usage; a parse-failure rate above 2% voids qualification. Third-assessor lesson: the survivors of a 46% loss "were whatever was cheap to think about" |

**S4 Judge.** For each criterion **separately** (one call per criterion, §1.1 anchoring):
- **Pairwise**, both orders. If a judge's verdict differs between orders, it is a **tie** for that judge.
- **Reference-guided:** the judge receives the dossier *including instrument outputs*, framed as the evidence to grade against. This is the largest measured mitigation (§2.1).
- Output format: the verdict ({A, B, tie}), then a ≤ 3-sentence rationale citing dossier sections. Rationale-after is the variant with positive evidence; CoT-before showed null or negative effects (§2.2). Record both.
- Paraphrase the judge prompt across panel members, from a frozen set of at least 3 paraphrases, so that repeated judgments are less correlated (§2.3; untested, so its benefit is measured in S6, not assumed).
- **Schedule:**
  - n ≤ 30 after dedup: full round-robin.
  - n > 30: a random design of at least 3·n·ln n distinct pairs, then adaptive allocation to pairs straddling the provisional top-k boundary, keeping at least 20% of the remaining budget random (§3.2 rule 5, [DERIVED]).
- **Hidden interleave:** 10–20% of all calls are calibration-split items, indistinguishable from live ones.
- No debate and no consultancy in this stage (§4.4).

**S5 Aggregate.**
- Per criterion, fit a **regularized BT** model (ridge on log-scores). Also compute **Copeland win counts** as a model-free cross-check (§3.1). If the two disagree on top-k membership, report both and flag non-transitivity.
- **Uncertainty:** bootstrap (≥ 1,000 resamples) over *artifacts, judges and paraphrases jointly*.
- **Rank = 1 + the number of artifacts whose CI lies entirely above** (Arena rule). Report tiers.
- Report per-judge and per-family agreement (Fleiss κ or α across the panel) and **the trivial-baseline agreement beside it**.

**S6 Monitor controls.** Before any result leaves the kernel, check the hidden-interleave items and the round's
seeded negatives. The void conditions are in §9.4.

**S7 Held-out and adversarial re-score.**
- **Held-out judge:** the top-k tier plus the next tier are re-judged by the held-out judge. Report the proxy-vs-held-out rank correlation. A large drop is the Goodhart signal (§8.3, Gao's gold-vs-proxy gap applied to judges).
- **Fresh-draw re-score:** the shortlist is re-judged with a new paraphrase set. This addresses regressional Goodhart, the winner's curse (§8.1).
- **Adversarial probe set:** each round, apply a standing archive of judge attacks to a mediocre real candidate and confirm it does not climb. The archive covers authority decoration, length padding, the null dossier and universal-phrase-style suffixes, and is grown QD-style as in Rainbow Teaming (§7.2).

**S8 Emit.**
- Write the result as `Evidence` (`evidence_kind: "predicted"`, `method` = the kernel version and preregistration ref, `limitations` ≥ 1).
- Each criterion-level verdict becomes an `Assessment.dimensions[*]` entry with a named reviewer (judge tuple) and `evidence_links`. The `independence_rationale` states the panel families and the generator exclusion.
- No composite truth score (§5.4). Where a decision needs one scalar, see §9.5.

**S9 Prospective scoring of the grader** (CAFA-style, continuing). When experimental outcomes arrive for shortlisted or
control artifacts, score the kernel's *earlier* predicted order against them and publish the result, including
non-progress. **The kernel's credibility is its prospective record and nothing else.** Graders that predicted badly
lose qualification. The outcomes join the known-answer calibration set, which then grows from real results.

### 9.4 Void conditions (any one → `NO_RANKING`, with the reason recorded)

1. Any panel judge fails a S3 gate, and fewer than 3 qualified judges or fewer than 2 families remain.
2. On hidden-interleave items, any judge's accuracy CI lower bound falls to or below the trivial baseline.
3. Any seeded negative (null dossier, must-fail mutant) ranks **above the median real candidate** on any criterion.
4. Adversarial probes lift a mediocre candidate into the top-k tier.
5. The panel-level α on a criterion is below 0.667. That criterion is reported as **unreliable** and excluded. If it was required by the decision rule, the round is void.
6. Parse failures above 2% in S4.
7. Any frozen file's hash differs from the preregistration.

### 9.5 Decision rule (when a single choice must be made)

- Preregister one of:
  - (a) **lexicographic** over criteria in a stated order, using tiers, not point estimates;
  - (b) **Pareto shortlist**: every candidate not dominated at the tier level;
  - (c) a **weighted sum** with preregistered weights, accompanied by a sensitivity analysis showing the top-k under ±50% perturbation of each weight.
- If the selection changes under that perturbation, the output says so and lists every candidate that enters.
- Ties at the cut are broken **only by additional evidence** (more comparisons, an instrument, an experiment), never by a coin or by the point estimate.

### 9.6 What must be recorded for the result to be re-checkable

| Record | Content |
|---|---|
| Preregistration | Everything in S0, with on-disk sha256 and git blob hash |
| Artifacts | Content hash, type, generator agent and model (**stored, never shown to judges**), cluster membership |
| Dossiers | Rendered bytes and hash, renderer version, removed-citation log |
| Instruments | Tool name and version, parameters, input hash, raw output, control outcomes |
| Judge calls | Judge tuple (model ID, version string, prompt hash, paraphrase ID, temperature, seed if any), pair, order, criterion, raw response, parsed verdict, rationale, stop reason, token usage, wall time, whether the item was a hidden control |
| Qualification | Per-judge, per-criterion metrics, bootstrap CIs, trivial-baseline values, pass or fail per gate |
| Aggregation | Code version, bootstrap seed and count, BT and Copeland outputs, CIs, tiers |
| Controls | Interleave accuracy, seeded-negative ranks, adversarial-probe outcomes, void checks |
| Held-out re-score | Held-out judge outputs and proxy-vs-held-out correlation |
| Decision | Rule applied, sensitivity analysis, final shortlist or `NO_RANKING` with reason |
| Prospective log | Later experimental outcomes linked back to the predicted ranks |

The test of the record: a second party with the record and API access to the same model versions must be able to
(i) reproduce every number in S5 from the raw judge responses alone, with no model calls, and (ii) re-run any
subset of judge calls and get verdicts within the measured re-run noise.

### 9.7 Cost sketch [DERIVED]

For n = 30 after dedup, 5 criteria, a panel of 3, both orders, full round-robin:
- 435 pairs × 2 orders × 5 criteria × 3 judges = **13,050 judge calls**;
- plus about 15% hidden controls (about 2,000);
- plus qualification (30 pairs × 2 × 5 × 3 = 900 per judge candidate);
- plus the held-out re-score.

That is affordable for a decision that precedes wet-lab spend. Where it is not, reduce n at S2, not the controls.

### 9.8 What this kernel deliberately does not claim

- It does not make an LLM judge correct about biology. It measures whether the judge beats trivial baselines and
  agrees with experts and known outcomes **on the calibration distribution**, and it voids rounds where that
  measurement fails. Live candidates may lie outside that distribution, and novel designs are by definition
  likely to. **A judge qualified on known designs can still fail silently on unknown ones.** That is why S9
  exists and why the output is labelled `predicted`.
- It does not resolve the correlated-judges problem from §0.2. Cross-family panels reduce it. Inter-model
  similarity of 71–82% (§7.1) and GPT-4/Claude-3-Opus correlation of about 0.7 (§2.3) say it remains. Only
  prospective ground truth breaks it.

---

## 10. Open questions this research could not settle

1. **No in-domain grader study exists in what we retrieved.** The first experiment this kernel should run is
   on itself: S3 on a protein calibration set with experimental outcomes, for example published binder
   campaigns with reported hit and non-hit sets. This is a measurement, not a feature.
2. **Swiss vs round-robin vs adaptive for LLM judges:** no retrieved source.
3. **Cross-family vs same-family panels at matched cost:** not measured.
4. **Whether prompt paraphrase actually decorrelates repeated judgments:** not measured.
5. **Halo in LLM multi-criterion judging:** no primary measurement retrieved.
6. **Whether in-silico metrics *rank* affinity among binders** (as opposed to filtering binders from non-binders): only `secondary` evidence, which points negative.

---

## Appendix A. Read-level ledger

**`full-text`** (retrieved and searched this session):
- **Judging:** Zheng 2023 (2306.05685); Wang 2023 (2305.17926); Shi 2024 (2406.07791); Saito 2023 (2310.10076); Dubois 2024 (2404.04475); Panickssery 2024 (2404.13076); Wataoka 2024 (2410.21819); Liu 2023 G-Eval (2303.16634); Chiang & Lee 2023a (2305.01937) and 2023b (2310.05657); Kim 2023 Prometheus (2310.08491); Kim 2024 Prometheus 2 (2405.01535); Zhu 2023 JudgeLM (2310.17631); Thakur 2024 (2406.12624 v6); Stureborg 2024 (2405.01724); Chen 2024 (2402.10669); Ye 2024 CALM (2410.02736); Koo 2023 CoBBLEr (2309.17012); Sharma 2023 (2310.13548); Verga 2024 PoLL (2404.18796); Chan 2023 ChatEval (2308.07201); Huang 2023 (2310.01798).
- **Ranking:** Yan 2014 (1411.1168); Negahban et al. (1209.1688); Chen & Suh 2015 (1504.07218); Chen, Fan, Ma, Wang 2019 (1707.09971); Shah & Wainwright 2018 (1512.08949); Heckel et al. 2019 (1606.08842); Jamieson & Nowak 2011 (1109.3701; quotes from the abstract); Bengs et al. survey (1807.11398, sections); Chiang 2024 Chatbot Arena (2403.04132); Boubdir 2023 (2311.17295); Balduzzi 2018 (1806.02643); Herbrich et al. 2006 TrueSkill (MSR PDF).
- **Debate:** Irving 2018 (1805.00899); Parrish 2022a (2204.05212); Parrish 2022b (2210.10860); Michael 2023 (2311.08702); Khan 2024 (2402.06782); Kenton 2024 (2407.04622); Du 2023 (2305.14325); Smit 2024 (2311.17371); Wang 2024 (2402.18272); Choi 2025 (2508.17536); Brown-Cohen 2024 (2311.14125, intro only).
- **Benchmarks:** Radivojac 2013 CAFA1 (PMC3584181); Jiang 2016 CAFA2 (PMC5015320); Zhou 2019 CAFA3 (PMC6864930); Robin 2021 CAMEO (PMC8673552); Bennett 2023 (PMC10163288); ProteinGym README and project page; Jha 2021 (2109.04460).
- **Generation and Goodhart:** Jiang 2025 Artificial Hivemind (2510.22954); Kirk 2024 (2310.06452); Padmakumar & He 2024 (2309.05196); Watson 2023 RFdiffusion (PMC10468394); Pugh 2016 (Frontiers); Mouret & Clune 2015 (1504.04909); Fontaine CMA-ME (1912.02400); Lehman 2022 ELM (2206.08896); Bradley 2023 QDAIF (2310.13032); Romera-Paredes FunSearch (PMC10794145); Novikov 2025 AlphaEvolve (2506.13131); Samvelyan 2024 Rainbow Teaming (2402.16822); Manheim & Garrabrant 2018 (1803.04585); Lehman et al. 2018 Surprising Creativity (1803.03453); Ibarz 2018 (1811.06521); Zheng 2025 null models (2410.07137); Raina 2024 (2402.14016); Singhal 2024 (2310.03716); Gao 2022 (2210.10760); Pan 2022 (2201.03544); Baker 2025 (2503.11926); Trabucco 2021 COMs (2107.06882); Brookes 2019 CbAS (1901.10060); Trabucco 2022 Design-Bench (2202.08450); Skalse 2022 (2209.13085); Amodei 2016 (1606.06565); Coste 2024 (2310.02743); Eisenstein 2024 (2312.09244).

**`abstract-only`:** Braverman & Mossel 2008 (0707.1051); Kryshtafovych 2023 CASP15; Fleiss 1971; Cook 2024 TICK (2410.03608); Lin 2024 WildBench (2406.04770); Kim 2024 BiGGen (2406.05761); Hashemi 2024 LLM-Rubric (2501.00274); Lehman & Stanley 2011 (agent's note, not re-checked); Jonsson & Svingby 2007 (metadata only, no abstract text); Feinstein & Cicchetti 1990 (metadata only).

**`secondary` (not load-bearing):** Krippendorff α thresholds; Landis & Koch bands and their critique; ProteinGym CV-split definitions; Adaptyv Bio competition results; LLM-judge halo preprint and blog.

**`not-retrieved`:** Bradley & Terry 1952; Zermelo 1929; Ford 1957; Hunter 2004; Yue et al. 2012; Cohen 1960; Thorndike 1920; Haas et al. 2018 (CAMEO); the CASP assessment papers' bodies; the LMSYS Elo→BT blog; Krakovna's specification-gaming list; METR's reward-hacking report. Fannjiang & Listgarten 2020 (2006.08052) was downloaded in full but **not read**, and nothing is quoted from it.

## Appendix B. Retrieval blocks encountered

predictioncenter.org (proxy 403); export.arxiv.org (403); proteingym.org, adaptyvbio.substack.com, afhayes.com,
lmsys.org, openai.com, deepmind.google, vkrakovna.wordpress.com (not allowed in this session's network policy);
biorxiv.org (HTTP 429). Each is the reason one or more items above sit below `full-text`.
