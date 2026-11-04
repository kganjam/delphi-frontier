-- Dependency propagation; see docs/specs/SPEC-ASK-artifact-graph.md section 4 item 2.
-- Authoritative copy is the live schema in Postgres; this records the shape.
--
-- PostgreSQL database dump
--

\restrict EtWK7hMB8fbVSIhQex7nNGh4ZTlPoH2UWOLgldHV1DZOBlWXd0ICTG5rKyUXi4D

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: claim_depends; Type: TABLE; Schema: public; Owner: morphoswarm
--

CREATE TABLE public.claim_depends (
    claim_id bigint NOT NULL,
    depends_on bigint NOT NULL,
    how text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.claim_depends OWNER TO morphoswarm;

--
-- Name: review_flag; Type: TABLE; Schema: public; Owner: morphoswarm
--

CREATE TABLE public.review_flag (
    id bigint NOT NULL,
    claim_id bigint,
    subproblem_id text,
    part_id text,
    triggered_by bigint NOT NULL,
    reason text NOT NULL,
    depth integer DEFAULT 1 NOT NULL,
    status text DEFAULT 'open'::text NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    resolved_at timestamp with time zone,
    resolution text,
    CONSTRAINT review_flag_status_check CHECK ((status = ANY (ARRAY['open'::text, 'reviewed'::text, 'cleared'::text, 'confirmed-broken'::text])))
);


ALTER TABLE public.review_flag OWNER TO morphoswarm;

--
-- Name: review_flag_id_seq; Type: SEQUENCE; Schema: public; Owner: morphoswarm
--

CREATE SEQUENCE public.review_flag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.review_flag_id_seq OWNER TO morphoswarm;

--
-- Name: review_flag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: morphoswarm
--

ALTER SEQUENCE public.review_flag_id_seq OWNED BY public.review_flag.id;


--
-- Name: review_flag id; Type: DEFAULT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.review_flag ALTER COLUMN id SET DEFAULT nextval('public.review_flag_id_seq'::regclass);


--
-- Name: claim_depends claim_depends_pkey; Type: CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.claim_depends
    ADD CONSTRAINT claim_depends_pkey PRIMARY KEY (claim_id, depends_on);


--
-- Name: review_flag review_flag_pkey; Type: CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.review_flag
    ADD CONSTRAINT review_flag_pkey PRIMARY KEY (id);


--
-- Name: idx_dep_on; Type: INDEX; Schema: public; Owner: morphoswarm
--

CREATE INDEX idx_dep_on ON public.claim_depends USING btree (depends_on);


--
-- Name: idx_flag_status; Type: INDEX; Schema: public; Owner: morphoswarm
--

CREATE INDEX idx_flag_status ON public.review_flag USING btree (status, depth);


--
-- Name: claim_depends claim_depends_claim_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.claim_depends
    ADD CONSTRAINT claim_depends_claim_id_fkey FOREIGN KEY (claim_id) REFERENCES public.claim(id) ON DELETE CASCADE;


--
-- Name: claim_depends claim_depends_depends_on_fkey; Type: FK CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.claim_depends
    ADD CONSTRAINT claim_depends_depends_on_fkey FOREIGN KEY (depends_on) REFERENCES public.claim(id) ON DELETE CASCADE;


--
-- Name: review_flag review_flag_claim_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.review_flag
    ADD CONSTRAINT review_flag_claim_id_fkey FOREIGN KEY (claim_id) REFERENCES public.claim(id);


--
-- Name: review_flag review_flag_part_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.review_flag
    ADD CONSTRAINT review_flag_part_id_fkey FOREIGN KEY (part_id) REFERENCES public.part(id);


--
-- Name: review_flag review_flag_subproblem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.review_flag
    ADD CONSTRAINT review_flag_subproblem_id_fkey FOREIGN KEY (subproblem_id) REFERENCES public.subproblem(id);


--
-- Name: review_flag review_flag_triggered_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.review_flag
    ADD CONSTRAINT review_flag_triggered_by_fkey FOREIGN KEY (triggered_by) REFERENCES public.claim(id);


--
-- Name: TABLE claim_depends; Type: ACL; Schema: public; Owner: morphoswarm
--

GRANT ALL ON TABLE public.claim_depends TO morphoswarm_agent;


--
-- Name: TABLE review_flag; Type: ACL; Schema: public; Owner: morphoswarm
--

GRANT ALL ON TABLE public.review_flag TO morphoswarm_agent;


--
-- Name: SEQUENCE review_flag_id_seq; Type: ACL; Schema: public; Owner: morphoswarm
--

GRANT ALL ON SEQUENCE public.review_flag_id_seq TO morphoswarm_agent;


--
-- PostgreSQL database dump complete
--

\unrestrict EtWK7hMB8fbVSIhQex7nNGh4ZTlPoH2UWOLgldHV1DZOBlWXd0ICTG5rKyUXi4D

CREATE OR REPLACE FUNCTION public.propagate_supersession(root bigint)
 RETURNS integer
 LANGUAGE plpgsql
AS $function$
declare n int := 0;
begin
  with recursive affected(claim_id, depth) as (
      select cd.claim_id, 1 from claim_depends cd where cd.depends_on = root
    union
      select cd.claim_id, a.depth + 1
        from claim_depends cd join affected a on cd.depends_on = a.claim_id
       where a.depth < 6
  )
  insert into review_flag (claim_id, triggered_by, reason, depth)
  select a.claim_id, root,
         'an input it depends on was superseded; recheck whether the conclusion still holds',
         min(a.depth)
    from affected a
   where not exists (select 1 from review_flag f
                      where f.claim_id = a.claim_id and f.triggered_by = root and f.status='open')
   group by a.claim_id;
  get diagnostics n = row_count;

  -- The subproblem that owns a flagged claim needs review too: its recorded answer may rest on it.
  insert into review_flag (subproblem_id, triggered_by, reason, depth)
  select distinct c.subproblem_id, root,
         'a claim recorded under this subproblem depends on a superseded input', 1
    from claim c
   where c.id in (select claim_id from review_flag where triggered_by = root and status='open')
     and c.subproblem_id is not null
     and not exists (select 1 from review_flag f
                      where f.subproblem_id = c.subproblem_id and f.triggered_by = root and f.status='open');
  return n;
end;
$function$

CREATE OR REPLACE FUNCTION public.on_claim_superseded()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
begin
  if new.superseded_by is not null and (old.superseded_by is null or old.superseded_by <> new.superseded_by) then
    perform propagate_supersession(new.id);
  end if;
  return new;
end;
$function$

