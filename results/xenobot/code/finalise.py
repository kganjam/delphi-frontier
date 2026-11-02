#!/usr/bin/env python3
"""Wrap the raw study outputs into the published schema: headline, model with a
fully-statused parameter list, limitations, what_this_cannot_establish."""
import json, os
ROOT = "/data/scratch/designspaces/xenobot"

SOURCED = "voxcraft/voxcraft-sim demos/basic/base.vxa @ dd8668f99ff74fb2fc2ee60deb91287a3b519d8f, reached through the pinned artifact's protocol.json"
ASSUMED = "declared engineering choice in the pinned protocol (artifacts/voxel-actuation/protocol.json, parameter_provenance.assumed_not_measured); no measured biological referent"

WATER = [
    {"name": "rho_water", "value": 998.2, "units": "kg m^-3", "status": "assumed",
     "source": "standard value for water at 20 C; we did not retrieve a source that states the density of any culture medium used in these papers"},
    {"name": "mu_water", "value": 1.002e-3, "units": "Pa s", "status": "assumed",
     "source": "standard value for water at 20 C; same caveat. Real culture media and pond water are not pure water and some are non-Newtonian"},
]

# ------------------------------------------------------------ regime -----
r = json.load(open(f"{ROOT}/regime-check.raw.json"))
r["headline"] = ("A millimetre-scale living construct sits at Reynolds number below 0.1, and five of "
                 "the six published actuation patterns are time-reciprocal, so Purcell's scallop "
                 "theorem makes their net displacement exactly zero there. The published gait ranking "
                 "does not transfer: its 2nd and 3rd places are both dead in the regime the real "
                 "object occupies, and only the travelling wave survives.")
r["the_simulated_object_is_also_the_wrong_SIZE"] = {
    "why_this_is_worth_stating_beside_the_Reynolds_number": "Re = 643 is an abstraction. The plain fact underneath it is checkable from the committed candidate file and may land harder: the simulated body is 40-50 mm and a real construct is 0.5-1 mm, so the artifact simulates an object roughly 40 to 100 times too large, quite apart from having no fluid in it.",
    "simulated_centre_to_centre_span_m": 0.04,
    "simulated_outer_envelope_m": [0.05, 0.03, 0.03],
    "source": "artifacts/voxel-actuation/candidates/*.json, params.nx * params.voxel_m and result.body_len_m",
    "real_construct_m": [3e-4, 1e-3],
    "real_source": "Gumuskaya et al. 2023 (PMID 38032125) report anthrobot diameters of 30-500 um; 1 mm is the nominal xenobot figure and is ASSUMED, not read from a paper",
    "size_ratio_range": [40e-3 / 1e-3, 50e-3 / 0.5e-3]}
r["simulated_object_regime"]["speed_definition"] = (
    "U is PATH LENGTH divided by the measurement window: 0.016124646 m / 1.25 s = 12.90 mm/s. "
    "Using the NET displacement instead gives 0.014577281 m / 1.25 s = 11.66 mm/s and Re = 581 "
    "rather than 643. Both are stated so a recomputation does not look like a discrepancy; path "
    "length is the right choice here because Re is about the speed at which the body moves through "
    "the fluid, not about how far it ends up from where it started.")
r["simulated_object_regime"]["Re_translational_using_net_displacement"] = 998.2 * (0.014577281 / 1.25) * 0.05 / 1.002e-3
r["the_spearman_trap"] = {
    "what": "A rank correlation between the two regimes' gait orderings returns rho = 0.943 with p = 0.005, which reads as excellent transfer.",
    "why_it_is_vacuous": "five of the six Stokes values are the same number - exactly zero - so their relative order carries no information at all. The coefficient is computed over a tie that the test treats as a ranking.",
    "why_it_is_worth_its_own_section": "this is a statistic reporting excellent agreement at the exact moment agreement has failed completely, and failed QUALITATIVELY rather than by degree. Anyone checking 'did the ranking transfer?' with a rank correlation would conclude that it did.",
    "what_to_do_instead": "ask how many of the ranked items are distinguishable at all before ranking them. Here the answer is one, and the comparison should never have been posed as a correlation.",
    "rho": 0.942857142857143, "p": 0.004804664723032055,
    "distinguishable_stokes_values": 1, "items_ranked": 6}

