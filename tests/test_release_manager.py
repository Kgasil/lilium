import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import zipfile
from desktop import release_manager as r


class ReleaseTests(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.source = self.root / 'source'
        self.source.mkdir()
        (self.source / 'Lilium.exe').write_bytes(b'fake executable, never launched')
        (self.source / '_internal').mkdir()
        (self.source / '_internal' / 'core.js').write_text('sample')
        self.output = self.root / 'release'
        self.m = r.package(self.source, self.output, 'a' * 40)
        self.archive = self.output / self.m['filename']
        self.man = self.output / 'manifest.json'
        self.parent = self.root / 'versions'
        self.parent.mkdir()

    def test_roundtrip(self):
        self.assertEqual(r.verify(self.archive, self.man, self.m['sha256']), self.m)
        dest = r.stage(self.archive, self.man, self.m['sha256'], self.parent)
        self.assertEqual((dest / 'Lilium.exe').read_bytes(), (self.source / 'Lilium.exe').read_bytes())
        self.assertEqual((dest / '_internal' / 'core.js').read_text(), 'sample')

    def test_old_version_preserved(self):
        old = self.parent / 'Lilium-old'
        old.mkdir()
        (old / 'history.db').write_bytes(b'keep')
        one = r.stage(self.archive, self.man, self.m['sha256'], self.parent)
        two = r.stage(self.archive, self.man, self.m['sha256'], self.parent)
        self.assertNotEqual(one, two)
        self.assertEqual((old / 'history.db').read_bytes(), b'keep')

    def test_wrong_digest(self):
        with self.assertRaises(ValueError):
            r.stage(self.archive, self.man, '0' * 64, self.parent)
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_tampering(self):
        with self.archive.open('ab') as f:
            f.write(b'tampered')
        with self.assertRaises(ValueError):
            r.verify(self.archive, self.man, self.m['sha256'])

    def test_existing_output_preserved(self):
        with self.assertRaises(FileExistsError):
            r.package(self.source, self.output, 'a' * 40)
        self.assertTrue(self.archive.exists())

    def test_wrong_manifest(self):
        self.man.write_text(json.dumps({**self.m, 'platform': 'other'}))
        with self.assertRaises(ValueError):
            r.verify(self.archive, self.man, self.m['sha256'])

    def test_unsafe_names(self):
        for name in ('../x', '/abs', 'C:/x', 'a\\b', 'NUL.txt', 'dir/COM1', 'a.', 'a//b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                r.safe_name(name)

    def test_malicious_archives(self):
        for name in ('../outside', '_INTERNAL/other', 'lilium.exe', '_internal/core.js/nested'):
            with self.subTest(name=name):
                with zipfile.ZipFile(self.archive, 'w') as z:
                    z.writestr('Lilium.exe', 'fake')
                    z.writestr('_internal/core.js', 'fake')
                    z.writestr(name, 'bad')
                m = r.manifest(self.archive, 'a' * 40)
                self.man.write_text(json.dumps(m))
                with self.assertRaises(ValueError):
                    r.stage(self.archive, self.man, m['sha256'], self.parent)
                self.assertEqual(list(self.parent.iterdir()), [])

    def test_missing_bundle(self):
        with zipfile.ZipFile(self.archive, 'w') as z:
            z.writestr('other.txt', 'bad')
        m = r.manifest(self.archive, 'a' * 40)
        self.man.write_text(json.dumps(m))
        with self.assertRaises(ValueError):
            r.verify(self.archive, self.man, m['sha256'])
