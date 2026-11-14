(function () {
  App.view({
    id: 'scenario', title: 'Scenario lens', tier: 1,
    heading: 'Which investigations matter for a given habitat?',
    intro: 'Pick a habitat, the kind of fuel and the fire-safety pillar. The 24 investigations are ranked by a transparent score, and the distance to the nearest real test is always stated.',
    needs: ['relevance'],
    brief: {
      need: 'A scenario picker that ranks the investigations and says how far the data are from the scenario. The score must be decomposed, never shown as one opaque number.',
      data: ['data/export/relevance.json: 60 pre-computed rankings keyed "scenario|phase|pillar"', 'weights and formula: docs/methods.md'],
      call: 'relevance(scenario="moon-habitat", fuel_phase="solid", pillar="detection")',
      keep: ['The gap sentence (nearest test of the requested fuel phase and its distance)', 'The notes returned with the ranking', 'Which conditions were unknown, taken from a range, or assumed to be cabin air', 'No PSI test was run in partial gravity'],
      backend: 'Live when the page is served by demo/server.py: the Custom choice sends free O2, pressure, flow and gravity values to relevance() and draws its answer. The static page has only the 5 presets.',
    },
    render(root, state, update) {
      const R = FIF.relevance;
      const keys = Object.keys(R);
      const scenarios = [...new Set(keys.map(k => k.split('|')[0]))];
      const live = !!App.backend;
      const custom = live && state.scenario === 'custom';
      const s = custom ? 'custom' : scenarios.includes(state.scenario) ? state.scenario : 'moon-habitat';
      const ph = state.phase || 'solid', pi = state.pillar || 'any';
      const label = k => R[`${k}|solid|any`].data.scenario.label;
      // A response may arrive after the user left this view: then only store it.
      const later = patch => { if (App.current && App.current.id === 'scenario') update(patch); else Object.assign(state, patch); };

      const scSel = App.select({ id: 'sc-scenario', label: 'Habitat scenario', options: [...scenarios.map(k => [k, label(k)]), ['custom', 'Custom values']], value: s,
        onChange: v => update({ scenario: v }) });
      const customOpt = scSel.querySelector('option[value="custom"]');
      if (customOpt && !live) customOpt.disabled = true;
      root.append(h('div', { class: 'row' },
        scSel,
        App.seg({ id: 'sc-phase', label: 'Fuel of concern', options: ['solid', 'liquid', 'gas'], value: ph, onChange: v => update({ phase: v }) }),
        App.seg({ id: 'sc-pillar', label: 'Pillar', options: [['any', 'Any'], 'prevention', 'detection', 'suppression'], value: pi, onChange: v => update({ pillar: v }) })));
      if (!live) root.append(h('p', { class: 'muted small', id: 'sc-custom-off', text: 'Custom values need the dashboard server; the static page has 5 presets.' }));

      let res;
      if (!custom) res = R[`${s}|${ph}|${pi}`];
      else {
        const cv = state.custom = Object.assign({ o2: 30, p: 70, flowSet: false, flow: 10, g: 0.165 }, state.custom || {});
        const argsFor = () => {
          const sc = { x_o2: cv.o2 / 100, pressure_kpa: cv.p, gravity_g: +cv.g };
          if (cv.flowSet) sc.flow_cm_s = cv.flow;
          return { scenario: sc, fuel_phase: ph, pillar: pi === 'any' ? null : pi };
        };
        const rank = () => {
          const args = argsFor(), my = (state._seq || 0) + 1;
          state._seq = my;
          update({ loading: true, error: null });
          App.api('relevance', args)
            .then(r => { if (state._seq === my) later({ loading: false, live: { args, r } }); })
            .catch(e => { if (state._seq === my) later({ loading: false, error: (e && e.message) || String(e) }); });
        };
        root.append(App.panel('Custom scenario',
          h('div', { class: 'row' },
            App.range({ id: 'sc-o2', label: 'Oxygen', min: 10, max: 100, step: 1, value: cv.o2, format: v => v + ' %', onChange: v => { cv.o2 = v; } }),
            App.range({ id: 'sc-p', label: 'Pressure', min: 20, max: 110, step: 1, value: cv.p, format: v => v + ' kPa', onChange: v => { cv.p = v; } })),
          h('div', { class: 'row' },
            App.seg({ id: 'sc-flowset', label: 'Ventilation flow', value: cv.flowSet ? 'set' : 'unspecified', options: [['unspecified', 'Unspecified'], ['set', 'Set a value']],
              onChange: v => update({ custom: Object.assign({}, cv, { flowSet: v === 'set' }) }) }),
            cv.flowSet ? App.range({ id: 'sc-flow', label: 'Flow', min: 0, max: 50, step: 1, value: cv.flow, format: v => v + ' cm/s', onChange: v => { cv.flow = v; } }) : null,
            App.select({ id: 'sc-g', label: 'Gravity', value: String(cv.g), options: [['0', '0 g (orbit)'], ['0.165', '0.165 g (Moon)'], ['0.38', '0.38 g (Mars)'], ['1', '1 g (Earth)']],
              onChange: v => { cv.g = +v; } }),
            h('button', { class: 'btn primary', type: 'button', id: 'sc-rank', disabled: !!state.loading, onclick: rank }, 'Rank')),
          h('p', { class: 'muted small', text: 'Unspecified flow leaves flow out of the distance. Fuel phase and pillar above apply too. Press Rank to compute.' })));
        if (state.loading) root.append(h('p', { class: 'muted', id: 'sc-loading', text: 'Ranking on the server…' }));
        if (state.error) root.append(App.notes([state.error], 'The ranking failed'));
        const L = state.live;
        if (L && L.r && L.r.data && !state.loading) {
          const same = L.args.fuel_phase === ph && (L.args.pillar || 'any') === pi;
          if (same) res = L.r;
          else {
            root.append(h('p', { class: 'muted', text: 'Fuel phase or pillar changed. Ranking again…' }));
            if (!state.error) setTimeout(() => { if (App.current && App.current.id === 'scenario' && !state.loading) rank(); }, 0);
          }
        }
        if (!res) { if (!state.loading && !state.error && !L) root.append(h('p', { class: 'muted', text: 'Set the values and press Rank.' })); return; }
        root.append(h('div', { class: 'row' }, App.chip('live from the server', 'good'),
          h('span', { class: 'small muted', text: `Ranked for ${App.pct(L.args.scenario.x_o2, 0)} O2, ${App.fmt(L.args.scenario.pressure_kpa)} kPa, ${L.args.scenario.flow_cm_s == null ? 'unspecified flow' : L.args.scenario.flow_cm_s + ' cm/s flow'}, ${L.args.scenario.gravity_g} g.` })));
      }
      if (!res || !res.data) { root.append(h('p', { class: 'muted', text: 'No ranking for this choice.' })); return; }
      drawResult(root, res, state, update, ph);
    },
  });

  // Draws one relevance() result: the static export (trimmed rows) and the live answer (with one_line, acronym, key_findings).
  function drawResult(root, res, state, update, ph) {
    const c = App.colors();
    const d = res.data, sc = d.scenario || {};

    root.append(h('div', { class: 'grid tiles' },
      h('div', { class: 'tile' }, h('b', { text: App.pct(sc.x_o2, 0) }), h('span', { text: 'oxygen' })),
      h('div', { class: 'tile' }, h('b', { text: App.fmt(sc.pressure_kpa, 1) }), h('span', { text: 'kPa total pressure' })),
      h('div', { class: 'tile' }, h('b', { text: sc.gravity_g == null ? '–' : App.fmt(sc.gravity_g) + ' g' }), h('span', { text: 'gravity (never tested in PSI unless 0 or 1 g)' })),
      h('div', { class: 'tile' }, h('b', { text: d.closest_same_phase ? App.inv(d.closest_same_phase).acronym : 'none' }), h('span', { text: `closest ${ph}-fuel investigation` }))));

    const gap = (res.notes || []).find(n => /^Gap:/.test(n));
    if (gap) root.append(h('div', { class: 'callout gap' }, h('b', { text: 'How far the data are from this scenario. ' }), gap.replace(/^Gap:\s*/, '')));

    const comps = Object.keys(d.weights);
    const wsum = comps.reduce((a, k) => a + d.weights[k], 0);
    const rows = [...(d.ranking || [])].sort((a, b) => b.score - a.score);
    const shown = state.all ? rows : rows.slice(0, 12);
    const ylab = shown.map(r => App.inv(r.accession).acronym);
    // Each segment is the component's contribution to the 0-100 score, so the bar length is the score.
    const active = comps.filter(k => shown.some(r => (r.components[k] || 0) > 0 && (k !== 'gravity' || sc.gravity_g > 0 && sc.gravity_g < 1)));
    const used = active.reduce((a, k) => a + d.weights[k], 0);
    const traces = active.map((k, i) => ({
      type: 'bar', orientation: 'h', name: `${k} (weight ${d.weights[k]})`, y: ylab,
      x: shown.map(r => 100 * d.weights[k] * (r.components[k] || 0) / used),
      customdata: shown.map(r => [r.components[k], r.score]),
      marker: { color: c.s[i], line: { color: c.surface, width: 2 } },
      hovertemplate: `%{y}<br>${k}: %{customdata[0]:.2f} of 1<br>adds %{x:.1f} points<br>score %{customdata[1]:.1f}<extra></extra>` }));
    const plot = h('div', {});
    App.plot(plot, traces, { barmode: 'stack', height: 60 + shown.length * 26, margin: { l: 150, r: 24, t: 8, b: 40 },
      xaxis: { title: 'relevance score (0-100)', range: [0, 100] }, yaxis: { autorange: 'reversed' }, legend: { orientation: 'h', y: 1.02, yanchor: 'bottom', x: 0 } },
      pt => showRow(rows.find(r => App.inv(r.accession).acronym === pt.y)));
    root.append(App.panel('Ranking, with the score split into its components', plot,
      h('div', { class: 'row' }, h('button', { class: 'btn', type: 'button', onclick: () => update({ all: !state.all }) }, state.all ? 'Show the top 12' : 'Show all 24'),
        h('span', { class: 'muted small', text: 'Click a bar for the nearest test and the assumptions behind the score.' }))));

    function showRow(r) {
      if (!r) return;
      const i = App.inv(r.accession), other = !r.nearest_test && r.nearest_test_other_phase, t = r.nearest_test || other || {};
      const flagList = (title, arr, kind) => arr && arr.length ? h('div', { class: 'chips' }, h('span', { class: 'small muted', text: title }), arr.map(x => App.chip(x, kind))) : null;
      App.drawer(`${i.acronym}: score ${App.fmt(r.score, 1)}`, h('div', { class: 'stack' },
        h('p', { text: r.one_line || i.one_line || '' }),
        h('dl', { class: 'kv' }, comps.flatMap(k => [h('dt', { text: k }), h('dd', { class: 'num', text: `${App.fmt(r.components[k], 2)} × weight ${d.weights[k]}` })])),
        h('h4', { text: other ? `Nearest test to the scenario (${other.fuel_phase} fuel: no ${ph}-fuel test in this investigation)` : 'Nearest test to the scenario' }),
        h('dl', { class: 'kv' },
          h('dt', { text: 'test' }), h('dd', { text: t.test_id || '–' }),
          h('dt', { text: 'fuel' }), h('dd', { text: `${t.fuel || '–'} (${t.fuel_phase || '–'})` }),
          h('dt', { text: 'O2' }), h('dd', { text: App.pct(t.x_o2_ambient) }),
          h('dt', { text: 'pressure' }), h('dd', { text: App.fmt(t.pressure_kpa, 1) + ' kPa' }),
          h('dt', { text: 'flow' }), h('dd', { text: App.fmt(t.flow_cm_s) + ' cm/s' }),
          h('dt', { text: 'distance' }), h('dd', { text: App.fmt(r.distance_to_scenario, 2) + ' steps (1 step = 3 points O2, 15 kPa or 10 cm/s)' })),
        flagList('not recorded:', r.conditions_unknown, 'crit'),
        flagList('known only as a range:', r.conditions_from_range, 'warn'),
        flagList('assumed cabin air:', r.conditions_assumed_cabin_air, 'warn'),
        Array.isArray(r.key_findings) && r.key_findings.length ? h('div', { class: 'stack', style: 'gap:6px' }, h('h4', { text: 'Key findings' }),
          r.key_findings.map(f => h('div', { class: 'small' }, citeOf(f.ref) && App.cite(citeOf(f.ref)), ' ', App.tex(f.claim || '')))) : null,
        h('div', { class: 'row' },
          h('button', { class: 'btn primary', type: 'button', onclick: () => App.go('investigation', { accession: r.accession }) }, 'Open the record'),
          h('button', { class: 'btn', type: 'button', onclick: () => App.go('tests', { accession: r.accession }) }, 'See its tests'))));
    }

    root.append(App.table({
      rows, pageSize: 24, onRow: showRow, sort: { key: 'score', dir: -1 },
      cols: [
        { key: 'accession', label: 'Investigation', fmt: v => App.name(v) },
        { key: 'score', label: 'Score', num: true, fmt: v => App.fmt(v, 1) },
        { key: 'distance_to_scenario', label: 'Distance (steps)', num: true, fmt: v => App.fmt(v, 2) },
        { key: 'nearest_test', label: 'Nearest test', sortable: false, fmt: (t, r) => { const o = t || r.nearest_test_other_phase;
          return o ? `${o.fuel || '?'}${t ? '' : ` (${o.fuel_phase}, not ${ph})`} · ${App.pct(o.x_o2_ambient)} O2 · ${App.fmt(o.pressure_kpa, 0)} kPa` : '–'; } },
        { key: 'flags', label: 'Assumptions', sortable: false, fmt: (_, r) => h('div', { class: 'chips' },
          (r.conditions_unknown || []).length ? App.chip('not recorded', 'crit') : null,
          (r.conditions_from_range || []).length ? App.chip('from a range', 'warn') : null,
          (r.conditions_assumed_cabin_air || []).length ? App.chip('assumed cabin air', 'warn') : null) },
      ] }));

    root.append(App.panel('How the score is computed',
      App.eq('S = 100\\,\\frac{\\sum_k w_k\\,c_k}{\\sum_k w_k},\\quad c_k\\in[0,1] \\qquad c_{\\text{conditions}} = e^{-d/2},\\quad d=\\sqrt{\\left(\\frac{\\Delta x_{O_2}}{0.03}\\right)^2+\\left(\\frac{\\Delta p}{15\\,\\text{kPa}}\\right)^2+\\left(\\frac{\\Delta u}{10\\,\\text{cm/s}}\\right)^2}'),
      h('p', { class: 'muted small', text: `Weights: ${comps.map(k => `${k} ${d.weights[k]}`).join(', ')} (sum ${wsum.toFixed(2)}; gravity counts only for partial-gravity scenarios). It is a judgement that can be argued with, not a measurement.` })));
    root.append(App.notes((res.notes || []).filter(n => !/^Gap:/.test(n))));
  }

  function citeOf(ref) {
    const m = String(ref || '').match(/^\[?(PSI-\d+)\s+([FLQ])(\d+)\]?$/);
    return m ? { accession: m[1], section: { F: 'findings', L: 'limitations', Q: 'open_questions' }[m[2]], index: +m[3] } : null;
  }
})();
