insert into subproblem (id, project_id, scale_id, question, why_it_matters, acceptance, falsifier) values

('S1','zebrafish-flight','organism',
 'Can a 0.4 g zebrafish reach takeoff speed from water?',
 'Exocoetids leave the water at 16-20 m/s. Zebrafish burst speed is of order 1 m/s. If that gap cannot be closed, every downstream morphological design is moot, so it is tested first.',
 'Measured Danio burst velocity (cited, with read-level) compared against the stall speed computed over a span x aspect-ratio x CL_max grid, reported as a ratio per cell.',
 'A published Danio fast-start measurement at or above the computed takeoff speed for any feasible wing.'),

('S2','zebrafish-flight','organism',
 'What lift-to-drag is physically available at Re 1e3-1e4?',
 'A zebrafish-scale wing operates two orders of magnitude below flying-fish Reynolds number, where conventional airfoil performance collapses and thin cambered plates win. The achievable L/D sets the glide range.',
 'Measured low-Re polars from the literature (Mueller/Okamoto/Sunada class), giving CL_max and peak L/D for a thin cambered membrane at the computed Re, with read-levels.',
 'Measured data showing a thin plate at Re~3e3 reaching the L/D assumed by the glide model.'),

('S3','zebrafish-flight','organism',
 'Does the mass and power budget close?',
 'Enlarged fins add mass and the animal must still launch and stabilise. A design that ignores wing mass is cheating.',
 'A mass budget with wing mass estimated from measured fin tissue density and the designed planform, plus a power requirement compared to measured fish white-muscle power density.',
 'A wing-mass estimate that exceeds the whole-body mass the design assumes.'),

('S5','zebrafish-flight','organ',
 'What pectoral fin planform is actually reachable by genetic enlargement?',
 'The wing is a pectoral fin. Published fin-overgrowth mutants give a measured ceiling on how much larger a fin can get; the design cannot assume more.',
 'Span and area reachable, expressed in body lengths, derived from measured fold-changes in real zebrafish long-fin alleles rather than assumed.',
 'A measured allele exceeding the stated ceiling, or evidence the overgrowth does not apply to pectorals.'),

('S6','zebrafish-flight','organ',
 'Can a lepidotrichial fin ray carry aerodynamic load without collapsing?',
 'A fin is a membrane on segmented bony rays evolved for water, where loads are distributed. Point lift loads in air may buckle or flutter it. This is the structural make-or-break.',
 'Beam analysis using measured lepidotrichia modulus and real ray geometry, giving tip deflection and the flutter speed, compared to the design flight speed.',
 'A measured modulus or ray geometry giving deflection within the tolerance the aerodynamics needs.'),

('S7','zebrafish-flight','organ',
 'Can the pectoral girdle bear and transmit lift?',
 'Fish pectoral girdles are built for paddling, not for a bending moment equal to body weight at a long moment arm.',
 'The root bending moment at design lift compared to the girdles measured or estimated strength, with the attachment geometry named.',
 'Evidence of a teleost pectoral girdle bearing comparable loads.'),

('S9','zebrafish-flight','tissue',
 'What are the measured material properties of fin ray bone and actinotrichia?',
 'Every structural claim at the organ scale depends on a modulus that must be measured, not assumed.',
 'Youngs modulus, strength and density for lepidotrichia and actinotrichia from the literature with read-levels, and the scatter across studies preserved.',
 'n/a - this is a measurement-gathering subproblem; it fails if no measured value exists, which is itself the finding.'),

('S10','zebrafish-flight','tissue',
 'Is there enough muscle power for flapping, if gliding is insufficient?',
 'If S1 and S2 rule out pure gliding, flapping is the fallback, and it has its own power floor.',
 'Required mass-specific mechanical power for sustained flapping at the design frequency, against measured maximum power density in fish fast muscle.',
 'A measured fish muscle power density meeting the requirement.'),

('S11','zebrafish-flight','cell',
 'What is the real bioelectric mechanism controlling fin size?',
 'Zebrafish fin size is under bioelectric control (potassium channel alleles). This is the actual, published lever on the geometry the whole design needs.',
 'The mechanism traced from allele to membrane potential to ray growth rate, each step with a citation and read-level, naming what is NOT established.',
 'Evidence that the bioelectric alleles act through an unrelated pathway.'),

('S13','zebrafish-flight','protein',
 'Can a stiffer structural protein variant be designed for the fin ray?',
 'If S6 fails on stiffness, a materials route is the alternative to a geometric one. This is where protein design models earn their place.',
 'Candidate sequences with predicted structure and stability from a real structure-prediction run, with the prediction clearly marked as prediction and never as measurement.',
 'Predicted stability changes indistinguishable from wild type.'),

('S14','zebrafish-flight','protein',
 'Can the fin-size potassium channel be engineered for graded, pectoral-restricted control?',
 'The published alleles are whole-animal and all-fin. A wing needs one pair of fins enlarged, controllably.',
 'Variant designs over the real channel sequence with predicted structural consequence, plus an honest statement of what prediction cannot establish about gating.',
 'Evidence the channel cannot tolerate the proposed substitutions.'),

('S15','zebrafish-flight','dna',
 'What is the minimal edit stack, and is each edit individually demonstrated?',
 'The deliverable the project is judged on: a concrete, buildable genetic design where every component exists in the literature.',
 'An ordered edit list, each with a gene symbol, a real allele or construct, a demonstrated phenotype, and an explicit statement of what combining them has NOT been shown to do.',
 'Any edit in the stack lacking a demonstrated zebrafish phenotype.'),

('S16','zebrafish-flight','dna',
 'Is there a pectoral-restricted regulatory element to drive the edits?',
 'Whole-animal fin overgrowth gives a fish that cannot swim. Restriction to the pectoral is what makes the design an animal rather than a lethal.',
 'Named enhancers or drivers with published pectoral specificity, with the specificity evidence and its read-level.',
 'Evidence that the named elements also drive caudal or dorsal expression.'),

('S18','zebrafish-flight','behaviour',
 'Could a zebrafish control attitude in air?',
 'An uncontrolled glider tumbles. Flying fish use the caudal lobe and fin adjustments; a zebrafish has no such repertoire and its vestibular system is tuned for water.',
 'Control authority estimated from the designed surfaces, with the stability margin, alongside what is known about Danio vestibulo-ocular response bandwidth.',
 'Published evidence of aerial attitude control in a non-exocoetid teleost of similar size.'),

('S20','zebrafish-flight','ecology',
 'Would flight pay for a zebrafish?',
 'Design without selection pressure is decoration. Exocoetid flight is predator escape; zebrafish are shallow-stream fish where the predator field and habitat differ.',
 'The energetic cost per launch against the predation benefit, using published Danio habitat and predator data, stating plainly whether the benefit exists.',
 'Published evidence of aerial predator escape in a danionin.')
on conflict (id) do nothing;

insert into subproblem_dep (subproblem_id, depends_on) values
 ('S3','S5'),('S3','S9'),('S6','S9'),('S7','S9'),('S5','S11'),
 ('S13','S9'),('S14','S11'),('S15','S11'),('S15','S16'),('S10','S2'),('S18','S5')
on conflict do nothing;
