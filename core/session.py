"""Process-scoped bearer capability for the loopback Desktop API."""
import re
import secrets
from hmac import compare_digest

HEADER = "x-lilium-session"
TOKEN = re.compile(r"[0-9a-f]{64}")


def new_token():
    return secrets.token_hex(32)


def protected(path):
    return path == "/api" or path.startswith("/api/")


def authorized(expected, supplied, origin, base_url, fetch_site):
    # No origin header is normal for native clients; a token is still mandatory.
    if origin is not None and origin != base_url.rstrip("/"):
        return False
    if fetch_site not in (None, "same-origin", "none"):
        return False
    if not isinstance(expected, str) or not TOKEN.fullmatch(expected):
        return False
    if not isinstance(supplied, str) or not TOKEN.fullmatch(supplied):
        return False
    return compare_digest(expected, supplied)


def access_url(base, token):
    if not TOKEN.fullmatch(token):
        raise ValueError("Invalid session token")
    return base.rstrip("/") + "/#access=" + token
