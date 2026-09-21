#!/usr/bin/env python3
"""Récupère les résultats ESPN des compétitions suivies et écrit data.json.
Aucune dépendance externe : bibliothèque standard uniquement."""
import json, urllib.request, datetime, zoneinfo, pathlib

PARIS = zoneinfo.ZoneInfo("Europe/Paris")
SAISON_DEBUT = "20260701"
BASE = "https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={a}-{b}&limit=1000"

COMPETITIONS = {
    "fr.1": "fra.1", "en.1": "eng.1", "es.1": "esp.1", "de.1": "ger.1",
    "it.1": "ita.1", "pt.1": "por.1", "nl.1": "ned.1", "tr.1": "tur.1",
    "cl": "uefa.champions", "el": "uefa.europa",
}

def recuperer(slug):
    fin = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y%m%d")
    url = BASE.format(slug=slug, a=SAISON_DEBUT, b=fin)
    req = urllib.request.Request(url, headers={"User-Agent": "dashboard-buts/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def matchs_termines(payload):
    """-> [date, heure_paris, domicile, exterieur, buts_dom, buts_ext, [minutes_buts]]"""
    sortie = []
    for ev in payload.get("events", []):
        comp = (ev.get("competitions") or [None])[0]
        if not comp:
            continue
        statut = (comp.get("status") or {}).get("type") or {}
        if not statut.get("completed"):
            continue
        equipes = comp.get("competitors") or []
        dom = next((c for c in equipes if c.get("homeAway") == "home"), None)
        ext = next((c for c in equipes if c.get("homeAway") == "away"), None)
        if not dom or not ext or dom.get("score") is None or ext.get("score") is None:
            continue
        try:
            quand = datetime.datetime.fromisoformat(
                (comp.get("date") or ev["date"]).replace("Z", "+00:00")).astimezone(PARIS)
        except Exception:
            continue
        minutes = []
        for d in comp.get("details") or []:
            if not d.get("scoringPlay"):
                continue
            h = (d.get("clock") or {}).get("displayValue")
            if not h:
                continue
            chiffres = "".join(ch for ch in str(h) if ch.isdigit())[:3]
            if chiffres:
                minutes.append(int(chiffres[:2] if len(chiffres) > 2 else chiffres))
        sortie.append([quand.strftime("%Y-%m-%d"), quand.strftime("%H:%M"),
                       dom["team"]["displayName"], ext["team"]["displayName"],
                       int(dom["score"]), int(ext["score"]), minutes])
    sortie.sort(key=lambda m: (m[0], m[1]))
    return sortie

def journees(matchs):
    """Reconstitue le numéro de journée : n-ième match de chaque équipe."""
    compteur, resultat = {}, []
    for m in matchs:
        n = max(compteur.get(m[2], 0), compteur.get(m[3], 0)) + 1
        compteur[m[2]] = compteur[m[3]] = n
        resultat.append([n] + m)
    return resultat

def main():
    data = {"_genere": datetime.datetime.now(PARIS).isoformat(timespec="seconds"),
            "_source": "ESPN", "competitions": {}}
    for code, slug in COMPETITIONS.items():
        try:
            payload = recuperer(slug)
            matchs = journees(matchs_termines(payload))
            nom = (payload.get("leagues") or [{}])[0].get("name") or code
            total = len(payload.get("events") or [])
            data["competitions"][code] = {"nom": nom, "total_programme": total, "matchs": matchs}
            buts = sum(m[5] + m[6] for m in matchs)
            moy = round(buts / len(matchs), 2) if matchs else 0
            print(f"{code:6} {nom[:34]:34} {len(matchs):3} matchs  {moy} buts/match")
        except Exception as e:
            print(f"{code:6} ECHEC : {e}")
            data["competitions"][code] = {"nom": code, "erreur": str(e), "matchs": []}
    pathlib.Path("data.json").write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    total = sum(len(c["matchs"]) for c in data["competitions"].values())
    print(f"\ndata.json écrit : {total} matchs sur {len(COMPETITIONS)} compétitions")

if __name__ == "__main__":
    main()
