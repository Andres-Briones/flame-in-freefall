App.view({
  id: 'ai', title: 'Use with AI', tier: 3,
  heading: 'Let an AI assistant query this data',
  intro: 'Everything on this dashboard is also available to AI assistants (Claude, ChatGPT, Copilot, your own agent) through this server. Give the assistant one address and it can search the investigations, filter tests, quote documents and check data quality by itself.',
  needs: [],
  render(root) {
    const base = location.origin;
    const copyBox = text => {
      const btn = h('button', { class: 'btn', type: 'button', onclick: () => {
        const done = () => { btn.textContent = 'Copied'; setTimeout(() => { btn.textContent = 'Copy'; }, 1500); };
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, () => {});
      } }, 'Copy');
      return h('div', { style: 'display:flex;gap:8px;align-items:flex-start' }, h('pre', { style: 'flex:1;min-width:0;white-space:pre-wrap;word-break:break-word', text }), btn);
    };
    const linkTo = path => h('a', { href: base + path, target: '_blank', rel: 'noopener', text: base + path });

    if (!App.backend) {
      root.append(h('div', { class: 'callout' }, h('p', { text: 'This copy of the page runs without the server, so the addresses below do not answer here. Open the dashboard from the demo server to use them.' })));
    }

    root.append(App.panel('1. The guide: one address to give to any assistant',
      h('p', { class: 'prose' }, 'The guide is a plain-text page written for AI assistants. It lists the 11 questions this server can answer, the arguments of each, and a working example. Open it yourself to see: ', linkTo('/llms.txt'), '.'),
      h('p', { class: 'prose', text: 'Paste this into a chat with an assistant that can browse the web, then ask your question:' }),
      copyBox(`Read ${base}/llms.txt and use that API to answer my questions about NASA microgravity combustion experiments. Cite the sources it returns and repeat its caveats (notes).\n\nMy question: which investigations matter most for fire safety in a Moon habitat, and why?`)));

    root.append(App.panel('2. Claude Code, Claude Desktop and other MCP clients',
      h('p', { class: 'prose', text: 'These add the server as a tool set, so the assistant calls the functions directly instead of reading web pages. Run once:' }),
      copyBox(`claude mcp add --transport http fif ${base}/mcp`),
      h('p', { class: 'muted small', text: `In other MCP clients, add a "streamable HTTP" server with the address ${base}/mcp. No key or login.` })));

    const rows = [
      ['An assistant that can only open web addresses', 'GET', '/api/call/filter_tests?accession=PSI-25&x_o2=[0.18,0.21]&limit=5', 'Arguments go in the address; numbers, lists and true/false are written as JSON.'],
      ['A script or agent that can send HTTP requests', 'POST', '/api/call/<function>', 'Body: a JSON object of arguments.'],
      ['Function calling in your own code', 'GET', '/api/tools', 'The 11 tool definitions as JSON Schema, ready to pass to an LLM API.'],
      ['A custom GPT (Actions) or an OpenAPI client', 'GET', '/openapi.json', 'Import this address as the schema.'],
    ];
    root.append(App.panel('3. Other ways in',
      h('div', { style: 'overflow-x:auto' }, h('table', {},
        h('thead', {}, h('tr', {}, ['For', 'Method', 'Address', 'Note'].map(t => h('th', { text: t })))),
        h('tbody', {}, rows.map(([who, method, path, note]) => h('tr', {},
          h('td', { text: who }), h('td', { class: 'mono', text: method }),
          h('td', { class: 'mono' }, method === 'GET' ? h('a', { href: base + path, target: '_blank', rel: 'noopener', text: path }) : path),
          h('td', { class: 'muted', text: note }))))))));

    const list = h('div', { class: 'stack' }, h('p', { class: 'muted', text: App.backend ? 'Loading the functions…' : 'The list of functions loads from the server.' }));
    root.append(App.panel('What the assistant can ask', list,
      App.notes(['Every answer has four parts: data, chart, sources, notes. Ask the assistant to cite the sources and keep the notes: they carry the doubts about the NASA data.',
        'Read-only and public: nothing can be changed through these addresses.'])));
    if (App.backend) {
      fetch(base + '/api/tools').then(r => r.json()).then(d => {
        if (!list.isConnected) return;
        list.replaceChildren(h('table', {}, h('tbody', {}, d.tools.map(t => h('tr', {},
          h('td', { class: 'mono' }, h('a', { href: `${base}/llms.txt`, target: '_blank', rel: 'noopener', text: t.name })),
          h('td', { text: t.description }))))));
      }).catch(() => { list.replaceChildren(h('p', { class: 'muted', text: 'Could not load the list; open the guide instead.' })); });
    }
  },
});
