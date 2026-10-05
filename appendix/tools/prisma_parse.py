#!/usr/bin/env python3
"""Read-only Prisma schema parser -> JSON. Usage: prisma_parse.py <snapshot_root> <out.json>"""
import json, re, sys, glob, os

SCALARS = {"String","Int","BigInt","Float","Decimal","Boolean","DateTime","Json","Bytes"}

def parse(path):
    lines = open(path, encoding="utf-8").read().split("\n")
    models, enums = {}, {}
    cur, kind, start = None, None, 0
    for i, raw in enumerate(lines, 1):
        line = raw.split("//")[0].rstrip() if "//" in raw and not raw.strip().startswith("///") else raw.rstrip()
        s = line.strip()
        m = re.match(r"^(model|enum|view)\s+(\w+)\s*\{", s)
        if m:
            kind, name = m.group(1), m.group(2)
            cur = {"name": name, "line": i, "fields": [], "attrs": [], "values": []}
            (models if kind in ("model","view") else enums)[name] = cur
            cur["kind"] = kind
            continue
        if cur is None:
            continue
        if s == "}":
            cur["end"] = i; cur = None; continue
        if not s:
            continue
        if kind == "enum":
            v = s.split()[0]
            if not v.startswith("@@"):
                cur["values"].append(v)
            continue
        if s.startswith("@@"):
            cur["attrs"].append({"text": s, "line": i}); continue
        fm = re.match(r"^(\w+)\s+([\w]+)(\[\])?(\?)?\s*(.*)$", s)
        if not fm:
            continue
        fname, ftype, arr, opt, rest = fm.groups()
        f = {"name": fname, "type": ftype, "list": bool(arr), "optional": bool(opt), "line": i, "attrs": rest}
        dm = re.search(r"@default\(((?:[^()]|\([^()]*\))*)\)", rest); f["default"] = dm.group(1) if dm else None
        f["id"] = "@id" in rest
        f["unique"] = "@unique" in rest
        mm = re.search(r'@map\("([^"]+)"\)', rest); f["column"] = mm.group(1) if mm else fname
        nt = re.search(r"@db\.(\w+(?:\([^)]*\))?)", rest); f["dbType"] = nt.group(1) if nt else None
        rm = re.search(r"@relation\(([^)]*)\)", rest)
        if rm:
            r = rm.group(1)
            fl = re.search(r"fields:\s*\[([^\]]*)\]", r); rf = re.search(r"references:\s*\[([^\]]*)\]", r)
            od = re.search(r"onDelete:\s*(\w+)", r); nm = re.search(r'"([^"]+)"', r)
            f["relation"] = {"fields": [x.strip() for x in fl.group(1).split(",")] if fl else [],
                             "references": [x.strip() for x in rf.group(1).split(",")] if rf else [],
                             "onDelete": od.group(1) if od else None, "name": nm.group(1) if nm else None}
        cur["fields"].append(f)
    for m in models.values():
        mp = [a for a in m["attrs"] if a["text"].startswith("@@map")]
        m["table"] = re.search(r'"([^"]+)"', mp[0]["text"]).group(1) if mp else m["name"]
        m["indexes"] = [a for a in m["attrs"] if a["text"].startswith(("@@index","@@unique","@@id"))]
    return models, enums

def main(root, out):
    res = {}
    for p in sorted(glob.glob(os.path.join(root, "apps/*/prisma/schema.prisma"))):
        svc = p.split("/apps/")[1].split("/")[0]
        models, enums = parse(p)
        res[svc] = {"path": os.path.relpath(p, root), "models": models, "enums": enums}
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)
    for s, d in res.items():
        print(s, len(d["models"]), "models", len(d["enums"]), "enums")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
