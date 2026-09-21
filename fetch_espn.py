#!/usr/bin/env python3
"""Récupère les résultats ESPN des compétitions suivies et écrit data.json.
Aucune dépendance externe : bibliothèque standard uniquement."""
import json, urllib.request, datetime, zoneinfo, pathlib, time

PARIS = zoneinfo.ZoneInfo("Europe/Paris")
SAISON_DEBUT = datetime.date(2026, 7, 1)

# site.api.espn.com est souvent en 403 (Akamai). site.web.api accepte
# un jour à la fois ; une plage dates=A-B renvoie 400.
SCOREBOARD = [
    "https://site.web.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={d}",
    "https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={d}",
]
CALENDRIER = [
    "https://sports.core.api.espn.com/v2/sports/soccer/leagues/{slug}/calendar/ondays",
]

ENTETES = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Referer": "https://www.espn.com/",
}

COMPETITIONS = {
    "fr.1": "fra.1", "en.1": "eng.1", "es.1": "esp.1", "de.1": "ger.1",
    "it.1": "ita.1", "pt.1": "por.1", "nl.1": "ned.1", "tr.1": "tur.1",
    "cl": "uefa.champions", "el": "uefa.europa",
}

def lire_json(url):
    req = urllib.request.Request(url, headers=ENTETES)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

def essayer(modeles, **params):
    """Essaie chaque URL, avec une relance. Lève la dernière erreur si tout échoue."""
    derniere = None
    for modele in modeles:
        url = modele.format(**params)
        for essai in range(2):
            try:
                return lire_json(url)
            except Exception as e:
                derniere = e
                time.sleep(1 * (essai + 1))
    raise derniere

def extraire_jours(valeur, limite):
    """Normalise les dates de calendrier ESPN (chaînes ISO ou structures imbriquées)."""
    jours = set()
    if isinstance(valeur, str) and len(valeur) >= 10:
        try:
            d = datetime.date.fromisoformat(valeur[:10])
        except ValueError:
            return jours
        if SAISON_DEBUT <= d <= limite:
            jours.add(d)
        return jours
    if isinstance(valeur, dict):
        dates = valeur.get("dates")
        if isinstance(dates, list) and dates and isinstance(dates[0], str):
            return extraire_jours(dates, limite)
        event_date = valeur.get("eventDate")
        if isinstance(event_date, dict):
            trouves = extraire_jours(event_date, limite)
            if trouves:
                return trouves
        for cle in ("calendar", "entries", "items"):
            if cle in valeur:
                jours |= extraire_jours(valeur[cle], limite)
        return jours
    if isinstance(valeur, list):
        for item in valeur:
            jours |= extraire_jours(item, limite)
    return jours

def jours_matchs(slug, limite):
    try:
        cal = essayer(CALENDRIER, slug=slug)
        jours = extraire_jours(cal, limite)
        if jours:
            return sorted(jours)
    except Exception:
        pass
    payload = essayer(SCOREBOARD, slug=slug, d=limite.strftime("%Y%m%d"))
    jours = extraire_jours((payload.get("leagues") or [{}])[0].get("calendar"), limite)
    if not jours:
        jours = {limite - datetime.timedelta(days=i) for i in range(16)}
    return sorted(jours)

def recuperer(slug):
    """Agrège le scoreboard de chaque jour de match déjà joué (ou prévu demain)."""
    limite = datetime.datetime.now(PARIS).date() + datetime.timedelta(days=1)
    jours = jours_matchs(slug, limite)
    fusion = {"leagues": [], "events": []}
    vus = set()
    derniere = None
    for jour in jours:
        try:
            payload = essayer(SCOREBOARD, slug=slug, d=jour.strftime("%Y%m%d"))
        except Exception as e:
            derniere = e
            continue
        if payload.get("leagues") and not fusion["leagues"]:
            fusion["leagues"] = payload["leagues"]
        for ev in payload.get("events") or []:
            ident = ev.get("id") or ev.get("uid")
            if ident:
                if ident in vus:
                    continue
                vus.add(ident)
            fusion["events"].append(ev)
    if not fusion["events"] and not fusion["leagues"]:
        raise derniere or RuntimeError(f"aucune journée récupérée pour {slug}")
    return fusion

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

def total_ok(data):
    return sum(len(c.get("matchs", [])) for c in data["competitions"].values()) > 0

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
    if total_ok(data):
        pathlib.Path("data.json").write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    total = sum(len(c["matchs"]) for c in data["competitions"].values())
    echecs = sum(1 for c in data["competitions"].values() if c.get("erreur"))
    print(f"\ndata.json écrit : {total} matchs, {echecs} compétition(s) en échec")
    if total == 0:
        print("ECHEC TOTAL : aucune donnée récupérée, data.json non écrasé")
        raise SystemExit(1)

if __name__ == "__main__":
    main()
