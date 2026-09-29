# -*- coding: utf-8 -*-
import zipfile, re, struct
APK = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
z = zipfile.ZipFile(APK)
def read_uleb(d,o):
    r=0;s=0
    while True:
        b=d[o];o+=1;r|=(b&0x7f)<<s
        if not b&0x80: break
        s+=7
    return r,o
def parse(d):
    ns=struct.unpack_from('<I',d,0x38)[0];os_=struct.unpack_from('<I',d,0x3c)[0]
    st=[]
    for i in range(ns):
        so=struct.unpack_from('<I',d,os_+i*4)[0]
        _,p=read_uleb(d,so);e=d.index(b'\x00',p)
        st.append(d[p:e].decode('utf-8','replace'))
    nt=struct.unpack_from('<I',d,0x40)[0];ot=struct.unpack_from('<I',d,0x44)[0]
    ty=[]
    for i in range(nt):
        idx=struct.unpack_from('<I',d,ot+i*4)[0]
        if idx<len(st): ty.append(st[idx])
    return st,ty
d=z.read('classes5.dex')
st,ty=parse(d)
print("===== home package classes =====")
for t in sorted(ty):
    if 'autoai/project/home' in t and '$' not in t:
        print(t)
print("\n===== key strings =====")
for s in st:
    if re.search(r'(?i)(allapp|isAllApps|installApp|queryInstall|getAppList|appList|all_apps|allapps|drawer_state|apps_view|APPS_VIEW|workspace\.screen|default_workspace)', s) and len(s)<120:
        print(s)
