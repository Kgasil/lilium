import tempfile
import unittest
from pathlib import Path
from desktop.runtime_evidence import NAMES,source_files,compare_bundle,openssl_version

class RuntimeEvidenceTests(unittest.TestCase):
    def test_openssl_3_patch_encoding(self):
        self.assertEqual(openssl_version(0x30500090,'OpenSSL 3.5.9 29 Sep 2026'),'3.5.9')
        self.assertEqual(openssl_version(0x30500000,'OpenSSL 3.5.0 1 Jan 2026'),'3.5.0')
        with self.assertRaises(ValueError): openssl_version(0x30500000,'OpenSSL 3.5.9 29 Sep 2026')
        with self.assertRaises(ValueError): openssl_version(0x1010100f,'OpenSSL 1.1.1 1 Jan 2026')
    def test_bundle_equal_and_reject_changed(self):
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/"source";bundle=root/"bundle";source.mkdir();bundle.mkdir()
            (source/"DLLs").mkdir()
            for name in NAMES:
                target=source/name if name=="python314.dll" else source/"DLLs"/name
                target.write_bytes(name.encode())
                (bundle/name).write_bytes(name.encode())
            expected=source_files(source)
            self.assertEqual(len(compare_bundle(bundle,expected)),4)
            (bundle/"sqlite3.dll").write_bytes(b"changed")
            with self.assertRaises(ValueError): compare_bundle(bundle,expected)
            (bundle/"sqlite3.dll").write_bytes(b"sqlite3.dll")
            (bundle/"python312.dll").write_bytes(b"old")
            with self.assertRaises(ValueError): compare_bundle(bundle,expected)
    def test_missing_source(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(ValueError): source_files(Path(folder))
if __name__=="__main__": unittest.main()
