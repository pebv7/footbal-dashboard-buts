# Goal Rates — pre-match dashboard

Sports-analytics tool for pre-match goal-rate research (Over 1.5 / 2.5 / 3.5, BTTS) across eleven European competitions. The main job: before a round, spot fixtures with high or low historical goal rates, then check the club and league context behind them. Data comes from the ESPN pipeline (`fetch_espn.py` → `data.json` → `build.py` → `index.html`). Every figure is a historical frequency from completed matches and is labelled as one. Brand: **Goal Rates**; FR descriptor “taux de buts”, not a second brand. Mark is a football in a goal net (`logo.png`). UI is bilingual EN (default) / FR.

## Atmosphere

Quiet slate with amber for brand and selection, and a muted green for values above their reference. No neon mint, no blue, no red, no purple.

## Information architecture

- **Mast** (not sticky): compact full-bleed pitch photo (`mast-banner.png`), amber wordmark, one-liner (~160px desktop / ~120px mobile). On scroll it leaves; controls stay in the sticky header.
- **Header** (sticky filter bar): scrollable league pills, market + Over|Under cluster, view tabs, tools (live / stamp / lang / refresh / theme). Data stamp also appears on the fixtures subtitle. Wraps below 1280px; mobile uses a horizontally scrollable market row + bottom tabs.
- **State in the URL**: `?lang=&league=&market=&view=`, e.g. `?lang=en&league=fr.1&market=o25&view=fixtures`. Old `#league/market/view` hashes migrate on load.
- **Keyboard**: `1`–`4` switch views, `[` / `]` change market, `/` focuses club search, `Esc` closes the drawer.
- **Fixtures** (default): next 7 days grouped by day; falls back to the next scheduled round when the week is empty (international breaks). Each row shows home rate at home, away rate away, and combined mean as a bar with a labelled league-average tick. Sort Date / Rate (sans-serif control); top 2–3 combined rates get an amber leading edge.
- **League**: KPI strip (with deltas vs 2025/26), goal-line ladder 0.5–3.5 plus BTTS, per-matchday chart with ±1 SD band (click a bar for its results), goal-minute distribution, kick-off weekday / time-slot table.
- **Clubs**: sortable table with the selected market at home, away and overall (sample size beside each rate), search, current season vs 2025/26, "hide small samples". Clicking a club opens the drawer: home vs away, last 8 match totals against the line, goal minutes, next fixture.
- **Compare**: dot range and ranking for the selected market and for goals per match; full figures table behind a toggle. Clicking a league switches to it.

## Honesty rules

- Show the sample size with every rate. Anything resting on fewer than 6 matches is dimmed; when most fixtures are small, a single "Early season" banner replaces per-row tags.
- Copy frames rates as “historical frequency from completed matches” wherever a rate could be read as a prediction.

## Color tokens

### Dark (default)
- `--bg #0E1116`, `--surf #151922`, `--surf2 #1C212B`, `--line #262C38`
- `--txt #E8EAEE`, `--mut #9AA3B2`, `--dim #7A8496`
- Brand amber: `--acc #E8A33D`, `--acc-tint rgba(232,163,61,.14)`
- Above-average green: `--pos #7DCF8A`, `--pos-tint rgba(125,207,138,.16)`
- Neutral bars: `--bar #4A5263`, `--bar-lo #2C323E`

### Light
- `--bg #F6F7F9`, `--surf #FFFFFF`, `--surf2 #EFF1F4`, `--line #DDE1E7`
- `--txt #111418`, `--mut #4B5563`, `--dim #6B7280`
- Brand amber: `--acc #A0620F`
- Above-average green: `--pos #1B6B34`, `--pos-tint rgba(27,107,52,.12)`

### `tone(value, reference)`
Returns `--pos` when the value beats the reference, `--bar` when close to or below it, `--bar-lo` when well below (more than 10 points). Heat cells use `--pos-tint` with green text. Amber stays for brand, selection, and the goal-line ladder.

## Typography

- Inter for UI and headings; JetBrains Mono with tabular figures for every number and market chips. Label segments (Date/Rate, chart opts, season) use Inter.
- Scale: 12 (meta), 13–14 (body), 16 (row values), 24 (view titles and KPIs).

## Shape

- Panels 8px radius, controls 6px, 1px `--line` borders. No shadows except the drawer.

## Responsive

- ≤900px: views move to a bottom tab bar, fixture rows become cards, the drawer becomes a bottom sheet, the clubs table scrolls with a sticky club column.

## Interaction

- Focus ring: 2px amber outline on `:focus-visible`. The drawer traps focus and returns it on close.
- Live link pulses while matches are in progress; `prefers-reduced-motion` disables animation.
- English UI; dates and kick-offs in Europe/Paris.
