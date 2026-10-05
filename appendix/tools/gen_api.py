#!/usr/bin/env python3
"""Build API inventory markdown + CSV from routes JSON (both snapshots) with controller-level data-touch analysis."""
import json, re, os, glob, csv, collections
B = "/home/claude/audit"
cur = json.load(open(f"{B}/data/routes_cur.json")); base = json.load(open(f"{B}/data/routes_base.json"))
bset = {(r["app"], r["method"], re.sub(r":\w+", ":p", r["path"])) for r in base["routes"]}
cset = {(r["app"], r["method"], re.sub(r":\w+", ":p", r["path"])) for r in cur["routes"]}
removed = sorted(bset - cset)

def ctrl_touch(root, rel):
    """Models read/written + tx + events by services injected in this controller (controller-level approximation)."""
    p = f"{root}/{rel}"; t = open(p, encoding="utf-8", errors="ignore").read()
    svc_types = set(re.findall(r"private\s+(?:readonly\s+)?\w+\s*:\s*(\w+Service)", t))
    files = []
    for st in svc_types:
        for f in glob.glob(f"{root}/apps/{rel.split('/')[1]}/src/**/*.ts", recursive=True):
            if f.endswith(".spec.ts"): continue
            try:
                if re.search(rf"export\s+class\s+{st}\b", open(f, encoding="utf-8", errors="ignore").read()): files.append(f)
            except Exception: pass
    W, R = set(), set(); tx = ev = raw = False
    for f in files:
        s = open(f, encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r"\b(?:prisma|tx|db|client|this\.prisma)\.(\w+)\.(create|createMany|update|updateMany|upsert|delete|deleteMany|findUnique|findFirst|findMany|count|aggregate|groupBy|findUniqueOrThrow|findFirstOrThrow)\b", s):
            (W if m.group(2) in ("create","createMany","update","updateMany","upsert","delete","deleteMany") else R).add(m.group(1))
        tx |= "$transaction" in s
        raw |= bool(re.search(r"\$(queryRaw|executeRaw)", s))
        ev |= bool(re.search(r"\b(publish|emit|outbox|Outbox|producer\.send)\w*\(", s))
    return {"writes": sorted(W), "reads": sorted(R - W), "tx": tx, "events": ev, "raw": raw, "svc_files": [os.path.relpath(f, root) for f in files]}

cache = {}
rows = []
for r in cur["routes"]:
    key = r["file"]
    if key not in cache: cache[key] = ctrl_touch(f"{B}/cur", key)
    r["touch"] = cache[key]
    r["in_base"] = (r["app"], r["method"], re.sub(r":\w+", ":p", r["path"])) in bset

ALIAS = {"organization": "org", "audit-aggregator": "audit"}
md = ["# API Inventory & Routing — Nile Pharma ERP", "",
      "مُولّد آليًا من decorators في `apps/*/src/**/*.controller.ts` (CURRENT fa40270) ومقارن بـBASELINE 89c2c31. قراءة ثابتة فقط — لم يُستدعَ أي endpoint.", "",
      "**مفتاح الأعمدة:** External = المسار كما يطلبه المتصفح عبر Next.js rewrite (`/api/<alias>/...`)، Internal = المسار داخل الخدمة بعد `setGlobalPrefix('api')`. Perm = `@Permissions(...)` المطلوبة (تُفرض فقط إذا كان `PermissionsGuard` مطبقًا). Mounted = هل الـcontroller ضمن module مستورد (transitively) في `AppModule`. B = موجود في BASELINE. Web = عدد مواضع الاستدعاء في `apps/web` (مطابقة نصية تقريبية).",
      "**Tables/Tx/Events** على مستوى الـcontroller (اتحاد ما تلمسه الـservices المحقونة) — تقريب لا يحدد handler بعينه. التفاصيل الدقيقة لكل handler موثقة للمسارات الحرجة في Process Catalogue.", ""]
stat = collections.Counter(); stat_m = collections.Counter()
for r in cur["routes"]:
    stat[r["app"]] += 1; stat_m[(r["app"], r["mounted"])] += 1
