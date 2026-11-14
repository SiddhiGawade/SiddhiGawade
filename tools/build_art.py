"""Rebuild the original pixel artwork. Run with Python 3 and Pillow."""
from pathlib import Path
import math
import random
from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parents[1] / "assets"
OUT.mkdir(exist_ok=True)
# Hand-set bitmap alphabet, drawn on the same grid as the illustrations.
ROWS = {
'A':'01110 10001 10001 11111 10001 10001 10001','B':'11110 10001 10001 11110 10001 10001 11110','C':'01111 10000 10000 10000 10000 10000 01111','D':'11110 10001 10001 10001 10001 10001 11110','E':'11111 10000 10000 11110 10000 10000 11111','F':'11111 10000 10000 11110 10000 10000 10000','G':'01111 10000 10000 10111 10001 10001 01111','H':'10001 10001 10001 11111 10001 10001 10001','I':'111 010 010 010 010 010 111','J':'00111 00010 00010 00010 00010 10010 01100','K':'10001 10010 10100 11000 10100 10010 10001','L':'10000 10000 10000 10000 10000 10000 11111','M':'10001 11011 10101 10101 10001 10001 10001','N':'10001 11001 11001 10101 10011 10011 10001','O':'01110 10001 10001 10001 10001 10001 01110','P':'11110 10001 10001 11110 10000 10000 10000','Q':'01110 10001 10001 10001 10101 10010 01101','R':'11110 10001 10001 11110 10100 10010 10001','S':'01111 10000 10000 01110 00001 00001 11110','T':'11111 00100 00100 00100 00100 00100 00100','U':'10001 10001 10001 10001 10001 10001 01110','V':'10001 10001 10001 10001 10001 01010 00100','W':'10001 10001 10001 10101 10101 11011 10001','X':'10001 10001 01010 00100 01010 10001 10001','Y':'10001 10001 01010 00100 00100 00100 00100','Z':'11111 00001 00010 00100 01000 10000 11111',' ':'000 000 000 000 000 000 000','0':'01110 10011 10101 10101 10101 11001 01110','1':'010 110 010 010 010 010 111','2':'01110 10001 00001 00010 00100 01000 11111','6':'01110 10000 10000 11110 10001 10001 01110','/':'00001 00010 00010 00100 01000 01000 10000','.':'0 0 0 0 0 1 1','-':'000 000 000 111 000 000 000'}

def label(d, xy, words, size, color):
    x,y = xy
    for ch in words.upper():
        rows=ROWS[ch].split()
        for j,row in enumerate(rows):
            for i,bit in enumerate(row):
                if bit=='1':
                    xx,yy=x+i*size,y+j*size
                    d.rectangle((xx,yy,xx+size-1,yy+size-1),fill=color)
        x+=(len(rows[0])+1)*size
    return x

