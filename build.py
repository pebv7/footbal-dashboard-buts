#!/usr/bin/env python3
"""Injecte data.json dans template.html et écrit index.html.

Le template contient le marqueur __SNAP__, remplacé par la copie embarquée
qui sert de secours quand le navigateur n'a pas accès à ESPN.
"""
import json, pathlib, datetime, re, unicodedata

RACINE = pathlib.Path(__file__).parent
LABELS_COUPES = ["League MD1","League MD2","League MD3","League MD4","League MD5","League MD6","League MD7","League MD8",
                 "Play-offs 1","Play-offs 2","Round of 16","Quarter-finals","Semi-finals","Final"]
TOTAL = {"fr.1":306,"en.1":380,"es.1":380,"de.1":306,"it.1":380,
         "pt.1":306,"nl.1":306,"tr.1":306,"cl":189,"el":189,"unl":200}


def agreger(matchs):
    """Statistiques de saison sur une liste [md, date, heure, dom, ext, bd, be, minutes]."""
    n = len(matchs)
    if n < 2:
        return None
    tot = sum(m[5] + m[6] for m in matchs)
    moy = tot / n
    var = sum((m[5] + m[6] - moy) ** 2 for m in matchs) / (n - 1)
    p = lambda f: round(100 * sum(1 for m in matchs if f(m)) / n, 2)
    return dict(n=n, goals=tot, avg=round(moy, 4), sd=round(var ** 0.5, 4),
                ggp=p(lambda m: m[5] > 0 and m[6] > 0), ngp=p(lambda m: m[5] == 0 or m[6] == 0),
                o05=p(lambda m: m[5]+m[6] > 0.5), u05=p(lambda m: m[5]+m[6] < 0.5),
                o15=p(lambda m: m[5]+m[6] > 1.5), u15=p(lambda m: m[5]+m[6] < 1.5),
                o25=p(lambda m: m[5]+m[6] > 2.5), u25=p(lambda m: m[5]+m[6] < 2.5),
                o35=p(lambda m: m[5]+m[6] > 3.5), u35=p(lambda m: m[5]+m[6] < 3.5),
                hw=p(lambda m: m[5] > m[6]), dr=p(lambda m: m[5] == m[6]),
                aw=p(lambda m: m[5] < m[6]), nil=p(lambda m: m[5]+m[6] == 0))


def par_club(matchs):
    T = {}
    for m in matchs:
        tot = m[5] + m[6]
        for cote, bp, bc in ((m[3], m[5], m[6]), (m[4], m[6], m[5])):
            s = T.setdefault(cote, dict(p=0, gf=0, ga=0, gg=0, o15=0, o25=0, o35=0, cs=0, w=0, d=0))
            s["p"] += 1; s["gf"] += bp; s["ga"] += bc
            if m[5] > 0 and m[6] > 0: s["gg"] += 1
            if tot > 1.5: s["o15"] += 1
            if tot > 2.5: s["o25"] += 1
            if tot > 3.5: s["o35"] += 1
            if bc == 0: s["cs"] += 1
            if bp > bc: s["w"] += 1
            elif bp == bc: s["d"] += 1
    out = {}
    for k, v in T.items():
        n = v["p"]; r = lambda x: round(100 * x / n, 2)
        out[k] = [n, v["w"] * 3 + v["d"], v["gf"], v["ga"], round((v["gf"] + v["ga"]) / n, 4),
                  r(v["gg"]), r(v["o15"]), r(v["o25"]), r(v["o35"]), r(v["cs"])]
    return out


def main():
    data = json.loads((RACINE / "data.json").read_text(encoding="utf-8"))
    ancien = {}
    p_ancien = RACINE / "historique.json"          # saison précédente, optionnel
    if p_ancien.exists():
        ancien = json.loads(p_ancien.read_text(encoding="utf-8"))

    snap = {"_date": datetime.date.today().isoformat(), "_source": "ESPN",
            "_genere": data.get("_genere")}
    for code, v in data.get("competitions", {}).items():
        matchs = v.get("matchs") or []
        if not matchs:
            continue
        e = {"name": v.get("nom", code), "total": TOTAL.get(code, len(matchs)), "m": matchs,
             "u": v.get("a_venir") or []}
        if code in ("cl", "el"):
            e["labels"] = LABELS_COUPES
        h = (ancien.get("competitions") or {}).get(code)
        if h and h.get("matchs"):
            e["prev"] = agreger(h["matchs"])
            e["prevTeams"] = par_club(h["matchs"])
            e["prevName"] = f"{v.get('nom', code)} 2025/26"
        else:
            e["prev"] = None; e["prevTeams"] = {}
        snap[code] = e

    modele = (RACINE / "template.html").read_text(encoding="utf-8")
    if "__SNAP__" not in modele:
        raise SystemExit("template.html ne contient pas le marqueur __SNAP__")
    sortie = modele.replace("__SNAP__", json.dumps(snap, ensure_ascii=False, separators=(",", ":")))
    (RACINE / "index.html").write_text(sortie, encoding="utf-8")
    total = sum(len(v["m"]) for k, v in snap.items() if isinstance(v, dict) and "m" in v)
    print(f"index.html écrit : {len(sortie)//1024} Ko, {total} matchs embarqués")

    lastmod = snap["_date"]
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://www.matchfreq.com/?lang=en</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.matchfreq.com/?lang=en"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://www.matchfreq.com/?lang=fr"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.matchfreq.com/?lang=en"/>
  </url>
  <url>
    <loc>https://www.matchfreq.com/?lang=fr</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://www.matchfreq.com/?lang=en"/>
    <xhtml:link rel="alternate" hreflang="fr" href="https://www.matchfreq.com/?lang=fr"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="https://www.matchfreq.com/?lang=en"/>
  </url>
</urlset>
'''
    (RACINE / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"sitemap.xml écrit : lastmod={lastmod}")


if __name__ == "__main__":
    main()
