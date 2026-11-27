import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from desktop.license_evidence import copy_notice, verify_archive, upstream_bytes, git_blob, is_notice_name
class NoticeTests(unittest.TestCase):
    def test_license_spelling_and_authors(self):
        for name in ('LICENSE.txt','LICENCE.rst','LICENCE.python','AUTHORS.rst','AUTHORS.txt','NOTICE'):
            self.assertTrue(is_notice_name(name),name)
        for name in ('LICENSED.py','AUTHORSHIP.py','some_LICENSE.txt','example.py'):
            self.assertFalse(is_notice_name(name),name)

    def test_notice_archive_exact_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            row=copy_notice(root,"notice.txt",b"synthetic license","fixture")
            index=root/"index.json";index.write_text(json.dumps({"notices":[row]}))
            archive=root/"test.zip"
            with zipfile.ZipFile(archive,"w") as z:
                z.writestr("NOTICES/index.json",index.read_bytes());z.writestr(row["path"],b"synthetic license")
            verify_archive(archive,index)
            with zipfile.ZipFile(archive,"w") as z:
                z.writestr("NOTICES/index.json",index.read_bytes());z.writestr(row["path"],b"changed")
            with self.assertRaises(ValueError): verify_archive(archive,index)
    def test_path_and_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(ValueError): copy_notice(root,"../x",b"x","fixture")
            copy_notice(root,"x.txt",b"x","fixture")
            with self.assertRaises(FileExistsError): copy_notice(root,"x.txt",b"x","fixture")
    def test_upstream_blob(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/"notice.txt";p.write_bytes(b"text\r\n")
            self.assertEqual(upstream_bytes(p,git_blob(b"text\n")),b"text\n")
            with self.assertRaises(ValueError): upstream_bytes(p,"0"*40)
