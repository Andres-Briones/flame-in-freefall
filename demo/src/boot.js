(function boot() {
  const nav = document.getElementById('nav');
  let tier = null;
  for (const v of App.views) {
    if (tier != null && v.tier !== tier) nav.append(h('span', { class: 'nav-sep' }));
    tier = v.tier;
    nav.append(h('a', { href: '#' + v.id, 'data-id': v.id }, v.title));
  }
  document.getElementById('drawer-close').addEventListener('click', App.closeDrawer);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') App.closeDrawer(); });
  window.addEventListener('hashchange', App.render);
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  if (mq.addEventListener) mq.addEventListener('change', App.render);
  new MutationObserver(App.render).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  App.detectBackend().then(() => { document.documentElement.dataset.backend = String(App.backend); App.render(); });
})();
