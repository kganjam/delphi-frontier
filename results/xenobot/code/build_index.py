#!/usr/bin/env python3
import json, os
ROOT = "/data/scratch/designspaces/xenobot"
rc = json.load(open(f"{ROOT}/regime-check.json"))
cv = json.load(open(f"{ROOT}/convergence.json"))
cw = json.load(open(f"{ROOT}/cargo-work.json"))

studies = [
    {"id": "regime-check",
     "title": "The gait ranking is from the wrong physics",
     "scale": "fluid",
     "kind": "analysis + simulation",
     "question": "A real millimetre-scale construct moves through water at a Reynolds number far below 1. The published gait comparison is dry friction on a floor under gravity, with inertia. Does its ranking of six actuation patterns transfer to the regime the real object occupies?",
     "summary": "No, and the failure is qualitative rather than a reordering. Computed from the sizes and speeds the papers themselves report, anthrobots sit at Re = 1.5e-4 to 2.5e-2 and a nominal 1 mm xenobot at Re = 0.0996; the simulated artifact's own body, at its own size and speed, would be at Re = 643 in water, 3.8 orders of magnitude away. Five of the six published patterns assign only the phases 0 and pi, so the whole body is driven by one scalar in time and the stroke retraces itself: they are time-reciprocal, and Purcell's scallop theorem makes their net displacement exactly zero at low Reynolds number. A Rotne-Prager-Yamakawa bead-model Stokes swimmer confirms it, with the travelling wave at 0.034 body lengths per cycle and every other pattern at the numerical floor. The weakness is the one the page must not hide: this applies cleanly to a FREE SWIMMER, and a xenobot crawling on a dish with its ventral surface in contact is not one, because surface friction is not Stokes drag and sits outside the theorem's assumptions. Separately, most published constructs are cilia-driven, and cilia are surface thrust rather than a body gait, so this bears directly on the 2020 cardiac-driven constructs and only indirectly on the rest.",
     "code": "code/regime_check.py (with code/lattice.py and code/stokes.py)",
     "data": "regime-check.json, data/regime-reynolds-grid.npz",
     "summary_table_title": "Dry friction against Stokes flow, the same six gaits",
     "figures": [
         {"file": "figures/regime-reynolds-map.png",
          "alt": "Heat map of Reynolds number against construct size from 0.3 to 2 mm and speed from 50 to 1000 micrometres per second, in water at 20 degrees Celsius. Contours mark Re = 0.032, 0.1 and 0.32. Markers show an anthrobot at Re = 0.025 and a 1 mm xenobot at Re = 0.1. A boxed annotation records that the voxel-actuation artifact's own body would sit at Re = 643, off the chart.",
          "caption": "Simulation (closed form). Reynolds number across the real parameter range. Everywhere a published construct actually sits, Re is at most about 0.1: inertia is irrelevant and viscosity dominates. The simulated body that the published gait ranking came from would be at Re = 643 in water, 3.8 orders of magnitude away. That simulation contains no fluid at all, so this is a comparison of scales rather than a property of it."},
         {"file": "figures/regime-ranking-compare.png",
          "alt": "Two dot plots side by side on a shared logarithmic axis, one for dry friction and one for Stokes flow, listing six gaits. Under dry friction all six have non-zero values from 0.073 down to 4e-6 body lengths per cycle. Under Stokes flow only the travelling wave has a value, 0.034; the other five are marked with open circles and arrows pointing off-scale labelled exactly zero.",
          "caption": "Simulation. The same six gaits, ranked in each regime. Under dry friction the travelling wave beats the longitudinal split by 2.4 times. In Stokes flow the longitudinal split does not work at all, because it is time-reciprocal. Note the trap: Spearman's rho over all six is 0.94 with p = 0.005, which reads as excellent transfer and is vacuous, because five of the six Stokes values are the same number."}]},

    {"id": "convergence",
     "title": "It does not converge, and the flagged swing was the encoding",
     "scale": "design-loop",
     "kind": "simulation",
     "question": "An independent audit recorded a 7.25-fold change in net displacement under grid refinement and left spatial convergence unresolved, and flagged a body-size series that swung ten-fold without trending. Does the model converge on a clean refinement series, and is that swing a gait-length resonance or a numerical artifact?",
     "summary": "It does not converge, and the swing is neither of the offered options: it is the actuation encoding. On a parity-matched refinement, holding the outer envelope and the physical actuation field fixed while refining the lattice four-fold from 45 to 2880 voxels, the travelling wave spans 41% of its coarsest value and the longitudinal split 54%, and both series turn over rather than settling. The winner is stable across all four levels but the margin falls from 19.4 to 10.4 times and is still moving at the finest grid. The flagged swing resolves cleanly: the longitudinal pattern splits the body at index nx/2, so odd nx gives an asymmetric actuator layout and even nx a symmetric one, and sweeping nx from 3 to 16 reveals two smooth monotone branches interleaved. Two discriminators declared in advance both fail for a resonance: the alternation is absent from the travelling wave, whose phase does not depend on parity, by a median factor of 1.008 against 20.3; and the optimum frequency does not move with body length, sitting at 12 Hz for both nx = 4 and nx = 8 while the body doubles. The weakness is that only two of six patterns were refined, so this cannot offer a corrected ranking, and four levels can show a series failing to settle but cannot extract a trustworthy convergence order.",
     "code": "code/convergence.py (with code/sweeps.py, code/sweep_freqopt.py, code/refine_local.py, code/run_voxelyze.py)",
     "data": "convergence.json, data/sweeps.json, data/freqopt.json, data/refine_local.json",
     "summary_table_title": "Four refinement levels, two parity-matched series",
     "figures": [
         {"file": "figures/convergence-series.png",
          "alt": "Three panels. The first shows the travelling wave's normalised displacement across four refinement levels at 45, 360, 1215 and 2880 voxels, rising then falling, spread 41 per cent. The second shows the parity-matched longitudinal split across 36, 288, 972 and 2304 voxels, rising then falling, spread 54 per cent. The third shows the ratio between them falling from 19.4 to 10.4 across the same levels.",
          "caption": "Simulation. A parity-matched grid refinement, four levels, outer envelope and physical actuation field held fixed. Neither series settles: both turn over, and the successive differences do not fall the way a converging series' do. The published artifact instead refined nx from 5 to 10, which moved its actuation split from 20 mm to 25 mm and flipped its parity at the same time. Removing that confound does not produce convergence; it only shows that convergence was never the thing being measured."},
         {"file": "figures/convergence-parity-resonance.png",
          "alt": "Three panels. The top sweeps nx from 3 to 16 on a log axis: longitudinal alternates sharply between an upper odd-nx branch and a lower even-nx branch, each smooth and monotone, while the travelling wave is a single smooth curve with no alternation. The lower left shows travelling's frequency response from 0.25 to 16 Hz at four body lengths, broad and shallow. The lower right plots the optimum frequency against body length, showing longitudinal flat at 12 Hz against a dashed 1/L reference.",
          "caption": "Simulation. The flagged non-monotonicity is the actuation encoding, not the mechanics and not the solver. The four points the audit flagged are two adjacent points of each smooth branch. Both predeclared discriminators fail for a resonance: the alternation does not appear in the parity-free pattern, and the optimum frequency does not scale with body length."}]},

    {"id": "cargo-work",
     "title": "Does the best self-mover also push best?",
     "scale": "application",
     "kind": "simulation",
     "question": "Every headline xenobot result is about the construct moving itself. What body plan and actuation pattern lets it do useful mechanical work on an external object, and is the published optimisation target the right one for the application?",
     "summary": "Our predeclared expectation was that the best self-mover would not be the best pusher. It was wrong, and we report it as a failed prediction. The travelling wave is first on every metric: 103.6 mm of cargo moved against 35.8 and 21.7 mm, a transport ratio of 0.95 of its own path transferred to the cargo against 0.51 and 0.26, and seven times the useful work per unit of actuation energy. What the study did find is that the live constraint is reach rather than push — with the cargo one clear lattice site away, only one gait of six covers that distance in the artifact's own five cycles, so a contact-gated forty-cycle arm was added to separate the two — and that all three contacting gaits stall at the same 64 g cargo with efficiency peaking just below it, so the heaviest load that still moves is the right one to carry. The swarm arm returns an honest negative: a uniform swarm sweeps but does not corral, with the particle field's radius of gyration increasing in 28 of 30 runs, and the one apparent exception — 2 of 5 seeds at the largest swarm size — tested rather than hedged and shown to be a field-size effect rather than an onset. The weakness is that all of it is in the dry-friction regime, which our own first study says is not the regime a real construct occupies; in water, four of the six gaits compared here could not push anything at all.",
     "code": "code/cargo_actuation.cpp, code/cargo_work.py, code/cargo_contact.py, code/cargo_mass.py, code/cargo_swarm.py, code/cargo_assemble.py",
     "data": "cargo-work.json, data/cargo-arm1b.json, data/cargo-arm2b.json, data/cargo-arm3.json",
     "summary_table_title": "Self-locomotion against cargo transport, per gait",
     "figures": [
         {"file": "figures/cargo-work-by-gait.png",
          "alt": "Two panels. The upper shows paired horizontal bars per gait for self-locomotion and cargo displacement over 40 cycles: travelling 117.4 and 103.6 mm, longitudinal 47.5 and 35.8, lateral 43.4 and 21.7, and three gaits marked as never having reached the cargo. The lower shows two separate bar charts for the three contacting gaits, transport ratio from 0.95 down to 0.26 and efficiency from 3.26 down to 0.44 per cent.",
          "caption": "Simulation, dry friction. The best self-mover is also the best pusher, contradicting our predeclared expectation, and its advantage is larger in pushing than in self-locomotion. Three of six gaits never reach the cargo at all even in forty cycles, which is a reach result rather than a push result and is reported separately for that reason."},
         {"file": "figures/cargo-swarm-aggregation.png",
          "alt": "Two panels against swarm size from one to eight constructs, each with a min-to-max band over five seeds. The left shows mean particle displacement rising from about 2 to 19 mm, slightly faster than linear. The right shows the change in the particle field's radius of gyration staying positive at every swarm size, with a shaded region below zero labelled as where aggregation would appear and a single seed at N equals eight dipping into it.",
          "caption": "Simulation, dry friction. A uniform swarm sweeps; it does not corral. Material moved rises slightly faster than linearly with swarm size, but energy efficiency is flat and the particle field disperses in 28 of 30 runs. The two exceptions, both at the largest swarm size here, prompted a follow-up arm in a density-matched wider field out to 16 constructs; it found no aggregation at any swarm size, so the exceptions were a property of the narrower field rather than of swarm size. Every construct runs the same gait, so their effects add as a common drift rather than converging — which is exactly why the published semitoroidal progenitor, whose concave mouth traps material, aggregates when a uniform swarm does not."},
         {"file": "figures/cargo-swarm.mp4",
          "alt": "Animation of a top-down simulation: six constructs drawn as clusters of green points travel leftwards through a field of orange points representing passive particles, pushing particles ahead of them and leaving the field more spread out than it started.",
          "caption": "Simulation, not a recording. Six constructs on the travelling gait and 120 passive particles under dry Coulomb friction. Voxel centres only — the data hold centres and nothing else, so no orientations, deformed meshes, forces or cellular states are drawn or implied."}]},
]
out = {"studies": studies}
for s in studies:
    import re as _re
    n = len([x for x in _re.split(r"(?<=[.!?]) +", s["summary"]) if x.strip()])
    assert 3 <= n <= 6, (s["id"], n)
    for f in s["figures"]:
        p = os.path.join(ROOT, f["file"])
        f["exists"] = os.path.exists(p)
json.dump(out, open(f"{ROOT}/index-fragment.json", "w"), indent=2)
for s in studies:
    print(s["id"], "figures:", [(f["file"].split("/")[-1], f["exists"]) for f in s["figures"]])
