/* Landing page skills section: renders the glass tab bar and the curved card stage from
   the #skills-data JSON config written by _landing_stats() (routes/dashboard_routes.py),
   so no tab or card is hardcoded in the markup.

   Behaviour:
   - tabs select a category; a glass pill slides behind the selected tab (transform+width)
   - cards sit on a convex arc that stays centred for any card count: 1 card = a single
     tilted card, 2-5 = a symmetric arc, 6-9 = a tighter arc with ~5 cards visible that
     auto-advances its centre card every few seconds
   - changing tab slides the old set out and the new set in, staggered from the centre
     outward; direction follows tab order
   - everything animates transform + opacity only; prefers-reduced-motion collapses the
     slide to a crossfade and stops the auto-advance
*/
(function () {
  'use strict';

  var dataEl = document.getElementById('skills-data');
  var tablist = document.querySelector('[data-skills-tabs]');
  var stage = document.querySelector('[data-skills-stage]');
  if (!dataEl || !tablist || !stage) return;

  var tabs = null;
  try {
    tabs = JSON.parse(dataEl.textContent || '[]');
  } catch (err) {
    tabs = null;
  }
  if (!Array.isArray(tabs) || !tabs.length) return;

  var panel = stage; // role="tabpanel" — aria-labelledby points at the selected tab
  var staticBase = stage.getAttribute('data-skills-static') || ''; // "/static/" from url_for
  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  var narrowScreen = window.matchMedia('(max-width: 760px)');

  var MOVE_MS = 600;     // one slide; with the outermost stagger the whole move lands ~800ms
  var STAGGER_MS = 40;   // centre card first, ~40-60ms per ring outward
  var OFF_STAGE = 320;   // how far the incoming/outgoing sets travel
  var AUTO_MS = 3400;    // dense tabs advance to the next centre card every 3-4 seconds

  // Gradient families per category, built from the site's accent palette (sky, violet,
  // amber, pink, indigo, emerald) — one hue family per tab, angle/stops vary per card.
  var HUES = {
    tech: 199,
    design: 268,
    business: 34,
    creative: 332,
    career: 246,
    sustainability: 158
  };

  var active = 0;
  var centre = 0;
  var cards = [];
  var autoTimer = null;

  /* ─── TAB BAR ─── */

  var pill = document.createElement('span');
  pill.className = 'skills-tab-pill';
  pill.setAttribute('aria-hidden', 'true');
  tablist.appendChild(pill);

  var tabButtons = tabs.map(function (tab, index) {
    var button = document.createElement('button');
    button.type = 'button';
    button.className = 'skills-tab';
    button.id = 'skills-tab-' + index;
    button.setAttribute('role', 'tab');
    button.setAttribute('aria-controls', panel.id);
    button.setAttribute('aria-selected', index === 0 ? 'true' : 'false');
    button.tabIndex = index === 0 ? 0 : -1;
    button.appendChild(document.createTextNode(tab.label || ''));
    var count = document.createElement('span');
    count.className = 'skills-tab-count';
    count.textContent = String(Array.isArray(tab.cards) ? tab.cards.length : 0);
    button.appendChild(count);
    button.addEventListener('click', function () {
      selectTab(index);
    });
    tablist.appendChild(button);
    return button;
  });

  function movePill(index, instant) {
    var button = tabButtons[index];
    if (!button) return;
    if (instant) pill.style.transition = 'none';
    pill.style.width = button.offsetWidth + 'px';
    pill.style.transform = 'translate3d(' + button.offsetLeft + 'px, 0, 0)';
    if (instant) {
      pill.getBoundingClientRect(); // commit the jump before transitions come back
      pill.style.transition = '';
    }
  }

  tablist.addEventListener('keydown', function (event) {
    var next = null;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (active + 1) % tabs.length;
    else if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (active - 1 + tabs.length) % tabs.length;
    else if (event.key === 'Home') next = 0;
    else if (event.key === 'End') next = tabs.length - 1;
    if (next === null) return;
    event.preventDefault();
    selectTab(next, true);
  });

  function selectTab(index, moveFocus) {
    if (index < 0 || index >= tabs.length) return;
    if (index === active) {
      if (moveFocus) tabButtons[index].focus();
      return;
    }
    var dir = index > active ? 1 : -1;
    active = index;
    tabButtons.forEach(function (button, i) {
      var selected = i === active;
      button.setAttribute('aria-selected', selected ? 'true' : 'false');
      button.tabIndex = selected ? 0 : -1;
      if (selected) panel.setAttribute('aria-labelledby', button.id);
    });
    if (moveFocus) tabButtons[active].focus();
    movePill(active);
    // Keeps the selected tab in view inside the horizontally scrolling mobile bar.
    if (tabButtons[active].scrollIntoView) {
      tabButtons[active].scrollIntoView({ block: 'nearest', inline: 'center' });
    }
    renderCards(dir);
    startAutoAdvance();
  }

  /* ─── ARC GEOMETRY ─── */

  function curve(count) {
    var mobile = narrowScreen.matches;
    var dense = count >= 6; // wider, tighter arc showing about five cards at once
    return {
      gap: mobile ? 132 : (dense ? 138 : 186),   // centre-to-centre spacing
      drop: mobile ? 12 : (dense ? 15 : 17),     // how fast the sides step down
      rot: mobile ? 4 : (dense ? 6.5 : 7.5),     // degrees of outward rotation per step
      tilt: mobile ? 2 : 4.5,                    // small rotateY per step
      scaleStep: mobile ? 0.05 : 0.06,
      dim: mobile ? 0.14 : 0.16,
      base: mobile ? -20 : -26,                  // lift the whole arc, centre card highest
      window: dense ? 2 : 99                     // cards beyond this offset fade out
    };
  }

  function offsetOf(index, center, count) {
    if (count < 6) return index - center; // small sets centre between two cards: symmetric
    var d = (index - center) % count;
    if (d > count / 2) d -= count;
    if (d < -count / 2) d += count;
    return d;
  }

  function applyArc(el, x, y, rz, ry, scale, opacity, z) {
    el.style.setProperty('--cx', x.toFixed(1) + 'px');
    el.style.setProperty('--cy', y.toFixed(1) + 'px');
    el.style.setProperty('--crz', rz.toFixed(2) + 'deg');
    el.style.setProperty('--cry', ry.toFixed(2) + 'deg');
    el.style.setProperty('--cs', scale.toFixed(3));
    el.style.setProperty('--co', opacity.toFixed(3));
    el.style.setProperty('--cz', String(z));
    el.classList.toggle('is-offscreen', opacity <= 0.01);
  }

  function layoutCards() {
    var count = cards.length;
    if (!count) return;
    var cfg = curve(count);
    var width = cards[0].el.offsetWidth || 264;
    var offsets = cards.map(function (card, index) {
      return offsetOf(index, centre, count);
    });
    var largest = offsets.reduce(function (max, o) {
      return Math.max(max, Math.abs(o));
    }, 0);
    // Never let the outer cards outgrow the stage on mid-size screens.
    var available = (stage.clientWidth || 1080) / 2 - width / 2 - 16;
    var gap = largest > 0 ? Math.max(0, Math.min(cfg.gap, available / largest)) : 0;

    cards.forEach(function (card, index) {
      var o = offsets[index];
      var abs = Math.abs(o);
      var hidden = abs > cfg.window;
      card.offset = o;
      card.x = o * gap;
      applyArc(
        card.el,
        card.x,
        cfg.base + o * o * cfg.drop,
        count === 1 ? -2 : o * cfg.rot,
        count === 1 ? 3 : -o * cfg.tilt,
        Math.max(0.7, 1 - Math.min(abs, 3) * cfg.scaleStep),
        hidden ? 0 : (abs < 0.01 ? 1 : Math.max(0.45, 1 - abs * cfg.dim)),
        hidden ? 0 : 20 - Math.round(abs * 2)
      );
    });
  }

  function gradient(tab, index) {
    var hue = HUES[tab.key];
    if (hue === undefined) hue = 205;               // unknown category: the site's accent blue
    var angle = 145 + ((index * 23) % 72);          // a different angle per card
    var mid = 46 + (index % 3) * 9;                 // and a different stop rhythm
    return 'linear-gradient(' + angle + 'deg,' +
      ' hsl(' + hue + ' 68% 42%) 0%,' +
      ' hsl(' + (hue + 14) + ' 62% 30%) ' + mid + '%,' +
      ' hsl(' + (hue + 26) + ' 58% 20%) 100%)';
  }

  /* ─── CARD SETS + TAB SLIDE ─── */

  function assignRings(list, keyOf) {
    var keys = [];
    list.forEach(function (item) {
      var key = Math.round(keyOf(item) * 100) / 100;
      if (keys.indexOf(key) === -1) keys.push(key);
    });
    keys.sort(function (a, b) { return a - b; });
    list.forEach(function (item) {
      var key = Math.round(keyOf(item) * 100) / 100;
      item.delay = reducedMotion.matches ? 0 : keys.indexOf(key) * STAGGER_MS;
    });
  }

  function renderCards(dir) {
    var tab = tabs[active] || {};
    var data = Array.isArray(tab.cards) ? tab.cards : [];
    var reduced = reducedMotion.matches;
    var count = data.length;

    // Dense sets loop a centre card; small sets centre between two cards for symmetry.
    centre = count >= 6 ? 0 : (count - 1) / 2;

    // Everything currently on stage slides out, including sets still mid-exit.
    var outgoing = Array.prototype.slice.call(stage.querySelectorAll('.skills-card'));

    var fresh = [];
    data.forEach(function (item, index) {
      var el = document.createElement('article');
      el.className = 'skills-card';
      el.style.setProperty('--card-bg', gradient(tab, index));
      // Each tab has its own photo; the gradient above stays as the fallback layer.
      if (tab.image && staticBase) {
        el.style.setProperty('--card-photo', 'url("' + staticBase + 'images/landing/' + tab.image + '")');
      }
      var label = document.createElement('span');
      label.className = 'skills-card-cat';
      label.textContent = tab.label || '';
      var body = document.createElement('div');
      body.className = 'skills-card-body';
      var title = document.createElement('h3');
      title.className = 'skills-card-title';
      title.textContent = item.title || '';
      var topics = document.createElement('span');
      topics.className = 'skills-card-topics';
      topics.textContent = (item.topics || 0) + ' structured topics';
      body.appendChild(title);
      body.appendChild(topics);
      el.appendChild(label);
      el.appendChild(body);
      stage.appendChild(el);
      fresh.push({ el: el, x: 0, offset: 0 });
    });
    cards = fresh;
    layoutCards();

    if (!dir || !outgoing.length) return; // first paint: already in place

    var from = dir > 0 ? 1 : -1; // forward tabs slide left, back tabs slide right
    var incomingLeavers = outgoing.map(function (el) {
      var x = parseFloat(el.style.getPropertyValue('--cx'));
      return { el: el, x: isNaN(x) ? 0 : x };
    });

    assignRings(cards, function (card) { return Math.abs(card.offset); });
    assignRings(incomingLeavers, function (card) { return Math.abs(card.x); });
    var maxDelay = cards.reduce(function (max, card) {
      return Math.max(max, card.delay);
    }, 0);

    // Hold the new set off-stage on the side it arrives from…
    cards.forEach(function (card) {
      card.el.style.transition = 'none';
      card.el.style.setProperty('--co', '0');
      if (!reduced) card.el.style.setProperty('--cx', (card.x + from * OFF_STAGE) + 'px');
    });
    // …and keep the old set travelling the way it came from.
    incomingLeavers.forEach(function (card) {
      card.el.style.setProperty('--tdel', card.delay + 'ms');
      card.el.style.setProperty('--co', '0');
      if (!reduced) card.el.style.setProperty('--cx', (card.x - from * OFF_STAGE) + 'px');
    });

    stage.getBoundingClientRect(); // commit the off-stage state before transitions run
    cards.forEach(function (card) {
      card.el.style.transition = '';
      card.el.style.setProperty('--tdel', card.delay + 'ms');
    });
    layoutCards(); // final arc positions — transform + opacity ease into them

    window.setTimeout(function () {
      incomingLeavers.forEach(function (card) {
        if (card.el.parentNode) card.el.parentNode.removeChild(card.el);
      });
      cards.forEach(function (card) {
        card.el.style.setProperty('--tdel', '0ms');
      });
    }, reduced ? 380 : MOVE_MS + maxDelay + 80);
  }

  /* ─── AUTO-ADVANCE (dense tabs only) ─── */

  function stopAutoAdvance() {
    if (autoTimer) {
      window.clearInterval(autoTimer);
      autoTimer = null;
    }
  }

  function startAutoAdvance() {
    stopAutoAdvance();
    if (reducedMotion.matches) return;
    var tab = tabs[active] || {};
    if (!Array.isArray(tab.cards) || tab.cards.length < 6) return;
    autoTimer = window.setInterval(function () {
      if (document.hidden) return; // pause while the tab is in the background
      centre = Math.floor(centre) + 1;
      layoutCards();
    }, AUTO_MS);
  }

  /* ─── INIT ─── */

  panel.setAttribute('aria-labelledby', tabButtons[0].id);
  movePill(0, true);
  renderCards(0);
  startAutoAdvance();

  // Web fonts change tab widths — snap the pill again once they settle.
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(function () {
      movePill(active, true);
    });
  }

  var resizeTimer = null;
  window.addEventListener('resize', function () {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(function () {
      movePill(active, true);
      layoutCards();
    }, 120);
  });

  document.addEventListener('visibilitychange', function () {
    if (document.hidden) stopAutoAdvance();
    else startAutoAdvance();
  });

  if (reducedMotion.addEventListener) {
    reducedMotion.addEventListener('change', function () {
      if (reducedMotion.matches) stopAutoAdvance();
      else startAutoAdvance();
    });
  }
})();
