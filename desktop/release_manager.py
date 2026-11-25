"""Offline portable preview packaging and staging; never launches or replaces an app."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import stat
import tempfile
import zipfile

MAX_ZIP = 1024**3
MAX_TOTAL = 2 * 1024**3
MAX_FILES = 20000
VERSION = "0.14.0"
HEX = re.compile(r"[0-9a-f]{64}")
NAME = re.compile(r"[A-Za-z0-9._+@= -]+")
RESERVED = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"} | {f"{p}{i}" for p in ("COM", "LPT") for i in range(1, 10)}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def safe_name(name):
    parts = name.split("/")
    require(len(name) <= 220 and all(NAME.fullmatch(p) and p not in (".", "..") and p == p.strip() and not p.endswith(".") and p.split(".")[0].upper() not in RESERVED for p in parts), "Unsafe Windows path")
    return parts


def inventory(z):
    infos = z.infolist()
    require(0 < len(infos) <= MAX_FILES, "Invalid file count")
    files, dirs = {}, {}
    total = 0
    for info in infos:
        parts = safe_name(info.filename)
        mode = stat.S_IFMT(info.external_attr >> 16)
        require(not info.is_dir() and mode in (0, stat.S_IFREG) and not info.flag_bits & 1 and info.compress_type in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED), "Unsupported ZIP entry")
        key = info.filename.casefold()
        require(key not in files and key not in dirs, "Duplicate or conflicting path")
        for i in range(1, len(parts)):
            folder = "/".join(parts[:i])
            k = folder.casefold()
            require(k not in files and dirs.get(k, folder) == folder, "Conflicting directory")
            dirs[k] = folder
        files[key] = info.filename
        total += info.file_size
        require(total <= MAX_TOTAL, "Expanded archive too large")
    require(files.get("lilium.exe") == "Lilium.exe" and any(k.startswith("_internal/") for k in files), "Missing portable bundle files")
    return infos


def digest(stream):
    stream.seek(0)
    h = hashlib.sha256()
    size = 0
    for chunk in iter(lambda: stream.read(1024 * 1024), b""):
        size += len(chunk)
        require(size <= MAX_ZIP, "Archive too large")
        h.update(chunk)
    stream.seek(0)
    return h.hexdigest(), size


def manifest(archive, commit, version=VERSION):
    require(re.fullmatch(r"[0-9a-f]{40}", commit) and re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}", version), "Invalid release identifiers")
    with Path(archive).open("rb") as stream:
        sha, size = digest(stream)
    return {"schema_version": "1.0", "kind": "lilium.portable", "version": version, "platform": "windows-x64", "channel": "preview", "commit": commit, "filename": f"Lilium-{version}-windows-x64-preview.zip", "sha256": sha, "bytes": size}


def read_manifest(path):
    with Path(path).open("rb") as stream:
        raw = stream.read(8193)
    require(len(raw) <= 8192, "Manifest too large")
    m = json.loads(raw)
    fields = {"schema_version", "kind", "version", "platform", "channel", "commit", "filename", "sha256", "bytes"}
    require(isinstance(m, dict) and set(m) == fields, "Invalid manifest")
    require(m["schema_version"] == "1.0" and m["kind"] == "lilium.portable" and m["platform"] == "windows-x64" and m["channel"] == "preview", "Unsupported release")
    require(all(isinstance(m[k], str) for k in fields - {"bytes"}), "Invalid manifest types")
    require(re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}", m["version"]) and re.fullmatch(r"[0-9a-f]{40}", m["commit"]) and HEX.fullmatch(m["sha256"]) and m["filename"] == f"Lilium-{m['version']}-windows-x64-preview.zip" and type(m["bytes"]) is int and 0 < m["bytes"] <= MAX_ZIP, "Invalid release metadata")
    return m


def check(stream, m, trusted_sha):
    require(isinstance(trusted_sha, str) and HEX.fullmatch(trusted_sha), "Provide an independently trusted lowercase SHA-256")
    sha, size = digest(stream)
    require(sha == trusted_sha == m["sha256"] and size == m["bytes"], "Archive integrity check failed")


def verify(archive, manifest_path, trusted_sha):
    m = read_manifest(manifest_path)
    require(Path(archive).name == m["filename"], "Unexpected archive name")
    with Path(archive).open("rb") as stream:
        check(stream, m, trusted_sha)
        with zipfile.ZipFile(stream) as z:
            inventory(z)
    return m


def stage(archive, manifest_path, trusted_sha, parent):
    m = read_manifest(manifest_path)
    require(Path(archive).name == m["filename"], "Unexpected archive name")
    with Path(archive).open("rb") as stream:
        check(stream, m, trusted_sha)
        with zipfile.ZipFile(stream) as z:
            infos = inventory(z)
            folder = Path(tempfile.mkdtemp(prefix=f"Lilium-{m['version']}-", dir=parent))
            try:
                for info in infos:
                    target = folder.joinpath(*safe_name(info.filename))
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with z.open(info) as src, target.open("xb") as dst:
                        shutil.copyfileobj(src, dst, 1024 * 1024)
                check(stream, m, trusted_sha)
            except BaseException:
                shutil.rmtree(folder)
                raise
    return folder


def package(source, output, commit, version=VERSION):
    source, output = Path(source).resolve(), Path(output).resolve()
    require(source.is_dir() and not output.is_relative_to(source), "Choose a separate output directory")
    require(re.fullmatch(r"[0-9a-f]{40}", commit) and re.fullmatch(r"\d{1,3}\.\d{1,3}\.\d{1,3}", version), "Invalid release identifiers")
    output.mkdir()
    try:
        archive = output / f"Lilium-{version}-windows-x64-preview.zip"
        total = count = 0
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for p in sorted(source.rglob("*")):
                require(not p.is_symlink() and not (hasattr(p, "is_junction") and p.is_junction()), "Links are not supported")
                if p.is_dir():
                    continue
                require(p.is_file(), "Unsupported source file")
                name = p.relative_to(source).as_posix()
                safe_name(name)
                total += p.stat().st_size
                count += 1
                require(total <= MAX_TOTAL and count <= MAX_FILES, "Bundle exceeds limits")
                z.write(p, name)
            inventory(z)
        m = manifest(archive, commit, version)
        (output / "manifest.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
        (output / "SHA256SUMS.txt").write_text(m["sha256"] + "  " + m["filename"] + "\n", encoding="ascii")
        return m
    except BaseException:
        shutil.rmtree(output)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("package")
    for name in ("source", "output", "commit"):
        p.add_argument("--" + name, required=True)
    for command in ("verify", "stage"):
        p = sub.add_parser(command)
        for name in ("archive", "manifest", "sha256"):
            p.add_argument("--" + name, required=True)
        if command == "stage":
            p.add_argument("--parent", required=True)
    a = parser.parse_args(argv)
    try:
        if a.command == "package":
            result = package(a.source, a.output, a.commit)
        elif a.command == "verify":
            result = verify(a.archive, a.manifest, a.sha256)
        else:
            result = {"staged_folder": str(stage(a.archive, a.manifest, a.sha256, a.parent)), "executed": False}
        print(json.dumps(result, indent=2))
        return 0
    except (ValueError, OSError, zipfile.BadZipFile, RuntimeError) as exc:
        print("Release operation failed: " + str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
