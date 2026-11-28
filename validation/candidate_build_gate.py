"""Authorize one isolated build only; owner attestations are not independent legal/AV proof."""
import json,re,subprocess,sys
from pathlib import Path
AUTH="validation/candidate-authorization.json"
FIELDS={"schema","source_commit","owner_authorized_build","owner_reviewed_terms","microsoft_entitlement_reviewed","controlled_retention_authorized","release_approved"}

def validate(row, parent, changed):
    if (not isinstance(row,dict) or set(row)!=FIELDS or type(row["schema"]) is not int or row["schema"]!=1
        or not re.fullmatch(r"[0-9a-f]{40}",parent) or row["source_commit"]!=parent
        or changed!=[AUTH] or row["release_approved"] is not False
        or any(row[k] is not True for k in ("owner_authorized_build","owner_reviewed_terms","microsoft_entitlement_reviewed","controlled_retention_authorized"))):
        raise ValueError("Explicit authorization for exact parent, with authorization-only commit, required")

def git(*args):
    return subprocess.check_output(["git",*args],text=True).strip()

def main():
    if git("rev-list","--parents","-n","1","HEAD").count(" ")!=1: raise ValueError("Single-parent authorization commit required")
    parent=git("rev-parse","HEAD^")
    changed=git("diff","--name-only","HEAD^","HEAD").splitlines()
    p=Path(AUTH)
    if p.is_symlink() or not p.is_file() or p.stat().st_size>8192: raise ValueError("Invalid authorization file")
    row=json.loads(p.read_text(encoding="utf-8"))
    validate(row,parent,changed)
    print("Owner attestation for exact source parent verified; build only, no release approval.")

if __name__=="__main__":
    try: main()
    except (ValueError,OSError,subprocess.CalledProcessError) as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
