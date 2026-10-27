import os, re
os.chdir(r"D:\Letolt\liget")

CARDS = [
    ("beszelgetes", 900, 600, "45% 50%", "Illusztráció: egy gondozó beszélget egy idős úrral a kerti padon",
     '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
     "Éjjel-nappal mellette", "24 órás felügyelet, gondozás és alapápolás."),
    ("ketagyas", 1200, 675, "50% 50%", "Illusztráció: világos kétágyas szoba fotelekkel az ablaknál",
     '<path d="M3 19v-9M3 15h18v4M21 15v-2a3 3 0 0 0-3-3h-7v5"/><circle cx="7" cy="12" r="1.6"/>',
     "Teljes ellátás", "Szállás, napi étkezés és takarítás."),
    ("kartya", 1200, 675, "40% 50%", "Illusztráció: idősek kártyáznak egy világos közösségi teremben, egy gondozó mosolyogva figyeli őket",
     '<circle cx="9" cy="8" r="3"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><circle cx="17" cy="9" r="2.4"/><path d="M16 14.3a4.6 4.6 0 0 1 5 4.7"/>',
     "Közös délutánok", "Közösségi programok és mentálhigiénés foglalkozások."),
    ("seta", 900, 507, "24% 60%", "Illusztráció: két idős hölgy sétál karonfogva a rezidencia kertjében",
     '<path d="M12 21v-6"/><path d="M12 15a4.5 4.5 0 0 0 4.4-5.5A4.5 4.5 0 0 0 12 3a4.5 4.5 0 0 0-4.4 6.5A4.5 4.5 0 0 0 12 15z"/>',
     "Kert és közös terek", "Séta, friss levegő, beszélgetés a szabadban."),
]
n = len(CARDS)
cards = "\n".join(f'''          <li class="svc-card" aria-roledescription="kártya" aria-label="{i+1} / {n}">
            <img src="assets/img/rezidencia/{slug}.jpg" width="{w}" height="{h}" style="object-position:{pos}" alt="{alt}" loading="lazy" decoding="async">
            <div class="svc-body">
              <span class="svc-icon"><svg viewBox="0 0 24 24" aria-hidden="true">{svg}</svg></span>
              <h3 class="svc-name">{name}</h3>
              <p class="svc-sub">{sub}</p>
            </div>
          </li>''' for i, (slug, w, h, pos, alt, svg, name, sub) in enumerate(CARDS))

s = open("index.html", encoding="utf-8").read()
a = s.index('      <ul class="svc-grid">')
b = s.index('      <p class="care-note">', a)
s = s[:a] + f'''      <div class="svc-car" data-svc-car role="region" aria-roledescription="kártyalapozó" aria-label="Szolgáltatások">
        <ul class="svc-track" tabindex="0">
{cards}
        </ul>
        <div class="svc-nav">
          <div class="svc-progress" aria-hidden="true"><span></span></div>
          <button class="car-btn" type="button" data-svc-prev aria-label="Előző kártya"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M12.5 4.5L7 10l5.5 5.5" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>
          <button class="car-btn" type="button" data-svc-next aria-label="Következő kártya"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M7.5 4.5L13 10l-5.5 5.5" fill="none" stroke="currentColor" stroke-width="2"/></svg></button>
        </div>
      </div>
''' + s[b:]

js_anchor = '  var sticky = document.getElementById("sticky-cta");'
assert s.count(js_anchor) == 1
s = s.replace(js_anchor, '''  /* Szolgáltatás-kártyák lapozása */
  document.querySelectorAll("[data-svc-car]").forEach(function(car){
    var track = car.querySelector(".svc-track"), bar = car.querySelector(".svc-progress span");
    var prev = car.querySelector("[data-svc-prev]"), next = car.querySelector("[data-svc-next]");
    function step(){ var c = track.children[0]; return c.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 0); }
    function update(){
      var max = track.scrollWidth - track.clientWidth;
      var visible = track.clientWidth / track.scrollWidth;
      bar.style.width = (visible + (max > 0 ? track.scrollLeft / max : 1) * (1 - visible)) * 100 + "%";
      prev.disabled = track.scrollLeft <= 2; next.disabled = track.scrollLeft >= max - 2;
      car.classList.toggle("no-overflow", max <= 2);
    }
    prev.addEventListener("click", function(){ track.scrollBy({ left: -step(), behavior: "smooth" }); });
    next.addEventListener("click", function(){ track.scrollBy({ left: step(), behavior: "smooth" }); });
    track.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    update();
  });

''' + js_anchor)
open("index.html", "w", encoding="utf-8", newline="\n").write(s)

c = "assets/css/style.css"
t = open(c, encoding="utf-8").read()
a = t.index(".svc-grid{list-style")
b = t.index(".care-note{")
t = t[:a] + t[b:]
a = t.index(".svc-grid{grid-auto-flow:dense}")
t = t[:a]
t = t.replace("@media (prefers-reduced-motion:reduce){.svc{transition:none}}\n", "")
t += """/* Szolgáltatás-kártyák: lapozható sor */
.svc-car{margin-top:clamp(36px,5vw,64px)}
.svc-track{list-style:none;margin:0;padding:0 0 4px;display:grid;grid-auto-flow:column;grid-auto-columns:82%;gap:clamp(12px,1.6vw,20px);overflow-x:auto;scroll-snap-type:x mandatory;overscroll-behavior-x:contain;scrollbar-width:none}
.svc-track::-webkit-scrollbar{display:none}
.svc-track:focus-visible{outline:2px solid var(--gold);outline-offset:4px;border-radius:12px}
@media (min-width:640px){.svc-track{grid-auto-columns:calc((100% - 20px) / 2.15)}}
@media (min-width:1000px){.svc-track{grid-auto-columns:calc((100% - 40px) / 3.2)}}
.svc-card{position:relative;min-width:0;aspect-ratio:4/5;border-radius:12px;overflow:hidden;scroll-snap-align:start;background:var(--green-deep)}
.svc-card img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .6s ease}
@media (hover:hover){.svc-card:hover img{transform:scale(1.04)}}
.svc-body{position:absolute;inset:auto 0 0 0;display:flex;flex-direction:column;gap:8px;padding:72px clamp(20px,2.2vw,30px) clamp(20px,2.2vw,30px);background:linear-gradient(to top,rgba(16,48,42,.94) 35%,rgba(16,48,42,0))}
.svc-icon{display:grid;place-items:center;width:48px;height:48px;margin-bottom:6px;border-radius:50%;background:var(--gold);color:var(--green-deep)}
.svc-icon svg{width:24px;height:24px;fill:none;stroke:currentColor;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}
.svc-name{font:400 clamp(1.75rem,1.3rem + 1.4vw,2.375rem)/1.05 var(--serif);color:var(--on-green)}
.svc-sub{font-size:clamp(1rem,.95rem + .25vw,1.125rem);line-height:1.4;color:var(--on-green-2)}
.svc-nav{display:flex;align-items:center;gap:12px;margin-top:clamp(18px,2.4vw,28px)}
.svc-progress{flex:1;height:2px;margin-right:8px;background:var(--on-green-line);border-radius:2px;overflow:hidden}
.svc-progress span{display:block;height:100%;width:30%;background:var(--gold);transition:width .2s}
.svc-nav .car-btn:disabled{opacity:.35;cursor:default}
.svc-car.no-overflow .svc-nav{display:none}
@media (prefers-reduced-motion:reduce){.svc-card img,.svc-progress span{transition:none}}
"""
open(c, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
