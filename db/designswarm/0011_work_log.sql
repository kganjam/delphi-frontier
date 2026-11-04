--
-- PostgreSQL database dump
--

\restrict HlmGm1wLeok059eRB74q9Grcas6beAJHGOVH3SS12nwo9Vx6m0KFdJQjB4QDxuh

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
-- Name: work_log; Type: TABLE; Schema: public; Owner: morphoswarm
--

CREATE TABLE public.work_log (
    id bigint NOT NULL,
    project_id text,
    kind text NOT NULL,
    ref text NOT NULL,
    detail text,
    at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT work_log_kind_check CHECK ((kind = ANY (ARRAY['dispatched'::text, 'harvested'::text, 'scanned'::text, 'skipped'::text])))
);


ALTER TABLE public.work_log OWNER TO morphoswarm;

--
-- Name: work_log_id_seq; Type: SEQUENCE; Schema: public; Owner: morphoswarm
--

CREATE SEQUENCE public.work_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.work_log_id_seq OWNER TO morphoswarm;

--
-- Name: work_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: morphoswarm
--

ALTER SEQUENCE public.work_log_id_seq OWNED BY public.work_log.id;


--
-- Name: work_log id; Type: DEFAULT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.work_log ALTER COLUMN id SET DEFAULT nextval('public.work_log_id_seq'::regclass);


--
-- Name: work_log work_log_kind_ref_key; Type: CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.work_log
    ADD CONSTRAINT work_log_kind_ref_key UNIQUE (kind, ref);


--
-- Name: work_log work_log_pkey; Type: CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.work_log
    ADD CONSTRAINT work_log_pkey PRIMARY KEY (id);


--
-- Name: work_log work_log_project_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: morphoswarm
--

ALTER TABLE ONLY public.work_log
    ADD CONSTRAINT work_log_project_id_fkey FOREIGN KEY (project_id) REFERENCES public.project(id);


--
-- PostgreSQL database dump complete
--

\unrestrict HlmGm1wLeok059eRB74q9Grcas6beAJHGOVH3SS12nwo9Vx6m0KFdJQjB4QDxuh

