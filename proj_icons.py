# -*- coding: utf-8 -*-
from PIL import Image

def clusters(path, tag):
    im = Image.open(path).convert("L")
    cols = []
    for x in range(1350, 1920):
        c = sum(1 for y in range(8, 70) if im.getpixel((x, y)) > 150)
        cols.append(c)
    # cluster runs with c>2
    runs = []
    start = None
    for i, c in enumerate(cols):
        if c > 2 and start is None:
            start = i
        elif c <= 2 and start is not None:
            if i - start >= 6:
                runs.append((1350+start, 1350+i))
            start = None
    if start is not None:
        runs.append((1350+start, 1350+len(cols)))
    print(tag, runs)

clusters(r"c:\Users\24920\Documents\trae_projects\MT8666\fx_next_00.png", "nav-ON  fx_next_00")
clusters(r"c:\Users\24920\Documents\trae_projects\MT8666\study\f_study\f_000.png", "nav-OFF study_000")
