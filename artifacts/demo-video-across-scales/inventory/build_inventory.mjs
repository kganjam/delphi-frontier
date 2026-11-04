import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { Workbook } from '@oai/artifact-tool';

// Rebuild the portable review artifacts from the archived, curated inventory.
// This does not run scientific models or regenerate scientific results.
const here = path.dirname(fileURLToPath(import.meta.url));
const data = JSON.parse(await fs.readFile(path.join(here, 'simulation-inventory.json'), 'utf8'));
const records = data.records;
if (records.length !== 49 || new Set(records.map(r => r.id)).size !== 49) {
  throw new Error('The frozen source review must retain all 49 distinct records.');
}
const columns = [
  ['number', 'number'], ['category', 'category'], ['id', 'id'], ['title', 'title'],
  ['primary_scale', 'primary_scale'], ['all_scales', r => r.scales.join('; ')],
  ['media_kind', 'media_kind'], ['recorded_test', 'recorded_test'],
  ['scope_limit', 'scope_limit'], ['PROPOSED_function_first_question', 'proposed_question'],
  ['PROPOSED_next_experiment', 'next_experiment'], ['source_video_state', 'source_video_state'],
  ['integrity_check', 'integrity'], ['duration_seconds', r => r.duration_s === '' ? '' : Number(r.duration_s)],
  ['video_url', 'video_url'], ['figure_url', 'figure_url'], ['source_manifest_url', 'source_manifest'],
  ['downloaded_sha256', 'sha256'], ['recorded_HTTP_status', 'http_status'], ['parent_record', 'parent_record'],
];
const matrix = [columns.map(([name]) => name), ...records.map(r => columns.map(([, key]) => typeof key === 'function' ? key(r) : r[key] ?? ''))];
const workbook = Workbook.create();
const sheet = workbook.worksheets.add('Inventory');
const range = sheet.getRangeByIndexes(0, 0, matrix.length, matrix[0].length);
range.values = matrix;
workbook.recalculate();
const values = range.values;
if (JSON.stringify(values) !== JSON.stringify(matrix)) throw new Error('Spreadsheet cells changed during authoring.');
const inspection = await workbook.inspect({ kind: 'region', sheetId: 'Inventory', range: 'A1:F5', maxChars: 1600, tableMaxRows: 5, tableMaxCols: 6 });
const quote = value => '"' + String(value ?? '').replaceAll('"', '""') + '"';
await fs.writeFile(path.join(here, 'simulation-inventory.csv'), '\ufeff' + values.map(row => row.map(quote).join(',')).join('\n') + '\n');

const lines = [
  'DELPHI BIO / MORPHOSWARM STUDIO — PUBLIC SOURCE INVENTORY',
  'Frozen source review: ' + data.generated_at_seattle, 'Snapshot: ' + data.snapshot_label,
  'Source: ' + data.source_url, '', data.scope, '', data.archive_note, '',
  'RECORDED describes saved output. PROPOSED questions and next experiments are editorial possibilities, not achieved fish functions or measured outcomes.',
  '', 'PROPOSED DESIGN QUESTIONS ACROSS SCALES',
  ...Object.entries(data.proposed_scale_questions).map(([scale, question]) => `${scale}: ${question}`),
  '', 'SOURCE RECORDS',
];
for (const r of records) {
  lines.push('', `${r.number}. ${r.title} [${r.id}]`, `CATEGORY: ${r.category}; SCALES: ${r.scales.join(', ')}`,
    'RECORDED: ' + r.recorded_test, 'SCOPE: ' + r.scope_limit,
    'PROPOSED QUESTION: ' + r.proposed_question, 'PROPOSED NEXT EXPERIMENT: ' + r.next_experiment,
    'MEDIA: ' + (r.video_url || r.figure_url || 'No video or figure is linked for this record.'),
    'SOURCE MANIFEST: ' + r.source_manifest, 'RECORDED FILE CHECK: ' + r.integrity,
    'SHA-256: ' + (r.sha256 || 'Not recorded for this artifact.'));
}
lines.push('', 'METHOD', data.method, '', 'PUBLIC LINK CHECKS',
  'See public-link-checks.json for the dated archive-time HTTP checks. These establish link availability only, not biological validity or future availability.',
  'The machine-specific working paths and duplicate raw source payloads were omitted. The recorded scientific descriptions and proposed questions were preserved.');
