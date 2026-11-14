(function () {
  const KINDS = [['pdf', 'PDF'], ['video', 'Video'], ['image', 'Image'], ['table', 'Table'], ['text', 'Text'], ['other', 'Other']];
  const KIND_LABEL = Object.fromEntries(KINDS);
  const MISSING_AT_LAST_DOWNLOAD = 44;
  const cache = {};
  let totals = null;

  const bytes = n => (App.fmtBytes ? App.fmtBytes(n) : App.fmt(n) + ' B');
  const extOf = f => ((String(f).match(/\.([A-Za-z0-9]+)$/) || [, ''])[1] || '').toLowerCase();

  // Flat, cached file list of one investigation. `short` drops the "PSI-NN_<category>_" prefix PSI adds to every name.
  function filesOf(acc) {
    if (cache[acc]) return cache[acc];
    const out = [];
    const cats = (FIF.files || {})[acc] || {};
    for (const category of Object.keys(cats)) {
      const prefix = `${acc}_${category}_`;
      for (const [name, size] of cats[category]) {
        out.push({ name, short: name.startsWith(prefix) && name.length > prefix.length ? name.slice(prefix.length) : name,
          category, kind: App.fileKind(name), size: typeof size === 'number' ? size : null, lname: name.toLowerCase() });
      }
    }
    return cache[acc] = out;
  }

  function catalogueTotals() {
    if (totals) return totals;
    const t = { files: 0, zip: 0, ts: 0, kindBytes: {}, kindCount: {} };
    for (const acc of Object.keys(FIF.files || {})) {
      for (const f of filesOf(acc)) {
        t.files++;
        const e = extOf(f.name);
        if (e === 'zip') t.zip++;
        if (e === 'ts') t.ts++;
        t.kindBytes[f.kind] = (t.kindBytes[f.kind] || 0) + (f.size || 0);
        t.kindCount[f.kind] = (t.kindCount[f.kind] || 0) + 1;
      }
    }
    return totals = t;
  }

  App.view({
    id: 'files', title: 'Files and media', tier: 1,
    heading: 'Every original file, straight from NASA PSI',
    intro: 'Browse the documents, videos and raw data files of each investigation. Every file opens from its official NASA PSI address; nothing is copied here.',
    needs: ['files'],
    brief: {
      need: 'Scientists must be able to open the original document, video or raw file behind any statement, at the cited page.',
      data: ['data/processed/files.csv: the catalogue (accession, category, file name, size in bytes)',
        'official address: https://psi.nasa.gov/geode-py/ws/studies/<ACCESSION>/download?file=<file name>'],
      call: 'GET /api/resolve?accession=PSI-25&file=<file name>   (demo/server.py)\n-> {"url": "<presigned NASA storage address, valid about 2 hours>"}',
      keep: ['The official NASA PSI link, next to every preview', 'Nothing from NASA is stored: files are linked or streamed',
        'Formats that cannot be shown in a browser (.zip image sets, .ts video, office files) are named as such, with the download link'],
      backend: 'Inline PDF pages and raw-file previews need the server to resolve the storage address. Videos, images and links work without it.',
    },
    render(root, state, update) {
      const c = App.colors();
      const invs = (FIF.investigations || []).map(i => i.accession).filter(a => (FIF.files || {})[a]);
      for (const a of Object.keys(FIF.files || {})) if (!invs.includes(a)) invs.push(a);
      const acc = invs.includes(state.accession) ? state.accession : (invs.includes('PSI-25') ? 'PSI-25' : invs[0]);
      if (!acc) { root.append(h('p', { class: 'muted', text: 'The file catalogue is empty.' })); return; }
      const all = filesOf(acc);
      const kind = KIND_LABEL[state.kind] ? state.kind : '';
      const q = String(state.q || '').trim().toLowerCase();

      const catCount = {}, catBytes = {}, kindCount = {};
      let total = 0;
      for (const f of all) {
        catCount[f.category] = (catCount[f.category] || 0) + 1;
        catBytes[f.category] = (catBytes[f.category] || 0) + (f.size || 0);
        kindCount[f.kind] = (kindCount[f.kind] || 0) + 1;
        total += f.size || 0;
      }
      const cats = Object.keys(catCount).sort((a, b) => catCount[b] - catCount[a]);
      const category = catCount[state.category] ? state.category : '';
      const tsHere = all.reduce((n, f) => n + (extOf(f.name) === 'ts' ? 1 : 0), 0);

      root.append(h('div', { class: 'row' },
        App.select({ id: 'fl-acc', label: 'Investigation', value: acc,
          options: invs.map(a => [a, `${App.name(a)} · ${filesOf(a).length} files`]),
          onChange: v => update({ accession: v, category: '', q: '' }) })));

      root.append(h('div', { class: 'grid tiles' },
        h('div', { class: 'tile' }, h('b', { text: String(all.length) }), h('span', { text: 'files listed at PSI' })),
        h('div', { class: 'tile' }, h('b', { text: bytes(total) }), h('span', { text: 'total size' })),
        h('div', { class: 'tile' }, h('b', { text: String(kindCount.video || 0) }), h('span', { text: tsHere ? `playable videos (plus ${tsHere} .ts that browsers cannot play)` : 'playable videos' })),
        h('div', { class: 'tile' }, h('b', { text: String(kindCount.pdf || 0) }), h('span', { text: 'documents (PDF)' })),
        h('div', { class: 'tile' }, h('b', { text: String(kindCount.table || 0) }), h('span', { text: 'data tables (csv, asc, dat)' }))));

      // Videos first: they are what people most want to see and they play without a server.
      const videos = [];
      for (const f of all) if (f.kind === 'video') videos.push(f);
      if (videos.length) {
        const play = f => App.openFile({ accession: acc, file: f.name, title: f.short });
        root.append(App.panel(`Videos (${videos.length})`,
          h('div', { class: 'grid' }, videos.slice(0, 6).map(f => h('div', { class: 'card', onclick: () => play(f) },
            h('h4', { style: 'overflow-wrap:anywhere', text: f.short }),
            h('span', { class: 'small muted', text: `${f.category} · ${bytes(f.size)}` }),
            h('div', {}, h('button', { class: 'btn primary', type: 'button', onclick: e => { e.stopPropagation(); play(f); } }, 'Play'))))),
          videos.length > 6 && h('div', {}, h('button', { id: 'fl-videos-all', class: 'btn', type: 'button', onclick: () => update({ kind: 'video', category: '', q: '' }) }, `Show all ${videos.length} videos in the list`))));
      }

      // Chart: size or count per category of this investigation. Click a bar to filter the list.
      const metric = state.metric === 'count' ? 'count' : 'size';
      const vals = cats.map(k => metric === 'count' ? catCount[k] : catBytes[k]);
      const pos = vals.filter(v => v > 0);
      const useLog = pos.length > 1 && Math.max(...pos) / Math.min(...pos) > 1000;
      const plotCats = cats.filter((k, i) => !useLog || vals[i] > 0);
      const plotEl = h('div', {});
      App.plot(plotEl, [{
        type: 'bar', orientation: 'h', y: plotCats, x: plotCats.map(k => metric === 'count' ? catCount[k] : catBytes[k]),
        customdata: plotCats.map(k => [catCount[k], bytes(catBytes[k])]),
        marker: { color: plotCats.map(k => k === category ? c.accent : c.s[0]), line: { color: c.surface, width: 1 } },
        hovertemplate: '%{y}<br>%{customdata[0]} files<br>%{customdata[1]}<extra></extra>',
      }], {
        height: 70 + plotCats.length * 30, margin: { l: 170, r: 24, t: 8, b: 44 },
        xaxis: { title: metric === 'count' ? 'number of files' + (useLog ? ' (log scale)' : '') : 'total size, bytes' + (useLog ? ' (log scale)' : ''),
          type: useLog ? 'log' : 'linear', ...(metric === 'size' ? { tickformat: '.2s' } : {}) },
        yaxis: { autorange: 'reversed' },
      }, pt => update({ category: pt.y === category ? '' : pt.y }));
      root.append(App.panel('Where the bytes are, by PSI category',
        h('div', { class: 'row' }, App.seg({ id: 'fl-metric', label: 'Measure', options: [['size', 'Total size'], ['count', 'Number of files']], value: metric, onChange: v => update({ metric: v }) }),
          h('span', { class: 'small muted', text: 'Click a bar to list only that category.' })),
        plotEl));

      // Filters and the file list.
      const kindOpts = [['', `All ${all.length}`], ...KINDS.filter(([k]) => kindCount[k]).map(([k, l]) => [k, `${l} ${kindCount[k]}`])];
      if (kind && !kindCount[kind]) kindOpts.push([kind, `${KIND_LABEL[kind]} 0`]);
      root.append(h('div', { class: 'row' },
        App.seg({ id: 'fl-kind', label: 'Kind', options: kindOpts, value: kind, onChange: v => update({ kind: v }) }),
        App.select({ id: 'fl-cat', label: 'Category', value: category,
          options: [['', `All categories (${all.length})`], ...cats.map(k => [k, `${k} (${catCount[k]})`])], onChange: v => update({ category: v }) }),
        App.search({ id: 'fl-q', label: 'File name contains', value: state.q || '', placeholder: 'e.g. 21162D1, Final, mp4', onChange: v => update({ q: v }) })));

      const rows = [];
      for (const f of all) {
        if (kind && f.kind !== kind) continue;
        if (category && f.category !== category) continue;
        if (q && f.lname.indexOf(q) < 0) continue;
        rows.push(f);
      }
      const kindChip = k => App.chip(KIND_LABEL[k] || k, k === 'other' ? 'warn' : '');
      root.append(rows.length ? App.table({
        rows, pageSize: 25, onRow: r => App.openFile({ accession: acc, file: r.name, title: r.short }),
        cols: [
          { key: 'short', label: 'File', fmt: (v, r) => h('span', { title: r.name, style: 'overflow-wrap:anywhere' }, v) },
          { key: 'category', label: 'Category' },
          { key: 'kind', label: 'Kind', fmt: v => kindChip(v) },
          { key: 'size', label: 'Size', num: true, fmt: v => bytes(v) },
        ] }) : h('p', { class: 'muted', text: 'No file matches these filters.' }));

      const T = catalogueTotals();
      root.append(App.notes([
        'Files are streamed from NASA PSI and never copied: every link goes to the official PSI address.',
        `${T.zip} of the ${T.files} files in the catalogue are archives (.zip), mostly image sets. They can only be downloaded.`,
        `${T.ts} videos are MPEG transport streams (.ts), which browsers do not play. Download them and use a player such as VLC.`,
        `Some files listed by PSI answer "not found" (${MISSING_AT_LAST_DOWNLOAD} at the last download). The viewer then says so and keeps the link.`,
        'Inline PDF pages and raw-file previews need the dashboard server. Without it, files open at NASA PSI.',
      ], 'About these files'));
    },
  });
})();
