/* HVSS Android Google Apps Script bridge.
 * The web app already uses JSONP for CENTRAL reads. Android WebView cannot
 * reliably read the cross-origin Apps Script POST response, so for APK builds
 * we send the same POST in no-cors mode and return a synthetic successful
 * response to the existing HVSS code. This preserves the original web code.
 */
(function () {
  if (!window.Capacitor || !window.fetch) return;
  var originalFetch = window.fetch.bind(window);
  var GAS_PREFIX = 'https://script.google.com/macros/s/';

  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : (input && input.url) || '';
    var method = ((init && init.method) || (input && input.method) || 'GET').toUpperCase();
    if (method !== 'POST' || url.indexOf(GAS_PREFIX) !== 0) {
      return originalFetch(input, init);
    }

    var opts = Object.assign({}, init || {}, { method: 'POST', mode: 'no-cors' });
    return originalFetch(url, opts).then(function () {
      var bodyText = JSON.stringify({ ok: true, androidWebView: true });
      return {
        ok: true,
        status: 200,
        text: function () { return Promise.resolve(bodyText); },
        json: function () { return Promise.resolve({ ok: true, androidWebView: true }); }
      };
    });
  };
})();
