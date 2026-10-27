import json, urllib.parse, urllib.request
B = "47.45,20.40,48.18,21.45"
q = f"""[out:json][timeout:180];
(
  way["waterway"="river"]["name"~"^(Tisza|Sajó|Eger|Rima|Hejő)$"]({B});
  way["water"="oxbow"]({B});
  relation["water"="oxbow"]({B});
  relation["name"="Tisza-tó"]({B});
  way["name"="Tisza-tó"]["natural"="water"]({B});
  way["highway"="motorway"]({B});
);
out geom;"""
import time
for url in ["https://overpass.private.coffee/api/interpreter", "https://overpass.kumi.systems/api/interpreter", "https://overpass-api.de/api/interpreter"]:
  try:
    req = urllib.request.Request(url, data=urllib.parse.urlencode({"data": q}).encode(),
                             headers={"User-Agent": "AroktoiLigetSite/1.0"})
    d = json.load(urllib.request.urlopen(req, timeout=240)); break
  except Exception as ex: print(url, ex)
json.dump(d, open(r"D:\Letolt\liget\_proba\osm.json", "w", encoding="utf-8"))
from collections import Counter
c = Counter()
for e in d["elements"]:
    t = e.get("tags", {})
    c[(e["type"], t.get("waterway") or t.get("water") or t.get("highway") or t.get("natural"), t.get("name", ""))] += 1
open(r"D:\Letolt\liget\_proba\osm.txt", "w", encoding="utf-8").write("\n".join(f"{k} {v}" for k, v in c.most_common()))
