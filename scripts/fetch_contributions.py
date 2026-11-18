import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path
from datetime import datetime

USERNAME = "Pragyansh-mishra"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "data" / "contributions.json"

URL = f"https://github.com/users/{USERNAME}/contributions"

print("Fetching GitHub contributions...")

response = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

days = []

for cell in soup.select("td.ContributionCalendar-day"):
    date = cell.get("data-date")
    count = cell.get("data-level")

    tooltip = cell.get("aria-label", "")

    if date:
        days.append({
            "date": date,
            "level": int(count or 0),
            "tooltip": tooltip
        })

if not days:
    raise RuntimeError(
        "No contribution data found. GitHub may have changed its HTML."
    )

data = {
    "username": USERNAME,
    "updated": datetime.now().isoformat(),
    "total_days": len(days),
    "days": days
}

OUTPUT.write_text(
    json.dumps(data, indent=2),
    encoding="utf-8"
)

print("SUCCESS!")
print(f"Collected {len(days)} contribution days.")
print(f"Saved to: {OUTPUT}")
