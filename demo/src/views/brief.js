App.view({
  id: 'brief', title: 'Brief', tier: 3,
  heading: 'What the science side needs from the dashboard',
  intro: 'The requirements behind every view of this demo, in one place. Each row names the data file to load, the function that answers it and the caveats that must stay on screen.',
  needs: [],
  render(root) {
    const inv = FIF.investigations, d = FIF.discrepancies, s = FIF.synthesis;
    const tests = inv.reduce((a, i) => a + (i.n_test_rows || 0), 0), findings = inv.reduce((a, i) => a + (i.n_findings || 0), 0);
    root.append(App.panel('What the data contain',
      h('div', { class: 'grid tiles' },
        [[inv.length, 'investigations, one knowledge record each'], [tests, 'test rows on one common schema'], [findings, 'findings with quoted sources'],
         [s.limits.length, 'measured flammability limits'], [s.micro_vs_1g.length, 'microgravity vs 1 g comparisons'], [s.gaps.length, 'ranked knowledge gaps'],
         [8, 'small models (4 predictive)'], [d.raw_data_conflicts.length, 'conflicts found in NASA tables'], [FIF.questions.length, 'tested questions for the assistant']]
          .map(([n, l]) => h('div', { class: 'tile' }, h('b', { text: String(n) }), h('span', { text: l })))),
      h('p', { class: 'muted small', text: 'Everything is pre-computed in data/export/ (JSON, about 14 MB) for a front end without a backend. The same answers come live from 11 Python functions in fif/api.py, each returning {data, chart, sources, notes}.' })));

    root.append(App.panel('Five rules for every screen', h('ol', { class: 'prose', style: 'margin:0;padding-left:20px' },
      [['Every number links to its source.', 'A citation chip opens the PSI file, page and verbatim quote, or the external reference.'],
       ['Caveats travel with the answer.', 'The notes a function returns are shown next to its chart, never hidden behind a click.'],
       ['Extrapolation is labelled.', 'No test was run in partial gravity and no solid burned in an exploration atmosphere. The distance to the nearest real test is always stated.'],
       ['Errors in the NASA tables stay visible.', 'Flagged rows carry a badge that opens the evidence. The original value is kept.'],
       ['Scores are decomposed.', 'The relevance score shows its components and weights so that it can be argued with.']]
        .map(([a, b]) => h('li', {}, h('b', { text: a + ' ' }), b)))));

    const views = App.views.filter(v => v.brief);
    root.append(h('h2', { text: 'Feature by feature' }));
    root.append(h('div', { class: 'table-wrap' }, h('table', { class: 't' },
      h('thead', {}, h('tr', {}, ['Feature', 'What scientists need', 'Data and function', 'Must stay visible', 'Needs a backend'].map(t => h('th', { text: t })))),
      h('tbody', {}, views.map(v => { const b = v.brief; return h('tr', {},
        h('td', {}, h('a', { href: '#' + v.id }, v.title)),
        h('td', { style: 'min-width:220px' }, b.need || ''),
        h('td', { style: 'min-width:240px' }, (b.data || []).map(x => h('div', { class: 'small', text: x })), b.call && h('pre', { style: 'margin-top:6px', text: b.call })),
        h('td', { style: 'min-width:240px' }, h('ul', { style: 'margin:0;padding-left:16px' }, (b.keep || []).map(x => h('li', { text: x })))),
        h('td', { style: 'min-width:180px' }, b.backend || h('span', { class: 'muted', text: 'no' }))); })))));

    root.append(App.panel('Not in this demo, and why',
      h('ul', { class: 'prose', style: 'margin:0;padding-left:20px' }, [
        'Free scenario sliders: relevance() takes any O2, pressure, flow and gravity, but the static export holds 5 presets.',
        'Sensor traces of any test: timeseries() reads the raw files (7.5 GB). Two examples and 1,051 per-recording summaries are exported.',
        'A live assistant: needs a server for the API key. The tool specs (data/processed/tools.json) and the question bank are ready.',
        'Full-text search of the documents: find_evidence() searches 22,879 passages by keyword; the evidence table is too large for a static page.',
        'Images and video: the 7.8 TB of PSI imagery were not downloaded. The records say which files exist and what could be measured from them.',
      ].map(t => h('li', { text: t })))));
  },
});
