# Goal Rates

Pre-match goal-rate research for Europe’s top leagues — Over 1.5 / 2.5 / 3.5 and BTTS as **historical frequencies** from completed matches.

**FR:** Recherche de taux de buts avant match sur les grands championnats européens — fréquences historiques sur matchs terminés.

Live: [https://pebv7.github.io/footbal-dashboard-buts/](https://pebv7.github.io/footbal-dashboard-buts/)

## Pipeline

```
fetch_espn.py   ESPN scoreboard API  -> data.json
build.py        inject into template -> index.html
GitHub Actions  daily fetch + build + publish
GitHub Pages    serves index.html (+ robots.txt, sitemap.xml, og.png)
```

On load, the page also queries ESPN from the browser. The embedded snapshot is a fallback when the network fails.

## Local

```bash
python3 fetch_espn.py              # current season → data.json
# python3 fetch_espn.py --historique  # also refresh historique.json (slow)
python3 build.py
# open index.html, or: python3 -m http.server 8000
```

## Custom domain (goalrates.com)

Preferred brand domain: **goalrates.com** (fallback: goalfreq.com, goalscope.com; FR: goalrates.fr / tauxbuts.fr).

1. Buy the domain at your registrar.
2. In the repo root, add a `CNAME` file with a single line:
   ```
   goalrates.com
   ```
3. GitHub → **Settings → Pages → Custom domain** → enter `goalrates.com` → enable **Enforce HTTPS**.
4. At the registrar, point DNS:
   - **Apex:** A records to GitHub Pages IPs (`185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`), or an ALIAS/ANAME to `pebv7.github.io`
   - **www (optional):** CNAME → `pebv7.github.io`
5. After the domain is live, update canonical / OG / sitemap / robots URLs in `template.html` and `sitemap.xml` / `robots.txt` from the `github.io` path to `https://goalrates.com/`. Keep `github.io` as a redirect only.
6. Optional: redirect `goalrates.fr` → `goalrates.com` (or `?lang=fr`).

Until the custom domain is attached, SEO tags and the sitemap point at the GitHub Pages URL.

Shareable state uses query params, e.g. `?lang=fr&league=fr.1&market=o25&view=fixtures` (old `#league/market/view` hashes still migrate).

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

## Notes

- GitHub disables scheduled workflows after 60 days of inactivity — any commit resets the clock.
- ESPN’s API is undocumented; if it breaks, the UI stays on the embedded copy.
- The repo must stay public for free GitHub Pages.
