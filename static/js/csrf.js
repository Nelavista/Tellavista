// Attaches the CSRF token to same-origin fetch() requests automatically, so pages
// using fetch() for POST/PUT/PATCH/DELETE don't each need to remember to send it.
// Reads the token from <meta name="csrf-token">, set by every template that includes this file.
(function () {
  var tokenMeta = document.querySelector('meta[name="csrf-token"]');
  if (!tokenMeta) return;
  var token = tokenMeta.getAttribute('content');
  var originalFetch = window.fetch;
  var UNSAFE_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE'];

  window.fetch = function (input, init) {
    init = init || {};
    var method = (init.method || (input && input.method) || 'GET').toUpperCase();
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    var isSameOrigin = url.indexOf('http://') !== 0 && url.indexOf('https://') !== 0;

    if (isSameOrigin && UNSAFE_METHODS.indexOf(method) !== -1) {
      init.headers = new Headers(init.headers || {});
      if (!init.headers.has('X-CSRFToken')) {
        init.headers.set('X-CSRFToken', token);
      }
    }
    return originalFetch.call(this, input, init);
  };
})();
