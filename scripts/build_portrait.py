"""Build a native SVG animation by sampling the existing portrait, without altering the source image."""
from PIL import Image
from pathlib import Path
import random, math, html
R=Path(__file__).resolve().parents[1]
source=R/'assets/portrait-header.png'
im=Image.open(source).convert('RGB');random.seed(7)
s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" role="img" aria-label="Sarthak Gupta, animated particle portrait and developer profile"><title>Sarthak Gupta: portrait dissolves into particles and reforms</title><rect width="1180" height="610" rx="16" fill="#0b1020"/><rect x="1" y="1" width="1178" height="608" rx="16" fill="none" stroke="#28354b"/><path d="M0 46H1180" stroke="#28354b"/>']
for x,c in [(26,'#ff5f57'),(48,'#febc2e'),(70,'#28c840')]:s.append(f'<circle cx="{x}" cy="23" r="6" fill="{c}"/>')
def text(x,y,t,size=14,c='#9aa9c2',extra=''):
 return f'<text x="{x}" y="{y}" font-family="ui-monospace,monospace" font-size="{size}" fill="{c}" {extra}>{html.escape(t)}</text>'
s.append(text(590,28,'profile.sh --live',13,extra='text-anchor="middle"'))
for x,w in [(28,418),(474,678)]:s.append(f'<rect x="{x}" y="66" width="{w}" height="516" rx="10" fill="none" stroke="#28354b"/>')
s.extend([text(44,89,'VISUAL.MAP',12,'#45d9e8'),text(490,89,'SYSTEM.INFO',12,'#45d9e8'),text(1080,89,'● LIVE',12,'#ff6b80')])
s.append('<defs><clipPath id="portrait"><rect x="44" y="104" width="386" height="452" rx="8"/></clipPath></defs><g clip-path="url(#portrait)">')
paths={}; moving=[]
# Sample the portrait region of the original header into vector dots.
for iy in range(106,836,4):
 for ix in range(22,738,4):
  r,g,b=im.getpixel((ix,iy)); bright=max(r,g,b)
  if bright<58 or b<r*.9:continue
  x=46+(ix-22)*382/716;y=113+(iy-106)*430/730
  level=min(3,int(bright/64));color=['#453268','#7454a8','#a78bfa','#ddcaff'][level]
  if random.random()<.1:
   moving.append((x,y,color,random.uniform(-115,115),random.uniform(-100,100)))
  else:
   key=(level,random.randrange(16));paths.setdefault(key,[]).append(f'M{x:.1f} {y:.1f}h1.7v1.7h-1.7z')
for (level,phase),commands in paths.items():
 s.append(f'<path fill="{["#453268","#7454a8","#a78bfa","#ddcaff"][level]}" d="{"".join(commands)}"><animate attributeName="opacity" values="1;1;0;0;1;1" keyTimes="0;.23;.39;.64;.82;1" dur="14s" begin="{phase*.018:.3f}s" repeatCount="indefinite"/></path>')
for x,y,c,dx,dy in moving:
 s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.2" fill="{c}"><animateTransform attributeName="transform" type="translate" values="0 0;0 0;{dx:.1f} {dy:.1f};{-dx*.55:.1f} {dy*.7:.1f};0 0;0 0" keyTimes="0;.23;.43;.62;.82;1" dur="14s" repeatCount="indefinite"/><animate attributeName="fill" values="{c};{c};#45d9e8;#45d9e8;{c};{c}" keyTimes="0;.23;.43;.62;.82;1" dur="14s" repeatCount="indefinite"/></circle>')
s.append('</g>')
s.append(text(498,146,'Sarthak Gupta',29,'#e8e6ff'))
s.append(text(498,181,'AI & Backend Developer',18,'#b59aff'))
rows=[('Focus','Agentic AI / LLM integration'),('Languages','Python / Node.js / TypeScript'),('Frontend','React / Next.js / Tailwind'),('Backend','REST APIs / Express'),('Work','ABTalksOnAI / Klymb.ai'),('Learning','LangChain / system design'),('Portfolio','portfolio-topaz-six-57.vercel.app'),('LinkedIn','/in/sarthak-gupta-946295258'),('GitHub','@Sarthakgupta7')]
for i,(label,value) in enumerate(rows):
 y=231+i*31
 s.extend([text(498,y,label,13,'#7c90af'),f'<path d="M498 {y+10}H1126" stroke="#25324b" stroke-dasharray="1 5"/>',text(1125,y,value,13,'#d1daeb','text-anchor="end"')])
s.append(text(498,551,'BUILD / LEARN / IMPROVE / REPEAT',12,'#45d9e8'))
s.append('</svg>')
(R/'assets/animated-header.svg').write_text(''.join(s))
print(f'Generated animated SVG with {len(moving)} moving particles and {sum(map(len,paths.values()))} portrait dots')
