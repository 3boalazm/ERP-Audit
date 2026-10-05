#!/usr/bin/env python3
"""Read-only NestJS route extractor + web call-site matcher. Usage: routes.py <snapshot_root> <out.json>"""
import re, os, sys, json, glob

ALIAS = {"iam": "iam", "organization": "org", "products": "products", "inventory": "inventory", "crm": "crm",
         "sales": "sales", "accounting": "accounting", "incentives": "incentives", "audit-aggregator": "audit"}
HTTP = ("Get", "Post", "Put", "Patch", "Delete")

def strarg(s):
    m = re.match(r"\s*['\"`]([^'\"`]*)['\"`]", s or "")
    return m.group(1) if m else ""

def deco_args(text):
    return re.findall(r"['\"]([\w.:*-]+)['\"]", text)

def module_graph(app_dir):
    mods = {}
    for p in glob.glob(f"{app_dir}/src/**/*.module.ts", recursive=True):
        t = open(p, encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r"@Module\(\{(.*?)\}\)\s*export\s+class\s+(\w+)", t, re.S):
            body, name = m.group(1), m.group(2)
            imp = re.search(r"imports\s*:\s*\[(.*?)\]\s*,?\s*(controllers|providers|exports|\}|$)", body, re.S)
            ctr = re.search(r"controllers\s*:\s*\[(.*?)\]", body, re.S)
            imports = re.findall(r"\b([A-Z]\w*Module)\b", imp.group(1)) if imp else []
            controllers = re.findall(r"\b([A-Z]\w*Controller)\b", ctr.group(1)) if ctr else []
            mods[name] = {"imports": imports, "controllers": controllers, "file": p}
    return mods

def reachable(mods, root="AppModule"):
    seen, st = set(), [root]
    while st:
        n = st.pop()
        if n in seen or n not in mods: continue
        seen.add(n); st += mods[n]["imports"]
    ctrls = set()
    for n in seen: ctrls |= set(mods[n]["controllers"])
    return ctrls

def controllers(root, app):
    app_dir = f"{root}/apps/{app}"
    mods = module_graph(app_dir)
    mounted = reachable(mods)
    out = []
    for p in sorted(glob.glob(f"{app_dir}/src/**/*.controller.ts", recursive=True)):
        rel = os.path.relpath(p, root)
        lines = open(p, encoding="utf-8", errors="ignore").read().split("\n")
        pending, cls, cls_perm, cls_guards, cls_public, base_path = [], None, [], [], False, ""
        brace_depth = 0
        i = 0
        while i < len(lines):
            s = lines[i].strip()
            if s.startswith("@"):
                # gather multi-line decorator(s), split several decorators on one line
                buf, j = s, i
                while buf.count("(") > buf.count(")") and j + 1 < len(lines):
                    j += 1; buf += " " + lines[j].strip()
                rest = buf
                while rest.startswith("@"):
                    m0 = re.match(r"@\w+", rest); k = m0.end()
                    if k < len(rest) and rest[k] == "(":
                        depth = 0
                        for q in range(k, len(rest)):
                            if rest[q] == "(": depth += 1
                            elif rest[q] == ")":
                                depth -= 1
                                if depth == 0: k = q + 1; break
                    pending.append((rest[:k], i + 1)); rest = rest[k:].strip()
                if rest:
                    lines[j] = rest; i = j; continue
                i = j + 1; continue
            cm = re.match(r"export\s+class\s+(\w+)", s)
            if cm:
                cls = cm.group(1)
                for d, ln in pending:
                    if d.startswith("@Controller"): base_path = strarg(d[len("@Controller("):])
                    if d.startswith("@Permissions"): cls_perm = deco_args(d)
                    if d.startswith("@UseGuards"): cls_guards = re.findall(r"(\w+Guard)", d)
                    if d.startswith("@Public"): cls_public = True
                pending = []; i += 1; continue
            mm = re.match(r"(?:async\s+)?(\w+)\s*\((.*)", s)
            if cls and pending and mm and any(d.startswith(tuple("@" + h + "(" for h in HTTP)) for d, _ in pending):
                handler = mm.group(1)
                # signature (multi-line)
                sig, j = s, i
                while sig.count("(") > sig.count(")") and j + 1 < len(lines):
                    j += 1; sig += " " + lines[j].strip()
                for d, ln in pending:
                    hm = re.match(r"@(Get|Post|Put|Patch|Delete)\((.*)\)", d)
                    if not hm: continue
                    method, sub = hm.group(1).upper(), strarg(hm.group(2))
                    perms = [x for dd, _ in pending if dd.startswith("@Permissions") for x in deco_args(dd)]
                    guards = [g for dd, _ in pending if dd.startswith("@UseGuards") for g in re.findall(r"(\w+Guard)", dd)]
                    public = cls_public or any(dd.startswith("@Public") for dd, _ in pending)
                    throttle = any(dd.startswith("@Throttle") for dd, _ in pending)
                    httpcode = next((re.sub(r"\D", "", dd) for dd, _ in pending if dd.startswith("@HttpCode")), "")
                    body = re.search(r"@Body\(\)\s*\w+\s*:\s*([\w<>\[\]]+)", sig)
                    body_any = re.search(r"@Body\([^)]*\)\s*\w+\s*:\s*([\w<>\[\]{}:;, ?]+)", sig)
                    params = re.findall(r"@Param\(\s*['\"](\w+)['\"]", sig)
                    query = re.findall(r"@Query\(\s*['\"]?(\w*)", sig)
                    path = "/api/" + "/".join(x.strip("/") for x in (base_path, sub) if x.strip("/"))
                    out.append({"app": app, "method": method, "path": path, "controller": cls, "handler": handler,
                                "file": rel, "line": ln, "perms": perms or cls_perm, "perm_level": "method" if perms else ("class" if cls_perm else "none"),
                                "guards": guards or cls_guards, "public": public, "throttle": throttle, "httpcode": httpcode,
                                "body": (body.group(1) if body else (body_any.group(1).strip() if body_any else "")),
                                "params": params, "query": [q for q in query if q], "mounted": cls in mounted})
                pending = []; i = j + 1; continue
            if s and not s.startswith(("//", "*", "/*")) and not s.startswith("@"):
                pending = [] if not s.startswith(")") else pending
            i += 1
    return out

