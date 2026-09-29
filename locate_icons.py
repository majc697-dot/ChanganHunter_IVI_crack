# -*- coding: utf-8 -*-
from PIL import Image
im = Image.open(r"c:\Users\24920\Documents\trae_projects\MT8666\study\f_study\f_000.png").convert("L")
w,h = im.size
print("size", w, h)
# scan top 80 rows: columns with bright pixels (icons are white on dark bar)
for y0 in (0, 20, 40, 60):
    row_ranges = []
    for y in range(y0, min(y0+20,h)):
        xs = [x for x in range(w) if im.getpixel((x,y)) > 150]
        if xs:
            row_ranges.append((y, min(xs), max(xs), len(xs)))
    # summarize clusters
    print("yband", y0, row_ranges[:6])
# left dock: x 0..140, bright pixel y distribution
ys = {}
for y in range(0, 200):
    c = sum(1 for x in range(0,140) if im.getpixel((x,y))>150)
    if c > 20: ys[y]=c
print("left bright rows:", list(ys.items())[:20])
