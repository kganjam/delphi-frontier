# Challenge 26: does Boltz2's confidence on the kcnk5b tail track MSA depth rather than disorder?

**Claim under review (claim 26, from commit `699500a7` on `origin/swarm-architecture`):**
"An MSA-dependent model's confidence tracks ALIGNMENT DEPTH, not disorder: PDB70 depth falls to
0.0 from residue 326 because crystallised K2P constructs are truncated, and Boltz2 reads 41.4 there
while MSA-independent ESMFold2 reads 76.4."
Recorded evidence level: *derived*. Value: 76.4 mean pLDDT.

**Verdict: WEAKENED.** The 76.4 reproduces exactly. The 41.4 does not reproduce for the stated
window. The depth profile cannot be reproduced from anything committed. And the claim's central
contrast, "depth, not disorder", is contradicted by the ESMFold2 structure's own geometry and by
the sequence.

Inputs read (all full-text, read from git objects in this repo):
- `results/fish-proteins/structures/kcnk5b_esmfold2.cif` and `kcnk5b_boltz2.cif` @ `699500a7`.
  Each has 3,582 atoms, one chain and 448 residues. I parsed both by the names in the
  `_atom_site.` header, because the ESMFold2 CIF puts its columns in a non-standard order.
- `results/fish-proteins/Q6PFU3.fasta` (448 aa) and `kcnk5b-HITS.md` @ `699500a7`.
- `results/mol-sims/claude-20261101/structures/msa/kcnk5b_core.a3m` on `origin/claude/mol-sims-20261101`.
  This is a **different** PDB70 MSA (76 rows) for a **1–265 construct**. It was not the MSA Boltz2 used.

## 1. Arithmetic, redone independently (calculated from the CIFs, not observed)

Mean per-residue pLDDT, read from the B-factor of each CA atom. Atom-mean per residue gives identical numbers.

| window | ESMFold2 | Boltz2 |
|---|---|---|
| whole chain 1–448 | 83.63 (matches confidence.json 0.8363) | 62.03 |
| 1–260 | 88.87 | 76.95 |
| **326–448 (the claimed window, "from 326")** | **76.43** | **36.37** |
| 261–448 | 76.38 | **41.39** |
| 262–448 | 76.32 | 41.26 |

- **ESMFold2's 76.4 over 326–448 is correct.**
- **Boltz2's 41.4 is not the value over 326–448.** Over that window Boltz2 reads **36.4**. 41.4
  reproduces only over **261–448**, the region the source commit calls "depth 0.5 past residue 261".
  ESMFold2 also reads 76.4 over 261–448 (76.38), so the quoted pair looks like the 261–448 window
  relabelled as "from 326". This is my inference from the window scan; the author's working is not
  recorded. The error happens to understate the gap: the true gap over 326–448 is 40.1 points, not 35.0.
- Over 326–448, 87.8% of Boltz2 residues sit below 50 and none above 70. For ESMFold2, 82.9% sit
  above 70 and none below 50.

## 2. Proxy check: "MSA depth" here is a relayed number, and it cannot be reproduced

The depth profile ("0.5 past 261, 0.0 from 326") came from the running agent. It was not
recomputed by anyone. `kcnk5b-HITS.md` points to `kcnk5b_pdb70.a3m`. I searched the file trees of
every remote branch in this repository for `*.a3m`, and that file **is not committed on any of
them**. The only kcnk5b A3M is `kcnk5b_core.a3m`, and it stops at residue 265. So **the depth
profile for residues 266–448 is unknown from committed artifacts**. Its evidence level should be
"relayed", not "derived".

The core A3M does allow a partial test of the mechanism over residues 1–265, where depth actually
varies (window means from 1.2 to 56.7 rows). These are calculated, and they use a proxy MSA:

- Spearman(depth, Boltz2 pLDDT) = 0.247. Spearman(depth, ESMFold2 pLDDT) = **0.363**.
- Spearman(depth, Boltz2 − ESMFold2) = **0.071**.
- Core residues with depth ≤ 5 (n = 36): Boltz2 66.9, ESMFold2 80.3.

If Boltz2's confidence were driven by depth specifically, its gap to the MSA-free model should
widen where depth is low. In the one region where this can be checked, the gap barely tracks depth
(ρ = 0.07), and the MSA-free model correlates with depth more strongly than Boltz2 does. Caveat:
this MSA is a proxy and not Boltz2's actual input.

## 3. The hidden assumption: ESMFold2's 76.4 means the tail is not disordered

