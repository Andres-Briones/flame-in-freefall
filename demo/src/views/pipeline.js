App.view({
  id: 'pipeline', title: 'How it works', tier: 3,
  heading: 'From NASA files to an answer on screen',
  intro: 'What happens between the NASA archive and this dashboard, step by step: what is read, what is computed, where AI was used, and how every number stays traceable to its source.',
  needs: [],
  render(root) {
    const inv = FIF.investigations, d = FIF.discrepancies;
    const findings = inv.reduce((a, i) => a + (i.n_findings || 0), 0);
    const n = x => Number(x).toLocaleString('en-US');
    const steps = [
      ['1', 'Download from NASA PSI', `The ${inv.length} combustion investigations of NASA's Physical Sciences Informatics archive: reports, test logs, spreadsheets and sensor recordings (about 16,400 files listed; images and videos are not copied, they are streamed from NASA when you open them).`,
        'scripts/fetch_psi.py, fetch_psi_files.py → files table', 'files'],
      ['2', 'One table of tests', `Each investigation logs its experiments in its own layout. They are read into one table with the same columns for all: ${n(d.rows_total)} rows with fuel, oxygen, pressure, flow, gravity level, and how the flame ended. Units are converted; nothing is guessed silently.`,
        'build_tests → tests table', 'tests'],
      ['3', 'Errors in the source stay visible', `Where a NASA table contradicts the raw sensor data or its own documents, the value is not quietly fixed: a recorded patch says what was there, what replaces it and why (${d.raw_data_conflicts.length} conflicts). ${n(d.rows_flagged)} rows carry a flag that explains a doubt.`,
        'data/corrections/ → discrepancies', 'quality'],
      ['4', 'Text of every document, by page', 'PDFs, slides, Word and Excel files are cut into about 21,600 passages, each remembering its file and page, so a quote can always be reopened at the right page. Postal addresses, private contact details and credentials are removed at this step.',
        'build_evidence, redact → evidence table', 'search'],
      ['5', 'Sensor traces reduced to features', 'For 1,051 recorded tests the raw time series (temperatures, pressure, flows, radiometers) are summarised into numbers such as ignition time, burn duration and peak temperature. The full trace is fetched from NASA when you plot it.',
        'build_timeseries → features table', 'traces'],
      ['6', 'A reviewed knowledge record per investigation', `AI agents read the documents of each investigation and wrote a structured record: goals, method, findings, equations, limits. Each of the ${findings} findings carries a verbatim quote, and a program checks that every quote really is in the cited file.`,
        'data/digest/, check_digest', 'investigation'],
      ['7', 'Synthesis across investigations', 'The records are compared to extract what matters for fire safety: measured flammability limits, microgravity against normal gravity, ranked knowledge gaps, and a relevance score of each investigation for a mission scenario.',
        'synthesis, relevance', 'insights'],
      ['8', 'Small models', 'Four small predictive models are fitted on the tests table (for example: will this flame go out by itself?). Each score is shown with the range it takes when test days are resampled, and the models refuse conditions that were never tested.',
        'build_models → models', 'models'],
      ['9', '11 functions answer every question', 'All of the above is reached through 11 functions (search, filter tests, find evidence, relevance, predict, data quality and others). Each returns the same four parts: data, a chart hint, the sources, and notes with the caveats.',
        'fif/api.py', 'ask'],
      ['10', 'Dashboard and AI assistants use the same functions', 'This page calls those functions on the server; an AI assistant calls exactly the same ones. So a person and an assistant get the same numbers, sources and caveats.',
        'demo/server.py', 'ai'],
    ];
    const has = id => App.views.some(v => v.id === id);
    root.append(App.panel('The ten steps', h('div', { class: 'stack' }, steps.map(([num, title, text, where, view]) =>
      h('div', { style: 'display:grid;grid-template-columns:32px 1fr;gap:10px;align-items:start' },
        h('b', { style: 'font-size:18px;color:var(--accent);text-align:right', text: num }),
        h('div', {},
          h('h4', { style: 'margin:0 0 2px', text: title }),
          h('p', { class: 'prose', style: 'margin:0 0 4px', text }),
          h('p', { class: 'small muted', style: 'margin:0' }, h('span', { class: 'mono', text: where }),
            has(view) ? [' · ', h('a', { href: '#' + view, text: 'see it in ' + App.views.find(v => v.id === view).title })] : null)))))));

    root.append(App.panel('What an answer looks like',
      h('p', { class: 'prose', text: 'Whatever is asked, by a click here or by an assistant, the reply has the same four parts:' }),
      h('table', {}, h('tbody', {}, [
        ['data', 'The rows or numbers that answer the question.'],
        ['chart', 'A suggestion of how to plot them (the dashboard draws it; an assistant may ignore it).'],
        ['sources', 'The NASA file, page and quote, or the table row, behind each statement.'],
        ['notes', 'Caveats: doubts about the source, extrapolations, what was not measured.'],
      ].map(([k, v]) => h('tr', {}, h('td', { class: 'mono', text: k }), h('td', { text: v })))))));

    root.append(App.panel('Where AI was used, and where not',
      App.notes([
        'AI read the documents and wrote the knowledge records and the synthesis (steps 6 and 7). Quotes from NASA files are machine-checked against the extracted text; quotes from external publications are not.',
        'Tables, sensor features, patches and models (steps 2 to 5 and 8) are ordinary programs: the same input always gives the same output, and a full rebuild from the raw files was verified to be identical.',
        'No experiment in the archive was run in Moon or Mars gravity, and no solid was burned in an exploration atmosphere. Statements about those cases are extrapolations and are labelled as such.',
        'Nothing from NASA is stored on this server except the generated tables; documents, videos and raw recordings are opened from NASA storage.'])));
  },
});
