// Shared app-shell behavior: mobile drawer + theme toggle. Used by every authenticated
// screen via components/skills_footer.html (Skills) or components/academia_footer.html
// (Academia) — extracted here so the two shells don't carry two copies of the same script.
(function () {
  const theme = localStorage.getItem('theme') || 'dark';
  if (theme === 'light') {
    document.body.classList.add('light-mode');
    const icon = document.querySelector('#theme-toggle i');
    if (icon) icon.className = 'ri-sun-line';
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
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
  const icon = document.querySelector('#theme-toggle i');
  if (icon) icon.className = isLight ? 'ri-sun-line' : 'ri-moon-line';
  const meta = document.querySelector('meta[name="theme-color"]');
  if (meta) meta.content = isLight ? '#f3f4f6' : '#050810';
}
