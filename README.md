# MatchFreq

Pre-match goal-frequency research for Europe’s top leagues — Over 1.5 / 2.5 / 3.5 and BTTS as **historical frequencies** from completed matches.

**FR:** Recherche de fréquences de buts avant match sur les grands championnats européens — fréquences historiques sur matchs terminés.

**Production (AWS CloudFront):** [https://www.matchfreq.com](https://www.matchfreq.com)

Brand domain: **www.matchfreq.com** — see [`infra/HOSTING.md`](infra/HOSTING.md).

## Pipeline

```
fetch_espn.py   ESPN scoreboard API  -> data.json
build.py        inject into template -> index.html
GitHub Actions  daily fetch + build + S3 sync + CloudFront invalidate
AWS             S3 (private) + CloudFront (OAC) serves the site
```

On load, the page may also query ESPN from the browser. The embedded snapshot is a fallback when the network fails.

## Local

```bash
python3 fetch_espn.py              # current season → data.json
# python3 fetch_espn.py --historique  # also refresh historique.json (slow)
python3 build.py
# open index.html, or: python3 -m http.server 8000
```

## Custom domain (matchfreq.com)

1. Buy `matchfreq.com`.
2. ACM certificate in **us-east-1**, attach to the CloudFront distribution.
3. Point DNS at CloudFront; set `SITE_ORIGIN` to `https://www.matchfreq.com` in `template.html`, rebuild, deploy.
4. Full checklist: [`infra/HOSTING.md`](infra/HOSTING.md).

Shareable state uses query params, e.g. `?lang=fr&league=fr.1&market=o25&view=fixtures`.

## Files

| File | Role |
|---|---|
| `fetch_espn.py` | current season from ESPN (`--historique` for previous season) |
| `build.py` | merges `data.json` into `template.html` |
| `template.html` | app source (`__SNAP__` marker) |
| `index.html` | build output — **do not edit by hand** |
| `data.json` | daily ESPN snapshot |
| `historique.json` | optional previous season |
| `robots.txt` / `sitemap.xml` | crawl hints |
| `og.png` | Open Graph / Twitter image |
| `infra/matchfreq-site.yaml` | CloudFormation (S3 + CloudFront + OIDC role) |

## Notes

- GitHub disables scheduled workflows after 60 days of inactivity — any commit resets the clock.
- ESPN’s API is undocumented; if it breaks, the UI stays on the embedded copy.
- Deploy uses GitHub Actions with an IAM user (`matchfreq-ci`) stored as repository secrets `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`. An OIDC role also exists in the CloudFormation stack for a future keyless migrate.
