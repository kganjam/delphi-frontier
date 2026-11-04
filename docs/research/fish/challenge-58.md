# Challenge 58: "LAWENTRY fick-diffusion dispatched"

- **Claim under attack:** "LAWENTRY fick-diffusion dispatched"
- **Recorded evidence level:** unknown. **Value:** n/a.
- **Source session:** `session_01EeoYQermc1y2miVqXjrRY4`
- **Challenger:** adversarial cloud review, 2026-11-04, about 08:19 to 08:30 UTC
- **Verdict: SURVIVED, with caveats.** The dispatch is real. It produced a law entry, the entry
  passes the library's dimension gate, and every number in it reproduced when I redid the
  arithmetic. Four things limit what a reader may infer:
  1. The entry is **not merged**.
  2. Its generated page was **never built**.
  3. The zebrafish worked example is a rescaled copy of the mammalian textbook distance. It holds no
     zebrafish information (see §3).
  4. The entry lists the Krogh capillary cylinder as inside its domain, but the stated `k = 4`
     formula does not describe that geometry (see §5).

  The claim says "dispatched". It does not say "merged", "rendered" or "verified", so none of these
  four points refutes it.

## What the claim asserts

The claim records an operation: a task to write a "fick-diffusion" law-library entry was sent out.
It contains no number and no physics. "Dispatched" is a **proxy**. What matters is whether the
library now holds a correct, gated entry for Fick diffusion. I tested both the operation and that
quantity.

## 1. Was it dispatched, and did it deliver? (observed, from git and tool output)

| Check | Method | Result | Kind |
|---|---|---|---|
| Source session transcript | not attempted | could-not-access (I did not try; challenge 53 found these transcripts unreachable) | — |
| Commit | `git fetch` of all remote branches, then `git log --all` | `origin/claude/fick-diffusion-law-nv8p7l` holds commit **`0b307d41`** (2026-11-04 08:18:19 UTC): "Add Fick diffusion law entry, with the critical length beyond which diffusive supply fails". Its `Claude-Session` trailer names **`session_01EeoYQermc1y2miVqXjrRY4`**, which is the claim's source. `git ls-remote` confirms the branch is on GitHub. | observation |
| This review's own branch | `git rev-parse` | `claude/challenge-58-fick-diffusion-gocwiq` pointed at `3272d3e` (`work/frontier-foundation`), so it is **not** evidence of the dispatch. Challenges 47 and 53 record the same trap. | observation |
| Files the commit adds | `git show --stat` | Only `library/laws/fick-diffusion.yaml` (+225). There is no page and no index row. | observation |
| Dimension gate | `library/tools/check_laws.py --dir library/laws` on a worktree at `0b307d41` | `ok fick-diffusion.yaml … 3 entries, 0 problems`. `--selftest` passes. | observation (tool output) |
| My own negative controls | Mutated the equation and re-ran the gate | Dropping the square root was **rejected** ("L^1, other side is L^2"). Multiplying by q instead of dividing was **rejected**. Dropping C0 was **rejected**. Using the exponent `^1/3` was **rejected**. The gate bites on this entry. | observation (tool output) |
| Gate quirk (not an entry fault) | Wrote the exponent as `^(1/2)` | **Rejected** as L^2. The tokenizer accepts `^1/2` but silently drops `^(1/2)`, so a correctly written equation in that form would fail the gate. This is a tool limitation; the entry uses the form that parses. | observation (tool output) |
| Page build | `library/tools/build_pages.py --check` | `{"stale": ['fick-diffusion.md', 'index.md']}`. The page was never generated. | observation (tool output) |
| Merged? | `git merge-base --is-ancestor 0b307d41 origin/main` | **NOT merged**. `origin/main` has no `library/` directory. | observation |

The link between the claim and the commit is the commit trailer only.

## 2. Arithmetic, redone independently (all CALCULATED by me, not observed)

