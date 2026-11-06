-- ============================================================================================
-- THE RESOURCE GRAPH, and the evidence-aggregation primitive.
--
-- Both shapes are BORROWED FROM SciDEX substrate (migrations/0001_initial_schema.sql, SPEC-001
-- sections 6.1 and 10.1) rather than invented here, because they solve two problems better than
-- what this schema had:
--
--  * `schema_registry` makes artifact TYPES registered and versioned ("{type}@v{N}"), so a wiki
--    page, a protein, an analysis and a dataset live in one graph without a schema change each
--    time. Our `part.kind` was a closed enum, which cannot grow.
--  * `artifact_signals` is a GENERAL aggregation primitive -- entity, dimension, voter, value,
--    weight, unit, reason -- rather than an evaluation-specific grade table. Evidence aggregation
--    and decision models need exactly this shape.
--
-- Changes from the original are additive and marked.
-- ============================================================================================

create table if not exists schema_registry (
  id              text primary key,            -- "{type}@v{N}"
  artifact_type   text not null,
  schema_version  int not null,
  is_current      boolean not null default true,
  schema_json     jsonb not null,
  proposed_by     text,
  approved_at     timestamptz,
  created_at      timestamptz not null default now(),
  unique (artifact_type, schema_version)
);

-- A resource: anything a human or an agent might need to FIND. Papers, datasets, MCP servers,
-- databases, people, tools, wiki pages, software. Deliberately one table: the point of the graph is
-- that a protein and a paper and an MCP server are findable by the same query.
create table if not exists resource (
  id              text primary key,
  artifact_type   text not null,               -- resolves against schema_registry.artifact_type
  name            text not null,
  summary         text not null,               -- what it IS, one sentence, for a reader
  provides        text[],                      -- CAPABILITIES, which is how discovery works
  endpoint        text,
  auth_required   boolean,
  verified_at     timestamptz,                 -- when someone last confirmed it actually works
  verified_how    text,                        -- the command or probe, so it can be re-run
  status          text check (status in ('live','degraded','dead','unverified')),
  licence         text,
  payload         jsonb,                       -- type-specific fields, validated against the schema
  created_at      timestamptz not null default now()
);

-- An artifact may belong to a project OR be shared across all of them. A null project_id means
-- shared, which is the default for a resource: the whole point is cross-project reuse.
create table if not exists resource_project (
  resource_id   text not null references resource(id) on delete cascade,
  project_id    text not null references project(id) on delete cascade,
  used_how      text,
  primary key (resource_id, project_id)
);

-- The aggregation primitive. One row per signal ABOUT an entity, from one voter.
-- `voter_kind` matters: a measurement, a model's confidence and an agent's opinion are all signals
-- and must never be pooled as if they were the same thing.
create table if not exists artifact_signal (
  id            bigserial primary key,
  entity_type   text not null,                 -- 'claim' | 'resource' | 'part' | 'idea' | 'subproblem'
  entity_id     text not null,
  kind          text not null,                 -- 'reliability' | 'relevance' | 'confidence' | 'cost'
  dimension     text,
  voter_id      text not null,
  voter_kind    text not null check (voter_kind in
                 ('measurement','model','agent','human','derived','literature')),
  value         numeric not null,
  weight        numeric not null default 1.0,
  unit          text,
  reason        text not null,                 -- ADDED: a signal with no stated reason is a number
  metadata      jsonb,
  created_at    timestamptz not null default now()
);

create index if not exists idx_resource_type on resource(artifact_type, status);
create index if not exists idx_resource_provides on resource using gin(provides);
create index if not exists idx_signal_entity on artifact_signal(entity_type, entity_id, kind);
create index if not exists idx_signal_voter on artifact_signal(voter_id, voter_kind);

insert into schema_registry (id, artifact_type, schema_version, schema_json, proposed_by) values
 ('mcp-server@v1','mcp-server',1,'{"required":["name","endpoint","provides","status"],"optional":["auth_required","tools_count"]}','bootstrap'),
 ('database@v1','database',1,'{"required":["name","endpoint","provides"],"optional":["licence","record_count"]}','bootstrap'),
 ('paper@v1','paper',1,'{"required":["name","doi","read_level"],"optional":["sha256","local_path"]}','bootstrap'),
 ('dataset@v1','dataset',1,'{"required":["name","provides"],"optional":["licence","size_bytes","sha256"]}','bootstrap'),
 ('software@v1','software',1,'{"required":["name","provides"],"optional":["licence","repo","version"]}','bootstrap'),
 ('wiki-page@v1','wiki-page',1,'{"required":["name","summary"],"optional":["path","generated_from"]}','bootstrap'),
 ('protein@v1','protein',1,'{"required":["name","accession","sequence_sha256"],"optional":["structure_artifact"]}','bootstrap'),
 ('analysis@v1','analysis',1,'{"required":["name","run_id"],"optional":["code_sha","inputs"]}','bootstrap')
on conflict (id) do nothing;
