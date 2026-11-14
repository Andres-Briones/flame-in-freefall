/* File viewer: App.viewer({accession, file, page, title}) opens a wide drawer for one PSI file.
   Nothing is stored by us: media use the official PSI address directly; PDF pages and raw-file previews fetch a
   short-lived NASA storage address that App.resolve gets from the dashboard server. The official link is always shown.
   Also defines App.parseTable(text) (pure, tested in node), App.fmtBytes(n) and App.fileInfo(accession, file). */
(function () {
  const PDF_WORKER = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  const PREVIEW_BYTES = 2097152;
  const TEXT_LINES = 400, TABLE_ROWS = 200, PLOT_POINTS = 5000, MAX_Y = 4;

  // Bumped on every open: async work started for an older file checks it and stops.
  let token = 0;
  let pdfState = null;   // {task, doc, renderTask} of the PDF currently open, destroyed when another file opens

  function fmtBytes(n) {
    if (typeof n !== 'number' || !isFinite(n) || n < 0) return '–';
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    let i = 0, v = n;
    while (v >= 1000 && i < units.length - 1) { v /= 1000; i++; }
    return (i === 0 ? String(Math.round(v)) : v >= 100 ? v.toFixed(0) : v >= 10 ? v.toFixed(1) : v.toFixed(2)) + ' ' + units[i];
  }

  function fileInfo(accession, file) {
    const cat = window.FIF && FIF.files && FIF.files[accession];
    if (!cat) return null;
    for (const [category, list] of Object.entries(cat)) {
      for (const f of list) if (f[0] === file) return { category, size: f[1] };
    }
    return null;
  }

  const extOf = file => ((String(file).match(/\.([A-Za-z0-9]+)$/) || [, ''])[1] || '').toLowerCase();

  /* ---------- table parser (pure) ---------- */

  function splitQuoted(line, d) {
    const out = [];
    let cur = '', q = false;
    for (let i = 0; i < line.length; i++) {
      const ch = line[i];
      if (q) {
        if (ch === '"') { if (line[i + 1] === '"') { cur += '"'; i++; } else q = false; }
        else cur += ch;
      } else if (ch === '"' && cur.trim() === '') { q = true; cur = ''; }
      else if (ch === d) { out.push(cur.trim()); cur = ''; }
      else cur += ch;
    }
    out.push(cur.trim());
    return out;
  }
  const SPLITTERS = {
    ',': l => splitQuoted(l, ','),
    '\t': l => splitQuoted(l, '\t'),
    ';': l => splitQuoted(l, ';'),
    ' ': l => { const t = l.trim(); return t ? t.split(/\s+/) : []; },
  };
  const toCell = s => {
    if (s === '' || s == null) return s;
    const t = s.trim();
    if (!/^[+-]?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$/.test(t)) return s;
    const x = Number(t);
    return isFinite(x) ? x : s;
  };

  // Finds the delimiter and the header row of a raw text table. Raw files often open with metadata lines: the header
  // is the first line after which most lines have its number of fields (2 or more). Returns {header, rows, skipped,
  // delimiter, preamble, hasHeader} or null when the text is not a table. `skipped` counts preamble lines plus rows
  // whose number of fields differs from the header.
  function parseTable(text) {
    if (typeof text !== 'string' || !text) return null;
    let lines = text.split(/\r\n|\n|\r/);
    while (lines.length && lines[lines.length - 1].trim() === '') lines.pop();
    if (lines.length < 2) return null;
    const SCAN = Math.min(lines.length, 60), WINDOW = 50;
    let best = null;
    for (const d of Object.keys(SPLITTERS)) {
      const split = SPLITTERS[d];
      const counts = [];
      for (let i = 0; i < Math.min(lines.length, SCAN + WINDOW); i++) counts.push(lines[i].trim() === '' ? 0 : split(lines[i]).length);
      for (let i = 0; i < SCAN; i++) {
        const k = counts[i];
        if (k < 2) continue;
        let same = 0, seen = 0;
        for (let j = i + 1; j < Math.min(counts.length, i + 1 + WINDOW); j++) {
          if (counts[j] === 0) continue;
          seen++; if (counts[j] === k) same++;
        }
        if (seen === 0 || same / seen < 0.8) continue;
        // The earliest consistent line wins for a delimiter; across delimiters prefer more fields, then earlier start.
        const score = k * 1000 - i;
        if (!best || score > best.score) best = { d, i, k, score };
        break;
      }
    }
    if (!best) return null;
    const split = SPLITTERS[best.d];
    const first = split(lines[best.i]);
    // A header line is mostly text while the data are mostly numbers; otherwise the first line is already data.
    const nextLine = lines.slice(best.i + 1).find(l => split(l).length === best.k);
    const numericShare = cells => cells.filter(c => typeof toCell(c) === 'number').length / Math.max(1, cells.length);
    const hasHeader = numericShare(first) < 0.5 && (nextLine == null || numericShare(split(nextLine)) >= numericShare(first));
    const header = hasHeader ? first.map((c, i) => c || `col ${i + 1}`) : first.map((_, i) => `col ${i + 1}`);
    const rows = [];
    let skipped = best.i;
    for (let j = hasHeader ? best.i + 1 : best.i; j < lines.length; j++) {
      if (lines[j].trim() === '') continue;
      const cells = split(lines[j]);
      if (cells.length !== best.k) { skipped++; continue; }
      rows.push(cells.map(toCell));
    }
    if (!rows.length) return null;
    return { header, rows, skipped, delimiter: best.d, preamble: lines.slice(0, best.i), hasHeader };
  }

  /* ---------- shared pieces ---------- */

  const link = (accession, file, label) => h('a', { href: App.fileUrl(accession, file), target: '_blank', rel: 'noopener' }, label || 'Open at NASA PSI');
  const msg = (text, cls) => h('p', { class: cls || '', text });

  function headerNode(accession, file, page, info) {
    const bits = [App.name(accession)];
    if (info && info.category) bits.push(info.category);
    if (info && typeof info.size === 'number') bits.push(fmtBytes(info.size));
    if (page) bits.push(`cited page p. ${page}`);
    return h('div', { class: 'stack', style: 'gap:4px' },
      h('div', { class: 'row', style: 'align-items:center;justify-content:space-between' },
        h('span', { class: 'small muted', text: bits.join(' · ') }),
        h('a', { class: 'btn', href: App.fileUrl(accession, file), target: '_blank', rel: 'noopener' }, 'Open at NASA PSI')),
      h('p', { class: 'small mono', style: 'overflow-wrap:anywhere', text: file }),
      h('p', { class: 'small muted', text: 'Streamed from NASA PSI. Nothing is stored on this server.' }));
  }

  function fallback(accession, file, sentence) {
    return h('div', { class: 'callout' }, h('p', {}, sentence, ' ', link(accession, file, 'Open at NASA PSI'), '.'));
  }

  const stale = (t, node) => t !== token || !node.isConnected;

  function cleanupPdf() {
    const s = pdfState;
    pdfState = null;
    if (!s) return;
    try { if (s.renderTask) s.renderTask.cancel(); } catch (e) { /* already finished */ }
    try { if (s.task && s.task.destroy) s.task.destroy(); } catch (e) { /* already destroyed */ }
  }

  /* ---------- PDF ---------- */

  function pdfError(e) {
    const name = e && e.name;
    if (name === 'MissingPDFException') return 'NASA PSI did not return this document (file not found).';
    if (name === 'InvalidPDFException') return 'The file is not a readable PDF.';
    if (name === 'PasswordException') return 'The PDF is password protected.';
    if (name === 'UnexpectedResponseException') return `NASA storage answered ${e.status || 'an error'}; the address may have expired. Reopen the file.`;
    return 'The PDF could not be shown: ' + ((e && e.message) || String(e)) + '.';
  }

  function showPdf(body, ref, t) {
    const { accession, file } = ref;
    const lib = window.pdfjsLib;
    if (!App.backend || !lib || !lib.getDocument) {
      body.append(fallback(accession, file,
        (!App.backend ? 'Showing PDF pages here needs the dashboard server.' : 'The PDF library did not load (it needs internet access to cdnjs).') +
        ' Open at NASA PSI downloads the file' + (ref.page ? `; the cited page is p. ${ref.page}` : '')));
      return;
    }
    const status = msg('Finding the document at NASA PSI…', 'muted small');
    const canvasWrap = h('div', { style: 'overflow:auto;max-width:100%' });
    const pageInput = h('input', { id: 'fv-page', type: 'number', min: 1, value: 1, style: 'width:72px', 'aria-label': 'Page number' });
    const ofN = h('span', { class: 'small muted num', text: 'of …' });
    const zoomLabel = h('span', { class: 'small muted num', text: '100%' });
    const btn = (id, label, fn) => h('button', { id, class: 'btn', type: 'button', disabled: true, onclick: fn }, label);
    const prev = btn('fv-prev', 'Previous', () => go(cur - 1));
    const next = btn('fv-next', 'Next', () => go(cur + 1));
    const zOut = btn('fv-zoom-out', 'Zoom out', () => setZoom(zoom / 1.25));
    const zIn = btn('fv-zoom-in', 'Zoom in', () => setZoom(zoom * 1.25));
    pageInput.disabled = true;
    pageInput.addEventListener('change', () => go(parseInt(pageInput.value, 10)));
    const controls = h('div', { class: 'row', style: 'align-items:center;gap:8px' },
      prev, next, h('label', { class: 'row small', style: 'align-items:center;gap:6px' }, 'Page', pageInput), ofN, zOut, zIn, zoomLabel);
    body.append(controls, status, canvasWrap);

    let doc = null, cur = 1, zoom = 1, seq = 0;
    const clamp = n => Math.min(Math.max(1, isFinite(n) ? n : 1), doc ? doc.numPages : 1);
    function sync() {
      if (!doc) return;
      pageInput.value = cur; pageInput.max = doc.numPages;
      prev.disabled = cur <= 1; next.disabled = cur >= doc.numPages;
      zOut.disabled = zoom <= 0.4; zIn.disabled = zoom >= 4;
      zoomLabel.textContent = Math.round(zoom * 100) + '%';
    }
    function go(n) { if (!doc) return; cur = clamp(n); sync(); draw(); }
    function setZoom(z) { zoom = Math.min(4, Math.max(0.4, z)); sync(); draw(); }

    async function draw() {
      const mine = ++seq;
      const s = pdfState;
      if (!doc || !s || stale(t, body)) return;
      if (s.renderTask) {
        try { s.renderTask.cancel(); } catch (e) { /* finished */ }
        try { await s.renderTask.promise; } catch (e) { /* cancelled */ }
        s.renderTask = null;
      }
      if (mine !== seq || stale(t, body)) return;
      status.textContent = 'Loading page…';
      try {
        const pg = await doc.getPage(cur);
        if (mine !== seq || stale(t, body)) return;
        const base = pg.getViewport({ scale: 1 });
        const avail = Math.max(320, (canvasWrap.clientWidth || body.clientWidth || 900) - 4);
        const vp = pg.getViewport({ scale: (avail / base.width) * zoom });
        const dpr = Math.min(3, window.devicePixelRatio || 1);
        const canvas = h('canvas', { class: 'viewer-canvas', 'aria-label': `Page ${cur} of ${file}` });
        canvas.width = Math.floor(vp.width * dpr);
        canvas.height = Math.floor(vp.height * dpr);
        canvas.style.width = Math.floor(vp.width) + 'px';
        if (zoom > 1) canvas.style.maxWidth = 'none';
        const ctx = canvas.getContext && canvas.getContext('2d');
        if (!ctx) throw new Error('this browser cannot draw on a canvas');
        const task = pg.render({ canvasContext: ctx, viewport: vp, transform: dpr !== 1 ? [dpr, 0, 0, dpr, 0, 0] : null });
        s.renderTask = task;
        await task.promise;
        if (s.renderTask === task) s.renderTask = null;
        if (mine !== seq || stale(t, body)) return;
        canvasWrap.replaceChildren(canvas);
        status.textContent = '';
      } catch (e) {
        if (e && e.name === 'RenderingCancelledException') return;
        if (mine !== seq || stale(t, body)) return;
        status.textContent = `Page ${cur} could not be drawn: ${(e && e.message) || e}.`;
      }
    }

    (async () => {
      let url;
      try { url = await App.resolve(accession, file); } catch (e) {
        if (stale(t, body)) return;
        status.replaceWith(fallback(accession, file, (e && e.message) || 'The address could not be found.'));
        controls.remove();
        return;
      }
      if (stale(t, body)) return;
      try {
        if (lib.GlobalWorkerOptions) lib.GlobalWorkerOptions.workerSrc = PDF_WORKER;
        status.textContent = 'Opening the document…';
        const task = lib.getDocument({ url, rangeChunkSize: 262144, disableAutoFetch: true, disableStream: true });
        pdfState = { task, doc: null, renderTask: null, token: t };
        const d = await task.promise;
        if (stale(t, body)) { try { task.destroy(); } catch (e) { /* ignore */ } return; }
        doc = d; pdfState.doc = d;
        ofN.textContent = `of ${d.numPages}`;
        pageInput.disabled = false;
        cur = clamp(ref.page || 1);
        if (ref.page && ref.page > d.numPages) status.textContent = `The cited page p. ${ref.page} is beyond the last page; showing p. ${cur}.`;
        sync();
        await draw();
      } catch (e) {
        if (stale(t, body)) return;
        status.textContent = pdfError(e);
        controls.remove();
      }
    })();
  }

  /* ---------- video and image ---------- */

  function showMedia(body, ref, kind) {
    const { accession, file } = ref;
    const src = App.fileUrl(accession, file);
    const holder = h('div', {});
    const el = kind === 'video'
      ? h('video', { controls: true, preload: 'metadata', class: 'viewer-media', src })
      : h('img', { class: 'viewer-media', src, alt: file });
    el.addEventListener('error', () => {
      holder.replaceChildren(fallback(accession, file,
        kind === 'video' ? 'This browser cannot play this file here.' : 'This browser cannot show this image here.'));
    });
    holder.append(el);
    body.append(holder);
    if (kind === 'video') body.append(msg('The video streams from NASA storage; seeking loads only the part you jump to.', 'small muted'));
  }

  /* ---------- text and table ---------- */

  async function readPrefix(url) {
    const r = await fetch(url, { headers: { Range: `bytes=0-${PREVIEW_BYTES - 1}` } });
    if (r.status !== 200 && r.status !== 206) throw new Error(`NASA storage answered ${r.status}.`);
    let total = null;
    const cr = r.headers && r.headers.get && r.headers.get('Content-Range');
    const m = cr && cr.match(/\/(\d+)\s*$/);
    if (m) total = +m[1];
    let bytes;
    if (r.body && r.body.getReader) {
      // A server that ignores Range answers 200 with the whole file: stop reading at the preview size.
      const reader = r.body.getReader(), parts = [];
      let n = 0;
      while (n < PREVIEW_BYTES) {
        const { done, value } = await reader.read();
        if (done) break;
        parts.push(value); n += value.length;
      }
      try { reader.cancel(); } catch (e) { /* done */ }
      bytes = new Uint8Array(Math.min(n, PREVIEW_BYTES));
      let o = 0;
      for (const p of parts) { const take = Math.min(p.length, bytes.length - o); bytes.set(p.subarray(0, take), o); o += take; if (o >= bytes.length) break; }
    } else {
      bytes = new Uint8Array(await r.arrayBuffer());
      if (bytes.length > PREVIEW_BYTES) bytes = bytes.subarray(0, PREVIEW_BYTES);
    }
    return { bytes, total, status: r.status };
  }

  function looksBinary(bytes) {
    const n = Math.min(bytes.length, 4096);
    if (!n) return false;
    let bad = 0;
    for (let i = 0; i < n; i++) { const b = bytes[i]; if (b === 0 || (b < 32 && b !== 9 && b !== 10 && b !== 13)) bad++; }
    return bad / n > 0.05;
  }

  function truncationNote(got, total, catalogueSize) {
    const whole = total != null ? total : catalogueSize;
    if (whole != null && whole > got) return `Preview of the first ${fmtBytes(got)} of ${fmtBytes(whole)}. Open at NASA PSI for the whole file.`;
    if (whole == null && got >= PREVIEW_BYTES) return `Preview of the first ${fmtBytes(got)}; the file may be longer.`;
    return '';
  }

  function textNode(text, truncated) {
    const lines = text.split(/\r\n|\n|\r/);
    if (truncated && lines.length > 1) lines.pop();   // the last line was cut by the byte limit
    const shown = lines.slice(0, TEXT_LINES);
    return h('div', { class: 'stack', style: 'gap:6px' },
      h('p', { class: 'small muted', text: lines.length > TEXT_LINES ? `First ${TEXT_LINES} lines of ${lines.length} read.` : `${lines.length} lines.` }),
      h('pre', { style: 'max-height:65vh;overflow:auto;white-space:pre', text: shown.join('\n') }));
  }

  const CLOCK = /^(\d{1,2}):(\d{2}):(\d{2})(?:[:.](\d{1,6}))?$/;
  const STAMP = /^\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(\.\d+)?$/;
  function clockSeconds(s) {
    const m = String(s).trim().match(CLOCK);
    if (!m) return null;
    const frac = m[4] ? +m[4] / Math.pow(10, m[4].length) : 0;
    return +m[1] * 3600 + +m[2] * 60 + +m[3] + frac;
  }
  function stampSeconds(s) {
    const t = String(s).trim();
    if (!STAMP.test(t)) return null;
    const ms = Date.parse(t.replace(' ', 'T').replace(/(\.\d{3})\d+$/, '$1') + 'Z');
    return isFinite(ms) ? ms / 1000 : null;
  }

  // Numeric columns for the quick plot. Clock or date-time columns become seconds from the first row.
  function plotColumns(parsed) {
    const cols = [];
    const n = parsed.rows.length;
    parsed.header.forEach((name, i) => {
      let nums = 0, clocks = 0, stamps = 0, filled = 0;
      for (const r of parsed.rows) {
        const v = r[i];
        if (v === '' || v == null) continue;
        filled++;
        if (typeof v === 'number') nums++;
        else if (clockSeconds(v) != null) clocks++;
        else if (stampSeconds(v) != null) stamps++;
      }
      if (!filled) return;
      if (nums / filled >= 0.9) {
        const vals = parsed.rows.map(r => typeof r[i] === 'number' ? r[i] : null);
        let lo = Infinity, hi = -Infinity;
        for (const v of vals) if (v != null) { if (v < lo) lo = v; if (v > hi) hi = v; }
        cols.push({ i, name, vals, constant: lo === hi });
      } else if (clocks / filled >= 0.9 || stamps / filled >= 0.9) {
        const f = clocks >= stamps ? clockSeconds : stampSeconds;
        let t0 = null, prev = null, wrap = 0;
        const vals = parsed.rows.map(r => {
          let s = f(r[i]);
          if (s == null) return null;
          if (f === clockSeconds && prev != null && s + wrap < prev - 43200) wrap += 86400;   // passed midnight
          s += f === clockSeconds ? wrap : 0;
          prev = s;
          if (t0 == null) t0 = s;
          return s - t0;
        });
        cols.push({ i, name: name + ' (s from first row)', vals, constant: false, time: true });
      }
    });
    return { cols, n };
  }

  function tableNode(parsed) {
    const box = h('div', { class: 'stack' });
    const shownRows = parsed.rows.slice(0, TABLE_ROWS).map(r => {
      const o = {};
      parsed.header.forEach((_, i) => { o['c' + i] = r[i]; });
      return o;
    });
    const cols = parsed.header.map((name, i) => ({ key: 'c' + i, label: name,
      num: shownRows.some(r => typeof r['c' + i] === 'number'),
      fmt: v => typeof v === 'number' ? String(v) : (v == null || v === '' ? '–' : String(v)) }));
    const delim = { ',': 'comma', '\t': 'tab', ';': 'semicolon', ' ': 'spaces' }[parsed.delimiter];
    box.append(h('p', { class: 'small muted', text:
      `${parsed.rows.length} rows read, ${parsed.header.length} columns, separated by ${delim}.` +
      (parsed.preamble.length ? ` ${parsed.preamble.length} metadata line(s) before the ${parsed.hasHeader ? 'header' : 'data'} are listed below.` : '') +
      (parsed.skipped > parsed.preamble.length ? ` ${parsed.skipped - parsed.preamble.length} line(s) with a different number of fields were left out.` : '') +
      (!parsed.hasHeader ? ' The file has no header row; columns are numbered.' : '') }));
    box.append(quickPlot(parsed));
    box.append(h('h4', { text: parsed.rows.length > TABLE_ROWS ? `First ${TABLE_ROWS} rows` : 'Rows' }));
    box.append(App.table({ cols, rows: shownRows, pageSize: 25 }));
    if (parsed.preamble.length) box.append(h('details', {}, h('summary', { class: 'small', text: 'Metadata lines before the table' }),
      h('pre', { style: 'max-height:30vh;overflow:auto', text: parsed.preamble.slice(0, 60).join('\n') })));
    return box;
  }

  function quickPlot(parsed) {
    const { cols } = plotColumns(parsed);
    const wrap = h('div', { class: 'stack', style: 'gap:8px' });
    if (!cols.length) { wrap.append(msg('No numeric column to plot.', 'small muted')); return wrap; }
    const INDEX = '__row__';
    const byKey = Object.fromEntries(cols.map(c => [String(c.i), c]));
    const timeCol = cols.find(c => c.time);
    let x = timeCol ? String(timeCol.i) : String(cols[0].i);
    const ys = [];
    const candidates = cols.filter(c => String(c.i) !== x && !c.time);
    const firstY = candidates.find(c => !c.constant) || candidates[0];
    if (firstY) ys.push(String(firstY.i));
    if (!ys.length) x = INDEX, ys.push(String(cols[0].i));
    const plotEl = h('div', {});
    const info = h('p', { class: 'small muted' });
    const opts = [[INDEX, 'row number'], ...cols.map(c => [String(c.i), c.name])];
    const ySel = k => App.select({ id: 'fv-y' + (k + 1), label: `y ${k + 1}`, options: [['', 'none'], ...cols.filter(c => !c.time).map(c => [String(c.i), c.name])],
      value: ys[k] || '', onChange: v => { ys[k] = v; draw(); } });
    const controls = h('div', { class: 'row' },
      App.select({ id: 'fv-x', label: 'x', options: opts, value: x, onChange: v => { x = v; draw(); } }),
      [0, 1, 2, 3].slice(0, MAX_Y).map(ySel));
    function draw() {
      const n = parsed.rows.length;
      const step = Math.max(1, Math.ceil(n / PLOT_POINTS));
      const xc = x === INDEX ? null : byKey[x];
      const traces = [];
      for (const key of ys) {
        const yc = key && byKey[key];
        if (!yc) continue;
        const tx = [], ty = [];
        for (let r = 0; r < n; r += step) {
          const xv = xc ? xc.vals[r] : r + 1, yv = yc.vals[r];
          if (typeof xv === 'number' && isFinite(xv) && typeof yv === 'number' && isFinite(yv)) { tx.push(xv); ty.push(yv); }
        }
        if (tx.length) traces.push({ type: 'scatter', mode: 'lines', name: yc.name, x: tx, y: ty, line: { width: 1.4 },
          hovertemplate: `${yc.name.replace(/[<>%{}]/g, '')}: %{y}<br>x: %{x}<extra></extra>` });
      }
      info.textContent = step > 1 ? `Every ${step}th row is drawn (${Math.ceil(n / step)} points).` : '';
      if (!traces.length) { plotEl.replaceChildren(msg('Pick at least one y column with numbers.', 'small muted')); return; }
      const fresh = h('div', {});
      plotEl.replaceChildren(fresh);
      App.plot(fresh, traces, { height: 320, xaxis: { title: xc ? xc.name : 'row number' }, yaxis: { title: traces.length === 1 ? traces[0].name : 'value (raw units)' } });
    }
    wrap.append(h('h4', { text: 'Quick plot' }), controls,
      h('div', { class: 'notes' }, h('p', { class: 'small', text: 'Quick look, raw units as in the file. The columns share one y axis and may have different units.' })),
      plotEl, info);
    draw();
    return wrap;
  }

  function showData(body, ref, kind, info, t) {
    const { accession, file } = ref;
    if (!App.backend) {
      body.append(fallback(accession, file, 'A preview of raw files here needs the dashboard server. Open at NASA PSI downloads the file'));
      return;
    }
    const status = msg('Reading the start of the file from NASA PSI…', 'muted small');
    body.append(status);
    (async () => {
      try {
        const url = await App.resolve(accession, file);
        if (stale(t, body)) return;
        const { bytes, total } = await readPrefix(url);
        if (stale(t, body)) return;
        if (looksBinary(bytes)) {
          status.replaceWith(fallback(accession, file, 'This file is binary despite its name, so it is not shown here.'));
          return;
        }
        const text = new TextDecoder('utf-8').decode(bytes);
        const note = truncationNote(bytes.length, total, info && info.size);
        const parts = [];
        if (note) parts.push(h('p', { class: 'small muted', text: note }));
        let parsed = null;
        if (kind === 'table') {
          // Drop the line cut by the byte limit so it is not counted as a malformed row.
          const usable = note ? text.slice(0, Math.max(text.lastIndexOf('\n'), 0)) : text;
          parsed = parseTable(usable);
        }
        if (parsed) parts.push(tableNode(parsed));
        else {
          if (kind === 'table') parts.push(msg('No table with two or more columns was found; showing the text.', 'small muted'));
          parts.push(textNode(text, !!note));
        }
        status.replaceWith(h('div', { class: 'stack' }, parts));
      } catch (e) {
        if (stale(t, body)) return;
        status.replaceWith(fallback(accession, file, ((e && e.message) || 'The file could not be read.').replace(/\.?$/, '.')));
      }
    })();
  }

  /* ---------- other formats ---------- */

  function whyNot(file) {
    const ext = extOf(file);
    if (ext === 'zip') return 'This is an archive, often a set of camera images: download it and unpack it on your computer.';
    if (['xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'rtf'].includes(ext)) return 'Office files open in their own application (a spreadsheet, word processor or presentation program).';
    if (ext === 'ts') return 'This is an MPEG transport stream (.ts), which web browsers do not play: download it and use a player such as VLC.';
    if (ext === 'avi') return 'AVI video does not play in web browsers: download it and use a player such as VLC.';
    if (['tif', 'tiff', 'nef'].includes(ext)) return 'Web browsers do not display this image format: download it and open it in an image viewer.';
    if (ext === 'pxp') return 'This is an Igor Pro experiment file: it opens in Igor Pro.';
    if (ext === 'mdipsug') return 'This is an instrument file in a format web browsers cannot read: download it.';
    return 'Web browsers cannot show this format here: download it to open it.';
  }

  /* ---------- entry ---------- */

  App.viewer = function ({ accession, file, page, title } = {}) {
    cleanupPdf();
    const t = ++token;
    const body = h('div', { class: 'stack' });
    if (!accession || !file) {
      body.append(msg('No file was given.'));
      App.drawer(title || 'File', body, true);
      return;
    }
    const info = fileInfo(accession, file);
    const p = Number.isFinite(+page) && +page >= 1 ? Math.floor(+page) : null;
    body.append(headerNode(accession, file, p, info));
    App.drawer(title || file, body, true);
    const kind = App.fileKind(file);
    try {
      if (kind === 'pdf') showPdf(body, { accession, file, page: p }, t);
      else if (kind === 'video' || kind === 'image') showMedia(body, { accession, file }, kind);
      else if (kind === 'table' || kind === 'text') showData(body, { accession, file }, kind, info, t);
      else body.append(h('div', { class: 'callout' }, h('p', {}, whyNot(file), ' ',
        info && typeof info.size === 'number' ? `Size ${fmtBytes(info.size)}. ` : '', link(accession, file, 'Open at NASA PSI'), '.')));
    } catch (e) {
      console.warn(e);
      body.append(fallback(accession, file, 'The viewer could not show this file.'));
    }
  };

  App.parseTable = parseTable;
  App.fmtBytes = fmtBytes;
  App.fileInfo = fileInfo;
})();
