# -*- coding: utf-8 -*-
import zipfile, re, struct
APKS = [r"c:\Users\24920\Documents\trae_projects\MT8666\CA_Launcher.apk",
        r"c:\Users\24920\Documents\trae_projects\MT8666\P201_COMMON_APP.apk"]
def read_uleb(d,o):
    r=0;s=0
    while True:
        b=d[o];o+=1;r|=(b&0x7f)<<s
        if not b&0x80: break
        s+=7
    return r,o
import zipfile as zf
for APK in APKS:
    print("#####", APK.split("\\")[-1])
    z=zf.ZipFile(APK)
    seen=set()
    for name in sorted(n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex', n)):
        d=z.read(name)
        ns=struct.unpack_from('<I',d,0x38)[0];os_=struct.unpack_from('<I',d,0x3c)[0]
        for i in range(ns):
            so=struct.unpack_from('<I',d,os_+i*4)[0]
            _,p=read_uleb(d,so);e=d.index(b'\x00',p)
            t=d[p:e].decode('utf-8','replace')
            if ('/rpc/' in t and ('manager/' in t or 'RpcService' in t or 'Connect' in t or 'Service' in t)) and '$' not in t and '[' not in t and t not in seen:
                seen.add(t); print(name, t)
