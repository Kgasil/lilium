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
