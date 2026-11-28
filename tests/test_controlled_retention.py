import hashlib,json,tempfile,unittest
from pathlib import Path
from desktop.controlled_retention import retain,REQUIRED

class RetentionTests(unittest.TestCase):
    def test_explicit_review_integrity_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);root=p/"private";root.mkdir(mode=0o700)
            archive=p/"sample.zip";archive.write_bytes(b"synthetic fixture, not executable")
            sha=hashlib.sha256(archive.read_bytes()).hexdigest()
            rows={}
            for role in REQUIRED:
                e=p/(role+".txt");e.write_text("synthetic "+role)
                rows[role]={"name":e.name,"sha256":hashlib.sha256(e.read_bytes()).hexdigest()}
            r={"schema":1,"candidate_sha256":sha,"owner_authorized_retention":True,"reviewed_full_current_scans":True,"rights_reviewed_for_controlled_handoff":True,"access_restricted_confirmed":True,"release_approved":False,"evidence":rows}
            review=p/"review.json"
            def save(): review.write_text(json.dumps(r))
            save()
            r["reviewed_full_current_scans"]=False;save()
            with self.assertRaises(ValueError): retain(archive,review,root,sha)
            r["reviewed_full_current_scans"]=True;save()
            with self.assertRaises(ValueError): retain(archive,review,root,"0"*64)
            e=p/"defender.txt";orig=e.read_bytes();e.write_bytes(b"tampered")
            with self.assertRaises(ValueError): retain(archive,review,root,sha)
            e.write_bytes(orig)
            out=retain(archive,review,root,sha)
            self.assertEqual((out/"candidate.zip").read_bytes(),archive.read_bytes())
            self.assertFalse(json.loads((out/"retention.json").read_text())["release_approved"])
            with self.assertRaises(ValueError): retain(archive,review,root,sha)
