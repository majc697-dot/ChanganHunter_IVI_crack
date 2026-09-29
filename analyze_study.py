# -*- coding: utf-8 -*-
import glob, os
from PIL import Image

d = r"c:\Users\24920\Documents\trae_projects\MT8666\study\f_study"
files = sorted(glob.glob(os.path.join(d, "f_*.png")))

# ROIs in 1920x720: (l,t,r,b)
TOP = (1635, 8, 1695, 70)      # status-bar nav paper-plane (icons reflow when gone)
LEFT = (0, 20, 120, 155)       # dock nav button

def metrics(im):
    px = im.convert("L")
    t = px.crop(TOP); l = px.crop(LEFT)
    th = sum(1 for p in t.getdata() if p > 150) / (t.width*t.height)
    lh = sum(1 for p in l.getdata() if p > 150) / (l.width*l.height)
    return th, lh

events = {44:'NEXT', 56:'NEXT', 68:'NEXT'}
rows = []
for f in files:
    i = int(os.path.basename(f)[2:5])
    th, lh = metrics(Image.open(f))
    rows.append((i, th, lh))
# compact timeline: T=top plane present, L=left button highlighted
print("frame:  T(top nav plane)  L(dock button)")
for i, th, lh in rows:
    t = '1' if th > 0.02 else '.'
    l = '1' if lh > 0.15 else '.'
    mark = ' <=NEXT' if i in events else ''
    print(f"{i:3d}  {t}  {l}   top={th:.3f} left={lh:.3f}{mark}")
