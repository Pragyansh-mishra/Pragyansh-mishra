from pathlib import Path
import html

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "info-card.svg"

WIDTH = 620
HEIGHT = 400

details = [
    ("Name", "Pragyansh Mishra"),
    ("Role", "Developer & Entrepreneur"),
    ("Education", "B.Tech CSE (AI)"),
    ("Company", "Co-Founder @ KaayKreat"),
    ("Experience", "Ex-President, JKLU IIC"),
    ("Languages", "Python | C | JavaScript"),
    ("Frameworks", "React | Streamlit"),
    ("Interests", "AI | Startups | Technology"),
    ("Currently", "Building & learning."),
]

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',

    '<rect width="100%" height="100%" rx="12" fill="#000000"/>',
    '<rect x="1" y="1" width="618" height="398" rx="12" fill="none" stroke="#30363d"/>',

    '<circle cx="24" cy="23" r="6" fill="#ff5f56"/>',
    '<circle cx="44" cy="23" r="6" fill="#ffbd2e"/>',
    '<circle cx="64" cy="23" r="6" fill="#27c93f"/>',

    '<text x="90" y="28" fill="#8b949e" font-size="13" font-family="monospace">pragyansh@github ~</text>',

    '<text x="28" y="75" fill="#39d353" font-size="21" font-weight="bold" font-family="monospace">pragyansh@github</text>',

    '<text x="28" y="100" fill="#8b949e" font-size="13" font-family="monospace">------------------------------------------</text>',
]

for i, (key, value) in enumerate(details):

    y = 135 + i * 27
    delay = i * 0.18

    safe_key = html.escape(key)
    safe_value = html.escape(value)

    svg.append(f'''
    <g opacity="0">
        <animate attributeName="opacity"
                 from="0" to="1"
                 begin="{delay}s"
                 dur="0.35s"
                 fill="freeze"/>

        <text x="30" y="{y}"
              fill="#39d353"
              font-size="14"
              font-family="monospace">{safe_key}</text>

        <text x="155" y="{y}"
              fill="#e6edf3"
              font-size="14"
              font-family="monospace">{safe_value}</text>
    </g>
    ''')

svg.append('''
<text x="28" y="380"
      fill="#8b949e"
      font-size="11"
      font-family="monospace">
    "Building. Learning. Creating."
</text>
</svg>
''')

OUTPUT.write_text("\\n".join(svg), encoding="utf-8")

print("SUCCESS!")
print(f"Generated: {OUTPUT}")
