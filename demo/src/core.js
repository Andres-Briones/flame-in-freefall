/* Shared core for every view. Views register with App.view({...}) and use only the helpers documented here.

   App.view({
     id: 'scenario',                // hash name, ASCII letters/digits/hyphens
     title: 'Scenario lens',        // nav label
     tier: 1,                       // 1 story, 2 depth, 3 AI and hand-over (nav separators)
     intro: 'one or two sentences under the title',
     needs: ['relevance'],          // lazy data files to load before render (base data are always there)
     brief: { need, data: [], call, keep: [], backend },   // what the dashboard team must build (see brief view)
     render(root, state, update) {} // fill `root`; `state` persists per view; update(patch) merges and re-renders
   })

   Data: window.FIF.<name>. Always loaded: investigations, synthesis, coverage, questions, discrepancies.
   Lazy (list in `needs`): relevance, tests, records, models, tsfeatures, tsexamples.

   Backend (optional). The page works as static files. When it is served by demo/server.py, App.backend is true
   (set before the first render) and these work; without it App.api rejects and views must degrade to links.
     App.backend                       true when api/health answered
     App.api(fn, args)                 Promise of a fif.api result {data, chart, sources, notes}; fn is one of the 11 functions
     App.resolve(accession, file)      Promise of a short-lived direct address (NASA storage, readable by scripts)
   Files (PSI originals are never stored by us; every file is linked or streamed from its official address)
     App.fileUrl(accession, file)      the official PSI download address; fine for <a href>, <video src>, <img src>
     App.fileKind(file)                'pdf' | 'video' | 'image' | 'table' | 'text' | 'other' (by extension)
     App.openFile({accession, file, page, title})   open the file viewer (src/viewer.js); page is a 1-based PDF page
     App.parseSource(s)                {accession, file, page} for a psi_file source of a record, or null

   Helpers
     h(tag, attrs, ...children)        element builder; attrs: class, text, html, on<event>, dataset, others as attributes
     App.go(viewId, statePatch)        navigate to a view, optionally presetting its state
     App.inv(accession)                investigation card {accession, acronym, title, one_line, pillars, fuel_phases, flight, ...}
     App.name(accession)               "BASS-II (PSI-25)"
     App.fmt(value, digits)            number formatting, '–' for null
     App.pct(x)                        0.209 -> "20.9%"
     App.select({id, label, options, value, onChange})   options: [[value, label], ...] or [value, ...]
     App.seg({id, label, options, value, onChange})      segmented buttons, same options shape
     App.range({id, label, min, max, step, value, onChange, format})
     App.search({id, label, value, onChange, placeholder})
     App.table({cols, rows, pageSize, onRow, sort})      cols: [{key, label, num, fmt(value,row)->string|Node, width}]
     App.plot(el, traces, layout, onClick)               Plotly with theme colours; returns the element
     App.colors()                      {fg, fg2, fg3, line, bg, surface, accent, s:[8 series], warn, crit, good, seqLo, seqHi, neutral}
     App.cite(c)                       chip for {accession, section, index} (1-based); opens the quoted source in the drawer
     App.cites(list)                   row of chips
     App.notes(list, title)            the caveat box that must stay next to an answer
     App.chip(text, kind)              kind: '', 'warn', 'crit', 'good'
     App.confidence(level)             chip for high / medium / low
     App.pillar(p), App.phase(p)       chips
     App.legend([[label, color], ...])
     App.drawer(title, node, wide)     open the right-hand drawer; wide = true for documents, video and tables
     App.tex(text)                     Node: text with $inline$ math rendered; App.eq(latex) display equation
     App.panel(title, ...children)     titled surface
     App.PHASE_COLOR, App.PILLAR_COLOR lookups into colors().s — colour follows the entity everywhere
*/
const FIF = window.FIF = window.FIF || {};

function h(tag, attrs, ...children) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v == null || v === false) continue;
    if (k === 'class') el.className = v;
    else if (k === 'text') el.textContent = v;
    else if (k === 'html') el.innerHTML = v;
    else if (k === 'dataset') Object.assign(el.dataset, v);
    else if (k.startsWith('on') && typeof v === 'function') el.addEventListener(k.slice(2), v);
    else el.setAttribute(k, v === true ? '' : v);
  }
  for (const c of children.flat(Infinity)) {
    if (c == null || c === false) continue;
    el.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return el;
}

