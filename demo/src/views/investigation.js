App.view({
  id: 'investigation', title: 'Investigations', tier: 1,
  heading: 'One investigation, the whole record',
  intro: 'The knowledge record behind each investigation: question, physics, method, test matrix, findings with their quoted sources, and what is still missing. Compare up to three side by side.',
  needs: ['records'],
  brief: {
    need: 'A readable page per investigation where every claim can be traced to a PSI file and page, plus a side-by-side comparison of two or three investigations.',
    data: ['data/export/records.json: the 24 knowledge records', 'data/export/investigations.json for names, pillars and counts', 'docs/digest/PSI-*.md as the same record in prose'],
    call: 'get_investigation(accession="PSI-25", sections=["findings", "limitations"])\ncompare(accessions=["PSI-25", "PSI-26", "PSI-98"])',
    keep: ['Confidence and kind on every finding', 'The sources of every finding: PSI file, page and verbatim quote, or the external URL', 'Quotes from PSI files are machine-checked against the files; external quotes are not independently checked', 'Citation ids such as [PSI-25 F3], L for limitations, Q for open questions, G for gaps (1-based)', 'Limitations and gaps next to the findings, not on a separate page', 'Files marked as removed from PSI'],
  },
  render(root, state, update) {
    const R = FIF.records || {};
    const accs = (FIF.investigations || []).map(i => i.accession).filter(a => R[a]);
    Object.keys(R).forEach(a => { if (!accs.includes(a)) accs.push(a); });
    const acc = R[state.accession] ? state.accession : (R['PSI-25'] ? 'PSI-25' : accs[0]);
    const rec = R[acc];
    const toTop = () => setTimeout(() => window.scrollTo(0, 0), 0);
    const open = a => { update({ accession: a, compare: (state.compare || []).filter(x => x !== a) }); toTop(); };
    const compare = (state.compare || []).filter(a => R[a] && a !== acc).slice(0, 2);

    // ---- generic renderers: record sections differ in shape between investigations
    const isEmpty = v => v == null || v === '' || (Array.isArray(v) && !v.length);
    const pretty = k => String(k).replace(/_/g, ' ');
    const src = s => {
      if (!s || typeof s !== 'object') return s ? h('div', { class: 'small', text: String(s) }) : null;
      const extra = ['sheet', 'row', 'value', 'field', 'id'].filter(k => s[k] != null && s[k] !== '' && !(k === 'sheet' && s.sheet === s.file));
      return h('div', { class: 'stack', style: 'gap:2px' }, App.sourceNode(s),
        extra.length ? h('div', { class: 'small mono muted', text: extra.map(k => `${k}: ${s[k]}`).join(' · ') }) : null);
    };
    const srcList = list => h('div', { class: 'stack', style: 'gap:8px' }, (list || []).map(src));
    const srcFold = list => list && list.length ? h('details', {}, h('summary', { class: 'small muted', style: 'cursor:pointer' }, `Sources (${list.length})`), h('div', { style: 'padding-top:6px' }, srcList(list))) : null;
    const srcBtn = list => list && list.length ? App.chip(`${list.length} source${list.length > 1 ? 's' : ''}`, '', e => { e.stopPropagation(); App.drawer('Sources', srcList(list)); }) : h('span', { class: 'muted', text: '–' });
    const gen = v => {
      if (isEmpty(v)) return h('span', { class: 'muted', text: '–' });
      if (typeof v === 'boolean') return h('span', { text: v ? 'yes' : 'no' });
      if (typeof v !== 'object') return h('p', {}, App.tex(String(v)));
      if (Array.isArray(v)) {
        if (v.every(x => x == null || typeof x !== 'object')) return h('ul', { style: 'margin:0;padding-left:18px' }, v.map(x => h('li', {}, App.tex(String(x ?? '–')))));
        return h('div', { class: 'stack', style: 'gap:8px' }, v.map(x => h('div', { style: 'border-left:2px solid var(--line);padding-left:10px' }, gen(x))));
      }
      const main = v.text ?? v.claim ?? v.value;
      const mainKey = v.text != null ? 'text' : v.claim != null ? 'claim' : v.value != null ? 'value' : null;
      const rest = Object.keys(v).filter(k => k !== mainKey && k !== 'sources' && !isEmpty(v[k]));
      return h('div', { class: 'stack', style: 'gap:6px' },
        mainKey && gen(main),
        rest.length ? h('dl', { class: 'kv' }, rest.flatMap(k => [h('dt', { text: pretty(k) }), h('dd', {}, gen(v[k]))])) : null,
        Array.isArray(v.sources) ? srcFold(v.sources) : null);
    };
    const smallTable = (rows, cols) => rows && rows.length ? App.table({ rows, cols, pageSize: 50 }) : h('p', { class: 'muted', text: 'Not stated in the record.' });
    const txt = v => isEmpty(v) ? '–' : typeof v === 'object' ? (v.text ?? v.value ?? JSON.stringify(v)) : String(v);

    // ---- controls
    root.append(h('div', { class: 'row' },
      App.select({ id: 'inv-acc', label: 'Investigation', options: accs.map(a => [a, App.name(a)]), value: acc, onChange: open }),
      h('button', { class: 'btn primary', type: 'button', onclick: () => App.go('tests', { accession: acc }) }, 'See its tests'),
      h('button', { class: 'btn', type: 'button', id: 'inv-files', onclick: () => App.go('files', { accession: acc }) }, 'Files and videos'),
      h('button', { class: 'btn', type: 'button', id: 'inv-search', onclick: () => App.go('search', { accession: acc }) }, 'Search its documents'),
      compare.length < 2 && App.select({ id: 'inv-compare-add', label: 'Compare with', value: '',
        options: [['', 'Add an investigation'], ...accs.filter(a => a !== acc && !compare.includes(a)).map(a => [a, App.name(a)])],
        onChange: v => { if (v) update({ compare: [...compare, v] }); } }),
      compare.length ? h('div', { class: 'ctl' }, h('span', { text: 'Comparing' }), h('div', { class: 'chips' },
        compare.map(a => App.chip(App.name(a) + ' ×', '', () => update({ compare: compare.filter(x => x !== a) }))),
        h('button', { class: 'btn link', type: 'button', onclick: () => update({ compare: [] }) }, 'clear'))) : null));

    if (!rec) { root.append(h('div', { class: 'notes' }, h('p', { text: 'No record was found for this investigation.' }))); return; }

    // ---- compare
    if (compare.length) {
      const set = [acc, ...compare];
      const inv = a => App.inv(a);
      const findings = a => ((R[a] || {}).findings || []).slice(0, 3);
      const fields = [
        ['Question', a => App.tex(txt((R[a] || {}).question))],
        ['Fuels and samples', a => { const f = (((R[a] || {}).method || {}).fuels_and_samples || []); return f.length ? h('ul', { style: 'margin:0;padding-left:16px' }, f.map(x => h('li', {}, typeof x === 'object' ? `${x.name || '–'}${x.phase ? ' (' + x.phase + ')' : ''}` : String(x)))) : '–'; }],
        ['Pillars', a => h('div', { class: 'chips' }, (((R[a] || {}).fire_safety || {}).pillars || inv(a).pillars || []).map(App.pillar))],
        ['Fuel phases', a => h('div', { class: 'chips' }, (inv(a).fuel_phases || []).map(App.phase))],
        ['Tests', a => { const n = (((R[a] || {}).test_matrix || {}).n_tests || {}).value; return `${App.fmt(inv(a).n_test_rows)} rows in the tests table; record says: ${n == null ? 'not stated' : String(n)}`; }],
        ['First 3 findings', a => h('ol', { style: 'margin:0;padding-left:18px' }, findings(a).map((f, i) => h('li', {},
          App.tex(typeof f === 'object' ? (f.claim || f.text || '') : String(f)), ' ',
          h('span', { class: 'chips', style: 'display:inline-flex' }, App.cite({ accession: a, section: 'findings', index: i + 1 }), typeof f === 'object' ? App.confidence(f.confidence) : null))))],
        ['Top limitations', a => h('ol', { style: 'margin:0;padding-left:18px' }, ((R[a] || {}).limitations || []).slice(0, 3).map((l, i) => h('li', {},
          App.tex(typeof l === 'object' ? (l.text || '') : String(l)), ' ', App.cite({ accession: a, section: 'limitations', index: i + 1 }))))],
      ];
      root.append(App.panel(`Side by side: ${set.map(a => inv(a).acronym || a).join(', ')}`,
        App.table({ pageSize: 20, rows: fields.map(([label, fn]) => ({ label, fn })), cols: [
          { key: 'label', label: 'Field', sortable: false, width: '110px' },
          ...set.map(a => ({ key: a, label: App.name(a), sortable: false, width: '260px', fmt: (_, r) => { try { return r.fn(a); } catch (e) { return '–'; } } }))] }),
        h('p', { class: 'muted small', text: 'Scroll sideways on a narrow screen. Click a citation for its quoted source.' })));
    }

    // ---- header
    const id = rec.identity || {}, info = App.inv(acc), tm = rec.test_matrix || {}, phys = rec.physics || {};
    const nTests = (tm.n_tests || {}).value;
    root.append(h('div', { class: 'stack', style: 'gap:6px' },
      h('h2', { text: `${id.acronym || info.acronym || acc} · ${acc}` }),
      h('p', { text: id.title || info.title || '' }),
      h('div', { class: 'chips' }, (info.pillars || []).map(App.pillar), (info.fuel_phases || []).map(App.phase), App.chip(info.flight ? 'flight' : 'ground or analysis'))));
    root.append(h('div', { class: 'grid tiles' },
      h('div', { class: 'tile' }, h('b', { text: App.fmt(info.n_test_rows) }), h('span', { text: 'rows in the tests table' })),
      h('div', { class: 'tile' }, h('b', { text: typeof nTests === 'number' ? String(nTests) : '–' }), h('span', { text: typeof nTests === 'string' ? 'tests: see the test matrix, the count is disputed' : 'tests according to the record' })),
      h('div', { class: 'tile' }, h('b', { text: String((rec.findings || []).length) }), h('span', { text: 'findings' })),
      h('div', { class: 'tile' }, h('b', { text: String((phys.equations || []).length) }), h('span', { text: 'equations' })),
      h('div', { class: 'tile' }, h('b', { text: String((rec.limitations || []).length) }), h('span', { text: 'limitations' }))));

    const hooks = rec.dashboard_hooks || [];
    if (hooks.length) root.append(h('section', { class: 'panel', style: 'border-color:var(--accent)' },
      h('h3', { text: 'Dashboard views this record suggests' }),
      h('p', { class: 'muted small', text: 'Written while reading the PSI files: the views this investigation would need, the fields they use, and why.' }),
      h('div', { class: 'grid' }, hooks.map(k => h('div', { class: 'stack', style: 'gap:4px;border-left:3px solid var(--accent);padding-left:10px' },
        h('h4', { text: (k && k.view) || 'view' }),
        k && k.why ? h('p', { class: 'small' }, App.tex(k.why)) : null,
        k && k.fields && k.fields.length ? h('div', { class: 'chips' }, k.fields.map(f => h('code', { class: 'chip', text: String(f) }))) : null)))));

    // ---- sections
    const S = [];
    const sec = (key, title, ...body) => S.push([key, title, body]);
    const findings = rec.findings || [];

    sec('identity', 'Identity', h('dl', { class: 'kv' },
      h('dt', { text: 'Principal investigators' }), h('dd', {}, gen(id.principal_investigators)),
      h('dt', { text: 'Dates' }), h('dd', { text: id.dates && typeof id.dates === 'object' ? `${id.dates.start || '?'} to ${id.dates.end || '?'}` : txt(id.dates) }),
      ...['platform', 'facility', 'hardware', 'project_type'].flatMap(k => [h('dt', { text: pretty(k) }), h('dd', {}, gen(id[k]))])));
    sec('summary', 'Summary', h('div', { class: 'prose' }, gen(rec.summary)));
    sec('question', 'Question', h('div', { class: 'prose' }, gen(rec.question)));
    sec('physics', 'Physics', h('div', { class: 'prose' }, gen(phys.text), srcFold(phys.sources)),
      (phys.equations || []).map((e, i) => h('div', { class: 'stack', style: 'gap:4px;border-top:1px solid var(--line-soft);padding-top:8px' },
        h('span', { class: 'small muted', text: `Equation ${i + 1}` }),
        e && e.latex ? App.eq(e.latex) : null,
        e && e.meaning ? h('p', { class: 'small' }, App.tex(e.meaning)) : null,
        e && typeof e !== 'object' ? gen(e) : null,
        e && srcFold(e.sources))));
    const meth = rec.method || {};
    sec('method', 'Method',
      h('h4', { text: 'Apparatus' }), gen(meth.apparatus),
      h('h4', { text: 'Fuels and samples' }),
      Array.isArray(meth.fuels_and_samples) ? smallTable(meth.fuels_and_samples, [
        { key: 'name', label: 'Fuel or sample', sortable: false, width: '280px', fmt: v => App.tex(txt(v)) },
        { key: 'phase', label: 'Phase', fmt: v => v ? App.phase(v) : '–' },
        { key: 'form', label: 'Form', sortable: false, fmt: v => txt(v) },
        { key: 'sources', label: 'Sources', sortable: false, fmt: srcBtn }]) : gen(meth.fuels_and_samples),
      h('h4', { text: 'Procedure' }), gen(meth.procedure));
    sec('test_matrix', 'Test matrix',
      h('div', { class: 'stack', style: 'gap:4px' }, h('p', {}, h('b', { text: 'Number of tests: ' }), App.tex(txt(nTests))), srcFold((tm.n_tests || {}).sources)),
      h('h4', { text: 'Varied' }),
      Array.isArray(tm.varied) ? smallTable(tm.varied, [
        { key: 'parameter', label: 'Parameter', width: '200px' }, { key: 'range', label: 'Range', sortable: false, width: '260px', fmt: v => App.tex(txt(v)) },
        { key: 'unit', label: 'Unit' }, { key: 'sources', label: 'Sources', sortable: false, fmt: srcBtn }]) : gen(tm.varied),
      h('h4', { text: 'Held constant' }),
      Array.isArray(tm.held_constant) ? smallTable(tm.held_constant, [
        { key: 'parameter', label: 'Parameter', width: '200px' }, { key: 'value', label: 'Value', sortable: false, width: '300px', fmt: v => App.tex(txt(v)) },
        { key: 'sources', label: 'Sources', sortable: false, fmt: srcBtn }]) : gen(tm.held_constant));
    sec('measurements', 'Measurements', Array.isArray(rec.measurements) ? smallTable(rec.measurements, [
      { key: 'quantity', label: 'Quantity', width: '240px', fmt: v => App.tex(txt(v)) }, { key: 'instrument', label: 'Instrument', sortable: false, width: '240px', fmt: v => App.tex(txt(v)) },
      { key: 'derived', label: 'Derived', fmt: v => v == null ? '–' : v ? 'yes' : 'no' }, { key: 'sources', label: 'Sources', sortable: false, fmt: srcBtn }]) : gen(rec.measurements));
    sec('findings', `Findings (${findings.length})`,
      h('p', { class: 'muted small', text: 'Quotes from PSI files are machine-checked against the files. External quotes are not independently checked.' }),
      findings.map((f, i) => {
        const o = f && typeof f === 'object' ? f : { claim: String(f ?? '') };
        return h('div', { class: 'stack', style: 'gap:6px;border-top:1px solid var(--line-soft);padding-top:10px' },
          h('div', { class: 'chips' }, h('span', { class: 'chip cite', text: `${acc} F${i + 1}` }), o.kind ? App.chip(pretty(o.kind)) : null, App.confidence(o.confidence)),
          h('p', {}, App.tex(o.claim || o.text || '')),
          o.sources && o.sources.length ? h('div', { style: 'padding-left:10px' }, srcList(o.sources)) : h('p', { class: 'small muted', text: 'No source listed.' }));
      }));
    const fs = rec.fire_safety || {};
    sec('fire_safety', 'Fire-safety relevance',
      h('div', { class: 'chips' }, (fs.pillars || []).map(App.pillar)),
      h('h4', { text: 'Relevance' }), gen(fs.relevance),
      h('h4', { text: 'Habitat conditions' }), gen(fs.habitat_conditions),
      h('h4', { text: 'Benefits on Earth' }), gen(fs.earth_benefits));
    const numbered = (list, letter) => Array.isArray(list) && list.length
      ? h('div', { class: 'stack', style: 'gap:8px' }, list.map((x, i) => h('div', { class: 'row', style: 'align-items:flex-start;flex-wrap:nowrap' },
        h('span', { class: 'chip cite', style: 'flex:none', text: `${letter}${i + 1}` }), h('div', { style: 'min-width:0;flex:1' }, gen(x)))))
      : gen(list);
    sec('limitations', 'Limitations', numbered(rec.limitations, 'L'));
    sec('open_questions', 'Open questions', numbered(rec.open_questions, 'Q'));
    sec('gaps', 'Gaps', numbered(rec.gaps, 'G'));
    sec('related', 'Related investigations', Array.isArray(rec.related) && rec.related.length
      ? h('div', { class: 'chips' }, rec.related.map(r => {
        const a = r && typeof r === 'object' ? r.accession : r;
        const lab = `${App.name(a)}${r && r.relation ? ': ' + r.relation : ''}`;
        return R[a] ? App.chip(lab, '', () => open(a)) : App.chip(lab);
      }))
      : gen(rec.related));
    const pd = rec.psi_data || {};
    sec('psi_data', 'PSI data files',
      h('div', { class: 'prose' }, gen(pd.summary)),
      pd.tests_table_rows != null ? h('p', { class: 'small', text: `Rows in the PSI tests table: ${pd.tests_table_rows}` }) : h('p', { class: 'small muted', text: 'This investigation has no PSI tests table.' }),
      Array.isArray(pd.file_groups) ? smallTable(pd.file_groups, [
        { key: 'category', label: 'Category' }, { key: 'what', label: 'What', sortable: false, width: '320px', fmt: v => txt(v) },
        { key: 'formats', label: 'Formats', sortable: false, fmt: v => Array.isArray(v) ? v.join(' ') : txt(v) },
        { key: 'n_files', label: 'Files', num: true }, { key: 'size_gb', label: 'GB', num: true, fmt: v => App.fmt(v, 3) },
        { key: 'usable_now', label: 'Usable now', fmt: v => v == null ? '–' : App.chip(v ? 'yes' : 'no', v ? 'good' : 'warn') }]) : gen(pd.file_groups));

    const known = new Set(['accession', 'identity', 'one_line', 'summary', 'question', 'physics', 'method', 'test_matrix', 'measurements', 'findings', 'fire_safety', 'limitations', 'open_questions', 'gaps', 'related', 'psi_data', 'dashboard_hooks']);
    Object.keys(rec).filter(k => !known.has(k) && !isEmpty(rec[k])).forEach(k => sec(k, pretty(k), gen(rec[k])));

    root.append(h('nav', { class: 'chips', 'aria-label': 'Sections of this record' },
      h('span', { class: 'small muted', text: 'Jump to:' }),
      S.map(([key, title]) => App.chip(title, '', () => { const el = document.getElementById('inv-sec-' + key); if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' }); }))));
    for (const [key, title, body] of S) {
      const p = App.panel(title, body);
      p.id = 'inv-sec-' + key;
      p.style.scrollMarginTop = '96px';
      root.append(p);
    }
    root.append(h('div', { class: 'row' },
      h('button', { class: 'btn primary', type: 'button', onclick: () => App.go('tests', { accession: acc }) }, 'See its tests'),
      h('button', { class: 'btn', type: 'button', onclick: () => window.scrollTo(0, 0) }, 'Back to top')));
  },
});
