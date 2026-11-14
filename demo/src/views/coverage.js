App.view({
  id: 'coverage', title: 'Coverage map', tier: 1,
  heading: 'Where do data exist, and where is nothing?',
  intro: 'Number of tests in each cell of ambient oxygen against pressure. The marked atmospheres are the ones exploration missions plan to use. Empty cells are the knowledge gaps.',
  needs: ['tests'],
  brief: {
    need: 'A map of test counts on physical axes with the mission atmospheres overlaid, so the gaps are seen at once. Clicking a cell must list the real tests behind it.',
    data: ['data/export/coverage.json: cells and reference atmospheres for all fuels and per phase', 'data/export/tests.json for the tests in a cell'],
    call: 'coverage(x="x_o2_ambient", y="pressure_kpa", fuel_phase="solid")',
    keep: ['How many rows are not on the map because O2 or pressure was not recorded', 'Rows placed from an investigation-level range, not a per-test value', 'x_o2_burner (inverse flames, up to 0.85) is an oxidiser stream and must never be drawn on the ambient O2 axis'],
    backend: 'Other axis pairs (flow, fuel, gravity) are computed by coverage(x, y); only O2 against pressure is pre-computed.',
  },
  render(root, state, update) {
    const c = App.colors();
    const phase = state.phase || 'all';
    const cov = FIF.coverage[phase], cells = cov.data.cells, refs = cov.data.references;
    root.append(h('div', { class: 'row' },
      App.seg({ id: 'cov-phase', label: 'Fuel phase', options: [['all', 'All fuels'], 'solid', 'liquid', 'gas'], value: phase, onChange: v => update({ phase: v, cell: null }) }),
      h('span', { class: 'muted small', text: `${cov.data.n_on_map} tests on the map` })));

    const maxN = Math.max(...cells.map(k => k.n));
    const mix = t => { // sequential single hue, log scale because counts span 1 to several hundred
      const a = c.seqLo.match(/\w\w/g).map(x => parseInt(x, 16)), b = c.seqHi.match(/\w\w/g).map(x => parseInt(x, 16));
      return 'rgb(' + a.map((v, i) => Math.round(v + (b[i] - v) * t)).join(',') + ')';
    };
    const shapes = cells.map(k => ({ type: 'rect', x0: k.x_min * 100, x1: k.x_max * 100, y0: k.y_min, y1: k.y_max, layer: 'below',
      fillcolor: mix(maxN > 1 ? Math.log(k.n) / Math.log(maxN) : 1), line: { color: c.surface, width: 2 } }));
    const hover = { type: 'scatter', mode: 'markers', name: 'tests in cell', showlegend: false,
      x: cells.map(k => (k.x_min + k.x_max) * 50), y: cells.map(k => (k.y_min + k.y_max) / 2),
      marker: { size: 18, color: 'rgba(0,0,0,0)' }, customdata: cells.map((k, i) => i),
      text: cells.map(k => `${k.n} tests<br>O2 ${(k.x_min * 100).toFixed(0)}-${(k.x_max * 100).toFixed(0)}%, ${k.y_min}-${k.y_max} kPa<br>${Object.entries(k.by_phase).map(([p, n]) => `${p} ${n}`).join(', ')}<br>${k.accessions.map(a => App.inv(a).acronym).join(', ')}`),
      hovertemplate: '%{text}<extra></extra>' };
    const refTrace = { type: 'scatter', mode: 'markers+text', name: 'reference atmospheres', showlegend: false,
      x: refs.map(r => r.x_o2 * 100), y: refs.map(r => r.pressure_kpa),
      text: refs.map(r => r.label.replace(/\s*\(.*/, '')), textposition: refs.map(r => r.x_o2 > 0.6 ? 'middle left' : 'top right'), textfont: { color: c.fg, size: 11 },
      marker: { symbol: 'diamond-open', size: 13, color: c.crit, line: { width: 2.5, color: c.crit } },
      customdata: refs.map(r => r.n_tests_in_cell), hovertemplate: '%{text}<br>%{x:.0f}% O2, %{y:.1f} kPa<br>%{customdata} tests in this cell<extra></extra>' };
    const plot = h('div', {});
    App.plot(plot, [hover, refTrace], { height: 460, shapes, hovermode: 'closest',
      xaxis: { title: 'ambient oxygen (mole %)', range: [8, 104] }, yaxis: { title: 'pressure (kPa)', rangemode: 'tozero' } },
      pt => { if (pt.data.name === 'tests in cell') update({ cell: pt.customdata }); });
    root.append(App.panel('Tests per cell', plot,
      h('div', { class: 'legend' }, h('span', {}, 'fewer', h('span', { style: `display:inline-block;width:120px;height:10px;border-radius:3px;background:linear-gradient(90deg, ${c.seqLo}, ${c.seqHi})` }), `more (max ${maxN}, log scale)`),
        h('span', {}, h('span', { style: `color:${c.crit};font-size:14px` }, '◇'), 'reference atmosphere'), h('span', { class: 'muted' }, 'Click a cell to list its tests.'))));

    root.append(App.table({ pageSize: 10, rows: refs, cols: [
      { key: 'label', label: 'Reference atmosphere' },
      { key: 'x_o2', label: 'O2', num: true, fmt: v => App.pct(v, 0) },
      { key: 'pressure_kpa', label: 'kPa', num: true, fmt: v => App.fmt(v, 1) },
      { key: 'n_tests_in_cell', label: phase === 'all' ? 'Tests in its cell' : `${phase} tests in its cell`, num: true, fmt: v => v ? String(v) : h('span', { class: 'chip crit' }, 'none') },
      { key: 'nearest_test', label: 'Nearest test', sortable: false, fmt: t => t ? `${App.inv(t.accession).acronym} ${t.test_id}: ${t.fuel} (${t.fuel_phase}), ${App.pct(t.x_o2_ambient)} O2, ${App.fmt(t.pressure_kpa, 0)} kPa${(t.not_measured || []).length ? ` (${t.not_measured.map(c => c === 'x_o2_ambient' ? 'O2' : 'pressure').join(' and ')} not measured for this test: middle of the investigation's stated range)` : ''}` : '–' } ] }));

    if (state.cell != null && cells[state.cell]) {
      const k = cells[state.cell];
      const inCell = FIF.tests.filter(t => (t.row_kind || 'test') === 'test' && (phase === 'all' || t.fuel_phase === phase) &&
        t.x_o2_ambient >= k.x_min && t.x_o2_ambient < k.x_max && t.pressure_kpa >= k.y_min && t.pressure_kpa < k.y_max);
      root.append(App.panel(`Tests at ${(k.x_min * 100).toFixed(0)}-${(k.x_max * 100).toFixed(0)}% O2 and ${k.y_min}-${k.y_max} kPa`,
        h('p', { class: 'muted small', text: `${inCell.length} rows carry their own per-test O2 and pressure; the cell counts ${k.n} because some rows are placed from their investigation's stated range.` }),
        App.table({ pageSize: 10, rows: inCell, onRow: t => App.go('tests', { accession: t.accession, q: t.test_id }), cols: [
          { key: 'acronym', label: 'Investigation' }, { key: 'test_id', label: 'Test' }, { key: 'fuel', label: 'Fuel' }, { key: 'fuel_phase', label: 'Phase' },
          { key: 'x_o2_ambient', label: 'O2', num: true, fmt: v => App.pct(v) }, { key: 'pressure_kpa', label: 'kPa', num: true, fmt: v => App.fmt(v, 1) },
          { key: 'flow_cm_s', label: 'Flow cm/s', num: true }, { key: 'extinction_mode', label: 'Outcome', fmt: (v, t) => (v || t.outcome || '–').replace(/_/g, ' ') } ] })));
    }
    root.append(App.notes(cov.notes));
  },
});
