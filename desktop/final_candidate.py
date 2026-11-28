"""Exact final candidate checks. No signing, publication or automatic legal approval."""
import argparse,hashlib,json,re,zipfile
from pathlib import Path
from desktop.release_manager import read_manifest,verify
HEX=re.compile(r"[0-9a-f]{64}")

def require(ok,msg):
    if not ok: raise ValueError(msg)
def read(p): return json.loads(Path(p).read_text(encoding="utf-8-sig"))
def sha(p):
    require(p.is_file() and not p.is_symlink(),"regular file required")
    with p.open("rb") as f: return hashlib.file_digest(f,"sha256").hexdigest()
def inventory(bundle):
    result={}
    for p in sorted(bundle.rglob("*")):
        require(not p.is_symlink() and not (hasattr(p,"is_junction") and p.is_junction()),"link in bundle")
        if p.is_dir(): continue
        name=p.relative_to(bundle).as_posix()
        result[name]={"sha256":sha(p),"bytes":p.stat().st_size}
    require("Lilium.exe" in result and "TERMS-REVIEW.txt" in result and "NOTICES/index.json" in result,"missing candidate components")
    return result
def rights(inventory_report,review):
    require(review.get("schema")==1 and review.get("owner_reviewed_applicable_rights") is True and review.get("release_approved") is False,"reviewed source rights record required")
    expected=review.get("files")
    require(isinstance(expected,dict) and bool(expected),"reviewed Microsoft file map missing")
    actual={}
    for row in inventory_report["files"]:
        name=Path(row["path"].replace("\\","/")).name.lower()
        require(name not in actual,"duplicate runtime DLL")
        require(row["signature_status"]=="Valid" and row["matching_python_source_paths"] and HEX.fullmatch(row["sha256"]),"unverified Microsoft DLL source")
        require("Microsoft Corporation" in row["signer"],"unexpected signer")
        actual[name]=row["sha256"]
    require(actual==expected,"Microsoft runtime bytes differ from reviewed source list")
def snapshot(bundle,archive,manifest_path,commit,output):
    m=read_manifest(manifest_path)
    require(m["commit"]==commit,"manifest commit mismatch")
    verify(archive,manifest_path,m["sha256"])
    rows=inventory(bundle)
    with zipfile.ZipFile(archive) as z:
        require(set(z.namelist())==set(rows),"archive/bundle inventory mismatch")
        for name,row in rows.items():
            with z.open(name) as f:
                h=hashlib.file_digest(f,"sha256").hexdigest()
            require(h==row["sha256"] and z.getinfo(name).file_size==row["bytes"],"archive file mismatch: "+name)
    data={"schema":1,"commit":commit,"archive_sha256":m["sha256"],"archive_bytes":m["bytes"],"files":rows,"release_approved":False}
    Path(output).write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    return data
def main():
    p=argparse.ArgumentParser();p.add_argument("mode",choices=["rights","snapshot"])
    p.add_argument("paths",nargs="+");a=p.parse_args()
    if a.mode=="rights":
        rights(read(a.paths[0]),read(a.paths[1]))
        print("Actual named Microsoft runtime bytes match owner-reviewed sources; not legal certification")
    else:
        bundle,archive,manifest,commit,output=a.paths
        snapshot(Path(bundle),Path(archive),Path(manifest),commit,output)
if __name__=="__main__":main()
