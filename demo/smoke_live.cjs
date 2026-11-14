// Live check against a running demo/server.py: drives the server-only features in jsdom.
//   NODE_PATH=<jsdom>/node_modules node demo/smoke_live.cjs http://localhost:8000
const fs = require('fs'), path = require('path');
const { JSDOM } = require('jsdom');
const BASE = (process.argv[2] || 'http://localhost:8000').replace(/\/?$/, '/');
const DIST = path.join(__dirname, 'dist');
const page = fs.readFileSync(path.join(DIST, 'page.html'), 'utf8');
const inline = page.match(/<script>\n([\s\S]*)<\/script>\s*$/)[1];
const html = page.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<link[^>]*>/g, '');
const dom = new JSDOM(`<!doctype html><html><body>${html}</body></html>`, { runScripts: 'outside-only', pretendToBeVisual: true, url: BASE });
const w = dom.window, problems = [];
let plots = 0;
w.scrollTo = () => {};
w.matchMedia = () => ({ addEventListener() {} });
w.katex = { renderToString: s => `<math>${String(s).length}</math>` };
w.Plotly = { newPlot(el, traces) { plots += traces.length ? 1 : 0; el.on = () => {}; return Promise.resolve(el); } };
w.fetch = (u, o) => fetch(new URL(u, BASE), o);
w.AbortController = AbortController;
w.console.error = (...a) => problems.push(a.map(x => (x && x.stack) || x).join(' '));
for (const f of fs.readdirSync(path.join(DIST, 'data'))) w.eval(fs.readFileSync(path.join(DIST, 'data', f), 'utf8'));
w.eval(inline + '\nwindow.App = App;');
const $ = s => w.document.querySelector(s);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const text = () => w.document.getElementById('main').textContent;
const drawer = () => w.document.getElementById('drawer-body').textContent;
async function until(what, test, ms = 60000) {
  for (const t0 = Date.now(); Date.now() - t0 < ms;) { if (test()) return true; await sleep(150); }
  problems.push(`timeout: ${what}`); return false;
}
async function show(id, patch) { Object.assign(w.App.state[id], patch || {}); w.location.hash = id; await w.App.render(); await sleep(60); }
const check = (name, ok, detail) => { console.log((ok ? 'ok   ' : 'FAIL ') + name + (detail ? '  ' + detail : '')); if (!ok) problems.push(name); };
(async () => {
  const A = w.App;
  await until('backend detected', () => A.backend, 8000);
  check('backend detected', A.backend);

  await show('scenario', { scenario: 'custom' });
  check('custom scenario has a Rank button', !!$('#sc-rank'));
  if ($('#sc-rank')) { $('#sc-rank').click(); await until('custom ranking', () => /live from the server/i.test(text()) && !A.state.scenario.loading); }
  check('custom ranking drawn', /live from the server/i.test(text()) && !/failed to draw/.test(text()), text().match(/How far the data[^.]*\.[^.]*\./)?.[0]?.slice(0, 140));

  for (const raw of [false, true]) {
    await show('search', { q: 'radiative extinction', raw, results: null });
    $('#se-go').click();
    await until('search results', () => !A.state.search.loading && A.state.search.results);
    const n = w.document.querySelectorAll('#main .chip.cite').length, docs = [...w.document.querySelectorAll('#main button')].filter(b => /Open the document/.test(b.textContent));
    check(`search raw=${raw}`, n > 0 && (!raw || docs.length > 0), `${n} citation chips, ${docs.length} document buttons`);
    if (raw && docs[0]) { docs[0].click(); await sleep(300); check('search result opens the viewer', !w.document.getElementById('drawer').hidden && /NASA PSI/.test(drawer())); }
  }

  await show('traces', { accession: 'PSI-159', test_id: '21088 M4' });
  await until('live trace', () => !A.state.traces.liveLoading && (A.state.traces.live || A.state.traces.liveError), 150000);
  check('live trace PSI-159 21088 M4', !!A.state.traces.live && !A.state.traces.liveError, A.state.traces.liveError || `${A.state.traces.live?.data?.series?.length} samples`);

  await show('ask', { n: 1 });
  const live = [...w.document.querySelectorAll('#main button')].find(b => /Run it live/.test(b.textContent));
  check('ask has Run it live', !!live);
  if (live) { live.click(); await sleep(4000); check('ask live answer shown', /"ranking"|notes|score/i.test(text())); }

  const files = [
    ['table', 'PSI-159', 'PSI-159_Raw Data_21130M3_mfcSetpoints.csv', /rows|columns|quick look/i],
    ['table (big)', 'PSI-159', 'PSI-159_Raw Data_21088M4_data.csv', /rows|columns|quick look/i],
    ['text', 'PSI-39', 'PSI-39_Raw Data_F068A03_Chamber_Readings.txt', /./],
    ['video', 'PSI-23', 'PSI-23_Raw Data_vlc-record-2020-01-06-22h54m02s-udp_20006A4.mp4', /NASA PSI/],
    ['pdf', 'PSI-25', 'PSI-25_Reports_BASS-II Summary Report.pdf', /NASA PSI/],
    ['excluded', 'PSI-142', '1-Cover Page.docx', /NASA PSI/],
  ];
  for (const [kind, accession, file, expect] of files) {
    A.openFile({ accession, file, page: 21 });
    await sleep(kind.startsWith('t') ? 6000 : 500);
    const d = drawer(), body = w.document.getElementById('drawer-body');
    const link = [...body.querySelectorAll('a')].some(a => a.href.startsWith('https://psi.nasa.gov/'));
    check(`viewer ${kind}`, link && expect.test(d) && !/undefined|\[object/.test(d), `${body.querySelectorAll('tr').length} table rows, video=${!!body.querySelector('video')}; ${d.replace(/\s+/g, ' ').slice(0, 150)}`);
  }
  console.log(`${plots} charts drawn`);
  if (problems.length) { console.log('\n' + [...new Set(problems)].slice(0, 20).join('\n')); process.exit(1); }
  console.log('live smoke ok');
  process.exit(0);
})();
