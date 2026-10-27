import os, html
OUT = r"D:\Letolt\liget\_proba\fontok"
os.makedirs(OUT, exist_ok=True)

# (slug, név, hangulat, címbetű, címsúly, alapbetű, Google Fonts család-paraméterek, címbetű letter-spacing)
COMBOS = [
    ("fraunces-figtree", "Fraunces + Figtree", "Meleg, puha talpas cím, barátságos modern alapszöveg.",
     "Fraunces", 800, "Figtree", "family=Fraunces:opsz,wght@9..144,800&family=Figtree:wght@400;500;700", "-.02em"),
    ("bricolage-atkinson", "Bricolage Grotesque + Atkinson Hyperlegible Next", "Karakteres, mai talpatlan cím; idősek számára tervezett, nagyon jól olvasható alapszöveg.",
     "Bricolage Grotesque", 800, "Atkinson Hyperlegible Next", "family=Bricolage+Grotesque:opsz,wght@12..96,800&family=Atkinson+Hyperlegible+Next:wght@400;500;700", "-.035em"),
    ("bodoni-manrope", "Bodoni Moda + Manrope", "Elegáns, prémium kontraszt: divatlapos cím, letisztult alapszöveg.",
     "Bodoni Moda", 800, "Manrope", "family=Bodoni+Moda:opsz,wght@6..96,800&family=Manrope:wght@400;500;700", "-.02em"),
    ("gloock-albert", "Gloock + Albert Sans", "Magazinos, súlyos talpas cím, nyugodt skandináv alapszöveg.",
     "Gloock", 400, "Albert Sans", "family=Gloock&family=Albert+Sans:wght@400;500;700", "-.015em"),
    ("abril-lato", "Abril Fatface + Lato", "Klasszikus, nagyon vastag kontrasztos cím, ismerős, semleges alapszöveg.",
     "Abril Fatface", 400, "Lato", "family=Abril+Fatface&family=Lato:wght@400;700", "-.01em"),
    ("literata-lexend", "Literata + Lexend", "Könyves, megbízható cím; az olvasási nehézségekre optimalizált Lexend alapszöveg.",
     "Literata", 800, "Lexend", "family=Literata:opsz,wght@7..72,800&family=Lexend:wght@400;500;700", "-.02em"),
    ("merriweather", "Merriweather + Merriweather Sans", "Robusztus, képernyőre tervezett család: erős cím, egymáshoz illő alapszöveg.",
     "Merriweather", 900, "Merriweather Sans", "family=Merriweather:wght@900&family=Merriweather+Sans:wght@400;500;700", "-.02em"),
    ("archivo", "Archivo Black súly + Archivo", "Egyetlen talpatlan család: tömör, határozott, nagyon modern.",
     "Archivo", 900, "Archivo", "family=Archivo:wght@400;500;700;900", "-.035em"),
    ("newsreader-public", "Newsreader + Public Sans", "Újságos, hiteles cím; közszolgálati egyszerűségű alapszöveg.",
     "Newsreader", 800, "Public Sans", "family=Newsreader:opsz,wght@6..72,800&family=Public+Sans:wght@400;500;700", "-.02em"),
    ("playfair-source", "Playfair Display + Source Sans 3", "Hagyományos, ünnepélyes cím, kiforrott, jól olvasható alapszöveg.",
     "Playfair Display", 900, "Source Sans 3", "family=Playfair+Display:wght@900&family=Source+Sans+3:wght@400;600;700", "-.015em"),
]
N = len(COMBOS)
IMG = "../../assets/img/rezidencia/"