await fs.writeFile(path.join(here, 'simulation-inventory.txt'), lines.join('\n') + '\n');

const esc = value => String(value ?? '').replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
const sourceLink = (url, label) => url ? `<a href="${esc(url)}">${esc(label)}</a>` : '';
function card(r) {
  const media = r.video_url
    ? `<video controls preload="none" aria-label="${esc(r.title)}"><source src="${esc(r.video_url)}" type="video/mp4">${sourceLink(r.video_url, 'Open source video')}</video>`
    : r.figure_url ? `<a href="${esc(r.figure_url)}"><img loading="lazy" src="${esc(r.figure_url)}" alt="Published source figure for ${esc(r.title)}"></a>`
      : '<div class="missing">No video or figure is linked for this record.</div>';
  return `<article id="record-${esc(r.id)}" data-scales="${esc(r.scales.join('|'))}" data-category="${esc(r.category)}">
  <div class="record">${r.number} · ${esc(r.category)} · ${esc(r.scales.join(', '))}</div><h3>${esc(r.title)}</h3>
  <p class="id">${esc(r.id)}</p>${media}
  <p><strong>Recorded test.</strong> ${esc(r.recorded_test)}</p><p class="scope"><strong>Scope.</strong> ${esc(r.scope_limit)}</p>
  <div class="proposed"><h4>Proposed flying-fish design question</h4><p>${esc(r.proposed_question)}</p><p><strong>Next experiment.</strong> ${esc(r.next_experiment)}</p></div>
  <p class="links">${[sourceLink(r.video_url, 'Public video'), sourceLink(r.figure_url, 'Public figure'), sourceLink(r.source_manifest, 'Source manifest')].filter(Boolean).join(' · ')}</p>
  <details><summary>Recorded file check</summary><p>${esc(r.integrity)}</p><p class="digest">${esc(r.sha256 || 'No SHA-256 recorded for this artifact.')}</p></details></article>`;
}
const scaleOrder = [...Object.keys(data.proposed_scale_questions), 'across scales'];
const sections = scaleOrder.map(scale => {
  const rows = records.filter(r => r.primary_scale === scale);
  return rows.length ? `<section class="scale-section"><h2>${esc(scale)} <small>${rows.length} records</small></h2><div class="grid">${rows.map(card).join('\n')}</div></section>` : '';
}).join('\n');
const categories = [...new Set(records.map(r => r.category))];
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Delphi Bio — simulation and media inventory</title>
<style>
:root{font:17px/1.55 system-ui,sans-serif;color:#142438;background:#f2f5f8}*{box-sizing:border-box}body{margin:0}header,main{max-width:1440px;margin:auto;padding:36px 28px}header{padding-bottom:8px}h1,h2,h3{font-family:Georgia,serif;line-height:1.15}h1{font-size:clamp(34px,5vw,58px);margin:12px 0}h2{font-size:30px;text-transform:capitalize;margin:40px 0 20px}h2 small{font:14px system-ui;color:#526174;text-transform:none;margin-left:8px}h3{font-size:25px;margin:8px 0}h4{font-size:16px;margin:0;color:#2457d6}a{color:#2457d6;overflow-wrap:anywhere}.eyebrow{color:#2457d6;font-size:13px;font-weight:700;letter-spacing:.08em}.intro{max-width:1050px}.note,.scale-map{padding:20px;background:#fff;border:1px solid #c6d0dc;border-radius:8px}.note{border-left:4px solid #2457d6}.toplinks,.filters{display:flex;gap:18px;flex-wrap:wrap;margin:20px 0}.filters label{display:grid;gap:4px;font-size:14px}select{font:inherit;padding:8px;max-width:100%}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px}article{padding:22px;background:#fff;border:1px solid #c6d0dc;border-radius:8px;min-width:0}.record,.id{font-size:12px;color:#526174}.id{overflow-wrap:anywhere;margin:8px 0 16px}video,img{display:block;width:100%;height:290px;object-fit:contain;background:#e9edf2}video{background:#122034}.missing{min-height:180px;display:grid;place-items:center;text-align:center;background:#e9edf2;padding:24px}.scope{font-size:15px;color:#43556a}.proposed{padding:16px;background:#eef3ff;border-left:3px solid #2457d6}.proposed p:last-child{margin-bottom:0}.links,details{font-size:14px}.digest{overflow-wrap:anywhere;font-size:12px}.scale-map{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px 24px}.scale-map p{margin:0}.scale-map strong{text-transform:capitalize}footer{margin:36px 0;color:#526174;font-size:14px}.hidden{display:none!important}@media(max-width:760px){header,main{padding:24px 16px}.grid,.scale-map{grid-template-columns:1fr}article{padding:18px}video,img{height:240px}.filters{display:block}.filters label{margin:12px 0}}
</style></head><body><header><div class="eyebrow">DELPHI BIO / MORPHOSWARM STUDIO · SOURCE REVIEW</div><h1>Every simulation has a question.</h1>
<p class="intro">${esc(data.scope)}</p><div class="note"><strong>Recorded output and proposed use are different.</strong> Recorded tests describe saved source output. The blue panels suggest design questions and future experiments; they do not claim those functions were achieved. Generic models, failed checks and unresolved transfers remain visible.</div>
<nav class="toplinks"><a href="simulation-inventory.csv">49-entry CSV</a><a href="simulation-inventory.txt">Readable text</a><a href="simulation-inventory.json">Structured inventory</a><a href="${esc(data.source_url)}">Live Studio</a></nav>
<p>Source review: ${esc(data.generated_at_seattle)}. Media streams from public source URLs; no local machine paths or extra video copies are required.</p>
<h2>Proposed questions across all 11 scales</h2><div class="scale-map">${Object.entries(data.proposed_scale_questions).map(([s,q])=>`<p><strong>${esc(s)}.</strong> ${esc(q)}</p>`).join('')}</div>
<div class="filters"><label>Scale<select id="scale"><option value="all">All scales</option>${scaleOrder.map(s=>`<option>${esc(s)}</option>`).join('')}</select></label><label>Artifact category<select id="category"><option value="all">All categories</option>${categories.map(s=>`<option>${esc(s)}</option>`).join('')}</select></label><p id="count" aria-live="polite">49 records shown</p></div></header>
<main>${sections}<footer><p>${esc(data.method)}</p><p>Grouped by the first source scale; the filter includes every scale tag. Registry gaps remain explicit. File identity and link availability do not establish biological validity.</p><p><a href="public-link-checks.json">Dated public-link checks</a> · Frozen source label: ${esc(data.snapshot_label)}. Public sources can change after capture.</p></footer></main>
<script>const cards=[...document.querySelectorAll('article[data-scales]')];function filter(){const scale=document.querySelector('#scale').value;const category=document.querySelector('#category').value;let n=0;cards.forEach(card=>{const show=(scale==='all'||card.dataset.scales.split('|').includes(scale))&&(category==='all'||card.dataset.category===category);card.classList.toggle('hidden',!show);if(show)n++;});document.querySelectorAll('.scale-section').forEach(section=>section.classList.toggle('hidden',![...section.querySelectorAll('article')].some(card=>!card.classList.contains('hidden'))));document.querySelector('#count').textContent=n+' records shown';}document.querySelectorAll('select').forEach(select=>select.addEventListener('change',filter));</script></body></html>`;
if ((html.match(/<article /g) || []).length !== 49) throw new Error('HTML omitted records.');
await fs.writeFile(path.join(here, 'simulation-inventory.html'), html);
await fs.writeFile(path.join(here, 'inventory-build-check.json'), JSON.stringify({records:records.length,columns:columns.length,exact_spreadsheet_round_trip:true,html_cards:49,inspection},null,2)+'\n');
console.log(JSON.stringify({records:49,columns:columns.length,htmlCards:49,exactRoundTrip:true}));
