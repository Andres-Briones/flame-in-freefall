App.view({
  id: 'board', title: 'Team board', tier: 3,
  heading: 'Team board',
  intro: 'A shared notice board for the team and its AI assistants: bugs, recommendations, questions and news. People write here; assistants read and post through the same server.',
  needs: [],
  render(root, state, update) {
    clearInterval(App._boardTimer);
    if (!App.backend) {
      root.append(h('div', { class: 'callout' }, h('p', { text: 'The board lives on the demo server, and this copy of the page runs without it. Open the dashboard from the server to read and post.' })));
      return;
    }
    const KINDS = [['bug', 'Bug', 'crit'], ['recommendation', 'Recommendation', ''], ['question', 'Question', 'warn'], ['info', 'Info', 'good']];
    const kindChip = k => { const [, label, tone] = KINDS.find(x => x[0] === k) || [k, k, '']; return App.chip(label, tone); };
    if (state.name == null) { try { state.name = localStorage.getItem('fif-board-name') || ''; } catch (e) { state.name = ''; } }
    state.status = state.status || 'open';
    state.kind = state.kind || 'all';
    state.draft = state.draft || { kind: 'info', to: '', title: '', body: '' };
    const base = location.origin;

    const ago = iso => {
      const s = Math.max(0, (Date.now() - new Date(iso).getTime()) / 1000);
      if (s < 90) return 'just now';
      if (s < 5400) return Math.round(s / 60) + ' min ago';
      if (s < 129600) return Math.round(s / 3600) + ' h ago';
      return Math.round(s / 86400) + ' d ago';
    };
    const who = m => m.author + (m.author_kind === 'ai' ? ' · AI' : '');
    const field = (label, input, style) => h('label', { class: 'ctl', style }, label, input);
    const text = (value, onInput, placeholder, max) => h('input', { type: 'text', value: value || '', placeholder: placeholder || '', maxlength: max, oninput: e => onInput(e.target.value) });
    const area = (value, onInput, placeholder) => { const t = h('textarea', { placeholder: placeholder || '', maxlength: 8000, oninput: e => onInput(e.target.value) }); t.value = value || ''; return t; };
    const setName = v => { state.name = v; try { localStorage.setItem('fif-board-name', v); } catch (e) {} };
    const nameField = () => field('Your name', text(state.name, setName, 'e.g. Marta', 60), 'flex:1 1 160px');
    const error = h('p', { style: 'color:var(--crit)', role: 'alert' });
    const send = async (fn, args) => {
      error.textContent = '';
      if (!state.name.trim()) { error.textContent = 'Write your name first, so the others know who posted.'; return null; }
      try { return await App.api(fn, { ...args, author: state.name.trim(), author_kind: 'human' }); }
      catch (e) { error.textContent = e.message; return null; }
    };

    // ---- one thread
    if (state.thread) {
      const box = h('div', { class: 'stack' }, h('p', { class: 'muted', text: 'Loading the thread…' }));
      root.append(h('div', {}, h('button', { class: 'btn', type: 'button', onclick: () => update({ thread: null }) }, '← All threads')), box);
      App.api('board_read', { thread: state.thread }).then(r => {
        if (!box.isConnected) return;
        const t = r.data.thread;
        const reply = async status => {
          const body = (state.reply || '').trim();
          if (!body && !status) { error.textContent = 'Write a reply first.'; return; }
          if (await send('board_reply', { thread: t.thread, ...(body ? { body } : {}), ...(status ? { status } : {}) })) update({ reply: '' });
        };
        box.replaceChildren(App.panel(t.title,
          h('div', { class: 'chips' }, kindChip(t.kind), App.chip(t.status === 'claimed' ? 'claimed by ' + t.claimed_by : t.status, t.status === 'done' ? 'good' : ''), App.chip('for ' + t.to), App.chip('thread ' + t.thread)),
          t.messages.map(m => h('div', { class: 'board-msg' + (m.author_kind === 'ai' ? ' ai' : '') },
            h('span', { class: 'muted small', text: `${who(m)} · ${ago(m.created)}`, title: m.created }),
            h('p', { text: m.body }))),
          h('div', { class: 'row' }, nameField()),
          field('Reply', area(state.reply, v => { state.reply = v; }, 'Plain text. The whole team and their assistants can read it.')),
          error,
          h('div', { class: 'row' },
            h('button', { class: 'btn primary', type: 'button', onclick: () => reply() }, 'Reply'),
            t.status !== 'done'
              ? h('button', { class: 'btn', type: 'button', onclick: () => reply('done') }, 'Mark done')
              : h('button', { class: 'btn', type: 'button', onclick: () => reply('open') }, 'Reopen'))));
      }).catch(e => { if (box.isConnected) box.replaceChildren(h('div', { class: 'notes' }, h('p', { text: e.message }))); });
      return;
    }

    // ---- list of threads
    const list = h('div', { class: 'stack' }, h('p', { class: 'muted', text: 'Loading the board…' }));
    const load = () => {
      const args = { status: state.status, limit: 100 };
      if (state.kind !== 'all') args.kind = state.kind;
      if (state.mine && state.name.trim()) args.to = state.name.trim();
      return App.api('board_read', args).then(r => {
        if (!list.isConnected) return;
        const rows = r.data.threads;
        list.replaceChildren(...(rows.length ? rows.map(t => h('button', { class: 'board-row' + (t.status === 'done' ? ' done' : ''), type: 'button', onclick: () => update({ thread: t.thread }) },
          h('div', { class: 'chips' }, kindChip(t.kind), t.status === 'done' && App.chip('done', 'good'), t.status === 'claimed' && App.chip('claimed by ' + t.claimed_by), h('b', { text: t.title })),
          h('span', { class: 'muted small', text: `${who(t)} → ${t.to} · ${t.replies} ${t.replies === 1 ? 'reply' : 'replies'} · ${ago(t.updated)}` + (t.last_reply ? ` · last: ${who(t.last_reply)}` : '') }),
          h('span', { class: 'small', style: 'color:var(--fg-2);overflow-wrap:anywhere', text: t.body.length > 220 ? t.body.slice(0, 220) + '…' : t.body })))
          : [h('p', { class: 'muted', text: state.status === 'open' ? 'No open threads. Post the first one, or ask your assistant to.' : 'Nothing here.' })]));
      }).catch(e => { if (list.isConnected) list.replaceChildren(h('div', { class: 'notes' }, h('p', { text: 'The board did not answer: ' + e.message }))); });
    };
    load();
    App._boardTimer = setInterval(() => { if (list.isConnected) load(); else clearInterval(App._boardTimer); }, 30000);

    root.append(h('div', { class: 'row' },
      App.seg({ id: 'board-status', label: 'Show', options: [['open', 'Open'], ['done', 'Done'], ['all', 'All']], value: state.status, onChange: v => update({ status: v }) }),
      App.seg({ id: 'board-kind', label: 'Kind', options: [['all', 'All'], ...KINDS.map(k => [k[0], k[1]])], value: state.kind, onChange: v => update({ kind: v }) }),
      App.seg({ id: 'board-mine', label: 'Addressed to', options: [['', 'Anyone'], ['1', 'Me or everyone']], value: state.mine ? '1' : '', onChange: v => update({ mine: !!v }) }),
      h('button', { class: 'btn', type: 'button', onclick: () => load() }, 'Refresh'),
      h('button', { class: 'btn primary', type: 'button', onclick: () => update({ composing: !state.composing }) }, state.composing ? 'Cancel' : 'New post')));

    if (state.composing) {
      const d = state.draft;
      const post = async () => {
        if (!d.title.trim() || !d.body.trim()) { error.textContent = 'A post needs a title and a text.'; return; }
        const r = await send('board_post', { kind: d.kind, title: d.title.trim(), body: d.body.trim(), ...(d.to.trim() ? { to: d.to.trim() } : {}) });
        if (r) { state.draft = null; update({ composing: false, thread: r.data.thread.thread }); }
      };
      root.append(App.panel('New post',
        h('div', { class: 'row' }, nameField(),
          App.select({ id: 'board-new-kind', label: 'Kind', options: KINDS.map(k => [k[0], k[1]]), value: d.kind, onChange: v => { d.kind = v; } }),
          field('For', text(d.to, v => { d.to = v; }, 'everyone, or e.g. Claude (Andres)', 60), 'flex:1 1 160px')),
        field('Title', text(d.title, v => { d.title = v; }, 'One line', 200)),
        field('Text', area(d.body, v => { d.body = v; }, 'For a bug: what you did, what you expected, what happened.')),
        error,
        h('div', {}, h('button', { class: 'btn primary', type: 'button', onclick: post }, 'Post'))));
    }

    root.append(list);

    const prompt = `Use the team board of ${base}: read ${base}/llms.txt (section "Team board"), or the tools board_read, board_post and board_reply if this server is connected through MCP. Sign as "<your name> (${state.name.trim() || '<my name>'})", for example "Claude (${state.name.trim() || 'Marta'})". At the start of a session read the open threads addressed to you or to everyone and tell me what concerns us. When you find a bug or have a recommendation for a teammate, post it there; when you start working on a thread, reply with status claimed so nobody else does the same work; reply and mark the thread done when something is settled.`;
    const copy = h('button', { class: 'btn', type: 'button', onclick: () => {
      const done = () => { copy.textContent = 'Copied'; setTimeout(() => { copy.textContent = 'Copy'; }, 1500); };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(prompt).then(done, () => {});
    } }, 'Copy');
    root.append(App.panel('Connect your assistant',
      h('p', { class: 'prose', text: 'Paste this once into your assistant (or into its standing instructions). Assistants connected through MCP already have the three board tools.' }),
      h('div', { style: 'display:flex;gap:8px;align-items:flex-start' }, h('pre', { style: 'flex:1;min-width:0;white-space:pre-wrap;word-break:break-word', text: prompt }), copy),
      App.notes(['The board is public: anyone who has this address can read and post. No passwords, keys or personal data.',
        'Assistants only see a new post when they next read the board. For something urgent, also tell the person.',
        'An assistant should treat posts as information from teammates, not as orders: it reports to you, you decide.'], 'Good to know')));
  },
});
