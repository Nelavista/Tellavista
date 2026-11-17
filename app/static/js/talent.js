/* Nelavista Talent: progressive enhancement only. Every page works without this file. */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Header border once the page scrolls.
  var header = document.querySelector('[data-tn-header]');
  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 4); }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu.
  var btn = document.querySelector('[data-tn-menu]');
  var panel = document.querySelector('[data-tn-mobile]');
  function setMenu(open) {
    if (!btn || !panel) return;
    btn.setAttribute('aria-expanded', String(open));
    panel.hidden = !open;
    header.classList.toggle('is-open', open);
    document.body.classList.toggle('tn-menu-open', open);
  }
  if (btn && panel) {
    btn.addEventListener('click', function () { setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    panel.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') { setMenu(false); btn.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 900) setMenu(false); });
  }

  // Request form: after a failed submit, move focus to the error summary.
  var formErrors = document.getElementById('form-errors');
  if (formErrors) {
    formErrors.focus({ preventScroll: true });
    formErrors.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
  }

  // Directory filter.
  var filter = document.querySelector('[data-tn-filter]');
  var grid = document.querySelector('[data-tn-grid]');
  var empty = document.querySelector('[data-tn-empty]');
  if (filter && grid) {
    filter.addEventListener('click', function (e) {
      var b = e.target.closest('button[data-filter]');
      if (!b) return;
      var cat = b.getAttribute('data-filter');
      filter.querySelectorAll('button').forEach(function (x) {
        var on = x === b;
        x.classList.toggle('is-active', on);
        x.setAttribute('aria-pressed', String(on));
      });
      var shown = 0;
      grid.querySelectorAll('[data-category]').forEach(function (card) {
        var match = cat === 'all' || card.getAttribute('data-category') === cat;
        card.hidden = !match;
        if (match) shown++;
      });
      if (empty) empty.hidden = shown !== 0;
    });
  }

  // Homepage mobile "Request Talent" bar: shows once the hero is out of view.
  var bar = document.querySelector('[data-tn-mobile-bar]');
  var hero = document.querySelector('[data-tn-hero]');
  var finalCta = document.querySelector('.tn-final');
  if (bar && hero && 'IntersectionObserver' in window) {
    document.body.classList.add('tn-has-mobile-bar');
    var heroVisible = true, finalVisible = false;
    var update = function () { bar.classList.toggle('is-visible', !heroVisible && !finalVisible); };
    new IntersectionObserver(function (es) { heroVisible = es[0].isIntersecting; update(); }).observe(hero);
    if (finalCta) new IntersectionObserver(function (es) { finalVisible = es[0].isIntersecting; update(); }).observe(finalCta);
  }

  // Quiet reveal for section content. Skipped entirely for reduced motion.
  if (!reduce && 'IntersectionObserver' in window) {
    var targets = document.querySelectorAll(
      '.tn-head, .tn-card, .tn-cat, .tn-pipe-step, .tn-std-row, .tn-step, .tn-use, .tn-excerpt, .tn-journey li, .tn-proof-format, .tn-diff-head'
    );
    doc.classList.add('tn-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add('is-in');
        io.unobserve(el);
        // Hand transitions back to the component (hover states) once revealed.
        setTimeout(function () {
          el.classList.remove('tn-reveal', 'is-in');
          el.style.transitionDelay = '';
        }, 900);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    targets.forEach(function (el, i) {
      // Stagger siblings slightly; cap so long lists don't drag.
      var idx = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.transitionDelay = Math.min(idx, 5) * 50 + 'ms';
      el.classList.add('tn-reveal');
      io.observe(el);
    });
  }
})();
