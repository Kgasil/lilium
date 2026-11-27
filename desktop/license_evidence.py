"""Collect exact license texts for a controlled build; not redistribution clearance."""
import argparse
import hashlib
import importlib.metadata as md
import json
from pathlib import Path
import re
import sys
import zipfile

UPSTREAM=Path(__file__).resolve().parent / "third_party_notices"
def require(ok,msg):
    if not ok: raise ValueError(msg)

def sha(data): return hashlib.sha256(data).hexdigest()

def git_blob(data): return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def is_notice_name(name):
    return re.fullmatch(r"(LICEN[CS]E|COPYING|NOTICE|COPYRIGHT|AUTHORS)([._-].*)?",name,re.I) is not None

def copy_notice(dest,name,data,origin):
    require(re.fullmatch(r"[A-Za-z0-9._-]+",name) is not None and name not in {".",".."},"unsafe notice name")
    require(0<len(data)<=2*1024*1024,"empty or oversized notice")
    target=dest/name
    with target.open("xb") as stream: stream.write(data)
    return {"path":"NOTICES/"+name,"sha256":sha(data),"bytes":len(data),"source":origin}

def upstream_bytes(path,expected):
    raw=path.read_bytes()
    # Windows Git may materialize CRLF. Restore original bytes only when the
    # resulting bytes match the known upstream Git blob.
    if git_blob(raw)!=expected: raw=raw.replace(b"\r\n",b"\n")
    require(git_blob(raw)==expected,"upstream notice blob mismatch")
    return raw

def collect(bundle,evidence):
    require((bundle/"Lilium.exe").is_file() and (bundle/"_internal").is_dir(),"bundle missing")
    require(sys.version_info[:3]==(3,14,10),"unexpected Python version")
    dest=bundle/"NOTICES"
    dest.mkdir()
    installed=Path(sys.base_prefix)/"LICENSE.txt"
    require(installed.is_file() and not installed.is_symlink(),"installed Python license missing")
    records=[copy_notice(dest,"python-3.14.10-installed.txt",installed.read_bytes(),"LICENSE.txt from verified official CPython installation")]
    for item in json.loads((UPSTREAM/"sources.json").read_text(encoding="utf-8")):
        records.append(copy_notice(dest,item["name"],upstream_bytes(UPSTREAM/item["name"],item["blob"]),item["source"]))
    packages=[]
    seq=0
    for dist in sorted(md.distributions(),key=lambda d:(d.metadata.get("Name","").lower(),d.version)):
        name=dist.metadata.get("Name","")
        root=Path(dist.locate_file("")).resolve()
        found=[]
        for f in sorted(dist.files or [],key=str):
            parts=f.parts
            if not parts or not parts[0].endswith(".dist-info") or any(p in {".",".."} for p in parts): continue
            if not ("licenses" in parts[1:-1] or is_notice_name(f.name)): continue
            p=Path(dist.locate_file(f))
            require(p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(root),"invalid distribution notice")
            seq+=1
            row=copy_notice(dest,f"package-{seq:04d}.txt",p.read_bytes(),f"{name}=={dist.version}:{f.as_posix()}")
            records.append(row);found.append(row["path"])
        packages.append({"name":name,"version":dist.version,"license_expression":dist.metadata.get("License-Expression"),"license_files":found,"status":"TEXT_COLLECTED" if found else "REVIEW_REQUIRED"})
    index={"schema":"lilium.notice-evidence.v1","scope":"Installed CPython and upstream reference notices plus available build-environment distribution notices; not proof all packages shipped or all embedded licenses covered","notices":records,"build_environment":packages,"outstanding":["complete embedded component/license mapping","SQLite provenance/public-domain dedication and extensions","Microsoft runtime redistribution entitlement","XZ and other applicable source/notice obligations","first-party terms"],"license_clearance":"NOT_TESTED","release_approved":False}
    raw=(json.dumps(index,indent=2,ensure_ascii=False)+"\n").encode("utf-8")
    (dest/"index.json").write_bytes(raw)
    evidence.parent.mkdir(parents=True,exist_ok=True);evidence.write_bytes(raw)
    print("Notices collected:",len(records),"build environment distributions:",len(packages),"missing explicit notices:",sum(not p["license_files"] for p in packages))
def verify_archive(archive,evidence):
    raw=evidence.read_bytes();index=json.loads(raw)
    with zipfile.ZipFile(archive) as z:
        require(z.read("NOTICES/index.json")==raw,"notice index mismatch")
        for r in index["notices"]:
            require(z.namelist().count(r["path"])==1,"duplicate or missing notice")
            data=z.read(r["path"])
            require(len(data)==r["bytes"] and sha(data)==r["sha256"],"notice mismatch")
    print("Packaged notice hash verification PASS:",len(index["notices"]))
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("mode",choices=["collect","verify"]);p.add_argument("target",type=Path);p.add_argument("evidence",type=Path);a=p.parse_args()
    if a.mode=="collect": collect(a.target,a.evidence)
    else: verify_archive(a.target,a.evidence)
if __name__=="__main__": main()
