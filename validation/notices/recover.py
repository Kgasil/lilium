"""Recover explicit upstream notices from exact PyPI source archives, without executing packages."""
import hashlib, io, json, re, tarfile, sys, zipfile
from pathlib import Path, PurePosixPath
from urllib.request import urlopen
from urllib.parse import urlsplit
PINS=[
 ("openpyxl","3.1.5","openpyxl-3.1.5.tar.gz","cf0e3cf56142039133628b5acffe8ef0c12bc902d2aadd3e0fe5878dc08d1050"),
 ("et-xmlfile","2.0.0","et_xmlfile-2.0.0.tar.gz","dab3f4764309081ce75662649be815c4c9081e88f0837825f90fd28317d4da54"),
]
WHEEL_PINS={
 "openpyxl":("openpyxl-3.1.5-py2.py3-none-any.whl","5282c12b107bffeef825f4617dc029afaf41d0ea60823bbb665ef3079dc79de2"),
 "et-xmlfile":("et_xmlfile-2.0.0-py3-none-any.whl","7a91720bc756843502c3b7504c77b8fe44217c85c537d85037f0f536151b2caa"),
}
def require(ok,msg):
    if not ok: raise ValueError(msg)
def digest(raw): return hashlib.sha256(raw).hexdigest()
def read(url,host,limit):
    require(urlsplit(url).scheme=="https" and urlsplit(url).hostname==host,"unexpected URL")
    with urlopen(url,timeout=30) as response:
        require(urlsplit(response.geturl()).scheme=="https" and urlsplit(response.geturl()).hostname==host,"unexpected redirect")
        raw=response.read(limit+1)
    require(len(raw)<=limit,"oversized download")
    return raw
def notices(raw,filename,expected):
    require(digest(raw)==expected,"source archive hash mismatch")
    records={}
    candidates=[]
    with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as z:
        for m in z:
            p=PurePosixPath(m.name)
            if not m.isfile(): continue
            if re.search(r"licen[cs]e|copying|notice|copyright|authors",p.name,re.I): candidates.append(m.name)
            if len(p.parts)!=2 or p.parts[0]!=filename.removesuffix(".tar.gz"): continue
            if not re.fullmatch(r"(LICEN[CS]E|COPYING|NOTICE|COPYRIGHT|AUTHORS)([._-].*)?",p.name,re.I): continue
            require(p.name not in records and 0<m.size<=262144,"invalid notice member")
            data=z.extractfile(m).read()
            require(len(data)==m.size,"truncated notice")
            records[p.name]=data
    print(filename,"notice-like paths:",json.dumps(candidates),flush=True)
    require(any(re.match(r"(LICEN[CS]E|COPYING)",n,re.I) for n in records),"no explicit root license text")
    return records
def inspect_wheel(raw,expected,source_notices):
    require(digest(raw)==expected,"wheel digest mismatch")
    rows=[]
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos=z.infolist()
        require(len({m.filename for m in infos})==len(infos),"duplicate wheel entry")
        require(sum(m.file_size for m in infos)<=32*1024*1024,"oversized wheel contents")
        require(z.testzip() is None,"wheel CRC mismatch")
        for m in infos:
            p=PurePosixPath(m.filename)
            if m.is_dir() or not re.fullmatch(r"(LICEN[CS]E|COPYING|NOTICE|COPYRIGHT|AUTHORS)([._-].*)?",p.name,re.I): continue
            require(not p.is_absolute() and ".." not in p.parts and 0<m.file_size<=262144,"invalid wheel notice")
            data=z.read(m)
            rows.append({"member":m.filename,"sha256":digest(data),"size":len(data),"collector_eligible":p.parts[0].endswith(".dist-info"),"exact_source_matches":[name for name,original in sorted(source_notices.items()) if original==data]})
    matched={name for row in rows if row["collector_eligible"] for name in row["exact_source_matches"]}
    return {"notices":rows,"source_notices_not_exactly_covered_by_collector":sorted(set(source_notices)-matched),"scope":"official wheel bytes only, not installed build or final ZIP"}
def main():
    out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
    results=[]
    for name,version,filename,expected in PINS:
        source=f"https://pypi.org/pypi/{name}/{version}/json"
        meta=json.loads(read(source,"pypi.org",2*1024*1024))
        files=[x for x in meta["urls"] if x["filename"]==filename and x["packagetype"]=="sdist"]
        require(len(files)==1 and files[0]["digests"]["sha256"]==expected,"unexpected release digest")
        raw=read(files[0]["url"],"files.pythonhosted.org",2*1024*1024)
        found=notices(raw,filename,expected)
        rows=[]
        for member,data in sorted(found.items()):
            dest=f"{name}-{version}-{member}"
            (out/dest).write_bytes(data)
            rows.append({"file":dest,"member":member,"sha256":digest(data),"size":len(data)})
        wheel_name,wheel_sha=WHEEL_PINS[name]
        wheels=[x for x in meta["urls"] if x["filename"]==wheel_name and x["packagetype"]=="bdist_wheel"]
        require(len(wheels)==1 and wheels[0]["digests"]["sha256"]==wheel_sha,"unexpected wheel digest")
        wheel=inspect_wheel(read(wheels[0]["url"],"files.pythonhosted.org",2*1024*1024),wheel_sha,found)
        wheel.update({"filename":wheel_name,"sha256":wheel_sha,"url":wheels[0]["url"]})
        print(name,"wheel notice coverage:",json.dumps(wheel),flush=True)
        results.append({"wheel":wheel,"package":name,"version":version,"source_url":files[0]["url"],"source_sha256":expected,"notices":rows,"status":"UPSTREAM_TEXT_RECOVERED"})
        print(name,version,"verified source archive; explicit notice files:",len(rows))
    (out/"report.json").write_text(json.dumps({"schema":"lilium.upstream-notice-recovery.v1","results":results,"package_inclusion":"NOT_TESTED","license_clearance":"NOT_TESTED","release_approved":False},indent=2)+"\n",encoding="utf-8")
if __name__=="__main__":main()
