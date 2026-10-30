import tempfile
import subprocess
import sys
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET
from compose_profile_stats import compose, panel, tag

SVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="304" height="195" viewBox="0 0 304 195" aria-labelledby="title"><title id="title">Stats</title><style>.header {fill: red;} .stagger {opacity: 0; animation: fade 1s;} @keyframes fade {to {opacity: 1;}}</style><rect data-testid="card-bg"/><text class="header stagger">Real data</text></svg>'''

class CompositionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.a = Path(self.tmp.name) / 'a.svg'
        self.b = Path(self.tmp.name) / 'b.svg'
        self.a.write_text(SVG)
        self.b.write_text(SVG.replace('304', '300').replace('195', '165'))

    def test_combination_and_themes(self):
        for dark in (False, True):
            root = ET.fromstring(compose(self.a, self.b, dark))
            self.assertEqual(root.attrib['viewBox'], '0 0 652 219')
            panels = root.findall(tag('svg'))
            self.assertEqual([n.attrib['height'] for n in panels], ['195', '165'])
            self.assertEqual([n.attrib['y'] for n in panels], ['12', '12'])
            self.assertEqual(root.find(tag('rect')).attrib['fill'], '#0d1117' if dark else '#ffffff')
            ids = [n.attrib['id'] for n in root.iter() if 'id' in n.attrib]
            self.assertEqual(len(ids), len(set(ids)))
            self.assertEqual(len(root.findall('.//' + tag('rect'))), 1)
            self.assertEqual(len(root.findall('.//' + tag('text'))), 2)
            css = '\n'.join(n.text for n in root.findall('.//' + tag('style')))
            self.assertIn('.stats-header', css)
            self.assertIn('.langs-header', css)
            self.assertNotIn('opacity: 0;', css)
            self.assertNotIn('animation:', css)

    def test_missing(self):
        with self.assertRaises(FileNotFoundError):
            compose(self.a, self.b.with_name('missing.svg'))

    def test_failure_preserves_existing_outputs(self):
        folder = Path(self.tmp.name)
        out = folder / 'output'
        out.mkdir()
        old = out / 'github-stats.svg'
        old.write_text('last good card')
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('compose_profile_stats.py')),
                                 '--input-dir', str(folder), '--output-dir', str(out)], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(old.read_text(), 'last good card')

    def test_bad_inputs(self):
        bad = ['<svg', '<html/>', SVG.replace('Real data', 'Something went wrong'),
               SVG.replace('width="304"', 'width="0"'),
               SVG.replace('</svg>', '<script>alert(1)</script></svg>'),
               SVG.replace('<text ', '<text onclick="alert(1)" '),
               SVG.replace('<style>', '<style>@import "https://example.com";')]
        for content in bad:
            with self.subTest(content=content):
                self.b.write_text(content)
                with self.assertRaises((ValueError, ET.ParseError)):
                    compose(self.a, self.b)

if __name__ == '__main__':
    unittest.main()
