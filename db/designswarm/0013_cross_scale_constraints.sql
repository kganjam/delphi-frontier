-- Cross-scale constraints. See docs/architecture/cross-scale-constraints.md.
-- A claim at scale N entails requirements at N+-1; those requirements ARE the verification, and
-- they double as the parameter prior for a simulation at the target scale.

create table if not exists constraint_entailed (
  id            bigserial primary key,
  project_id    text references project(id),
  source_claim  bigint references claim(id),      -- the claim that ENTAILS this requirement
  source_scale  text references scale(id),
  target_scale  text references scale(id) not null,
  kind          text not null check (kind in
                 ('existence','range','timescale','spatial','energetic','conservation')),
  statement     text not null,                    -- generic: names a ROLE, not a molecule
  quantity      text,
  lo            double precision,
  hi            double precision,
  units         text,
  status        text not null default 'open' check (status in
                 ('open','satisfied','unsatisfied','unsatisfiable','assumed')),
  satisfied_by  text,                             -- what fills the role, with its own evidence
  satisfied_evidence text check (satisfied_evidence in
                 ('measured','simulated','derived','literature','assumed','unknown',null)),
  note          text,
  created_at    timestamptz not null default now()
);
create index if not exists idx_con_status on constraint_entailed(status, target_scale);
create index if not exists idx_con_source on constraint_entailed(source_claim);

-- The verification criterion made queryable: a claim is verified to the extent its entailed
-- constraints are satisfied. An OPEN existence constraint is a missing part, not a weak model.
create or replace view claim_multiscale_support as
select c.id, left(c.statement, 90) as claim, c.evidence,
       count(k.id) as entailed,
       count(*) filter (where k.status='satisfied')     as satisfied,
       count(*) filter (where k.status='open')          as open,
       count(*) filter (where k.status='unsatisfiable') as unsatisfiable,
       case when count(k.id)=0 then 'no constraints written'
            when count(*) filter (where k.status='unsatisfiable') > 0 then 'REFUTED FROM BELOW'
            when count(*) filter (where k.status='open') > 0 then 'scenario: has unsatisfied requirements'
            else 'supported at adjacent scales' end as multiscale_status
  from claim c left join constraint_entailed k on k.source_claim = c.id
 where c.superseded_by is null
 group by c.id, c.statement, c.evidence;
