insert into project (id, title, goal) values
 ('zebrafish-flight', 'Making a zebrafish fly',
  'Derive, from first principles and published measurement, what it would take to turn Danio rerio (4 cm, ~0.4 g) into an animal that can glide or fly. NOT to copy Exocoetidae. Carry the design from ecology down to DNA, with every cross-scale junction labelled by how well it is calibrated, and every claim carrying the evidence level that earned it.')
on conflict (id) do nothing;

insert into scale (id, ord, title, what_lives_here, what_a_sim_here_produces, what_makes_it_checkable) values
 ('dna',       1, 'DNA and regulation', 'Alleles, promoters, enhancers, edits, guide designs', 'Predicted expression change, edit efficiency, off-target set', 'An allele that exists and a measured phenotype in the literature'),
 ('protein',   2, 'Protein', 'Sequences, structures, stability and binding predictions', 'Structure, ddG, interface score, folding confidence', 'A solved structure, or a measured stability/binding value'),
 ('cell',      3, 'Cell', 'Cell types, signalling state, bioelectric potential', 'Membrane potential, proliferation rate, differentiation outcome', 'A measured electrophysiological or expression value'),
 ('tissue',    4, 'Tissue', 'Fin rays, membrane, bone, muscle blocks', 'Stiffness, strength, growth field, material properties', 'A measured modulus, or a loading test'),
 ('organ',     5, 'Organ and appendage', 'Pectoral fin as a wing, caudal fin as a thruster', 'Planform, area, span, mass, second moment of area', 'A measured morphometry on real fish'),
 ('organism',  6, 'Whole organism', 'Mass budget, power budget, flight mechanics', 'Lift, drag, glide ratio, takeoff speed, power required', 'A wind-tunnel or kinematic measurement'),
 ('behaviour', 7, 'Behaviour and control', 'Launch, stabilisation, sensing, landing', 'Trajectory, control authority, stability margin', 'Observed kinematics of a real animal'),
 ('ecology',   8, 'Ecology', 'Why flight pays, predation, habitat, viability', 'Fitness benefit, energetic return, population consequence', 'Field observation or a published ecological study')
on conflict (id) do nothing;
