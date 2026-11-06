-- ============================================================================================
-- IDEA INTAKE -> DUE DILIGENCE -> PROJECT PROMOTION, and the settings that govern a project.
-- Specced in docs/specs/SPEC-idea-intake-and-settings.md.
--
-- The design principle: an idea is NOT a project. Most ideas should die cheaply, and the system's
-- job is to kill them cheaply and record why, so the same idea arriving twice is recognised rather
-- than re-investigated. Promotion to a project is the expensive, deliberate step.
-- ============================================================================================

create table if not exists idea (
  id            bigserial primary key,
  title         text not null,
  body          text not null,                 -- what the person actually typed, VERBATIM
  submitted_by  text,
  submitted_at  timestamptz not null default now(),
  -- The design question in the form the system can act on. Written by an agent, NOT by the
  -- submitter, and kept separate from `body` so the original wording is never lost to a tidy-up.
  normalised_question text,
  target_scales text[],
  status        text not null default 'new'
                check (status in ('new','triaging','parked','rejected','promoted','duplicate')),
  duplicate_of  bigint references idea(id),
  decided_at    timestamptz,
  decision_note text,
  project_id    text references project(id)    -- set on promotion
);

-- Cheap due diligence, run BEFORE any promotion. Each check is a row so a partial assessment is
-- visible as partial rather than looking like a completed one.
create table if not exists idea_check (
  id            bigserial primary key,
  idea_id       bigint not null references idea(id) on delete cascade,
  check_kind    text not null check (check_kind in
                 ('prior-art','physical-plausibility','binding-constraint','existing-coverage',
                  'tractability','ethics-and-safety','resource-estimate')),
  verdict       text check (verdict in ('pass','fail','uncertain','not-run')),
  finding       text,
  evidence      text check (evidence in ('measured','derived','literature','assumed','unknown',null)),
  source        text,
  read_level    text,
  run_by        text,
  created_at    timestamptz not null default now()
);

-- Ranking. The score is a function of the CHECKS, never of the idea's wording or its author --
-- AGENTS.md section 1 rule 3: never compute a score from anything but the thing being scored.
create table if not exists idea_score (
  id            bigserial primary key,
  idea_id       bigint not null references idea(id) on delete cascade,
  rubric_id     text references rubric(id),
  grader        text not null,
  scores        jsonb not null,
  total         double precision,
  rationale     text,
  created_at    timestamptz not null default now()
);

-- ------------------------------------------------------------------------------------------
-- SETTINGS, at two levels. A project setting overrides a system setting of the same key; nothing
-- else overrides anything, because a deeper override chain is where configuration becomes
-- unauditable. `locked` marks a setting an agent may read but never change -- the honesty floor
-- lives here, and a system that can relax its own standards will.
-- ------------------------------------------------------------------------------------------
create table if not exists setting (
  scope         text not null check (scope in ('system','project')),
  project_id    text references project(id),
  key           text not null,
  value         jsonb not null,
  locked        boolean not null default false,
  reason        text,
  updated_at    timestamptz not null default now(),
  updated_by    text,
  id            bigserial primary key
);
-- Postgres will not take an expression in a PRIMARY KEY, so uniqueness is a unique INDEX over the
-- same expression. A system setting has project_id NULL, and coalesce makes the pair comparable.
create unique index if not exists uq_setting_scope_key on setting (scope, coalesce(project_id,''), key);

-- What the swarm is permitted to do on a project, read at dispatch time rather than compiled in.
create table if not exists project_capability (
  project_id    text not null references project(id),
  capability    text not null,                 -- mcp_server | skill | model | tool | dataset
  name          text not null,
  enabled       boolean not null default true,
  config        jsonb,
  reason        text,
  primary key (project_id, capability, name)
);

create index if not exists idx_idea_status on idea(status);
create index if not exists idx_check_idea on idea_check(idea_id);
create index if not exists idx_setting_key on setting(key);

-- System defaults. These are the ones that must not be negotiable.
insert into setting (scope, project_id, key, value, locked, reason, updated_by) values
 ('system', null, 'honesty.evidence_required', 'true', true,
  'Every recorded value carries how it was obtained. Not negotiable at any level.', 'bootstrap'),
 ('system', null, 'honesty.read_level_required', 'true', true,
  'Every literature source carries a read-level. A search summary is a lead, not evidence.', 'bootstrap'),
 ('system', null, 'honesty.supersede_never_overwrite', 'true', true,
  'Corrections create a new record. ASK dimension 4.', 'bootstrap'),
 ('system', null, 'honesty.grader_must_be_calibrated', 'true', true,
  'A grader is an instrument; an uncalibrated one measures itself.', 'bootstrap'),
 ('system', null, 'billing.forbid_owner_card', 'true', true,
  'No action may bill the owner''s payment method. Granted and subscription capacity only.', 'bootstrap'),
 ('system', null, 'billing.forbidden_accounts', '["api_allen","ent_allen"]', true,
  'Owner instruction, 2026-11-04: do not spend the Allen Institute enterprise API credit.', 'bootstrap'),
 ('system', null, 'swarm.max_concurrent_cloud', '40', false,
  'Concurrent cloud sessions held open by the monitor.', 'bootstrap'),
 ('system', null, 'swarm.nebius_max_in_flight', '1', false,
  'Measured workbench limit: one operation per key, enforced server-side.', 'bootstrap')
on conflict do nothing;
