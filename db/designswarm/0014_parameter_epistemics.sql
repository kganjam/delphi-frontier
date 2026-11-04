-- ============================================================================================
-- THE EPISTEMIC GRAPH FOR SIMULATION PARAMETERS.
--
-- A simulation parameter is not a number. It is a POSTERIOR: an estimate, an interval, the route
-- by which it was obtained, the other quantities that route depends on, the assumptions that
-- license it, and the conditions under which it holds.
--
-- Two kinds of node, and keeping them apart is the point:
--   * PARAMETER   -- a quantity with a distribution.
--   * STRUCTURAL  -- a claim that a process FOLLOWS a particular law or model form.
-- "We assume this scales as M^(3/4)" is not a parameter value; it is a choice of model, and it can
-- be wrong in ways no amount of parameter refinement will reveal. Statistics calls this
-- model-structure uncertainty, and conflating it with parameter uncertainty is how a well-fitted
-- wrong model comes to look well-supported.
-- ============================================================================================

create table if not exists parameter (
  id            text primary key,                 -- 'CL_max.zebrafish-wing'
  project_id    text references project(id),
  symbol        text not null,
  name          text not null,
  description   text not null,                    -- what it IS, for a reader who does not know
  units         text,
  dimension     text,
  point         double precision,
  lo            double precision,                 -- interval, NOT a fabricated +/-
  hi            double precision,
  interval_kind text check (interval_kind in
                 ('measured-ci','observed-range','expert-range','sensitivity-bound','none',null)),
  derivation    text not null check (derivation in
                 ('measured','derived','fitted','assumed','borrowed','unknown')),
  how           text not null,                    -- the actual route, in words
  conditions    text,                             -- a value without its conditions is not a parameter
  source        text,
  read_level    text,
  superseded_by text references parameter(id),
  created_at    timestamptz not null default now()
);

-- The DAG. An estimate depends on other estimates; that structure is what uncertainty propagates
-- along, and what tells you which measurement would most reduce the spread.
create table if not exists parameter_depends (
  parameter_id  text not null references parameter(id) on delete cascade,
  depends_on    text not null references parameter(id) on delete cascade,
  relation      text not null,                    -- 'input to formula' | 'calibration target' | 'proxy for'
  sensitivity   text,                             -- how hard this parent pushes the child
  primary key (parameter_id, depends_on)
);

-- Structural assumptions: WHICH LAW the process is taken to follow. Its own node, its own evidence,
-- its own alternatives -- because the alternative is usually what makes it falsifiable.
create table if not exists structural_assumption (
  id            text primary key,
  project_id    text references project(id),
  statement     text not null,                    -- 'lift follows the steady thin-airfoil relation'
  law_id        text,                             -- library/laws/<id>.yaml where one applies
  applies_to    text,                             -- the parameter or run it licenses
  evidence      text not null check (evidence in
                 ('measured','derived','literature','assumed','unknown')),
  alternatives  text,                             -- what else it could be; the falsifiable part
  consequence_if_wrong text not null,             -- REQUIRED: an assumption with no stated
                                                  -- consequence cannot be prioritised
  read_level    text,
  source        text
);

create table if not exists parameter_structural (
  parameter_id  text not null references parameter(id) on delete cascade,
  assumption_id text not null references structural_assumption(id) on delete cascade,
  primary key (parameter_id, assumption_id)
);

-- Tie a SIMULATION to what it actually used: its equations, its parameters, its data.
create table if not exists run_uses (
  run_id        bigint references run(id) on delete cascade,
  kind          text not null check (kind in ('parameter','law','dataset','structural','artifact')),
  ref           text not null,
  role          text,
  primary key (run_id, kind, ref)
);

create index if not exists idx_param_proj on parameter(project_id);
create index if not exists idx_pdep_on on parameter_depends(depends_on);

-- What would most reduce uncertainty: a parameter with many dependents, a wide interval, and a
-- weak derivation. This is the question "which measurement should we buy next", asked of the graph.
create or replace view parameter_leverage as
select p.id, p.symbol, p.point, p.lo, p.hi, p.derivation,
       (select count(*) from parameter_depends d where d.depends_on = p.id) as dependents,
       case when p.lo is not null and p.hi is not null and p.point is not null and p.point <> 0
            then round(((p.hi - p.lo) / abs(p.point))::numeric, 2) end as relative_spread,
       (select count(*) from parameter_structural s where s.parameter_id = p.id) as structural_assumptions
  from parameter p where p.superseded_by is null;