def gradient(d, rect, start, end, bands=20):
    x,y,r,b=rect
    for j in range(bands):
        t=j/(bands-1)
        col=tuple(round(a+(z-a)*t) for a,z in zip(start,end))
        d.rectangle((x,y+(b-y+1)*j//bands,r,y+(b-y+1)*(j+1)//bands-1),fill=col)

def spark(d,x,y,color,rad=2):
    d.line((x-rad,y,x+rad,y),fill=color)
    d.line((x,y-rad,x,y+rad),fill=color)

def hero(t):
    im=Image.new('RGB',(480,180),'#15142e')
    d=ImageDraw.Draw(im)
    gradient(d,(0,0,479,179),(27,24,57),(44,32,68))
    for x in range(0,480,8):
        for y in range(0,180,8):
            d.point((x,y),fill='#4b395d')
    # Wide, recessed apartment window with a coastal skyline at twilight.
    d.rectangle((248,9,468,131),fill='#100f25')
    d.rectangle((251,12,465,128),fill='#65527d')
    gradient(d,(254,15,462,123),(59,57,113),(249,152,139))
    d.ellipse((392,33,431,72), fill='#ffdcaa')
    for y in (57,62,67):
        d.line((392,y,431,y),fill='#f6ad9f')
    rng=random.Random(45)
    for i in range(35):
        x,y=rng.randint(257,458),rng.randint(19,76)
        d.point((x,y),fill='#ffe9c8' if (i+t//4)%4 else '#d4b3cc')
    for x,y,w in [(257,54,47),(327,31,38),(385,77,13),(415,45,32),(273,71,38)]:
        drift=t//12
        d.line((x+drift,y,x+w+drift,y),fill='#c390ab',width=2)
        d.line((x+6+drift,y-2,x+w-8+drift,y-2),fill='#c390ab')
    for base,shade,lo,hi in [(102,'#866b99',9,30),(111,'#5b507d',8,36),(120,'#373956',9,26)]:
        x=254
        while x<463:
            w,h=rng.randint(4,12),rng.randint(lo,hi)
            r=min(x+w,462)
            d.rectangle((x,base-h,r,base),fill=shade)
            if w>7 and x+5<462:d.rectangle((x+2,base-h-2,x+5,base-h),fill=shade)
            for yy in range(base-h+3,base-1,4):
                for xx in range(x+2,r-1,4):
                    if rng.random()<.38:d.line((xx,yy,xx+1,yy), fill='#eeb794')
            x+=w+1
    d.rectangle((254,116,462,123),fill='#5c608c')
    for i in range(24):
        x=rng.randrange(254,456);y=rng.randrange(117,124)
        d.line((x,y,min(462,x+rng.randrange(2,7)),y),fill='#b78f9e')
    # Cable-stayed bridge silhouette across the bay.
    for x in (292,316):
        d.rectangle((x,91,x+1,117),fill='#464367')
        for off in (5,9,12):
            d.line((x,92,x-off,110),fill='#675b7f');d.line((x+1,92,x+off,110),fill='#675b7f')
    d.line((255,110,339,110),fill='#414160',width=2)
    for x in (321,418):
        d.rectangle((x,13,x+2,125),fill='#463a5e')
    d.rectangle((247,127,469,131),fill='#8b6680')
    # Desk, bevelled laptop, live terminal, coffee and plant.
    d.rectangle((234,147,479,153),fill='#a77882')
    d.rectangle((234,149,479,152),fill='#805673');d.rectangle((237,154,479,170),fill='#473247')
    for x in (248,454):d.rectangle((x,154,x+3,171),fill='#30263b')
    d.polygon([(288,97),(359,97),(359,100),(355,139),(283,139)],fill='#201d37')
    d.polygon([(291,100),(355,100),(351,135),(287,135)],fill='#486278')
    d.polygon([(293,103),(352,103),(348,132),(290,132)],fill='#223846')
    d.line((294,106,348,106),fill='#49827f')
    name='SIDDHI'
    n=min(len(name),(t%32)//2+1)
    end=label(d,(296,113),name[:n],1,'#b6ffe1')
    if t%10<7:d.line((end,119,end+2,119),fill='#fbc2a4')
    for x,y,w in [(296,125,12),(311,125,16),(296,128,24)]:
        d.line((x,y,x+w,y),fill='#4a8585')
    d.polygon([(282,140),(355,140),(369,146),(273,146)],fill='#afa1ad')
    d.line((279,145,359,145),fill='#cdb9b9');d.line((287,142,353,142),fill='#655b75')
    d.rectangle((372,135,380,145),fill='#e7b494');d.rectangle((380,137,383,142),outline='#d5a08a')
    for j in range(3):
        y=132-((t//2+j*3)%9);x=375+round(math.sin((y+t)/3))
        d.line((x,y,x+1,y-1),fill='#e4babe')
    # Pixel plant and a stack of sketchbooks.
    for pts,col in [([(431,134),(428,115),(419,107),(417,109),(422,122)],'#496e73'), ([(431,135),(430,107),(434,94),(437,95),(437,111)],'#71a894'), ([(432,133),(441,110),(450,107),(449,116),(441,125)],'#5d8e86'), ([(428,133),(417,123),(409,122),(412,128)],'#81ac92')]:
        d.polygon(pts,fill=col)
    d.rectangle((422,132,441,135),fill='#dd9b86');d.polygon([(424,136),(439,136),(437,146),(426,146)],fill='#ad7275')
    for y,w,c in [(146,19,'#9887aa'),(143,16,'#c89d92'),(140,17,'#8ba9a5')]:
        d.rectangle((395,y-2,395+w,y),fill=c)
    # Identity, with a two-tone offset reminiscent of screen-printed arcade marquees.
    label(d,(17,19),'SG / PLAYER ONE',1,'#a8f4d6')
    for y,word in [(40,'SIDDHI'),(78,'GAWADE')]:
        label(d,(19,y+3),word,5,'#7f517d')
        label(d,(17,y),word,5,'#ffecd6')
    label(d,(18,130),'FREELANCE FULL-STACK',1,'#e2d4e9')
    label(d,(18,143),'DEVELOPER',1,'#e2d4e9')
    d.rectangle((0,167,479,179), fill='#131626')
    for x in range(15,54,6):d.rectangle((x,172,x+3,174), fill='#9be5cb' if x<45 else '#4d6572')
    label(d,(361,170),'MUMBAI / INDIA',1,'#afacc7')
    return im.resize((960,360),Image.Resampling.NEAREST)

def cartridge(kind):
    im=Image.new('RGB',(236,92),'#24263f')
    d=ImageDraw.Draw(im)
    travel=kind=='ttb'
    dark,mid,accent=('#153a3e','#376566','#b5f0cf') if travel else ('#3c2748','#764868','#ffd1b1')
    d.rectangle((2,2,233,89),fill=dark,outline=mid)
    d.line((9,7,226,7),fill=mid)
    label(d,(11,14),'TRAVEL / SOLO BUILD' if travel else 'COMMERCE / FULL STACK',1,accent)
    if travel:
        label(d,(11,34),'TTB',3,'#fff0dc')
        label(d,(11,62),'EXPERIENCES',1,'#fff0dc')
        # Postage-stamp landscape with a stepped mountain and torii gate.
        d.rectangle((141,22,222,78), fill='#a3d2bf')
        gradient(d,(144,25,219,75),(254,199,157),(253,228,177),10)
        d.ellipse((190,29,204,43),fill='#db806c')
        d.polygon([(144,64),(162,55),(174,41),(191,58),(219,64),(219,76),(144,76)],fill='#7e9f96')
        d.polygon([(167,50),(174,41),(180,48),(176,47),(174,49),(172,47)],fill='#ffedd7')
        d.polygon([(144,67),(156,61),(175,65),(198,55),(219,60),(219,76),(144,76)],fill='#507976')
        d.rectangle((144,70,219,75),fill='#67958c')
        for x in (156,167): d.rectangle((x,58,x+2,72),fill='#493e45')
        d.rectangle((152,57,174,59),fill='#b55e51');d.line((154,62,172,62),fill='#4b4148',width=2)
    else:
        label(d,(11,36),'ELEGANCE',2,'#fff0dc')
        label(d,(11,64),'BUY / RENT',1,'#ffdbbf')
        d.rectangle((145,23,222,78),fill='#b37a84')
        d.rectangle((148,26,219,75),fill='#51354e')
        for cx in (168,198):
            d.arc((cx-4,30,cx+4,42),130,430,fill='#f7c080',width=2)
            d.line((cx,40,cx,46),fill='#f4bf80',width=2)
            outer=[(cx,44),(cx+8,55),(cx+7,60),(cx,67),(cx-7,60),(cx-8,55)]
            d.polygon(outer,fill='#e8aa7d')
            d.polygon([(cx,47),(cx+5,55),(cx+4,60),(cx,64),(cx-5,58),(cx-5,54)],fill='#ab6887')
            d.line((cx-4,54,cx,48,cx-1,58),fill='#ffd0ba');d.line((cx,61,cx+4,56),fill='#df9ca3')
        spark(d,210,34,'#ffe3bd',2)
    return im.resize((708,276),Image.Resampling.NEAREST)

def award(kind,metric,caption):
    im=Image.new('RGB',(148,62),'#202238')
    d=ImageDraw.Draw(im)
    d.rectangle((1,1,146,60),outline='#4d465d')
    gold='#f7bf7e';light='#ffe5ac';deep='#b77967'
    if kind=='trophy':
        d.rectangle((11,17,37,28),outline=gold,width=2)
        d.polygon([(15,14),(33,14),(31,29),(26,33),(22,33),(17,29)],fill=gold)
        d.rectangle((23,33,26,38),fill=deep);d.rectangle((18,38,31,40),fill=gold)
        d.line((18,17,19,25),fill=light,width=2)
    elif kind=='medal':
        d.polygon([(13,12),(20,12),(25,24),(20,27)],fill='#bd8abc')
        d.polygon([(28,12),(36,12),(28,27),(22,25)],fill='#88c1b1')
        d.ellipse((15,23,33,41),fill=deep);d.ellipse((16,23,32,39),fill=gold)
        spark(d,24,31,light,4)
    else:
        d.polygon([(8,23),(24,15),(40,23),(24,30)],fill='#9ce1cb')
        d.polygon([(15,28),(24,32),(33,28),(33,33),(24,37),(15,33)],fill='#6bb1ab')
        d.line((38,24,38,34),fill=gold,width=2)
    label(d,(47,19),metric,2,'#ffecd6')
    label(d,(11,46),caption,1,'#cfccd9')
    return im.resize((444,186),Image.Resampling.NEAREST)

if __name__=='__main__':
    frames=[hero(t) for t in range(32)]
    palette=frames[24].quantize(colors=191)
    animated=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    animated[0].save(OUT/'title.gif',save_all=True,append_images=animated[1:],duration=125,loop=0,optimize=True)
    frames[24].save(OUT/'title-still.png')
    for name in ('ttb','elegance'):
        cartridge(name).save(OUT/(name+'.png'))
    for spec in [('cap','10','B.TECH CGPA'),('trophy','TOP 60','QUASAR FINALIST'),('medal','6TH','SYNAPHACK 3.0')]:
        # The caption alone needs the digit three.
        ROWS['3']='11110 00001 00001 01110 00001 00001 11110'
        award(*spec).save(OUT/(spec[0]+'.png'))
