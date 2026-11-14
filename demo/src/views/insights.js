App.view({
  id: 'insights', title: 'Insights', tier: 2,
  heading: 'What do the 24 investigations say together?',
  intro: 'Cross-investigation results: measured limits, microgravity against 1 g, ranked gaps, open research questions, how the investigations build on each other, and the parameter ranges each one covered.',
  needs: [],
  brief: {
    need: 'One place for the conclusions that span investigations: limit values with their conditions, how microgravity changes the hazard, what is still unknown and in what order, and the ranges each investigation covered. Every row must lead back to its quoted source.',
    data: ['data/export/synthesis.json: limits (35), micro_vs_1g (28), gaps (13), research_questions (20), lineage (35), parameter_coverage (51)', 'data/export/records.json to resolve citations', 'data/export/investigations.json for names and fuel phases'],
    call: 'insights(topic="limits")\ninsights(topic="micro_vs_1g")\ninsights(topic="gaps")\ninsights(topic="research_questions")\ninsights(topic="lineage")\ninsights(topic="parameter_coverage", accession="PSI-25")',
    keep: ['The conditions next to every limit value (a limit without its O2, pressure and flow is meaningless)', 'Citation chips on every row', 'Microgravity and 1-g values are text with ranges and qualifiers; do not turn them into numbers', 'Burner-stream O2 (inverse flames) is not an ambient atmosphere and has its own parameter row', 'Limit values marked as model or theory are not measurements'],
    backend: 'Nothing: all six sections are static in synthesis.json. A backend is only needed to search across them in free text.',
  },
  render(root, state, update) {
    const S = FIF.synthesis || {};
    const c = App.colors();
    const arr = k => Array.isArray(S[k]) ? S[k] : [];
    const tabs = [['limits', 'Measured limits'], ['micro', 'Microgravity vs 1 g'], ['gaps', 'Ranked gaps'],
      ['questions', 'Research questions'], ['lineage', 'Lineage'], ['ranges', 'Parameter ranges']];
    const tab = tabs.some(t => t[0] === state.tab) ? state.tab : 'limits';
    root.append(h('div', { class: 'row' },
      App.seg({ id: 'ins-tab', label: 'Section', options: tabs, value: tab, onChange: v => update({ tab: v }) })));

    const phaseOfAcc = acc => { const p = App.inv(acc).fuel_phases || []; return p.length === 1 && p[0] in App.PHASE_SLOT ? p[0] : 'other'; };
    const baseOfPhase = p => { const w = String(p || '').split(/[\s(]/)[0]; return w in App.PHASE_SLOT ? w : 'other'; };
    const txt = v => v == null || v === '' ? '–' : App.tex(v);
    const accBtn = acc => acc ? App.chip(App.name(acc), '', () => App.go('investigation', { accession: acc })) : '–';
    const empty = what => h('p', { class: 'muted', text: `No ${what} in synthesis.json.` });

    if (tab === 'limits') drawLimits();
    else if (tab === 'micro') drawMicro();
    else if (tab === 'gaps') drawGaps();
    else if (tab === 'questions') drawQuestions();
    else if (tab === 'lineage') drawLineage();
    else drawRanges();

    function drawLimits() {
      const all = arr('limits');
      if (!all.length) { root.append(empty('limits')); return; }
      const count = (list, key) => list.reduce((m, r) => m.set(r[key], (m.get(r[key]) || 0) + 1), new Map());
      const types = [...count(all, 'limit_type').entries()].sort((a, b) => String(a[0]).localeCompare(String(b[0])));
      const ltype = types.some(t => t[0] === state.ltype) ? state.ltype : '';
      const rows = ltype ? all.filter(r => r.limit_type === ltype) : all;
      const units = [...count(rows.filter(r => typeof r.value === 'number'), 'unit').entries()].sort((a, b) => b[1] - a[1]);
      const unit = units.some(u => u[0] === state.lunit) ? state.lunit : (units[0] || [null])[0];

      root.append(h('div', { class: 'row' },
        App.select({ id: 'ins-ltype', label: 'Limit type', value: ltype, onChange: v => update({ ltype: v }),
          options: [['', `All limit types (${all.length})`], ...types.map(([t, n]) => [t, `${t} (${n})`])] }),
        units.length ? App.select({ id: 'ins-lunit', label: 'Chart: values in', value: unit, onChange: v => update({ lunit: v }),
          options: units.map(([u, n]) => [u, `${u} (${n})`]) }) : null));

      const pts = rows.filter(r => r.unit === unit && typeof r.value === 'number' && isFinite(r.value));
      if (pts.length) {
        const label = r => `${r.fuel || '?'} · ${r.limit_type || '?'}`;
        const cats = [...new Set(pts.slice().sort((a, b) => a.value - b.value).map(label))];
        const phases = [...new Set(pts.map(r => phaseOfAcc(r.accession)))];
        const traces = phases.map(p => {
          const sel = pts.filter(r => phaseOfAcc(r.accession) === p);
          return { type: 'scatter', mode: 'markers', name: p === 'other' ? 'aerosol or mixed' : p + ' fuel',
            x: sel.map(r => r.value), y: sel.map(label), customdata: sel.map(r => pts.indexOf(r)),
            text: sel.map(r => `${r.fuel || '?'}<br>${r.limit_type || '?'}: ${App.fmt(r.value)} ${r.unit || ''}<br>${r.conditions || ''}<br>${App.name(r.accession)}`),
            hovertemplate: '%{text}<extra></extra>',
            marker: { size: 11, color: App.phaseColor(p), line: { color: c.surface, width: 1 } } };
        });
        const plot = h('div', {});
        App.plot(plot, traces, { height: Math.max(240, 70 + cats.length * 24), hovermode: 'closest', showlegend: traces.length > 1,
          margin: { l: 220, r: 24, t: 8, b: 48 }, legend: { orientation: 'h', y: 1.02, yanchor: 'bottom', x: 0 },
          xaxis: { title: `limit value (${unit})` }, yaxis: { type: 'category', categoryorder: 'array', categoryarray: cats } },
          pt => { const r = pts[pt && pt.customdata]; if (r && r.citation) App.openCite(r.citation); });
        root.append(App.panel(`Limits measured in ${unit}`, plot,
          h('p', { class: 'muted small', text: `${pts.length} of ${rows.length} limits shown; the others use a different unit. Colour is the fuel phase of the investigation. Click a dot for its source.` })));
      }

      root.append(App.table({ rows, pageSize: 40, sort: { key: 'limit_type', dir: 1 }, cols: [
        { key: 'limit_type', label: 'Limit' },
        { key: 'fuel', label: 'Fuel' },
        { key: 'value', label: 'Value', num: true, fmt: v => App.fmt(v) },
        { key: 'unit', label: 'Unit' },
        { key: 'conditions', label: 'Conditions', width: '220px', fmt: v => txt(v) },
        { key: 'accession', label: 'Investigation', fmt: v => App.name(v) },
        { key: 'citation', label: 'Source', sortable: false, fmt: v => v ? App.cite(v) : '–' } ] }));
      root.append(App.notes(['Each value holds only under the conditions next to it (O2, pressure, flow, geometry).',
        'Rows marked model, theory or drop tower in the fuel or conditions are not microgravity flight measurements.',
        'Mole fraction 0.135 means 13.5% O2.']));
    }

    function drawMicro() {
      const all = arr('micro_vs_1g');
      if (!all.length) { root.append(empty('microgravity comparisons')); return; }
      const group = d => {
        const s = String(d || '').toLowerCase().trim();
        if (s.startsWith('more hazardous')) return ['more hazardous', 'crit'];
        if (s.startsWith('less hazardous')) return ['less hazardous', 'good'];
        if (/^(same|about equal|similar|no gravity effect)/.test(s)) return ['about the same', ''];
        if (/unresolved|not a hazard metric/.test(s)) return ['unresolved or not a hazard metric', ''];
        return ['different, read the row', 'warn'];
      };
      const order = ['more hazardous', 'less hazardous', 'about the same', 'different, read the row', 'unresolved or not a hazard metric'];
      const counts = new Map(order.map(k => [k, 0]));
      for (const r of all) counts.set(group(r.direction)[0], counts.get(group(r.direction)[0]) + 1);
      const gsel = order.includes(state.mgroup) ? state.mgroup : '';
      root.append(h('div', { class: 'grid tiles' }, order.filter(k => counts.get(k)).map(k =>
        h('button', { type: 'button', class: 'tile', style: `text-align:left;cursor:pointer;${gsel === k ? 'border-color:var(--accent)' : ''}`,
          'aria-pressed': String(gsel === k), onclick: () => update({ mgroup: gsel === k ? '' : k }) },
          h('b', { text: String(counts.get(k)) }), h('span', { text: k })))));
      const rows = (gsel ? all.filter(r => group(r.direction)[0] === gsel) : all);
      root.append(h('p', { class: 'muted small', text: `${rows.length} of ${all.length} comparisons${gsel ? ' (' + gsel + '; click the tile again to show all)' : '. Click a tile to filter'}. The direction is the reviewers' reading of the sources, kept as written.` }));

      const clean = v => typeof v === 'number' ? v : (typeof v === 'string' && /^\s*-?\d+(\.\d+)?\s*$/.test(v) ? parseFloat(v) : null);
      const pairs = all.filter(r => clean(r.microgravity) != null && clean(r.one_g) != null);
      if (pairs.length >= 2) {
        const lab = pairs.map(r => `${r.material} · ${r.quantity}`);
        const plot = h('div', {});
        App.plot(plot, [
          { type: 'scatter', mode: 'markers', name: 'microgravity', y: lab, x: pairs.map(r => clean(r.microgravity)), marker: { size: 11, color: c.s[0] }, hovertemplate: '%{y}<br>microgravity %{x}<extra></extra>' },
          { type: 'scatter', mode: 'markers', name: '1 g', y: lab, x: pairs.map(r => clean(r.one_g)), marker: { size: 11, color: c.s[1], symbol: 'diamond' }, hovertemplate: '%{y}<br>1 g %{x}<extra></extra>' }],
          { height: 80 + pairs.length * 30, hovermode: 'closest', margin: { l: 220, r: 24, t: 8, b: 48 }, xaxis: { title: 'value (units differ per row)' } });
        root.append(App.panel('Rows with a plain number on both sides', plot));
      } else {
        root.append(h('p', { class: 'muted small', text: `No chart: only ${pairs.length} of ${all.length} rows have a plain number on both sides${pairs.length ? ' (' + pairs.map(r => r.material + ', ' + r.quantity).join('; ') + ')' : ''}. The others carry ranges, ratios or words, so they are shown as written.` }));
      }

      root.append(App.table({ rows, pageSize: 30, cols: [
        { key: 'material', label: 'Material or flame' },
        { key: 'quantity', label: 'Quantity' },
        { key: 'microgravity', label: 'Microgravity', fmt: v => txt(v) },
        { key: 'one_g', label: '1 g', fmt: v => txt(v) },
        { key: 'direction', label: 'Microgravity is', fmt: v => v ? App.chip(v, group(v)[1]) : '–' },
        { key: 'citations', label: 'Sources', sortable: false, fmt: v => App.cites(v) || '–' } ] }));
      root.append(App.notes(['Values are quoted as the sources give them, with ranges, qualifiers and units in the text.',
        'Some rows compare a flight result with a model or a drop-tower test; the material column says so.',
        'In these rows, more hazardous means a lower O2 limit or spread where the 1-g test did not spread. It is not a rule for every material.']));
    }

    function drawGaps() {
      const all = arr('gaps').slice().sort((a, b) => (a.rank ?? 1e9) - (b.rank ?? 1e9));
      if (!all.length) { root.append(empty('gaps')); return; }
      root.append(h('ol', { class: 'stack', style: 'margin:0;padding-left:22px' }, all.map(g =>
        h('li', {}, h('div', { class: 'panel' },
          h('h3', {}, App.tex(g.gap || '–')),
          g.why && h('p', {}, h('b', { text: 'Why it matters. ' }), App.tex(g.why)),
          g.partial_fill && h('p', { class: 'small' }, h('span', { class: 'muted', text: 'Partly filled by: ' }), App.tex(g.partial_fill)),
          App.cites(g.citations))))));
      root.append(App.notes(['The order is the reviewers’ judgement of importance for exploration habitats, not a computed score.']));
    }

    function drawQuestions() {
      const all = arr('research_questions');
      if (!all.length) { root.append(empty('research questions')); return; }
      root.append(h('div', { class: 'grid two' }, all.map((q, i) => App.panel(null,
        h('h3', {}, `${i + 1}. `, App.tex(q.question || '–')),
        (q.accessions || []).length ? h('div', { class: 'chips' }, q.accessions.map(accBtn)) : null,
        h('dl', { class: 'kv' },
          h('dt', { text: 'data needed' }), h('dd', {}, txt(q.data_needed)),
          h('dt', { text: 'expected result' }), h('dd', {}, txt(q.expected))),
        App.cites(q.citations)))));
      root.append(App.notes(['These are questions the archived data could answer with more analysis. Most need files beyond the tests table (named under data needed).']));
    }

    function drawLineage() {
      const all = arr('lineage').filter(r => r && r.from && r.to);
      if (!all.length) { root.append(empty('lineage relations')); return; }
      const num = a => parseInt(String(a).replace(/\D+/g, ''), 10) || 0;
      const nodes = [...new Set([...(FIF.investigations || []).map(i => i.accession), ...all.flatMap(r => [r.from, r.to])])].sort((a, b) => num(a) - num(b));
      const pos = new Map(nodes.map((a, i) => { const t = Math.PI / 2 - 2 * Math.PI * i / nodes.length; return [a, [Math.cos(t), Math.sin(t)]]; }));
      const ann = all.map(r => { const [x0, y0] = pos.get(r.from), [x1, y1] = pos.get(r.to);
        return { x: x1, y: y1, ax: x0, ay: y0, xref: 'x', yref: 'y', axref: 'x', ayref: 'y', text: '', showarrow: true,
          arrowhead: 2, arrowsize: 1, arrowwidth: 1.2, arrowcolor: c.neutral, standoff: 9, startstandoff: 9 }; });
      const mids = { type: 'scatter', mode: 'markers', name: 'relation', showlegend: false,
        x: all.map(r => (pos.get(r.from)[0] + pos.get(r.to)[0]) / 2), y: all.map(r => (pos.get(r.from)[1] + pos.get(r.to)[1]) / 2),
        marker: { size: 7, color: c.neutral, symbol: 'circle-open' },
        text: all.map(r => `${App.name(r.from)}<br>${r.relation || 'related'}<br>${App.name(r.to)}`), hovertemplate: '%{text}<extra></extra>' };
      const phases = [...new Set(nodes.map(phaseOfAcc))];
      const nodeTraces = phases.map(p => {
        const sel = nodes.filter(a => phaseOfAcc(a) === p);
        return { type: 'scatter', mode: 'markers+text', name: p === 'other' ? 'aerosol or mixed' : p,
          x: sel.map(a => pos.get(a)[0]), y: sel.map(a => pos.get(a)[1]), customdata: sel,
          text: sel.map(a => App.inv(a).acronym || a), textposition: sel.map(a => pos.get(a)[1] >= 0 ? 'top center' : 'bottom center'),
          textfont: { color: c.fg, size: 11 }, hovertext: sel.map(a => `${App.name(a)}<br>${all.filter(r => r.from === a || r.to === a).length} relations`),
          hovertemplate: '%{hovertext}<extra></extra>', marker: { size: 14, color: App.phaseColor(p), line: { color: c.surface, width: 2 } } };
      });
      const plot = h('div', {});
      App.plot(plot, [mids, ...nodeTraces], { height: 560, hovermode: 'closest', annotations: ann, showlegend: true,
        margin: { l: 16, r: 16, t: 24, b: 40 }, legend: { orientation: 'h', y: -0.04, x: 0 },
        xaxis: { visible: false, range: [-1.35, 1.35] }, yaxis: { visible: false, range: [-1.3, 1.3], scaleanchor: 'x' } },
        pt => { if (pt && typeof pt.customdata === 'string') App.go('investigation', { accession: pt.customdata }); });
      root.append(App.panel('How the investigations connect', plot,
        h('p', { class: 'muted small', text: 'Arrows point from the first investigation to the second in each relation. Hover the small rings on the arrows for the relation; click an investigation to open it. Node colour is the fuel phase.' })));
      const rows = all.map(r => Object.assign({ fromName: App.name(r.from), toName: App.name(r.to) }, r));
      root.append(App.table({ rows, pageSize: 40, sort: { key: 'relation', dir: 1 }, onRow: r => App.go('investigation', { accession: r.from }), cols: [
        { key: 'fromName', label: 'From' }, { key: 'relation', label: 'Relation' }, { key: 'toName', label: 'To' } ] }));
    }

    function drawRanges() {
      const all = arr('parameter_coverage');
      if (!all.length) { root.append(empty('parameter ranges')); return; }
      const counts = all.reduce((m, r) => m.set(r.parameter, (m.get(r.parameter) || 0) + 1), new Map());
      const params = [...counts.entries()].sort((a, b) => b[1] - a[1] || String(a[0]).localeCompare(String(b[0])));
      const param = counts.has(state.param) ? state.param : params[0][0];
      root.append(h('div', { class: 'row' }, App.select({ id: 'ins-param', label: 'Parameter', value: param, onChange: v => update({ param: v }),
        options: params.map(([p, n]) => [p, `${p} (${n})`]) })));
      const rows = all.filter(r => r.parameter === param);
      const units = [...new Set(rows.map(r => r.unit))];
      const unit = units.slice().sort((a, b) => rows.filter(r => r.unit === b).length - rows.filter(r => r.unit === a).length)[0];
      const isNum = v => typeof v === 'number' && isFinite(v);
      const drawn = rows.filter(r => r.unit === unit && (isNum(r.min) || isNum(r.max)));
      if (drawn.length) {
        const seen = new Map();
        const label = r => { const base = App.name(r.accession); const k = (seen.get(base) || 0) + 1; seen.set(base, k); return k > 1 ? `${base} #${k}` : base; };
        const labels = drawn.map(label);
        const bases = [...new Set(drawn.map(r => baseOfPhase(r.fuel_phase)))];
        const traces = bases.map(b => {
          const x = [], y = [], text = [];
          drawn.forEach((r, i) => {
            if (baseOfPhase(r.fuel_phase) !== b) return;
            const lo = isNum(r.min) ? r.min : r.max, hi = isNum(r.max) ? r.max : r.min;
            const t = `${labels[i]}<br>${App.fmt(r.min)} to ${App.fmt(r.max)} ${r.unit || ''}<br>${r.fuel_phase || 'phase not stated'}${r.note ? '<br>' + r.note : ''}`;
            x.push(lo, hi, null); y.push(labels[i], labels[i], null); text.push(t, t, null);
          });
          return { type: 'scatter', mode: 'lines+markers', name: b === 'other' ? 'other or model' : b + ' fuel', x, y, text, connectgaps: false,
            hovertemplate: '%{text}<extra></extra>', line: { color: App.phaseColor(b), width: 8 }, marker: { size: 10, color: App.phaseColor(b) } };
        });
        const plot = h('div', {});
        App.plot(plot, traces, { height: Math.max(220, 70 + labels.length * 30), hovermode: 'closest', showlegend: traces.length > 1,
          margin: { l: 170, r: 24, t: 8, b: 48 }, legend: { orientation: 'h', y: 1.02, yanchor: 'bottom', x: 0 },
          xaxis: { title: `${param} (${unit || 'no unit'})` }, yaxis: { type: 'category', categoryorder: 'array', categoryarray: labels.slice().reverse() } });
        root.append(App.panel(`Range covered by each investigation: ${param}`, plot,
          drawn.length < rows.length ? h('p', { class: 'muted small', text: `${rows.length - drawn.length} rows are not drawn: a different unit or no numeric range.` }) : null));
      }
      root.append(App.table({ rows, pageSize: 30, cols: [
        { key: 'accession', label: 'Investigation', fmt: v => App.name(v) },
        { key: 'min', label: 'Min', num: true }, { key: 'max', label: 'Max', num: true },
        { key: 'unit', label: 'Unit' }, { key: 'fuel_phase', label: 'Fuel phase' },
        { key: 'note', label: 'Note', fmt: v => txt(v) },
        { key: 'citations', label: 'Sources', sortable: false, fmt: v => App.cites(v) || '–' } ] }));
      const keep = ['A range is the span of the whole investigation, not a grid of tests: the corners may be untested.'];
      if (/burner/i.test(param)) keep.unshift('Burner-stream O2 is the oxidiser fed through the burner in inverse flames. It is not the cabin atmosphere and must not be compared with ambient O2.');
      if (/1-g|ground/i.test(param)) keep.unshift('These are 1-g ground tests, not microgravity.');
      root.append(App.notes(keep));
    }
  },
});
