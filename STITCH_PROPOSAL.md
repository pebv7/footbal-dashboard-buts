# Goal Rates — Stitch UX proposal

Mocks-only pass (evolve Goal Rates slate + amber). **Live `template.html` unchanged.**

## Stitch project

| | |
|---|---|
| **Title** | Goal Rates — UX proposal |
| **Project ID** | `5170020727712277226` |
| **Design system** | `assets/14547378215595196146` (Goal Rates: dark slate, amber `#E8A33D`, pos green `#7DCF8A`, Inter, round 8) |
| **Open** | [Stitch](https://stitch.withgoogle.com/) → project **Goal Rates — UX proposal** |

### Screens generated

| Screen | ID | Local preview |
|--------|-----|---------------|
| Mobile Fixtures | `0a62ae52cf2a41dfbbe555c89e39fc2a` | [`stitch-proposal/mobile-fixtures.png`](stitch-proposal/mobile-fixtures.png) |
| Desktop League (Ligue 1) | `fd1afa8842df4f38a2c6231cb698bdb5` | [`stitch-proposal/desktop-league.png`](stitch-proposal/desktop-league.png) |
| Desktop Clubs + drawer | `0d5a3dccc2ea49bb9eb2f3679b2b1ebd` | [`stitch-proposal/desktop-clubs.png`](stitch-proposal/desktop-clubs.png) |
| Desktop Fixtures | (session refine; open in Stitch canvas) | — |

## UX thesis (unchanged)

Primary job: **spot high/low goal-rate fixtures**, then drill into league/club context.

1. Compact mast → sticky filter bar → data.
2. Filter hierarchy: leagues → line markets + Over|Under → view.
3. Plain labels, sample sizes, labelled average tick, amber accent on top rates.
4. Honesty: historical frequencies from completed matches — no tipster framing.

## What Stitch got right (adopt in a future code pass)

- **Clubs master–detail**: table + selected-row amber edge + side drawer (home/away bars, last-N vs line, next fixture combined). Stronger than the current sheet-only pattern.
- **League KPI focus**: one market card visually primary (amber border) while companions stay quieter.
- **Mobile card stack**: kickoff + clubs + domicile/extérieur + combiné bar + vs moyenne badge; bottom tabs preserved.
- **FR microcopy on mobile**: Domicile / Extérieur / Combiné / vs moyenne — aligns with the clarity pass.
- **Brand consistency**: dark slate ground, amber selection, muted green for above-ref — not the mint “odds terminal” zip.

## What to reject or tame (Stitch drift)

Do **not** port these without editing:

- **“Analytics Terminal” / Export Data / Corners market** — tipster–trading tone; out of brand.
- **Goals-per-match bars as primary fixture metric** — our product is **hit rates** for +1.5/+2.5/+3.5/BTTS, not expected goals on a 0–5 axis.
- **`<1.5 Goals` as default chip** and **All Leagues** aggregator — keep single-competition focus + `+1.5 / +2.5 / +3.5 / BTTS` + Over|Under.
- **Nav rename** (Matrix, Methodology as top tabs) — keep Fixtures / League / Clubs / Compare + collapsed Method.
- **Season toggle in global chrome** — keep season on Clubs only (this season vs prev).

## Keep from the live app

- Query URL state (`lang`, `league`, `market`, `view`).
- Over|Under side toggle; BTTS disables Under.
- Combined = mean(home@home, away@away); tick = league average for the selected market key.
- Small-sample dimming (n &lt; 6) and honesty copy without tip negation.
- Compact mast (~160 / ~120) already shipped in the clarity pass.

## Recommended next implement slice (when you say go)

1. Clubs drawer layout inspired by Stitch (reuse live data/`openClub`).
2. League KPI “primary market” card emphasis.
3. Mobile fixture card spacing/hierarchy polish (labels already cleared).
4. Skip Stitch’s Export / Corners / terminal chrome.

## Files

- Screenshots: [`stitch-proposal/`](stitch-proposal/)
- Design tokens source: [`DESIGN.md`](DESIGN.md)
