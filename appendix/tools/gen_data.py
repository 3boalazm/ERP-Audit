#!/usr/bin/env python3
"""Generate data dictionary, ERDs (mermaid), schema diff and heuristic schema-gap checks from parsed JSON."""
import json, os, re, collections
B = "/home/claude/audit"
cur = json.load(open(f"{B}/data/schema_cur.json"))
base = json.load(open(f"{B}/data/schema_base.json"))
OUT = f"{B}/out"
os.makedirs(f"{OUT}/diagrams/erd", exist_ok=True)

SCAL = {"String","Int","BigInt","Float","Decimal","Boolean","DateTime","Json","Bytes"}
MONEY = re.compile(r"(amount|total|price|cost|balance|paid|debit|credit|tax|vat|discount|fee|salary|net|gross|value|rate|limit|exposure|commission|outstanding|subtotal)", re.I)

def ftype(f):
    t = f["type"] + ("[]" if f["list"] else "") + ("?" if f["optional"] else "")
    if f["dbType"]: t += f" @db.{f['dbType']}"
    return t

def is_rel(f, models, enums):
    return f["type"] in models

# ---------- Data dictionary ----------
dd = ["# Data Dictionary — Nile Pharma ERP (CURRENT fa40270, مع تمييز ما يختلف عن BASELINE 89c2c31)", "",
      "مُولّد آليًا من `apps/*/prisma/schema.prisma` (قراءة فقط). العمود **B?** = هل الحقل موجود في BASELINE 89c2c31 (✓ موجود، ✗ غير موجود/مضاف لاحقًا).",
      "PK=@id, U=@unique, FK=علاقة Prisma فعلية (@relation fields)، LREF=مرجع منطقي (حقل *Id بلا @relation) — لا يوجد FK في القاعدة له إلا إذا أنشأته migration يدويًا.", ""]
stats = []
for svc in sorted(cur):
    d = cur[svc]; bd = base.get(svc, {"models": {}, "enums": {}})
    dd += [f"## خدمة `{svc}` — DB `nile_{svc.replace('audit-aggregator','audit')}`", f"المصدر: `{d['path']}`", ""]
    for mn in sorted(d["models"], key=lambda x: d["models"][x]["line"]):
        m = d["models"][mn]; bm = bd["models"].get(mn)
        tag = "" if bm else " **(CURRENT فقط)**"
        dd += [f"### {mn} → `{m['table']}`{tag}", f"`{d['path']}:{m['line']}`", "",
               "| Field | Column | Type | Null | Default | Key | B? |", "|---|---|---|---|---|---|---|"]
        bfields = {f["name"]: f for f in bm["fields"]} if bm else {}
        for f in m["fields"]:
            if f["type"] in d["models"] and not f.get("relation"):
                continue  # back-relation list
            key = []
            if f["id"]: key.append("PK")
            if f["unique"]: key.append("U")
            if f.get("relation"): key.append(f"FK→{f['type']}({','.join(f['relation']['references'])}) onDelete={f['relation']['onDelete'] or 'default'}")
            elif f["name"].endswith("Id") and f["type"] in ("String","Int") and not f["id"]:
                # is it the fields side of a relation?
                used = any(f["name"] in (g.get("relation") or {}).get("fields", []) for g in m["fields"])
                key.append("FK-col" if used else "LREF")
            if f["type"] in d["models"] and f.get("relation"):
                continue_row = True
            b = "✓" if f["name"] in bfields else ("✗" if bm else "—")
            dflt = (f["default"] or "").replace("|", "\\|")
            dd.append(f"| {f['name']} | {f['column']} | {ftype(f)} | {'Y' if f['optional'] else 'N'} | {dflt} | {' '.join(key)} | {b} |")
        if m["indexes"]:
            dd.append("")
            dd.append("Indexes/constraints: " + "; ".join(f"`{a['text']}`" for a in m["indexes"]))
        if bm:
            removed = [n for n in bfields if n not in {f['name'] for f in m['fields']}]
            if removed: dd.append(f"\n⚠️ حقول في BASELINE أزيلت في CURRENT: {', '.join(removed)}")
        dd.append("")
    if d["enums"]:
        dd += [f"#### Enums ({svc})", "| Enum | Values | B? |", "|---|---|---|"]
        for en, e in d["enums"].items():
            be = bd["enums"].get(en)
            diff = "" if not be else (" (+" + ",".join(v for v in e["values"] if v not in be["values"]) + ")" if set(e["values"]) - set(be["values"]) else "")
            dd.append(f"| {en} | {', '.join(e['values'])} | {'✓'+diff if be else '✗'} |")
        dd.append("")
