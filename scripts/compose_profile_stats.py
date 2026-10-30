"""Compose real generated stats into one static, unscaled, accessible SVG."""
from pathlib import Path
import argparse
import re
import xml.etree.ElementTree as ET

NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

def tag(name):
    return f'{{{NS}}}{name}'


def panel(path, prefix):
    content = Path(path).read_text()
    if 'Something went wrong' in content or '<!DOCTYPE' in content or '<!ENTITY' in content:
        raise ValueError(f'Invalid or error card: {path}')
    root = ET.fromstring(content)
    if root.tag != tag('svg'):
        raise ValueError('Expected SVG root')
    width, height = (float(root.attrib[key]) for key in ('width', 'height'))
    if not (100 <= width <= 1000 and 100 <= height <= 1000):
        raise ValueError('Unexpected card dimensions')
    if not root.findall('.//' + tag('text')):
        raise ValueError('Card contains no text')
    for node in root.iter():
        if node.tag in {tag('script'), tag('foreignObject'), tag('image')}:
            raise ValueError('Active or external SVG content is not supported')
        for key, value in node.attrib.items():
            if key.lower().startswith('on') or (key.endswith('href') and not value.startswith('#')):
                raise ValueError('Unsafe SVG attribute')
    # Namespace ids/classes and keyframes so the two generators cannot interfere.
    ids = {n.attrib['id'] for n in root.iter() if 'id' in n.attrib}
    classes = {c for n in root.iter() for c in n.attrib.get('class', '').split()}
    def refs(value):
        for old in sorted(ids, key=len, reverse=True):
            value = value.replace(f'url(#{old})', f'url(#{prefix}{old})')
            if value == '#' + old:
                value = '#' + prefix + old
        return value
    for node in root.iter():
        for key, value in list(node.attrib.items()):
            if key == 'id':
                node.set(key, prefix + value)
            elif key == 'class':
                node.set(key, ' '.join(prefix + c for c in value.split()))
            elif key in ('aria-labelledby', 'aria-describedby'):
                node.set(key, ' '.join(prefix + c for c in value.split()))
            else:
                node.set(key, refs(value))
        if node.tag == tag('style') and node.text:
            css = refs(node.text)
            if re.search(r'@import|url\(\s*["\']?(?!#)', css, re.I):
                raise ValueError('External CSS is not supported')
            for old in sorted(classes, key=len, reverse=True):
                css = re.sub(r'\.' + re.escape(old) + r'(?![\w-])', '.' + prefix + old, css)
            for old in sorted(ids, key=len, reverse=True):
                css = re.sub(r'#' + re.escape(old) + r'(?![\w-])', '#' + prefix + old, css)
            for name in re.findall(r'@keyframes\s+([\w-]+)', css):
                css = re.sub(r'\b' + re.escape(name) + r'\b', prefix + name, css)
            # Static content: avoid renderer-dependent invisible animation start frames.
            css = re.sub(r'animation(?:-[\w-]+)?\s*:[^;}]+;?', '', css)
            css = re.sub(r'opacity\s*:\s*0\s*;', 'opacity: 1;', css)
            node.text = css
    # Remove only the individual backgrounds; the composition stays transparent.
    for parent in root.iter():
        for child in list(parent):
            if child.attrib.get('data-testid') == 'card-bg':
                parent.remove(child)
    return root, width, height


def compose(stats, languages, dark=False):
    left, lw, lh = panel(stats, 'stats-')
    right, rw, rh = panel(languages, 'langs-')
    padding, gap = 12, 24
    width, height = lw + rw + 2 * padding + gap, max(lh, rh) + 2 * padding
    root = ET.Element(tag('svg'), {
        'width': f'{width:g}', 'height': f'{height:g}',
        'viewBox': f'0 0 {width:g} {height:g}', 'fill': 'none',
        'role': 'img', 'aria-labelledby': 'profile-title profile-description',
    })
    ET.SubElement(root, tag('title'), {'id': 'profile-title'}).text = 'Pika-Yalei — GitHub Stats'
    ET.SubElement(root, tag('desc'), {'id': 'profile-description'}).text = (
        'Public GitHub contribution statistics and most used repository languages. Updated daily.'
    )
    # No outer background, border or divider: blend directly into the profile.
    for node, x in ((left, padding), (right, padding + lw + gap)):
        node.set('x', f'{x:g}')
        node.set('y', str(padding))
        root.append(node)  # Original width/viewBox unchanged: no font scaling.
    return ET.tostring(root, encoding='unicode') + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-dir', type=Path, default=Path('.profile-stats-input'))
    parser.add_argument('--output-dir', type=Path, default=Path('profile'))
    args = parser.parse_args()
    outputs = {}
    for dark, suffix in ((False, ''), (True, '-dark')):
        outputs[f'github-stats{suffix}.svg'] = compose(
            args.input_dir / f'stats{suffix}.svg',
            args.input_dir / f'top-langs{suffix}.svg', dark,
        )
    # Validate both themes before touching outputs; any failure stops the workflow commit.
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for name, svg in outputs.items():
        target = args.output_dir / name
        temp = target.with_suffix('.svg.tmp')
        temp.write_text(svg)
        temp.replace(target)
        print(f'Generated {target}')


if __name__ == '__main__':
    main()