md += ["## ملخص", "| Service | Alias | Routes CURRENT | Unmounted | Routes BASELINE | Public |", "|---|---|---|---|---|---|"]
bstat = collections.Counter(r["app"] for r in base["routes"])
for a in sorted(stat):
    pub = sum(1 for r in cur["routes"] if r["app"] == a and r["public"])
    md.append(f"| {a} | /api/{ALIAS.get(a,a)} | {stat[a]} | {stat_m[(a, False)]} | {bstat[a]} | {pub} |")
md.append(f"| **Total** | | **{sum(stat.values())}** | **{sum(v for (a,m),v in stat_m.items() if not m)}** | **{sum(bstat.values())}** | |")
md.append("")
md += ["## Routes موجودة في BASELINE وأُزيلت/تغيّر مسارها في CURRENT", ""] + ([f"- {a} {m} {p}" for a, m, p in removed] or ["- لا يوجد"]) + [""]
unm = [c for c in cur["unmatched_web_calls"]]
md += ["## استدعاءات Web لا تطابق أي route مُعرّف (CURRENT)", "| Method | Path | Caller |", "|---|---|---|"] + [f"| {c['method']} | `{c['path']}` | `{c['file']}:{c['line']}` |" for c in unm] + [""]
md += ["## استدعاءات Web إلى routes غير mounted (ستعيد 404) — CURRENT", "| Method | External | Controller | Web caller |", "|---|---|---|---|"]
for r in cur["routes"]:
    if not r["mounted"] and r["web_refs"]:
        md.append(f"| {r['method']} | `{r['external']}` | {r['controller']} | `{r['web_refs'][0]}` |")
md.append("")
for a in sorted(stat):
    md += [f"## {a}", ""]
    by_ctrl = collections.defaultdict(list)
    for r in cur["routes"]:
        if r["app"] == a: by_ctrl[(r["controller"], r["file"])].append(r)
    for (c, f), rs in sorted(by_ctrl.items()):
        t = rs[0]["touch"]
        md.append(f"### {c} — `{f}`" + ("" if rs[0]["mounted"] else " ⚠️ **NOT MOUNTED**"))
        md.append(f"- Writes: {', '.join(t['writes']) or '—'} | Reads: {', '.join(t['reads']) or '—'} | `$transaction`: {'yes' if t['tx'] else 'no'} | events/outbox: {'yes' if t['events'] else 'no'} | raw SQL: {'yes' if t['raw'] else 'no'}")
        md += ["", "| Method | External | Internal | Handler | Perm | Body DTO | Guard | B | Web |", "|---|---|---|---|---|---|---|---|---|"]
        for r in rs:
            g = "Public" if r["public"] else ("Perm" if "PermissionsGuard" in r["guards"] else "JWT only")
            md.append(f"| {r['method']} | `{r['external']}` | `{r['path']}` | {r['handler']} (L{r['line']}) | {', '.join(r['perms']) or '—'} | {r['body'] or '—'} | {g} | {'✓' if r['in_base'] else '**new**'} | {len(r['web_refs'])} |")
        md.append("")
open(f"{B}/out/05-API-Inventory.md", "w").write("\n".join(md))
with open(f"{B}/out/api-inventory.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["service","method","external_route","internal_route","controller","handler","file","line","permissions","guard","public","body_dto","params","query","mounted","in_baseline","web_callers","ctrl_writes","ctrl_reads","ctrl_tx","ctrl_events"])
    for r in cur["routes"]:
        t = r["touch"]
        w.writerow([r["app"], r["method"], r["external"], r["path"], r["controller"], r["handler"], r["file"], r["line"], " ".join(r["perms"]),
                    "Public" if r["public"] else ("PermissionsGuard" if "PermissionsGuard" in r["guards"] else "JwtAuthGuard only"),
                    r["public"], r["body"], " ".join(r["params"]), " ".join(r["query"]), r["mounted"], r["in_base"], len(r["web_refs"]),
                    " ".join(t["writes"]), " ".join(t["reads"]), t["tx"], t["events"]])
print("done", len(cur["routes"]), "removed", len(removed))
