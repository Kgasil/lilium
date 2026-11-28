import json
from pathlib import Path
import tempfile
import os
import subprocess
import sys
import unittest
from desktop.terms import accepted, forget, require_acceptance, TERMS_SHA256, receipt_path

class TermsTests(unittest.TestCase):
    def test_decline_has_no_side_effect(self):
        with tempfile.TemporaryDirectory() as root:
            directory=Path(root)/"profile"
            self.assertFalse(require_acceptance(directory,input_fn=lambda _: "no",output_fn=lambda _: None))
            self.assertFalse(directory.exists())
    def test_exact_explicit_acceptance_and_reuse(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertFalse(require_acceptance(root,"0"*64))
            self.assertFalse(accepted(root))
            self.assertTrue(require_acceptance(root,TERMS_SHA256))
            self.assertTrue(accepted(root))
            row=json.loads(receipt_path(root).read_text())
            self.assertEqual(set(row),{"schema","terms_sha256","accepted_utc"})
            self.assertTrue(require_acceptance(root,input_fn=lambda _: self.fail("unexpected prompt")))
            forget(root)
            self.assertFalse(accepted(root))
    def test_stale_or_corrupt_receipt(self):
        with tempfile.TemporaryDirectory() as root:
            require_acceptance(root,TERMS_SHA256)
            row=json.loads(receipt_path(root).read_text())
            row["terms_sha256"]="0"*64
            receipt_path(root).write_text(json.dumps(row))
            self.assertFalse(accepted(root))
            receipt_path(root).write_text("invalid")
            self.assertFalse(accepted(root))
    def test_interactive_acceptance_and_eof(self):
        with tempfile.TemporaryDirectory() as root:
            def eof(_): raise EOFError()
            self.assertFalse(require_acceptance(root,input_fn=eof,output_fn=lambda _: None))
            self.assertTrue(require_acceptance(root,input_fn=lambda _: "ACEITO",output_fn=lambda _: None))

    def test_launcher_decline_and_show_terms(self):
        with tempfile.TemporaryDirectory() as root:
            env=dict(os.environ, LOCALAPPDATA=root, XDG_DATA_HOME=root, PYTHONIOENCODING="utf-8")
            cmd=[sys.executable,"-m","desktop.launcher"]
            show=subprocess.run(cmd+["--show-terms"],env=env,capture_output=True,text=True,encoding="utf-8",timeout=15)
            self.assertEqual(show.returncode,0,show.stderr)
            self.assertIn(TERMS_SHA256,show.stdout)
            no=subprocess.run(cmd+["--no-browser"],input="no\n",env=env,capture_output=True,text=True,encoding="utf-8",timeout=15)
            self.assertEqual(no.returncode,2,no.stderr)
            self.assertNotIn("LILIUM_READY",no.stdout)
            self.assertEqual(list(Path(root).iterdir()),[])