open(f"{OUT}/07-Data-Dictionary.md", "w").write("\n".join(dd))

# ---------- ERDs ----------
def erd(svc, d, only=None, title=None):
    lines = ["erDiagram"]
    models = d["models"]
    names = [n for n in models if (only is None or n in only)]
    for mn in names:
        m = models[mn]
        lines.append(f"  {mn} {{")
        for f in m["fields"]:
            if f["type"] in models or f["list"] and f["type"] not in SCAL and f["type"] not in d["enums"]:
                continue
            t = f["type"] if f["type"] in SCAL else "enum"
            k = "PK" if f["id"] else ("FK" if any(f["name"] in (g.get("relation") or {}).get("fields", []) for g in m["fields"]) else ("UK" if f["unique"] else ""))
            if not (f["id"] or k or f["name"].endswith("Id") or f["name"] in ("status","number","code","name","totalAmount","amount","createdAt","deletedAt")):
                continue
            lines.append(f"    {t} {f['name']} {k}".rstrip())
        lines.append("  }")
    seen = set()
    for mn in names:
        for f in models[mn]["fields"]:
            r = f.get("relation")
            if r and r["fields"] and f["type"] in names:
                tgt = f["type"]
                # cardinality: child (mn) many-to-one parent unless fk field unique
                uniq = any(g["name"] in r["fields"] and g["unique"] for g in models[mn]["fields"])
                card = "|o--o|" if uniq else "}o--||"
                if f["optional"]: card = card.replace("||", "o|") if not uniq else card
                key = (mn, tgt, f["name"])
                if key in seen: continue
                seen.add(key)
                lines.append(f"  {tgt} {card[::-1].replace('o}','{o').replace('|o','o|') if False else ''}" if False else f"  {mn} {card} {tgt} : \"{f['name']}\"")
    return "\n".join(lines)

erd_index = []
for svc, d in cur.items():
    txt = erd(svc, d)
    open(f"{OUT}/diagrams/erd/erd-{svc}.mmd", "w").write(txt)
    erd_index.append(svc)

# ---------- relationship stats & logical refs ----------
rows = []
cross = []
model_owner = {}
for svc, d in cur.items():
    for mn in d["models"]: model_owner.setdefault(mn, []).append(svc)
gap = collections.defaultdict(list)
for svc, d in cur.items():
    models = d["models"]
    nfk = nl = 0
    for mn, m in models.items():
        fkcols = set()
        for f in m["fields"]:
            if f.get("relation"): fkcols |= set(f["relation"]["fields"])
        idx_text = " ".join(a["text"] for a in m["indexes"])
        names = {f["name"] for f in m["fields"]}
        for f in m["fields"]:
            if f.get("relation") and f["relation"]["fields"]:
                nfk += 1
                # FK column without index
                first = f["relation"]["fields"][0]
                fcol = next((g for g in m["fields"] if g["name"] == first), None)
                if not re.search(r"\[\s*" + first + r"\b", idx_text) and not (fcol and (fcol["unique"] or fcol["id"])):
                    gap["FK بلا index"].append(f"{svc}.{mn}.{first} ({d['path']}:{f['line']})")
            if f["name"].endswith("Id") and f["type"] in ("String","Int") and not f["id"] and f["name"] not in fkcols:
                nl += 1
                cross.append((svc, mn, f["name"], f"{d['path']}:{f['line']}"))
            if f["type"] == "Float" and MONEY.search(f["name"]):
                gap["قيمة مالية/كمية بنوع Float"].append(f"{svc}.{mn}.{f['name']} ({d['path']}:{f['line']})")
            if f["type"] == "Decimal" and not f["dbType"]:
                gap["Decimal بلا precision صريحة (Prisma default Decimal(65,30))"].append(f"{svc}.{mn}.{f['name']} ({d['path']}:{f['line']})")
            if f["name"] == "status" and f["type"] == "String":
                gap["status كنص حر (String) بدل enum"].append(f"{svc}.{mn}.status ({d['path']}:{f['line']})")
        if "createdAt" not in names: gap["جدول بلا createdAt"].append(f"{svc}.{mn} ({d['path']}:{m['line']})")
        if "updatedAt" not in names and not mn.lower().endswith(("entry","event","log","line","snapshot","run","posting")):
            gap["جدول قابل للتعديل بلا updatedAt (heuristic)"].append(f"{svc}.{mn} ({d['path']}:{m['line']})")
        if any(n in names for n in ("deletedAt","isDeleted","archivedAt","isActive")):
            gap["_soft-delete/archival fields present (info)"].append(f"{svc}.{mn}")
        if not any(f["id"] for f in m["fields"]) and "@@id" not in idx_text:
            gap["بلا Primary Key"].append(f"{svc}.{mn}")
    rows.append((svc, len(models), len(d["enums"]), nfk, nl))

