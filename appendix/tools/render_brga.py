import re, subprocess, os, sys
P='/home/claude/audit/pkg/29-E2E-Processes-As-Is-To-Be.md'
D='/home/claude/audit/pkg/diagrams/brga'; os.makedirs(D, exist_ok=True)
s=open(P).read()
blocks=list(re.finditer(r'```mermaid\n(.*?)```', s, re.S))
out=[]; last=0; fails=[]
for i,m in enumerate(blocks,1):
    # nearest previous heading for name
    name=f'p29-{i:02d}'
    if os.path.exists(f'{D}/{name}.svg') and os.path.exists(f'{D}/{name}.mmd') and open(f'{D}/{name}.mmd').read()==m.group(1):
        out.append(s[last:m.start()]); out.append(f'![{name}](diagrams/brga/{name}.svg)\n\n<sub>مصدر الرسم: `diagrams/brga/{name}.mmd`</sub>\n'); last=m.end(); continue
    open(f'{D}/{name}.mmd','w').write(m.group(1))
    r=subprocess.run(['mmdc','-i',f'{D}/{name}.mmd','-o',f'{D}/{name}.svg','-b','white','-p','/etc/puppeteer-config.json'] if os.path.exists('/etc/puppeteer-config.json') else ['mmdc','-i',f'{D}/{name}.mmd','-o',f'{D}/{name}.svg','-b','white'],capture_output=True,text=True,timeout=120)
    ok=r.returncode==0 and os.path.exists(f'{D}/{name}.svg')
    if not ok: fails.append((name,r.stderr[-400:]))
    out.append(s[last:m.start()])
    out.append(f'![{name}](diagrams/brga/{name}.svg)\n\n<sub>مصدر الرسم: `diagrams/brga/{name}.mmd`</sub>\n' if ok else m.group(0))
    last=m.end()
out.append(s[last:])
open(P,'w').write(''.join(out))
print(len(blocks),'blocks; fails',len(fails))
for f in fails: print(f)