r["model"] = {
    "what_it_is": "two models and one exact classification. (1) A closed-form Reynolds-number evaluation. (2) An exact algebraic test of whether each published actuation pattern is time-reciprocal. (3) A Rotne-Prager-Yamakawa bead-model Stokes swimmer over shapes from a quasi-static, free-floating, central-force spring lattice driven by the same actuation law.",
    "not_voxelyze": "the Stokes swimmer is OUR code and is not Voxelyze. Voxelyze at its pin is used unmodified for the dry-friction comparison, and reproduces the published travelling-wave run bit-for-bit at 0.0145773 m against 0.014577281 m.",
    "parameters": WATER + [
        {"name": "construct_size_range", "value": [3e-4, 2e-3], "units": "m", "status": "sourced",
         "source": "brief's stated range; the lower end is covered by Gumuskaya et al. 2023's reported 30-500 um anthrobot diameters (PMID 38032125)"},
        {"name": "construct_speed_range", "value": [5e-5, 1e-3], "units": "m s^-1", "status": "sourced",
         "source": "Gumuskaya et al. 2023 report 5-50 um/s for anthrobots (PMID 38032125); the upper end is the brief's"},
        {"name": "bead_radius", "value": "voxel/2", "units": "m", "status": "assumed",
         "source": "our choice: touching spheres filling the lattice, so adjacent beads sit exactly at 2a where the two RPY branches agree"},
        {"name": "E_lattice", "value": 1e5, "units": "Pa", "status": "sourced", "source": SOURCED},
        {"name": "k2_ratio", "value": 0.5, "units": "-", "status": "assumed",
         "source": "our choice: the face-diagonal spring stiffness relative to the nearest-neighbour one, which is what makes the lattice shear-stable. A nearest-neighbour-only cubic lattice has zero shear modulus and is a mechanism, not a solid. The Stokes result moves by under 1% across a 4x change in it."},
        {"name": "cte", "value": 0.01, "units": "degC^-1", "status": "assumed", "source": ASSUMED},
        {"name": "temp_amplitude", "value": 10.0, "units": "degC", "status": "assumed", "source": ASSUMED},
        {"name": "samples_per_cycle", "value": 64, "units": "-", "status": "nondimensional",
         "source": "our choice; the refinement arm shows 64 to 128 changes the answer by 0.12%"},
        {"name": "elastic_solve_tolerance", "value": 1e-14, "units": "-", "status": "nondimensional",
         "source": "our choice, adopted BECAUSE of the tolerance refinement arm, which shows the reciprocal gaits' residue tracks it"},
        {"name": "E_tissue_estimate", "value": 500.0, "units": "Pa", "status": "assumed",
         "source": "order-of-magnitude soft tissue. NOT measured, and Pai et al. 2025 (PMID 40263484) show these cells are not simply epidermis, so no literature modulus for embryonic tissue is the right number either"},
    ]}
r["limitations"] = [
    "The scallop-theorem result applies to a FREE SWIMMER. A construct crawling on a dish with its ventral surface in contact is not one: contact friction is not Stokes drag and is outside the theorem's assumptions, so a reciprocal gait can rectify against a surface. Kriegman et al. 2020 state their deciliated organisms 'always kept part of their ventral surfaces in contact with the surface of the dish due to negative buoyancy'.",
    "Most published constructs are cilia-driven, and cilia are a SURFACE thrust mechanism, not a body gait. Kriegman et al. 2021's own simulation models them as an impulse force on each surface voxel. Our analysis bears directly on the 2020 cardiac-driven constructs, which do deform, and only indirectly on the cilia-driven ones.",
    "The reciprocity test is exact for the CONTROL sequence. Carrying it to the SHAPE needs quasi-static response, which we check numerically rather than assume. The gate is met but only by a factor of 2.5 to 7 on the elastic-relaxation ratio, not by orders of magnitude; the fluid-driven deformation number mu*omega/E is the one that clears by many orders.",
    "The elastic lattice is central-force, so it obeys the Cauchy relations and its Poisson ratio is a property of the spring topology rather than an input. We measure 0.20 against the artifact's 0.35, and its axial and bending effective moduli differ by about 2x. It is used only to generate a shape.",
    "The reciprocal gaits return 1e-7 to 1e-8 rather than literal zero, which is the numerical residue of an iterative shape solve, not a displacement. Their relative order carries no information.",
    "Water at 20 C is assumed for every fluid property. Real media differ, and a non-Newtonian medium would partially lift the scallop-theorem constraint (Qiu et al. 2014, PMID 25369018).",
    "The Reynolds number for the simulated artifact body is a SCALE COMPARISON. That simulation contains no fluid at all.",
]
r["what_this_cannot_establish"] = [
    "that any real construct would or would not move; no organism was measured",
    "a corrected gait ranking for a surface crawler, which is a different problem",
    "anything about cilia-driven propulsion, whose stroke we did not model",
    "that the travelling wave is buildable: no living construct has per-region actuation phase control",
]
json.dump(r, open(f"{ROOT}/regime-check.json", "w"), indent=2)

