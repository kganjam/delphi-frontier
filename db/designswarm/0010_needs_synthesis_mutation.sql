-- ============================================================================================
-- Mechanisms from Wang, Marom, Pal, Luu, Lu, Berkovich & Buehler, arXiv:2603.14312, read at
-- full-text abstract and introduction. These are the four we did NOT have.
-- ============================================================================================

-- 1. NEEDS, broadcast mid-work to a shared global index.
-- Our `subproblem` is a question someone sat down and WROTE. A need is emitted by an agent in the
-- middle of doing something else -- "I require a measured modulus to finish this" -- and is the
-- unit that makes plannerless coordination possible: a peer with an idle slot fulfils it without
-- anyone assigning it.
create table if not exists need (
  id            bigserial primary key,
  project_id    text references project(id),
  raised_by     text not null,
  raised_at     timestamptz not null default now(),
  need_type     text not null,              -- measured-value | structure | law | dataset | method | review
  statement     text not null,
  atype         text,                       -- the artifact type that would satisfy it
  context       jsonb,
  depth         int not null default 0,     -- parent depth in the artifact DAG
  coverage      int not null default 0,     -- how many times it has been fulfilled already
  status        text not null default 'open' check (status in ('open','claimed','fulfilled','withdrawn')),
  fulfilled_by  bigint references claim(id),
  fulfilled_at  timestamptz
);
create index if not exists idx_need_open on need(status, need_type);

-- Pressure, computed exactly as ScienceClaw does it (artifacts/pressure.py:194), reproduced rather
-- than reinvented. No LLM in this loop: coordination stays reproducible and auditable. The age term
-- is the part worth keeping -- it is what stops an unglamorous need starving forever.
create or replace function need_pressure(n need) returns double precision as $$
  select 2.0 * (1.0 / (1.0 + n.coverage))
       + 1.0 * least(6.0, (select count(*) from need m
                            where m.atype = n.atype and m.id <> n.id and m.status = 'open'))
       + 0.5 * n.depth
       + 0.2 * ln(1 + greatest(0, extract(epoch from (now() - n.raised_at)) / 60.0));
$$ language sql stable;

-- 2. MULTI-PARENT SYNTHESIS on schema overlap.
-- The mechanism we most conspicuously lacked: when two INDEPENDENT analyses produce artifacts whose
-- schemas overlap, that overlap is itself a finding, and a synthesis is triggered. Our swarm ran 200
-- branches without ever cross-pollinating two results that touched the same quantity.
create table if not exists synthesis (
  id            bigserial primary key,
  project_id    text references project(id),
  parents       bigint[] not null,          -- the claims synthesised; >= 2 by construction
  overlap_on    text not null,              -- the shared quantity, scale or source
  trigger       text not null check (trigger in ('schema-overlap','shared-source','contradiction','same-quantity')),
  finding       text,
  status        text not null default 'proposed' check (status in ('proposed','running','recorded','rejected')),
  created_at    timestamptz not null default now()
);

-- 3. THE MUTATION LAYER: prune, fork or merge redundant and conflicting branches.
-- With 200+ branches the DAG grows faster than anyone reads it, and redundancy is indistinguishable
-- from corroboration unless something records which it is.
create table if not exists dag_mutation (
  id            bigserial primary key,
  project_id    text references project(id),
  action        text not null check (action in ('prune','fork','merge','supersede')),
  targets       text[] not null,
  reason        text not null,
  evidence      text,
  applied       boolean not null default false,
  created_at    timestamptz not null default now()
);

-- 4. AGENT PROFILES. In the paper agents select tools by their scientific profile; ours are
-- undifferentiated, which is also why their outputs are hard to compare -- an ensemble of identical
-- agents is one agent run many times.
create table if not exists agent_profile (
  id            text primary key,
  description   text not null,
  scales        text[],
  prefers       text[],                     -- tool or capability names
  disposition   text check (disposition in ('builder','breaker','synthesiser','measurer','reviewer')),
  created_at    timestamptz not null default now()
);

insert into agent_profile (id, description, scales, disposition) values
 ('builder','Proposes designs and extends existing ones. Optimistic by role, and its output is expected to be challenged.', null, 'builder'),
 ('breaker','Attacks claims and designs. Told to TRY and to report honestly when a claim survives, because an agent rewarded for finding faults manufactures them.', null, 'breaker'),
 ('synthesiser','Looks for overlap between independent results and proposes multi-parent syntheses.', null, 'synthesiser'),
 ('measurer','Hunts primary sources and replaces proxies with measured values.', null, 'measurer'),
 ('reviewer','Checks method rather than result: how would this pipeline produce a confident wrong answer?', null, 'reviewer')
on conflict (id) do nothing;

create index if not exists idx_synth_status on synthesis(status);
create index if not exists idx_mut_applied on dag_mutation(applied);
