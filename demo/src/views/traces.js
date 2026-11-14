App.view({
  id: 'traces', title: 'Sensor traces', tier: 2,
  heading: 'What did the sensors record during a test?',
  intro: 'Two example recordings with every channel (any recording when the page is served by the dashboard server), and one summary row for each of 1,051 recordings (burn duration, peak temperatures, pressure rise) to compare tests.',
  needs: ['tsexamples', 'tsfeatures'],
  brief: {
    need: 'Scientists need the time history behind a test row: when the flame lit and went out, how temperatures and pressure moved, and whether flows held steady. They also need per-recording summaries to compare tests without opening raw files.',
    data: ['data/export/timeseries_examples.json: 2 decimated recordings (PSI-159 21088 M4, PSI-98 S1) with notes and sources', 'data/export/timeseries_features.json: 1,051 per-recording summaries (PSI-10, 23, 39, 98, 100, 159)', 'docs/formats.md: channel names and units'],
    call: 'timeseries(test_id="21088 M4", channels=["burner_temp_c", "chamber_pressure_kpa"])\ntimeseries(test_id="S1", accession="PSI-98")',
    keep: ['Volt channels (radiometers, PMTs) have no archived calibration: compare shapes, not magnitudes', 'Traces are decimated; say by how much', 'One unit per axis', 'Test ids here have no space (21088M4); the tests table writes 21088 M4', 'Recordings without a timeline file have no ignition or flameout time'],
    backend: 'Live when the page is served by demo/server.py: "Any recording, live" calls timeseries() for any of the 1,051 recordings (the server fetches the raw file from NASA on first use). The static page has only the two exported examples.',
  },
  render(root, state, update) {
    const c = App.colors();
    const EX = FIF.tsexamples || {}, F = Array.isArray(FIF.tsfeatures) ? FIF.tsfeatures : [];
    const UNITS = [['_w_cm2', 'W/cm²'], ['_cm_s', 'cm/s'], ['_slpm', 'slpm'], ['_kpa', 'kPa'], ['_pct', '%'], ['_ua', 'µA'], ['_c', '°C'], ['_v', 'V'], ['_k', 'K'], ['_mm', 'mm'], ['_s', 's']];
    const unitOf = ch => (UNITS.find(([suf]) => ch.endsWith(suf)) || [null, 'other'])[1];
    const isNum = v => typeof v === 'number' && isFinite(v);

    // Draws one timeseries() result (an exported example or a live answer): unit picker, plot, summary, notes, sources.
    // `k` names the state keys so the example and the live recording keep separate unit and channel choices.
    const drawRecording = (E, key, k) => {
      const d = (E && E.data) || {}, series = Array.isArray(d.series) ? d.series : [];
      const xKey = (E.chart && E.chart.x) || 'time_s';
      const listed = Array.isArray(E.chart && E.chart.y) ? E.chart.y : Object.keys(series[0] || {}).filter(x => x !== xKey);
      const channels = listed.filter(ch => series.some(r => isNum(r[ch])));
      const groups = new Map();
      for (const ch of channels) { const u = unitOf(ch); if (!groups.has(u)) groups.set(u, []); groups.get(u).push(ch); }
      const units = [...groups.keys()];
      const unit = groups.has(state[k.unit]) ? state[k.unit] : (groups.has('°C') ? '°C' : units[0]);
      const title = `${App.inv(d.accession).acronym || d.accession || ''} ${d.test_id || key}`.trim();

      if (units.length) root.append(h('div', { class: 'row' },
        App.seg({ id: k.id + '-unit', label: 'Unit on the y axis', options: units.map(u => [u, `${u} (${groups.get(u).length})`]), value: unit, onChange: v => update({ [k.unit]: v }) })));

      if (!series.length || !unit) root.append(h('p', { class: 'muted', text: 'This recording has no numeric channels.' }));
      else {
        const inGroup = groups.get(unit);
        const selKey = `${key}|${unit}`;
        const selAll = Object.assign({}, state[k.chans] || {});
        const chosen = (Array.isArray(selAll[selKey]) ? selAll[selKey] : inGroup.slice(0, 8)).filter(ch => inGroup.includes(ch)).slice(0, 8);
        const msg = h('span', { class: 'small', style: 'color:var(--warn)' });
        const boxes = h('div', { class: 'chips', role: 'group', 'aria-label': 'Channels' }, inGroup.map(ch =>
          h('label', { class: 'chip', style: 'cursor:pointer' },
            h('input', { type: 'checkbox', id: k.id + '-ch-' + ch.replace(/[^\w-]/g, '-'), checked: chosen.includes(ch), onchange: e => {
              const next = e.target.checked ? [...chosen, ch] : chosen.filter(x => x !== ch);
              if (next.length > 8) { e.target.checked = false; msg.textContent = 'At most 8 channels at once.'; return; }
              selAll[selKey] = next; update({ [k.chans]: selAll });
            } }), ch)));
        const xs = series.map(r => isNum(r[xKey]) ? r[xKey] : null);
        const traces = chosen.map((ch, i) => ({ type: 'scatter', mode: 'lines', name: ch, x: xs, y: series.map(r => isNum(r[ch]) ? r[ch] : null),
          line: { color: c.s[i % c.s.length], width: 1.6 }, hovertemplate: '%{y:.4g}' }));
        const plot = h('div', {});
        if (traces.length) App.plot(plot, traces, { height: 420, hovermode: 'x unified', showlegend: traces.length > 1,
          xaxis: { title: xKey === 'time_s' ? 'time since start of recording (s)' : xKey }, yaxis: { title: unit } });
        root.append(App.panel(`${title}: channels in ${unit}`,
          unit === 'V' ? h('div', { class: 'callout gap' }, h('b', { text: 'Volts: no archived calibration: compare shapes, not magnitudes.' })) : null,
          h('div', { class: 'row' }, boxes, msg),
          traces.length ? plot : h('p', { class: 'muted', text: 'Tick at least one channel.' }),
          h('p', { class: 'muted small', text: `${series.length} points per channel. One unit per chart: pick another unit above to see the other channels.` })));
      }

      const feat = Array.isArray(d.features) ? d.features[0] : null;
      if (feat) {
        const shown = Object.entries(feat).filter(([, v]) => v != null && v !== '' && typeof v !== 'object');
        root.append(h('details', { class: 'panel' }, h('summary', { text: `Summary of this recording (${shown.length} fields)` }),
          h('dl', { class: 'kv' }, shown.flatMap(([f, v]) => [h('dt', { class: 'mono', text: f }), h('dd', { text: typeof v === 'boolean' ? String(v) : App.fmt(v) })]))));
      }
      root.append(App.notes(E.notes, 'Notes on this recording'));
      const srcs = Array.isArray(E.sources) ? E.sources : [];
      if (srcs.length) root.append(h('div', { class: 'small muted' }, 'Sources: ', srcs.map((s, i) => h('span', {},
        i ? ' · ' : '', s.accession ? App.name(s.accession) + ': ' : '', h('span', { class: 'mono', text: s.file || s.page || s.url || JSON.stringify(s) })))));
    };
    const bare = x => String(x || '').replace(/\s+/g, '').toLowerCase();
    const baseName = p => String(p || '').split('/').pop();

    // Without the server a recording passed in from another view only narrows the summaries below.
    if (!App.backend && (state.accession || state.test_id || state.test_point)) {
      if (state.accession) state.acc = state.accession;
      delete state.accession; delete state.test_id; delete state.test_point;
    }

    // Part 0: any recording, live from the server
    if (App.backend && F.length) {
      // A recording passed in from another view (accession and test_id, optionally test_point): preselect and load it.
      if (state.accession || state.test_id || state.test_point) {
        const want = F.find(r => (!state.accession || r.accession === state.accession) &&
          (state.test_point ? r.test_point === state.test_point : bare(r.test_id) === bare(state.test_id) || bare(r.test_point) === bare(state.test_id)));
        if (want) { state.liveAcc = want.accession; state.liveTp = want.test_point; state.liveFilter = ''; state._autoload = true; }
        else if (state.accession) state.liveAcc = state.accession;
        delete state.accession; delete state.test_id; delete state.test_point;
      }
      const accNumL = a => parseInt(String(a).replace(/\D+/g, ''), 10) || 0;
      const liveAccs = [...new Set(F.map(r => r.accession))].sort((a, b) => accNumL(a) - accNumL(b));
      const lacc = liveAccs.includes(state.liveAcc) ? state.liveAcc : liveAccs.includes('PSI-159') ? 'PSI-159' : liveAccs[0];
      const term = String(state.liveFilter || '').trim().toLowerCase();
      const inAcc = F.filter(r => r.accession === lacc);
      const cands = inAcc.filter(r => !term || [r.test_id, r.test_point, r.fuel_gas, r.oxidizer_gas].some(v => String(v || '').toLowerCase().includes(term)));
      const ltp = cands.some(r => r.test_point === state.liveTp) ? state.liveTp : (cands[0] && cands[0].test_point);
      const pick = F.find(r => r.accession === lacc && r.test_point === ltp);
      const later = patch => { if (App.current && App.current.id === 'traces') update(patch); else Object.assign(state, patch); };
      const load = rec => {
        if (!rec) return;
        const args = { test_id: rec.test_id, test_point: rec.test_point, accession: rec.accession, max_points: 1500 };
        const my = (state._seq || 0) + 1;
        state._seq = my;
        update({ liveLoading: true, liveError: null, liveAcc: rec.accession, liveTp: rec.test_point });
        App.api('timeseries', args)
          .then(r => { if (state._seq === my) later({ liveLoading: false, live: { args, r } }); })
          .catch(e => { if (state._seq === my) later({ liveLoading: false, liveError: (e && e.message) || String(e) }); });
      };
      const recLabel = r => `${r.test_id || r.test_point}${r.test_point && bare(r.test_point) !== bare(r.test_id) ? ' (' + r.test_point + ')' : ''}${r.fuel_gas ? ' · ' + r.fuel_gas : ''}`;

      root.append(h('h2', { text: 'Any recording, live' }));
      root.append(h('div', { class: 'row' },
        App.select({ id: 'tr-live-acc', label: 'Investigation', value: lacc, options: liveAccs.map(a => [a, `${App.name(a)} (${F.filter(r => r.accession === a).length})`]),
          onChange: v => update({ liveAcc: v, liveTp: null, liveFilter: '' }) }),
        App.search({ id: 'tr-live-filter', label: 'Filter recordings', value: state.liveFilter || '', placeholder: 'test id, gas…', onChange: v => update({ liveFilter: v }) }),
        cands.length ? App.select({ id: 'tr-live-rec', label: `Recording (${cands.length} of ${inAcc.length})`, value: ltp, options: cands.map(r => [r.test_point, recLabel(r)]),
          onChange: v => update({ liveTp: v }) }) : h('span', { class: 'muted small', text: 'No recording matches the filter.' }),
        h('button', { class: 'btn primary', type: 'button', id: 'tr-live-load', disabled: !pick || !!state.liveLoading, onclick: () => load(pick) }, 'Load trace')));
      if (state.liveLoading) root.append(h('p', { class: 'muted', id: 'tr-live-loading', text: 'Loading the recording… The first load of a recording can take a few seconds: the server fetches the raw file from NASA.' }));
      if (state.liveError) root.append(App.notes([state.liveError], 'The recording could not be loaded'));
      const L = state.live;
      if (L && L.r && L.r.data && !state.liveLoading) {
        const src = (Array.isArray(L.r.sources) ? L.r.sources : []).find(s => s && s.file && s.accession);
        root.append(h('div', { class: 'row' }, App.chip('live from the server', 'good'),
          src ? h('button', { class: 'btn', type: 'button', id: 'tr-live-open', onclick: () => App.openFile({ accession: src.accession, file: baseName(src.file) }) }, 'Open the raw file') : null));
        drawRecording(L.r, `live|${L.args.accession}|${L.args.test_point}`, { id: 'tr-live', unit: 'liveUnit', chans: 'liveChans' });
      } else if (!state.liveLoading && !state.liveError) root.append(h('p', { class: 'muted', text: 'Pick a recording and press Load trace.' }));
      if (state._autoload) {
        delete state._autoload;
        setTimeout(() => { if (App.current && App.current.id === 'traces') load(pick); }, 0);
      }
    }

    // Part A: example recordings
    const keys = Object.keys(EX);
    root.append(h('h2', { text: 'Example recordings' }));
    if (!App.backend) root.append(h('p', { class: 'muted small', id: 'tr-live-off', text: 'Any of the 1,051 recordings can be plotted when the page is served by demo/server.py. The static page has these two examples.' }));
    if (!keys.length) root.append(h('p', { class: 'muted', text: 'No example recordings in the export.' }));
    else {
      const key = keys.includes(state.ex) ? state.ex : keys[0];
      const exLabel = k => { const e = EX[k] || {}, dd = e.data || {}; return `${App.inv(dd.accession).acronym || dd.accession || ''} ${dd.test_id || k}`.trim(); };
      root.append(h('div', { class: 'row' },
        App.select({ id: 'tr-example', label: 'Recording', options: keys.map(k => [k, exLabel(k)]), value: key, onChange: v => update({ ex: v, unit: null }) })));
      drawRecording(EX[key] || {}, key, { id: 'tr', unit: 'unit', chans: 'chans' });
    }

    // Part B: per-recording summaries
    root.append(h('h2', { text: 'Per-recording summaries' }));
    if (!F.length) { root.append(h('p', { class: 'muted', text: 'No per-recording summaries in the export.' })); return; }
    const accNum = a => parseInt(String(a).replace(/\D+/g, ''), 10) || 0;
    const accCounts = F.reduce((m, r) => m.set(r.accession, (m.get(r.accession) || 0) + 1), new Map());
    const accs = [...accCounts.keys()].sort((a, b) => accNum(a) - accNum(b));
    const acc = accCounts.has(state.acc) ? state.acc : '';
    const sel = acc ? F.filter(r => r.accession === acc) : F;
    const cols = [];
    for (const r of F) for (const k of Object.keys(r)) if (!cols.includes(k) && isNum(r[k])) cols.push(k);
    const n = k => sel.reduce((a, r) => a + (isNum(r[k]) ? 1 : 0), 0);
    const numCols = cols.filter(k => n(k) > 0);
    const pick = (want, fallback) => numCols.includes(want) ? want : fallback;
    const xk = pick(state.x, pick('burn_duration_s', numCols[0]));
    const yk = pick(state.y, pick('burner_temp_max_c', numCols[1] || numCols[0]));
    const colour = state.colour === 'flame' ? 'flame' : 'none';

    root.append(h('div', { class: 'row' },
      App.select({ id: 'tr-acc', label: 'Investigation', value: acc, onChange: v => update({ acc: v }),
        options: [['', `All (${F.length})`], ...accs.map(a => [a, `${App.name(a)} (${accCounts.get(a)})`])] }),
      numCols.length ? App.select({ id: 'tr-x', label: 'x', value: xk, onChange: v => update({ x: v }), options: numCols.map(k => [k, `${k} (${n(k)})`]) }) : null,
      numCols.length ? App.select({ id: 'tr-y', label: 'y', value: yk, onChange: v => update({ y: v }), options: numCols.map(k => [k, `${k} (${n(k)})`]) }) : null,
      App.seg({ id: 'tr-colour', label: 'Colour', options: [['none', 'None'], ['flame', 'Flame detected']], value: colour, onChange: v => update({ colour: v }) })));

    const showRow = r => {
      if (!r) return;
      const entries = Object.entries(r).filter(([, v]) => v != null && v !== '');
      App.drawer(`${r.test_id || 'recording'} (${App.name(r.accession)})`, h('div', { class: 'stack' },
        h('dl', { class: 'kv' }, entries.flatMap(([k, v]) => [h('dt', { class: 'mono', text: k }), h('dd', { text: typeof v === 'boolean' ? String(v) : App.fmt(v) })])),
        h('p', { class: 'muted small', text: 'Fields that are empty for this recording are not listed. Test ids here have no space; the tests table may write the same test with a space.' }),
        h('div', { class: 'row' },
          h('button', { class: 'btn primary', type: 'button', onclick: () => App.go('tests', { accession: r.accession, q: r.test_id }) }, 'Find in the tests table'),
          h('button', { class: 'btn', type: 'button', onclick: () => App.go('investigation', { accession: r.accession }) }, 'Open the record'),
          App.backend ? h('button', { class: 'btn', type: 'button', onclick: () => { App.closeDrawer(); update({ accession: r.accession, test_point: r.test_point, test_id: r.test_id }); window.scrollTo(0, 0); } }, 'Plot this recording') : null)));
    };

    const both = sel.filter(r => isNum(r[xk]) && isNum(r[yk]));
    const groupsB = colour === 'flame'
      ? [['flame detected', r => r.flame_detected === true, c.s[1]], ['no flame detected', r => r.flame_detected === false, c.s[0]], ['not determined', r => typeof r.flame_detected !== 'boolean', c.neutral]]
      : [['recordings', () => true, c.accent]];
    const traces = groupsB.map(([name, test, col]) => {
      const rs = both.filter(test);
      return { type: 'scattergl', mode: 'markers', name: `${name} (${rs.length})`, x: rs.map(r => r[xk]), y: rs.map(r => r[yk]), customdata: rs.map(r => F.indexOf(r)),
        text: rs.map(r => `${r.test_id || '?'} (${App.inv(r.accession).acronym || r.accession})`),
        hovertemplate: `%{text}<br>${xk} %{x:.4g}<br>${yk} %{y:.4g}<extra></extra>`, marker: { size: 6, color: col, opacity: 0.75 } };
    }).filter(t => t.x.length);
    const plot = h('div', {});
    if (traces.length) App.plot(plot, traces, { height: 420, hovermode: 'closest', showlegend: traces.length > 1, xaxis: { title: xk }, yaxis: { title: yk } },
      pt => showRow(F[pt && pt.customdata]));
    root.append(App.panel(`${yk} against ${xk}`,
      traces.length ? plot : h('p', { class: 'muted', text: 'No recording in this selection has both values.' }),
      h('p', { class: 'muted small', text: `${both.length} of ${sel.length} recordings have both values. Click a point for all its fields.` })));

    const tableCols = [...new Set(['accession', 'test_id', 'fuel_gas', 'oxidizer_gas', 'flame_detected', 'burn_duration_s', xk, yk])];
    root.append(App.table({ rows: sel, pageSize: 15, onRow: showRow, sort: { key: 'test_id', dir: 1 }, cols: tableCols.map(k => (
      k === 'accession' ? { key: k, label: 'Investigation', fmt: v => App.inv(v).acronym || v }
        : k === 'flame_detected' ? { key: k, label: 'Flame', fmt: v => v === true ? App.chip('yes') : v === false ? App.chip('no', 'warn') : '–' }
          : cols.includes(k) ? { key: k, label: k, num: true, fmt: v => App.fmt(v) } : { key: k, label: k })) }));
    root.append(App.notes([
      'Test ids here have no space ("21088M4"); the tests table writes "21088 M4". Match them with the space removed.',
      'Radiometer and PMT values in volts have no archived calibration: compare shapes, not magnitudes.',
      'Recordings without a timeline file (features_note "no _TP.txt timeline") have no ignition or flameout time.',
      'Mean flows a little below zero are most likely the flow-meter offset around zero, not reverse flow.',
      'Only PSI-10, 23, 39, 98, 100 and 159 have archived time series that were summarised.']));
  },
});
