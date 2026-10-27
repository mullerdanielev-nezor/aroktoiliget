import re, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"}
css = urllib.request.urlopen(urllib.request.Request("https://fonts.googleapis.com/css2?family=Archivo:wght@100..900&display=swap", headers=UA), timeout=60).read().decode()
log = [css]
for subset, block in re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*\{[^}]*\})", css):
    if subset not in ("latin", "latin-ext"): continue
    url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
    rng = re.search(r"unicode-range:\s*([^;]+);", block).group(1)
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
    open(rf"D:\Letolt\liget\assets\fonts\archivo-{subset}.woff2", "wb").write(data)
    log.append(f"{subset} {len(data)//1024}KB RANGE {rng}")
open(r"D:\Letolt\liget\_proba\archivo.txt", "w", encoding="utf-8").write("\n".join(log))
