# Apex Pitch — Design System

Dense sports-data dashboard for live under-goal tracking. Visual language aligned with Stitch **Apex Pitch & Odds Terminal** (colors, type, denser terminal chrome). Product scope stays the existing section structure and ESPN pipeline — **no bet-slip, fair-odds, DEC/FRAC odds, or left-sidebar terminal IA**.

## Atmosphere

Dark terminal field, slate surfaces, emerald signal. Analytical and compact — broadcast-style panels without marketing chrome. Avoid purple gradients, cream editorial themes, amber-on-navy legacy look, glow effects, and decorative pill clusters.

## Color

CSS variable names (`--amber`, `--blue`, `--rose`, `--mint`) are kept for JS/`colour()` compatibility; values map to Apex roles.

### Dark mode (primary)
- **Field** `#0B0F17` — page background (`--bg`)
- **Surface** `#111827` — panels, tables, sticky chrome (`--surf`)
- **Inset** `#1E293B` — wells, tracks, hover (`--surf2`)
- **Hairline** `#1E293B` / `#334155` — borders (`--line` / `--line2`); panels also use `rgba(148,163,184,.12)`
- **Paper** `#F8FAFC` — primary text (`--txt`)
- **Muted / dim** `#94A3B8` / `#64748B` (`--mut` / `--dim`)
- **Signal emerald** `#10B981` — selection, Over, KPIs, focus, live pulse (`--amber`)
- **Cool cyan** `#06B6D4` — Under / away / cool metrics (`--blue`)
- **Crimson** `#EF4444` — home-win / high extremes (`--rose`)
- **Mint** `#4EDEA3` — GG / both-teams-scored (`--mint`)
- **Emerald tint** `rgba(16,185,129,.12)` — selected fills (`--emerald-tint`)

### Light mode
- Background `#F1F5F9`, surface `#FFFFFF`, inset `#E2E8F0`
- Lines `#CBD5E1` / `#94A3B8`
- Text `#0F172A`, muted `#475569`, dim `#64748B`
- Emerald `#059669`, cyan `#0891B2`, crimson `#DC2626`, mint `#047857`
- Tint `rgba(5,150,105,.12)`

### Pair bars
- **Over** → emerald (`--amber`)
- **Under** → cyan (`--blue`)
- 1X2: home crimson, draw dim, away cyan

## Typography

- **Body / UI**: Inter, ~14px body, 12–13px helpers.
- **Numbers / KPIs / clocks / table metrics**: JetBrains Mono, weights 600–700, with `font-feature-settings: "tnum" 1`.
- **Micro labels** (`.plab`, `.lbl`, table headers, chip labels): uppercase JetBrains Mono ~10–12px, tracking ~0.08em.

## Shape & layout

- Corner radius **8px** on panels/tables; inputs often **4px**; interactive filter chips stay full pill.
- Max content width **1080px**, horizontal padding 16px.
- Sticky top + mobile bottom nav: same structure as before; Apex surfaces + optional light `backdrop-filter` on chrome only (not table scroll areas).
- Pair bars: complementary over/under on one 100% track.

## Components (existing markup)

- **Panels** (`.grp`, `.chartbox`, `.mdonut`, `.lv`, tables): hairline border, 8px radius.
- **Pills** (`.opt`): selected = emerald border + `--emerald-tint` fill.
- **Selection / `aria-pressed` / `aria-current`**: emerald underline or border (not amber).
- **Focus ring**: 2px emerald.
- **Live**: emerald clock + pulse; late match inset emerald.
- **Matchday SVG + minutes donut**: strokes/fills via CSS vars (`colour()` + `--amber` / `--blue` / `--rose`).

## Out of scope (do not pull from Stitch)

- Bet-slip drawer, Simulate MD, market vs fair odds, sidebar navigation IA.
- Replacing ESPN / `build.py` / section JS with odds-terminal features.

## Interaction

- Emerald underline / inset for pressed and current.
- Live clock may pulse; respect `prefers-reduced-motion`.
- English UI; kickoff times in Europe/Paris.
