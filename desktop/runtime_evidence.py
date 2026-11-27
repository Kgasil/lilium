"""Candidate-only Windows runtime evidence, not antivirus or licensing approval."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import sqlite3
import ssl
import sys

EXPECTED={"python":"3.14.10","openssl":"3.5.9","sqlite":"3.50.4"}
NAMES=("python314.dll","libcrypto-3.dll","libssl-3.dll","sqlite3.dll")

def require(condition, message):
    if not condition:
        raise ValueError(message)

def runtime():
    observed={"python":platform.python_version(),"openssl":".".join(map(str,ssl.OPENSSL_VERSION_INFO[:3])),"sqlite":sqlite3.sqlite_version}
    require(sys.platform=="win32" and platform.machine().upper() in {"AMD64","X86_64"} and sys.maxsize>2**32,"Windows x64 required")
    require(observed==EXPECTED,"unexpected runtime: "+str(observed))
    with sqlite3.connect(":memory:") as db:
        require(db.execute("PRAGMA integrity_check").fetchone()==("ok",),"SQLite integrity")
        db.execute("CREATE TABLE demo (value INTEGER)")
        db.execute("INSERT INTO demo VALUES (42)")
        require(db.execute("SELECT value FROM demo").fetchone()==(42,),"SQLite query")
    require(ssl.create_default_context().verify_mode==ssl.CERT_REQUIRED,"TLS verification")
    return observed

def hash_file(p):
    with p.open("rb") as f: return hashlib.file_digest(f,"sha256").hexdigest()

def source_files(root):
    result={}
    for name in NAMES:
        found=[p for p in (root/name,root/"DLLs"/name) if p.is_file()]
        require(len(found)==1,"source DLL missing or ambiguous: "+name)
        result[name]={"sha256":hash_file(found[0]),"size":found[0].stat().st_size}
    return result

def compare_bundle(root,expected):
    result={}
    for name in NAMES:
        found=[p for p in root.rglob(name) if p.is_file()]
        require(len(found)==1,"bundle DLL missing or ambiguous: "+name)
        actual={"sha256":hash_file(found[0]),"size":found[0].stat().st_size}
        require(actual==expected[name],"bundle DLL mismatch: "+name)
        result[name]={**actual,"path":found[0].relative_to(root).as_posix()}
    require(not any(root.rglob("python312.dll")),"old Python DLL retained")
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("output",type=Path)
    p.add_argument("--bundle",type=Path)
    a=p.parse_args()
    observed=runtime()
    sources=source_files(Path(sys.base_prefix))
    report={"schema":"lilium.runtime-evidence.v1","versions":observed,"source_dlls":sources,"bundle_dlls":None,"release_approved":False,"malware_scan":"NOT_TESTED","license_clearance":"NOT_TESTED"}
    if a.bundle: report["bundle_dlls"]=compare_bundle(a.bundle,sources)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print("Runtime evidence PASS:",observed,"bundle matched:",bool(a.bundle))
if __name__=="__main__": main()
