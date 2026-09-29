# -*- coding: utf-8 -*-
import zipfile, re, struct, sys
APK = sys.argv[1]
z = zipfile.ZipFile(APK)
def read_uleb(d,o):
    r=0;s=0
    while True:
        b=d[o];o+=1;r|=(b&0x7f)<<s
        if not b&0x80: break
        s+=7
    return r,o
pat = re.compile(sys.argv[2], re.I)
seen=set()
for name in sorted(n for n in z.namelist() if re.fullmatch(r'classes\d*\.dex', n)):
    d=z.read(name)
    ns=struct.unpack_from('<I',d,0x38)[0];os_=struct.unpack_from('<I',d,0x3c)[0]
    for i in range(ns):
        so=struct.unpack_from('<I',d,os_+i*4)[0]
        _,p=read_uleb(d,so);e=d.index(b'\x00',p)
        s=d[p:e].decode('utf-8','replace')
        if pat.search(s) and s not in seen and len(s)<160:
            seen.add(s); print(name, repr(s))