CSS = """
:root{--green:#183E35;--green-deep:#10302A;--gold:#C5AA77;--gold-ink:#7A6034;--ivory:#F5F0E6;--white:#fff;--ink:#202A25;--ink-2:#4F554D;--line:#E3DCCD;--on-green:#F5F0E6;--on-green-2:#CDD5CA}
*{box-sizing:border-box}
body{margin:0;background:var(--ivory);color:var(--ink);font:400 1.125rem/1.6 var(--sans);-webkit-font-smoothing:antialiased}
h1,h2,h3,.num{font-family:var(--head);font-weight:var(--hw);letter-spacing:var(--ls);margin:0;line-height:1.02}
p{margin:0}
.wrap{max-width:1160px;margin:0 auto;padding-inline:max(16px,4vw)}
.bar{position:sticky;top:0;z-index:5;background:var(--green-deep);color:var(--on-green);font:500 .9375rem/1.3 var(--sans)}
.bar .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:8px 18px;padding-block:12px}
.bar b{font-weight:700}
.bar .mood{color:var(--on-green-2);flex:1 1 20em}
.bar nav{display:flex;gap:8px}
.bar a{color:var(--on-green);text-decoration:none;padding:6px 12px;border:1px solid rgba(245,240,230,.3);border-radius:999px;white-space:nowrap}
.bar a:hover{background:rgba(245,240,230,.1)}
.hero{text-align:center;padding-block:clamp(48px,8vw,104px) 40px}
.hero h1{font-size:clamp(2.75rem,.5rem + 8vw,7rem);color:var(--green);max-width:11em;margin-inline:auto;text-wrap:balance}
.hero p{margin:22px auto 0;max-width:26em;font-size:clamp(1.125rem,1rem + .6vw,1.5rem);color:var(--ink-2);text-wrap:balance}
.ctas{display:flex;flex-wrap:wrap;justify-content:center;gap:12px;margin-top:32px}
.btn{display:inline-flex;align-items:center;justify-content:center;min-height:56px;min-width:14rem;padding:0 28px;border-radius:6px;background:var(--gold);color:var(--green-deep);font:700 1.0625rem/1 var(--sans);text-decoration:none}
.hero-img{display:block;width:100%;height:auto;aspect-ratio:21/9;object-fit:cover;border-radius:12px;margin-top:clamp(36px,5vw,56px)}
section{padding-block:clamp(48px,7vw,96px)}
.center{text-align:center}
.center h2{font-size:clamp(2.25rem,1.2rem + 3.6vw,4.25rem);max-width:13em;margin-inline:auto;text-wrap:balance}
.lead{margin:18px auto 0;max-width:30em;font-size:clamp(1.125rem,1rem + .5vw,1.375rem);color:var(--ink-2);text-wrap:balance}
.grid{display:grid;gap:18px;margin-top:40px}
@media (min-width:860px){.grid{grid-template-columns:1fr 1fr 1fr}}
.card{background:var(--white);border-radius:12px;overflow:hidden}
.card img{display:block;width:100%;height:auto;aspect-ratio:4/3;object-fit:cover}
.card div{padding:22px 24px 26px}
.card h3{font-size:clamp(1.75rem,1.3rem + 1.2vw,2.25rem)}
.card .meta{margin-top:4px;color:var(--ink-2);font-size:1rem}
.card .num{display:block;margin-top:18px;padding-top:16px;border-top:1px solid var(--line);font-size:2rem;color:var(--green)}
.card .lbl{font-size:.9375rem;color:var(--ink-2)}
.green{background:var(--green);color:var(--on-green)}
.green h2{color:var(--on-green)}
.green .lead{color:var(--on-green-2)}
.two{display:grid;gap:28px;align-items:center}
@media (min-width:860px){.two{grid-template-columns:1fr 1fr;gap:56px}}
.wiz{background:var(--white);color:var(--ink);border-radius:14px;padding:clamp(22px,4vw,44px)}
.wiz .step{font:700 .9375rem/1 var(--sans);color:var(--gold-ink);letter-spacing:.08em}
.wiz h3{margin-top:14px;font-size:clamp(2.125rem,1.5rem + 2.2vw,3.25rem);color:var(--ink)}
.opt{display:flex;align-items:center;gap:16px;margin-top:12px;padding:18px 20px;border:1.5px solid var(--line);border-radius:10px}
.opt.on{border-color:var(--green);background:#E9EFE8}
.ring{flex:none;width:26px;height:26px;border-radius:50%;border:2px solid #B4AA97}
.on .ring{border-color:var(--green);background:var(--green);box-shadow:inset 0 0 0 5px #fff}
.opt b{display:block;font-size:1.25rem}
.opt small{color:var(--ink-2);font-size:1rem}
.body-sample p+p{margin-top:16px}
.body-sample p{color:var(--on-green-2);font-size:1.125rem}
.body-sample h2{font-size:clamp(2rem,1.2rem + 2.6vw,3.25rem);margin-bottom:20px;text-align:left}
.closing{text-align:center}
.closing h2{font-size:min(7.4vw,6.5rem);line-height:1;color:var(--green);white-space:nowrap}
.closing h2 span{display:block}
.closing h2 span+span{color:var(--gold-ink)}
.closing .btn{margin-top:36px;min-height:64px;font-size:1.25rem}
.chars{border-top:1px solid var(--line);padding-block:28px 48px;color:var(--ink-2);font-size:1rem}
.chars .h{font-family:var(--head);font-weight:var(--hw);font-size:2rem;color:var(--ink);line-height:1.2}
"""

