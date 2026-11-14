(function () {
  const ACTIONS = ['replace', 'fill', 'flag', 'note'];
  const ACTION_KIND = { replace: 'crit', fill: 'warn', flag: 'warn', note: '' };
  const accNum = a => parseInt(String(a).replace(/\D/g, ''), 10) || 0;
  const show = v => v == null || v === '' ? 'empty' : typeof v === 'object' ? JSON.stringify(v) : String(v);
  const plain = s => String(s ?? '').replace(/[<>&]/g, ch => ({ '<': '‹', '>': '›', '&': '+' })[ch]);
  const text = x => [].concat(x).filter(v => v != null).map(v => typeof v === 'object' ? JSON.stringify(v) : String(v)).join(' ').toLowerCase();

  // Filter conflicts and changed values by investigation, action and search. An exact test id wins over substring hits.
  function select(D, s) {
    const q = String(s.q || '').trim().toLowerCase();
    const byQ = (list, ids, hay) => {
      if (!q) return list;
      const ex = list.filter(x => ids(x).some(id => id != null && String(id).toLowerCase() === q));
      return ex.length ? ex : list.filter(x => hay(x).includes(q));
    };
    const conflicts = byQ((D.raw_data_conflicts || []).filter(c => (!s.accession || c.accession === s.accession) && (!s.action || s.action === 'all' || c.action === s.action)),
      c => [c.test_id, c.test_id_now, c.id],
      c => text([c.id, c.accession, c.test_id, c.test_id_now, c.column, c.table_value, c.evidence_value, c.action, c.flag, c.evidence, c.evidence_source]));
    const changed = byQ((D.values_changed || []).filter(v => !s.accession || v.accession === s.accession),
      v => [v.test_id],
      v => text([v.accession, v.test_id, v.column, v.table_value, v.value_now, v.flags, v.patch_ids]));
    return { conflicts, changed };
  }

  App.view({
    id: 'quality', title: 'Data quality', tier: 2,
    heading: 'Where are the NASA tables wrong or doubtful?',
    intro: 'Errors and doubts in the PSI tables are shown here, never fixed silently. Every change keeps the original value next to the evidence for it.',
    needs: [],
    brief: {
      need: 'One place that lists every conflict between the NASA tables and the raw data or reports, with the evidence, so a scientist can decide whether to trust a value.',
      data: ['data/export/discrepancies.json: raw_data_conflicts, values_changed, flags (with meanings and row counts), actions, removed_sources', 'data/export/tests.json for the flagged rows themselves'],
      call: 'discrepancies(accession="PSI-10", test_id="22024M1")',
      keep: [
        'The original table value is always kept and shown next to the value now.',
        'A "flag" action means the table value was kept because the evidence is not decisive.',
        'Flagged rows elsewhere in the dashboard carry a badge linked to this evidence.',
        'Raw files exist only for PSI-10, 23, 39, 98, 100, 101 and 159. The other tables were checked against the reports only.',
        'Some source files were removed from the PSI site; citations to them are marked.',
      ],
    },
    select,

    render(root, state, update) {
      const D = FIF.discrepancies || {};
      const c = App.colors();
      const conflictsAll = D.raw_data_conflicts || [], changedAll = D.values_changed || [], flags = D.flags || [], removed = D.removed_sources || [];
      const actions = D.actions || {};
      const flagMeaning = Object.fromEntries(flags.map(f => [f.flag, f.meaning]));

      // Arrival from another view: a new investigation without a new search clears the old search.
      const acc0 = state.accession || '', q0 = state.q || '';
      if (state._seenAcc !== undefined && (acc0 !== state._seenAcc || q0 !== state._seenQ)) {
        if (acc0 !== state._seenAcc && q0 === state._seenQ) state.q = '';
        state.action = 'all';
      }
      state._seenAcc = state.accession || ''; state._seenQ = state.q || '';
      const set = p => { const n = Object.assign({}, state, p); update(Object.assign({}, p, { _seenAcc: n.accession || '', _seenQ: n.q || '' })); };

      const nNotes = conflictsAll.filter(x => x.action === 'note').length;
      root.append(h('div', { class: 'grid tiles' },
        h('div', { class: 'tile' }, h('b', { text: String(conflictsAll.length) }), h('span', { text: `conflicts with the raw data (${nNotes} whole-investigation notes)` })),
        h('div', { class: 'tile' }, h('b', { text: String(changedAll.length) }), h('span', { text: 'values changed, originals kept' })),
        h('div', { class: 'tile' }, h('b', { text: D.rows_flagged != null ? String(D.rows_flagged) : '–' }), h('span', { text: `rows flagged of ${D.rows_total != null ? D.rows_total : '–'} rows` })),
        h('div', { class: 'tile' }, h('b', { text: String(removed.length) }), h('span', { text: 'cited source files removed from PSI' }))));

      // Flags by number of rows
      const fs = [...flags].sort((a, b) => (b.rows || 0) - (a.rows || 0));
      const plotBox = h('div', {});
      if (fs.length) {
        App.plot(plotBox, [{ type: 'bar', orientation: 'h', name: 'rows', y: fs.map(f => f.flag), x: fs.map(f => f.rows || 0),
          marker: { color: c.s[0] }, text: fs.map(f => String(f.rows || 0)), textposition: 'outside', cliponaxis: false, textfont: { color: c.fg2, size: 11 },
          customdata: fs.map(f => plain(f.meaning || '').replace(/`/g, '')),
          hovertemplate: '%{y}: %{x} rows<br>%{customdata}<extra></extra>' }],
          { height: 60 + fs.length * 20, margin: { l: 190, r: 48, t: 8, b: 40 }, bargap: 0.3,
            xaxis: { title: 'rows carrying the flag' }, yaxis: { autorange: 'reversed', tickfont: { family: 'JetBrains Mono, monospace', size: 11, color: c.fg2 } } },
          pt => { const f = fs.find(x => x.flag === (pt && pt.y)); if (f) showFlag(f); });
      } else plotBox.append(h('p', { class: 'muted', text: 'No flags in the data.' }));
      root.append(h('div', { class: 'grid two' },
        App.panel('Flags by number of rows', h('p', { class: 'muted small', text: 'A row can carry several flags. Click a bar for its meaning and its tests.' }), plotBox),
        App.panel('What each action does',
          h('dl', { class: 'kv' }, ACTIONS.filter(a => actions[a] != null).concat(Object.keys(actions).filter(a => !ACTIONS.includes(a))).flatMap(a => [
            h('dt', {}, App.chip(a, ACTION_KIND[a] || '')),
            h('dd', {}, App.tex(actions[a]), h('span', { class: 'muted small', text: ` (${conflictsAll.filter(x => x.action === a).length} entries)` }))])),
          h('p', { class: 'small muted', text: 'Changes made from the reports or records, not from raw data, appear under values changed with no patch id.' }))));

      function showFlag(f) {
        App.drawer(f.flag, h('div', { class: 'stack' },
          h('p', {}, App.tex(f.meaning || 'No meaning recorded.')),
          h('p', { class: 'small muted', text: `${f.rows || 0} rows carry this flag.` }),
          h('button', { class: 'btn primary', type: 'button', onclick: () => App.go('tests', { accession: '', q: f.flag }) }, 'See these tests')));
      }

      // Raw-data conflicts
      const sel = select(D, state);
      const accs = [...new Set([...conflictsAll, ...changedAll].map(x => x.accession).concat(state.accession ? [state.accession] : []).filter(Boolean))]
        .sort((a, b) => accNum(a) - accNum(b));
      root.append(h('div', { class: 'row' },
        App.select({ id: 'dq-acc', label: 'Investigation', value: state.accession || '', onChange: v => set({ accession: v }),
          options: [['', 'All investigations'], ...accs.map(a => [a, App.name(a)])] }),
        App.seg({ id: 'dq-action', label: 'Action', value: state.action || 'all', onChange: v => set({ action: v }), options: [['all', 'All'], ...ACTIONS] }),
        App.search({ id: 'dq-q', label: 'Search (test id, column, evidence)', value: state.q || '', onChange: v => set({ q: v }), placeholder: 'e.g. 22024M1' }),
        h('button', { class: 'btn', type: 'button', id: 'dq-reset', onclick: () => set({ accession: '', q: '', action: 'all' }) }, 'Reset')));

      function testOf(x) { return x.test_id_now || x.test_id; }
      function showConflict(x) {
        const tid = testOf(x);
        App.drawer(`${x.id}: ${App.inv(x.accession).acronym || x.accession}${tid ? ' ' + tid : ''}`, h('div', { class: 'stack' },
          h('p', { class: 'small muted' }, App.name(x.accession), x.column ? ' · column ' : '', x.column ? h('span', { class: 'mono', text: x.column }) : null),
          h('div', { class: 'chips' }, App.chip(x.action || 'no action', ACTION_KIND[x.action] || ''), x.flag && App.chip(x.flag, 'warn')),
          actions[x.action] && h('p', { class: 'small' }, App.tex(actions[x.action])),
          x.action !== 'note' && h('dl', { class: 'kv' },
            h('dt', { text: 'test id in table' }), h('dd', { class: 'mono', text: show(x.test_id) }),
            x.test_id_now && x.test_id_now !== x.test_id && h('dt', { text: 'test id now' }), x.test_id_now && x.test_id_now !== x.test_id && h('dd', { class: 'mono', text: x.test_id_now }),
            h('dt', { text: 'table value' }), h('dd', { class: 'mono', text: show(x.table_value) }),
            h('dt', { text: 'evidence value' }), h('dd', { class: 'mono', text: show(x.evidence_value) }),
            h('dt', { text: 'value now' }), h('dd', { class: 'mono', text: x.action === 'flag' ? show(x.table_value) + ' (table value kept)' : show(x.evidence_value) })),
          h('h4', { text: 'Evidence' }),
          h('p', { text: x.evidence || 'No evidence text recorded.' }),
          h('p', { class: 'small muted', text: 'Source: ' + (x.evidence_source || 'not recorded') }),
          x.flag && flagMeaning[x.flag] && h('p', { class: 'small' }, App.chip(x.flag, 'warn'), ' ', App.tex(flagMeaning[x.flag])),
          tid ? h('button', { class: 'btn primary', type: 'button', onclick: () => App.go('tests', { accession: x.accession, q: tid }) }, 'See the test')
            : h('p', { class: 'small muted', text: 'This entry concerns the whole investigation, not one test.' })));
      }

      root.append(App.panel(`Conflicts with the raw sensor data (${sel.conflicts.length} of ${conflictsAll.length})`,
        sel.conflicts.length ? App.table({ rows: sel.conflicts, pageSize: 15, onRow: showConflict, cols: [
          { key: 'id', label: 'Id', fmt: v => h('span', { class: 'mono', text: v || '–' }) },
          { key: 'accession', label: 'Investigation', fmt: v => App.inv(v).acronym || v },
          { key: 'test_id', label: 'Test', fmt: (v, r) => h('span', { class: 'mono', text: r.test_id_now && r.test_id_now !== v ? `${v} → ${r.test_id_now}` : show(v === null ? '–' : v) }) },
          { key: 'column', label: 'Column', fmt: v => v ? h('span', { class: 'mono', text: v }) : '–' },
          { key: 'table_value', label: 'Table value', sortable: false, fmt: v => show(v) },
          { key: 'evidence_value', label: 'Evidence value', sortable: false, fmt: v => show(v) },
          { key: 'action', label: 'Action', fmt: v => App.chip(v || '–', ACTION_KIND[v] || '') },
          { key: 'evidence', label: 'Evidence', sortable: false, fmt: v => { const s = String(v || ''); return s.length > 90 ? s.slice(0, 88) + '…' : s || '–'; } },
        ] }) : h('p', { class: 'muted', text: 'No raw-data conflict matches this selection.' })));

      function showChanged(v) {
        const patches = Array.isArray(v.patch_ids) ? v.patch_ids : [];
        App.drawer(`${App.inv(v.accession).acronym || v.accession} ${v.test_id}: ${v.column}`, h('div', { class: 'stack' },
          h('dl', { class: 'kv' },
            h('dt', { text: 'column' }), h('dd', { class: 'mono', text: show(v.column) }),
            h('dt', { text: 'table value' }), h('dd', { class: 'mono', text: show(v.table_value) }),
            h('dt', { text: 'value now' }), h('dd', { class: 'mono', text: show(v.value_now) })),
          h('div', { class: 'chips' }, String(v.flags || '').split(';').filter(Boolean).map(f => App.chip(f, 'warn'))),
          patches.length ? h('div', { class: 'chips' }, h('span', { class: 'small muted', text: 'patches:' }),
            patches.map(id => { const x = conflictsAll.find(k => k.id === id); return App.chip(id, 'crit', x ? () => showConflict(x) : null); }))
            : h('p', { class: 'small muted', text: 'Changed from the reports or records, not from raw data. See the flags above.' }),
          h('button', { class: 'btn primary', type: 'button', onclick: () => App.go('tests', { accession: v.accession, q: v.test_id }) }, 'See the test')));
      }

      root.append(App.panel(`Values changed (${sel.changed.length} of ${changedAll.length})`,
        h('p', { class: 'muted small', text: 'Each changed value keeps the NASA table value in the test row (extra, as <column>_original).' }),
        sel.changed.length ? App.table({ rows: sel.changed, pageSize: 15, onRow: showChanged, cols: [
          { key: 'accession', label: 'Investigation', fmt: v => App.inv(v).acronym || v },
          { key: 'test_id', label: 'Test', fmt: v => h('span', { class: 'mono', text: show(v) }) },
          { key: 'column', label: 'Column', fmt: v => h('span', { class: 'mono', text: show(v) }) },
          { key: 'table_value', label: 'Table value → value now', sortable: false, fmt: (v, r) => `${show(v)} → ${show(r.value_now)}` },
          { key: 'patch_ids', label: 'Patches', sortable: false, fmt: v => Array.isArray(v) && v.length ? v.join(', ') : 'report or record' },
          { key: 'flags', label: 'Flags', sortable: false, fmt: v => { const n = String(v || '').split(';').filter(Boolean).length; return n ? App.chip(`${n} flag${n > 1 ? 's' : ''}`, 'warn') : ''; } },
        ] }) : h('p', { class: 'muted', text: 'No changed value matches this selection.' })));

      root.append(App.panel('Flag dictionary',
        App.table({ rows: fs, pageSize: 40, sort: { key: 'rows', dir: -1 }, onRow: showFlag, cols: [
          { key: 'flag', label: 'Flag', fmt: v => App.chip(v || '–', 'warn') },
          { key: 'rows', label: 'Rows', num: true },
          { key: 'meaning', label: 'Meaning', sortable: false, fmt: v => h('span', {}, App.tex(v || '')) },
        ] })));

      root.append(App.panel('Cited source files removed from the PSI site',
        removed.length ? h('ul', { style: 'margin:0;padding-left:18px', class: 'stack' }, removed.map(r => h('li', { class: 'small' },
          h('b', { text: App.name(r.accession) }), ' · ', h('span', { class: 'mono', text: r.where || '–' }), ' · ',
          /^https?:\/\//.test(r.url || '') ? h('a', { href: r.url, target: '_blank', rel: 'noopener', style: 'overflow-wrap:anywhere' }, r.url) : (r.url || 'no link')))) :
          h('p', { class: 'muted', text: 'None.' })));

      root.append(App.notes([
        'The original NASA value is never dropped. Replaced values stay in the test row as `<column>_original`.',
        'A "flag" action keeps the table value: the raw evidence is not decisive (sensor accuracy unknown, or a difference a few seconds wide).',
        'Raw files exist only for PSI-10, 23, 39, 98, 100, 101 and 159. The other tables were checked against the reports only.',
      ]));
    },
  });
})();
