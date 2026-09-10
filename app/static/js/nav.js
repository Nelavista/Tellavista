// Shared behavior for templates/components/navbar.html — extracted from templates/landing.html.
// Powers every public page: canvas ribbon background, theme toggle, slide-out menu, PWA install
// prompt, scroll-based top-bar morph, and reveal-on-scroll (a no-op on pages with no .reveal
// elements). Load this after navbar.html's markup is on the page.
(function () {
  // ===== ANIMATED BACKGROUND =====
  const canvas = document.getElementById('nelavista-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let width, height, ribbons = [];
    const RIBBON_COUNT = 14;

    function resize() {
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width;
      canvas.height = height;
    }
    window.addEventListener('resize', resize);
    resize();

    class Ribbon {
      constructor() {
        this.reset();
        this.points = [];
        this.generatePoints();
      }
      reset() {
        this.baseY = Math.random() * height;
        this.amplitude = 70 + Math.random() * 100;
        this.frequency = 0.004 + Math.random() * 0.006;
        this.speed = 0.15 + Math.random() * 0.35;
        this.phase = Math.random() * Math.PI * 2;
        this.opacity = 0.12 + Math.random() * 0.2;
        this.lineWidth = 0.4 + Math.random() * 1.2;
      }
      generatePoints() {
        this.points = [];
        for (let x = 0; x <= width; x += 18) {
          this.points.push({ x, y: 0 });
        }
      }
      update(scrollOffset = 0) {
        this.phase += this.speed * 0.008;
        const dynamicBase = this.baseY + Math.sin(scrollOffset * 0.0004 + this.phase) * 35;
        for (let i = 0; i < this.points.length; i++) {
          const pt = this.points[i];
          if (!pt) continue;
          pt.y = dynamicBase + Math.sin(pt.x * this.frequency + this.phase) * this.amplitude;
        }
      }
      draw(ctx) {
        if (this.points.length < 2) return;
        ctx.beginPath();
        ctx.moveTo(this.points[0].x, this.points[0].y);
        for (let i = 1; i < this.points.length - 1; i++) {
          const xc = (this.points[i].x + this.points[i + 1].x) / 2;
          const yc = (this.points[i].y + this.points[i + 1].y) / 2;
          ctx.quadraticCurveTo(this.points[i].x, this.points[i].y, xc, yc);
        }
        const isLight = document.body.classList.contains('light-theme');
        const strokeColor = isLight ? `rgba(37,99,235,${this.opacity * 0.7})` : `rgba(56,189,248,${this.opacity})`;
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = this.lineWidth;
        ctx.stroke();
      }
    }

    for (let i = 0; i < RIBBON_COUNT; i++) ribbons.push(new Ribbon());

    function animate() {
      if (document.hidden) {
        requestAnimationFrame(animate);
        return;
      }
      ctx.clearRect(0, 0, width, height);
      const scrollY = window.scrollY || 0;
      ribbons.forEach(r => {
        r.update(scrollY);
        r.draw(ctx);
      });
      requestAnimationFrame(animate);
    }
    animate();

    window.addEventListener('resize', () => {
      ribbons.forEach(r => r.generatePoints());
    });
  }

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
    let ct = st || (pd ? 'dark' : 'light');

    const icon = tt.querySelector('.theme-icon');
    function applyTheme(t) {
      if (t === 'light') {
        b.classList.add('light-theme');
        if (icon) icon.textContent = '☀️';
      } else {
        b.classList.remove('light-theme');
        if (icon) icon.textContent = '🌙';
      }
      localStorage.setItem('theme', t);
    }
    applyTheme(ct);
    tt.addEventListener('click', () => {
      ct = b.classList.contains('light-theme') ? 'dark' : 'light';
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
