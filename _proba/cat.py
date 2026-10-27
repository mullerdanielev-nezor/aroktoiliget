import json, re, urllib.parse, urllib.request
UA = {"User-Agent": "AroktoiLigetSite/1.0 (contact via site)"}
API = "https://commons.wikimedia.org/w/api.php?"
def call(p):
    p["format"] = "json"
    return json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(p), headers=UA), timeout=60))
def clean(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h or "")).strip()

out = open(r"D:\Letolt\liget\_proba\cat.txt", "w", encoding="utf-8")
seen = set()
def walk(cat, depth):
    if cat in seen or depth > 2: return
    seen.add(cat)
    cont = {}
    while True:
        d = call(dict({"action": "query", "generator": "categorymembers", "gcmtitle": cat, "gcmlimit": 200, "gcmtype": "file|subcat",
                  "prop": "imageinfo", "iiprop": "size|extmetadata", "iiextmetadatafilter": "LicenseShortName|Artist|ImageDescription"}, **cont))
        for p in d.get("query", {}).get("pages", {}).values():
            if p["ns"] == 14: walk(p["title"], depth + 1); continue
            if "imageinfo" not in p: continue
            ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
            out.write(f'{cat[9:]} | {p["title"]} | {ii["width"]}x{ii["height"]} | {m.get("LicenseShortName",{}).get("value")} | {clean(m.get("Artist",{}).get("value"))[:25]} | {clean(m.get("ImageDescription",{}).get("value"))[:90]}\n')
        if "continue" not in d: break
        cont = {"gcmcontinue": d["continue"]["gcmcontinue"], "continue": d["continue"]["continue"]}
walk("Category:Ároktő", 0)
out.close()
