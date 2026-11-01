# Neural scale of the flying-fish project (claude-neuro, 2026-11-01)

All results are SIMULATED, not observed. Each run directory holds `manifest.json`, which names the project scale ("neural"), the seed, the input hashes, the code hashes, the checks and a summary. It also holds `run_receipt.json` (command, exit code, resource caps, manifest sha256), `results.json` (full sweeps), `figure.png`, and the stdout/stderr logs.

| Model | Code | Run | Perturbation sweep | Experiment design and limits |
|---|---|---|---|---|
| M1 escape -> emergence -> taxi -> glide release | engineering/neuro/fast_start.py | m1-fast-start (seed 20261101, n 20000, exit 0) | Mauthner latency, muscle corner, emergence command, muscle power | engineering/neuro/cards.json |
| M2 caudal CPG -> thrust (extends behavior-cpg) | engineering/neuro/caudal_cpg.py | m2-caudal-cpg (seed 20261101, exit 0) | f x H x f_m x lambda x drag (8,580 equilibria); coupling x detuning (48); taxi power x wetted fraction | engineering/neuro/cards.json |
| M3 glide pitch/roll stabiliser | engineering/neuro/glide_stab.py | m3-glide-stabilizer (seed 20261101, exit 0) | canal x vision delay, gain, static margin, dihedral x caudal-fin area, gust x delay x sensor set | engineering/neuro/cards.json |
| M4 neural implementation; what is NOT established | engineering/neuro/NEURAL_IMPLEMENTATION.md | - | - | - |

Sources with verification levels: engineering/neuro/sources.json. The LLM review log, with the decision on each point: reviews/RESPONSE.md.
Reproduce a run: `engineering/neuro/run.sh <caudal_cpg|fast_start|glide_stab> <run id> --seed 20261101`. Each takes under 10 minutes on one CPU thread; no GPU is needed.
Site: scripts/build_site.py adds one card per exit-0 run (engineering/neuro/site.py). The neural panel in site/content/projects.json now links these cards and their sources. The regenerated site/data is NOT committed here.
