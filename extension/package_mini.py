"""Build a reproducible, unpacked-installation ZIP from Mini's runtime files."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

RUNTIME = ("manifest.json", "math.js", "popup.css", "popup.html", "popup.js")


def build(source, output):
    files = {}
    for name in RUNTIME:
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f"Missing or invalid runtime file: {name}")
        files[name] = path.read_bytes()
    manifest = json.loads(files["manifest.json"])
    if manifest.get("manifest_version") != 3:
        raise ValueError("Expected Manifest V3")
    if set(manifest) != {"manifest_version", "name", "version", "description", "action"}:
        raise ValueError("Review changed manifest capabilities before packaging")
    if manifest.get("name") != "Lilium Mini" or manifest.get("action") != {
        "default_title": "Lilium Mini", "default_popup": "popup.html"
    }:
        raise ValueError("Unexpected extension identity or popup")
    version = manifest["version"]
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValueError("Unexpected version format")
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f"Lilium-Mini-{version}-experimental.zip"
    with ZipFile(archive, "w", compression=ZIP_DEFLATED, compresslevel=9) as z:
        for name in RUNTIME:
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, files[name], compress_type=ZIP_DEFLATED, compresslevel=9)
    with ZipFile(archive) as z:
        if z.namelist() != list(RUNTIME) or z.testzip() is not None:
            raise ValueError("Archive integrity check failed")
        for name, data in files.items():
            if z.read(name) != data:
                raise ValueError(f"Archive content mismatch: {name}")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    (output / (archive.name + ".sha256")).write_bytes(
        f"{digest}  {archive.name}\n".encode("ascii")
    )
    return archive, digest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    archive, digest = build(Path(__file__).resolve().parent, args.output)
    print(f"{archive.name}: {digest}")