def web_calls(root):
    calls = []
    for p in glob.glob(f"{root}/apps/web/**/*.ts*", recursive=True):
        if "node_modules" in p or ".spec." in p or "/e2e/" in p: continue
        rel = os.path.relpath(p, root)
        for n, line in enumerate(open(p, encoding="utf-8", errors="ignore"), 1):
            for m in re.finditer(r"(?:\b(get|post|put|patch|del|delete|fetch|request|apiFetch|getBlob|download\w*|upload\w*)\w*\s*(?:<[^>]*>)?\s*\(\s*)?[`'\"](/api/(iam|org|products|inventory|crm|sales|accounting|incentives|audit)/[^`'\"]*)[`'\"]?", line):
                verb = (m.group(1) or "").lower()
                raw = m.group(2)
                raw = re.sub(r"(?<!/)\$\{.*$", "", raw)
                path = re.sub(r"\$\{[^}]*\}?", ":p", raw).split("?")[0]
                path = re.sub(r":p[^/]*", ":p", path).rstrip("/")
                if verb in ("post", "put", "patch"): meth = verb.upper()
                elif verb in ("del", "delete"): meth = "DELETE"
                elif verb == "get": meth = "GET"
                else:
                    mm = re.search(r"method\s*:\s*['\"](\w+)['\"]", line); meth = mm.group(1).upper() if mm else "?"
                calls.append({"method": meth, "path": path, "svc": m.group(3), "file": rel, "line": n})
    return calls

def norm(p):
    return re.sub(r"/:[\w]+", "/:p", p).rstrip("/")

def main(root, outp):
    routes = []
    for app in ALIAS:
        if os.path.isdir(f"{root}/apps/{app}/src"):
            routes += controllers(root, app)
    calls = web_calls(root)
    # match
    for r in routes:
        ext = norm("/api/" + ALIAS[r["app"]] + r["path"][len("/api"):])
        r["external"] = "/api/" + ALIAS[r["app"]] + r["path"][len("/api"):]
        pat = re.compile("^" + re.sub(r":p", r"[^/]+", re.escape(ext).replace("\\:p", ":p")) + "$")
        r["web_refs"] = [f"{c['file']}:{c['line']}" for c in calls if (c["method"] in (r["method"], "?")) and (pat.match(c["path"]) or norm(c["path"]) == ext)]
    unmatched = []
    for c in calls:
        cp = norm(c["path"])
        hit = False
        for r in routes:
            ext = norm(r["external"])
            pat = re.compile("^" + re.sub(r":p", r"[^/]+", re.escape(ext).replace("\\:p", ":p")) + "$")
            if (c["method"] in (r["method"], "?")) and (pat.match(cp) or cp == ext):
                hit = True; break
        if not hit: unmatched.append(c)
    json.dump({"routes": routes, "web_calls": calls, "unmatched_web_calls": unmatched}, open(outp, "w"), indent=1)
    print(len(routes), "routes;", sum(r["mounted"] for r in routes), "mounted;", len(calls), "web calls;", len(unmatched), "unmatched")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
