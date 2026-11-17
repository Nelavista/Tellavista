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
    btn.setAttribute('aria-expanded', String(open));
    panel.hidden = !open;
    header.classList.toggle('is-open', open);
    document.body.classList.toggle('tx-menu-open', open);
  }
  if (btn && panel && header) {
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

  // Talent directory filters.
  var form = document.querySelector('[data-tn-filter-form]');
  var grid = document.querySelector('[data-tn-grid]');
  if (form && grid) {
    var details = document.querySelector('[data-tn-filters]');
    var countEl = document.querySelector('[data-tn-result-count]');
    var badge = document.querySelector('[data-tn-filter-count]');
    var empty = document.querySelector('[data-tn-empty]');
    var cards = Array.prototype.slice.call(grid.querySelectorAll('[data-category]'));
    var checked = function (name) {
      return Array.prototype.map.call(form.querySelectorAll('input[name="' + name + '"]:checked'), function (i) { return i.value; });
    };
    var apply = function () {
      var cat = form.category.value, country = form.country.value;
      var skill = form.skill.value.trim().toLowerCase();
      var levels = checked('level'), work = checked('work');
      var availableOnly = checked('available').length > 0, vettedOnly = checked('vetted').length > 0;
      var active = [cat, country, skill].filter(Boolean).length + levels.length + work.length + (availableOnly ? 1 : 0) + (vettedOnly ? 1 : 0);
      var shown = 0;
      cards.forEach(function (c) {
        var d = c.dataset;
        var cardWork = d.work.split('|');
        var ok = (!cat || d.category === cat) &&
          (!country || d.country === country) &&
          (!skill || d.skills.indexOf(skill) !== -1) &&
          (!levels.length || levels.indexOf(d.level) !== -1) &&
          (!work.length || work.some(function (w) { return cardWork.indexOf(w) !== -1; })) &&
          (!availableOnly || d.availability === 'available') &&
          (!vettedOnly || d.vetted === '1');
        c.hidden = !ok;
        if (ok) shown++;
      });
      if (countEl) countEl.textContent = shown;
      if (empty) empty.hidden = shown !== 0;
      if (badge) { badge.hidden = !active; badge.textContent = active; }
    };
    form.addEventListener('input', apply);
    form.addEventListener('change', apply);
    form.addEventListener('reset', function () { setTimeout(apply, 0); });
    // Collapse the filter panel on small screens; it's a sidebar on desktop.
    if (details && window.matchMedia('(max-width: 1140px)').matches) details.open = false;
  }

  // Homepage mobile action bar: shown once the hero is out of view, hidden at the final CTA.
  var bar = document.querySelector('[data-tn-mobile-bar]');
  var hero = document.querySelector('[data-tn-hero]');
  var finalCta = document.querySelector('.tx-final');
  if (bar && hero && 'IntersectionObserver' in window) {
    document.body.classList.add('tx-has-mobile-bar');
    var heroVisible = true, finalVisible = false;
    var update = function () { bar.classList.toggle('is-visible', !heroVisible && !finalVisible); };
    new IntersectionObserver(function (es) { heroVisible = es[0].isIntersecting; update(); }).observe(hero);
    if (finalCta) new IntersectionObserver(function (es) { finalVisible = es[0].isIntersecting; update(); }).observe(finalCta);
  }

  // Quiet reveal for section content. Skipped entirely for reduced motion.
  if (!reduce && 'IntersectionObserver' in window) {
    var targets = document.querySelectorAll(
      '.tx-head, .tx-layer, .tx-cred, .tx-cat, .tx-step, .tx-use, .tx-excerpt, .tx-eco li, .tx-journey li, .tx-africa-copy, .tx-emp-media, .tx-talent-media'
    );
    doc.classList.add('tx-js');
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add('is-in');
        io.unobserve(el);
        // Hand transitions back to the component (hover states) once revealed.
        setTimeout(function () { el.classList.remove('tx-reveal', 'is-in'); el.style.transitionDelay = ''; }, 1000);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    targets.forEach(function (el) {
      var idx = Array.prototype.indexOf.call(el.parentNode.children, el);
      el.style.transitionDelay = Math.min(idx, 5) * 50 + 'ms';
      el.classList.add('tx-reveal');
      io.observe(el);
    });
  }
})();
