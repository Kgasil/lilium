import os
import socket
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from desktop import launcher


class DesktopTests(unittest.TestCase):
    def test_windows_directory(self):
        with tempfile.TemporaryDirectory() as base, patch.object(launcher.sys, "platform", "win32"), patch.dict(os.environ, {"LOCALAPPDATA": base}):
            self.assertEqual(launcher.data_directory(), Path(base) / "K&G Vision" / "Lilium")

    def test_missing_localappdata(self):
        with patch.object(launcher.sys, "platform", "win32"), patch.dict(os.environ, {"LOCALAPPDATA": ""}):
            with self.assertRaises(RuntimeError):
                launcher.data_directory()

    def test_reserved_socket(self):
        with launcher.reserve_socket() as sock:
            self.assertEqual(sock.getsockname()[0], "127.0.0.1")
            self.assertGreater(sock.getsockname()[1], 0)
            with socket.socket() as second:
                with self.assertRaises(OSError):
                    second.bind(sock.getsockname())

    def test_self_test(self):
        launcher.self_test()


if __name__ == "__main__":
    unittest.main()
