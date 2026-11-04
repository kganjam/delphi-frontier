-- ============================================================================================
-- PROJECT HISTORY: append-only, replayable, with design revisions visible.
--
-- What existed already covered SUPERSESSION -- claim.superseded_by, immutable part_revision,
-- retraction, regime_transition -- which satisfies ASK dimension 4's "without overwriting earlier
-- states". It did NOT give replay. The graph could say what is true now and what was corrected,
-- but not "what did this project look like at 02:00", which is what makes a design auditable
-- rather than merely current.
--
-- The log is written by TRIGGERS, not by callers. A history that depends on every writer
-- remembering to append is a history with holes exactly where someone was in a hurry.
-- ============================================================================================

create table if not exists project_event (
  seq           bigserial primary key,          -- total order; the replay cursor
  project_id    text,
  at            timestamptz not null default now(),
  actor         text,                           -- session, agent or trigger
  entity_type   text not null,
  entity_id     text not null,
  op            text not null check (op in ('insert','update','delete')),
  field         text,                           -- for an update, which field moved
  old_value     jsonb,
  new_value     jsonb,
  note          text
);
create index if not exists idx_event_entity on project_event(entity_type, entity_id, seq);
create index if not exists idx_event_at on project_event(project_id, at);

-- A named point you can cite and return to. A design revision is a snapshot with a label.
create table if not exists project_snapshot (
  id            text primary key,               -- 'zebrafish-flight@r3'
  project_id    text not null references project(id),
  label         text not null,
  at_seq        bigint not null,                -- replay the log up to here
  taken_at      timestamptz not null default now(),
  reason        text not null,
  counts        jsonb                           -- cheap summary so a reader sees the shape at once
);

-- Generic capture. Records the whole row on insert, and only the fields that MOVED on update --
-- a diff is readable where a full row dump is not, and the point of a history is that someone
-- reads it.
create or replace function log_event() returns trigger as $$
declare
  pid text; k text; oldj jsonb; newj jsonb; eid text;
begin
  oldj := case when TG_OP = 'INSERT' then '{}'::jsonb else to_jsonb(OLD) end;
  newj := case when TG_OP = 'DELETE' then '{}'::jsonb else to_jsonb(NEW) end;
  eid  := coalesce(newj->>'id', oldj->>'id', '?');
  pid  := coalesce(newj->>'project_id', oldj->>'project_id');

  if TG_OP = 'UPDATE' then
    -- one row per changed field, so "when did this value change and to what" is a single query
    for k in select jsonb_object_keys(newj) loop
      if (oldj->k) is distinct from (newj->k) then
        insert into project_event (project_id, actor, entity_type, entity_id, op, field, old_value, new_value)
        values (pid, current_user, TG_TABLE_NAME, eid, 'update', k, oldj->k, newj->k);
      end if;
    end loop;
  else
    insert into project_event (project_id, actor, entity_type, entity_id, op, new_value, old_value)
    values (pid, current_user, TG_TABLE_NAME, eid, lower(TG_OP),
            case when TG_OP='DELETE' then null else newj end,
            case when TG_OP='DELETE' then oldj else null end);
  end if;
  return coalesce(NEW, OLD);
end;
$$ language plpgsql;

do $$
declare t text;
begin
  foreach t in array array['claim','subproblem','part','part_revision','spec_parameter',
                           'challenge','regime_transition','retraction','idea','resource','setting'] loop
    execute format('drop trigger if exists trg_hist_%1$s on %1$I', t);
    execute format('create trigger trg_hist_%1$s after insert or update or delete on %1$I
                    for each row execute function log_event()', t);
  end loop;
end $$;

-- Replay: the state of one entity as of a sequence number.
create or replace function entity_at(etype text, eid text, upto bigint)
returns jsonb as $$
declare state jsonb := '{}'::jsonb; r record;
begin
  for r in select op, field, new_value from project_event
            where entity_type = etype and entity_id = eid and seq <= upto order by seq loop
    if r.op = 'insert' then state := r.new_value;
    elsif r.op = 'update' then state := jsonb_set(state, array[r.field], coalesce(r.new_value,'null'::jsonb));
    elsif r.op = 'delete' then state := '{}'::jsonb;
    end if;
  end loop;
  return state;
end;
$$ language plpgsql;
