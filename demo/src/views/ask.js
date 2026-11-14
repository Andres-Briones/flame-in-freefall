App.view({
  id: 'ask', title: 'Ask the data', tier: 3,
  heading: 'What an AI assistant can answer from these data',
  intro: 'The 33 questions of the question bank. Each one shows the tool call an assistant would make, the answer it gets today and the view that draws it. Answers here are pre-computed: no model runs in this demo.',
  needs: [],
  brief: {
    need: 'An assistant that answers by calling the data functions, shows which call it made, cites the sources and repeats the caveats. It must not answer from its own memory.',
    data: ['data/export/questions.json: question, call, chart suggestion, answer', 'data/processed/tools.json: the 11 tool specs to give the model'],
    call: 'fif.tools.call(name, arguments)  # routes a tool call to fif.api',
    keep: ['The call behind each answer, so a scientist can check it', 'Sources returned by the function, shown as citations', 'The notes returned by the function, repeated in the answer', 'find_evidence is keyword search, not semantic search; raw document passages are unreviewed'],
    backend: 'A live assistant needs a server (or serverless function) holding the API key and running fif.api. The question bank is the test set for it: tests/test_questions.py runs every call.',
  },
  render(root, state, update) {
    const Q = FIF.questions;
    const themes = [...new Set(Q.map(q => q.theme))];
    const theme = state.theme || '';
    const term = (state.q || '').toLowerCase();
    const rows = Q.map((q, i) => ({ ...q, n: i + 1 })).filter(q => (!theme || q.theme === theme) && (!term || (q.question + ' ' + q.answer).toLowerCase().includes(term)));
    const sel = state.n ? Q[state.n - 1] : null;
    const target = q => {
      const a = q.arguments || {};
      const acc = Array.isArray(a.accession) ? a.accession[0] : a.accession;
      switch (q.function) {
        case 'relevance': return ['scenario', { scenario: a.scenario, phase: a.fuel_phase || 'solid', pillar: a.pillar || 'any' }, 'Scenario lens'];
        case 'coverage': return ['coverage', { phase: a.fuel_phase || 'all', cell: null }, 'Coverage map'];
        case 'filter_tests': return ['tests', { accession: acc || '', phase: a.fuel_phase || '', q: '' }, 'Test explorer'];
        case 'insights': return ['insights', { tab: { micro_vs_1g: 'micro', limits: 'limits', gaps: 'gaps', research_questions: 'questions', lineage: 'lineage', parameter_coverage: 'ranges' }[a.topic] || 'gaps' }, 'Insights'];
        case 'discrepancies': return ['quality', { accession: acc || '' }, 'Data quality'];
        case 'predict': return ['models', { model: a.model_id }, 'Models'];
        case 'timeseries': return ['traces', {}, 'Sensor traces'];
        case 'find_evidence': return ['search', { q: a.query || '', accession: acc || '', error: null }, 'Document search'];
        case 'get_investigation': case 'compare': case 'search_investigations':
          return acc ? ['investigation', { accession: acc }, 'Investigation record'] : ['overview', {}, 'Overview'];
        default: return null;
      }
    };
    const later = patch => { if (App.current && App.current.id === 'ask') update(patch); else Object.assign(state, patch); };
    const runLive = q => {
      const my = (state._seq || 0) + 1;
      state._seq = my;
      update({ liveN: state.n, live: null, liveError: null, liveLoading: true });
      App.api(q.function, q.arguments || {})
        .then(r => { if (state._seq === my) later({ liveLoading: false, live: r }); })
        .catch(e => { if (state._seq === my) later({ liveLoading: false, liveError: (e && e.message) || String(e) }); });
    };
    const describe = d => {
      if (Array.isArray(d)) return `${d.length} rows`;
      if (d && typeof d === 'object') return Object.entries(d).map(([k, v]) => `${k}: ${Array.isArray(v) ? v.length + ' items' : v && typeof v === 'object' ? Object.keys(v).length + ' fields' : 'value'}`).join(', ');
      return d == null ? 'no data' : 'one value';
    };
    const srcText = s => s && typeof s === 'object' ? [s.ref, s.accession && !s.ref ? s.accession : null, s.file, s.locator, s.page, s.url, s.table].filter(Boolean).join(' · ') || JSON.stringify(s) : String(s);
    const livePane = () => {
      if (state.liveN !== state.n) return null;
      if (state.liveLoading) return h('p', { class: 'muted', id: 'ask-live-loading', text: 'Calling the function on the server…' });
      if (state.liveError) return App.notes([state.liveError], 'The live call failed');
      const r = state.live;
      if (!r || typeof r !== 'object') return null;
      let json = '';
      try { json = JSON.stringify(r.data, null, 1) || ''; } catch (e) { json = String(r.data); }
      const srcs = Array.isArray(r.sources) ? r.sources : [];
      return h('div', { class: 'stack', style: 'gap:8px', id: 'ask-live' },
        h('div', { class: 'row' }, App.chip('live from the server', 'good'),
          h('span', { class: 'small num', text: `${describe(r.data)}; ${(json.length / 1024).toFixed(1)} KB of JSON; ${srcs.length} sources.` })),
        srcs.length ? h('div', { class: 'small' }, h('div', { class: 'small muted', text: 'First sources' }),
          h('ul', { style: 'margin:0;padding-left:18px' }, srcs.slice(0, 5).map(s => h('li', { class: 'mono', text: srcText(s) })))) : null,
        App.notes(Array.isArray(r.notes) ? r.notes : [], 'Notes returned by the function'),
        h('details', {}, h('summary', { text: 'The returned data' }),
          h('pre', { style: 'max-height:320px;overflow:auto', text: json.length > 3000 ? json.slice(0, 3000) + `\n… (${json.length - 3000} more characters)` : json })));
    };
    const call = q => `${q.function}(${Object.entries(q.arguments || {}).map(([k, v]) => `${k}=${JSON.stringify(v)}`).join(', ')})`;

    root.append(h('div', { class: 'row' },
      App.select({ id: 'ask-theme', label: 'Theme', options: [['', 'All themes'], ...themes.map(t => [t, t])], value: theme, onChange: v => update({ theme: v, n: null }) }),
      App.search({ id: 'ask-q', label: 'Search questions and answers', value: state.q, onChange: v => update({ q: v, n: null }), placeholder: 'cool flame, smoke, CO2…' }),
      h('span', { class: 'muted small', text: `${rows.length} of ${Q.length} questions` })));

    const list = h('div', { class: 'stack', style: 'gap:6px' }, rows.map(q =>
      h('button', { class: 'card', type: 'button', style: sel && sel === Q[q.n - 1] ? 'border-color:var(--accent)' : null, onclick: () => update({ n: q.n }) },
        h('div', { class: 'small muted', text: `${q.n}. ${q.theme}` }), h('div', { text: q.question }))));

    const pane = h('div', { class: 'panel', style: 'position:sticky;top:96px;align-self:start' });
    if (!sel) pane.append(h('h3', { text: 'Pick a question' }), h('p', { class: 'muted', text: 'The answer, the call behind it and the chart to draw appear here.' }));
    else {
      const t = target(sel);
      pane.append(
        h('h3', { text: sel.question }),
        h('div', {}, h('div', { class: 'small muted', text: 'The assistant calls' }), h('pre', { text: call(sel) })),
        h('div', {}, h('div', { class: 'small muted', text: 'Answer today' }), h('p', {}, App.tex(sel.answer))),
        h('div', {}, h('div', { class: 'small muted', text: 'Chart to draw' }), h('p', { text: sel.chart || 'none' })),
        h('div', { class: 'row' },
          t && h('button', { class: 'btn primary', type: 'button', onclick: () => App.go(t[0], t[1]) }, `Open in ${t[2]}`),
          App.backend && h('button', { class: 'btn', type: 'button', id: 'ask-run-live', disabled: !!(state.liveLoading && state.liveN === state.n), onclick: () => runLive(sel) }, 'Run it live')),
        App.backend ? livePane() : null,
        App.notes([App.backend
          ? 'The answer above is pre-computed. "Run it live" makes the same call on the server; the real dashboard lets the model make it and must cite the sources and repeat the notes the function returns.'
          : 'Pre-computed on the current tables. In the real dashboard the model makes this call live and must cite the sources and repeat the notes the function returns.'], 'Demo limit'));
    }
    root.append(h('div', { class: 'grid two' }, list, pane));
  },
});
