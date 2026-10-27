import os
from PIL import Image
os.chdir(r"D:\Letolt\liget")

def save(src, dst, w, q=74):
    im = Image.open("images/" + src).convert("RGB")
    h = round(im.height * w / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    im.save("assets/img/rezidencia/" + dst, "JPEG", quality=q, optimize=True, progressive=True)
    print(dst, im.size, os.path.getsize("assets/img/rezidencia/" + dst) // 1024, "KB")

save("Nyugodt idősek otthona udvara.png", "epulet.jpg", 1400)
save("Kártyaparti a gondozóotthonban.png", "kartya.jpg", 1200)
save("Békés séta az idősek otthona kertjében.png", "seta.jpg", 900)
save("Meghitt beszélgetés a kertben.png", "beszelgetes.jpg", 900)

def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for a, b in pairs:
        assert s.count(a) == 1, (p, a[:70], s.count(a))
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="\n").write(s)

def photo(cls, slug, w, h, alt, cap):
    return (f'        <li class="svc-photo {cls}"><img src="assets/img/rezidencia/{slug}.jpg" width="{w}" height="{h}" alt="{alt}" loading="lazy" decoding="async">'
            f'<span class="svc-photo-cap">{cap}</span></li>\n')

s = open("index.html", encoding="utf-8").read()
import re
lis = re.findall(r'        <li class="svc">.*?</li>\n', s)
assert len(lis) == 8
im = {n: Image.open("assets/img/rezidencia/" + n + ".jpg").size for n in ["kartya", "seta", "beszelgetes"]}
k = photo("svc-wide", "kartya", *im["kartya"], "Illusztráció: idősek kártyáznak egy világos közösségi teremben, egy gondozó mosolyogva figyeli őket", "Közös délutánok")
sz = photo("svc-seta", "seta", *im["seta"], "Illusztráció: két idős hölgy sétál karonfogva a rezidencia kertjében", "Séta a kertben")
b = photo("svc-beszelgetes", "beszelgetes", *im["beszelgetes"], "Illusztráció: egy gondozó beszélget egy idős úrral a kerti padon", "Mindig van kihez szólni")
new = k + lis[0] + lis[1] + lis[2] + lis[3] + sz + "".join(lis[4:8]) + b
old = "".join(lis)
assert s.count(old) == 1
s = s.replace(old, new)
s = s.replace('<p class="care-note">A szolgáltatások pontos köre a projekt előrehaladásával véglegesedik.</p>',
              '<p class="care-note">A képek illusztrációk. A szolgáltatások pontos köre a projekt előrehaladásával véglegesedik.</p>')
open("index.html", "w", encoding="utf-8", newline="\n").write(s)

e = Image.open("assets/img/rezidencia/epulet.jpg").size
edit("index.html", [
    ('<img src="assets/img/rezidencia/egyagyas.jpg" width="1200" height="675" alt="Illusztráció: egy gondozó beszélget egy idős hölggyel a napfényes szobában" loading="lazy" decoding="async">',
     f'<img src="assets/img/rezidencia/epulet.jpg" width="{e[0]}" height="{e[1]}" alt="Illusztráció: a felújított, kétszintes épület parkosított udvarral; idősek padon és asztaloknál, gondozók kísérik őket" loading="lazy" decoding="async">'),
])
edit("assets/css/style.css", [
    (".bento-main img{object-position:60% 50%}", ".bento-main img{object-position:50% 60%}"),
])
css = """.svc-grid{grid-auto-flow:dense}
.svc-photo{position:relative;min-width:0;min-height:clamp(180px,22vw,240px);border-radius:10px;overflow:hidden;background:var(--green-deep)}
.svc-photo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.svc-photo-cap{position:absolute;inset:auto 0 0 0;padding:40px clamp(16px,2vw,24px) clamp(14px,1.8vw,22px);font:400 clamp(1.125rem,.95rem + .6vw,1.5rem)/1.15 var(--serif);color:var(--on-green);background:linear-gradient(to top,rgba(16,48,42,.85),rgba(16,48,42,0))}
.svc-wide{grid-column:span 2;aspect-ratio:16/10}
.svc-seta img{object-position:22% 60%}
.svc-beszelgetes img{object-position:45% 50%}
@media (min-width:860px){.svc-wide{aspect-ratio:auto}}
"""
open("assets/css/style.css", "a", encoding="utf-8", newline="\n").write(css)
print("ok")
