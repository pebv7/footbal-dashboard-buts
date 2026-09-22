# Marchés de buts — Design System

Dense sports-data dashboard for live under-goal betting. Utilitarian, high-contrast, calm navy surfaces with an amber accent. Not playful, not marketing — a tool for reading match tempo around the 70th minute.

## Atmosphere

Dense, analytical, night-match. Surfaces stack like broadcast graphics: charcoal-navy panels on a deeper navy field. Typography is condensed for numbers, humanist sans for labels. One job per section. Avoid purple gradients, cream editorial themes, glow effects, and oversized rounded pills as decoration.

## Color

### Dark mode (primary)
- **Field navy** `#0E1428` — page background
- **Panel navy** `#151D38` — cards, tables, sticky header surface
- **Inset navy** `#1D2749` — pressed/hover wells, track backgrounds
- **Hairline indigo** `#2A365F` — borders; `#3A4877` for stronger separators
- **Paper** `#E9EDF8` — primary text
- **Muted slate** `#8A96BC` — secondary text; `#5C6890` for tertiary/dim
- **Signal amber** `#F0B23C` — selection, key KPIs, sort, focus
- **Ice blue** `#5A8AFF` — under/cool metrics, “neg” deltas
- **Rose live** `#E2607C` — live minute, live nav cue
- **Mint** `#4FC3A1` — GG / both-teams-scored accent

### Light mode
- Background `#F1F3F8`, surface `#FFFFFF`, inset `#E7EBF4`
- Lines `#D3D9E6` / `#B8C2D6`
- Text `#111827`, muted `#5A6480`, dim `#8A93A8`
- Amber `#A85E00`, blue `#2B55C8`, rose `#B32B4C`, mint `#0E7256`

## Typography

- **Headlines / numbers**: Barlow Condensed, weight 600–700. Large KPIs ~42px, scores ~20px, section titles ~23px.
- **Body / UI**: IBM Plex Sans, 14–15px body, 12–13px helper text.
- Numbers always use the condensed face (`.num`, scores, ends).

## Shape & layout

- Corner radius **7–8px** on panels, inputs, buttons — softly squared, not pill-shaped for containers.
- Filter chips may use full pill radius only when they are interactive toggles.
- Max content width **1080px**, horizontal padding 16px.
- Sticky top bar with league select + refresh; section scroll-margin under the bar.
- Tables: sticky header row, optional sticky first column, horizontal scroll with edge fade.
- Pair bars: complementary over/under sharing one 100% track.

## Components

- **Live match card**: home | score | away | clock; expand with total goals, under-line chips (−1.5 / −2.5 / −3.5), season under rate for the selected line, soft highlight when minute ≥ 70.
- **Mobile nav**: three primary destinations — Live / Stats / Compare — not eight equal text links.
- **Repères**: hero KPI + paired percentage bars; clickable to drive the journée chart.
- **Journée mobile**: stacked KPI card first; full multi-column table behind “voir détail”.

## Interaction

- Amber underline / inset for `aria-pressed` and `aria-current`.
- Focus ring: 2px amber.
- Live clock may pulse gently; respect `prefers-reduced-motion`.
- French labels; all kickoff times shown in Europe/Paris.
