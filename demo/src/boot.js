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
  const grip = document.getElementById('drawer-grip'), root = document.documentElement;
  const setWidth = (mode, px) => root.style.setProperty('--drawer-' + mode, Math.round(Math.max(320, Math.min(px, window.innerWidth - 360))) + 'px');
  try { for (const m of ['narrow', 'wide']) { const px = +localStorage.getItem('fif-drawer-' + m); if (px) setWidth(m, px); } } catch (e) { /* storage blocked */ }
  grip.addEventListener('pointerdown', e => {
    const mode = root.dataset.drawer;
    if (!mode) return;
    e.preventDefault();
    grip.setPointerCapture(e.pointerId);
    grip.classList.add('drag');
    const move = ev => setWidth(mode, window.innerWidth - ev.clientX);
    const up = () => {
      grip.removeEventListener('pointermove', move);
      grip.classList.remove('drag');
      try { localStorage.setItem('fif-drawer-' + mode, parseInt(root.style.getPropertyValue('--drawer-' + mode), 10)); } catch (e) { /* storage blocked */ }
      window.dispatchEvent(new Event('resize'));
    };
    grip.addEventListener('pointermove', move);
    grip.addEventListener('pointerup', up, { once: true });
    grip.addEventListener('pointercancel', up, { once: true });
  });
  window.addEventListener('hashchange', App.render);
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  if (mq.addEventListener) mq.addEventListener('change', App.render);
  new MutationObserver(App.render).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  App.detectBackend().then(() => { document.documentElement.dataset.backend = String(App.backend); App.render(); });
})();
