# -*- coding: utf-8 -*-
import cv2, numpy as np

path = r"c:\Users\24920\Documents\trae_projects\MT8666\study2.mp4"
cap = cv2.VideoCapture(path)
fps = cap.get(cv2.CAP_PROP_FPS)
n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("fps", fps, "frames", n, "size", W, H)
sx, sy = W/1920.0, H/720.0
def roi(box):
    l,t,r,b = box
    return (int(l*sx),int(t*sy),int(r*sx),int(b*sy))
TOP = roi((1635,8,1695,70))
LEFT = roi((0,20,120,155))

t_vals=[]; l_vals=[]
idx=0
while True:
    ok, fr = cap.read()
    if not ok: break
    g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    x1,y1,x2,y2 = TOP
    t_vals.append(g[y1:y2, x1:x2].mean())
    x1,y1,x2,y2 = LEFT
    l = g[y1:y2, x1:x2]
    l_vals.append((l>150).mean())
    idx+=1
t_vals=np.array(t_vals); l_vals=np.array(l_vals)

def stats(a,b,name,thr_lo,thr_hi,vals):
    seg = vals[int(a*fps):int(b*fps)]
    on = seg > thr_hi
    # count rising edges
    edges = int(np.sum((~on[:-1]) & (on[1:])))
    print(f"{name:12s} {a:4.1f}-{b:4.1f}s  mean={seg.mean():7.2f} min={seg.min():7.2f} max={seg.max():7.2f} onfrac={on.mean():.2f} blinks(rises)={edges}")

print("\n--- top plane mean brightness ---")
for a,b,nm in [(0,10,"idle0-10"),(11.5,13.2,"evt1"),(14.5,16.2,"evt2"),(17.5,19.2,"evt3"),(19.5,22,"post")]:
    stats(a,b,nm,0,0,t_vals)
print("\n--- left button bright fraction ---")
for a,b,nm in [(0,10,"idle0-10"),(11.5,13.2,"evt1"),(14.5,16.2,"evt2"),(17.5,19.2,"evt3"),(19.5,22,"post")]:
    stats(a,b,nm,0.15,0.15,l_vals)

# dump per-0.5s averaged series
print("\ntime  topMean  leftOn")
for k in range(0, len(t_vals), int(fps*0.5)):
    t = k/fps
    print(f"{t:5.1f}  {t_vals[k:k+int(fps*0.5)].mean():6.1f}  {l_vals[k:k+int(fps*0.5)].mean():.2f}")
