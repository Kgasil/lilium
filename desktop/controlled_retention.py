"""Offline owner-controlled handoff. Copies reviewed bytes; never grants release approval."""
import argparse
import hashlib
import json
from pathlib import Path
import os
import re
import shutil
import tempfile
import subprocess
from datetime import datetime, timezone

HEX=re.compile(r"[0-9a-f]{64}")
REQUIRED={"manifest","inventory","notices","defender","clamav","rights","authorization"}

def require(ok,msg):
    if not ok: raise ValueError(msg)

def digest(p):
    require(p.is_file() and not p.is_symlink(),"regular non-link file required")
    with p.open("rb") as f: return hashlib.file_digest(f,"sha256").hexdigest()

def verify_windows_acl(path, root=False):
    # Read-only check. No execution-policy override, ACL modification or network access.
    system=Path(os.environ.get("SystemRoot", r"C:\\Windows"))
    exe=system/"System32"/"WindowsPowerShell"/"v1.0"/"powershell.exe"
    script=Path(__file__).with_name("retention_acl.ps1")
    args=[str(exe),"-NoProfile","-NonInteractive","-File",str(script),"-Path",str(path)]
    if root: args.append("-Root")
    proc=subprocess.run(args,capture_output=True,text=True,timeout=30)
    require(proc.returncode==0 and proc.stdout.strip()=="ACL_PASS","Windows retention ACL check failed: "+proc.stderr.strip()[:500])

def retain(archive,review,root,expected):
    archive,review,root=map(Path,(archive,review,root))
    require(isinstance(expected,str) and HEX.fullmatch(expected),"trusted SHA-256 required")
    require(root.is_dir() and not root.is_symlink(),"existing owner-controlled directory required")
    require(not hasattr(root,"is_junction") or not root.is_junction(),"junction refused")
    if os.name=="nt":
        verify_windows_acl(root,root=True)
    elif os.name=="posix":
        require(root.stat().st_uid==os.getuid() and root.stat().st_mode&0o077==0,"directory must be owner-only")
    else:
        raise ValueError("Unsupported retention OS")
    require(review.is_file() and not review.is_symlink() and review.stat().st_size<=65536,"review record required")
    raw=review.read_bytes()
    r=json.loads(raw)
    require(r.get("schema")==1 and r.get("candidate_sha256")==expected and r.get("owner_authorized_retention") is True and r.get("reviewed_full_current_scans") is True and r.get("rights_reviewed_for_controlled_handoff") is True and r.get("access_restricted_confirmed") is True and r.get("release_approved") is False,"explicit owner review required")
    require(digest(archive)==expected,"candidate hash mismatch")
    evidence=r.get("evidence")
    require(isinstance(evidence,dict) and set(evidence)==REQUIRED,"required evidence missing")
    files=[]
    for role,row in evidence.items():
        name=row.get("name","")
        require(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{0,120}",name) is not None and name not in (".",".."),"invalid evidence name")
        p=review.parent/name
        require(HEX.fullmatch(row.get("sha256","")) and digest(p)==row["sha256"],"evidence hash mismatch: "+role)
        files.append((role,p,row["sha256"]))
    final=root/expected
    require(not final.exists() and not final.is_symlink(),"existing retained candidate; never overwrite")
    temp=Path(tempfile.mkdtemp(prefix=".handoff-",dir=root))
    try:
        if os.name=="nt": verify_windows_acl(temp)
        def copy_checked(p,to,h):
            with p.open("rb") as src,to.open("xb") as dst: shutil.copyfileobj(src,dst)
            require(digest(to)==h and digest(p)==h,"copy/source hash mismatch")
        copy_checked(archive,temp/"candidate.zip",expected)
        for role,p,h in files: copy_checked(p,temp/(role+".evidence"),h)
        (temp/"review.json").write_bytes(raw)
        (temp/"retention.json").write_text(json.dumps({"schema":1,"sha256":expected,"retained_utc":datetime.now(timezone.utc).isoformat(),"release_approved":False,"scope":"owner attestations and byte integrity only; not independent AV or legal verification"},indent=2),encoding="utf-8")
        if os.name=="nt":
            verify_windows_acl(root,root=True)
            for p in temp.iterdir(): verify_windows_acl(p)
        require(not final.exists(),"candidate already retained")
        temp.rename(final)
    except BaseException:
        shutil.rmtree(temp)
        raise
    return final

def main():
    p=argparse.ArgumentParser(description=__doc__)
    for x in ("archive","review","root","sha256"): p.add_argument("--"+x,required=True)
    a=p.parse_args()
    print(retain(a.archive,a.review,a.root,a.sha256))
if __name__=="__main__": main()
