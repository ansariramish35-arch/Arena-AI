"""Render accessible, deterministic instructional visuals for PDF and DOCX.
No network images, screenshots, experimental values or fictitious test metrics.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

BASE = Path(__file__).resolve().parent
FONT = BASE/'report'/'assets'/'fonts'
NAVY=(23,40,64)
BLUE=(69,113,148)
PALE=(232,239,245)
INK=(37,49,65)
WHITE=(255,255,255)


def font(size,bold=False):
    return ImageFont.truetype(str(FONT/('Tinos-Bold.ttf' if bold else 'Tinos-Regular.ttf')),size)


def fit_lines(draw,text,f,max_width):
    words=text.split(); lines=[]; current=''
    for w in words:
        trial=(current+' '+w).strip()
        if current and draw.textbbox((0,0),trial,font=f)[2]>max_width:
            lines.append(current);current=w
        else:current=trial
    if current:lines.append(current)
    return lines


def centre_lines(draw,area,text,f,fill=INK,max_lines=3):
    x0,y0,x1,y1=area
    lines=fit_lines(draw,text,f,x1-x0-30)[:max_lines]
    line_h=f.size+5
    first=(y0+y1-len(lines)*line_h)//2
    for j,line in enumerate(lines):
        box=draw.textbbox((0,0),line,font=f)
        x=(x0+x1-(box[2]-box[0]))//2
        draw.text((x,first+j*line_h),line,font=f,fill=fill)


def build(visual,path):
    kind,title,labels=visual
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    image=Image.new('RGB',(1320,360),WHITE);d=ImageDraw.Draw(image)
    d.rounded_rectangle((10,10,1310,350),radius=18,fill=WHITE,outline=(174,191,205),width=3)
    d.rectangle((11,11,1309,66),fill=NAVY)
    d.text((36,24),'ILLUSTRATIVE DIAGRAM' if kind in ('flow','split') else 'MANUALLY DERIVED GRAPH',font=font(24,True),fill=WHITE)
    if kind=='flow':
        n=len(labels); gap=23; usable=1238-gap*(n-1); cell=usable//n
        for i,label in enumerate(labels):
            x=42+i*(cell+gap)
            d.rounded_rectangle((x,114,x+cell,278),radius=16,fill=PALE,outline=BLUE,width=3)
            d.ellipse((x+15,127,x+53,165),fill=BLUE)
            d.text((x+27,130),str(i+1),font=font(23,True),fill=WHITE)
            centre_lines(d,(x+7,165,x+cell-7,274),label,font(30,True))
            if i<n-1:
                cx=x+cell+gap//2
                d.line((cx-9,194,cx+9,194),fill=BLUE,width=5)
                d.polygon([(cx+9,194),(cx-2,185),(cx-2,203)],fill=BLUE)
    elif kind=='split':
        for i,label in enumerate(labels):
            x=55+i*625
            d.rounded_rectangle((x,108,x+586,291),radius=18,fill=(232,239,245) if i==0 else (240,244,248),outline=BLUE,width=3)
            d.text((x+20,126),'A' if i==0 else 'B',font=font(29,True),fill=BLUE)
            centre_lines(d,(x+25,160,x+561,285),label,font(32,True))
        d.text((640,183),'vs',font=font(27,True),fill=NAVY,anchor='mm')
    else:
        vals=[]
        for label in labels:
            name,count=label.rsplit(':',1);vals.append((name,int(count)))
        max_v=max(v for _,v in vals)
        n=len(vals); gap=20; width=(1180-(n-1)*gap)//n
        for i,(name,value) in enumerate(vals):
            x=70+i*(width+gap)
            bar_height=round(125*value/max_v)
            d.rounded_rectangle((x,258-bar_height,x+width-12,258),radius=7,fill=[BLUE,(112,146,173),(172,190,205),(203,217,227)][i%4])
            d.text((x+width//2-6,267),name,font=font(21 if n>=7 else 26),fill=INK,anchor='mt')
            d.text((x+(width-12)//2,249-bar_height),str(value),font=font(27,True),fill=NAVY,anchor='mb')
        d.line((55,259,1270,259),fill=NAVY,width=3)
        d.text((70,320),'Count from the stated example; not a runtime measurement',font=font(22),fill=INK)
    image.save(path)
    return path
