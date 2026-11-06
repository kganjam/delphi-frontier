-- 0015: give `claim` and `constraint_entailed` a conditions column.
--
-- WHY. SPEC-ASK D5 requires "a serialisation in which a value cannot be separated from its
-- units, conditions and scope", and swarm/export_transfer.py implements it. Its census measured
-- 7 of 1,620 live quantities exportable (claim 3166): `parameter` contributes 5 and
-- `spec_parameter` 2, while `claim` (1,309 quantities) and `constraint_entailed` (304) have no
-- conditions column at all, so for those the conditions exist only in prose and prose does not
-- travel with the number. A format nothing can be exported through is not transferability.
--
-- THE DATA IS ALREADY THERE, IN THE WRONG PLACE. 2,025 of 3,013 live claims (67.2%) carry a
-- `conditions: ...` field inside `statement`, written in a fixed shape by the harvester -- for
-- example "conditions: 5-6 dpf larvae, looming-evoked escape, bend duration". Extracting it is
-- mechanical rather than a judgement, which is why this is a migration and a backfill rather
-- than the reading task export_transfer.py's docstring describes.
--
-- ADDITIVE AND REVERSIBLE. Both columns are nullable and nothing reads them yet; `drop column`
-- reverses this file completely. NULL keeps its usual meaning here: no conditions recorded, as
-- distinct from an empty string, which would assert that the value holds unconditionally.
alter table claim               add column if not exists conditions text;
alter table constraint_entailed add column if not exists conditions text;

comment on column claim.conditions is
  'The conditions under which the value holds, for ASK D5 export. NULL means none recorded; it '
  'does NOT mean the value is unconditional. Backfilled for harvested claims from the '
  '`conditions:` field their statement already carries; see db/designswarm/0015_claim_conditions.sql';
