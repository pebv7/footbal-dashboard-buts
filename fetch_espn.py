#!/usr/bin/env python3
"""Récupère les résultats ESPN des compétitions suivies.

Écrit data.json (saison en cours) et historique.json (saison précédente).
Aucune dépendance externe : bibliothèque standard uniquement."""
import json, urllib.request, datetime, zoneinfo, pathlib, time

PARIS = zoneinfo.ZoneInfo("Europe/Paris")
SAISON_COURANTE = datetime.date(2026, 7, 1)
SAISON_PREV_DEBUT = datetime.date(2025, 7, 1)
SAISON_PREV_FIN = datetime.date(2026, 6, 30)

# site.api.espn.com est souvent en 403 (Akamai). site.web.api accepte
# un jour à la fois ; une plage dates=A-B renvoie 400.
SCOREBOARD = [
    "https://site.web.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={d}",
    "https://site.api.espn.com/apis/site/v2/sports/soccer/{slug}/scoreboard?dates={d}",
]
CALENDRIER = [
    "https://sports.core.api.espn.com/v2/sports/soccer/leagues/{slug}/seasons/{year}/types/1/calendar/ondays",
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
    "cl": "uefa.champions", "el": "uefa.europa", "unl": "uefa.nations",
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

def extraire_jours(valeur, debut, limite):
    """Normalise les dates de calendrier ESPN (chaînes ISO ou structures imbriquées)."""
    jours = set()
    if isinstance(valeur, str) and len(valeur) >= 10:
        try:
            d = datetime.date.fromisoformat(valeur[:10])
        except ValueError:
            return jours
        if debut <= d <= limite:
            jours.add(d)
        return jours
    if isinstance(valeur, dict):
        dates = valeur.get("dates")
        if isinstance(dates, list) and dates and isinstance(dates[0], str):
            return extraire_jours(dates, debut, limite)
        event_date = valeur.get("eventDate")
        if isinstance(event_date, dict):
            trouves = extraire_jours(event_date, debut, limite)
            if trouves:
                return trouves
        for cle in ("calendar", "entries", "items"):
            if cle in valeur:
                jours |= extraire_jours(valeur[cle], debut, limite)
        return jours
    if isinstance(valeur, list):
        for item in valeur:
            jours |= extraire_jours(item, debut, limite)
    return jours

def jours_matchs(slug, debut, limite):
    year = debut.year
    try:
        cal = essayer(CALENDRIER, slug=slug, year=year)
        jours = extraire_jours(cal, debut, limite)
        if jours:
            return sorted(jours)
    except Exception:
        pass
    try:
        payload = essayer(SCOREBOARD, slug=slug, d=limite.strftime("%Y%m%d"))
        jours = extraire_jours((payload.get("leagues") or [{}])[0].get("calendar"), debut, limite)
        if jours:
            return sorted(jours)
    except Exception:
        pass
    jours = {limite - datetime.timedelta(days=i) for i in range(16)
             if debut <= limite - datetime.timedelta(days=i)}
    return sorted(jours)

def recuperer(slug, debut, limite):
    """Agrège le scoreboard de chaque jour de match dans [debut, limite]."""
    jours = jours_matchs(slug, debut, limite)
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

def matchs_termines(payload, debut, limite):
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
        jour = quand.date()
        if jour < debut or jour > limite:
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

def matchs_a_venir(payload, debut, limite):
    """-> [date, heure_paris, domicile, exterieur] pour les matchs pas encore commencés."""
    sortie = []
    for ev in payload.get("events", []):
        comp = (ev.get("competitions") or [None])[0]
        if not comp:
            continue
        statut = (comp.get("status") or {}).get("type") or {}
        if statut.get("state") != "pre" or statut.get("completed"):
            continue
        equipes = comp.get("competitors") or []
        dom = next((c for c in equipes if c.get("homeAway") == "home"), None)
        ext = next((c for c in equipes if c.get("homeAway") == "away"), None)
        if not dom or not ext:
            continue
        try:
            quand = datetime.datetime.fromisoformat(
                (comp.get("date") or ev["date"]).replace("Z", "+00:00")).astimezone(PARIS)
        except Exception:
            continue
        if quand.date() < debut or quand.date() > limite:
            continue
        sortie.append([quand.strftime("%Y-%m-%d"), quand.strftime("%H:%M"),
                       dom["team"]["displayName"], ext["team"]["displayName"]])
    sortie.sort(key=lambda m: (m[0], m[1]))
    return sortie

def prochaine_journee(slug, apres, horizon=45, largeur=3):
    """Matchs de la prochaine série de jours de match après `apres` (trêve, pause…)."""
    jours = [j for j in jours_matchs(slug, apres, apres + datetime.timedelta(days=horizon)) if j > apres]
    if not jours:
        return []
    debut = jours[0]
    fin = debut + datetime.timedelta(days=largeur)
    fusion = {"events": []}
    for jour in (j for j in jours if j <= fin):
        try:
            fusion["events"] += essayer(SCOREBOARD, slug=slug, d=jour.strftime("%Y%m%d")).get("events") or []
        except Exception:
            continue
    return matchs_a_venir(fusion, debut, fin)

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

def recuperer_saison(label, debut, limite, avenir_depuis=None):
    data = {"_genere": datetime.datetime.now(PARIS).isoformat(timespec="seconds"),
            "_source": "ESPN", "competitions": {}}
    print(f"\n=== {label} ({debut} → {limite}) ===")
    for code, slug in COMPETITIONS.items():
        try:
            payload = recuperer(slug, debut, limite)
            matchs = journees(matchs_termines(payload, debut, limite))
            nom = (payload.get("leagues") or [{}])[0].get("name") or code
            total = len(payload.get("events") or [])
            data["competitions"][code] = {"nom": nom, "total_programme": total, "matchs": matchs}
            a_venir = []
            if avenir_depuis:
                a_venir = matchs_a_venir(payload, avenir_depuis, limite)
                if not a_venir:
                    a_venir = prochaine_journee(slug, limite)
                data["competitions"][code]["a_venir"] = a_venir
            buts = sum(m[5] + m[6] for m in matchs)
            moy = round(buts / len(matchs), 2) if matchs else 0
            print(f"{code:6} {nom[:34]:34} {len(matchs):3} matchs  {moy} buts/match  {len(a_venir)} à venir")
        except Exception as e:
            print(f"{code:6} ECHEC : {e}")
            data["competitions"][code] = {"nom": code, "erreur": str(e), "matchs": []}
    return data

def ecrire(path, data, obligatoire=True):
    total = sum(len(c["matchs"]) for c in data["competitions"].values())
    echecs = sum(1 for c in data["competitions"].values() if c.get("erreur"))
    if total_ok(data):
        pathlib.Path(path).write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"\n{path} écrit : {total} matchs, {echecs} compétition(s) en échec")
        return True
    print(f"\n{path} non écrit : {total} matchs, {echecs} échec(s)")
    if obligatoire and total == 0:
        return False
    return total > 0

def main():
    import argparse
    p = argparse.ArgumentParser(description="Récupère les résultats ESPN des compétitions suivies.")
    p.add_argument("--historique", action="store_true",
                   help="Aussi régénérer historique.json (saison précédente ; lent).")
    args = p.parse_args()

    aujourdhui = datetime.datetime.now(PARIS).date()
    limite_courante = aujourdhui + datetime.timedelta(days=7)
    courant = recuperer_saison("saison en cours", SAISON_COURANTE, limite_courante,
                               avenir_depuis=aujourdhui)
    if not ecrire("data.json", courant, obligatoire=True):
        print("ECHEC TOTAL : aucune donnée courante, data.json non écrasé")
        raise SystemExit(1)

    if args.historique:
        precedent = recuperer_saison("saison 2025/26", SAISON_PREV_DEBUT, SAISON_PREV_FIN)
        if not ecrire("historique.json", precedent, obligatoire=False):
            print("AVERTISSEMENT : historique.json non mis à jour (saison précédente vide)")
    else:
        print("\nHistorique inchangé (passe --historique pour le régénérer).")

if __name__ == "__main__":
    main()