rep = ["# Schema Statistics & Heuristic Gap Scan (CURRENT)", "",
       "| Service | Models | Enums | Prisma FKs | Logical refs (*Id بلا FK) |", "|---|---|---|---|---|"]
for r in rows: rep.append("| " + " | ".join(map(str, r)) + " |")
rep += ["", "## Logical references without FK (LREF)", "| Service | Model | Field | Evidence |", "|---|---|---|---|"]
for c in cross: rep.append(f"| {c[0]} | {c[1]} | {c[2]} | `{c[3]}` |")
for k, v in gap.items():
    rep += ["", f"## {k} ({len(v)})"] + [f"- {x}" for x in v]
open(f"{B}/data/schema_stats.md", "w").write("\n".join(rep))

# ---------- base vs cur diff ----------
df = ["# Schema diff BASELINE 89c2c31 → CURRENT fa40270 (Prisma models)", ""]
for svc in sorted(set(cur) | set(base)):
    c = cur.get(svc, {"models": {}, "enums": {}}); b = base.get(svc, {"models": {}, "enums": {}})
    add = sorted(set(c["models"]) - set(b["models"])); rem = sorted(set(b["models"]) - set(c["models"]))
    fchg = []
    for mn in set(c["models"]) & set(b["models"]):
        cf = {f["name"]: ftype(f) for f in c["models"][mn]["fields"]}
        bf = {f["name"]: ftype(f) for f in b["models"][mn]["fields"]}
        a = [n for n in cf if n not in bf]; r = [n for n in bf if n not in cf]
        t = [f"{n}: {bf[n]} → {cf[n]}" for n in cf if n in bf and cf[n] != bf[n]]
        ci = sorted(x["text"] for x in c["models"][mn]["indexes"]); bi = sorted(x["text"] for x in b["models"][mn]["indexes"])
        ia = [x for x in ci if x not in bi]; ir = [x for x in bi if x not in ci]
        if a or r or t or ia or ir:
            fchg.append((mn, a, r, t, ia, ir))
    eadd = sorted(set(c["enums"]) - set(b["enums"]))
    echg = [f"{e}: +{sorted(set(c['enums'][e]['values'])-set(b['enums'][e]['values']))} -{sorted(set(b['enums'][e]['values'])-set(c['enums'][e]['values']))}" for e in set(c["enums"]) & set(b["enums"]) if set(c["enums"][e]["values"]) != set(b["enums"][e]["values"])]
    if not (add or rem or fchg or eadd or echg):
        df.append(f"## {svc}: لا تغيير في Prisma models/enums"); df.append(""); continue
    df.append(f"## {svc}")
    if add: df.append(f"- Models مضافة: {', '.join(add)}")
    if rem: df.append(f"- Models محذوفة: {', '.join(rem)}")
    if eadd: df.append(f"- Enums مضافة: {', '.join(eadd)}")
    for e in echg: df.append(f"- Enum تغيّر: {e}")
    for mn, a, r, t, ia, ir in sorted(fchg):
        s = f"- `{mn}`:"
        if a: s += f" +fields[{', '.join(a)}]"
        if r: s += f" -fields[{', '.join(r)}]"
        if t: s += f" type[{'; '.join(t)}]"
        if ia: s += f" +idx[{'; '.join(ia)}]"
        if ir: s += f" -idx[{'; '.join(ir)}]"
        df.append(s)
    df.append("")
open(f"{B}/data/schema_diff.md", "w").write("\n".join(df))
print("ok", rows)
