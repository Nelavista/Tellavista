/* Nelavista Campus Map: one university's interactive map.
 *
 * Data comes from the page (<script id="cm-data">), built by services/campus_maps.py's
 * build_map_payload(). Nothing in this file is specific to one university.
 *
 * Kept from the original LASU map: Leaflet + OpenStreetMap / Esri imagery, live location
 * tracking (watchPosition), road-following routes via OSRM (Leaflet Routing Machine,
 * now loaded only when a student asks for directions) and nearest-place distance.
 * Every university (LASU, University of Abuja, ...) gets this same live map; only its
 * dataset of places differs. Place names show as map labels by zoom tier.
 * Dropped: draggable markers (a calibration tool that let
 * students move buildings on their own screen); place positions are edited by admins.
 */
(function () {
  'use strict';

  var DATA = JSON.parse(document.getElementById('cm-data').textContent);
  var SLUG = DATA.university.slug;
  var PLACES = DATA.places || [];
  var CATS = {};
  (DATA.categories || []).forEach(function (c) { CATS[c.key] = c; });
  var BY_ID = {};
  PLACES.forEach(function (p) { BY_ID[p.id] = p; });

  var KEY = {
    saved: 'nv_campus_saved_' + SLUG,
    layer: 'nv_campus_layer_' + SLUG,
    recent: 'nv_campus_recent',
  };
  var WALK_M_PER_MIN = 80;          // ~4.8 km/h
  var NEAR_CAMPUS_M = 5000;          // farther than this, routing on the campus map is pointless
  var LRM_SRC = 'https://unpkg.com/leaflet-routing-machine@3.2.12/dist/leaflet-routing-machine.min.js';

  function store(k, v) { try { if (v === undefined) return JSON.parse(localStorage.getItem(k)); localStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }
  function $(id) { return document.getElementById(id); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function isDesktop() { return window.matchMedia('(min-width: 900px)').matches; }
  function catOf(p) { return CATS[p.category] || { label: 'Other places', singular: 'Campus place', icon: 'ri-map-pin-2-line', color: '#4a5160' }; }
  function fmtDist(m) { return m < 1000 ? Math.round(m / 10) * 10 + ' m' : (m / 1000).toFixed(1) + ' km'; }
  function walkMin(m) { return Math.max(1, Math.round(m / WALK_M_PER_MIN)); }

  var toastTimer;
  function toast(msg) {
    var t = $('cm-toast');
    t.textContent = msg; t.hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.hidden = true; }, 3200);
  }

  // Remember this university for the picker's "Recently viewed".
  (function () {
    var r = (store(KEY.recent) || []).filter(function (s) { return s !== SLUG; });
    r.unshift(SLUG);
    store(KEY.recent, r.slice(0, 6));
  })();

  var campusSelect = $('cm-campus');
  if (campusSelect) campusSelect.addEventListener('change', function () {
    window.location.href = window.location.pathname + '?campus=' + encodeURIComponent(campusSelect.value);
  });

  if (!DATA.map.center) return;   // no coordinates for this campus yet: the empty state says so

  // ── Map + base layers ──────────────────────────────────────────────────────────
  // Every university uses the same live map; only the dataset differs.
  // Labels appear by tier as the student zooms in (see campus_maps.label_tier).
  var Z = { focus: 18, fitMax: 18, max: 20, tier1: 16, tier2: 18 };
  var map = L.map('cm-map', { zoomControl: false, maxZoom: Z.max, minZoom: 5, zoomSnap: 0.5, tap: true });
  L.control.zoom({ position: 'topright' }).addTo(map);
  var layers = {
    satellite: L.layerGroup([
      L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxNativeZoom: 19, maxZoom: 20, attribution: 'Imagery © Esri, Maxar, Earthstar Geographics',
      }),
    ]),
    street: L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxNativeZoom: 19, maxZoom: 20, attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }),
  };
  // The university's default base layer, unless the student switched it for this school.
  var saved_layer = store(KEY.layer);
  var layerName = saved_layer === 'street' || saved_layer === 'satellite' ? saved_layer
    : (DATA.map.default_layer === 'street' ? 'street' : 'satellite');
  layers[layerName].addTo(map);
  var layerBtn = $('cm-layer');
  function syncLayerBtn() {
    var toStreet = layerName === 'satellite';
    layerBtn.innerHTML = '<i class="' + (toStreet ? 'ri-map-2-line' : 'ri-earth-line') + '" aria-hidden="true"></i>';
    layerBtn.setAttribute('aria-label', toStreet ? 'Switch to map view' : 'Switch to satellite view');
    document.body.classList.toggle('cm-on-satellite', layerName === 'satellite');
  }
  layerBtn.addEventListener('click', function () {
    map.removeLayer(layers[layerName]);
    layerName = layerName === 'satellite' ? 'street' : 'satellite';
    layers[layerName].addTo(map);
    store(KEY.layer, layerName);
    syncLayerBtn();
  });
  syncLayerBtn();

  if (DATA.map.boundary) {
    L.polygon(DATA.map.boundary, { color: '#7d9bff', weight: 2, fill: false, dashArray: '6 6', interactive: false }).addTo(map);
  }

  var campusBounds = DATA.map.bounds ? L.latLngBounds(DATA.map.bounds).pad(0.08) : null;
  function fitCampus(animate) {
    if (campusBounds) map.fitBounds(campusBounds, fitOptions(animate));
    else map.setView(DATA.map.center, DATA.map.zoom || 16, { animate: !!animate });
  }
  function panelHeight() { var el = $('cm-panel'); return (!el || isDesktop()) ? 0 : el.getBoundingClientRect().height; }
  function fitOptions(animate) {
    var pad = { animate: !!animate, maxZoom: Z.fitMax };
    if (isDesktop()) { pad.paddingTopLeft = [24, 24]; pad.paddingBottomRight = [40, 24]; }
    else { pad.paddingTopLeft = [16, 16]; pad.paddingBottomRight = [16, panelHeight() + 16]; }
    return pad;
  }
  $('cm-fit').addEventListener('click', function () { fitCampus(true); });

  function syncLabels() {
    var z = map.getZoom(), el = $('cm-map');
    el.classList.toggle('cm-show-t1', z >= Z.tier1);
    el.classList.toggle('cm-compact', z < 17);
    el.classList.toggle('cm-show-t2', z >= Z.tier2);
  }
  map.on('zoomend', syncLabels);

  if (!PLACES.length) {   // campus coordinates but no places yet
    fitCampus(false);
    return;
  }

  // ── Markers ────────────────────────────────────────────────────────────────────
  var markers = {};
  function pinIcon(p, active) {
    var c = catOf(p);
    return L.divIcon({
      className: 'cm-pin-wrap',
      html: '<span class="cm-pin' + (active ? ' is-active' : '') + '" style="--c:' + c.color + '"><i class="' + c.icon + '"></i></span>',
      iconSize: active ? [38, 38] : [30, 30],
      iconAnchor: active ? [19, 19] : [15, 15],
    });
  }
  PLACES.forEach(function (p) {
    var m = L.marker([p.lat, p.lng], { icon: pinIcon(p, false), title: p.name, keyboard: true, riseOnHover: true });
    // Map-style text label beside the pin, shown by tier as the student zooms in.
    m.bindTooltip(esc(p.name), {
      permanent: true, direction: 'right', offset: [13, 0],
      className: 'cm-label cm-t' + (p.label_tier === 1 ? 1 : 2) + (p.category === 'faculty' ? ' cm-label-major' : ''),
    });
    m.on('click', function () { openPlace(p.id, { pan: false }); });
    markers[p.id] = m;
  });
  function showOnMap(p, show) {
    var m = markers[p.id];
    if (show && !map.hasLayer(m)) m.addTo(map);
    else if (!show && map.hasLayer(m)) map.removeLayer(m);
  }

  // A place's block outline (where its dataset has one) is drawn only while it is open.
  var outline = null;
  function showOutline(p) {
    if (outline) { map.removeLayer(outline); outline = null; }
    if (p && p.outline) {
      outline = L.polygon(p.outline, { color: '#3a5fe0', weight: 2, opacity: 0.9, fillColor: '#3a5fe0', fillOpacity: 0.1, interactive: false }).addTo(map);
    }
  }

  // ── Panel (bottom sheet on phones, side panel on desktop) ────────────────────────
  var panel = $('cm-panel');
  var handle = $('cm-handle');
  function setSheet(state) {
    panel.setAttribute('data-state', state);
    handle.setAttribute('aria-expanded', state === 'peek' ? 'false' : 'true');
    handle.setAttribute('aria-label', state === 'peek' ? 'Show list of places' : 'Hide list of places');
  }
  
  handle.addEventListener('click', function () {
    var s = panel.getAttribute('data-state');
    if (s === 'peek') setSheet(selectedId ? 'detail' : 'list');
    else setSheet('peek');
  });
  // Swipe the handle area up/down on touch screens.
  (function () {
    var y0 = null;
    var zone = $('cm-panel-top');
    [handle, zone].forEach(function (el) {
      el.addEventListener('touchstart', function (e) { y0 = e.touches[0].clientY; }, { passive: true });
      el.addEventListener('touchend', function (e) {
        if (y0 == null) return;
        var dy = e.changedTouches[0].clientY - y0; y0 = null;
        if (dy < -40 && panel.getAttribute('data-state') === 'peek') setSheet(selectedId ? 'detail' : 'list');
        else if (dy > 40 && panel.getAttribute('data-state') !== 'peek' && document.activeElement !== $('cm-search')) setSheet('peek');
      }, { passive: true });
    });
  })();
  map.on('click', function () { if (!isDesktop() && !selectedId) setSheet('peek'); });

  // ── Filters: search + category chips ───────────────────────────────────────────
  var saved = new Set(store(KEY.saved) || []);
  var activeCat = 'all';
  var query = '';
  var searchInput = $('cm-search');
  var searchBox = $('cm-search-box');

  function renderChips() {
    var chips = [{ key: 'all', label: 'All', count: PLACES.length }];
    var savedCount = PLACES.filter(function (p) { return saved.has(p.id); }).length;
    if (savedCount) chips.push({ key: 'saved', label: 'Saved', icon: 'ri-bookmark-fill', count: savedCount });
    (DATA.categories || []).forEach(function (c) { chips.push(c); });
    if (activeCat === 'saved' && !savedCount) activeCat = 'all';
    $('cm-chips').innerHTML = chips.map(function (c) {
      var on = c.key === activeCat;
      return '<button type="button" class="cm-chip' + (on ? ' is-on' : '') + '" data-cat="' + esc(c.key) + '" aria-pressed="' + on + '"' +
        (c.color ? ' style="--c:' + c.color + '"' : '') + '>' +
        (c.color ? '<span class="cm-chip-dot" aria-hidden="true"></span>' : (c.icon ? '<i class="' + c.icon + '" aria-hidden="true"></i>' : '')) +
        esc(c.label) + '<span class="n">' + c.count + '</span></button>';
    }).join('');
  }
  $('cm-chips').addEventListener('click', function (e) {
    var b = e.target.closest('.cm-chip');
    if (!b) return;
    activeCat = b.getAttribute('data-cat');
    renderChips();
    if (selectedId) closePlace();
    applyFilters(true);
    if (!isDesktop()) setSheet('list');
  });

  function matches(p) {
    if (activeCat === 'saved' && !saved.has(p.id)) return false;
    if (activeCat !== 'all' && activeCat !== 'saved' && p.category !== activeCat) return false;
    if (!query) return true;
    var hay = (p.name + ' ' + catOf(p).label + ' ' + catOf(p).singular + ' ' + (p.description || '') + ' ' +
      (p.aliases || []).join(' ')).toLowerCase();
    return query.split(/\s+/).every(function (w) { return hay.indexOf(w) !== -1; });
  }

  var visible = [];
  function applyFilters(fit) {
    visible = PLACES.filter(matches);
    if (userLatLng) visible.sort(function (a, b) { return dist(a) - dist(b); });
    var ids = new Set(visible.map(function (p) { return p.id; }));
    PLACES.forEach(function (p) { showOnMap(p, ids.has(p.id) || p.id === selectedId); });
    renderList();
    if (fit && visible.length && (activeCat !== 'all' || query)) {
      var b = L.latLngBounds(visible.map(function (p) { return [p.lat, p.lng]; }));
      map.fitBounds(b.pad(0.2), fitOptions(true));
    }
  }

  function renderList() {
    var list = $('cm-list');
    var catLabel = activeCat === 'all' ? 'places' : activeCat === 'saved' ? 'saved places' : (CATS[activeCat] ? CATS[activeCat].label.toLowerCase() : 'places');
    $('cm-list-count').textContent = visible.length + ' ' + (visible.length === 1 && activeCat === 'all' ? 'place' : catLabel) +
      (userLatLng ? ' · nearest first' : '');
    list.innerHTML = visible.map(function (p) {
      var c = catOf(p);
      return '<li><button type="button" class="cm-place" data-id="' + esc(p.id) + '">' +
        '<span class="cm-place-icon" style="--c:' + c.color + '" aria-hidden="true"><i class="' + c.icon + '"></i></span>' +
        '<span class="cm-place-main"><span class="cm-place-name">' + esc(p.name) + '</span>' +
        '<span class="cm-place-sub">' + esc(c.singular) + (saved.has(p.id) ? ' · <i class="ri-bookmark-fill" aria-label="Saved"></i>' : '') + '</span></span>' +
        (userLatLng ? '<span class="cm-place-dist">' + fmtDist(dist(p)) + '</span>' : '') +
        '</button></li>';
    }).join('');
    var empty = $('cm-list-empty');
    empty.hidden = visible.length > 0;
    if (!visible.length) {
      $('cm-list-empty-title').textContent = query ? 'Nothing matches “' + searchInput.value.trim() + '”.' : 'No places here yet.';
      $('cm-list-empty-hint').textContent = activeCat !== 'all' ? 'You are only looking at one category.' : 'Try a building name, a faculty or a word like “library”.';
      $('cm-list-reset').hidden = !(query || activeCat !== 'all');
    }
  }
  $('cm-list').addEventListener('click', function (e) {
    var b = e.target.closest('.cm-place');
    if (b) openPlace(b.getAttribute('data-id'), { pan: true });
  });
  $('cm-list-reset').addEventListener('click', function () {
    activeCat = 'all'; query = ''; searchInput.value = ''; searchBox.classList.remove('has-value');
    renderChips(); applyFilters(false);
  });

  searchInput.addEventListener('focus', function () { if (!isDesktop() && !selectedId) setSheet('list'); });
  searchInput.addEventListener('input', function () {
    query = searchInput.value.trim().toLowerCase();
    searchBox.classList.toggle('has-value', !!query);
    if (selectedId) closePlace(true);
    applyFilters(false);
  });
  searchInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      if (visible[0]) { openPlace(visible[0].id, { pan: true }); searchInput.blur(); }
    } else if (e.key === 'Escape') {
      searchInput.value = ''; query = ''; searchBox.classList.remove('has-value'); applyFilters(false);
    }
  });
  $('cm-search-clear').addEventListener('click', function () {
    searchInput.value = ''; query = ''; searchBox.classList.remove('has-value'); applyFilters(false); searchInput.focus();
  });

  // ── Place detail ───────────────────────────────────────────────────────────────
  var selectedId = null;
  var NO_IMG_HIDE = function () { $('cm-detail-media').hidden = true; };
  $('cm-detail-img').addEventListener('error', NO_IMG_HIDE);

  function setUrlPlace(id) {
    var u = new URL(window.location.href);
    if (id) u.searchParams.set('place', id); else u.searchParams.delete('place');
    history.replaceState(null, '', u.pathname + (u.search ? u.search : ''));
  }

  function focusOn(p) {
    var z = Math.max(map.getZoom(), Z.focus);
    var ll = L.latLng(p.lat, p.lng);
    if (isDesktop()) { map.setView(ll, z, { animate: true }); return; }
    // Keep the pin above the bottom sheet, not hidden behind it.
    var pt = map.project(ll, z).add([0, panelHeight() / 2]);
    map.setView(map.unproject(pt, z), z, { animate: true });
  }

  function openPlace(id, opts) {
    var p = BY_ID[id];
    if (!p) return;
    if (selectedId && BY_ID[selectedId]) setActive(BY_ID[selectedId], false);
    selectedId = id;
    showOnMap(p, true);
    setActive(p, true);

    var c = catOf(p);
    $('cm-detail-kicker').innerHTML = '<span class="cm-chip-dot" style="--c:' + c.color + '" aria-hidden="true"></span>' + esc(c.singular);
    $('cm-detail-name').textContent = p.name;
    $('cm-detail-where').textContent = whereText(p);
    var desc = $('cm-detail-desc');
    desc.hidden = !p.description; desc.textContent = p.description || '';
    $('cm-detail-verify').hidden = !p.verify;
    var media = $('cm-detail-media');
    if (p.image) { $('cm-detail-img').src = p.image; $('cm-detail-img').alt = p.name; media.hidden = false; }
    else media.hidden = true;
    $('cm-gmaps').href ='https://www.google.com/maps/dir/?api=1&travelmode=walking&destination=' + p.lat + ',' + p.lng;
    syncSave();
    $('cm-route').hidden = !(route && route.id === id);
    if (route && route.id !== id) clearRoute();

    $('cm-list-view').hidden = true;
    $('cm-detail').hidden = false;
    setSheet('detail');
    $('cm-panel-body').scrollTop = 0;
    setUrlPlace(id);
    if (!opts || opts.pan !== false) focusOn(p);
    else if (!isDesktop()) setTimeout(function () { focusOn(p); }, 0);
  }

  function setActive(p, on) {
    markers[p.id].setIcon(pinIcon(p, on));
    markers[p.id].setZIndexOffset(on ? 1000 : 0);
    // The open place keeps its label at any zoom.
    var tip = markers[p.id].getTooltip();
    if (tip && tip.getElement()) tip.getElement().classList.toggle('is-sel', on);
    showOutline(on ? p : null);
  }
  function whereText(p) {
    var w = DATA.university.name + (p.campus ? ' · ' + p.campus : '');
    if (userLatLng) w += ' · ' + fmtDist(dist(p)) + ' from you';
    return w;
  }

  function closePlace(keepSheet) {
    if (selectedId && BY_ID[selectedId]) setActive(BY_ID[selectedId], false);
    selectedId = null;
    $('cm-detail').hidden = true;
    $('cm-list-view').hidden = false;
    setUrlPlace(null);
    if (!keepSheet) setSheet(isDesktop() ? 'list' : 'peek');
    else setSheet('list');
    applyFilters(false);
  }
  $('cm-detail-back').addEventListener('click', function () { closePlace(true); });
  $('cm-detail-close').addEventListener('click', function () { closePlace(false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && selectedId && document.activeElement !== searchInput) closePlace(true);
  });

  // Save
  function syncSave() {
    var on = saved.has(selectedId);
    var b = $('cm-save');
    b.setAttribute('aria-pressed', on);
    b.classList.toggle('is-on', on);
    b.innerHTML = '<i class="' + (on ? 'ri-bookmark-fill' : 'ri-bookmark-line') + '" aria-hidden="true"></i><span>' + (on ? 'Saved' : 'Save') + '</span>';
  }
  $('cm-save').addEventListener('click', function () {
    if (!selectedId) return;
    if (saved.has(selectedId)) { saved.delete(selectedId); toast('Removed from saved places'); }
    else { saved.add(selectedId); toast('Saved. Find it under “Saved”.'); }
    store(KEY.saved, Array.from(saved));
    syncSave(); renderChips();
  });

  // Share
  $('cm-share').addEventListener('click', function () {
    var p = BY_ID[selectedId]; if (!p) return;
    var url = window.location.origin + window.location.pathname + '?' +
      (DATA.campus && DATA.campuses.length > 1 ? 'campus=' + DATA.campus.id + '&' : '') + 'place=' + encodeURIComponent(p.id);
    var title = p.name + ' · ' + (DATA.university.short_name || DATA.university.name);
    if (navigator.share) { navigator.share({ title: title, url: url }).catch(function () {}); return; }
    (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject())
      .then(function () { toast('Link copied'); })
      .catch(function () { window.prompt('Copy this link', url); });
  });

  // ── Location ───────────────────────────────────────────────────────────────────
  var userLatLng = null, userMarker = null, userAccuracy = null, watchId = null, firstFix = true, onFix = null;
  function dist(p) { return userLatLng ? userLatLng.distanceTo([p.lat, p.lng]) : Infinity; }
  function campusCentre() { return campusBounds ? campusBounds.getCenter() : L.latLng(DATA.map.center); }

  function startLocating() {
    if (!navigator.geolocation) { toast('Location is not available on this device.'); return false; }
    if (watchId !== null) return true;
    $('cm-locate').classList.add('is-busy');
    watchId = navigator.geolocation.watchPosition(function (pos) {
      userLatLng = L.latLng(pos.coords.latitude, pos.coords.longitude);
      $('cm-locate').classList.remove('is-busy');
      $('cm-locate').classList.add('is-on');
      if (!userMarker) {
        userAccuracy = L.circle(userLatLng, { radius: pos.coords.accuracy, color: '#3a5fe0', weight: 1, fillOpacity: 0.12, interactive: false }).addTo(map);
        userMarker = L.marker(userLatLng, {
          icon: L.divIcon({ className: 'cm-me-wrap', html: '<span class="cm-me"></span>', iconSize: [22, 22], iconAnchor: [11, 11] }),
          keyboard: false, zIndexOffset: 2000,
        }).addTo(map).bindTooltip('You are here', { direction: 'top', offset: [0, -10] });
      } else {
        userMarker.setLatLng(userLatLng);
        userAccuracy.setLatLng(userLatLng).setRadius(pos.coords.accuracy);
      }
      var onCampus = userLatLng.distanceTo(campusCentre()) < NEAR_CAMPUS_M;
      if (firstFix) {
        firstFix = false;
        if (onCampus) map.setView(userLatLng, Math.max(map.getZoom(), 17), { animate: true });
        else toast('You seem to be away from campus. Distances are from where you are now.');
      }
      showNearest();
      applyFilters(false);
      if (selectedId) $('cm-detail-where').textContent = whereText(BY_ID[selectedId]);
      if (route) updateRouteStart();
      if (onFix) { var f = onFix; onFix = null; f(onCampus); }
    }, function (err) {
      $('cm-locate').classList.remove('is-busy');
      navigator.geolocation.clearWatch(watchId); watchId = null;
      toast(err.code === 1 ? 'Location is turned off for Nelavista. Allow it in your browser to see where you are.' : 'Could not find your location. Try again outside.');
      if (onFix) { var f = onFix; onFix = null; f(null); }
    }, { enableHighAccuracy: true, maximumAge: 3000, timeout: 15000 });
    return true;
  }
  $('cm-locate').addEventListener('click', function () {
    if (userLatLng) { map.setView(userLatLng, Math.max(map.getZoom(), 17), { animate: true }); return; }
    startLocating();
  });
  window.addEventListener('pagehide', function () { if (watchId !== null) navigator.geolocation.clearWatch(watchId); });

  function showNearest() {
    var best = null, bd = Infinity;
    PLACES.forEach(function (p) { var d = dist(p); if (d < bd) { bd = d; best = p; } });
    var el = $('cm-near');
    if (!best || bd > NEAR_CAMPUS_M) { el.hidden = true; return; }
    el.hidden = false;
    el.innerHTML = '<button type="button" class="cm-near-btn" data-id="' + esc(best.id) + '"><i class="ri-navigation-line" aria-hidden="true"></i>Nearest: ' + esc(best.name) + ' · ' + fmtDist(bd) + '</button>';
  }
  $('cm-near').addEventListener('click', function (e) {
    var b = e.target.closest('.cm-near-btn'); if (b) openPlace(b.getAttribute('data-id'), { pan: true });
  });

  // ── Directions ─────────────────────────────────────────────────────────────────
  var route = null;   // { id, control, line }
  var lrmLoading = null;
  function loadRouting() {
    if (window.L && L.Routing) return Promise.resolve();
    if (lrmLoading) return lrmLoading;
    lrmLoading = new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = LRM_SRC; s.onload = resolve; s.onerror = reject;
      document.head.appendChild(s);
    });
    return lrmLoading;
  }
  function clearRoute() {
    if (!route) return;
    if (route.control) map.removeControl(route.control);
    if (route.line) map.removeLayer(route.line);
    route = null;
    $('cm-route').hidden = true;
  }
  $('cm-route-end').addEventListener('click', clearRoute);

  function routeText(meters) {
    $('cm-route-text').textContent = fmtDist(meters) + ' · about ' + walkMin(meters) + ' min walk';
    $('cm-route').hidden = false;
  }
  function drawFallback(p) {
    // OSRM unavailable: a straight dashed line with the as-the-crow-flies distance.
    route.line = L.polyline([userLatLng, [p.lat, p.lng]], { color: '#3a5fe0', weight: 4, dashArray: '8 8', opacity: 0.9 }).addTo(map);
    routeText(dist(p));
    map.fitBounds(route.line.getBounds().pad(0.25), fitOptions(true));
  }
  function updateRouteStart() {
    if (!route || !userLatLng) return;
    var p = BY_ID[route.id];
    if (route.control) route.control.setWaypoints([userLatLng, L.latLng(p.lat, p.lng)]);
    else if (route.line) route.line.setLatLngs([userLatLng, [p.lat, p.lng]]);
  }

  function routeTo(p) {
    clearRoute();
    route = { id: p.id };
    $('cm-route-text').textContent = 'Finding a route…';
    $('cm-route').hidden = false;
    loadRouting().then(function () {
      if (!route || route.id !== p.id) return;
      var zoomed = false;
      route.control = L.Routing.control({
        waypoints: [userLatLng, L.latLng(p.lat, p.lng)],
        router: L.Routing.osrmv1({ serviceUrl: 'https://router.project-osrm.org/route/v1', profile: 'driving' }),
        show: false, addWaypoints: false, draggableWaypoints: false, routeWhileDragging: false,
        fitSelectedRoutes: false, createMarker: function () { return null; },
        lineOptions: { styles: [{ color: '#ffffff', weight: 8, opacity: 0.9 }, { color: '#3a5fe0', weight: 5, opacity: 1 }], addWaypoints: false },
      }).addTo(map);
      route.control.on('routesfound', function (e) {
        var r = e.routes[0];
        routeText(r.summary.totalDistance);
        if (!zoomed) { zoomed = true; map.fitBounds(L.latLngBounds(r.coordinates).pad(0.15), fitOptions(true)); }
      });
      route.control.on('routingerror', function () {
        if (!route || route.id !== p.id) return;
        map.removeControl(route.control); route.control = null;
        drawFallback(p);
      });
    }).catch(function () { if (route && route.id === p.id) drawFallback(p); });
  }

  $('cm-directions').addEventListener('click', function () {
    var p = BY_ID[selectedId]; if (!p) return;
    function go(onCampus) {
      if (!userLatLng) { window.open($('cm-gmaps').href, '_blank', 'noopener'); return; }
      if (!onCampus && userLatLng.distanceTo([p.lat, p.lng]) > NEAR_CAMPUS_M) {
        toast('You are far from campus, so we opened Google Maps for the full journey.');
        window.open($('cm-gmaps').href, '_blank', 'noopener');
        return;
      }
      routeTo(p);
    }
    if (userLatLng) { go(userLatLng.distanceTo(campusCentre()) < NEAR_CAMPUS_M); return; }
    toast('Finding your location…');
    onFix = go;
    if (!startLocating()) { onFix = null; window.open($('cm-gmaps').href, '_blank', 'noopener'); }
  });

  // ── Start ──────────────────────────────────────────────────────────────────────
  renderChips();
  applyFilters(false);
  var startId = new URL(window.location.href).searchParams.get('place');
  if (startId && BY_ID[startId]) {
    map.setView([BY_ID[startId].lat, BY_ID[startId].lng], Z.focus, { animate: false });
    openPlace(startId, { pan: true });
  } else {
    // Always open on the whole campus, never on wherever the last visit ended.
    if (startId) setUrlPlace(null);
    setSheet(isDesktop() ? 'list' : 'peek');
    fitCampus(false);
  }
  // Major labels always show at the opening whole-campus view, even on a narrow phone.
  if (!startId || !BY_ID[startId]) Z.tier1 = Math.min(Z.tier1, map.getZoom());
  syncLabels();
  window.matchMedia('(min-width: 900px)').addEventListener('change', function (e) {
    if (e.matches && panel.getAttribute('data-state') === 'peek') setSheet('list');
    setTimeout(function () { map.invalidateSize(); }, 50);
  });
})();
