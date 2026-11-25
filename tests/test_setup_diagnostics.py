import hashlib
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
from desktop import diagnostics, setup_env


class SetupTests(unittest.TestCase):
    def setUp(self):
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.env = self.root / '.venv'
        self.exe = self.env / 'Scripts' / 'python.exe'
        self.exe.parent.mkdir(parents=True)
        self.exe.touch()
        self.req = self.root / 'requirements.txt'
        self.req.write_text('example==1.0', encoding='ascii')
        self.marker = self.env / '.lilium-requirements-sha256'
        self.history = self.root / 'history.db'
        self.history.write_bytes(b'keep')

    @patch('desktop.setup_env.subprocess.run')
    def test_initial_install(self, run):
        self.assertEqual(setup_env.ensure_environment(self.root), self.exe)
        self.assertEqual(run.call_count, 3)
        self.assertEqual(self.marker.read_text().strip(), hashlib.sha256(self.req.read_bytes()).hexdigest())

    @patch('desktop.setup_env.subprocess.run')
    def test_reuse(self, run):
        setup_env.ensure_environment(self.root)
        run.reset_mock()
        setup_env.ensure_environment(self.root)
        self.assertEqual(run.call_count, 1)

    @patch('desktop.setup_env.subprocess.run')
    def test_repair(self, run):
        setup_env.ensure_environment(self.root, repair=True)
        self.assertIn('--force-reinstall', run.call_args_list[1].args[0])
        self.assertEqual(self.history.read_bytes(), b'keep')

    @patch('desktop.setup_env.subprocess.run')
    def test_changed_requirements(self, run):
        setup_env.ensure_environment(self.root)
        self.req.write_text('example==2.0', encoding='ascii')
        run.reset_mock()
        setup_env.ensure_environment(self.root)
        self.assertEqual(run.call_count, 3)

    @patch('desktop.setup_env.subprocess.run')
    def test_failed_repair_invalidates_marker(self, run):
        setup_env.ensure_environment(self.root)
        run.side_effect = [None, OSError('failure')]
        with self.assertRaises(OSError):
            setup_env.ensure_environment(self.root, repair=True)
        self.assertFalse(self.marker.exists())

    def test_partial_environment_preserved(self):
        self.exe.unlink()
        with self.assertRaises(RuntimeError):
            setup_env.ensure_environment(self.root)
        self.assertTrue(self.env.exists())


class DiagnosticTests(unittest.TestCase):
    def test_dependencies(self):
        self.assertEqual(diagnostics.dependency_versions(), diagnostics.EXPECTED)

    def test_redacted_failure_and_temporary_storage(self):
        import socket
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            history = root / 'lilium.sqlite3'
            history.write_bytes(b'not a database; must stay untouched')
            def reserve():
                sock = socket.socket()
                sock.bind(('127.0.0.1', 0))
                return sock
            def fail():
                raise RuntimeError('private path ' + tmp)
            result = diagnostics.report('0.14.0', [], lambda: root, reserve, fail)
            checks = {x['id']: x['status'] for x in result['checks']}
            self.assertEqual(checks['storage_write'], 'pass')
            self.assertEqual(checks['loopback'], 'pass')
            self.assertEqual(checks['api_self_test'], 'fail')
            self.assertFalse(result['ready'])
            self.assertNotIn(tmp, json.dumps(result))
            self.assertEqual(list(root.iterdir()), [history])
            self.assertEqual(history.read_bytes(), b'not a database; must stay untouched')
