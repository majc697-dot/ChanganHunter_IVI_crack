# -*- coding: utf-8 -*-
import zipfile, re, struct
APK = r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk"
z = zipfile.ZipFile(APK)
def read_uleb(data, off):
    r=0; s=0
    while True:
        b=data[off]; off+=1; r|=(b&0x7f)<<s
        if not b&0x80: break
        s+=7
    return r,off
def parse(data):
    ns=struct.unpack_from('<I',data,0x38)[0]; os_=struct.unpack_from('<I',data,0x3c)[0]
    strs=[]
    for i in range(ns):
        so=struct.unpack_from('<I',data,os_+i*4)[0]
        _,p=read_uleb(data,so); e=data.index(b'\x00',p)
        strs.append(data[p:e].decode('utf-8','replace'))
    nt=struct.unpack_from('<I',data,0x40)[0]; ot=struct.unpack_from('<I',data,0x44)[0]
    types=[]
    for i in range(nt):
        idx=struct.unpack_from('<I',data,ot+i*4)[0]
        if idx<len(strs): types.append(strs[idx])
    return strs, types

pat = re.compile(r'(?i)(Controller|AllApp|AppList|Apps|Installer|Package)')
allhits=set()
for name in sorted(n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex', n)):
    strs, types = parse(z.read(name))
    hits = {t for t in types if pat.search(t) and ('autoai' in t or 'bon/' in t) and 'databinding' not in t}
    for h in sorted(hits):
        print(name, h)
