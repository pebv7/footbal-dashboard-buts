# Contexte du projet — à lire avant toute modification

Document de passation. Il décrit l'état du projet, les décisions prises et surtout
**les impasses déjà explorées**, pour éviter de les refaire.

---

## 1. Ce que fait le projet

Un dashboard d'analyse des **marchés de buts** au football, sur dix compétitions.
Il sert à préparer des paris de type « moins de N,5 buts » : moyennes de buts par
journée, taux GG/NG, seuils over/under, répartition des minutes de but, comparaison
entre championnats.

L'utilisateur parie en direct, généralement vers la 70ᵉ minute, avec un but de marge
par rapport au score en cours.

## 2. Architecture

```
fetch_espn.py    API ESPN  ──────────────►  data.json
build.py         data.json + template.html ►  index.html
update.yml       enchaîne les deux, chaque heure, commit + push
GitHub Pages     sert index.html
```

**Point essentiel** : `index.html` embarque une copie des données, mais le dashboard
**interroge ESPN lui-même** au chargement du navigateur et remplace tout. La copie
embarquée n'est qu'un secours pour le cas hors ligne.

| Fichier | Rôle |
|---|---|
| `template.html` | **le dashboard** — c'est ici qu'on développe. Contient le marqueur `__SNAP__` |
| `index.html` | produit du build. **Ne jamais éditer à la main**, écrasé chaque heure |
| `fetch_espn.py` | récupère les matchs terminés + les minutes de but |
| `build.py` | injecte les données dans le template |
| `data.json` | sortie brute d'ESPN |
| `historique.json` | optionnel, saison précédente, même format |

Aucune dépendance : bibliothèque standard Python, JavaScript vanilla, zéro build front.

## 3. Compétitions suivies

`fr.1 en.1 es.1 de.1 it.1 pt.1 nl.1 tr.1 cl el` mappées sur les slugs ESPN
`fra.1 eng.1 esp.1 ger.1 ita.1 por.1 ned.1 tur.1 uefa.champions uefa.europa`.

Moyennes constatées au 21/09/2026 (465 matchs) :

| Compétition | Buts/match | Buts après la 70ᵉ |
|---|---|---|
| Ligue Europa | 2,61 | 21,3 % |
| Primeira Liga | 2,74 | 32,4 % |
| Ligue 1 | 2,75 | 30,5 % |
| Premier League | 2,85 | 26,1 % |
| Süper Lig | 2,89 | 24,1 % |
| Serie A | 3,00 | 29,0 % |
| Liga | 3,05 | 32,8 % |
| Ligue des champions | 3,83 | 28,6 % |
| Bundesliga | 3,85 | 28,3 % |
| Eredivisie | 3,94 | 28,4 % |

## 4. Fonctionnalités du dashboard

- **En direct** : matchs en cours, score et minute, rafraîchi toutes les 60 s.
  Exclus des statistiques tant qu'ils ne sont pas terminés. Section masquée si vide.
- **Repères de saison** : les 15 indicateurs, groupés en paires complémentaires
  (+1,5 / −1,5 sur la même barre à 100 %). Cliquables pour tracer le graphique.
- **Par journée** : graphique avec une **bande de hasard** — l'intervalle où une
  journée tombe 19 fois sur 20 si rien ne change. Largeur adaptée au nombre de matchs
  du tour. Verdict textuel sous le graphique.
- **Tableau des journées** : 19 colonnes, 4 préréglages, tri sur tous les en-têtes,
  clic sur une ligne pour ouvrir les matchs. Tours incomplets marqués d'un point ambre.
- **Jours et horaires** : agrégats par jour de match et par créneau. **Toutes les
  heures sont converties en heure de Paris**, y compris Angleterre et Portugal.
- **Clubs** : trois vues (saison en cours / 2025/26 / écart), filtre de recherche.
- **Minutes** : répartition en 6 tranches de 15 min + part des buts après la 70ᵉ.
- **Championnats** : les 10 compétitions positionnées entre min et max sur 9 indicateurs,
  bascule over/under, tableau comparatif trié.
- Thème clair/sombre suivant le système, navigation collante, responsive mobile.

