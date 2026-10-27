import json, re, urllib.parse, urllib.request
UA = {"User-Agent": "AroktoiLigetSite/1.0 (contact via site)"}
API = "https://commons.wikimedia.org/w/api.php?"
def call(p):
    p["format"] = "json"
    return json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(p), headers=UA), timeout=60))
def clean(h): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", h or "")).strip()
out = open(r"D:\Letolt\liget\_proba\geo.txt", "w", encoding="utf-8")
def dump(label, d):
    for p in d.get("query", {}).get("pages", {}).values():
        if "imageinfo" not in p: continue
        ii = p["imageinfo"][0]; m = ii.get("extmetadata", {})
        out.write(f'{label} | {p["title"]} | {ii["width"]}x{ii["height"]} | {m.get("LicenseShortName",{}).get("value")} | {clean(m.get("Artist",{}).get("value"))[:25]} | {clean(m.get("ImageDescription",{}).get("value"))[:110]}\n')
props = {"prop": "imageinfo", "iiprop": "size|extmetadata", "iiextmetadatafilter": "LicenseShortName|Artist|ImageDescription"}
dump("GEO", call(dict({"action": "query", "generator": "geosearch", "ggscoord": "47.7308|20.9423", "ggsradius": 6000, "ggslimit": 100, "ggsnamespace": 6}, **props)))
for q in ["Ároktő", "Arokto", "Ároktő Tisza", "Ároktő komp", "Ároktői"]:
    dump("S:" + q, call(dict({"action": "query", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 50}, **props)))
out.close()
