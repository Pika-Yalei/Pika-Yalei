"""Generate local flat, brand-colored technology badges with embedded icons."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)
BADGES = [
    ('react', 'React', 86, '#61dafb', '#17202a'),
    ('vue', 'Vue', 73, '#4fc08d', '#ffffff'),
    ('java', 'Java', 79, '#f89820', '#ffffff'),
    ('spring', 'Spring', 91, '#6db33f', '#ffffff'),
    ('mysql', 'MySQL', 94, '#4479a1', '#ffffff'),
    ('postgresql', 'PostgreSQL', 132, '#4169e1', '#ffffff'),
    ('oracle', 'Oracle', 93, '#f80000', '#ffffff'),
    ('mongodb', 'MongoDB', 117, '#47a248', '#ffffff'),
    ('dameng', '达梦', 77, '#c83030', '#ffffff'),
    ('docker', 'Docker', 97, '#2496ed', '#ffffff'),
    ('compose', 'Compose', 119, '#2496ed', '#ffffff'),
    ('linux', 'Linux', 86, '#fcc624', '#17202a'),
    ('cicd', 'CI/CD', 90, '#2088ff', '#ffffff'),
]

def node(parent, tag, attrs, text=None):
    element = ET.SubElement(parent, f'{{{NS}}}{tag}', attrs)
    element.text = text
    return element


def main():
    output = Path(__file__).resolve().parents[1] / 'profile' / 'badges'
    output.mkdir(parents=True, exist_ok=True)
    for slug, label, width, bg, fg in BADGES:
        root = ET.Element(f'{{{NS}}}svg', {
            'width': str(width + 4), 'height': '32', 'viewBox': f'0 0 {width+4} 32',
            'role': 'img', 'aria-label': label,
        })
        node(root, 'title', {}, label)
        node(root, 'rect', {'width': str(width), 'height': '28', 'fill': bg})
        icon_path = output / 'icons' / (('docker' if slug == 'compose' else slug) + '.svg')
        if icon_path.exists():
            icon = ET.parse(icon_path).getroot()
            icon.attrib.update({'x': '7', 'y': '6', 'width': '16', 'height': '16'})
            # Monochrome marks match the supplied flat-badge reference.
            for element in ([] if slug == 'linux' else icon.iter()):
                if element.tag.endswith('path') and 'fill' not in element.attrib:
                    element.set('fill', fg)
                for key in ('fill', 'stroke'):
                    if key in element.attrib and element.get(key) != 'none':
                        element.set(key, fg)
                if 'style' in element.attrib:
                    element.set('style', re.sub(r'fill\s*:\s*[^;]+', f'fill:{fg}', element.get('style')))
            root.append(icon)
        elif slug == 'dameng':
            node(root, 'text', {'x':'7','y':'14','dominant-baseline':'central','fill':fg,
                               'font-family':'Arial,sans-serif','font-size':'10','font-weight':'700'}, 'DM')
        else:
            node(root, 'path', {'d':'M8 12a6 6 0 0 1 10-3l2 2m0-5v5h-5M22 16a6 6 0 0 1-10 3l-2-2m0 5v-5h5',
                               'fill':'none','stroke':fg,'stroke-width':'1.6'})
        node(root, 'text', {
            'x':'30','y':'14','dominant-baseline':'central','fill':fg,
            'font-family':'-apple-system,BlinkMacSystemFont,Segoe UI,Arial,sans-serif',
            'font-size':'14','font-weight':'400',
        }, label)
        (output / f'{slug}.svg').write_text(ET.tostring(root, encoding='unicode') + '\n')

if __name__ == '__main__':
    main()
