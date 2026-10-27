import os, re
from PIL import Image
os.chdir(r"D:\Letolt\liget")
R = "assets/img/rezidencia/"

def conv(src, dst, w, q=74):
    im = Image.open("images/" + src).convert("RGB")
    im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(R + dst, "JPEG", quality=q, optimize=True, progressive=True)
    return im.size
SZ = {
    "viragoskert": conv("Gondoskodás a virágos kertben.png", "viragoskert.jpg", 1400),
    "sutes": conv("Közös sütés a gondozóotthonban.png", "sutes.jpg", 1400),
    "sakk": conv("Idős férfiak sakkpartija egy otthonos társalgóban.png", "sakk.jpg", 1400),
    "album": conv("Meghitt emlékek a fotóalbumban.png", "album.jpg", 1000),
}
for n in ["epulet", "egyagyas"]:
    SZ[n] = Image.open(R + n + ".jpg").size

def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

PREV = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M12.5 4.5L7 10l5.5 5.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
NEXT = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
def nav(what):
    return f'''        <div class="svc-nav">
          <div class="svc-progress" aria-hidden="true"><span></span></div>
          <button class="car-btn" type="button" data-svc-prev aria-label="Előző {what}">{PREV}</button>
          <button class="car-btn" type="button" data-svc-next aria-label="Következő {what}">{NEXT}</button>
        </div>
'''

s = open("index.html", encoding="utf-8").read()

# 1) Bemutató: a képes rács helyett lapozható látványterv
PLAN = [
    ("epulet", "50% 55%", "Illusztráció: a felújított, kétszintes épület parkosított udvarral; idősek padon és asztaloknál, gondozók kísérik őket",
     "A megújuló épület", "Felújítás és bővítés, parkosított udvarral."),
    ("viragoskert", "40% 50%", "Illusztráció: egy gondozó és egy idős hölgy virágokat locsol a rezidencia kertjében, háttérben fedett terasz",
     "Kert és terasz", "Virágágyások, árnyas terasz, padok."),
    ("sakk", "45% 50%", "Illusztráció: két idős úr sakkozik a napfényes társalgóban, háttérben könyvespolc",
     "Társalgó", "Olvasás, beszélgetés, egy parti sakk."),
    ("sutes", "50% 50%", "Illusztráció: idős hölgyek egy gondozóval közösen pogácsát szaggatnak a közösségi konyhában",
     "Közösségi konyha", "Közös sütés, ahogy otthon."),
    ("egyagyas", "50% 50%", "Illusztráció: napfényes egyágyas szoba, egy gondozó beszélget egy idős hölggyel",
     "Napfényes szobák", "Egy-, két- és négyágyas kialakítás."),
]
n = len(PLAN)
slides = "\n".join(f'''          <li class="plan-slide" aria-roledescription="dia" aria-label="{i+1} / {n}">
            <img src="{R}{slug}.jpg" width="{SZ[slug][0]}" height="{SZ[slug][1]}" style="object-position:{pos}" alt="{alt}" loading="lazy" decoding="async">
            <div class="plan-cap"><span class="plan-no">{i+1:02d}</span><div><h3 class="plan-name">{name}</h3><p class="plan-sub">{sub}</p></div></div>
          </li>''' for i, (slug, pos, alt, name, sub) in enumerate(PLAN))
a = s.index('      <div class="bento">')
b = s.index('      <figure class="render" data-render-block="intro" hidden>', a)
s = s[:a] + f'''      <div class="svc-car plan-car" data-svc-car role="region" aria-roledescription="képlapozó" aria-label="A rezidencia látványterve">
        <ul class="svc-track plan-track" tabindex="0">
{slides}
        </ul>
{nav("kép")}      </div>
      <p class="plan-note">Illusztrációk. A végleges kialakítás a tervezés során változhat.</p>
''' + s[b:]

