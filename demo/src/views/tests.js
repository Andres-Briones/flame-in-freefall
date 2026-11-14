(function () {
  // Numeric columns offered as chart axes. pct: stored as a mole fraction, shown as percent.
  // x_o2_burner is its own axis on purpose: it is an oxidiser stream, never an atmosphere.
  const AXES = [
    { key: 'x_o2_ambient', label: 'ambient O2 (atmosphere)', unit: 'mole %', pct: true },
    { key: 'x_o2_burner', label: 'burner-stream O2 (inverse flames, not an atmosphere)', unit: 'mole %', pct: true },
    { key: 'pressure_kpa', label: 'pressure', unit: 'kPa' },
    { key: 'flow_cm_s', label: 'flow velocity', unit: 'cm/s' },
    { key: 'fuel_fraction', label: 'fuel mole fraction', unit: '' },
    { key: 'burn_time_s', label: 'burn time', unit: 's' },
    { key: 'spread_rate_mm_s', label: 'flame spread rate', unit: 'mm/s' },
    { key: 'burn_length_cm', label: 'burned length', unit: 'cm' },
    { key: 'burn_rate_k_mm2_s', label: 'burning-rate constant K', unit: 'mm²/s' },
    { key: 'd0_mm', label: 'initial droplet diameter', unit: 'mm' },
    { key: 'ext_diameter_mm', label: 'extinction diameter', unit: 'mm' },
    { key: 'n_reignitions', label: 're-ignitions', unit: 'count' },
    { key: 'peak_temp_c', label: 'peak burner temperature', unit: '°C' },
    { key: 't_ad_k', label: 'adiabatic flame temperature', unit: 'K' },
    { key: 'flame_length_mm', label: 'flame length', unit: 'mm' },
    { key: 'n_flames', label: 'flames per test day', unit: 'count' },
  ];
  const NONE = '__none__';
  const PHASES = ['solid', 'liquid', 'gas', 'aerosol'];
  const FILTER_KEYS = ['phase', 'fuel', 'config', 'ext', 'o2min', 'o2max', 'pmin', 'pmax', 'flagged', 'allKinds'];

  const num = v => typeof v === 'number' && isFinite(v);
  const parseNum = v => { const x = parseFloat(v); return isFinite(x) ? x : null; };
  const flagList = r => String(r.flags || '').split(';').map(s => s.trim()).filter(Boolean);
  const kindOf = r => r.row_kind || 'test';
  const accNum = a => parseInt(String(a).replace(/\D/g, ''), 10) || 0;
  const axisTitle = a => a.unit ? `${a.label} (${a.unit})` : a.label;
  const plain = s => String(s ?? '').replace(/[<>&]/g, ch => ({ '<': '‹', '>': '›', '&': '+' })[ch]);
  const fmtVal = (a, v) => num(v) ? (a.pct ? App.pct(v) : App.fmt(v)) : '–';

  // Rows passing the investigation, phase and kind filters: the base for option lists.
  function baseRows(rows, s) {
    const out = [];
    for (const r of rows) {
      if (!s.allKinds && kindOf(r) !== 'test') continue;
      if (s.accession && r.accession !== s.accession) continue;
      if (s.phase && s.phase !== 'all' && r.fuel_phase !== s.phase) continue;
      out.push(r);
    }
    return out;
  }

  function optionValues(rows, key) {
    const seen = new Map();
    for (const r of rows) { const v = r[key] == null || r[key] === '' ? NONE : String(r[key]); seen.set(v, (seen.get(v) || 0) + 1); }
    return [...seen.entries()].sort((a, b) => a[0] === NONE ? 1 : b[0] === NONE ? -1 : a[0].localeCompare(b[0]));
  }

  const matchCat = (r, key, want) => !want || (want === NONE ? r[key] == null || r[key] === '' : String(r[key] ?? '') === want);

  function haystack(r) {
    return [r.accession, r.acronym, r.test_id, r.fuel, r.fuel_raw, r.config, r.geometry, r.flags, r.extinction_mode, r.date]
      .filter(x => x != null).join(' ').toLowerCase();
  }

  // Full filter. Returns {rows, base, exact, fuelOk, ...}. `s` is the view state.
  function filter(all, s) {
    const base = baseRows(all, s);
    const fuels = optionValues(base, 'fuel').map(x => x[0]);
    const fuel = s.fuel && fuels.includes(s.fuel) ? s.fuel : '';
    const o2min = parseNum(s.o2min), o2max = parseNum(s.o2max), pmin = parseNum(s.pmin), pmax = parseNum(s.pmax);
    const q = String(s.q || '').trim().toLowerCase();
    const pre = [];
    for (const r of base) {
      if (!matchCat(r, 'fuel', fuel) || !matchCat(r, 'config', s.config) || !matchCat(r, 'extinction_mode', s.ext)) continue;
      if (o2min != null || o2max != null) {
        // Only the atmosphere: x_o2_burner never answers an ambient O2 filter.
        const x = r.x_o2_ambient;
        if (!num(x)) continue;
        if (o2min != null && x * 100 < o2min) continue;
        if (o2max != null && x * 100 > o2max) continue;
      }
      if (pmin != null || pmax != null) {
        const p = r.pressure_kpa;
        if (!num(p)) continue;
        if (pmin != null && p < pmin) continue;
        if (pmax != null && p > pmax) continue;
      }
      if (s.flagged && !r.flags) continue;
      pre.push(r);
    }
    let rows = pre, exact = false;
    if (q) {
      // Sensor-recording ids have no space ("21088M4"); the table writes "21088 M4".
      const bare = x => String(x || '').toLowerCase().replace(/\s+/g, '');
      const ex = pre.filter(r => bare(r.test_id) === bare(q));
      if (ex.length) { rows = ex; exact = true; } else rows = pre.filter(r => haystack(r).includes(q));
    }
    return { rows, base, fuel, exact, total: s.allKinds ? all.length : all.filter(r => kindOf(r) === 'test').length };
  }

  // Raw-data conflicts and changed values that concern one test row.
  function evidenceFor(t, D) {
    D = D || {};
    let ids = [];
    try { const ex = t.extra ? JSON.parse(t.extra) : {}; if (Array.isArray(ex.discrepancies)) ids = ex.discrepancies; } catch (e) { /* unparsable extra */ }
    const conflicts = (D.raw_data_conflicts || []).filter(c => c.accession === t.accession &&
      ((c.test_id != null && c.test_id === t.test_id) || (c.test_id_now != null && c.test_id_now === t.test_id) || ids.includes(c.id)));
    const changed = (D.values_changed || []).filter(v => v.accession === t.accession && v.test_id === t.test_id);
    return { conflicts, changed };
  }

  function availableAxes(rows) {
    return AXES.filter(a => { let n = 0; for (const r of rows) if (num(r[a.key]) && ++n >= 1) return true; return false; });
  }

  function openTest(t) {
    const D = FIF.discrepancies || {};
    const meaning = Object.fromEntries((D.flags || []).map(f => [f.flag, f.meaning]));
    const flags = flagList(t);
    const ev = evidenceFor(t, D);
    let extra = null, extraErr = false;
    try { extra = t.extra ? JSON.parse(t.extra) : null; } catch (e) { extraErr = true; }
    const show = (k, v) => {
      if (typeof v === 'boolean') return k === 'cool_flame' && v ? 'true (an empty cell means no data, not "no cool flame")' : String(v);
      if (num(v)) return /^x_o2/.test(k) ? `${App.pct(v, 2)} (${v})` : App.fmt(v);
      if (v == null) return 'empty in source';
      return typeof v === 'object' ? JSON.stringify(v) : String(v);
    };
    const skip = new Set(['extra', 'flags', 'source_file', 'source_row']);
    const sourceName = String(t.source_file || '').split('/').pop();
    const traceSlot = h('span', {});
    const fields = Object.keys(t).filter(k => !skip.has(k) && t[k] != null && t[k] !== '');
    const body = h('div', { class: 'stack' },
      h('p', { class: 'small muted' }, App.name(t.accession), ' · ', kindOf(t).replace(/_/g, ' '), t.fuel_phase ? ' · ' : '', t.fuel_phase ? App.phase(t.fuel_phase) : null),
      num(t.x_o2_burner) && h('div', { class: 'callout gap small', text: `Inverse flame: ${App.pct(t.x_o2_burner)} O2 is the burner oxidiser stream. The surrounding atmosphere is fuel and N2, with no O2.` }),
      flags.length ? h('div', { class: 'stack', style: 'gap:6px' }, h('h4', { text: `Flags (${flags.length})` }),
        flags.map(f => h('div', {}, App.chip(f, 'warn'), ' ', h('span', { class: 'small' }, meaning[f] ? App.tex(meaning[f]) : 'No meaning recorded for this flag.')))) : null,
      ev.conflicts.length ? h('div', { class: 'stack', style: 'gap:6px' }, h('h4', { text: 'Conflicts with the raw sensor data' }),
        ev.conflicts.map(c => h('div', { class: 'panel', style: 'padding:10px' },
          h('div', { class: 'chips' }, App.chip(c.id, 'crit'), App.chip(c.action || 'no action'), c.column && h('span', { class: 'mono', text: c.column })),
          h('dl', { class: 'kv' },
            h('dt', { text: 'table value' }), h('dd', { class: 'mono', text: show('', c.table_value) }),
            h('dt', { text: 'value now' }), h('dd', { class: 'mono', text: c.action === 'flag' ? `${show('', c.table_value)} (kept; evidence says ${show('', c.evidence_value)})` : show('', c.evidence_value) }),
            h('dt', { text: 'evidence' }), h('dd', { text: c.evidence || '–' }),
            h('dt', { text: 'source' }), h('dd', { class: 'small', text: c.evidence_source || '–' }))))) : null,
      ev.changed.length ? h('div', { class: 'stack', style: 'gap:6px' }, h('h4', { text: 'Values changed from the NASA table' }),
        App.table({ rows: ev.changed, pageSize: 10, cols: [
          { key: 'column', label: 'Column', fmt: v => h('span', { class: 'mono', text: v || '–' }) },
          { key: 'table_value', label: 'Table value', fmt: v => show('', v) },
          { key: 'value_now', label: 'Value now', fmt: v => show('', v) },
          { key: 'patch_ids', label: 'Patches', sortable: false, fmt: v => Array.isArray(v) && v.length ? v.join(', ') : 'report or record' }] })) : null,
      h('h4', { text: 'All recorded fields' }),
      h('dl', { class: 'kv' }, fields.flatMap(k => [h('dt', { class: 'mono', text: k }), h('dd', { text: show(k, t[k]) })])),
      h('h4', { text: 'Original table columns' }),
      extraErr ? h('pre', { text: String(t.extra) }) :
        extra && typeof extra === 'object' && Object.keys(extra).length ?
          h('dl', { class: 'kv' }, Object.keys(extra).flatMap(k => [h('dt', { class: 'mono', text: k }), h('dd', { text: show(k, extra[k]) })])) :
          h('p', { class: 'muted small', text: 'None.' }),
      h('h4', { text: 'Source' }),
      h('p', { class: 'small mono', text: `${t.source_file || 'unknown file'}${t.source_row != null ? ', row ' + t.source_row : ''}` }),
      h('div', { class: 'row' },
        h('button', { class: 'btn primary', type: 'button', onclick: () => App.go('quality', { accession: t.accession, q: t.test_id }) }, 'Open in Data quality'),
        h('button', { class: 'btn', type: 'button', onclick: () => App.go('investigation', { accession: t.accession }) }, 'Open the record'),
        sourceName ? h('button', { class: 'btn', type: 'button', id: 'te-open-source', onclick: () => App.openFile({ accession: t.accession, file: sourceName }) }, 'Open the source table at NASA PSI') : null,
        traceSlot));
    App.drawer(`${t.acronym || t.accession} ${t.test_id}`, body);
    // Recording ids have no space ("21088M4"); the tests table writes "21088 M4".
    const bare = x => String(x ?? '').replace(/\s+/g, '').toLowerCase();
    App.load(['tsfeatures']).then(() => {
      const rec = (Array.isArray(FIF.tsfeatures) ? FIF.tsfeatures : []).find(r => r.accession === t.accession && t.test_id != null && bare(r.test_id) === bare(t.test_id));
      if (rec) traceSlot.replaceChildren(h('button', { class: 'btn', type: 'button', id: 'te-plot-trace',
        onclick: () => App.go('traces', { accession: t.accession, test_id: rec.test_id, test_point: rec.test_point }) }, 'Plot its sensor trace'));
    }).catch(() => { /* without the summaries there is just no trace link */ });
  }

  App.view({
    id: 'tests', title: 'Test explorer', tier: 1,
    heading: 'What was tested, and what happened?',
    intro: 'Every row of the per-test table, with the conditions and the measured outcomes. Flagged rows carry a badge that leads to the evidence.',
    needs: ['tests'],
    brief: {
      need: 'A filterable table and scatter of every test, so a scientist can find the tests near a condition and open the original row, its corrections and the evidence behind them.',
      data: ['data/export/tests.json: 2,177 rows (2,059 single tests), column dictionary in docs/tests-table.md', 'data/export/discrepancies.json for flag meanings and the evidence of each change'],
      call: 'filter_tests(accession="PSI-10", fuel_phase="gas", x_o2=[0.15, 0.25], pressure_kpa=[50, 110], row_kind="test")\ndiscrepancies(accession="PSI-10", test_id="22024M1")',
      keep: [
        'x_o2_ambient is the atmosphere. x_o2_burner (up to 0.85) is the oxidiser stream of inverse flames. Never put them on one axis or in one filter.',
        'Only row_kind = test rows are single tests. Test days, condition sets and planned rows are labelled when shown.',
        'cool_flame is true or empty, never false. Empty means no data.',
        'Flagged rows carry a badge linked to the evidence (discrepancies). The original NASA value is always kept and shown.',
        'Rows without a value are not on the chart; say how many.',
      ],
      backend: 'None for this view. 2,177 rows filter fast in the browser. A server is only needed if the table grows or for the raw sensor traces.',
    },
    filter, evidenceFor, availableAxes, AXES,

    render(root, state, update) {
      const all = FIF.tests || [];
      const c = App.colors();

      // State coming from another view (App.go with accession or q): start from clean filters.
      const acc0 = state.accession || '', q0 = state.q || '';
      const external = state._seenAcc === undefined ? !!(acc0 || q0) : acc0 !== state._seenAcc || q0 !== state._seenQ;
      if (external) {
        if (state._seenAcc !== undefined && acc0 !== state._seenAcc && q0 === state._seenQ) state.q = '';
        for (const k of FILTER_KEYS) delete state[k];
        if (state.q && !filter(all, state).rows.length && filter(all, Object.assign({}, state, { allKinds: true })).rows.length) state.allKinds = true;
      }
      state._seenAcc = state.accession || ''; state._seenQ = state.q || '';
      const set = p => { const n = Object.assign({}, state, p); update(Object.assign({}, p, { _seenAcc: n.accession || '', _seenQ: n.q || '' })); };

      const res = filter(all, state);
      const index = new Map(all.map((r, i) => [r, i]));
      const rows = res.rows;
      const accs = [...new Set(all.map(r => r.accession))].sort((a, b) => accNum(a) - accNum(b));
      const catOpts = (key, allLabel, noneLabel) => [['', allLabel], ...optionValues(res.base, key).map(([v, n]) => [v, `${v === NONE ? noneLabel : v.replace(/_/g, ' ')} (${n})`])];
      const numInput = (id, label, key, placeholder) => h('label', { class: 'ctl', style: 'flex:0 1 110px' }, label,
        h('input', { id, type: 'number', step: 'any', value: state[key] ?? '', placeholder, onchange: e => set({ [key]: e.target.value }) }));
      const check = (id, label, key) => h('label', { class: 'ctl', style: 'flex-direction:row;align-items:center;gap:6px;min-height:32px' },
        h('input', { id, type: 'checkbox', checked: !!state[key], onchange: e => set({ [key]: e.target.checked }) }), label);
      const nOther = all.filter(r => kindOf(r) !== 'test').length;

      root.append(h('div', { class: 'row' },
        App.select({ id: 'te-acc', label: 'Investigation', value: state.accession || '', onChange: v => set({ accession: v, fuel: '' }),
          options: [['', 'All investigations'], ...accs.map(a => [a, App.name(a)])] }),
        App.seg({ id: 'te-phase', label: 'Fuel phase', value: state.phase || 'all', onChange: v => set({ phase: v, fuel: '' }),
          options: [['all', 'All'], ...PHASES] }),
        App.select({ id: 'te-fuel', label: 'Fuel', value: res.fuel, onChange: v => set({ fuel: v }), options: catOpts('fuel', 'All fuels', 'not labelled') }),
        App.select({ id: 'te-config', label: 'Configuration', value: state.config || '', onChange: v => set({ config: v }), options: catOpts('config', 'All', 'not recorded') }),
        App.select({ id: 'te-ext', label: 'Extinction mode', value: state.ext || '', onChange: v => set({ ext: v }), options: catOpts('extinction_mode', 'All', 'not recorded') })));
      root.append(h('div', { class: 'row' },
        numInput('te-o2min', 'Ambient O2 min %', 'o2min', 'e.g. 15'),
        numInput('te-o2max', 'Ambient O2 max %', 'o2max', 'e.g. 25'),
        numInput('te-pmin', 'Pressure min kPa', 'pmin', 'e.g. 50'),
        numInput('te-pmax', 'Pressure max kPa', 'pmax', 'e.g. 110'),
        App.search({ id: 'te-q', label: 'Search (test id, fuel, flag)', value: state.q || '', onChange: v => set({ q: v }), placeholder: 'e.g. 22024M1' }),
        check('te-flagged', 'Flagged only', 'flagged'),
        check('te-kinds', `Include test days, condition sets and planned rows (${nOther})`, 'allKinds'),
        h('button', { class: 'btn', type: 'button', id: 'te-reset', onclick: () => set({ accession: '', q: '', phase: 'all', fuel: '', config: '', ext: '', o2min: '', o2max: '', pmin: '', pmax: '', flagged: false, allKinds: false }) }, 'Reset')));

      const nFlag = rows.filter(r => r.flags).length;
      const ranged = parseNum(state.o2min) != null || parseNum(state.o2max) != null;
      root.append(h('p', { class: 'num' },
        h('b', { text: `${rows.length} of ${res.total} ${state.allKinds ? 'rows' : 'tests'}` }),
        `, ${nFlag} flagged.`,
        res.exact ? ` Exact test id match for "${state.q}".` : '',
        ranged ? ' The O2 filter uses ambient O2 only, so inverse flames and rows without a per-test O2 are left out.' : ''));

      // Chart
      const axes = availableAxes(rows);
      const keys = axes.map(a => a.key);
      let xk = keys.includes(state.x) ? state.x : keys.includes('x_o2_ambient') ? 'x_o2_ambient' : keys[0];
      let yk = keys.includes(state.y) && state.y !== xk ? state.y : keys.includes('pressure_kpa') && xk !== 'pressure_kpa' ? 'pressure_kpa' : keys.find(k => k !== xk);
      const colorBy = state.color === 'outcome' ? 'outcome' : 'phase';
      const plotBox = h('div', {});
      const panelKids = [];
      if (xk && yk) {
        const ax = AXES.find(a => a.key === xk), ay = AXES.find(a => a.key === yk);
        const pts = rows.filter(r => num(r[xk]) && num(r[yk]));
        const scale = (a, v) => a.pct ? v * 100 : v;
        let groups;
        if (colorBy === 'outcome') {
          const counts = new Map();
          for (const r of pts) if (r.extinction_mode) counts.set(r.extinction_mode, (counts.get(r.extinction_mode) || 0) + 1);
          const top = [...counts.entries()].sort((a, b) => b[1] - a[1]).slice(0, 3).map(x => x[0]);
          groups = top.map((m, i) => [m.replace(/_/g, ' '), c.s[i], r => r.extinction_mode === m]);
          groups.push([top.length ? 'other or not recorded' : 'outcome not recorded', c.neutral, r => !top.includes(r.extinction_mode)]);
        } else {
          groups = PHASES.map(p => [p, App.phaseColor(p), r => r.fuel_phase === p]);
          groups.push(['phase not recorded', c.neutral, r => !PHASES.includes(r.fuel_phase)]);
        }
        const type = pts.length > 1500 ? 'scattergl' : 'scatter';
        const traces = groups.map(([name, color, test]) => {
          const g = pts.filter(test);
          return { type, mode: 'markers', name, x: g.map(r => scale(ax, r[xk])), y: g.map(r => scale(ay, r[yk])), customdata: g.map(r => index.get(r)),
            marker: { color, size: 7, opacity: 0.75, line: { width: 0 } },
            text: g.map(r => `${plain(App.name(r.accession))} ${plain(r.test_id)}<br>${plain(r.fuel || r.fuel_raw || 'fuel not labelled')}<br>${plain(ax.label)}: ${fmtVal(ax, r[xk])}<br>${plain(ay.label)}: ${fmtVal(ay, r[yk])}`),
            hovertemplate: '%{text}<extra></extra>' };
        }).filter(t => t.x.length);
        const axisOpts = axes.map(a => [a.key, a.label]);
        panelKids.push(h('div', { class: 'row' },
          App.select({ id: 'te-x', label: 'x axis', value: xk, options: axisOpts, onChange: v => set({ x: v }) }),
          App.select({ id: 'te-y', label: 'y axis', value: yk, options: axisOpts, onChange: v => set({ y: v }) }),
          App.seg({ id: 'te-color', label: 'Colour by', value: colorBy, options: [['phase', 'Fuel phase'], ['outcome', 'Outcome']], onChange: v => set({ color: v }) }),
          h('span', { class: 'muted small', text: `${pts.length} of ${rows.length} rows have both values. Click a point for the test.` })));
        if (traces.length) {
          App.plot(plotBox, traces, { height: 420, hovermode: 'closest',
            xaxis: { title: axisTitle(ax) }, yaxis: { title: axisTitle(ay) } },
            pt => { const r = all[pt && pt.customdata]; if (r) openTest(r); });
          panelKids.push(plotBox);
        } else panelKids.push(h('p', { class: 'muted', text: 'No row in this selection has both values.' }));
      } else panelKids.push(h('p', { class: 'muted', text: 'Fewer than two numeric columns have data in this selection, so there is nothing to plot.' }));
      root.append(App.panel('Tests on two measured quantities', ...panelKids));

      root.append(App.notes([
        'Ambient O2 (`x_o2_ambient`) is the atmosphere. Burner-stream O2 (`x_o2_burner`, up to 85%) is the oxidiser stream of inverse flames, whose surroundings hold fuel and N2 and no O2. They are separate axes and never merged.',
        '`cool_flame` is true or empty, never false. An empty cell means no cool-flame data, not that there was no cool flame.',
        'Only rows of kind "test" are single tests. Test days, condition sets and planned (not flown) rows are hidden unless included.',
        'A flag badge marks a correction or a doubt. The original NASA value is kept; open the row to see it with its evidence.',
      ], 'Read before comparing'));

      const showBurner = rows.some(r => num(r.x_o2_burner));
      const cols = [
        { key: 'acronym', label: 'Investigation', fmt: (v, r) => v || r.accession },
        { key: 'test_id', label: 'Test', fmt: v => h('span', { class: 'mono', text: v || '–' }) },
        state.allKinds && { key: 'row_kind', label: 'Kind', fmt: v => (v || 'test') === 'test' ? 'test' : App.chip(String(v).replace(/_/g, ' '), 'warn') },
        { key: 'fuel', label: 'Fuel', fmt: (v, r) => v || r.fuel_raw || '–' },
        { key: 'fuel_phase', label: 'Phase' },
        { key: 'config', label: 'Config' },
        { key: 'x_o2_ambient', label: 'Ambient O2', num: true, fmt: v => App.pct(v) },
        showBurner && { key: 'x_o2_burner', label: 'Burner-stream O2', num: true, fmt: v => App.pct(v) },
        { key: 'pressure_kpa', label: 'kPa', num: true, fmt: v => App.fmt(v, 1) },
        { key: 'flow_cm_s', label: 'Flow cm/s', num: true },
        { key: 'burn_time_s', label: 'Burn s', num: true },
        { key: 'extinction_mode', label: 'Outcome', fmt: v => v ? String(v).replace(/_/g, ' ') : '–' },
        { key: '_nflags', label: 'Flags', num: true, fmt: (v, r) => v ? App.chip(`${v} flag${v > 1 ? 's' : ''}`, 'warn') : '' },
      ].filter(Boolean);
      const tableRows = rows.map(r => Object.assign({}, r, { _nflags: flagList(r).length, _row: r }));
      root.append(App.table({ cols, rows: tableRows, pageSize: 25, onRow: r => openTest(r._row) }));
    },
  });
})();