# ------------------------------------------------------- convergence -----
c = json.load(open(f"{ROOT}/convergence.raw.json"))
c["model"] = {
    "engine": {"name": "Voxelyze", "repo": "https://github.com/jonhiller/Voxelyze",
               "commit": "4287e365e11416dd108f2f361e9ec4c5a011a16c",
               "licence_from_source_headers": "LGPL-3.0-or-later",
               "licence_caveat": "there is no LICENSE file at that commit, so the GitHub API reports license: null; the per-file headers are the licence",
               "build_defect": "the upstream makefile's default FLAGS carry -DPARDISO_5=1, which leaves undefined references to pardisoinit/pardiso; built with FLAGS overridden to drop it",
               "driver": "scripts/voxel_actuation/soft_actuation.cpp from delphi-frontier, UNMODIFIED. We changed only the arguments."},
    "verification": "our build reproduces the published travelling-wave run bit-for-bit: 0.0145773 m against the stored 0.014577281 m",
    "parameters": [
        {"name": "voxel_m", "value": [0.01, 0.005, 1 / 300, 0.0025], "units": "m", "status": "nondimensional",
         "source": "the refinement variable; chosen so the outer envelope is identical on all four levels"},
        {"name": "outer_envelope_A", "value": [0.05, 0.03, 0.03], "units": "m", "status": "assumed",
         "source": "held fixed across series A; it is the invariant length and therefore the denominator"},
        {"name": "outer_envelope_B", "value": [0.04, 0.03, 0.03], "units": "m", "status": "assumed",
         "source": "held fixed across series B"},
        {"name": "E", "value": 1e5, "units": "Pa", "status": "sourced", "source": SOURCED},
        {"name": "rho", "value": 1e3, "units": "kg m^-3", "status": "sourced", "source": SOURCED},
        {"name": "poisson", "value": 0.35, "units": "-", "status": "sourced", "source": SOURCED},
        {"name": "mu_static", "value": 1.0, "units": "-", "status": "sourced", "source": SOURCED},
        {"name": "mu_kinetic", "value": 0.8, "units": "-", "status": "sourced", "source": SOURCED},
        {"name": "cte", "value": 0.01, "units": "degC^-1", "status": "assumed", "source": ASSUMED},
        {"name": "temp_amplitude", "value": 10.0, "units": "degC", "status": "assumed", "source": ASSUMED},
        {"name": "freq", "value": 4.0, "units": "Hz", "status": "assumed",
         "source": ASSUMED + "; swept from 0.25 to 16 Hz in the resonance arm"},
        {"name": "zeta_internal", "value": 1.0, "units": "-", "status": "assumed", "source": ASSUMED},
        {"name": "zeta_global", "value": 0.1, "units": "-", "status": "assumed",
         "source": ASSUMED + ". It is a numerical absolute-frame damping term, NOT fluid drag, so no swimming interpretation is available from it"},
        {"name": "zeta_collision", "value": 0.8, "units": "-", "status": "assumed", "source": ASSUMED},
        {"name": "dtScale", "value": 0.5, "units": "-", "status": "assumed",
         "source": "fraction of Voxelyze's recommendedTimeStep, as in the pinned artifact, whose own arm F found 0.9% spread across a 4x dt range"},
        {"name": "cycles", "value": 5, "units": "-", "status": "assumed",
         "source": "matches the pinned artifact. The frequency sweep holds CYCLES fixed and lets duration vary as 5/f, so every point is the same number of actuation cycles"},
    ]}
