import importlib.util,unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location("gate",Path(__file__).with_name("candidate_build_gate.py"))
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)

class GateTests(unittest.TestCase):
    def setUp(self):
        self.sha="a"*40
        self.row={"schema":1,"source_commit":self.sha,"owner_authorized_build":True,"owner_reviewed_terms":True,"microsoft_entitlement_reviewed":True,"controlled_retention_authorized":True,"release_approved":False}
    def test_authorization_only(self):
        gate.validate(self.row,self.sha,[gate.AUTH])
    def test_wrong_parent_or_extra_file(self):
        for parent,files in [("b"*40,[gate.AUTH]),(self.sha,[gate.AUTH,"desktop/main.py"]),(self.sha,[])]:
            with self.subTest(parent=parent,files=files),self.assertRaises(ValueError):gate.validate(self.row,parent,files)
    def test_missing_or_false_approval(self):
        for key in ("owner_authorized_build","owner_reviewed_terms","microsoft_entitlement_reviewed","controlled_retention_authorized","release_approved"):
            row=dict(self.row);row[key]=not row[key]
            with self.subTest(key=key),self.assertRaises(ValueError):gate.validate(row,self.sha,[gate.AUTH])
if __name__=="__main__":unittest.main()