const App = {
  views: [], state: {}, current: null,

  view(def) { App.views.push(def); App.state[def.id] = App.state[def.id] || {}; },

  load(names) {
    return Promise.all((names || []).map(name => {
      if (FIF[name]) return null;
      App._loading = App._loading || {};
      return App._loading[name] = App._loading[name] || new Promise((resolve, reject) => {
        const s = document.createElement('script');
        s.src = `data/${name}.js`;
        s.onload = resolve;
        s.onerror = () => reject(new Error(`Could not load data/${name}.js`));
        document.head.append(s);
      });
    }));
  },

  go(id, patch) {
    if (patch) Object.assign(App.state[id] = App.state[id] || {}, patch);
    // Docked beside the page (wide screens) the drawer stays open across views; as an overlay it would hide the new view.
    if (!window.matchMedia('(min-width: 1000px)').matches) App.closeDrawer();
    if (location.hash === '#' + id) App.render(); else location.hash = id;
  },

  async render() {
    const id = (location.hash || '').replace(/^#/, '') || App.views[0].id;
    const v = App.views.find(x => x.id === id) || App.views[0];
    App.current = v;
    for (const a of document.querySelectorAll('#nav a')) {
      if (a.dataset.id === v.id) a.setAttribute('aria-current', 'page'); else a.removeAttribute('aria-current');
    }
    const main = document.getElementById('main');
    const scroll = window.scrollY, same = main.dataset.view === v.id;
    if (!same) main.replaceChildren(h('p', { class: 'muted', text: 'Loading…' }));
    try { await App.load(v.needs); } catch (e) {
      main.replaceChildren(h('div', { class: 'notes' }, h('p', { text: e.message + '. Open this page next to its data folder.' })));
      return;
    }
    if (App.current !== v) return;
    const root = h('div', { class: 'stack' });
    const head = h('div', { class: 'view-head' },
      h('div', {}, h('h1', { text: v.heading || v.title }), v.intro && h('p', { text: v.intro })),
      v.brief && h('button', { class: 'btn', type: 'button', onclick: () => App.drawer('For the dashboard team: ' + v.title, App.briefNode(v)) }, 'For the dashboard team'));
    const update = patch => { Object.assign(App.state[v.id], patch || {}); App.render(); };
    try { v.render(root, App.state[v.id], update); } catch (e) {
      console.error(e);
      root.replaceChildren(h('div', { class: 'notes' }, h('p', { text: 'This view failed to draw: ' + e.message })));
    }
    main.dataset.view = v.id;
    main.replaceChildren(head, root);
    window.scrollTo(0, same ? scroll : 0);
  },

  briefNode(v) {
    const b = v.brief || {};
    const sec = (title, node) => node && h('div', {}, h('h4', { text: title }), node);
    const list = a => a && a.length && h('ul', { style: 'margin:0;padding-left:18px' }, a.map(x => h('li', { text: x })));
    return h('div', { class: 'brief stack' },
      sec('What scientists need', b.need && h('p', { text: b.need })),
      sec('Data', list((b.data || []).map(d => d))),
      sec('Function', b.call && h('pre', { text: b.call })),
      sec('Must stay visible', list(b.keep)),
      sec('Needs a backend', b.backend && h('p', { text: b.backend })));
  },

  backend: false,
  async detectBackend() {
    if (!/^https?:$/.test(location.protocol)) return false;
    try {
      const ctl = new AbortController(), timer = setTimeout(() => ctl.abort(), 2500);
      const r = await fetch('api/health', { signal: ctl.signal });
      clearTimeout(timer);
      App.backend = r.ok && (await r.json()).ok === true;
    } catch (e) { App.backend = false; }
    return App.backend;
  },
  async api(fn, args) {
    if (!App.backend) throw new Error('This needs the dashboard server; the static page has only pre-computed answers.');
    const r = await fetch('api/call/' + fn, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(args || {}) });
    const body = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(body.detail || `The server answered ${r.status}`);
    return body;
  },
  async resolve(accession, file) {
    if (!App.backend) throw new Error('This needs the dashboard server.');
    const r = await fetch(`api/resolve?accession=${encodeURIComponent(accession)}&file=${encodeURIComponent(file)}`);
    const body = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(body.detail || `The server answered ${r.status}`);
    return body.url;
  },
  fileUrl(accession, file) { return `https://psi.nasa.gov/geode-py/ws/studies/${encodeURIComponent(accession)}/download?file=${encodeURIComponent(file)}`; },
  fileKind(file) {
    const ext = (String(file).match(/\.([A-Za-z0-9]+)$/) || [, ''])[1].toLowerCase();
    if (ext === 'pdf') return 'pdf';
    if (['mp4', 'webm', 'mov', 'm4v'].includes(ext)) return 'video';
    if (['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'].includes(ext)) return 'image';
    if (['csv', 'tsv', 'asc', 'dat'].includes(ext)) return 'table';
    if (['txt', 'log', 'meta', 'metadata', 'json', 'xml'].includes(ext)) return 'text';
    return 'other';
  },
  openFile(ref) {
    if (App.viewer) return App.viewer(ref);
    App.drawer(ref.title || ref.file, h('p', {}, h('a', { href: App.fileUrl(ref.accession, ref.file), target: '_blank', rel: 'noopener' }, 'Open the file at NASA PSI')));
  },
  parseSource(s) {
    if (!s || !s.file || s.psi_status === 'removed') return null;
    const acc = (String(s.file).match(/^(PSI-\d+)_/) || [])[1];
    if (!acc) return null;
    const page = (String(s.locator || '').match(/^p\.?\s*(\d+)/i) || [])[1];
    return { accession: acc, file: s.file, page: page ? +page : null };
  },

  inv(acc) {
    App._inv = App._inv || Object.fromEntries(FIF.investigations.map(i => [i.accession, { ...i, acronym: i.acronym || i.accession }]));
    return App._inv[acc] || { accession: acc, acronym: acc, title: acc, pillars: [], fuel_phases: [] };
  },
  name(acc) { const i = App.inv(acc); return i.acronym && i.acronym !== acc ? `${i.acronym} (${acc})` : acc; },

  fmt(v, digits) {
    if (v == null || v === '') return '–';
    if (typeof v !== 'number') return String(v);
    if (!isFinite(v)) return '–';
    if (digits != null) return v.toFixed(digits);
    const a = Math.abs(v);
    if (Number.isInteger(v)) return String(v);
    return a >= 100 ? v.toFixed(0) : a >= 10 ? v.toFixed(1) : a >= 1 ? v.toFixed(2) : v.toPrecision(2);
  },
  pct(x, digits) { return x == null ? '–' : (x * 100).toFixed(digits == null ? 1 : digits) + '%'; },

  _opts(options) { return options.map(o => Array.isArray(o) ? o : [o, o == null || o === '' ? 'All' : String(o)]); },
  select({ id, label, options, value, onChange }) {
    const sel = h('select', { id, onchange: e => onChange(e.target.value) },
      App._opts(options).map(([v, l]) => h('option', { value: v, selected: String(v) === String(value ?? '') }, l)));
    return h('label', { class: 'ctl' }, label, sel);
  },
  seg({ id, label, options, value, onChange }) {
    const box = h('div', { class: 'seg', id, role: 'group', 'aria-label': label || id },
      App._opts(options).map(([v, l]) => h('button', { type: 'button', 'aria-pressed': String(String(v) === String(value ?? '')), onclick: () => onChange(v) }, l)));
    return h('div', { class: 'ctl' }, label && h('span', { text: label }), box);
  },
  range({ id, label, min, max, step, value, onChange, format }) {
    const out = h('span', { class: 'num', style: 'color:var(--fg)' }, (format || App.fmt)(value));
    const input = h('input', { id, type: 'range', min, max, step, value,
      oninput: e => { out.textContent = (format || App.fmt)(+e.target.value); },
      onchange: e => onChange(+e.target.value) });
    return h('label', { class: 'ctl', style: 'flex:1 1 180px' }, h('span', {}, label, ' ', out), input);
  },
  search({ id, label, value, onChange, placeholder }) {
    return h('label', { class: 'ctl', style: 'flex:1 1 200px' }, label,
      h('input', { id, type: 'search', value: value || '', placeholder: placeholder || '', onchange: e => onChange(e.target.value) }));
  },

  table({ cols, rows, pageSize, onRow, sort }) {
    const st = { key: sort && sort.key, dir: (sort && sort.dir) || 1, page: 0 };
    const size = pageSize || 25;
    const wrap = h('div', { class: 'stack', style: 'gap:0' });
    const draw = () => {
      let data = rows;
      if (st.key) {
        data = [...rows].sort((a, b) => {
          const x = a[st.key], y = b[st.key];
          if (x == null && y == null) return 0; if (x == null) return 1; if (y == null) return -1;
          return (typeof x === 'number' && typeof y === 'number' ? x - y : String(x).localeCompare(String(y), undefined, { numeric: true })) * st.dir;
        });
      }
      const pages = Math.max(1, Math.ceil(data.length / size));
      st.page = Math.min(st.page, pages - 1);
      const slice = data.slice(st.page * size, (st.page + 1) * size);
      const thead = h('thead', {}, h('tr', {}, cols.map(c => h('th', {
        class: c.num ? 'n' : '', 'data-key': c.sortable === false ? null : c.key, style: c.width ? `min-width:${c.width}` : null,
        'aria-sort': st.key === c.key ? (st.dir > 0 ? 'ascending' : 'descending') : null,
        onclick: c.sortable === false ? null : () => { st.dir = st.key === c.key ? -st.dir : 1; st.key = c.key; draw(); } }, c.label || c.key))));
      const tbody = h('tbody', {}, slice.map(r => h('tr', { class: onRow ? 'click' : '', onclick: onRow ? () => onRow(r) : null },
        cols.map(c => { const v = c.fmt ? c.fmt(r[c.key], r) : (c.num ? App.fmt(r[c.key]) : (r[c.key] ?? '–')); return h('td', { class: c.num ? 'n' : '' }, v); }))));
      const pager = h('div', { class: 'pager' },
        h('span', { text: `${data.length} rows` }),
        pages > 1 && h('button', { class: 'btn', type: 'button', disabled: st.page === 0, onclick: () => { st.page--; draw(); } }, 'Previous'),
        pages > 1 && h('span', { class: 'num', text: `${st.page + 1} / ${pages}` }),
        pages > 1 && h('button', { class: 'btn', type: 'button', disabled: st.page >= pages - 1, onclick: () => { st.page++; draw(); } }, 'Next'));
      wrap.replaceChildren(h('div', { class: 'table-wrap' }, h('table', { class: 't' }, thead, tbody)), pager);
    };
    draw();
    return wrap;
  },

  colors() {
    const cs = getComputedStyle(document.documentElement), g = n => cs.getPropertyValue(n).trim();
    return { fg: g('--fg'), fg2: g('--fg-2'), fg3: g('--fg-3'), line: g('--line'), lineSoft: g('--line-soft'), bg: g('--bg'), surface: g('--surface'),
      accent: g('--accent'), warn: g('--warn'), crit: g('--crit'), good: g('--good'), seqLo: g('--seq-lo'), seqHi: g('--seq-hi'), neutral: g('--neutral-mark'),
      s: [1, 2, 3, 4, 5, 6, 7, 8].map(i => g('--s' + i)) };
  },
  PHASE_SLOT: { solid: 0, liquid: 1, gas: 2 },
  PILLAR_SLOT: { prevention: 0, detection: 1, suppression: 2, fundamental: 6 },
  phaseColor(p) { const c = App.colors(); return p in App.PHASE_SLOT ? c.s[App.PHASE_SLOT[p]] : c.neutral; },
  pillarColor(p) { const c = App.colors(); return p in App.PILLAR_SLOT ? c.s[App.PILLAR_SLOT[p]] : c.neutral; },

  plot(el, traces, layout, onClick) {
    const c = App.colors();
    if (!window.Plotly) { el.replaceChildren(h('p', { class: 'muted', text: 'Chart library not loaded (needs internet access to cdnjs).' })); return el; }
    const axis = { gridcolor: c.lineSoft, linecolor: c.line, zerolinecolor: c.line, tickfont: { color: c.fg2, size: 11 }, title: { font: { color: c.fg2, size: 12 } }, automargin: true };
    const L = Object.assign({ paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)', font: { family: 'Inter, system-ui, sans-serif', color: c.fg, size: 12 },
      margin: { l: 56, r: 16, t: 12, b: 48 }, height: 380, showlegend: traces.length > 1, colorway: c.s,
      legend: { orientation: 'h', y: -0.2, font: { color: c.fg2, size: 11 } }, hoverlabel: { bgcolor: c.surface, bordercolor: c.line, font: { color: c.fg, size: 12 } } }, layout || {});
    for (const k of Object.keys(L)) if (/^[xy]axis\d*$/.test(k)) {
      const t = L[k].title; L[k] = Object.assign({}, axis, L[k]);
      if (typeof t === 'string') L[k].title = { text: t, font: axis.title.font };
    }
    if (!L.xaxis) L.xaxis = axis; if (!L.yaxis) L.yaxis = axis;
    el.classList.add('plot');
    // The element must be in the document before Plotly measures it.
    requestAnimationFrame(() => {
      Plotly.newPlot(el, traces, L, { displayModeBar: false, responsive: true }).then(() => {
        if (onClick) el.on('plotly_click', ev => onClick(ev.points[0], ev));
      });
    });
    return el;
  },

  chip(text, kind, onClick) {
    return h(onClick ? 'button' : 'span', { class: 'chip' + (kind ? ' ' + kind : ''), type: onClick ? 'button' : null, onclick: onClick }, text);
  },
  confidence(level) { return level ? App.chip(level + ' confidence', level === 'high' ? 'good' : level === 'low' ? 'crit' : 'warn') : null; },
  pillar(p) { return h('span', { class: 'chip' }, h('span', { class: 'dot', style: `background:${App.pillarColor(p)}` }), p); },
  phase(p) { return h('span', { class: 'chip' }, h('span', { class: 'dot', style: `background:${App.phaseColor(p)}` }), p); },
  legend(items) { return h('div', { class: 'legend' }, items.map(([l, col]) => h('span', {}, h('span', { class: 'dot', style: `background:${col}` }), l))); },
  panel(title, ...children) { return h('section', { class: 'panel' }, title && h('h3', { text: title }), children); },
  notes(list, title) {
    if (!list || !list.length) return null;
    return h('div', { class: 'notes' }, h('h4', { text: title || 'Caveats that belong next to this answer' }), h('ul', {}, list.map(n => h('li', {}, App.tex(n)))));
  },

  citeLabel(c) {
    const letter = { findings: 'F', limitations: 'L', open_questions: 'Q', gaps: 'G' }[c.section];
    return `${c.accession} ${letter && c.index != null ? letter + c.index : c.section + (c.index != null ? ' ' + c.index : '')}`;
  },
  cite(c) { return h('button', { class: 'chip cite', type: 'button', title: 'Show the source', onclick: e => { e.stopPropagation(); App.openCite(c); } }, App.citeLabel(c)); },
  cites(list) { return list && list.length ? h('div', { class: 'chips' }, list.map(App.cite)) : null; },

  // a PSI file or tests-table row is part of an investigation's dataset, which PSI asks to be cited by its own DOI
  datasetDoi(s) {
    const m = /^psi_/.test(s.type || '') && /^(PSI-\d+)_/.exec(s.file || s.table || '');
    const i = m && App.inv(m[1]);
    return i && i.doi_url ? h('div', { class: 'small muted' }, `Dataset DOI (${m[1]}): `,
      h('a', { href: i.doi_url, target: '_blank', rel: 'noopener', text: i.doi, onclick: e => e.stopPropagation() })) : null;
  },
  sourceNode(s) {
    if (!s) return null;
    const where = s.file ? `${s.file}${s.locator ? ', ' + s.locator : ''}` : s.url || s.doi || s.table || s.field || '';
    return h('div', { class: 'stack', style: 'gap:4px' },
      h('div', { class: 'small muted' }, s.type ? s.type.replace(/_/g, ' ') + ': ' : '', s.url ? h('a', { href: s.url, target: '_blank', rel: 'noopener' }, s.url) : where,
        s.psi_status === 'removed' && App.chip('removed from PSI', 'warn')),
      s.quote && h('div', { class: 'quote', text: '“' + s.quote + '”' }),
      App.datasetDoi(s),
      App.parseSource(s) && h('div', {}, h('button', { class: 'btn link small', type: 'button', onclick: e => { e.stopPropagation(); App.openFile(App.parseSource(s)); } },
        App.parseSource(s).page ? `Open the document at page ${App.parseSource(s).page}` : 'Open the document')),
      s.note && h('div', { class: 'small', text: s.note }));
  },
  async openCite(c) {
    App.drawer(App.citeLabel(c), h('p', { class: 'muted', text: 'Loading the record…' }));
    await App.load(['records']);
    const rec = FIF.records[c.accession];
    const sec = rec && rec[c.section];
    const item = Array.isArray(sec) && c.index != null ? sec[c.index - 1] : sec;
    const body = h('div', { class: 'stack' });
    body.append(h('p', { class: 'small muted' }, App.name(c.accession), ' · ', c.section.replace(/_/g, ' '), c.index != null ? ' ' + c.index : ''));
    if (item == null) body.append(h('p', { text: 'This citation points to a section that is not in the record.' }));
    else if (typeof item === 'string') body.append(h('p', {}, App.tex(item)));
    else {
      const text = item.claim || item.text || item.summary;
      if (text) body.append(h('p', {}, App.tex(text)));
      else body.append(h('pre', { text: JSON.stringify(item, null, 1).slice(0, 4000) }));
      body.append(h('div', { class: 'chips' }, item.kind && App.chip(item.kind), App.confidence(item.confidence)));
      if (item.sources && item.sources.length) body.append(h('h4', { text: 'Sources' }), item.sources.map(App.sourceNode));
    }
    body.append(h('button', { class: 'btn', type: 'button', onclick: () => App.go('investigation', { accession: c.accession }) }, 'Open the full record'));
    App.drawer(App.citeLabel(c), body);
  },

  drawer(title, node, wide) {
    document.getElementById('drawer').classList.toggle('wide', !!wide);
    document.getElementById('drawer-title').textContent = title;
    document.getElementById('drawer-body').replaceChildren(node);
    document.getElementById('drawer').hidden = false;
    App.dockDrawer(wide ? 'wide' : 'narrow');
  },
  // The page gives up the drawer's width (app.css); charts only re-fit on a window resize event.
  dockDrawer(mode) {
    const root = document.documentElement;
    if ((root.dataset.drawer || null) === mode) return;
    if (mode) root.dataset.drawer = mode; else delete root.dataset.drawer;
    window.dispatchEvent(new Event('resize'));
  },
  closeDrawer() {
    const body = document.getElementById('drawer-body');
    // A video removed from the page keeps playing its sound unless it is paused first.
    body.querySelectorAll('video, audio').forEach(m => { try { m.pause(); m.removeAttribute('src'); m.load(); } catch (e) { /* not started */ } });
    if (App.viewerClose) App.viewerClose();
    body.replaceChildren();
    document.getElementById('drawer').hidden = true;
    App.dockDrawer(null);
  },

  math(latex, display) {
    const span = h('span', {});
    try { span.innerHTML = window.katex.renderToString(latex, { output: 'mathml', throwOnError: false, displayMode: !!display }); }
    catch (e) { span.textContent = latex; span.className = 'mono'; }
    return span;
  },
  tex(text) {
    const frag = document.createDocumentFragment();
    String(text ?? '').split(/(\$\$[^$]+\$\$|\$[^$\n]+\$|`[^`]+`)/).forEach(part => {
      if (!part) return;
      if (part.startsWith('$$')) frag.append(App.math(part.slice(2, -2), true));
      else if (part.startsWith('$') && part.length > 2) frag.append(App.math(part.slice(1, -1)));
      else if (part.startsWith('`')) frag.append(h('code', { text: part.slice(1, -1) }));
      else frag.append(part);
    });
    return frag;
  },
  eq(latex) { return h('div', { class: 'eq' }, App.math(latex, true)); },
};
