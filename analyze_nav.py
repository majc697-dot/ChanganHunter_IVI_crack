# -*- coding: utf-8 -*-
import cv2, numpy as np

path = r"c:\Users\24920\Documents\trae_projects\MT8666\study_nav.mp4"
cap = cv2.VideoCapture(path)
fps = cap.get(cv2.CAP_PROP_FPS); n=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
W=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); H=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("fps",fps,"frames",n,W,H)
sx,sy=W/1920,H/720
def crop(g,box):
    l,t,r,b=box
    return g[int(t*sy):int(b*sy), int(l*sx):int(r*sx)]
ROIS = {
 "topPlane": (1635,8,1695,70),      # status bar paper plane
 "dockNav" : (0,20,120,155),        # left dock nav button
 "turnCard": (140,100,600,310),     # top-left maneuver card
 "rtBtn"   : (1780,130,1890,260),   # top-right round red button
}
data={k:[] for k in ROIS}
prev={}
diff={k:[] for k in ROIS}
while True:
    ok,fr=cap.read()
    if not ok: break
    g=cv2.cvtColor(fr,cv2.COLOR_BGR2GRAY)
    for k,b in ROIS.items():
        c=crop(g,b).astype(np.float32)
        data[k].append(c.mean())
        if k in prev:
            diff[k].append(np.abs(c-prev[k]).mean())
        else:
            diff[k].append(0.0)
        prev[k]=c
for k in data: data[k]=np.array(data[k]); diff[k]=np.array(diff[k])

events={6.0:"NEXT",10.0:"PREV",14.0:"NEXT"}
# print 0.1s resolution diff spikes grouped per ROI around events
for k in ROIS:
    print(f"\n== {k}: mean={data[k].mean():.1f} ==")
    line=""
    for fi in range(0,n,int(round(fps*0.25))):
        t=fi/fps
        d=diff[k][fi:fi+int(fps*0.25)].mean()
        mark=""
        for et,en in events.items():
            if abs(t-et)<0.3: mark=en
        line += f"{t:4.1f}:{d:4.1f}{mark} "
    print(line)