| Entry states | My result | Match |
|---|---|---|
| Geometry factor k = 2, 4, 6 (slab, solid cylinder, sphere) | For C = C0 − q(R² − r²)/(2nD), the n-dimensional radial Laplacian of r² is 2n. That satisfies D∇²C = q with C(R) = C0 and a regular centre. The centre drop is qR²/(2nD), so k = 2n = 2, 4, 6. | yes |
| Implied q = 2·D·C0/L², with D = 2.1e-9 m²/s, C0 = 0.2 mol/m³, L = 200 and 100 µm | 0.0210 and 0.0840 mol m⁻³ s⁻¹ | yes |
| Zebrafish R_crit = √(4·2.1e-9·0.258/q), for q = 0.021 and 0.084 | 3.21e-4 m and 1.61e-4 m | yes |
| t = L²/(2D) for L = 1 µm, 100 µm, 1 mm and 1 cm | 2.38e-4 s, 2.38 s, 238 s and 2.38e4 s (6.61 h) | yes |
| Pe for 1 mm/s over 10 µm | 4.76 | yes ("about 5") |
| 8.3 mg/L and 8.24 mg/L of O2 as molar concentration | 0.259 mM and 0.2575 mM | yes |
| Dimensions of L_crit = √(k·D·C0/q) | L, confirmed by the gate and by the mutants above | yes |

I found no arithmetic error.

## 3. Proxy: the zebrafish example is the textbook number rescaled

The second worked example presents 160 to 320 µm as a CALCULATED critical radius for the zebrafish.
The entry labels q as inferred and not a zebrafish measurement, which is honest. Its q, though, comes
from the first example: q = 2·D·C0'/L², with C0' = 0.2 at 37 °C. Substituting that q gives the
following (my algebra):

R_crit = L_textbook · √((4·0.258)/(2·0.2)) = **1.606 · L_textbook**

D cancels out. The zebrafish range is therefore the mammalian "100 to 200 µm from a vessel" figure
multiplied by a fixed factor of 1.6. That factor comes only from the change of geometry factor (k from
2 to 4) and the change of surface O2 (C0 from 0.2 to 0.258). The example contains **no information
about zebrafish O2 consumption**. It also carries a 37 °C, mammalian-tissue q into a 25 °C fish. The
entry notes neither the temperature mismatch nor the circularity.

The quantity that matters is the zebrafish volumetric O2 consumption. The entry records it as
`unknown`. I did not find it either; I made no literature fetch for it in this review. The entry does
say that comparing the result with the 14 to 21 dpf transition (Rombough 2002) is UNTESTED, so
nothing false is asserted. A reader should still not treat the 160 to 320 µm range as a
zebrafish-specific estimate. This weakens one worked example. It does not touch the dispatch claim.

## 4. Hidden assumptions, relaxed

- **Zero-order kinetics.** Break (3) says the zero-order L_crit "underestimates the thickness at which
  C first touches zero" under Michaelis–Menten uptake. My inference: under q = Vmax·C/(Km + C), uptake
  becomes first-order as C → 0. The concentration then decays toward zero without reaching it at any
  finite size, so under that model the "thickness at which C first touches zero" does not exist. The
  direction the entry gives (zero-order is the conservative bound for the anoxia criterion) still
  holds. Only the wording is loose.
- **C(centre) = 0 as the failure point.** The entry already replaces C0 with C0 − C_min for a viability
  threshold, and it cites necrosis at central pO2 of 42 to 57 mmHg (search-summary level). This is
  handled.
- **D in water as an upper bound.** This is correct in direction, and the entry states it. D in tissue
  remains `unknown` in the entry, and I did not source it.

## 5. Regime the author missed: the Krogh cylinder is not the k = 4 solid cylinder

