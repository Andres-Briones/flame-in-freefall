/* Browser twin of fif.models.predict. Uses the per-unit coefficients from models.json, so it agrees with the
   fitted estimator up to the 4 significant figures the card stores. Returns {prediction: null} with the reason
   in `outside_domain`, `note` or `error` whenever predict() would not give a value or the card is not enough. */
function modelPredict(model, inputs, opts) {
  const m = model || {}, feats = Array.isArray(m.features) ? m.features : [], given = inputs || {};
  const out = { model_id: m.id, accession: m.accession, target: m.target, kind: m.kind, use: m.use,
    in_domain: false, outside_domain: {}, n_train: m.n, cv_metric: m.cv_metric, prediction: null };
  const names = feats.map(f => f.name);
  const missing = names.filter(n => given[n] == null || given[n] === '');
  const unknown = Object.keys(given).filter(n => !names.includes(n));
  if (!feats.length || missing.length || unknown.length) {
    out.error = `${m.id} needs exactly [${names.join(', ')}]; missing [${missing.join(', ')}], unknown [${unknown.join(', ')}]`;
    return out;
  }
  const x = feats.map(f => Number(given[f.name]));
  const bad = names.filter((n, j) => !isFinite(x[j]));
  if (bad.length) { out.error = `not a number: ${bad.join(', ')}`; return out; }
  feats.forEach((f, j) => {
    const d = Array.isArray(f.domain) ? f.domain : [], lo = d[0], hi = d[1];
    if (!(lo <= x[j] && x[j] <= hi)) out.outside_domain[f.name] = { value: x[j], min: lo, max: hi };
    (f.untested || []).forEach(g => {
      if (g.range[0] <= x[j] && x[j] <= g.range[1]) out.outside_domain[f.name] = { value: x[j], min: lo, max: hi,
        untested: g.range, reason: `only ${g.n_tests} training tests between ${g.range[0]} and ${g.range[1]}` };
    });
  });
  const impossible = feats.filter((f, j) => Array.isArray(f.allowed) && !f.allowed.includes(x[j]))
    .map(f => `${f.name} must be one of [${f.allowed.join(', ')}]`);
  const parts = (m.constraints || {}).sum_at_most_one;
  if (parts) {
    const total = parts.reduce((s, n) => s + Number(given[n]), 0);
    if (total > 1 + 1e-9) impossible.push(`${parts.join(' + ')} = ${total.toPrecision(3)}: mole fractions cannot sum to more than 1`);
  }
  if (impossible.length) { out.error = `impossible conditions: ${impossible.join('; ')}`; return out; }
  out.in_domain = Object.keys(out.outside_domain).length === 0;
  if (m.use === 'descriptive') {
    out.note = 'descriptive only: no held-out skill or too few rows; see the card’s table and caveats';
    if (m.descriptive_table) out.observed = m.descriptive_table;
    return out;
  }
  if (!out.in_domain && !(opts && opts.allowExtrapolation)) return out;

  const co = m.coefficients || {}, terms = Array.isArray(co.terms) ? co.terms : [];
  const pipe = ((m.estimator || {}).pipeline || []).join('+');
  const link = { classifier: 'StandardScaler+LogisticRegression', regressor: 'StandardScaler+LinearRegression' }[m.kind];
  const termName = f => f.transform ? `${f.transform}(${f.name})` : f.name;
  const problems = [];
  if (pipe !== link) problems.push(`estimator "${pipe || 'not stated'}" is not the linear pipeline this page can evaluate`);
  if (typeof co.intercept_per_unit !== 'number') problems.push('no intercept_per_unit');
  if (terms.length !== feats.length) problems.push('coefficient terms do not match the features');
  const z = feats.map((f, j) => {
    const t = terms.find(tt => tt.feature === termName(f));
    if (!t || typeof t.per_unit !== 'number') { problems.push(`no per-unit coefficient for ${termName(f)}`); return NaN; }
    if (f.transform == null) return x[j];
    if (f.transform === 'log10') {
      if (!(x[j] > 0)) problems.push(`log10 of a non-positive ${f.name}`);
      return Math.log10(x[j]);
    }
    problems.push(`unknown transform ${f.transform} on ${f.name}`);
    return NaN;
  });
  if (problems.length) { out.error = 'The exported card is not enough to reproduce predict(): ' + problems.join('; ') + '.'; return out; }
  const eta = feats.reduce((s, f, j) => s + terms.find(tt => tt.feature === termName(f)).per_unit * z[j], co.intercept_per_unit);
  if (m.kind === 'classifier') {
    const p = 1 / (1 + Math.exp(-eta));
    out.probability = p;
    out.prediction = p >= 0.5;
  } else {
    out.prediction = eta;
    const pi = m.prediction_interval || {}, q = pi.residual_quantiles || null;
    if (Array.isArray(q) && q.length === 2) {
      out.interval = [eta + q[0], eta + q[1]];
      if (typeof pi.floor === 'number') {
        const [low, high] = out.interval;
        out.interval_unclipped = [low, high];
        out.interval_low_unclipped = low;
        out.prediction_below_floor = eta < pi.floor;
        if (high < pi.floor) {
          out.interval = null;
          out.interval_clipped = false;
          out.interval_unavailable = `the whole range is below ${pi.floor}, which is impossible`;
        } else {
          out.interval = [Math.max(pi.floor, low), high];
          out.interval_clipped = low < pi.floor;
          out.interval_unavailable = null;
        }
      }
      out.interval_nominal = pi.nominal;
      out.interval_coverage = pi.held_out_coverage;
    }
    // predict() leaves a transformed target on its fitted scale; the page shows both.
    if (m.target_transform === 'log10') {
      out.target_scale = 'log10';
      out.back_transformed = Math.pow(10, eta);
      if (out.interval) out.back_transformed_interval = out.interval.map(v => Math.pow(10, v));
    } else if (m.target_transform) out.target_scale = m.target_transform;
  }
  return out;
}
App.modelPredict = modelPredict;