def page(i):
    slug, name, mood, head, hw, body, fam, ls = COMBOS[i]
    prev = f"{(i - 1) % N + 1:02d}-{COMBOS[(i - 1) % N][0]}.html"
    nxt = f"{(i + 1) % N + 1:02d}-{COMBOS[(i + 1) % N][0]}.html"
    return f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{i+1:02d} · {html.escape(name)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fam}&display=swap">
<style>:root{{--head:"{head}",Georgia,serif;--hw:{hw};--ls:{ls};--sans:"{body}",system-ui,sans-serif}}{CSS}</style>
</head><body>
<div class="bar"><div class="wrap"><b>{i+1:02d} / {N} · {html.escape(name)}</b><span class="mood">{html.escape(mood)}</span>
<nav><a href="{prev}">← Előző</a><a href="index.html">Összes</a><a href="{nxt}">Következő →</a></nav></div></div>

<header class="hero wrap">
  <h1>A gondoskodásnak is lehet otthona.</h1>
  <p>Tervezett, száz férőhelyes senior rezidencia Ároktőn, a Tisza mellett.</p>
  <div class="ctas"><a class="btn" href="#">Jelentkezem időben</a><a class="btn" href="#">Szobák és díjak</a></div>
  <img class="hero-img" src="{IMG}udvar.jpg" alt="">
</header>

<section class="wrap center">
  <h2>Méltó környezet az élet következő fejezetéhez.</h2>
  <p class="lead">Egy meglévő épület megújításával és bővítésével, száz lakó számára.</p>
  <div class="grid">
    <div class="card"><img src="{IMG}egyagyas.jpg" alt=""><div><h3>Egyágyas szoba</h3><p class="meta">1 lakó / szoba</p><span class="num">6 000 000 Ft</span><span class="lbl">egyszeri belépési hozzájárulás / fő</span></div></div>
    <div class="card"><img src="{IMG}ketagyas.jpg" alt=""><div><h3>Kétágyas szoba</h3><p class="meta">2 lakó / szoba</p><span class="num">4 800 000 Ft</span><span class="lbl">egyszeri belépési hozzájárulás / fő</span></div></div>
    <div class="card"><img src="{IMG}negyagyas.jpg" alt=""><div><h3>Négyágyas szoba</h3><p class="meta">4 lakó / szoba</p><span class="num">3 000 000 Ft</span><span class="lbl">egyszeri belépési hozzájárulás / fő</span></div></div>
  </div>
</section>

