// Headless render check: draws every view in jsdom with Plotly and KaTeX stubbed, and fails on any view error.
//   NODE_PATH=<dir with jsdom>/node_modules node demo/smoke.cjs
const fs = require('fs'), path = require('path');
const { JSDOM } = require('jsdom');
const DIST = path.join(__dirname, 'dist');
const page = fs.readFileSync(path.join(DIST, 'page.html'), 'utf8');
const inline = page.match(/<script>\n([\s\S]*)<\/script>\s*$/)[1];
const html = page.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<link[^>]*>/g, '');
const dom = new JSDOM(`<!doctype html><html><body>${html}</body></html>`, { runScripts: 'outside-only', pretendToBeVisual: true, url: 'http://localhost/' });
const w = dom.window;
const problems = [], plots = [];
w.scrollTo = () => {};
w.matchMedia = () => ({ addEventListener() {} });
w.katex = { renderToString: s => `<math>${String(s).length}</math>` };
w.Plotly = { newPlot(el, traces, layout) {
  traces.forEach((t, i) => {
    const lens = ['x', 'y', 'text', 'customdata'].filter(k => Array.isArray(t[k])).map(k => t[k].length);
    if (new Set(lens).size > 1) problems.push(`${w.location.hash}: trace ${i} has arrays of unequal length ${lens}`);
    if (!lens.length && !['heatmap', 'table'].includes(t.type)) problems.push(`${w.location.hash}: trace ${i} has no data arrays`);
    for (const k of ['x', 'y']) if (Array.isArray(t[k]) && t[k].some(v => typeof v === 'number' && !isFinite(v))) problems.push(`${w.location.hash}: trace ${i} has NaN in ${k}`);
  });
  if (layout.yaxis2 && layout.yaxis2.overlaying) problems.push(`${w.location.hash}: dual y axis`);
  plots.push(w.location.hash);
  el.on = () => {};
  return Promise.resolve(el);
} };
w.console.error = (...a) => problems.push(`${w.location.hash}: ${a.map(x => (x && x.stack) || x).join(' ')}`);
for (const f of fs.readdirSync(path.join(DIST, 'data'))) w.eval(fs.readFileSync(path.join(DIST, 'data', f), 'utf8'));
w.eval(inline + '\nwindow.App = App; window.h = h;');
const tick = () => new Promise(r => setTimeout(r, 40));
const main = () => w.document.getElementById('main');
async function show(id, patch) {
  Object.assign(w.App.state[id], patch || {});
  w.location.hash = id;
  await w.App.render(); await tick();
  const copy = main().cloneNode(true);
  copy.querySelectorAll('.quote').forEach(q => q.remove());  // verbatim source quotes may contain any word
  const text = copy.textContent;
  if (/failed to draw|Could not load/.test(text)) problems.push(`${id} ${JSON.stringify(patch || {})}: ${text.slice(0, 300)}`);
  if (/undefined|NaN|\[object Object\]/.test(text)) problems.push(`${id} ${JSON.stringify(patch || {})}: text contains "${text.match(/.{0,50}(undefined|NaN|\[object Object\]).{0,30}/)[0]}"`);
  return text.length;
}
(async () => {
  const A = w.App, F = w.FIF;
  for (const v of A.views) console.log(v.id.padEnd(14), await show(v.id), 'chars');
  for (const k of Object.keys(F.relevance)) { const [scenario, phase, pillar] = k.split('|'); await show('scenario', { scenario, phase, pillar, all: true }); }
  for (const phase of ['all', 'solid', 'liquid', 'gas']) for (let cell = 0; cell < F.coverage[phase].data.cells.length; cell += 5) await show('coverage', { phase, cell });
  const has = id => A.views.some(v => v.id === id);
  if (has('investigation')) for (const i of F.investigations) await show('investigation', { accession: i.accession });
  if (has('investigation')) await show('investigation', { accession: 'PSI-25', compare: ['PSI-26', 'PSI-98'] });
  if (has('tests')) for (const i of F.investigations) await show('tests', { accession: i.accession, q: '' });
  if (has('tests')) await show('tests', { accession: 'PSI-10', q: '22024M1' });
  if (has('tests')) { await show('tests', { accession: 'PSI-159', q: '21088M4' }); if (!/Exact test id match/.test(main().textContent)) problems.push('tests: id without a space is not matched'); }
  if (has('insights')) for (const tab of ['limits', 'micro', 'gaps', 'questions', 'lineage', 'ranges']) await show('insights', { tab });
  if (has('models')) for (const m of F.models.models) await show('models', { model: m.id });
  if (has('quality')) await show('quality', { accession: 'PSI-10', q: '22024M1' });
  if (has('ask')) for (let n = 1; n <= F.questions.length; n++) await show('ask', { n });
  // every citation in the synthesis must resolve to an item of a record
  let cites = 0;
  JSON.stringify(F.synthesis, (k, v) => { if (v && v.accession && v.section && !Array.isArray(v)) { cites++;
    const sec = (F.records[v.accession] || {})[v.section]; const item = Array.isArray(sec) && v.index != null ? sec[v.index - 1] : sec;
    if (item == null) problems.push(`citation does not resolve: ${JSON.stringify(v)}`); } return v; });
  console.log(`${plots.length} charts drawn, ${cites} citations checked, ${A.views.length} views`);
  if (problems.length) { console.log([...new Set(problems)].slice(0, 40).join('\n')); process.exit(1); }
  console.log('smoke ok');
})();
