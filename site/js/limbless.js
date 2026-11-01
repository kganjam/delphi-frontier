/* Studio > Limbless mouse: a design space rather than a design. Every route is drawn from snap.limbless.routes with its own evidence level;
 * every figure is a recorded simulation or sequence analysis, never an observation. Rows the data declares at a scale this page does not
 * declare are shown in a stated "unplaced" group rather than dropped, so a mismatch between the two files is visible instead of silent. */
(function () {
  const DF = window.DF; const { html, raw, esc } = DF; const U = DF.ui;

  const L = (snap) => snap.limbless || null;

  /* Evidence strength and difficulty are the data's own words; the tone map only chooses a colour and never rewrites a value. */
  const EV_TONE = { direct_mouse_phenotype: "ok", direct_other_species: "done", cis_regulatory_inference: "cur", model_only: "st-unk", proposed: "warn" };
  const EV_TEXT = { direct_mouse_phenotype: "direct mouse phenotype", direct_other_species: "direct, another species", cis_regulatory_inference: "cis-regulatory inference", model_only: "model only", proposed: "proposed" };
  const DIFF_TONE = { low: "ok", medium: "warn", high: "no" };
  const CHAIN_TONE = { model: "ok", scenario: "warn", refused: "no", assumption: "warn" };
  const evPill = (s) => U.pill(EV_TEXT[s] || String(s || "not stated").replace(/_/g, " "), EV_TONE[s] || "st-unk");

  const phenotypeKey = (r) => {
    const t = String(r.predicted_phenotype || "").toLowerCase();
    if (/amelia|no limb|absent limb|complete limb loss/.test(t)) return "amelia";
    if (/truncat|micromelia|stunted|reduced limb/.test(t)) return "truncation";
    if (/forelimb|hindlimb|one pair|single pair/.test(t)) return "one-pair";
    if (/digit|polydactyl|element/.test(t)) return "digits";
    return "other";
  };
  const PHEN_LABEL = { amelia: "Amelia (no limb at all)", truncation: "Truncation or micromelia", "one-pair": "One limb pair only", digits: "Digit or element change", other: "Other or mixed" };

  /* ----------------------------------------------------------------- the card that appears in the Studio project list */
  DF.limbless = {
    card(snap) {
      const l = L(snap); if (!l) return "";
      const c = l.counts || {};
      return html`<article class="card pform lmcard"><h3>${l.title} ${U.pill(l.group, "grp")} ${U.pill("design space, not a design", "warn")}</h3>
        <p><b>Question.</b> ${l.goal}</p><p class="small">${l.summary}</p>
        <p class="small faint">${c.routes || 0} sourced routes across ${(l.scales || []).length} scales · ${c.studies_present || 0} of ${c.studies_declared || 0} computed studies present · nothing here was run in an animal.</p>
        <p><a class="btn" href="${DF.href("/studio/limbless-mouse")}">Open the design space</a></p></article>`;
    },

    page(snap, route) { return page(snap, route); },
  };

  /* A short alias, so the page can be shared as #/limbless-mouse as well as from inside the Studio. */
  DF.views["limbless-mouse"] = function (snap, route) { return page(snap, route); };

  /* ----------------------------------------------------------------- where each family of routes acts, drawn once.
   * A schematic of a limb bud, not a measurement and not to scale: it exists so a reader can see that the routes on this page
   * act at different places in one system rather than being a list of interchangeable genes. Each pin filters the routes below. */
  function budDiagram(l) {
    const have = new Set(((l.routes || {}).routes || []).map((r) => r.scale));
    /* [x, y, number label, the scale the pin filters to, name, what acts there] */
    const PINS = [
      [70, 240, "gene", "Limb-field induction", "Tbx5 for the forelimb, Tbx4 and Pitx1 for the hindlimb, Meis1/2 proximally. Remove the field and nothing starts at all."],
      [205, 310, "molecular", "ZPA and its ZRS enhancer", "Shh is switched on in the ZPA by the ZRS, which sits about a megabase away inside an intron of Lmbr1. This is the cis-regulatory route: edit the switch, not the gene."],
      [330, 374, "gene", "Ridge induction", "Fgf10 from the mesenchyme and Wnt3 / β-catenin in the ectoderm raise the apical ectodermal ridge. Lose it and there is no limb at all — this is the amelia route."],
      [398, 168, "cellular", "Ridge maintenance", "The ridge itself: p63, Fgf4 and Fgf8, or physical ablation. The bud starts and then stops, which is truncation rather than absence."],
      [352, 240, "pattern", "Skeletal patterning", "BMP–SOX9–WNT sets how many elements the field makes and how far apart. A small enough field makes none."],
      [740, 200, "tissue", "The maintenance loop", "SHH → GREM1 ⊣ BMP ⊣ FGF → SHH. Break any arm and the bud stops being held open, whichever arm you break."],
    ];
    return html`<figure class="lmbud">
      <svg viewBox="0 0 960 440" role="img" aria-labelledby="budt budd" preserveAspectRatio="xMidYMid meet">
        <title id="budt">Where each family of routes acts on the limb bud</title>
        <desc id="budd">On the left, a schematic limb bud projecting from the body wall, with the apical ectodermal ridge along its distal rim, the zone of polarising activity at its posterior base and the progenitor mesenchyme between them. On the right, the maintenance loop drawn as a circuit of four nodes: SHH activates GREM1, GREM1 inhibits BMP, BMP inhibits FGF, and FGF activates SHH. Six numbered pins mark where the routes on this page act; each one is named in the list under this figure.</desc>
        <defs>
          <marker id="lmar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#0e7c86"></path></marker>
          <marker id="lmbar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M8 1 L8 9" stroke="#b3261e" stroke-width="2.6" fill="none"></path></marker>
        </defs>
        <rect x="0" y="0" width="960" height="440" fill="#fffdf8"></rect>
        <line x1="512" y1="40" x2="512" y2="400" stroke="#ddd3c0" stroke-dasharray="5 6"></line>
        <text x="265" y="42" class="lmb-ttl" text-anchor="middle">The bud</text>
        <text x="740" y="42" class="lmb-ttl" text-anchor="middle">The loop that holds it open</text>

        <rect x="20" y="80" width="90" height="320" rx="6" fill="#efe7d6" stroke="#ddd3c0"></rect>
        <text x="65" y="72" class="lmb-ax" text-anchor="middle">flank</text>
        <path d="M 110 150 C 210 136, 318 140, 372 152 C 418 163, 442 200, 442 245 C 442 290, 418 327, 372 338 C 318 350, 210 354, 110 340 Z" fill="#e3f1f1" stroke="#0e7c86" stroke-width="2"></path>
        <path d="M 372 152 C 418 163, 442 200, 442 245 C 442 290, 418 327, 372 338" fill="none" stroke="#9a6700" stroke-width="10" stroke-linecap="round" opacity=".9"></path>
        <text x="456" y="249" class="lmb-lab" text-anchor="start">AER</text>
        <text x="280" y="232" class="lmb-lab" text-anchor="middle">mesenchyme</text>
        <text x="280" y="250" class="lmb-sub" text-anchor="middle">progenitor pool</text>
        <ellipse cx="242" cy="310" rx="50" ry="21" fill="#fdf0d8" stroke="#c99a2e"></ellipse>
        <text x="248" y="315" class="lmb-lab" text-anchor="middle">ZPA</text>
        <path d="M 300 358 L 348 344" class="lmb-arr" marker-end="url(#lmar)"></path>
        <text x="294" y="362" class="lmb-sub" text-anchor="end">Fgf10 · Wnt3</text>
        <text x="265" y="124" class="lmb-sub" text-anchor="middle">proximal ← → distal</text>

        <ellipse cx="620" cy="120" rx="54" ry="23" fill="#fdf0d8" stroke="#c99a2e"></ellipse><text x="620" y="126" class="lmb-lab" text-anchor="middle">SHH</text>
        <ellipse cx="862" cy="120" rx="54" ry="23" fill="#e3f1f1" stroke="#0e7c86"></ellipse><text x="862" y="126" class="lmb-lab" text-anchor="middle">GREM1</text>
        <ellipse cx="862" cy="282" rx="54" ry="23" fill="#fffdf8" stroke="#8a74b8"></ellipse><text x="862" y="288" class="lmb-lab" text-anchor="middle">BMP</text>
        <ellipse cx="620" cy="282" rx="54" ry="23" fill="#fdf0d8" stroke="#9a6700"></ellipse><text x="620" y="288" class="lmb-lab" text-anchor="middle">FGF4/8</text>
        <path d="M 676 120 L 800 120" class="lmb-arr" marker-end="url(#lmar)"></path>
        <path d="M 862 164 L 862 257" class="lmb-arr inh" marker-end="url(#lmbar)"></path>
        <path d="M 806 282 L 676 282" class="lmb-arr inh" marker-end="url(#lmbar)"></path>
        <path d="M 620 257 L 620 164" class="lmb-arr" marker-end="url(#lmar)"></path>
        <text x="740" y="356" class="lmb-note" text-anchor="middle">break any arm and the bud stops growing</text>
        <text x="620" y="152" class="lmb-sub" text-anchor="middle">in the ZPA</text>
        <text x="862" y="152" class="lmb-sub" text-anchor="middle">in the mesenchyme</text>
        <text x="862" y="320" class="lmb-sub" text-anchor="middle">in the mesenchyme</text>
        <text x="620" y="320" class="lmb-sub" text-anchor="middle">in the ridge</text>

        ${PINS.map(([x, y, scale, name, note], i) => html`<g class="lmpin ${have.has(scale) ? "" : "off"}" data-scale="${scale}" tabindex="0" role="button" aria-label="${(i + 1) + ". " + name}: ${note} Activate to show only routes at this scale.">
          <circle cx="${x}" cy="${y}" r="15"></circle><text x="${x}" y="${y + 5}" text-anchor="middle" class="lmb-pin">${i + 1}</text></g>`)}
      </svg>
      <figcaption class="small">Schematic, not a measurement and not to scale. Each numbered pin is a place the routes below act; select one to show only that scale.
        <ol class="lmpinlist small">${PINS.map(([, , scale, name, note]) => html`<li data-scale="${scale}"><b>${name}</b> <span class="faint">(${(l.scales || []).find((s) => s.key === scale) ? l.scales.find((s) => s.key === scale).label : scale})</span> — ${note}</li>`)}</ol></figcaption></figure>`;
  }

  /* ----------------------------------------------------------------- routes */
  function routeCard(r, i) {
    const ev = r.evidence || [];
    return html`<article class="lmroute" id="route-${r.id || "r" + i}" data-scale="${r.scale || ""}" data-strength="${r.evidence_strength || ""}" data-phen="${phenotypeKey(r)}">
      <h4>${r.title || r.id}</h4>
      <p class="lmtags">${evPill(r.evidence_strength)} ${r.difficulty ? U.pill("difficulty: " + r.difficulty, DIFF_TONE[String(r.difficulty).toLowerCase()] || "st-unk") : ""} ${r.specificity ? U.pill(r.specificity, "grp") : ""}</p>
      <p class="lmphen"><b>Predicted phenotype.</b> ${r.predicted_phenotype || "not stated"}</p>
      <p class="small"><b>Mechanism.</b> ${r.mechanism || ""}</p>
      <p class="small"><b>What you would actually do.</b> ${r.intervention || "not stated"}</p>
      <dl class="lmmeta small">
        ${r.reversibility ? html`<dt>Reversible?</dt><dd>${r.reversibility}</dd>` : ""}
        ${r.lethality_risk ? html`<dt>Lethality risk</dt><dd>${r.lethality_risk}</dd>` : ""}
        ${r.what_we_would_run ? html`<dt>What bears on it here</dt><dd>${r.what_we_would_run}</dd>` : ""}
      </dl>
      ${ev.length ? html`<details class="lmev"><summary class="small"><b>${ev.length} source${ev.length === 1 ? "" : "s"}</b> <span class="faint">with read levels</span></summary><ul class="small">${ev.map((e) => html`<li>${e.cite || ""} ${e.read_level ? U.pill(e.read_level + " read", "rl") : ""}${e.pmid ? html`<br><a href="https://pubmed.ncbi.nlm.nih.gov/${String(e.pmid)}/" target="_blank" rel="noopener noreferrer">PMID ${e.pmid}</a>` : ""}${e.doi ? html` <span class="faint">doi ${e.doi}</span>` : ""}${e.finding ? html`<br><span class="small">${e.finding}</span>` : ""}</li>`)}</ul></details>`
        : html`<p class="small faint">No source is attached to this route, so it is a proposal only.</p>`}
      ${(r.open_questions || []).length ? html`<details class="small"><summary><b>Open questions</b></summary><ul>${r.open_questions.map((q) => html`<li>${q}</li>`)}</ul></details>` : ""}</article>`;
  }

  function routesSection(l) {
    const R = l.routes || {}; const rs = R.routes || [];
    if (!rs.length) return html`<section class="panel" id="routes"><h2>The design space</h2><p class="empty">${R.present === false ? "The route file " + (R.data || "") + " is not in this build, so no route is shown. The page does not invent one." : "No route is recorded yet."}</p></section>`;
    const declared = (l.scales || []).map((s) => s.key);
    const groups = (l.scales || []).map((s) => ({ ...s, rows: rs.filter((r) => r.scale === s.key) }));
    const unplaced = rs.filter((r) => !declared.includes(r.scale));
    const strengths = [...new Set(rs.map((r) => r.evidence_strength).filter(Boolean))];
    const phens = [...new Set(rs.map(phenotypeKey))];
    return html`<section class="panel" id="routes" aria-labelledby="lm-rt"><h2 id="lm-rt">The design space: ${rs.length} routes across ${groups.filter((g) => g.rows.length).length} scales</h2>
      <p class="note small">Every row is a published perturbation or a bounded proposal, with its own evidence level. <b>None of them has been attempted here.</b> The filters below are a reading aid; they change nothing and submit nothing.</p>
      <form class="lmfilter filters" aria-label="Filter routes">
        <label>Scale <select name="scale"><option value="">all scales</option>${groups.filter((g) => g.rows.length).map((g) => html`<option value="${g.key}">${g.label} (${g.rows.length})</option>`)}</select></label>
        <label>Phenotype <select name="phen"><option value="">any phenotype</option>${phens.map((p) => html`<option value="${p}">${PHEN_LABEL[p] || p}</option>`)}</select></label>
        <label>Evidence <select name="strength"><option value="">any evidence level</option>${strengths.map((s) => html`<option value="${s}">${EV_TEXT[s] || s}</option>`)}</select></label>
        <span class="small faint" id="lmcount" role="status"></span></form>
      ${groups.filter((g) => g.rows.length).map((g) => html`<section class="lmscale" data-scale="${g.key}"><h3>${g.label} <span class="faint small">${g.rows.length} route${g.rows.length === 1 ? "" : "s"}</span></h3>
        <p class="small faint">${g.blurb || ""}</p><div class="lmroutes">${g.rows.map(routeCard)}</div></section>`)}
      ${unplaced.length ? html`<section class="lmscale" data-scale="__unplaced"><h3>Unplaced <span class="faint small">${unplaced.length}</span></h3>
        <p class="note warn small">These routes name a scale this page does not declare (${[...new Set(unplaced.map((r) => r.scale))].join(", ")}). They are shown rather than dropped, so the mismatch between the route file and the page is visible.</p>
        <div class="lmroutes">${unplaced.map(routeCard)}</div></section>` : ""}
      ${R.href ? html`<p class="small"><a href="${R.href}" download>Download the route file</a> <span class="faint">sha256 ${U.sha(R.sha256)}</span></p>` : ""}</section>`;
  }

  /* ----------------------------------------------------------------- one computed study: figures, equations, parameter provenance, controls */
  function paramTable(params) {
    if (!params || !params.length) return "";
    const tone = { sourced: "ok", measured: "ok", assumed: "warn", nondimensional: "grp", derived: "cur" };
    return html`<details><summary><b>${params.length} parameters</b> <span class="faint small">each marked sourced or assumed; an assumed value is not a measurement</span></summary>
      <div class="tablewrap"><table><thead><tr><th scope="col">Parameter</th><th scope="col">Value</th><th scope="col">Units</th><th scope="col">Status</th><th scope="col">Source or justification</th></tr></thead>
      <tbody>${params.map((p) => html`<tr><td><code>${p.name}</code></td><td>${typeof p.value === "number" ? DF.fmt(p.value, 4) : String(p.value)}</td><td class="small">${p.units || ""}</td><td>${U.pill(String(p.status || "not stated").replace(/_/g, " "), tone[p.status] || "st-unk")}</td><td class="small">${p.source || p.justification || ""}</td></tr>`)}</tbody></table></div></details>`;
  }

  /* The threshold of each design knob, with the numerical uncertainty taken from the refinement arm when the sweep itself
   * does not carry one. A threshold with no uncertainty beside it is reported as "not reported", never as exact. */
  function sweepTable(d) {
    const sweeps = d.sweeps || {}; const keys = Object.keys(sweeps); if (!keys.length) return "";
    const ref = ((d.refinement_arm || {}).thresholds) || {};
    const unc = (k, s) => {
      const u = s.threshold_uncertainty !== undefined && s.threshold_uncertainty !== null ? s.threshold_uncertainty : (ref[k] || {}).uncertainty;
      if (u === undefined || u === null) return html`<span class="faint">not reported</span>`;
      return typeof u === "number" ? "± " + DF.fmt(u, 2) : String(u);
    };
    return html`<h4>What each knob does, and where it breaks</h4>
      <p class="small faint">A threshold is the value of that knob below which this model's loop never engages. It is a property of the model; the uncertainty beside it is how far the number moved across integrators and tolerances, which is not the same as being right.</p>
      <div class="tablewrap"><table><thead><tr><th scope="col">Knob</th><th scope="col">What it stands for</th><th scope="col">Threshold</th><th scope="col">Numerical uncertainty</th></tr></thead>
      <tbody>${keys.map((k) => { const s = sweeps[k] || {}; return html`<tr><td><code>${k}</code>${s.label ? html`<br><span class="small faint">${s.label}</span>` : ""}</td><td class="small">${s.meaning || s.description || ""}${s.source ? html`<br><span class="faint">${s.source}</span>` : ""}</td><td>${s.threshold === undefined || s.threshold === null ? html`<span class="faint">none in the range swept</span>` : DF.fmt(s.threshold, 3)}${s.threshold_note ? html`<br><span class="small faint">${s.threshold_note}</span>` : ""}</td><td class="small">${unc(k, s)}</td></tr>`; })}</tbody></table></div>`;
  }

  function listOf(title, items, cls) {
    if (!items || !items.length) return "";
    return html`<h4>${title}</h4><ul class="small ${cls || ""}">${items.map((x) => html`<li>${typeof x === "string" ? x : (x.name ? html`<b>${x.name}.</b> ${x.result || x.text || x.note || ""}` : JSON.stringify(x))}</li>`)}</ul>`;
  }

  function studySection(s) {
    const d = s.data || {};
    const model = d.model || {};
    const eqs = model.equations_latex || d.equations_latex || [];
    const sources = d.sources || [];
    const figs = (s.figures || []).filter((f) => f.state === "present");
    const missing = (s.figures || []).filter((f) => f.state !== "present");
    return html`<section class="panel lmstudy" id="study-${s.id}" aria-labelledby="st-${s.id}">
      <h3 id="st-${s.id}">${s.title} ${U.pill(s.kind || "computed", "warn")} ${s.scale ? U.pill(s.scale, "grp") : ""}</h3>
      ${s.present ? "" : html`<p class="note warn"><b>Declared and not present.</b> The result file <code>${s.data_path || ""}</code> is not in this build, so nothing below is shown for it. It is listed rather than hidden.</p>`}
      ${s.summary ? html`<p>${s.summary}</p>` : ""}
      ${s.question ? html`<p class="small"><b>The design question it answers.</b> ${s.question}</p>` : ""}
      ${figs.length ? html`<div class="lmfigs">${figs.map((f) => html`<figure><img src="${f.href}" alt="${f.alt || f.caption || s.title}" loading="lazy"><figcaption class="small">${f.caption || ""} <span class="faint">${/simulation/i.test(s.kind || "") ? "Simulation output" : "Analysis output"}, not an observation. sha256 ${U.sha(f.sha256)}</span></figcaption></figure>`)}</div>` : ""}
      ${missing.length ? html`<p class="small faint">${missing.length} declared figure${missing.length === 1 ? "" : "s"} not in this build: ${missing.map((f) => f.file).join(", ")}.</p>` : ""}
      ${d.headline ? html`<p class="lmhead"><b>${d.headline}</b></p>` : ""}
      ${eqs.length ? html`<h4>The model, as written</h4><div class="lmeqs">${eqs.map((e) => html`<div class="eqcard">${typeof e === "string" ? DF.texSpan(e, true) : html`${e.name ? html`<h5>${e.name}</h5>` : ""}${DF.texSpan(e.latex || e.tex || "", true)}${e.note ? html`<p class="small faint">${e.note}</p>` : ""}`}</div>`)}</div>` : ""}
      ${(model.edges || []).length ? html`<details><summary><b>${model.edges.length} regulatory edges</b> <span class="faint small">each one's source, or marked assumed</span></summary><ul class="small">${model.edges.map((e) => html`<li><code>${e.from || e.source_node || "?"} → ${e.to || e.target || "?"}</code> ${e.sign ? U.pill(e.sign, e.sign === "activates" || e.sign === "+" ? "ok" : "no") : ""} ${e.note || e.description || ""} ${e.source && e.source !== "assumed" ? html`<span class="faint">[${e.source}]</span>` : U.pill("assumed", "warn")}</li>`)}</ul></details>` : ""}
      ${paramTable(model.parameters || d.parameters)}
      ${sweepTable(d)}
      ${d.critical_domain_size ? html`<p class="lmhead"><b>Critical domain size.</b> ${DF.fmt(d.critical_domain_size.value, 3)} ${d.critical_domain_size.units || ""}${d.critical_domain_size.uncertainty ? " (± " + DF.fmt(d.critical_domain_size.uncertainty, 2) + ")" : ""} — below this the field cannot hold a complete element.</p>` : ""}
      ${d.linear_stability ? html`<p class="small"><b>Internal control.</b> Linear stability predicts a wavelength of ${DF.fmt(d.linear_stability.predicted_wavelength, 3)}; the simulated pattern measures ${d.measured_wavelength === undefined ? "not reported" : DF.fmt(d.measured_wavelength, 3)}. A disagreement is reported, not tuned away.</p>` : ""}
      ${d.control_arm ? html`<details><summary><b>Control arm</b> <span class="faint small">run first; the design sweep is only read if this passes</span></summary><pre class="small lmjson">${JSON.stringify(d.control_arm, null, 1)}</pre></details>` : ""}
      ${d.refinement_arm ? html`<details><summary><b>Refinement arm</b> <span class="faint small">a tighter solver or a finer grid; how far the answer moved</span></summary><pre class="small lmjson">${JSON.stringify(d.refinement_arm, null, 1)}</pre></details>` : ""}
      ${listOf("Controls", d.controls)}
      ${listOf("Numerical checks", d.numerical_checks)}
      ${d.phenotype_classes ? html`<details><summary><b>How each run was classified</b> <span class="faint small">declared before the sweep was read</span></summary><dl class="lmmeta small">${Object.entries(d.phenotype_classes).map(([k, v]) => html`<dt>${k}</dt><dd>${v}</dd>`)}</dl></details>` : ""}
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
      ${(d.limitations || []).length ? html`<div class="lmlimits"><h4>What this study does not establish</h4><ul class="small">${d.limitations.map((x) => html`<li>${x}</li>`)}</ul></div>` : ""}
      ${sources.length ? html`<details><summary><b>${sources.length} sources</b> <span class="faint small">with read levels</span></summary><ul class="small">${sources.map((x) => html`<li>${x.cite || x.title || ""} ${x.read_level ? U.pill(x.read_level + " read", "rl") : ""}${x.pmid ? html`<br><a href="https://pubmed.ncbi.nlm.nih.gov/${String(x.pmid)}/" target="_blank" rel="noopener noreferrer">PMID ${x.pmid}</a>` : ""}${x.doi ? html` <span class="faint">doi ${x.doi}</span>` : ""}</li>`)}</ul></details>` : ""}
      <p class="small faint">${s.code ? html`Code: <code>${s.code}</code>. ` : ""}${s.data_href ? html`<a href="${s.data_href}" download>Download the full result file</a> · ` : ""}sha256 ${U.sha(s.sha256)}</p></section>`;
  }

  /* ----------------------------------------------------------------- the page */
  function page(snap, route) {
    const l = L(snap);
    if (!l) return { html: html`<section class="pagehead"><h1>Limbless mouse</h1><p class="lede">This build carries no limbless-mouse content block. <a href="${DF.href("/studio")}">Back to the Studio</a>.</p></section>` };
    const R = l.routes || {}; const rec = R.recommendation || null; const welfare = R.welfare || null; const genes = R.judge_gene_candidates || [];
    const chain = l.chain || {};
    const allSources = [...new Set([...(R.sources || []).map((s) => s.pmid).filter(Boolean)])];
    return {
      html: html`<section class="pagehead lmhead-sec"><p class="eyebrow"><a href="${DF.href("/studio")}">Studio</a> / ${l.group}</p><h1>${l.title}</h1>
        <p class="lede">${l.goal}</p>
        <p>${U.pill("design space, not a design", "warn")} ${U.pill("no animal work", "ok")} ${U.pill((l.counts || {}).routes + " sourced routes", "cur")} ${U.pill((l.counts || {}).studies_present + " computed studies", "ev")}</p></section>

      <section class="panel lmanswer" aria-labelledby="lm-a"><h2 id="lm-a">${(l.answer || {}).headline || "The answer"}</h2>
        ${((l.answer || {}).paragraphs || []).map((p) => html`<p>${p}</p>`)}
        ${(l.answer || {}).precision_note ? html`<p class="note warn">${l.answer.precision_note}</p>` : ""}
        <p class="small"><a href="#routes">Jump to the ${(l.counts || {}).routes || 0} routes</a> · <a href="#studies">what we ran</a> · <a href="#chain">where the chain breaks</a> · <a href="#welfare">welfare and 3Rs</a></p></section>

      ${rec ? html`<section class="panel lmrec" aria-labelledby="lm-rec"><h2 id="lm-rec">If you asked us to actually do it</h2>
        ${rec.headline ? html`<p class="lmhead"><b>${rec.headline}</b></p>` : ""}
        ${rec.route ? html`<p><b>Route.</b> ${rec.route}</p>` : ""}
        ${rec.why ? html`<p>${rec.why}</p>` : ""}
        ${(rec.steps || []).length ? html`<h3>What that looks like</h3><ol>${rec.steps.map((x) => html`<li>${x}</li>`)}</ol>` : ""}
        ${rec.alternative ? html`<p class="note small"><b>If the goal is a viable adult rather than an embryonic phenotype.</b> ${rec.alternative}</p>` : ""}
        ${(rec.risks || []).length ? html`<p class="small"><b>What would sink it.</b> ${rec.risks.join(" ")}</p>` : ""}</section>` : ""}

      <section class="panel lmbudsec" aria-labelledby="lm-bd"><h2 id="lm-bd">Where the routes act</h2>
        <p class="small">All of this happens in one structure over about two days of mouse development. The routes below are not interchangeable genes; they are interventions at different places in that structure, and that is why they give different animals.</p>
        ${budDiagram(l)}</section>

      ${routesSection(l)}

      <section class="panel" id="studies" aria-labelledby="lm-st"><h2 id="lm-st">What we ran</h2>
        <p class="note small">Three studies, each one a <b>simulation or a sequence analysis</b>. None is an observation, none is calibrated to a measured mouse limb bud, and no part of any of them was run in an animal. Each carries its own controls, its refinement arm, and a statement of what it does not establish.</p>
        ${(l.studies || []).map(studySection)}</section>

      <section class="panel lmchain" id="chain" aria-labelledby="lm-ch"><h2 id="lm-ch">${chain.title || "The chain across scales"}</h2>
        ${chain.intro ? html`<p>${chain.intro}</p>` : ""}
        <ol class="lmlinks">${(chain.links || []).map((k) => html`<li class="lmlink ${k.status}"><p><b>${k.from}</b> <span class="lmarrow" aria-hidden="true">→</span> <b>${k.to}</b> ${U.pill(k.status === "model" ? "inside one model" : k.status, CHAIN_TONE[k.status] || "st-unk")}</p><p class="small">${k.note}</p></li>`)}</ol>
        ${chain.verdict ? html`<p class="note warn">${chain.verdict}</p>` : ""}
        <p class="small faint">This is the same discipline the rest of this site applies to every cross-scale coupling: a junction is composable, scenario-level, or refused. <a href="${DF.href("/studio/flying-fish", { scale: "organ" })}">The flying-fish project uses the same contract.</a></p></section>

      ${genes.length ? html`<section class="panel" id="genes" aria-labelledby="lm-g"><h2 id="lm-g">“He said he identified a gene for it” — what that could mean</h2>
        <p class="small">Several genes would fit that description and they do not produce the same animal. This is written so we can answer sensibly whichever one he means, not to guess which it is.</p>
        <div class="tablewrap"><table><caption class="sr">Candidate genes and what each would actually produce</caption><thead><tr><th scope="col">Gene</th><th scope="col">Species the evidence is in</th><th scope="col">What losing it does</th><th scope="col">Phenotype class</th><th scope="col">Evidence</th></tr></thead>
        <tbody>${genes.map((g) => html`<tr><td><b>${g.gene || g.name}</b></td><td class="small">${g.species || ""}</td><td class="small">${g.effect || g.what_it_does || ""}</td><td class="small">${g.phenotype || ""}</td><td class="small">${g.pmid ? html`<a href="https://pubmed.ncbi.nlm.nih.gov/${String(g.pmid)}/" target="_blank" rel="noopener noreferrer">PMID ${g.pmid}</a>` : ""} ${g.read_level ? U.pill(g.read_level + " read", "rl") : ""}</td></tr>`)}</tbody></table></div></section>` : ""}

      ${welfare ? html`<section class="panel lmwelfare" id="welfare" aria-labelledby="lm-w"><h2 id="lm-w">${welfare.title || "Animal welfare and the 3Rs"}</h2>
        ${(welfare.paragraphs || [welfare.text]).filter(Boolean).map((p) => html`<p>${p}</p>`)}
        ${(welfare.refinements || []).length ? html`<h3>Refinements that change the answer</h3><ul>${welfare.refinements.map((x) => html`<li>${typeof x === "string" ? x : html`<b>${x.name}.</b> ${x.note}`}</li>`)}</ul>` : ""}
        ${(welfare.review_turns_on || []).length ? html`<h3>What a licence or IACUC review would turn on</h3><ul class="small">${welfare.review_turns_on.map((x) => html`<li>${x}</li>`)}</ul>` : ""}
        ${(welfare.non_animal_first || []).length ? html`<h3>What to do before any animal</h3><ul class="small">${welfare.non_animal_first.map((x) => html`<li>${x}</li>`)}</ul>` : ""}</section>` : ""}

      <section class="panel lmnot" aria-labelledby="lm-n"><h2 id="lm-n">What this page does not claim</h2>
        <ul>${(l.not_claimed || []).map((x) => html`<li>${x}</li>`)}</ul>
        ${(R.limitations || []).length ? html`<h3>Limits the route map states for itself</h3><ul class="small">${R.limitations.map((x) => html`<li>${x}</li>`)}</ul>` : ""}
        <p class="small faint">Page text <code>site/content/limbless-mouse.json</code> sha256 ${U.sha(l.content_sha256)}; studies indexed by <code>results/limbless-mouse/index.json</code> sha256 ${U.sha(l.index_sha256)}. ${allSources.length ? allSources.length + " distinct PubMed identifiers are cited across the routes." : ""}</p></section>

      ${l.closing ? html`<section class="panel"><h2>${l.closing.title}</h2><p>${l.closing.text}</p>
        <p class="small"><a href="${DF.href("/studio")}">All projects</a> · <a href="${DF.href("/frontier")}">Open questions</a> · <a href="https://github.com/kganjam/delphi-frontier/blob/main/docs/dossier/12-limbless-mouse.md" target="_blank" rel="noopener noreferrer">The longer written answer in the repository</a></p></section>` : ""}`,

      after(root) {
        DF.renderMath(root);
        const form = root.querySelector(".lmfilter"); if (!form) return;
        const count = root.querySelector("#lmcount");
        const apply = () => {
          const want = { scale: form.scale.value, phen: form.phen.value, strength: form.strength.value };
          let shown = 0, total = 0;
          root.querySelectorAll(".lmroute").forEach((el) => {
            total++;
            const ok = (!want.scale || el.dataset.scale === want.scale) && (!want.phen || el.dataset.phen === want.phen) && (!want.strength || el.dataset.strength === want.strength);
            el.hidden = !ok; if (ok) shown++;
          });
          root.querySelectorAll(".lmscale").forEach((sec) => { sec.hidden = ![...sec.querySelectorAll(".lmroute")].some((el) => !el.hidden); });
          count.textContent = shown === total ? `showing all ${total} routes` : `showing ${shown} of ${total} routes`;
          root.querySelectorAll(".lmpin").forEach((g) => g.classList.toggle("on", !!want.scale && g.dataset.scale === want.scale));
        };
        const pick = (sc) => { form.scale.value = sc === form.scale.value ? "" : sc; apply(); const t = root.querySelector("#routes"); if (t) t.scrollIntoView({ behavior: "smooth", block: "start" }); };
        root.querySelectorAll(".lmpin").forEach((g) => {
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
