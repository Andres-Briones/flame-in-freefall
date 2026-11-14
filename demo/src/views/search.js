(function () {
  const EXAMPLES = ['partial gravity', 'cool flame reignition', 'smoke detector alarm'];
  const LETTER_SECTION = { F: 'findings', L: 'limitations', Q: 'open_questions' };
  const KIND_LABEL = { finding: 'finding', limitation: 'limitation', open_question: 'open question', summary: 'summary' };
  const STATIC_LIMIT = 60;
  let seq = 0;

  // "[PSI-69 F4]" -> {accession, section, index}; "[PSI-101]" -> the record summary.
  function parseRef(ref, accession) {
    const m = String(ref || '').match(/^\[?(PSI-\d+)(?:\s+([FLQ])(\d+))?\]?$/);
    if (!m) return accession ? { accession, section: 'summary' } : null;
    return m[2] ? { accession: m[1], section: LETTER_SECTION[m[2]], index: +m[3] } : { accession: m[1], section: 'summary' };
  }
  const pageOf = locator => { const m = String(locator || '').match(/^p\.?\s*(\d+)$/i); return m ? +m[1] : null; };

  // Reviewed findings, limitations and open questions that contain every word of the query.
  function staticSearch(q, accession) {
    const words = String(q || '').toLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) return [];
    const out = [];
    const hit = t => { const s = String(t || '').toLowerCase(); return words.every(w => s.includes(w)); };
    for (const [acc, rec] of Object.entries(FIF.records || {})) {
      if (accession && acc !== accession) continue;
      (Array.isArray(rec.findings) ? rec.findings : []).forEach((f, i) => {
        if (f && hit(f.claim)) out.push({ accession: acc, kind: 'finding', text: f.claim, confidence: f.confidence, cite: { accession: acc, section: 'findings', index: i + 1 } });
      });
      (Array.isArray(rec.limitations) ? rec.limitations : []).forEach((l, i) => {
        const t = typeof l === 'string' ? l : l && l.text;
        if (hit(t)) out.push({ accession: acc, kind: 'limitation', text: t, cite: { accession: acc, section: 'limitations', index: i + 1 } });
      });
      (Array.isArray(rec.open_questions) ? rec.open_questions : []).forEach((x, i) => {
        const t = typeof x === 'string' ? x : x && x.text;
        if (hit(t)) out.push({ accession: acc, kind: 'open_question', text: t, cite: { accession: acc, section: 'open_questions', index: i + 1 } });
      });
    }
    return out;
  }

  function digestCard(p) {
    const cite = p.cite || parseRef(p.ref, p.accession);
    return h('div', { class: 'card stack', style: 'gap:6px' },
      h('div', { class: 'chips' },
        h('span', { class: 'small muted', text: App.name(p.accession) }),
        App.chip(KIND_LABEL[p.kind] || String(p.kind || 'passage').replace(/_/g, ' ')),
        cite && App.cite(cite),
        App.confidence(p.confidence)),
      h('p', { style: 'margin:0' }, App.tex(p.text || '')));
  }

  function documentCard(p) {
    const file = p.file_name || p.file || '';
    const page = pageOf(p.locator);
    return h('div', { class: 'card stack', style: 'gap:6px' },
      h('div', { class: 'chips' },
        h('span', { class: 'small muted', text: App.name(p.accession) }),
        App.chip('unreviewed raw text', 'warn'),
        p.transcribed ? App.chip('AI reading of a scan', 'warn') : null,
        h('span', { class: 'small mono', text: file }),
        p.locator ? h('span', { class: 'small muted', text: String(p.locator) }) : null),
      h('p', { class: 'small', style: 'margin:0;white-space:pre-wrap', text: String(p.text || '') }),
      file && p.accession ? h('div', {}, h('button', { class: 'btn small', type: 'button',
        onclick: () => App.openFile({ accession: p.accession, file, page }) }, page ? `Open the document at page ${page}` : 'Open the document')) : null);
  }

  App.view({
    id: 'search', title: 'Document search', tier: 2,
    heading: 'Search the findings and the NASA documents',
    intro: 'Find the passage behind a claim: reviewed findings carry a citation, and raw passages from the PSI documents open in the original file.',
    needs: [],
    brief: {
      need: 'Find the passage behind a claim and open it in the original document.',
      data: ['data/processed/evidence.parquet (server side, 22,879 passages from the PSI documents)', 'data/export/records.json (static fallback: reviewed findings only)'],
      call: 'find_evidence(query="partial gravity", accession="PSI-25", k=20, raw=True)',
      keep: ['Keyword search, not semantic search', 'Raw document passages are unreviewed text and may contain extraction errors', 'Reviewed findings carry their citation ids'],
      backend: 'Required for the raw documents: find_evidence runs a keyword index over 22,879 passages on the server (demo/server.py).',
    },
    render(root, state, update) {
      const live = !!App.backend;
      // A response may arrive after the user left this view: then only store it.
      const later = patch => { if (App.current && App.current.id === 'search') update(patch); else Object.assign(state, patch); };
      const accs = FIF.investigations.map(i => i.accession);
      const mode = state.raw === false || state.raw === 'digest' ? 'digest' : 'raw';

      const run = q => {
        const query = String(q || '').trim();
        if (!query) { update({ q: '', results: null, error: null, loading: false }); return; }
        const my = ++seq;
        if (!live) {
          if (FIF.records) { update({ q: query, error: null, loading: false }); return; }
          update({ q: query, error: null, loading: true });
          App.load(['records']).then(() => { if (my === seq) later({ loading: false }); })
            .catch(e => { if (my === seq) later({ loading: false, error: e.message }); });
          return;
        }
        const args = { query, accession: state.accession || null, k: 20, raw: mode === 'raw' };
        update({ q: query, error: null, loading: true, results: null });
        App.api('find_evidence', args)
          .then(r => { if (my === seq) later({ loading: false, results: { args, r } }); })
          .catch(e => { if (my === seq) later({ loading: false, error: (e && e.message) || String(e) }); });
      };

      if (!live) root.append(h('div', { class: 'callout gap' },
        h('b', { text: 'Document search needs the dashboard server. ' }),
        'The 22,879 passages from the NASA documents are too large for a static page. Here you can search the reviewed findings, limitations and open questions of the 24 records.'));

      const box = App.search({ id: 'se-q', label: live ? 'Search for' : 'Search the reviewed findings', value: state.q || '', placeholder: 'e.g. radiative extinction',
        onChange: v => { state.q = v; } });
      const input = box.querySelector('input');
      if (input) input.addEventListener('keydown', e => { if (e.key === 'Enter') { e.preventDefault(); run(input.value); } });
      root.append(h('div', { class: 'row' },
        box,
        App.select({ id: 'se-acc', label: 'Investigation', value: state.accession || '', options: [['', 'All investigations'], ...accs.map(a => [a, App.name(a)])],
          onChange: v => { update({ accession: v, error: null }); } }),
        live ? App.seg({ id: 'se-raw', label: 'Search in', value: mode, options: [['digest', 'Reviewed findings only'], ['raw', 'Findings and raw documents']],
          onChange: v => update({ raw: v === 'raw', error: null }) }) : null,
        h('button', { class: 'btn primary', type: 'button', id: 'se-go', onclick: () => run(input ? input.value : state.q) }, 'Search')));
      root.append(h('div', { class: 'row' }, h('span', { class: 'small muted', text: 'Examples:' }),
        EXAMPLES.map((x, i) => h('button', { class: 'btn small', type: 'button', id: 'se-ex-' + (i + 1), onclick: () => run(x) }, x))));

      const notes = ['Keyword search (TF-IDF), not semantic search: a passage must share words with the query.'];
      if (state.loading) root.append(h('p', { class: 'muted', id: 'se-loading', text: live ? 'Searching the findings and the documents…' : 'Loading the reviewed records…' }));
      if (state.error) root.append(App.notes([state.error], 'The search failed'));

      if (!live) {
        notes.push('Static page: only the reviewed findings, limitations and open questions are searched, for passages containing every word.');
        if (state.q && FIF.records && !state.loading) {
          const hits = staticSearch(state.q, state.accession);
          root.append(h('p', { class: 'num' }, h('b', { text: `${hits.length} reviewed passages` }), ` contain every word of "${state.q}"`,
            state.accession ? ` in ${App.name(state.accession)}` : '', hits.length > STATIC_LIMIT ? `. The first ${STATIC_LIMIT} are shown.` : '.'));
          root.append(h('div', { class: 'stack', style: 'gap:8px' }, hits.slice(0, STATIC_LIMIT).map(digestCard)));
        }
        notes.push('Raw passages from the NASA documents can be searched when the page is served by demo/server.py.');
      } else if (state.results && !state.loading) {
        const { args, r } = state.results;
        const d = (r && r.data) || {};
        const digest = Array.isArray(d.digest) ? d.digest : [], docs = Array.isArray(d.documents) ? d.documents : [];
        notes.unshift(...(Array.isArray(r && r.notes) ? r.notes : []));
        root.append(h('p', { class: 'num' }, h('b', { text: `${digest.length} reviewed passages` }),
          args.raw ? `, ${docs.length} raw document passages` : '', ` for "${args.query}"`, args.accession ? ` in ${App.name(args.accession)}` : '', '.',
          ' ', App.chip('live from the server', 'good')));
        if (!digest.length && !docs.length) root.append(h('p', { class: 'muted', text: 'Nothing matched. Try other words: the search matches words, not meaning.' }));
        if (digest.length) root.append(App.panel('Reviewed findings', h('div', { class: 'stack', style: 'gap:8px' }, digest.map(digestCard))));
        if (docs.length) root.append(App.panel('Raw passages from the NASA documents (unreviewed)', h('div', { class: 'stack', style: 'gap:8px' }, docs.map(documentCard))));
      }
      if (live) notes.push('Raw document passages are unreviewed extracts and may contain extraction errors. Check them in the original file.');
      root.append(App.notes(notes, 'How to read these results'));

      // A query preset by another view, or changed filters, runs after this render (never inside it).
      const q = String(state.q || '').trim();
      if (q && !state.loading && !state.error) {
        const a = state.results && state.results.args;
        const stale = live ? !a || a.query !== q || (a.accession || '') !== (state.accession || '') || a.raw !== (mode === 'raw') : !FIF.records;
        if (stale) setTimeout(() => { if (App.current && App.current.id === 'search' && String(state.q || '').trim() === q) run(q); }, 0);
      }
    },
  });
})();
