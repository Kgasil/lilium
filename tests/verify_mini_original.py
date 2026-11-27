"""Verify Lilium Mini 0.1.1 runtime against the pinned public source and a temporary build."""
from hashlib import sha1, sha256
from pathlib import Path
import importlib.util
import json
import stat
import sys
import struct
import tempfile
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
EXT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "extension"
EXPECTED = {
    "icon128.png": "1a205af5d49bcb54dc97f5d02b378727391c710e",
    "manifest.json": "e1abd929ef84c5088d6e65a2f02a549b59e5a109",
    "math.js": "a4d3ffe06625d224bdf02668cbfcfafe636b0fe0",
    "popup.css": "428cad5bef43b237451b14381dc0b52a790b7ab3",
    "popup.html": "84155cc4229a03bc042e00a81733860da27db09f",
    "popup.js": "13ce392cb00ce749fe05c6b09996b2742154cdc7",
}
def require(ok, msg):
    if not ok:
        raise SystemExit(msg)

def git_blob(data):
    return sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def main():
    for name, expected in EXPECTED.items():
        p = EXT / name
        require(p.is_file() and not p.is_symlink(), f"Missing or invalid: {name}")
        require(git_blob(p.read_bytes()) == expected, f"Runtime differs from pinned version: {name}")
    m = json.loads((EXT / "manifest.json").read_bytes())
    require(set(m) == {"manifest_version","name","version","description","action","icons"}, "Unexpected manifest capability")
    require(m["manifest_version"] == 3 and m["version"] == "0.1.1", "Unexpected version")
    png = (EXT / "icon128.png").read_bytes()
    require(png[:8] == b"\x89PNG\r\n\x1a\n" and struct.unpack(">II",png[16:24]) == (128,128), "Invalid PNG")
    pos = 8
    while pos < len(png):
        require(pos+12 <= len(png), "Truncated PNG")
        n = struct.unpack_from(">I",png,pos)[0]
        end = pos+12+n
        require(end <= len(png), "Truncated PNG chunk")
        require(zlib.crc32(png[pos+4:end-4]) == struct.unpack_from(">I",png,end-4)[0], "PNG CRC mismatch")
        if png[pos+4:pos+8] == b"IEND":
            require(n == 0 and end == len(png), "Unexpected trailing PNG bytes")
            break
        pos = end
    else:
        raise SystemExit("Missing IEND")
    spec = importlib.util.spec_from_file_location("package_mini", EXT / "package_mini.py")
    pack = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pack)
    with tempfile.TemporaryDirectory() as td:
        a, h1 = pack.build(EXT, Path(td)/"a")
        b, h2 = pack.build(EXT, Path(td)/"b")
        require(a.read_bytes() == b.read_bytes() and h1 == h2, "Non-reproducible build")
        with zipfile.ZipFile(a) as z:
            entries = z.infolist()
            require(len(entries) == 6 and set(z.namelist()) == set(EXPECTED), "Unexpected archive entries")
            require(all(not i.is_dir() and not i.flag_bits & 1 and not stat.S_ISLNK(i.external_attr >> 16) for i in entries), "Unexpected entry type")
            require(z.testzip() is None, "ZIP CRC failure")
            for name, expected in EXPECTED.items():
                require(git_blob(z.read(name)) == expected, f"ZIP source mismatch: {name}")
        require(sha256(a.read_bytes()).hexdigest() == h1, "Build digest mismatch")
        print("Temporary build SHA-256:", h1)
    print("6/6 pinned runtime files, manifest, PNG, ZIP CRC, source parity and repeat build PASS.")
    print("Integrity only; not an antivirus scan. No public packages modified.")

if __name__ == "__main__":
    main()
