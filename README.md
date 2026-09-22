# Dashboard des marchés de buts

Suivi des statistiques de buts sur dix compétitions : moyennes par journée, GG/NG,
seuils over/under, répartition des minutes de but, comparaison entre championnats.

## Comment ça marche

```
fetch_espn.py   interroge l'API ESPN         -> data.json
build.py        injecte data.json            -> index.html
GitHub Actions  enchaîne les deux, une fois par jour, et publie
GitHub Pages    sert index.html
```

Une fois en ligne, le dashboard interroge **lui-même** ESPN à chaque ouverture :
les données affichées sont donc celles du moment, pas celles du dernier build.
La copie embarquée dans `index.html` n'est qu'un secours si le réseau échoue.

## Mise en route

### En local

```bash
python3 fetch_espn.py
python3 build.py
# ouvrir index.html, ou : python3 -m http.server 8000
```

### En ligne (GitHub Pages)

1. Déposer à la racine : `fetch_espn.py`, `build.py`, `template.html`
2. Déposer `update.yml` dans `.github/workflows/`
3. **Settings → Pages → Source : Deploy from a branch → main / (root)**
4. Onglet **Actions**, lancer « Mise à jour des résultats » à la main

Dashboard : [https://pebv7.github.io/footbal-dashboard-buts/](https://pebv7.github.io/footbal-dashboard-buts/)

## Fichiers

| Fichier | Rôle |
|---|---|
| `fetch_espn.py` | récupère les matchs terminés, avec les minutes de but |
| `build.py` | fusionne `data.json` dans `template.html` |
| `template.html` | le dashboard, avec le marqueur `__SNAP__` |
| `index.html` | résultat du build, servi par Pages — **ne pas modifier à la main** |
| `data.json` | données ESPN brutes, régénérées une fois par jour |
| `historique.json` | optionnel : même format, saison précédente, pour les comparaisons |

## Points de vigilance

- **GitHub désactive les workflows planifiés après 60 jours sans activité** sur le dépôt.
  Un commit quelconque relance le compteur.
- L'API ESPN n'est pas documentée. Si elle change, le dashboard cesse de se mettre à
  jour sans message d'erreur. Le bandeau reste bloqué sur « copie ESPN du … » au lieu
  d'afficher « ESPN en direct » : c'est le signal d'alerte.
- Le dépôt doit rester public pour que Pages le serve gratuitement.