## 5. Impasses déjà explorées — ne pas refaire

| Piste | Verdict |
|---|---|
| **openfootball** (GitHub) | 5 à 10 jours de retard. Abandonné comme source principale. |
| **football-data.co.uk** | figé à la saison 2024/25. |
| **Flashscore** | page rendue en JS, aucun score dans le HTML. |
| **Flashscore lite** (`m.flashscore.fr`) | **fonctionne**, HTML pur, paramètres `?d=-1&s=3`. Mais liste toutes les compétitions du monde sur une page : impraticable en masse, utile pour une vérification ponctuelle. |
| **football-data.org** | gratuit, 12 championnats, **pas de xG**. |
| **Sportmonks** | xG en direct = add-on à 199-399 €/mois. Hors budget. |
| **TheStatsAPI** | 50 $/mois, xG + cotes annoncés. Piste à creuser si besoin de xG. |
| **Publication sur claude.ai** | les pages hébergées interdisent les requêtes vers d'autres sites : ESPN serait bloqué. |

## 6. Pièges techniques rencontrés

**ESPN renvoie 403** à un client sans en-têtes de navigateur. Il faut un `User-Agent`
Chrome complet, plus `Accept`, `Accept-Language` et `Referer`. C'est dans `fetch_espn.py`.

**ESPN renvoie 400** sur une plage de dates longue. D'où l'interrogation **mois par mois**
avec `?dates=AAAAMM`. Le script teste plusieurs variantes d'URL et retient celle qui marche.

**ESPN ne fournit pas le numéro de journée.** Il est reconstruit : le numéro est le
n-ième match de chaque équipe. Fragile en cas de report, acceptable en pratique.

**Les noms de clubs diffèrent** entre ESPN (« Lyon ») et openfootball (« Olympique
Lyonnais »). Si `historique.json` vient d'ESPN, le problème disparaît. Sinon il faut
une table de correspondance : recouvrement de jetons, puis inclusion de chaîne en
repli, avec contrainte d'unicité — sans quoi « Atlético Madrid » s'apparie à
« Real Madrid ».

**Pas de `localStorage`** dans le dashboard. Tout l'état vit en mémoire.

**GitHub désactive les workflows planifiés après 60 jours** sans activité sur le dépôt.

## 7. État connu et améliorations possibles

- `historique.json` n'existe pas encore : les vues « 2025/26 » et « Écart » sont vides.
  Le correctif propre est d'ajouter une passe sur la saison 2025/26 dans `fetch_espn.py`.
- Le dashboard ne lit pas `data.json` : il va directement à ESPN. Le lire en second
  recours rendrait le secours vieux d'une heure plutôt que du dernier build.
- **xG en direct** : non implémenté. ESPN expose un endpoint de détail par match
  (`/summary?event={id}`) qui contient le boxscore, mais une requête par rencontre.
  Faisable pour les 5-10 matchs en cours à un instant donné. Non vérifié : ce endpoint
  donne-t-il le xG pendant le match ou seulement après ?
- Les cotes sont exposées par ESPN (`/odds`), jamais exploitées.

## 8. Le second besoin, hors de ce dépôt

L'analyse de paris en direct à partir de captures d'écran fait l'objet d'un prompt
séparé (`prompt-analyse-live.md`). Elle partage la méthode statistique mais pas le code.

Méthode, en résumé : intensité du match = xG cumulé rapporté au temps joué, comparé
à la moyenne du championnat. En dessous de 60 %, match fermé. Au-dessus de 150 %, fuir.
Puis loi de Poisson sur les buts attendus d'ici la fin, et comparaison de la probabilité
obtenue au seuil imposé par la cote.

**Deux corrections issues d'erreurs mesurées** : appliquer un facteur 1,3 en fin de
match, car le modèle sous-estimait le rythme d'un facteur deux sur deux cas ; et
toujours calculer le rythme implicite des cotes pour se contrôler — un écart supérieur
à 30 % signale une erreur de modèle, pas une opportunité.

Si un jour le dashboard intègre le xG en direct, les deux besoins fusionnent : la
section « En direct » afficherait l'intensité et le seuil de pari de chaque match en cours.
