--
-- PostgreSQL database dump
--

\restrict Y3ICkfrwimSr6aFsJZpZt0k3hJz2xWgz64hhaky5Hiz3sKDNkmEMsNCHidlODXK

-- Dumped from database version 16.15 (Debian 16.15-1.pgdg12+2)
-- Dumped by pg_dump version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: benchmark_item; Type: TABLE DATA; Schema: public; Owner: morphoswarm
--

COPY public.benchmark_item (id, applies_to, payload, known_answer, item_kind, provenance) FROM stdin;
1	claim	{"check": "v^2/g", "statement": "Ballistic range at 45 degrees from a measured burst of 1.38 m/s is 19.4 cm"}	CORRECT: 1.38^2/9.81 = 0.194 m. Recomputed in session 2026-11-04.	known-good	verified by the recorder
2	claim	{"check": "dimensional balance", "statement": "Reynolds number Re = rho*U*L/mu is dimensionless"}	CORRECT: M/L^3 * L/T * L / (M/(L*T)) cancels to dimensionless. Checked by check_laws.py.	known-good	verified by the recorder
3	claim	{"check": "recount from the a3m", "statement": "PDB70 MSA depth for kcnk5b is 0.0 from residue 326 onward"}	CORRECT: recomputed from the committed kcnk5b_pdb70.a3m, 72 sequences, max depth 0 past 326.	known-good	verified by the recorder
4	claim	{"check": "v^2/g", "statement": "Ballistic range at 45 degrees from a measured burst of 1.38 m/s is 1.94 m"}	WRONG by 10x: 1.38^2/9.81 = 0.194 m, not 1.94 m. A grader must catch this.	known-bad	seeded by the recorder
5	claim	{"check": "regime validity", "statement": "A zebrafish-scale wing at Re 3e3 achieves CL_max 1.5, the standard thick-airfoil value"}	WRONG: 1.5 is a high-Reynolds thick-airfoil figure. Measured thin plates at Re 7e2-1e4 give 0.9-1.15. A real value applied in the wrong regime.	known-bad	seeded by the recorder
6	claim	{"check": "scaling", "statement": "A 40 mm bluegill ray EI of 3.8e-6 N m^2 can be compared directly against a 120 mm ray requirement of 6.3e-4 N m^2"}	WRONG: EI scales as L^4, so (120/40.3)^4 = 78.6x. Comparing unscaled inflates the gap from 2.1x to 165x. This error was live in this project for hours.	known-bad	seeded from a real defect
7	claim	{"evidence": "measured", "statement": "MEASURED: adult zebrafish burst speed is 0.842 m/s"}	WRONG EVIDENCE LEVEL: 0.842 m/s was DERIVED from a measured Reynolds number, not measured directly. The number is right and the level is not.	known-bad	seeded by the recorder
\.


--
-- Data for Name: grader_calibration; Type: TABLE DATA; Schema: public; Owner: morphoswarm
--

COPY public.grader_calibration (id, grader, rubric_id, n_items, n_correct, caught_known_bad, n_known_bad, measured_at, verdict, note) FROM stdin;
1	cloud:claude-opus-5-5 (session_01QbcBRXmj1D5f1cmzW25ocp)	\N	7	7	4	4	2026-11-04 09:10:03.390653+00	trusted	Blind run: not told how many were defective and told explicitly not to assume a balance. 3/3 known-good marked correct; 4/4 known-bad caught with the right defect named. Arithmetic (decimal off by 10x); regime error (gave the correct low-Re CL_max range unprompted); scale error (computed 3^4=81 against the recorder's 78.6 and noted the scaled value is STILL below requirement, so it did not overcorrect); evidence inflation (and additionally spotted that 0.842 conflicts with the 1.38 m/s used in other items, a cross-item inconsistency it was not asked to look for). Two of the four seeded defects were REAL errors this project made.
\.


--
-- Name: benchmark_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: morphoswarm
--

SELECT pg_catalog.setval('public.benchmark_item_id_seq', 7, true);


--
-- Name: grader_calibration_id_seq; Type: SEQUENCE SET; Schema: public; Owner: morphoswarm
--

SELECT pg_catalog.setval('public.grader_calibration_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

\unrestrict Y3ICkfrwimSr6aFsJZpZt0k3hJz2xWgz64hhaky5Hiz3sKDNkmEMsNCHidlODXK

