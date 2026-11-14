// Live check of the Team board view against a running demo/server.py with an EMPTY board: posts as a person,
// replies as an AI through MCP, marks the thread done. It writes to the board, so point FIF_BOARD_DB at a scratch file:
//   FIF_BOARD_DB=/tmp/b.db PORT=8765 uv run python demo/server.py &
//   NODE_PATH=<jsdom>/node_modules node demo/smoke_board.cjs http://localhost:8765
const fs = require('fs'), path = require('path');
const { JSDOM } = require('jsdom');
const BASE = (process.argv[2] || 'http://localhost:8000').replace(/\/?$/, '/');
const DIST = path.join(__dirname, 'dist');
const page = fs.readFileSync(path.join(DIST, 'page.html'), 'utf8');
const inline = page.match(/<script>\n([\s\S]*)<\/script>\s*$/)[1];
const html = page.replace(/<script[\s\S]*?<\/script>/g, '').replace(/<link[^>]*>/g, '');
const dom = new JSDOM(`<!doctype html><html><body>${html}</body></html>`, { runScripts: 'outside-only', pretendToBeVisual: true, url: BASE });
const w = dom.window, problems = [];
w.scrollTo = () => {}; w.matchMedia = () => ({ addEventListener() {} });
w.katex = { renderToString: s => '' }; w.Plotly = { newPlot: el => { el.on = () => {}; return Promise.resolve(el); } };
w.fetch = (u, o) => fetch(new URL(u, BASE), o); w.AbortController = AbortController;
w.console.error = (...a) => problems.push(a.map(x => (x && x.stack) || x).join(' '));
for (const f of fs.readdirSync(path.join(DIST, 'data'))) w.eval(fs.readFileSync(path.join(DIST, 'data', f), 'utf8'));
w.eval(inline + '\nwindow.App = App;');
const sleep = ms => new Promise(r => setTimeout(r, ms));
const main = () => w.document.getElementById('main');
const until = async (what, test) => { for (let i = 0; i < 60; i++) { if (test()) return; await sleep(100); } problems.push('timeout: ' + what); };
const btn = label => [...main().querySelectorAll('button')].find(b => b.textContent.trim() === label);
const type = (el, v) => { el.value = v; el.dispatchEvent(new w.Event('input', { bubbles: true })); };
(async () => {
  const A = w.App;
  await until('backend', () => A.backend);
  w.location.hash = 'board'; await A.render();
  await until('empty board', () => /No open threads/.test(main().textContent));
  btn('New post').click(); await sleep(50);
  const inputs = () => [...main().querySelectorAll('input[type=text]')];
  type(inputs()[1], "Claude (Marta)"); type(inputs()[2], 'Coverage map: log scale'); type(main().querySelector('textarea'), 'Line one\n<b>not html</b>');
  btn('Post').click(); await sleep(100);
  if (!/Write your name first/.test(main().textContent)) problems.push('no name warning');
  type(inputs()[0], 'Andres'); btn('Post').click();
  await until('thread shown after post', () => /Andres · just now/.test(main().textContent) && /<b>not html<\/b>/.test(main().textContent));
  if (main().querySelector('.board-msg b')) problems.push('body rendered as HTML');
  // an AI answers through MCP
  const r = await fetch(BASE + 'mcp', { method: 'POST', body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'tools/call', params: { name: 'board_reply', arguments: { thread: 1, author: "Claude (Marta)", body: 'Agreed.' } } }) });
  if ((await r.json()).result.isError) problems.push('mcp reply failed');
  type(main().querySelector('textarea'), 'Done then.'); btn('Mark done').click();
  await until('done + ai reply visible', () => /Claude \(Marta\) · AI/.test(main().textContent) && /Reopen/.test(main().textContent) && /Done then\./.test(main().textContent));
  btn('← All threads').click();
  await until('open list empty again', () => /No open threads/.test(main().textContent));
  [...main().querySelectorAll('#board-status button')].find(b => b.textContent === 'Done').click();
  await until('done list', () => /Coverage map: log scale/.test(main().textContent) && /2 replies/.test(main().textContent));
  if (/undefined|NaN|\[object Object\]/.test(main().textContent)) problems.push('bad text in view');
  console.log(problems.length ? 'PROBLEMS\n' + problems.join('\n') : 'board live ok');
  process.exit(problems.length ? 1 : 0);
})();
