import json
from pathlib import Path
from datetime import date, timedelta
import html

ROOT = Path(__file__).resolve().parent.parent

INPUT = ROOT / "data" / "contributions.json"
OUTPUT = ROOT / "contrib-heatmap.svg"

print("Generating premium contribution heatmap...")

with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

days = data["days"]

# Vibrant GitHub-inspired green palette
PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353"
]

CELL = 13
GAP = 4

LEFT = 45
TOP = 75

# Parse contribution data
contributions = {
    date.fromisoformat(item["date"]): int(item["level"])
    for item in days
}

first_date = min(contributions)
last_date = max(contributions)

# Align calendar to Sunday
start_date = first_date - timedelta(
    days=(first_date.weekday() + 1) % 7
)

total_days = (last_date - start_date).days + 1
weeks = (total_days + 6) // 7

WIDTH = LEFT + weeks * (CELL + GAP) + 35
HEIGHT = TOP + 7 * (CELL + GAP) + 65

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" '
    f'width="{WIDTH}" height="{HEIGHT}" '
    f'viewBox="0 0 {WIDTH} {HEIGHT}">',

    '<rect width="100%" height="100%" '
    'rx="12" fill="#0d1117"/>',

    '<text x="20" y="30" fill="#e6edf3" '
    'font-size="17" font-weight="bold" '
    'font-family="monospace">'
    'GitHub Contributions</text>',

    '<text x="20" y="50" fill="#8b949e" '
    'font-size="11" font-family="monospace">'
    f'{html.escape(data["username"])}'
    '</text>'
]

# Weekday labels
weekday_names = ["Sun", "Mon", "Tue", "Wed",
                 "Thu", "Fri", "Sat"]

for i, name in enumerate(weekday_names):
    if i % 2 == 1:
        y = TOP + i * (CELL + GAP) + 10

        svg.append(
            f'<text x="5" y="{y}" fill="#8b949e" '
            f'font-size="9" font-family="monospace">'
            f'{name}</text>'
        )

# Month labels
previous_month = None

for week in range(weeks):
    current = start_date + timedelta(days=week * 7)

    for offset in range(7):
        current_day = current + timedelta(days=offset)

        if current_day.day == 1:
            month = current_day.strftime("%b")

            if month != previous_month:
                x = LEFT + week * (CELL + GAP)

                svg.append(
                    f'<text x="{x}" y="{TOP - 12}" '
                    f'fill="#8b949e" font-size="10" '
                    f'font-family="monospace">{month}</text>'
                )

                previous_month = month

# Draw contribution squares
for i in range(total_days):

    current = start_date + timedelta(days=i)

    week = i // 7
    weekday = i % 7

    level = min(
        max(contributions.get(current, 0), 0),
        4
    )

    x = LEFT + week * (CELL + GAP)
    y = TOP + weekday * (CELL + GAP)

    delay = (week * 0.025) + (weekday * 0.015)

    color = PALETTE[level]

    svg.append(f'''
    <rect x="{x}" y="{y}"
          width="{CELL}" height="{CELL}"
          rx="3"
          fill="{color}"
          opacity="0">

        <animate attributeName="opacity"
                 from="0" to="1"
                 begin="{delay:.3f}s"
                 dur="0.35s"
                 fill="freeze"/>
    </rect>
    ''')

# Legend
legend_y = HEIGHT - 20

svg.append(
    f'<text x="20" y="{legend_y}" fill="#8b949e" '
    f'font-size="10" font-family="monospace">Less</text>'
)

for i, color in enumerate(PALETTE):

    x = 55 + i * 20

    svg.append(
        f'<rect x="{x}" y="{legend_y - 11}" '
        f'width="13" height="13" rx="3" '
        f'fill="{color}"/>'
    )

svg.append(
    f'<text x="165" y="{legend_y}" fill="#8b949e" '
    f'font-size="10" font-family="monospace">More</text>'
)

svg.append("</svg>")

OUTPUT.write_text(
    "\n".join(svg),
    encoding="utf-8"
)

print("--------------------------------")
print("SUCCESS!")
print(f"Weeks: {weeks}")
print(f"Days: {total_days}")
print(f"Generated: {OUTPUT}")
print("--------------------------------")
