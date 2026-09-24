# Terminal V4.2 — Goal Markets

Dense multi-league goal-markets dashboard. Visual shell aligned with Stitch **Football Dashboard Redesign** / **Apex Pitch & Odds Terminal** (sidebar, status chrome, section tabs, Material surfaces). Data and section logic stay on the ESPN pipeline — **no bet-slip, fair-odds, DEC/FRAC odds, Simulate MD, or radar club charts**.

## Atmosphere

Institutional terminal: pitch-dark canvas, tonal slate panels, emerald signal. Analytical and dense. Avoid purple gradients, cream editorial themes, and decorative glow.

## Shell layout

- **Rail** (256px, fixed left): brand `TERMINAL V4.2` / `GOAL MARKETS`, competition list (active emerald + pulse), Market Scope (season + round, read-only), Data Feed footer (ESPN + stamp).
- **Chrome** (sticky): Live data chip, `ESPN API · Paris (CET)`, Refresh, theme toggle.
- **Subnav** (sticky under chrome): Overview & Markets, Matchday Trends, All Matchdays, Kick-offs, Clubs, Minutes, Leagues (+ Live when matches in progress). Micro KPIs (Avg / BTTS / Over 2.5) from ≥1100px.
- **Canvas**: full remaining width (no 1080px cap). Mobile: rail off-canvas via menu + scrim; bottom nav Live / Stats / Compare.

## Color

CSS aliases `--amber` / `--blue` / `--rose` / `--mint` kept for JS `colour()`.

### Dark (primary)
- Canvas / lowest: `#0f131c` / `#0a0e16`
- Surfaces: `#181c24` / `#1c2028` / `#262a33`
- Text: `#dfe2ee` / muted `#bbcabf` / dim `#86948a`
- Primary emerald: `#4edea3` (signal), fill `#10b981`
- Secondary amber: `#ffb95f` (outliers, peaks, MA line)
- Tertiary cyan: `#4cd7f6` (away / cool)
- Under / destructive: `#EF4444` (`--rose` — Over/Under pair Under side)
- Tint: `rgba(16,185,129,.12)`; hairline `rgba(148,163,184,.12)`

### Light
- Slate neutrals; emerald primary; cyan tertiary; crimson under; amber-warn secondary.

### Pair bars
- Over → emerald (`--amber`)
- Under → crimson (`--rose`)
- 1X2: home crimson, draw dim, away cyan

## Typography

- Inter for UI / section titles
- JetBrains Mono for KPIs, clocks, table metrics, micro labels (`tnum` + `zero`)
- Label-caps: ~10px, tracking 0.08em, uppercase

## Shape

- Panels / tables: 12px radius; controls often 8px; pills only for interactive chips where needed
- Glass on chrome only (`backdrop-filter: blur(12px)`), not on scrolling tables

## Out of scope

Do not pull from Stitch: DEC/FRAC/AMER toggles, fair vs implied odds, Asian handicap, Simulate MD, bet-slip drawer, Poisson badges, user avatar, attack/defense radar.

## Interaction

- Emerald `aria-current` / `aria-pressed` / focus ring 2px
- Live chip pulses when matches in progress
- Respect `prefers-reduced-motion`
- English UI; kick-offs in Europe/Paris
