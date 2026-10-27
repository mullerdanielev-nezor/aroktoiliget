/* Süti-hozzájárulás és mérés – minden oldalon fut.
   API: window.ALConsent.get(), .open(showPrefs), .onChange(fn); window.alTrack(name, params) */
(function(){
  "use strict";
  var CONFIG = window.AL_CONFIG || {};
  var KEY = "al_consent_v1", VERSION = 2, MAX_AGE_DAYS = 365;

  function getJSON(key){ try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : null; } catch(e){ return null; } }
  function setJSON(key, val){ try { localStorage.setItem(key, JSON.stringify(val)); } catch(e){} }

  /* 12 hónap után, vagy a tájékoztató lényeges változásakor újra megkérdezzük. */
  var consent = getJSON(KEY);
  if (consent && (consent.v !== VERSION || !consent.ts || (Date.now() - Date.parse(consent.ts)) > MAX_AGE_DAYS * 864e5)) consent = null;

  var listeners = [];
  function emit(){ listeners.forEach(function(fn){ try { fn(consent, !banner.hidden); } catch(e){} }); }

  /* ===== Sáv ===== */
  var banner = document.createElement("div");
  banner.className = "consent"; banner.id = "consent"; banner.hidden = true;
  banner.setAttribute("role", "region"); banner.setAttribute("aria-label", "Süti-beállítások");
  banner.innerHTML =
    '<div class="wrap">' +
      '<div class="consent-text"><p><strong>Sütik és mérés.</strong> A működéshez szükséges tároláson túl csak az Ön hozzájárulásával használunk statisztikai és hirdetésmérő eszközöket. Részletek: <a href="cookie-tajekoztato.html">süti-tájékoztató</a>. Döntését bármikor módosíthatja az oldal alján.</p></div>' +
      '<div class="consent-actions">' +
        '<button type="button" class="btn btn-primary" data-c="reject">Csak a szükségesek</button>' +
        '<button type="button" class="btn btn-primary" data-c="accept">Mindet elfogadom</button>' +
        '<button type="button" class="btn btn-ghost" data-c="custom" aria-expanded="false" aria-controls="consent-prefs">Beállítások</button>' +
      '</div>' +
      '<div class="consent-prefs" id="consent-prefs" hidden>' +
        '<div class="check"><input type="checkbox" id="c-necessary" checked disabled><label for="c-necessary"><strong>Szükséges</strong>: a süti-döntés megjegyzése. Mindig aktív.</label></div>' +
        '<div class="check"><input type="checkbox" id="c-analytics"><label for="c-analytics"><strong>Statisztika</strong>: látogatottsági adatok (Google Analytics)</label></div>' +
        '<div class="check"><input type="checkbox" id="c-marketing"><label for="c-marketing"><strong>Hirdetésmérés</strong>: a Facebook- és Instagram-hirdetések eredményeinek mérése (Meta Pixel)</label></div>' +
        '<div><button type="button" class="btn btn-primary" data-c="save">Kiválasztottak mentése</button></div>' +
      '</div>' +
    '</div>';
  document.body.appendChild(banner);
  var prefs = banner.querySelector("#consent-prefs"), customBtn = banner.querySelector('[data-c="custom"]');
  var cA = banner.querySelector("#c-analytics"), cM = banner.querySelector("#c-marketing");

  /* ===== Mérőkódok ===== */
  function loadScript(src){ var s = document.createElement("script"); s.async = true; s.src = src; document.head.appendChild(s); }
  var gaLoaded = false, pixelLoaded = false;
  function loadGA(){
    if (gaLoaded || !CONFIG.ga4MeasurementId) return; gaLoaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function(){ window.dataLayer.push(arguments); };
    window.gtag("consent", "default", { analytics_storage: "granted", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
    window.gtag("js", new Date()); window.gtag("config", CONFIG.ga4MeasurementId);
    loadScript("https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(CONFIG.ga4MeasurementId));
  }
  function loadPixel(){
    if (pixelLoaded || !CONFIG.metaPixelId) return; pixelLoaded = true;
    var n = window.fbq = function(){ n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments); };
    if (!window._fbq) window._fbq = n;
    n.push = n; n.loaded = true; n.version = "2.0"; n.queue = [];
    loadScript("https://connect.facebook.net/hu_HU/fbevents.js");
    window.fbq("init", CONFIG.metaPixelId); window.fbq("track", "PageView");
  }
  /* Visszavonáskor a már létrejött mérősütiket is töröljük. */
  function clearCookies(re){
    var host = location.hostname, parts = host.split("."), domains = [""];
    for (var i = 0; i < parts.length - 1; i++) domains.push(";domain=." + parts.slice(i).join("."));
    document.cookie.split(";").forEach(function(c){
      var name = c.split("=")[0].trim(); if (!re.test(name)) return;
      domains.forEach(function(d){ document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/" + d; });
    });
  }
  function applyConsent(prev){
    if (!consent) return;
    if (consent.analytics) loadGA(); else clearCookies(/^(_ga|_gid|_gat)/);
    if (consent.marketing) loadPixel(); else clearCookies(/^(_fbp|_fbc)$/);
    /* Ha egy már betöltött mérőkódot vontak vissza, újratöltéssel állítjuk le. */
    if (prev && ((prev.analytics && !consent.analytics && gaLoaded) || (prev.marketing && !consent.marketing && pixelLoaded))) location.reload();
  }
  function save(a, m){
    var prev = consent;
    consent = { analytics: !!a, marketing: !!m, ts: new Date().toISOString(), v: VERSION };
    setJSON(KEY, consent); banner.hidden = true; applyConsent(prev); emit();
  }
  function open(showPrefs){
    cA.checked = !!(consent && consent.analytics); cM.checked = !!(consent && consent.marketing);
    prefs.hidden = !showPrefs; customBtn.setAttribute("aria-expanded", String(!!showPrefs));
    banner.hidden = false; emit();
    var first = banner.querySelector(showPrefs ? "#c-analytics" : "button"); if (first) first.focus({ preventScroll: true });
  }

  banner.addEventListener("click", function(e){
    var b = e.target.closest("[data-c]"); if (!b) return;
    var c = b.getAttribute("data-c");
    if (c === "reject") save(false, false);
    else if (c === "accept") save(true, true);
    else if (c === "save") save(cA.checked, cM.checked);
    else if (c === "custom") { var o = prefs.hidden; prefs.hidden = !o; customBtn.setAttribute("aria-expanded", String(o)); }
  });
  document.addEventListener("click", function(e){ if (e.target.closest("[data-consent-open]")) { e.preventDefault(); open(true); } });

  /* Csak személyes adat nélküli paraméterek. */
  var PIXEL_EVENTS = { waitlist_submit: "Lead" };
  window.alTrack = function(name, params){
    params = params || {};
    if (consent && consent.analytics && window.gtag) window.gtag("event", name, params);
    if (consent && consent.marketing && window.fbq && PIXEL_EVENTS[name]) window.fbq("track", PIXEL_EVENTS[name], params);
  };
  window.ALConsent = {
    get: function(){ return consent; },
    open: open,
    onChange: function(fn){ listeners.push(fn); },
    bannerOpen: function(){ return !banner.hidden; }
  };

  if (consent) applyConsent(null); else banner.hidden = false;
})();
