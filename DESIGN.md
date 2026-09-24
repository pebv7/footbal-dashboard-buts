# Goal Markets — pre-match dashboard

Pre-match research tool for goal markets (Over 1.5 / 2.5 / 3.5, BTTS) across ten European competitions. The main job: before a round, spot fixtures likely to be goal-heavy or goal-light, then check the club and league context behind them. Data comes from the ESPN pipeline (`fetch_espn.py` → `data.json` → `build.py` → `index.html`). No odds, bet slips or probability models: every figure is a historical frequency and is labelled as one.

## Atmosphere

Quiet, near-monochrome slate with a single amber accent. The accent carries one meaning only: **this value is above its reference** (league average, cross-league mean, or an even share). Everything else is grey. No green, blue, red or purple; no gradients, glow or decorative shadows.

## Information architecture

- **Header** (one row, 56px, sticky): brand, scrollable league strip, market segmented control (O 1.5 / O 2.5 / O 3.5 / BTTS), view tabs (Fixtures / League / Clubs / Compare), live link when matches are in progress, data stamp, refresh, theme. Wraps to two rows below 1280px.
- **State in the URL**: `#<league>/<market>/<view>`, e.g. `#fr.1/o25/fixtures`. Shareable and restored on load.
- **Keyboard**: `1`–`4` switch views, `[` / `]` change market, `/` focuses club search, `Esc` closes the drawer.
- **Fixtures** (default): next 7 days grouped by day; falls back to the next scheduled round when the week is empty (international breaks). Each row shows the home club's rate at home, the away club's rate away, and their mean as the combined value, drawn as a bar with a league-average tick. Sort by kick-off or by highest combined.
- **League**: KPI strip (with deltas vs 2025/26), goal-line ladder 0.5–3.5 plus BTTS, per-matchday chart with ±1 SD band (click a bar for its results), goal-minute distribution, kick-off weekday / time-slot table.
- **Clubs**: sortable table with the selected market at home, away and overall (sample size beside each rate), search, current season vs 2025/26, "hide small samples". Clicking a club opens the drawer: home vs away, last 8 match totals against the line, goal minutes, next fixture.
- **Compare**: dot range and ranking for the selected market and for goals per match; full figures table behind a toggle. Clicking a league switches to it.

## Honesty rules

- Show the sample size with every rate. Anything resting on fewer than 6 matches is dimmed; when most fixtures are small, a single "Early season" banner replaces per-row tags.
- Copy says "historical frequency, not a probability" wherever a rate could be read as a prediction.

## Color tokens

### Dark (default)
- `--bg #0E1116`, `--surf #151922`, `--surf2 #1C212B`, `--line #262C38`
- `--txt #E8EAEE`, `--mut #9AA3B2`, `--dim #7A8496`
- `--acc #E8A33D`, `--acc-tint rgba(232,163,61,.14)`
- Neutral bars: `--bar #4A5263`, `--bar-lo #2C323E`

### Light
- `--bg #F6F7F9`, `--surf #FFFFFF`, `--surf2 #EFF1F4`, `--line #DDE1E7`
- `--txt #111418`, `--mut #4B5563`, `--dim #6B7280`
- `--acc #A0620F` (darker so amber text keeps 4.5:1 on white)

### `tone(value, reference)`
The only colour decision in the code. Returns `--acc` when the value beats the reference, `--bar` when close to or below it, `--bar-lo` when well below (more than 10 points). Heat cells use `--acc-tint` with amber text.

## Typography

- Inter for UI and headings; JetBrains Mono with tabular figures for every number.
- Scale: 12 (meta), 13–14 (body), 16 (row values), 24 (view titles and KPIs).

## Shape

- Panels 8px radius, controls 6px, 1px `--line` borders. No shadows except the drawer.

## Responsive

- ≤900px: views move to a bottom tab bar, fixture rows become cards, the drawer becomes a bottom sheet, the clubs table scrolls with a sticky club column.

## Interaction

- Focus ring: 2px amber outline on `:focus-visible`. The drawer traps focus and returns it on close.
- Live link pulses while matches are in progress; `prefers-reduced-motion` disables animation.
- English UI; dates and kick-offs in Europe/Paris.
