"""Build a portable Windows x64 folder. Run only on Windows with build dependencies."""
from pathlib import Path
import platform
import subprocess
import sys
from desktop.make_icon import create


def main():
    if sys.platform != "win32" or platform.machine().upper() not in {"AMD64", "X86_64"} or sys.maxsize <= 2**32:
        raise SystemExit("Build requires 64-bit Python on Windows x64.")
    root = Path(__file__).resolve().parent.parent
    icon = root / "build" / "lilium.ico"
    create(icon)
    assets = [root / "core" / "workspace.html", *sorted((root / "core").glob("*.js"))]
    args = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean",
            "--onedir", "--console", "--name", "Lilium", "--icon", str(icon),
            "--paths", str(root), "--collect-submodules", "uvicorn"]
    for path in assets:
        args += ["--add-data", str(path) + ":core"]
    args.append(str(root / "desktop" / "launcher.py"))
    subprocess.run(args, cwd=root, check=True)
    subprocess.run([str(root / "dist" / "Lilium" / "Lilium.exe"), "--self-test"], check=True, cwd=root)
    from desktop.terms import TERMS_BYTES
    (root / "dist" / "Lilium" / "TERMS-REVIEW.txt").write_bytes(TERMS_BYTES)
    print("Portable folder: dist/Lilium (keep all files together).")


if __name__ == "__main__":
    main()
