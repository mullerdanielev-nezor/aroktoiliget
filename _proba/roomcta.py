import os, re
os.chdir(r"D:\Letolt\liget")

def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:80], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

s = open("index.html", encoding="utf-8").read()
# 1) Szobakártyák: saját CTA, ami előre kijelöli a szobát
for slug in ["egyagyas", "ketagyas", "negyagyas"]:
    a = s.index(f'src="assets/img/rezidencia/{slug}.jpg" width="1200" height="675" alt="Illusztráció', s.index('<div class="rooms">'))
    b = s.index('<p class="room-price-label">egyszeri belépési hozzájárulás</p>', a) + len('<p class="room-price-label">egyszeri belépési hozzájárulás</p>')
    s = s[:b] + f'\n            <a class="btn btn-gold room-cta" href="#jelentkezes" data-open="varolista" data-room="{slug}">Ezt választom</a>' + s[b:]

# 2) A beküldés utáni köszönő blokk helyett külön köszönőoldal
a = s.index('        <div class="success thanks" data-role="success" hidden>')
b = s.index('        </div>\n', s.index('<p class="small muted">Addig a projekt előrehaladásáról is tájékoztatjuk.', a)) + len('        </div>\n')
s = s[:a] + s[b:]
open("index.html", "w", encoding="utf-8", newline="\n").write(s)

edit("index.html", [
# kattintás forrása + szoba előválasztás
('''    var el = e.target.closest("[data-open]"); if (!el) return;
    setMenu(false);''',
'''    var el = e.target.closest("[data-open]"); if (!el) return;
    setMenu(false);
    setOrigin(el);'''),
('''  document.addEventListener("click", function(e){
    var el = e.target.closest("[data-open]");''',
'''  /* Honnan indult a jelentkezés: a beküldött e-mailben is látszik. Szobagombnál a szobát is előre kijelöljük. */
  var ORIGIN_NAMES = { top: "Nyitórész", rezidencia: "A rezidenciáról", ellatas: "Ellátás", arokto: "Ároktő", dijak: "Szobák és díjak", gyik: "Gyakori kérdések", closing: "Záró rész" };
  function setOrigin(el){
    var form = document.getElementById("form-varolista"); if (!form) return;
    var where = el.closest("dialog") ? "Díjak panel" : el.closest(".sticky-cta") ? "Alsó sáv" : el.closest(".site-header") ? "Fejléc" : "";
    if (!where) { var sec = el.closest("section"); where = sec ? (ORIGIN_NAMES[sec.id] || ORIGIN_NAMES[sec.classList[0]] || "") : ""; }
    var room = el.dataset.room && form.querySelector('input[name="room"][value="' + el.dataset.room + '"]');
    if (room) {
      room.checked = true;
      var fs = room.closest("fieldset[data-required]"); if (fs && fs.classList.contains("is-invalid")) checkGroup(fs, form);
      where = (where === "Díjak panel" ? "Díjak panel" : "Szobakártya") + " – " + room.dataset.label;
      track("room_cta_click", { room_type: el.dataset.room });
    }
    form.dataset.origin = where || "–";
  }
  document.addEventListener("click", function(e){
    var el = e.target.closest("[data-open]");'''),
# drawer: szobánként gomb
('''      li.innerHTML = '<img class="dr-img" alt="" width="1200" height="675"><div><span class="dr-name"></span><span class="dr-meta"></span><span class="dr-amount"></span><span class="dr-unit">belépési hozzájárulás / fő</span></div>';''',
'''      li.innerHTML = '<img class="dr-img" alt="" width="1200" height="675"><div><span class="dr-name"></span><span class="dr-meta"></span><span class="dr-amount"></span><span class="dr-unit">belépési hozzájárulás / fő</span><a class="btn btn-ghost dr-cta" href="#jelentkezes" data-open="varolista" data-close>Ezt választom</a></div>';
      li.querySelector(".dr-cta").dataset.room = card.querySelector(".room-cta").dataset.room;'''),
# payload + e-mail
('''    p.pricingReviewed = fd.get("pricing_reviewed") === "on";
    return p;''',
'''    p.pricingReviewed = fd.get("pricing_reviewed") === "on";
    p.origin = form.dataset.origin || "–";
    return p;'''),
('''    r["Kampányforrás"] = src || "–";''',
'''    r["Honnan jelentkezett"] = p.origin;
    r["Kampányforrás"] = src || "–";'''),
# siker: átirányítás a köszönőoldalra
('''        if (n) personalize();
        panel.hidden = true;
        var ok = card.querySelector('[data-role="success"]'); ok.hidden = false;
        ok.scrollIntoView({ block: "center", behavior: "smooth" }); ok.querySelector("h3").focus({ preventScroll: true });
        var ev = { form_type: formType, room_type: payload.roomType, timing: payload.timing, relation: payload.relation, campaign_source: attribution.utm_source || "(nincs)" };
        track(type === "varolista" ? "waitlist_submit" : "survey_submit", ev);
        updateSticky();''',
'''        var ev = { form_type: formType, room_type: payload.roomType, timing: payload.timing, relation: payload.relation, entry_point: payload.origin, campaign_source: attribution.utm_source || "(nincs)" };
        /* A köszönőoldal ebből szólítja meg a jelentkezőt és ott méri a konverziót; kiolvasás után törli. */
        var stored = false;
        try { sessionStorage.setItem("al_thanks", JSON.stringify({ g: givenName(), rel: payload.relation === "sajat" ? "self" : "rel", ev: ev })); stored = true; } catch(e){}
        if (!stored) track("waitlist_submit", ev);
        location.href = "koszonjuk.html";'''),
])

c = "assets/css/style.css"
t = open(c, encoding="utf-8").read()
t = re.sub(r"\n\.thanks[^\n]*", "", t)
t += """
/* Szobakártya és díjpanel: „Ezt választom” */
.room-body{flex:1}
.room-price-label{margin-bottom:22px}
.room-cta{margin-top:auto;width:100%;min-height:52px}
.dr-cta{display:inline-flex;margin-top:12px;min-height:40px;padding-inline:16px;font-size:.9375rem}
"""
open(c, "w", encoding="utf-8", newline="\n").write(t)
open("_proba/batch.txt", "w").write("ok")
