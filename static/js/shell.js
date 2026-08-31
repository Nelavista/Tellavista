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
  const pref = localStorage.getItem('theme') || 'dark';
  skApplyTheme(skResolveTheme(pref));
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', () => {
      if ((localStorage.getItem('theme') || 'dark') === 'system') {
        skApplyTheme(skResolveTheme('system'));
      }
    });
  }
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(regs => regs.forEach(r => r.unregister()));
  }
})();

function skToggleMenu() {
  document.getElementById('side-menu').classList.toggle('active');
  document.getElementById('overlay').classList.toggle('active');
  document.body.style.overflow = document.getElementById('side-menu').classList.contains('active') ? 'hidden' : '';
}
function skClosMenu() {
  document.getElementById('side-menu').classList.remove('active');
  document.getElementById('overlay').classList.remove('active');
  document.body.style.overflow = '';
}
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
