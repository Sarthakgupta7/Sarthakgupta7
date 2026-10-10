import collections, datetime, html, json, os, pathlib, urllib.request
ROOT = pathlib.Path(__file__).resolve().parents[1]
query = '''query { user(login:"Sarthakgupta7") { login contributionsCollection { contributionCalendar { totalContributions weeks { contributionDays { date contributionCount color } } } } repositories(first:100,ownerAffiliations:OWNER,privacy:PUBLIC,isFork:false) { nodes { languages(first:10,orderBy:{field:SIZE,direction:DESC}) { edges { size node { name color } } } } } } }'''
if os.environ.get('GITHUB_TOKEN'):
    req = urllib.request.Request('https://api.github.com/graphql', data=json.dumps({'query':query}).encode(), headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Content-Type':'application/json'})
    data = json.load(urllib.request.urlopen(req))
else:
    data = json.loads((ROOT/'data.json').read_text())
if data.get('errors'): raise RuntimeError(data['errors'])
u=data['data'].get('user') or data['data'].get('viewer')
if u['login'].lower() != 'sarthakgupta7': raise RuntimeError('Unexpected account')
cal=u['contributionsCollection']['contributionCalendar']; days=[d for w in cal['weeks'] for d in w['contributionDays']]
longest=run=0
for d in days:
    run=run+1 if d['contributionCount'] else 0
    longest=max(longest,run)
current=0
eligible=days[:-1] if days and not days[-1]['contributionCount'] else days
for d in reversed(eligible):
    if not d['contributionCount']: break
    current+=1
langs=collections.Counter(); colors={}
for repo in u['repositories']['nodes']:
    for e in repo['languages']['edges']:
        name=e['node']['name']; langs[name]+=e['size']; colors[name]=e['node']['color'] or '#8993a5'
def start(w,h,title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}"><title>{html.escape(title)}</title><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16" fill="#0b1020" stroke="#28354b"/>'
def txt(x,y,s,size=14,color='#9aa9c2',extra=''):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="monospace" font-size="{size}" {extra}>{html.escape(str(s))}</text>'
s=start(900,196,'GitHub contributions over the last year')
s+=txt(30,33,'GITHUB / LAST 12 MONTHS',12,'#45d9e8')
for x,n,label in [(150,cal['totalContributions'],'CONTRIBUTIONS'),(450,current,'CURRENT STREAK'),(750,longest,'LONGEST STREAK')]:
    s+=txt(x,103,f'{n:,}',42,'#b59aff','text-anchor="middle"')+txt(x,134,label,12,'#45d9e8','text-anchor="middle"')
    if 'STREAK' in label: s+=txt(x,155,'days',11,'#9aa9c2','text-anchor="middle"')
s+=txt(30,179,'Source: GitHub contribution calendar | Updated '+days[-1]['date'],10)
(ROOT/'assets/stats.svg').write_text(s+'</svg>')
s=start(900,215,'Most used languages by code bytes in public original repositories')+txt(30,33,'LANGUAGES / PUBLIC ORIGINAL REPOSITORIES',12,'#45d9e8')
total=sum(langs.values()) or 1; x=30
for name,size in langs.most_common():
    width=840*size/total
    s+=f'<rect x="{x}" y="55" width="{width}" height="12" fill="{colors[name]}"/>'; x+=width
for i,(name,size) in enumerate(langs.most_common(6)):
    x=30+(i%3)*285; y=103+(i//3)*39
    s+=f'<circle cx="{x+5}" cy="{y-4}" r="5" fill="{colors[name]}"/>'+txt(x+20,y,f'{name}  {size/total:.1%}',13,'#dde5f3')
s+=txt(30,192,'Repository composition, not a measure of proficiency.',10)
(ROOT/'assets/languages.svg').write_text(s+'</svg>')
