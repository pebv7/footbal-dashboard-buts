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

CSS aliases `--amber` / `--blue` / `--rose` / `--mint` kept for JS `colour()`. Prefer Stitch **Neutral Core** overrides (`#0B0F17` canvas, `#10B981` Pitch Emerald) over Material mint/olive namedColors (`#4edea3` / `#bbcabf`), which read muddy on this shell.

### Dark (primary)
- Canvas / rail: `#0B0F17`
- Cards: `#111827`; hover / inset: `#1E293B`
- Text: `#F8FAFC` / muted `#94A3B8` / dim `#64748B`
- Primary Pitch Emerald: `#10B981` (Over, selection, live)
- Secondary Kinetic Amber: `#F59E0B` (outliers, BTTS highlight, MA)
- Tertiary Cool Cyan: `#06B6D4` (away / cool metrics)
- Under / destructive: `#EF4444`
- Tint: `rgba(16,185,129,.12)`; hairline `rgba(148,163,184,.12)`

### Light
- Cool slate neutrals; emerald `#059669`; cyan `#0891B2`; crimson under; amber-warn secondary.

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