The claim needs ESMFold2's high pLDDT to count as evidence against disorder. Two tests (calculated):

**Geometry of the ESMFold2 model itself.**

| | ESMFold2 core 1–325 | ESMFold2 tail 326–448 | Boltz2 tail 326–448 |
|---|---|---|---|
| helix proxy (CAᵢ–CAᵢ₊₃ in 4.5–5.6 Å) | 0.66 | **0.07** | 0.48 |
| long-range contacts per residue (CA < 8 Å, \|i−j\| ≥ 12) | 0.71 | **0.00** | 2.33 |
| contacts per residue with 1–261 (CA < 10 Å) | – | **0.00** | 3.61 |
| radius of gyration of the tail | – | **58.8 Å** | 16.2 Å |

For reference, 123 residues would have Rg of about 13.7 Å as a compact globule and about 34 Å as a
random coil (standard scaling laws). ESMFold2's tail has mean CAᵢ–CAᵢ₊₂ 6.78 Å and an end-to-end
distance of 108 Å. It is an extended ribbon with **zero tertiary contacts**, more extended than a
random coil. That is what a disordered segment looks like when a predictor draws it as one
conformer. The pLDDT of 76 sits on a structure that has no fold to be confident about. So in this
case pLDDT is a poor proxy for order (my inference).

**Sequence.** I used the repo's own FoldIndex formula. My implementation reproduces the recorded
whole-chain kcnk5b value of +0.166 exactly.
- Tail 326–448: FoldIndex **−0.094** (predicted unfolded), with 60 of 73 51-aa windows below 0.
- Core 1–260: +0.379.
- Tail composition: 21.1% Ser+Thr and 21.1% large hydrophobics, against 45.8% large hydrophobics
  in the core. It also contains an NNNN run and a basic patch (RRKKK) near its N-terminal end.

The sequence evidence points toward disorder, which is the reading the claim rejects.

**Confound.** The claim treats "depth" and "disorder" as rival explanations. But its own
explanation ("crystallised K2P constructs are truncated") makes them dependent. Constructs are
usually truncated *because* the termini are flexible. One protein cannot separate the two causes.

## 4. Evidence level

- The 76.4 is honestly **derived**: I recomputed it from the CIF.
- The 41.4 is mislabelled by window.
- The depth profile is **relayed** from the agent, and its source A3M is missing, so it cannot be
  re-derived.
- "Confidence tracks depth, not disorder" is an **interpretation**, and the artifacts contradict it.

The source commit's own hedge ("76.4 removes the evidence for disorder, it does not establish
order") is more careful than the claim text. My geometry and FoldIndex results argue that even
that hedge goes too far.

## 5. Published counterexample: deep-learning pLDDT can be high on intrinsically disordered regions

- Alderson, Pritišanac, Kolarić, Moses & Forman-Kay, *PNAS* 2023, doi:10.1073/pnas.2304302120.
  Read-level: **search-summary**; I did not read the full text.
- What it reports: AlphaFold2 gives confident pLDDT to about 15% of human intrinsically disordered
  regions, often matching a conditionally folded state.
- Why it matters here: high pLDDT on an intrinsically disordered region is a known regime, so
  ESMFold2's 76 cannot count as evidence of order by itself.
- Scope: that paper covers AlphaFold2, not ESMFold2. I found no ESMFold2-specific study and ran
  only one search for this item.

## What survives

- The two models do disagree sharply on the tail: 36.4 vs 76.4 over residues 326–448.
- Boltz2's low tail confidence and its compact, packed tail are consistent with poor MSA support.

**What does not survive:**
- that 41.4 is the value "from 326";
- that the depth profile is verified;
- that the disagreement shows the tail is *not* disordered.

The most defensible reading is narrower. Over residues 326–448 the two models disagree by about
40 pLDDT points, and the available evidence (tail geometry with no contacts, negative FoldIndex)
leans toward disorder. The low-depth explanation is plausible but unidentified.

```swarm-challenge
{"claim_id": 26, "outcome": "weakened", "reason": "Boltz2 reads 36.4 not 41.4 over 326-448 (41.4 is the 261-448 mean), the PDB70 depth profile cannot be reproduced because kcnk5b_pdb70.a3m is not committed, and ESMFold2's 76.4 sits on a contact-free extended ribbon (Rg 58.8 A, 0 long-range contacts) with tail FoldIndex -0.094, so 'not disorder' is unsupported.", "corrected_value": "Boltz2 36.4 vs ESMFold2 76.4 mean CA pLDDT over residues 326-448"}
```
