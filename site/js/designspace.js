/* Studio > design spaces. A design space is not a design: it maps the routes to a stated outcome across scales, each with its own
 * evidence level, and runs the models that can be run. ONE renderer serves every design space, because the only thing that differs
 * between them is data — the authored prose in site/content/design-spaces/<id>.json, the route map and the computed studies indexed
 * by results/<id>/index.json. Adding a design space is a data directory, never an edit to this file.
 *
 * Every route is drawn from that design space's own route file with its own evidence level; every figure is a recorded simulation or
 * analysis, never an observation. Rows the data declares at a scale the page does not declare are shown in a stated "unplaced" group
 * rather than dropped, so a mismatch between the two files is visible instead of silent. */
(function () {
  const DF = window.DF; const { html, raw } = DF; const U = DF.ui;

  const ALL = (snap) => snap.design_spaces || {};
  const L = (snap, id) => ALL(snap)[id] || null;

  /* Evidence strength is each design space's own vocabulary — a mouse phenotype, a coral phenotype, an insect phenotype — so the tone
   * map matches on the SHAPE of the value instead of enumerating them. An unrecognised strength still prints, in the neutral tone,
   * rather than being dropped or silently renamed. A route file may override any label through its own `evidence_labels` map, which is
   * the only place a design space's wording for its own vocabulary belongs. */
  const evTone = (s) => {
    const t = String(s || "");
    if (/^direct_\w+_phenotype$/.test(t)) return "ok";
    if (/^direct_/.test(t)) return "done";
    if (/_inference$/.test(t)) return "cur";
    if (t === "model_only") return "st-unk";
    if (t === "proposed") return "warn";
    return "st-unk";
  };
  const evText = (R, s) => ((R || {}).evidence_labels || {})[s] || String(s === undefined || s === null || s === "" ? "not stated" : s).replace(/_/g, " ");
  const DIFF_TONE = { low: "ok", medium: "warn", high: "no" };
  const CHAIN_TONE = { model: "ok", scenario: "warn", refused: "no", assumption: "warn" };
  const evPill = (R, s) => U.pill(evText(R, s), evTone(s));

  /* The outcome filter. Which outcomes a design space distinguishes is the whole point of that design space — amelia versus truncation
   * for a limb, bleaching versus morphology for a coral — so the classes are declared by the route file as
   * `outcome_classes: [{key, label, match}]`, `match` being a regular expression read against the route's predicted phenotype. A design
   * space that declares none simply has no outcome filter; nothing here invents a classification for it. */
  const outcomeClasses = (R) => ((R || {}).outcome_classes || []).filter((c) => c && c.key && c.label);
  /* These patterns are authored in Python files, and Python accepts a leading inline flag — `(?i)` — that JavaScript's RegExp
   * rejects outright as a syntax error. Every match then throws, every route silently loses its outcome tag, the filter has
   * nothing to offer and is not rendered, and the page dies later on a missing form field: a long way from the cause. The
   * flag is redundant here because the "i" below already supplies it, so stripping it changes no behaviour and costs nothing
   * for a pattern that never had one. */
  const jsRe = (p) => new RegExp(String(p).replace(/^\(\?[imsx]+\)/, ""), "i");
  const outcomeKey = (R, r) => {
    const t = String(r.predicted_phenotype || "");
    const hit = outcomeClasses(R).find((c) => { try { return c.match && jsRe(c.match).test(t); } catch (e) { return false; } });
    return hit ? hit.key : "";
  };

  /* ----------------------------------------------------------------- the card that appears in the Studio project list */
  DF.designSpace = {
    ids(snap) { return Object.keys(ALL(snap)); },
    listed(snap) { return Object.entries(ALL(snap)).filter(([, l]) => l && l.listed !== false).map(([id]) => id); },

    card(snap, id) {
      const l = L(snap, id); if (!l) return "";
      const c = l.counts || {};
      return html`<article class="card pform dscard"><h3>${l.title} ${U.pill(l.group, "grp")} ${U.pill("design space, not a design", "warn")}</h3>
        <p><b>Question.</b> ${l.goal}</p><p class="small">${l.summary}</p>
        <p class="small faint">${c.routes || 0} sourced routes across ${(l.scales || []).length} scales · ${c.studies_present || 0} of ${c.studies_declared || 0} computed studies present · ${l.nothing_attempted_note || "nothing here has been attempted."}</p>
        <p><a class="btn" href="${DF.href("/studio/" + id)}">Open the design space</a></p></article>`;
    },

    page(snap, id, route) { return page(snap, id, route); },
  };

  /* A short alias per design space, so a page can be shared as #/<id> as well as from inside the Studio. The alias is registered from
   * the data, so a new design space gets one without this file changing. DF.views is read at route time, and the snapshot is not in
   * scope here, so the aliases are installed once the snapshot is first seen. */
  DF.registerDesignSpaceAliases = function (snap) {
    Object.keys(ALL(snap)).forEach((id) => {
      if (!DF.views[id]) DF.views[id] = function (s, r) { return page(s, id, r); };
    });
  };

  /* An authored block whose keys ARE its headings: the route file decides what sections it has, and a section it adds later
   * appears without a code change rather than being silently dropped. Keys are humanised; nothing is reordered or renamed. */
  const HEAD = (k) => k.replace(/_/g, " ").replace(/\biacuc\b/i, "IACUC").replace(/^./, (c) => c.toUpperCase());
  /* A record's field can itself hold an object or a list, and `String()` renders an object as the literal "[object Object]".
   * One such field -- a control whose `result` is a dict of its own measurements -- put that on a published page, and it is
   * the kind of defect that reads as a rendering glitch rather than as missing data, so nobody files it. Flatten instead:
   * lists join, objects become "key: value; key: value", and the content stays readable without inventing a layout for an
   * arbitrarily nested shape. A design space that wants better presentation than this should give the field a schema. */
  const flat = (v) => (v === null || v === undefined ? ""
    : Array.isArray(v) ? v.map(flat).join(", ")
    : typeof v === "object" ? Object.entries(v).map(([k, x]) => `${HEAD(k)}: ${flat(x)}`).join("; ")
    : String(v));
  function blocks(obj, skip = []) {
    if (!obj) return "";
    return Object.entries(obj).filter(([k, v]) => !skip.includes(k) && v !== null && v !== undefined && (!Array.isArray(v) || v.length)).map(([k, v]) => {
      if (typeof v === "string") return html`<h3>${HEAD(k)}</h3><p>${v}</p>`;
      if (Array.isArray(v)) return html`<h3>${HEAD(k)}</h3><ul>${v.map((x) => {
        if (typeof x === "string") return html`<li>${x}</li>`;
        /* A list of records usually leads with the field the list is named after ("refinements" -> "refinement"), and
         * repeating that label on every row is noise. Lead with its value; label only the fields that add something. */
        const ent = Object.entries(x); const [k0, v0] = ent[0] || ["", ""];
        const lead = k.toLowerCase().includes(k0.toLowerCase()) && typeof v0 === "string";
        const rest = lead ? ent.slice(1) : ent;
        return html`<li>${lead ? html`${v0} ` : ""}${rest.map(([kk, vv]) => html`<b>${HEAD(kk)}:</b> ${flat(vv)} `)}</li>`;
      })}</ul>`;
      if (typeof v === "object") return html`<h3>${HEAD(k)}</h3><dl class="dsmeta">${Object.entries(v).map(([kk, vv]) => html`<dt>${HEAD(kk)}</dt><dd>${typeof vv === "string" ? vv : JSON.stringify(vv)}</dd>`)}</dl>`;
      return html`<h3>${HEAD(k)}</h3><p>${String(v)}</p>`;
    });
  }

  /* ----------------------------------------------------------------- where each family of routes acts, drawn once.
   * A schematic of the system the routes act on, never a measurement and never to scale: it exists so a reader can see that the routes
   * are interventions at different places in ONE system rather than a list of interchangeable genes. Each pin filters the routes below.
   *
   * The drawing itself is an authored file per design space (site/content/design-spaces/<id>.schematic.svg, inlined by the build) and
   * the pins are data beside it, so a pin and the list item describing it are written once and cannot disagree. Only the NUMBER goes in
   * the figure; the names are in the caption list, because four label pairs inside one drawing collided at 390 px and the numbers do
   * not. A design space that declares no schematic simply has none — nothing here draws a generic diagram to fill the space. */
  function schematic(l) {
    const S = l.schematic; if (!S || !S.svg) return "";
    const have = new Set(((l.routes || {}).routes || []).map((r) => r.scale));
    const pins = (S.pins || []).filter((p) => p && p.name);
    const label = (key) => { const s = (l.scales || []).find((x) => x.key === key); return s ? s.label : key; };
    return html`<figure class="dsschem">
      <svg viewBox="${S.viewBox || "0 0 960 440"}" role="img" aria-labelledby="dsschemt dsschemd" preserveAspectRatio="xMidYMid meet">
        <title id="dsschemt">${S.title || "Where each family of routes acts"}</title>
        <desc id="dsschemd">${S.desc || ""}</desc>
        ${raw(S.svg)}
        ${pins.map((p, i) => html`<g class="dspin ${have.has(p.scale) ? "" : "off"}" data-scale="${p.scale}" tabindex="0" role="button" aria-label="${(i + 1) + ". " + p.name}: ${p.note || ""} Activate to show only routes at this scale.">
          <circle cx="${p.x}" cy="${p.y}" r="15"></circle><text x="${p.x}" y="${p.y + 5}" text-anchor="middle" class="dsb-pin">${i + 1}</text></g>`)}
      </svg>
      <figcaption class="small">${S.caption || "Schematic, not a measurement and not to scale."} Each numbered pin is a place the routes below act; select one to show only that scale.
        <ol class="dspinlist small">${pins.map((p) => html`<li data-scale="${p.scale}"><b>${p.name}</b> <span class="faint">(${label(p.scale)})</span> — ${p.note || ""}</li>`)}</ol></figcaption></figure>`;
  }

  /* ----------------------------------------------------------------- routes */
  /* Several of these fields are authored as a list of one or more strings (species an observation was made in, for
   * instance) and several as a plain string. Joining here rather than at each call site means a design space may
   * author either shape without the renderer caring, and an empty list renders as nothing rather than as "". */
  const listish = (v) => (Array.isArray(v) ? v.filter((x) => x !== null && x !== undefined && String(x).trim()).join(", ") : (v === null || v === undefined ? "" : String(v).trim()));

  const routeCard = (R) => function (r, i) {
    const ev = r.evidence || [];
    /* The card leads with the one thing that distinguishes these routes from each other — the outcome it predicts — and folds the
     * mechanism, the intervention and the trade-offs. With dozens of routes the alternative is a page nobody finishes. */
    return html`<article class="dsroute" id="route-${r.id || "r" + i}" data-scale="${r.scale || ""}" data-strength="${r.evidence_strength || ""}" data-phen="${outcomeKey(R, r)}">
      <h4>${r.title || r.id}</h4>
      <p class="dstags">${evPill(R, r.evidence_strength)} ${r.difficulty ? U.pill("difficulty: " + String(r.difficulty).split(/[.,]/)[0], DIFF_TONE[String(r.difficulty).toLowerCase().split(/[ -]/)[0]] || "st-unk") : ""} ${r.study ? html`<a class="pill ev" href="#study-${r.study}">we ran something on this</a>` : ""}</p>
      <p class="dsphen"><b>Predicted phenotype.</b> ${r.predicted_phenotype || "not stated"}</p>
      <details class="dsdet"><summary>How it works, what it costs, and the evidence${ev.length ? " (" + ev.length + ")" : ""}</summary>
        <p class="small"><b>Mechanism.</b> ${r.mechanism || ""}</p>
        <p class="small"><b>What you would actually do.</b> ${r.intervention || "not stated"}</p>
        <dl class="dsmeta small">
          ${r.specificity ? html`<dt>Specificity</dt><dd>${r.specificity}</dd>` : ""}
          ${listish(r.species_of_evidence) ? html`<dt>Evidence comes from</dt><dd>${listish(r.species_of_evidence)}</dd>` : ""}
          ${r.route_kind ? html`<dt>Kind of route</dt><dd>${String(r.route_kind).replace(/_/g, " ")}</dd>` : ""}
          ${r.addressable_runtime_control === undefined ? "" : html`<dt>Addressable at runtime?</dt><dd>${r.addressable_runtime_control ? "yes — appearance can be changed on command" : "no — the change is made once, not driven"}</dd>`}
          ${r.reversibility ? html`<dt>Reversible?</dt><dd>${r.reversibility}</dd>` : ""}
          ${r.lethality_risk ? html`<dt>Lethality risk</dt><dd>${r.lethality_risk}</dd>` : ""}
          ${r.difficulty ? html`<dt>Difficulty</dt><dd>${r.difficulty}</dd>` : ""}
          ${r.what_we_would_run ? html`<dt>What bears on it here</dt><dd>${r.what_we_would_run}</dd>` : ""}
        </dl>
        ${ev.length ? html`<h5 class="small">Sources</h5><ul class="small dsevlist">${ev.map((e) => html`<li>${e.cite || ""} ${e.read_level ? U.pill(e.read_level + " read", "rl") : ""}${e.pmid ? html`<br><a href="https://pubmed.ncbi.nlm.nih.gov/${String(e.pmid)}/" target="_blank" rel="noopener noreferrer">PMID ${e.pmid}</a>` : ""}${e.doi ? html` <span class="faint">doi ${e.doi}</span>` : ""}${e.finding ? html`<br>${e.finding}` : ""}</li>`)}</ul>`
          : html`<p class="small faint">No source is attached to this route, so it is a proposal only.</p>`}
        ${(r.open_questions || []).length ? html`<h5 class="small">Open questions</h5><ul class="small">${r.open_questions.map((q) => html`<li>${q}</li>`)}</ul>` : ""}
      </details></article>`;
  }

  function routesSection(l) {
    const R = l.routes || {}; const rs = R.routes || [];
    if (!rs.length) return html`<section class="panel" id="routes"><h2>The design space</h2><p class="empty">${R.present === false ? "The route file " + (R.data || "") + " is not in this build, so no route is shown. The page does not invent one." : "No route is recorded yet."}</p></section>`;
    const declared = (l.scales || []).map((s) => s.key);
    const groups = (l.scales || []).map((s) => ({ ...s, rows: rs.filter((r) => r.scale === s.key) }));
    const unplaced = rs.filter((r) => !declared.includes(r.scale));
    const strengths = [...new Set(rs.map((r) => r.evidence_strength).filter(Boolean))];
    /* Only the outcome classes that some route actually matches, in the order the route file declared them. A class the data declares
     * and no route satisfies would otherwise sit in the filter as an option that always yields nothing. */
    const matched = new Set(rs.map((r) => outcomeKey(R, r)).filter(Boolean));
    const phens = outcomeClasses(R).filter((c) => matched.has(c.key));
    const card = routeCard(R);
    return html`<section class="panel" id="routes" aria-labelledby="ds-rt"><h2 id="ds-rt">The design space: ${rs.length} routes across ${groups.filter((g) => g.rows.length).length} scales</h2>
      <p class="note small">Every row is a published perturbation or a bounded proposal, with its own evidence level. <b>${R.nothing_attempted || "None of them has been attempted here."}</b> The filters below are a reading aid; they change nothing and submit nothing.</p>
      <form class="dsfilter filters" aria-label="Filter routes">
        <label>Scale <select name="scale"><option value="">all scales</option>${groups.filter((g) => g.rows.length).map((g) => html`<option value="${g.key}">${g.label} (${g.rows.length})</option>`)}</select></label>
        ${phens.length ? html`<label>${R.outcome_filter_label || "Outcome"} <select name="phen"><option value="">any outcome</option>${phens.map((c) => html`<option value="${c.key}">${c.label}</option>`)}</select></label>` : ""}
        <label>Evidence <select name="strength"><option value="">any evidence level</option>${strengths.map((s) => html`<option value="${s}">${evText(R, s)}</option>`)}</select></label>
        <span class="small faint" id="dscount" role="status"></span></form>
      ${groups.filter((g) => g.rows.length).map((g) => html`<section class="dsscale" data-scale="${g.key}"><h3>${g.label} <span class="faint small">${g.rows.length} route${g.rows.length === 1 ? "" : "s"}</span></h3>
        <p class="small faint">${g.blurb || ""}</p><div class="dsroutes">${g.rows.map(card)}</div></section>`)}
      ${unplaced.length ? html`<section class="dsscale" data-scale="__unplaced"><h3>Unplaced <span class="faint small">${unplaced.length}</span></h3>
        <p class="note warn small">These routes name a scale this page does not declare (${[...new Set(unplaced.map((r) => r.scale))].join(", ")}). They are shown rather than dropped, so the mismatch between the route file and the page is visible.</p>
        <div class="dsroutes">${unplaced.map(card)}</div></section>` : ""}
      ${R.href ? html`<p class="small"><a href="${R.href}" download>Download the route file</a> <span class="faint">sha256 ${U.sha(R.sha256)}</span></p>` : ""}</section>`;
  }

  /* ----------------------------------------------------------------- one computed study: figures, equations, parameter provenance, controls */
  /* A parameter arrives in one of two shapes and `String(p.value)` was wrong for both of the interesting ones. A point
   * value is `value` + `units`. A PRIOR is `lo`/`hi`/`distribution` with no `value` at all (coral's settlement study),
   * and reading `value` there printed the word "undefined" into nine live rows that also lost their names, because the
   * names are under `label`/`key` in that shape. A null `value` is the third case and it is deliberate: chromatophore
   * marks its one fitted parameter and its one swept parameter that way, and "null" in the cell reports a decision as
   * a glitch. Say which of the three it is; never stringify the raw value. */
  function paramValue(p) {
    if (typeof p.value === "number") return DF.fmt(p.value, 4);
    if (p.value !== null && p.value !== undefined && String(p.value).trim() !== "") return String(p.value);
    if (typeof p.lo === "number" && typeof p.hi === "number") {
      return html`${DF.fmt(p.lo, 4)} to ${DF.fmt(p.hi, 4)}${p.distribution ? html` <span class="faint small">(${String(p.distribution)})</span>` : ""}`;
    }
    return html`<span class="faint">not a fixed input</span>`;
  }

  function paramTable(params) {
    if (!params || !params.length) return "";
    const tone = { sourced: "ok", measured: "ok", assumed: "warn", nondimensional: "grp", derived: "cur" };
    return html`<details><summary><b>${params.length} parameters</b> <span class="faint small">each marked sourced or assumed; an assumed value is not a measurement</span></summary>
      <div class="tablewrap"><table><thead><tr><th scope="col">Parameter</th><th scope="col">Value</th><th scope="col">Units</th><th scope="col">Status</th><th scope="col">Source or justification</th></tr></thead>
      <tbody>${params.map((p) => html`<tr><td><code>${p.name || p.label || p.key || ""}</code></td><td>${paramValue(p)}</td><td class="small">${p.units || ""}</td><td>${U.pill(String(p.status || "not stated").replace(/_/g, " "), tone[p.status] || "st-unk")}</td><td class="small">${p.source || p.justification || ""}</td></tr>`)}</tbody></table></div></details>`;
  }

  /* The threshold of each design knob, with the numerical uncertainty taken from the refinement arm when the sweep itself
   * does not carry one. A threshold with no uncertainty beside it is reported as "not reported", never as exact. */
  /* A sweep arrives in one of two shapes: a knob with a threshold (the ODE study) or a series of runs (the Turing study).
   * Rendering both from one function keeps the page honest about which it has, instead of printing an empty threshold column. */
  function sweepSeries(d) {
    const sweeps = d.sweeps || {}; const desc = d.sweep_descriptions || {};
    const keys = Object.keys(sweeps).filter((k) => Array.isArray(sweeps[k])); if (!keys.length) return "";
    return html`<h4>What each knob does, run by run</h4>
      <p class="small faint">Element counts are the mean over the recorded seeds, with their spread: a Turing pattern is seed-dependent and an average alone would hide that. The class is assigned by a rule declared before the sweep was read.</p>
      ${keys.map((k) => { const rows = sweeps[k]; return html`<details><summary><b>${k.replace(/_/g, " ")}</b> <span class="faint small">${rows.length} settings</span></summary>
        ${desc[k] ? html`<p class="small">${desc[k]}</p>` : ""}
        <div class="tablewrap"><table><thead><tr><th scope="col">Setting</th><th scope="col">Elements (mean ± sd)</th><th scope="col">Seeds</th><th scope="col">Class</th>${rows[0] && rows[0].ap_extent_in_wavelengths !== undefined ? html`<th scope="col">AP width (wavelengths)</th>` : ""}</tr></thead>
        <tbody>${rows.map((r) => html`<tr><td>${DF.fmt(r.value, 3)}</td><td>${DF.fmt(r.element_count_mean, 3)} ± ${DF.fmt(r.element_count_sd, 2)}</td><td>${r.n_seeds === undefined ? "" : r.n_seeds}</td><td class="small">${r.cls || r.class || ""}</td>${r.ap_extent_in_wavelengths !== undefined ? html`<td>${DF.fmt(r.ap_extent_in_wavelengths, 3)}</td>` : ""}</tr>`)}</tbody></table></div></details>`; })}`;
  }

  function sweepTable(d) {
    const all = d.sweeps || {}; const sweeps = Object.fromEntries(Object.entries(all).filter(([, v]) => v && !Array.isArray(v)));
    const keys = Object.keys(sweeps); if (!keys.length) return sweepSeries(d);
    const ref = ((d.refinement_arm || {}).thresholds) || {};
    const unc = (k, s) => {
      const u = s.threshold_uncertainty !== undefined && s.threshold_uncertainty !== null ? s.threshold_uncertainty : (ref[k] || {}).uncertainty;
      if (u === undefined || u === null) return html`<span class="faint">not reported</span>`;
      return typeof u === "number" ? "± " + DF.fmt(u, 2) : String(u);
    };
    return html`<h4>What each knob does, and where it breaks</h4>
      <p class="small faint">A threshold is the value of that knob below which this model's loop never engages. It is a property of the model; the uncertainty beside it is how far the number moved across integrators and tolerances, which is not the same as being right.</p>
      <div class="tablewrap"><table><thead><tr><th scope="col">Knob</th><th scope="col">What it stands for</th><th scope="col">Threshold</th><th scope="col">Numerical uncertainty</th></tr></thead>
      <tbody>${keys.map((k) => { const s = sweeps[k] || {}; return html`<tr><td><code>${k}</code>${s.label ? html`<br><span class="small faint">${s.label}</span>` : ""}</td><td class="small">${s.meaning || s.description || ""}${s.source ? html`<br><span class="faint">${s.source}</span>` : ""}</td><td>${s.threshold === undefined || s.threshold === null ? html`<span class="faint">none in the range swept</span>` : DF.fmt(s.threshold, 3)}${s.threshold_note ? html`<br><span class="small faint">${s.threshold_note}</span>` : ""}</td><td class="small">${unc(k, s)}</td></tr>`; })}</tbody></table></div>
      ${sweepSeries(d)}`;
  }

  function listOf(title, items, cls) {
    if (!items || !items.length) return "";
    /* `result` is whatever the study recorded, and a control that reports several measurements records a dict there. Passing
     * that straight into the template prints "[object Object]" where the result belongs -- which looks like a styling bug
     * rather than a missing measurement, so it gets ignored. `flat` renders it instead. */
    return html`<h4>${title}</h4><ul class="small ${cls || ""}">${items.map((x) => html`<li>${typeof x === "string" ? x : (x.name ? html`<b>${x.name}.</b> ${flat(x.result || x.text || x.note || "")}` : JSON.stringify(x))}</li>`)}</ul>`;
  }

  function studySection(s) {
    const d = s.data || {};
    const model = d.model || {};
    const eqs = model.equations_latex || d.equations_latex || [];
    const sources = d.sources || [];
    const figs = (s.figures || []).filter((f) => f.state === "present");
    const missing = (s.figures || []).filter((f) => f.state !== "present");
    return html`<section class="panel dsstudy" id="study-${s.id}" aria-labelledby="st-${s.id}">
      <h3 id="st-${s.id}">${s.title} ${U.pill(s.kind || "computed", "warn")} ${s.scale ? U.pill(s.scale, "grp") : ""}</h3>
      ${s.present ? "" : html`<p class="note warn dsabsent"><b>Declared and not present.</b> The result file <code>${s.data_path || ""}</code> is not in this build, so nothing below is shown for it. It is listed rather than hidden.</p>`}
      ${s.summary ? html`<p>${s.summary}</p>` : ""}
      ${s.question ? html`<p class="small"><b>The design question it answers.</b> ${s.question}</p>` : ""}
      ${figs.length ? html`<div class="dsfigs">${figs.map((f) => html`<figure>${/\.(mp4|webm)$/.test(f.file) ? html`<video controls playsinline muted loop preload="metadata" src="${f.href}" aria-label="${f.alt || f.caption || s.title}"></video>` : html`<img src="${f.href}" alt="${f.alt || f.caption || s.title}" loading="lazy">`}<figcaption class="small">${f.caption || ""} <span class="faint">${/simulation/i.test(s.kind || "") ? "Simulation output" : "Analysis output"}, not an observation. sha256 ${U.sha(f.sha256)}</span></figcaption></figure>`)}</div>` : ""}
      ${missing.length ? html`<p class="small faint">${missing.length} declared figure${missing.length === 1 ? "" : "s"} not in this build: ${missing.map((f) => f.file).join(", ")}.</p>` : ""}
      ${d.headline ? html`<p class="dshead"><b>${d.headline}</b></p>` : ""}
      ${eqs.length ? html`<h4>The model, as written</h4><div class="dseqs">${eqs.map((e) => html`<div class="eqcard">${typeof e === "string" ? DF.texSpan(e, true) : html`${e.name ? html`<h5>${e.name}</h5>` : ""}${DF.texSpan(e.latex || e.tex || "", true)}${e.note ? html`<p class="small faint">${e.note}</p>` : ""}`}</div>`)}</div>` : ""}
      ${(model.edges || []).length ? html`<details><summary><b>${model.edges.length} regulatory edges</b> <span class="faint small">each one's source, or marked assumed</span></summary><ul class="small">${model.edges.map((e) => html`<li><code>${e.from || e.source_node || "?"} → ${e.to || e.target || "?"}</code> ${e.sign ? U.pill(e.sign, e.sign === "activates" || e.sign === "+" ? "ok" : "no") : ""} ${e.note || e.description || ""} ${e.source && e.source !== "assumed" ? html`<span class="faint">[${e.source}]</span>` : U.pill("assumed", "warn")}</li>`)}</ul></details>` : ""}
      ${paramTable(model.parameters || d.parameters)}
      ${sweepTable(d)}
      ${Object.keys(d).filter((k) => /^one_condition/.test(k)).map((k) => { const u = d[k] || {};
        return html`<div class="dscrit"><h4>What the sweeps have in common</h4><p class="dshead">${u.statement || ""}</p>
          ${Object.entries(u).filter(([kk]) => kk !== "statement").map(([kk, vv]) => html`<p class="small"><b>${kk.replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase())}.</b> ${String(vv)}</p>`)}</div>`; })}
      ${d.classification_rule_change ? html`<details><summary><b>The counting rule was changed after the first run</b> <span class="faint small">recorded rather than quietly made</span></summary><p class="small">${typeof d.classification_rule_change === "string" ? d.classification_rule_change : JSON.stringify(d.classification_rule_change)}</p></details>` : ""}
      ${d.controls && !Array.isArray(d.controls) ? html`<details><summary><b>Controls</b> <span class="faint small">${Object.values(d.controls).filter((c) => c && c.pass === false || (c && /DID NOT/.test(String(c.result || "")))).length ? "one of them did not behave as designed, and says so" : "each with what it had to show"}</span></summary>
        <dl class="dsmeta small">${Object.entries(d.controls).map(([k, c]) => html`<dt>${k.replace(/_/g, " ")}</dt><dd>${c && typeof c === "object" ? Object.entries(c).map(([kk, vv]) => html`<b>${kk.replace(/_/g, " ")}:</b> ${typeof vv === "number" ? DF.fmt(vv, 4) : String(vv)}. `) : String(c)}</dd>`)}</dl></details>` : ""}
      ${d.critical_domain_size ? (() => { const c = d.critical_domain_size;
        return html`<div class="dscrit"><h4>Critical domain size</h4>
          ${c.value === null || c.value === undefined
            ? html`<p class="small"><b>Not resolved to a number by this sweep.</b> ${c.definition ? "It is defined as: " + c.definition : ""}</p>`
            : html`<p class="dshead"><b>${DF.fmt(c.value, 3)} ${c.units || ""}</b>${c.uncertainty ? " ± " + DF.fmt(c.uncertainty, 2) : ""}${c.axis ? html` <span class="small faint">measured on the ${c.axis}</span>` : ""}</p>
              ${c.value_under_the_original_counting_rule !== undefined ? html`<p class="small"><b>And ${DF.fmt(c.value_under_the_original_counting_rule, 3)} ${c.units || ""}${c.uncertainty_under_the_original_counting_rule ? " \u00b1 " + DF.fmt(c.uncertainty_under_the_original_counting_rule, 2) : ""} under the counting rule that was declared first.</b> ${c.rule_sensitivity || ""}</p>` : ""}`}
          ${c.reading ? html`<p class="small">${c.reading}</p>` : ""}</div>`; })() : ""}
      ${d.linear_stability ? (() => { const L = d.linear_stability; const m = d.measured_wavelength; const cmp = (m && m.comparison_to_linear_prediction) || {};
        return html`<div class="dsctrl"><h4>Internal control: does the pattern have the wavelength the maths predicts?</h4>
          <p class="small">Linear stability analysis predicts ${DF.fmt(L.predicted_wavelength, 4)} ${L.predicted_wavelength_units || ""}${L.predicted_at_F !== undefined ? " at the operating point used" : ""}. ${typeof m === "number" ? "The simulated pattern measures " + DF.fmt(m, 4) + "." : (m && m.two_d_AP_element_spacing !== undefined ? "The simulated two-dimensional pattern measures " + DF.fmt(m.two_d_AP_element_spacing, 4) + "." : "")}</p>
          ${cmp.verdict ? html`<p class="note warn small"><b>Verdict.</b> ${cmp.verdict}</p>` : ""}
          ${L.published_set_check ? html`<details><summary><b>Could the published parameter set be reproduced?</b> <span class="faint small">${L.published_set_check.answer || ""}</span></summary>
            <p class="small"><b>Question.</b> ${L.published_set_check.question}</p><p class="small"><b>Scope of the search.</b> ${L.published_set_check.scope}</p>
            ${L.published_set_check.diagnosis ? html`<p class="small"><b>Diagnosis.</b> ${L.published_set_check.diagnosis}</p>` : ""}
            ${L.published_set_check.what_this_does_and_does_not_mean ? html`<p class="note small">${L.published_set_check.what_this_does_and_does_not_mean}</p>` : ""}</details>` : ""}
          <details><summary class="small">Method</summary><p class="small">${L.method || ""}</p></details></div>`; })() : ""}
      ${d.control_arm ? html`<details><summary><b>Control arm</b> <span class="faint small">run first; the design sweep is only read if this passes</span></summary><pre class="small dsjson">${JSON.stringify(d.control_arm, null, 1)}</pre></details>` : ""}
      ${d.refinement_arm ? html`<details><summary><b>Refinement arm</b> <span class="faint small">a tighter solver or a finer grid; how far the answer moved</span></summary><pre class="small dsjson">${JSON.stringify(d.refinement_arm, null, 1)}</pre></details>` : ""}
      ${Object.keys(d).filter((k) => /_ablation$/.test(k)).map((k) => { const ab = d[k] || {}; const arms = ab.arms || [];
        if (!arms.length) return "";
        const cols = [...new Set(arms.flatMap((a) => Object.keys(a)))];
        return html`<h4>${k.replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase())}</h4>
          <p class="small faint">Each published mechanism removed on its own, to find out which one the result actually rests on. This is the arm most likely to contradict the author, and it is reported either way.</p>
          <div class="tablewrap"><table><thead><tr>${cols.map((c) => html`<th scope="col">${c.replace(/_/g, " ")}</th>`)}</tr></thead>
          <tbody>${arms.map((a) => html`<tr>${cols.map((c) => html`<td class="small">${a[c] === undefined || a[c] === null ? html`<span class="faint">—</span>` : (typeof a[c] === "number" ? DF.fmt(a[c], 4) : (a[c] === true ? U.pill("yes", "ok") : a[c] === false ? U.pill("no", "no") : String(a[c])))}</td>`)}</tr>`)}</tbody></table></div>
          ${ab.finding ? html`<p class="note warn small"><b>What it found.</b> ${ab.finding}</p>` : ""}`; })}
      ${Array.isArray(d.controls) ? listOf("Controls", d.controls) : ""}
      ${listOf("Numerical checks", d.numerical_checks)}
      ${d.phenotype_classes ? html`<details><summary><b>How each run was classified</b> <span class="faint small">declared before the sweep was read</span></summary><dl class="dsmeta small">${Object.entries(d.phenotype_classes).map(([k, v]) => html`<dt>${k}</dt><dd>${v}</dd>`)}</dl></details>` : ""}
      ${(d.retrievals || []).length ? html`<details><summary><b>${d.retrievals.length} retrievals</b> <span class="faint small">every sequence fetched, with its accession and digest</span></summary>
        <div class="tablewrap"><table><thead><tr><th scope="col">Species</th><th scope="col">Accession</th><th scope="col">Coordinates</th><th scope="col">HTTP</th><th scope="col">Bytes</th><th scope="col">sha256</th><th scope="col">Retrieved</th></tr></thead>
        <tbody>${d.retrievals.map((r) => html`<tr><td class="small">${r.species || ""}</td><td class="small">${r.url ? html`<a href="${r.url}" target="_blank" rel="noopener noreferrer">${r.accession || r.url}</a>` : (r.accession || "")}</td><td class="small">${r.coords || ""}</td><td>${r.http_status === undefined ? "" : r.http_status}</td><td>${r.bytes === undefined ? "" : r.bytes}</td><td>${r.sha256 ? U.sha(r.sha256) : ""}</td><td class="small">${r.retrieved_at || ""}</td></tr>`)}</tbody></table></div></details>` : ""}
      ${(d.summary_table || []).length ? (() => {
        /* The columns are the union over all rows, not the first row's keys: a field that appears only on the one row that
         * needs it (a species with no ZRS, say) would otherwise be dropped from the table without trace. */
        const cols = [...new Set(d.summary_table.flatMap((r) => Object.keys(r)))];
        const cell = (v) => v === null || v === undefined ? html`<span class="faint">—</span>` : (typeof v === "number" ? DF.fmt(v, 4) : (v === true ? U.pill("yes", "ok") : v === false ? U.pill("no", "no") : String(v)));
        return html`<h4>${d.summary_table_title || s.summary_table_title || "Per row"}</h4><div class="tablewrap"><table><thead><tr>${cols.map((k) => html`<th scope="col">${k.replace(/_/g, " ")}</th>`)}</tr></thead>
          <tbody>${d.summary_table.map((row) => html`<tr>${cols.map((k) => html`<td class="small">${cell(row[k])}</td>`)}</tr>`)}</tbody></table></div>
          <p class="small faint">An em dash means the field is not applicable or was not tested, never that it was measured as zero.</p>`;
      })() : ""}
      ${(d.limitations || []).length || (d.what_this_does_not_establish || []).length ? html`<div class="dslimits"><h4>What this study does not establish</h4>
        <ul class="small">${[...(d.what_this_does_not_establish || []), ...(d.limitations || [])].map((x) => html`<li>${typeof x === "string" ? x : (x.claim || x.text || JSON.stringify(x))}</li>`)}</ul></div>` : ""}
      ${sources.length ? html`<details><summary><b>${sources.length} sources</b> <span class="faint small">with read levels</span></summary><ul class="small">${sources.map((x) => html`<li>${x.cite || x.title || ""} ${x.read_level ? U.pill(x.read_level + " read", "rl") : ""}${x.pmid ? html`<br><a href="https://pubmed.ncbi.nlm.nih.gov/${String(x.pmid)}/" target="_blank" rel="noopener noreferrer">PMID ${x.pmid}</a>` : ""}${x.doi ? html` <span class="faint">doi ${x.doi}</span>` : ""}</li>`)}</ul></details>` : ""}
      <p class="small faint">${s.code ? html`Code: <code>${s.code}</code>. ` : ""}${s.data_href ? html`<a href="${s.data_href}" download>Download the full result file</a> · ` : ""}sha256 ${U.sha(s.sha256)}</p></section>`;
  }

  /* ----------------------------------------------------------------- the page */
  function page(snap, id, route) {
    const l = L(snap, id);
    if (!l) return { html: html`<section class="pagehead"><h1>Design space</h1><p class="lede">This build carries no content block for <code>${id}</code>, so the page says so rather than inventing one. <a href="${DF.href("/studio")}">Back to the Studio</a>.</p></section>` };
    const R = l.routes || {}; const rec = R.recommendation || null; const welfare = R.welfare || null; const genes = R.judge_gene_candidates || [];
    const chain = l.chain || {};
    const allSources = [...new Set([...(R.sources || []).map((s) => s.pmid).filter(Boolean)])];
    return {
      html: html`<section class="pagehead dshead-sec"><p class="eyebrow"><a href="${DF.href("/studio")}">Studio</a> / ${l.group}</p><h1>${l.title}</h1>
        <p class="lede">${l.goal}</p>
        <p>${U.pill("design space, not a design", "warn")} ${l.scope_pill ? U.pill(l.scope_pill, "ok") : ""} ${U.pill((l.counts || {}).routes + " sourced routes", "cur")} ${U.pill((l.counts || {}).studies_present + " computed studies", "ev")}</p></section>

      <section class="panel dsanswer" aria-labelledby="ds-a"><h2 id="ds-a">${(l.answer || {}).headline || "The answer"}</h2>
        <div class="dscols">${((l.answer || {}).paragraphs || []).map((p) => html`<p>${p}</p>`)}</div>
        ${(l.answer || {}).precision_note ? html`<p class="note warn">${l.answer.precision_note}</p>` : ""}
        <p class="small"><a href="#routes">Jump to the ${(l.counts || {}).routes || 0} routes</a> · <a href="#studies">what we ran</a> · <a href="#chain">where the chain breaks</a>${(l.routes || {}).welfare ? html` · <a href="#welfare">${(l.routes || {}).welfare_title || "welfare and 3Rs"}</a>` : ""}</p></section>

      ${rec ? html`<section class="panel dsrec" aria-labelledby="ds-rec"><h2 id="ds-rec">${R.recommendation_title || "If you asked us to actually do it"}</h2>
        ${rec.single_best_route ? html`<p class="small"><b>The route:</b> <a href="#route-${rec.single_best_route}">${(((l.routes || {}).routes || []).find((r) => r.id === rec.single_best_route) || {}).title || rec.single_best_route}</a></p>` : ""}
        ${blocks(rec, ["single_best_route"])}</section>` : ""}

      ${(l.schematic || {}).svg ? html`<section class="panel dsschemsec" aria-labelledby="ds-bd"><h2 id="ds-bd">${l.schematic.section_title || "Where the routes act"}</h2>
        ${l.schematic.intro ? html`<p class="small">${l.schematic.intro}</p>` : ""}
        ${schematic(l)}</section>` : ""}

      ${routesSection(l)}

      <section class="panel" id="studies" aria-labelledby="ds-st"><h2 id="ds-st">What we ran</h2>
        <p class="note small">${l.studies_note || html`${(l.counts || {}).studies_declared || 0} studies, each one a <b>computed model or analysis</b>. None is an observation. Each carries its own controls and a statement of what it does not establish.`}</p>
        ${(l.studies || []).map(studySection)}</section>

      <section class="panel dschain" id="chain" aria-labelledby="ds-ch"><h2 id="ds-ch">${chain.title || "The chain across scales"}</h2>
        ${chain.intro ? html`<p>${chain.intro}</p>` : ""}
        <ol class="dslinks">${(chain.links || []).map((k) => html`<li class="dslink ${k.status}"><p><b>${k.from}</b> <span class="dsarrow" aria-hidden="true">→</span> <b>${k.to}</b> ${U.pill(k.status === "model" ? "inside one model" : k.status, CHAIN_TONE[k.status] || "st-unk")}</p><p class="small">${k.note}</p></li>`)}</ol>
        ${chain.verdict ? html`<p class="note warn">${chain.verdict}</p>` : ""}
        <p class="small faint">This is the same discipline the rest of this site applies to every cross-scale coupling: a junction is composable, scenario-level, or refused. <a href="${DF.href("/studio/flying-fish", { scale: "organ" })}">The flying-fish project uses the same contract.</a></p></section>

      ${genes.length ? html`<section class="panel" id="genes" aria-labelledby="ds-g"><h2 id="ds-g">${R.gene_table_title || "Candidate genes, and what each would actually give you"}</h2>
        <p class="small">${R.gene_table_note || "Several genes fit the description and they do not produce the same organism. The last column is the question that would tell them apart."}</p>
        <div class="tablewrap"><table class="dsgenes"><caption class="sr">Candidate genes, what each would actually produce, and the question that distinguishes them</caption>
        <thead><tr><th scope="col">Gene</th><th scope="col">Evidence is in</th><th scope="col">What it would actually produce</th><th scope="col">Why a researcher might say this</th><th scope="col">The question that tells them apart</th></tr></thead>
        <tbody>${genes.map((g) => html`<tr><td><b>${g.gene || g.name}</b>${g.key_pmid ? html`<br><a class="small" href="https://pubmed.ncbi.nlm.nih.gov/${String(g.key_pmid)}/" target="_blank" rel="noopener noreferrer">PMID ${g.key_pmid}</a>` : ""}</td>
          <td class="small">${g.species_of_evidence || g.species || ""}</td><td class="small">${g.what_it_would_actually_produce || g.effect || ""}</td>
          <td class="small">${g.why_a_researcher_might_say_this || ""}</td><td class="small">${g.distinguishing_question || ""}</td></tr>`)}</tbody></table></div></section>` : ""}

      ${welfare ? html`<section class="panel dswelfare" id="welfare" aria-labelledby="ds-w"><h2 id="ds-w">${R.welfare_title || "Animal welfare and the 3Rs"}</h2>
        ${blocks(welfare)}</section>` : ""}

      <section class="panel dsnot" aria-labelledby="ds-n"><h2 id="ds-n">What this page does not claim</h2>
        <ul>${(l.not_claimed || []).map((x) => html`<li>${x}</li>`)}</ul>
        ${(R.limitations || []).length ? html`<h3>Limits the route map states for itself</h3><ul class="small">${R.limitations.map((x) => html`<li>${x}</li>`)}</ul>` : ""}
        <p class="small faint">Page text <code>${l.content_path || ""}</code> sha256 ${U.sha(l.content_sha256)}; studies indexed by <code>${l.index_path || ""}</code> sha256 ${U.sha(l.index_sha256)}. ${allSources.length ? allSources.length + " distinct PubMed identifiers are cited across the routes." : ""}</p></section>

      ${l.closing ? html`<section class="panel"><h2>${l.closing.title}</h2><p>${l.closing.text}</p>
        <p class="small"><a href="${DF.href("/studio")}">All projects</a> · <a href="${DF.href("/frontier")}">Open questions</a>${l.closing.link ? html` · <a href="${l.closing.link.href}" target="_blank" rel="noopener noreferrer">${l.closing.link.text || "The longer written answer in the repository"}</a>` : ""}</p></section>` : ""}`,

      after(root) {
        DF.renderMath(root);
        const form = root.querySelector(".dsfilter"); if (!form) return;
        const count = root.querySelector("#dscount");
        const apply = () => {
          const want = { scale: form.scale.value, phen: form.phen.value, strength: form.strength.value };
          let shown = 0, total = 0;
          root.querySelectorAll(".dsroute").forEach((el) => {
            total++;
            const ok = (!want.scale || el.dataset.scale === want.scale) && (!want.phen || el.dataset.phen === want.phen) && (!want.strength || el.dataset.strength === want.strength);
            el.hidden = !ok; if (ok) shown++;
          });
          root.querySelectorAll(".dsscale").forEach((sec) => { sec.hidden = ![...sec.querySelectorAll(".dsroute")].some((el) => !el.hidden); });
          count.textContent = shown === total ? `showing all ${total} routes` : `showing ${shown} of ${total} routes`;
          root.querySelectorAll(".dspin").forEach((g) => g.classList.toggle("on", !!want.scale && g.dataset.scale === want.scale));
        };
        const pick = (sc) => { form.scale.value = sc === form.scale.value ? "" : sc; apply(); const t = root.querySelector("#routes"); if (t) t.scrollIntoView({ behavior: "smooth", block: "start" }); };
        root.querySelectorAll(".dspin").forEach((g) => {
          g.addEventListener("click", () => pick(g.dataset.scale));
          g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(g.dataset.scale); } });
        });
        form.addEventListener("change", apply);
        form.addEventListener("submit", (e) => e.preventDefault());
        apply();
      },
    };
  }
})();
