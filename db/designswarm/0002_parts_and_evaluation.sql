-- ============================================================================================
-- PART 1: the parts library. CAD/PLM identity, borrowed deliberately.
-- The distinction that matters and that software-origin systems usually miss: a PART is an
-- identity that survives change; a REVISION is an immutable released state of it. A content
-- hash alone cannot express "the same part, revision B", and an assigned id alone cannot
-- prove integrity -- so we carry both.
-- ============================================================================================

create table if not exists part (
  id            text primary key,            -- assigned, non-intelligent: PRT-000123
  project_id    text references project(id),
  kind          text not null,               -- protein | complex | actuator | scaffold | assembly |
                                             -- mechanism | rig | construct | sequence | material
  name          text not null,
  function      text not null,               -- what it is FOR, in one sentence
  scale_id      text references scale(id),
  created_at    timestamptz not null default now(),
  retired_at    timestamptz,
  supersedes    text references part(id)
);

create table if not exists part_revision (
  id            bigserial primary key,
  part_id       text not null references part(id),
  rev           text not null,               -- A, B, C ... released revisions only
  state         text not null default 'working'
                check (state in ('working','in-review','released','superseded','withdrawn')),
  content_sha256 text,                       -- integrity: what the artifact actually IS
  artifact_id   bigint references artifact(id),
  design_note   text,
  released_at   timestamptz,
  released_by   text,
  change_reason text,                        -- why this revision exists; required to release
  unique (part_id, rev)
);

-- The spec sheet. One row per characterised parameter, because a datasheet is a TABLE of
-- parameters each with its own conditions and its own evidence -- not a blob of prose.
create table if not exists spec_parameter (
  id            bigserial primary key,
  revision_id   bigint not null references part_revision(id) on delete cascade,
  name          text not null,               -- e.g. "area expansion ratio"
  symbol        text,
  value_nominal double precision,
  value_min     double precision,            -- the operating envelope, not a fake tolerance
  value_max     double precision,
  units         text,
  conditions    text,                        -- temperature, pH, load, medium: a value without
                                             -- its conditions is not a specification
  evidence      text not null check (evidence in
                 ('measured','simulated','predicted','derived','literature','assumed','unknown')),
  method        text,                        -- the instrument, model or code that produced it
  run_id        bigint references run(id),
  source        text,
  read_level    text,
  is_limit      boolean default false,       -- absolute maximum rating vs typical value
  notes         text
);

-- Multi-level BOM. `where-used` is just the reverse query on this table.
create table if not exists bom_line (
  id            bigserial primary key,
  parent_rev    bigint not null references part_revision(id) on delete cascade,
  child_part    text not null references part(id),
  child_rev     text,                        -- null = "latest released", as PLM systems allow
  quantity      double precision default 1,
  ref_designator text,
  note          text
);

-- How parts mate. The CAD analogue is an interface control document; in biology it is a
-- binding surface, a fusion junction, a promoter-CDS boundary, a mechanical attachment.
create table if not exists part_interface (
  id            bigserial primary key,
  part_id       text not null references part(id),
  name          text not null,
  direction     text check (direction in ('provides','requires','bidirectional')),
  interface_type text not null,              -- binding-site | fusion-junction | mechanical-attach |
                                             -- regulatory | electrical | fluidic
  spec          text not null,               -- what must be true for a mate to work
  compatible_with text                       -- free text or a part/interface reference
);

-- ============================================================================================
-- PART 2: the evaluation kernel. ONE mechanism, reused for every artifact type.
--   propose -> characterise -> grade -> challenge -> rank -> release
-- Two things make it honest rather than decorative:
--   (a) the RUBRIC is itself a versioned artifact, declared BEFORE the candidates are scored,
--       so a rubric edited after seeing results is a recorded event and not a silent one;
--   (b) the GRADER is calibrated against benchmark items with known answers, including seeded
--       bad ones, because an uncalibrated grader measures itself rather than the candidate.
-- ============================================================================================

create table if not exists rubric (
  id            text primary key,            -- RUB-protein-stiffness-v1
  project_id    text references project(id),
  applies_to    text not null,               -- the part kind this rubric grades
  version       int not null default 1,
  criteria      jsonb not null,              -- [{key, question, scale, anchors:{1:..,5:..}, weight}]
  aggregation   text not null default 'weighted-sum',
  registered_at timestamptz not null default now(),
  frozen        boolean not null default false,
  superseded_by text references rubric(id),
  change_reason text                         -- required when superseding: what the old one got wrong
);

create table if not exists candidate (
  id            bigserial primary key,
  project_id    text references project(id),
  subproblem_id text references subproblem(id),
  part_id       text references part(id),
  generator     text not null,               -- which agent or model proposed it
  generation    int default 0,               -- which round of the loop
  proposal      jsonb not null,
  created_at    timestamptz not null default now()
);

create table if not exists grade (
  id            bigserial primary key,
  candidate_id  bigint not null references candidate(id) on delete cascade,
  rubric_id     text not null references rubric(id),
  grader        text not null,               -- agent/model identity; graders are compared, so named
  scores        jsonb not null,              -- {criterion_key: score}
  total         double precision,
  rationale     text,
  order_seed    int,                         -- position-bias control: which order it saw candidates
  created_at    timestamptz not null default now()
);

-- Pairwise comparisons, because absolute LLM scores are poorly calibrated and pairwise is not.
-- Each pair is run in BOTH orders; `order_swapped` records which, so position bias is measurable
-- rather than assumed away.
create table if not exists comparison (
  id            bigserial primary key,
  rubric_id     text not null references rubric(id),
  left_id       bigint not null references candidate(id),
  right_id      bigint not null references candidate(id),
  grader        text not null,
  winner        text check (winner in ('left','right','tie')),
  order_swapped boolean not null default false,
  rationale     text,
  created_at    timestamptz not null default now()
);

-- Calibration. A benchmark item has a KNOWN answer, including deliberately bad candidates a
-- competent grader must reject. A grader that passes a seeded-bad item is not used.
create table if not exists benchmark_item (
  id            bigserial primary key,
  applies_to    text not null,
  payload       jsonb not null,
  known_answer  text not null,
  item_kind     text not null check (item_kind in ('known-good','known-bad','known-ordering')),
  provenance    text not null
);

create table if not exists grader_calibration (
  id            bigserial primary key,
  grader        text not null,
  rubric_id     text references rubric(id),
  n_items       int not null,
  n_correct     int not null,
  caught_known_bad int,
  n_known_bad   int,
  measured_at   timestamptz not null default now(),
  verdict       text check (verdict in ('trusted','untrusted','provisional')),
  note          text
);

create index if not exists idx_rev_part    on part_revision(part_id, state);
create index if not exists idx_spec_rev    on spec_parameter(revision_id);
create index if not exists idx_spec_ev     on spec_parameter(evidence);
create index if not exists idx_bom_parent  on bom_line(parent_rev);
create index if not exists idx_bom_child   on bom_line(child_part);
create index if not exists idx_cand_sub    on candidate(subproblem_id);
create index if not exists idx_grade_cand  on grade(candidate_id);
create index if not exists idx_cmp_rubric  on comparison(rubric_id);
