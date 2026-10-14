from pathlib import Path
from difflib import SequenceMatcher
import json

ROOT = Path(__file__).resolve().parent
names = ['original', 'oka', 'matsuda']
lines = {n: (ROOT / (n + '.md')).read_text(encoding='utf-8-sig').splitlines() for n in names}
changes = {}
for n in names[1:]:
    changes[n] = [dict(start=a, end=b, vs=c, ve=d) for tag,a,b,c,d in SequenceMatcher(None, lines['original'], lines[n], autojunk=False).get_opcodes() if tag != 'equal']
events = sorted([(x['start'],x['end'],n,x) for n in names[1:] for x in changes[n]], key=lambda t:(t[0],t[1]))
groups=[]
for a,b,n,x in events:
    if groups and a <= groups[-1]['end']:
        groups[-1]['end']=max(b,groups[-1]['end']); groups[-1]['events'].append((n,x))
    else: groups.append(dict(start=a,end=b,events=[(n,x)]))

def variant(n,a,b):
    result=[]; cursor=a
    for x in changes[n]:
        if x['start'] < a or x['end'] > b: continue
        result.extend(lines['original'][cursor:x['start']]); result.extend(lines[n][x['vs']:x['ve']]); cursor=x['end']
    result.extend(lines['original'][cursor:b])
    return result

def section(a):
    heads=[]; fenced=False
    for line in lines['original'][:a+1]:
        if line.startswith('```'): fenced=not fenced
        if not fenced and line.startswith('#'):
            level=len(line)-len(line.lstrip('#'))
            heads=[h for h in heads if h[0]<level]; heads.append((level,line.lstrip('# ')))
    return ' / '.join(h[1] for h in heads)

records=[]
for i,g in enumerate(groups,1):
    a,b=g['start'],g['end']; base=lines['original'][a:b]; o=variant('oka',a,b); m=variant('matsuda',a,b)
    status='両者同じ改訂' if o==m else '双方が異なる改訂' if o!=base and m!=base else 'okaのみ改訂' if o!=base else 'matsudaのみ改訂'
    records.append(dict(id=f'D{i:02}',start=a+1,end=b,section=section(a),status=status,original='\n'.join(base),oka='\n'.join(o),matsuda='\n'.join(m)))
(ROOT/'comparison_data.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
for r in records:
    print(f"{r['id']} L{r['start']}-{r['end']} {r['status']} {r['section']} | O:{r['oka'][:70]!r} | M:{r['matsuda'][:70]!r}")
