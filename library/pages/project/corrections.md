---
title: Corrections
---

**Nothing here was deleted.** Each row is a value that was replaced, kept beside what replaced it. This page is the project's error record, and it getting longer is a sign the system is working rather than failing.

## Superseded (10)

| was | became | now |
|---|---|---|
| **#3** Speed deficit is 10.4x and kinetic-energy deficit is 109x for the 1-BL wing case `10.4` | → #24 | Current best evidence: required takeoff 4.37 m/s against a measured burst of 0.842 m/s is a 5.2x speed and 27x `5.2` |
| **#5** Reynolds number is pinned at ~2e3-4e3 by body weight, so CL_max is probably <= 0.6; the value at that Re is un `3000` | → #86 | Replication: Re 1.9e3-4.0e3 reproduces, but measured steady CL_max near Re 3e3 is ~1.0 (0.9-1.1) for cambered/ `1` |
| **#11** PDB70 search on kcnk5b returns 72 sequences whose top hits are real K2P channel structures: 4BW5/4WFE (TRAAK), `72` | → #83 | PDB70 search on kcnk5b a3m holds 76 sequences (query + 75 PDB70 hit chains, 73 distinct entries); top hits are `76` |
| **#12** PDB70 returns NO structural homolog for and1 (only the query itself), so there is no template to design a stif `1` | → #69 | And1 PDB70 homolog hits = 0; a template-free AlphaFold model exists with 157/570 residues at pLDDT>=70 (global `157` |
| **#13** and1 and and2 are each 11.8% proline against a UniProt-wide average near 4.7%, with Ile+Val+Phe at 7.4% and 11 `11.8` | → #28 | and2 is NOT supported as intrinsically disordered: FoldIndex +0.070 (positive) and a disordered-window fractio `0.07` |
| **#28** and2 is NOT supported as intrinsically disordered: FoldIndex +0.070 (positive) and a disordered-window fractio `0.07` | → #70 | and2 disorder call is NOT supported either way: FoldIndex +0.035 on mature chain, 95% bootstrap CI [-0.052,+0. `0.035` |
| **#29** No tandem repeats in any of the three proteins against a null of 200 composition-preserving shuffles: and2's m `0.098` | → #71 | and2 max self-identity 0.098 sits at ~89th percentile of composition-preserving shuffles (p=0.106), not below  `0.098` |
| **#31** Cysteine close pairs are ZERO in all three and significantly fewer than chance in and2 (z=-2.02), with no CxxC `0` | → #87 | Replication: Cys close pairs (\|i-j\|<=3) = 0/0/0 and 0 CxxC reproduce; but and2 z = -1.6 (p one-sided ~0.08,  `-1.6` |
| **#36** Surface taxiing cannot close the launch gap, and the binding limit is TAIL-BEAT FREQUENCY not thrust force: su `73` | → #52 | S24 applied the Strouhal CRUISING band 0.2-0.3, but the law library records that small, low-Reynolds swimmers  `2.5` |
| **#52** S24 applied the Strouhal CRUISING band 0.2-0.3, but the law library records that small, low-Reynolds swimmers  `2.5` | → #84 | Replication: required tail-beat frequency at 1.95 m/s is 72-83 Hz (bracket 64-101), 1.4-1.6x the 52 Hz EMG max `77.5` |

## Open review flags (4)

Raised automatically when a claim they depend on was superseded.

| affected | triggered by | depth | status |
|---|---|---|---|
| claim 36 | claim #52 | 1 | open |
| S24 | claim #52 | 1 | open |
| claim 24 | claim #3 | 1 | open |
| S1 | claim #3 | 1 | open |
