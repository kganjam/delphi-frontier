# Replication of claim 207: "CHALLENGER AUDIT" (a sampled audit of challenge.evidence)

**What kind of result this is.** These are **observations** of repository records and of published sources:
git objects, and text I fetched and searched myself. They also include **calculations**, meaning arithmetic I
redid. I made no laboratory measurement and ran no simulation. Each row below is labelled.

## Disclosure: what I could and could not see

- **I was given** only the title "CHALLENGER AUDIT" and the context line "sampled audit of challenge.evidence".
  I was **not** given the claim's statement, sample size, metric or recorded value.
- **What `challenge.evidence` is.** `db/designswarm/0001_core.sql` (branch `origin/swarm-architecture`, read in full
  around the table) defines `create table challenge (… challenger text, attack text, outcome text, evidence text …)`.
  `swarm/swarm.py` on the same branch inserts challenge rows with `outcome='not-run'` and no evidence. It tells the
  challenger to write `docs/research/fish/challenge-{cid}.md` ending in a ```` ```swarm-challenge ```` block.
- **The database could not be accessed.** `psql -h 127.0.0.1 -p 5436 -U morphoswarm -d designswarm` gave
  "Connection refused" from this container. I read **no** `challenge.evidence` row.
  - **My inference, not a verified fact:** the column is filled from the challenge documents in git. So I audited
    those documents. If the column holds something else, this audit is of the wrong object.
- **What I deliberately did not open.** I did not open `origin/claude/challenge-207-audit-yrcec6`, any file whose
  path contains `207`, `library/pages/project/claims.md`, or `corrections.md`.
  - **Caveat on that exclusion:** I removed from the population every challenge document whose text contains the
    string "207", so that I would not read the original working by accident. This removed 11 of 172 claim IDs and
    may bias the sample.
- **Disclosure on claim 208.** I read one sibling file, `challenge-208/collect.py` (claim 208, not 207), to learn the
  `swarm-challenge` block format. It contains code only, no values. I did not read the rest of the 208 work, and I
  did not read 222.
- **I defined the metric myself**, because the claim text was withheld. The recorded claim may measure something
  else, such as the honesty of evidence labels or the distribution of outcomes. In that case my number does not
  answer it.

## Method

1. **Collect** (`replicate-207/collect.py`). Gather every blob of `docs/research/fish/challenge-N.md` from the history
   of all remote branches, and parse its `swarm-challenge` block.
   - **Observed:** 215 unique blobs, all with a block, covering 172 distinct `claim_id`s.
   - **Observed:** outcomes across the blobs were weakened 151, survived 54, refuted 10.
   - **Observed:** the blocks have the keys `claim_id, outcome, reason, corrected_value, depends_on`. None has an
     `evidence` key.
2. **Population.** Keep the latest version per `claim_id` (by commit time), then drop any document mentioning "207".
   This leaves **N = 161**.
3. **Sample** (`replicate-207/sample.py`). `random.seed(20261104)` with `random.sample(pop, 10)` gives claim IDs
   **62, 109, 135, 190, 221, 6, 67, 140, 2, 201**.
4. **Audit.** In each sampled document, check the concrete evidential assertions that I can re-check
   independently: git facts, quoted values from cited papers, and arithmetic.
   - I chose 2–4 assertions per document, preferring the ones each verdict rests on.
   - This is **not** an exhaustive re-review of each document, and not an adversarial re-challenge.
5. **Metric (mine):** the fraction of sampled challenge documents whose checked evidence reproduces. The secondary
   metric is the fraction of checked assertions that reproduce.

## Inputs and checks

Calculations are in `replicate-207/checks.py`.

| # | Assertion in the challenge document | My check | Kind | Source and read-level | Result |
|---|---|---|---|---|---|
| 62 | Commit `79960f11` (2026-11-04 08:19:33 UTC) has the trailer `session_01EeoYQenugRMpZgH9iNWVH9` | `git log -1` | observation | git object, full-text | reproduces |
| 62 | That commit is not merged into main | `merge-base --is-ancestor` against `7b5ba52` (main); only its own branch contains it | observation | git, full-text | reproduces |
| 62 | Golden angle 137.5078°, Lucas angle 99.502° | 360/φ² = 137.50776; 360/(2+φ) = 99.50155 | calculation | — | reproduces |
| 109 | Shortfall 1.22–2.56×, break-even f 2.50–4.45× (full p0 range) | 0.65/(0.26·2.05) = 1.2195; 0.77/(0.173·1.74) = 2.558; 0.65/0.26 = 2.50; 0.77/0.173 = 4.451 | calculation | inputs as stated in the document | reproduces |
| 135 | k-bound kL³/3 = 4.32×10⁻⁵ N·m² | 1.98·0.0403³/3 = 4.3198×10⁻⁵ | calculation | — | reproduces |
| 135 | Isometric bound 3.4×10⁻³ N·m² (λ⁴ = 78.6) | (120/40.3)⁴ = 78.61; product 3.396×10⁻³ | calculation | — | reproduces |
| 135 | Puri et al. 2018 quote a bluegill ray EI of 3.8×10⁻⁶ N·m² (PMC5868929) | Europe PMC fullTextXML, searched: "bending stiffness of bluegill rays of 3.8×10⁻⁶ N m²". First author Puri, 2018 | observation | **full-text** | reproduces |
| 190 | L/W = 9.77 % at launch, 4.89 % at apex | ½·1.225·1.38²·192e-6·1.07 / (0.25e-3·9.81) = 0.09771; ×cos²45° = 0.04886 | calculation | — | reproduces |
| 221 | M = 1.081×10⁻⁴ N·m, d_req = 0.2601 mm | My own chain gives 1.0813×10⁻⁴ and 0.26009 mm | calculation | — | reproduces |
| 221 | "~4×" at the mid geometry is 4.06× | (0.26009/0.163)³ = 4.063 | calculation | — | reproduces |
| 6 | Perathoner 2014: wild type k = 1.29 | PMC3894163 fullTextXML: "Wild type (wt) fins … (k = 1.29)" | observation | **full-text** | reproduces |
| 6 | Perathoner 2014: alf/+ "k near 2" | same text: "allometric coefficient k near 2" | observation | **full-text** | reproduces |
| 67 | Commit `f6dec5c8` (2026-11-04 08:18 UTC) has the trailer `session_01HsfzftZ4uzxNPXv7tEXKWM` and is the tip of `glide-ratio-law-d2al63` | `git log -1`; `rev-parse` | observation | git, full-text | reproduces |
| 67 | Not merged | `merge-base` against main; `branch -r --contains` | observation | git | reproduces |
| 140 | v = √(gR) = 3.13 m/s (1 m), 2.21 m/s (0.5 m) | 3.1321; 2.2147 | calculation | — | reproduces |
| 140 | Demesmay et al. 2025: adult D. rerio maximal speed 1.57 ± 0.27 m/s (PMC12604801) | fullTextXML: "157 ± 27 cm/s for controls" | observation | **full-text** | reproduces |
| 2 | Palstra et al. 2010: Ucrit 0.548 ± 0.007 m/s, 18.0 BL/s | Europe PMC record (DOI 10.1371/journal.pone.0014483, PMC3013094): "U(crit) of 0.548±0.007 m s(-1) or 18.0 standard body lengths (BL) s(-1)" | observation | **abstract** | reproduces |
| 2 | Speed deficit 5.84/0.548 = 10.65× | 10.657 | calculation | — | reproduces |
| 2 | KE deficit "113×" | 113.57. This rounds to 114, not 113. | calculation | — | reproduces, with a cosmetic rounding slip under 0.5 % |
| 201 | Lift per fin 5.89×10⁻³ N; lever arm 18.7 mm | 3·0.4e-3·9.81/2 = 5.886×10⁻³; 1.1e-4/5.886e-3 = 18.69 mm | calculation | — | reproduces |
| 201 | Air-medium fin area ≈ 14 cm² | 5.886e-3/(½·1.2·9·0.78) = 13.97 cm² | calculation | — | reproduces |

Row count: the table has 21 rows. Several rows hold two values: 62 (two angles), 109 (two quantities), 2 (two
quoted values) and 201 (two quantities). Counting each value separately gives **27 assertions** in total. Of those,
**27 reproduce**. One (the "113×" in document 2) has a cosmetic rounding slip under 0.5 %.

## Arithmetic for the headline

- **Documents.** 10 of 10 sampled documents had all their checked evidence reproduce.
  - The point estimate is **10/10 = 100 %**.
  - The exact (Clopper–Pearson) one-sided 95 % lower bound for an all-success result is (0.025)^(1/10) = **0.692**.
  - Scaled to the population of N = 161, that bound is ≥ ~111 documents. This is a calculation, not an observation.
- **Assertions.** 27 of 27 reproduce. The lower bound is (0.025)^(1/27) = **0.872**.
  - These assertions are clustered within 10 documents, so treat this bound as optimistic.

**Uncertainty and scope.** This is a positive result **only for the claims I checked**.

- I checked 2–4 assertions per document, and I chose them, which is a selection effect.
- I checked whether the cited evidence **exists and says what the challenge says it says**, and whether the
  arithmetic is right. I did **not** check whether each verdict (weakened/survived) is the right judgement.
- Population scope: challenge documents in git on 2026-11-04, excluding the 11 claim IDs that mention "207". The
  database column itself was not accessed.

## My value

**10/10 sampled challenge documents (27/27 checked assertions) had their cited evidence reproduce.**

- The 95 % lower bound is 69 % of documents and 87 % of assertions.
- There was one cosmetic rounding slip ("113×" for 113.6×).
- This is an observation plus calculation on git documents. It is not a reading of the database column.

## Comparison with the recorded value

Done only after the value above was fixed and committed. See the section added below.
