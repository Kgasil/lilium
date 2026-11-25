import unittest
from core.session import new_token, authorized, protected, access_url

BASE = "http://127.0.0.1:12345"
TOKEN = "a" * 64


class SessionTests(unittest.TestCase):
    def check(self, supplied=TOKEN, origin=None, site=None, expected=TOKEN):
        return authorized(expected, supplied, origin, BASE, site)

    def test_random_tokens(self):
        self.assertNotEqual(new_token(), new_token())
        self.assertRegex(new_token(), r"^[0-9a-f]{64}$")

    def test_matching_native_token(self):
        self.assertTrue(self.check())

    def test_same_origin_browser(self):
        self.assertTrue(self.check(origin=BASE, site="same-origin"))

    def test_missing(self):
        self.assertFalse(self.check(supplied=None))

    def test_wrong(self):
        self.assertFalse(self.check(supplied="b" * 64))

    def test_unicode_and_bad_format(self):
        for value in ("é" * 64, "a" * 63, "a" * 65, "A" * 64, "a" * 64 + "\n"):
            self.assertFalse(self.check(supplied=value))

    def test_invalid_expected(self):
        self.assertFalse(self.check(expected=""))

    def test_cross_origin(self):
        self.assertFalse(self.check(origin="https://example.com"))

    def test_null_origin(self):
        self.assertFalse(self.check(origin="null"))

    def test_cross_site(self):
        for site in ("cross-site", "same-site", "unexpected"):
            self.assertFalse(self.check(site=site))

    def test_api_path(self):
        for path in ("/api", "/api/v1/history", "/api/v1/backup", "/api/v1/analyze"):
            self.assertTrue(protected(path))
        for path in ("/", "/health", "/assets/workspace.js", "/openapi.json", "/apix"):
            self.assertFalse(protected(path))

    def test_fragment(self):
        self.assertEqual(access_url(BASE, TOKEN), BASE + "/#access=" + TOKEN)
        with self.assertRaises(ValueError):
            access_url(BASE, "bad")
