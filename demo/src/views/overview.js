App.view({
  id: 'overview', title: 'Overview', tier: 1,
  heading: 'What is in the data',
  intro: 'Twenty-four NASA PSI microgravity combustion investigations, read and digested for fire safety. Start with the key messages, then open any investigation.',
  needs: [],
  brief: {
    need: 'A landing page that says how much evidence exists, what it concludes, and lets a scientist reach any investigation in two clicks by pillar, fuel phase, platform or keyword.',
    data: ['data/export/investigations.json: the 24 cards with counts', 'data/export/synthesis.json: key_messages with confidence and citations', 'data/export/discrepancies.json: raw_data_conflicts and rows_flagged', 'data/export/records.json for the equation count (lazy)'],
    call: 'search_investigations(query="soot", pillar="detection", fuel_phase="gas", flight=True)\ninsights(topic="key_messages")',
    keep: ['The confidence label on every key message', 'Citation ids such as [PSI-26 F3] that open the record and its quoted source', 'Quotes from PSI files are machine-checked against the files; external quotes are not independently checked', 'The number of test rows flagged or corrected because the PSI tables contain errors', 'Five investigations are ground-based or have no tests table: zero rows is not zero evidence'],
  },
  render(root, state, update) {
    const invs = FIF.investigations || [];
    const syn = FIF.synthesis || {};
    const disc = FIF.discrepancies || {};
    const sum = key => invs.reduce((a, i) => a + (typeof i[key] === 'number' ? i[key] : 0), 0);
    const countEq = () => Object.values(FIF.records || {}).reduce((a, r) => a + (((r || {}).physics || {}).equations || []).length, 0);

    const eqVal = h('b', { text: FIF.records ? String(countEq()) : '…' });
    if (!FIF.records) App.load(['records']).then(() => { eqVal.textContent = String(countEq()); }).catch(() => { eqVal.textContent = '–'; });
    const nFlight = invs.filter(i => i.flight).length;
    const conflicts = (disc.raw_data_conflicts || []).length;
    const tile = (val, label) => h('div', { class: 'tile' }, val instanceof Node ? val : h('b', { text: String(val) }), h('span', { text: label }));
    root.append(h('div', { class: 'grid tiles' },
      tile(invs.length, `investigations (${nFlight} flown, ${invs.length - nFlight} ground or analysis)`),
      tile(sum('n_test_rows'), 'rows in the tests table'),
      tile(sum('n_findings'), 'findings, each with quoted sources'),
      tile(eqVal, 'equations with their meaning'),
      tile(conflicts, 'conflicts between PSI tables and raw files'),
      tile(disc.rows_flagged ?? '–', `test rows flagged or corrected${disc.rows_total ? ' of ' + disc.rows_total : ''}`)));

    const msgs = syn.key_messages || [];
    if (msgs.length) {
      root.append(App.panel(`${msgs.length} key messages across the investigations`,
        h('p', { class: 'muted small', text: 'Each message cites the findings behind it. Click a citation to see the quoted source.' }),
        h('ol', { class: 'stack', style: 'margin:0;padding-left:22px' }, msgs.map(m => h('li', {},
          h('div', { class: 'stack', style: 'gap:4px' },
            h('p', {}, App.tex(m.text)),
            h('div', { class: 'chips' }, App.confidence(m.confidence), App.cites(m.citations || []))))))));
    }

    const pillar = state.pillar || '', phase = state.phase || '', where = state.where || 'all', q = (state.q || '').trim().toLowerCase();
    const phases = [...new Set(invs.flatMap(i => i.fuel_phases || []))].sort();
    const shown = invs.filter(i =>
      (!pillar || (i.pillars || []).includes(pillar)) &&
      (!phase || (i.fuel_phases || []).includes(phase)) &&
      (where === 'all' || (where === 'flight') === !!i.flight) &&
      (!q || [i.accession, i.acronym, i.title, i.one_line].some(s => s && String(s).toLowerCase().includes(q))));

    root.append(h('div', { class: 'row' },
      App.seg({ id: 'ov-pillar', label: 'Pillar', options: ['', 'prevention', 'detection', 'suppression', 'fundamental'], value: pillar, onChange: v => update({ pillar: v }) }),
      App.select({ id: 'ov-phase', label: 'Fuel phase', options: ['', ...phases], value: phase, onChange: v => update({ phase: v }) }),
      App.seg({ id: 'ov-where', label: 'Platform', options: [['all', 'All'], ['flight', 'Flight'], ['ground', 'Ground or analysis']], value: where, onChange: v => update({ where: v }) }),
      App.search({ id: 'ov-q', label: 'Search title and description', value: state.q, placeholder: 'e.g. soot, droplet, PMMA', onChange: v => update({ q: v }) }),
      h('span', { class: 'muted small', text: `${shown.length} of ${invs.length} investigations` })));

    const label = i => i.acronym || i.accession;
    const withRows = shown.filter(i => i.n_test_rows > 0).sort((a, b) => b.n_test_rows - a.n_test_rows);
    const noRows = shown.filter(i => !(i.n_test_rows > 0));
    if (withRows.length) {
      const firstPhase = i => (i.fuel_phases || [])[0] || 'unknown';
      const usedPhases = [...new Set(withRows.map(firstPhase))];
      const traces = usedPhases.map(p => {
        const sel = withRows.filter(i => firstPhase(i) === p);
        return { type: 'bar', orientation: 'h', name: p, y: sel.map(label), x: sel.map(i => i.n_test_rows),
          customdata: sel.map(i => [i.accession, (i.fuel_phases || []).join(', '), i.n_findings]),
          marker: { color: App.phaseColor(p) },
          hovertemplate: '%{y} (%{customdata[0]})<br>%{x} test rows<br>fuel phase: %{customdata[1]}<br>%{customdata[2]} findings<extra></extra>' };
      });
      const plot = h('div', {});
      App.plot(plot, traces, { barmode: 'stack', height: 70 + withRows.length * 24, margin: { l: 150, r: 24, t: 8, b: 44 },
        xaxis: { title: 'rows in the tests table (log scale)', type: 'log' },
        yaxis: { categoryorder: 'array', categoryarray: withRows.map(label), autorange: 'reversed' },
        legend: { orientation: 'h', y: 1.02, yanchor: 'bottom', x: 0 } },
        pt => { const acc = pt && pt.customdata && pt.customdata[0]; if (acc) App.go('investigation', { accession: acc }); });
      root.append(App.panel('How many tests each investigation logged', plot,
        h('p', { class: 'muted small' }, 'Colour is the fuel phase (the first one listed). Click a bar to open the record.',
          noRows.length ? ` No tests table: ${noRows.map(i => App.name(i.accession)).join(', ')}.` : '')));
    }

    root.append(h('div', { class: 'grid' }, shown.map(i => {
      const open = () => App.go('investigation', { accession: i.accession });
      return h('article', { class: 'card', tabindex: '0', role: 'button', 'aria-label': 'Open ' + App.name(i.accession), onclick: open,
        onkeydown: e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } } },
        h('div', { class: 'row', style: 'justify-content:space-between;align-items:baseline;gap:6px' },
          h('h4', { text: label(i) }), h('span', { class: 'mono muted', text: i.accession })),
        h('p', { class: 'small', style: 'font-weight:500', text: i.title || '' }),
        i.one_line && h('p', { class: 'small muted', text: i.one_line }),
        h('div', { class: 'chips' }, (i.pillars || []).map(App.pillar), (i.fuel_phases || []).map(App.phase), App.chip(i.flight ? 'flight' : 'ground or analysis')),
        h('p', { class: 'small num' }, `${App.fmt(i.n_test_rows)} test rows · ${App.fmt(i.n_findings)} findings`));
    })));
    if (!shown.length) root.append(h('p', { class: 'muted', text: 'No investigation matches these filters.' }));

    root.append(App.notes([
      `Counts of test rows come from the PSI tables after cleaning. ${invs.filter(i => !(i.n_test_rows > 0)).length} investigations have no tests table, so their evidence is in findings only.`,
      'Quotes from PSI files are machine-checked against the files. External quotes (papers, URLs) are not independently checked.',
      `${disc.rows_flagged ?? '?'} test rows carry a correction or doubt flag; ${conflicts} conflicts between the PSI tables and the raw files are listed with their evidence.`,
    ]));
  },
});
