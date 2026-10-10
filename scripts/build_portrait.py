"""Build an animated SG monogram with orbital particles."""
from pathlib import Path
import random, math, html
R=Path(__file__).resolve().parents[1]
random.seed(7)
s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1180 610" role="img" aria-label="SG, animated spatial monogram and developer profile"><title>SG: orbital particles scatter and reform</title><rect width="1180" height="610" rx="16" fill="#0b1020"/><rect x="1" y="1" width="1178" height="608" rx="16" fill="none" stroke="#28354b"/><path d="M0 46H1180" stroke="#28354b"/>']
for x,c in [(26,'#ff5f57'),(48,'#febc2e'),(70,'#28c840')]:s.append(f'<circle cx="{x}" cy="23" r="6" fill="{c}"/>')
def text(x,y,t,size=14,c='#9aa9c2',extra=''):
 return f'<text x="{x}" y="{y}" font-family="ui-monospace,monospace" font-size="{size}" fill="{c}" {extra}>{html.escape(t)}</text>'
s.append(text(590,28,'profile.sh --live',13,extra='text-anchor="middle"'))
for x,w in [(28,418),(474,678)]:s.append(f'<rect x="{x}" y="66" width="{w}" height="516" rx="10" fill="none" stroke="#28354b"/>')
s.extend([text(44,89,'SPATIAL.MAP',12,'#45d9e8'),text(490,89,'SYSTEM.INFO',12,'#45d9e8'),text(1080,89,'● LIVE',12,'#ff6b80')])
s.append('<defs><clipPath id="portrait"><rect x="44" y="104" width="386" height="452" rx="8"/></clipPath></defs><g clip-path="url(#portrait)">')
paths={}; moving=[]
# Native bitmap lettering sampled into a vector point cloud.
letters=['01111011110','11000011001','11000011000','01110011011','00011011001','00011011001','11110001110']
for row,line in enumerate(letters):
 for col,cell in enumerate(line):
  if cell!='1': continue
  for oy in range(0,25,4):
   for ox in range(0,25,4):
    x=74+col*30+ox; y=227+row*30+oy
    level=2 if (row+col)%3 else 3
    color=['#453268','#7454a8','#a78bfa','#ddcaff'][level]
    if random.random()<.45:
     moving.append((x,y,color,random.uniform(-110,110),random.uniform(-100,100)))
    else:
     key=(level,random.randrange(16));paths.setdefault(key,[]).append(f'M{x:.1f} {y:.1f}h2.5v2.5h-2.5z')
# Depth cues: a star field and two tilted elliptical orbits.
for i in range(65):
 x=random.uniform(50,428); y=random.uniform(119,548)
 s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(.5,1.3):.1f}" fill="#9ba8d9" opacity=".4"><animate attributeName="opacity" values=".15;.65;.15" dur="{random.uniform(3,7):.1f}s" repeatCount="indefinite"/></circle>')
for angle,color,duration in [(-24,'#45d9e8',18),(32,'#b59aff',25)]:
 s.append(f'<g transform="rotate({angle} 237 337)"><ellipse cx="237" cy="337" rx="180" ry="108" fill="none" stroke="{color}" stroke-opacity=".23" stroke-width="1"/><g><animateTransform attributeName="transform" type="rotate" from="0 237 337" to="360 237 337" dur="{duration}s" repeatCount="indefinite"/><circle cx="417" cy="337" r="4" fill="{color}"/></g></g>')
for (level,phase),commands in paths.items():
 s.append(f'<path fill="{["#453268","#7454a8","#a78bfa","#ddcaff"][level]}" d="{"".join(commands)}"><animate attributeName="opacity" values="1;1;0;0;1;1" keyTimes="0;.23;.39;.64;.82;1" dur="14s" begin="{phase*.018:.3f}s" repeatCount="indefinite"/></path>')
for x,y,c,dx,dy in moving:
 s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.2" fill="{c}"><animateTransform attributeName="transform" type="translate" values="0 0;0 0;{dx:.1f} {dy:.1f};{-dx*.55:.1f} {dy*.7:.1f};0 0;0 0" keyTimes="0;.23;.43;.62;.82;1" dur="14s" repeatCount="indefinite"/><animate attributeName="fill" values="{c};{c};#45d9e8;#45d9e8;{c};{c}" keyTimes="0;.23;.43;.62;.82;1" dur="14s" repeatCount="indefinite"/></circle>')
s.append('</g>')
s.append(text(498,146,'SG',36,'#e8e6ff'))
s.append(text(498,181,'AI & Backend Developer',18,'#b59aff'))
rows=[('Approach','Applying automation wherever possible'),('Languages','Python / Node.js / TypeScript'),('Frontend','React / Next.js / Tailwind'),('Backend','REST APIs / Express'),('Work','ABTalksOnAI / Klymb.ai'),('Learning','LangChain / system design'),('Portfolio','portfolio-topaz-six-57.vercel.app'),('LinkedIn','/in/sarthak-gupta7'),('GitHub','@Sarthakgupta7')]
for i,(label,value) in enumerate(rows):
 y=231+i*31
 s.extend([text(498,y,label,13,'#7c90af'),f'<path d="M498 {y+10}H1126" stroke="#25324b" stroke-dasharray="1 5"/>',text(1125,y,value,13,'#d1daeb','text-anchor="end"')])
s.append(text(498,551,'BUILD / LEARN / IMPROVE / REPEAT',12,'#45d9e8'))
s.append('</svg>')
(R/'assets/animated-header.svg').write_text(''.join(s))
print(f'Generated animated SVG with {len(moving)} moving particles and {sum(map(len,paths.values()))} portrait dots')
