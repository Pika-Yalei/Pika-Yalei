"""Generate self-contained, consistently styled technology badges (no external service)."""
from pathlib import Path
from html import escape

BADGES = [
    ('react', 'React', 76), ('vue', 'Vue', 65),
    ('java', 'Java', 70), ('spring', 'Spring', 82),
    ('mysql', 'MySQL', 84), ('postgresql', 'PostgreSQL', 119),
    ('oracle', 'Oracle', 84), ('mongodb', 'MongoDB', 106), ('dameng', '达梦', 70),
    ('docker', 'Docker', 88), ('compose', 'Compose', 106),
    ('linux', 'Linux', 76), ('cicd', 'CI/CD', 83),
]

def main():
    output = Path(__file__).resolve().parents[1] / 'profile' / 'badges'
    output.mkdir(parents=True, exist_ok=True)
    accents = {
        'react': '#61dafb', 'vue': '#42b883', 'java': '#f89820',
        'spring': '#6db33f', 'mysql': '#69b8d6', 'postgresql': '#699eca',
        'oracle': '#f87171', 'mongodb': '#69b86c', 'dameng': '#e98a8a',
        'docker': '#4ea8f4', 'compose': '#4ea8f4', 'linux': '#e8c15a',
        'cicd': '#a99cec',
    }
    for slug, label, width in BADGES:
        width -= 8
        text = escape(label)
        (output / f'{slug}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width+4}" height="30" viewBox="0 0 {width+4} 30" role="img" aria-label="{text}">
  <title>{text}</title>
  <rect x="0.5" y="0.5" width="{width-1}" height="25" rx="3" fill="#24292f" stroke="#444c56"/>
  <rect x="8" y="7" width="2" height="12" rx="1" fill="{accents[slug]}"/>
  <text x="18" y="13" dominant-baseline="central" fill="#f0f3f6" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif" font-size="12" font-weight="600">{text}</text>
</svg>
''')

if __name__ == '__main__':
    main()
