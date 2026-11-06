-- The design-swarm store. Project-agnostic BY CONSTRUCTION: nothing here names fish, coral or insect.
-- A project instantiates the same ladder, the same subproblem frontier and the same artifact provenance.

create table if not exists project (
  id            text primary key,
  title         text not null,
  goal          text not null,
  created_at    timestamptz not null default now()
);

-- The scale ladder. `ord` is the ladder position; a junction always joins two adjacent-or-not scales.
create table if not exists scale (
  id            text primary key,
  ord           int  not null,
  title         text not null,
  what_lives_here text not null,
  what_a_sim_here_produces text not null,
  what_makes_it_checkable  text not null
);

-- The frontier. An autonomous agent picks the next `open` row whose dependencies are `passed`.
create table if not exists subproblem (
  id            text primary key,
  project_id    text not null references project(id),
  scale_id      text references scale(id),
  question      text not null,
  why_it_matters text,
  acceptance    text not null,              -- what would settle it
  falsifier     text,                       -- what observation would REFUTE the current answer
  status        text not null default 'open'
                check (status in ('open','running','answered','blocked','refuted','superseded')),
  answer        text,
  answer_kind   text check (answer_kind in
                 ('measured','simulated','derived','literature','scenario','refused',null)),
  blocked_on    text,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);
create table if not exists subproblem_dep (
  subproblem_id text not null references subproblem(id) on delete cascade,
  depends_on    text not null references subproblem(id) on delete cascade,
  primary key (subproblem_id, depends_on)
);

-- Everything a run emits. Addressed by sha256 so a figure on a page can be traced to the code that made it.
create table if not exists artifact (
  id            bigserial primary key,
  project_id    text not null references project(id),
  subproblem_id text references subproblem(id),
  scale_id      text references scale(id),
  kind          text not null,              -- figure | mesh | dataset | sequence | model | document | video
  path          text not null,
  sha256        text,
  produced_by_run bigint,
  code_sha      text,
  created_at    timestamptz not null default now()
);

create table if not exists run (
  id            bigserial primary key,
  project_id    text not null references project(id),
  subproblem_id text references subproblem(id),
  tool          text not null,              -- the simulator or model actually invoked
  command       text,
  code_sha      text,
  params        jsonb,
  exit_code     int,
  started_at    timestamptz not null default now(),
  finished_at   timestamptz,
  notes         text
);

-- A stated finding. `evidence` is the honesty floor made queryable: nothing is 'measured' unless it was.
create table if not exists claim (
  id            bigserial primary key,
  project_id    text not null references project(id),
  subproblem_id text references subproblem(id),
  scale_id      text references scale(id),
  statement     text not null,
  evidence      text not null check (evidence in
                 ('measured','simulated','derived','literature','assumed','refused','unknown')),
  value_num     double precision,
  units         text,
  source        text,
  read_level    text check (read_level in
                 ('full-text','abstract','listing','search-summary','could-not-access',null)),
  run_id        bigint references run(id),
  artifact_id   bigint references artifact(id),
  superseded_by bigint references claim(id),
  created_at    timestamptz not null default now()
);

-- The hard part: where one scale hands a number to another. `calibration` is the vocabulary that
-- stops a scenario being read as a calibrated model.
create table if not exists junction (
  id            bigserial primary key,
  project_id    text not null references project(id),
  from_scale    text not null references scale(id),
  to_scale      text not null references scale(id),
  quantity      text not null,
  calibration   text not null check (calibration in
                 ('calibrated','uncalibrated','scenario','assumed','refused')),
  justification text not null,
  claim_id      bigint references claim(id),
  created_at    timestamptz not null default now()
);

-- The swarm itself, so credit burn and progress are both queryable.
create table if not exists agent_session (
  id            text primary key,           -- cloud session id, or a local agent name
  project_id    text references project(id),
  subproblem_id text references subproblem(id),
  harness       text not null,              -- cloud | local | orchestra
  account       text,
  model         text,
  status        text,
  cost_usd      double precision,
  credit_before double precision,
  branch        text,
  started_at    timestamptz not null default now(),
  finished_at   timestamptz,
  result        text
);

-- Adversarial review: a challenge to a claim, and whether the claim survived it.
create table if not exists challenge (
  id            bigserial primary key,
  claim_id      bigint not null references claim(id),
  challenger    text not null,
  attack        text not null,              -- the specific way it tries to break the claim
  outcome       text check (outcome in ('survived','refuted','weakened','not-run',null)),
  evidence      text,
  created_at    timestamptz not null default now()
);

create index if not exists idx_sub_status   on subproblem(project_id, status);
create index if not exists idx_sub_scale    on subproblem(project_id, scale_id);
create index if not exists idx_claim_sub    on claim(subproblem_id);
create index if not exists idx_claim_ev     on claim(project_id, evidence);
create index if not exists idx_art_sub      on artifact(subproblem_id);
create index if not exists idx_junc_proj    on junction(project_id, calibration);
create index if not exists idx_sess_status  on agent_session(status);
create index if not exists idx_chal_claim   on challenge(claim_id);
