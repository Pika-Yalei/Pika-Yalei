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
    for slug, label, width in BADGES:
        text = escape(label)
        (output / f'{slug}.svg').write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width+4}" height="34" viewBox="0 0 {width+4} 34" role="img" aria-label="{text}">
  <title>{text}</title>
  <rect x="0.5" y="0.5" width="{width-1}" height="29" rx="8" fill="#eff6ff" stroke="#bfdbfe"/>
  <circle cx="13" cy="15" r="3" fill="#2563eb"/>
  <text x="24" y="15" dominant-baseline="central" fill="#1e40af" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif" font-size="13" font-weight="600">{text}</text>
</svg>
''')

if __name__ == '__main__':
    main()