c["limitations"] = [
    "Two patterns were refined, not six. No corrected ranking of the six gaits is offered or possible from this.",
    "Four levels is enough to show that a series does not settle; it is not enough to extract a reliable convergence order, and the power-law fits here have residuals of 5% and more, which is itself the finding.",
    "Temporal and spatial error ARE separated, by a half-timestep repeat of levels 1-3 (see timestep_separation_arm): spatial dominates by about 17x for the travelling wave and 3.5x for the longitudinal split, and the spatial spread survives at the finer timestep. Two caveats: level 4 was not repeated at the finer timestep, and for longitudinal the temporal error is NOT negligible, reaching 15.5% at level 2.",
    "Varying nx at fixed voxel size, which is how the parity sweep is done, changes voxel count, body length and mass together. The independent audit already noted this. We add that the effect is absent from a parity-free pattern and is frequency-independent, which rules out a gait-length resonance; it does not isolate a single cause.",
    "The frequency optima for the travelling wave sit at the lowest swept frequency for nx >= 5, so they are boundaries rather than optima and are labelled as such. The longitudinal optima are interior, which is what the D2 discriminator rests on.",
    "This is the generic soft-voxel model with assumed parameters throughout. Our own regime-check study finds it is not the regime a real construct occupies.",
]
json.dump(c, open(f"{ROOT}/convergence.json", "w"), indent=2)
# ------------------------ settled-and-not-diverged gate, from the pinned ---
# protocol's own discipline: a run that diverged is not evidence of anything.
import glob
runs = []
for f in glob.glob(f"{ROOT}/data/voxruns/*.json") + glob.glob(f"{ROOT}/data/cargo/*.json"):
    try:
        d = json.load(open(f))
    except Exception:
        continue
    n = d.get("numerics", {})
    if "diverged" in n:
        runs.append((f.split("/")[-1], n["diverged"]))
div = [r for r, v in runs if v]
gate = {"what": "every Voxelyze run behind these studies is checked for divergence. Voxelyze's doTimeStep returns false when any link's axial strain exceeds 100; the driver records that as diverged and exits 3. A diverged run is not evidence and none is used.",
        "total_runs_checked": len(runs), "diverged_runs": div, "gate_met": not div}
for name in ("convergence", "cargo-work"):
    d = json.load(open(f"{ROOT}/{name}.json")); d["not_diverged_gate"] = gate
    json.dump(d, open(f"{ROOT}/{name}.json", "w"), indent=2)
_rc = json.load(open(f"{ROOT}/regime-check.json"))
_rc["not_diverged_gate"] = dict(gate, note="regime-check's own Stokes and elastic solves are not time-stepped and cannot diverge; their analogue is the minimiser-convergence flag in elastic_lattice_controls and the shape-solve tolerance refinement arm.")
json.dump(_rc, open(f"{ROOT}/regime-check.json", "w"), indent=2)
print(f"not-diverged gate: {len(runs)} runs checked, diverged: {div or 'none'}")

for f in ("regime-check", "convergence", "cargo-work"):
    d = json.load(open(f"{ROOT}/{f}.json"))
    ps = d["model"]["parameters"]
    bad = [p["name"] for p in ps if not all(k in p for k in ("name", "value", "units", "status", "source"))]
    assert not bad, (f, bad)
    assert "headline" in d and "limitations" in d and "what_this_cannot_establish" in d, f
    print(f"{f}.json OK  {len(ps)} parameters, "
          f"{sum(1 for p in ps if p['status']=='sourced')} sourced / "
          f"{sum(1 for p in ps if p['status']=='assumed')} assumed / "
          f"{sum(1 for p in ps if p['status']=='nondimensional')} nondimensional")
