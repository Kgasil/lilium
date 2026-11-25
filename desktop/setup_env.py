"""Source-only Windows setup. Repair never deletes the environment or user data."""
import argparse
import hashlib
from pathlib import Path
import platform
import subprocess
import sys
import venv


def ensure_environment(root, repair=False):
    root = Path(root).resolve()
    env = root / ".venv"
    exe = env / "Scripts" / "python.exe"
    req = root / "requirements.txt"
    marker = env / ".lilium-requirements-sha256"
    digest = hashlib.sha256(req.read_bytes()).hexdigest()
    if not exe.is_file():
        if env.exists():
            raise RuntimeError("Incomplete .venv. Close Lilium and rename that folder before retrying.")
        venv.EnvBuilder(with_pip=True).create(env)
    subprocess.run([str(exe), "-c", "import sys; assert sys.version_info[:2] == (3,12) and sys.maxsize > 2**32"], cwd=root, check=True)
    installed = marker.read_text(encoding="ascii").strip() if marker.is_file() else ""
    if repair or installed != digest:
        marker.unlink(missing_ok=True)
        args = [str(exe), "-m", "pip", "install", "--disable-pip-version-check"]
        if repair:
            args.append("--force-reinstall")
        subprocess.run(args + ["-r", str(req)], cwd=root, check=True)
        subprocess.run([str(exe), "-m", "pip", "check"], cwd=root, check=True)
        marker.write_text(digest + "\n", encoding="ascii")
    return exe


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lilium source setup (Windows x64)")
    parser.add_argument("--repair", action="store_true")
    args = parser.parse_args(argv)
    if sys.platform != "win32" or sys.version_info[:2] != (3, 12) or sys.maxsize <= 2**32 or platform.machine().upper() not in {"AMD64", "X86_64"}:
        print("Use Windows x64 and 64-bit Python 3.12.", file=sys.stderr)
        return 1
    try:
        ensure_environment(Path(__file__).resolve().parent.parent, args.repair)
    except (OSError, RuntimeError, subprocess.CalledProcessError, UnicodeError) as exc:
        print("Setup failed: " + type(exc).__name__ + ". See desktop/README.md.", file=sys.stderr)
        return 1
    print("Lilium environment ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