# 2) Gondoskodás: fotóalbumos kártya + mentálhigiéné külön
album = f'''          <li class="svc-card" aria-roledescription="kártya" aria-label="4 / 5">
            <img src="{R}album.jpg" width="{SZ["album"][0]}" height="{SZ["album"][1]}" style="object-position:45% 50%" alt="Illusztráció: egy idős úr és a lánya mosolyogva lapozzák a régi fotóalbumot a társalgóban" loading="lazy" decoding="async">
            <div class="svc-body">
              <span class="svc-icon"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7.5-4.6-7.5-10.2A4.2 4.2 0 0 1 12 7.3a4.2 4.2 0 0 1 7.5 2.5C19.5 15.4 12 20 12 20z"/></svg></span>
              <h3 class="svc-name">Lélekben is jól</h3>
              <p class="svc-sub">Mentálhigiénés foglalkozások és személyes figyelem.</p>
            </div>
          </li>
'''
s = s.replace('<p class="svc-sub">Közösségi programok és mentálhigiénés foglalkozások.</p>', '<p class="svc-sub">Közösségi programok, játék, beszélgetés.</p>')
for i in range(1, 5): s = s.replace(f'aria-roledescription="kártya" aria-label="{i} / 4"', f'aria-roledescription="kártya" aria-label="{i if i < 4 else 5} / 5"')
anchor = '          <li class="svc-card" aria-roledescription="kártya" aria-label="5 / 5">'
assert s.count(anchor) == 1
s = s.replace(anchor, album + anchor)

# 3) Ároktő: montázs + saját térkép
svg = open("_proba/map.svg", encoding="utf-8").read()
def lic(name, url): return f'<a href="{url}" target="_blank" rel="noopener">{name}</a>'
a = s.index('      <div class="place-head">')
b = s.index('  </section>', a)
s = s[:a] + f'''      <div class="place-head">
        <p class="eyebrow">A helyszín</p>
        <h2 id="place-title">Ároktő: csend a Tisza partján.</h2>
        <p class="place-lead">Nyugodt falu a Tisza mellett, Miskolctól 45 km-re.</p>
      </div>

      <div class="place-grid">
        <div class="montage">
          <figure class="mt mt-a"><img src="assets/img/arokto/komp.jpg" width="1400" height="933" alt="Kisebb komp autóval a Tisza vizén, háttérben ártéri erdő, naplementében" loading="lazy" decoding="async"><figcaption>Komp a Tiszán</figcaption></figure>
          <figure class="mt mt-b"><img src="assets/img/arokto/templom.jpg" width="1050" height="1400" alt="Az ároktői református templom tornya kék ég előtt" loading="lazy" decoding="async"><figcaption>Ároktői templom</figcaption></figure>
          <figure class="mt mt-c"><img src="assets/img/arokto/tisza-gat.jpg" width="1050" height="1400" alt="Kerékpárút a füves Tisza-gát tetején, egyik oldalon erdő, másikon szántóföld" loading="lazy" decoding="async"><figcaption>Tisza-gát</figcaption></figure>
          <figure class="mt mt-d"><img src="assets/img/arokto/tiszadorogma.jpg" width="1400" height="820" alt="Falusi látkép a gátról: rét, fák és egy fehér tornyú templom" loading="lazy" decoding="async"><figcaption>Tiszadorogma</figcaption></figure>
        </div>

        <div class="map-card">
          {svg}
          <div class="map-foot">
            <p class="small muted">A pontos címet a projekt előrehaladásával tesszük közzé.</p>
            <div class="map-links">
              <a class="btn btn-ghost" href="https://www.openstreetmap.org/?mlat=47.7308&amp;mlon=20.9423#map=13/47.7308/20.9423" target="_blank" rel="noopener">Nagyobb térkép</a>
              <a class="btn btn-ghost" href="https://www.google.com/maps/dir/?api=1&amp;destination=47.7308,20.9423" target="_blank" rel="noopener">Útvonaltervezés</a>
            </div>
          </div>
        </div>
      </div>
      <p class="place-credits">Komp a Tiszán Ároktő és Tiszacsege között: Michal Gorski, {lic("CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0/deed.hu")} · Református templom: Tothh417, {lic("CC0", "https://creativecommons.org/publicdomain/zero/1.0/deed.hu")} · Tisza-gát Tiszacsegénél: Beroesz, {lic("CC BY-SA 2.5 HU", "https://creativecommons.org/licenses/by-sa/2.5/hu/deed.hu")} · Tiszadorogma: Tothh417, {lic("CC0", "https://creativecommons.org/publicdomain/zero/1.0/deed.hu")} · Forrás: Wikimedia Commons · Térképadatok: © {lic("OpenStreetMap-közreműködők", "https://www.openstreetmap.org/copyright")}</p>
    </div>
''' + s[b:]

