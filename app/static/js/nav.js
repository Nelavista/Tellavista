// Shared behavior for templates/components/navbar.html — extracted from templates/landing.html.
// Powers every public page: theme toggle, slide-out menu, PWA install
// prompt, scroll-based top-bar morph, and reveal-on-scroll (a no-op on pages with no .reveal
// elements). Load this after navbar.html's markup is on the page.
(function () {
  // ===== PWA INSTALL PROMPT =====
  let deferredPrompt, isAppInstalled = false;
  if (window.matchMedia('(display-mode: standalone)').matches) isAppInstalled = true;
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    const btn = document.getElementById('header-install-btn');
    if (btn) btn.classList.add('show');
  });
  window.addEventListener('appinstalled', () => {
    isAppInstalled = true;
    deferredPrompt = null;
    const btn = document.getElementById('header-install-btn');
    if (btn) btn.classList.remove('show');
  });
  window.installApp = function () {
    if (isAppInstalled) {
      alert('Nelavista is already installed!');
      return;
    }
    if (deferredPrompt) {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(() => {
        deferredPrompt = null;
        const btn = document.getElementById('header-install-btn');
        if (btn) btn.classList.remove('show');
      });
    }
  };

  // ===== THEME TOGGLE =====
  const tt = document.getElementById('theme-toggle');
  if (tt) {
    const b = document.body;
    const st = localStorage.getItem('theme');
    const pd = window.matchMedia('(prefers-color-scheme: dark)').matches;
    let ct = st || 'system';

    const icon = tt.querySelector('.theme-icon');
    function applyTheme(t) {
      const effective = t === 'system' ? (pd ? 'dark' : 'light') : t;
      if (effective === 'light') {
        b.classList.add('light-theme');
        if (icon) icon.innerHTML = '<i class="ri-sun-line"></i>';
      } else {
        b.classList.remove('light-theme');
        if (icon) icon.innerHTML = '<i class="ri-moon-line"></i>';
      }
    }
    applyTheme(ct);
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if ((localStorage.getItem('theme') || 'system') === 'system') applyTheme('system');
      });
    }
    tt.addEventListener('click', () => {
      ct = b.classList.contains('light-theme') ? 'dark' : 'light';
      localStorage.setItem('theme', ct);
      tt.classList.add('spin');
      applyTheme(ct);
      setTimeout(() => tt.classList.remove('spin'), 400);
    });
  }

  // ===== SLIDE-OUT MENU =====
  const mt = document.getElementById('menu-toggle'),
    sm = document.getElementById('side-menu'),
    ov = document.getElementById('overlay'),
    cs = document.getElementById('closeSidebar');
  if (mt && sm && ov && cs) {
    const openMenu = () => {
      sm.classList.add('active');
      ov.classList.add('active');
      mt.classList.add('is-open');
      mt.setAttribute('aria-expanded', 'true');
      mt.setAttribute('aria-label', 'Close menu');
      requestAnimationFrame(() => ov.classList.add('show'));
    };
    const closeMenu = () => {
      sm.classList.remove('active');
      ov.classList.remove('show');
      mt.classList.remove('is-open');
      mt.setAttribute('aria-expanded', 'false');
      mt.setAttribute('aria-label', 'Open menu');
      setTimeout(() => ov.classList.remove('active'), 400);
    };
    mt.addEventListener('click', () => (sm.classList.contains('active') ? closeMenu() : openMenu()));
    cs.addEventListener('click', closeMenu);
    ov.addEventListener('click', closeMenu);
    document.querySelectorAll('a[href^="#"]').forEach(a =>
      a.addEventListener('click', function (e) {
        const t = document.querySelector(this.getAttribute('href'));
        if (t) {
          e.preventDefault();
          t.scrollIntoView({ behavior: 'smooth' });
          closeMenu();
        }
      })
    );
  }

  // ===== TOP BAR SCROLL MORPH =====
  const topBar = document.getElementById('top-bar');
  if (topBar) {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    let navTicking = false;
    function applyNavScrollState() {
      const y = window.scrollY || 0;
      const p = Math.min(y / 90, 1);
      topBar.classList.toggle('scrolled', y > 10);
      if (!reduceMotion) {
        topBar.style.setProperty('--nav-h', (84 - p * 12) + 'px');
        topBar.style.setProperty('--nav-blur', (20 + p * 14) + 'px');
        topBar.style.setProperty('--nav-op', (0.55 + p * 0.34).toFixed(2));
      }
      navTicking = false;
    }
    applyNavScrollState();
    window.addEventListener('scroll', () => {
      if (!navTicking) {
        requestAnimationFrame(applyNavScrollState);
        navTicking = true;
      }
    }, { passive: true });
  }

  // ===== REVEAL ON SCROLL (no-op if the page has no .reveal elements) =====
  const revealTargets = document.querySelectorAll('.reveal');
  if (revealTargets.length) {
    const revealObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.classList.add('visible');
          revealObs.unobserve(e.target);
        }
      });
    }, { threshold: 0.1 });
    revealTargets.forEach(el => revealObs.observe(el));
  }

  // ===== COUNT-UP STATS (no-op if the page has none) =====
  const countTargets = document.querySelectorAll('.count-up');
  if (countTargets.length) {
    const countObs = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target, target = parseInt(el.dataset.target, 10);
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
          el.textContent = target.toLocaleString();
          return;
        }
        const duration = 1400, start = performance.now();
        function tick(now) {
          const p = Math.min((now - start) / duration, 1);
          el.textContent = Math.round((1 - Math.pow(1 - p, 3)) * target).toLocaleString();
          if (p < 1) requestAnimationFrame(tick);
        }
        requestAnimationFrame(tick);
        countObs.unobserve(el);
      });
    }, { threshold: 0.5 });
    countTargets.forEach(el => countObs.observe(el));
  }

  // ===== POINTER-TRACKED GLOW (nav CTA + feature cards, if present) =====
  document.querySelectorAll('.header-cta, .feature-card').forEach(el => {
    el.addEventListener('pointermove', (e) => {
      const r = el.getBoundingClientRect();
      el.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
      el.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
    });
  });

  // Nelavista is a plain website for now — no offline mode. Actively unregister any
  // service worker left over from earlier visits so it stops intercepting requests.
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.getRegistrations().then(regs => {
      regs.forEach(reg => reg.unregister());
    });
    if (window.caches) {
      caches.keys().then(names => names.forEach(name => caches.delete(name)));
    }
  }
})();