<section class="green"><div class="wrap two">
  <div class="body-sample">
    <h2>Gondoskodás a mindennapokban.</h2>
    <p>Ároktő a Tisza jobb partján fekvő, nyugodt borsodi község, Miskolctól mintegy 45 kilométerre délre. A falu határa ártéri erdőkkel, holtágakkal és természetvédelmi területekkel érintkezik.</p>
    <p>A rezidencia koncepciójának középpontjában a mindennapi biztonság, a személyes gondoskodás és a közösséghez tartozás áll: 24 órás felügyelet, napi étkezés, közösségi programok és kertkapcsolat.</p>
  </div>
  <div class="wiz">
    <span class="step">1 / 6</span>
    <h3>Kinek szól a jelentkezés?</h3>
    <div class="opt on"><span class="ring"></span><span><b>A szerettemnek</b><small>Szülőnek, nagyszülőnek vagy más hozzátartozónak</small></span></div>
    <div class="opt"><span class="ring"></span><span><b>Saját magamnak</b></span></div>
  </div>
</div></section>

<section class="wrap closing">
  <h2><span>Ők gondoskodtak rólunk.</span> <span>Most rajtunk a sor.</span></h2>
  <a class="btn" href="#">Jelentkezem időben</a>
</section>

<div class="wrap chars">
  <p class="h">Árvíztűrő tükörfúrógép · ÁRVÍZTŰRŐ · 0123456789</p>
  <p>Alapszöveg: Árvíztűrő tükörfúrógép, ő ű Ő Ű – 550 000 Ft / fő / hó. Címbetű: {html.escape(head)} {hw} · Alapbetű: {html.escape(body)} 400/700</p>
</div>
</body></html>"""

for i, c in enumerate(COMBOS):
    open(os.path.join(OUT, f"{i+1:02d}-{c[0]}.html"), "w", encoding="utf-8").write(page(i))

fams = "&".join(c[6] for c in COMBOS)
items = "\n".join(f"""  <a class="it" href="{i+1:02d}-{c[0]}.html" style="--head:'{c[3]}';--hw:{c[4]};--ls:{c[7]};--sans:'{c[5]}'">
    <span class="no">{i+1:02d}</span>
    <span class="h">Ők gondoskodtak rólunk.</span>
    <span class="b">Tervezett, száz férőhelyes senior rezidencia Ároktőn, a Tisza mellett. Árvíztűrő tükörfúrógép.</span>
    <span class="n">{html.escape(c[1])}</span>
  </a>""" for i, c in enumerate(COMBOS))
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>10 betűtípus-páros</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fams}&display=swap">
<style>
body{{margin:0;background:#F5F0E6;color:#202A25;font:400 1rem/1.5 system-ui,sans-serif}}
.wrap{{max-width:1160px;margin:0 auto;padding:40px max(16px,4vw) 64px}}
h1{{font:700 1.75rem/1.2 system-ui,sans-serif;margin:0 0 6px}}
.sub{{color:#4F554D;margin:0 0 28px}}
.list{{display:grid;gap:14px}}
@media (min-width:860px){{.list{{grid-template-columns:1fr 1fr}}}}
.it{{display:grid;gap:8px;padding:24px 26px;background:#fff;border-radius:12px;color:inherit;text-decoration:none;border:1.5px solid transparent}}
.it:hover{{border-color:#183E35}}
.no{{font:700 .8125rem/1 system-ui,sans-serif;color:#7A6034;letter-spacing:.1em}}
.h{{font-family:var(--head);font-weight:var(--hw);letter-spacing:var(--ls);font-size:clamp(2rem,1.4rem + 2vw,2.75rem);line-height:1.02;color:#183E35}}
.b{{font-family:var(--sans);font-size:1.0625rem;color:#4F554D}}
.n{{font:700 .9375rem/1.3 system-ui,sans-serif;margin-top:4px}}
</style></head><body><div class="wrap">
<h1>10 vastag cím + alapbetű páros</h1>
<p class="sub">Kattintson bármelyikre: teljes oldalrészlet a valódi szövegekkel, képekkel és színekkel. Mind kezeli a magyar ő/ű betűket.</p>
<div class="list">
{items}
</div></div></body></html>""")
open(r"D:\Letolt\liget\_proba\batch.txt", "w").write("ok")