# 4) Adatkezelési összefoglaló ki – a lábléc linkjei maradnak
a = s.index('  <!-- PRIVACY -->')
b = s.index('  <!-- ZÁRÁS -->', a)
s = s[:a] + s[b:]
s = s.replace('''  var privacy = document.getElementById("adatkezeles");
  document.addEventListener("click", function(e){
    var p = e.target.closest("[data-privacy]"); if (p) { privacy.open = true; return; }
    var el''', '''  document.addEventListener("click", function(e){
    var el''')
open("index.html", "w", encoding="utf-8", newline="\n").write(s)

# Jogi oldalak: a térkép már nem külső beágyazás
edit("adatkezeles.html", [
    ("A helyszíni térképet az OpenStreetMap szolgáltatja; a térkép betöltésekor a böngészője – mint minden webes kérésnél – közli az IP-címét az OpenStreetMap szerverével. Sütit általunk ismert módon nem helyez el.",
     "A helyszíni térkép az OpenStreetMap nyílt adataiból készült, és szintén saját tárhelyünkről töltődik be, ezért megjelenítésekor nem jön létre kapcsolat külső szolgáltatóval."),
])
t = open("adatkezeles.html", encoding="utf-8").read()
t = re.sub(r'\s*<tr><td data-label="Szolgáltató">OpenStreetMap Foundation.*?</tr>', "", t, count=1)
t = t.replace(" Az OpenStreetMap Foundation az Egyesült Királyságban működik, amelyre az Európai Bizottság megfelelőségi határozata vonatkozik.", "")
open("adatkezeles.html", "w", encoding="utf-8", newline="\n").write(t)
edit("cookie-tajekoztato.html", [
    ("A helyszíni térkép az OpenStreetMap szervereiről érkezik; ez általunk ismert módon nem helyez el követő sütit, de a betöltéshez a böngészője közli vele az IP-címét. Részletek az <a href=\"adatkezeles.html#cimzettek\">adatkezelési tájékoztatóban</a>.",
     "A helyszíni térkép is saját tárhelyről töltődik be, külső szolgáltatóhoz nem kapcsolódik."),
])
t = open("impresszum.html", encoding="utf-8").read()
t, k = re.subn(r'\s*<tr><td data-label="Kép"><a href="https://commons.wikimedia.org/wiki/File:(Biking_bridge|Nine-arched)[^\n]*</tr>', "", t); assert k == 2, k
open("impresszum.html", "w", encoding="utf-8", newline="\n").write(t)

# CSS
c = "assets/css/style.css"
t = open(c, encoding="utf-8").read()
t = re.sub(r"\n/\* Bemutató: képes rács \*/\n.*?\n\}\n", "\n", t, count=1, flags=re.S)
assert ".bento" not in t, "bento left"
a = t.index(".place-head{"); b = t.index(".map-links{")
keep = "".join(l + "\n" for l in t[a:b].split("\n") if l.startswith(".car-btn"))
assert keep.count("\n") == 3, keep
t = t[:a] + keep + t[b:]
t = t.replace(".map-links .btn{flex:1 1 10em;min-height:48px}\n", ".map-links .btn{flex:1 1 10em;min-height:48px}\n", 1)
t = t.replace(".closing h2{font-size:clamp(2.75rem,.6rem + 8.4vw,8rem);line-height:.95;letter-spacing:-.03em;color:var(--green)}\n.closing h2 span{display:block}",
              ".closing h2{font-size:min(7.4vw,6.75rem);line-height:1;letter-spacing:-.03em;color:var(--green)}\n.closing h2 span{display:block;white-space:nowrap}")