App.view({
  id: 'models', title: 'Models', tier: 2,
  heading: 'What predicts a test outcome, and how well?',
  intro: 'Eight small models, each fitted inside one investigation. Each card shows the question, how well it does on held-out test days against simple baselines, whether the coefficients agree with the physics, and where it must not be used.',
  needs: ['models'],
  brief: {
    need: 'Model cards that make the honest score and the physics check visible before any prediction, and a calculator that refuses to answer outside the fitted range. Scientists need to see which models are only descriptive.',
    data: ['data/export/models.json: models (8 cards) and dropped (7 candidates with the reason)', 'docs/models.md: the same cards as text, with the physics behind each feature'],
    call: 'predict(model_id="flex_burning_rate", is_heptane=1, x_o2_ambient=0.21, x_co2=0, x_he=0, pressure_kpa=101.3, d0_mm=3)\npredict()  # lists the models',
    keep: ['use: predictive or descriptive only (4 of 8 are descriptive and must not be used as calculators)', 'The grouped (held-out test day) score next to the baselines; never the in-sample score alone', 'Fitted on one investigation’s hardware and fuels; not a general flammability model', 'No value outside the fitted range of any feature; the range check does not cover untested combinations', 'Caveats and must-not-be-used-for, next to the result', 'x_o2_burner is a burner stream, not the atmosphere'],
    backend: 'The nearest real tests to a query (predict() returns 5 with their outcomes) need the training rows, which are not exported. The static page can compute the prediction itself from the card (App.modelPredict), up to the rounding of the stored coefficients.',
  },
  render(root, state, update) {
    const M = FIF.models || {}, models = Array.isArray(M.models) ? M.models : [], dropped = Array.isArray(M.dropped) ? M.dropped : [];
    const c = App.colors();
    if (!models.length) { root.append(h('p', { class: 'muted', text: 'models.json has no model cards.' })); return; }
    const m = models.find(x => x.id === state.model) || models[0];
    const metricOf = mm => (mm.cv_metric || {}).name;
    const grp = mm => (((mm.cv || {}).grouped_by_date || {})[metricOf(mm)]) || {};
    const ungrp = mm => (((mm.cv || {}).ungrouped || {})[metricOf(mm)]) || {};
    const comps = mm => ((mm.comparison_cv || {}).grouped_by_date) || {};
    const useChip = u => u === 'predictive' ? App.chip('predictive', 'good') : App.chip(u === 'descriptive' ? 'descriptive only' : (u || 'use not stated'), 'warn');
    const pm = (o, d) => o && typeof o.mean === 'number' ? `${App.fmt(o.mean, d)}${typeof o.sd === 'number' ? ' ± ' + App.fmt(o.sd, d) : ''}` : '–';

    root.append(App.table({ rows: models.map(mm => Object.assign({ _score: grp(mm).mean, _metric: metricOf(mm), _base: (comps(mm).majority_class || comps(mm).mean_predictor || {})[metricOf(mm)] }, mm)),
      pageSize: 10, onRow: r => update({ model: r.id }), cols: [
        { key: 'id', label: 'Model', fmt: (v, r) => h('span', { class: 'mono', style: r.id === m.id ? 'font-weight:700;color:var(--accent)' : '' }, v) },
        { key: 'accession', label: 'Investigation', fmt: v => App.name(v) },
        { key: 'kind', label: 'Kind' },
        { key: 'use', label: 'Use', fmt: v => useChip(v) },
        { key: 'n', label: 'n', num: true },
        { key: '_metric', label: 'Metric' },
        { key: '_score', label: 'Held-out days', num: true, fmt: (v, r) => pm(grp(r), 3) },
        { key: '_base', label: 'Baseline', num: true, sortable: false, fmt: v => pm(v, 3) } ] }));
    root.append(h('p', { class: 'muted small', text: 'Click a row to open its card. Baseline is the majority class (classifiers) or the mean (regressors).' }));

    const feats = Array.isArray(m.features) ? m.features : [];
    const co = m.coefficients || {}, terms = Array.isArray(co.terms) ? co.terms : [];
    const metric = metricOf(m) || 'score';

    root.append(App.panel(null,
      h('div', { class: 'chips' }, useChip(m.use), App.chip(m.kind || 'kind not stated'),
        m.accession ? App.chip(App.name(m.accession), '', () => App.go('investigation', { accession: m.accession })) : null,
        App.chip(`n = ${App.fmt(m.n)} tests`), App.chip(`${App.fmt(m.n_groups)} test days`)),
      h('h2', {}, App.tex(m.question || m.id)),
      h('dl', { class: 'kv' },
        h('dt', { text: 'model id' }), h('dd', { class: 'mono', text: m.id }),
        h('dt', { text: 'target' }), h('dd', {}, h('span', { class: 'mono', text: m.target || '–' }), m.target_definition ? h('span', {}, ': ', App.tex(m.target_definition)) : null),
        m.target_transform ? [h('dt', { text: 'target scale' }), h('dd', { text: `${m.target_transform} (fitted on ${m.target_transform}(${m.target}))` })] : null,
        h('dt', { text: 'estimator' }), h('dd', { text: ((m.estimator || {}).pipeline || []).join(' then ') || '–' }))));

    // Score against the comparison lines
    const order = [['this model', null], ['majority class', 'majority_class'], ['mean predictor', 'mean_predictor'], ['single best feature', 'single_best_feature_rule'],
      ['decision tree, depth 3', 'decision_tree_depth3'], ['gradient boosting', 'gradient_boosting']];
    const uc = ((m.comparison_cv || {}).ungrouped) || {};
    const scoreRows = order.map(([label, key]) => {
      const g = key ? (comps(m)[key] || {})[metric] : grp(m), u = key ? (uc[key] || {})[metric] : ungrp(m);
      return g || u ? { label, g, u, mine: !key } : null;
    }).filter(Boolean);
    root.append(App.panel(`Cross-validated ${metric}`,
      h('p', { class: 'muted small', text: `Held out by test day: ${(m.cv_scheme || {}).grouped_by_date || 'grouped by date'}. Shuffled: ${(m.cv_scheme || {}).ungrouped || 'ungrouped'}. The gap between the two columns is the optimism from same-day tests. ${metric === 'r2' ? 'R² below 0 is worse than predicting the mean.' : metric === 'roc_auc' ? 'ROC AUC 0.5 is no skill.' : ''}` }),
      App.table({ rows: scoreRows, pageSize: 10, cols: [
        { key: 'label', label: 'Model', sortable: false, fmt: (v, r) => r.mine ? h('b', { text: v }) : v },
        { key: 'g', label: 'Held-out days, mean ± SD', num: true, sortable: false, fmt: (v, r) => r.mine ? h('b', { text: pm(v, 3) }) : pm(v, 3) },
        { key: 'gp', label: 'pooled', num: true, sortable: false, fmt: (v, r) => App.fmt((r.g || {}).pooled, 3) },
        { key: 'u', label: 'Shuffled, mean', num: true, sortable: false, fmt: v => App.fmt((v || {}).mean, 3) } ] }),
      typeof (m.cv_metric || {}).brier_grouped_pooled === 'number' ? h('p', { class: 'small', text: `Brier score of the probabilities on held-out days (pooled, lower is better): ${App.fmt(m.cv_metric.brier_grouped_pooled, 3)}, against ${App.fmt(m.cv_metric.brier_baseline_grouped_pooled, 3)} for always giving the base rate. AUC only ranks the tests; Brier also penalises probabilities that are off.` }) : null));

    // Features and coefficients
    const termFor = f => terms.find(t => t.feature === (f.transform ? `${f.transform}(${f.name})` : f.name));
    root.append(App.panel('Inputs, fitted range and expected sign',
      App.table({ rows: feats.map(f => Object.assign({ _lo: (f.domain || [])[0], _hi: (f.domain || [])[1] }, f)), pageSize: 20, cols: [
        { key: 'name', label: 'Feature', fmt: v => h('span', { class: 'mono', text: v }) },
        { key: 'unit', label: 'Unit' },
        { key: 'transform', label: 'Transform', fmt: v => v || 'none' },
        { key: '_lo', label: 'Fitted min', num: true }, { key: '_hi', label: 'Fitted max', num: true },
        { key: 'expected_sign', label: 'Expected', fmt: v => v || '?' },
        { key: 'why', label: 'Why', fmt: v => v ? App.tex(v) : '–' } ] })));

    const agreeKind = a => /^agrees$/.test(a || '') ? 'good' : /oppos|disagree|wrong/.test(a || '') ? 'crit' : /no prior/.test(a || '') ? '' : 'warn';
    const ct = terms.filter(t => typeof t.per_sd === 'number');
    const ci = t => Array.isArray(t.per_sd_ci95_cluster_bootstrap) ? t.per_sd_ci95_cluster_bootstrap : [null, null];
    const coefPlot = h('div', {});
    if (ct.length) {
      App.plot(coefPlot, [{ type: 'scatter', mode: 'markers', name: 'coefficient per SD', y: ct.map(t => t.feature), x: ct.map(t => t.per_sd),
        error_x: { type: 'data', symmetric: false, color: c.fg3, thickness: 1.5, width: 4,
          array: ct.map(t => typeof ci(t)[1] === 'number' ? ci(t)[1] - t.per_sd : 0), arrayminus: ct.map(t => typeof ci(t)[0] === 'number' ? t.per_sd - ci(t)[0] : 0) },
        marker: { size: 11, color: c.accent },
        text: ct.map(t => `${t.feature}<br>${App.fmt(t.per_sd, 3)} per SD, 95% CI ${App.fmt(ci(t)[0], 3)} to ${App.fmt(ci(t)[1], 3)}<br>per unit ${App.fmt(t.per_unit, 4)}<br>expected ${t.expected_sign || '?'}: ${t.agreement || '–'}`),
        hovertemplate: '%{text}<extra></extra>' }],
      { height: 80 + ct.length * 42, hovermode: 'closest', showlegend: false, margin: { l: 180, r: 24, t: 8, b: 48 },
        xaxis: { title: `change in ${co.scale || 'target'} for +1 SD of the feature`, zeroline: true, zerolinewidth: 2 },
        yaxis: { type: 'category', autorange: 'reversed' } });
    }
    root.append(App.panel('Coefficients and the physics check',
      h('p', { class: 'muted small', text: `Per standard deviation of each feature, on the ${co.scale || 'target'} scale, with 95% intervals from a bootstrap over test days. Agrees means the sign matches the physics and the interval excludes 0.` }),
      ct.length ? coefPlot : h('p', { class: 'muted', text: 'No coefficients in the card.' }),
      App.table({ rows: terms, pageSize: 20, cols: [
        { key: 'feature', label: 'Term', fmt: v => h('span', { class: 'mono', text: v }) },
        { key: 'per_sd', label: 'Per SD', num: true, fmt: v => App.fmt(v, 3) },
        { key: 'ci', label: '95% CI', num: true, sortable: false, fmt: (_, t) => `${App.fmt(ci(t)[0], 3)} to ${App.fmt(ci(t)[1], 3)}` },
        { key: 'per_unit', label: 'Per unit', num: true, fmt: v => App.fmt(v, 4) },
        { key: 'expected_sign', label: 'Expected' },
        { key: 'agreement', label: 'Verdict', fmt: v => v ? App.chip(v, agreeKind(v)) : '–' } ] }),
      h('p', { class: 'small muted', text: `Intercept per unit: ${App.fmt(co.intercept_per_unit, 4)}.` }),
      m.interpretation ? h('div', { class: 'callout' }, h('b', { text: 'Does it match the physics? ' }), App.tex(m.interpretation)) : null));

    if (Array.isArray(m.descriptive_table) && m.descriptive_table.length) {
      const d0 = m.descriptive_table[0], keyCols = Object.keys(d0).filter(k => !['n', 'positives', 'fraction', 'wilson95'].includes(k));
      root.append(App.panel('Observed fractions (the robust statement)',
        App.table({ rows: m.descriptive_table, pageSize: 20, cols: [
          ...keyCols.map(k => ({ key: k, label: k.replace(/_/g, ' ') })),
          { key: 'positives', label: 'Positives', num: true }, { key: 'n', label: 'n', num: true },
          { key: 'fraction', label: 'Fraction', num: true, fmt: v => App.fmt(v, 2) },
          { key: 'wilson95', label: 'Wilson 95%', num: true, sortable: false, fmt: v => Array.isArray(v) ? `${App.fmt(v[0], 2)} to ${App.fmt(v[1], 2)}` : '–' } ] })));
    }

    root.append(m.use === 'predictive' ? tryIt() : App.panel('No calculator for this model',
      h('p', { text: `This model did not hold up in cross-validation (held-out ${metric} ${pm(grp(m), 3)}), so it is descriptive only. Use the observed table and the coefficient signs, not a predicted value.` })));

    if (Array.isArray(m.training_filter) && m.training_filter.length) {
      root.append(App.panel('Training rows', h('ul', { style: 'margin:0;padding-left:18px' }, m.training_filter.map(s =>
        h('li', { class: 'small' }, s.step ? `${s.step}: ${App.fmt(s.rows)}` : `excluded ${App.fmt(s.excluded)}: `, s.why ? App.tex(s.why) : '')))));
    }
    root.append(App.notes([...(m.caveats || []), ...(m.must_not_be_used_for || []).map(x => 'Must not be used for: ' + x)], 'Caveats and what this model must not be used for'));

    if (dropped.length) {
      root.append(App.panel('Candidate models that were dropped, and why',
        App.table({ rows: dropped, pageSize: 20, cols: [
          { key: 'id', label: 'Candidate', fmt: v => h('span', { class: 'mono', text: v || '–' }) },
          { key: 'accession', label: 'Investigation', fmt: v => App.name(v) },
          { key: 'reason', label: 'Reason', fmt: v => v ? App.tex(v) : '–' } ] })));
    }

    function tryIt() {
      const wide = !!state.wide;
      const all = Object.assign({}, state.inputs || {});
      const cur = Object.assign({}, all[m.id] || {});
      const choices = f => {
        const pairs = [...String(f.unit || '').matchAll(/(\d+)\s+([A-Za-z][\w-]*)/g)].map(a => [a[1], `${a[1]} (${a[2]})`]);
        const lo = Math.ceil((f.domain || [0])[0]), hi = Math.floor((f.domain || [0, 0])[1]);
        const ints = []; for (let v = lo; v <= hi && ints.length < 20; v++) ints.push(v);
        return ints.map(v => (pairs.find(p => +p[0] === v) || [String(v), String(v)]));
      };
      const discrete = f => /^(is_|n_)/.test(f.name) && Array.isArray(f.domain) && Number.isInteger(f.domain[0]) && Number.isInteger(f.domain[1]);
      for (const f of feats) {
        if (cur[f.name] != null) continue;
        const [lo, hi] = f.domain || [0, 1];
        cur[f.name] = discrete(f) ? Math.ceil(lo) : f.transform === 'log10' && lo > 0 ? Math.pow(10, (Math.log10(lo) + Math.log10(hi)) / 2) : (lo + hi) / 2;
      }
      const setInput = (name, v) => { all[m.id] = Object.assign({}, cur, { [name]: v }); update({ inputs: all }); };
      const ctl = feats.map((f, j) => {
        const [lo, hi] = f.domain || [0, 1];
        const id = `mo-${m.id}-${f.name}`.replace(/[^\w-]/g, '-');
        const label = `${f.name} (${f.unit || 'no unit'})`;
        if (discrete(f)) return App.select({ id, label, options: choices(f), value: String(cur[f.name]), onChange: v => setInput(f.name, Number(v)) });
        let min = lo, max = hi;
        if (wide) {
          const span = hi - lo;
          min = f.transform === 'log10' ? lo / 1.5 : lo >= 0 ? Math.max(0, lo - 0.25 * span) : lo - 0.25 * span;
          max = f.transform === 'log10' ? hi * 1.5 : hi + 0.25 * span;
        }
        const step = (max - min) / 200;
        return App.range({ id, label, min, max, step, value: cur[f.name], onChange: v => setInput(f.name, wide ? v : Math.min(hi, Math.max(lo, v))), format: v => App.fmt(v) });
      });
      const r = modelPredict(m, cur);
      const unit = (/_mm2_s$/.test(m.target) && 'mm²/s') || (/_mm$/.test(m.target) && 'mm') || (/_s$/.test(m.target) && 's') || (/_kpa$/.test(m.target) && 'kPa') || '';
      let result;
      if (r.error) result = h('div', { class: 'callout gap' }, h('b', { text: 'No value. ' }), r.error);
      else if (!r.in_domain) {
        result = h('div', { class: 'callout gap' }, h('b', { text: 'Outside the fitted range, so no value (as predict() does). ' }),
          Object.entries(r.outside_domain).map(([n, o]) => o.reason ? `${n} = ${App.fmt(o.value)}: ${o.reason}. ` : `${n} = ${App.fmt(o.value)} is outside ${App.fmt(o.min)} to ${App.fmt(o.max)}. `),
          'The backend also returns the nearest real tests; they are not in the static export.');
      } else if (m.kind === 'classifier') {
        result = h('div', { class: 'tile' }, h('b', { text: App.pct(r.probability, 0) }),
          h('span', { text: `probability that ${m.target} = 1 (${r.prediction ? 'more likely yes' : 'more likely no'})` }));
      } else {
        const y = r.back_transformed != null ? r.back_transformed : r.prediction, iv = r.back_transformed_interval || r.interval;
        const cov = r.interval_coverage, lv = cov && cov.by ? Object.entries(cov.by.levels || {}) : [];
        const share = o => `${o.n_inside} of ${o.n}`, nominal = cov ? App.pct(cov.nominal, 0) : '90%';
        const low = lv.filter(([, o]) => o.verdict === 'below nominal').map(([k]) => k);
        if (cov && cov.verdict === 'below nominal') low.unshift('these tests');
        result = h('div', {}, h('div', { class: 'tile' }, h('b', { text: `${App.fmt(y, 3)} ${unit}` }),
          h('span', { text: `${m.target}${iv ? `; range ${App.fmt(iv[0], 3)} to ${App.fmt(iv[1], 3)} ${unit} (target ${nominal} of held-out errors)` : ''}` })),
          cov ? h('p', { class: 'small', text: `Measured on held-out test days the range held ${share(cov)} tests${lv.length ? ' (' + lv.map(([k, o]) => `${k} ${share(o)}`).join(', ') + ')' : ''}; ${nominal} is the target, not the result.${low.length ? ` It is too narrow for ${low.join(' and ')}.` : ''}` }) : null,
          r.interval_clipped ? h('p', { class: 'small', text: `The lower end was cut at 0 (it came out at ${App.fmt(r.interval_low_unclipped, 3)} ${unit}): the quantity cannot be negative.` }) : null,
          r.interval_unavailable ? h('p', { class: 'small', text: `Range not available: the whole range came out below 0 (${App.fmt(r.interval_unclipped[0], 3)} to ${App.fmt(r.interval_unclipped[1], 3)} ${unit}), which is impossible.` }) : null,
          r.prediction_below_floor ? h('div', { class: 'callout gap' }, h('b', { text: 'Do not use this value. ' }), 'The estimate itself is below 0, which is impossible: each input is inside its fitted range, but this combination was not tested.') : null);
      }
      return App.panel('Try it',
        h('div', { class: 'row' }, ctl),
        h('label', { class: 'ctl', style: 'flex-direction:row;align-items:center;gap:6px' },
          h('input', { id: 'mo-wide', type: 'checkbox', checked: wide, onchange: e => update({ wide: e.target.checked }) }),
          'Let the sliders go 25% past the fitted range (to see the refusal)'),
        result,
        h('p', { class: 'small', text: 'Fitted on one investigation’s hardware and fuels; not a general flammability model.' }),
        h('p', { class: 'muted small', text: 'Computed in the browser from the card’s per-unit coefficients (rounded to 4 significant figures), so it can differ from predict() in the third decimal. The range check is per feature: a combination never tested can still pass it.' }));
    }
  },
});
