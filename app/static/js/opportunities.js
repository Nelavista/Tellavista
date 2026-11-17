// Nelavista Opportunities: save, share, "I applied", and the "did you apply?" prompt
// shown when a student comes back from an official application page.
// Everything degrades without JS: Apply is a plain link, Report is a plain form.
(function () {
  'use strict';

  var page = document.querySelector('.opp-detail[data-opp-id]');
  var pageOppId = page ? page.getAttribute('data-opp-id') : null;
  var pageSlug = page ? page.getAttribute('data-opp-slug') : null;
  // Discover listings and gigs share this script; each page/card says which API it uses.
  var DEFAULT_BASE = '/opportunities/discover/';
  var pageBase = (page && page.getAttribute('data-opp-base')) || DEFAULT_BASE;
  function baseFor(el) {
    var holder = el && el.closest('[data-opp-base]');
    return (holder && holder.getAttribute('data-opp-base')) || pageBase;
  }
  var PENDING_KEY = 'nv_opp_apply_pending';
  var PENDING_MAX_MS = 3 * 60 * 60 * 1000;

  function toast(msg) {
    var el = document.getElementById('opp-toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.add('show');
    clearTimeout(el._t);
    el._t = setTimeout(function () { el.classList.remove('show'); }, 2600);
  }

  function post(url, body) {
    return fetch(url, {
      method: 'POST', credentials: 'same-origin',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(body || {})
    }).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  function storage() { try { return window.sessionStorage; } catch (e) { return null; } }
  function getPending() {
    var s = storage(); if (!s) return null;
    try { var v = JSON.parse(s.getItem(PENDING_KEY) || 'null'); } catch (e) { return null; }
    if (!v || Date.now() - v.t > PENDING_MAX_MS) return null;
    return v;
  }
  function setPending(slug) { var s = storage(); if (s) try { s.setItem(PENDING_KEY, JSON.stringify({ slug: slug, t: Date.now() })); } catch (e) {} }
  function clearPending() { var s = storage(); if (s) try { s.removeItem(PENDING_KEY); } catch (e) {} }

  // ---- save
  function setSaveUi(btn, saved) {
    btn.classList.toggle('saved', saved);
    btn.setAttribute('aria-pressed', saved ? 'true' : 'false');
    var icon = btn.querySelector('i');
    if (icon) icon.className = saved ? 'ri-bookmark-fill' : 'ri-bookmark-line';
    if (btn.hasAttribute('title')) btn.setAttribute('title', saved ? 'Saved' : 'Save');
    var label = btn.querySelector('[data-save-label]');
    if (label) label.textContent = saved ? 'Saved' : 'Save';
  }

  // ---- applied
  function isApplied() {
    var box = document.querySelector('[data-opp-applied-box]');
    return !!(box && box.classList.contains('is-applied'));
  }
  function setApplied(applied) {
    if (!pageOppId) return;
    post(pageBase + pageOppId + '/applied', { applied: applied }).then(function (res) {
      document.querySelectorAll('[data-opp-applied-box]').forEach(function (box) {
        box.classList.toggle('is-applied', !!res.applied);
        var label = box.querySelector('[data-opp-applied-label]');
        if (label && res.applied_label && !box.classList.contains('compact')) label.textContent = res.applied_label;
      });
      clearPending();
      toast(res.applied ? 'Marked as applied' : 'Removed from your applications');
    }).catch(function () { toast("Couldn't update. Check your connection and try again."); });
  }

  // ---- share
  function shareText(btn) {
    var t = btn.getAttribute('data-share-title'), o = btn.getAttribute('data-share-org'), d = btn.getAttribute('data-share-deadline');
    var label = btn.getAttribute('data-share-label') || 'Deadline';
    return t + ' (' + o + ')' + (d ? '. ' + label + ': ' + d : '') + '. Found on Nelavista:';
  }
  function logShare(id, channel, base) { post((base || pageBase) + id + '/share', { channel: channel }).catch(function () {}); }
  function openShareSheet(btn) {
    var id = btn.getAttribute('data-opp-share'), url = btn.getAttribute('data-share-url'), text = shareText(btn);
    var full = text + ' ' + url;
    var sheet = document.getElementById('opp-share-sheet');
    if (!sheet) {
      sheet = document.createElement('div');
      sheet.id = 'opp-share-sheet';
      sheet.className = 'opp-sheet';
      sheet.setAttribute('role', 'dialog');
      sheet.setAttribute('aria-modal', 'true');
      sheet.innerHTML = '<div class="opp-sheet-card"><h3>Share this opportunity</h3><div class="opp-share-grid">' +
        '<a data-ch="whatsapp" target="_blank" rel="noopener"><i class="ri-whatsapp-line"></i>WhatsApp</a>' +
        '<a data-ch="telegram" target="_blank" rel="noopener"><i class="ri-telegram-line"></i>Telegram</a>' +
        '<a data-ch="x" target="_blank" rel="noopener"><i class="ri-twitter-x-line"></i>X</a>' +
        '<button type="button" data-ch="copy"><i class="ri-link"></i>Copy link</button>' +
        '</div><div class="opp-sheet-actions"><button type="button" class="sk-btn ghost" data-close-sheet>Close</button></div></div>';
      document.body.appendChild(sheet);
    }
    var enc = encodeURIComponent;
    sheet.querySelector('[data-ch="whatsapp"]').href = 'https://wa.me/?text=' + enc(full);
    sheet.querySelector('[data-ch="telegram"]').href = 'https://t.me/share/url?url=' + enc(url) + '&text=' + enc(text);
    sheet.querySelector('[data-ch="x"]').href = 'https://twitter.com/intent/tweet?text=' + enc(text) + '&url=' + enc(url);
    sheet._oppId = id; sheet._full = full; sheet._url = url; sheet._base = baseFor(btn);
    sheet.hidden = false;
  }

  document.addEventListener('click', function (e) {
    // Filters panel: close when tapping outside it.
    document.querySelectorAll('details.opp-filters[open]').forEach(function (d) {
      if (!d.contains(e.target)) d.open = false;
    });

    var saveBtn = e.target.closest('[data-opp-save]');
    if (saveBtn) {
      e.preventDefault();
      var want = !saveBtn.classList.contains('saved');
      var id = saveBtn.getAttribute('data-opp-save');
      document.querySelectorAll('[data-opp-save="' + id + '"]').forEach(function (b) { setSaveUi(b, want); });
      post(baseFor(saveBtn) + id + '/save', { saved: want }).then(function () {
        toast(want ? 'Saved to My opportunities' : 'Removed from saved');
      }).catch(function () {
        document.querySelectorAll('[data-opp-save="' + id + '"]').forEach(function (b) { setSaveUi(b, !want); });
        toast("Couldn't save. Check your connection and try again.");
      });
      return;
    }

    var shareBtn = e.target.closest('[data-opp-share]');
    if (shareBtn) {
      e.preventDefault();
      var sid = shareBtn.getAttribute('data-opp-share');
      if (navigator.share) {
        navigator.share({ title: shareBtn.getAttribute('data-share-title'), text: shareText(shareBtn), url: shareBtn.getAttribute('data-share-url') })
          .then(function () { logShare(sid, 'native', baseFor(shareBtn)); }).catch(function () {});
      } else {
        openShareSheet(shareBtn);
      }
      return;
    }

    var ch = e.target.closest('#opp-share-sheet [data-ch]');
    if (ch) {
      var sheet = document.getElementById('opp-share-sheet');
      var channel = ch.getAttribute('data-ch');
      logShare(sheet._oppId, channel, sheet._base);
      if (channel === 'copy') {
        e.preventDefault();
        var done = function () { toast('Link copied'); };
        if (navigator.clipboard) navigator.clipboard.writeText(sheet._full).then(done, function () { window.prompt('Copy this link', sheet._url); });
        else window.prompt('Copy this link', sheet._url);
      }
      sheet.hidden = true;
      return;
    }

    var applyLink = e.target.closest('[data-opp-apply]');
    if (applyLink && pageSlug) {
      setPending(pageSlug);
      // Brief pressed state so a slow-opening tab doesn't look like a dead tap.
      if (!applyLink.classList.contains('is-opening')) {
        var original = applyLink.innerHTML;
        applyLink.classList.add('is-opening');
        applyLink.setAttribute('aria-busy', 'true');
        applyLink.textContent = 'Opening…';
        setTimeout(function () {
          applyLink.classList.remove('is-opening');
          applyLink.removeAttribute('aria-busy');
          applyLink.innerHTML = original;
        }, 1800);
      }
      return; // let the link open normally
    }


    var appliedBtn = e.target.closest('[data-opp-applied]');
    if (appliedBtn) {
      e.preventDefault();
      setApplied(appliedBtn.getAttribute('data-opp-applied') === '1');
    }

    if (e.target.closest('[data-opp-report-open]')) {
      var rs = document.getElementById('opp-report-sheet');
      if (rs) rs.hidden = false;
      return;
    }

    if (e.target.closest('[data-close-sheet]') || e.target.classList.contains('opp-sheet')) {
      var s = e.target.closest('.opp-sheet');
      if (s) s.hidden = true;
      if (s && s.id === 'opp-return-sheet') clearPending();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.opp-sheet').forEach(function (s) { s.hidden = true; });
    document.querySelectorAll('details.opp-filters[open]').forEach(function (d) {
      d.open = false;
      var sum = d.querySelector('summary'); if (sum) sum.focus();
    });
  });

  // ---- "Welcome back, did you apply?" when returning from the official site
  function maybePromptReturn() {
    if (!pageSlug || isApplied()) return;
    var p = getPending();
    if (!p || p.slug !== pageSlug) return;
    var sheet = document.getElementById('opp-return-sheet');
    if (sheet && sheet.hidden) sheet.hidden = false;
  }
  var leftAt = 0;
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'hidden') { leftAt = Date.now(); return; }
    // Only after a real trip away (a few seconds), not a quick tab flick.
    if (leftAt && Date.now() - leftAt > 4000) maybePromptReturn();
  });
  window.addEventListener('pageshow', function () {
    // Came back via the back button from the in-app view (same tab).
    var p = getPending();
    if (p && Date.now() - p.t > 4000) maybePromptReturn();
  });
})();
