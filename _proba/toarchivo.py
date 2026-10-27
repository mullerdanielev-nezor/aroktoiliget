import os, re, glob
os.chdir(r"D:\Letolt\liget")
log = open(r"D:\Letolt\liget\_proba\archivo.txt", encoding="utf-8").read()
R = dict(re.findall(r"^(latin(?:-ext)?) \d+KB RANGE (.+)$", log, re.M))

c = "assets/css/style.css"
t = open(c, encoding="utf-8").read()
lines = t.split("\n")
assert all(l.startswith("@font-face") for l in lines[1:5]), lines[1:5]
ff = [f'@font-face{{font-family:"Archivo";font-style:normal;font-weight:100 900;font-display:swap;src:url("../fonts/archivo-{s}.woff2") format("woff2");unicode-range:{R[s]}}}' for s in ("latin-ext", "latin")]
lines[1:5] = ff
t = "\n".join(lines)

t = re.sub(r'--serif:[^;]+;', '--serif:"Archivo","Helvetica Neue",Arial,sans-serif;', t, count=1)
t = re.sub(r'--sans:[^;]+;', '--sans:"Archivo","Helvetica Neue",Arial,sans-serif;', t, count=1)
# alapszöveg 400, címek tömör 900 / 800
t = t.replace("font:500 1.125rem/1.6 var(--sans);-webkit-font-smoothing", "font:400 1.125rem/1.6 var(--sans);-webkit-font-smoothing")
t = t.replace("h1,h2,h3{font-family:var(--serif);font-weight:500;margin:0;text-wrap:balance;letter-spacing:-.01em}",
              "h1,h2{font-family:var(--serif);font-weight:900;margin:0;text-wrap:balance;letter-spacing:-.035em}\nh3{font-family:var(--serif);font-weight:800;margin:0;text-wrap:balance;letter-spacing:-.025em}")
t = t.replace(".num{font-family:var(--serif);font-weight:400;white-space:nowrap}", ".num{font-family:var(--serif);font-weight:800;letter-spacing:-.02em;white-space:nowrap}")
# minden var(--serif)-es font-rövidítés: 800-as súly
t = re.sub(r"font:(?:400|500|600) ((?:italic )?[^;{}]*?var\(--serif\))", r"font:800 \1", t)
t = t.replace("font:800 italic 34px var(--serif)", "font:700 34px var(--serif)")
t = t.replace(".m-place{font:800 68px var(--serif)", ".m-place{font:900 68px var(--serif)")
t = t.replace(".brand-name{font:800 1.1875rem/1 var(--serif);letter-spacing:.07em", ".brand-name{font:800 1.1875rem/1 var(--serif);letter-spacing:.05em")
# nagy címek: szorosabb betűköz
for a, b in [(".hero h1{font-size:clamp(2.5rem,.5rem + 8vw,7.5rem);line-height:.96;letter-spacing:-.025em", ".hero h1{font-size:clamp(2.5rem,.5rem + 7.4vw,7rem);line-height:.96;letter-spacing:-.045em"),
             ("letter-spacing:-.015em;color:var(--ink);margin:0;text-wrap:balance}", "letter-spacing:-.035em;color:var(--ink);margin:0;text-wrap:balance}"),
             (".signup-head h2{font-size:clamp(2.375rem,1rem + 5vw,4.75rem);line-height:1;letter-spacing:-.025em", ".signup-head h2{font-size:clamp(2.375rem,1rem + 5vw,4.75rem);line-height:1;letter-spacing:-.04em"),
             ("/1.05 var(--serif);letter-spacing:-.02em;max-width:15em", "/1.05 var(--serif);letter-spacing:-.04em;max-width:15em"),
             (".closing h2{font-size:min(7.4vw,6.75rem);line-height:1;letter-spacing:-.03em", ".closing h2{font-size:min(6.6vw,6rem);line-height:1;letter-spacing:-.045em")]:
    assert t.count(a) == 1, a
    t = t.replace(a, b)
open(c, "w", encoding="utf-8", newline="\n").write(t)

PRE_OLD = re.compile(r'<link rel="preload" href="(/?)assets/fonts/dm-serif-display-latin\.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="/?assets/fonts/atkinson-hyperlegible-next-latin\.woff2" as="font" type="font/woff2" crossorigin>')
for p in glob.glob("*.html"):
    s = open(p, encoding="utf-8").read()
    s2, k = PRE_OLD.subn(r'<link rel="preload" href="\1assets/fonts/archivo-latin.woff2" as="font" type="font/woff2" crossorigin>', s)
    assert k == 1, p
    s2 = s2.replace("font:500 clamp(4.5rem,3rem + 8vw,8rem)/.9 var(--serif)", "font:900 clamp(4.5rem,3rem + 8vw,8rem)/.9 var(--serif)")
    s2 = s2.replace("font:400 1.25rem/1 var(--serif)", "font:800 1.25rem/1 var(--serif)")
    s2 = s2.replace("Betűtípusok: DM Serif Display és Atkinson Hyperlegible Next (SIL Open Font License).", "Betűtípus: Archivo, Omnibus-Type (SIL Open Font License 1.1).")
    open(p, "w", encoding="utf-8", newline="\n").write(s2)
for f in ["dm-serif-display-latin", "dm-serif-display-latin-ext", "atkinson-hyperlegible-next-latin", "atkinson-hyperlegible-next-latin-ext"]:
    os.remove(f"assets/fonts/{f}.woff2")
open(r"D:\Letolt\liget\_proba\batch.txt", "w").write("ok")