t += """
/* Bemutató: lapozható látványterv */
.plan-car{margin-top:clamp(36px,5vw,64px)}
.plan-track{grid-auto-columns:88%}
@media (min-width:860px){.plan-track{grid-auto-columns:calc((100% - 20px) / 1.45)}}
.plan-slide{display:flex;flex-direction:column;min-width:0;border-radius:12px;overflow:hidden;background:var(--white);scroll-snap-align:start;box-shadow:0 1px 2px rgba(16,48,42,.05),0 18px 40px -26px rgba(16,48,42,.35)}
.plan-slide img{display:block;width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;background:var(--ph)}
.plan-cap{display:flex;align-items:baseline;gap:clamp(14px,2vw,24px);padding:clamp(18px,2.2vw,28px) clamp(20px,2.4vw,32px)}
.plan-no{font:400 clamp(1.5rem,1.2rem + 1vw,2.25rem)/1 var(--serif);color:var(--gold-ink)}
.plan-name{font-size:clamp(1.5rem,1.2rem + 1vw,2.125rem);line-height:1.1}
.plan-sub{margin-top:4px;font-size:clamp(1rem,.95rem + .25vw,1.125rem);color:var(--ink-2)}
.plan-car .svc-progress{background:var(--line)}
.plan-car .svc-progress span{background:var(--green)}
.plan-car .car-btn:disabled{opacity:.4}
.plan-note{margin-top:14px;text-align:center;font-size:.875rem;color:var(--ink-2)}

/* Helyszín: fotómontázs + saját térkép */
.place-head{display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center;margin-bottom:clamp(32px,4.5vw,56px)}
.place-lead{font-size:clamp(1.125rem,1rem + .5vw,1.375rem);color:var(--ink-2);text-wrap:balance}
.place-grid{display:grid;gap:clamp(12px,1.6vw,20px)}
.place-grid > *{min-width:0}
.montage{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:1.25fr 1fr 1fr;gap:clamp(10px,1.4vw,16px);aspect-ratio:4/5}
.mt{position:relative;margin:0;min-height:0;border-radius:12px;overflow:hidden;background:var(--ph)}
.mt img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
@media (hover:hover){.mt:hover img{transform:scale(1.04)}}
.mt figcaption{position:absolute;left:12px;bottom:12px;padding:6px 12px;border-radius:999px;background:var(--white);color:var(--ink);font:700 .875rem/1.2 var(--sans);box-shadow:0 2px 10px rgba(16,48,42,.15)}
.mt-a{grid-column:1 / -1}
.mt-b{grid-row:2 / 4}
.mt-b img{object-position:50% 25%}
.mt-c img{object-position:50% 62%}
.map-card{display:flex;flex-direction:column;background:var(--white);border-radius:12px;overflow:hidden}
.map-svg{display:block;width:100%;height:auto}
.map-foot{display:flex;flex-direction:column;gap:14px;padding:clamp(16px,2vw,24px)}
.place-credits{margin-top:16px;font-size:.75rem;line-height:1.6;color:var(--ink-2);text-align:center}
.place-credits a{color:inherit}
@media (min-width:900px){
  .place-grid{grid-template-columns:minmax(0,7fr) minmax(0,5fr)}
  .montage{aspect-ratio:auto}
}
@media (prefers-reduced-motion:reduce){.mt img{transition:none}}
.m-bg{fill:#F7F3EA}
.m-road{fill:none;stroke:#E2D6BE;stroke-width:4;stroke-linecap:round;stroke-linejoin:round}
.m-water{fill:#C7DAD3}
.m-river{fill:none;stroke:#A9C6BD;stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
.m-river-s{fill:none;stroke:#BBD2CA;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}
.m-town{fill:var(--white);stroke:var(--ink-2);stroke-width:3}
.m-label,.m-place,.m-water-label{paint-order:stroke;stroke:#F7F3EA;stroke-linejoin:round}
.m-label{font:700 30px var(--sans);fill:var(--ink-2);stroke-width:8px}
.m-water-label{font:400 italic 34px var(--serif);fill:#5E8A7F;letter-spacing:.06em;stroke-width:8px}
.m-place{font:400 68px var(--serif);fill:var(--green);stroke-width:12px}
.m-dot{fill:var(--green);stroke:var(--white);stroke-width:5}
.m-halo{fill:rgba(197,170,119,.32)}
.m-pulse{fill:var(--gold);transform-box:fill-box;transform-origin:center;animation:mapPulse 2.6s ease-out infinite}
@keyframes mapPulse{from{transform:scale(1);opacity:.7}to{transform:scale(3.4);opacity:0}}
@media (prefers-reduced-motion:reduce){.m-pulse{animation:none;opacity:0}}
"""
open(c, "w", encoding="utf-8", newline="\n").write(t)
open("_proba/batch.txt", "w").write("ok")
