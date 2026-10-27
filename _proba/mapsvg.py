import json, math
d = json.load(open(r"D:\Letolt\liget\_proba\osm.json", encoding="utf-8"))
LON0, LON1, LAT0, LAT1 = 20.46, 21.30, 47.50, 48.135
K = math.cos(math.radians(47.85))
W = 1000
S = W / ((LON1 - LON0) * K)
H = round((LAT1 - LAT0) * S)
def P(lat, lon): return ((lon - LON0) * K * S, (LAT1 - lat) * S)

def simplify(pts, tol=1.6):
    out = [pts[0]]
    for p in pts[1:-1]:
        if math.dist(p, out[-1]) >= tol: out.append(p)
    out.append(pts[-1]); return out
def path(pts, close=False):
    pts = simplify(pts)
    s = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    return s + ("Z" if close else "")
def geom(g): return [P(p["lat"], p["lon"]) for p in g]

def rings(ways):
    ways = [w[:] for w in ways]; out = []
    while ways:
        r = ways.pop(0)
        while r[0] != r[-1]:
            for i, w in enumerate(ways):
                if w[0] == r[-1]: r += w[1:]; break
                if w[-1] == r[-1]: r += w[::-1][1:]; break
                if w[-1] == r[0]: r = w + r[1:]; break
                if w[0] == r[0]: r = w[::-1] + r[1:]; break
            else: break
            ways.pop(i)
        out.append(r)
    return out

water, rivers_main, rivers_small, roads = [], [], [], []
for e in d["elements"]:
    t = e.get("tags", {})
    if e["type"] == "way":
        g = geom(e["geometry"])
        if t.get("highway") == "motorway": roads.append(path(g))
        elif t.get("waterway") == "river": (rivers_main if t.get("name") == "Tisza" else rivers_small).append(path(g))
        elif g[0] == g[-1]: water.append(path(g, True))
    else:
        ws = [[(p["lat"], p["lon"]) for p in m["geometry"]] for m in e["members"] if m["type"] == "way" and "geometry" in m]
        for r in rings(ws):
            if len(r) > 2: water.append(path([P(a, b) for a, b in r], True))

TOWNS = [("Miskolc", 48.1035, 20.7784, "end", -14, 6), ("Mezőkövesd", 47.8070, 20.5770, "start", 14, 6),
         ("Tiszaújváros", 47.9300, 21.0700, "start", 14, 6), ("Tiszafüred", 47.6190, 20.7600, "start", 16, 10),
         ("Tiszacsege", 47.6990, 21.0000, "start", 14, 18), ("Hortobágy", 47.5850, 21.1500, "end", -14, 6)]
AX, AY = P(47.7308, 20.9423)

svg = [f'<svg class="map-svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="map-title">',
       '<title id="map-title">Ároktő elhelyezkedése: a Tisza jobb partján, Miskolctól délre, a Tisza-tó és Hortobágy közelében</title>',
       f'<rect width="{W}" height="{H}" class="m-bg"/>',
       f'<path class="m-road" d="{" ".join(roads)}"/>',
       f'<path class="m-water" fill-rule="evenodd" d="{" ".join(water)}"/>',
       f'<path class="m-river-s" d="{" ".join(rivers_small)}"/>',
       f'<path class="m-river" d="{" ".join(rivers_main)}"/>']
for name, lat, lon, anchor, dx, dy in TOWNS:
    x, y = P(lat, lon)
    svg.append(f'<circle class="m-town" cx="{x:.0f}" cy="{y:.0f}" r="6"/><text class="m-label" x="{x+dx:.0f}" y="{y+dy:.0f}" text-anchor="{anchor}">{name}</text>')
tx, ty = P(47.585, 20.585)
svg.append(f'<text class="m-water-label" x="{tx:.0f}" y="{ty:.0f}" text-anchor="middle">Tisza-tó</text>')
rx, ry = P(47.86, 21.035)
svg.append(f'<text class="m-water-label" x="{rx:.0f}" y="{ry:.0f}" transform="rotate(-62 {rx:.0f} {ry:.0f})">Tisza</text>')
svg.append(f'<g class="m-pin" transform="translate({AX:.0f} {AY:.0f})"><circle class="m-pulse" r="18"/><circle class="m-halo" r="26"/><circle class="m-dot" r="13"/>'
           f'<text class="m-place" x="-30" y="12" text-anchor="end">Ároktő</text></g>')
svg.append("</svg>")
out = "\n".join(svg)
open(r"D:\Letolt\liget\_proba\map.svg", "w", encoding="utf-8").write(out)
open(r"D:\Letolt\liget\_proba\map.txt", "w").write(f"{W}x{H} {len(out)//1024}KB water={len(water)} roads={len(roads)}")
