import unittest
from desktop.final_candidate import rights
class RightsTests(unittest.TestCase):
    def test_exact_review_only(self):
        h="a"*64
        row={"path":"_internal/vcruntime140.dll","sha256":h,"signature_status":"Valid","matching_python_source_paths":["vcruntime140.dll"],"signer":"O=Microsoft Corporation"}
        review={"schema":1,"owner_reviewed_applicable_rights":True,"release_approved":False,"files":{"vcruntime140.dll":h}}
        rights({"files":[row]},review)
        for changed in [dict(row,sha256="b"*64),dict(row,signature_status="NotSigned"),dict(row,matching_python_source_paths=[])]:
            with self.assertRaises(ValueError):rights({"files":[changed]},review)
        with self.assertRaises(ValueError):rights({"files":[row,row]},review)
        with self.assertRaises(ValueError):rights({"files":[row]},dict(review,release_approved=True))

class SnapshotTests(unittest.TestCase):
    def test_exact_archive_and_post_scan_mutation(self):
        import tempfile,json
        from pathlib import Path
        from desktop.release_manager import package
        from desktop.final_candidate import snapshot
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);bundle=root/"bundle";bundle.mkdir()
            for name in ("Lilium.exe","_internal/sample.dll","TERMS-REVIEW.txt","NOTICES/index.json"):
                p=bundle/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b"synthetic bytes "+name.encode())
            out=root/"out";commit="a"*40
            m=package(bundle,out,commit)
            archive=out/m["filename"]
            before=snapshot(bundle,archive,out/"manifest.json",commit,root/"before.json")
            after=snapshot(bundle,archive,out/"manifest.json",commit,root/"after.json")
            self.assertEqual(before,after)
            self.assertEqual((root/"before.json").read_bytes(),(root/"after.json").read_bytes())
            with self.assertRaises(ValueError):
                snapshot(bundle,archive,out/"manifest.json","b"*40,root/"bad.json")
            (bundle/"_internal/sample.dll").write_bytes(b"changed after scan")
            with self.assertRaises(ValueError):
                snapshot(bundle,archive,out/"manifest.json",commit,root/"bad.json")

class SourceBindingTests(unittest.TestCase):
    def test_exact_source_and_review_binding(self):
        import json
        from pathlib import Path
        from desktop.final_candidate import reviewed_source
        root=Path(__file__).resolve().parents[1]/"validation"
        source=json.loads((root/"microsoft-source-evidence.json").read_text())
        review=json.loads((root/"microsoft-reviewed-files.json").read_text())
        reviewed_source(review,source)
        with self.assertRaises(ValueError): reviewed_source(dict(review,files={"unknown.dll":"0"*64}),source)
        with self.assertRaises(ValueError): reviewed_source(review,dict(source,artifact_id=1))
