"""Neural-scale sensorimotor/control models for the flying-fish project (claude-neuro harness, 2026-11-01).

m1 fast_start   : Mauthner-triggered C-start escape -> surface emergence -> taxi -> glide release distribution
m2 caudal_cpg   : extends engineering.behavior's phase/amplitude CPG to caudal-fin thrust (EBT + quasi-steady lobe)
m3 glide_stab   : pitch/roll stabilisation with pectoral/pelvic control surfaces, sensing delay and noise
All outputs are SIMULATED, not observed.
"""
