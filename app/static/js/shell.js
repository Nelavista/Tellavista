// Shared app-shell behavior: mobile drawer + theme toggle. Used by every authenticated
// screen via components/skills_footer.html (Skills) or components/academia_footer.html
// (Academia) — extracted here so the two shells don't carry two copies of the same script.
// Settings > Appearance > Theme (models.UserPreferences.theme) writes here via
// localStorage['theme'] -- 'light' | 'dark' | 'system'. 'system' resolves against the
// OS/browser's prefers-color-scheme and stays live if that changes while the tab is open
// (e.g. the OS switches to dark mode at sunset). The quick single-click toggle button in
// the top bar (skToggleTheme below) always sets an explicit 'light'/'dark', never
// 'system' -- picking "System" is only available from the fuller Settings page.
function skResolveTheme(pref) {
  if (pref === 'system') {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  return pref;
}
function skApplyTheme(effective) {
  document.body.classList.toggle('light-mode', effective === 'light');
  const icon = document.querySelector('#theme-toggle i');
  if (icon) icon.className = effective === 'light' ? 'ri-sun-line' : 'ri-moon-line';
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = effective === 'light' ? '#f3f4f6' : '#050810';
}
(function () {
  const pref = localStorage.getItem('theme') || 'system';
  skApplyTheme(skResolveTheme(pref));
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => {
      if ((localStorage.getItem('theme') || 'system') === 'system') {
        skApplyTheme(skResolveTheme('system'));
      }
    });
  }
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(regs => regs.forEach(r => r.unregister()));
  }
})();

// Desktop (>=1024px) uses a persistent rail that can be collapsed; mobile uses an
// off-canvas drawer with an overlay. Same markup and same toggle on every path, so the
// two behaviours live here instead of in each sidebar template.
function skSidebarIsDesktop() {
  return !window.matchMedia || window.matchMedia('(min-width: 1024px)').matches;
}
function skApplySidebarState() {
  const sidebar = document.getElementById('side-menu');
  const overlay = document.getElementById('overlay');
  if (!sidebar) return;
  const desktop = skSidebarIsDesktop();
  const toggle = document.getElementById('menu-toggle');
  let open;

  if (desktop) {
    // The rail's state is body.sidebar-collapsed (see skills.css); clear any drawer state
    // left over from a mobile-sized viewport so the two models never fight.
    sidebar.classList.remove('active');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = '';
    open = !document.body.classList.contains('sidebar-collapsed');
  } else {
    open = sidebar.classList.contains('active');
    if (overlay) overlay.classList.toggle('active', open);
    document.body.style.overflow = open ? 'hidden' : '';
  }

  sidebar.setAttribute('aria-hidden', open ? 'false' : 'true');
  if (toggle) {
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    const icon = toggle.querySelector('i');
    if (icon) icon.className = open ? 'ri-close-line' : 'ri-menu-line';
  }
}
function skToggleMenu() {
  const sidebar = document.getElementById('side-menu');
  if (!sidebar) return;
  if (skSidebarIsDesktop()) {
    const collapsed = document.body.classList.toggle('sidebar-collapsed');
    try { localStorage.setItem('sidebar', collapsed ? 'collapsed' : 'open'); } catch (e) {}
  } else {
    sidebar.classList.toggle('active');
  }
  skApplySidebarState();
}
function skCloseMenu() {
  const sidebar = document.getElementById('side-menu');
  if (!sidebar) return;
  if (skSidebarIsDesktop()) {
    document.body.classList.add('sidebar-collapsed');
    try { localStorage.setItem('sidebar', 'collapsed'); } catch (e) {}
  } else {
    sidebar.classList.remove('active');
  }
  skApplySidebarState();
}
function skInitSidebar() {
  try {
    if (localStorage.getItem('sidebar') === 'collapsed') {
      document.body.classList.add('sidebar-collapsed');
    }
  } catch (e) {}
  skApplySidebarState();
}
skInitSidebar();
window.addEventListener('resize', skApplySidebarState);
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') skCloseMenu();
});
function skToggleTheme() {
  const isLight = document.body.classList.toggle('light-mode');
  const next = isLight ? 'light' : 'dark';
  localStorage.setItem('theme', next);
  skApplyTheme(next);
  // Best-effort sync to the server so Settings shows the current value on next visit --
  // never blocks the instant local toggle above on network success.
  if (window.fetch && document.querySelector('meta[name="csrf-token"]')) {
    fetch('/settings/update', {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ field: 'theme', value: next }),
    }).catch(() => {});
  }
}
