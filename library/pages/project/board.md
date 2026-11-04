---
title: Subproblem board
---

Every question as an issue: its state, its scale, how many claims it carries, and whether anything it depends on has been superseded.

## Dependencies

```{mermaid}
graph LR
  S10["S10<br/>tissue"]:::done
  S11["S11<br/>cell"]:::done
  S13["S13<br/>protein"]:::ref
  S14["S14<br/>protein"]:::done
  S15["S15<br/>dna"]:::run
  S16["S16<br/>dna"]:::done
  S18["S18<br/>behaviour"]:::opn
  S2["S2<br/>organism"]:::done
  S21["S21<br/>behaviour"]:::done
  S22["S22<br/>dna"]:::done
  S23["S23<br/>protein"]:::done
  S24["S24<br/>behaviour"]:::done
  S3["S3<br/>organism"]:::opn
  S5["S5<br/>organ"]:::run
  S6["S6<br/>organ"]:::done
  S7["S7<br/>organ"]:::done
  S9["S9<br/>tissue"]:::done
  S5 --> S3
  S9 --> S3
  S9 --> S6
  S9 --> S7
  S11 --> S5
  S9 --> S13
  S11 --> S14
  S11 --> S15
  S16 --> S15
  S2 --> S10
  S5 --> S18
  S21 --> S24
  S9 --> S23
  S22 --> S15
  classDef done fill:#d4f4d4,stroke:#2a7
  classDef ref fill:#f9d4d4,stroke:#a22
  classDef run fill:#fdf2c4,stroke:#aa2
  classDef opn fill:#d4e4f9,stroke:#27a
```

*An arrow runs from a prerequisite to the question it unblocks.*

## 🔵 open — 2

| id | scale | claims | blocked on | question |
|---|---|---|---|---|
| **S3** | organism | 0 | S5, S9 | Does the mass and power budget close? |
| **S18** | behaviour | 0 | S5 | Could a zebrafish control attitude in air? |

## 🟡 running — 3

| id | scale | claims | blocked on | question |
|---|---|---|---|---|
| **S15** | dna | 0 | S11, S16, S22 | What is the minimal edit stack, and is each edit individually demonstrated? |
| **S16-D** | dna | 0 | — | Deepen S16: attack its most sensitive input |
| **S5** | organ | 0 | S11 | What pectoral fin planform is actually reachable by genetic enlargement? |

## 🟢 answered — 48

| id | scale | claims | blocked on | question |
|---|---|---|---|---|
| **S16** | dna | 1 | — | Is there a pectoral-restricted regulatory element to drive the edits? |
| **S22** | dna | 10 | — | What exactly did Daane et al. achieve in phenocopying flying-fish fin proportions? |
| **S22-D** | dna | 1 | — | Deepen S22: attack its most sensitive input |
| **S22-D-D** | dna | 2 | — | Deepen S22-D: attack its most sensitive input |
| **S22-D-D-D** | dna | 2 | — | Deepen S22-D-D: attack its most sensitive input |
| **S13-D** | protein | 1 | — | Deepen S13: attack its most sensitive input |
| **S14** | protein | 13 | S11 | Can the fin-size potassium channel be engineered for graded, pectoral-restricted control? |
| **S14-D** | protein | 0 | — | Deepen S14: attack its most sensitive input |
| **S14-D-D** | protein | 1 | — | Deepen S14-D: attack its most sensitive input |
| **S23** | protein | 1 | S9 | Can actinotrichia be stiffened by gain-of-function, given only loss-of-function is demonstrated? |
| **S23-D** | protein | 1 | — | Deepen S23: attack its most sensitive input |
| **S23-D-D** | protein | 2 | — | Deepen S23-D: attack its most sensitive input |
| **S11** | cell | 2 | — | What is the real bioelectric mechanism controlling fin size? |
| **S10** | tissue | 3 | S2 | Is there enough muscle power for flapping, if gliding is insufficient? |
| **S10-D** | tissue | 1 | — | Deepen S10: attack its most sensitive input |
| **S10-D-D** | tissue | 1 | — | Deepen S10-D: attack its most sensitive input |
| **S10-D-D-D** | tissue | 1 | — | Deepen S10-D-D: attack its most sensitive input |
| **S9** | tissue | 2 | — | What are the measured material properties of fin ray bone and actinotrichia? |
| **S9-D** | tissue | 1 | — | Deepen S9: attack its most sensitive input |
| **S9-D-D** | tissue | 2 | — | Deepen S9-D: attack its most sensitive input |
| **S25** | organ | 1 | — | Which relaying of Flammang 2013 fin-ray stiffness is correct: 3.8e-6 or 565e-6 N m^2? |
| **S26** ⚠️ | organ | 7 | — | Can ACTIVE stiffening carry the load a passive ray cannot? |
| **S26-D** | organ | 1 | — | Deepen S26: attack its most sensitive input |
| **S6** | organ | 3 | S9 | Can a lepidotrichial fin ray carry aerodynamic load without collapsing? |
| **S6-D** | organ | 1 | — | Deepen S6: attack its most sensitive input |
| **S6-D-D** | organ | 3 | — | Deepen S6-D: attack its most sensitive input |
| **S7** | organ | 1 | S9 | Can the pectoral girdle bear and transmit lift? |
| **S7-D** | organ | 1 | — | Deepen S7: attack its most sensitive input |
| **S7-D-D** | organ | 2 | — | Deepen S7-D: attack its most sensitive input |
| **S1** ⚠️ | organism | 4 | — | Can a 0.4 g zebrafish reach takeoff speed from water? |
| **S1-D** | organism | 1 | — | Deepen S1: attack its most sensitive input |
| **S1-D-D** | organism | 2 | — | Deepen S1-D: attack its most sensitive input |
| **S2** | organism | 2 | — | What lift-to-drag is physically available at Re 1e3-1e4? |
| **S2-D** | organism | 1 | — | Deepen S2: attack its most sensitive input |
| **S2-D-D** | organism | 3 | — | Deepen S2-D: attack its most sensitive input |
| **S28** | organism | 7 | — | Given everything established, what is the best achievable design and what can it actually do? |
| **S29** | organism | 8 | — | Can launch energy be engineered, via latch-mediated spring actuation, to reach 4.37 m/s? |
| **S21** | behaviour | 5 | — | What is the measured PEAK velocity of an adult zebrafish fast-start? |
| **S21-D** | behaviour | 1 | — | Deepen S21: attack its most sensitive input |
| **S21-D-D** | behaviour | 2 | — | Deepen S21-D: attack its most sensitive input |
| **S21-D-D-D** | behaviour | 2 | — | Deepen S21-D-D: attack its most sensitive input |
| **S24** ⚠️ | behaviour | 4 | S21 | Could an extended in-water acceleration run (surface taxiing) close the launch gap? |
| **S24-D** | behaviour | 1 | — | Deepen S24: attack its most sensitive input |
| **S24-D-D** | behaviour | 2 | — | Deepen S24-D: attack its most sensitive input |
| **S20** | ecology | 1 | — | Would flight pay for a zebrafish? |
| **S20-D** | ecology | 1 | — | Deepen S20: attack its most sensitive input |
| **S20-D-D** | ecology | 1 | — | Deepen S20-D: attack its most sensitive input |
| **S20-D-D-D** | ecology | 2 | — | Deepen S20-D-D: attack its most sensitive input |

## 🔴 refuted — 1

| id | scale | claims | blocked on | question |
|---|---|---|---|---|
| **S13** | protein | 11 | S9 | Can a stiffer structural protein variant be designed for the fin ray? |

⚠️ marks a subproblem with an open review flag: something it rests on was superseded.