The entry credits the cylindrical case to Krogh (1919), hedged with "did not confirm the exact form".
It also lists "the tissue cylinder around one capillary (Krogh)" among the taxa in
`domain_of_validity`. Krogh's geometry is the inverse of the solid cylinder used here. Supply comes
from a central capillary of radius r_c, outward into an annulus with a no-flux outer boundary at R.
The standard Krogh–Erlang solution, which I quote **from memory** and did not check against a source
in this review, contains a logarithmic term:

C(r) = C_c − (q/4D)(r² − r_c²) + (q R²/2D) ln(r/r_c)

So √(4·D·C0/q) is not Krogh's critical radius. The k = 4 formula describes a solid rod supplied from
its outer skin, which is the zebrafish-body use, not a capillary-supplied tissue. My inference: the
Krogh item in `domain_of_validity` should cite a different equation, or the entry should drop it.
This is a content defect in the entry, not in the dispatch.

## 6. Evidence level

`unknown` is under-specified, but it overstates nothing. The accurate level is "operational record,
verified from the git trailer and tool output". Inside the entry the labels are honest. Derived
numbers are tagged CALCULATED or INVERSE, with `evidence: derived`. The only number tagged
`evidence: literature` is the spheroid viable rim, held at search-summary level. Unsourced constants
(q, D in tissue) are recorded as `unknown` and not invented. Disagreements are kept, not averaged:
230 vs 257 to 259 µM for solubility, the myoglobin knockout results, and the necrosis-onset rule. I
found no derived number presented as measured.

## 7. What I did not verify

I made no literature fetches. Every citation in the entry keeps the read level the author recorded.
My own read level for each is could-not-access, because I did not try. That covers Krogh, Harvey,
Pelster & Burggren, Rombough, Mueller-Klieser & Sutherland, Franko & Sutherland, Groebe &
Mueller-Klieser, Carmeliet & Jain, Weiss et al., Magliaro et al., Garry et al., Gödecke et al.,
Zoladz et al. and the BioNumbers entries. One phrase reads oddly to me: Franko & Sutherland
"found necrosis when the O2 diffusion distance fell below about 80 µm". I could not check whether the
direction ("fell below") matches the source. This is flagged, not refuted.

## Sources

- Git history of `kganjam/delphi-frontier`, remote branches as fetched about 08:19 UTC on
  2026-11-04, including commit `0b307d41` on `origin/claude/fick-diffusion-law-nv8p7l`. Read level:
  full-text.
- `library/laws/fick-diffusion.yaml`, `library/tools/check_laws.py` and `library/tools/build_pages.py`
  at `0b307d41`. Read level: full-text.
- `docs/research/fish/challenge-53.md` on commit `cb5758d0` (precedent and format). Read level:
  full-text.
- Source session transcript. Read level: could-not-access (not attempted).
- Krogh–Erlang solution: from memory. Read level: could-not-access.

```swarm-challenge
{"claim_id": 58, "outcome": "survived", "reason": "Commit 0b307d41 (08:18:19 UTC, Claude-Session trailer matching the source session) adds library/laws/fick-diffusion.yaml, which passes check_laws.py (no-sqrt, q-multiplied and no-C0 mutants are rejected) and whose numbers all reproduce; it is unmerged, its page was never built, its zebrafish R_crit is the mammalian textbook distance times 1.606 with no zebrafish information, and it wrongly lists the Krogh capillary cylinder under a k=4 solid-cylinder formula, none of which contradicts 'dispatched'.",
  "corrected_value": null,
  "depends_on": ["commit 0b307d41 on origin/claude/fick-diffusion-law-nv8p7l with Claude-Session trailer session_01EeoYQermc1y2miVqXjrRY4", "check_laws.py output at 0b307d41 and my mutant runs", "build_pages.py --check output at 0b307d41", "origin/main ancestry check as of 2026-11-04 ~08:22 UTC", "entry inputs D=2.1e-9 m^2/s, C0=0.2 and 0.258 mol/m^3, L=100-200 um", "Krogh-Erlang solution form (from memory, unverified)"]}
```
